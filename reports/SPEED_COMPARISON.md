# Speed Comparison
<!-- style: v2, 2026-04-12 -->

markcrawl is the fastest crawler at 14.0 pages/sec overall, 50% faster than
the runner-up scrapy+md (9.3 p/s). The async httpx engine in v0.2.0 is the
main driver — pure HTTP tools dominate, while browser-based tools (crawl4ai,
crawlee, playwright) are 3-7x slower.

**Run:** `run_20260412_195003` | **Sites:** 8 | **Tools:** 7 | **Iterations:** 3 (median reported)

## Summary

| Tool | Engine | Total pages | Total time (s) | Pages/sec | JS rendering |
|------|--------|-------------|----------------|-----------|-------------|
| **markcrawl** | **async httpx** | **1456** | **103.9** | **14.0** | **Optional** |
| scrapy+md | Scrapy async | 1284 | 138.8 | 9.3 | No |
| colly+md | Go (Colly) | 1376 | 209.3 | 6.6 | No |
| playwright | Playwright | 1448 | 692.8 | 2.1 | Yes |
| crawl4ai | Playwright | 1456 | 716.4 | 2.0 | Yes |
| crawlee | Playwright | 1456 | 806.2 | 1.8 | Yes |
| crawl4ai-raw | Playwright | 1456 | 1027.5 | 1.4 | Yes |

The speed gap is driven by engine choice: plain HTTP tools (markcrawl, scrapy,
colly) skip browser overhead entirely. Browser-based tools (crawl4ai, crawlee,
playwright) launch Chromium per page, which adds 200-500ms of overhead.

Note: scrapy+md fetched fewer pages (1284 vs 1456) due to timeouts on
python-docs. Higher word counts don't mean higher quality — see
[QUALITY_COMPARISON.md](QUALITY_COMPARISON.md).

## Per-Site Breakdown

### quotes-toscrape (15 pages) — Simple paginated HTML

| Tool | Pages | Time (s) | Std dev | Pages/sec |
|------|-------|----------|---------|-----------|
| **markcrawl** | **15** | **3.6** | **0.6** | **4.2** |
| colly+md | 15 | 4.0 | 0.5 | 3.8 |
| scrapy+md | 15 | 4.7 | 0.1 | 3.2 |
| crawl4ai | 15 | 5.0 | 0.1 | 3.0 |
| playwright | 15 | 5.1 | 0.0 | 3.0 |
| crawlee | 15 | 6.8 | 0.4 | 2.2 |
| crawl4ai-raw | 15 | 9.6 | 0.4 | 1.6 |

### books-toscrape (60 pages) — E-commerce catalog

| Tool | Pages | Time (s) | Std dev | Pages/sec |
|------|-------|----------|---------|-----------|
| **markcrawl** | **60** | **4.2** | **0.6** | **14.3** |
| scrapy+md | 60 | 4.9 | 0.2 | 12.3 |
| colly+md | 60 | 6.5 | 0.0 | 9.2 |
| crawl4ai | 60 | 11.4 | 0.5 | 5.3 |
| crawlee | 60 | 16.6 | 0.1 | 3.6 |
| crawl4ai-raw | 60 | 27.7 | 1.1 | 2.2 |
| playwright | 60 | 35.1 | 12.2 | 1.8 |

### fastapi-docs (153 pages) — API documentation

| Tool | Pages | Time (s) | Std dev | Pages/sec |
|------|-------|----------|---------|-----------|
| **markcrawl** | **153** | **11.4** | **0.3** | **13.4** |
| colly+md | 153 | 27.1 | 1.5 | 5.6 |
| scrapy+md | 153 | 29.6 | 0.6 | 5.2 |
| playwright | 153 | 86.3 | 1.0 | 1.8 |
| crawl4ai | 153 | 90.4 | 13.8 | 1.7 |
| crawlee | 153 | 128.1 | 6.7 | 1.2 |
| crawl4ai-raw | 153 | 139.8 | 7.4 | 1.1 |

### python-docs (500 pages) — Standard library reference

| Tool | Pages | Time (s) | Std dev | Pages/sec |
|------|-------|----------|---------|-----------|
| **markcrawl** | **500** | **22.1** | **2.3** | **22.7** |
| colly+md | 500 | 43.6 | 4.1 | 11.5 |
| scrapy+md | 328 | 37.6 | 0.5 | 8.7 |
| crawlee | 500 | 74.4 | 2.8 | 6.7 |
| playwright | 500 | 121.1 | 38.5 | 4.4 |
| crawl4ai | 500 | 131.0 | 27.3 | 3.9 |
| crawl4ai-raw | 500 | 187.6 | 3.7 | 2.7 |

scrapy+md only fetched 328 of 500 pages due to timeouts.

