# End-to-End RAG Pipeline Timing Benchmark
<!-- style: v2, 2026-04-12 -->

Measures how long each crawler takes across the full RAG pipeline:
scraping, chunking, embedding, and querying.

**Run:** `run_20260412_075832` | **Sites:** books-toscrape, fastapi-docs, python-docs, quotes-toscrape | **Embedding model:** text-embedding-3-small | **Answer model:** gpt-4o-mini

## Summary: Total Pipeline Time by Tool

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | **Total (s)** | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|--------------|-------|--------|------|
| colly+md | 62.7 | 1.1 | 5.2 | 190.6 | **259.6** | 728 | 17037 | $0.187 |
| scrapy+md | 73.3 | 0.6 | 3.6 | 190.5 | **268.0** | 556 | 14104 | $0.154 |
| **markcrawl** | 113.1 | 1.0 | 4.1 | 182.6 | **300.8** | 728 | 12901 | $0.162 |
| playwright | 168.5 | 1.5 | 5.4 | 160.9 | **336.3** | 728 | 17109 | $0.196 |
| crawl4ai | 162.8 | 0.8 | 4.1 | 176.8 | **344.6** | 728 | 17908 | $0.240 |
| crawlee | 201.5 | 1.2 | 5.1 | 176.9 | **384.7** | 728 | 17108 | $0.196 |
| crawl4ai-raw | 342.3 | 0.8 | 4.2 | 176.0 | **523.3** | 728 | 17908 | $0.240 |

*(Cost uses OpenAI `text-embedding-3-small` at $0.02/1M tokens, `gpt-4o-mini` at $0.15/$0.6 per 1M input/output tokens)*

## Per-Page Pipeline Cost (normalized)

Since scrapy+md fetched fewer pages (due to timeouts), this table normalizes
time and cost per page for a fairer comparison.

| Tool | Pages | Total (s) | s/page | Cost/page | Chunks/page |
|------|-------|----------|--------|-----------|-------------|
| colly+md | 728 | 259.6 | 0.36 | $0.0003 | 23.4 |
| scrapy+md | 556 | 268.0 | 0.48 | $0.0003 | 25.4 |
| **markcrawl** | 728 | 300.8 | 0.41 | $0.0002 | 17.7 |
| playwright | 728 | 336.3 | 0.46 | $0.0003 | 23.5 |
| crawl4ai | 728 | 344.6 | 0.47 | $0.0003 | 24.6 |
| crawlee | 728 | 384.7 | 0.53 | $0.0003 | 23.5 |
| crawl4ai-raw | 728 | 523.3 | 0.72 | $0.0003 | 24.6 |

## Phase Breakdown (% of Total Pipeline Time)

| Tool | Scrape % | Chunk % | Embed % | Query % |
|------|---------|--------|--------|--------|
| colly+md | 24.2% | 0.4% | 2.0% | 73.4% |
| scrapy+md | 27.4% | 0.2% | 1.3% | 71.1% |
| markcrawl | 37.6% | 0.3% | 1.4% | 60.7% |
| playwright | 50.1% | 0.5% | 1.6% | 47.8% |
| crawl4ai | 47.2% | 0.2% | 1.2% | 51.3% |
| crawlee | 52.4% | 0.3% | 1.3% | 46.0% |
| crawl4ai-raw | 65.4% | 0.1% | 0.8% | 33.6% |

## API Cost Breakdown

*(Pricing: `text-embedding-3-small` at $0.02/1M tokens, `gpt-4o-mini` input at $0.15/1M, output at $0.6/1M)*

| Tool | Embed tokens | Embed cost | Query in tokens | Query out tokens | Query cost | **Total cost** |
|------|-------------|-----------|----------------|-----------------|-----------|---------------|
| colly+md | 7,242,268 | $0.145 | 250,565 | 7,997 | $0.042 | **$0.187** |
| scrapy+md | 5,618,112 | $0.112 | 243,768 | 7,984 | $0.041 | **$0.154** |
| **markcrawl** | 6,187,564 | $0.124 | 223,139 | 8,169 | $0.038 | **$0.162** |
| playwright | 7,696,966 | $0.154 | 248,793 | 7,753 | $0.042 | **$0.196** |
| crawl4ai | 9,536,889 | $0.191 | 301,452 | 6,620 | $0.049 | **$0.240** |
| crawlee | 7,694,726 | $0.154 | 249,796 | 7,814 | $0.042 | **$0.196** |
| crawl4ai-raw | 9,536,790 | $0.191 | 301,450 | 6,566 | $0.049 | **$0.240** |

## Per-Site Breakdown

