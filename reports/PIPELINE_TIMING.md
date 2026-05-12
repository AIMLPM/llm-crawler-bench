# End-to-End RAG Pipeline Timing Benchmark
<!-- style: v2, 2026-04-12 -->

markcrawl completes the full RAG pipeline (scrape + chunk + embed + query) in 440.7s — 1.1x faster than the median tool. For HTTP-only crawlers, the LLM query phase dominates at 95-98% of total time, not scraping.

> **Single-trial measurement.** Each per-site number reported here comes from one benchmark run. Network jitter, WAF state, and server load can shift per-site speed and coverage between runs by single-digit percent. Confidence intervals reflect query-set sampling only — not run-to-run variance. Multi-trial validation is v1.5 work; see [METHODOLOGY.md](METHODOLOGY.md#single-trial-measurement).

**Sites:** huggingface-transformers, ikea, kubernetes-docs, mdn-css, newegg, postgres-docs, propublica, react-dev, rust-book, smittenkitchen, stripe-docs | **Embedding model:** text-embedding-3-small | **Answer model:** gpt-4o-mini

**Run:** `run_v13_merged_20260504_203748` | **Started:** 2026-05-04T13:36:42Z | **Ended:** 2026-05-05T05:41:25.381501+00:00 | **Pool:** 1.2 (sha256:caa35)

**Tool versions in this run:**

| Tool | Version | Status |
|---|---|---|
| colly+md | go binary | available |
| crawl4ai | 0.8.6 | available |
| crawl4ai-raw | go binary | available |
| crawlee | 1.6.2 | available |
| firecrawl | — | skipped: FIRECRAWL_API_KEY not set |
| markcrawl | 0.10.5 | available |
| playwright | 1.58.0 | available |
| scrapy+md | 2.15.0 | available |


## What these phases mean

Each tool is measured across four pipeline phases:

- **Scrape** = fetch HTML and convert to Markdown (dominated by network I/O). HTTP-only tools (markcrawl, scrapy+md, colly+md) scrape 2-7x faster than browser-based tools (crawl4ai, crawlee, playwright) because they skip JavaScript rendering overhead.
- **Chunk** = split Markdown into overlapping text chunks (CPU-only, fast)
- **Embed** = send chunks to OpenAI embedding API (scales with chunk count)
- **Query** = embed question + retrieve top chunks + send to LLM for answer (scales with query count)

## Summary: Total Pipeline Time by Tool

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | **Total (s)** | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|--------------|-------|--------|------|
| markcrawl | 0.0 | 2.9 | 5.6 | 432.1 | **440.7** | 2521 | 30773 | $0.397 |
| scrapy+md | 0.0 | 7.1 | 9.6 | 434.6 | **451.3** | 2644 | 52487 | $1.05 |
| playwright | 0.0 | 8.5 | 11.1 | 441.6 | **461.2** | 3071 | 58406 | $3.54 |
| crawl4ai-raw | 0.0 | 3.2 | 5.5 | 470.1 | **478.9** | 3350 | 32119 | $0.523 |
| colly+md | 0.0 | 9.9 | 12.6 | 465.3 | **487.8** | 2648 | 65652 | $3.82 |
| crawlee | 0.0 | 8.5 | 10.9 | 478.3 | **497.7** | 2589 | 58979 | $3.19 |
| crawl4ai | 0.0 | 3.1 | 5.2 | 507.0 | **515.3** | 3050 | 30257 | $0.493 |

> **Column definitions:** **Scrape/Chunk/Embed/Query (s)** = wall-clock seconds for each pipeline phase (summed across all sites). **Total (s)** = sum of all phases. **Pages** = total pages fetched. **Chunks** = total text chunks produced. **Cost** = total API cost (embedding + LLM query).

*(Cost uses OpenAI `text-embedding-3-small` at $0.02/1M tokens, `gpt-4o-mini` at $0.15/$0.6 per 1M input/output tokens)*

## Per-Page Pipeline Cost (normalized)

Since scrapy+md fetched fewer pages (due to timeouts), this table normalizes
time and cost per page for a fairer comparison.

| Tool | Pages | Total (s) | s/page | Cost/page | Chunks/page |
|------|-------|----------|--------|-----------|-------------|
| markcrawl | 2521 | 440.7 | 0.17 | $0.0002 | 12.2 |
| scrapy+md | 2644 | 451.3 | 0.17 | $0.0004 | 19.9 |
| playwright | 3071 | 461.2 | 0.15 | $0.0012 | 19.0 |
| crawl4ai-raw | 3350 | 478.9 | 0.14 | $0.0002 | 9.6 |
| colly+md | 2648 | 487.8 | 0.18 | $0.0014 | 24.8 |
| crawlee | 2589 | 497.7 | 0.19 | $0.0012 | 22.8 |
| crawl4ai | 3050 | 515.3 | 0.17 | $0.0002 | 9.9 |

> **Column definitions:** **s/page** = Total (s) ÷ Pages. **Cost/page** = total API cost ÷ Pages. **Chunks/page** = Chunks ÷ Pages. All values are per-page averages.

## Phase Breakdown (% of Total Pipeline Time)

| Tool | Scrape % | Chunk % | Embed % | Query % |
|------|---------|--------|--------|--------|
| markcrawl | 0.0% | 0.7% | 1.3% | 98.1% |
| scrapy+md | 0.0% | 1.6% | 2.1% | 96.3% |
| playwright | 0.0% | 1.8% | 2.4% | 95.7% |
| crawl4ai-raw | 0.0% | 0.7% | 1.2% | 98.2% |
| colly+md | 0.0% | 2.0% | 2.6% | 95.4% |
| crawlee | 0.0% | 1.7% | 2.2% | 96.1% |
| crawl4ai | 0.0% | 0.6% | 1.0% | 98.4% |

> Each percentage = phase time ÷ total pipeline time. Shows which phase dominates.

## API Cost Breakdown

*(Pricing: `text-embedding-3-small` at $0.02/1M tokens, `gpt-4o-mini` input at $0.15/1M, output at $0.6/1M)*

| Tool | Embed tokens | Embed cost | Query in tokens | Query out tokens | Query cost | **Total cost** |
|------|-------------|-----------|----------------|-----------------|-----------|---------------|
| markcrawl | 15,559,006 | $0.311 | 499,862 | 18,048 | $0.086 | **$0.397** |
| scrapy+md | 47,053,870 | $0.941 | 627,201 | 16,688 | $0.104 | **$1.05** |
| playwright | 171,367,925 | $3.43 | 660,759 | 16,977 | $0.109 | **$3.54** |
| crawl4ai-raw | 20,689,132 | $0.414 | 657,102 | 17,225 | $0.109 | **$0.523** |
| colly+md | 184,834,053 | $3.70 | 750,997 | 15,609 | $0.122 | **$3.82** |
| crawlee | 154,771,745 | $3.10 | 566,130 | 16,769 | $0.095 | **$3.19** |
| crawl4ai | 19,590,997 | $0.392 | 607,716 | 16,540 | $0.101 | **$0.493** |

> **Embed tokens** = tokens sent to the embedding API (all chunks). **Query in/out tokens** = tokens sent to and received from the answer LLM. **Total cost** = Embed cost + Query cost.

## What the results mean

For fast HTTP-only crawlers, scraping is NOT the bottleneck — LLM queries dominate at 70-77% of total pipeline time. The scrape phase only matters for browser-based tools where JavaScript rendering adds 3-7x overhead.

The biggest cost lever is chunk count: markcrawl produces 30,773 chunks vs colly+md's 65,652, leading to 11.9x lower embedding costs ($0.311 vs $3.70). At scale, the per-query cost difference is small; the savings compound from embedding fewer chunks.

See [COST_AT_SCALE.md](COST_AT_SCALE.md) for projections of these per-run costs to production workloads.

## Per-Site Breakdown

### huggingface-transformers

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| crawl4ai-raw | 0.0 | 0.1 | 0.2 | 21.9 | 22.2 | 300 | 1018 | $0.020 |
| crawlee | 0.0 | 0.0 | 0.0 | 25.5 | 25.5 | 16 | 67 | $0.011 |
| scrapy+md | 0.0 | 0.7 | 1.2 | 27.5 | 29.5 | 240 | 6346 | $0.194 |
| markcrawl | 0.0 | 0.4 | 0.7 | 37.0 | 38.1 | 219 | 3580 | $0.056 |
| playwright | 0.0 | 0.0 | 0.1 | 41.7 | 41.8 | 300 | 356 | $0.018 |

### ikea

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| crawl4ai-raw | 0.0 | 0.1 | 0.3 | 14.3 | 14.7 | 200 | 1554 | $0.030 |
| crawlee | 0.0 | 0.7 | 0.8 | 14.7 | 16.2 | 203 | 4610 | $0.262 |
| crawl4ai | 0.0 | 0.1 | 0.3 | 16.1 | 16.6 | 200 | 1622 | $0.031 |
| scrapy+md | 0.0 | 0.1 | 0.2 | 18.9 | 19.2 | 194 | 1107 | $0.036 |
| playwright | 0.0 | 0.5 | 0.7 | 21.3 | 22.5 | 200 | 3308 | $0.193 |
| markcrawl | 0.0 | 0.1 | 0.2 | 25.9 | 26.1 | 200 | 928 | $0.018 |
| colly+md | 0.0 | 0.4 | 0.5 | 31.3 | 32.3 | 200 | 2942 | $0.161 |

### kubernetes-docs

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| crawlee | 0.0 | 0.7 | 1.2 | 24.0 | 25.9 | 400 | 6813 | $0.097 |
| playwright | 0.0 | 0.7 | 1.2 | 24.0 | 25.9 | 400 | 6812 | $0.091 |
| colly+md | 0.0 | 0.8 | 1.2 | 26.3 | 28.3 | 399 | 6743 | $0.089 |
| markcrawl | 0.0 | 0.6 | 1.4 | 29.0 | 31.0 | 400 | 7922 | $0.085 |
| crawl4ai-raw | 0.0 | 0.7 | 1.2 | 36.0 | 37.8 | 400 | 6822 | $0.091 |
| scrapy+md | 0.0 | 0.4 | 0.6 | 40.5 | 41.5 | 315 | 3507 | $0.080 |
| crawl4ai | 0.0 | 0.7 | 1.2 | 43.8 | 45.6 | 400 | 6822 | $0.091 |

### mdn-css

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| crawlee | 0.0 | 0.5 | 0.7 | 21.6 | 22.8 | 300 | 3891 | $0.066 |
| markcrawl | 0.0 | 0.1 | 0.2 | 25.7 | 26.0 | 300 | 1006 | $0.016 |
| playwright | 0.0 | 0.5 | 0.8 | 27.8 | 29.1 | 300 | 4168 | $0.071 |
| crawl4ai-raw | 0.0 | 0.4 | 0.7 | 31.4 | 32.5 | 300 | 3864 | $0.067 |
| crawl4ai | 0.0 | 0.4 | 0.7 | 32.1 | 33.2 | 300 | 3864 | $0.067 |
| colly+md | 0.0 | 0.7 | 0.8 | 39.6 | 41.1 | 289 | 4190 | $0.168 |
| scrapy+md | 0.0 | 0.1 | 0.1 | 50.7 | 50.9 | 300 | 621 | $0.058 |

### newegg

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| crawl4ai | 0.0 | 0.7 | 1.0 | 21.6 | 23.4 | 200 | 5857 | $0.093 |
| colly+md | 0.0 | 1.1 | 1.3 | 30.8 | 33.2 | 165 | 6574 | $0.474 |
| crawl4ai-raw | 0.0 | 0.7 | 1.0 | 31.9 | 33.6 | 200 | 5856 | $0.092 |
| playwright | 0.0 | 0.4 | 0.2 | 41.9 | 42.5 | 200 | 1195 | $0.431 |

### postgres-docs

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| playwright | 0.0 | 0.1 | 0.2 | 29.9 | 30.2 | 400 | 1216 | $0.019 |
| colly+md | 0.0 | 0.1 | 0.2 | 31.7 | 32.0 | 401 | 1115 | $0.018 |
| scrapy+md | 0.0 | 0.1 | 0.3 | 36.4 | 36.8 | 394 | 1531 | $0.022 |
| crawlee | 0.0 | 0.1 | 0.2 | 38.9 | 39.3 | 400 | 1226 | $0.019 |
| markcrawl | 0.0 | 0.2 | 0.4 | 41.7 | 42.3 | 400 | 2348 | $0.028 |
| crawl4ai-raw | 0.0 | 0.1 | 0.2 | 58.8 | 59.2 | 400 | 1193 | $0.021 |
| crawl4ai | 0.0 | 0.1 | 0.2 | 69.4 | 69.7 | 400 | 1193 | $0.021 |

### propublica

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| markcrawl | 0.0 | 0.1 | 0.2 | 28.7 | 29.0 | 150 | 1264 | $0.014 |
| crawl4ai-raw | 0.0 | 0.1 | 0.3 | 29.8 | 30.2 | 150 | 1563 | $0.024 |
| playwright | 0.0 | 0.4 | 0.4 | 29.8 | 30.5 | 150 | 2197 | $0.092 |
| scrapy+md | 0.0 | 0.1 | 0.2 | 34.3 | 34.7 | 146 | 1396 | $0.019 |
| crawlee | 0.0 | 0.4 | 0.4 | 35.0 | 35.7 | 150 | 2099 | $0.092 |
| colly+md | 0.0 | 0.4 | 0.4 | 42.2 | 43.0 | 150 | 2196 | $0.085 |
| crawl4ai | 0.0 | 0.1 | 0.3 | 44.3 | 44.8 | 150 | 1563 | $0.024 |

### react-dev

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| markcrawl | 0.0 | 0.0 | 0.1 | 85.0 | 85.1 | 51 | 419 | $0.020 |
| scrapy+md | 0.0 | 0.1 | 0.2 | 89.0 | 89.3 | 217 | 1259 | $0.027 |
| crawl4ai-raw | 0.0 | 0.3 | 0.6 | 101.3 | 102.1 | 500 | 3210 | $0.057 |
| playwright | 0.0 | 0.3 | 0.5 | 112.7 | 113.6 | 221 | 3067 | $0.086 |
| colly+md | 0.0 | 0.6 | 0.9 | 125.8 | 127.3 | 292 | 5083 | $0.129 |
| crawl4ai | 0.0 | 0.3 | 0.6 | 127.4 | 128.2 | 500 | 3210 | $0.057 |
| crawlee | 0.0 | 0.4 | 0.5 | 139.9 | 140.8 | 217 | 3063 | $0.086 |

### rust-book

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| scrapy+md | 0.0 | 0.3 | 0.5 | 30.4 | 31.2 | 200 | 2978 | $0.043 |
| markcrawl | 0.0 | 0.1 | 0.2 | 32.3 | 32.6 | 112 | 1287 | $0.019 |
| playwright | 0.0 | 0.3 | 0.5 | 32.8 | 33.6 | 200 | 2829 | $0.040 |
| crawl4ai-raw | 0.0 | 0.3 | 0.5 | 37.2 | 37.9 | 200 | 2702 | $0.042 |
| crawl4ai | 0.0 | 0.3 | 0.5 | 38.9 | 39.6 | 200 | 2702 | $0.042 |
| colly+md | 0.0 | 0.2 | 0.3 | 39.7 | 40.3 | 54 | 1976 | $0.029 |
| crawlee | 0.0 | 0.3 | 0.5 | 57.4 | 58.1 | 200 | 2829 | $0.040 |

### smittenkitchen

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| playwright | 0.0 | 0.5 | 0.5 | 12.0 | 13.1 | 200 | 3029 | $0.263 |
| colly+md | 0.0 | 0.7 | 0.7 | 28.3 | 29.7 | 199 | 3708 | $0.258 |
| crawl4ai | 0.0 | 0.1 | 0.1 | 31.1 | 31.4 | 200 | 773 | $0.027 |
| crawl4ai-raw | 0.0 | 0.1 | 0.1 | 35.2 | 35.4 | 200 | 773 | $0.027 |
| scrapy+md | 0.0 | 3.3 | 3.6 | 29.9 | 36.8 | 138 | 18860 | $0.211 |
| crawlee | 0.0 | 0.8 | 0.8 | 35.5 | 37.0 | 203 | 4167 | $0.288 |
| markcrawl | 0.0 | 1.2 | 2.0 | 42.9 | 46.1 | 200 | 10115 | $0.109 |

### stripe-docs

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| crawl4ai-raw | 0.0 | 0.3 | 0.6 | 72.4 | 73.3 | 500 | 3564 | $0.053 |
| playwright | 0.0 | 4.7 | 6.0 | 67.6 | 78.4 | 500 | 30229 | $2.23 |
| colly+md | 0.0 | 5.0 | 6.2 | 69.4 | 80.6 | 499 | 31125 | $2.41 |
| scrapy+md | 0.0 | 1.8 | 2.6 | 76.8 | 81.3 | 500 | 14882 | $0.356 |
| crawl4ai | 0.0 | 0.2 | 0.4 | 82.3 | 82.9 | 500 | 2651 | $0.041 |
| markcrawl | 0.0 | 0.1 | 0.3 | 83.9 | 84.3 | 489 | 1904 | $0.032 |
| crawlee | 0.0 | 4.7 | 5.8 | 85.8 | 96.3 | 500 | 30214 | $2.23 |

## Key Findings

- **Fastest end-to-end:** markcrawl (440.7s total)
- **Slowest end-to-end:** crawl4ai (515.3s total)
- **markcrawl:** querying dominates at 98% of pipeline time
- **scrapy+md:** querying dominates at 96% of pipeline time
- **playwright:** querying dominates at 96% of pipeline time
- **Cheapest API cost:** markcrawl ($0.397)
- **Most expensive API cost:** colly+md ($3.82)

## Methodology

- **Scrape timing** comes from `benchmark_all_tools.py` run metadata
- **Chunk timing** uses markcrawl's `chunk_markdown()` with 400-word chunks and 50-word overlap
- **Embed timing** uses OpenAI `text-embedding-3-small` (cached after first run)
- **Query timing** includes embedding the query, cosine retrieval, and `gpt-4o-mini` answer generation
- **Cost tracking** counts actual tokens from API responses (embed tokens estimated via tiktoken, query tokens from response.usage)
- **Embedding cache** — chunks are cached by content hash; re-runs with unchanged pages.jsonl skip API calls entirely
- See [METHODOLOGY.md](METHODOLOGY.md) for full test setup

## See also

- [SPEED_COMPARISON.md](SPEED_COMPARISON.md) — raw crawl speed without pipeline overhead
- [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) — why chunk counts vary between tools
- [COST_AT_SCALE.md](COST_AT_SCALE.md) — what these per-run costs look like at scale
- [ANSWER_QUALITY.md](ANSWER_QUALITY.md) — whether answer quality differs despite similar pipeline costs
- [METHODOLOGY.md](METHODOLOGY.md) — full test setup