### react-dev (221 pages) — SPA, JS-rendered

| Tool | Pages | Time (s) | Std dev | Pages/sec |
|------|-------|----------|---------|-----------|
| **markcrawl** | **221** | **8.4** | **0.6** | **26.3** |
| scrapy+md | 221 | 22.9 | 0.6 | 9.6 |
| colly+md | 221 | 32.3 | 4.2 | 6.9 |
| playwright | 221 | 59.7 | 0.1 | 3.7 |
| crawlee | 221 | 76.8 | 5.3 | 2.9 |
| crawl4ai | 221 | 109.7 | 4.7 | 2.0 |
| crawl4ai-raw | 221 | 123.1 | 4.4 | 1.8 |

markcrawl does not use JS rendering here — it fetches the server-rendered HTML.
Tools with lower word counts may miss JS-only content. See
[QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) for content completeness.

### wikipedia-python (50 pages) — Tables, infoboxes, citations

| Tool | Pages | Time (s) | Std dev | Pages/sec |
|------|-------|----------|---------|-----------|
| **markcrawl** | **50** | **6.7** | **0.2** | **7.5** |
| scrapy+md | 50 | 8.2 | 1.8 | 6.3 |
| colly+md | 50 | 9.0 | 0.5 | 5.6 |
| playwright | 42 | 12.2 | 0.1 | 3.5 |
| crawlee | 50 | 17.0 | 1.6 | 3.0 |
| crawl4ai-raw | 50 | 29.5 | 0.7 | 1.7 |
| crawl4ai | 50 | 41.7 | 10.4 | 1.2 |

playwright only fetched 42 of 50 pages.

### stripe-docs (257 pages) — Tabbed content, code samples

| Tool | Pages | Time (s) | Std dev | Pages/sec |
|------|-------|----------|---------|-----------|
| scrapy+md | 257 | 24.2 | 1.0 | 10.6 |
| **markcrawl** | **257** | **35.7** | **1.0** | **7.2** |
| colly+md | 254 | 58.0 | 9.7 | 4.4 |
| crawl4ai | 257 | 268.5 | 35.5 | 1.0 |
| playwright | 257 | 333.2 | 41.3 | 0.8 |
| crawlee | 257 | 413.2 | 90.0 | 0.6 |
| crawl4ai-raw | 257 | 423.1 | 8.3 | 0.6 |

scrapy+md is faster than markcrawl on stripe-docs (10.6 vs 7.2 p/s). Stripe's
heavy JS-rendered content slows all browser-based tools significantly. colly+md
missed 3 pages.

### blog-engineering (200 pages) — GitHub Engineering Blog

| Tool | Pages | Time (s) | Std dev | Pages/sec |
|------|-------|----------|---------|-----------|
| scrapy+md | 200 | 6.7 | 0.4 | 30.1 |
| **markcrawl** | **200** | **11.7** | **2.7** | **17.5** |
| colly+md | 124 | 28.9 | 8.0 | 4.4 |
| crawl4ai | 200 | 58.9 | 9.9 | 3.4 |
| playwright | 200 | 40.2 | 0.3 | 5.0 |
| crawlee | 200 | 73.4 | 4.3 | 2.7 |
| crawl4ai-raw | 200 | 87.0 | 4.3 | 2.3 |

scrapy+md wins on blog-engineering (30.1 vs 17.5 p/s). colly+md only fetched
124 of 200 pages.

## Key Findings

- **Fastest overall:** markcrawl at 14.0 pages/sec (1456 pages in 103.9s)
- **Runner-up:** scrapy+md at 9.3 pages/sec — faster on 2 of 8 sites
  (stripe-docs, blog-engineering)
- **Biggest gap:** python-docs where markcrawl hits 22.7 p/s vs scrapy+md's 8.7
- **Page completeness:** scrapy+md fetched 1284/1456 pages (88%); colly+md
  fetched 1376/1456 (95%); playwright missed pages on wikipedia. All other
  tools fetched all pages.
- **Engine matters most:** HTTP-only tools are 3-7x faster than browser-based
  tools regardless of framework quality

Speed doesn't tell the full story — higher word counts don't mean higher
quality. See [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) for extraction
cleanliness, and [COST_AT_SCALE.md](COST_AT_SCALE.md) for how speed and output
size affect total pipeline cost.

## Methodology

- **Two-phase approach:** markcrawl discovers URLs first, then all tools fetch
  the identical URL list (pure fetch+convert speed, no discovery advantage)
- **Settings:** concurrency=5, delay=0, 3 iterations per tool per site
  (median reported with std dev)
- **Warm-up:** 1 throwaway run per site before timing
- See [METHODOLOGY.md](METHODOLOGY.md) for full test setup