### books-toscrape

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| crawl4ai | 11.8 | 0.0 | 0.1 | 50.8 | 62.8 | 60 | 628 | $0.021 |
| **markcrawl** | 9.5 | 0.0 | 0.0 | 55.5 | 65.0 | 60 | 112 | $0.013 |
| playwright | 23.5 | 0.0 | 0.0 | 52.1 | 75.6 | 60 | 134 | $0.018 |
| scrapy+md | 4.6 | 0.0 | 0.0 | 71.0 | 75.7 | 60 | 130 | $0.018 |
| crawlee | 15.9 | 0.0 | 0.0 | 60.0 | 75.9 | 60 | 134 | $0.018 |
| crawl4ai-raw | 26.8 | 0.1 | 0.1 | 49.9 | 76.9 | 60 | 628 | $0.021 |
| colly+md | 5.9 | 0.0 | 0.0 | 73.4 | 79.4 | 60 | 134 | $0.018 |

### fastapi-docs

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| colly+md | 18.9 | 0.3 | 1.5 | 59.3 | 80.0 | 153 | 3869 | $0.035 |
| scrapy+md | 17.2 | 0.2 | 0.8 | 61.9 | 80.1 | 153 | 3739 | $0.031 |
| **markcrawl** | 30.0 | 0.1 | 0.8 | 54.0 | 84.8 | 153 | 3288 | $0.022 |
| crawl4ai | 60.0 | 0.2 | 1.0 | 49.7 | 110.9 | 153 | 4147 | $0.043 |
| playwright | 60.0 | 0.3 | 1.6 | 54.6 | 116.5 | 153 | 3857 | $0.041 |
| crawl4ai-raw | 119.8 | 0.1 | 0.8 | 51.0 | 171.7 | 153 | 4147 | $0.043 |
| crawlee | 125.7 | 0.4 | 1.0 | 53.8 | 180.8 | 153 | 3856 | $0.041 |

### python-docs

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| colly+md | 34.5 | 0.7 | 3.7 | 32.9 | 71.8 | 500 | 13006 | $0.123 |
| scrapy+md | 46.9 | 0.4 | 2.7 | 33.8 | 84.0 | 328 | 10210 | $0.094 |
| crawlee | 52.8 | 0.8 | 4.0 | 39.1 | 96.8 | 500 | 13090 | $0.126 |
| playwright | 79.5 | 1.2 | 3.8 | 35.5 | 120.0 | 500 | 13090 | $0.126 |
| **markcrawl** | 69.5 | 0.9 | 3.3 | 50.0 | 123.7 | 500 | 9477 | $0.117 |
| crawl4ai | 86.5 | 0.6 | 3.0 | 40.3 | 130.4 | 500 | 13110 | $0.162 |
| crawl4ai-raw | 186.7 | 0.5 | 3.2 | 36.6 | 227.1 | 500 | 13110 | $0.162 |

### quotes-toscrape

| Tool | Scrape (s) | Chunk (s) | Embed (s) | Query (s) | Total (s) | Pages | Chunks | Cost |
|------|-----------|----------|----------|----------|----------|-------|--------|------|
| playwright | 5.4 | 0.0 | 0.0 | 18.7 | 24.1 | 15 | 28 | $0.010 |
| **markcrawl** | 4.0 | 0.0 | 0.0 | 23.2 | 27.2 | 15 | 24 | $0.010 |
| scrapy+md | 4.6 | 0.0 | 0.0 | 23.7 | 28.3 | 15 | 25 | $0.011 |
| colly+md | 3.3 | 0.0 | 0.0 | 25.0 | 28.3 | 15 | 28 | $0.010 |
| crawlee | 7.1 | 0.0 | 0.0 | 24.0 | 31.1 | 15 | 28 | $0.010 |
| crawl4ai | 4.5 | 0.0 | 0.0 | 36.1 | 40.6 | 15 | 23 | $0.014 |
| crawl4ai-raw | 9.1 | 0.0 | 0.0 | 38.5 | 47.6 | 15 | 23 | $0.014 |

## Key Findings

- **Fastest end-to-end:** colly+md (259.6s total)
- **Slowest end-to-end:** crawl4ai-raw (523.3s total)
- **colly+md:** querying dominates at 73% of pipeline time
- **scrapy+md:** querying dominates at 71% of pipeline time
- **markcrawl:** querying dominates at 61% of pipeline time
- **Cheapest API cost:** colly+md ($0.187)
- **Most expensive API cost:** crawl4ai ($0.240)

## Methodology

- **Scrape timing** comes from `benchmark_all_tools.py` run metadata
- **Chunk timing** uses markcrawl's `chunk_markdown()` with 400-word chunks and 50-word overlap
- **Embed timing** uses OpenAI `text-embedding-3-small` (cached after first run)
- **Query timing** includes embedding the query, cosine retrieval, and `gpt-4o-mini` answer generation
- **Cost tracking** counts actual tokens from API responses (embed tokens estimated via tiktoken, query tokens from response.usage)
- **Embedding cache** — chunks are cached by content hash; re-runs with unchanged pages.jsonl skip API calls entirely
- See [METHODOLOGY.md](METHODOLOGY.md) for full test setup
