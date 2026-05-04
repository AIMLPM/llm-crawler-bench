#!/usr/bin/env python3
"""Crawlee worker — runs in a subprocess so each invocation gets a fresh event loop.

Usage: python crawlee_worker.py <url> <out_dir> <max_pages> [url1 url2 ...]

Each call avoids the asyncio.Lock/event-loop mismatch that occurs when crawlee
is invoked multiple times in the same process (Python 3.13 regression in
crawlee's storage client).

Tuning effort applied (see reports/METHODOLOGY.md "Crawler tuning"):
  - --disable-blink-features=AutomationControlled chromium flag removes the
    navigator.webdriver=true signal that JS-side bot detectors check first.
  - Browser-like User-Agent (Chrome on macOS) + 1920x1080 viewport + en-US
    locale, via browser_new_context_options. Reduces fingerprint divergence
    from a real session.
  - Sec-Ch-Ua / Accept-Language / Upgrade-Insecure-Requests extra HTTP
    headers via context. Same set as scrapy_runner / colly main.go for
    apples-to-apples comparison across crawlers.
  Doesn't promise to defeat aggressive anti-bot like newegg's, but raises
  the floor so the gap reflects crawler design rather than missing config.
"""
import asyncio
import json
import os
import sys

url = sys.argv[1]
out_dir = sys.argv[2]
max_pages = int(sys.argv[3])
url_list = sys.argv[4:] if len(sys.argv) > 4 else [url]

os.makedirs(out_dir, exist_ok=True)
pages_saved = 0
jsonl_path = os.path.join(out_dir, "pages.jsonl")


async def _run():
    global pages_saved
    from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext
    from markdownify import markdownify as md

    # Browser-like UA + headers, mirroring scrapy_runner + colly main.go so
    # all three HTTP/browser tools present the same fingerprint surface.
    browser_ua = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    )
    extra_http_headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Ch-Ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"macOS"',
        "Upgrade-Insecure-Requests": "1",
    }

    # Stealth chromium flags: AutomationControlled removal is the single highest-
    # value flag — it strips navigator.webdriver=true, which is the first thing
    # JS-side bot detection scripts (Cloudflare bot management, DataDome, PerimeterX)
    # check.
    chromium_args = ["--disable-blink-features=AutomationControlled"]
    launch_options = {"args": chromium_args}
    if os.getuid() == 0 or os.path.exists("/.dockerenv"):
        launch_options["args"] = chromium_args + ["--no-sandbox", "--disable-setuid-sandbox"]

    crawler = PlaywrightCrawler(
        max_requests_per_crawl=max_pages,
        headless=True,
        browser_launch_options=launch_options,
        browser_new_context_options={
            "user_agent": browser_ua,
            "viewport": {"width": 1920, "height": 1080},
            "locale": "en-US",
            "extra_http_headers": extra_http_headers,
        },
    )

    @crawler.router.default_handler
    async def handler(context: PlaywrightCrawlingContext) -> None:
        global pages_saved
        if pages_saved >= max_pages:
            return
        page_url = context.request.url
        title = await context.page.title()
        content = await context.page.content()
        markdown = md(
            content,
            heading_style="ATX",
            strip=["img", "script", "style", "nav", "footer"],
        )
        if len(markdown.split()) < 5:
            return
        safe_name = page_url.replace("://", "_").replace("/", "_")[:80]
        with open(
            os.path.join(out_dir, f"{safe_name}.md"), "w", encoding="utf-8"
        ) as f:
            f.write(markdown)
        with open(jsonl_path, "a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {"url": page_url, "title": title, "text": markdown},
                    ensure_ascii=False,
                )
                + "\n"
            )
        pages_saved += 1
        if len(url_list) == 1 and url_list[0] == url:
            await context.enqueue_links()

    try:
        await crawler.run(url_list[:max_pages])
    except Exception as e:
        print(f"crawlee error: {e}", file=sys.stderr)


try:
    asyncio.run(_run())
except Exception as e:
    print(f"crawlee fatal error: {e}", file=sys.stderr)
print(pages_saved)
