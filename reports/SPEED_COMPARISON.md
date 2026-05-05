# Speed Comparison
<!-- style: v2, 2026-05-05 -->

scrapy+md leads aggregate speed at 5.00 pages/sec across all 11 sites; markcrawl follows at 4.95 p/s. Single-tool throughput numbers (per-site cells below) show markcrawl as the speed champion when sites cooperate (postgres-docs at 22.3 p/s, kubernetes at 13.3 p/s, mdn-css at 11.4 p/s).

**Run:** `run_v13_merged_20260504_203748` (v1.3 cycle, aggregated from per-tool gap-fill passes 2026-05-04/05) | **Pool:** v1.2 (npr-news removed, propublica added — see METHODOLOGY.md "Crawler tuning" + "Site pool ethics")

**Tool versions in this run:**

| Tool | Version | Status |
|---|---|---|
| colly+md | go binary | available |
| crawl4ai | 0.8.6 | available |
| crawl4ai-raw | go binary | available |
| crawlee | 1.6.2 | available |
| markcrawl | 0.10.5 | available |
| playwright | 1.58.0 | available |
| scrapy+md | 2.15.0 | available |
| firecrawl | — | skipped: FIRECRAWL_API_KEY not set |

## Methodology note (v1.3 specific)

The v1.3 main run died mid-flight from macOS jetsam pressure; the recovery used per-tool sequential gap-fill passes. Speed numbers below are aggregated from those passes — each (tool, site) pair was crawled in isolation, so the numbers reflect single-tool throughput rather than under-load behavior. The trade-off is real: this **avoids** the WAF-concurrency penalty that hurt colly+md/scrapy+md on shared sites in the original parallel run, but it may **understate** speed for tools that genuinely benefit from parallel multi-site crawling.

## Summary: aggregate speed across all 11 sites

| Tool | Sites | Total pages | Total wall-clock (s) | Avg pages/sec (a÷b) |
|---|---|---|---|---|
| scrapy+md | 11/11 | 2657 | 531 | **5.00** |
| markcrawl | 11/11 | 2323 | 469 | **4.95** |
| playwright | 11/11 | 3071 | 1238 | **2.48** |
| crawl4ai | 11/11 | 3050 | 2219 | **1.37** |
| crawl4ai-raw | 11/11 | 3350 | 2439 | **1.37** |
| crawlee | 11/11 | 2602 | 2067 | **1.26** |
| colly+md | 10/11 | 2649 | 2646 | **1.00** |

> **Column definitions:** **Total pages** = best-of pages.jsonl line counts across passes. **Total wall-clock** = sum of median per-iteration timing across all sites. **Avg pages/sec (a÷b)** = total pages ÷ total wall-clock.

## Per-site detail (median timings)

| Site | scrapy+md | markcrawl | playwright | crawl4ai | crawl4ai-raw | crawlee | colly+md |
|------|---|---|---|---|---|---|---|
| huggingface-transformers | 1.5 (240p/161s) | 0.1 (21p/167s) | 3.2 (300p/94s) | — | 0.8 (300p/370s) | 0.1 (16p/168s) | — |
| ikea | 5.2 (194p/33s) | 3.0 (200p/65s) | 1.1 (200p/177s) | 0.9 (200p/237s) | 0.8 (200p/271s) | 1.3 (203p/157s) | 0.3 (200p/609s) |
| kubernetes-docs | 6.9 (315p/45s) | 13.3 (400p/30s) | 3.3 (400p/121s) | 1.9 (400p/210s) | 1.8 (400p/218s) | 1.0 (404p/400s) | 1.9 (399p/208s) |
| mdn-css | 13.0 (300p/23s) | 11.3 (300p/26s) | 3.9 (300p/80s) | 1.7 (300p/180s) | 1.9 (300p/168s) | 0.9 (308p/329s) | 0.6 (289p/506s) |
| newegg | — | — | 6.8 (200p/29s) | 0.7 (200p/274s) | 1.2 (200p/181s) | — | 0.6 (165p/275s) |
| postgres-docs | 27.0 (400p/16s) | 22.2 (400p/19s) | 3.7 (400p/126s) | 2.8 (400p/141s) | 3.0 (400p/136s) | 4.6 (400p/87s) | 1.6 (401p/262s) |
| propublica | 8.0 (146p/18s) | 3.1 (150p/49s) | 2.2 (150p/67s) | 1.5 (150p/98s) | 1.6 (150p/96s) | 1.4 (150p/104s) | 1.0 (150p/150s) |
| react-dev | 16.3 (217p/13s) | 8.3 (51p/6s) | 5.2 (221p/42s) | 2.2 (500p/223s) | 2.3 (500p/216s) | 3.2 (217p/67s) | 12.6 (292p/23s) |
| rust-book | 12.6 (200p/16s) | 22.1 (112p/5s) | 9.1 (200p/22s) | 3.1 (200p/64s) | 3.3 (200p/60s) | 3.5 (201p/56s) | 8.9 (54p/6s) |
| smittenkitchen | 1.0 (145p/145s) | 11.9 (200p/17s) | 4.6 (200p/44s) | 2.5 (200p/82s) | 2.4 (200p/84s) | 2.2 (203p/93s) | 0.4 (200p/478s) |
| stripe-docs | 8.8 (500p/57s) | 6.3 (489p/78s) | 1.1 (500p/435s) | 0.7 (500p/707s) | 0.8 (500p/640s) | 0.9 (500p/601s) | 3.8 (499p/129s) |

> Cell format: `pps (pages/time_s)`. Em-dash = no pages crawled (anti-bot, JS-on-SPA limit, etc.).

Per-site retrieval+quality detail in [RETRIEVAL_COMPARISON.md](RETRIEVAL_COMPARISON.md) and [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md).
