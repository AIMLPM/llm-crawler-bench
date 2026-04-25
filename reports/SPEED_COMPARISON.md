# Speed Comparison
<!-- style: v2, 2026-04-25 -->

markcrawl is the fastest crawler at 6.0 pages/sec overall, followed by scrapy+md (5.3 p/s).

Generated: 2026-04-25 08:41:09 UTC

**Tool versions in this run:**

| Tool | Version |
|---|---|
| colly+md | go binary |
| crawl4ai | 0.8.6 |
| crawl4ai-raw | go binary |
| crawlee | 1.6.2 |
| markcrawl | 0.5.0 |
| playwright | 1.58.0 |
| scrapy+md | 2.15.0 |

## Methodology

**Per-tool discovery:** Each tool starts from the same seed URL and discovers
its own pages through link-following. This tests real-world crawl behavior —
discovery quality, link extraction, and content extraction are all measured.
Page counts may vary between tools depending on each tool's link-following strategy.

Settings:
- **Seed URL:** Same for all tools per site
- **Max pages:** Same limit for all tools per site
- **Delay:** 0 (no politeness throttle)
- **Concurrency:** 5
- **Iterations:** 3 per tool per site (reporting median + std dev)
- **Warm-up:** 1 throwaway run per site before timing
- **Output:** Markdown files + JSONL index

See [METHODOLOGY.md](METHODOLOGY.md) for full methodology.

## Tools tested

| Tool | Type | Available | Notes |
|---|---|---|---|
| markcrawl | HTTP | Yes | requests + BeautifulSoup + markdownify — [AIMLPM/markcrawl](https://github.com/AIMLPM/markcrawl) |
| crawl4ai | Browser | Yes | Playwright + arun_many() batch concurrency — [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) |
| crawl4ai-raw | Browser | Yes | Playwright + sequential arun(), default config (out-of-box baseline) |
| scrapy+md | HTTP | Yes | Scrapy async + markdownify — [scrapy/scrapy](https://github.com/scrapy/scrapy) |
| crawlee | Browser | Yes | Playwright + markdownify — [apify/crawlee-python](https://github.com/apify/crawlee-python) |
| colly+md | HTTP | Yes | Go fetch (Colly) + Python markdownify — [gocolly/colly](https://github.com/gocolly/colly) |
| playwright | Browser | Yes | Raw Playwright baseline + markdownify (no framework) |
| firecrawl | Browser (self-hosted) | Not installed | Self-hosted Docker — [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) |

## Context for the numbers

**Pages/sec** measures raw crawl throughput — how fast a tool fetches and converts HTML to Markdown. Tools using Playwright (browser rendering) are inherently slower than HTTP-only tools (requests/Scrapy/Colly) because they must launch a browser and wait for JavaScript execution. **Avg words** and **Output KB** reflect output volume, not quality — see [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) for whether more words means better content.

## Results by site

### react-dev — React docs (SPA, JS-rendered, interactive examples)

Max pages: 500

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] |
|---|---|---|---|---|---|
| markcrawl | 221 | 11.8 | 18.7 | 1565 | 2720 |
| colly+md | 292 | 24.6 | 11.9 | 5535 | 18880 |
| scrapy+md | 217 | 22.4 | 10.9 | 1625 | 2900 |
| playwright | 221 | 49.1 | 4.5 | 4330 | 11657 |
| crawlee | 217 | 79.2 | 2.8 | 4452 | 11715 |
| crawl4ai | 500 | 221.8 | 2.3 | 1870 | 10934 |
| crawl4ai-raw | 500 | 281.6 | 1.8 | 1870 | 10934 |

### stripe-docs — Stripe API docs (tabbed content, code samples, sidebars)

Max pages: 500

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] |
|---|---|---|---|---|---|
| scrapy+md | 497 | 56.2 | 8.9 | 5774 | 35049 |
| markcrawl | 500 | 81.7 | 6.1 | 730 | 2622 |
| colly+md | 498 | 140.5 | 3.5 | 19030 | 273600 |
| crawlee | 501 | 485.6 | 1.0 | 21254 | 282210 |
| playwright | 500 | 487.9 | 1.0 | 20399 | 270004 |
| crawl4ai-raw | 500 | 645.8 | 0.8 | 1995 | 9902 |
| crawl4ai | 500 | 741.4 | 0.7 | 1481 | 7450 |

### huggingface-transformers — Hugging Face Transformers docs -- model cards, code examples, SPA

Max pages: 300

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] |
|---|---|---|---|---|---|
| playwright | 60 | 22.8 | 2.7 | 251 | 462 |
| crawl4ai-raw | 300 | 329.4 | 0.9 | 895 | 2905 |
| crawl4ai | 300 | 359.3 | 0.8 | 1043 | 3993 |
| scrapy+md | 36 | 26.8 | 0.7 | 0 | 0 |
| crawlee | 0 | 4.4 | 0.0 | 0 | 0 |
| colly+md | 0 | 5.9 | 0.0 | 0 | 0 |
| markcrawl | — | — | — | error: heartbeat stall: no new pages for 180s |

### kubernetes-docs — Kubernetes concepts + reference docs -- long-form, cross-linked

Max pages: 400

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] |
|---|---|---|---|---|---|
| markcrawl | 400 | 22.9 | 17.5 | 1712 | 5781 |
| scrapy+md | 314 | 44.5 | 7.1 | 4865 | 12405 |
| playwright | 400 | 129.8 | 3.1 | 5382 | 38057 |
| crawl4ai-raw | 400 | 220.5 | 1.8 | 5353 | 45832 |
| crawl4ai | 400 | 245.6 | 1.6 | 5382 | 46049 |
| crawlee | 401 | 425.2 | 0.9 | 5443 | 39223 |
| colly+md | — | — | — | error: heartbeat stall: 0 pages after 120s |

