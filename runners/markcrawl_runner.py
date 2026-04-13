"""MarkCrawl runner — httpx async + BeautifulSoup + markdownify.

Tested with: markcrawl >= 0.1.0
"""
from __future__ import annotations

import os
from typing import List, Optional


def check() -> bool:
    try:
        from markcrawl.core import crawl  # noqa: F401
        return True
    except ImportError:
        return False


def _run_async(url_list: List[str], out_dir: str, concurrency: int) -> int:
    """Fetch url_list concurrently using AsyncCrawlEngine + process pool."""
    import asyncio

    from markcrawl.core import AsyncCrawlEngine, _extract_content_worker
    from markcrawl.fetch import fetch_async

    async def _go() -> int:
        engine = AsyncCrawlEngine(
            out_dir=out_dir, fmt="markdown", min_words=5, delay=0,
            timeout=15, concurrency=concurrency, include_subdomains=False,
            user_agent=None, proxy=None, show_progress=False,
        )
        sem = asyncio.Semaphore(concurrency)
        jsonl_path = os.path.join(out_dir, "pages.jsonl")
        loop = asyncio.get_running_loop()

        async def _fetch_and_extract(page_url: str):
            async with sem:
                resp = await fetch_async(engine.session, page_url, engine.timeout)
            if not resp or not getattr(resp, "is_success", getattr(resp, "ok", False)):
                return None
            ct = resp.headers.get("content-type", "").lower()
            if "text/html" not in ct:
                return None
            html_text = resp.text
            # Offload CPU-bound extraction to process pool
            if engine._executor:
                result = await loop.run_in_executor(
                    engine._executor,
                    _extract_content_worker, html_text, page_url, "markdown", "default",
                )
            else:
                result = _extract_content_worker(html_text, page_url, "markdown", "default")
            if result is None:
                return None
            title, content, links = result
            return {"url": page_url, "title": title, "content": content, "links": links}

        with open(jsonl_path, "w", encoding="utf-8") as jsonl_file:
            # Launch all fetches; semaphore handles concurrency
            tasks = [
                asyncio.create_task(_fetch_and_extract(u))
                for u in url_list
            ]
            for coro in asyncio.as_completed(tasks):
                try:
                    page_data = await coro
                except Exception:
                    continue
                if page_data:
                    engine.save_page(page_data, jsonl_file)

        await engine.close()
        return engine.saved_count

    return asyncio.run(_go())


def _run_sync(url_list: List[str], out_dir: str, concurrency: int) -> int:
    """Fallback: fetch url_list sequentially using CrawlEngine."""
    from markcrawl.core import CrawlEngine

    engine = CrawlEngine(
        out_dir=out_dir, fmt="markdown", min_words=5, delay=0,
        timeout=15, concurrency=concurrency, include_subdomains=False,
        user_agent=None, render_js=False, proxy=None, show_progress=False,
    )
    jsonl_path = os.path.join(out_dir, "pages.jsonl")
    with open(jsonl_path, "w", encoding="utf-8") as jsonl_file:
        for page_url in url_list:
            resp = engine.fetch_page(page_url)
            page_data = engine.process_response(page_url, resp)
            if page_data:
                engine.save_page(page_data, jsonl_file)
    engine.close()
    return engine.saved_count


def run(url: str, out_dir: str, max_pages: int, url_list: Optional[List[str]] = None, concurrency: int = 1, **kwargs) -> int:
    """Run MarkCrawl and return pages saved."""
    from markcrawl.core import crawl

    if url_list:
        os.makedirs(out_dir, exist_ok=True)
        try:
            from markcrawl.core import AsyncCrawlEngine  # noqa: F401
            return _run_async(url_list, out_dir, concurrency)
        except ImportError:
            return _run_sync(url_list, out_dir, concurrency)
    else:
        result = crawl(
            base_url=url,
            out_dir=out_dir,
            fmt="markdown",
            max_pages=max_pages,
            delay=0,
            timeout=15,
            show_progress=False,
            min_words=5,
            concurrency=concurrency,
        )
        return result.pages_saved
