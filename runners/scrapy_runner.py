"""Scrapy + markdownify runner — async HTTP crawling with Scrapy framework.

Tested with: scrapy (unpinned), markdownify (unpinned)

Tuning effort applied (see reports/METHODOLOGY.md "Crawler tuning"):
  - Browser-like User-Agent + full Sec-Ch-Ua / Accept / Sec-Fetch-* headers,
    mirroring the colly+md WAF-bypass fix (commit 06501ac). Same intent: don't
    let modern WAFs reject us purely on default-UA fingerprint. Doesn't help
    JS-rendered SPAs (still HTTP-only) but fixes UA-only blocks on sites like
    newegg / postgres-docs / kubernetes-docs.
  - Subprocess timeout bumped from 300s -> 600s to align with the wrapper's
    heartbeat-stall budget. Exception caught so partial output is preserved.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import List, Optional

# Browser-like UA + headers, kept identical across HTTP-only crawlers
# (colly+md, scrapy+md) so the apples-to-apples comparison reflects crawler
# behavior, not header-tuning advantage. See METHODOLOGY.md "Crawler tuning".
_BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)
_BROWSER_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Ch-Ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Upgrade-Insecure-Requests": "1",
}


def check() -> bool:
    try:
        import markdownify  # noqa: F401
        import scrapy  # noqa: F401
        return True
    except ImportError:
        return False


def run(url: str, out_dir: str, max_pages: int, url_list: Optional[List[str]] = None, concurrency: int = 1, **kwargs) -> int:
    """Run Scrapy with markdownify pipeline via subprocess."""
    os.makedirs(out_dir, exist_ok=True)

    ua_repr = repr(_BROWSER_UA)
    headers_repr = repr(_BROWSER_HEADERS)

    if url_list:
        url_list_json = json.dumps(url_list)
        spider_code = f'''
import json
import os
import scrapy
from markdownify import markdownify as md
from scrapy.crawler import CrawlerProcess

class BenchSpider(scrapy.Spider):
    name = "bench"
    start_urls = {url_list_json}
    custom_settings = {{
        "LOG_LEVEL": "ERROR",
        "ROBOTSTXT_OBEY": True,
        "CONCURRENT_REQUESTS": {concurrency},
        "DOWNLOAD_DELAY": 0,
        "USER_AGENT": {ua_repr},
        "DEFAULT_REQUEST_HEADERS": {headers_repr},
    }}

    def parse(self, response):
        body = response.css("main").get() or response.css("body").get() or response.text
        markdown = md(body, heading_style="ATX", strip=["img", "script", "style", "nav", "footer"])
        title = response.css("title::text").get() or ""
        if len(markdown.split()) < 5:
            return
        safe_name = response.url.replace("://", "_").replace("/", "_")[:80]
        md_path = os.path.join("{out_dir}", f"{{safe_name}}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        jsonl_path = os.path.join("{out_dir}", "pages.jsonl")
        with open(jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({{
                "url": response.url,
                "title": title.strip(),
                "text": markdown,
            }}, ensure_ascii=False) + "\\n")

process = CrawlerProcess()
process.crawl(BenchSpider)
process.start()
'''
    else:
        spider_code = f'''
import json
import os
import scrapy
from markdownify import markdownify as md
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse

class BenchSpider(scrapy.Spider):
    name = "bench"
    start_urls = ["{url}"]
    custom_settings = {{
        "LOG_LEVEL": "ERROR",
        "ROBOTSTXT_OBEY": True,
        "CONCURRENT_REQUESTS": {concurrency},
        "DOWNLOAD_DELAY": 0,
        "CLOSESPIDER_PAGECOUNT": {max_pages},
        "USER_AGENT": {ua_repr},
        "DEFAULT_REQUEST_HEADERS": {headers_repr},
    }}
    pages_saved = 0

    def parse(self, response):
        if self.pages_saved >= {max_pages}:
            return
        body = response.css("main").get() or response.css("body").get() or response.text
        markdown = md(body, heading_style="ATX", strip=["img", "script", "style", "nav", "footer"])
        title = response.css("title::text").get() or ""
        if len(markdown.split()) < 5:
            return
        safe_name = response.url.replace("://", "_").replace("/", "_")[:80]
        md_path = os.path.join("{out_dir}", f"{{safe_name}}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        jsonl_path = os.path.join("{out_dir}", "pages.jsonl")
        with open(jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({{
                "url": response.url,
                "title": title.strip(),
                "text": markdown,
            }}, ensure_ascii=False) + "\\n")
        self.pages_saved += 1
        base_domain = urlparse("{url}").netloc
        for href in response.css("a::attr(href)").getall():
            full_url = response.urljoin(href)
            if urlparse(full_url).netloc == base_domain:
                yield scrapy.Request(full_url, callback=self.parse)

process = CrawlerProcess()
process.crawl(BenchSpider)
process.start()
'''

    spider_file = os.path.join(out_dir, "_spider.py")
    with open(spider_file, "w") as f:
        f.write(spider_code)

    # Subprocess timeout 300s -> 600s aligns with wrapper heartbeat-stall budget.
    # Caught so partial pages.jsonl on disk is still counted on timeout.
    try:
        subprocess.run(
            [sys.executable, spider_file],
            capture_output=True,
            timeout=600,
            check=False,
        )
    except subprocess.TimeoutExpired:
        pass

    jsonl_path = os.path.join(out_dir, "pages.jsonl")
    if os.path.isfile(jsonl_path):
        with open(jsonl_path) as f:
            return sum(1 for line in f if line.strip())
    return 0