### postgres-docs — PostgreSQL docs -- dense SQL reference, text-heavy

Max pages: 400

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] |
|---|---|---|---|---|---|
| markcrawl | 400 | 16.8 | 25.6 | 859 | 3438 |
| scrapy+md | 400 | 19.1 | 22.1 | 1112 | 3501 |
| crawlee | 400 | 99.8 | 4.0 | 974 | 3763 |
| playwright | 400 | 135.0 | 3.3 | 969 | 3746 |
| crawl4ai-raw | 400 | 145.2 | 2.8 | 962 | 5315 |
| crawl4ai | 400 | 162.5 | 2.5 | 962 | 5315 |
| colly+md | — | — | — | error: heartbeat stall: 0 pages after 120s |

### mdn-css — MDN CSS reference -- property/selector pages, deeply linked

Max pages: 300

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] |
|---|---|---|---|---|---|
| markcrawl | 300 | 11.3 | 26.6 | 946 | 2207 |
| scrapy+md | 299 | 21.7 | 13.8 | 575 | 8568 |
| playwright | 300 | 69.8 | 4.3 | 4452 | 29971 |
| crawl4ai-raw | 300 | 159.9 | 1.9 | 4213 | 38422 |
| crawl4ai | 300 | 211.9 | 1.5 | 4213 | 38398 |
| crawlee | 300 | 396.6 | 0.8 | 4167 | 29393 |
| colly+md | — | — | — | error: heartbeat stall: 0 pages after 120s |

### rust-book — The Rust Programming Language book -- chaptered tutorial

Max pages: 200

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] |
|---|---|---|---|---|---|
| scrapy+md | 200 | 17.0 | 11.8 | 3614 | 7394 |
| markcrawl | 200 | 18.0 | 11.1 | 5119 | 9980 |
| playwright | 200 | 22.2 | 9.0 | 4182 | 6939 |
| colly+md | 54 | 6.5 | 8.4 | 11006 | 4564 |
| crawlee | 200 | 56.0 | 3.6 | 4182 | 6939 |
| crawl4ai-raw | 200 | 62.4 | 3.2 | 4062 | 8391 |
| crawl4ai | 200 | 69.6 | 2.9 | 4062 | 8391 |

### newegg — Newegg electronics catalog -- product listings with pricing, clean /<slug>/p/<id> URL pattern

Max pages: 200

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] |
|---|---|---|---|---|---|
| markcrawl | 200 | 38.4 | 5.5 | 603 | 804 |
| playwright | 3 | 2.9 | 1.0 | 1565 | 649 |
| crawl4ai | 200 | 217.7 | 1.0 | 9900 | 35389 |
| crawl4ai-raw | 200 | 254.6 | 0.8 | 9900 | 35390 |
| colly+md | 17 | 98.0 | 0.2 | 3727 | 1397 |
| scrapy+md | 0 | 2.9 | 0.0 | 0 | 0 |
| crawlee | 0 | 5.2 | 0.0 | 0 | 0 |

### ikea — IKEA US furniture catalog -- product + category pages with pricing

