# Speed Comparison
<!-- style: v2, 2026-04-23 -->

markcrawl is the fastest crawler at 2.3 pages/sec overall, followed by N/A (0.0 p/s).

Generated: 2026-04-23 19:14:57 UTC

## Methodology

**Per-tool discovery:** Each tool starts from the same seed URL and discovers
its own pages through link-following. This tests real-world crawl behavior —
discovery quality, link extraction, and content extraction are all measured.
Page counts may vary between tools depending on each tool's link-following strategy.

Settings:
- **Seed URL:** Same for all tools per site
- **Max pages:** Same limit for all tools per site
- **Delay:** 0 (no politeness throttle)
- **Concurrency:** 1
- **Iterations:** 3 per tool per site (reporting median + std dev)
- **Warm-up:** 1 throwaway run per site before timing
- **Output:** Markdown files + JSONL index

See [METHODOLOGY.md](METHODOLOGY.md) for full methodology.

## Tools tested

| Tool | Type | Available | Notes |
|---|---|---|---|
| markcrawl | HTTP | Yes | requests + BeautifulSoup + markdownify — [AIMLPM/markcrawl](https://github.com/AIMLPM/markcrawl) |
| crawl4ai | Browser | Not installed | Playwright + arun_many() batch concurrency — [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) |
| crawl4ai-raw | Browser | Not installed | Playwright + sequential arun(), default config (out-of-box baseline) |
| scrapy+md | HTTP | Not installed | Scrapy async + markdownify — [scrapy/scrapy](https://github.com/scrapy/scrapy) |
| crawlee | Browser | Not installed | Playwright + markdownify — [apify/crawlee-python](https://github.com/apify/crawlee-python) |
| colly+md | HTTP | Not installed | Go fetch (Colly) + Python markdownify — [gocolly/colly](https://github.com/gocolly/colly) |
| playwright | Browser | Not installed | Raw Playwright baseline + markdownify (no framework) |
| firecrawl | Browser (self-hosted) | Not installed | Self-hosted Docker — [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) |

## Context for the numbers

**Pages/sec** measures raw crawl throughput — how fast a tool fetches and converts HTML to Markdown. Tools using Playwright (browser rendering) are inherently slower than HTTP-only tools (requests/Scrapy/Colly) because they must launch a browser and wait for JavaScript execution. **Avg words** and **Output KB** reflect output volume, not quality — see [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) for whether more words means better content.

## Results by site

### quotes-toscrape — Paginated quotes (simple HTML, link-following)

Max pages: 15

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|
| markcrawl | 15 | 5.6 | 2.7 | 261 | 25 | 120 |

### books-toscrape — E-commerce catalog (60 pages, pagination)

Max pages: 60

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|
| markcrawl | 60 | 17.5 | 3.4 | 615 | 316 | 39 |

### fastapi-docs — API documentation (code blocks, headings, tutorials)

Max pages: 500

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|
| markcrawl | 156 | 35.2 | 4.4 | 2063 | 2975 | 38 |

### python-docs — Python standard library docs

Max pages: 500

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|
| markcrawl | 500 | 260.6 | 1.9 | 3059 | 15004 | 48 |

### react-dev — React docs (SPA, JS-rendered, interactive examples)

Max pages: 500

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|
| markcrawl | 221 | 55.3 | 4.0 | 1587 | 2770 | 34 |

### wikipedia-python — Wikipedia (tables, infoboxes, citations, deep linking)

Max pages: 50

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|
| markcrawl | 50 | 16.9 | 3.0 | 3274 | 1769 | 30 |

### stripe-docs — Stripe API docs (tabbed content, code samples, sidebars)

Max pages: 500

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|
| markcrawl | 500 | 365.8 | 1.4 | 771 | 2825 | 31 |

### blog-engineering — GitHub Engineering Blog (articles, images, technical content)

Max pages: 200

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|
| markcrawl | 200 | 30.0 | 6.7 | 766 | 1235 | 29 |

### gen2fund — Gen2 Fund -- venture fund marketing site (small static)

Max pages: 50

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | error: wall-clock timeout after 160s |

### brex — Brex -- NA fintech neobank marketing + product pages

Max pages: 150

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|
| markcrawl | 150 | 57.1 | 2.6 | 1925 | 2110 | 25 |

### supabase-docs — Supabase platform docs -- OSS backend, modern SPA

Max pages: 300

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|
| markcrawl | 300 | 109.4 | 2.7 | 70 | 167 | 27 |

### tailwind-docs — Tailwind CSS utility-first framework docs

Max pages: 200

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] | Peak MB [4] |
|---|---|---|---|---|---|---|
| markcrawl | 200 | 51.9 | 3.9 | 841 | 1417 | 26 |

> **Column definitions:** **Pages (a)** = pages discovered and fetched by this tool (varies per tool).
> **Time (b)** = wall-clock seconds to fetch and convert all pages (median of 3 iterations).
> **[1] Pages/sec** = median throughput across iterations.
> Approximately a÷b; small differences arise because each column is an independent median.
> **[2] Avg words** = mean words per page. **[3] Output KB** = total Markdown output size across all pages.
> **[4] Peak MB** = peak resident memory (RSS) during crawl.

## Overall summary

| Tool | Total pages (a) | Total time (b) | Avg pages/sec (a÷b) | Notes |
|---|---|---|---|---|
| markcrawl | 2352 | 1005.3 | 2.3 | *(11/12 sites)* |

> **Column definitions:** **Total pages (a)** = sum of pages fetched across all sites.
> **Total time (b)** = sum of median wall-clock times across all sites. **Avg pages/sec (a÷b)** = overall throughput.

> **Note on variance:** These benchmarks fetch pages from live public websites.
> Network conditions, server load, and CDN caching can cause significant
> run-to-run variance. For the most reliable comparison,
> run multiple iterations and compare medians.

## What the results mean

HTTP-only tools (markcrawl, scrapy+md, colly+md) are consistently 2-7x faster than browser-based tools (crawl4ai, crawlee, playwright). The speed gap comes from skipping browser startup and JavaScript execution entirely.

markcrawl is fastest on every site tested.

Higher word counts from browser-based tools (crawlee, playwright) do not indicate better extraction quality — they often reflect extra navigation chrome and repeated boilerplate. See [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) for content signal analysis.

Some tools miss pages on certain sites: scrapy+md and colly+md fetch fewer pages than expected on some sites, which inflates their per-page speed but means incomplete coverage. Check the per-site tables for exact page counts.

## Reproducing these results

```bash
# Install all tools
pip install markcrawl crawl4ai scrapy markdownify
playwright install chromium  # for crawl4ai

# Run comparison
python benchmark_all_tools.py
```

For FireCrawl, also run:
```bash
docker run -p 3002:3002 firecrawl/firecrawl:latest
export FIRECRAWL_API_URL=http://localhost:3002
python benchmark_all_tools.py
```

## See also

- [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) — higher word counts don't mean higher quality
- [COST_AT_SCALE.md](COST_AT_SCALE.md) — what these speed differences cost at 100K+ pages
- [METHODOLOGY.md](METHODOLOGY.md) — full test setup and fairness decisions