Max pages: 200

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] |
|---|---|---|---|---|---|
| scrapy+md | 186 | 43.2 | 4.5 | 1265 | 2618 |
| markcrawl | 200 | 115.5 | 1.7 | 1655 | 2762 |
| playwright | 200 | 192.5 | 1.0 | 5084 | 28217 |
| crawlee | 201 | 205.1 | 1.0 | 6389 | 35145 |
| crawl4ai-raw | 200 | 243.4 | 0.8 | 2327 | 5765 |
| crawl4ai | 200 | 426.7 | 0.5 | 2180 | 5267 |
| colly+md | — | — | — | error: heartbeat stall: 0 pages after 120s |

### smittenkitchen — Smitten Kitchen recipe blog -- WordPress long-form, recipe microdata

Max pages: 200

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] |
|---|---|---|---|---|---|
| markcrawl | 200 | 28.0 | 7.2 | 16247 | 19245 |
| playwright | 200 | 43.6 | 4.6 | 3970 | 29487 |
| crawl4ai | 200 | 82.3 | 2.4 | 1190 | 3494 |
| crawl4ai-raw | 200 | 83.6 | 2.4 | 1184 | 3481 |
| scrapy+md | 190 | 189.6 | 1.0 | 59206 | 91797 |
| crawlee | 104 | 81.7 | 0.7 | 4291 | 31866 |
| colly+md | — | — | — | error: heartbeat stall: 0 pages after 120s |

### npr-news — NPR news section -- wire-style articles, deep linking, stable URLs

Max pages: 150

| Tool | Pages (a) | Time (b) | Pages/sec [1] | Avg words [2] | Output KB [3] |
|---|---|---|---|---|---|
| crawl4ai-raw | 150 | 91.3 | 1.6 | 2995 | 5292 |
| crawl4ai | 150 | 106.6 | 1.4 | 2994 | 5281 |
| markcrawl | 150 | 116.8 | 1.3 | 288 | 324 |
| crawlee | 150 | 179.8 | 0.8 | 6498 | 23530 |
| scrapy+md | — | — | — | error: heartbeat stall: 0 pages after 120s |
| colly+md | — | — | — | error: heartbeat stall: 0 pages after 120s |
| playwright | — | — | — | error: wall-clock timeout after 360s |

> **Column definitions:** **Pages (a)** = pages discovered and fetched by this tool (varies per tool).
> **Time (b)** = wall-clock seconds to fetch and convert all pages (median of 3 iterations).
> **[1] Pages/sec** = median throughput across iterations.
> Approximately a÷b; small differences arise because each column is an independent median.
> **[2] Avg words** = mean words per page. **[3] Output KB** = total Markdown output size across all pages.

## Overall summary

| Tool | Total pages (a) | Total time (b) | Avg pages/sec (a÷b) | Notes |
|---|---|---|---|---|
| markcrawl | 2771 | 461.2 | 6.0 | *(10/11 sites)* *(missing 579 pages)* |
| scrapy+md | 2338 | 443.5 | 5.3 | *(10/11 sites)* *(missing 1011 pages)* |
| colly+md | 862 | 275.4 | 3.1 | *(5/11 sites)* *(missing 2488 pages)* |
| playwright | 2484 | 1155.7 | 2.1 | *(10/11 sites)* *(missing 866 pages)* |
| crawl4ai-raw | 3350 | 2517.7 | 1.3 |  |
| crawlee | 2474 | 2018.7 | 1.2 | *(missing 875 pages)* |
| crawl4ai | 3350 | 2845.3 | 1.2 |  |

> **Column definitions:** **Total pages (a)** = sum of pages fetched across all sites.
> **Total time (b)** = sum of median wall-clock times across all sites. **Avg pages/sec (a÷b)** = overall throughput.

> **Note on variance:** These benchmarks fetch pages from live public websites.
> Network conditions, server load, and CDN caching can cause significant
> run-to-run variance. For the most reliable comparison,
> run multiple iterations and compare medians.

## What the results mean

HTTP-only tools (markcrawl, scrapy+md, colly+md) are consistently 2-7x faster than browser-based tools (crawl4ai, crawlee, playwright). The speed gap comes from skipping browser startup and JavaScript execution entirely.

markcrawl is fastest overall, but loses on stripe-docs (scrapy+md), huggingface-transformers (playwright), rust-book (scrapy+md), ikea (scrapy+md), npr-news (crawl4ai-raw). Site-specific results vary with server response times and content complexity.

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
