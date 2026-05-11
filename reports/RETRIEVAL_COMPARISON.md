# Retrieval Quality Comparison
<!-- style: v2, 2026-05-11 -->

Crawler choice barely matters for retrieval — retrieval mode matters more.

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


Does each tool's output produce embeddings that answer real questions?
This benchmark chunks each tool's crawl output, embeds it with
`text-embedding-3-small`, and measures retrieval across four modes:

- **Embedding**: Cosine similarity on OpenAI embeddings
- **BM25**: Keyword search (Okapi BM25)
- **Hybrid**: Embedding + BM25 fused via Reciprocal Rank Fusion
- **Reranked**: Hybrid candidates reranked by `cross-encoder/ms-marco-MiniLM-L-6-v2`

**557 queries** across 11 sites.
Hit rate = correct source page in top-K results. Higher is better.
Summary tables use the **495-query common subset** (9 sites) so all tools are compared on identical queries. Sites excluded: huggingface-transformers, newegg (not all tools have data). Per-site tables show full results.

## Quick summary: best retrieval mode per tool

For each tool, the mode with the highest MRR. Most readers can stop here.

| Tool | Best mode | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR | Page MRR |
|---|---|---|---|---|---|---|---|
| crawl4ai-raw | embedding | 70% (347/495) ±4% | 83% (409/495) ±3% | 87% (431/495) ±3% | 91% (450/495) ±3% | 0.777 | 0.791 |
| crawl4ai | embedding | 68% (339/495) ±4% | 82% (407/495) ±3% | 87% (429/495) ±3% | 90% (446/495) ±3% | 0.766 | 0.779 |
| playwright | embedding | 68% (337/495) ±4% | 81% (402/495) ±3% | 86% (424/495) ±3% | 90% (447/495) ±3% | 0.761 | 0.773 |
| crawlee | embedding | 67% (334/495) ±4% | 82% (405/495) ±3% | 86% (428/495) ±3% | 91% (448/495) ±3% | 0.758 | 0.769 |
| colly+md | embedding | 45% (223/495) ±4% | 53% (260/495) ±4% | 54% (267/495) ±4% | 55% (274/495) ±4% | 0.490 | 0.497 |
| markcrawl | hybrid | 23% (113/495) ±4% | 34% (169/495) ±4% | 36% (177/495) ±4% | 37% (184/495) ±4% | 0.287 | 0.290 |
| scrapy+md | reranked | 16% (81/495) ±3% | 19% (95/495) ±3% | 21% (103/495) ±4% | 22% (108/495) ±4% | 0.182 | 0.185 |

> **Column definitions:** **Best mode** = retrieval strategy that maximizes MRR for this tool. **Hit@K** = % of queries where the correct source page appeared in the top K (chunk-level). **MRR** (chunk-level) = Mean Reciprocal Rank across all retrieved chunks. **Page MRR** (DS-1) = MRR after collapsing chunks-per-URL to unique pages — removes the chunk-density gaming signal where a tool emitting more chunks per page would otherwise rank ahead at the same content.

> **Density sensitivity (DS-9):** Hit@1 is the LEAST chunk-density-sensitive (each chunk competes for one slot, so emitting more chunks doesn't help unless the first one is right). Hit@10 is the MOST sensitive (more chunks = more chances to land somewhere in the top 10). MRR sits between the two. Page MRR removes the density signal entirely — read it as the chunk-density-corrected MRR.

## Summary: retrieval modes compared

_Computed over 495 queries on 9 common sites (ikea, kubernetes-docs, mdn-css, postgres-docs, propublica, react-dev, rust-book, smittenkitchen, stripe-docs)._

| Tool | Mode | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Page MRR |
|---|---|---|---|---|---|---|---|---|
| crawl4ai-raw | embedding | 70% (347/495) ±4% | 83% (409/495) ±3% | 87% (431/495) ±3% | 91% (450/495) ±3% | 95% (468/495) ±2% | 0.777 | 0.791 |
| crawl4ai | embedding | 68% (339/495) ±4% | 82% (407/495) ±3% | 87% (429/495) ±3% | 90% (446/495) ±3% | 94% (463/495) ±2% | 0.766 | 0.779 |
| playwright | embedding | 68% (337/495) ±4% | 81% (402/495) ±3% | 86% (424/495) ±3% | 90% (447/495) ±3% | 93% (460/495) ±2% | 0.761 | 0.773 |
| crawlee | embedding | 67% (334/495) ±4% | 82% (405/495) ±3% | 86% (428/495) ±3% | 91% (448/495) ±3% | 93% (458/495) ±2% | 0.758 | 0.769 |
| colly+md | embedding | 45% (223/495) ±4% | 53% (260/495) ±4% | 54% (267/495) ±4% | 55% (274/495) ±4% | 57% (282/495) ±4% | 0.490 | 0.497 |
| markcrawl | embedding | 22% (108/495) ±4% | 31% (155/495) ±4% | 35% (174/495) ±4% | 38% (190/495) ±4% | 40% (198/495) ±4% | 0.276 | 0.283 |
| scrapy+md | embedding | 16% (79/495) ±3% | 20% (98/495) ±4% | 21% (105/495) ±4% | 22% (107/495) ±4% | 22% (111/495) ±4% | 0.182 | 0.182 |
| crawlee | bm25 | 46% (230/495) ±4% | 61% (302/495) ±4% | 67% (331/495) ±4% | 75% (371/495) ±4% | 81% (402/495) ±3% | 0.560 | 0.575 |
| crawl4ai-raw | bm25 | 45% (223/495) ±4% | 63% (311/495) ±4% | 69% (341/495) ±4% | 75% (373/495) ±4% | 81% (402/495) ±3% | 0.556 | 0.566 |
| crawl4ai | bm25 | 45% (225/495) ±4% | 62% (309/495) ±4% | 68% (338/495) ±4% | 75% (371/495) ±4% | 80% (397/495) ±4% | 0.555 | 0.565 |
| playwright | bm25 | 44% (220/495) ±4% | 60% (297/495) ±4% | 65% (324/495) ±4% | 74% (366/495) ±4% | 79% (392/495) ±4% | 0.542 | 0.557 |
| colly+md | bm25 | 26% (128/495) ±4% | 34% (170/495) ±4% | 39% (193/495) ±4% | 42% (207/495) ±4% | 46% (229/495) ±4% | 0.311 | 0.326 |
| markcrawl | bm25 | 18% (88/495) ±3% | 28% (139/495) ±4% | 31% (153/495) ±4% | 34% (168/495) ±4% | 37% (182/495) ±4% | 0.239 | 0.241 |
| scrapy+md | bm25 | 11% (54/495) ±3% | 15% (74/495) ±3% | 18% (89/495) ±3% | 20% (97/495) ±3% | 20% (101/495) ±4% | 0.138 | 0.140 |
| crawl4ai-raw | hybrid | 64% (319/495) ±4% | 84% (418/495) ±3% | 88% (437/495) ±3% | 94% (464/495) ±2% | 96% (476/495) ±2% | 0.753 | 0.763 |
| crawlee | hybrid | 66% (327/495) ±4% | 82% (404/495) ±3% | 87% (429/495) ±3% | 92% (457/495) ±2% | 94% (463/495) ±2% | 0.750 | 0.762 |
| playwright | hybrid | 65% (324/495) ±4% | 82% (407/495) ±3% | 87% (431/495) ±3% | 92% (456/495) ±2% | 94% (466/495) ±2% | 0.747 | 0.761 |
| crawl4ai | hybrid | 64% (317/495) ±4% | 84% (414/495) ±3% | 87% (432/495) ±3% | 92% (457/495) ±2% | 95% (472/495) ±2% | 0.746 | 0.756 |
| colly+md | hybrid | 40% (200/495) ±4% | 49% (245/495) ±4% | 52% (259/495) ±4% | 56% (278/495) ±4% | 58% (285/495) ±4% | 0.457 | 0.465 |
| markcrawl | hybrid | 23% (113/495) ±4% | 34% (169/495) ±4% | 36% (177/495) ±4% | 37% (184/495) ±4% | 39% (195/495) ±4% | 0.287 | 0.290 |
| scrapy+md | hybrid | 16% (78/495) ±3% | 19% (92/495) ±3% | 20% (98/495) ±4% | 22% (107/495) ±4% | 23% (112/495) ±4% | 0.176 | 0.180 |
| playwright | reranked | 65% (322/495) ±4% | 83% (409/495) ±3% | 87% (429/495) ±3% | 91% (448/495) ±3% | 94% (464/495) ±2% | 0.750 | 0.757 |
| crawl4ai-raw | reranked | 64% (319/495) ±4% | 82% (408/495) ±3% | 88% (437/495) ±3% | 93% (458/495) ±2% | 97% (480/495) ±2% | 0.748 | 0.756 |
| crawl4ai | reranked | 64% (317/495) ±4% | 82% (407/495) ±3% | 87% (433/495) ±3% | 92% (455/495) ±2% | 96% (475/495) ±2% | 0.743 | 0.751 |
| crawlee | reranked | 62% (309/495) ±4% | 80% (395/495) ±4% | 84% (414/495) ±3% | 87% (432/495) ±3% | 91% (449/495) ±3% | 0.720 | 0.728 |
| colly+md | reranked | 42% (209/495) ±4% | 52% (258/495) ±4% | 55% (270/495) ±4% | 57% (284/495) ±4% | 58% (287/495) ±4% | 0.478 | 0.483 |
| markcrawl | reranked | 23% (114/495) ±4% | 33% (163/495) ±4% | 36% (180/495) ±4% | 39% (193/495) ±4% | 40% (197/495) ±4% | 0.285 | 0.289 |
| scrapy+md | reranked | 16% (81/495) ±3% | 19% (95/495) ±3% | 21% (103/495) ±4% | 22% (108/495) ±4% | 23% (113/495) ±4% | 0.182 | 0.185 |

> **Column definitions:** **Hit@K** = percentage of queries where the correct source page appeared in the top K results (shown as % with raw counts). **MRR** (Mean Reciprocal Rank, chunk-level) = average of 1/rank for correct results across the chunk-ordered top-K (1.0 = always rank 1, 0.5 = always rank 2). **Page MRR** (DS-1, page-level) = MRR after collapsing multiple chunks per URL into a single rank — neutralises chunk-density inflation. Page MRR ≥ MRR by construction; the gap measures how much chunk-density was inflating the chunk-level number. **Mode** = retrieval strategy used (see definitions above).

## Summary: embedding-only (hit rate at multiple K values)

_Computed over 495 queries on 9 common sites._

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Avg words |
|---|---|---|---|---|---|---|---|---|
| crawl4ai-raw | 70% (347/495) ±4% | 83% (409/495) ±3% | 87% (431/495) ±3% | 91% (450/495) ±3% | 95% (468/495) ±2% | 0.777 | 25245 | 344 |
| crawl4ai | 68% (339/495) ±4% | 82% (407/495) ±3% | 87% (429/495) ±3% | 90% (446/495) ±3% | 94% (463/495) ±2% | 0.766 | 24400 | 345 |
| playwright | 68% (337/495) ±4% | 81% (402/495) ±3% | 86% (424/495) ±3% | 90% (447/495) ±3% | 93% (460/495) ±2% | 0.761 | 56855 | 382 |
| crawlee | 67% (334/495) ±4% | 82% (405/495) ±3% | 86% (428/495) ±3% | 91% (448/495) ±3% | 93% (458/495) ±2% | 0.758 | 58912 | 382 |
| colly+md | 45% (223/495) ±4% | 53% (260/495) ±4% | 54% (267/495) ±4% | 55% (274/495) ±4% | 57% (282/495) ±4% | 0.490 | 59078 | 385 |
| markcrawl | 22% (108/495) ±4% | 31% (155/495) ±4% | 35% (174/495) ±4% | 38% (190/495) ±4% | 40% (198/495) ±4% | 0.276 | 27193 | 334 |
| scrapy+md | 16% (79/495) ±3% | 20% (98/495) ±4% | 21% (105/495) ±4% | 22% (107/495) ±4% | 22% (111/495) ±4% | 0.182 | 46141 | 364 |

> **Column definitions:** **Hit@K** = correct source page in top K results. **MRR** = Mean Reciprocal Rank (1/rank of correct result, averaged). **Chunks** = total chunks produced by this tool (across all pages in common sites). **Avg words** = mean words per chunk.

## What this means

Tools span MRR 0.182-0.777 on embedding mode (a 0.596 spread). Tools crawl similar pages from the same seed URLs, and we apply identical chunking and embedding pipelines, but extraction differences -- see [content quality](QUALITY_COMPARISON.md) -- show up at retrieval time.

**Retrieval mode matters more than crawler choice.** Embedding search beats BM25 by roughly 2x on MRR across all tools. Hybrid and reranked modes fall between the two. Choosing the right retrieval strategy will improve your RAG pipeline far more than switching crawlers.

**The noise-vs-recall trade-off.** Noisier tools (crawlee, playwright) have slightly higher hit rates, but they produce 2x the chunks of leaner tools (markcrawl, scrapy+md). More chunks means higher embedding and storage costs with diminishing retrieval returns. See [COST_AT_SCALE.md](COST_AT_SCALE.md) for the dollar impact.

**For most use cases, pick your crawler based on speed and cost, not retrieval quality.** The differences here are within confidence intervals. Where crawler choice _does_ matter is content quality and downstream answer quality -- see [ANSWER_QUALITY.md](ANSWER_QUALITY.md).

## huggingface-transformers

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 100% (4/4) | 100% (4/4) | 100% (4/4) | 100% (4/4) | 100% (4/4) | 1.000 | 4518 | 300 |
| crawl4ai-raw | 100% (4/4) | 100% (4/4) | 100% (4/4) | 100% (4/4) | 100% (4/4) | 1.000 | 1018 | 295 |
| crawlee | 100% (4/4) | 100% (4/4) | 100% (4/4) | 100% (4/4) | 100% (4/4) | 1.000 | 67 | 16 |
| playwright | 100% (4/4) | 100% (4/4) | 100% (4/4) | 100% (4/4) | 100% (4/4) | 1.000 | 356 | 300 |
| scrapy+md | 50% (2/4) | 50% (2/4) | 50% (2/4) | 50% (2/4) | 50% (2/4) | 0.510 | 6346 | 240 |
| crawl4ai | — | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — | — |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for huggingface-transformers</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is the command to install Transformers using uv?**
*(expects URL containing: `installation`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | huggingface.co/docs/transformers/installation | 0.621 | huggingface.co/docs/transformers/v5.8.0/en/install | 0.621 | huggingface.co/docs/transformers/installation | 0.531 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | #1 | huggingface.co/docs/transformers/installation | 0.626 | huggingface.co/docs/transformers/installation | 0.516 | huggingface.co/docs/transformers/installation | 0.460 |
| scrapy+md | #24 | huggingface.co/docs/transformers/index | 0.492 | huggingface.co/docs/transformers/index | 0.464 | huggingface.co/DavidAU/Qwen3.5-9B-Claude-4.6-Opus- | 0.443 |
| crawlee | #1 | huggingface.co/docs/transformers/installation | 0.659 | huggingface.co/docs/transformers/installation | 0.622 | huggingface.co/docs/transformers/installation | 0.504 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | huggingface.co/docs/transformers/installation | 0.659 | huggingface.co/docs/transformers/installation | 0.621 | huggingface.co/docs/transformers/installation | 0.504 |


**Q2: How can I set up Transformers for offline usage?**
*(expects URL containing: `installation`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | huggingface.co/docs/transformers/installation | 0.584 | huggingface.co/docs/transformers/v5.8.0/en/install | 0.584 | huggingface.co/docs/transformers/main/en/big_model | 0.520 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | #1 | huggingface.co/docs/transformers/installation | 0.598 | huggingface.co/docs/transformers/index | 0.519 | huggingface.co/docs/transformers/index | 0.487 |
| scrapy+md | miss | huggingface.co/docs/transformers/index | 0.538 | huggingface.co/docs/transformers/index | 0.506 | huggingface.co/docs/transformers/trainer | 0.487 |
| crawlee | #1 | huggingface.co/docs/transformers/installation | 0.519 | huggingface.co/docs/transformers/installation | 0.515 | huggingface.co/docs/transformers/index | 0.502 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | huggingface.co/docs/transformers/installation | 0.526 | huggingface.co/docs/transformers/index | 0.526 | huggingface.co/docs/transformers/installation | 0.519 |


**Q3: What are the main design principles of Transformers?**
*(expects URL containing: `transformers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | huggingface.co/docs/transformers/philosophy | 0.521 | huggingface.co/docs/transformers/v5.8.0/en/philoso | 0.521 | huggingface.co/docs/transformers/v5.8.0/en/index | 0.518 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | #1 | huggingface.co/docs/transformers/index | 0.526 | huggingface.co/docs/transformers/index | 0.522 | huggingface.co/docs/transformers/index | 0.429 |
| scrapy+md | #1 | huggingface.co/docs/transformers/index | 0.538 | huggingface.co/docs/transformers/philosophy | 0.530 | huggingface.co/docs/transformers/index | 0.500 |
| crawlee | #1 | huggingface.co/docs/transformers/index | 0.501 | huggingface.co/docs/transformers/index | 0.479 | huggingface.co/docs/transformers/index | 0.414 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | huggingface.co/docs/transformers/index | 0.521 | huggingface.co/docs/transformers/index | 0.482 | huggingface.co/docs/transformers/quicktour | 0.441 |


**Q4: What features does Transformers provide for inference or training?**
*(expects URL containing: `transformers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | huggingface.co/docs/transformers/index | 0.627 | huggingface.co/docs/transformers/v5.8.0/en/index | 0.627 | huggingface.co/docs/transformers/v5.8.0/en/main_cl | 0.624 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | #1 | huggingface.co/docs/transformers/index | 0.661 | huggingface.co/docs/transformers/index | 0.603 | huggingface.co/docs/transformers/index | 0.581 |
| scrapy+md | #1 | huggingface.co/docs/transformers/index | 0.644 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.615 | huggingface.co/docs/transformers/index | 0.607 |
| crawlee | #1 | huggingface.co/docs/transformers/index | 0.662 | huggingface.co/docs/transformers/index | 0.571 | huggingface.co/docs/transformers/index | 0.568 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | huggingface.co/docs/transformers/index | 0.634 | huggingface.co/docs/transformers/quicktour | 0.601 | huggingface.co/docs/transformers/index | 0.598 |


</details>

## ikea

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai-raw | 68% (41/60) | 77% (46/60) | 83% (50/60) | 90% (54/60) | 98% (59/60) | 0.753 | 1554 | 200 |
| crawl4ai | 60% (36/60) | 77% (46/60) | 80% (48/60) | 87% (52/60) | 93% (56/60) | 0.700 | 1622 | 200 |
| crawlee | 58% (35/60) | 65% (39/60) | 75% (45/60) | 82% (49/60) | 82% (49/60) | 0.643 | 4610 | 203 |
| playwright | 52% (31/60) | 63% (38/60) | 65% (39/60) | 73% (44/60) | 75% (45/60) | 0.586 | 3308 | 200 |
| colly+md | 33% (20/60) | 42% (25/60) | 43% (26/60) | 47% (28/60) | 47% (28/60) | 0.384 | 2942 | 200 |
| markcrawl | 25% (15/60) | 32% (19/60) | 32% (19/60) | 35% (21/60) | 37% (22/60) | 0.284 | 928 | 200 |
| scrapy+md | 12% (7/60) | 12% (7/60) | 12% (7/60) | 12% (7/60) | 12% (7/60) | 0.117 | 1107 | 194 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for ikea</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is the price of the NÄSINGE extendable table?**
*(expects URL containing: `furniture-fu001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #14 | www.ikea.com/us/en/cat/outdoor-patio-furniture-od0 | 0.503 | www.ikea.com/us/en/cat/tables-chairs-fu002/ | 0.503 | www.ikea.com/us/en/cat/outdoor-patio-furniture-od0 | 0.500 |
| crawl4ai | #23 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.741 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.725 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.648 |
| crawl4ai-raw | #20 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.741 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.725 | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.676 |
| scrapy+md | #28 | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.595 | www.ikea.com/us/en/cat/dining-tables-21825/ | 0.583 | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.568 |
| crawlee | #8 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.709 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.659 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.655 |
| colly+md | miss | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.586 | www.ikea.com/us/en/cat/dining-tables-21825/ | 0.583 | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.581 |
| playwright | #50 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.708 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.659 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.656 |


**Q2: What features does the STORKLINTA series offer?**
*(expects URL containing: `furniture-fu001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #6 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.460 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.459 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.445 |
| crawl4ai | #12 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-w | 0.525 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.524 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.523 |
| crawl4ai-raw | #14 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-w | 0.525 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.524 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.523 |
| scrapy+md | #1 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.429 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.380 | www.ikea.com/us/en/cat/patar-series-36839/ | 0.380 |
| crawlee | #1 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.506 | www.ikea.com/us/en/cat/furniture-fu001/?page=2#pro | 0.506 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.493 |
| colly+md | miss | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.493 | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.491 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.485 |
| playwright | #22 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.493 | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.491 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.466 |


**Q3: What is the height and diameter of the PÅDRAG vase?**
*(expects URL containing: `padrag-vase-clear-glass-10470991`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/vases-10776/ | 0.472 | www.ikea.com/us/en/p/stockholm-2025-vase-black-105 | 0.463 | www.ikea.com/us/en/cat/vases-bowls-10769/ | 0.462 |
| crawl4ai | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.665 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.607 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.603 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.604 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.593 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.557 |
| scrapy+md | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.665 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.475 | www.ikea.com/us/en/p/godmiddag-serving-plate-white | 0.458 |
| crawlee | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.665 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.575 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.560 |
| colly+md | miss | www.ikea.com/us/en/rooms/dining/ | 0.375 | www.ikea.com/us/en/cat/outdoor-pots-plants-31787/ | 0.374 | www.ikea.com/us/en/cat/outdoor-pots-plants-31787/ | 0.360 |
| playwright | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.665 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.575 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.560 |


**Q4: Who is the designer of the PÅDRAG vase?**
*(expects URL containing: `padrag-vase-clear-glass-10470991`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/vases-10776/ | 0.493 | www.ikea.com/us/en/cat/vases-10776/ | 0.491 | www.ikea.com/us/en/cat/vases-bowls-10769/ | 0.490 |
| crawl4ai | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.701 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.642 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.640 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.640 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.627 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.594 |
| scrapy+md | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.697 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.541 | www.ikea.com/us/en/p/skogstundra-vase-light-blue-0 | 0.538 |
| crawlee | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.697 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.629 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.580 |
| colly+md | miss | www.ikea.com/us/en/cat/outdoor-pots-plants-31787/ | 0.422 | www.ikea.com/us/en/rooms/dining/ | 0.407 | www.ikea.com/us/en/p/perjohan-stool-with-storage-p | 0.406 |
| playwright | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.697 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.629 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.580 |


**Q5: What are the different types of ottomans available at IKEA?**
*(expects URL containing: `ottomans-20926`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.666 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.658 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.656 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.670 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.657 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.657 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.669 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.659 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.658 |
| scrapy+md | miss | www.ikea.com/us/en/p/strandmon-slipcover-for-armch | 0.558 | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.539 | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.535 |
| crawlee | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.701 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.670 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.625 |
| colly+md | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.641 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.628 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.626 |
| playwright | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.701 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.616 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.606 |


**Q6: What is the price of the FÖRLUNDA Pouffe?**
*(expects URL containing: `ottomans-20926`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.544 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.537 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.528 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.585 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.570 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.548 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.605 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.568 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.548 |
| scrapy+md | miss | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.510 | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.485 | www.ikea.com/us/en/cat/nytillverkad-collection-620 | 0.484 |
| crawlee | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.578 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.529 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.522 |
| colly+md | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.581 | www.ikea.com/us/en/cat/sleeper-sofas-10663/ | 0.528 | www.ikea.com/us/en/cat/sleeper-sofas-10663/ | 0.524 |
| playwright | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.522 | www.ikea.com/us/en/cat/stockholm-collection-11989/ | 0.504 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.489 |


**Q7: How many points do IKEA Family members collect for every $1 spent?**
*(expects URL containing: `rewards`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.789 | www.ikea.com/us/en/customer-service/terms-conditio | 0.768 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.755 |
| crawl4ai | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.758 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.753 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.751 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.758 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.753 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.751 |
| scrapy+md | miss | www.ikea.com/us/en/customer-service/ikea-family-te | 0.790 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.754 | www.ikea.com/us/en/ikea-family/?itm_campaign=assur | 0.751 |
| crawlee | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.757 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.734 | www.ikea.com/us/en/ikea-family/ | 0.725 |
| colly+md | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.757 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.735 | www.ikea.com/us/en/ikea-family/ | 0.725 |
| playwright | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.757 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.735 | www.ikea.com/us/en/ikea-family/ | 0.726 |


**Q8: What actions can earn you points in the IKEA Family rewards program?**
*(expects URL containing: `rewards`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.816 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.785 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.785 |
| crawl4ai | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.815 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.781 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.781 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.815 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.782 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.780 |
| scrapy+md | miss | www.ikea.com/us/en/customer-service/ikea-family-te | 0.816 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.785 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.754 |
| crawlee | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.791 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.758 | www.ikea.com/us/en/ikea-family/ | 0.743 |
| colly+md | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.791 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.759 | www.ikea.com/us/en/ikea-family/ | 0.743 |
| playwright | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.791 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.759 | www.ikea.com/us/en/ikea-family/ | 0.743 |


**Q9: What is the current offer for IKEA Family members on points collection?**
*(expects URL containing: `offers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #9 | www.ikea.com/us/en/ikea-family/ | 0.780 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.774 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.764 |
| crawl4ai | #11 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.769 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.753 | www.ikea.com/us/en/ikea-family/benefits/ | 0.749 |
| crawl4ai-raw | #11 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.769 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.753 | www.ikea.com/us/en/ikea-family/benefits/ | 0.749 |
| scrapy+md | miss | www.ikea.com/us/en/ikea-family/?itm_campaign=assur | 0.781 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.774 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.761 |
| crawlee | #7 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.777 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.762 | www.ikea.com/us/en/ikea-family/ | 0.753 |
| colly+md | #6 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.777 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.762 | www.ikea.com/us/en/ikea-family/ | 0.753 |
| playwright | #7 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.777 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.762 | www.ikea.com/us/en/ikea-family/ | 0.753 |


**Q10: What discounts are available on sofas and sectionals?**
*(expects URL containing: `offers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | www.ikea.com/us/en/rooms/living-room/ | 0.570 | www.ikea.com/us/en/offers/ | 0.558 | www.ikea.com/us/en/ | 0.518 |
| crawl4ai | #3 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.577 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.568 | www.ikea.com/us/en/offers/family-offers/ | 0.567 |
| crawl4ai-raw | #3 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.577 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.568 | www.ikea.com/us/en/offers/family-offers/?filters=f | 0.567 |
| scrapy+md | miss | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.480 | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.468 | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.461 |
| crawlee | #4 | www.ikea.com/us/en/cat/sleeper-sofas-10663/ | 0.592 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.587 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.568 |
| colly+md | #5 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.591 | www.ikea.com/us/en/cat/sleeper-sofas-10663/ | 0.578 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.570 |
| playwright | #1 | www.ikea.com/us/en/offers/family-offers/?filters=f | 0.603 | www.ikea.com/us/en/offers/family-offers/?filters=f | 0.603 | www.ikea.com/us/en/offers/family-offers/ | 0.603 |


**Q11: What warranty is offered for SEKTION kitchens?**
*(expects URL containing: `sektion-kitchen-ka005`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/customer-service/returns-claims | 0.605 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.489 | www.ikea.com/us/en/cat/tables-chairs-fu002/ | 0.451 |
| crawl4ai | #3 | www.ikea.com/us/en/customer-service/returns-claims | 0.673 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.659 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.593 |
| crawl4ai-raw | #10 | www.ikea.com/us/en/customer-service/returns-claims | 0.673 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.659 | www.ikea.com/us/en/customer-service/returns-claims | 0.587 |
| scrapy+md | miss | www.ikea.com/us/en/p/mittzon-frame-w-castors-disp- | 0.493 | www.ikea.com/us/en/p/faxaelven-mirror-cabinet-w-bu | 0.478 | www.ikea.com/us/en/p/mittzon-desk-white-s99513954/ | 0.460 |
| crawlee | #3 | www.ikea.com/us/en/customer-service/returns-claims | 0.662 | www.ikea.com/us/en/customer-service/returns-claims | 0.596 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.585 |
| colly+md | #2 | www.ikea.com/us/en/customer-service/returns-claims | 0.662 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.620 | www.ikea.com/us/en/customer-service/returns-claims | 0.596 |
| playwright | #4 | www.ikea.com/us/en/customer-service/returns-claims | 0.662 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.657 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.637 |


**Q12: What types of products are included in the SEKTION kitchen system?**
*(expects URL containing: `sektion-kitchen-ka005`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/planners/ | 0.501 | www.ikea.com/us/en/cat/cookware-tableware-kt001/ | 0.498 | www.ikea.com/us/en/cat/cookware-tableware-kt001/ | 0.483 |
| crawl4ai | #2 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.656 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.637 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.601 |
| crawl4ai-raw | #2 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.656 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.608 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.601 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.494 | www.ikea.com/us/en/campaigns/ikea-binging-with-bab | 0.477 | www.ikea.com/us/en/p/laektare-chair-cover-gunnared | 0.473 |
| crawlee | #1 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.723 | www.ikea.com/us/en/cat/kitchen-cabinets-700292/ | 0.641 | www.ikea.com/us/en/cat/kitchens-ka003/ | 0.604 |
| colly+md | #2 | www.ikea.com/us/en/cat/kitchen-cabinets-700292/ | 0.639 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.622 | www.ikea.com/us/en/cat/kitchens-ka003/ | 0.603 |
| playwright | #1 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.723 | www.ikea.com/us/en/cat/kitchen-cabinets-700292/ | 0.648 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.618 |


**Q13: What are the dimensions of the STORKLINTA 4-drawer dresser?**
*(expects URL containing: `storklinta-4-drawer-dresser-oak-effect-anchor-unlock-function-20559290`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.676 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.587 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.578 |
| crawl4ai | #2 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.684 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.673 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.670 |
| crawl4ai-raw | #2 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.684 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.673 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.670 |
| scrapy+md | miss | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.560 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.555 | www.ikea.com/us/en/cat/patar-series-36839/ | 0.541 |
| crawlee | #4 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.682 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.664 | www.ikea.com/us/en/p/storklinta-nightstand-dark-br | 0.659 |
| colly+md | miss | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.682 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.664 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.656 |
| playwright | miss | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.634 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.632 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.628 |


**Q14: What safety feature does the STORKLINTA 4-drawer dresser include to reduce tip-over risk?**
*(expects URL containing: `storklinta-4-drawer-dresser-oak-effect-anchor-unlock-function-20559290`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.692 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.601 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.577 |
| crawl4ai | #1 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.637 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.634 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.629 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.637 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.634 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.629 |
| scrapy+md | miss | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.555 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.551 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.471 |
| crawlee | #2 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.629 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.626 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.624 |
| colly+md | miss | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.629 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.626 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.624 |
| playwright | miss | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.614 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.606 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.602 |


**Q15: What are some tips for organizing a dresser?**
*(expects URL containing: `5-tidy-tips-how-to-organize-a-dresser-pub64488700`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.729 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.610 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.605 |
| crawl4ai | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.711 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.620 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.598 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.711 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.620 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.598 |
| scrapy+md | miss | www.ikea.com/us/en/cat/basket-drawer-units-46081/ | 0.565 | www.ikea.com/us/en/cat/basket-drawer-units-46081/ | 0.551 | www.ikea.com/us/en/cat/makeup-vanities-dressing-ta | 0.492 |
| crawlee | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.705 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.674 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.645 |
| colly+md | miss | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.724 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.667 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.595 |
| playwright | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.724 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.705 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.595 |


**Q16: How can I use clothes boxes to keep items ordered in a dresser?**
*(expects URL containing: `5-tidy-tips-how-to-organize-a-dresser-pub64488700`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.616 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.586 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.559 |
| crawl4ai | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.608 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.602 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.595 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.608 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.602 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.595 |
| scrapy+md | miss | www.ikea.com/us/en/cat/basket-drawer-units-46081/ | 0.473 | www.ikea.com/us/en/cat/basket-drawer-units-46081/ | 0.461 | www.ikea.com/us/en/cat/cube-storage-55012/ | 0.436 |
| crawlee | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.633 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.627 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.565 |
| colly+md | miss | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.637 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.533 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.532 |
| playwright | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.637 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.565 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.531 |


**Q17: What are the dimensions of the DYTÅG curtains?**
*(expects URL containing: `dytag-curtains-1-pair-white-with-heading-tape-00466715`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/customer-service/product-suppor | 0.425 | www.ikea.com/us/en/customer-service/product-suppor | 0.407 | www.ikea.com/us/en/p/valtorp-bench-with-storage-sa | 0.384 |
| crawl4ai | #1 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.663 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.626 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.606 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.676 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.626 | www.ikea.com/us/en/cat/curtains-10700/ | 0.594 |
| scrapy+md | miss | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.432 | www.ikea.com/us/en/p/mittzon-frame-w-cstrs-clths-r | 0.431 | www.ikea.com/us/en/p/vinterfint-pre-cut-fabric-chr | 0.429 |
| crawlee | #1 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.653 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.636 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.618 |
| colly+md | miss | www.ikea.com/us/en/cat/curtains-10700/ | 0.532 | www.ikea.com/us/en/cat/curtains-10700/ | 0.485 | www.ikea.com/us/en/cat/curtains-10700/ | 0.461 |
| playwright | miss | www.ikea.com/us/en/cat/curtains-10700/ | 0.542 | www.ikea.com/us/en/cat/curtains-10700/ | 0.505 | www.ikea.com/us/en/cat/curtains-10700/ | 0.499 |


**Q18: What material are the DYTÅG curtains made of?**
*(expects URL containing: `dytag-curtains-1-pair-white-with-heading-tape-00466715`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/inndyr-storage-bench-nordvall | 0.454 | www.ikea.com/us/en/customer-service/product-suppor | 0.434 | www.ikea.com/us/en/customer-service/product-suppor | 0.427 |
| crawl4ai | #1 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.662 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.651 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.645 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.662 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.647 | www.ikea.com/us/en/cat/curtains-10700/ | 0.641 |
| scrapy+md | miss | www.ikea.com/us/en/p/klippbraecka-pre-cut-fabric-w | 0.484 | www.ikea.com/us/en/p/klippbraecka-pre-cut-fabric-w | 0.481 | www.ikea.com/us/en/p/vinterfint-pre-cut-fabric-chr | 0.462 |
| crawlee | #1 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.686 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.672 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.662 |
| colly+md | miss | www.ikea.com/us/en/cat/curtains-10700/ | 0.564 | www.ikea.com/us/en/cat/curtains-10700/ | 0.492 | www.ikea.com/us/en/cat/curtains-10700/ | 0.482 |
| playwright | miss | www.ikea.com/us/en/cat/curtains-10700/ | 0.573 | www.ikea.com/us/en/cat/curtains-10700/ | 0.553 | www.ikea.com/us/en/cat/curtains-10700/ | 0.528 |


**Q19: What types of refrigerators does IKEA offer?**
*(expects URL containing: `fridges-freezers-20822`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/ideas/tips-for-more-sustainable | 0.562 | www.ikea.com/us/en/ | 0.545 | www.ikea.com/us/en/ikea-business/network/ | 0.523 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.692 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.680 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.670 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.701 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.688 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.670 |
| scrapy+md | miss | www.ikea.com/us/en/p/ikea-365-food-container-with- | 0.529 | www.ikea.com/us/en/cat/ikea-365-food-storage-49524 | 0.528 | www.ikea.com/us/en/p/ikea-365-food-storage-basket- | 0.526 |
| crawlee | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.731 | www.ikea.com/us/en/cat/products-products/ | 0.660 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.649 |
| colly+md | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.659 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.657 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.621 |
| playwright | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.731 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.666 | www.ikea.com/us/en/cat/products-products/ | 0.660 |


**Q20: How can I ensure my new fridge fits in my kitchen space?**
*(expects URL containing: `fridges-freezers-20822`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/ideas/tips-for-more-sustainable | 0.429 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.419 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.390 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.641 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.606 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.570 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.641 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.606 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.560 |
| scrapy+md | miss | www.ikea.com/us/en/cat/dishwashers-20825/ | 0.427 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.419 | www.ikea.com/us/en/cat/dishwashers-20825/ | 0.416 |
| crawlee | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.634 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.588 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.556 |
| colly+md | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.618 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.607 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.596 |
| playwright | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.634 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.588 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.548 |


**Q21: What is the range of values for IKEA Gift Cards?**
*(expects URL containing: `gift-cards-pub3d1efe50`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.662 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.633 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.632 |
| crawl4ai | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.627 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.621 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.615 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.627 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.621 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.615 |
| scrapy+md | miss | www.ikea.com/us/en/customer-service/ikea-family-te | 0.576 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.568 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.555 |
| crawlee | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.662 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.633 | www.ikea.com/us/en/customer-service/faq/ | 0.616 |
| colly+md | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.662 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.635 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.633 |
| playwright | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.662 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.633 | www.ikea.com/us/en/customer-service/faq/ | 0.616 |


**Q22: How can I check the balance of my IKEA Gift Card?**
*(expects URL containing: `gift-cards-pub3d1efe50`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.717 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.709 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.700 |
| crawl4ai | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.812 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.718 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.685 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.812 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.718 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.685 |
| scrapy+md | miss | www.ikea.com/us/en/customer-service/ikea-family-te | 0.573 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.572 | www.ikea.com/us/en/customer-service/services/finan | 0.571 |
| crawlee | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.750 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.717 | www.ikea.com/us/en/customer-service/faq/ | 0.667 |
| colly+md | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.716 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.709 | www.ikea.com/us/en/customer-service/faq/ | 0.667 |
| playwright | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.717 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.684 | www.ikea.com/us/en/customer-service/faq/ | 0.667 |


**Q23: What is the price of the SNIGLAR Crib?**
*(expects URL containing: `baby-kids-bc001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/customer-service/product-suppor | 0.458 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.400 | www.ikea.com/us/en/customer-service/product-suppor | 0.398 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.499 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.487 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.439 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.499 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.487 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.439 |
| scrapy+md | miss | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.384 | www.ikea.com/us/en/cat/hemnes-bedroom-series-58619 | 0.382 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.379 |
| crawlee | miss | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.419 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.411 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-w | 0.410 |
| colly+md | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-w | 0.419 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.419 | www.ikea.com/us/en/p/storklinta-nightstand-gray-gr | 0.419 |
| playwright | #1 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.506 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.432 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.418 |


**Q24: What materials are used in children's mattresses at IKEA?**
*(expects URL containing: `baby-kids-bc001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/customer-service/product-suppor | 0.597 | www.ikea.com/us/en/customer-service/product-suppor | 0.573 | www.ikea.com/us/en/p/inndyr-storage-bench-nordvall | 0.564 |
| crawl4ai | #4 | www.ikea.com/us/en/customer-service/faq/ | 0.647 | www.ikea.com/us/en/cat/beds-bm003/ | 0.621 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.617 |
| crawl4ai-raw | #4 | www.ikea.com/us/en/customer-service/faq/ | 0.647 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.624 | www.ikea.com/us/en/cat/beds-bm003/ | 0.621 |
| scrapy+md | miss | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.606 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.589 | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.549 |
| crawlee | miss | www.ikea.com/us/en/cat/products-products/ | 0.601 | www.ikea.com/us/en/p/mammut-childrens-chair-indoor | 0.599 | www.ikea.com/us/en/p/mammut-childrens-chair-indoor | 0.599 |
| colly+md | miss | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.647 | www.ikea.com/us/en/cat/mattresses-bm002/ | 0.637 | www.ikea.com/us/en/cat/mattress-bases-24825/ | 0.625 |
| playwright | #2 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.694 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.653 | www.ikea.com/us/en/cat/home-textiles-tl001/ | 0.618 |


**Q25: What types of storage solutions are included in the BRIMNES series?**
*(expects URL containing: `brimnes-series-700496`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.580 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.572 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.556 |
| crawl4ai | #2 | www.ikea.com/us/en/p/brimnes-bookcase-black-403012 | 0.639 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.638 | www.ikea.com/us/en/p/brimnes-bookcase-white-903012 | 0.634 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.658 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.645 | www.ikea.com/us/en/p/brimnes-bookcase-black-403012 | 0.641 |
| scrapy+md | miss | www.ikea.com/us/en/cat/hemnes-bedroom-series-58619 | 0.576 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.573 | www.ikea.com/us/en/cat/hemnes-bedroom-series-58619 | 0.559 |
| crawlee | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.776 | www.ikea.com/us/en/p/brimnes-bookcase-black-403012 | 0.683 | www.ikea.com/us/en/p/brimnes-bookcase-white-903012 | 0.675 |
| colly+md | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.666 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.644 | www.ikea.com/us/en/p/brimnes-bookcase-white-903012 | 0.625 |
| playwright | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.776 | www.ikea.com/us/en/cat/besta-storage-system-46053/ | 0.632 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.619 |


**Q26: How many items are available in the BRIMNES series?**
*(expects URL containing: `brimnes-series-700496`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.552 | www.ikea.com/us/en/rooms/bedroom/ | 0.546 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.543 |
| crawl4ai | #2 | www.ikea.com/us/en/p/brimnes-bookcase-black-403012 | 0.654 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.652 | www.ikea.com/us/en/p/brimnes-bookcase-white-903012 | 0.644 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.701 | www.ikea.com/us/en/p/brimnes-bookcase-black-403012 | 0.655 | www.ikea.com/us/en/p/brimnes-bookcase-black-403012 | 0.653 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.602 | www.ikea.com/us/en/cat/hemnes-bedroom-series-58619 | 0.590 | www.ikea.com/us/en/cat/hemnes-bedroom-series-58619 | 0.588 |
| crawlee | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.792 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.683 | www.ikea.com/us/en/p/brimnes-bookcase-black-403012 | 0.660 |
| colly+md | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.683 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.679 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.641 |
| playwright | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.792 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.654 | www.ikea.com/us/en/cat/gullaberg-series-700613/ | 0.590 |


**Q27: What personal data do we collect from parents using Småland?**
*(expects URL containing: `ikea-smaland-privacy-notice-pubf7ed5e70`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.654 | www.ikea.com/us/en/customer-service/privacy-policy | 0.454 | www.ikea.com/us/en/customer-service/privacy-policy | 0.435 |
| crawl4ai | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.712 | www.ikea.com/us/en/customer-service/privacy-policy | 0.627 | www.ikea.com/us/en/customer-service/privacy-policy | 0.624 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.712 | www.ikea.com/us/en/customer-service/privacy-policy | 0.627 | www.ikea.com/us/en/customer-service/privacy-policy | 0.624 |
| scrapy+md | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.631 | www.ikea.com/us/en/customer-service/privacy-policy | 0.624 | www.ikea.com/us/en/customer-service/privacy-policy | 0.622 |
| crawlee | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.656 | www.ikea.com/us/en/customer-service/privacy-policy | 0.631 | www.ikea.com/us/en/customer-service/privacy-policy | 0.622 |
| colly+md | miss | www.ikea.com/us/en/customer-service/privacy-policy | 0.656 | www.ikea.com/us/en/customer-service/privacy-policy | 0.631 | www.ikea.com/us/en/customer-service/privacy-policy | 0.623 |
| playwright | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.656 | www.ikea.com/us/en/customer-service/privacy-policy | 0.631 | www.ikea.com/us/en/customer-service/privacy-policy | 0.622 |


**Q28: How long does IKEA retain personal data provided in connection with Småland?**
*(expects URL containing: `ikea-smaland-privacy-notice-pubf7ed5e70`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.719 | www.ikea.com/us/en/customer-service/privacy-policy | 0.610 | www.ikea.com/us/en/customer-service/privacy-policy | 0.604 |
| crawl4ai | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.726 | www.ikea.com/us/en/customer-service/privacy-policy | 0.714 | www.ikea.com/us/en/customer-service/privacy-policy | 0.702 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.726 | www.ikea.com/us/en/customer-service/privacy-policy | 0.714 | www.ikea.com/us/en/customer-service/privacy-policy | 0.702 |
| scrapy+md | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.723 | www.ikea.com/us/en/customer-service/privacy-policy | 0.722 | www.ikea.com/us/en/customer-service/privacy-policy | 0.715 |
| crawlee | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.723 | www.ikea.com/us/en/customer-service/privacy-policy | 0.722 | www.ikea.com/us/en/customer-service/privacy-policy | 0.702 |
| colly+md | miss | www.ikea.com/us/en/customer-service/privacy-policy | 0.723 | www.ikea.com/us/en/customer-service/privacy-policy | 0.721 | www.ikea.com/us/en/customer-service/privacy-policy | 0.721 |
| playwright | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.723 | www.ikea.com/us/en/customer-service/privacy-policy | 0.722 | www.ikea.com/us/en/customer-service/privacy-policy | 0.702 |


**Q29: What discounts do IKEA Family members receive?**
*(expects URL containing: `family-offers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/ikea-family/ | 0.731 | www.ikea.com/us/en/ikea-family/ | 0.727 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.713 |
| crawl4ai | #15 | www.ikea.com/us/en/ikea-family/ | 0.744 | www.ikea.com/us/en/ikea-family/benefits/ | 0.744 | www.ikea.com/us/en/ikea-family/benefits/ | 0.739 |
| crawl4ai-raw | #15 | www.ikea.com/us/en/ikea-family/benefits/ | 0.744 | www.ikea.com/us/en/ikea-family/ | 0.744 | www.ikea.com/us/en/ikea-family/benefits/ | 0.739 |
| scrapy+md | miss | www.ikea.com/us/en/ikea-family/?itm_campaign=assur | 0.740 | www.ikea.com/us/en/ikea-family/?itm_campaign=assur | 0.719 | www.ikea.com/us/en/ikea-family/?itm_campaign=assur | 0.712 |
| crawlee | miss | www.ikea.com/us/en/ikea-family/ | 0.729 | www.ikea.com/us/en/ikea-family/ | 0.728 | www.ikea.com/us/en/ikea-family/ | 0.719 |
| colly+md | miss | www.ikea.com/us/en/ikea-family/ | 0.729 | www.ikea.com/us/en/ikea-family/ | 0.728 | www.ikea.com/us/en/ikea-family/ | 0.719 |
| playwright | #6 | www.ikea.com/us/en/ikea-family/ | 0.729 | www.ikea.com/us/en/ikea-family/ | 0.728 | www.ikea.com/us/en/ikea-family/ | 0.719 |


**Q30: How many points do IKEA Family members collect for every dollar spent?**
*(expects URL containing: `family-offers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/customer-service/ikea-family-te | 0.785 | www.ikea.com/us/en/customer-service/terms-conditio | 0.757 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.749 |
| crawl4ai | #12 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.753 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.748 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.746 |
| crawl4ai-raw | #12 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.753 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.748 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.746 |
| scrapy+md | miss | www.ikea.com/us/en/customer-service/ikea-family-te | 0.785 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.749 | www.ikea.com/us/en/ikea-family/?itm_campaign=assur | 0.745 |
| crawlee | miss | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.750 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.728 | www.ikea.com/us/en/ikea-family/ | 0.720 |
| colly+md | miss | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.750 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.729 | www.ikea.com/us/en/ikea-family/ | 0.720 |
| playwright | #7 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.750 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.729 | www.ikea.com/us/en/ikea-family/ | 0.720 |


**Q31: What is the price of the STORKLINTA 6-drawer dresser?**
*(expects URL containing: `storklinta-series-700569`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.620 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.571 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.534 |
| crawl4ai | #6 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.690 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.672 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.669 |
| crawl4ai-raw | #10 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.690 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.674 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.667 |
| scrapy+md | miss | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.526 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.522 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.522 |
| crawlee | #9 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.672 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.658 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.647 |
| colly+md | #30 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.693 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.654 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.651 |
| playwright | miss | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.688 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.654 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.646 |


**Q32: What safety feature does the STORKLINTA chest of drawers have?**
*(expects URL containing: `storklinta-series-700569`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.683 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.625 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.612 |
| crawl4ai | #44 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.708 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.708 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.707 |
| crawl4ai-raw | #44 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.708 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.708 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.707 |
| scrapy+md | miss | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.605 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.599 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.515 |
| crawlee | #45 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.690 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.690 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-w | 0.690 |
| colly+md | #24 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.690 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.690 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-w | 0.690 |
| playwright | #15 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.690 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.677 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.673 |


**Q33: What types of outdoor products are available at IKEA?**
*(expects URL containing: `outdoor-od001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.694 | www.ikea.com/us/en/rooms/outdoor/ | 0.686 | www.ikea.com/us/en/rooms/outdoor/ | 0.679 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.677 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.673 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.672 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.677 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.673 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.672 |
| scrapy+md | miss | www.ikea.com/us/en/customer-service/shopping-at-ik | 0.578 | www.ikea.com/us/en/p/saellskaplig-bowl-with-lid-cl | 0.574 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.571 |
| crawlee | miss | www.ikea.com/us/en/cat/products-products/ | 0.787 | www.ikea.com/us/en/new/new-products/ | 0.676 | www.ikea.com/us/en/cat/products-products/ | 0.644 |
| colly+md | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.698 | www.ikea.com/us/en/cat/outdoor-patio-furniture-od0 | 0.690 | www.ikea.com/us/en/cat/outdoor-kitchens-700349/ | 0.669 |
| playwright | #2 | www.ikea.com/us/en/cat/products-products/ | 0.787 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.735 | www.ikea.com/us/en/cat/home-improvement-hi001/ | 0.711 |


**Q34: What is the price of the HAVSTEN Loveseat, outdoor?**
*(expects URL containing: `outdoor-od001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.552 | www.ikea.com/us/en/cat/outdoor-patio-lounge-chairs | 0.549 | www.ikea.com/us/en/cat/outdoor-patio-furniture-od0 | 0.543 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.612 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.593 | www.ikea.com/us/en/p/vittskaer-armchair-plastic-ra | 0.562 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.613 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.593 | www.ikea.com/us/en/p/vittskaer-2-seat-section-for- | 0.576 |
| scrapy+md | miss | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.518 | www.ikea.com/us/en/cat/dining-chairs-25219/ | 0.502 | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.483 |
| crawlee | miss | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.531 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.527 | www.ikea.com/us/en/cat/stockholm-collection-11989/ | 0.526 |
| colly+md | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.671 | www.ikea.com/us/en/cat/outdoor-patio-furniture-od0 | 0.571 | www.ikea.com/us/en/p/vittskaer-armchair-plastic-ra | 0.562 |
| playwright | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.671 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.545 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.538 |


**Q35: What are some themes available at IKEA?**
*(expects URL containing: `themes-themes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/rooms/ | 0.682 | www.ikea.com/us/en/ideas/ | 0.638 | www.ikea.com/us/en/this-is-ikea/ | 0.637 |
| crawl4ai | #6 | www.ikea.com/us/en/ideas/ | 0.677 | www.ikea.com/us/en/cat/furniture-fu001/?page=2 | 0.676 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.669 |
| crawl4ai-raw | #4 | www.ikea.com/us/en/cat/furniture-fu001/?page=2 | 0.678 | www.ikea.com/us/en/ideas/ | 0.676 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.675 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.662 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.622 | www.ikea.com/us/en/customer-service/shopping-at-ik | 0.608 |
| crawlee | #1 | www.ikea.com/us/en/cat/themes-themes/ | 0.825 | www.ikea.com/us/en/cat/furniture-fu001/?page=2#pro | 0.676 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.676 |
| colly+md | #1 | www.ikea.com/us/en/cat/themes-themes/ | 0.721 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.654 | www.ikea.com/us/en/favorites/ | 0.643 |
| playwright | #1 | www.ikea.com/us/en/cat/themes-themes/ | 0.825 | www.ikea.com/us/en/cat/products-products/ | 0.667 | www.ikea.com/us/en/cat/home-improvement-hi001/ | 0.660 |


**Q36: What materials does IKEA prefer for their products?**
*(expects URL containing: `themes-themes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.641 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.577 | www.ikea.com/us/en/ikea-business/ | 0.566 |
| crawl4ai | #4 | www.ikea.com/us/en/customer-service/faq/ | 0.695 | www.ikea.com/us/en/cat/furniture-fu001/?page=2 | 0.673 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.673 |
| crawl4ai-raw | #4 | www.ikea.com/us/en/customer-service/faq/ | 0.695 | www.ikea.com/us/en/cat/furniture-fu001/?page=2 | 0.673 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.653 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.669 | www.ikea.com/us/en/p/kragsta-nesting-tables-set-of | 0.586 | www.ikea.com/us/en/customer-service/terms-conditio | 0.552 |
| crawlee | #5 | www.ikea.com/us/en/cat/products-products/ | 0.717 | www.ikea.com/us/en/cat/furniture-fu001/?page=2#pro | 0.669 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.669 |
| colly+md | #10 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.669 | www.ikea.com/us/en/customer-service/faq/ | 0.637 | www.ikea.com/us/en/product-guides/sustainable-prod | 0.601 |
| playwright | #7 | www.ikea.com/us/en/cat/products-products/ | 0.717 | www.ikea.com/us/en/cat/furniture-fu001/?page=2 | 0.669 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.641 |


**Q37: What are the dimensions of the STORKLINTA 3-drawer dresser?**
*(expects URL containing: `storklinta-3-drawer-dresser-gray-green-anchor-unlock-function-80574645`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.650 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.632 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.614 |
| crawl4ai | #3 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.679 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.677 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.673 |
| crawl4ai-raw | #2 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.677 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.673 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.672 |
| scrapy+md | miss | www.ikea.com/us/en/cat/patar-series-36839/ | 0.557 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.556 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.551 |
| crawlee | #4 | www.ikea.com/us/en/p/storklinta-nightstand-dark-br | 0.669 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.662 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.660 |
| colly+md | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.662 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.660 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.655 |
| playwright | miss | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.639 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.637 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.631 |


**Q38: What safety feature does the STORKLINTA 3-drawer dresser include?**
*(expects URL containing: `storklinta-3-drawer-dresser-gray-green-anchor-unlock-function-80574645`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.632 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.631 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.625 |
| crawl4ai | #2 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.658 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.655 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.645 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.655 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.647 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.644 |
| scrapy+md | miss | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.546 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.545 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.517 |
| crawlee | #5 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.645 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.638 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.637 |
| colly+md | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.645 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.638 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.637 |
| playwright | miss | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.633 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.621 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.619 |


**Q39: What is the price of the GLADELIG plate in gray?**
*(expects URL containing: `gladelig-plate-gray-10600756`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/serveware-16043/?filters=f- | 0.486 | www.ikea.com/us/en/cat/serveware-16043/?filters=f- | 0.431 | www.ikea.com/us/en/cat/batskaer-series-700500/ | 0.429 |
| crawl4ai | #1 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.608 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.597 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.595 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.613 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.585 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.541 |
| scrapy+md | miss | www.ikea.com/us/en/campaigns/ikea-binging-with-bab | 0.430 | www.ikea.com/us/en/cat/bowls-18864/ | 0.419 | www.ikea.com/us/en/cat/serving-bowls-20619/f/gray- | 0.410 |
| crawlee | #1 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.640 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.596 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.563 |
| colly+md | miss | www.ikea.com/us/en/cat/cabinet-knobs-handles-pulls | 0.417 | www.ikea.com/us/en/cat/gullaberg-series-700613/ | 0.398 | www.ikea.com/us/en/cat/outdoor-kitchens-700349/ | 0.393 |
| playwright | miss | www.ikea.com/us/en/cat/outdoor-kitchens-700349/ | 0.423 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.386 | www.ikea.com/us/en/rooms/dining/ | 0.385 |


**Q40: What materials is the GLADELIG plate made of?**
*(expects URL containing: `gladelig-plate-gray-10600756`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/serveware-16043/?filters=f- | 0.409 | www.ikea.com/us/en/cat/bowls-dishes-16308/ | 0.374 | www.ikea.com/us/en/cat/cookware-tableware-kt001/ | 0.363 |
| crawl4ai | #1 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.571 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.509 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.501 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.509 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.497 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.493 |
| scrapy+md | miss | www.ikea.com/us/en/campaigns/ikea-binging-with-bab | 0.409 | www.ikea.com/us/en/p/glattis-tray-brass-color-7035 | 0.394 | www.ikea.com/us/en/p/kragsta-nesting-tables-set-of | 0.377 |
| crawlee | #1 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.541 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.513 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.473 |
| colly+md | miss | www.ikea.com/us/en/p/sundsoe-cabinet-anthracite-ou | 0.358 | www.ikea.com/us/en/p/sundsoe-cabinet-off-white-out | 0.357 | www.ikea.com/us/en/p/sundsoe-cabinet-dark-blue-out | 0.356 |
| playwright | miss | www.ikea.com/us/en/cat/cookware-tableware-kt001/ | 0.342 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.342 | www.ikea.com/us/en/cat/stockholm-collection-11989/ | 0.333 |


**Q41: What are the dimensions of the LOHALS rug?**
*(expects URL containing: `lohals-rug-flatwoven-natural-00277395`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/rugs-10653/ | 0.495 | www.ikea.com/us/en/cat/rugs-10653/ | 0.466 | www.ikea.com/us/en/cat/rugs-10653/ | 0.457 |
| crawl4ai | #1 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.637 | www.ikea.com/us/en/cat/rugs-10653/ | 0.576 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.572 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.590 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.572 | www.ikea.com/us/en/cat/rugs-10653/ | 0.554 |
| scrapy+md | miss | www.ikea.com/us/en/p/omar-shelving-unit-with-3-bas | 0.335 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.332 | www.ikea.com/us/en/p/omar-shelving-unit-with-3-bas | 0.331 |
| crawlee | #1 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.698 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.620 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.589 |
| colly+md | miss | www.ikea.com/us/en/cat/rugs-10653/ | 0.499 | www.ikea.com/us/en/cat/rugs-10653/ | 0.493 | www.ikea.com/us/en/cat/rugs-10653/ | 0.472 |
| playwright | #1 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.697 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.591 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.575 |


**Q42: What material is the LOHALS rug made from?**
*(expects URL containing: `lohals-rug-flatwoven-natural-00277395`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/rugs-10653/ | 0.518 | www.ikea.com/us/en/cat/rugs-10653/ | 0.474 | www.ikea.com/us/en/cat/rugs-10653/ | 0.472 |
| crawl4ai | #1 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.621 | www.ikea.com/us/en/cat/rugs-10653/ | 0.594 | www.ikea.com/us/en/cat/rugs-10653/ | 0.592 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.595 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.588 | www.ikea.com/us/en/cat/rugs-10653/ | 0.541 |
| scrapy+md | miss | www.ikea.com/us/en/p/vinterfint-pre-cut-fabric-chr | 0.363 | www.ikea.com/us/en/p/stamsill-coaster-water-hyacin | 0.345 | www.ikea.com/us/en/p/laektare-chair-cover-gunnared | 0.342 |
| crawlee | #1 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.655 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.610 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.580 |
| colly+md | miss | www.ikea.com/us/en/ | 0.475 | www.ikea.com/us/en/cat/rugs-10653/ | 0.459 | www.ikea.com/us/en/cat/outdoor-rugs-34204/ | 0.457 |
| playwright | #1 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.654 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.580 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.566 |


**Q43: What types of kitchen systems does IKEA offer?**
*(expects URL containing: `kitchen-appliances-ka001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/cookware-tableware-kt001/ | 0.601 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.587 | www.ikea.com/us/en/cat/tables-chairs-fu002/ | 0.579 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.730 | www.ikea.com/us/en/rooms/kitchen/ | 0.696 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.692 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.730 | www.ikea.com/us/en/rooms/kitchen/ | 0.696 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.689 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.559 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.556 | www.ikea.com/us/en/cat/cookware-sets-31774/ | 0.556 |
| crawlee | miss | www.ikea.com/us/en/cat/kitchens-ka003/ | 0.775 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.729 | www.ikea.com/us/en/cat/products-products/ | 0.703 |
| colly+md | miss | www.ikea.com/us/en/cat/kitchen-cabinets-700292/ | 0.670 | www.ikea.com/us/en/rooms/kitchen/ | 0.667 | www.ikea.com/us/en/rooms/kitchen/ | 0.651 |
| playwright | #2 | www.ikea.com/us/en/cat/kitchens-ka003/ | 0.775 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.734 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.729 |


**Q44: How can I book an appointment with a kitchen expert at IKEA?**
*(expects URL containing: `kitchen-appliances-ka001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/planners/ | 0.632 | www.ikea.com/us/en/planners/ | 0.603 | www.ikea.com/us/en/customer-service/ | 0.574 |
| crawl4ai | #6 | www.ikea.com/us/en/rooms/kitchen/ | 0.670 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.668 | www.ikea.com/us/en/customer-service/faq/ | 0.656 |
| crawl4ai-raw | #6 | www.ikea.com/us/en/rooms/kitchen/ | 0.670 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.668 | www.ikea.com/us/en/customer-service/faq/ | 0.656 |
| scrapy+md | miss | www.ikea.com/us/en/customer-service/shopping-at-ik | 0.543 | www.ikea.com/us/en/customer-service/shopping-at-ik | 0.543 | www.ikea.com/us/en/customer-service/contact-us/ | 0.517 |
| crawlee | miss | www.ikea.com/us/en/customer-service/faq/ | 0.743 | www.ikea.com/us/en/rooms/kitchen/ | 0.654 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.652 |
| colly+md | miss | www.ikea.com/us/en/customer-service/faq/ | 0.743 | www.ikea.com/us/en/rooms/kitchen/ | 0.655 | www.ikea.com/us/en/customer-service/faq/ | 0.645 |
| playwright | #3 | www.ikea.com/us/en/customer-service/faq/ | 0.743 | www.ikea.com/us/en/rooms/kitchen/ | 0.654 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.653 |


**Q45: What is the starting cost for IKEA's delivery service?**
*(expects URL containing: `services`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/customer-service/services/deliv | 0.721 | www.ikea.com/us/en/campaigns/dream-lineup-pub85251 | 0.691 | www.ikea.com/us/en/customer-service/services/deliv | 0.680 |
| crawl4ai | #1 | www.ikea.com/us/en/customer-service/services/deliv | 0.718 | www.ikea.com/us/en/customer-service/services/deliv | 0.703 | www.ikea.com/us/en/customer-service/services/deliv | 0.702 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/customer-service/services/deliv | 0.718 | www.ikea.com/us/en/customer-service/services/deliv | 0.703 | www.ikea.com/us/en/customer-service/services/deliv | 0.702 |
| scrapy+md | #1 | www.ikea.com/us/en/customer-service/services/deliv | 0.721 | www.ikea.com/us/en/customer-service/services/deliv | 0.721 | www.ikea.com/us/en/customer-service/services/deliv | 0.684 |
| crawlee | #1 | www.ikea.com/us/en/customer-service/services/deliv | 0.721 | www.ikea.com/us/en/customer-service/services/deliv | 0.696 | www.ikea.com/us/en/customer-service/services/deliv | 0.684 |
| colly+md | #1 | www.ikea.com/us/en/customer-service/services/deliv | 0.721 | www.ikea.com/us/en/customer-service/services/deliv | 0.696 | www.ikea.com/us/en/customer-service/services/deliv | 0.684 |
| playwright | #1 | www.ikea.com/us/en/customer-service/services/deliv | 0.721 | www.ikea.com/us/en/customer-service/services/deliv | 0.721 | www.ikea.com/us/en/customer-service/services/deliv | 0.696 |


**Q46: Does IKEA offer assembly service for their products?**
*(expects URL containing: `services`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | www.ikea.com/us/en/ikea-business/network/ | 0.644 | www.ikea.com/us/en/customer-service/services/ | 0.641 | www.ikea.com/us/en/campaigns/dream-lineup-pub85251 | 0.617 |
| crawl4ai | #1 | www.ikea.com/us/en/customer-service/services/assem | 0.718 | www.ikea.com/us/en/customer-service/faq/ | 0.707 | www.ikea.com/us/en/customer-service/services/assem | 0.682 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/customer-service/services/assem | 0.736 | www.ikea.com/us/en/customer-service/faq/ | 0.707 | www.ikea.com/us/en/customer-service/services/assem | 0.682 |
| scrapy+md | #1 | www.ikea.com/us/en/customer-service/services/assem | 0.673 | www.ikea.com/us/en/customer-service/services/assem | 0.661 | www.ikea.com/us/en/customer-service/services/assem | 0.641 |
| crawlee | #2 | www.ikea.com/us/en/customer-service/faq/ | 0.724 | www.ikea.com/us/en/customer-service/services/assem | 0.667 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.667 |
| colly+md | #2 | www.ikea.com/us/en/customer-service/faq/ | 0.724 | www.ikea.com/us/en/customer-service/services/assem | 0.667 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.667 |
| playwright | #3 | www.ikea.com/us/en/customer-service/faq/ | 0.724 | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.669 | www.ikea.com/us/en/customer-service/services/assem | 0.667 |


**Q47: What is one way to extend your countertop in a small kitchen?**
*(expects URL containing: `maximising-kitchen-space-for-more-room-to-cook-pub969bcf40`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/cookware-tableware-kt001/ | 0.391 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.382 | www.ikea.com/us/en/rooms/outdoor/ | 0.376 |
| crawl4ai | #2 | www.ikea.com/us/en/cat/kitchen-countertops-24264/ | 0.561 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.557 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.516 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.557 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.534 | www.ikea.com/us/en/cat/kitchen-countertops-24264/ | 0.518 |
| scrapy+md | miss | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.399 | www.ikea.com/us/en/cat/kitchen-towels-18851/ | 0.396 | www.ikea.com/us/en/cat/sideboards-buffets-10412/ | 0.390 |
| crawlee | #1 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.570 | www.ikea.com/us/en/cat/kitchen-countertops-24264/ | 0.512 | www.ikea.com/us/en/cat/kitchen-countertops-24264/ | 0.502 |
| colly+md | miss | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.558 | www.ikea.com/us/en/cat/kitchen-countertops-24264/ | 0.510 | www.ikea.com/us/en/cat/kitchen-countertops-24264/ | 0.500 |
| playwright | #1 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.558 | www.ikea.com/us/en/cat/kitchen-countertops-24264/ | 0.514 | www.ikea.com/us/en/cat/kitchen-countertops-24264/ | 0.502 |


**Q48: How can you add more storage under your wall cabinets?**
*(expects URL containing: `maximising-kitchen-space-for-more-room-to-cook-pub969bcf40`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.468 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.438 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.435 |
| crawl4ai | #1 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.526 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.509 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.482 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.526 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.509 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.482 |
| scrapy+md | miss | www.ikea.com/us/en/cat/wall-shelves-10398/ | 0.512 | www.ikea.com/us/en/cat/wall-shelves-10398/ | 0.475 | www.ikea.com/us/en/cat/wall-shelves-10398/ | 0.445 |
| crawlee | #3 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.471 | www.ikea.com/us/en/rooms/dining/how-to/how-to-desi | 0.461 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.454 |
| colly+md | miss | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.511 | www.ikea.com/us/en/cat/storage-cabinets-10385/ | 0.469 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.468 |
| playwright | #1 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.511 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.474 | www.ikea.com/us/en/rooms/dining/how-to/how-to-desi | 0.462 |


**Q49: What are the dimensions of the BRIMNES 3-drawer dresser?**
*(expects URL containing: `brimnes-3-drawer-dresser-black-20574243`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.560 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.518 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.505 |
| crawl4ai | miss | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.580 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.578 | www.ikea.com/us/en/p/brimnes-bookcase-black-403012 | 0.576 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.770 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.770 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-gray | 0.756 |
| scrapy+md | miss | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.575 | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.559 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.555 |
| crawlee | miss | www.ikea.com/us/en/p/brimnes-bookcase-black-403012 | 0.597 | www.ikea.com/us/en/p/brimnes-bookcase-white-903012 | 0.593 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.582 |
| colly+md | #2 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.708 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.708 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.701 |
| playwright | miss | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.590 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.580 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.554 |


**Q50: What is the price of the BRIMNES 3-drawer dresser?**
*(expects URL containing: `brimnes-3-drawer-dresser-black-20574243`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.545 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.514 | www.ikea.com/us/en/p/gullaberg-storage-bench-white | 0.512 |
| crawl4ai | miss | www.ikea.com/us/en/p/brimnes-bookcase-black-403012 | 0.648 | www.ikea.com/us/en/p/brimnes-bookcase-white-903012 | 0.634 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.616 |
| crawl4ai-raw | #4 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.672 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-gray | 0.671 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.671 |
| scrapy+md | miss | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.576 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.566 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.557 |
| crawlee | miss | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.636 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.612 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.612 |
| colly+md | #2 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.734 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.718 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.715 |
| playwright | miss | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.636 | www.ikea.com/us/en/ | 0.556 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.551 |


**Q51: What types of storage solutions are available for hallways?**
*(expects URL containing: `hallway`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.568 | www.ikea.com/us/en/cat/hallway-benches-59246/ | 0.534 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.512 |
| crawl4ai | #1 | www.ikea.com/us/en/rooms/hallway/ | 0.592 | www.ikea.com/us/en/rooms/hallway/ | 0.586 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.575 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.600 | www.ikea.com/us/en/rooms/hallway/ | 0.592 | www.ikea.com/us/en/rooms/hallway/ | 0.586 |
| scrapy+md | miss | www.ikea.com/us/en/cat/wall-shelves-10398/ | 0.511 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.474 | www.ikea.com/us/en/cat/cube-storage-55012/ | 0.472 |
| crawlee | #1 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.622 | www.ikea.com/us/en/rooms/hallway/ | 0.547 | www.ikea.com/us/en/rooms/hallway/ | 0.545 |
| colly+md | #1 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.621 | www.ikea.com/us/en/rooms/hallway/ | 0.575 | www.ikea.com/us/en/rooms/hallway/ | 0.558 |
| playwright | #1 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.622 | www.ikea.com/us/en/rooms/hallway/ | 0.575 | www.ikea.com/us/en/rooms/hallway/ | 0.545 |


**Q52: How can I create a welcoming entryway with smart storage?**
*(expects URL containing: `hallway`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.547 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.538 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.511 |
| crawl4ai | #1 | www.ikea.com/us/en/rooms/hallway/ | 0.596 | www.ikea.com/us/en/rooms/hallway/ | 0.579 | www.ikea.com/us/en/rooms/hallway/ | 0.574 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/rooms/hallway/ | 0.596 | www.ikea.com/us/en/rooms/hallway/ | 0.579 | www.ikea.com/us/en/rooms/hallway/ | 0.574 |
| scrapy+md | miss | www.ikea.com/us/en/cat/wall-shelves-10398/ | 0.512 | www.ikea.com/us/en/cat/cube-storage-55012/ | 0.474 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.470 |
| crawlee | #1 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.596 | www.ikea.com/us/en/rooms/hallway/ | 0.555 | www.ikea.com/us/en/rooms/hallway/ | 0.546 |
| colly+md | #1 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.592 | www.ikea.com/us/en/rooms/hallway/ | 0.563 | www.ikea.com/us/en/rooms/hallway/ | 0.558 |
| playwright | #1 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.596 | www.ikea.com/us/en/rooms/hallway/ | 0.563 | www.ikea.com/us/en/rooms/hallway/ | 0.558 |


**Q53: What is the price of the GÅTEBO microwave oven?**
*(expects URL containing: `microwave-ovens-microwave-combo-ovens-20815`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/stockholm-2025-tealight-holde | 0.416 | www.ikea.com/us/en/cat/serveware-16043/?filters=f- | 0.396 | www.ikea.com/us/en/cat/batskaer-series-700500/ | 0.395 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.606 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.593 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.579 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.626 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.606 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.568 |
| scrapy+md | miss | www.ikea.com/us/en/p/godmiddag-serving-bowl-white- | 0.404 | www.ikea.com/us/en/p/faergklar-baking-serving-dish | 0.402 | www.ikea.com/us/en/p/faergklar-baking-serving-dish | 0.402 |
| crawlee | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.606 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.590 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.568 |
| colly+md | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.600 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.578 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.520 |
| playwright | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.592 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.562 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.554 |


**Q54: What are the differences between microwave ovens and microwave oven combos?**
*(expects URL containing: `microwave-ovens-microwave-combo-ovens-20815`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.250 | www.ikea.com/us/en/cat/cookware-tableware-kt001/ | 0.241 | www.ikea.com/us/en/cat/home-electronics-he001/ | 0.232 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.695 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.505 | www.ikea.com/us/en/cat/ovens-20810/ | 0.485 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.615 | www.ikea.com/us/en/cat/ovens-20810/ | 0.485 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.467 |
| scrapy+md | miss | www.ikea.com/us/en/cat/cookware-sets-31774/ | 0.310 | www.ikea.com/us/en/cat/ikea-365-food-storage-49524 | 0.307 | www.ikea.com/us/en/cat/dishwashers-20825/ | 0.289 |
| crawlee | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.660 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.613 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.595 |
| colly+md | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.684 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.485 | www.ikea.com/us/en/cat/ovens-20810/ | 0.464 |
| playwright | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.658 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.613 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.595 |


**Q55: What are the dimensions of the STORKLINTA 6-drawer dresser?**
*(expects URL containing: `storklinta-6-drawer-dresser-dark-brown-oak-effect-anchor-unlock-function-70559278`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.636 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.577 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.573 |
| crawl4ai | #2 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.672 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.658 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.650 |
| crawl4ai-raw | #2 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.672 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.659 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.650 |
| scrapy+md | miss | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.562 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.560 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.552 |
| crawlee | #6 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.675 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.673 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.663 |
| colly+md | miss | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.675 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.673 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.661 |
| playwright | #3 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.675 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.673 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.654 |


**Q56: What safety feature does the STORKLINTA 6-drawer dresser include?**
*(expects URL containing: `storklinta-6-drawer-dresser-dark-brown-oak-effect-anchor-unlock-function-70559278`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.627 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.608 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.601 |
| crawl4ai | #10 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.658 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.654 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.653 |
| crawl4ai-raw | #9 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.658 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.653 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.652 |
| scrapy+md | miss | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.555 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.553 | www.ikea.com/us/en/cat/patar-series-36839/ | 0.522 |
| crawlee | #5 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.653 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.646 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.645 |
| colly+md | miss | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.653 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.646 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.644 |
| playwright | #2 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.653 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.641 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.637 |


**Q57: What features do the desk chairs have that support comfort during work?**
*(expects URL containing: `desk-chairs-20652`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.505 | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.455 | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.405 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.594 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.592 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.545 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.594 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.581 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.565 |
| scrapy+md | miss | www.ikea.com/us/en/cat/desks-computer-desks-20649/ | 0.517 | www.ikea.com/us/en/cat/desks-computer-desks-20649/ | 0.507 | www.ikea.com/us/en/p/mittzon-desk-white-s99513954/ | 0.503 |
| crawlee | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.614 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.591 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.538 |
| colly+md | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.618 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.591 | www.ikea.com/us/en/cat/workspace-desks-chairs-fu00 | 0.530 |
| playwright | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.591 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.583 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.538 |


**Q58: What is the price of the MULLSJÖ swivel chair?**
*(expects URL containing: `desk-chairs-20652`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.538 | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.523 | www.ikea.com/us/en/p/saltsjoebaden-3-seat-sofa-ton | 0.519 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.629 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.579 | www.ikea.com/us/en/cat/armchairs-chaises-fu006/ | 0.557 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.629 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.603 | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.548 |
| scrapy+md | miss | www.ikea.com/us/en/cat/dining-chairs-25219/ | 0.553 | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.525 | www.ikea.com/us/en/cat/dining-chairs-25219/ | 0.523 |
| crawlee | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.628 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.587 | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.569 |
| colly+md | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.593 | www.ikea.com/us/en/p/mullsjoe-desk-oak-veneer-3055 | 0.583 | www.ikea.com/us/en/cat/armchairs-chaises-fu006/ | 0.571 |
| playwright | #6 | www.ikea.com/us/en/cat/workspace-desks-chairs-fu00 | 0.560 | www.ikea.com/us/en/cat/tables-chairs-fu002/ | 0.537 | www.ikea.com/us/en/cat/stockholm-collection-11989/ | 0.528 |


**Q59: What is the material of the KALAS plate?**
*(expects URL containing: `kalas-plate-mixed-colors-80461380`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/kallsoe-bench-with-shoe-stora | 0.333 | www.ikea.com/us/en/rooms/kitchen/how-to/buen-prove | 0.311 | www.ikea.com/us/en/p/smarra-box-with-lid-natural-9 | 0.301 |
| crawl4ai | #1 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.555 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.506 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.481 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.555 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.501 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.481 |
| scrapy+md | miss | www.ikea.com/us/en/p/kragsta-nesting-tables-set-of | 0.352 | www.ikea.com/us/en/campaigns/ikea-binging-with-bab | 0.333 | www.ikea.com/us/en/p/godmiddag-serving-plate-white | 0.323 |
| crawlee | #1 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.595 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.505 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.501 |
| colly+md | miss | www.ikea.com/us/en/cat/kallax-series-27534/ | 0.301 | www.ikea.com/us/en/rooms/dining/ | 0.294 | www.ikea.com/us/en/p/sundsoe-cabinet-anthracite-ou | 0.292 |
| playwright | miss | www.ikea.com/us/en/cat/kallax-series-27534/ | 0.307 | www.ikea.com/us/en/p/lack-wall-shelf-unit-black-br | 0.295 | www.ikea.com/us/en/rooms/dining/ | 0.294 |


**Q60: What is the diameter of the KALAS plate?**
*(expects URL containing: `kalas-plate-mixed-colors-80461380`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/stockholm-2025-bowl-dark-blue | 0.282 | www.ikea.com/us/en/p/kallsoe-bench-with-shoe-stora | 0.278 | www.ikea.com/us/en/cat/serveware-16043/?filters=f- | 0.277 |
| crawl4ai | #1 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.505 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.458 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.440 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.505 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.453 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.440 |
| scrapy+md | miss | www.ikea.com/us/en/p/godmiddag-serving-plate-white | 0.331 | www.ikea.com/us/en/cat/cube-storage-55012/ | 0.309 | www.ikea.com/us/en/p/godmiddag-serving-bowl-white- | 0.299 |
| crawlee | #1 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.569 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.466 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.461 |
| colly+md | miss | www.ikea.com/us/en/cat/kallax-series-27534/ | 0.291 | www.ikea.com/us/en/cat/kallax-series-27534/ | 0.276 | www.ikea.com/us/en/rooms/dining/ | 0.271 |
| playwright | miss | www.ikea.com/us/en/cat/kallax-series-27534/ | 0.278 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.276 | www.ikea.com/us/en/rooms/dining/ | 0.271 |


</details>

## kubernetes-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawlee | 82% (47/57) | 89% (51/57) | 91% (52/57) | 91% (52/57) | 96% (55/57) | 0.869 | 6813 | 400 |
| playwright | 82% (47/57) | 89% (51/57) | 91% (52/57) | 91% (52/57) | 96% (55/57) | 0.869 | 6812 | 400 |
| crawl4ai | 82% (47/57) | 88% (50/57) | 91% (52/57) | 91% (52/57) | 93% (53/57) | 0.862 | 6822 | 400 |
| crawl4ai-raw | 82% (47/57) | 88% (50/57) | 91% (52/57) | 91% (52/57) | 93% (53/57) | 0.862 | 6822 | 400 |
| colly+md | 72% (41/57) | 79% (45/57) | 81% (46/57) | 81% (46/57) | 86% (49/57) | 0.764 | 6743 | 399 |
| markcrawl | 40% (23/57) | 60% (34/57) | 70% (40/57) | 72% (41/57) | 74% (42/57) | 0.519 | 7922 | 400 |
| scrapy+md | 2% (1/57) | 4% (2/57) | 4% (2/57) | 5% (3/57) | 7% (4/57) | 0.031 | 3507 | 315 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for kubernetes-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is the purpose of the Topology Manager in Kubernetes?**
*(expects URL containing: `resource-managers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/workloads/resource-man | 0.717 | kubernetes.io/docs/concepts/services-networking/to | 0.565 | kubernetes.io/docs/concepts/_print/ | 0.541 |
| crawl4ai | #24 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.769 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.647 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.636 |
| crawl4ai-raw | #24 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.769 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.647 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.636 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.541 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.540 | kubernetes.io/feed.xml | 0.538 |
| crawlee | #15 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.753 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.628 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.626 |
| colly+md | #16 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.753 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.628 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.626 |
| playwright | #17 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.753 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.628 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.626 |


**Q2: What are the two available policies for the CPU Manager in Kubernetes?**
*(expects URL containing: `resource-managers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | kubernetes.io/docs/concepts/_print/ | 0.711 | kubernetes.io/docs/concepts/workloads/_print/ | 0.711 | kubernetes.io/docs/concepts/workloads/resource-man | 0.711 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/workloads/resource-man | 0.694 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.673 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.673 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/workloads/resource-man | 0.694 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.673 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.673 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.711 | kubernetes.io/docs/concepts/_print/ | 0.649 | kubernetes.io/docs/concepts/_print/ | 0.649 |
| crawlee | #1 | kubernetes.io/docs/concepts/workloads/resource-man | 0.685 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.668 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.664 |
| colly+md | #1 | kubernetes.io/docs/concepts/workloads/resource-man | 0.685 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.668 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.664 |
| playwright | #1 | kubernetes.io/docs/concepts/workloads/resource-man | 0.685 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.668 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.664 |


**Q3: How do I list the current namespaces in a Kubernetes cluster?**
*(expects URL containing: `namespaces`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tutorials/cluster-management/na | 0.647 | kubernetes.io/docs/tutorials/cluster-management/na | 0.646 | kubernetes.io/docs/concepts/overview/working-with- | 0.628 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.686 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.655 | kubernetes.io/docs/concepts/overview/working-with- | 0.644 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.686 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.655 | kubernetes.io/docs/concepts/overview/working-with- | 0.644 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.630 | kubernetes.io/docs/concepts/_print/ | 0.596 | kubernetes.io/docs/concepts/_print/ | 0.563 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.678 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.648 | kubernetes.io/docs/concepts/overview/working-with- | 0.637 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.678 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.648 | kubernetes.io/docs/concepts/overview/working-with- | 0.637 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.678 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.648 | kubernetes.io/docs/concepts/overview/working-with- | 0.637 |


**Q4: What command do I use to delete a namespace in Kubernetes?**
*(expects URL containing: `namespaces`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | kubernetes.io/docs/tutorials/stateful-application/ | 0.566 | kubernetes.io/docs/tutorials/cluster-management/na | 0.538 | kubernetes.io/docs/tutorials/cluster-management/na | 0.521 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.584 | kubernetes.io/docs/concepts/overview/working-with- | 0.566 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.557 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.584 | kubernetes.io/docs/concepts/overview/working-with- | 0.566 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.557 |
| scrapy+md | miss | kubernetes.io/docs/reference/generated/kubectl/kub | 0.524 | kubernetes.io/docs/reference/generated/kubectl/kub | 0.516 | kubernetes.io/docs/reference/generated/kubectl/kub | 0.501 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.584 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.573 | kubernetes.io/docs/concepts/overview/working-with- | 0.522 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.584 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.573 | kubernetes.io/docs/concepts/overview/working-with- | 0.521 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.584 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.573 | kubernetes.io/docs/concepts/overview/working-with- | 0.522 |


**Q5: What is a VolumeSnapshot in Kubernetes?**
*(expects URL containing: `volume-snapshots`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.829 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.750 | kubernetes.io/docs/concepts/storage/_print/ | 0.748 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.774 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.761 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.679 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.774 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.761 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.679 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.746 | kubernetes.io/docs/concepts/_print/ | 0.653 | kubernetes.io/docs/concepts/_print/ | 0.622 |
| crawlee | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.770 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.752 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.653 |
| colly+md | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.770 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.752 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.653 |
| playwright | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.770 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.752 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.653 |


**Q6: How can you provision a new volume from a snapshot?**
*(expects URL containing: `volume-snapshots`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.667 | kubernetes.io/docs/concepts/storage/_print/ | 0.606 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.606 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.605 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.605 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.583 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.605 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.605 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.583 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.609 | kubernetes.io/docs/concepts/_print/ | 0.553 | kubernetes.io/docs/concepts/_print/ | 0.552 |
| crawlee | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.609 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.604 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.552 |
| colly+md | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.609 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.604 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.576 |
| playwright | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.609 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.604 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.552 |


**Q7: How do you create a namespace for default CPU limits?**
*(expects URL containing: `cpu-default-namespace`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/concepts/policy/_print/ | 0.510 | kubernetes.io/docs/concepts/_print/ | 0.510 | kubernetes.io/docs/concepts/policy/resource-quotas | 0.510 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.614 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.604 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.596 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.614 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.604 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.596 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.510 | kubernetes.io/docs/concepts/_print/ | 0.502 | kubernetes.io/feed.xml | 0.485 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.629 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.613 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.599 |
| colly+md | miss | kubernetes.io/docs/tasks/administer-cluster/manage | 0.629 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.613 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.599 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.629 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.613 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.599 |


**Q8: What are the default CPU request and limit values applied by the control plane?**
*(expects URL containing: `cpu-default-namespace`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/concepts/_print/ | 0.509 | kubernetes.io/docs/concepts/workloads/_print/ | 0.509 | kubernetes.io/docs/concepts/workloads/resource-man | 0.509 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.611 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.553 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.526 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.611 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.553 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.526 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.506 | kubernetes.io/docs/concepts/_print/ | 0.505 | kubernetes.io/docs/concepts/_print/ | 0.504 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.611 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.543 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.532 |
| colly+md | miss | kubernetes.io/docs/tasks/administer-cluster/manage | 0.611 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.543 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.532 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.611 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.543 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.532 |


**Q9: What are some examples of API objects that act as policies in Kubernetes?**
*(expects URL containing: `policy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/policy/ | 0.643 | kubernetes.io/docs/concepts/overview/kubernetes-ap | 0.643 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.625 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/policy/ | 0.684 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.630 | kubernetes.io/docs/concepts/overview/working-with- | 0.629 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/policy/ | 0.684 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.630 | kubernetes.io/docs/concepts/overview/working-with- | 0.629 |
| scrapy+md | #32 | kubernetes.io/docs/concepts/_print/ | 0.625 | kubernetes.io/docs/concepts/_print/ | 0.623 | kubernetes.io/docs/concepts/_print/ | 0.604 |
| crawlee | #1 | kubernetes.io/docs/concepts/policy/ | 0.652 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.625 | kubernetes.io/docs/concepts/services-networking/ne | 0.613 |
| colly+md | #1 | kubernetes.io/docs/concepts/policy/ | 0.652 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.625 | kubernetes.io/docs/concepts/services-networking/ne | 0.613 |
| playwright | #1 | kubernetes.io/docs/concepts/policy/ | 0.652 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.625 | kubernetes.io/docs/concepts/services-networking/ne | 0.613 |


**Q10: How do dynamic admission controllers apply policies on API requests?**
*(expects URL containing: `policy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | kubernetes.io/docs/concepts/_print/ | 0.630 | kubernetes.io/docs/concepts/policy/_print/ | 0.602 | kubernetes.io/docs/reference/access-authn-authz/ad | 0.597 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/policy/ | 0.634 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.559 | kubernetes.io/docs/concepts/security/controlling-a | 0.500 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/policy/ | 0.634 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.559 | kubernetes.io/docs/concepts/security/controlling-a | 0.500 |
| scrapy+md | #17 | kubernetes.io/docs/concepts/_print/ | 0.630 | kubernetes.io/hi/docs/_print/ | 0.592 | kubernetes.io/docs/concepts/_print/ | 0.553 |
| crawlee | #1 | kubernetes.io/docs/concepts/policy/ | 0.626 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.553 | kubernetes.io/docs/concepts/security/security-chec | 0.489 |
| colly+md | #1 | kubernetes.io/docs/concepts/policy/ | 0.626 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.553 | kubernetes.io/docs/concepts/security/security-chec | 0.489 |
| playwright | #1 | kubernetes.io/docs/concepts/policy/ | 0.626 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.553 | kubernetes.io/docs/concepts/security/security-chec | 0.490 |


**Q11: What are the two options for configuring the topology of highly available Kubernetes clusters?**
*(expects URL containing: `ha-topology`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/setup/production-environment/ | 0.590 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.579 | kubernetes.io/docs/setup/production-environment/ | 0.556 |
| crawl4ai | #1 | kubernetes.io/docs/setup/production-environment/to | 0.663 | kubernetes.io/docs/setup/production-environment/to | 0.642 | kubernetes.io/docs/setup/production-environment/to | 0.618 |
| crawl4ai-raw | #1 | kubernetes.io/docs/setup/production-environment/to | 0.663 | kubernetes.io/docs/setup/production-environment/to | 0.642 | kubernetes.io/docs/setup/production-environment/to | 0.618 |
| scrapy+md | miss | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.588 | kubernetes.io/docs/concepts/_print/ | 0.543 | kubernetes.io/docs/concepts/_print/ | 0.523 |
| crawlee | #1 | kubernetes.io/docs/setup/production-environment/to | 0.641 | kubernetes.io/docs/setup/production-environment/to | 0.612 | kubernetes.io/docs/setup/production-environment/ | 0.591 |
| colly+md | #1 | kubernetes.io/docs/setup/production-environment/to | 0.641 | kubernetes.io/docs/setup/production-environment/to | 0.612 | kubernetes.io/docs/setup/production-environment/to | 0.605 |
| playwright | #1 | kubernetes.io/docs/setup/production-environment/to | 0.641 | kubernetes.io/docs/setup/production-environment/to | 0.612 | kubernetes.io/docs/setup/production-environment/to | 0.605 |


**Q12: What is the minimum number of control plane nodes required for a stacked HA cluster?**
*(expects URL containing: `ha-topology`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/setup/production-environment/ | 0.529 | kubernetes.io/docs/setup/production-environment/ | 0.449 | kubernetes.io/docs/setup/production-environment/ | 0.448 |
| crawl4ai | #2 | kubernetes.io/docs/setup/production-environment/to | 0.580 | kubernetes.io/docs/setup/production-environment/to | 0.576 | kubernetes.io/docs/setup/production-environment/to | 0.518 |
| crawl4ai-raw | #2 | kubernetes.io/docs/setup/production-environment/to | 0.580 | kubernetes.io/docs/setup/production-environment/to | 0.576 | kubernetes.io/docs/setup/production-environment/to | 0.518 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.441 | kubernetes.io/de/docs/_print/ | 0.439 | kubernetes.io/docs/concepts/_print/ | 0.425 |
| crawlee | #1 | kubernetes.io/docs/setup/production-environment/to | 0.581 | kubernetes.io/docs/setup/production-environment/to | 0.557 | kubernetes.io/docs/setup/production-environment/ | 0.529 |
| colly+md | #1 | kubernetes.io/docs/setup/production-environment/to | 0.581 | kubernetes.io/docs/setup/production-environment/to | 0.557 | kubernetes.io/docs/setup/production-environment/ | 0.529 |
| playwright | #1 | kubernetes.io/docs/setup/production-environment/to | 0.581 | kubernetes.io/docs/setup/production-environment/to | 0.557 | kubernetes.io/docs/setup/production-environment/ | 0.529 |


**Q13: How can I create Secret objects using kubectl?**
*(expects URL containing: `configmap-secret`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.763 | kubernetes.io/docs/concepts/configuration/secret/ | 0.666 | kubernetes.io/docs/concepts/_print/ | 0.623 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.673 | kubernetes.io/docs/concepts/configuration/secret/ | 0.643 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.640 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.673 | kubernetes.io/docs/concepts/configuration/secret/ | 0.643 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.640 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.624 | kubernetes.io/docs/concepts/_print/ | 0.600 | kubernetes.io/docs/concepts/_print/ | 0.597 |
| crawlee | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.671 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.633 | kubernetes.io/docs/tasks/inject-data-application/d | 0.625 |
| colly+md | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.671 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.633 | kubernetes.io/docs/tasks/inject-data-application/d | 0.625 |
| playwright | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.671 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.633 | kubernetes.io/docs/tasks/inject-data-application/d | 0.625 |


**Q14: What file format can be used to create Secret objects in Kubernetes?**
*(expects URL containing: `configmap-secret`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | kubernetes.io/docs/concepts/configuration/secret/ | 0.677 | kubernetes.io/docs/concepts/configuration/_print/ | 0.648 | kubernetes.io/docs/concepts/_print/ | 0.648 |
| crawl4ai | #4 | kubernetes.io/docs/concepts/configuration/secret/ | 0.659 | kubernetes.io/docs/concepts/configuration/secret/ | 0.645 | kubernetes.io/docs/concepts/configuration/secret/ | 0.640 |
| crawl4ai-raw | #4 | kubernetes.io/docs/concepts/configuration/secret/ | 0.659 | kubernetes.io/docs/concepts/configuration/secret/ | 0.645 | kubernetes.io/docs/concepts/configuration/secret/ | 0.640 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.650 | kubernetes.io/docs/concepts/_print/ | 0.631 | kubernetes.io/docs/concepts/_print/ | 0.606 |
| crawlee | #4 | kubernetes.io/docs/concepts/configuration/secret/ | 0.650 | kubernetes.io/docs/concepts/configuration/secret/ | 0.631 | kubernetes.io/docs/concepts/configuration/secret/ | 0.630 |
| colly+md | #4 | kubernetes.io/docs/concepts/configuration/secret/ | 0.650 | kubernetes.io/docs/concepts/configuration/secret/ | 0.631 | kubernetes.io/docs/concepts/configuration/secret/ | 0.630 |
| playwright | #4 | kubernetes.io/docs/concepts/configuration/secret/ | 0.650 | kubernetes.io/docs/concepts/configuration/secret/ | 0.631 | kubernetes.io/docs/concepts/configuration/secret/ | 0.630 |


**Q15: What is a service account in Kubernetes?**
*(expects URL containing: `service-accounts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | kubernetes.io/docs/concepts/_print/ | 0.753 | kubernetes.io/docs/concepts/security/_print/ | 0.750 | kubernetes.io/docs/concepts/_print/ | 0.749 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.757 | kubernetes.io/docs/concepts/security/service-accou | 0.752 | kubernetes.io/docs/concepts/security/service-accou | 0.734 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.757 | kubernetes.io/docs/concepts/security/service-accou | 0.752 | kubernetes.io/docs/concepts/security/service-accou | 0.734 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.753 | kubernetes.io/docs/concepts/_print/ | 0.748 | kubernetes.io/docs/concepts/_print/ | 0.747 |
| crawlee | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.748 | kubernetes.io/docs/concepts/security/service-accou | 0.747 | kubernetes.io/docs/concepts/security/service-accou | 0.730 |
| colly+md | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.748 | kubernetes.io/docs/concepts/security/service-accou | 0.747 | kubernetes.io/docs/concepts/security/service-accou | 0.730 |
| playwright | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.748 | kubernetes.io/docs/concepts/security/service-accou | 0.747 | kubernetes.io/docs/concepts/security/service-accou | 0.730 |


**Q16: How do you assign a ServiceAccount to a Pod?**
*(expects URL containing: `service-accounts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | kubernetes.io/docs/concepts/_print/ | 0.676 | kubernetes.io/docs/concepts/security/service-accou | 0.676 | kubernetes.io/docs/concepts/security/_print/ | 0.676 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.684 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.676 | kubernetes.io/docs/concepts/security/service-accou | 0.663 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.684 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.676 | kubernetes.io/docs/concepts/security/service-accou | 0.663 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.676 | kubernetes.io/docs/concepts/_print/ | 0.661 | kubernetes.io/docs/concepts/_print/ | 0.653 |
| crawlee | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.676 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.670 | kubernetes.io/docs/concepts/security/service-accou | 0.661 |
| colly+md | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.676 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.670 | kubernetes.io/docs/concepts/security/service-accou | 0.661 |
| playwright | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.676 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.670 | kubernetes.io/docs/concepts/security/service-accou | 0.661 |


**Q17: What is required for an Ingress to work in a Kubernetes cluster?**
*(expects URL containing: `ingress-controllers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.715 | kubernetes.io/docs/concepts/services-networking/in | 0.665 | kubernetes.io/docs/concepts/_print/ | 0.622 |
| crawl4ai | #2 | kubernetes.io/docs/concepts/services-networking/in | 0.661 | kubernetes.io/docs/concepts/services-networking/in | 0.621 | kubernetes.io/docs/concepts/services-networking/in | 0.609 |
| crawl4ai-raw | #2 | kubernetes.io/docs/concepts/services-networking/in | 0.661 | kubernetes.io/docs/concepts/services-networking/in | 0.621 | kubernetes.io/docs/concepts/services-networking/in | 0.609 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.622 | kubernetes.io/feed.xml | 0.601 | kubernetes.io/docs/concepts/_print/ | 0.587 |
| crawlee | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.700 | kubernetes.io/docs/concepts/services-networking/in | 0.664 | kubernetes.io/docs/concepts/services-networking/in | 0.609 |
| colly+md | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.700 | kubernetes.io/docs/concepts/services-networking/in | 0.664 | kubernetes.io/docs/concepts/services-networking/in | 0.609 |
| playwright | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.700 | kubernetes.io/docs/concepts/services-networking/in | 0.664 | kubernetes.io/docs/concepts/services-networking/in | 0.609 |


**Q18: Which ingress controllers are supported and maintained by the Kubernetes project?**
*(expects URL containing: `ingress-controllers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | kubernetes.io/docs/concepts/services-networking/_p | 0.747 | kubernetes.io/docs/concepts/services-networking/in | 0.747 | kubernetes.io/docs/concepts/_print/ | 0.747 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.744 | kubernetes.io/docs/concepts/services-networking/in | 0.706 | kubernetes.io/docs/concepts/services-networking/in | 0.695 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.744 | kubernetes.io/docs/concepts/services-networking/in | 0.706 | kubernetes.io/docs/concepts/services-networking/in | 0.695 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.747 | kubernetes.io/docs/concepts/_print/ | 0.681 | kubernetes.io/feed.xml | 0.629 |
| crawlee | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.747 | kubernetes.io/docs/concepts/services-networking/in | 0.731 | kubernetes.io/docs/concepts/services-networking/in | 0.671 |
| colly+md | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.747 | kubernetes.io/docs/concepts/services-networking/in | 0.731 | kubernetes.io/docs/concepts/services-networking/in | 0.671 |
| playwright | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.747 | kubernetes.io/docs/concepts/services-networking/in | 0.731 | kubernetes.io/docs/concepts/services-networking/in | 0.671 |


**Q19: What is a workload in Kubernetes?**
*(expects URL containing: `workloads`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/workloads/ | 0.691 | kubernetes.io/docs/concepts/workloads/_print/ | 0.690 | kubernetes.io/docs/concepts/workloads/_print/ | 0.663 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/workloads/ | 0.727 | kubernetes.io/docs/concepts/workloads/workload-api | 0.674 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.668 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/workloads/ | 0.727 | kubernetes.io/docs/concepts/workloads/workload-api | 0.674 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.668 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.663 | kubernetes.io/docs/concepts/_print/ | 0.648 | kubernetes.io/docs/concepts/_print/ | 0.637 |
| crawlee | #1 | kubernetes.io/docs/concepts/workloads/ | 0.681 | kubernetes.io/docs/concepts/workloads/workload-api | 0.679 | kubernetes.io/docs/concepts/workloads/ | 0.655 |
| colly+md | #1 | kubernetes.io/docs/concepts/workloads/ | 0.681 | kubernetes.io/docs/concepts/workloads/workload-api | 0.679 | kubernetes.io/docs/concepts/workloads/ | 0.663 |
| playwright | #1 | kubernetes.io/docs/concepts/workloads/ | 0.681 | kubernetes.io/docs/concepts/workloads/workload-api | 0.679 | kubernetes.io/docs/concepts/workloads/ | 0.655 |


**Q20: What are the built-in workload resources provided by Kubernetes?**
*(expects URL containing: `workloads`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/workloads/_print/ | 0.728 | kubernetes.io/docs/concepts/workloads/ | 0.728 | kubernetes.io/docs/concepts/_print/ | 0.727 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/workloads/ | 0.703 | kubernetes.io/docs/concepts/workloads/ | 0.645 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.644 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/workloads/ | 0.703 | kubernetes.io/docs/concepts/workloads/ | 0.645 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.644 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.727 | kubernetes.io/docs/concepts/_print/ | 0.613 | kubernetes.io/docs/concepts/_print/ | 0.593 |
| crawlee | #1 | kubernetes.io/docs/concepts/workloads/ | 0.728 | kubernetes.io/docs/concepts/workloads/ | 0.664 | kubernetes.io/docs/concepts/workloads/workload-api | 0.629 |
| colly+md | #1 | kubernetes.io/docs/concepts/workloads/ | 0.728 | kubernetes.io/docs/concepts/workloads/ | 0.664 | kubernetes.io/docs/concepts/workloads/workload-api | 0.629 |
| playwright | #1 | kubernetes.io/docs/concepts/workloads/ | 0.728 | kubernetes.io/docs/concepts/workloads/ | 0.664 | kubernetes.io/docs/concepts/workloads/workload-api | 0.629 |


**Q21: What does this page provide a list of?**
*(expects URL containing: `turnkey-solutions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/contribute/style/page-content-t | 0.399 | kubernetes.io/docs/concepts/extend-kubernetes/comp | 0.395 | kubernetes.io/docs/concepts/extend-kubernetes/comp | 0.395 |
| crawl4ai | miss | kubernetes.io/docs/concepts/extend-kubernetes/comp | 0.396 | kubernetes.io/docs/concepts/cluster-administration | 0.395 | kubernetes.io/docs/concepts/services-networking/en | 0.393 |
| crawl4ai-raw | miss | kubernetes.io/docs/concepts/extend-kubernetes/comp | 0.396 | kubernetes.io/docs/concepts/cluster-administration | 0.395 | kubernetes.io/docs/concepts/services-networking/en | 0.393 |
| scrapy+md | miss | kubernetes.io/hi/docs/reference/scheduling/_print/ | 0.412 | kubernetes.io/pt-br/releases/1.36/_print/ | 0.404 | kubernetes.io/it/releases/1.36/_print/ | 0.404 |
| crawlee | #13 | kubernetes.io/docs/concepts/extend-kubernetes/comp | 0.398 | kubernetes.io/pl/docs/concepts/ | 0.389 | kubernetes.io/docs/tasks/ | 0.383 |
| colly+md | #12 | kubernetes.io/docs/concepts/extend-kubernetes/comp | 0.398 | kubernetes.io/pl/docs/concepts/ | 0.389 | kubernetes.io/docs/concepts/overview/working-with- | 0.369 |
| playwright | #13 | kubernetes.io/docs/concepts/extend-kubernetes/comp | 0.398 | kubernetes.io/pl/docs/concepts/ | 0.389 | kubernetes.io/docs/tasks/ | 0.383 |


**Q22: How can I learn to install and set up production-ready clusters from the providers listed?**
*(expects URL containing: `turnkey-solutions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/setup/production-environment/ | 0.637 | kubernetes.io/docs/setup/production-environment/ | 0.587 | kubernetes.io/docs/setup/production-environment/ | 0.561 |
| crawl4ai | miss | kubernetes.io/docs/setup/production-environment/ | 0.564 | kubernetes.io/docs/setup/production-environment/ | 0.548 | kubernetes.io/docs/setup/learning-environment/ | 0.532 |
| crawl4ai-raw | miss | kubernetes.io/docs/setup/production-environment/ | 0.564 | kubernetes.io/docs/setup/production-environment/ | 0.548 | kubernetes.io/docs/setup/learning-environment/ | 0.532 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.521 | kubernetes.io/de/docs/_print/ | 0.475 | kubernetes.io/de/docs/_print/ | 0.450 |
| crawlee | #28 | kubernetes.io/docs/setup/production-environment/ | 0.636 | kubernetes.io/docs/setup/production-environment/ | 0.561 | kubernetes.io/docs/setup/production-environment/ | 0.527 |
| colly+md | #27 | kubernetes.io/docs/setup/production-environment/ | 0.636 | kubernetes.io/docs/setup/production-environment/ | 0.561 | kubernetes.io/docs/setup/production-environment/ | 0.527 |
| playwright | #28 | kubernetes.io/docs/setup/production-environment/ | 0.636 | kubernetes.io/docs/setup/production-environment/ | 0.561 | kubernetes.io/docs/setup/production-environment/ | 0.527 |


**Q23: What is the recommended approach for providing kubelet parameters?**
*(expects URL containing: `kubelet-config-file`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/reference/command-line-tools-re | 0.566 | kubernetes.io/docs/reference/command-line-tools-re | 0.549 | kubernetes.io/docs/reference/command-line-tools-re | 0.542 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.621 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.584 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.567 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.621 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.584 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.567 |
| scrapy+md | miss | kubernetes.io/feed.xml | 0.530 | kubernetes.io/docs/concepts/_print/ | 0.510 | kubernetes.io/docs/concepts/_print/ | 0.491 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.610 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.566 | kubernetes.io/docs/setup/production-environment/to | 0.554 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.610 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.566 | kubernetes.io/docs/setup/production-environment/to | 0.554 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.610 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.566 | kubernetes.io/docs/setup/production-environment/to | 0.554 |


**Q24: What format must the kubelet configuration file be in?**
*(expects URL containing: `kubelet-config-file`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/reference/node/kubelet-files/ | 0.582 | kubernetes.io/docs/reference/node/kubelet-files/ | 0.570 | kubernetes.io/docs/reference/command-line-tools-re | 0.528 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.651 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.613 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.591 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.651 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.613 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.591 |
| scrapy+md | miss | kubernetes.io/feed.xml | 0.554 | kubernetes.io/feed.xml | 0.509 | kubernetes.io/docs/concepts/_print/ | 0.495 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.638 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.609 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.588 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.638 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.609 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.588 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.638 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.609 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.588 |


**Q25: What are the four sections of the debugging guide?**
*(expects URL containing: `debug`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tasks/debug/debug-application/ | 0.446 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.425 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.386 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.512 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.505 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.505 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.512 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.505 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.505 |
| scrapy+md | miss | kubernetes.io/docs/reference/generated/kubectl/kub | 0.416 | kubernetes.io/feed.xml | 0.382 | kubernetes.io/docs/concepts/_print/ | 0.375 |
| crawlee | #1 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.502 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.486 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.483 |
| colly+md | #1 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.502 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.486 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.483 |
| playwright | #1 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.502 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.486 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.483 |


**Q26: How can I get help if my question isn't covered in the documentation?**
*(expects URL containing: `debug`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #17 | kubernetes.io/docs/concepts/cluster-administration | 0.407 | kubernetes.io/docs/contribute/participate/ | 0.373 | kubernetes.io/docs/contribute/style/style-guide/ | 0.370 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/debug/ | 0.573 | kubernetes.io/docs/tasks/debug/ | 0.465 | kubernetes.io/docs/tasks/debug/ | 0.449 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/debug/ | 0.573 | kubernetes.io/docs/tasks/debug/ | 0.465 | kubernetes.io/docs/tasks/debug/ | 0.449 |
| scrapy+md | miss | kubernetes.io/de/docs/reference/kubernetes-api/ | 0.405 | kubernetes.io/de/docs/search/ | 0.402 | kubernetes.io/fr/docs/tutorials/services/ | 0.391 |
| crawlee | #1 | kubernetes.io/docs/tasks/debug/ | 0.571 | kubernetes.io/docs/tasks/debug/ | 0.468 | kubernetes.io/docs/tasks/debug/ | 0.453 |
| colly+md | #1 | kubernetes.io/docs/tasks/debug/ | 0.571 | kubernetes.io/docs/tasks/debug/ | 0.468 | kubernetes.io/docs/tasks/debug/ | 0.453 |
| playwright | #1 | kubernetes.io/docs/tasks/debug/ | 0.571 | kubernetes.io/docs/tasks/debug/ | 0.468 | kubernetes.io/docs/tasks/debug/ | 0.453 |


**Q27: What should I do if `kubeadm join` from v1.18 cannot join a cluster created by kubeadm v1.17?**
*(expects URL containing: `troubleshooting-kubeadm`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/setup/production-environment/to | 0.758 | kubernetes.io/docs/setup/production-environment/to | 0.587 | kubernetes.io/docs/reference/setup-tools/kubeadm/k | 0.583 |
| crawl4ai | #1 | kubernetes.io/docs/setup/production-environment/to | 0.662 | kubernetes.io/docs/setup/production-environment/to | 0.581 | kubernetes.io/docs/setup/production-environment/to | 0.568 |
| crawl4ai-raw | #1 | kubernetes.io/docs/setup/production-environment/to | 0.662 | kubernetes.io/docs/setup/production-environment/to | 0.581 | kubernetes.io/docs/setup/production-environment/to | 0.568 |
| scrapy+md | miss | kubernetes.io/id/docs/reference/setup-tools/kubead | 0.458 | kubernetes.io/feed.xml | 0.430 | kubernetes.io/feed.xml | 0.423 |
| crawlee | #1 | kubernetes.io/docs/setup/production-environment/to | 0.667 | kubernetes.io/docs/setup/production-environment/to | 0.589 | kubernetes.io/docs/setup/production-environment/to | 0.575 |
| colly+md | miss | kubernetes.io/docs/setup/production-environment/to | 0.667 | kubernetes.io/docs/setup/production-environment/to | 0.589 | kubernetes.io/docs/setup/production-environment/to | 0.575 |
| playwright | #1 | kubernetes.io/docs/setup/production-environment/to | 0.667 | kubernetes.io/docs/setup/production-environment/to | 0.589 | kubernetes.io/docs/setup/production-environment/to | 0.575 |


**Q28: How can I resolve the issue of `coredns` pods being in `CrashLoopBackOff` or `Error` state?**
*(expects URL containing: `troubleshooting-kubeadm`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/setup/production-environment/to | 0.701 | kubernetes.io/docs/setup/production-environment/to | 0.682 | kubernetes.io/docs/setup/production-environment/to | 0.633 |
| crawl4ai | #1 | kubernetes.io/docs/setup/production-environment/to | 0.694 | kubernetes.io/docs/setup/production-environment/to | 0.689 | kubernetes.io/docs/setup/production-environment/to | 0.659 |
| crawl4ai-raw | #1 | kubernetes.io/docs/setup/production-environment/to | 0.694 | kubernetes.io/docs/setup/production-environment/to | 0.689 | kubernetes.io/docs/setup/production-environment/to | 0.659 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.558 | kubernetes.io/docs/concepts/_print/ | 0.535 | kubernetes.io/docs/concepts/_print/ | 0.504 |
| crawlee | #1 | kubernetes.io/docs/setup/production-environment/to | 0.700 | kubernetes.io/docs/setup/production-environment/to | 0.693 | kubernetes.io/docs/setup/production-environment/to | 0.685 |
| colly+md | miss | kubernetes.io/docs/setup/production-environment/to | 0.699 | kubernetes.io/docs/setup/production-environment/to | 0.693 | kubernetes.io/docs/setup/production-environment/to | 0.685 |
| playwright | #1 | kubernetes.io/docs/setup/production-environment/to | 0.699 | kubernetes.io/docs/setup/production-environment/to | 0.693 | kubernetes.io/docs/setup/production-environment/to | 0.685 |


**Q29: What is the default operating mode for connections from nodes to the control plane?**
*(expects URL containing: `control-plane-node-communication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | kubernetes.io/docs/concepts/architecture/_print/ | 0.550 | kubernetes.io/docs/concepts/_print/ | 0.550 | kubernetes.io/docs/concepts/architecture/control-p | 0.516 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.504 | kubernetes.io/docs/concepts/architecture/control-p | 0.499 | kubernetes.io/docs/concepts/services-networking/wi | 0.454 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.504 | kubernetes.io/docs/concepts/architecture/control-p | 0.499 | kubernetes.io/docs/concepts/services-networking/wi | 0.454 |
| scrapy+md | #6 | kubernetes.io/docs/concepts/_print/ | 0.550 | kubernetes.io/docs/concepts/_print/ | 0.509 | kubernetes.io/de/docs/_print/ | 0.475 |
| crawlee | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.509 | kubernetes.io/docs/concepts/architecture/control-p | 0.501 | kubernetes.io/docs/setup/production-environment/to | 0.428 |
| colly+md | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.509 | kubernetes.io/docs/concepts/architecture/control-p | 0.501 | kubernetes.io/docs/concepts/architecture/control-p | 0.459 |
| playwright | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.509 | kubernetes.io/docs/concepts/architecture/control-p | 0.501 | kubernetes.io/docs/concepts/architecture/control-p | 0.459 |


**Q30: How does the Konnectivity service improve control plane to node communication?**
*(expects URL containing: `control-plane-node-communication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | kubernetes.io/docs/concepts/_print/ | 0.587 | kubernetes.io/docs/concepts/architecture/control-p | 0.587 | kubernetes.io/docs/concepts/architecture/_print/ | 0.587 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.598 | kubernetes.io/docs/concepts/architecture/control-p | 0.592 | kubernetes.io/docs/concepts/architecture/control-p | 0.512 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.598 | kubernetes.io/docs/concepts/architecture/control-p | 0.592 | kubernetes.io/docs/concepts/architecture/control-p | 0.512 |
| scrapy+md | #2 | kubernetes.io/docs/concepts/_print/ | 0.587 | kubernetes.io/it/docs/concepts/architecture/contro | 0.533 | kubernetes.io/de/docs/_print/ | 0.515 |
| crawlee | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.592 | kubernetes.io/docs/concepts/architecture/control-p | 0.587 | kubernetes.io/docs/concepts/architecture/cloud-con | 0.480 |
| colly+md | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.592 | kubernetes.io/docs/concepts/architecture/control-p | 0.587 | kubernetes.io/docs/concepts/architecture/control-p | 0.526 |
| playwright | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.592 | kubernetes.io/docs/concepts/architecture/control-p | 0.587 | kubernetes.io/docs/concepts/architecture/control-p | 0.526 |


**Q31: What are the two sorts of isolation for a pod in Kubernetes NetworkPolicies?**
*(expects URL containing: `network-policies`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | kubernetes.io/docs/concepts/services-networking/_p | 0.751 | kubernetes.io/docs/concepts/services-networking/ne | 0.751 | kubernetes.io/docs/concepts/_print/ | 0.751 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.759 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.669 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.648 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.759 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.669 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.648 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.751 | kubernetes.io/docs/concepts/_print/ | 0.662 | kubernetes.io/docs/concepts/_print/ | 0.643 |
| crawlee | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.751 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.662 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.643 |
| colly+md | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.751 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.662 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.643 |
| playwright | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.751 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.662 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.643 |


**Q32: What must be used to implement NetworkPolicies in a Kubernetes cluster?**
*(expects URL containing: `network-policies`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.746 | kubernetes.io/docs/reference/glossary/?all=true | 0.650 | kubernetes.io/docs/concepts/services-networking/ne | 0.649 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.682 | kubernetes.io/docs/concepts/services-networking/ne | 0.648 | kubernetes.io/docs/concepts/services-networking/ne | 0.647 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.682 | kubernetes.io/docs/concepts/services-networking/ne | 0.648 | kubernetes.io/docs/concepts/services-networking/ne | 0.647 |
| scrapy+md | miss | kubernetes.io/docs/reference/glossary/?all=true | 0.650 | kubernetes.io/docs/concepts/_print/ | 0.649 | kubernetes.io/docs/concepts/_print/ | 0.640 |
| crawlee | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.676 | kubernetes.io/docs/concepts/services-networking/ne | 0.649 | kubernetes.io/docs/concepts/services-networking/ne | 0.640 |
| colly+md | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.676 | kubernetes.io/docs/concepts/services-networking/ne | 0.649 | kubernetes.io/docs/concepts/services-networking/ne | 0.640 |
| playwright | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.676 | kubernetes.io/docs/concepts/services-networking/ne | 0.649 | kubernetes.io/docs/concepts/services-networking/ne | 0.640 |


**Q33: What is the principle of least privilege in RBAC?**
*(expects URL containing: `rbac-good-practices`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.579 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.509 | kubernetes.io/docs/concepts/security/_print/ | 0.509 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.515 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.514 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.457 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.515 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.514 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.457 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.509 | kubernetes.io/docs/concepts/_print/ | 0.482 | kubernetes.io/docs/concepts/_print/ | 0.449 |
| crawlee | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.531 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.509 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.449 |
| colly+md | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.531 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.509 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.449 |
| playwright | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.530 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.509 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.449 |


**Q34: How can users escalate their privileges in Kubernetes RBAC?**
*(expects URL containing: `rbac-good-practices`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | kubernetes.io/docs/reference/access-authn-authz/rb | 0.686 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.686 | kubernetes.io/docs/concepts/security/_print/ | 0.686 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.689 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.646 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.630 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.689 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.646 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.630 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.686 | kubernetes.io/docs/concepts/_print/ | 0.648 | kubernetes.io/docs/concepts/_print/ | 0.630 |
| crawlee | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.686 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.648 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.630 |
| colly+md | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.686 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.648 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.630 |
| playwright | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.686 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.648 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.630 |


**Q35: How can pods created by a Job communicate with each other using hostnames?**
*(expects URL containing: `job-with-pod-to-pod-communication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/concepts/workloads/pods/pod-hos | 0.577 | kubernetes.io/docs/concepts/workloads/pods/ | 0.530 | kubernetes.io/docs/concepts/_print/ | 0.530 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.722 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.632 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.626 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.722 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.632 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.626 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.530 | kubernetes.io/docs/concepts/_print/ | 0.525 | kubernetes.io/docs/concepts/_print/ | 0.519 |
| crawlee | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.722 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.688 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.565 |
| colly+md | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.722 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.688 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.584 |
| playwright | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.722 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.688 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.565 |


**Q36: What is the required configuration for a headless Service in a Job with pod-to-pod communication?**
*(expects URL containing: `job-with-pod-to-pod-communication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/concepts/workloads/_print/ | 0.510 | kubernetes.io/docs/concepts/_print/ | 0.510 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.510 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.642 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.614 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.592 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.642 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.614 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.592 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.507 | kubernetes.io/docs/concepts/_print/ | 0.490 | kubernetes.io/docs/concepts/_print/ | 0.481 |
| crawlee | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.642 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.608 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.511 |
| colly+md | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.642 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.608 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.556 |
| playwright | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.642 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.608 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.511 |


**Q37: What is Node Problem Detector?**
*(expects URL containing: `monitor-node-health`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/setup/best-practices/node-confo | 0.411 | kubernetes.io/docs/tasks/debug/debug-cluster/ | 0.399 | kubernetes.io/docs/concepts/architecture/_print/ | 0.397 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.566 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.542 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.538 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.566 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.542 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.538 |
| scrapy+md | miss | kubernetes.io/feed.xml | 0.429 | kubernetes.io/de/docs/_print/ | 0.409 | kubernetes.io/de/docs/_print/ | 0.405 |
| crawlee | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.560 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.538 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.477 |
| colly+md | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.560 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.538 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.477 |
| playwright | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.560 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.538 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.477 |


**Q38: How can you enable Node Problem Detector using kubectl?**
*(expects URL containing: `monitor-node-health`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/tasks/debug/debug-cluster/ | 0.526 | kubernetes.io/docs/tasks/debug/debug-cluster/ | 0.509 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.494 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.696 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.661 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.648 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.696 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.661 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.648 |
| scrapy+md | miss | kubernetes.io/feed.xml | 0.481 | kubernetes.io/docs/concepts/_print/ | 0.465 | kubernetes.io/feed.xml | 0.456 |
| crawlee | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.699 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.618 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.608 |
| colly+md | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.699 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.618 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.608 |
| playwright | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.699 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.618 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.608 |


**Q39: What command is used to safely evict all pods from a node before maintenance?**
*(expects URL containing: `safely-drain-node`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.642 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.637 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.607 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.622 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.592 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.583 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.622 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.592 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.583 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.573 | kubernetes.io/docs/concepts/_print/ | 0.540 | kubernetes.io/docs/concepts/_print/ | 0.537 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.612 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.588 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.578 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.588 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.578 | kubernetes.io/docs/concepts/scheduling-eviction/ap | 0.573 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.612 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.588 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.578 |


**Q40: What should you configure to ensure workloads remain available during maintenance?**
*(expects URL containing: `safely-drain-node`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #44 | kubernetes.io/docs/reference/command-line-tools-re | 0.500 | kubernetes.io/docs/reference/command-line-tools-re | 0.475 | kubernetes.io/docs/reference/command-line-tools-re | 0.474 |
| crawl4ai | miss | kubernetes.io/docs/tasks/run-application/configure | 0.471 | kubernetes.io/docs/concepts/cluster-administration | 0.471 | kubernetes.io/docs/tasks/configure-pod-container/a | 0.468 |
| crawl4ai-raw | miss | kubernetes.io/docs/tasks/run-application/configure | 0.471 | kubernetes.io/docs/concepts/cluster-administration | 0.471 | kubernetes.io/docs/tasks/configure-pod-container/a | 0.468 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.453 | kubernetes.io/feed.xml | 0.450 | kubernetes.io/docs/concepts/_print/ | 0.449 |
| crawlee | miss | kubernetes.io/docs/concepts/workloads/management/ | 0.496 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.490 | kubernetes.io/docs/concepts/workloads/workload-api | 0.473 |
| colly+md | miss | kubernetes.io/docs/concepts/workloads/management/ | 0.496 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.490 | kubernetes.io/docs/concepts/workloads/management/ | 0.490 |
| playwright | miss | kubernetes.io/docs/concepts/workloads/management/ | 0.496 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.490 | kubernetes.io/docs/concepts/workloads/management/ | 0.490 |


**Q41: What is Kubernetes?**
*(expects URL containing: `concepts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/overview/ | 0.689 | kubernetes.io/docs/concepts/overview/_print/ | 0.668 | kubernetes.io/docs/home/ | 0.656 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/overview/ | 0.665 | kubernetes.io/docs/concepts/overview/ | 0.663 | kubernetes.io/docs/concepts/overview/ | 0.624 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/overview/ | 0.665 | kubernetes.io/docs/concepts/overview/ | 0.663 | kubernetes.io/docs/concepts/overview/ | 0.624 |
| scrapy+md | #1 | kubernetes.io/docs/concepts/_print/ | 0.654 | kubernetes.io/docs/concepts/_print/ | 0.649 | kubernetes.io/docs/reference/glossary/?all=true | 0.632 |
| crawlee | #2 | kubernetes.io/ | 0.656 | kubernetes.io/docs/concepts/overview/ | 0.654 | kubernetes.io/docs/concepts/overview/ | 0.649 |
| colly+md | #2 | kubernetes.io/ | 0.660 | kubernetes.io/docs/concepts/overview/ | 0.654 | kubernetes.io/docs/concepts/overview/ | 0.649 |
| playwright | #2 | kubernetes.io/ | 0.660 | kubernetes.io/docs/concepts/overview/ | 0.654 | kubernetes.io/docs/concepts/overview/ | 0.649 |


**Q42: How do I change the default StorageClass in Kubernetes?**
*(expects URL containing: `change-default-storage-class`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/concepts/storage/storage-classe | 0.715 | kubernetes.io/docs/concepts/storage/storage-classe | 0.713 | kubernetes.io/docs/concepts/storage/_print/ | 0.713 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.758 | kubernetes.io/docs/tasks/administer-cluster/change | 0.724 | kubernetes.io/docs/concepts/storage/storage-classe | 0.707 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.758 | kubernetes.io/docs/tasks/administer-cluster/change | 0.724 | kubernetes.io/docs/concepts/storage/storage-classe | 0.707 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.713 | kubernetes.io/docs/concepts/_print/ | 0.640 | kubernetes.io/docs/concepts/_print/ | 0.598 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.727 | kubernetes.io/docs/tasks/administer-cluster/change | 0.716 | kubernetes.io/docs/concepts/storage/storage-classe | 0.692 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.727 | kubernetes.io/docs/concepts/storage/storage-classe | 0.692 | kubernetes.io/docs/concepts/storage/storage-classe | 0.687 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.727 | kubernetes.io/docs/tasks/administer-cluster/change | 0.716 | kubernetes.io/docs/concepts/storage/storage-classe | 0.692 |


**Q43: Why might I want to change the default StorageClass?**
*(expects URL containing: `change-default-storage-class`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/concepts/_print/ | 0.621 | kubernetes.io/docs/concepts/storage/_print/ | 0.621 | kubernetes.io/docs/concepts/storage/storage-classe | 0.621 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.680 | kubernetes.io/docs/tasks/administer-cluster/change | 0.648 | kubernetes.io/docs/concepts/storage/storage-classe | 0.602 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.680 | kubernetes.io/docs/tasks/administer-cluster/change | 0.648 | kubernetes.io/docs/concepts/storage/storage-classe | 0.602 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.621 | kubernetes.io/docs/concepts/_print/ | 0.544 | kubernetes.io/docs/concepts/_print/ | 0.527 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.649 | kubernetes.io/docs/tasks/administer-cluster/change | 0.635 | kubernetes.io/docs/concepts/storage/storage-classe | 0.596 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.635 | kubernetes.io/docs/concepts/storage/storage-classe | 0.596 | kubernetes.io/docs/concepts/storage/storage-classe | 0.588 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.649 | kubernetes.io/docs/tasks/administer-cluster/change | 0.635 | kubernetes.io/docs/concepts/storage/storage-classe | 0.596 |


**Q44: What is a kubeconfig file?**
*(expects URL containing: `organize-cluster-access-kubeconfig`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.662 | kubernetes.io/docs/concepts/configuration/_print/ | 0.640 | kubernetes.io/docs/concepts/configuration/organize | 0.640 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.635 | kubernetes.io/docs/concepts/configuration/organize | 0.610 | kubernetes.io/docs/concepts/configuration/organize | 0.598 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.635 | kubernetes.io/docs/concepts/configuration/organize | 0.610 | kubernetes.io/docs/concepts/configuration/organize | 0.598 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.640 | kubernetes.io/docs/concepts/_print/ | 0.592 | kubernetes.io/docs/concepts/_print/ | 0.529 |
| crawlee | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.640 | kubernetes.io/docs/concepts/configuration/organize | 0.592 | kubernetes.io/docs/concepts/configuration/organize | 0.586 |
| colly+md | miss | kubernetes.io/docs/concepts/configuration/organize | 0.640 | kubernetes.io/docs/concepts/configuration/organize | 0.592 | kubernetes.io/docs/concepts/configuration/organize | 0.586 |
| playwright | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.639 | kubernetes.io/docs/concepts/configuration/organize | 0.593 | kubernetes.io/docs/concepts/configuration/organize | 0.586 |


**Q45: How does kubectl determine which kubeconfig file to use?**
*(expects URL containing: `organize-cluster-access-kubeconfig`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | kubernetes.io/docs/concepts/_print/ | 0.670 | kubernetes.io/docs/concepts/configuration/_print/ | 0.670 | kubernetes.io/docs/concepts/configuration/organize | 0.670 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.648 | kubernetes.io/docs/concepts/configuration/organize | 0.610 | kubernetes.io/docs/concepts/configuration/organize | 0.548 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.648 | kubernetes.io/docs/concepts/configuration/organize | 0.610 | kubernetes.io/docs/concepts/configuration/organize | 0.548 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.676 | kubernetes.io/docs/concepts/_print/ | 0.605 | kubernetes.io/docs/concepts/_print/ | 0.500 |
| crawlee | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.676 | kubernetes.io/docs/concepts/configuration/organize | 0.605 | kubernetes.io/docs/tasks/access-application-cluste | 0.546 |
| colly+md | miss | kubernetes.io/docs/concepts/configuration/organize | 0.676 | kubernetes.io/docs/concepts/configuration/organize | 0.605 | kubernetes.io/docs/tasks/access-application-cluste | 0.546 |
| playwright | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.676 | kubernetes.io/docs/concepts/configuration/organize | 0.605 | kubernetes.io/docs/tasks/access-application-cluste | 0.546 |


**Q46: What is dynamic volume provisioning in Kubernetes?**
*(expects URL containing: `dynamic-provisioning`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.803 | kubernetes.io/docs/concepts/storage/_print/ | 0.682 | kubernetes.io/docs/concepts/_print/ | 0.682 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.724 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.624 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.580 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.724 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.624 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.580 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.683 | kubernetes.io/docs/concepts/_print/ | 0.600 | kubernetes.io/docs/concepts/_print/ | 0.579 |
| crawlee | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.725 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.683 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.608 |
| colly+md | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.725 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.683 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.620 |
| playwright | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.725 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.683 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.620 |


**Q47: How can a cluster administrator enable dynamic provisioning?**
*(expects URL containing: `dynamic-provisioning`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.650 | kubernetes.io/docs/concepts/_print/ | 0.566 | kubernetes.io/docs/concepts/storage/_print/ | 0.566 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.624 | kubernetes.io/docs/setup/best-practices/cluster-la | 0.536 | kubernetes.io/docs/setup/production-environment/to | 0.535 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.624 | kubernetes.io/docs/setup/best-practices/cluster-la | 0.536 | kubernetes.io/docs/setup/production-environment/to | 0.535 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.565 | kubernetes.io/docs/concepts/_print/ | 0.496 | kubernetes.io/docs/concepts/_print/ | 0.475 |
| crawlee | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.588 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.565 | kubernetes.io/docs/concepts/cluster-administration | 0.490 |
| colly+md | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.588 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.565 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.525 |
| playwright | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.588 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.565 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.525 |


**Q48: What command-line flag is used to enable the API Priority and Fairness feature?**
*(expects URL containing: `flow-control`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.714 | kubernetes.io/docs/concepts/cluster-administration | 0.640 | kubernetes.io/docs/concepts/cluster-administration | 0.602 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.623 | kubernetes.io/docs/concepts/cluster-administration | 0.608 | kubernetes.io/docs/concepts/cluster-administration | 0.579 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.623 | kubernetes.io/docs/concepts/cluster-administration | 0.608 | kubernetes.io/docs/concepts/cluster-administration | 0.579 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.603 | kubernetes.io/docs/concepts/_print/ | 0.581 | kubernetes.io/docs/concepts/_print/ | 0.521 |
| crawlee | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.620 | kubernetes.io/docs/concepts/cluster-administration | 0.603 | kubernetes.io/docs/concepts/cluster-administration | 0.581 |
| colly+md | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.620 | kubernetes.io/docs/concepts/cluster-administration | 0.603 | kubernetes.io/docs/concepts/cluster-administration | 0.581 |
| playwright | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.620 | kubernetes.io/docs/concepts/cluster-administration | 0.603 | kubernetes.io/docs/concepts/cluster-administration | 0.581 |


**Q49: What are the two types of resources involved in the flow control API?**
*(expects URL containing: `flow-control`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | kubernetes.io/docs/reference/generated/kubernetes- | 0.495 | kubernetes.io/docs/concepts/_print/ | 0.482 | kubernetes.io/docs/concepts/cluster-administration | 0.482 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.489 | kubernetes.io/docs/concepts/cluster-administration | 0.454 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.450 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.489 | kubernetes.io/docs/concepts/cluster-administration | 0.454 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.450 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.482 | kubernetes.io/docs/reference/glossary/?all=true | 0.469 | kubernetes.io/docs/concepts/_print/ | 0.458 |
| crawlee | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.482 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.458 | kubernetes.io/docs/concepts/cluster-administration | 0.457 |
| colly+md | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.482 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.458 | kubernetes.io/docs/concepts/cluster-administration | 0.457 |
| playwright | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.482 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.458 | kubernetes.io/docs/concepts/cluster-administration | 0.457 |


**Q50: What are the main components of a Kubernetes cluster?**
*(expects URL containing: `architecture`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | kubernetes.io/docs/concepts/overview/components/ | 0.711 | kubernetes.io/docs/concepts/overview/_print/ | 0.709 | kubernetes.io/docs/concepts/_print/ | 0.703 |
| crawl4ai | #2 | kubernetes.io/docs/concepts/overview/components/ | 0.699 | kubernetes.io/docs/concepts/architecture/ | 0.640 | kubernetes.io/docs/concepts/architecture/ | 0.635 |
| crawl4ai-raw | #2 | kubernetes.io/docs/concepts/overview/components/ | 0.699 | kubernetes.io/docs/concepts/architecture/ | 0.640 | kubernetes.io/docs/concepts/architecture/ | 0.635 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.698 | kubernetes.io/docs/concepts/_print/ | 0.657 | kubernetes.io/it/docs/_print/ | 0.648 |
| crawlee | #2 | kubernetes.io/docs/concepts/overview/components/ | 0.707 | kubernetes.io/docs/concepts/architecture/ | 0.643 | kubernetes.io/docs/concepts/architecture/ | 0.639 |
| colly+md | #2 | kubernetes.io/docs/concepts/overview/components/ | 0.707 | kubernetes.io/docs/concepts/architecture/ | 0.643 | kubernetes.io/docs/concepts/architecture/ | 0.639 |
| playwright | #2 | kubernetes.io/docs/concepts/overview/components/ | 0.707 | kubernetes.io/docs/concepts/architecture/ | 0.641 | kubernetes.io/docs/concepts/overview/components/ | 0.638 |


**Q51: What is the role of the kube-scheduler in a Kubernetes cluster?**
*(expects URL containing: `architecture`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | kubernetes.io/docs/reference/command-line-tools-re | 0.634 | kubernetes.io/docs/concepts/scheduling-eviction/ku | 0.611 | kubernetes.io/docs/concepts/_print/ | 0.600 |
| crawl4ai | #4 | kubernetes.io/docs/concepts/scheduling-eviction/ku | 0.598 | kubernetes.io/it/docs/concepts/ | 0.576 | kubernetes.io/docs/concepts/scheduling-eviction/ku | 0.562 |
| crawl4ai-raw | #4 | kubernetes.io/docs/concepts/scheduling-eviction/ku | 0.598 | kubernetes.io/it/docs/concepts/ | 0.576 | kubernetes.io/docs/concepts/scheduling-eviction/ku | 0.562 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.600 | kubernetes.io/docs/concepts/_print/ | 0.568 | kubernetes.io/docs/concepts/_print/ | 0.561 |
| crawlee | #2 | kubernetes.io/docs/concepts/scheduling-eviction/ku | 0.633 | kubernetes.io/docs/concepts/architecture/ | 0.567 | kubernetes.io/docs/concepts/scheduling-eviction/ku | 0.561 |
| colly+md | #2 | kubernetes.io/docs/concepts/scheduling-eviction/ku | 0.633 | kubernetes.io/docs/concepts/architecture/ | 0.568 | kubernetes.io/docs/concepts/scheduling-eviction/ku | 0.561 |
| playwright | #2 | kubernetes.io/docs/concepts/scheduling-eviction/ku | 0.633 | kubernetes.io/docs/concepts/architecture/ | 0.567 | kubernetes.io/docs/concepts/scheduling-eviction/ku | 0.561 |


**Q52: What is the purpose of Kubernetes auditing?**
*(expects URL containing: `audit`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.755 | kubernetes.io/docs/concepts/security/_print/ | 0.688 | kubernetes.io/docs/concepts/security/_print/ | 0.590 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.657 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.611 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.602 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.657 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.611 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.602 |
| scrapy+md | miss | kubernetes.io/blog/2021/10/05/nsa-cisa-kubernetes- | 0.674 | kubernetes.io/blog/2021/10/05/nsa-cisa-kubernetes- | 0.601 | kubernetes.io/docs/concepts/_print/ | 0.575 |
| crawlee | #2 | kubernetes.io/docs/concepts/security/ | 0.716 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.643 | kubernetes.io/docs/concepts/security/ | 0.572 |
| colly+md | #2 | kubernetes.io/docs/concepts/security/ | 0.716 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.643 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.588 |
| playwright | #2 | kubernetes.io/docs/concepts/security/ | 0.715 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.643 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.588 |


**Q53: What are the defined stages for audit events in Kubernetes?**
*(expects URL containing: `audit`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.753 | kubernetes.io/docs/concepts/security/_print/ | 0.608 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.534 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.707 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.570 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.568 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.707 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.570 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.568 |
| scrapy+md | miss | kubernetes.io/blog/2021/10/05/nsa-cisa-kubernetes- | 0.574 | kubernetes.io/blog/2021/10/05/nsa-cisa-kubernetes- | 0.571 | kubernetes.io/blog/2021/12/09/pod-security-admissi | 0.537 |
| crawlee | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.693 | kubernetes.io/docs/concepts/security/ | 0.628 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.530 |
| colly+md | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.693 | kubernetes.io/docs/concepts/security/ | 0.628 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.530 |
| playwright | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.693 | kubernetes.io/docs/concepts/security/ | 0.627 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.530 |


**Q54: What is the example YAML file used to deploy a simple webserver application running inside a Windows container?**
*(expects URL containing: `user-guide`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.715 | kubernetes.io/docs/concepts/_print/ | 0.678 | kubernetes.io/docs/concepts/windows/_print/ | 0.678 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.616 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.501 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.487 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.616 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.501 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.487 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.682 | kubernetes.io/docs/concepts/_print/ | 0.493 | kubernetes.io/docs/concepts/_print/ | 0.454 |
| crawlee | #1 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.623 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.493 | kubernetes.io/docs/tasks/access-application-cluste | 0.481 |
| colly+md | #1 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.623 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.493 | kubernetes.io/docs/tasks/access-application-cluste | 0.481 |
| playwright | #1 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.623 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.493 | kubernetes.io/docs/tasks/access-application-cluste | 0.481 |


**Q55: How can Windows container workloads be configured to use Group Managed Service Accounts (GMSA)?**
*(expects URL containing: `user-guide`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #9 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.718 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.647 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.640 |
| crawl4ai | #12 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.667 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.658 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.643 |
| crawl4ai-raw | #12 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.667 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.658 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.643 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.479 | kubernetes.io/docs/concepts/_print/ | 0.448 | kubernetes.io/docs/concepts/_print/ | 0.430 |
| crawlee | #11 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.658 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.649 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.640 |
| colly+md | #11 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.658 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.649 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.640 |
| playwright | #11 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.658 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.649 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.640 |


**Q56: How do I define a default memory resource limit for a namespace?**
*(expects URL containing: `manage-resources`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | kubernetes.io/docs/tasks/configure-pod-container/a | 0.548 | kubernetes.io/docs/concepts/policy/resource-quotas | 0.534 | kubernetes.io/docs/concepts/_print/ | 0.534 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.662 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.596 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.595 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.662 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.596 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.595 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.534 | kubernetes.io/docs/concepts/_print/ | 0.510 | kubernetes.io/docs/concepts/_print/ | 0.489 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.658 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.627 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.595 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.658 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.627 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.595 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.658 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.627 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.595 |


**Q57: What is the purpose of configuring overall memory and CPU resource limits for a namespace?**
*(expects URL containing: `manage-resources`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | kubernetes.io/docs/tasks/configure-pod-container/a | 0.595 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.588 | kubernetes.io/docs/concepts/configuration/windows- | 0.569 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.593 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.592 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.587 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.593 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.592 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.587 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.555 | kubernetes.io/feed.xml | 0.551 | kubernetes.io/docs/concepts/_print/ | 0.550 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.599 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.597 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.585 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.599 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.597 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.585 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.599 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.597 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.585 |


</details>

## mdn-css

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawlee | 80% (48/60) | 98% (59/60) | 98% (59/60) | 100% (60/60) | 100% (60/60) | 0.891 | 3891 | 300 |
| crawl4ai | 78% (47/60) | 98% (59/60) | 100% (60/60) | 100% (60/60) | 100% (60/60) | 0.885 | 3864 | 300 |
| crawl4ai-raw | 78% (47/60) | 98% (59/60) | 100% (60/60) | 100% (60/60) | 100% (60/60) | 0.885 | 3864 | 300 |
| playwright | 77% (46/60) | 92% (55/60) | 93% (56/60) | 98% (59/60) | 100% (60/60) | 0.854 | 4168 | 300 |
| colly+md | 30% (18/60) | 37% (22/60) | 37% (22/60) | 37% (22/60) | 37% (22/60) | 0.328 | 4190 | 289 |
| markcrawl | 22% (13/60) | 25% (15/60) | 27% (16/60) | 30% (18/60) | 32% (19/60) | 0.245 | 1006 | 300 |
| scrapy+md | 12% (7/60) | 13% (8/60) | 13% (8/60) | 13% (8/60) | 13% (8/60) | 0.126 | 621 | 300 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for mdn-css</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is auto-placement in CSS grid layout?**
*(expects URL containing: `Auto-placement`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.771 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.690 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.659 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.703 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.676 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.674 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.703 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.676 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.674 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.419 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.362 | developer.mozilla.org/en-US/docs/Web/CSS | 0.359 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.698 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.667 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.666 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.727 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.704 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.683 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.709 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.683 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.649 |


**Q2: How can you control the size of automatically created rows in the implicit grid?**
*(expects URL containing: `Auto-placement`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.680 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.570 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.546 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.623 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.576 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.573 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.623 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.576 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.573 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.291 | developer.mozilla.org/ja/docs/Web/CSS/Reference/Pr | 0.290 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.262 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.612 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.551 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.539 |
| colly+md | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.544 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.540 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.531 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.669 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.544 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.537 |


**Q3: What does the CSS scoping module define?**
*(expects URL containing: `Scoping`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.606 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.606 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.569 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.557 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.551 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.526 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.557 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.551 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.526 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.518 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.487 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.480 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.573 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.570 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.569 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.639 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.569 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.546 |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.573 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.570 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.569 |


**Q4: How do selectors behave within a shadow tree in CSS?**
*(expects URL containing: `Scoping`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.572 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.568 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ne | 0.562 |
| crawl4ai | #4 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.575 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.565 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.564 |
| crawl4ai-raw | #4 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.575 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.565 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.564 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.447 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.444 | developer.mozilla.org/en-US/docs/Web/XML/XSLT/Guid | 0.438 |
| crawlee | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.571 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.561 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.559 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.641 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.621 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.616 |
| playwright | #4 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.569 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.566 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.560 |


**Q5: What is the Fetch API used for?**
*(expects URL containing: `Fetch_API`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.243 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.228 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.225 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.576 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.552 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.541 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.576 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.552 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.541 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/API/XMLHttpRe | 0.433 | developer.mozilla.org/en-US/docs/Web/API/XMLHttpRe | 0.371 | developer.mozilla.org/zh-CN/docs/Web/HTTP/Referenc | 0.366 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.561 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.557 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.540 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/API/Fetch/API | 0.588 | developer.mozilla.org/en-US/docs/Web/API/Fetch/API | 0.545 | developer.mozilla.org/en-US/docs/Web/API/Fetch/API | 0.540 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.557 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.552 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.540 |


**Q6: What method is used to fetch a resource with the Fetch API?**
*(expects URL containing: `Fetch_API`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.286 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.279 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.218 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.550 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.550 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.522 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.550 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.550 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.522 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/API/XMLHttpRe | 0.416 | developer.mozilla.org/zh-CN/docs/Web/HTTP/Referenc | 0.386 | developer.mozilla.org/zh-CN/docs/Web/HTTP/Referenc | 0.371 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.550 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.531 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.531 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/API/Fetch/API | 0.555 | developer.mozilla.org/en-US/docs/Web/API/Fetch/API | 0.545 | developer.mozilla.org/en-US/docs/Web/API/Fetch/API | 0.528 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.550 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.546 | developer.mozilla.org/en-US/docs/Web/API/Fetch_API | 0.531 |


**Q7: What is the purpose of the :target pseudo-class in CSS?**
*(expects URL containing: `Using_:target`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.698 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.659 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.608 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.636 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.583 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.563 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.636 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.583 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.563 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/HTML/Referenc | 0.421 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.411 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.405 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.617 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.573 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.572 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.589 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.575 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ps | 0.575 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.628 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.573 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.554 |


**Q8: How can you style all targeted elements using the universal selector?**
*(expects URL containing: `Using_:target`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #6 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.574 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.572 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.564 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.583 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.577 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.559 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.583 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.577 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.559 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.430 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.427 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.425 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.574 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.565 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.543 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.574 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.553 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.552 |
| playwright | #8 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.574 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.574 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.545 |


**Q9: What types of images can be used in CSS?**
*(expects URL containing: `Images`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #7 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.617 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.581 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.555 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.615 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.596 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.593 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.615 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.596 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.593 |
| scrapy+md | #2 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.543 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.532 | developer.mozilla.org/en-US/docs/Web/CSS | 0.525 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.619 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.617 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.601 |
| colly+md | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.617 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.613 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.605 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.619 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.617 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.610 |


**Q10: What is the image-resolution property in CSS?**
*(expects URL containing: `Images`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #11 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.603 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.595 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.591 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.618 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.570 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.541 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.618 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.570 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.541 |
| scrapy+md | #1 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.497 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.454 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.451 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.602 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.569 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.552 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.597 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.569 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.564 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.597 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.569 | developer.mozilla.org/en-US/docs/Web/HTML/Guides/R | 0.564 |


**Q11: What are the two types of CSS properties based on inheritance?**
*(expects URL containing: `Inheritance`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.622 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.587 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.572 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.607 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.597 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.584 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.607 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.597 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.584 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.559 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.461 | developer.mozilla.org/en-US/docs/Web/CSS | 0.455 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.600 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.581 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.565 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.609 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.596 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.587 |
| playwright | #7 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.619 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.596 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.586 |


**Q12: What happens when no value is specified for a non-inherited property on an element?**
*(expects URL containing: `Inheritance`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.453 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.444 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.440 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.493 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.484 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.478 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.493 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.484 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.478 |
| scrapy+md | miss | developer.mozilla.org/ko/docs/Web/JavaScript/Refer | 0.384 | developer.mozilla.org/ja/docs/Web/JavaScript/Refer | 0.372 | developer.mozilla.org/ru/docs/Web/JavaScript/Refer | 0.364 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.501 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.497 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.467 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.557 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.467 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.464 |
| playwright | #9 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.467 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.464 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.464 |


**Q13: What are at-rules in CSS?**
*(expects URL containing: `At-rules`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.761 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.665 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ne | 0.655 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.682 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.650 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.632 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.682 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.650 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.632 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.519 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.444 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.442 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.675 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.654 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.646 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.728 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.661 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.660 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.678 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.661 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.654 |


**Q14: What is the purpose of the @import at-rule?**
*(expects URL containing: `At-rules`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.612 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.502 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.494 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.593 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.560 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.484 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.593 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.560 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.484 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.381 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.379 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.379 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.572 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.568 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.488 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.577 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.573 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.551 |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.573 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.566 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.511 |


**Q15: What is the purpose of the HTTP Observatory?**
*(expects URL containing: `observatory`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.305 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.270 | developer.mozilla.org/en-US/docs/Web/CSS | 0.268 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/HTTP | 0.436 | developer.mozilla.org/en-US/observatory | 0.423 | developer.mozilla.org/en-US/docs/Web/HTTP | 0.408 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/HTTP | 0.436 | developer.mozilla.org/en-US/observatory | 0.423 | developer.mozilla.org/en-US/docs/Web/HTTP | 0.408 |
| scrapy+md | miss | developer.mozilla.org/zh-CN/docs/Web/HTTP/Referenc | 0.353 | developer.mozilla.org/en-US/docs/Web/API/XMLHttpRe | 0.317 | developer.mozilla.org/zh-CN/docs/Web/HTTP/Referenc | 0.313 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/HTTP | 0.550 | developer.mozilla.org/en-US/observatory | 0.527 | developer.mozilla.org/en-US/docs/Web/HTTP | 0.454 |
| colly+md | #1 | developer.mozilla.org/en-US/observatory | 0.520 | developer.mozilla.org/en-US/docs/Web/HTTP | 0.454 | developer.mozilla.org/en-US/observatory | 0.447 |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/HTTP | 0.550 | developer.mozilla.org/en-US/observatory | 0.527 | developer.mozilla.org/en-US/docs/Web/HTTP | 0.454 |


**Q16: How many websites has the HTTP Observatory provided insights to?**
*(expects URL containing: `observatory`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.282 | developer.mozilla.org/en-US/docs/Web/CSS | 0.276 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.273 |
| crawl4ai | #1 | developer.mozilla.org/en-US/observatory | 0.443 | developer.mozilla.org/en-US/docs/Web/HTTP | 0.438 | developer.mozilla.org/en-US/blog/ | 0.433 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/observatory | 0.443 | developer.mozilla.org/en-US/docs/Web/HTTP | 0.438 | developer.mozilla.org/en-US/blog/ | 0.433 |
| scrapy+md | miss | developer.mozilla.org/zh-CN/docs/Web/HTTP/Referenc | 0.337 | developer.mozilla.org/zh-CN/docs/Web/HTTP/Referenc | 0.318 | developer.mozilla.org/en-US/docs/Web/API/XMLHttpRe | 0.283 |
| crawlee | #1 | developer.mozilla.org/en-US/observatory | 0.537 | developer.mozilla.org/en-US/docs/Web/HTTP | 0.523 | developer.mozilla.org/en-US/docs/Web | 0.452 |
| colly+md | #1 | developer.mozilla.org/en-US/observatory | 0.526 | developer.mozilla.org/en-US/docs/Web/HTTP | 0.450 | developer.mozilla.org/en-US/docs/Web/Security | 0.429 |
| playwright | #1 | developer.mozilla.org/en-US/observatory | 0.537 | developer.mozilla.org/en-US/docs/Web/HTTP | 0.523 | developer.mozilla.org/en-US/docs/Web | 0.452 |


**Q17: What properties are defined by the CSS box model?**
*(expects URL containing: `Box_model`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.661 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.657 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.656 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.697 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.665 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.661 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.698 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.665 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.660 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.558 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.493 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.473 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.696 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.673 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.655 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.705 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.703 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.672 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.696 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.673 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.655 |


**Q18: What does the CSS box model describe about the layout of elements?**
*(expects URL containing: `Box_model`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.673 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.642 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.640 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.652 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.647 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.644 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.652 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.647 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.644 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.554 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.476 | developer.mozilla.org/en-US/docs/Web/CSS | 0.474 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.675 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.646 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.640 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.681 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.661 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.656 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.675 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.646 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.640 |


**Q19: How does the `order` property affect the visual order of flex items?**
*(expects URL containing: `Ordering_items`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.696 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.696 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.625 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.750 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.750 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.742 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.750 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.750 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.742 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.460 | developer.mozilla.org/en-US/docs/Web/HTML/Referenc | 0.403 | developer.mozilla.org/en-US/docs/Web/HTML/Referenc | 0.345 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.743 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.727 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.699 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.742 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.705 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.692 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.742 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.705 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.692 |


**Q20: What should authors avoid when using the `order` property in flexbox layouts?**
*(expects URL containing: `Ordering_items`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.609 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.594 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.590 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.669 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.656 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.606 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.669 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.656 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.606 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.463 | developer.mozilla.org/en-US/docs/Web/HTML/Referenc | 0.384 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.370 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.639 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.638 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.613 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.618 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.617 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.638 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.615 |


**Q21: What are the types of easing functions defined in the CSS easing functions module?**
*(expects URL containing: `Easing_functions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.582 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.525 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.519 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.703 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.601 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.591 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.703 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.601 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.591 |
| scrapy+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.644 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.466 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.448 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.708 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.582 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.555 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.666 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.612 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.582 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.708 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.582 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.555 |


**Q22: How do cubic bezier easing functions enhance user interface elements?**
*(expects URL containing: `Easing_functions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.479 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.457 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.439 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.588 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.454 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.450 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.588 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.454 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.450 |
| scrapy+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.523 | developer.mozilla.org/en-US/docs/Glossary/Bezier_c | 0.419 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.398 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.604 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.457 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.432 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.628 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.476 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.469 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.604 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.489 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.434 |


**Q23: What are Uniform Resource Identifiers (URI)?**
*(expects URL containing: `URI`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.338 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.335 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.319 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/URI | 0.502 | developer.mozilla.org/en-US/docs/Glossary/XHTML | 0.458 | developer.mozilla.org/en-US/docs/Web/URI | 0.432 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/URI | 0.502 | developer.mozilla.org/en-US/docs/Glossary/XHTML | 0.458 | developer.mozilla.org/en-US/docs/Web/URI | 0.432 |
| scrapy+md | #1 | developer.mozilla.org/zh-CN/docs/Web/JavaScript/Re | 0.449 | developer.mozilla.org/fr/docs/Web/JavaScript/Refer | 0.413 | developer.mozilla.org/zh-CN/docs/Web/JavaScript/Re | 0.349 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/URI | 0.525 | developer.mozilla.org/en-US/docs/Web/URI | 0.455 | developer.mozilla.org/en-US/docs/Glossary/XHTML | 0.427 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/URI | 0.549 | developer.mozilla.org/en-US/docs/Web/URI | 0.548 | developer.mozilla.org/en-US/docs/Glossary/XHTML | 0.427 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/URI | 0.525 | developer.mozilla.org/en-US/docs/Web/URI | 0.455 | developer.mozilla.org/en-US/docs/Glossary/XHTML | 0.427 |


**Q24: What is the purpose of the fragment in a URI?**
*(expects URL containing: `URI`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.525 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.412 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.352 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/URI | 0.569 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.497 | developer.mozilla.org/en-US/docs/Web/URI | 0.480 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/URI | 0.569 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.497 | developer.mozilla.org/en-US/docs/Web/URI | 0.480 |
| scrapy+md | #1 | developer.mozilla.org/zh-CN/docs/Web/JavaScript/Re | 0.329 | developer.mozilla.org/fr/docs/Web/JavaScript/Refer | 0.322 | developer.mozilla.org/fr/docs/Web/JavaScript/Refer | 0.320 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/URI | 0.615 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.507 | developer.mozilla.org/en-US/docs/Web/URI | 0.480 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/URI | 0.510 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.390 | developer.mozilla.org/en-US/docs/Web/URI | 0.376 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/URI | 0.615 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.531 | developer.mozilla.org/en-US/docs/Web/URI | 0.480 |


**Q25: What problem does scroll anchoring solve?**
*(expects URL containing: `Overview`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.665 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.497 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.478 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.636 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.616 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.604 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.636 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.616 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.604 |
| scrapy+md | #43 | developer.mozilla.org/ja/docs/Web/CSS/Reference/Pr | 0.372 | developer.mozilla.org/ja/docs/Web/CSS/Reference/Pr | 0.308 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.294 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.612 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.597 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.596 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.601 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.586 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.581 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.612 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.599 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.596 |


**Q26: How can I disable scroll anchoring in my document?**
*(expects URL containing: `Overview`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.641 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.506 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.477 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.714 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.624 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.587 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.714 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.624 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.587 |
| scrapy+md | #36 | developer.mozilla.org/ja/docs/Web/CSS/Reference/Pr | 0.401 | developer.mozilla.org/en-US/docs/Web/API/Event/pre | 0.352 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.350 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.662 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.594 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.593 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.620 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.601 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.572 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.660 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.594 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.593 |


**Q27: How can I assign names to grid lines in CSS?**
*(expects URL containing: `Named_grid_lines`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.615 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.614 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.614 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.625 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.622 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.614 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.625 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.622 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.614 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.418 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.412 | developer.mozilla.org/en-US/docs/Web/CSS | 0.405 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.621 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.608 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.598 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.644 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.614 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.609 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.659 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.614 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.611 |


**Q28: What happens when I use the repeat() syntax for naming grid lines?**
*(expects URL containing: `Named_grid_lines`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.586 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.545 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.523 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.639 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.624 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.571 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.639 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.624 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.571 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.332 | developer.mozilla.org/ja/docs/Web/SVG/Reference/At | 0.324 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.313 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.630 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.613 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.560 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.648 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.602 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.579 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.648 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.603 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.579 |


**Q29: What does the CSS box alignment module specify?**
*(expects URL containing: `Box_alignment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.663 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.625 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.618 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.693 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.662 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.650 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.693 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.662 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.650 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.514 | developer.mozilla.org/en-US/docs/Web/CSS | 0.444 | developer.mozilla.org/en-US/docs/Web/CSS | 0.412 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.700 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.688 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.654 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.715 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.683 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.658 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.700 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.688 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.667 |


**Q30: How is alignment linked to writing modes in CSS?**
*(expects URL containing: `Box_alignment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #29 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Wr | 0.672 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.637 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.611 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.650 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.647 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.635 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.650 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.647 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.635 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS | 0.454 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.452 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.445 |
| crawlee | #9 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Wr | 0.618 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.616 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.702 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.666 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Wr | 0.658 |
| playwright | #12 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.681 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.666 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.644 |


**Q31: What are CSS logical properties and values?**
*(expects URL containing: `Logical_properties_and_values`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.658 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.615 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.611 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.828 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.702 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.682 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.828 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.702 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.682 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.610 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.514 | developer.mozilla.org/en-US/docs/Web/CSS | 0.508 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.672 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.648 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.645 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.667 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.627 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.624 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.672 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.667 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.649 |


**Q32: How do logical properties define direction-relative equivalents to physical properties?**
*(expects URL containing: `Logical_properties_and_values`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.474 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.443 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.401 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.521 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.483 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.478 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.521 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.483 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.478 |
| scrapy+md | miss | developer.mozilla.org/ko/docs/Web/JavaScript/Refer | 0.332 | developer.mozilla.org/ko/docs/Web/JavaScript/Refer | 0.297 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.290 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.515 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.463 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.443 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.476 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.434 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.417 |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.476 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.443 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.443 |


**Q33: What does the CSS view transitions module define?**
*(expects URL containing: `View_transitions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.635 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.635 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.612 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.713 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.693 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.636 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.713 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.693 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.636 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.515 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.503 | developer.mozilla.org/en-US/docs/Web/CSS | 0.482 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.670 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.630 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.621 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.672 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.642 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.612 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.670 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.630 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.621 |


**Q34: How can developers create animated transitions using the View Transition API?**
*(expects URL containing: `View_transitions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.580 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.580 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.542 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.564 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.490 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.486 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.564 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.490 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.486 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/JavaScript/Gu | 0.378 | developer.mozilla.org/en-US/docs/Web/JavaScript/Gu | 0.365 | developer.mozilla.org/en-US/docs/Web/JavaScript/Gu | 0.336 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.554 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.484 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.482 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.496 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.492 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.486 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.554 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.496 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.482 |


**Q35: What are the four commonly-used CSS math functions?**
*(expects URL containing: `Using_math_functions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.608 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.580 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.570 |
| crawl4ai | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.677 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.660 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.658 |
| crawl4ai-raw | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.677 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.660 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.658 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.461 | developer.mozilla.org/en-US/docs/Web/CSS | 0.457 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.440 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.689 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.662 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.624 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.642 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.593 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.563 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.714 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.702 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.689 |


**Q36: How does the `calc()` function work in CSS?**
*(expects URL containing: `Using_math_functions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.756 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.707 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.697 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.628 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.614 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.594 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.628 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.614 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.594 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.453 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.447 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.441 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.606 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.588 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.566 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.562 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.554 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.542 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.689 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.639 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.608 |


**Q37: What is the focus of web security?**
*(expects URL containing: `Security`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.302 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.298 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.286 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/Security | 0.540 | developer.mozilla.org/en-US/docs/Web/Security | 0.538 | developer.mozilla.org/en-US/docs/Web/Security | 0.526 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/Security | 0.541 | developer.mozilla.org/en-US/docs/Web/Security | 0.538 | developer.mozilla.org/en-US/docs/Web/Security | 0.526 |
| scrapy+md | #1 | developer.mozilla.org/en-US/docs/Web/Security/Atta | 0.428 | developer.mozilla.org/en-US/docs/Web/Security/Atta | 0.400 | developer.mozilla.org/en-US/docs/Web/Security/Atta | 0.393 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/Security | 0.531 | developer.mozilla.org/en-US/docs/Web/Security | 0.529 | developer.mozilla.org/en-US/docs/Web/Security | 0.520 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/Security | 0.582 | developer.mozilla.org/en-US/docs/Web/Security | 0.547 | developer.mozilla.org/en-US/docs/Web/Security | 0.531 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/Security | 0.531 | developer.mozilla.org/en-US/docs/Web/Security | 0.529 | developer.mozilla.org/en-US/docs/Web/Security | 0.520 |


**Q38: How do modern browsers protect users' security on the web?**
*(expects URL containing: `Security`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.372 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.355 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.346 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/Privacy | 0.638 | developer.mozilla.org/en-US/docs/Web/Security | 0.634 | developer.mozilla.org/en-US/docs/Web/Privacy | 0.621 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/Privacy | 0.638 | developer.mozilla.org/en-US/docs/Web/Security | 0.634 | developer.mozilla.org/en-US/docs/Web/Privacy | 0.621 |
| scrapy+md | #1 | developer.mozilla.org/en-US/docs/Web/Security/Atta | 0.454 | developer.mozilla.org/en-US/docs/Web/Security/Atta | 0.433 | developer.mozilla.org/en-US/docs/Web/Security/Atta | 0.426 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/Privacy | 0.649 | developer.mozilla.org/en-US/docs/Web/Security | 0.622 | developer.mozilla.org/en-US/docs/Web/Privacy | 0.620 |
| colly+md | #3 | developer.mozilla.org/en-US/docs/Web/Privacy | 0.649 | developer.mozilla.org/en-US/docs/Web/Privacy | 0.620 | developer.mozilla.org/en-US/docs/Web/Security | 0.601 |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/Privacy | 0.649 | developer.mozilla.org/en-US/docs/Web/Security | 0.622 | developer.mozilla.org/en-US/docs/Web/Privacy | 0.620 |


**Q39: What does the object-view-box property do?**
*(expects URL containing: `Using_object-view-box`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.431 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.431 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.429 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.516 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.509 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.484 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.516 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.509 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.484 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.396 | developer.mozilla.org/en-US/docs/Web/JavaScript/Gu | 0.373 | developer.mozilla.org/en-US/docs/Web/JavaScript/Gu | 0.358 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.527 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.510 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.501 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.541 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.527 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.523 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.527 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.523 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.501 |


**Q40: How does the object-view-box property differ from object-fit?**
*(expects URL containing: `Using_object-view-box`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.609 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.601 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.638 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.621 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.583 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.638 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.621 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.583 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.536 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.412 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.373 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.663 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.594 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.663 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.622 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.575 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.663 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.622 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.594 |


**Q41: What are the different textual data types in CSS?**
*(expects URL containing: `Textual_data_types`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.685 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.638 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.612 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.675 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.674 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.593 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.675 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.674 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.593 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.585 | developer.mozilla.org/en-US/docs/Web/CSS | 0.552 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.537 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.660 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.633 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.612 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.714 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.660 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.627 |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.660 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.642 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.612 |


**Q42: What do the CSS-wide keywords represent?**
*(expects URL containing: `Textual_data_types`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.620 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.571 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.569 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.616 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.583 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.558 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.616 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.583 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.558 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.510 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.504 | developer.mozilla.org/en-US/docs/Web/CSS | 0.488 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.622 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.582 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.557 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.593 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.587 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.582 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.557 |


**Q43: What does the CSS motion path module allow authors to do?**
*(expects URL containing: `Motion_path`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.584 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.536 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.502 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.654 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.513 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.512 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.654 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.513 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.512 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.465 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.449 | developer.mozilla.org/en-US/docs/Web/CSS | 0.449 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.508 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.507 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.693 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.577 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.511 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.629 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.508 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.507 |


**Q44: How can you animate an element along a defined path using CSS motion paths?**
*(expects URL containing: `Motion_path`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.583 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.581 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.561 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.685 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.572 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.495 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.685 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.572 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.495 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.376 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.356 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.353 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.661 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.558 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.502 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.678 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.663 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.549 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.668 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.558 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.549 |


**Q45: What properties can be used for visual styling of scrollbars?**
*(expects URL containing: `Scrollbars_styling`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.676 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.671 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.633 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.630 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.553 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.540 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.630 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.553 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.540 |
| scrapy+md | miss | developer.mozilla.org/ja/docs/Web/CSS/Reference/Pr | 0.462 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.442 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.438 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.629 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.553 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.544 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.645 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.551 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.636 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.625 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.551 |


**Q46: How can you customize the color of the scrollbar track and thumb?**
*(expects URL containing: `Scrollbars_styling`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.568 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.552 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.547 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.625 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.406 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.405 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.625 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.406 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.405 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.442 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.412 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.410 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.592 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.422 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.400 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.648 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.603 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.445 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.596 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.530 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.442 |


**Q47: What can the border-radius generator tool be used for?**
*(expects URL containing: `Border-radius_generator`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.736 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.619 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.557 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.717 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.611 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.578 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.717 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.611 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.578 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS | 0.443 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.396 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.388 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.670 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.610 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.587 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.553 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.547 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.539 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.670 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.610 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.610 |


**Q48: How does the border-radius generator help in generating CSS effects?**
*(expects URL containing: `Border-radius_generator`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.746 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.622 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.615 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.693 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.608 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.597 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.693 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.608 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.597 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS | 0.515 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.413 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.407 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.663 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.604 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.596 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.600 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.587 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.583 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.663 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.620 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.613 |


**Q49: What does the CSS round display module define?**
*(expects URL containing: `Round_display`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ro | 0.715 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.627 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.572 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ro | 0.619 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.567 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.559 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ro | 0.619 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.567 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.559 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.565 | developer.mozilla.org/en-US/docs/Web/CSS | 0.488 | developer.mozilla.org/en-US/docs/Web/CSS | 0.482 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ro | 0.601 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.572 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.569 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ro | 0.635 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.572 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.569 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ro | 0.601 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.572 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.569 |


**Q50: Which properties are introduced in the CSS round display module?**
*(expects URL containing: `Round_display`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ro | 0.727 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.641 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.640 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ro | 0.644 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.629 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.614 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ro | 0.644 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.629 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.614 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.637 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.566 | developer.mozilla.org/en-US/docs/Web/CSS | 0.523 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.641 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ro | 0.623 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.606 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ro | 0.693 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.641 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.640 |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.641 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ro | 0.623 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.606 |


**Q51: What is the purpose of the CSS ruby layout module?**
*(expects URL containing: `Ruby_layout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.609 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.585 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.572 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ru | 0.674 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.604 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.575 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ru | 0.674 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.604 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.575 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS | 0.550 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.530 | developer.mozilla.org/en-US/docs/Web/CSS | 0.504 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ru | 0.639 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.609 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.558 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.609 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ru | 0.585 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Po | 0.575 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ru | 0.639 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.609 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.558 |


**Q52: Which properties are introduced by the CSS ruby layout module?**
*(expects URL containing: `Ruby_layout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.674 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.601 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.593 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ru | 0.694 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.641 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ru | 0.630 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ru | 0.694 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.641 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ru | 0.630 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.590 | developer.mozilla.org/en-US/docs/Web/CSS | 0.556 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.545 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.674 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ru | 0.659 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.598 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.674 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Po | 0.641 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ru | 0.608 |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.674 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ru | 0.659 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.598 |


**Q53: What is the HTML DOM API made up of?**
*(expects URL containing: `HTML_DOM_API`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.465 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.448 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.438 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.686 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.669 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.621 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.686 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.669 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.621 |
| scrapy+md | miss | developer.mozilla.org/ja/docs/Web/JavaScript/Refer | 0.584 | developer.mozilla.org/en-US/docs/Web/API/XMLHttpRe | 0.480 | developer.mozilla.org/en-US/docs/Web/XML/XSLT/Guid | 0.435 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.681 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.632 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.631 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/API/HTML/DOM/ | 0.681 | developer.mozilla.org/en-US/docs/Web/API/HTML/DOM/ | 0.647 | developer.mozilla.org/en-US/docs/Web/API/HTML/DOM/ | 0.632 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.681 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.632 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.631 |


**Q54: What functionality does the HTMLElement interface provide?**
*(expects URL containing: `HTML_DOM_API`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.420 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.415 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.414 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.628 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.592 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.584 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.628 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.592 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.584 |
| scrapy+md | miss | developer.mozilla.org/ja/docs/Web/JavaScript/Refer | 0.466 | developer.mozilla.org/en-US/docs/Web/API/XMLHttpRe | 0.438 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.413 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.603 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.589 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.588 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/API/HTML/DOM/ | 0.603 | developer.mozilla.org/en-US/docs/Web/API/HTML/DOM/ | 0.589 | developer.mozilla.org/en-US/docs/Web/API/HTML/DOM/ | 0.588 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.603 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.589 | developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_ | 0.588 |


**Q55: How are grid lines numbered in CSS grid layout?**
*(expects URL containing: `Line-based_placement`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.618 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.614 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.633 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.620 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.619 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.633 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.620 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.619 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS | 0.411 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.408 | developer.mozilla.org/en-US/docs/Web/CSS | 0.402 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.642 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.615 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.606 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.628 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.617 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.612 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.628 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.617 |


**Q56: What properties are used for positioning items by line number in a grid?**
*(expects URL containing: `Line-based_placement`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.663 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.596 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.566 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.682 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.620 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.613 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.682 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.620 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.613 |
| scrapy+md | miss | developer.mozilla.org/ja/docs/Web/SVG/Reference/At | 0.381 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.372 | developer.mozilla.org/de/docs/Web/SVG/Reference/At | 0.362 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.670 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.615 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.606 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.668 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.616 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.608 |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.668 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.616 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.596 |


**Q57: What does the CSS transforms module define?**
*(expects URL containing: `Transforms`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.616 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.616 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.609 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.648 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.629 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.609 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.647 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.629 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.609 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS | 0.499 | developer.mozilla.org/en-US/docs/Web/CSS | 0.498 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.498 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.646 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.625 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.612 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.634 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.609 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.603 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.616 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.609 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.594 |


**Q58: How can the perspective property affect the view of a 3D transformed element?**
*(expects URL containing: `Transforms`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.626 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.592 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.555 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.653 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.563 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.509 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.653 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.563 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.509 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.350 | developer.mozilla.org/en-US/docs/Web/JavaScript/Gu | 0.336 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.332 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.558 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.518 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.627 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.582 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.537 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.581 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.537 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.507 |


**Q59: What is CSS masking?**
*(expects URL containing: `Introduction`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.750 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.733 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.625 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.668 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.640 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.622 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.668 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.640 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.622 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/Security/Atta | 0.456 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.442 | developer.mozilla.org/en-US/docs/Web/CSS | 0.419 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.639 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.637 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.617 |
| colly+md | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.668 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.654 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.650 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.639 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.637 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.618 |


**Q60: How do alpha masks work in CSS?**
*(expects URL containing: `Introduction`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.658 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.643 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.639 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.666 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.618 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.610 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.666 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.618 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.610 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.433 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.402 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.401 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.652 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.609 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.607 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.644 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.626 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.624 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.652 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.644 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ma | 0.626 |


</details>

## newegg

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai | 64% (37/58) | 78% (45/58) | 81% (47/58) | 91% (53/58) | 98% (57/58) | 0.729 | 5857 | 200 |
| crawl4ai-raw | 64% (37/58) | 78% (45/58) | 81% (47/58) | 90% (52/58) | 98% (57/58) | 0.729 | 5856 | 200 |
| colly+md | 9% (5/58) | 12% (7/58) | 16% (9/58) | 24% (14/58) | 24% (14/58) | 0.122 | 6574 | 165 |
| playwright | 2% (1/58) | 3% (2/58) | 3% (2/58) | 3% (2/58) | 16% (9/58) | 0.043 | 1195 | 200 |
| markcrawl | — | — | — | — | — | — | — | — |
| scrapy+md | — | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — | — |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for newegg</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What brands are available in the DIY Cooling category?**
*(expects URL containing: `ID-3635`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/Fans-PC-Cooling/Category/ID-11 | 0.584 | www.newegg.com/DIY-Cooling/SubCategory/ID-3635 | 0.567 | www.newegg.com/DIY-Cooling/SubCategory/ID-3635 | 0.552 |
| crawl4ai-raw | #2 | www.newegg.com/Fans-PC-Cooling/Category/ID-11 | 0.582 | www.newegg.com/DIY-Cooling/SubCategory/ID-3635 | 0.568 | www.newegg.com/DIY-Cooling/SubCategory/ID-3635 | 0.552 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/p/pl?N=4803%204801 | 0.455 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.442 | www.newegg.com/p/pl?N=4803%204801 | 0.430 |
| playwright | miss | www.newegg.com/ | 0.430 | www.newegg.com/ | 0.408 | www.newegg.com/ | 0.405 |


**Q2: What types of products can I find under DIY Cooling?**
*(expects URL containing: `ID-3635`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/DIY-Cooling/SubCategory/ID-3635 | 0.592 | www.newegg.com/DIY-Cooling/SubCategory/ID-3635 | 0.574 | www.newegg.com/DIY-Cooling/SubCategory/ID-3635 | 0.550 |
| crawl4ai-raw | #1 | www.newegg.com/DIY-Cooling/SubCategory/ID-3635 | 0.592 | www.newegg.com/DIY-Cooling/SubCategory/ID-3635 | 0.575 | www.newegg.com/DIY-Cooling/SubCategory/ID-3635 | 0.550 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/tools/custom-pc-builder?cm/sp=Head/ | 0.448 | www.newegg.com/p/pl?N=4803%204801 | 0.428 | www.newegg.com/p/pl?N=4803%204801 | 0.418 |
| playwright | miss | www.newegg.com/insider/how-to-choose-the-best-desk | 0.434 | www.newegg.com/ | 0.433 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.424 |


**Q3: What brands of USB / IEEE-1394 Firewire Adapters are available?**
*(expects URL containing: `ID-3025`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.642 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.607 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.585 |
| crawl4ai-raw | #1 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.642 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.607 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.585 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.397 | www.newegg.com/category | 0.380 | www.newegg.com/ASUS/BrandStore/ID-1315 | 0.360 |
| playwright | #21 | www.newegg.com/ | 0.343 | www.newegg.com/ | 0.335 | www.newegg.com/ | 0.316 |


**Q4: What is the price range for USB / IEEE-1394 Firewire Adapters on Newegg?**
*(expects URL containing: `ID-3025`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.644 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.623 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.600 |
| crawl4ai-raw | #1 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.644 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.623 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.600 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.423 | www.newegg.com/Email-Deals/EventSaleStore/ID-10382 | 0.422 | www.newegg.com/category | 0.419 |
| playwright | #2 | www.newegg.com/promotions/nepro/18-1881/index.html | 0.379 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.376 | www.newegg.com/Thunderbolt-Cables-Adapters/SubCate | 0.358 |


**Q5: What types of desktop computers are available on Newegg?**
*(expects URL containing: `ID-228`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #6 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.689 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.664 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.646 |
| crawl4ai-raw | #6 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.689 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.664 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.646 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Computer-Systems/Store/ID-3 | 0.621 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.604 | www.newegg.com/p/pl?N=4889 | 0.583 |
| playwright | #47 | www.newegg.com/ | 0.573 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.538 | www.newegg.com/ | 0.536 |


**Q6: What brands of desktop computers can I find on Newegg?**
*(expects URL containing: `ID-228`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #9 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.683 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.665 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.632 |
| crawl4ai-raw | #11 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.683 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.665 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.632 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/p/pl?N=4889 | 0.596 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.594 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.592 |
| playwright | #34 | www.newegg.com/ | 0.578 | www.newegg.com/ | 0.541 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.509 |


**Q7: What types of fan controllers are available in the Controller Panels category?**
*(expects URL containing: `ID-11`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.602 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.598 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.573 |
| crawl4ai-raw | #1 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.602 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.598 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.573 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.376 | www.newegg.com/d/Best-Sellers/Computer-Case/c/ID-9 | 0.372 | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.369 |
| playwright | miss | www.newegg.com/ | 0.418 | www.newegg.com/ | 0.352 | www.newegg.com/ | 0.346 |


**Q8: Which brands are featured in the Controller Panels section?**
*(expects URL containing: `ID-11`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.578 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.538 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.535 |
| crawl4ai-raw | #1 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.578 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.538 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.535 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.496 | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.455 | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.454 |
| playwright | miss | www.newegg.com/ | 0.427 | www.newegg.com/ | 0.398 | www.newegg.com/ | 0.395 |


**Q9: What brands of barebone PCs are available on Newegg?**
*(expects URL containing: `ID-3`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Barebone-PCs/SubCategory/ID-3 | 0.697 | www.newegg.com/Mini-PC-Barebone/SubCategory/ID-309 | 0.666 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.661 |
| crawl4ai-raw | #1 | www.newegg.com/Barebone-PCs/SubCategory/ID-3 | 0.697 | www.newegg.com/Mini-PC-Barebone/SubCategory/ID-309 | 0.666 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.661 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #9 | www.newegg.com/p/pl?d=NPU&mid1=PageSEO | 0.568 | www.newegg.com/p/pl?N=4889 | 0.564 | www.newegg.com/p/pl?d=AI+NPU&mid1=PageSEO | 0.554 |
| playwright | #11 | www.newegg.com/ | 0.546 | www.newegg.com/server-system-configurator/ | 0.544 | www.newegg.com/ | 0.491 |


**Q10: What is the maximum RAM support for the Shuttle XPC slim DH610 Barebone System?**
*(expects URL containing: `ID-3`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #4 | www.newegg.com/System-Specific-Memory/SubCategory/ | 0.541 | www.newegg.com/AMD-Motherboards/SubCategory/ID-22 | 0.529 | www.newegg.com/System-Specific-Memory/SubCategory/ | 0.521 |
| crawl4ai-raw | #4 | www.newegg.com/System-Specific-Memory/SubCategory/ | 0.541 | www.newegg.com/AMD-Motherboards/SubCategory/ID-22 | 0.529 | www.newegg.com/System-Specific-Memory/SubCategory/ | 0.521 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #7 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.488 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.482 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.478 |
| playwright | #13 | www.newegg.com/ | 0.460 | www.newegg.com/ | 0.432 | www.newegg.com/ | 0.427 |


**Q11: What are the types of products available in the Barebone / Mini Computers category?**
*(expects URL containing: `ID-3`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.743 | www.newegg.com/Mini-PC-Barebone/SubCategory/ID-309 | 0.731 | www.newegg.com/Mini-PC-Barebone/SubCategory/ID-309 | 0.707 |
| crawl4ai-raw | #1 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.743 | www.newegg.com/Mini-PC-Barebone/SubCategory/ID-309 | 0.731 | www.newegg.com/Mini-PC-Barebone/SubCategory/ID-309 | 0.707 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #10 | www.newegg.com/p/pl?d=NPU&mid1=PageSEO | 0.555 | www.newegg.com/p/pl?d=NPU&mid1=PageSEO | 0.545 | www.newegg.com/p/pl?d=NPU&mid1=PageSEO | 0.542 |
| playwright | #29 | www.newegg.com/ | 0.533 | www.newegg.com/ | 0.527 | www.newegg.com/server-system-configurator/ | 0.527 |


**Q12: What is the price of the ASUS NUC 16 Pro Mini Gaming PC?**
*(expects URL containing: `ID-3`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.682 | www.newegg.com/Chromebox-Desktop-Mini-PC/Store/ID- | 0.644 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.640 |
| crawl4ai-raw | #1 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.682 | www.newegg.com/Chromebox-Desktop-Mini-PC/Store/ID- | 0.644 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.640 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #34 | www.newegg.com/p/pl?N=4889 | 0.649 | www.newegg.com/p/pl?d=NPU&mid1=PageSEO | 0.645 | www.newegg.com/ASUS/BrandStore/ID-1315 | 0.642 |
| playwright | #31 | www.newegg.com/asus-nuc-configurator?cm_sp=hamburg | 0.634 | www.newegg.com/asus-nuc-configurator?cm_sp=hamburg | 0.628 | www.newegg.com/asus-nuc-configurator?cm_sp=hamburg | 0.602 |


**Q13: What types of memory are available on the Newegg Deals page?**
*(expects URL containing: `ID-9447`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.663 | www.newegg.com/Memory/Category/ID-17 | 0.649 | www.newegg.com/Laptop-Memory/SubCategory/ID-381 | 0.642 |
| crawl4ai-raw | #1 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.663 | www.newegg.com/Memory/Category/ID-17 | 0.649 | www.newegg.com/Laptop-Memory/SubCategory/ID-381 | 0.642 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #2 | www.newegg.com/DEALCEMBER-After-Christmas-Sale/Eve | 0.596 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.596 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.593 |
| playwright | #27 | www.newegg.com/ | 0.577 | www.newegg.com/ | 0.561 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.536 |


**Q14: Which brands of desktop memory can be found in the Newegg Deals section?**
*(expects URL containing: `ID-9447`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #11 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.712 | www.newegg.com/Memory/Category/ID-17 | 0.709 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.708 |
| crawl4ai-raw | #11 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.712 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.708 | www.newegg.com/System-Specific-Memory/SubCategory/ | 0.693 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #5 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.641 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.628 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.622 |
| playwright | #15 | www.newegg.com/ | 0.562 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.555 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.553 |


**Q15: What types of audio/video splitters are available?**
*(expects URL containing: `ID-3050`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.671 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.572 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.571 |
| crawl4ai-raw | #1 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.671 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.572 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.571 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/category | 0.344 | www.newegg.com/p/pl?N=100006740%2050001186&mid1=Pa | 0.332 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.321 |
| playwright | miss | www.newegg.com/ | 0.322 | www.newegg.com/ | 0.314 | www.newegg.com/ | 0.312 |


**Q16: Which brands are featured for audio/video splitters?**
*(expects URL containing: `ID-3050`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.688 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.629 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.618 |
| crawl4ai-raw | #1 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.688 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.629 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.618 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.451 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.436 | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.427 |
| playwright | #50 | www.newegg.com/ | 0.371 | www.newegg.com/ | 0.363 | www.newegg.com/ | 0.359 |


**Q17: What brands are available for computer accessories?**
*(expects URL containing: `pl`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/Computer-Accessories/Category/ID-1 | 0.588 | www.newegg.com/p/pl?N=100006640+4016 | 0.585 | www.newegg.com/Computer-Accessories/Category/ID-1 | 0.580 |
| crawl4ai-raw | #2 | www.newegg.com/Computer-Accessories/Category/ID-1 | 0.588 | www.newegg.com/p/pl?N=100006640+4016 | 0.585 | www.newegg.com/Computer-Accessories/Category/ID-1 | 0.580 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #8 | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.566 | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.552 | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.552 |
| playwright | miss | www.newegg.com/ | 0.540 | www.newegg.com/ | 0.518 | www.newegg.com/ | 0.508 |


**Q18: What is the model number of the refurbished ASUS ROG Ryujin III 240mm ARGB liquid CPU cooler?**
*(expects URL containing: `pl`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/p/pl?N=100006640+4016 | 0.692 | www.newegg.com/Water-Liquid-Cooling/SubCategory/ID | 0.547 | www.newegg.com/CPU-Fans-Heatsinks/SubCategory/ID-5 | 0.539 |
| crawl4ai-raw | #1 | www.newegg.com/p/pl?N=100006640+4016 | 0.692 | www.newegg.com/Water-Liquid-Cooling/SubCategory/ID | 0.547 | www.newegg.com/CPU-Air-Coolers/SubCategory/ID-574 | 0.539 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #40 | www.newegg.com/ASUS/BrandStore/ID-1315 | 0.637 | www.newegg.com/MSI/BrandStore/ID-1312 | 0.554 | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.553 |
| playwright | #44 | www.newegg.com/ | 0.500 | www.newegg.com/ | 0.485 | www.newegg.com/ | 0.476 |


**Q19: What brands of audio adapters are available on Newegg?**
*(expects URL containing: `ID-3020`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.670 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.628 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.628 |
| crawl4ai-raw | #1 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.670 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.628 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.628 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.471 | www.newegg.com/p/pl?d=NPU&mid1=PageSEO | 0.461 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.459 |
| playwright | miss | www.newegg.com/ | 0.445 | www.newegg.com/ | 0.421 | www.newegg.com/ | 0.413 |


**Q20: What is the price range for audio adapters on Newegg?**
*(expects URL containing: `ID-3020`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.629 | www.newegg.com/Audio-Video-Converters/SubCategory/ | 0.579 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.575 |
| crawl4ai-raw | #1 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.629 | www.newegg.com/Audio-Video-Converters/SubCategory/ | 0.579 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.575 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.454 | www.newegg.com/d/Best-Sellers/Electronics/t/ID-10 | 0.450 | www.newegg.com/Acer-America/BrandStore/ID-1146 | 0.446 |
| playwright | #18 | www.newegg.com/promotions/nepro/18-1881/index.html | 0.395 | www.newegg.com/ | 0.391 | www.newegg.com/ | 0.384 |


**Q21: What brands are available for data adapters?**
*(expects URL containing: `ID-3021`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/Other-Adapters-Gender-Changers/SubC | 0.533 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.527 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.525 |
| crawl4ai-raw | #2 | www.newegg.com/Other-Adapters-Gender-Changers/SubC | 0.533 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.527 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.524 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.475 | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.423 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.407 |
| playwright | miss | www.newegg.com/ | 0.378 | www.newegg.com/ | 0.363 | www.newegg.com/ | 0.357 |


**Q22: What is the price range for data adapters on Newegg?**
*(expects URL containing: `ID-3021`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.621 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.575 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.570 |
| crawl4ai-raw | #1 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.621 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.576 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.570 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.474 | www.newegg.com/Acer-America/BrandStore/ID-1146 | 0.473 | www.newegg.com/Email-Deals/EventSaleStore/ID-10382 | 0.468 |
| playwright | miss | www.newegg.com/promotions/nepro/18-1881/index.html | 0.425 | www.newegg.com/ | 0.418 | www.newegg.com/ | 0.410 |


**Q23: What brands of power supplies are available on Newegg?**
*(expects URL containing: `ID-58`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Power-Supplies/SubCategory/ID-58 | 0.655 | www.newegg.com/Power-Supplies/SubCategory/ID-58 | 0.647 | www.newegg.com/Power-Supply/Category/ID-32 | 0.637 |
| crawl4ai-raw | #1 | www.newegg.com/Power-Supplies/SubCategory/ID-58 | 0.655 | www.newegg.com/Power-Supplies/SubCategory/ID-58 | 0.647 | www.newegg.com/Power-Supply/Category/ID-32 | 0.637 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.595 | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.577 | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.575 |
| playwright | miss | www.newegg.com/ | 0.515 | www.newegg.com/ | 0.502 | www.newegg.com/ | 0.501 |


**Q24: What types of power supply connectors are listed on the page?**
*(expects URL containing: `ID-58`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Power-Supplies/SubCategory/ID-58 | 0.579 | www.newegg.com/Power-Supplies/SubCategory/ID-58 | 0.569 | www.newegg.com/Power-Supply/Category/ID-32 | 0.569 |
| crawl4ai-raw | #1 | www.newegg.com/Power-Supplies/SubCategory/ID-58 | 0.579 | www.newegg.com/Power-Supplies/SubCategory/ID-58 | 0.569 | www.newegg.com/Power-Supply/Category/ID-32 | 0.568 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.491 | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.484 | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.475 |
| playwright | miss | www.newegg.com/ | 0.415 | www.newegg.com/ | 0.387 | www.newegg.com/ | 0.381 |


**Q25: What brands of duplicators are available on this page?**
*(expects URL containing: `ID-528`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.677 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.662 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.648 |
| crawl4ai-raw | #1 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.677 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.662 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.648 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.459 | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.450 | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.450 |
| playwright | #47 | www.newegg.com/ | 0.379 | www.newegg.com/ | 0.374 | www.newegg.com/ | 0.373 |


**Q26: What types of duplicators can I find listed on this page?**
*(expects URL containing: `ID-528`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.671 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.651 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.637 |
| crawl4ai-raw | #1 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.671 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.651 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.637 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Product/PowerSearch?SubCategory=3 | 0.410 | www.newegg.com/category | 0.399 | www.newegg.com/category | 0.388 |
| playwright | #33 | www.newegg.com/ | 0.354 | www.newegg.com/ | 0.352 | www.newegg.com/ | 0.347 |


**Q27: What brands are available for server and workstation systems?**
*(expects URL containing: `ID-386`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Server-Workstation-System/SubCatego | 0.647 | www.newegg.com/Server-Workstation-System/SubCatego | 0.643 | www.newegg.com/Server-Components/Category/ID-449 | 0.637 |
| crawl4ai-raw | #1 | www.newegg.com/Server-Workstation-System/SubCatego | 0.647 | www.newegg.com/Server-Workstation-System/SubCatego | 0.643 | www.newegg.com/Server-Components/Category/ID-449 | 0.637 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Computer-Systems/Store/ID-3 | 0.555 | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.536 | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.535 |
| playwright | #49 | www.newegg.com/server-system-configurator/ | 0.587 | www.newegg.com/server-system-configurator/ | 0.528 | www.newegg.com/ | 0.488 |


**Q28: What types of server and workstation systems are listed?**
*(expects URL containing: `ID-386`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Server-Workstation-System/SubCatego | 0.630 | www.newegg.com/Server-Workstation-System/SubCatego | 0.619 | www.newegg.com/Server-Workstation-System/SubCatego | 0.597 |
| crawl4ai-raw | #1 | www.newegg.com/Server-Workstation-System/SubCatego | 0.630 | www.newegg.com/Server-Workstation-System/SubCatego | 0.619 | www.newegg.com/Server-Workstation-System/SubCatego | 0.597 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Computer-Systems/Store/ID-3 | 0.551 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.533 | www.newegg.com/Business-Laptops/SubCategory/ID-341 | 0.515 |
| playwright | miss | www.newegg.com/server-system-configurator/ | 0.537 | www.newegg.com/server-system-configurator/ | 0.512 | www.newegg.com/ | 0.453 |


**Q29: What brands of power extension cords are available on Newegg?**
*(expects URL containing: `ID-2829`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Power-Extension-Cords/SubCategory/I | 0.696 | www.newegg.com/Computer-Power-Extension-Cords/SubC | 0.688 | www.newegg.com/Power-Extension-Cords/SubCategory/I | 0.681 |
| crawl4ai-raw | #1 | www.newegg.com/Power-Extension-Cords/SubCategory/I | 0.696 | www.newegg.com/Computer-Power-Extension-Cords/SubC | 0.688 | www.newegg.com/Power-Extension-Cords/SubCategory/I | 0.681 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/Server-Components/t/ | 0.520 | www.newegg.com/d/Best-Sellers/Server-Components/t/ | 0.491 | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.484 |
| playwright | #49 | www.newegg.com/ | 0.460 | www.newegg.com/ | 0.440 | www.newegg.com/ | 0.421 |


**Q30: What types of power extension cords can I find on Newegg?**
*(expects URL containing: `ID-2829`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/Computer-Power-Extension-Cords/SubC | 0.701 | www.newegg.com/Power-Extension-Cords/SubCategory/I | 0.695 | www.newegg.com/Power-Extension-Cords/SubCategory/I | 0.684 |
| crawl4ai-raw | #2 | www.newegg.com/Computer-Power-Extension-Cords/SubC | 0.701 | www.newegg.com/Power-Extension-Cords/SubCategory/I | 0.695 | www.newegg.com/Power-Extension-Cords/SubCategory/I | 0.684 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/Server-Components/t/ | 0.514 | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.493 | www.newegg.com/d/Best-Sellers/Server-Components/t/ | 0.487 |
| playwright | miss | www.newegg.com/ | 0.456 | www.newegg.com/ | 0.438 | www.newegg.com/ | 0.411 |


**Q31: What brands of power distribution units are available?**
*(expects URL containing: `ID-1042`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.640 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.637 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.591 |
| crawl4ai-raw | #1 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.640 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.637 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.591 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.458 | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.442 | www.newegg.com/d/Best-Sellers/Server-Components/t/ | 0.425 |
| playwright | miss | www.newegg.com/ | 0.386 | www.newegg.com/ | 0.369 | www.newegg.com/ | 0.363 |


**Q32: What is the input voltage for the CyberPower PDU15B10R?**
*(expects URL containing: `ID-1042`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.564 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.554 | www.newegg.com/Battery-Backup-UPS/SubCategory/ID-7 | 0.541 |
| crawl4ai-raw | #1 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.565 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.553 | www.newegg.com/Battery-Backup-UPS/SubCategory/ID-7 | 0.541 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/Server-Components/t/ | 0.499 | www.newegg.com/d/Best-Sellers/Server-Components/t/ | 0.445 | www.newegg.com/d/Best-Sellers/Computer-Peripherals | 0.445 |
| playwright | #34 | www.newegg.com/ | 0.391 | www.newegg.com/ | 0.325 | www.newegg.com/server-system-configurator/ | 0.321 |


**Q33: What brands of hard drive adapters are available on Newegg?**
*(expects URL containing: `ID-3022`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Hard-Drive-Adapters/SubCategory/ID- | 0.657 | www.newegg.com/Hard-Drive-Adapters/SubCategory/ID- | 0.630 | www.newegg.com/HDD-SSD-Accessories/SubCategory/ID- | 0.630 |
| crawl4ai-raw | #1 | www.newegg.com/Hard-Drive-Adapters/SubCategory/ID- | 0.656 | www.newegg.com/HDD-SSD-Accessories/SubCategory/ID- | 0.630 | www.newegg.com/Hard-Drive-Adapters/SubCategory/ID- | 0.629 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.489 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.486 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.482 |
| playwright | #44 | www.newegg.com/ | 0.443 | www.newegg.com/ | 0.435 | www.newegg.com/ | 0.425 |


**Q34: What is the price range for hard drive adapters on Newegg?**
*(expects URL containing: `ID-3022`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Hard-Drive-Adapters/SubCategory/ID- | 0.629 | www.newegg.com/Other-Adapters-Gender-Changers/SubC | 0.607 | www.newegg.com/Hard-Drive-Adapters/SubCategory/ID- | 0.603 |
| crawl4ai-raw | #1 | www.newegg.com/Hard-Drive-Adapters/SubCategory/ID- | 0.629 | www.newegg.com/Other-Adapters-Gender-Changers/SubC | 0.607 | www.newegg.com/Hard-Drive-Adapters/SubCategory/ID- | 0.602 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.487 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.481 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.481 |
| playwright | #18 | www.newegg.com/ | 0.434 | www.newegg.com/ | 0.430 | www.newegg.com/promotions/nepro/18-1881/index.html | 0.408 |


**Q35: What brands of crypto mining equipment are available on Newegg?**
*(expects URL containing: `ID-3924`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.680 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.604 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.589 |
| crawl4ai-raw | #1 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.680 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.604 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.589 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/p/pl?d=NPU&mid1=PageSEO | 0.510 | www.newegg.com/d/Best-Sellers/CPU-Processor/c/ID-3 | 0.501 | www.newegg.com/d/Best-Sellers/Server-Components/t/ | 0.500 |
| playwright | #26 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.505 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.502 | www.newegg.com/ | 0.500 |


**Q36: What is the hashrate of the Stellapex Bitcoin Solo Miner NerdMiner V2?**
*(expects URL containing: `ID-3924`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.549 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.547 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.527 |
| crawl4ai-raw | #1 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.549 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.547 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.527 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/CPU-Processor/c/ID-3 | 0.342 | www.newegg.com/p/pl?d=CPU&mid1=PageSEO | 0.342 | www.newegg.com/p/pl?d=AI+NPU&mid1=PageSEO | 0.342 |
| playwright | #1 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.358 | www.newegg.com/Power-Inverters/SubCategory/ID-536 | 0.348 | www.newegg.com/insider/how-to-choose-a-pc-power-su | 0.347 |


**Q37: What brands are available for external CD/DVD/Blu-Ray drives?**
*(expects URL containing: `ID-420`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #9 | www.newegg.com/CD-DVD-Drives/SubCategory/ID-55 | 0.670 | www.newegg.com/Blu-Ray-Drives/SubCategory/ID-598 | 0.649 | www.newegg.com/CD-DVD-Blu-Ray-Burners-Media/Catego | 0.645 |
| crawl4ai-raw | #9 | www.newegg.com/CD-DVD-Drives/SubCategory/ID-55 | 0.670 | www.newegg.com/Blu-Ray-Drives/SubCategory/ID-598 | 0.649 | www.newegg.com/CD-DVD-Blu-Ray-Burners-Media/Catego | 0.645 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.431 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.406 | www.newegg.com/d/Product/PowerSearch?SubCategory=3 | 0.405 |
| playwright | miss | www.newegg.com/ | 0.384 | www.newegg.com/ | 0.359 | www.newegg.com/ | 0.356 |


**Q38: What types of external drives can I find on this page?**
*(expects URL containing: `ID-420`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #37 | www.newegg.com/Portable-External-Hard-Drives/SubCa | 0.616 | www.newegg.com/Desktop-External-Hard-Drives/SubCat | 0.611 | www.newegg.com/Desktop-External-Hard-Drives/SubCat | 0.600 |
| crawl4ai-raw | #36 | www.newegg.com/Desktop-External-Hard-Drives/SubCat | 0.625 | www.newegg.com/Portable-External-Hard-Drives/SubCa | 0.617 | www.newegg.com/Desktop-External-Hard-Drives/SubCat | 0.600 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/category | 0.496 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.470 | www.newegg.com/DELL/BrandStore/ID-10772 | 0.468 |
| playwright | miss | www.newegg.com/ | 0.461 | www.newegg.com/ | 0.445 | www.newegg.com/ | 0.422 |


**Q39: What brands of sound cards are available on Newegg?**
*(expects URL containing: `ID-57`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Sound-Card/SubCategory/ID-57 | 0.686 | www.newegg.com/Sound-Card/Category/ID-36 | 0.663 | www.newegg.com/Sound-Card/Category/ID-36 | 0.643 |
| crawl4ai-raw | #1 | www.newegg.com/Sound-Card/SubCategory/ID-57 | 0.686 | www.newegg.com/Sound-Card/Category/ID-36 | 0.663 | www.newegg.com/Sound-Card/Category/ID-36 | 0.643 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.497 | www.newegg.com/p/pl?N=4889 | 0.488 | www.newegg.com/ | 0.472 |
| playwright | miss | www.newegg.com/ | 0.472 | www.newegg.com/promotions/nepro/18-1881/index.html | 0.442 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.440 |


**Q40: What is the SNR of the Creative Sound Blaster Audigy Fx V2?**
*(expects URL containing: `ID-57`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Sound-Card/SubCategory/ID-57 | 0.622 | www.newegg.com/Sound-Card/SubCategory/ID-57 | 0.524 | www.newegg.com/Sound-Card/SubCategory/ID-57 | 0.520 |
| crawl4ai-raw | #1 | www.newegg.com/Sound-Card/SubCategory/ID-57 | 0.622 | www.newegg.com/Sound-Card/SubCategory/ID-57 | 0.524 | www.newegg.com/Sound-Card/SubCategory/ID-57 | 0.520 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.391 | www.newegg.com/d/Best-Sellers/Components-Storage/t | 0.389 | www.newegg.com/Shell-Shocker/EventSaleStore/ID-103 | 0.389 |
| playwright | #17 | www.newegg.com/ | 0.349 | www.newegg.com/ | 0.313 | www.newegg.com/ | 0.305 |


**Q41: What types of RAM are available on Newegg?**
*(expects URL containing: `ID-17`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Memory/Category/ID-17 | 0.679 | www.newegg.com/System-Specific-Memory/SubCategory/ | 0.671 | www.newegg.com/Server-Memory/SubCategory/ID-541 | 0.629 |
| crawl4ai-raw | #1 | www.newegg.com/Memory/Category/ID-17 | 0.671 | www.newegg.com/System-Specific-Memory/SubCategory/ | 0.671 | www.newegg.com/Server-Memory/SubCategory/ID-541 | 0.629 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #1 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.599 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.574 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.568 |
| playwright | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.553 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.550 | www.newegg.com/ | 0.495 |


**Q42: What is the maximum capacity per module for DDR4 RAM?**
*(expects URL containing: `ID-17`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #3 | www.newegg.com/System-Specific-Memory/SubCategory/ | 0.671 | www.newegg.com/Server-Memory/SubCategory/ID-541 | 0.660 | www.newegg.com/Memory/Category/ID-17 | 0.656 |
| crawl4ai-raw | #3 | www.newegg.com/System-Specific-Memory/SubCategory/ | 0.671 | www.newegg.com/Server-Memory/SubCategory/ID-541 | 0.660 | www.newegg.com/Memory/Category/ID-17 | 0.656 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #1 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.519 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.515 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.512 |
| playwright | miss | www.newegg.com/ | 0.484 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.428 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.428 |


**Q43: What types of GPUs are available on this page?**
*(expects URL containing: `ID-9447`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #6 | www.newegg.com/Workstation-Graphics-Cards/SubCateg | 0.596 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.592 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.586 |
| crawl4ai-raw | #6 | www.newegg.com/Workstation-Graphics-Cards/SubCateg | 0.596 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.592 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.586 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.595 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.595 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.590 |
| playwright | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.485 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.485 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.421 |


**Q44: What is the maximum resolution supported by the graphics cards listed?**
*(expects URL containing: `ID-9447`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #13 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.556 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.542 | www.newegg.com/Workstation-Graphics-Cards/SubCateg | 0.523 |
| crawl4ai-raw | #13 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.556 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.542 | www.newegg.com/Workstation-Graphics-Cards/SubCateg | 0.523 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.542 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.542 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.517 |
| playwright | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.378 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.378 | www.newegg.com/ | 0.361 |


**Q45: What brands of gaming desktop PCs are available?**
*(expects URL containing: `ID-3742`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/Desktop-Computer/Category/ID-228 | 0.661 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.658 | www.newegg.com/Desktop-Computer/Category/ID-228 | 0.632 |
| crawl4ai-raw | #2 | www.newegg.com/Desktop-Computer/Category/ID-228 | 0.661 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.658 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.618 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #2 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.584 | www.newegg.com/d/Best-Sellers/Gaming-Desktop-PC/s/ | 0.582 | www.newegg.com/d/Best-Sellers/Gaming-Desktop-PC/s/ | 0.576 |
| playwright | miss | www.newegg.com/ | 0.493 | www.newegg.com/ | 0.476 | www.newegg.com/ | 0.463 |


**Q46: What types of cooling systems are offered for gaming desktop PCs?**
*(expects URL containing: `ID-3742`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #16 | www.newegg.com/DIY-Cooling/SubCategory/ID-3635 | 0.669 | www.newegg.com/VGA-Cooling/SubCategory/ID-576 | 0.636 | www.newegg.com/VGA-Cooling/SubCategory/ID-576 | 0.632 |
| crawl4ai-raw | #16 | www.newegg.com/DIY-Cooling/SubCategory/ID-3635 | 0.669 | www.newegg.com/VGA-Cooling/SubCategory/ID-576 | 0.636 | www.newegg.com/VGA-Cooling/SubCategory/ID-576 | 0.632 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #1 | www.newegg.com/d/Best-Sellers/Gaming-Desktop-PC/s/ | 0.552 | www.newegg.com/tools/custom-pc-builder?cm/sp=Head/ | 0.540 | www.newegg.com/tools/custom-pc-builder?cm/sp=Head/ | 0.537 |
| playwright | miss | www.newegg.com/insider/how-to-choose-the-best-desk | 0.521 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.447 | www.newegg.com/ | 0.440 |


**Q47: What types of gaming PC systems are available?**
*(expects URL containing: `ID-3`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.653 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.616 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.616 |
| crawl4ai-raw | #1 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.653 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.616 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.616 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #1 | www.newegg.com/d/Best-Sellers/Gaming-Desktop-PC/s/ | 0.589 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.585 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.549 |
| playwright | miss | www.newegg.com/ | 0.464 | www.newegg.com/ | 0.441 | www.newegg.com/ | 0.437 |


**Q48: What are the categories of desktop systems listed on the page?**
*(expects URL containing: `ID-3`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #4 | www.newegg.com/Desktop-Computer/Category/ID-228 | 0.536 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.532 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.527 |
| crawl4ai-raw | #4 | www.newegg.com/Desktop-Computer/Category/ID-228 | 0.536 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.532 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.527 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #1 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.564 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.553 | www.newegg.com/d/Best-Sellers/Gaming-Desktop-PC/s/ | 0.529 |
| playwright | miss | www.newegg.com/insider/how-to-choose-the-best-desk | 0.506 | www.newegg.com/ | 0.494 | www.newegg.com/ | 0.486 |


**Q49: What brands are available for memory and chipset cooling?**
*(expects URL containing: `ID-572`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.664 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.658 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.637 |
| crawl4ai-raw | #1 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.664 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.658 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.637 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.506 | www.newegg.com/d/Best-Sellers/Components-Storage/t | 0.505 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.495 |
| playwright | #20 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.459 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.452 | www.newegg.com/ | 0.448 |


**Q50: What types of products are included in the memory and chipset cooling category?**
*(expects URL containing: `ID-572`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.669 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.665 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.612 |
| crawl4ai-raw | #1 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.669 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.665 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.612 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/category | 0.526 | www.newegg.com/d/Best-Sellers/Components-Storage/t | 0.500 | www.newegg.com/tools/custom-pc-builder/showcase/fe | 0.483 |
| playwright | #33 | www.newegg.com/ | 0.493 | www.newegg.com/ | 0.484 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.483 |


**Q51: What types of SSD form factors are available?**
*(expects URL containing: `ID-9447`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #8 | www.newegg.com/SSD/Category/ID-119 | 0.609 | www.newegg.com/SSD/Category/ID-119 | 0.604 | www.newegg.com/Internal-SSDs/SubCategory/ID-636 | 0.599 |
| crawl4ai-raw | #8 | www.newegg.com/SSD/Category/ID-119 | 0.609 | www.newegg.com/SSD/Category/ID-119 | 0.604 | www.newegg.com/Internal-SSDs/SubCategory/ID-636 | 0.599 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #8 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.465 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.461 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.457 |
| playwright | miss | www.newegg.com/server-system-configurator/ | 0.378 | www.newegg.com/ | 0.377 | www.newegg.com/ | 0.368 |


**Q52: Which brands of SSDs are featured on this page?**
*(expects URL containing: `ID-9447`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #16 | www.newegg.com/SSD/Category/ID-119 | 0.691 | www.newegg.com/SSD/Category/ID-119 | 0.664 | www.newegg.com/Enterprise-SSDs/SubCategory/ID-2021 | 0.657 |
| crawl4ai-raw | #16 | www.newegg.com/SSD/Category/ID-119 | 0.691 | www.newegg.com/SSD/Category/ID-119 | 0.664 | www.newegg.com/Enterprise-SSDs/SubCategory/ID-2021 | 0.657 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #5 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.627 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.620 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.616 |
| playwright | miss | www.newegg.com/ | 0.510 | www.newegg.com/ | 0.506 | www.newegg.com/ | 0.457 |


**Q53: What types of DVI cables are available?**
*(expects URL containing: `ID-2814`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.676 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.658 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.656 |
| crawl4ai-raw | #1 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.677 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.658 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.656 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/DELL/BrandStore/ID-10772 | 0.394 | www.newegg.com/Laptop-Notebook/Category/ID-223 | 0.385 | www.newegg.com/p/pl?N=100006740%2050001186&mid1=Pa | 0.363 |
| playwright | miss | www.newegg.com/ | 0.311 | www.newegg.com/ | 0.268 | www.newegg.com/ | 0.266 |


**Q54: Which brands offer DVI cables on this page?**
*(expects URL containing: `ID-2814`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.655 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.648 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.641 |
| crawl4ai-raw | #1 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.654 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.648 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.641 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/DELL/BrandStore/ID-10772 | 0.458 | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.450 | www.newegg.com/Laptop-Notebook/Category/ID-223 | 0.440 |
| playwright | miss | www.newegg.com/ | 0.417 | www.newegg.com/ | 0.385 | www.newegg.com/ | 0.376 |


**Q55: What brands of enterprise SSDs are available on Newegg?**
*(expects URL containing: `ID-2021`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Enterprise-SSDs/SubCategory/ID-2021 | 0.657 | www.newegg.com/Enterprise-SSDs/SubCategory/ID-2021 | 0.657 | www.newegg.com/External-SSDs/SubCategory/ID-2022 | 0.634 |
| crawl4ai-raw | #1 | www.newegg.com/Enterprise-SSDs/SubCategory/ID-2021 | 0.657 | www.newegg.com/Enterprise-SSDs/SubCategory/ID-2021 | 0.657 | www.newegg.com/External-SSDs/SubCategory/ID-2022 | 0.634 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.591 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.581 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.563 |
| playwright | #37 | www.newegg.com/server-system-configurator/ | 0.459 | www.newegg.com/ | 0.452 | www.newegg.com/ | 0.450 |


**Q56: What is the maximum sequential read speed of the Micron SSD 2500 PCIe Gen4 NVMe SSD?**
*(expects URL containing: `ID-2021`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #9 | www.newegg.com/Internal-SSDs/SubCategory/ID-636 | 0.676 | www.newegg.com/SSD/Category/ID-119 | 0.668 | www.newegg.com/SSD/Category/ID-119 | 0.634 |
| crawl4ai-raw | #9 | www.newegg.com/Internal-SSDs/SubCategory/ID-636 | 0.676 | www.newegg.com/SSD/Category/ID-119 | 0.668 | www.newegg.com/SSD/Category/ID-119 | 0.634 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.550 | www.newegg.com/Newegg-Select/EventSaleStore/ID-183 | 0.546 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.539 |
| playwright | #39 | www.newegg.com/ | 0.440 | www.newegg.com/ | 0.421 | www.newegg.com/ | 0.401 |


**Q57: What brands are available for laptop add-on cards?**
*(expects URL containing: `ID-421`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/Add-On-Cards/SubCategory/ID-73 | 0.629 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.611 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.605 |
| crawl4ai-raw | #2 | www.newegg.com/Add-On-Cards/SubCategory/ID-73 | 0.629 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.611 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.605 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Gaming-Laptops/SubCategory/ID-3365? | 0.504 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.492 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.492 |
| playwright | miss | www.newegg.com/ | 0.465 | www.newegg.com/ | 0.457 | www.newegg.com/ | 0.451 |


**Q58: What is the price range for laptop add-on cards on Newegg?**
*(expects URL containing: `ID-421`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #3 | www.newegg.com/Add-On-Cards/SubCategory/ID-73 | 0.645 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.600 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.593 |
| crawl4ai-raw | #3 | www.newegg.com/Add-On-Cards/SubCategory/ID-73 | 0.645 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.600 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.593 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/All-Laptop/SubCategory/ID-32/Page-3 | 0.553 | www.newegg.com/All-Laptop/SubCategory/ID-32/Page-4 | 0.553 | www.newegg.com/All-Laptop/SubCategory/ID-32/Page-6 | 0.553 |
| playwright | #35 | www.newegg.com/promotions/nepro/18-1881/index.html | 0.465 | www.newegg.com/ | 0.464 | www.newegg.com/ | 0.451 |


</details>

## postgres-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| colly+md | 80% (37/46) | 96% (44/46) | 96% (44/46) | 96% (44/46) | 96% (44/46) | 0.877 | 1115 | 401 |
| crawlee | 80% (37/46) | 96% (44/46) | 96% (44/46) | 96% (44/46) | 96% (44/46) | 0.866 | 1226 | 400 |
| playwright | 80% (37/46) | 96% (44/46) | 96% (44/46) | 96% (44/46) | 96% (44/46) | 0.866 | 1216 | 400 |
| crawl4ai | 74% (34/46) | 83% (38/46) | 91% (42/46) | 93% (43/46) | 93% (43/46) | 0.800 | 1193 | 400 |
| crawl4ai-raw | 74% (34/46) | 83% (38/46) | 89% (41/46) | 93% (43/46) | 93% (43/46) | 0.798 | 1193 | 400 |
| markcrawl | 28% (13/46) | 35% (16/46) | 37% (17/46) | 39% (18/46) | 39% (18/46) | 0.319 | 2348 | 400 |
| scrapy+md | 4% (2/46) | 4% (2/46) | 7% (3/46) | 7% (3/46) | 7% (3/46) | 0.050 | 1531 | 394 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for postgres-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: Who are the current committers for PostgreSQL?**
*(expects URL containing: `committers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/index.html | 0.541 | www.postgresql.org/docs/current/index.html | 0.535 | www.postgresql.org/docs/current/internals.html | 0.513 |
| crawl4ai | #1 | www.postgresql.org/developer/committers/ | 0.714 | www.postgresql.org/developer/committers/ | 0.698 | www.postgresql.org/community/contributors/ | 0.690 |
| crawl4ai-raw | #1 | www.postgresql.org/developer/committers/ | 0.714 | www.postgresql.org/developer/committers/ | 0.698 | www.postgresql.org/community/contributors/ | 0.690 |
| scrapy+md | miss | www.postgresql.org/developer/core/ | 0.625 | www.postgresql.org/about/policies/coc/reports/2018 | 0.619 | www.postgresql.org/about/policies/coc/reports/2019 | 0.617 |
| crawlee | #1 | www.postgresql.org/developer/committers/ | 0.751 | www.postgresql.org/developer/committers/ | 0.714 | www.postgresql.org/community/contributors/ | 0.703 |
| colly+md | #1 | www.postgresql.org/developer/committers/ | 0.751 | www.postgresql.org/developer/committers/ | 0.714 | www.postgresql.org/community/contributors/ | 0.703 |
| playwright | #1 | www.postgresql.org/developer/committers/ | 0.751 | www.postgresql.org/developer/committers/ | 0.714 | www.postgresql.org/community/contributors/ | 0.704 |


**Q2: What criteria are used to select new committers for PostgreSQL?**
*(expects URL containing: `committers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/wal-reliability.ht | 0.405 | www.postgresql.org/docs/current/index.html | 0.401 | www.postgresql.org/docs/current/index.html | 0.399 |
| crawl4ai | #1 | www.postgresql.org/developer/committers/ | 0.762 | www.postgresql.org/about/policies/npos/ | 0.600 | www.postgresql.org/developer/committers/ | 0.595 |
| crawl4ai-raw | #1 | www.postgresql.org/developer/committers/ | 0.762 | www.postgresql.org/about/policies/npos/ | 0.600 | www.postgresql.org/developer/committers/ | 0.595 |
| scrapy+md | miss | www.postgresql.org/about/policies/npos/ | 0.603 | www.postgresql.org/about/policies/coc/reports/2020 | 0.596 | www.postgresql.org/about/policies/coc/reports/2020 | 0.547 |
| crawlee | #1 | www.postgresql.org/developer/committers/ | 0.764 | www.postgresql.org/developer/committers/ | 0.657 | www.postgresql.org/community/contributors/ | 0.618 |
| colly+md | #1 | www.postgresql.org/developer/committers/ | 0.764 | www.postgresql.org/developer/committers/ | 0.657 | www.postgresql.org/community/contributors/ | 0.618 |
| playwright | #1 | www.postgresql.org/developer/committers/ | 0.764 | www.postgresql.org/developer/committers/ | 0.657 | www.postgresql.org/community/contributors/ | 0.618 |


**Q3: How can I install PostgreSQL on FreeBSD?**
*(expects URL containing: `freebsd`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/install-make.html | 0.526 | www.postgresql.org/docs/current/install-make.html | 0.524 | www.postgresql.org/docs/current/install-make.html | 0.514 |
| crawl4ai | #2 | www.postgresql.org/download/macosx/ | 0.609 | www.postgresql.org/download/freebsd/ | 0.562 | www.postgresql.org/download/linux/redhat | 0.552 |
| crawl4ai-raw | #2 | www.postgresql.org/download/macosx/ | 0.609 | www.postgresql.org/download/freebsd/ | 0.562 | www.postgresql.org/download/linux/redhat | 0.552 |
| scrapy+md | miss | www.postgresql.org/docs/9.1/install-procedure.html | 0.549 | www.postgresql.org/docs/9.1/install-procedure.html | 0.542 | www.postgresql.org/docs/9.1/install-procedure.html | 0.526 |
| crawlee | #1 | www.postgresql.org/download/freebsd/ | 0.696 | www.postgresql.org/download/openbsd/ | 0.649 | www.postgresql.org/download/netbsd/ | 0.634 |
| colly+md | #1 | www.postgresql.org/download/freebsd/ | 0.696 | www.postgresql.org/download/openbsd/ | 0.649 | www.postgresql.org/download/netbsd/ | 0.634 |
| playwright | #1 | www.postgresql.org/download/freebsd/ | 0.696 | www.postgresql.org/download/openbsd/ | 0.649 | www.postgresql.org/download/netbsd/ | 0.634 |


**Q4: Where can I find a list of PostgreSQL packages for FreeBSD?**
*(expects URL containing: `freebsd`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/reference-server.h | 0.528 | www.postgresql.org/docs/current/index.html | 0.516 | www.postgresql.org/docs/current/index.html | 0.516 |
| crawl4ai | #1 | www.postgresql.org/download/freebsd/ | 0.662 | www.postgresql.org/download/macosx/ | 0.655 | www.postgresql.org/download/netbsd/ | 0.630 |
| crawl4ai-raw | #1 | www.postgresql.org/download/freebsd/ | 0.662 | www.postgresql.org/download/macosx/ | 0.655 | www.postgresql.org/download/netbsd/ | 0.630 |
| scrapy+md | miss | www.postgresql.org/docs/9.2/libpq-control.html | 0.558 | www.postgresql.org/docs/9.2/libpq-envars.html | 0.558 | www.postgresql.org/docs/9.2/libpq-connect.html | 0.555 |
| crawlee | #1 | www.postgresql.org/download/freebsd/ | 0.806 | www.postgresql.org/download/openbsd/ | 0.753 | www.postgresql.org/download/netbsd/ | 0.749 |
| colly+md | #1 | www.postgresql.org/download/freebsd/ | 0.806 | www.postgresql.org/download/openbsd/ | 0.753 | www.postgresql.org/download/netbsd/ | 0.749 |
| playwright | #1 | www.postgresql.org/download/freebsd/ | 0.806 | www.postgresql.org/download/openbsd/ | 0.753 | www.postgresql.org/download/netbsd/ | 0.749 |


**Q5: What should be included in every bug report?**
*(expects URL containing: `bug-reporting.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/runtime-config-log | 0.414 | www.postgresql.org/docs/current/error-style-guide. | 0.410 | www.postgresql.org/docs/current/admin.html | 0.339 |
| crawl4ai | #1 | www.postgresql.org/docs/17/bug-reporting.html | 0.641 | www.postgresql.org/docs/18/bug-reporting.html | 0.641 | www.postgresql.org/docs/current/bug-reporting.html | 0.641 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/bug-reporting.html | 0.641 | www.postgresql.org/docs/17/bug-reporting.html | 0.641 | www.postgresql.org/docs/18/bug-reporting.html | 0.641 |
| scrapy+md | miss | www.postgresql.org/docs/7.3/doc-style.html | 0.373 | www.postgresql.org/about/policies/coc/ | 0.364 | www.postgresql.org/docs/7.3/doc-style.html | 0.360 |
| crawlee | #1 | www.postgresql.org/docs/current/bug-reporting.html | 0.616 | www.postgresql.org/docs/17/bug-reporting.html | 0.616 | www.postgresql.org/docs/18/bug-reporting.html | 0.616 |
| colly+md | #1 | www.postgresql.org/docs/16/bug-reporting.html | 0.616 | www.postgresql.org/docs/18/bug-reporting.html | 0.616 | www.postgresql.org/docs/17/bug-reporting.html | 0.616 |
| playwright | #1 | www.postgresql.org/docs/18/bug-reporting.html | 0.616 | www.postgresql.org/docs/current/bug-reporting.html | 0.616 | www.postgresql.org/docs/17/bug-reporting.html | 0.616 |


**Q6: Where should I send bug reports for PostgreSQL?**
*(expects URL containing: `bug-reporting.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/runtime-config-rep | 0.515 | www.postgresql.org/docs/current/reference-server.h | 0.503 | www.postgresql.org/docs/current/runtime-config-fil | 0.488 |
| crawl4ai | #1 | www.postgresql.org/docs/17/bug-reporting.html | 0.722 | www.postgresql.org/docs/18/bug-reporting.html | 0.722 | www.postgresql.org/docs/current/bug-reporting.html | 0.722 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/bug-reporting.html | 0.722 | www.postgresql.org/docs/18/bug-reporting.html | 0.722 | www.postgresql.org/docs/current/bug-reporting.html | 0.722 |
| scrapy+md | miss | www.postgresql.org/docs/9.2/runtime-config-logging | 0.543 | www.postgresql.org/about/contact/ | 0.515 | www.postgresql.org/docs/7.3/release-0-02.html | 0.506 |
| crawlee | #1 | www.postgresql.org/docs/17/bug-reporting.html | 0.687 | www.postgresql.org/docs/18/bug-reporting.html | 0.687 | www.postgresql.org/docs/current/bug-reporting.html | 0.687 |
| colly+md | #1 | www.postgresql.org/docs/16/bug-reporting.html | 0.687 | www.postgresql.org/docs/18/bug-reporting.html | 0.687 | www.postgresql.org/docs/17/bug-reporting.html | 0.687 |
| playwright | #1 | www.postgresql.org/docs/current/bug-reporting.html | 0.687 | www.postgresql.org/docs/18/bug-reporting.html | 0.687 | www.postgresql.org/docs/17/bug-reporting.html | 0.687 |


**Q7: What is PL/Tcl?**
*(expects URL containing: `pltcl.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/pltcl.html | 0.690 | www.postgresql.org/docs/current/pltcl-overview.htm | 0.655 | www.postgresql.org/docs/current/pltcl-overview.htm | 0.652 |
| crawl4ai | #1 | www.postgresql.org/docs/current/pltcl.html | 0.530 | www.postgresql.org/docs/18/pltcl.html | 0.530 | www.postgresql.org/docs/17/pltcl.html | 0.528 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/pltcl.html | 0.530 | www.postgresql.org/docs/18/pltcl.html | 0.530 | www.postgresql.org/docs/17/pltcl.html | 0.528 |
| scrapy+md | miss | www.postgresql.org/docs/7.3/app-pgtclsh.html | 0.459 | www.postgresql.org/docs/7.4/release-0-03.html | 0.435 | www.postgresql.org/docs/7.3/release-0-03.html | 0.433 |
| crawlee | #1 | www.postgresql.org/docs/current/pltcl.html | 0.611 | www.postgresql.org/docs/18/pltcl.html | 0.611 | www.postgresql.org/docs/17/pltcl.html | 0.603 |
| colly+md | #1 | www.postgresql.org/docs/18/pltcl.html | 0.611 | www.postgresql.org/docs/current/pltcl.html | 0.611 | www.postgresql.org/docs/17/server-programming.html | 0.530 |
| playwright | #1 | www.postgresql.org/docs/current/pltcl.html | 0.611 | www.postgresql.org/docs/18/pltcl.html | 0.611 | www.postgresql.org/docs/17/pltcl.html | 0.603 |


**Q8: What language does PL/Tcl enable to write PostgreSQL functions and procedures?**
*(expects URL containing: `pltcl.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | www.postgresql.org/docs/current/pltcl-overview.htm | 0.693 | www.postgresql.org/docs/current/pltcl-overview.htm | 0.659 | www.postgresql.org/docs/current/pltcl.html | 0.657 |
| crawl4ai | #1 | www.postgresql.org/docs/current/pltcl.html | 0.651 | www.postgresql.org/docs/18/pltcl.html | 0.651 | www.postgresql.org/docs/17/pltcl.html | 0.649 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/pltcl.html | 0.651 | www.postgresql.org/docs/18/pltcl.html | 0.651 | www.postgresql.org/docs/17/pltcl.html | 0.649 |
| scrapy+md | miss | www.postgresql.org/docs/9.0/server-programming.htm | 0.560 | www.postgresql.org/docs/current/bookindex.html | 0.532 | www.postgresql.org/docs/7.3/app-pgtclsh.html | 0.530 |
| crawlee | #1 | www.postgresql.org/docs/18/pltcl.html | 0.702 | www.postgresql.org/docs/current/pltcl.html | 0.702 | www.postgresql.org/docs/17/pltcl.html | 0.694 |
| colly+md | #1 | www.postgresql.org/docs/18/pltcl.html | 0.702 | www.postgresql.org/docs/current/pltcl.html | 0.701 | www.postgresql.org/docs/18/xplang.html | 0.651 |
| playwright | #1 | www.postgresql.org/docs/current/pltcl.html | 0.702 | www.postgresql.org/docs/18/pltcl.html | 0.701 | www.postgresql.org/docs/17/pltcl.html | 0.694 |


**Q9: What are the procedural languages available in the standard PostgreSQL distribution?**
*(expects URL containing: `xplang.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/xplang.html | 0.707 | www.postgresql.org/docs/current/xfunc-pl.html | 0.662 | www.postgresql.org/docs/current/xplang-install.htm | 0.598 |
| crawl4ai | #1 | www.postgresql.org/docs/18/xplang.html | 0.675 | www.postgresql.org/docs/current/xplang.html | 0.675 | www.postgresql.org/docs/17/xplang.html | 0.675 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/xplang.html | 0.675 | www.postgresql.org/docs/18/xplang.html | 0.675 | www.postgresql.org/docs/17/xplang.html | 0.675 |
| scrapy+md | miss | www.postgresql.org/docs/9.0/server-programming.htm | 0.580 | www.postgresql.org/docs/9.1/client-interfaces.html | 0.559 | www.postgresql.org/docs/7.2/reference-client.html | 0.553 |
| crawlee | #1 | www.postgresql.org/docs/current/xplang.html | 0.716 | www.postgresql.org/docs/18/xplang.html | 0.716 | www.postgresql.org/docs/17/xplang.html | 0.715 |
| colly+md | #1 | www.postgresql.org/docs/18/xplang.html | 0.716 | www.postgresql.org/docs/current/xplang.html | 0.716 | www.postgresql.org/docs/17/xplang.html | 0.715 |
| playwright | #1 | www.postgresql.org/docs/current/xplang.html | 0.716 | www.postgresql.org/docs/18/xplang.html | 0.716 | www.postgresql.org/docs/17/xplang.html | 0.715 |


**Q10: How does PostgreSQL handle functions written in procedural languages?**
*(expects URL containing: `xplang.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | www.postgresql.org/docs/current/xfunc-pl.html | 0.693 | www.postgresql.org/docs/current/xplang.html | 0.679 | www.postgresql.org/docs/current/plpgsql-overview.h | 0.633 |
| crawl4ai | #3 | www.postgresql.org/docs/current/plhandler.html | 0.664 | www.postgresql.org/docs/18/plhandler.html | 0.664 | www.postgresql.org/docs/18/xplang.html | 0.629 |
| crawl4ai-raw | #3 | www.postgresql.org/docs/current/plhandler.html | 0.664 | www.postgresql.org/docs/18/plhandler.html | 0.664 | www.postgresql.org/docs/18/xplang.html | 0.629 |
| scrapy+md | miss | www.postgresql.org/docs/9.0/server-programming.htm | 0.590 | www.postgresql.org/docs/9.0/functions-info.html | 0.539 | www.postgresql.org/docs/8.1/functions.html | 0.537 |
| crawlee | #3 | www.postgresql.org/docs/18/plhandler.html | 0.679 | www.postgresql.org/docs/current/plhandler.html | 0.679 | www.postgresql.org/docs/18/xplang.html | 0.679 |
| colly+md | #2 | www.postgresql.org/docs/current/plhandler.html | 0.679 | www.postgresql.org/docs/18/xplang.html | 0.679 | www.postgresql.org/docs/current/xplang.html | 0.679 |
| playwright | #3 | www.postgresql.org/docs/current/plhandler.html | 0.679 | www.postgresql.org/docs/18/plhandler.html | 0.679 | www.postgresql.org/docs/current/xplang.html | 0.679 |


**Q11: What is a security vulnerability in PostgreSQL?**
*(expects URL containing: `security`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/perm-functions.htm | 0.540 | www.postgresql.org/docs/current/wal-reliability.ht | 0.525 | www.postgresql.org/docs/current/internals.html | 0.512 |
| crawl4ai | #1 | www.postgresql.org/support/security/ | 0.726 | www.postgresql.org/support/security/ | 0.718 | www.postgresql.org/support/security/ | 0.691 |
| crawl4ai-raw | #1 | www.postgresql.org/support/security/ | 0.726 | www.postgresql.org/support/security/ | 0.718 | www.postgresql.org/support/security/ | 0.691 |
| scrapy+md | #4 | www.postgresql.org/docs/7.4/libpq-pgpass.html | 0.522 | www.postgresql.org/docs/8.1/libpq-pgpass.html | 0.517 | www.postgresql.org/docs/8.2/libpq-pgpass.html | 0.513 |
| crawlee | #1 | www.postgresql.org/support/security/ | 0.705 | www.postgresql.org/support/security/ | 0.702 | www.postgresql.org/support/security/ | 0.701 |
| colly+md | #1 | www.postgresql.org/support/security/ | 0.705 | www.postgresql.org/support/security/ | 0.702 | www.postgresql.org/support/security/ | 0.701 |
| playwright | #1 | www.postgresql.org/support/security/ | 0.705 | www.postgresql.org/support/security/ | 0.702 | www.postgresql.org/support/security/ | 0.701 |


**Q12: How can I report a PostgreSQL security vulnerability?**
*(expects URL containing: `security`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/perm-functions.htm | 0.493 | www.postgresql.org/docs/current/sql-grant.html | 0.481 | www.postgresql.org/docs/current/runtime-config-rep | 0.476 |
| crawl4ai | #1 | www.postgresql.org/support/security/ | 0.787 | www.postgresql.org/support/security/ | 0.691 | www.postgresql.org/support/security/ | 0.679 |
| crawl4ai-raw | #1 | www.postgresql.org/support/security/ | 0.787 | www.postgresql.org/support/security/ | 0.691 | www.postgresql.org/support/security/ | 0.679 |
| scrapy+md | #21 | www.postgresql.org/docs/9.2/runtime-config-logging | 0.517 | www.postgresql.org/docs/7.4/libpq-pgpass.html | 0.500 | www.postgresql.org/docs/8.1/libpq-pgpass.html | 0.496 |
| crawlee | #1 | www.postgresql.org/support/security/ | 0.778 | www.postgresql.org/support/security/ | 0.713 | www.postgresql.org/support/security/ | 0.667 |
| colly+md | #1 | www.postgresql.org/support/security/ | 0.778 | www.postgresql.org/support/security/ | 0.713 | www.postgresql.org/support/security/ | 0.667 |
| playwright | #1 | www.postgresql.org/support/security/ | 0.778 | www.postgresql.org/support/security/ | 0.713 | www.postgresql.org/support/security/ | 0.667 |


**Q13: What is the title of the book authored by Jesús Espino?**
*(expects URL containing: `books`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/textsearch-control | 0.173 | www.postgresql.org/docs/current/spi-examples.html | 0.170 | www.postgresql.org/docs/current/app-psql.html | 0.168 |
| crawl4ai | #1 | www.postgresql.org/docs/books/ | 0.290 | www.postgresql.org/docs/books/ | 0.278 | www.postgresql.org/docs/books/ | 0.241 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/books/ | 0.290 | www.postgresql.org/docs/books/ | 0.278 | www.postgresql.org/docs/books/ | 0.241 |
| scrapy+md | miss | www.postgresql.org/docs/current/biblio.html | 0.169 | www.postgresql.org/docs/7.1/biblio.html | 0.148 | www.postgresql.org/docs/current/bookindex.html | 0.142 |
| crawlee | #1 | www.postgresql.org/docs/books/ | 0.256 | www.postgresql.org/docs/books/ | 0.254 | www.postgresql.org/docs/books/ | 0.238 |
| colly+md | #1 | www.postgresql.org/docs/books/ | 0.256 | www.postgresql.org/docs/books/ | 0.254 | www.postgresql.org/docs/books/ | 0.238 |
| playwright | #1 | www.postgresql.org/docs/books/ | 0.256 | www.postgresql.org/docs/books/ | 0.254 | www.postgresql.org/docs/books/ | 0.238 |


**Q14: Who are the authors of the book 'PostgreSQL 16 Administration Cookbook'?**
*(expects URL containing: `books`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/admin.html | 0.529 | www.postgresql.org/docs/current/index.html | 0.511 | www.postgresql.org/docs/current/admin.html | 0.479 |
| crawl4ai | #1 | www.postgresql.org/docs/books/ | 0.653 | www.postgresql.org/docs/books/ | 0.631 | www.postgresql.org/docs/books/ | 0.627 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/books/ | 0.653 | www.postgresql.org/docs/books/ | 0.631 | www.postgresql.org/docs/books/ | 0.627 |
| scrapy+md | miss | www.postgresql.org/docs/7.1/biblio.html | 0.558 | www.postgresql.org/docs/7.4/biblio.html | 0.553 | www.postgresql.org/docs/8.1/biblio.html | 0.551 |
| crawlee | #1 | www.postgresql.org/docs/books/ | 0.668 | www.postgresql.org/docs/books/ | 0.646 | www.postgresql.org/docs/books/ | 0.627 |
| colly+md | #1 | www.postgresql.org/docs/books/ | 0.668 | www.postgresql.org/docs/books/ | 0.646 | www.postgresql.org/docs/books/ | 0.627 |
| playwright | #1 | www.postgresql.org/docs/books/ | 0.668 | www.postgresql.org/docs/books/ | 0.646 | www.postgresql.org/docs/books/ | 0.627 |


**Q15: What are the procedural languages available in the standard PostgreSQL distribution?**
*(expects URL containing: `xplang.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/xplang.html | 0.707 | www.postgresql.org/docs/current/xfunc-pl.html | 0.662 | www.postgresql.org/docs/current/xplang-install.htm | 0.598 |
| crawl4ai | #1 | www.postgresql.org/docs/18/xplang.html | 0.675 | www.postgresql.org/docs/current/xplang.html | 0.675 | www.postgresql.org/docs/17/xplang.html | 0.675 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/xplang.html | 0.675 | www.postgresql.org/docs/18/xplang.html | 0.675 | www.postgresql.org/docs/17/xplang.html | 0.675 |
| scrapy+md | miss | www.postgresql.org/docs/9.0/server-programming.htm | 0.580 | www.postgresql.org/docs/9.1/client-interfaces.html | 0.559 | www.postgresql.org/docs/7.2/reference-client.html | 0.553 |
| crawlee | #1 | www.postgresql.org/docs/current/xplang.html | 0.716 | www.postgresql.org/docs/18/xplang.html | 0.716 | www.postgresql.org/docs/17/xplang.html | 0.715 |
| colly+md | #1 | www.postgresql.org/docs/18/xplang.html | 0.716 | www.postgresql.org/docs/current/xplang.html | 0.716 | www.postgresql.org/docs/17/xplang.html | 0.715 |
| playwright | #1 | www.postgresql.org/docs/current/xplang.html | 0.716 | www.postgresql.org/docs/18/xplang.html | 0.716 | www.postgresql.org/docs/17/xplang.html | 0.715 |


**Q16: How does PostgreSQL handle functions written in procedural languages?**
*(expects URL containing: `xplang.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | www.postgresql.org/docs/current/xfunc-pl.html | 0.693 | www.postgresql.org/docs/current/xplang.html | 0.679 | www.postgresql.org/docs/current/plpgsql-overview.h | 0.633 |
| crawl4ai | #3 | www.postgresql.org/docs/current/plhandler.html | 0.664 | www.postgresql.org/docs/18/plhandler.html | 0.664 | www.postgresql.org/docs/18/xplang.html | 0.629 |
| crawl4ai-raw | #3 | www.postgresql.org/docs/current/plhandler.html | 0.664 | www.postgresql.org/docs/18/plhandler.html | 0.664 | www.postgresql.org/docs/18/xplang.html | 0.629 |
| scrapy+md | miss | www.postgresql.org/docs/9.0/server-programming.htm | 0.590 | www.postgresql.org/docs/9.0/functions-info.html | 0.539 | www.postgresql.org/docs/8.1/functions.html | 0.537 |
| crawlee | #3 | www.postgresql.org/docs/18/plhandler.html | 0.679 | www.postgresql.org/docs/current/plhandler.html | 0.679 | www.postgresql.org/docs/18/xplang.html | 0.679 |
| colly+md | #2 | www.postgresql.org/docs/current/plhandler.html | 0.679 | www.postgresql.org/docs/18/xplang.html | 0.679 | www.postgresql.org/docs/current/xplang.html | 0.679 |
| playwright | #3 | www.postgresql.org/docs/current/plhandler.html | 0.679 | www.postgresql.org/docs/18/plhandler.html | 0.679 | www.postgresql.org/docs/current/xplang.html | 0.679 |


**Q17: What is logical replication in PostgreSQL?**
*(expects URL containing: `logical-replication.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.732 | www.postgresql.org/docs/current/logicaldecoding-ex | 0.648 | www.postgresql.org/docs/current/logicaldecoding-ex | 0.625 |
| crawl4ai | #1 | www.postgresql.org/docs/18/logical-replication.htm | 0.720 | www.postgresql.org/docs/current/logical-replicatio | 0.720 | www.postgresql.org/docs/17/logical-replication.htm | 0.712 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/logical-replication.htm | 0.720 | www.postgresql.org/docs/current/logical-replicatio | 0.720 | www.postgresql.org/docs/17/logical-replication.htm | 0.712 |
| scrapy+md | miss | www.postgresql.org/docs/8.0/mvcc.html | 0.490 | www.postgresql.org/docs/9.5/test-decoding.html | 0.488 | www.postgresql.org/docs/9.4/test-decoding.html | 0.487 |
| crawlee | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.707 | www.postgresql.org/docs/18/logical-replication.htm | 0.707 | www.postgresql.org/docs/17/logical-replication.htm | 0.699 |
| colly+md | #1 | www.postgresql.org/docs/18/logical-replication.htm | 0.707 | www.postgresql.org/docs/current/logical-replicatio | 0.707 | www.postgresql.org/docs/17/logical-replication.htm | 0.699 |
| playwright | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.707 | www.postgresql.org/docs/18/logical-replication.htm | 0.707 | www.postgresql.org/docs/17/logical-replication.htm | 0.699 |


**Q18: What are the typical use-cases for logical replication?**
*(expects URL containing: `logical-replication.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.629 | www.postgresql.org/docs/current/logical-replicatio | 0.574 | www.postgresql.org/docs/current/logical-replicatio | 0.557 |
| crawl4ai | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.661 | www.postgresql.org/docs/18/logical-replication.htm | 0.661 | www.postgresql.org/docs/17/logical-replication.htm | 0.654 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.661 | www.postgresql.org/docs/18/logical-replication.htm | 0.661 | www.postgresql.org/docs/17/logical-replication.htm | 0.654 |
| scrapy+md | miss | www.postgresql.org/docs/current/sql-createpublicat | 0.406 | www.postgresql.org/docs/current/sql-createpublicat | 0.360 | www.postgresql.org/docs/current/sql-createrole.htm | 0.351 |
| crawlee | #1 | www.postgresql.org/docs/18/logical-replication.htm | 0.650 | www.postgresql.org/docs/current/logical-replicatio | 0.650 | www.postgresql.org/docs/17/logical-replication.htm | 0.645 |
| colly+md | #1 | www.postgresql.org/docs/18/logical-replication.htm | 0.650 | www.postgresql.org/docs/current/logical-replicatio | 0.650 | www.postgresql.org/docs/17/logical-replication.htm | 0.645 |
| playwright | #1 | www.postgresql.org/docs/18/logical-replication.htm | 0.650 | www.postgresql.org/docs/current/logical-replicatio | 0.650 | www.postgresql.org/docs/17/logical-replication.htm | 0.645 |


**Q19: What is PgQue v0.1?**
*(expects URL containing: `pgque-v01-zero-bloat-postgres-queue-3284`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/libpq-pgpass.html | 0.393 | www.postgresql.org/docs/current/view-pg-file-setti | 0.390 | www.postgresql.org/docs/current/libpq-connect.html | 0.374 |
| crawl4ai | #1 | www.postgresql.org/about/news/pgque-v01-zero-bloat | 0.614 | www.postgresql.org/ | 0.519 | www.postgresql.org/about/newsarchive/ | 0.466 |
| crawl4ai-raw | #1 | www.postgresql.org/about/news/pgque-v01-zero-bloat | 0.614 | www.postgresql.org/ | 0.519 | www.postgresql.org/about/newsarchive/ | 0.466 |
| scrapy+md | miss | www.postgresql.org/docs/current/bookindex.html | 0.437 | www.postgresql.org/docs/current/bookindex.html | 0.437 | www.postgresql.org/docs/current/bookindex.html | 0.432 |
| crawlee | #1 | www.postgresql.org/about/news/pgque-v01-zero-bloat | 0.622 | www.postgresql.org/about/newsarchive/ | 0.462 | www.postgresql.org/ | 0.461 |
| colly+md | #1 | www.postgresql.org/about/news/pgque-v01-zero-bloat | 0.622 | www.postgresql.org/about/newsarchive/ | 0.462 | www.postgresql.org/ | 0.461 |
| playwright | #1 | www.postgresql.org/about/news/pgque-v01-zero-bloat | 0.622 | www.postgresql.org/about/newsarchive/ | 0.462 | www.postgresql.org/ | 0.461 |


**Q20: What are the key features of PgQue?**
*(expects URL containing: `pgque-v01-zero-bloat-postgres-queue-3284`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/plpgsql-overview.h | 0.429 | www.postgresql.org/docs/current/plpgsql-overview.h | 0.423 | www.postgresql.org/docs/current/view-pg-file-setti | 0.414 |
| crawl4ai | #1 | www.postgresql.org/about/news/pgque-v01-zero-bloat | 0.632 | www.postgresql.org/ | 0.558 | www.postgresql.org/about/newsarchive/ | 0.510 |
| crawl4ai-raw | #1 | www.postgresql.org/about/news/pgque-v01-zero-bloat | 0.632 | www.postgresql.org/ | 0.558 | www.postgresql.org/about/newsarchive/ | 0.510 |
| scrapy+md | miss | www.postgresql.org/docs/current/bookindex.html | 0.518 | www.postgresql.org/docs/current/bookindex.html | 0.502 | www.postgresql.org/docs/current/bookindex.html | 0.488 |
| crawlee | #1 | www.postgresql.org/about/news/pgque-v01-zero-bloat | 0.619 | www.postgresql.org/docs/current/bookindex.html | 0.518 | www.postgresql.org/docs/18/bookindex.html | 0.518 |
| colly+md | #1 | www.postgresql.org/about/news/pgque-v01-zero-bloat | 0.619 | www.postgresql.org/docs/current/bookindex.html | 0.518 | www.postgresql.org/about/newsarchive/ | 0.507 |
| playwright | #1 | www.postgresql.org/about/news/pgque-v01-zero-bloat | 0.619 | www.postgresql.org/docs/current/bookindex.html | 0.518 | www.postgresql.org/docs/18/bookindex.html | 0.518 |


**Q21: What does PostgreSQL use for date/time input support?**
*(expects URL containing: `datetime-appendix.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | www.postgresql.org/docs/current/datatype-datetime. | 0.696 | www.postgresql.org/docs/current/datatype-datetime. | 0.691 | www.postgresql.org/docs/current/datatype-datetime. | 0.661 |
| crawl4ai | #1 | www.postgresql.org/docs/18/datetime-appendix.html | 0.611 | www.postgresql.org/docs/current/datetime-appendix. | 0.611 | www.postgresql.org/about/ | 0.589 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/datetime-appendix.html | 0.611 | www.postgresql.org/docs/current/datetime-appendix. | 0.611 | www.postgresql.org/about/ | 0.589 |
| scrapy+md | miss | www.postgresql.org/docs/9.1/datatype-datetime.html | 0.664 | www.postgresql.org/docs/9.1/datatype-datetime.html | 0.663 | www.postgresql.org/docs/9.1/datatype-datetime.html | 0.652 |
| crawlee | #1 | www.postgresql.org/docs/current/datetime-appendix. | 0.634 | www.postgresql.org/docs/18/datetime-appendix.html | 0.634 | www.postgresql.org/about/ | 0.548 |
| colly+md | #1 | www.postgresql.org/docs/current/datetime-appendix. | 0.634 | www.postgresql.org/about/ | 0.548 | www.postgresql.org/about/ | 0.543 |
| playwright | #1 | www.postgresql.org/docs/18/datetime-appendix.html | 0.634 | www.postgresql.org/docs/current/datetime-appendix. | 0.634 | www.postgresql.org/about/ | 0.548 |


**Q22: What information does this appendix include about the parser?**
*(expects URL containing: `datetime-appendix.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #9 | www.postgresql.org/docs/current/parser-stage.html | 0.522 | www.postgresql.org/docs/current/catalog-pg-ts-pars | 0.513 | www.postgresql.org/docs/current/textsearch-parsers | 0.507 |
| crawl4ai | miss | www.postgresql.org/docs/18/appendixes.html | 0.418 | www.postgresql.org/docs/current/appendixes.html | 0.418 | www.postgresql.org/docs/current/internals.html | 0.418 |
| crawl4ai-raw | miss | www.postgresql.org/docs/current/appendixes.html | 0.418 | www.postgresql.org/docs/18/appendixes.html | 0.418 | www.postgresql.org/docs/18/internals.html | 0.418 |
| scrapy+md | miss | www.postgresql.org/docs/9.4/test-parser.html | 0.468 | www.postgresql.org/docs/9.3/test-parser.html | 0.455 | www.postgresql.org/docs/9.2/test-parser.html | 0.452 |
| crawlee | #46 | www.postgresql.org/docs/18/appendixes.html | 0.422 | www.postgresql.org/docs/current/appendixes.html | 0.422 | www.postgresql.org/docs/18/overview.html | 0.417 |
| colly+md | #34 | www.postgresql.org/docs/current/appendixes.html | 0.422 | www.postgresql.org/docs/current/overview.html | 0.417 | www.postgresql.org/docs/current/internals.html | 0.417 |
| playwright | #46 | www.postgresql.org/docs/current/appendixes.html | 0.422 | www.postgresql.org/docs/18/appendixes.html | 0.422 | www.postgresql.org/docs/18/overview.html | 0.417 |


**Q23: What is the contact email for press enquiries?**
*(expects URL containing: `press`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #43 | www.postgresql.org/docs/current/view-pg-publicatio | 0.182 | www.postgresql.org/docs/current/catalog-pg-publica | 0.179 | www.postgresql.org/docs/current/libpq-pgpass.html | 0.176 |
| crawl4ai | #5 | www.postgresql.org/community/contributors/ | 0.304 | www.postgresql.org/developer/related-projects/ | 0.275 | www.postgresql.org/community/contributors/ | 0.271 |
| crawl4ai-raw | #5 | www.postgresql.org/community/contributors/ | 0.304 | www.postgresql.org/developer/related-projects/ | 0.275 | www.postgresql.org/community/contributors/ | 0.271 |
| scrapy+md | miss | www.postgresql.org/about/contact/ | 0.237 | www.postgresql.org/about/policies/coc/ | 0.223 | www.postgresql.org/about/policies/coc/ | 0.209 |
| crawlee | #2 | www.postgresql.org/about/contact/ | 0.375 | www.postgresql.org/about/press/ | 0.337 | www.postgresql.org/community/contributors/ | 0.283 |
| colly+md | #2 | www.postgresql.org/about/contact/ | 0.375 | www.postgresql.org/about/press/ | 0.337 | www.postgresql.org/community/contributors/ | 0.283 |
| playwright | #2 | www.postgresql.org/about/contact/ | 0.375 | www.postgresql.org/about/press/ | 0.337 | www.postgresql.org/community/contributors/ | 0.283 |


**Q24: Who contributed to the PostgreSQL 18 press kit?**
*(expects URL containing: `press`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/index.html | 0.650 | www.postgresql.org/docs/current/index.html | 0.611 | www.postgresql.org/docs/current/appendixes.html | 0.596 |
| crawl4ai | #1 | www.postgresql.org/about/press/ | 0.780 | www.postgresql.org/community/contributors/ | 0.719 | www.postgresql.org/ | 0.717 |
| crawl4ai-raw | #1 | www.postgresql.org/about/press/ | 0.780 | www.postgresql.org/community/contributors/ | 0.719 | www.postgresql.org/ | 0.717 |
| scrapy+md | miss | www.postgresql.org/docs/current/bookindex.html | 0.688 | www.postgresql.org/developer/core/ | 0.687 | www.postgresql.org/about/contact/ | 0.686 |
| crawlee | #1 | www.postgresql.org/about/press/ | 0.812 | www.postgresql.org/ | 0.703 | www.postgresql.org/docs/release/ | 0.698 |
| colly+md | #1 | www.postgresql.org/about/press/ | 0.812 | www.postgresql.org/ | 0.703 | www.postgresql.org/docs/release/ | 0.698 |
| playwright | #1 | www.postgresql.org/about/press/ | 0.812 | www.postgresql.org/ | 0.703 | www.postgresql.org/docs/release/ | 0.698 |


**Q25: What companies provide the servers for www.postgresql.org?**
*(expects URL containing: `servers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/reference-server.h | 0.498 | www.postgresql.org/docs/current/admin.html | 0.497 | www.postgresql.org/docs/current/app-postgres.html | 0.496 |
| crawl4ai | #1 | www.postgresql.org/about/servers/ | 0.647 | www.postgresql.org/about/servers/ | 0.639 | www.postgresql.org/docs/17/history.html | 0.612 |
| crawl4ai-raw | #1 | www.postgresql.org/about/servers/ | 0.647 | www.postgresql.org/about/servers/ | 0.639 | www.postgresql.org/docs/17/history.html | 0.612 |
| scrapy+md | miss | www.postgresql.org/docs/7.3/reference.html | 0.522 | www.postgresql.org/docs/7.3/release-0-02.html | 0.517 | www.postgresql.org/community/user-groups/ | 0.514 |
| crawlee | #1 | www.postgresql.org/about/servers/ | 0.683 | www.postgresql.org/support/professional_hosting/ | 0.669 | www.postgresql.org/about/servers/ | 0.644 |
| colly+md | #1 | www.postgresql.org/about/servers/ | 0.683 | www.postgresql.org/support/professional/hosting/ | 0.669 | www.postgresql.org/about/servers/ | 0.644 |
| playwright | #1 | www.postgresql.org/about/servers/ | 0.683 | www.postgresql.org/support/professional_hosting/ | 0.669 | www.postgresql.org/about/servers/ | 0.644 |


**Q26: What are the specifications of the server named 'arp'?**
*(expects URL containing: `servers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/runtime-config-pre | 0.351 | www.postgresql.org/docs/current/runtime-config-con | 0.348 | www.postgresql.org/docs/current/runtime-config-con | 0.348 |
| crawl4ai | #6 | www.postgresql.org/docs/18/bookindex.html | 0.350 | www.postgresql.org/docs/current/bookindex.html | 0.350 | www.postgresql.org/docs/18/acronyms.html | 0.348 |
| crawl4ai-raw | #6 | www.postgresql.org/docs/18/bookindex.html | 0.350 | www.postgresql.org/docs/current/bookindex.html | 0.350 | www.postgresql.org/docs/current/acronyms.html | 0.348 |
| scrapy+md | miss | www.postgresql.org/docs/current/bookindex.html | 0.362 | www.postgresql.org/docs/current/bookindex.html | 0.331 | www.postgresql.org/docs/9.2/multibyte.html | 0.322 |
| crawlee | #3 | www.postgresql.org/docs/18/acronyms.html | 0.377 | www.postgresql.org/docs/current/acronyms.html | 0.377 | www.postgresql.org/about/servers/ | 0.366 |
| colly+md | #2 | www.postgresql.org/docs/current/acronyms.html | 0.377 | www.postgresql.org/about/servers/ | 0.366 | www.postgresql.org/docs/current/bookindex.html | 0.362 |
| playwright | #3 | www.postgresql.org/docs/current/acronyms.html | 0.377 | www.postgresql.org/docs/18/acronyms.html | 0.377 | www.postgresql.org/about/servers/ | 0.366 |


**Q27: What factors can affect query performance in PostgreSQL?**
*(expects URL containing: `performance-tips.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/performance-tips.h | 0.521 | www.postgresql.org/docs/current/pgstatstatements.h | 0.506 | www.postgresql.org/docs/current/indexes-types.html | 0.497 |
| crawl4ai | #4 | www.postgresql.org/docs/18/limits.html | 0.507 | www.postgresql.org/docs/current/limits.html | 0.507 | www.postgresql.org/about/ | 0.501 |
| crawl4ai-raw | #6 | www.postgresql.org/about/ | 0.521 | www.postgresql.org/docs/current/limits.html | 0.507 | www.postgresql.org/docs/18/limits.html | 0.507 |
| scrapy+md | miss | www.postgresql.org/docs/7.4/sql-explain.html | 0.510 | www.postgresql.org/docs/7.4/sql-cluster.html | 0.499 | www.postgresql.org/docs/8.0/maintenance.html | 0.482 |
| crawlee | #1 | www.postgresql.org/docs/current/performance-tips.h | 0.550 | www.postgresql.org/docs/18/performance-tips.html | 0.550 | www.postgresql.org/docs/17/performance-tips.html | 0.545 |
| colly+md | #1 | www.postgresql.org/docs/current/performance-tips.h | 0.550 | www.postgresql.org/docs/18/performance-tips.html | 0.550 | www.postgresql.org/docs/17/performance-tips.html | 0.545 |
| playwright | #1 | www.postgresql.org/docs/current/performance-tips.h | 0.550 | www.postgresql.org/docs/18/performance-tips.html | 0.550 | www.postgresql.org/docs/17/performance-tips.html | 0.545 |


**Q28: What does this chapter provide hints about regarding PostgreSQL performance?**
*(expects URL containing: `performance-tips.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/performance-tips.h | 0.658 | www.postgresql.org/docs/current/overview.html | 0.645 | www.postgresql.org/docs/current/internals.html | 0.606 |
| crawl4ai | #4 | www.postgresql.org/docs/current/monitoring.html | 0.634 | www.postgresql.org/docs/18/monitoring.html | 0.634 | www.postgresql.org/docs/17/monitoring.html | 0.633 |
| crawl4ai-raw | #4 | www.postgresql.org/docs/current/monitoring.html | 0.634 | www.postgresql.org/docs/18/monitoring.html | 0.634 | www.postgresql.org/docs/17/monitoring.html | 0.634 |
| scrapy+md | miss | www.postgresql.org/docs/7.3/biblio.html | 0.584 | www.postgresql.org/docs/8.0/admin.html | 0.583 | www.postgresql.org/docs/current/ | 0.582 |
| crawlee | #1 | www.postgresql.org/docs/18/performance-tips.html | 0.670 | www.postgresql.org/docs/current/performance-tips.h | 0.670 | www.postgresql.org/docs/17/performance-tips.html | 0.662 |
| colly+md | #1 | www.postgresql.org/docs/current/performance-tips.h | 0.670 | www.postgresql.org/docs/18/performance-tips.html | 0.670 | www.postgresql.org/docs/17/performance-tips.html | 0.662 |
| playwright | #1 | www.postgresql.org/docs/18/performance-tips.html | 0.670 | www.postgresql.org/docs/current/performance-tips.h | 0.670 | www.postgresql.org/docs/17/performance-tips.html | 0.662 |


**Q29: What are Recognised NPOs in relation to the PostgreSQL project?**
*(expects URL containing: `recognised-npos`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/index.html | 0.492 | www.postgresql.org/docs/current/index.html | 0.477 | www.postgresql.org/docs/current/catalog-pg-namespa | 0.471 |
| crawl4ai | #4 | www.postgresql.org/about/policies/npos/ | 0.713 | www.postgresql.org/about/donate/ | 0.686 | www.postgresql.org/about/policies/npos/ | 0.677 |
| crawl4ai-raw | #4 | www.postgresql.org/about/policies/npos/ | 0.713 | www.postgresql.org/about/donate/ | 0.686 | www.postgresql.org/about/policies/npos/ | 0.677 |
| scrapy+md | miss | www.postgresql.org/about/policies/npos/ | 0.722 | www.postgresql.org/about/policies/npos/ | 0.685 | www.postgresql.org/community/user-groups/ | 0.532 |
| crawlee | #2 | www.postgresql.org/about/policies/npos/ | 0.781 | www.postgresql.org/community/recognised-npos/ | 0.753 | www.postgresql.org/about/donate/ | 0.702 |
| colly+md | #2 | www.postgresql.org/about/policies/npos/ | 0.781 | www.postgresql.org/community/recognised-npos/ | 0.753 | www.postgresql.org/about/donate/ | 0.702 |
| playwright | #2 | www.postgresql.org/about/policies/npos/ | 0.781 | www.postgresql.org/community/recognised-npos | 0.753 | www.postgresql.org/community/recognised-npos/ | 0.753 |


**Q30: What is the goal of PostgreSQL Europe?**
*(expects URL containing: `recognised-npos`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/index.html | 0.495 | www.postgresql.org/docs/current/index.html | 0.485 | www.postgresql.org/docs/current/app-postgres.html | 0.483 |
| crawl4ai | #2 | www.postgresql.org/about/eventarchive/ | 0.644 | www.postgresql.org/community/recognised-npos/ | 0.635 | www.postgresql.org/community/recognised-npos | 0.635 |
| crawl4ai-raw | #2 | www.postgresql.org/about/eventarchive/ | 0.644 | www.postgresql.org/community/recognised-npos | 0.635 | www.postgresql.org/community/recognised-npos/ | 0.635 |
| scrapy+md | miss | www.postgresql.org/about/policies/npos/ | 0.565 | www.postgresql.org/community/user-groups/ | 0.560 | www.postgresql.org/community/user-groups/ | 0.550 |
| crawlee | #3 | www.postgresql.org/about/eventarchive/ | 0.634 | www.postgresql.org/about/eventarchive/ | 0.614 | www.postgresql.org/community/recognised-npos/ | 0.611 |
| colly+md | #3 | www.postgresql.org/about/eventarchive/ | 0.634 | www.postgresql.org/about/eventarchive/ | 0.614 | www.postgresql.org/community/recognised-npos/ | 0.611 |
| playwright | #3 | www.postgresql.org/about/eventarchive/ | 0.634 | www.postgresql.org/about/eventarchive/ | 0.614 | www.postgresql.org/community/recognised-npos | 0.611 |


**Q31: What do brackets indicate in the command synopsis?**
*(expects URL containing: `notation.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/app-psql.html | 0.470 | www.postgresql.org/docs/current/app-psql.html | 0.463 | www.postgresql.org/docs/current/app-psql.html | 0.455 |
| crawl4ai | miss | www.postgresql.org/docs/18/bookindex.html | 0.406 | www.postgresql.org/docs/current/bookindex.html | 0.406 | www.postgresql.org/docs/18/monitoring.html | 0.381 |
| crawl4ai-raw | miss | www.postgresql.org/docs/current/bookindex.html | 0.406 | www.postgresql.org/docs/18/bookindex.html | 0.406 | www.postgresql.org/docs/18/monitoring.html | 0.381 |
| scrapy+md | miss | www.postgresql.org/docs/8.3/app-psql.html | 0.438 | www.postgresql.org/docs/8.3/app-psql.html | 0.434 | www.postgresql.org/docs/8.3/app-psql.html | 0.434 |
| crawlee | #1 | www.postgresql.org/docs/18/notation.html | 0.421 | www.postgresql.org/docs/current/notation.html | 0.421 | www.postgresql.org/docs/17/notation.html | 0.415 |
| colly+md | #1 | www.postgresql.org/docs/current/notation.html | 0.421 | www.postgresql.org/docs/18/notation.html | 0.421 | www.postgresql.org/docs/16/notation.html | 0.419 |
| playwright | #1 | www.postgresql.org/docs/current/notation.html | 0.421 | www.postgresql.org/docs/18/notation.html | 0.421 | www.postgresql.org/docs/17/notation.html | 0.415 |


**Q32: What is the role of an administrator in PostgreSQL?**
*(expects URL containing: `notation.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/admin.html | 0.593 | www.postgresql.org/docs/current/app-postgres.html | 0.541 | www.postgresql.org/docs/current/admin.html | 0.527 |
| crawl4ai | #34 | www.postgresql.org/about/ | 0.592 | www.postgresql.org/docs/18/admin.html | 0.561 | www.postgresql.org/docs/current/admin.html | 0.561 |
| crawl4ai-raw | #34 | www.postgresql.org/docs/18/admin.html | 0.561 | www.postgresql.org/docs/current/admin.html | 0.561 | www.postgresql.org/docs/17/admin.html | 0.561 |
| scrapy+md | miss | www.postgresql.org/docs/current/database-roles.htm | 0.548 | www.postgresql.org/docs/8.0/admin.html | 0.546 | www.postgresql.org/docs/9.0/user-manag.html | 0.542 |
| crawlee | miss | www.postgresql.org/docs/17/admin.html | 0.555 | www.postgresql.org/docs/current/admin.html | 0.551 | www.postgresql.org/docs/18/admin.html | 0.551 |
| colly+md | miss | www.postgresql.org/docs/17/admin.html | 0.555 | www.postgresql.org/docs/current/admin.html | 0.551 | www.postgresql.org/docs/18/admin.html | 0.551 |
| playwright | miss | www.postgresql.org/docs/17/admin.html | 0.555 | www.postgresql.org/docs/current/admin.html | 0.551 | www.postgresql.org/docs/18/admin.html | 0.551 |


**Q33: What topics are covered in the Server Administration section?**
*(expects URL containing: `admin.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/admin.html | 0.555 | www.postgresql.org/docs/current/admin.html | 0.536 | www.postgresql.org/docs/current/admin.html | 0.497 |
| crawl4ai | #1 | www.postgresql.org/docs/current/admin.html | 0.533 | www.postgresql.org/docs/18/admin.html | 0.533 | www.postgresql.org/docs/17/admin.html | 0.524 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/admin.html | 0.533 | www.postgresql.org/docs/18/admin.html | 0.533 | www.postgresql.org/docs/17/admin.html | 0.523 |
| scrapy+md | #1 | www.postgresql.org/docs/8.0/admin.html | 0.490 | www.postgresql.org/docs/8.0/admin.html | 0.453 | www.postgresql.org/docs/9.0/server-programming.htm | 0.409 |
| crawlee | #1 | www.postgresql.org/docs/current/admin.html | 0.536 | www.postgresql.org/docs/18/admin.html | 0.536 | www.postgresql.org/docs/17/admin.html | 0.535 |
| colly+md | #1 | www.postgresql.org/docs/18/admin.html | 0.536 | www.postgresql.org/docs/current/admin.html | 0.536 | www.postgresql.org/docs/17/admin.html | 0.535 |
| playwright | #1 | www.postgresql.org/docs/18/admin.html | 0.536 | www.postgresql.org/docs/current/admin.html | 0.536 | www.postgresql.org/docs/17/admin.html | 0.535 |


**Q34: Who should be familiar with the topics in the Server Administration part?**
*(expects URL containing: `admin.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/admin.html | 0.534 | www.postgresql.org/docs/current/admin.html | 0.485 | www.postgresql.org/docs/current/admin.html | 0.459 |
| crawl4ai | #1 | www.postgresql.org/docs/17/admin.html | 0.482 | www.postgresql.org/docs/18/admin.html | 0.482 | www.postgresql.org/docs/current/admin.html | 0.482 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/admin.html | 0.482 | www.postgresql.org/docs/18/admin.html | 0.482 | www.postgresql.org/docs/current/admin.html | 0.482 |
| scrapy+md | #1 | www.postgresql.org/docs/8.0/admin.html | 0.474 | www.postgresql.org/docs/8.0/admin.html | 0.376 | www.postgresql.org/docs/9.0/server-programming.htm | 0.342 |
| crawlee | #1 | www.postgresql.org/docs/17/admin.html | 0.496 | www.postgresql.org/docs/18/admin.html | 0.494 | www.postgresql.org/docs/current/admin.html | 0.494 |
| colly+md | #1 | www.postgresql.org/docs/17/admin.html | 0.496 | www.postgresql.org/docs/18/admin.html | 0.494 | www.postgresql.org/docs/current/admin.html | 0.494 |
| playwright | #1 | www.postgresql.org/docs/17/admin.html | 0.496 | www.postgresql.org/docs/18/admin.html | 0.494 | www.postgresql.org/docs/current/admin.html | 0.494 |


**Q35: How do I install PL/Python in a PostgreSQL database?**
*(expects URL containing: `plpython.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/plpython.html | 0.593 | www.postgresql.org/docs/current/xplang.html | 0.570 | www.postgresql.org/docs/current/plpgsql-overview.h | 0.556 |
| crawl4ai | #1 | www.postgresql.org/docs/17/plpython.html | 0.654 | www.postgresql.org/docs/current/plpython.html | 0.654 | www.postgresql.org/docs/18/plpython.html | 0.654 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/plpython.html | 0.654 | www.postgresql.org/docs/18/plpython.html | 0.654 | www.postgresql.org/docs/current/plpython.html | 0.654 |
| scrapy+md | miss | www.postgresql.org/docs/9.1/plpython-python23.html | 0.635 | www.postgresql.org/docs/9.1/plpython-python23.html | 0.631 | www.postgresql.org/docs/9.1/install-procedure.html | 0.519 |
| crawlee | #1 | www.postgresql.org/docs/current/plpython.html | 0.647 | www.postgresql.org/docs/18/plpython.html | 0.647 | www.postgresql.org/docs/18/plpython.html | 0.570 |
| colly+md | #1 | www.postgresql.org/docs/18/plpython.html | 0.647 | www.postgresql.org/docs/current/plpython.html | 0.647 | www.postgresql.org/docs/18/plpython.html | 0.570 |
| playwright | #1 | www.postgresql.org/docs/current/plpython.html | 0.647 | www.postgresql.org/docs/18/plpython.html | 0.647 | www.postgresql.org/docs/17/plpython.html | 0.647 |


**Q36: What does it mean that PL/Python is an 'untrusted' language?**
*(expects URL containing: `plpython.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/plpython.html | 0.520 | www.postgresql.org/docs/current/xplang-install.htm | 0.511 | www.postgresql.org/docs/current/pltcl-overview.htm | 0.460 |
| crawl4ai | #1 | www.postgresql.org/docs/current/plpython.html | 0.568 | www.postgresql.org/docs/18/plpython.html | 0.568 | www.postgresql.org/docs/17/plpython.html | 0.568 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/plpython.html | 0.568 | www.postgresql.org/docs/current/plpython.html | 0.568 | www.postgresql.org/docs/17/plpython.html | 0.568 |
| scrapy+md | miss | www.postgresql.org/docs/9.1/plpython-python23.html | 0.535 | www.postgresql.org/docs/9.1/plpython-python23.html | 0.497 | www.postgresql.org/docs/9.0/server-programming.htm | 0.348 |
| crawlee | #1 | www.postgresql.org/docs/current/plpython.html | 0.559 | www.postgresql.org/docs/18/plpython.html | 0.559 | www.postgresql.org/docs/current/plpython.html | 0.544 |
| colly+md | #1 | www.postgresql.org/docs/18/plpython.html | 0.559 | www.postgresql.org/docs/current/plpython.html | 0.559 | www.postgresql.org/docs/18/plpython.html | 0.544 |
| playwright | #1 | www.postgresql.org/docs/17/plpython.html | 0.559 | www.postgresql.org/docs/current/plpython.html | 0.559 | www.postgresql.org/docs/18/plpython.html | 0.559 |


**Q37: What information do I need to provide to sign up for a free community account?**
*(expects URL containing: `signup`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/libpq-pgpass.html | 0.272 | www.postgresql.org/docs/current/runtime-config.htm | 0.267 | www.postgresql.org/docs/current/runtime-config-log | 0.245 |
| crawl4ai | #1 | www.postgresql.org/account/signup/ | 0.353 | www.postgresql.org/account/products/new/ | 0.301 | www.postgresql.org/account/ | 0.301 |
| crawl4ai-raw | #1 | www.postgresql.org/account/signup/ | 0.353 | www.postgresql.org/account/ | 0.301 | www.postgresql.org/account/comments/new/18/index.h | 0.301 |
| scrapy+md | miss | www.postgresql.org/about/policies/npos/ | 0.245 | www.postgresql.org/about/policies/npos/ | 0.236 | www.postgresql.org/about/policies/coc/ | 0.233 |
| crawlee | #1 | www.postgresql.org/account/signup/ | 0.438 | www.postgresql.org/account/events/new/ | 0.291 | www.postgresql.org/account/submitbug/ | 0.291 |
| colly+md | #1 | www.postgresql.org/account/signup/ | 0.438 | www.postgresql.org/account/login/?next=/account/su | 0.291 | www.postgresql.org/account/login/?next=/account/ | 0.291 |
| playwright | #1 | www.postgresql.org/account/signup/ | 0.438 | www.postgresql.org/account/products/new/ | 0.291 | www.postgresql.org/account/ | 0.291 |


**Q38: What happens after I enter my email address during the signup process?**
*(expects URL containing: `signup`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/protocol-flow.html | 0.226 | www.postgresql.org/docs/current/event-trigger-data | 0.220 | www.postgresql.org/docs/current/protocol-flow.html | 0.219 |
| crawl4ai | #1 | www.postgresql.org/account/signup/ | 0.246 | www.postgresql.org/community/contributors/ | 0.219 | www.postgresql.org/community/contributors/ | 0.217 |
| crawl4ai-raw | #1 | www.postgresql.org/account/signup/ | 0.246 | www.postgresql.org/community/contributors/ | 0.219 | www.postgresql.org/community/contributors/ | 0.217 |
| scrapy+md | miss | www.postgresql.org/docs/current/sspi-auth.html | 0.205 | www.postgresql.org/docs/current/sql-createrole.htm | 0.190 | www.postgresql.org/docs/8.3/app-createuser.html | 0.171 |
| crawlee | #1 | www.postgresql.org/account/signup/ | 0.316 | www.postgresql.org/community/contributors/ | 0.228 | www.postgresql.org/account/reset/ | 0.218 |
| colly+md | #1 | www.postgresql.org/account/signup/ | 0.316 | www.postgresql.org/community/contributors/ | 0.228 | www.postgresql.org/account/reset/ | 0.218 |
| playwright | #1 | www.postgresql.org/account/signup/ | 0.316 | www.postgresql.org/community/contributors/ | 0.228 | www.postgresql.org/account/reset/ | 0.218 |


**Q39: What is the formal name of the SQL standard?**
*(expects URL containing: `features.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/glossary.html | 0.504 | www.postgresql.org/docs/current/sql.html | 0.491 | www.postgresql.org/docs/current/sql.html | 0.478 |
| crawl4ai | #1 | www.postgresql.org/docs/current/features.html | 0.578 | www.postgresql.org/docs/18/features.html | 0.578 | www.postgresql.org/docs/current/glossary.html | 0.500 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/features.html | 0.578 | www.postgresql.org/docs/current/features.html | 0.578 | www.postgresql.org/docs/current/glossary.html | 0.500 |
| scrapy+md | miss | www.postgresql.org/docs/7.1/biblio.html | 0.452 | www.postgresql.org/docs/7.3/functions.html | 0.449 | www.postgresql.org/docs/current/biblio.html | 0.448 |
| crawlee | #1 | www.postgresql.org/docs/18/features.html | 0.588 | www.postgresql.org/docs/current/features.html | 0.588 | www.postgresql.org/docs/current/glossary.html | 0.504 |
| colly+md | #1 | www.postgresql.org/docs/current/features.html | 0.588 | www.postgresql.org/docs/current/glossary.html | 0.504 | www.postgresql.org/docs/current/sql.html | 0.469 |
| playwright | #1 | www.postgresql.org/docs/18/features.html | 0.588 | www.postgresql.org/docs/current/features.html | 0.588 | www.postgresql.org/docs/18/glossary.html | 0.504 |


**Q40: How many mandatory features does PostgreSQL conform to for full Core conformance?**
*(expects URL containing: `features.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/wal-reliability.ht | 0.527 | www.postgresql.org/docs/current/sql-createtable.ht | 0.519 | www.postgresql.org/docs/current/sql-select.html | 0.515 |
| crawl4ai | #1 | www.postgresql.org/docs/current/features.html | 0.662 | www.postgresql.org/docs/18/features.html | 0.662 | www.postgresql.org/docs/18/features.html | 0.658 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/features.html | 0.662 | www.postgresql.org/docs/18/features.html | 0.662 | www.postgresql.org/docs/18/features.html | 0.658 |
| scrapy+md | miss | www.postgresql.org/docs/8.0/sql-createtable.html | 0.540 | www.postgresql.org/docs/7.4/sql-createtable.html | 0.536 | www.postgresql.org/about/policies/npos/ | 0.528 |
| crawlee | #2 | www.postgresql.org/about/ | 0.675 | www.postgresql.org/docs/current/features.html | 0.662 | www.postgresql.org/docs/18/features.html | 0.662 |
| colly+md | #2 | www.postgresql.org/about/ | 0.675 | www.postgresql.org/docs/current/features.html | 0.662 | www.postgresql.org/docs/current/features.html | 0.657 |
| playwright | #2 | www.postgresql.org/about/ | 0.675 | www.postgresql.org/docs/current/features.html | 0.662 | www.postgresql.org/docs/18/features.html | 0.662 |


**Q41: How do I install PL/Python in a PostgreSQL database?**
*(expects URL containing: `plpython.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/plpython.html | 0.593 | www.postgresql.org/docs/current/xplang.html | 0.570 | www.postgresql.org/docs/current/plpgsql-overview.h | 0.556 |
| crawl4ai | #1 | www.postgresql.org/docs/17/plpython.html | 0.654 | www.postgresql.org/docs/current/plpython.html | 0.654 | www.postgresql.org/docs/18/plpython.html | 0.654 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/plpython.html | 0.654 | www.postgresql.org/docs/18/plpython.html | 0.654 | www.postgresql.org/docs/current/plpython.html | 0.654 |
| scrapy+md | miss | www.postgresql.org/docs/9.1/plpython-python23.html | 0.635 | www.postgresql.org/docs/9.1/plpython-python23.html | 0.631 | www.postgresql.org/docs/9.1/install-procedure.html | 0.519 |
| crawlee | #1 | www.postgresql.org/docs/current/plpython.html | 0.647 | www.postgresql.org/docs/18/plpython.html | 0.647 | www.postgresql.org/docs/18/plpython.html | 0.570 |
| colly+md | #1 | www.postgresql.org/docs/18/plpython.html | 0.647 | www.postgresql.org/docs/current/plpython.html | 0.647 | www.postgresql.org/docs/18/plpython.html | 0.570 |
| playwright | #1 | www.postgresql.org/docs/current/plpython.html | 0.647 | www.postgresql.org/docs/18/plpython.html | 0.647 | www.postgresql.org/docs/17/plpython.html | 0.647 |


**Q42: What does it mean that PL/Python is an 'untrusted' language?**
*(expects URL containing: `plpython.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/plpython.html | 0.520 | www.postgresql.org/docs/current/xplang-install.htm | 0.511 | www.postgresql.org/docs/current/pltcl-overview.htm | 0.460 |
| crawl4ai | #1 | www.postgresql.org/docs/current/plpython.html | 0.568 | www.postgresql.org/docs/18/plpython.html | 0.568 | www.postgresql.org/docs/17/plpython.html | 0.568 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/plpython.html | 0.568 | www.postgresql.org/docs/current/plpython.html | 0.568 | www.postgresql.org/docs/17/plpython.html | 0.568 |
| scrapy+md | miss | www.postgresql.org/docs/9.1/plpython-python23.html | 0.535 | www.postgresql.org/docs/9.1/plpython-python23.html | 0.497 | www.postgresql.org/docs/9.0/server-programming.htm | 0.348 |
| crawlee | #1 | www.postgresql.org/docs/current/plpython.html | 0.559 | www.postgresql.org/docs/18/plpython.html | 0.559 | www.postgresql.org/docs/current/plpython.html | 0.544 |
| colly+md | #1 | www.postgresql.org/docs/18/plpython.html | 0.559 | www.postgresql.org/docs/current/plpython.html | 0.559 | www.postgresql.org/docs/18/plpython.html | 0.544 |
| playwright | #1 | www.postgresql.org/docs/17/plpython.html | 0.559 | www.postgresql.org/docs/current/plpython.html | 0.559 | www.postgresql.org/docs/18/plpython.html | 0.559 |


**Q43: What is the signature of a table sampling method function in PostgreSQL?**
*(expects URL containing: `tablesample-method.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/sql-select.html | 0.584 | www.postgresql.org/docs/current/sql-select.html | 0.558 | www.postgresql.org/docs/current/xfunc-sql.html | 0.508 |
| crawl4ai | #1 | www.postgresql.org/docs/current/tablesample-method | 0.667 | www.postgresql.org/docs/18/tablesample-method.html | 0.667 | www.postgresql.org/docs/18/tablesample-method.html | 0.591 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/tablesample-method | 0.667 | www.postgresql.org/docs/18/tablesample-method.html | 0.667 | www.postgresql.org/docs/current/tablesample-method | 0.591 |
| scrapy+md | miss | www.postgresql.org/docs/9.6/tsm-system-rows.html | 0.535 | www.postgresql.org/docs/9.5/tsm-system-rows.html | 0.529 | www.postgresql.org/docs/9.6/tsm-system-time.html | 0.522 |
| crawlee | #1 | www.postgresql.org/docs/18/tablesample-method.html | 0.714 | www.postgresql.org/docs/current/tablesample-method | 0.714 | www.postgresql.org/docs/18/tablesample-method.html | 0.682 |
| colly+md | #1 | www.postgresql.org/docs/current/tablesample-method | 0.714 | www.postgresql.org/docs/current/tablesample-method | 0.682 | www.postgresql.org/docs/current/tablesample-method | 0.616 |
| playwright | #1 | www.postgresql.org/docs/18/tablesample-method.html | 0.714 | www.postgresql.org/docs/current/tablesample-method | 0.714 | www.postgresql.org/docs/current/tablesample-method | 0.682 |


**Q44: What does the `repeatable_across_queries` field in the TsmRoutine struct indicate?**
*(expects URL containing: `tablesample-method.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/glossary.html | 0.415 | www.postgresql.org/docs/current/glossary.html | 0.398 | www.postgresql.org/docs/current/textsearch-feature | 0.387 |
| crawl4ai | #1 | www.postgresql.org/docs/current/tablesample-method | 0.599 | www.postgresql.org/docs/18/tablesample-method.html | 0.599 | www.postgresql.org/docs/current/glossary.html | 0.415 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/tablesample-method.html | 0.599 | www.postgresql.org/docs/current/tablesample-method | 0.599 | www.postgresql.org/docs/current/glossary.html | 0.415 |
| scrapy+md | miss | www.postgresql.org/docs/14/tsm-system-time.html | 0.390 | www.postgresql.org/docs/15/tsm-system-time.html | 0.389 | www.postgresql.org/docs/13/tsm-system-time.html | 0.386 |
| crawlee | #1 | www.postgresql.org/docs/18/tablesample-method.html | 0.484 | www.postgresql.org/docs/current/tablesample-method | 0.483 | www.postgresql.org/docs/18/glossary.html | 0.415 |
| colly+md | #1 | www.postgresql.org/docs/current/tablesample-method | 0.483 | www.postgresql.org/docs/current/glossary.html | 0.415 | www.postgresql.org/docs/current/tablesample-method | 0.414 |
| playwright | #1 | www.postgresql.org/docs/current/tablesample-method | 0.483 | www.postgresql.org/docs/18/tablesample-method.html | 0.483 | www.postgresql.org/docs/18/glossary.html | 0.415 |


**Q45: What should be included in every bug report?**
*(expects URL containing: `bug-reporting.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/runtime-config-log | 0.414 | www.postgresql.org/docs/current/error-style-guide. | 0.410 | www.postgresql.org/docs/current/admin.html | 0.339 |
| crawl4ai | #1 | www.postgresql.org/docs/17/bug-reporting.html | 0.641 | www.postgresql.org/docs/18/bug-reporting.html | 0.641 | www.postgresql.org/docs/current/bug-reporting.html | 0.641 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/bug-reporting.html | 0.641 | www.postgresql.org/docs/17/bug-reporting.html | 0.641 | www.postgresql.org/docs/18/bug-reporting.html | 0.641 |
| scrapy+md | miss | www.postgresql.org/docs/7.3/doc-style.html | 0.373 | www.postgresql.org/about/policies/coc/ | 0.364 | www.postgresql.org/docs/7.3/doc-style.html | 0.360 |
| crawlee | #1 | www.postgresql.org/docs/current/bug-reporting.html | 0.616 | www.postgresql.org/docs/17/bug-reporting.html | 0.616 | www.postgresql.org/docs/18/bug-reporting.html | 0.616 |
| colly+md | #1 | www.postgresql.org/docs/16/bug-reporting.html | 0.616 | www.postgresql.org/docs/18/bug-reporting.html | 0.616 | www.postgresql.org/docs/17/bug-reporting.html | 0.616 |
| playwright | #1 | www.postgresql.org/docs/18/bug-reporting.html | 0.616 | www.postgresql.org/docs/current/bug-reporting.html | 0.616 | www.postgresql.org/docs/17/bug-reporting.html | 0.616 |


**Q46: Where should I send bug reports for PostgreSQL?**
*(expects URL containing: `bug-reporting.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/runtime-config-rep | 0.515 | www.postgresql.org/docs/current/reference-server.h | 0.503 | www.postgresql.org/docs/current/runtime-config-fil | 0.488 |
| crawl4ai | #1 | www.postgresql.org/docs/17/bug-reporting.html | 0.722 | www.postgresql.org/docs/18/bug-reporting.html | 0.722 | www.postgresql.org/docs/current/bug-reporting.html | 0.722 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/bug-reporting.html | 0.722 | www.postgresql.org/docs/18/bug-reporting.html | 0.722 | www.postgresql.org/docs/current/bug-reporting.html | 0.722 |
| scrapy+md | miss | www.postgresql.org/docs/9.2/runtime-config-logging | 0.543 | www.postgresql.org/about/contact/ | 0.515 | www.postgresql.org/docs/7.3/release-0-02.html | 0.506 |
| crawlee | #1 | www.postgresql.org/docs/17/bug-reporting.html | 0.687 | www.postgresql.org/docs/18/bug-reporting.html | 0.687 | www.postgresql.org/docs/current/bug-reporting.html | 0.687 |
| colly+md | #1 | www.postgresql.org/docs/16/bug-reporting.html | 0.687 | www.postgresql.org/docs/18/bug-reporting.html | 0.687 | www.postgresql.org/docs/17/bug-reporting.html | 0.687 |
| playwright | #1 | www.postgresql.org/docs/current/bug-reporting.html | 0.687 | www.postgresql.org/docs/18/bug-reporting.html | 0.687 | www.postgresql.org/docs/17/bug-reporting.html | 0.687 |


</details>

## propublica

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| playwright | 66% (37/56) | 77% (43/56) | 82% (46/56) | 88% (49/56) | 93% (52/56) | 0.731 | 2197 | 150 |
| crawl4ai-raw | 64% (36/56) | 70% (39/56) | 73% (41/56) | 82% (46/56) | 89% (50/56) | 0.694 | 1563 | 149 |
| crawl4ai | 64% (36/56) | 70% (39/56) | 73% (41/56) | 82% (46/56) | 89% (50/56) | 0.694 | 1563 | 149 |
| crawlee | 62% (35/56) | 71% (40/56) | 79% (44/56) | 86% (48/56) | 89% (50/56) | 0.693 | 2099 | 150 |
| colly+md | 18% (10/56) | 23% (13/56) | 25% (14/56) | 25% (14/56) | 29% (16/56) | 0.212 | 2196 | 150 |
| scrapy+md | 7% (4/56) | 7% (4/56) | 7% (4/56) | 7% (4/56) | 7% (4/56) | 0.071 | 1396 | 146 |
| markcrawl | 2% (1/56) | 2% (1/56) | 2% (1/56) | 2% (1/56) | 4% (2/56) | 0.019 | 1264 | 150 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for propublica</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What are some featured posts by Brandi Kellam?**
*(expects URL containing: `brandi-kellam`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/year-in-photos-illustra | 0.332 | www.propublica.org/article/year-in-photos-illustra | 0.319 | www.propublica.org/article/propublica-investigatio | 0.317 |
| crawl4ai | #31 | www.propublica.org/article/family-photos-of-shoe-l | 0.450 | www.propublica.org/people/sarahbeth-maney | 0.439 | www.propublica.org/people/jennifer-berry-hawes | 0.401 |
| crawl4ai-raw | #31 | www.propublica.org/article/family-photos-of-shoe-l | 0.450 | www.propublica.org/people/sarahbeth-maney | 0.439 | www.propublica.org/people/jennifer-berry-hawes | 0.401 |
| scrapy+md | miss | www.propublica.org/people/sarahbeth-maney | 0.432 | www.propublica.org/people/agnes-chang | 0.420 | www.propublica.org/people/ruth-talbot/page/3 | 0.412 |
| crawlee | #5 | www.propublica.org/article/why-destruction-of-a-bl | 0.454 | www.propublica.org/people/sarahbeth-maney | 0.432 | www.propublica.org/people/mollie-simon | 0.421 |
| colly+md | miss | www.propublica.org/people/mollie-simon | 0.428 | www.propublica.org/people/tony-briscoe | 0.419 | www.propublica.org/people/bethany-mollenkof | 0.407 |
| playwright | #3 | www.propublica.org/people/sarahbeth-maney | 0.432 | www.propublica.org/people/mollie-simon | 0.421 | www.propublica.org/people/brandi-kellam | 0.409 |


**Q2: What is the title of the article published on March 14, 2024?**
*(expects URL containing: `brandi-kellam`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-most-read-st | 0.428 | www.propublica.org/article/propublica-investigatio | 0.418 | www.propublica.org/article/propublica-most-read-st | 0.407 |
| crawl4ai | miss | www.propublica.org/archive | 0.444 | www.propublica.org/archive | 0.437 | www.propublica.org/topics/health-care | 0.429 |
| crawl4ai-raw | miss | www.propublica.org/archive | 0.444 | www.propublica.org/archive | 0.437 | www.propublica.org/topics/health-care | 0.429 |
| scrapy+md | miss | www.propublica.org/people/sarahbeth-maney | 0.490 | www.propublica.org/topics/health-insurance | 0.455 | www.propublica.org/topics/health-insurance | 0.448 |
| crawlee | miss | www.propublica.org/newsapps | 0.481 | www.propublica.org/topics/health-care | 0.462 | www.propublica.org/newsapps | 0.461 |
| colly+md | miss | www.propublica.org/newsapps | 0.481 | www.propublica.org/newsapps | 0.461 | www.propublica.org/newsapps | 0.450 |
| playwright | miss | www.propublica.org/newsapps | 0.481 | www.propublica.org/topics/health-care | 0.462 | www.propublica.org/newsapps | 0.461 |


**Q3: What is the main focus of ProPublica's criminal justice coverage?**
*(expects URL containing: `criminal-justice`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-most-read-st | 0.500 | www.propublica.org/article/propublica-investigatio | 0.491 | www.propublica.org/article/propublica-investigatio | 0.470 |
| crawl4ai | #1 | www.propublica.org/topics/criminal-justice | 0.607 | www.propublica.org/about | 0.574 | www.propublica.org/ | 0.561 |
| crawl4ai-raw | #1 | www.propublica.org/topics/criminal-justice | 0.607 | www.propublica.org/about | 0.574 | www.propublica.org/ | 0.561 |
| scrapy+md | miss | www.propublica.org/reports/page/2 | 0.536 | www.propublica.org/article/how-does-journalism-wor | 0.535 | www.propublica.org/media-center | 0.526 |
| crawlee | #1 | www.propublica.org/topics/criminal-justice | 0.634 | www.propublica.org/series/busted | 0.592 | www.propublica.org/series/nuisance-abatement | 0.584 |
| colly+md | miss | www.propublica.org/article/joseph-schwartz-trump-p | 0.593 | www.propublica.org/article/columbia-university-rob | 0.586 | www.propublica.org/article/nike-jobs-indonesia-liv | 0.560 |
| playwright | #1 | www.propublica.org/topics/criminal-justice | 0.634 | www.propublica.org/series/busted | 0.592 | www.propublica.org/series/nuisance-abatement | 0.584 |


**Q4: What issues are highlighted in the featured stories on the criminal justice page?**
*(expects URL containing: `criminal-justice`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/oklahoma-survivors-act- | 0.491 | www.propublica.org/article/immigration-military-tr | 0.478 | www.propublica.org/article/why-local-state-police- | 0.478 |
| crawl4ai | #1 | www.propublica.org/topics/criminal-justice | 0.607 | www.propublica.org/topics/criminal-justice | 0.603 | www.propublica.org/topics/criminal-justice | 0.590 |
| crawl4ai-raw | #1 | www.propublica.org/topics/criminal-justice | 0.607 | www.propublica.org/topics/criminal-justice | 0.603 | www.propublica.org/topics/criminal-justice | 0.590 |
| scrapy+md | miss | www.propublica.org/article/when-it-comes-to-rape-j | 0.519 | www.propublica.org/topics/courts | 0.511 | www.propublica.org/article/how-does-journalism-wor | 0.503 |
| crawlee | #1 | www.propublica.org/topics/criminal-justice | 0.618 | www.propublica.org/topics/criminal-justice | 0.591 | www.propublica.org/local-reporting-network | 0.571 |
| colly+md | miss | www.propublica.org/article/joseph-schwartz-trump-p | 0.601 | www.propublica.org/article/louisiana-parole-drop-j | 0.596 | www.propublica.org/article/columbia-university-rob | 0.587 |
| playwright | #1 | www.propublica.org/topics/criminal-justice | 0.618 | www.propublica.org/topics/criminal-justice | 0.591 | www.propublica.org/local-reporting-network | 0.571 |


**Q5: What is Francesca D’Annunzio's role at ProPublica?**
*(expects URL containing: `francesca-dannunzio`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-reaching-out | 0.411 | www.propublica.org/article/propublica-investigativ | 0.410 | www.propublica.org/article/year-in-photos-illustra | 0.398 |
| crawl4ai | #49 | www.propublica.org/staff | 0.599 | www.propublica.org/staff | 0.561 | www.propublica.org/staff | 0.559 |
| crawl4ai-raw | #48 | www.propublica.org/staff | 0.599 | www.propublica.org/staff | 0.561 | www.propublica.org/staff | 0.559 |
| scrapy+md | miss | www.propublica.org/diversity | 0.487 | www.propublica.org/article/how-we-compiled-trump-t | 0.486 | www.propublica.org/people/bernice-yeung | 0.486 |
| crawlee | #7 | www.propublica.org/staff | 0.573 | www.propublica.org/staff | 0.554 | www.propublica.org/press-releases | 0.548 |
| colly+md | miss | www.propublica.org/staff | 0.573 | www.propublica.org/staff | 0.554 | www.propublica.org/staff | 0.542 |
| playwright | #8 | www.propublica.org/staff | 0.573 | www.propublica.org/staff | 0.554 | www.propublica.org/press-releases | 0.548 |


**Q6: What is the topic of Francesca D’Annunzio's featured post from May 1, 2026?**
*(expects URL containing: `francesca-dannunzio`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/year-in-photos-illustra | 0.296 | www.propublica.org/article/ice-dilley-maria-antoni | 0.294 | www.propublica.org/article/fda-generic-drug-equiva | 0.288 |
| crawl4ai | #1 | www.propublica.org/people/francesca-dannunzio | 0.343 | www.propublica.org/people/sarahbeth-maney | 0.341 | www.propublica.org/archive | 0.337 |
| crawl4ai-raw | #1 | www.propublica.org/people/francesca-dannunzio | 0.343 | www.propublica.org/people/sarahbeth-maney | 0.341 | www.propublica.org/archive | 0.337 |
| scrapy+md | miss | www.propublica.org/people/sarahbeth-maney | 0.367 | www.propublica.org/people/nicole-santa-cruz | 0.345 | www.propublica.org/topics/education | 0.337 |
| crawlee | #1 | www.propublica.org/people/francesca-dannunzio | 0.429 | www.propublica.org/people/abrahm-lustgarten | 0.358 | www.propublica.org/people/liz-moughon | 0.352 |
| colly+md | miss | www.propublica.org/people/abrahm-lustgarten | 0.358 | www.propublica.org/people/abrahm-lustgarten/page/3 | 0.358 | www.propublica.org/topics/education | 0.337 |
| playwright | #1 | www.propublica.org/people/francesca-dannunzio | 0.428 | www.propublica.org/people/abrahm-lustgarten | 0.358 | www.propublica.org/people/liz-moughon | 0.352 |


**Q7: What states does the ProPublica Midwest team cover?**
*(expects URL containing: `midwest`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-most-read-st | 0.512 | www.propublica.org/article/trump-familia-deportaci | 0.475 | www.propublica.org/article/propublica-reaching-out | 0.464 |
| crawl4ai | #2 | www.propublica.org/local-initiatives | 0.739 | www.propublica.org/midwest | 0.673 | www.propublica.org/midwest | 0.631 |
| crawl4ai-raw | #2 | www.propublica.org/local-initiatives | 0.739 | www.propublica.org/midwest | 0.673 | www.propublica.org/midwest | 0.631 |
| scrapy+md | miss | www.propublica.org/reports/page/2 | 0.580 | www.propublica.org/article/how-does-journalism-wor | 0.554 | www.propublica.org/media-center | 0.554 |
| crawlee | #2 | www.propublica.org/local-initiatives | 0.727 | www.propublica.org/midwest | 0.639 | www.propublica.org/advertising | 0.626 |
| colly+md | #2 | www.propublica.org/article/nike-jobs-indonesia-liv | 0.623 | www.propublica.org/midwest | 0.621 | www.propublica.org/midwest | 0.618 |
| playwright | #2 | www.propublica.org/local-initiatives | 0.727 | www.propublica.org/midwest | 0.639 | www.propublica.org/advertising | 0.626 |


**Q8: Who is the Midwest Editor for ProPublica?**
*(expects URL containing: `midwest`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigativ | 0.503 | www.propublica.org/article/propublica-reaching-out | 0.467 | www.propublica.org/article/propublica-investigativ | 0.465 |
| crawl4ai | #4 | www.propublica.org/local-initiatives | 0.660 | www.propublica.org/press-releases | 0.650 | www.propublica.org/staff | 0.635 |
| crawl4ai-raw | #4 | www.propublica.org/local-initiatives | 0.660 | www.propublica.org/press-releases | 0.650 | www.propublica.org/staff | 0.635 |
| scrapy+md | miss | www.propublica.org/getinvolved/help-propublica-rep | 0.540 | www.propublica.org/reports/page/2 | 0.528 | www.propublica.org/people/jason-grotto | 0.525 |
| crawlee | #11 | www.propublica.org/local-initiatives | 0.647 | www.propublica.org/staff | 0.644 | www.propublica.org/press-releases | 0.626 |
| colly+md | #5 | www.propublica.org/staff | 0.637 | www.propublica.org/staff | 0.610 | www.propublica.org/staff | 0.598 |
| playwright | #11 | www.propublica.org/local-initiatives | 0.647 | www.propublica.org/staff | 0.644 | www.propublica.org/press-releases | 0.626 |


**Q9: What happened to A.L. Martin High School during desegregation in Thomasville?**
*(expects URL containing: `thomasville-alabama-segregation-academies`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/trump-education-departm | 0.398 | www.propublica.org/article/trump-education-departm | 0.395 | www.propublica.org/article/thomas-albus-fulton-cou | 0.388 |
| crawl4ai | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.758 | www.propublica.org/article/thomasville-alabama-seg | 0.731 | www.propublica.org/article/thomasville-alabama-seg | 0.680 |
| crawl4ai-raw | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.758 | www.propublica.org/article/thomasville-alabama-seg | 0.731 | www.propublica.org/article/thomasville-alabama-seg | 0.680 |
| scrapy+md | miss | www.propublica.org/topics/education | 0.279 | www.propublica.org/topics/education | 0.279 | www.propublica.org/article/has-the-moment-for-envi | 0.275 |
| crawlee | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.731 | www.propublica.org/article/thomasville-alabama-seg | 0.684 | www.propublica.org/article/thomasville-alabama-seg | 0.682 |
| colly+md | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.731 | www.propublica.org/article/thomasville-alabama-seg | 0.684 | www.propublica.org/article/thomasville-alabama-seg | 0.682 |
| playwright | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.731 | www.propublica.org/article/thomasville-alabama-seg | 0.684 | www.propublica.org/article/thomasville-alabama-seg | 0.682 |


**Q10: How did Black students in Thomasville respond to the conditions at Thomasville High after the merger?**
*(expects URL containing: `thomasville-alabama-segregation-academies`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/trump-education-departm | 0.449 | www.propublica.org/article/trump-education-departm | 0.429 | www.propublica.org/article/trump-education-departm | 0.372 |
| crawl4ai | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.709 | www.propublica.org/article/thomasville-alabama-seg | 0.679 | www.propublica.org/article/thomasville-alabama-seg | 0.618 |
| crawl4ai-raw | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.709 | www.propublica.org/article/thomasville-alabama-seg | 0.679 | www.propublica.org/article/thomasville-alabama-seg | 0.618 |
| scrapy+md | miss | www.propublica.org/article/north-carolina-legislat | 0.319 | www.propublica.org/article/north-carolina-legislat | 0.309 | www.propublica.org/topics/education | 0.298 |
| crawlee | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.679 | www.propublica.org/article/thomasville-alabama-seg | 0.644 | www.propublica.org/article/thomasville-alabama-seg | 0.632 |
| colly+md | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.679 | www.propublica.org/article/thomasville-alabama-seg | 0.644 | www.propublica.org/article/thomasville-alabama-seg | 0.632 |
| playwright | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.679 | www.propublica.org/article/thomasville-alabama-seg | 0.644 | www.propublica.org/article/thomasville-alabama-seg | 0.632 |


**Q11: What recent award did ProPublica and The Connecticut Mirror win?**
*(expects URL containing: `archive`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-most-read-st | 0.532 | www.propublica.org/article/propublica-reaching-out | 0.484 | www.propublica.org/article/propublica-investigatio | 0.476 |
| crawl4ai | miss | www.propublica.org/article/propublica-and-the-conn | 0.742 | www.propublica.org/article/propublica-and-the-conn | 0.725 | www.propublica.org/feeds/propublica/main | 0.671 |
| crawl4ai-raw | miss | www.propublica.org/article/propublica-and-the-conn | 0.742 | www.propublica.org/article/propublica-and-the-conn | 0.725 | www.propublica.org/feeds/propublica/main | 0.671 |
| scrapy+md | miss | www.propublica.org/ | 0.731 | www.propublica.org/media-center | 0.588 | www.propublica.org/steal-our-stories | 0.551 |
| crawlee | #42 | www.propublica.org/article/propublica-and-the-conn | 0.728 | www.propublica.org/ | 0.681 | www.propublica.org/feeds/propublica/main | 0.662 |
| colly+md | miss | www.propublica.org/article/propublica-and-the-conn | 0.756 | www.propublica.org/ | 0.692 | www.propublica.org/article/propublica-and-the-conn | 0.655 |
| playwright | #42 | www.propublica.org/article/propublica-and-the-conn | 0.728 | www.propublica.org/ | 0.681 | www.propublica.org/feeds/propublica/main | 0.662 |


**Q12: What is the focus of the Connecticut Senate's new towing reforms?**
*(expects URL containing: `dave-altimari`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/connecticut-towing-dmv- | 0.704 | www.propublica.org/article/connecticut-towing-dmv- | 0.684 | www.propublica.org/article/connecticut-towing-dmv- | 0.656 |
| crawl4ai | #13 | www.propublica.org/article/connecticut-towing-refo | 0.716 | www.propublica.org/feeds/propublica/main | 0.714 | www.propublica.org/feeds/propublica/main | 0.705 |
| crawl4ai-raw | #13 | www.propublica.org/article/connecticut-towing-refo | 0.716 | www.propublica.org/feeds/propublica/main | 0.714 | www.propublica.org/feeds/propublica/main | 0.705 |
| scrapy+md | miss | www.propublica.org/ | 0.451 | www.propublica.org/article/illinois-license-suspen | 0.433 | www.propublica.org/article/illinois-license-suspen | 0.431 |
| crawlee | #10 | www.propublica.org/article/connecticut-towing-refo | 0.716 | www.propublica.org/article/connecticut-towing-refo | 0.708 | www.propublica.org/feeds/propublica/main | 0.708 |
| colly+md | miss | www.propublica.org/article/connecticut-towing-refo | 0.715 | www.propublica.org/article/connecticut-towing-refo | 0.708 | www.propublica.org/article/connecticut-towing-refo | 0.696 |
| playwright | #11 | www.propublica.org/article/connecticut-towing-refo | 0.716 | www.propublica.org/article/connecticut-towing-refo | 0.708 | www.propublica.org/feeds/propublica/main | 0.708 |


**Q13: What issues are Connecticut towing companies facing with the new law?**
*(expects URL containing: `dave-altimari`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/connecticut-towing-dmv- | 0.731 | www.propublica.org/article/connecticut-towing-dmv- | 0.721 | www.propublica.org/article/connecticut-towing-dmv- | 0.693 |
| crawl4ai | #27 | www.propublica.org/article/connecticut-towing-comp | 0.739 | www.propublica.org/feeds/propublica/main | 0.713 | www.propublica.org/article/connecticut-towing-refo | 0.711 |
| crawl4ai-raw | #27 | www.propublica.org/article/connecticut-towing-comp | 0.739 | www.propublica.org/feeds/propublica/main | 0.714 | www.propublica.org/article/connecticut-towing-refo | 0.711 |
| scrapy+md | miss | www.propublica.org/ | 0.463 | www.propublica.org/article/illinois-license-suspen | 0.429 | www.propublica.org/article/illinois-license-suspen | 0.426 |
| crawlee | #23 | www.propublica.org/article/connecticut-towing-refo | 0.711 | www.propublica.org/feeds/propublica/main | 0.708 | www.propublica.org/article/connecticut-towing-comp | 0.702 |
| colly+md | miss | www.propublica.org/article/connecticut-towing-refo | 0.709 | www.propublica.org/article/connecticut-towing-refo | 0.696 | www.propublica.org/article/connecticut-towing-refo | 0.671 |
| playwright | #23 | www.propublica.org/article/connecticut-towing-refo | 0.711 | www.propublica.org/feeds/propublica/main | 0.708 | www.propublica.org/article/connecticut-towing-comp | 0.702 |


**Q14: What role did James Johnson's photographs play in the investigation of the Shoe Lane community's displacement?**
*(expects URL containing: `family-photos-of-shoe-lane-destruction`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/memphis-safe-task-force | 0.347 | www.propublica.org/article/memphis-safe-task-force | 0.344 | www.propublica.org/article/minneapolis-immigration | 0.330 |
| crawl4ai | #1 | www.propublica.org/article/family-photos-of-shoe-l | 0.623 | www.propublica.org/article/family-photos-of-shoe-l | 0.590 | www.propublica.org/article/family-photos-of-shoe-l | 0.590 |
| crawl4ai-raw | #1 | www.propublica.org/article/family-photos-of-shoe-l | 0.623 | www.propublica.org/article/family-photos-of-shoe-l | 0.590 | www.propublica.org/article/family-photos-of-shoe-l | 0.590 |
| scrapy+md | miss | www.propublica.org/article/our-journalists-stopped | 0.348 | www.propublica.org/article/how-photographers-sough | 0.347 | www.propublica.org/article/how-photographers-sough | 0.342 |
| crawlee | #1 | www.propublica.org/article/family-photos-of-shoe-l | 0.622 | www.propublica.org/article/family-photos-of-shoe-l | 0.617 | www.propublica.org/article/family-photos-of-shoe-l | 0.607 |
| colly+md | #1 | www.propublica.org/article/family-photos-of-shoe-l | 0.622 | www.propublica.org/article/family-photos-of-shoe-l | 0.617 | www.propublica.org/article/family-photos-of-shoe-l | 0.607 |
| playwright | #1 | www.propublica.org/article/family-photos-of-shoe-l | 0.622 | www.propublica.org/article/family-photos-of-shoe-l | 0.618 | www.propublica.org/article/family-photos-of-shoe-l | 0.607 |


**Q15: What actions did Christopher Newport University take regarding the Shoe Lane area in 1961?**
*(expects URL containing: `family-photos-of-shoe-lane-destruction`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/nike-factory-worker-rig | 0.361 | www.propublica.org/article/nike-factory-worker-rig | 0.355 | www.propublica.org/article/trump-education-departm | 0.320 |
| crawl4ai | #6 | www.propublica.org/article/christopher-newport-uni | 0.687 | www.propublica.org/article/christopher-newport-uni | 0.685 | www.propublica.org/article/christopher-newport-uni | 0.650 |
| crawl4ai-raw | #6 | www.propublica.org/article/christopher-newport-uni | 0.686 | www.propublica.org/article/christopher-newport-uni | 0.685 | www.propublica.org/article/christopher-newport-uni | 0.649 |
| scrapy+md | miss | www.propublica.org/article/what-happened-when-a-pu | 0.338 | www.propublica.org/article/has-the-moment-for-envi | 0.336 | www.propublica.org/article/north-carolina-legislat | 0.321 |
| crawlee | #4 | www.propublica.org/article/christopher-newport-uni | 0.674 | www.propublica.org/article/christopher-newport-uni | 0.671 | www.propublica.org/article/christopher-newport-uni | 0.638 |
| colly+md | #19 | www.propublica.org/article/how-virginia-college-ex | 0.728 | www.propublica.org/article/how-virginia-college-ex | 0.722 | www.propublica.org/article/how-virginia-college-ex | 0.696 |
| playwright | #4 | www.propublica.org/article/christopher-newport-uni | 0.674 | www.propublica.org/article/christopher-newport-uni | 0.671 | www.propublica.org/article/christopher-newport-uni | 0.638 |


**Q16: What are some featured posts by Wendi C. Thomas?**
*(expects URL containing: `wendi-thomas`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigatio | 0.325 | www.propublica.org/article/trump-education-departm | 0.299 | www.propublica.org/article/oklahoma-survivors-act- | 0.298 |
| crawl4ai | #10 | www.propublica.org/atpropublica/propublica-selects | 0.416 | www.propublica.org/people/jennifer-berry-hawes | 0.400 | www.propublica.org/people/jennifer-berry-hawes | 0.396 |
| crawl4ai-raw | #10 | www.propublica.org/atpropublica/propublica-selects | 0.416 | www.propublica.org/people/jennifer-berry-hawes | 0.400 | www.propublica.org/people/jennifer-berry-hawes | 0.396 |
| scrapy+md | miss | www.propublica.org/people/chris-alcantara | 0.393 | www.propublica.org/people/agnes-chang | 0.383 | www.propublica.org/people/sarahbeth-maney | 0.382 |
| crawlee | #2 | www.propublica.org/atpropublica/propublica-selects | 0.433 | www.propublica.org/people/wendi-thomas | 0.420 | www.propublica.org/people/jennifer-berry-hawes | 0.418 |
| colly+md | miss | www.propublica.org/people/doug-bock-clark | 0.395 | www.propublica.org/people/margaret-cheatham-willia | 0.386 | www.propublica.org/people/j-david-mcswane | 0.384 |
| playwright | #2 | www.propublica.org/atpropublica/propublica-selects | 0.433 | www.propublica.org/people/wendi-thomas | 0.420 | www.propublica.org/people/jennifer-berry-hawes | 0.418 |


**Q17: What is the date of the article about Trump's Memphis Crime Task Force?**
*(expects URL containing: `wendi-thomas`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/memphis-safe-task-force | 0.640 | www.propublica.org/article/memphis-safe-task-force | 0.611 | www.propublica.org/article/memphis-safe-task-force | 0.599 |
| crawl4ai | #3 | www.propublica.org/article/memphis-safe-task-force | 0.606 | www.propublica.org/article/memphis-safe-task-force | 0.581 | www.propublica.org/people/wendi-thomas | 0.567 |
| crawl4ai-raw | #3 | www.propublica.org/article/memphis-safe-task-force | 0.606 | www.propublica.org/article/memphis-safe-task-force | 0.581 | www.propublica.org/people/wendi-thomas | 0.567 |
| scrapy+md | miss | www.propublica.org/reports/page/2 | 0.436 | www.propublica.org/article/how-we-compiled-trump-t | 0.421 | www.propublica.org/topics/democracy | 0.417 |
| crawlee | #6 | www.propublica.org/article/memphis-safe-task-force | 0.621 | www.propublica.org/article/memphis-safe-task-force | 0.553 | www.propublica.org/article/memphis-safe-task-force | 0.553 |
| colly+md | miss | www.propublica.org/south | 0.458 | www.propublica.org/people/nick-mcmillan | 0.451 | www.propublica.org/article/sheriff-jerry-sheridan- | 0.449 |
| playwright | #6 | www.propublica.org/article/memphis-safe-task-force | 0.621 | www.propublica.org/article/memphis-safe-task-force | 0.553 | www.propublica.org/article/memphis-safe-task-force | 0.553 |


**Q18: What is the main focus of the investigation in the Juvenile Injustice series?**
*(expects URL containing: `juvenile-injustice-tennessee`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/wisconsin-corey-stingle | 0.412 | www.propublica.org/article/wisconsin-corey-stingle | 0.398 | www.propublica.org/article/trump-immigration-depor | 0.387 |
| crawl4ai | #1 | www.propublica.org/series/juvenile-injustice-tenne | 0.522 | www.propublica.org/series/schoolyard-sheriffs | 0.468 | www.propublica.org/local-reporting-network | 0.457 |
| crawl4ai-raw | #1 | www.propublica.org/series/juvenile-injustice-tenne | 0.522 | www.propublica.org/series/schoolyard-sheriffs | 0.468 | www.propublica.org/topics/criminal-justice | 0.457 |
| scrapy+md | miss | www.propublica.org/topics/education | 0.425 | www.propublica.org/topics/education | 0.414 | www.propublica.org/article/when-it-comes-to-rape-j | 0.408 |
| crawlee | #1 | www.propublica.org/series/juvenile-injustice-tenne | 0.518 | www.propublica.org/topics/criminal-justice | 0.483 | www.propublica.org/topics/criminal-justice | 0.464 |
| colly+md | #1 | www.propublica.org/series/juvenile-injustice-tenne | 0.520 | www.propublica.org/series/juvenile-injustice-tenne | 0.512 | www.propublica.org/article/black-children-were-jai | 0.496 |
| playwright | #1 | www.propublica.org/series/juvenile-injustice-tenne | 0.518 | www.propublica.org/topics/criminal-justice | 0.483 | www.propublica.org/topics/criminal-justice | 0.464 |


**Q19: What was the largest known domestic slave sale in United States history?**
*(expects URL containing: `charleston-slave-auction-historical-marker`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/trump-education-departm | 0.272 | www.propublica.org/article/memphis-safe-task-force | 0.259 | www.propublica.org/article/todd-blanche-complaint- | 0.253 |
| crawl4ai | #1 | www.propublica.org/article/charleston-slave-auctio | 0.568 | www.propublica.org/article/charleston-slave-auctio | 0.551 | www.propublica.org/article/charleston-slave-auctio | 0.549 |
| crawl4ai-raw | #1 | www.propublica.org/article/charleston-slave-auctio | 0.568 | www.propublica.org/article/charleston-slave-auctio | 0.551 | www.propublica.org/article/charleston-slave-auctio | 0.549 |
| scrapy+md | miss | www.propublica.org/article/hugo-holland-louisiana- | 0.233 | www.propublica.org/article/hugo-holland-louisiana- | 0.228 | www.propublica.org/article/bird-flu-airborne-usda- | 0.221 |
| crawlee | #1 | www.propublica.org/article/charleston-slave-auctio | 0.565 | www.propublica.org/article/charleston-slave-auctio | 0.549 | www.propublica.org/article/charleston-slave-auctio | 0.524 |
| colly+md | miss | www.propublica.org/topics/racial-justice | 0.328 | www.propublica.org/topics/racial-justice | 0.307 | www.propublica.org/article/how-virginia-college-ex | 0.283 |
| playwright | #1 | www.propublica.org/article/charleston-slave-auctio | 0.565 | www.propublica.org/article/charleston-slave-auctio | 0.549 | www.propublica.org/article/charleston-slave-auctio | 0.524 |


**Q20: Who was responsible for the discovery of the ad for the sale of 600 enslaved people?**
*(expects URL containing: `charleston-slave-auction-historical-marker`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/chicago-venezuela-immig | 0.329 | www.propublica.org/article/memphis-safe-task-force | 0.326 | www.propublica.org/article/trump-doj-colony-ridge- | 0.325 |
| crawl4ai | #1 | www.propublica.org/article/charleston-slave-auctio | 0.599 | www.propublica.org/article/charleston-slave-auctio | 0.573 | www.propublica.org/article/charleston-slave-auctio | 0.569 |
| crawl4ai-raw | #1 | www.propublica.org/article/charleston-slave-auctio | 0.599 | www.propublica.org/article/charleston-slave-auctio | 0.573 | www.propublica.org/article/charleston-slave-auctio | 0.569 |
| scrapy+md | miss | www.propublica.org/article/hugo-holland-louisiana- | 0.292 | www.propublica.org/article/trump-hud-weakening-enf | 0.282 | www.propublica.org/article/trump-hud-weakening-enf | 0.269 |
| crawlee | #1 | www.propublica.org/article/charleston-slave-auctio | 0.608 | www.propublica.org/article/charleston-slave-auctio | 0.569 | www.propublica.org/article/charleston-slave-auctio | 0.564 |
| colly+md | miss | www.propublica.org/topics/racial-justice | 0.423 | www.propublica.org/topics/racial-justice | 0.397 | www.propublica.org/article/historic-preservation-e | 0.359 |
| playwright | #1 | www.propublica.org/article/charleston-slave-auctio | 0.608 | www.propublica.org/article/charleston-slave-auctio | 0.568 | www.propublica.org/article/charleston-slave-auctio | 0.564 |


**Q21: What topics does Anna Clark cover in her reporting?**
*(expects URL containing: `anna-clark`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-reaching-out | 0.383 | www.propublica.org/article/trump-familia-deportaci | 0.358 | www.propublica.org/article/propublica-investigatio | 0.355 |
| crawl4ai | #1 | www.propublica.org/people/anna-clark | 0.622 | www.propublica.org/people/hannah-allam | 0.479 | www.propublica.org/people/anna-maria-barry-jester | 0.473 |
| crawl4ai-raw | #1 | www.propublica.org/people/anna-clark | 0.622 | www.propublica.org/people/hannah-allam | 0.479 | www.propublica.org/people/anna-maria-barry-jester | 0.473 |
| scrapy+md | miss | www.propublica.org/people/claire-perlman | 0.459 | www.propublica.org/getinvolved/help-propublica-rep | 0.403 | www.propublica.org/people/bernice-yeung/page/3 | 0.393 |
| crawlee | #1 | www.propublica.org/people/anna-clark | 0.501 | www.propublica.org/people/anna-maria-barry-jester | 0.453 | www.propublica.org/people/abrahm-lustgarten | 0.426 |
| colly+md | miss | www.propublica.org/people/abrahm-lustgarten | 0.421 | www.propublica.org/people/abrahm-lustgarten/page/3 | 0.421 | www.propublica.org/people/doug-bock-clark | 0.416 |
| playwright | #1 | www.propublica.org/people/anna-clark | 0.501 | www.propublica.org/people/anna-maria-barry-jester | 0.453 | www.propublica.org/people/abrahm-lustgarten | 0.426 |


**Q22: What is the title of Anna Clark's book that won the Hillman Prize for Book Journalism?**
*(expects URL containing: `anna-clark`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-reaching-out | 0.328 | www.propublica.org/article/tacrolimus-fda-death-mo | 0.322 | www.propublica.org/article/year-in-photos-illustra | 0.303 |
| crawl4ai | #1 | www.propublica.org/people/anna-clark | 0.509 | www.propublica.org/feeds/propublica/main | 0.384 | www.propublica.org/article/propublica-and-the-conn | 0.381 |
| crawl4ai-raw | #1 | www.propublica.org/people/anna-clark | 0.509 | www.propublica.org/feeds/propublica/main | 0.384 | www.propublica.org/article/propublica-and-the-conn | 0.381 |
| scrapy+md | miss | www.propublica.org/people/claire-perlman | 0.338 | www.propublica.org/people/sarahbeth-maney | 0.327 | www.propublica.org/article/meet-propublicas-2022-s | 0.315 |
| crawlee | #1 | www.propublica.org/people/anna-clark | 0.413 | www.propublica.org/feeds/propublica/main | 0.378 | www.propublica.org/feeds/propublica/main | 0.377 |
| colly+md | miss | www.propublica.org/people/abrahm-lustgarten/page/3 | 0.375 | www.propublica.org/people/abrahm-lustgarten | 0.375 | www.propublica.org/awards/goldsmith-prize-for-expl | 0.365 |
| playwright | #1 | www.propublica.org/people/anna-clark | 0.413 | www.propublica.org/feeds/propublica/main | 0.378 | www.propublica.org/feeds/propublica/main | 0.377 |


**Q23: How many people filed claims against Purdue Pharma for opioid-related harm?**
*(expects URL containing: `purdue-settlement-leaves-opioid-victims-behind`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/prospect-medical-malpra | 0.395 | www.propublica.org/article/prospect-medical-malpra | 0.383 | www.propublica.org/article/raadfest-peptide-inject | 0.380 |
| crawl4ai | #2 | www.propublica.org/feeds/propublica/main | 0.692 | www.propublica.org/article/purdue-settlement-leave | 0.691 | www.propublica.org/feeds/propublica/main | 0.645 |
| crawl4ai-raw | #2 | www.propublica.org/feeds/propublica/main | 0.692 | www.propublica.org/article/purdue-settlement-leave | 0.691 | www.propublica.org/feeds/propublica/main | 0.645 |
| scrapy+md | miss | www.propublica.org/ | 0.486 | www.propublica.org/ | 0.446 | www.propublica.org/article/rx-inspector-fda-generi | 0.363 |
| crawlee | #3 | www.propublica.org/feeds/propublica/main | 0.697 | www.propublica.org/feeds/propublica/main | 0.697 | www.propublica.org/article/purdue-settlement-leave | 0.691 |
| colly+md | miss | www.propublica.org/ | 0.486 | www.propublica.org/ | 0.442 | www.propublica.org/article/propublica-files-lawsui | 0.373 |
| playwright | #3 | www.propublica.org/feeds/propublica/main | 0.697 | www.propublica.org/feeds/propublica/main | 0.697 | www.propublica.org/article/purdue-settlement-leave | 0.691 |


**Q24: What significant provision was removed from the new Purdue settlement plan that affected victims' ability to prove their claims?**
*(expects URL containing: `purdue-settlement-leaves-opioid-victims-behind`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/prospect-medical-malpra | 0.407 | www.propublica.org/article/columbia-university-rob | 0.385 | www.propublica.org/article/trump-doj-colony-ridge- | 0.381 |
| crawl4ai | #1 | www.propublica.org/article/purdue-settlement-leave | 0.557 | www.propublica.org/article/purdue-settlement-leave | 0.555 | www.propublica.org/feeds/propublica/main | 0.544 |
| crawl4ai-raw | #1 | www.propublica.org/article/purdue-settlement-leave | 0.557 | www.propublica.org/article/purdue-settlement-leave | 0.555 | www.propublica.org/feeds/propublica/main | 0.544 |
| scrapy+md | miss | www.propublica.org/ | 0.369 | www.propublica.org/article/flint-water-crisis-invo | 0.343 | www.propublica.org/article/flint-water-crisis-invo | 0.342 |
| crawlee | #1 | www.propublica.org/article/purdue-settlement-leave | 0.557 | www.propublica.org/article/purdue-settlement-leave | 0.555 | www.propublica.org/feeds/propublica/main | 0.549 |
| colly+md | miss | www.propublica.org/article/trump-doj-colony-ridge- | 0.410 | www.propublica.org/article/columbia-university-rob | 0.394 | www.propublica.org/article/trump-doj-colony-ridge- | 0.393 |
| playwright | #1 | www.propublica.org/article/purdue-settlement-leave | 0.557 | www.propublica.org/article/purdue-settlement-leave | 0.555 | www.propublica.org/feeds/propublica/main | 0.549 |


**Q25: What topics does Anna Maria Barry-Jester report on?**
*(expects URL containing: `anna-maria-barry-jester`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/trump-familia-deportaci | 0.375 | www.propublica.org/article/propublica-most-read-st | 0.365 | www.propublica.org/article/trump-education-departm | 0.358 |
| crawl4ai | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.582 | www.propublica.org/people/anna-clark | 0.495 | www.propublica.org/people/jennifer-berry-hawes | 0.462 |
| crawl4ai-raw | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.582 | www.propublica.org/people/anna-clark | 0.495 | www.propublica.org/people/jennifer-berry-hawes | 0.462 |
| scrapy+md | miss | www.propublica.org/people/maryam-jameel/page/3 | 0.426 | www.propublica.org/people/maryam-jameel/page/4 | 0.426 | www.propublica.org/people/maryam-jameel/page/7 | 0.426 |
| crawlee | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.532 | www.propublica.org/people/jennifer-berry-hawes | 0.441 | www.propublica.org/people/anna-clark | 0.438 |
| colly+md | miss | www.propublica.org/topics/racial-justice/page/8 | 0.427 | www.propublica.org/people/amy-yurkanin | 0.421 | www.propublica.org/article/florida-court-ordered-c | 0.417 |
| playwright | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.532 | www.propublica.org/people/jennifer-berry-hawes | 0.441 | www.propublica.org/people/anna-clark | 0.438 |


**Q26: What awards has Anna Maria Barry-Jester received for her work?**
*(expects URL containing: `anna-maria-barry-jester`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/idaho-coroner-system-le | 0.278 | www.propublica.org/article/oklahoma-survivors-act- | 0.270 | www.propublica.org/article/year-in-photos-illustra | 0.257 |
| crawl4ai | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.475 | www.propublica.org/people/anna-clark | 0.430 | www.propublica.org/awards | 0.392 |
| crawl4ai-raw | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.475 | www.propublica.org/people/anna-clark | 0.430 | www.propublica.org/awards | 0.392 |
| scrapy+md | miss | www.propublica.org/people/sarahbeth-maney | 0.390 | www.propublica.org/article/meet-propublicas-2021-d | 0.374 | www.propublica.org/article/meet-propublicas-2021-d | 0.363 |
| crawlee | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.434 | www.propublica.org/awards | 0.398 | www.propublica.org/atpropublica/propublica-selects | 0.395 |
| colly+md | miss | www.propublica.org/awards | 0.398 | www.propublica.org/awards | 0.381 | www.propublica.org/article/propublica-and-the-conn | 0.346 |
| playwright | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.434 | www.propublica.org/awards | 0.398 | www.propublica.org/atpropublica/propublica-selects | 0.395 |


**Q27: How can I share my experience seeking payment from the opioid settlement trusts?**
*(expects URL containing: `purdue-endo-mallinckrodt-opioid-settlement-callout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/trump-doj-colony-ridge- | 0.461 | www.propublica.org/article/prospect-medical-malpra | 0.446 | www.propublica.org/article/trump-doj-colony-ridge- | 0.436 |
| crawl4ai | #1 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.676 | www.propublica.org/article/purdue-settlement-leave | 0.645 | www.propublica.org/article/purdue-settlement-leave | 0.618 |
| crawl4ai-raw | #1 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.676 | www.propublica.org/article/purdue-settlement-leave | 0.645 | www.propublica.org/feeds/propublica/main | 0.618 |
| scrapy+md | miss | www.propublica.org/ | 0.531 | www.propublica.org/ | 0.499 | www.propublica.org/article/our-journalists-stopped | 0.437 |
| crawlee | #1 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.678 | www.propublica.org/article/purdue-settlement-leave | 0.660 | www.propublica.org/feeds/propublica/main | 0.626 |
| colly+md | miss | www.propublica.org/ | 0.539 | www.propublica.org/ | 0.499 | www.propublica.org/article/trump-doj-colony-ridge- | 0.493 |
| playwright | #1 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.678 | www.propublica.org/article/purdue-settlement-leave | 0.660 | www.propublica.org/feeds/propublica/main | 0.625 |


**Q28: What is the focus of ProPublica and The Philadelphia Inquirer's investigation regarding opioid victims?**
*(expects URL containing: `purdue-endo-mallinckrodt-opioid-settlement-callout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/kentucky-addiction-reco | 0.528 | www.propublica.org/article/kentucky-addiction-reco | 0.517 | www.propublica.org/article/drug-testing-thresholds | 0.495 |
| crawl4ai | #1 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.673 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.672 | www.propublica.org/getinvolved | 0.658 |
| crawl4ai-raw | #1 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.673 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.672 | www.propublica.org/getinvolved | 0.658 |
| scrapy+md | miss | www.propublica.org/ | 0.614 | www.propublica.org/ | 0.569 | www.propublica.org/article/our-journalists-stopped | 0.503 |
| crawlee | #1 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.670 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.648 | www.propublica.org/article/purdue-settlement-leave | 0.637 |
| colly+md | miss | www.propublica.org/ | 0.619 | www.propublica.org/ | 0.569 | www.propublica.org/article/veterans-affairs-mental | 0.520 |
| playwright | #1 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.670 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.648 | www.propublica.org/article/purdue-settlement-leave | 0.637 |


**Q29: What is the purpose of the task force created by Newport News and Christopher Newport University?**
*(expects URL containing: `christopher-newport-university-black-community-uprooted-task-force`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/trump-cia-law-enforceme | 0.357 | www.propublica.org/article/trump-defense-departmen | 0.354 | www.propublica.org/article/north-carolina-legislat | 0.319 |
| crawl4ai | #1 | www.propublica.org/article/christopher-newport-uni | 0.603 | www.propublica.org/article/christopher-newport-uni | 0.576 | www.propublica.org/article/christopher-newport-uni | 0.568 |
| crawl4ai-raw | #1 | www.propublica.org/article/christopher-newport-uni | 0.603 | www.propublica.org/article/christopher-newport-uni | 0.576 | www.propublica.org/article/christopher-newport-uni | 0.568 |
| scrapy+md | miss | www.propublica.org/topics/military/page/2 | 0.334 | www.propublica.org/article/north-carolina-legislat | 0.328 | www.propublica.org/article/what-happened-when-a-pu | 0.324 |
| crawlee | #1 | www.propublica.org/article/christopher-newport-uni | 0.617 | www.propublica.org/article/christopher-newport-uni | 0.607 | www.propublica.org/article/christopher-newport-uni | 0.603 |
| colly+md | miss | www.propublica.org/article/christopher-newport-uni | 0.617 | www.propublica.org/article/christopher-newport-uni | 0.609 | www.propublica.org/article/christopher-newport-uni | 0.607 |
| playwright | #1 | www.propublica.org/article/christopher-newport-uni | 0.617 | www.propublica.org/article/christopher-newport-uni | 0.607 | www.propublica.org/article/christopher-newport-uni | 0.603 |


**Q30: How did the expansion of Christopher Newport University affect the Shoe Lane neighborhood?**
*(expects URL containing: `christopher-newport-university-black-community-uprooted-task-force`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/north-carolina-legislat | 0.325 | www.propublica.org/article/nike-jobs-indonesia-liv | 0.314 | www.propublica.org/article/norfolk-southern-train- | 0.301 |
| crawl4ai | #1 | www.propublica.org/article/christopher-newport-uni | 0.668 | www.propublica.org/article/christopher-newport-uni | 0.649 | www.propublica.org/article/christopher-newport-uni | 0.640 |
| crawl4ai-raw | #1 | www.propublica.org/article/christopher-newport-uni | 0.668 | www.propublica.org/article/christopher-newport-uni | 0.649 | www.propublica.org/article/christopher-newport-uni | 0.640 |
| scrapy+md | miss | www.propublica.org/article/north-carolina-legislat | 0.326 | www.propublica.org/article/north-carolina-legislat | 0.321 | www.propublica.org/article/what-happened-when-a-pu | 0.266 |
| crawlee | #1 | www.propublica.org/article/christopher-newport-uni | 0.649 | www.propublica.org/article/christopher-newport-uni | 0.639 | www.propublica.org/article/christopher-newport-uni | 0.633 |
| colly+md | miss | www.propublica.org/article/how-virginia-college-ex | 0.712 | www.propublica.org/article/how-virginia-college-ex | 0.712 | www.propublica.org/article/how-virginia-college-ex | 0.693 |
| playwright | #1 | www.propublica.org/article/christopher-newport-uni | 0.649 | www.propublica.org/article/christopher-newport-uni | 0.639 | www.propublica.org/article/christopher-newport-uni | 0.633 |


**Q31: What topics does Abrahm Lustgarten report on?**
*(expects URL containing: `abrahm-lustgarten`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/jackson-mississippi-syn | 0.325 | www.propublica.org/article/propublica-most-read-st | 0.321 | www.propublica.org/article/columbia-university-new | 0.309 |
| crawl4ai | #1 | www.propublica.org/people/abrahm-lustgarten | 0.515 | www.propublica.org/topics | 0.388 | www.propublica.org/article/connecticut-towing-refo | 0.385 |
| crawl4ai-raw | #1 | www.propublica.org/people/abrahm-lustgarten | 0.515 | www.propublica.org/topics | 0.388 | www.propublica.org/article/connecticut-towing-refo | 0.385 |
| scrapy+md | miss | www.propublica.org/topics/courts | 0.361 | www.propublica.org/topics/taxes | 0.357 | www.propublica.org/reports/page/2 | 0.355 |
| crawlee | #1 | www.propublica.org/people/abrahm-lustgarten | 0.494 | www.propublica.org/article/segregation-academies-p | 0.391 | www.propublica.org/topics | 0.386 |
| colly+md | #1 | www.propublica.org/people/abrahm-lustgarten | 0.501 | www.propublica.org/people/abrahm-lustgarten/page/3 | 0.501 | www.propublica.org/people/abrahm-lustgarten/page/3 | 0.422 |
| playwright | #1 | www.propublica.org/people/abrahm-lustgarten | 0.494 | www.propublica.org/article/segregation-academies-p | 0.390 | www.propublica.org/topics | 0.386 |


**Q32: What awards has Abrahm Lustgarten received for his reporting?**
*(expects URL containing: `abrahm-lustgarten`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/columbia-university-rob | 0.305 | www.propublica.org/article/columbia-university-rob | 0.303 | www.propublica.org/article/columbia-university-new | 0.300 |
| crawl4ai | #1 | www.propublica.org/people/abrahm-lustgarten | 0.468 | www.propublica.org/atpropublica/propublica-selects | 0.436 | www.propublica.org/awards | 0.429 |
| crawl4ai-raw | #1 | www.propublica.org/people/abrahm-lustgarten | 0.468 | www.propublica.org/atpropublica/propublica-selects | 0.436 | www.propublica.org/awards | 0.429 |
| scrapy+md | miss | www.propublica.org/article/meet-propublicas-2021-d | 0.389 | www.propublica.org/people/jason-grotto | 0.371 | www.propublica.org/article/meet-propublicas-2021-d | 0.354 |
| crawlee | #1 | www.propublica.org/people/abrahm-lustgarten | 0.518 | www.propublica.org/awards | 0.432 | www.propublica.org/atpropublica/propublica-selects | 0.424 |
| colly+md | #1 | www.propublica.org/people/abrahm-lustgarten | 0.525 | www.propublica.org/people/abrahm-lustgarten/page/3 | 0.525 | www.propublica.org/awards | 0.432 |
| playwright | #1 | www.propublica.org/people/abrahm-lustgarten | 0.518 | www.propublica.org/awards | 0.432 | www.propublica.org/atpropublica/propublica-selects | 0.424 |


**Q33: What is the role ProPublica is hiring for in partnership with On-Ramps?**
*(expects URL containing: `jobs`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigativ | 0.531 | www.propublica.org/article/propublica-investigativ | 0.497 | www.propublica.org/article/propublica-investigativ | 0.484 |
| crawl4ai | #1 | www.propublica.org/jobs | 0.670 | www.propublica.org/collaborate | 0.580 | www.propublica.org/atpropublica | 0.573 |
| crawl4ai-raw | #1 | www.propublica.org/jobs | 0.670 | www.propublica.org/collaborate | 0.580 | www.propublica.org/atpropublica | 0.574 |
| scrapy+md | miss | www.propublica.org/article/hand-picked-mentors-and | 0.553 | www.propublica.org/article/hand-picked-mentors-and | 0.539 | www.propublica.org/people/talia-buford | 0.533 |
| crawlee | miss | www.propublica.org/collaborate | 0.591 | www.propublica.org/press-releases | 0.571 | www.propublica.org/atpropublica | 0.554 |
| colly+md | #26 | job-boards.greenhouse.io/propublica | 0.706 | www.propublica.org/staff | 0.528 | www.propublica.org/ | 0.498 |
| playwright | #1 | www.propublica.org/jobs | 0.706 | www.propublica.org/collaborate | 0.591 | www.propublica.org/press-releases | 0.571 |


**Q34: How can I receive job opportunities at ProPublica directly in my inbox?**
*(expects URL containing: `jobs`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigativ | 0.575 | www.propublica.org/article/propublica-investigativ | 0.512 | www.propublica.org/article/propublica-investigativ | 0.492 |
| crawl4ai | #1 | www.propublica.org/jobs | 0.680 | www.propublica.org/collaborate | 0.623 | www.propublica.org/contact | 0.609 |
| crawl4ai-raw | #1 | www.propublica.org/jobs | 0.680 | www.propublica.org/collaborate | 0.623 | www.propublica.org/contact | 0.609 |
| scrapy+md | miss | www.propublica.org/diversity | 0.611 | www.propublica.org/fellowships | 0.578 | www.propublica.org/fellowships | 0.571 |
| crawlee | miss | www.propublica.org/collaborate | 0.622 | www.propublica.org/newsletters | 0.610 | www.propublica.org/fellowships | 0.596 |
| colly+md | miss | job-boards.greenhouse.io/propublica | 0.721 | www.propublica.org/newsletters | 0.578 | www.propublica.org/tips/federal-workers/ | 0.572 |
| playwright | #1 | www.propublica.org/jobs | 0.721 | www.propublica.org/collaborate | 0.622 | www.propublica.org/newsletters | 0.610 |


**Q35: What insights does ProPublica seek from current and former inspectors general?**
*(expects URL containing: `an-open-letter-to-the-inspectors-general-community`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/bop-prison-staffing-sho | 0.477 | www.propublica.org/article/propublica-reaching-out | 0.476 | www.propublica.org/article/propublica-reaching-out | 0.465 |
| crawl4ai | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.700 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.670 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.669 |
| crawl4ai-raw | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.700 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.670 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.669 |
| scrapy+md | miss | www.propublica.org/article/how-does-journalism-wor | 0.547 | www.propublica.org/reports/page/2 | 0.537 | www.propublica.org/article/how-does-journalism-wor | 0.528 |
| crawlee | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.679 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.670 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.606 |
| colly+md | miss | www.propublica.org/getinvolved/an-open-letter-to-t | 0.686 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.665 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.625 |
| playwright | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.679 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.670 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.606 |


**Q36: What concerns have been expressed about the new federal government watchdogs?**
*(expects URL containing: `an-open-letter-to-the-inspectors-general-community`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/institute-of-museum-and | 0.467 | www.propublica.org/article/trump-cia-law-enforceme | 0.463 | www.propublica.org/article/institute-of-museum-and | 0.461 |
| crawl4ai | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.501 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.471 | www.propublica.org/tips/federal-workers/ | 0.457 |
| crawl4ai-raw | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.501 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.471 | www.propublica.org/tips/federal-workers/ | 0.457 |
| scrapy+md | miss | www.propublica.org/article/trump-hud-weakening-enf | 0.450 | www.propublica.org/ | 0.448 | www.propublica.org/article/trump-hud-weakening-enf | 0.446 |
| crawlee | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.487 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.471 | www.propublica.org/ | 0.448 |
| colly+md | miss | www.propublica.org/getinvolved/an-open-letter-to-t | 0.499 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.469 | www.propublica.org/article/federal-government-ai-c | 0.453 |
| playwright | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.487 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.471 | www.propublica.org/ | 0.448 |


**Q37: What are some featured posts by Jason Trahan?**
*(expects URL containing: `jason-trahan`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/david-harvilicz-homelan | 0.336 | www.propublica.org/article/year-in-photos-illustra | 0.332 | www.propublica.org/article/year-in-photos-illustra | 0.316 |
| crawl4ai | #11 | www.propublica.org/people/hannah-allam | 0.410 | www.propublica.org/people/logan-jaffe | 0.391 | www.propublica.org/people/jesse-coburn | 0.386 |
| crawl4ai-raw | #11 | www.propublica.org/people/hannah-allam | 0.410 | www.propublica.org/people/logan-jaffe | 0.391 | www.propublica.org/people/jesse-coburn | 0.386 |
| scrapy+md | miss | www.propublica.org/people/jason-grotto | 0.482 | www.propublica.org/people/chris-alcantara | 0.428 | www.propublica.org/people/jason-grotto/page/3 | 0.414 |
| crawlee | #1 | www.propublica.org/people/jason-trahan | 0.413 | www.propublica.org/people/logan-jaffe | 0.413 | www.propublica.org/people/hannah-allam | 0.391 |
| colly+md | miss | www.propublica.org/people/tony-briscoe | 0.399 | www.propublica.org/article/ed-martin-trump-interim | 0.398 | www.propublica.org/people/doug-bock-clark | 0.391 |
| playwright | #1 | www.propublica.org/people/jason-trahan | 0.413 | www.propublica.org/people/logan-jaffe | 0.413 | www.propublica.org/people/hannah-allam | 0.391 |


**Q38: What is the topic of Jason Trahan's post published on April 27, 2026?**
*(expects URL containing: `jason-trahan`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/veterans-affairs-mental | 0.383 | www.propublica.org/article/propublica-most-read-st | 0.381 | www.propublica.org/article/propublica-most-read-st | 0.373 |
| crawl4ai | #30 | www.propublica.org/people/mollie-simon | 0.455 | www.propublica.org/people/j-david-mcswane | 0.450 | www.propublica.org/archive | 0.441 |
| crawl4ai-raw | #30 | www.propublica.org/people/mollie-simon | 0.455 | www.propublica.org/people/j-david-mcswane | 0.450 | www.propublica.org/archive | 0.441 |
| scrapy+md | miss | www.propublica.org/people/sarahbeth-maney | 0.471 | www.propublica.org/people/jason-grotto | 0.445 | www.propublica.org/topics/environment | 0.440 |
| crawlee | #1 | www.propublica.org/people/jason-trahan | 0.450 | www.propublica.org/south | 0.445 | www.propublica.org/people/hannah-allam | 0.444 |
| colly+md | miss | www.propublica.org/south | 0.445 | www.propublica.org/newsapps | 0.438 | www.propublica.org/article/inside-project-2025-sec | 0.431 |
| playwright | #1 | www.propublica.org/people/jason-trahan | 0.450 | www.propublica.org/south | 0.445 | www.propublica.org/people/hannah-allam | 0.444 |


**Q39: What is the main focus of ProPublica's politics section?**
*(expects URL containing: `politics`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-most-read-st | 0.550 | www.propublica.org/article/propublica-reaching-out | 0.476 | www.propublica.org/article/propublica-reaching-out | 0.472 |
| crawl4ai | #17 | www.propublica.org/about | 0.607 | www.propublica.org/local-initiatives | 0.589 | www.propublica.org/collaborate | 0.582 |
| crawl4ai-raw | #17 | www.propublica.org/about | 0.607 | www.propublica.org/local-initiatives | 0.589 | www.propublica.org/collaborate | 0.582 |
| scrapy+md | miss | www.propublica.org/reports/page/2 | 0.600 | www.propublica.org/media-center | 0.578 | www.propublica.org/advertising | 0.565 |
| crawlee | #2 | www.propublica.org/about | 0.589 | www.propublica.org/topics/politics | 0.582 | www.propublica.org/local-initiatives | 0.581 |
| colly+md | #2 | www.propublica.org/awards/toner-prizes-for-excelle | 0.566 | www.propublica.org/topics/politics | 0.565 | www.propublica.org/topics/politics | 0.562 |
| playwright | #2 | www.propublica.org/about | 0.589 | www.propublica.org/topics/politics | 0.582 | www.propublica.org/local-initiatives | 0.581 |


**Q40: What are some featured stories in the politics section of ProPublica?**
*(expects URL containing: `politics`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-most-read-st | 0.643 | www.propublica.org/article/propublica-most-read-st | 0.568 | www.propublica.org/article/propublica-most-read-st | 0.567 |
| crawl4ai | #10 | www.propublica.org/local-initiatives | 0.673 | www.propublica.org/newsletters | 0.669 | www.propublica.org/local-initiatives | 0.659 |
| crawl4ai-raw | #10 | www.propublica.org/local-initiatives | 0.673 | www.propublica.org/newsletters | 0.669 | www.propublica.org/local-initiatives | 0.659 |
| scrapy+md | miss | www.propublica.org/media-center | 0.672 | www.propublica.org/steal-our-stories | 0.649 | www.propublica.org/advertising | 0.638 |
| crawlee | #3 | www.propublica.org/impact | 0.672 | www.propublica.org/local-initiatives | 0.672 | www.propublica.org/topics/politics | 0.662 |
| colly+md | #2 | www.propublica.org/impact | 0.653 | www.propublica.org/topics/politics | 0.643 | www.propublica.org/awards/toner-prizes-for-excelle | 0.640 |
| playwright | #3 | www.propublica.org/impact | 0.672 | www.propublica.org/local-initiatives | 0.672 | www.propublica.org/topics/politics | 0.662 |


**Q41: What experiences did Cookie have while desegregating a white high school?**
*(expects URL containing: `cookie-zoe-macon-georgia-school-segregation-documentary`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/trump-education-departm | 0.415 | www.propublica.org/article/trump-education-departm | 0.397 | www.propublica.org/article/trump-education-departm | 0.391 |
| crawl4ai | #5 | www.propublica.org/article/macon-georgia-segregati | 0.682 | www.propublica.org/article/macon-georgia-segregati | 0.622 | www.propublica.org/article/macon-georgia-segregati | 0.606 |
| crawl4ai-raw | #5 | www.propublica.org/article/macon-georgia-segregati | 0.682 | www.propublica.org/article/macon-georgia-segregati | 0.622 | www.propublica.org/article/macon-georgia-segregati | 0.607 |
| scrapy+md | miss | www.propublica.org/getinvolved/help-propublica-rep | 0.354 | www.propublica.org/topics/education | 0.344 | www.propublica.org/topics/education | 0.334 |
| crawlee | #5 | www.propublica.org/article/macon-georgia-segregati | 0.674 | www.propublica.org/article/macon-georgia-segregati | 0.622 | www.propublica.org/article/macon-georgia-segregati | 0.617 |
| colly+md | miss | www.propublica.org/article/cookie-zoe-macon-georgi | 0.583 | www.propublica.org/article/cookie-zoe-macon-georgi | 0.543 | www.propublica.org/article/cookie-zoe-macon-georgi | 0.522 |
| playwright | #5 | www.propublica.org/article/macon-georgia-segregati | 0.674 | www.propublica.org/article/macon-georgia-segregati | 0.622 | www.propublica.org/article/macon-georgia-segregati | 0.617 |


**Q42: What school does Zo’e Johnson attend and why did her family choose it?**
*(expects URL containing: `cookie-zoe-macon-georgia-school-segregation-documentary`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/trump-administration-li | 0.313 | www.propublica.org/article/trump-education-departm | 0.302 | www.propublica.org/article/south-carolina-measles- | 0.281 |
| crawl4ai | #8 | www.propublica.org/article/macon-georgia-segregati | 0.561 | www.propublica.org/article/macon-georgia-segregati | 0.551 | www.propublica.org/article/macon-georgia-segregati | 0.531 |
| crawl4ai-raw | #8 | www.propublica.org/article/macon-georgia-segregati | 0.561 | www.propublica.org/article/macon-georgia-segregati | 0.551 | www.propublica.org/article/macon-georgia-segregati | 0.531 |
| scrapy+md | miss | www.propublica.org/article/meet-propublicas-2022-s | 0.397 | www.propublica.org/article/meet-propublicas-2021-d | 0.387 | www.propublica.org/article/meet-propublicas-2021-d | 0.384 |
| crawlee | #10 | www.propublica.org/article/macon-georgia-segregati | 0.581 | www.propublica.org/article/macon-georgia-segregati | 0.565 | www.propublica.org/article/macon-georgia-segregati | 0.531 |
| colly+md | miss | www.propublica.org/article/cookie-zoe-macon-georgi | 0.500 | www.propublica.org/article/cookie-zoe-macon-georgi | 0.490 | www.propublica.org/article/cookie-zoe-macon-georgi | 0.460 |
| playwright | #10 | www.propublica.org/article/macon-georgia-segregati | 0.582 | www.propublica.org/article/macon-georgia-segregati | 0.566 | www.propublica.org/article/macon-georgia-segregati | 0.531 |


**Q43: What is the main focus of ProPublica's Racial Justice topic?**
*(expects URL containing: `racial-justice`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/sheriff-jerry-sheridan- | 0.499 | www.propublica.org/article/trump-education-departm | 0.493 | www.propublica.org/article/trump-education-departm | 0.472 |
| crawl4ai | #1 | www.propublica.org/topics/racial-justice | 0.651 | www.propublica.org/topics | 0.622 | www.propublica.org/series/segregation-now | 0.613 |
| crawl4ai-raw | #1 | www.propublica.org/topics/racial-justice | 0.651 | www.propublica.org/topics | 0.622 | www.propublica.org/series/segregation-now | 0.613 |
| scrapy+md | miss | www.propublica.org/diversity | 0.531 | www.propublica.org/media-center | 0.513 | www.propublica.org/getinvolved/send-propublica-sto | 0.512 |
| crawlee | #4 | www.propublica.org/diversity | 0.640 | www.propublica.org/series/segregation-now | 0.638 | www.propublica.org/series/juvenile-injustice-tenne | 0.637 |
| colly+md | #1 | www.propublica.org/topics/racial-justice | 0.642 | www.propublica.org/article/historic-preservation-e | 0.630 | www.propublica.org/series/segregation-now | 0.626 |
| playwright | #4 | www.propublica.org/diversity | 0.640 | www.propublica.org/series/segregation-now | 0.638 | www.propublica.org/series/juvenile-injustice-tenne | 0.637 |


**Q44: How many Native American ancestors were returned to tribes in 2024 according to ProPublica's reporting?**
*(expects URL containing: `racial-justice`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/gallup-mckinley-native- | 0.449 | www.propublica.org/article/gallup-mckinley-native- | 0.428 | www.propublica.org/article/propublica-most-read-st | 0.423 |
| crawl4ai | #14 | www.propublica.org/article/native-american-remains | 0.667 | www.propublica.org/article/native-american-remains | 0.664 | www.propublica.org/article/native-american-remains | 0.660 |
| crawl4ai-raw | #14 | www.propublica.org/article/native-american-remains | 0.667 | www.propublica.org/article/native-american-remains | 0.664 | www.propublica.org/article/native-american-remains | 0.660 |
| scrapy+md | miss | www.propublica.org/article/trump-mass-deportation- | 0.408 | www.propublica.org/article/our-journalists-stopped | 0.390 | www.propublica.org/topics/environment | 0.386 |
| crawlee | #15 | www.propublica.org/article/native-american-remains | 0.723 | www.propublica.org/article/native-american-remains | 0.685 | www.propublica.org/article/native-american-remains | 0.664 |
| colly+md | #17 | www.propublica.org/article/how-to-report-on-repatr | 0.641 | www.propublica.org/article/how-to-report-on-repatr | 0.618 | www.propublica.org/article/how-to-report-on-repatr | 0.615 |
| playwright | #14 | www.propublica.org/article/native-american-remains | 0.723 | www.propublica.org/article/native-american-remains | 0.685 | www.propublica.org/article/native-american-remains | 0.664 |


**Q45: What is the main focus of the 'Segregation Now' series?**
*(expects URL containing: `segregation-now`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/trump-administration-li | 0.334 | www.propublica.org/article/trump-education-departm | 0.332 | www.propublica.org/article/memphis-safe-task-force | 0.312 |
| crawl4ai | #1 | www.propublica.org/series/segregation-now | 0.584 | www.propublica.org/series/segregation-now | 0.560 | www.propublica.org/series/segregation-now | 0.473 |
| crawl4ai-raw | #1 | www.propublica.org/series/segregation-now | 0.584 | www.propublica.org/series/segregation-now | 0.560 | www.propublica.org/series/segregation-now | 0.473 |
| scrapy+md | miss | www.propublica.org/article/trump-hud-weakening-enf | 0.364 | www.propublica.org/topics/education | 0.355 | www.propublica.org/article/has-the-moment-for-envi | 0.345 |
| crawlee | #1 | www.propublica.org/series/segregation-now | 0.576 | www.propublica.org/series/segregation-now | 0.514 | www.propublica.org/article/alabama-researchers-seg | 0.441 |
| colly+md | #1 | www.propublica.org/series/segregation-now | 0.576 | www.propublica.org/series/segregation-now | 0.514 | www.propublica.org/series/segregation-now | 0.441 |
| playwright | #1 | www.propublica.org/series/segregation-now | 0.576 | www.propublica.org/series/segregation-now | 0.514 | www.propublica.org/article/alabama-researchers-seg | 0.441 |


**Q46: How many stories have been published in the 'Segregation Now' series since 2012?**
*(expects URL containing: `segregation-now`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-most-read-st | 0.329 | www.propublica.org/article/propublica-most-read-st | 0.319 | www.propublica.org/article/trump-education-departm | 0.302 |
| crawl4ai | #1 | www.propublica.org/series/segregation-now | 0.504 | www.propublica.org/series/segregation-now | 0.493 | www.propublica.org/article/segregation-academies-p | 0.436 |
| crawl4ai-raw | #1 | www.propublica.org/series/segregation-now | 0.504 | www.propublica.org/series/segregation-now | 0.493 | www.propublica.org/article/segregation-academies-p | 0.436 |
| scrapy+md | miss | www.propublica.org/topics/education | 0.373 | www.propublica.org/article/in-new-york-intolerance | 0.360 | www.propublica.org/people/sarahbeth-maney | 0.349 |
| crawlee | #1 | www.propublica.org/series/segregation-now | 0.551 | www.propublica.org/series/segregation-now | 0.405 | www.propublica.org/series/segregation-now | 0.404 |
| colly+md | #1 | www.propublica.org/series/segregation-now | 0.551 | www.propublica.org/series/segregation-now | 0.405 | www.propublica.org/topics/racial-justice | 0.402 |
| playwright | #1 | www.propublica.org/series/segregation-now | 0.551 | www.propublica.org/series/segregation-now | 0.405 | www.propublica.org/series/segregation-now | 0.404 |


**Q47: What is the principal yardstick for ProPublica's success?**
*(expects URL containing: `impact`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #14 | www.propublica.org/article/propublica-most-read-st | 0.527 | www.propublica.org/article/propublica-reaching-out | 0.505 | www.propublica.org/article/propublica-reaching-out | 0.493 |
| crawl4ai | #6 | www.propublica.org/about | 0.622 | www.propublica.org/code-of-ethics | 0.610 | www.propublica.org/local-initiatives | 0.605 |
| crawl4ai-raw | #6 | www.propublica.org/about | 0.622 | www.propublica.org/code-of-ethics | 0.610 | www.propublica.org/local-initiatives | 0.605 |
| scrapy+md | miss | www.propublica.org/code-of-ethics | 0.593 | www.propublica.org/article/how-does-journalism-wor | 0.576 | www.propublica.org/reports/page/2 | 0.559 |
| crawlee | miss | www.propublica.org/about | 0.614 | www.propublica.org/code-of-ethics | 0.593 | www.propublica.org/local-initiatives | 0.586 |
| colly+md | #30 | www.propublica.org/code-of-ethics | 0.593 | www.propublica.org/article/propublica-and-the-conn | 0.548 | www.propublica.org/tips/ | 0.536 |
| playwright | miss | www.propublica.org/about | 0.614 | www.propublica.org/code-of-ethics | 0.593 | www.propublica.org/local-initiatives | 0.586 |


**Q48: How has ProPublica's reporting influenced legislation regarding abortion access?**
*(expects URL containing: `impact`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.propublica.org/article/propublica-investigatio | 0.604 | www.propublica.org/article/propublica-investigatio | 0.569 | www.propublica.org/article/high-risk-pregnancies-c | 0.551 |
| crawl4ai | #1 | www.propublica.org/impact | 0.661 | www.propublica.org/impact | 0.617 | www.propublica.org/getinvolved | 0.543 |
| crawl4ai-raw | #1 | www.propublica.org/impact | 0.661 | www.propublica.org/impact | 0.617 | www.propublica.org/getinvolved | 0.543 |
| scrapy+md | miss | www.propublica.org/article/how-does-journalism-wor | 0.522 | www.propublica.org/reports/page/2 | 0.514 | www.propublica.org/media-center | 0.493 |
| crawlee | #1 | www.propublica.org/impact | 0.601 | www.propublica.org/series/lost-mothers | 0.565 | www.propublica.org/getinvolved | 0.556 |
| colly+md | #1 | www.propublica.org/impact | 0.633 | www.propublica.org/topics/abortion | 0.590 | www.propublica.org/topics/abortion | 0.579 |
| playwright | #1 | www.propublica.org/impact | 0.602 | www.propublica.org/series/lost-mothers | 0.565 | www.propublica.org/getinvolved | 0.556 |


**Q49: How can I donate online to ProPublica?**
*(expects URL containing: `other-ways-to-give`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigativ | 0.494 | www.propublica.org/article/propublica-investigativ | 0.426 | www.propublica.org/article/propublica-investigativ | 0.418 |
| crawl4ai | #1 | www.propublica.org/support/other-ways-to-give | 0.714 | www.propublica.org/gift-acceptance-practices | 0.707 | www.propublica.org/support/other-ways-to-give | 0.695 |
| crawl4ai-raw | #1 | www.propublica.org/support/other-ways-to-give | 0.714 | www.propublica.org/gift-acceptance-practices | 0.707 | www.propublica.org/support/other-ways-to-give | 0.695 |
| scrapy+md | #1 | www.propublica.org/support/other-ways-to-give | 0.742 | www.propublica.org/support/other-ways-to-give | 0.709 | www.propublica.org/support/other-ways-to-give | 0.690 |
| crawlee | #1 | www.propublica.org/support/other-ways-to-give | 0.728 | www.propublica.org/gift-acceptance-practices | 0.701 | www.propublica.org/support/other-ways-to-give | 0.695 |
| colly+md | miss | www.propublica.org/tips/#common-questions | 0.657 | www.propublica.org/tips/#signal | 0.657 | www.propublica.org/tips/#postalmail | 0.657 |
| playwright | #1 | www.propublica.org/support/other-ways-to-give | 0.728 | www.propublica.org/gift-acceptance-practices | 0.701 | www.propublica.org/support/other-ways-to-give | 0.695 |


**Q50: What information do I need to include when making a gift in my estate plans for ProPublica?**
*(expects URL containing: `other-ways-to-give`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigativ | 0.395 | www.propublica.org/article/habeas-petitions-immigr | 0.380 | www.propublica.org/article/ice-dilley-children-let | 0.376 |
| crawl4ai | #1 | www.propublica.org/support/other-ways-to-give | 0.787 | www.propublica.org/support/other-ways-to-give | 0.651 | www.propublica.org/gift-acceptance-practices | 0.639 |
| crawl4ai-raw | #1 | www.propublica.org/support/other-ways-to-give | 0.787 | www.propublica.org/support/other-ways-to-give | 0.651 | www.propublica.org/gift-acceptance-practices | 0.638 |
| scrapy+md | #1 | www.propublica.org/support/other-ways-to-give | 0.758 | www.propublica.org/support/other-ways-to-give | 0.671 | www.propublica.org/support/other-ways-to-give | 0.613 |
| crawlee | #1 | www.propublica.org/support/other-ways-to-give | 0.755 | www.propublica.org/support/other-ways-to-give | 0.667 | www.propublica.org/gift-acceptance-practices | 0.637 |
| colly+md | miss | www.propublica.org/tips/#common-questions | 0.553 | www.propublica.org/tips/ | 0.553 | www.propublica.org/tips/#securedrop | 0.553 |
| playwright | #1 | www.propublica.org/support/other-ways-to-give | 0.755 | www.propublica.org/support/other-ways-to-give | 0.667 | www.propublica.org/gift-acceptance-practices | 0.637 |


**Q51: What topics does Sarahbeth Maney cover as a photojournalist?**
*(expects URL containing: `sarahbeth-maney`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/year-in-photos-illustra | 0.357 | www.propublica.org/article/trump-familia-deportaci | 0.353 | www.propublica.org/article/ice-dilley-children-let | 0.338 |
| crawl4ai | #1 | www.propublica.org/people/sarahbeth-maney | 0.653 | www.propublica.org/people/jennifer-berry-hawes | 0.482 | www.propublica.org/people/sarahbeth-maney | 0.473 |
| crawl4ai-raw | #1 | www.propublica.org/people/sarahbeth-maney | 0.653 | www.propublica.org/people/jennifer-berry-hawes | 0.482 | www.propublica.org/people/sarahbeth-maney | 0.473 |
| scrapy+md | #1 | www.propublica.org/people/sarahbeth-maney | 0.655 | www.propublica.org/people/sarahbeth-maney | 0.448 | www.propublica.org/article/meet-propublicas-2021-d | 0.446 |
| crawlee | #1 | www.propublica.org/people/sarahbeth-maney | 0.599 | www.propublica.org/people/jennifer-berry-hawes | 0.462 | www.propublica.org/people/liz-moughon | 0.459 |
| colly+md | miss | www.propublica.org/people/mary-hudetz | 0.414 | www.propublica.org/staff | 0.409 | www.propublica.org/staff | 0.403 |
| playwright | #1 | www.propublica.org/people/sarahbeth-maney | 0.599 | www.propublica.org/people/jennifer-berry-hawes | 0.462 | www.propublica.org/people/liz-moughon | 0.459 |


**Q52: What notable awards has Sarahbeth Maney received for her work?**
*(expects URL containing: `sarahbeth-maney`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/oklahoma-survivors-act- | 0.279 | www.propublica.org/article/election-denier-summit- | 0.268 | www.propublica.org/article/oklahoma-survivors-act- | 0.259 |
| crawl4ai | #1 | www.propublica.org/people/sarahbeth-maney | 0.520 | www.propublica.org/staff | 0.419 | www.propublica.org/leadership | 0.369 |
| crawl4ai-raw | #1 | www.propublica.org/people/sarahbeth-maney | 0.520 | www.propublica.org/staff | 0.419 | www.propublica.org/leadership | 0.369 |
| scrapy+md | #1 | www.propublica.org/people/sarahbeth-maney | 0.548 | www.propublica.org/people/bernice-yeung | 0.367 | www.propublica.org/people/bernice-yeung/page/2 | 0.367 |
| crawlee | #1 | www.propublica.org/people/sarahbeth-maney | 0.489 | www.propublica.org/atpropublica/propublica-selects | 0.374 | www.propublica.org/people/jennifer-berry-hawes | 0.371 |
| colly+md | miss | www.propublica.org/staff | 0.371 | www.propublica.org/awards | 0.360 | www.propublica.org/awards | 0.326 |
| playwright | #1 | www.propublica.org/people/sarahbeth-maney | 0.489 | www.propublica.org/atpropublica/propublica-selects | 0.374 | www.propublica.org/people/jennifer-berry-hawes | 0.371 |


**Q53: What types of donations does ProPublica accept?**
*(expects URL containing: `gift-acceptance-practices`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigativ | 0.454 | www.propublica.org/article/propublica-investigativ | 0.446 | www.propublica.org/article/propublica-most-read-st | 0.440 |
| crawl4ai | #1 | www.propublica.org/gift-acceptance-practices | 0.765 | www.propublica.org/support/other-ways-to-give | 0.688 | www.propublica.org/support/other-ways-to-give | 0.666 |
| crawl4ai-raw | #1 | www.propublica.org/gift-acceptance-practices | 0.765 | www.propublica.org/support/other-ways-to-give | 0.688 | www.propublica.org/support/other-ways-to-give | 0.666 |
| scrapy+md | miss | www.propublica.org/support/other-ways-to-give | 0.695 | www.propublica.org/support/other-ways-to-give | 0.681 | www.propublica.org/support/other-ways-to-give | 0.651 |
| crawlee | #1 | www.propublica.org/gift-acceptance-practices | 0.758 | www.propublica.org/support/other-ways-to-give | 0.686 | www.propublica.org/support/other-ways-to-give | 0.669 |
| colly+md | miss | www.propublica.org/tips/#securedrop | 0.583 | www.propublica.org/tips/ | 0.583 | www.propublica.org/tips/#common-questions | 0.583 |
| playwright | #1 | www.propublica.org/gift-acceptance-practices | 0.758 | www.propublica.org/support/other-ways-to-give | 0.686 | www.propublica.org/support/other-ways-to-give | 0.669 |


**Q54: What restrictions are placed on donations to ProPublica?**
*(expects URL containing: `gift-acceptance-practices`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigativ | 0.474 | www.propublica.org/article/oregon-campaign-finance | 0.459 | www.propublica.org/article/propublica-reaching-out | 0.456 |
| crawl4ai | #1 | www.propublica.org/gift-acceptance-practices | 0.739 | www.propublica.org/code-of-ethics | 0.628 | www.propublica.org/legal | 0.627 |
| crawl4ai-raw | #1 | www.propublica.org/gift-acceptance-practices | 0.739 | www.propublica.org/code-of-ethics | 0.628 | www.propublica.org/legal | 0.627 |
| scrapy+md | miss | www.propublica.org/code-of-ethics | 0.647 | www.propublica.org/support/other-ways-to-give | 0.637 | www.propublica.org/support/other-ways-to-give | 0.626 |
| crawlee | #1 | www.propublica.org/gift-acceptance-practices | 0.734 | www.propublica.org/code-of-ethics | 0.647 | www.propublica.org/support/other-ways-to-give | 0.622 |
| colly+md | miss | www.propublica.org/code-of-ethics | 0.647 | www.propublica.org/code-of-ethics | 0.579 | www.propublica.org/code-of-ethics | 0.572 |
| playwright | #1 | www.propublica.org/gift-acceptance-practices | 0.734 | www.propublica.org/code-of-ethics | 0.647 | www.propublica.org/support/other-ways-to-give | 0.622 |


**Q55: What is Nat Lash's role at ProPublica?**
*(expects URL containing: `nat-lash`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-reaching-out | 0.402 | www.propublica.org/article/propublica-investigativ | 0.397 | www.propublica.org/article/propublica-reaching-out | 0.389 |
| crawl4ai | #1 | www.propublica.org/people/nat-lash | 0.613 | www.propublica.org/staff | 0.558 | www.propublica.org/atpropublica | 0.541 |
| crawl4ai-raw | #1 | www.propublica.org/people/nat-lash | 0.613 | www.propublica.org/staff | 0.558 | www.propublica.org/atpropublica | 0.541 |
| scrapy+md | miss | www.propublica.org/reports/page/2 | 0.514 | www.propublica.org/getinvolved/help-propublica-rep | 0.477 | www.propublica.org/diversity | 0.476 |
| crawlee | #1 | www.propublica.org/people/nat-lash | 0.636 | www.propublica.org/article/segregation-academies-p | 0.539 | www.propublica.org/staff | 0.533 |
| colly+md | miss | www.propublica.org/staff | 0.533 | www.propublica.org/staff | 0.531 | www.propublica.org/staff | 0.525 |
| playwright | #1 | www.propublica.org/people/nat-lash | 0.636 | www.propublica.org/article/segregation-academies-p | 0.540 | www.propublica.org/staff | 0.533 |


**Q56: What is the title of the featured post by Nat Lash published on March 31, 2026?**
*(expects URL containing: `nat-lash`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigatio | 0.411 | www.propublica.org/article/propublica-investigatio | 0.392 | www.propublica.org/article/propublica-most-read-st | 0.375 |
| crawl4ai | #1 | www.propublica.org/people/nat-lash | 0.556 | www.propublica.org/nerds | 0.433 | www.propublica.org/people/joel-jacobs | 0.432 |
| crawl4ai-raw | #1 | www.propublica.org/people/nat-lash | 0.556 | www.propublica.org/nerds | 0.433 | www.propublica.org/people/joel-jacobs | 0.432 |
| scrapy+md | miss | www.propublica.org/people/sarahbeth-maney | 0.473 | www.propublica.org/people/talia-buford/page/2 | 0.447 | www.propublica.org/people/agnes-chang | 0.445 |
| crawlee | #1 | www.propublica.org/people/nat-lash | 0.537 | www.propublica.org/newsapps | 0.459 | www.propublica.org/people/joel-jacobs | 0.443 |
| colly+md | miss | www.propublica.org/newsapps | 0.459 | www.propublica.org/people/abrahm-lustgarten/page/3 | 0.433 | www.propublica.org/people/abrahm-lustgarten | 0.433 |
| playwright | #1 | www.propublica.org/people/nat-lash | 0.537 | www.propublica.org/newsapps | 0.459 | www.propublica.org/people/joel-jacobs | 0.443 |


</details>

## react-dev

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| scrapy+md | 79% (46/58) | 91% (53/58) | 93% (54/58) | 93% (54/58) | 93% (54/58) | 0.857 | 1259 | 216 |
| crawlee | 81% (47/58) | 86% (50/58) | 91% (53/58) | 93% (54/58) | 93% (54/58) | 0.851 | 3063 | 217 |
| playwright | 81% (47/58) | 86% (50/58) | 91% (53/58) | 93% (54/58) | 93% (54/58) | 0.851 | 3067 | 221 |
| colly+md | 78% (45/58) | 84% (49/58) | 84% (49/58) | 90% (52/58) | 90% (52/58) | 0.812 | 5083 | 292 |
| crawl4ai | 76% (44/58) | 84% (49/58) | 88% (51/58) | 88% (51/58) | 91% (53/58) | 0.807 | 3210 | 500 |
| crawl4ai-raw | 76% (44/58) | 84% (49/58) | 88% (51/58) | 88% (51/58) | 91% (53/58) | 0.807 | 3210 | 500 |
| markcrawl | 7% (4/58) | 7% (4/58) | 7% (4/58) | 7% (4/58) | 7% (4/58) | 0.069 | 419 | 51 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for react-dev</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is the purpose of the `addTransitionType` API?**
*(expects URL containing: `addTransitionType`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/reusing-logic-with-custom-hooks | 0.364 | react.dev/learn/reusing-logic-with-custom-hooks | 0.355 | react.dev/learn/typescript | 0.339 |
| crawl4ai | #1 | react.dev/reference/react/addTransitionType | 0.659 | react.dev/reference/react/addTransitionType | 0.646 | react.dev/reference/react/useTransition | 0.560 |
| crawl4ai-raw | #1 | react.dev/reference/react/addTransitionType | 0.659 | react.dev/reference/react/addTransitionType | 0.646 | react.dev/reference/react/useTransition | 0.560 |
| scrapy+md | #1 | react.dev/reference/react/addTransitionType | 0.687 | react.dev/reference/react/addTransitionType | 0.553 | react.dev/reference/react/useTransition | 0.552 |
| crawlee | #1 | react.dev/reference/react/addTransitionType | 0.647 | react.dev/reference/react/addTransitionType | 0.643 | react.dev/reference/react/addTransitionType | 0.576 |
| colly+md | #1 | react.dev/reference/react/addTransitionType | 0.647 | react.dev/reference/react/addTransitionType | 0.643 | react.dev/reference/react/addTransitionType | 0.576 |
| playwright | #1 | react.dev/reference/react/addTransitionType | 0.647 | react.dev/reference/react/addTransitionType | 0.643 | react.dev/reference/react/addTransitionType | 0.576 |


**Q2: What happens to Transition Types after each commit?**
*(expects URL containing: `addTransitionType`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/react-compiler/debugging | 0.366 | react.dev/learn/render-and-commit | 0.347 | react.dev/learn/typescript | 0.346 |
| crawl4ai | #1 | react.dev/reference/react/addTransitionType | 0.469 | react.dev/reference/react/useTransition | 0.457 | react.dev/reference/react/addTransitionType | 0.451 |
| crawl4ai-raw | #1 | react.dev/reference/react/addTransitionType | 0.469 | react.dev/reference/react/useTransition | 0.457 | react.dev/reference/react/addTransitionType | 0.451 |
| scrapy+md | #5 | react.dev/reference/react/useTransition | 0.468 | react.dev/reference/react/startTransition | 0.430 | react.dev/reference/react/startTransition | 0.428 |
| crawlee | #1 | react.dev/reference/react/addTransitionType | 0.536 | react.dev/reference/react/useTransition | 0.468 | react.dev/reference/react/startTransition | 0.460 |
| colly+md | #1 | react.dev/reference/react/addTransitionType | 0.536 | react.dev/reference/react/useTransition | 0.468 | react.dev/reference/react/startTransition | 0.460 |
| playwright | #1 | react.dev/reference/react/addTransitionType | 0.536 | react.dev/reference/react/useTransition | 0.468 | react.dev/reference/react/startTransition | 0.460 |


**Q3: What do the `react-dom/static` APIs allow you to generate?**
*(expects URL containing: `static`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/add-react-to-an-existing-project | 0.515 | react.dev/learn/add-react-to-an-existing-project | 0.506 | react.dev/learn/build-a-react-app-from-scratch | 0.502 |
| crawl4ai | #2 | de.react.dev/reference/react-dom | 0.654 | react.dev/reference/react-dom/static | 0.647 | react.dev/reference/react-dom | 0.610 |
| crawl4ai-raw | #2 | de.react.dev/reference/react-dom | 0.654 | react.dev/reference/react-dom/static | 0.647 | react.dev/reference/react-dom | 0.610 |
| scrapy+md | #1 | react.dev/reference/react-dom/static | 0.639 | react.dev/reference/react-dom/static/prerender | 0.611 | react.dev/reference/react-dom/static/prerenderToNo | 0.593 |
| crawlee | #1 | react.dev/reference/react-dom/static | 0.635 | react.dev/reference/react-dom | 0.611 | react.dev/blog/2024/04/25/react-19#ref-as-a-prop | 0.593 |
| colly+md | #1 | react.dev/reference/react-dom/static | 0.634 | react.dev/reference/react-dom | 0.611 | react.dev/blog/2024/12/05/react-19 | 0.593 |
| playwright | #1 | react.dev/reference/react-dom/static | 0.634 | react.dev/reference/react-dom | 0.611 | react.dev/blog/2024/12/05/react-19 | 0.593 |


**Q4: Which methods are available for rendering a React tree to static HTML with Node.js Streams?**
*(expects URL containing: `static`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/understanding-your-ui-as-a-tree | 0.579 | react.dev/learn/understanding-your-ui-as-a-tree | 0.534 | react.dev/learn/describing-the-ui | 0.531 |
| crawl4ai | #1 | 18.react.dev/reference/react-dom/server/renderToSt | 0.774 | 18.react.dev/reference/react-dom/server/renderToNo | 0.739 | 18.react.dev/reference/react-dom/server/renderToSt | 0.719 |
| crawl4ai-raw | #1 | 18.react.dev/reference/react-dom/server/renderToSt | 0.774 | 18.react.dev/reference/react-dom/server/renderToNo | 0.739 | 18.react.dev/reference/react-dom/server/renderToSt | 0.719 |
| scrapy+md | #1 | react.dev/reference/react-dom/static/prerenderToNo | 0.722 | react.dev/reference/react-dom/static/prerenderToNo | 0.716 | react.dev/reference/react-dom/server/renderToPipea | 0.685 |
| crawlee | #1 | react.dev/reference/react-dom/static/prerenderToNo | 0.722 | react.dev/reference/react-dom/server/renderToStrin | 0.692 | react.dev/reference/react-dom/server/renderToPipea | 0.685 |
| colly+md | #1 | react.dev/reference/react-dom/static/prerenderToNo | 0.722 | react.dev/reference/react-dom/server/renderToStrin | 0.692 | react.dev/reference/react-dom/server/renderToPipea | 0.685 |
| playwright | #1 | react.dev/reference/react-dom/static/prerenderToNo | 0.722 | react.dev/reference/react-dom/server/renderToStrin | 0.692 | react.dev/reference/react-dom/server/renderToPipea | 0.685 |


**Q5: What is the purpose of the `taintUniqueValue` function in React?**
*(expects URL containing: `experimental_taintUniqueValue`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/keeping-components-pure | 0.475 | react.dev/learn/rendering-lists | 0.452 | react.dev/learn/referencing-values-with-refs | 0.439 |
| crawl4ai | #1 | react.dev/reference/react/experimental_taintUnique | 0.692 | react.dev/reference/react/experimental_taintUnique | 0.673 | react.dev/reference/react/experimental_taintUnique | 0.672 |
| crawl4ai-raw | #1 | react.dev/reference/react/experimental_taintUnique | 0.692 | react.dev/reference/react/experimental_taintUnique | 0.673 | react.dev/reference/react/experimental_taintUnique | 0.672 |
| scrapy+md | #1 | react.dev/reference/react/experimental_taintUnique | 0.691 | react.dev/reference/react/experimental_taintUnique | 0.684 | react.dev/reference/react/experimental_taintUnique | 0.620 |
| crawlee | #1 | react.dev/reference/react/experimental_taintUnique | 0.706 | react.dev/reference/react/experimental_taintUnique | 0.674 | react.dev/reference/react/experimental_taintUnique | 0.674 |
| colly+md | miss | react.dev/reference/react/experimental/taintUnique | 0.706 | react.dev/reference/react/experimental/taintUnique | 0.674 | react.dev/reference/react/experimental/taintUnique | 0.674 |
| playwright | #1 | react.dev/reference/react/experimental_taintUnique | 0.706 | react.dev/reference/react/experimental_taintUnique | 0.674 | react.dev/reference/react/experimental_taintUnique | 0.674 |


**Q6: What parameters does the `taintUniqueValue` function accept?**
*(expects URL containing: `experimental_taintUniqueValue`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/keeping-components-pure | 0.203 | react.dev/learn/lifecycle-of-reactive-effects | 0.195 | react.dev/learn/reusing-logic-with-custom-hooks | 0.194 |
| crawl4ai | #1 | react.dev/reference/react/experimental_taintUnique | 0.590 | react.dev/reference/react/experimental_taintUnique | 0.556 | react.dev/reference/react/experimental_taintUnique | 0.555 |
| crawl4ai-raw | #1 | react.dev/reference/react/experimental_taintUnique | 0.590 | react.dev/reference/react/experimental_taintUnique | 0.556 | react.dev/reference/react/experimental_taintUnique | 0.555 |
| scrapy+md | #1 | react.dev/reference/react/experimental_taintUnique | 0.640 | react.dev/reference/react/experimental_taintUnique | 0.609 | react.dev/reference/react/experimental_taintUnique | 0.510 |
| crawlee | #1 | react.dev/reference/react/experimental_taintUnique | 0.591 | react.dev/reference/react/experimental_taintUnique | 0.558 | react.dev/reference/react/experimental_taintUnique | 0.545 |
| colly+md | miss | react.dev/reference/react/experimental/taintUnique | 0.591 | react.dev/reference/react/experimental/taintUnique | 0.558 | react.dev/reference/react/experimental/taintUnique | 0.545 |
| playwright | #1 | react.dev/reference/react/experimental_taintUnique | 0.591 | react.dev/reference/react/experimental_taintUnique | 0.558 | react.dev/reference/react/experimental_taintUnique | 0.545 |


**Q7: What are React components?**
*(expects URL containing: ``)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/your-first-component | 0.631 | react.dev/learn/your-first-component | 0.618 | react.dev/learn/describing-the-ui | 0.612 |
| crawl4ai | miss | 15.react.dev | 0.680 | react.dev/learn/your-first-component | 0.661 | az.react.dev/learn/describing-the-ui | 0.653 |
| crawl4ai-raw | miss | 15.react.dev | 0.680 | react.dev/learn/your-first-component | 0.661 | az.react.dev/learn/describing-the-ui | 0.653 |
| scrapy+md | miss | react.dev/learn/your-first-component | 0.655 | react.dev/learn/describing-the-ui | 0.639 | react.dev/learn/your-first-component | 0.610 |
| crawlee | miss | react.dev/learn/describing-the-ui | 0.643 | react.dev/reference/react/components | 0.641 | react.dev/learn/your-first-component | 0.634 |
| colly+md | miss | react.dev/reference/react/components | 0.641 | react.dev/learn/describing-the-ui | 0.638 | react.dev/learn/your-first-component | 0.634 |
| playwright | miss | react.dev/reference/react/components | 0.641 | react.dev/learn/describing-the-ui | 0.638 | react.dev/learn/your-first-component | 0.634 |


**Q8: How does React handle data updates in components?**
*(expects URL containing: ``)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/preserving-and-resetting-state | 0.590 | react.dev/learn/render-and-commit | 0.580 | react.dev/learn/updating-objects-in-state | 0.579 |
| crawl4ai | miss | react.dev/learn/queueing-a-series-of-state-updates | 0.619 | az.react.dev/learn/adding-interactivity | 0.609 | 18.react.dev/learn/adding-interactivity | 0.609 |
| crawl4ai-raw | miss | react.dev/learn/queueing-a-series-of-state-updates | 0.619 | az.react.dev/learn/adding-interactivity | 0.609 | 18.react.dev/learn/adding-interactivity | 0.609 |
| scrapy+md | miss | react.dev/learn/adding-interactivity | 0.595 | react.dev/learn/updating-objects-in-state | 0.581 | react.dev/reference/react/useReducer | 0.579 |
| crawlee | miss | react.dev/reference/react/Component | 0.638 | react.dev/learn/queueing-a-series-of-state-updates | 0.626 | react.dev/learn/you-might-not-need-an-effect | 0.610 |
| colly+md | miss | react.dev/reference/react/Component | 0.638 | react.dev/learn/queueing-a-series-of-state-updates | 0.626 | react.dev/learn/you-might-not-need-an-effect | 0.610 |
| playwright | miss | react.dev/reference/react/Component | 0.638 | react.dev/learn/queueing-a-series-of-state-updates | 0.626 | react.dev/learn/you-might-not-need-an-effect | 0.610 |


**Q9: How many languages is react.dev being translated into?**
*(expects URL containing: ``)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/react-compiler/incremental-adoptio | 0.457 | react.dev/learn/react-compiler/installation | 0.450 | react.dev/learn/setup | 0.448 |
| crawl4ai | miss | translations.react.dev/ | 0.732 | de.react.dev/community/translations | 0.659 | react.dev/community/translations | 0.648 |
| crawl4ai-raw | miss | translations.react.dev/ | 0.732 | de.react.dev/community/translations | 0.658 | react.dev/community/translations | 0.648 |
| scrapy+md | miss | react.dev/community/translations | 0.587 | react.dev/community/acknowledgements | 0.518 | react.dev/community/meetups | 0.517 |
| crawlee | miss | react.dev/community/translations | 0.625 | react.dev/community/translations | 0.618 | react.dev/community/acknowledgements | 0.545 |
| colly+md | miss | react.dev/community/translations | 0.625 | react.dev/community/translations | 0.618 | react.dev/community/acknowledgements | 0.545 |
| playwright | miss | react.dev/community/translations | 0.625 | react.dev/community/translations | 0.618 | react.dev/community/acknowledgements | 0.545 |


**Q10: Which languages have completed translations for both core and other content?**
*(expects URL containing: ``)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/react-compiler/incremental-adoptio | 0.247 | react.dev/learn/creating-a-react-app | 0.228 | react.dev/learn/react-compiler/incremental-adoptio | 0.227 |
| crawl4ai | miss | translations.react.dev/ | 0.564 | translations.react.dev/ | 0.553 | translations.react.dev/ | 0.487 |
| crawl4ai-raw | miss | translations.react.dev/ | 0.564 | translations.react.dev/ | 0.553 | translations.react.dev/ | 0.487 |
| scrapy+md | miss | react.dev/community/translations | 0.421 | react.dev/community/acknowledgements | 0.330 | react.dev/community/docs-contributors | 0.322 |
| crawlee | miss | react.dev/community/translations | 0.457 | react.dev/community/translations | 0.443 | react.dev/community/acknowledgements | 0.354 |
| colly+md | miss | react.dev/community/translations | 0.457 | react.dev/community/translations | 0.443 | react.dev/community/acknowledgements | 0.354 |
| playwright | miss | react.dev/community/translations | 0.457 | react.dev/community/translations | 0.443 | react.dev/community/acknowledgements | 0.354 |


**Q11: What is the purpose of using `<Fragment>` in React?**
*(expects URL containing: `Fragment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/writing-markup-with-jsx | 0.555 | react.dev/learn/rendering-lists | 0.504 | react.dev/learn/rendering-lists | 0.499 |
| crawl4ai | #1 | react.dev/reference/react/Fragment | 0.681 | react.dev/reference/react/Fragment | 0.662 | react.dev/reference/react/Fragment | 0.656 |
| crawl4ai-raw | #1 | react.dev/reference/react/Fragment | 0.681 | react.dev/reference/react/Fragment | 0.662 | react.dev/reference/react/Fragment | 0.656 |
| scrapy+md | #1 | react.dev/reference/react/Fragment | 0.634 | react.dev/reference/react/Fragment | 0.631 | react.dev/reference/react/Fragment | 0.600 |
| crawlee | #1 | react.dev/reference/react/Fragment | 0.635 | react.dev/reference/react/Fragment | 0.631 | react.dev/reference/react/Fragment | 0.609 |
| colly+md | #1 | react.dev/reference/react/Fragment | 0.634 | react.dev/reference/react/Fragment#rendering-a-lis | 0.634 | react.dev/reference/react/Fragment#rendering-a-lis | 0.631 |
| playwright | #1 | react.dev/reference/react/Fragment | 0.634 | react.dev/reference/react/Fragment | 0.631 | react.dev/reference/react/Fragment | 0.609 |


**Q12: How can you pass a `key` to a Fragment?**
*(expects URL containing: `Fragment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/rendering-lists | 0.457 | react.dev/learn/tutorial-tic-tac-toe | 0.387 | react.dev/learn/tutorial-tic-tac-toe | 0.371 |
| crawl4ai | #1 | react.dev/reference/react/Fragment | 0.459 | react.dev/reference/react/Fragment | 0.452 | react.dev/reference/react/Fragment | 0.440 |
| crawl4ai-raw | #1 | react.dev/reference/react/Fragment | 0.459 | react.dev/reference/react/Fragment | 0.452 | react.dev/reference/react/Fragment | 0.440 |
| scrapy+md | #1 | react.dev/reference/react/Fragment | 0.485 | react.dev/reference/react/Fragment | 0.440 | react.dev/reference/react/Fragment | 0.435 |
| crawlee | #1 | react.dev/reference/react/Fragment | 0.490 | react.dev/reference/react/Fragment | 0.438 | react.dev/learn/rendering-lists | 0.433 |
| colly+md | #1 | react.dev/reference/react/Fragment#rendering-a-lis | 0.490 | react.dev/reference/react/Fragment | 0.490 | react.dev/reference/react/Fragment#rendering-a-lis | 0.440 |
| playwright | #1 | react.dev/reference/react/Fragment | 0.490 | react.dev/reference/react/Fragment | 0.440 | react.dev/learn/rendering-lists | 0.432 |


**Q13: What does <StrictMode> do in React?**
*(expects URL containing: `StrictMode`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/synchronizing-with-effects | 0.517 | react.dev/learn/render-and-commit | 0.515 | react.dev/learn/keeping-components-pure | 0.512 |
| crawl4ai | #1 | react.dev/reference/react/StrictMode | 0.733 | react.dev/reference/react/StrictMode | 0.728 | react.dev/reference/react/StrictMode | 0.697 |
| crawl4ai-raw | #1 | react.dev/reference/react/StrictMode | 0.733 | react.dev/reference/react/StrictMode | 0.728 | react.dev/reference/react/StrictMode | 0.697 |
| scrapy+md | #1 | react.dev/reference/react/StrictMode | 0.730 | react.dev/reference/react/StrictMode | 0.719 | react.dev/reference/react/StrictMode | 0.677 |
| crawlee | #1 | react.dev/reference/react/StrictMode | 0.716 | react.dev/reference/react/StrictMode | 0.715 | react.dev/reference/react/StrictMode | 0.684 |
| colly+md | #1 | react.dev/reference/react/StrictMode | 0.716 | react.dev/reference/react/StrictMode#fixing-bugs-f | 0.716 | react.dev/reference/react/StrictMode | 0.715 |
| playwright | #1 | react.dev/reference/react/StrictMode | 0.716 | react.dev/reference/react/StrictMode | 0.715 | react.dev/reference/react/StrictMode | 0.684 |


**Q14: How can you enable Strict Mode for a part of your application?**
*(expects URL containing: `StrictMode`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/react-compiler/incremental-adoptio | 0.400 | react.dev/learn/react-compiler/incremental-adoptio | 0.368 | react.dev/learn/build-a-react-app-from-scratch | 0.359 |
| crawl4ai | #1 | react.dev/reference/react/StrictMode | 0.617 | react.dev/reference/react/StrictMode | 0.534 | react.dev/reference/react/StrictMode | 0.524 |
| crawl4ai-raw | #1 | react.dev/reference/react/StrictMode | 0.617 | react.dev/reference/react/StrictMode | 0.534 | react.dev/reference/react/StrictMode | 0.524 |
| scrapy+md | #1 | react.dev/reference/react/StrictMode | 0.652 | react.dev/reference/react/StrictMode | 0.612 | react.dev/reference/react/StrictMode | 0.546 |
| crawlee | #1 | react.dev/reference/react/StrictMode | 0.625 | react.dev/reference/react/StrictMode | 0.555 | react.dev/reference/react/StrictMode | 0.514 |
| colly+md | #1 | react.dev/reference/react/StrictMode#fixing-bugs-f | 0.625 | react.dev/reference/react/StrictMode | 0.625 | react.dev/reference/react/StrictMode | 0.555 |
| playwright | #1 | react.dev/reference/react/StrictMode | 0.625 | react.dev/reference/react/StrictMode | 0.555 | react.dev/reference/react/StrictMode | 0.514 |


**Q15: What does memo do in React?**
*(expects URL containing: `memo`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/typescript | 0.614 | react.dev/learn/react-compiler/introduction | 0.602 | react.dev/learn/you-might-not-need-an-effect | 0.577 |
| crawl4ai | #1 | react.dev/reference/react/memo | 0.723 | react.dev/reference/react/memo | 0.720 | react.dev/reference/react/useMemo | 0.695 |
| crawl4ai-raw | #1 | react.dev/reference/react/memo | 0.723 | react.dev/reference/react/memo | 0.720 | react.dev/reference/react/useMemo | 0.695 |
| scrapy+md | #1 | react.dev/reference/react/memo | 0.678 | react.dev/reference/react/memo | 0.672 | react.dev/reference/react/memo | 0.655 |
| crawlee | #1 | react.dev/reference/react-compiler/directives/use- | 0.756 | react.dev/reference/react/memo | 0.729 | react.dev/reference/react/memo | 0.689 |
| colly+md | #1 | react.dev/reference/react-compiler/directives/use- | 0.756 | react.dev/reference/react/memo | 0.728 | react.dev/reference/react/memo | 0.689 |
| playwright | #1 | react.dev/reference/react-compiler/directives/use- | 0.756 | react.dev/reference/react/memo | 0.728 | react.dev/reference/react/memo | 0.689 |


**Q16: How can you specify a custom comparison function for memo?**
*(expects URL containing: `memo`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/you-might-not-need-an-effect | 0.409 | react.dev/learn/typescript | 0.392 | react.dev/learn/react-compiler/introduction | 0.355 |
| crawl4ai | #1 | react.dev/reference/react/memo | 0.525 | react.dev/reference/react-compiler/directives/use- | 0.495 | react.dev/reference/react/useMemo | 0.448 |
| crawl4ai-raw | #1 | react.dev/reference/react/memo | 0.525 | react.dev/reference/react-compiler/directives/use- | 0.495 | react.dev/reference/react/useMemo | 0.448 |
| scrapy+md | #1 | react.dev/reference/react/memo | 0.550 | react.dev/reference/react-compiler/directives/use- | 0.502 | react.dev/reference/react/memo | 0.497 |
| crawlee | #1 | react.dev/reference/react/memo | 0.551 | react.dev/reference/react-compiler/directives/use- | 0.513 | react.dev/reference/react/memo | 0.500 |
| colly+md | #1 | react.dev/reference/react/memo | 0.551 | react.dev/reference/react-compiler/directives/use- | 0.513 | react.dev/reference/react/memo | 0.500 |
| playwright | #1 | react.dev/reference/react/memo | 0.550 | react.dev/reference/react-compiler/directives/use- | 0.513 | react.dev/reference/react/memo | 0.500 |


**Q17: What does cloneElement do in React?**
*(expects URL containing: `cloneElement`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/render-and-commit | 0.502 | react.dev/learn/react-compiler/introduction | 0.494 | react.dev/learn/react-compiler/introduction | 0.489 |
| crawl4ai | #1 | react.dev/reference/react/cloneElement | 0.747 | react.dev/reference/react/cloneElement | 0.707 | react.dev/reference/react/cloneElement | 0.673 |
| crawl4ai-raw | #1 | react.dev/reference/react/cloneElement | 0.747 | react.dev/reference/react/cloneElement | 0.707 | react.dev/reference/react/cloneElement | 0.672 |
| scrapy+md | #1 | react.dev/reference/react/cloneElement | 0.744 | react.dev/reference/react/cloneElement | 0.737 | react.dev/reference/react/cloneElement | 0.664 |
| crawlee | #1 | react.dev/reference/react/cloneElement | 0.737 | react.dev/reference/react/cloneElement | 0.716 | react.dev/reference/react/cloneElement | 0.685 |
| colly+md | #1 | react.dev/reference/react/cloneElement | 0.737 | react.dev/reference/react/cloneElement | 0.715 | react.dev/reference/react/cloneElement | 0.685 |
| playwright | #1 | react.dev/reference/react/cloneElement | 0.737 | react.dev/reference/react/cloneElement | 0.716 | react.dev/reference/react/cloneElement | 0.685 |


**Q18: What are the parameters required for cloneElement?**
*(expects URL containing: `cloneElement`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/passing-data-deeply-with-context | 0.273 | react.dev/learn/passing-props-to-a-component | 0.270 | react.dev/learn/passing-props-to-a-component | 0.266 |
| crawl4ai | #1 | react.dev/reference/react/cloneElement | 0.593 | react.dev/reference/react/cloneElement | 0.492 | react.dev/reference/react/cloneElement | 0.472 |
| crawl4ai-raw | #1 | react.dev/reference/react/cloneElement | 0.593 | react.dev/reference/react/cloneElement | 0.492 | react.dev/reference/react/cloneElement | 0.472 |
| scrapy+md | #1 | react.dev/reference/react/cloneElement | 0.590 | react.dev/reference/react/cloneElement | 0.545 | react.dev/reference/react/cloneElement | 0.415 |
| crawlee | #1 | react.dev/reference/react/cloneElement | 0.550 | react.dev/reference/react/cloneElement | 0.545 | react.dev/reference/react/cloneElement | 0.536 |
| colly+md | #1 | react.dev/reference/react/cloneElement | 0.550 | react.dev/reference/react/cloneElement | 0.545 | react.dev/reference/react/cloneElement | 0.536 |
| playwright | #1 | react.dev/reference/react/cloneElement | 0.550 | react.dev/reference/react/cloneElement | 0.545 | react.dev/reference/react/cloneElement | 0.536 |


**Q19: How do you share state between components in React?**
*(expects URL containing: `sharing-state-between-components`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/sharing-state-between-components | 0.662 | react.dev/learn/state-a-components-memory | 0.662 | react.dev/learn/managing-state | 0.652 |
| crawl4ai | #1 | react.dev/learn/sharing-state-between-components | 0.725 | react.dev/learn/state-a-components-memory | 0.690 | react.dev/learn/sharing-state-between-components | 0.688 |
| crawl4ai-raw | #1 | react.dev/learn/sharing-state-between-components | 0.726 | react.dev/learn/state-a-components-memory | 0.690 | react.dev/learn/sharing-state-between-components | 0.688 |
| scrapy+md | #1 | react.dev/learn/sharing-state-between-components | 0.707 | react.dev/learn/state-a-components-memory | 0.664 | react.dev/learn/sharing-state-between-components | 0.662 |
| crawlee | #2 | react.dev/learn/state-a-components-memory | 0.664 | react.dev/learn/sharing-state-between-components | 0.662 | react.dev/learn/sharing-state-between-components | 0.661 |
| colly+md | #3 | react.dev/learn/state-a-components-memory | 0.664 | react.dev/learn/state-a-components-memory#anatomy- | 0.664 | react.dev/learn/sharing-state-between-components | 0.662 |
| playwright | #2 | react.dev/learn/state-a-components-memory | 0.664 | react.dev/learn/sharing-state-between-components | 0.662 | react.dev/learn/managing-state | 0.653 |


**Q20: What is the difference between controlled and uncontrolled components?**
*(expects URL containing: `sharing-state-between-components`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/sharing-state-between-components | 0.514 | react.dev/learn/sharing-state-between-components | 0.487 | react.dev/learn/sharing-state-between-components | 0.360 |
| crawl4ai | #1 | react.dev/learn/sharing-state-between-components | 0.572 | react.dev/learn/sharing-state-between-components | 0.487 | react.dev/reference/react-dom/components/input | 0.369 |
| crawl4ai-raw | #1 | react.dev/learn/sharing-state-between-components | 0.573 | react.dev/learn/sharing-state-between-components | 0.486 | react.dev/reference/react-dom/components/input | 0.369 |
| scrapy+md | #1 | react.dev/learn/sharing-state-between-components | 0.487 | react.dev/learn/sharing-state-between-components | 0.467 | react.dev/reference/react-dom/components/input | 0.396 |
| crawlee | #1 | react.dev/learn/sharing-state-between-components | 0.520 | react.dev/learn/sharing-state-between-components | 0.487 | react.dev/learn/sharing-state-between-components | 0.475 |
| colly+md | #1 | react.dev/learn/sharing-state-between-components | 0.520 | react.dev/learn/sharing-state-between-components | 0.487 | react.dev/learn/sharing-state-between-components | 0.474 |
| playwright | #1 | react.dev/learn/sharing-state-between-components | 0.520 | react.dev/learn/sharing-state-between-components | 0.487 | react.dev/learn/sharing-state-between-components | 0.475 |


**Q21: What is the new domain for the React documentation site?**
*(expects URL containing: `introducing-react-dev`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/react-compiler | 0.502 | react.dev/learn/installation | 0.501 | react.dev/learn/react-developer-tools | 0.499 |
| crawl4ai | #1 | he.react.dev/blog/2023/03/16/introducing-react-dev | 0.731 | react.dev/blog/2023/03/16/introducing-react-dev | 0.713 | react.dev/blog/2023/03/16/introducing-react-dev | 0.646 |
| crawl4ai-raw | #1 | he.react.dev/blog/2023/03/16/introducing-react-dev | 0.731 | react.dev/blog/2023/03/16/introducing-react-dev | 0.713 | react.dev/blog/2023/03/16/introducing-react-dev | 0.646 |
| scrapy+md | #2 | react.dev/blog | 0.649 | react.dev/blog/2023/03/16/introducing-react-dev | 0.640 | react.dev/blog/2022/06/15/react-labs-what-we-have- | 0.614 |
| crawlee | #1 | react.dev/blog/2023/03/16/introducing-react-dev | 0.666 | react.dev/blog/2023/03/16/introducing-react-dev | 0.658 | react.dev/blog | 0.649 |
| colly+md | #1 | react.dev/blog/2023/03/16/introducing-react-dev | 0.666 | react.dev/blog/2023/03/16/introducing-react-dev | 0.658 | react.dev/blog | 0.649 |
| playwright | #1 | react.dev/blog/2023/03/16/introducing-react-dev | 0.666 | react.dev/blog/2023/03/16/introducing-react-dev | 0.658 | react.dev/blog | 0.649 |


**Q22: How does the new documentation teach React differently than before?**
*(expects URL containing: `introducing-react-dev`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/reacting-to-input-with-state | 0.558 | react.dev/learn/typescript | 0.552 | react.dev/learn/writing-markup-with-jsx | 0.532 |
| crawl4ai | #1 | he.react.dev/blog/2023/03/16/introducing-react-dev | 0.677 | react.dev/blog/2023/03/16/introducing-react-dev | 0.674 | react.dev/blog/2022/06/15/react-labs-what-we-have- | 0.658 |
| crawl4ai-raw | #1 | he.react.dev/blog/2023/03/16/introducing-react-dev | 0.677 | react.dev/blog/2023/03/16/introducing-react-dev | 0.674 | react.dev/blog/2022/06/15/react-labs-what-we-have- | 0.658 |
| scrapy+md | #1 | react.dev/blog/2023/03/16/introducing-react-dev | 0.666 | react.dev/blog/2022/06/15/react-labs-what-we-have- | 0.628 | react.dev/versions | 0.621 |
| crawlee | #1 | react.dev/blog/2023/03/16/introducing-react-dev | 0.682 | react.dev/blog/2022/06/15/react-labs-what-we-have- | 0.659 | react.dev/blog/2023/03/16/introducing-react-dev | 0.656 |
| colly+md | #1 | react.dev/blog/2023/03/16/introducing-react-dev | 0.682 | react.dev/blog/2022/06/15/react-labs-what-we-have- | 0.659 | react.dev/blog/2023/03/16/introducing-react-dev | 0.656 |
| playwright | #1 | react.dev/blog/2023/03/16/introducing-react-dev | 0.682 | react.dev/blog/2022/06/15/react-labs-what-we-have- | 0.659 | react.dev/blog/2023/03/16/introducing-react-dev | 0.656 |


**Q23: What is the mission of the React Foundation?**
*(expects URL containing: `introducing-the-react-foundation`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/build-a-react-app-from-scratch | 0.493 | react.dev/learn/installation | 0.484 | react.dev/learn/react-compiler | 0.483 |
| crawl4ai | #1 | react.dev/blog/2025/10/07/introducing-the-react-fo | 0.702 | ar.react.dev/blog/2025/10/07/introducing-the-react | 0.698 | react.dev/blog/2026/02/24/the-react-foundation | 0.686 |
| crawl4ai-raw | #1 | react.dev/blog/2025/10/07/introducing-the-react-fo | 0.702 | ar.react.dev/blog/2025/10/07/introducing-the-react | 0.698 | react.dev/blog/2026/02/24/the-react-foundation | 0.686 |
| scrapy+md | #2 | react.dev/blog/2026/02/24/the-react-foundation | 0.678 | react.dev/blog/2025/10/07/introducing-the-react-fo | 0.666 | react.dev/blog/2026/02/24/the-react-foundation | 0.635 |
| crawlee | #2 | react.dev/blog/2026/02/24/the-react-foundation | 0.693 | react.dev/blog/2025/10/07/introducing-the-react-fo | 0.675 | react.dev/blog/2025/10/07/introducing-the-react-fo | 0.672 |
| colly+md | #2 | react.dev/blog/2026/02/24/the-react-foundation | 0.693 | react.dev/blog/2025/10/07/introducing-the-react-fo | 0.675 | react.dev/blog/2025/10/07/introducing-the-react-fo | 0.672 |
| playwright | #2 | react.dev/blog/2026/02/24/the-react-foundation | 0.693 | react.dev/blog/2025/10/07/introducing-the-react-fo | 0.675 | react.dev/blog/2025/10/07/introducing-the-react-fo | 0.672 |


**Q24: Who will serve as the executive director of the React Foundation?**
*(expects URL containing: `introducing-the-react-foundation`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/build-a-react-app-from-scratch | 0.407 | react.dev/learn/creating-a-react-app | 0.407 | react.dev/learn/setup | 0.404 |
| crawl4ai | #4 | zh-hans.react.dev/blog/2026/02/24/the-react-founda | 0.695 | react.dev/blog/2026/02/24/the-react-foundation | 0.693 | tr.react.dev/blog/2026/02/24/the-react-foundation | 0.689 |
| crawl4ai-raw | #4 | zh-hans.react.dev/blog/2026/02/24/the-react-founda | 0.695 | react.dev/blog/2026/02/24/the-react-foundation | 0.693 | tr.react.dev/blog/2026/02/24/the-react-foundation | 0.689 |
| scrapy+md | #2 | react.dev/blog/2026/02/24/the-react-foundation | 0.666 | react.dev/blog/2025/10/07/introducing-the-react-fo | 0.661 | react.dev/blog/2026/02/24/the-react-foundation | 0.561 |
| crawlee | #2 | react.dev/blog/2026/02/24/the-react-foundation | 0.667 | react.dev/blog/2025/10/07/introducing-the-react-fo | 0.666 | react.dev/blog/2026/02/24/the-react-foundation | 0.650 |
| colly+md | #2 | react.dev/blog/2026/02/24/the-react-foundation | 0.667 | react.dev/blog/2025/10/07/introducing-the-react-fo | 0.666 | react.dev/blog/2026/02/24/the-react-foundation | 0.650 |
| playwright | #2 | react.dev/blog/2026/02/24/the-react-foundation | 0.667 | react.dev/blog/2025/10/07/introducing-the-react-fo | 0.666 | react.dev/blog/2026/02/24/the-react-foundation | 0.650 |


**Q25: What does 'use memo' do in React?**
*(expects URL containing: `use-memo`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/typescript | 0.618 | react.dev/learn/you-might-not-need-an-effect | 0.595 | react.dev/learn/react-compiler/introduction | 0.574 |
| crawl4ai | #3 | react.dev/reference/react/memo | 0.717 | react.dev/reference/react/memo | 0.710 | react.dev/reference/react-compiler/directives/use- | 0.686 |
| crawl4ai-raw | #3 | react.dev/reference/react/memo | 0.717 | react.dev/reference/react/memo | 0.710 | react.dev/reference/react-compiler/directives/use- | 0.686 |
| scrapy+md | #1 | react.dev/reference/react-compiler/directives/use- | 0.673 | react.dev/reference/react/memo | 0.670 | react.dev/reference/react-compiler/directives/use- | 0.669 |
| crawlee | #1 | react.dev/reference/react-compiler/directives/use- | 0.766 | react.dev/reference/react/memo | 0.716 | react.dev/reference/react/useMemo | 0.690 |
| colly+md | #1 | react.dev/reference/react-compiler/directives/use- | 0.766 | react.dev/reference/react/memo | 0.717 | react.dev/reference/react/useMemo | 0.690 |
| playwright | #1 | react.dev/reference/react-compiler/directives/use- | 0.766 | react.dev/reference/react/memo | 0.716 | react.dev/reference/react/useMemo | 0.690 |


**Q26: When should you consider using 'use memo'?**
*(expects URL containing: `use-memo`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/you-might-not-need-an-effect | 0.485 | react.dev/learn/typescript | 0.457 | react.dev/learn/react-compiler/introduction | 0.432 |
| crawl4ai | #2 | react.dev/reference/react/useMemo | 0.606 | react.dev/reference/react-compiler/directives/use- | 0.597 | react.dev/reference/react/memo | 0.586 |
| crawl4ai-raw | #2 | react.dev/reference/react/useMemo | 0.606 | react.dev/reference/react-compiler/directives/use- | 0.597 | react.dev/reference/react/memo | 0.586 |
| scrapy+md | #1 | react.dev/reference/react-compiler/directives/use- | 0.602 | react.dev/reference/react-compiler/directives/use- | 0.589 | react.dev/reference/react/memo | 0.585 |
| crawlee | #1 | react.dev/reference/react-compiler/directives/use- | 0.617 | react.dev/reference/react-compiler/directives/use- | 0.616 | react.dev/reference/react/memo | 0.585 |
| colly+md | #1 | react.dev/reference/react-compiler/directives/use- | 0.617 | react.dev/reference/react-compiler/directives/use- | 0.616 | react.dev/reference/react/memo | 0.585 |
| playwright | #1 | react.dev/reference/react-compiler/directives/use- | 0.617 | react.dev/reference/react-compiler/directives/use- | 0.616 | react.dev/reference/react/memo | 0.585 |


**Q27: What does renderToStaticMarkup do?**
*(expects URL containing: `renderToStaticMarkup`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/writing-markup-with-jsx | 0.362 | react.dev/learn/render-and-commit | 0.345 | react.dev/learn/understanding-your-ui-as-a-tree | 0.332 |
| crawl4ai | #1 | react.dev/reference/react-dom/server/renderToStati | 0.604 | react.dev/reference/react-dom/server/renderToStati | 0.548 | react.dev/reference/react-dom/server/renderToStati | 0.530 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/server/renderToStati | 0.604 | react.dev/reference/react-dom/server/renderToStati | 0.548 | react.dev/reference/react-dom/server/renderToStati | 0.530 |
| scrapy+md | #1 | react.dev/reference/react-dom/server/renderToStati | 0.506 | react.dev/reference/react-dom/server/renderToStrin | 0.438 | react.dev/reference/react-dom/static/prerenderToNo | 0.435 |
| crawlee | #1 | react.dev/reference/react-dom/server/renderToStati | 0.605 | react.dev/reference/react-dom/server/renderToStati | 0.585 | react.dev/reference/react-dom/server/renderToStati | 0.532 |
| colly+md | #1 | react.dev/reference/react-dom/server/renderToStati | 0.605 | react.dev/reference/react-dom/server/renderToStati | 0.585 | react.dev/reference/react-dom/server/renderToStati | 0.532 |
| playwright | #1 | react.dev/reference/react-dom/server/renderToStati | 0.605 | react.dev/reference/react-dom/server/renderToStati | 0.585 | react.dev/reference/react-dom/server/renderToStati | 0.532 |


**Q28: What are the parameters for renderToStaticMarkup?**
*(expects URL containing: `renderToStaticMarkup`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/understanding-your-ui-as-a-tree | 0.332 | react.dev/learn/build-a-react-app-from-scratch | 0.323 | react.dev/learn/render-and-commit | 0.299 |
| crawl4ai | #1 | react.dev/reference/react-dom/server/renderToStati | 0.529 | react.dev/reference/react-dom/server/renderToStati | 0.529 | react.dev/reference/react-dom/server/renderToStati | 0.473 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/server/renderToStati | 0.529 | react.dev/reference/react-dom/server/renderToStati | 0.529 | react.dev/reference/react-dom/server/renderToStati | 0.473 |
| scrapy+md | #1 | react.dev/reference/react-dom/server/renderToStati | 0.455 | react.dev/reference/react-dom/static/prerenderToNo | 0.388 | react.dev/reference/rsc/server-components | 0.387 |
| crawlee | #1 | react.dev/reference/react-dom/server/renderToStati | 0.537 | react.dev/reference/react-dom/server/renderToStati | 0.531 | react.dev/reference/react-dom/server/renderToStati | 0.501 |
| colly+md | #1 | react.dev/reference/react-dom/server/renderToStati | 0.537 | react.dev/reference/react-dom/server/renderToStati | 0.531 | react.dev/reference/react-dom/server/renderToStati | 0.501 |
| playwright | #1 | react.dev/reference/react-dom/server/renderToStati | 0.537 | react.dev/reference/react-dom/server/renderToStati | 0.531 | react.dev/reference/react-dom/server/renderToStati | 0.501 |


**Q29: What does the globals rule validate against in React?**
*(expects URL containing: `globals`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/react-compiler/introduction | 0.472 | react.dev/learn/lifecycle-of-reactive-effects | 0.471 | react.dev/learn/react-compiler/debugging | 0.461 |
| crawl4ai | #1 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.668 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.579 | react.dev/reference/rules | 0.573 |
| crawl4ai-raw | #1 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.668 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.579 | react.dev/reference/rules | 0.573 |
| scrapy+md | #1 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.653 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.556 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.534 |
| crawlee | #1 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.659 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.638 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.579 |
| colly+md | #1 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.659 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.638 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.579 |
| playwright | #1 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.659 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.638 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.579 |


**Q30: What are examples of invalid code for the globals rule?**
*(expects URL containing: `globals`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/react-compiler/debugging | 0.327 | react.dev/learn/react-compiler/debugging | 0.309 | react.dev/learn/choosing-the-state-structure | 0.297 |
| crawl4ai | #1 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.484 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.407 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.393 |
| crawl4ai-raw | #1 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.484 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.407 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.393 |
| scrapy+md | #1 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.454 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.399 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.369 |
| crawlee | #1 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.528 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.477 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.461 |
| colly+md | #1 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.528 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.477 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.461 |
| playwright | #1 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.528 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.477 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.461 |


**Q31: What does the `preconnect` function do?**
*(expects URL containing: `preconnect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/synchronizing-with-effects | 0.341 | react.dev/learn/lifecycle-of-reactive-effects | 0.315 | react.dev/learn/removing-effect-dependencies | 0.314 |
| crawl4ai | #1 | react.dev/reference/react-dom/preconnect | 0.584 | react.dev/reference/react-dom/preconnect | 0.569 | react.dev/reference/react-dom/preconnect | 0.551 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/preconnect | 0.584 | react.dev/reference/react-dom/preconnect | 0.569 | react.dev/reference/react-dom/preconnect | 0.551 |
| scrapy+md | #1 | react.dev/reference/react-dom/preconnect | 0.659 | react.dev/reference/react-dom/preconnect | 0.621 | react.dev/reference/react-dom/prefetchDNS | 0.486 |
| crawlee | #1 | react.dev/reference/react-dom/preconnect | 0.635 | react.dev/reference/react-dom/preconnect | 0.621 | react.dev/reference/react-dom/preconnect | 0.595 |
| colly+md | #1 | react.dev/reference/react-dom/preconnect | 0.635 | react.dev/reference/react-dom/preconnect | 0.621 | react.dev/reference/react-dom/preconnect | 0.594 |
| playwright | #1 | react.dev/reference/react-dom/preconnect | 0.635 | react.dev/reference/react-dom/preconnect | 0.621 | react.dev/reference/react-dom/preconnect | 0.594 |


**Q32: How can you call `preconnect` in an event handler?**
*(expects URL containing: `preconnect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/separating-events-from-effects | 0.382 | react.dev/learn/reusing-logic-with-custom-hooks | 0.382 | react.dev/learn/responding-to-events | 0.365 |
| crawl4ai | #1 | react.dev/reference/react-dom/preconnect | 0.562 | react.dev/reference/react-dom/preconnect | 0.556 | react.dev/reference/react-dom/preconnect | 0.547 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/preconnect | 0.562 | react.dev/reference/react-dom/preconnect | 0.556 | react.dev/reference/react-dom/preconnect | 0.547 |
| scrapy+md | #1 | react.dev/reference/react-dom/preconnect | 0.618 | react.dev/reference/react-dom/preconnect | 0.590 | react.dev/reference/react-dom/prefetchDNS | 0.476 |
| crawlee | #1 | react.dev/reference/react-dom/preconnect | 0.594 | react.dev/reference/react-dom/preconnect | 0.590 | react.dev/reference/react-dom/preconnect | 0.582 |
| colly+md | #1 | react.dev/reference/react-dom/preconnect | 0.594 | react.dev/reference/react-dom/preconnect | 0.590 | react.dev/reference/react-dom/preconnect | 0.582 |
| playwright | #1 | react.dev/reference/react-dom/preconnect | 0.594 | react.dev/reference/react-dom/preconnect | 0.590 | react.dev/reference/react-dom/preconnect | 0.582 |


**Q33: What are the special React props supported for all built-in components?**
*(expects URL containing: `common`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/passing-props-to-a-component | 0.574 | react.dev/learn/typescript | 0.574 | react.dev/learn/typescript | 0.561 |
| crawl4ai | #1 | react.dev/reference/react-dom/components/common | 0.658 | react.dev/reference/react-dom/components | 0.656 | react.dev/reference/react-dom/components/common | 0.654 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/components/common | 0.658 | react.dev/reference/react-dom/components | 0.656 | react.dev/reference/react-dom/components/common | 0.654 |
| scrapy+md | #1 | react.dev/reference/react-dom/components/common | 0.680 | react.dev/reference/react-dom/components | 0.660 | react.dev/reference/react-dom/components/common | 0.624 |
| crawlee | #1 | react.dev/reference/react-dom/components/common | 0.680 | react.dev/reference/react/components | 0.648 | react.dev/reference/react-dom/components | 0.645 |
| colly+md | #1 | react.dev/reference/react-dom/components/common#co | 0.680 | react.dev/reference/react-dom/components/common | 0.680 | react.dev/reference/react-dom/components/common#re | 0.680 |
| playwright | #1 | react.dev/reference/react-dom/components/common | 0.680 | react.dev/reference/react/components | 0.648 | react.dev/reference/react-dom/components | 0.645 |


**Q34: What does the `dangerouslySetInnerHTML` prop do in React components?**
*(expects URL containing: `common`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/keeping-components-pure | 0.484 | react.dev/learn/render-and-commit | 0.467 | react.dev/learn/writing-markup-with-jsx | 0.467 |
| crawl4ai | #1 | react.dev/reference/react-dom/components/common | 0.655 | react.dev/reference/react-dom/components/common | 0.591 | react.dev/reference/react-dom/components/common | 0.570 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/components/common | 0.655 | react.dev/reference/react-dom/components/common | 0.591 | react.dev/reference/react-dom/components/common | 0.570 |
| scrapy+md | #1 | react.dev/reference/react-dom/components/common | 0.638 | react.dev/reference/react-dom/components/common | 0.624 | react.dev/reference/react-dom/components/link | 0.508 |
| crawlee | #1 | react.dev/reference/react-dom/components/common | 0.638 | react.dev/reference/react-dom/components/common | 0.624 | react.dev/reference/react-dom/components/common | 0.599 |
| colly+md | #1 | react.dev/reference/react-dom/components/common | 0.638 | react.dev/reference/react-dom/components/common#co | 0.638 | react.dev/reference/react-dom/components/common#re | 0.638 |
| playwright | #1 | react.dev/reference/react-dom/components/common | 0.638 | react.dev/reference/react-dom/components/common | 0.624 | react.dev/reference/react-dom/components/common | 0.599 |


**Q35: Who leads the React development team?**
*(expects URL containing: `team`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/react-developer-tools | 0.518 | react.dev/learn/setup | 0.515 | react.dev/learn/react-compiler | 0.504 |
| crawl4ai | #1 | he.react.dev/community/team | 0.745 | de.react.dev/community/team | 0.737 | he.react.dev/community/acknowledgements | 0.726 |
| crawl4ai-raw | #1 | he.react.dev/community/team | 0.745 | de.react.dev/community/team | 0.737 | he.react.dev/community/acknowledgements | 0.726 |
| scrapy+md | #1 | react.dev/community/team | 0.662 | react.dev/ | 0.636 | react.dev/community/team | 0.628 |
| crawlee | #1 | react.dev/community/team | 0.674 | react.dev/community/team | 0.661 | react.dev/ | 0.645 |
| colly+md | #1 | react.dev/community/team | 0.674 | react.dev/community/team | 0.661 | react.dev/ | 0.645 |
| playwright | #1 | react.dev/community/team | 0.674 | react.dev/community/team | 0.661 | react.dev/ | 0.645 |


**Q36: What roles do the current members of the React Core team work on?**
*(expects URL containing: `team`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/creating-a-react-app | 0.527 | react.dev/learn/react-compiler | 0.499 | react.dev/learn/setup | 0.496 |
| crawl4ai | #1 | he.react.dev/community/team | 0.704 | de.react.dev/community/team | 0.694 | react.dev/community/team | 0.683 |
| crawl4ai-raw | #1 | he.react.dev/community/team | 0.704 | de.react.dev/community/team | 0.694 | react.dev/community/team | 0.683 |
| scrapy+md | #1 | react.dev/community/team | 0.658 | react.dev/blog/2026/02/24/the-react-foundation | 0.593 | react.dev/community/team | 0.593 |
| crawlee | #1 | react.dev/community/team | 0.662 | react.dev/community/team | 0.618 | react.dev/blog/2024/02/15/react-labs-what-we-have- | 0.610 |
| colly+md | #1 | react.dev/community/team | 0.662 | react.dev/community/team | 0.618 | react.dev/blog/2024/02/15/react-labs-what-we-have- | 0.610 |
| playwright | #1 | react.dev/community/team | 0.662 | react.dev/community/team | 0.618 | react.dev/blog/2024/02/15/react-labs-what-we-have- | 0.610 |


**Q37: What does renderToReadableStream do?**
*(expects URL containing: `renderToReadableStream`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/understanding-your-ui-as-a-tree | 0.290 | react.dev/learn/synchronizing-with-effects | 0.285 | react.dev/learn/render-and-commit | 0.278 |
| crawl4ai | #1 | react.dev/reference/react-dom/server/renderToReada | 0.562 | react.dev/reference/react-dom/server/renderToPipea | 0.519 | 18.react.dev/reference/react-dom/server/renderToNo | 0.492 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/server/renderToReada | 0.562 | react.dev/reference/react-dom/server/renderToPipea | 0.519 | 18.react.dev/reference/react-dom/server/renderToNo | 0.492 |
| scrapy+md | #1 | react.dev/reference/react-dom/server/renderToReada | 0.557 | react.dev/reference/react-dom/server/renderToReada | 0.507 | react.dev/reference/react-dom/server/renderToPipea | 0.468 |
| crawlee | #1 | react.dev/reference/react-dom/server/renderToReada | 0.586 | react.dev/reference/react-dom/server/renderToReada | 0.517 | react.dev/reference/react-dom/server/renderToPipea | 0.517 |
| colly+md | #1 | react.dev/reference/react-dom/server/renderToReada | 0.586 | react.dev/reference/react-dom/server/renderToReada | 0.517 | react.dev/reference/react-dom/server/renderToPipea | 0.517 |
| playwright | #1 | react.dev/reference/react-dom/server/renderToReada | 0.586 | react.dev/reference/react-dom/server/renderToReada | 0.517 | react.dev/reference/react-dom/server/renderToPipea | 0.517 |


**Q38: What parameters can be passed to renderToReadableStream?**
*(expects URL containing: `renderToReadableStream`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/understanding-your-ui-as-a-tree | 0.308 | react.dev/learn/build-a-react-app-from-scratch | 0.298 | react.dev/learn/keeping-components-pure | 0.253 |
| crawl4ai | #1 | react.dev/reference/react-dom/server/renderToReada | 0.507 | react.dev/reference/react-dom/server/renderToPipea | 0.484 | react.dev/reference/react-dom/server/renderToReada | 0.473 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/server/renderToReada | 0.507 | react.dev/reference/react-dom/server/renderToPipea | 0.484 | react.dev/reference/react-dom/server/renderToReada | 0.473 |
| scrapy+md | #1 | react.dev/reference/react-dom/server/renderToReada | 0.496 | react.dev/reference/react-dom/server/renderToReada | 0.459 | react.dev/reference/react-dom/server/renderToPipea | 0.440 |
| crawlee | #1 | react.dev/reference/react-dom/server/renderToReada | 0.518 | react.dev/reference/react-dom/server/renderToReada | 0.476 | react.dev/reference/react-dom/server/renderToPipea | 0.474 |
| colly+md | #1 | react.dev/reference/react-dom/server/renderToReada | 0.518 | react.dev/reference/react-dom/server/renderToReada | 0.476 | react.dev/reference/react-dom/server/renderToPipea | 0.473 |
| playwright | #1 | react.dev/reference/react-dom/server/renderToReada | 0.518 | react.dev/reference/react-dom/server/renderToReada | 0.476 | react.dev/reference/react-dom/server/renderToPipea | 0.473 |


**Q39: What do the `react-dom/server` APIs do?**
*(expects URL containing: `server`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/creating-a-react-app | 0.524 | react.dev/learn/add-react-to-an-existing-project | 0.520 | react.dev/learn/add-react-to-an-existing-project | 0.512 |
| crawl4ai | #2 | de.react.dev/reference/react-dom | 0.662 | react.dev/reference/react-dom/server | 0.659 | react.dev/reference/rsc/server-components | 0.650 |
| crawl4ai-raw | #2 | de.react.dev/reference/react-dom | 0.662 | react.dev/reference/react-dom/server | 0.659 | react.dev/reference/rsc/server-components | 0.650 |
| scrapy+md | #1 | react.dev/reference/react-dom/server | 0.657 | react.dev/reference/react-dom/client | 0.610 | react.dev/reference/react-dom | 0.605 |
| crawlee | #4 | react.dev/blog/2024/12/05/react-19 | 0.648 | react.dev/blog/2024/04/25/react-19#ref-as-a-prop | 0.648 | react.dev/reference/react-dom | 0.630 |
| colly+md | #3 | react.dev/blog/2024/12/05/react-19 | 0.649 | react.dev/reference/react-dom | 0.630 | react.dev/reference/react-dom/server | 0.617 |
| playwright | #4 | react.dev/blog/2024/04/25/react-19 | 0.648 | react.dev/blog/2024/12/05/react-19 | 0.648 | react.dev/reference/react-dom | 0.630 |


**Q40: What methods are available for Node.js Streams in the `react-dom/server` APIs?**
*(expects URL containing: `server`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/escape-hatches | 0.480 | react.dev/learn/creating-a-react-app | 0.479 | react.dev/learn/manipulating-the-dom-with-refs | 0.464 |
| crawl4ai | #1 | react.dev/reference/react-dom/server | 0.690 | react.dev/reference/react-dom/server | 0.658 | react.dev/reference/react-dom/server/renderToReada | 0.657 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/server | 0.690 | react.dev/reference/react-dom/server | 0.658 | react.dev/reference/react-dom/server/renderToReada | 0.657 |
| scrapy+md | #1 | react.dev/reference/react-dom/server/renderToReada | 0.660 | react.dev/blog/2024/12/05/react-19 | 0.639 | react.dev/reference/react-dom/server/renderToPipea | 0.635 |
| crawlee | #1 | react.dev/reference/react-dom/server | 0.672 | react.dev/reference/react-dom/server/renderToReada | 0.658 | react.dev/reference/react-dom/server/renderToPipea | 0.649 |
| colly+md | #1 | react.dev/reference/react-dom/server | 0.672 | react.dev/reference/react-dom/server/renderToReada | 0.658 | react.dev/reference/react-dom/server/renderToPipea | 0.649 |
| playwright | #1 | react.dev/reference/react-dom/server | 0.672 | react.dev/reference/react-dom/server/renderToReada | 0.658 | react.dev/reference/react-dom/server/renderToPipea | 0.649 |


**Q41: What does the `preinit` function do?**
*(expects URL containing: `preinit`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/you-might-not-need-an-effect | 0.375 | react.dev/learn/synchronizing-with-effects | 0.351 | react.dev/learn/build-a-react-app-from-scratch | 0.317 |
| crawl4ai | #1 | react.dev/reference/react-dom/preinit | 0.594 | react.dev/reference/react-dom/preinit | 0.571 | react.dev/reference/react-dom/preinitModule | 0.564 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/preinit | 0.594 | react.dev/reference/react-dom/preinit | 0.571 | react.dev/reference/react-dom/preinitModule | 0.564 |
| scrapy+md | #1 | react.dev/reference/react-dom/preinit | 0.617 | react.dev/reference/react-dom/preinit | 0.579 | react.dev/reference/react-dom/preinitModule | 0.552 |
| crawlee | #1 | react.dev/reference/react-dom/preinit | 0.622 | react.dev/reference/react-dom/preinitModule | 0.568 | react.dev/reference/react-dom/preinit | 0.566 |
| colly+md | #1 | react.dev/reference/react-dom/preinit | 0.622 | react.dev/reference/react-dom/preinitModule | 0.568 | react.dev/reference/react-dom/preinit | 0.567 |
| playwright | #1 | react.dev/reference/react-dom/preinit | 0.622 | react.dev/reference/react-dom/preinitModule | 0.568 | react.dev/reference/react-dom/preinit | 0.567 |


**Q42: What parameters does the `preinit` function accept?**
*(expects URL containing: `preinit`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/build-a-react-app-from-scratch | 0.285 | react.dev/learn/you-might-not-need-an-effect | 0.270 | react.dev/learn/synchronizing-with-effects | 0.269 |
| crawl4ai | #1 | react.dev/reference/react-dom/preinit | 0.550 | react.dev/reference/react-dom/preinit | 0.507 | react.dev/reference/react-dom/preinitModule | 0.494 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/preinit | 0.550 | react.dev/reference/react-dom/preinit | 0.507 | react.dev/reference/react-dom/preinitModule | 0.494 |
| scrapy+md | #1 | react.dev/reference/react-dom/preinit | 0.551 | react.dev/reference/react-dom/preinit | 0.528 | react.dev/reference/react-dom/preinitModule | 0.468 |
| crawlee | #1 | react.dev/reference/react-dom/preinit | 0.537 | react.dev/reference/react-dom/preinit | 0.513 | react.dev/reference/react-dom/preinit | 0.510 |
| colly+md | #1 | react.dev/reference/react-dom/preinit | 0.537 | react.dev/reference/react-dom/preinit | 0.513 | react.dev/reference/react-dom/preinit | 0.510 |
| playwright | #1 | react.dev/reference/react-dom/preinit | 0.537 | react.dev/reference/react-dom/preinit | 0.513 | react.dev/reference/react-dom/preinit | 0.510 |


**Q43: What is the main topic of the videos dedicated to React?**
*(expects URL containing: `videos`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/writing-markup-with-jsx | 0.572 | react.dev/learn/your-first-component | 0.562 | react.dev/learn/describing-the-ui | 0.561 |
| crawl4ai | #5 | he.react.dev/ | 0.693 | ru.react.dev/ | 0.682 | hi.react.dev/ | 0.682 |
| crawl4ai-raw | #5 | he.react.dev/ | 0.693 | ru.react.dev/ | 0.682 | hi.react.dev/ | 0.682 |
| scrapy+md | #1 | react.dev/community/videos | 0.647 | react.dev/ | 0.646 | react.dev/ | 0.645 |
| crawlee | #1 | react.dev/community/videos | 0.660 | react.dev/ | 0.646 | react.dev/ | 0.645 |
| colly+md | #1 | react.dev/community/videos | 0.660 | react.dev/ | 0.646 | react.dev/ | 0.645 |
| playwright | #1 | react.dev/community/videos | 0.660 | react.dev/ | 0.646 | react.dev/ | 0.645 |


**Q44: Who shared a welcome message at React Conf 2024?**
*(expects URL containing: `videos`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/creating-a-react-app | 0.446 | react.dev/learn/setup | 0.436 | react.dev/learn/react-compiler | 0.432 |
| crawl4ai | #45 | conf2024.react.dev/talks | 0.719 | az.react.dev/blog/2024/05/22/react-conf-2024-recap | 0.699 | he.react.dev/blog/2024/02/15/react-labs-what-we-ha | 0.699 |
| crawl4ai-raw | #45 | conf2024.react.dev/talks | 0.719 | az.react.dev/blog/2024/05/22/react-conf-2024-recap | 0.699 | he.react.dev/blog/2024/02/15/react-labs-what-we-ha | 0.699 |
| scrapy+md | #2 | react.dev/blog/2024/05/22/react-conf-2024-recap | 0.666 | react.dev/community/videos | 0.659 | react.dev/blog/2024/05/22/react-conf-2024-recap | 0.648 |
| crawlee | #7 | react.dev/blog/2024/05/22/react-conf-2024-recap | 0.686 | react.dev/blog/2024/05/22/react-conf-2024-recap | 0.666 | react.dev/blog/2024/05/22/react-conf-2024-recap | 0.662 |
| colly+md | #7 | react.dev/blog/2024/05/22/react-conf-2024-recap | 0.686 | react.dev/blog/2024/05/22/react-conf-2024-recap | 0.666 | react.dev/blog/2024/05/22/react-conf-2024-recap | 0.662 |
| playwright | #7 | react.dev/blog/2024/05/22/react-conf-2024-recap | 0.686 | react.dev/blog/2024/05/22/react-conf-2024-recap | 0.666 | react.dev/blog/2024/05/22/react-conf-2024-recap | 0.662 |


**Q45: What is React Compiler?**
*(expects URL containing: `introduction`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/react-compiler/introduction | 0.699 | react.dev/learn/react-compiler | 0.692 | react.dev/learn/react-compiler/introduction | 0.660 |
| crawl4ai | #12 | he.react.dev/blog/2024/02/15/react-labs-what-we-ha | 0.737 | az.react.dev/blog/2024/02/15/react-labs-what-we-ha | 0.736 | ar.react.dev/blog/2025/10/07/react-compiler-1 | 0.721 |
| crawl4ai-raw | #12 | he.react.dev/blog/2024/02/15/react-labs-what-we-ha | 0.737 | az.react.dev/blog/2024/02/15/react-labs-what-we-ha | 0.736 | ar.react.dev/blog/2025/10/07/react-compiler-1 | 0.721 |
| scrapy+md | #1 | react.dev/learn/react-compiler/introduction | 0.725 | react.dev/blog/2024/02/15/react-labs-what-we-have- | 0.705 | react.dev/learn/react-compiler/introduction | 0.694 |
| crawlee | #1 | react.dev/learn/react-compiler/introduction | 0.713 | react.dev/blog/2024/02/15/react-labs-what-we-have- | 0.705 | react.dev/learn/react-compiler/introduction | 0.694 |
| colly+md | #1 | react.dev/learn/react-compiler/introduction | 0.713 | react.dev/blog/2024/02/15/react-labs-what-we-have- | 0.705 | react.dev/learn/react-compiler/introduction | 0.694 |
| playwright | #1 | react.dev/learn/react-compiler/introduction | 0.713 | react.dev/blog/2024/02/15/react-labs-what-we-have- | 0.705 | react.dev/learn/react-compiler/introduction | 0.694 |


**Q46: How does React Compiler optimize re-renders?**
*(expects URL containing: `introduction`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/react-compiler/introduction | 0.697 | react.dev/learn/react-compiler/introduction | 0.674 | react.dev/learn/react-compiler/introduction | 0.642 |
| crawl4ai | #1 | react.dev/learn/react-compiler/introduction | 0.710 | he.react.dev/blog/2024/02/15/react-labs-what-we-ha | 0.696 | az.react.dev/blog/2024/02/15/react-labs-what-we-ha | 0.695 |
| crawl4ai-raw | #1 | react.dev/learn/react-compiler/introduction | 0.710 | he.react.dev/blog/2024/02/15/react-labs-what-we-ha | 0.696 | az.react.dev/blog/2024/02/15/react-labs-what-we-ha | 0.695 |
| scrapy+md | #1 | react.dev/learn/react-compiler/introduction | 0.705 | react.dev/learn/react-compiler/introduction | 0.696 | react.dev/blog/2024/02/15/react-labs-what-we-have- | 0.680 |
| crawlee | #1 | react.dev/learn/react-compiler/introduction | 0.701 | react.dev/learn/react-compiler/introduction | 0.696 | react.dev/reference/react/memo | 0.692 |
| colly+md | #1 | react.dev/learn/react-compiler/introduction | 0.701 | react.dev/learn/react-compiler/introduction | 0.696 | react.dev/reference/react/memo | 0.692 |
| playwright | #1 | react.dev/learn/react-compiler/introduction | 0.701 | react.dev/learn/react-compiler/introduction | 0.696 | react.dev/reference/react/memo | 0.692 |


**Q47: What does the `prerender` function do?**
*(expects URL containing: `prerender`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/render-and-commit | 0.426 | react.dev/learn/render-and-commit | 0.423 | react.dev/learn/understanding-your-ui-as-a-tree | 0.391 |
| crawl4ai | #1 | react.dev/reference/react-dom/static/prerender | 0.678 | react.dev/reference/react-dom/static/resumeAndPrer | 0.605 | react.dev/reference/react-dom/static/prerenderToNo | 0.602 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/static/prerender | 0.678 | react.dev/reference/react-dom/static/resumeAndPrer | 0.605 | react.dev/reference/react-dom/static/prerenderToNo | 0.602 |
| scrapy+md | #1 | react.dev/reference/react-dom/static/prerender | 0.691 | react.dev/reference/react-dom/static/prerenderToNo | 0.607 | react.dev/reference/react-dom/static/prerender | 0.602 |
| crawlee | #1 | react.dev/reference/react-dom/static/prerender | 0.691 | react.dev/reference/react-dom/static/prerender | 0.633 | react.dev/reference/react-dom/static/resumeAndPrer | 0.633 |
| colly+md | #1 | react.dev/reference/react-dom/static/prerender | 0.691 | react.dev/reference/react-dom/static/prerender | 0.633 | react.dev/reference/react-dom/static/resumeAndPrer | 0.633 |
| playwright | #1 | react.dev/reference/react-dom/static/prerender | 0.691 | react.dev/reference/react-dom/static/prerender | 0.633 | react.dev/reference/react-dom/static/resumeAndPrer | 0.633 |


**Q48: What parameters can be passed to the `prerender` function?**
*(expects URL containing: `prerender`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/understanding-your-ui-as-a-tree | 0.374 | react.dev/learn/render-and-commit | 0.357 | react.dev/learn/build-a-react-app-from-scratch | 0.355 |
| crawl4ai | #1 | react.dev/reference/react-dom/static/prerender | 0.639 | react.dev/reference/react-dom/static/resumeAndPrer | 0.615 | react.dev/reference/react-dom/static/prerender | 0.584 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/static/prerender | 0.639 | react.dev/reference/react-dom/static/resumeAndPrer | 0.615 | react.dev/reference/react-dom/static/prerender | 0.584 |
| scrapy+md | #1 | react.dev/reference/react-dom/static/prerender | 0.670 | react.dev/reference/react-dom/static/prerenderToNo | 0.595 | react.dev/reference/react-dom/static/prerender | 0.542 |
| crawlee | #1 | react.dev/reference/react-dom/static/prerender | 0.670 | react.dev/reference/react-dom/static/prerenderToNo | 0.595 | react.dev/reference/react-dom/static/prerender | 0.583 |
| colly+md | #1 | react.dev/reference/react-dom/static/prerender | 0.670 | react.dev/reference/react-dom/static/prerenderToNo | 0.595 | react.dev/reference/react-dom/static/prerender | 0.583 |
| playwright | #1 | react.dev/reference/react-dom/static/prerender | 0.670 | react.dev/reference/react-dom/static/prerenderToNo | 0.595 | react.dev/reference/react-dom/static/prerender | 0.583 |


**Q49: What does the built-in browser `<meta>` component do?**
*(expects URL containing: `meta`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/your-first-component | 0.412 | react.dev/learn/react-compiler/introduction | 0.401 | react.dev/learn/react-compiler | 0.384 |
| crawl4ai | #1 | react.dev/reference/react-dom/components/meta | 0.559 | react.dev/reference/react-dom/components/meta | 0.539 | react.dev/reference/react-dom/components/meta | 0.528 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/components/meta | 0.559 | react.dev/reference/react-dom/components/meta | 0.539 | react.dev/reference/react-dom/components/meta | 0.528 |
| scrapy+md | #1 | react.dev/reference/react-dom/components/meta | 0.667 | react.dev/reference/react-dom/components/meta | 0.561 | react.dev/blog/2023/03/22/react-labs-what-we-have- | 0.518 |
| crawlee | #1 | react.dev/reference/react-dom/components/meta | 0.557 | react.dev/reference/react-dom/components/meta | 0.540 | react.dev/blog/2023/03/22/react-labs-what-we-have- | 0.518 |
| colly+md | #1 | react.dev/reference/react-dom/components/meta | 0.557 | react.dev/reference/react-dom/components/meta | 0.540 | react.dev/blog/2023/03/22/react-labs-what-we-have- | 0.518 |
| playwright | #1 | react.dev/reference/react-dom/components/meta | 0.557 | react.dev/reference/react-dom/components/meta | 0.540 | react.dev/blog/2023/03/22/react-labs-what-we-have- | 0.518 |


**Q50: What props does the `<meta>` component support?**
*(expects URL containing: `meta`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/passing-props-to-a-component | 0.476 | react.dev/learn/passing-props-to-a-component | 0.452 | react.dev/learn/passing-props-to-a-component | 0.449 |
| crawl4ai | #1 | react.dev/reference/react-dom/components/meta | 0.652 | react.dev/reference/react-dom/components/meta | 0.627 | react.dev/reference/react-dom/components/meta | 0.601 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/components/meta | 0.652 | react.dev/reference/react-dom/components/meta | 0.627 | react.dev/reference/react-dom/components/meta | 0.601 |
| scrapy+md | #1 | react.dev/reference/react-dom/components/meta | 0.688 | react.dev/reference/react-dom/components/meta | 0.645 | react.dev/reference/react-dom/components | 0.563 |
| crawlee | #1 | react.dev/reference/react-dom/components/meta | 0.677 | react.dev/reference/react-dom/components/meta | 0.610 | react.dev/reference/react-dom/components/meta | 0.605 |
| colly+md | #1 | react.dev/reference/react-dom/components/meta | 0.677 | react.dev/reference/react-dom/components/meta | 0.610 | react.dev/reference/react-dom/components/meta | 0.605 |
| playwright | #1 | react.dev/reference/react-dom/components/meta | 0.677 | react.dev/reference/react-dom/components/meta | 0.610 | react.dev/reference/react-dom/components/meta | 0.605 |


**Q51: What is the purpose of forwardRef in React?**
*(expects URL containing: `forwardRef`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/manipulating-the-dom-with-refs | 0.628 | react.dev/learn/referencing-values-with-refs | 0.624 | react.dev/learn/escape-hatches | 0.595 |
| crawl4ai | #1 | react.dev/reference/react/forwardRef | 0.709 | react.dev/reference/react/forwardRef | 0.699 | react.dev/reference/react/forwardRef | 0.670 |
| crawl4ai-raw | #1 | react.dev/reference/react/forwardRef | 0.709 | react.dev/reference/react/forwardRef | 0.699 | react.dev/reference/react/forwardRef | 0.670 |
| scrapy+md | #1 | react.dev/reference/react/forwardRef | 0.706 | react.dev/reference/react/forwardRef | 0.675 | react.dev/reference/react/forwardRef | 0.640 |
| crawlee | #1 | react.dev/reference/react/forwardRef | 0.698 | react.dev/reference/react/forwardRef | 0.696 | react.dev/reference/react/forwardRef | 0.684 |
| colly+md | #1 | react.dev/reference/react/forwardRef | 0.698 | react.dev/reference/react/forwardRef | 0.696 | react.dev/reference/react/forwardRef | 0.685 |
| playwright | #1 | react.dev/reference/react/forwardRef | 0.698 | react.dev/reference/react/forwardRef | 0.696 | react.dev/reference/react/forwardRef | 0.684 |


**Q52: How do you expose a DOM node to the parent component using forwardRef?**
*(expects URL containing: `forwardRef`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/manipulating-the-dom-with-refs | 0.574 | react.dev/learn/manipulating-the-dom-with-refs | 0.573 | react.dev/learn/manipulating-the-dom-with-refs | 0.566 |
| crawl4ai | #1 | react.dev/reference/react/forwardRef | 0.714 | react.dev/reference/react/forwardRef | 0.681 | react.dev/reference/react/forwardRef | 0.665 |
| crawl4ai-raw | #1 | react.dev/reference/react/forwardRef | 0.714 | react.dev/reference/react/forwardRef | 0.681 | react.dev/reference/react/forwardRef | 0.665 |
| scrapy+md | #1 | react.dev/reference/react/forwardRef | 0.663 | react.dev/reference/react/forwardRef | 0.654 | react.dev/reference/react/forwardRef | 0.622 |
| crawlee | #1 | react.dev/reference/react/forwardRef | 0.708 | react.dev/reference/react/forwardRef | 0.691 | react.dev/reference/react/forwardRef | 0.654 |
| colly+md | #1 | react.dev/reference/react/forwardRef | 0.709 | react.dev/reference/react/forwardRef | 0.692 | react.dev/reference/react/forwardRef | 0.654 |
| playwright | #1 | react.dev/reference/react/forwardRef | 0.708 | react.dev/reference/react/forwardRef | 0.691 | react.dev/reference/react/forwardRef | 0.654 |


**Q53: What is the reason for deprecating Create React App?**
*(expects URL containing: `sunsetting-create-react-app`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/installation | 0.537 | react.dev/learn/build-a-react-app-from-scratch | 0.529 | react.dev/learn/build-a-react-app-from-scratch | 0.526 |
| crawl4ai | #1 | react.dev/blog/2025/02/14/sunsetting-create-react- | 0.744 | de.react.dev/blog/2025/02/14/sunsetting-create-rea | 0.730 | de.react.dev/blog/2025/02/14/sunsetting-create-rea | 0.677 |
| crawl4ai-raw | #1 | react.dev/blog/2025/02/14/sunsetting-create-react- | 0.744 | de.react.dev/blog/2025/02/14/sunsetting-create-rea | 0.730 | de.react.dev/blog/2025/02/14/sunsetting-create-rea | 0.677 |
| scrapy+md | #1 | react.dev/blog/2025/02/14/sunsetting-create-react- | 0.766 | react.dev/blog/2025/02/14/sunsetting-create-react- | 0.581 | react.dev/blog/2024/04/25/react-19-upgrade-guide | 0.559 |
| crawlee | #1 | react.dev/blog/2025/02/14/sunsetting-create-react- | 0.756 | react.dev/blog/2025/02/14/sunsetting-create-react- | 0.723 | react.dev/blog/2025/02/14/sunsetting-create-react- | 0.654 |
| colly+md | #1 | react.dev/blog/2025/02/14/sunsetting-create-react- | 0.756 | react.dev/blog/2025/02/14/sunsetting-create-react- | 0.722 | react.dev/blog/2025/02/14/sunsetting-create-react- | 0.654 |
| playwright | #1 | react.dev/blog/2025/02/14/sunsetting-create-react- | 0.756 | react.dev/blog/2025/02/14/sunsetting-create-react- | 0.723 | react.dev/blog/2025/02/14/sunsetting-create-react- | 0.654 |


**Q54: What are the recommended frameworks for creating new React apps?**
*(expects URL containing: `sunsetting-create-react-app`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/build-a-react-app-from-scratch | 0.687 | react.dev/learn/build-a-react-app-from-scratch | 0.681 | react.dev/learn/creating-a-react-app | 0.667 |
| crawl4ai | #14 | tr.react.dev/learn/creating-a-react-app | 0.705 | de.react.dev/learn/start-a-new-react-project | 0.702 | tr.react.dev/learn/creating-a-react-app | 0.702 |
| crawl4ai-raw | #14 | tr.react.dev/learn/creating-a-react-app | 0.705 | de.react.dev/learn/start-a-new-react-project | 0.702 | tr.react.dev/learn/creating-a-react-app | 0.702 |
| scrapy+md | #2 | react.dev/learn/build-a-react-app-from-scratch | 0.687 | react.dev/blog/2025/02/14/sunsetting-create-react- | 0.669 | react.dev/learn/creating-a-react-app | 0.658 |
| crawlee | #4 | react.dev/learn/creating-a-react-app | 0.704 | react.dev/learn/creating-a-react-app | 0.681 | react.dev/learn/build-a-react-app-from-scratch | 0.677 |
| colly+md | #7 | react.dev/learn/creating-a-react-app | 0.704 | react.dev/learn/creating-a-react-app#full-stack-fr | 0.704 | react.dev/learn/creating-a-react-app | 0.681 |
| playwright | #4 | react.dev/learn/creating-a-react-app | 0.704 | react.dev/learn/creating-a-react-app | 0.681 | react.dev/learn/build-a-react-app-from-scratch | 0.677 |


**Q55: What is the purpose of the useEffectEvent hook?**
*(expects URL containing: `useEffectEvent`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/separating-events-from-effects | 0.535 | react.dev/learn/separating-events-from-effects | 0.519 | react.dev/learn/reusing-logic-with-custom-hooks | 0.511 |
| crawl4ai | #3 | react.dev/blog/2025/10/01/react-19-2 | 0.610 | ar.react.dev/blog/2025/10/01/react-19-2 | 0.609 | react.dev/reference/react/useEffectEvent | 0.595 |
| crawl4ai-raw | #3 | react.dev/blog/2025/10/01/react-19-2 | 0.610 | ar.react.dev/blog/2025/10/01/react-19-2 | 0.609 | react.dev/reference/react/useEffectEvent | 0.595 |
| scrapy+md | #2 | react.dev/blog/2025/10/01/react-19-2 | 0.603 | react.dev/reference/react/useEffectEvent | 0.601 | react.dev/reference/react/useEffectEvent | 0.581 |
| crawlee | #1 | react.dev/reference/react/useEffectEvent | 0.611 | react.dev/blog/2025/10/01/react-19-2 | 0.603 | react.dev/reference/react/useEffectEvent | 0.587 |
| colly+md | #1 | react.dev/reference/react/useEffectEvent | 0.611 | react.dev/blog/2025/10/01/react-19-2 | 0.603 | react.dev/reference/react/useEffectEvent | 0.587 |
| playwright | #1 | react.dev/reference/react/useEffectEvent | 0.611 | react.dev/blog/2025/10/01/react-19-2 | 0.603 | react.dev/reference/react/useEffectEvent | 0.587 |


**Q56: How does useEffectEvent handle the latest values from render?**
*(expects URL containing: `useEffectEvent`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/separating-events-from-effects | 0.504 | react.dev/learn/separating-events-from-effects | 0.503 | react.dev/learn/you-might-not-need-an-effect | 0.500 |
| crawl4ai | #1 | react.dev/reference/react/useEffectEvent | 0.612 | react.dev/reference/react/useEffectEvent | 0.576 | react.dev/reference/react/useEffect | 0.565 |
| crawl4ai-raw | #1 | react.dev/reference/react/useEffectEvent | 0.612 | react.dev/reference/react/useEffectEvent | 0.576 | react.dev/reference/react/useEffect | 0.565 |
| scrapy+md | #1 | react.dev/reference/react/useEffectEvent | 0.572 | react.dev/reference/react/useEffectEvent | 0.559 | react.dev/reference/react/useEffectEvent | 0.546 |
| crawlee | #1 | react.dev/reference/react/useEffectEvent | 0.609 | react.dev/reference/react/useEffectEvent | 0.571 | react.dev/reference/react/useEffectEvent | 0.570 |
| colly+md | #1 | react.dev/reference/react/useEffectEvent | 0.609 | react.dev/reference/react/useEffectEvent | 0.572 | react.dev/reference/react/useEffectEvent | 0.571 |
| playwright | #1 | react.dev/reference/react/useEffectEvent | 0.609 | react.dev/reference/react/useEffectEvent | 0.572 | react.dev/reference/react/useEffectEvent | 0.571 |


**Q57: What does `Children.count(children)` do?**
*(expects URL containing: `Children`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/passing-props-to-a-component | 0.362 | react.dev/learn/preserving-and-resetting-state | 0.352 | react.dev/learn/preserving-and-resetting-state | 0.342 |
| crawl4ai | #1 | react.dev/reference/react/Children | 0.631 | react.dev/reference/react/Children | 0.516 | react.dev/reference/react/Children | 0.504 |
| crawl4ai-raw | #1 | react.dev/reference/react/Children | 0.631 | react.dev/reference/react/Children | 0.516 | react.dev/reference/react/Children | 0.504 |
| scrapy+md | #1 | react.dev/reference/react/Children | 0.536 | react.dev/reference/react/Children | 0.515 | react.dev/reference/react/Children | 0.489 |
| crawlee | #1 | react.dev/reference/react/Children | 0.659 | react.dev/reference/react/Children | 0.550 | react.dev/reference/react/Children | 0.535 |
| colly+md | #1 | react.dev/reference/react/Children | 0.658 | react.dev/reference/react/Children | 0.550 | react.dev/reference/react/Children | 0.535 |
| playwright | #1 | react.dev/reference/react/Children | 0.659 | react.dev/reference/react/Children | 0.550 | react.dev/reference/react/Children | 0.535 |


**Q58: How can you transform the children JSX received by a component?**
*(expects URL containing: `Children`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/passing-props-to-a-component | 0.604 | react.dev/learn/passing-props-to-a-component | 0.598 | react.dev/learn/writing-markup-with-jsx | 0.596 |
| crawl4ai | #1 | react.dev/reference/react/Children | 0.626 | react.dev/learn/passing-props-to-a-component | 0.614 | react.dev/learn/describing-the-ui | 0.596 |
| crawl4ai-raw | #1 | react.dev/reference/react/Children | 0.626 | react.dev/learn/passing-props-to-a-component | 0.614 | react.dev/learn/describing-the-ui | 0.596 |
| scrapy+md | #2 | react.dev/learn/passing-props-to-a-component | 0.603 | react.dev/reference/react/Children | 0.603 | react.dev/learn/passing-props-to-a-component | 0.593 |
| crawlee | #5 | react.dev/learn/writing-markup-with-jsx | 0.613 | react.dev/learn/passing-props-to-a-component | 0.603 | react.dev/reference/rules/components-and-hooks-mus | 0.602 |
| colly+md | #7 | react.dev/learn/writing-markup-with-jsx | 0.613 | react.dev/learn/passing-props-to-a-component | 0.603 | react.dev/learn/passing-props-to-a-component#passi | 0.603 |
| playwright | #5 | react.dev/learn/writing-markup-with-jsx | 0.613 | react.dev/learn/passing-props-to-a-component | 0.603 | react.dev/reference/rules/components-and-hooks-mus | 0.602 |


</details>

## rust-book

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 35% (21/60) | 70% (42/60) | 78% (47/60) | 83% (50/60) | 87% (52/60) | 0.543 | 1287 | 112 |
| crawl4ai | 38% (23/60) | 63% (38/60) | 73% (44/60) | 82% (49/60) | 88% (53/60) | 0.536 | 2702 | 200 |
| crawl4ai-raw | 38% (23/60) | 63% (38/60) | 73% (44/60) | 82% (49/60) | 88% (53/60) | 0.536 | 2702 | 200 |
| playwright | 32% (19/60) | 62% (37/60) | 72% (43/60) | 83% (50/60) | 88% (53/60) | 0.499 | 2829 | 200 |
| crawlee | 30% (18/60) | 62% (37/60) | 72% (43/60) | 83% (50/60) | 90% (54/60) | 0.492 | 2829 | 200 |
| scrapy+md | 5% (3/60) | 13% (8/60) | 13% (8/60) | 13% (8/60) | 13% (8/60) | 0.086 | 2978 | 199 |
| colly+md | 7% (4/60) | 10% (6/60) | 10% (6/60) | 10% (6/60) | 12% (7/60) | 0.080 | 1976 | 54 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for rust-book</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is a slice in Rust?**
*(expects URL containing: `ch04-03-slices.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.677 | doc.rust-lang.org/book/ch04-03-slices.html | 0.677 | doc.rust-lang.org/book/ch04-03-slices.html | 0.634 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch04-03-slices.html | 0.658 | doc.rust-lang.org/book/print.html | 0.658 | doc.rust-lang.org/book/ch04-03-slices.html | 0.658 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch04-03-slices.html | 0.658 | doc.rust-lang.org/book/print.html | 0.658 | doc.rust-lang.org/book/ch04-03-slices.html | 0.658 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.631 | doc.rust-lang.org/stable/book/print.html | 0.631 | doc.rust-lang.org/src/core/slice/index.rs.html | 0.601 |
| crawlee | #1 | doc.rust-lang.org/book/ch04-03-slices.html | 0.631 | doc.rust-lang.org/book/print.html | 0.631 | doc.rust-lang.org/stable/book/ch04-03-slices.html | 0.631 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.631 | doc.rust-lang.org/book/print.html | 0.631 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.596 |
| playwright | #1 | doc.rust-lang.org/stable/book/ch04-03-slices.html | 0.631 | doc.rust-lang.org/book/print.html | 0.631 | doc.rust-lang.org/book/ch04-03-slices.html | 0.631 |


**Q2: How do you create a string slice using a range?**
*(expects URL containing: `ch04-03-slices.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.596 | doc.rust-lang.org/book/ch04-03-slices.html | 0.596 | doc.rust-lang.org/book/ch08-02-strings.html | 0.557 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch04-03-slices.html | 0.576 | doc.rust-lang.org/book/ch04-03-slices.html | 0.576 | doc.rust-lang.org/book/print.html | 0.576 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch04-03-slices.html | 0.576 | doc.rust-lang.org/book/ch04-03-slices.html | 0.576 | doc.rust-lang.org/book/print.html | 0.576 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.547 | doc.rust-lang.org/book/print.html | 0.547 | doc.rust-lang.org/book/print.html | 0.541 |
| crawlee | #4 | doc.rust-lang.org/book/ch08-02-strings.html | 0.547 | doc.rust-lang.org/book/print.html | 0.547 | doc.rust-lang.org/stable/book/ch08-02-strings.html | 0.547 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.547 | doc.rust-lang.org/book/print.html | 0.547 | doc.rust-lang.org/stable/book/print.html | 0.541 |
| playwright | #5 | doc.rust-lang.org/book/print.html | 0.547 | doc.rust-lang.org/stable/book/ch08-02-strings.html | 0.547 | doc.rust-lang.org/book/ch08-02-strings.html | 0.547 |


**Q3: What advanced features are covered in this chapter?**
*(expects URL containing: `ch20-00-advanced-features.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch20-00-advanced-features.h | 0.549 | doc.rust-lang.org/book/print.html | 0.487 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.451 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.474 | doc.rust-lang.org/book/ch20-00-advanced-features.h | 0.468 | doc.rust-lang.org/book/print.html | 0.433 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.474 | doc.rust-lang.org/book/ch20-00-advanced-features.h | 0.468 | doc.rust-lang.org/book/print.html | 0.433 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.487 | doc.rust-lang.org/book/print.html | 0.487 | doc.rust-lang.org/book/print.html | 0.421 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.487 | doc.rust-lang.org/book/ch20-00-advanced-features.h | 0.442 | doc.rust-lang.org/book/ch03-00-common-programming- | 0.436 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.487 | doc.rust-lang.org/book/print.html | 0.487 | doc.rust-lang.org/book/print.html | 0.421 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.487 | doc.rust-lang.org/book/ch20-00-advanced-features.h | 0.442 | doc.rust-lang.org/book/ch03-00-common-programming- | 0.436 |


**Q4: What is Unsafe Rust in the context of this chapter?**
*(expects URL containing: `ch20-00-advanced-features.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #10 | doc.rust-lang.org/book/ch20-01-unsafe-rust.html | 0.671 | doc.rust-lang.org/book/print.html | 0.634 | doc.rust-lang.org/book/print.html | 0.611 |
| crawl4ai | #29 | doc.rust-lang.org/book/print.html | 0.642 | doc.rust-lang.org/book/ch20-01-unsafe-rust.html | 0.634 | doc.rust-lang.org/book/ch20-01-unsafe-rust.html | 0.625 |
| crawl4ai-raw | #29 | doc.rust-lang.org/book/print.html | 0.642 | doc.rust-lang.org/book/ch20-01-unsafe-rust.html | 0.634 | doc.rust-lang.org/book/ch20-01-unsafe-rust.html | 0.625 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.634 | doc.rust-lang.org/book/print.html | 0.634 | doc.rust-lang.org/stable/book/print.html | 0.611 |
| crawlee | #27 | doc.rust-lang.org/book/ch20-01-unsafe-rust.html | 0.670 | doc.rust-lang.org/book/print.html | 0.634 | doc.rust-lang.org/book/print.html | 0.611 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.634 | doc.rust-lang.org/stable/book/print.html | 0.634 | doc.rust-lang.org/stable/book/print.html | 0.611 |
| playwright | #27 | doc.rust-lang.org/book/ch20-01-unsafe-rust.html | 0.670 | doc.rust-lang.org/book/print.html | 0.634 | doc.rust-lang.org/book/print.html | 0.611 |


**Q5: When should you call `panic!` instead of returning a `Result`?**
*(expects URL containing: `ch09-03-to-panic-or-not-to-panic.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch09-03-to-panic-or-not-to- | 0.705 | doc.rust-lang.org/book/print.html | 0.701 | doc.rust-lang.org/book/ch09-03-to-panic-or-not-to- | 0.625 |
| crawl4ai | #4 | doc.rust-lang.org/book/print.html | 0.686 | doc.rust-lang.org/book/print.html | 0.616 | doc.rust-lang.org/book/print.html | 0.610 |
| crawl4ai-raw | #4 | doc.rust-lang.org/book/print.html | 0.686 | doc.rust-lang.org/book/print.html | 0.616 | doc.rust-lang.org/book/print.html | 0.610 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.675 | doc.rust-lang.org/book/print.html | 0.675 | doc.rust-lang.org/stable/book/print.html | 0.625 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.675 | doc.rust-lang.org/stable/book/ch09-03-to-panic-or- | 0.631 | doc.rust-lang.org/book/ch09-03-to-panic-or-not-to- | 0.631 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.675 | doc.rust-lang.org/stable/book/print.html | 0.675 | doc.rust-lang.org/stable/book/print.html | 0.625 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.675 | doc.rust-lang.org/book/ch09-03-to-panic-or-not-to- | 0.631 | doc.rust-lang.org/stable/book/ch09-03-to-panic-or- | 0.631 |


**Q6: What is the purpose of the `Guess` struct in the context of error handling?**
*(expects URL containing: `ch09-03-to-panic-or-not-to-panic.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch09-03-to-panic-or-not-to- | 0.592 | doc.rust-lang.org/book/print.html | 0.592 | doc.rust-lang.org/book/print.html | 0.547 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch09-03-to-panic-or- | 0.581 | doc.rust-lang.org/book/print.html | 0.581 | doc.rust-lang.org/book/ch09-03-to-panic-or-not-to- | 0.581 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch09-03-to-panic-or- | 0.581 | doc.rust-lang.org/book/print.html | 0.581 | doc.rust-lang.org/book/ch09-03-to-panic-or-not-to- | 0.581 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.530 | doc.rust-lang.org/book/print.html | 0.530 | doc.rust-lang.org/stable/book/print.html | 0.521 |
| crawlee | #1 | doc.rust-lang.org/stable/book/ch09-03-to-panic-or- | 0.536 | doc.rust-lang.org/book/ch09-03-to-panic-or-not-to- | 0.536 | doc.rust-lang.org/book/print.html | 0.530 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.530 | doc.rust-lang.org/stable/book/print.html | 0.530 | doc.rust-lang.org/stable/book/print.html | 0.521 |
| playwright | #1 | doc.rust-lang.org/book/ch09-03-to-panic-or-not-to- | 0.536 | doc.rust-lang.org/stable/book/ch09-03-to-panic-or- | 0.536 | doc.rust-lang.org/book/print.html | 0.530 |


**Q7: What are the three kinds of procedural macros in Rust?**
*(expects URL containing: `ch20-05-macros.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch20-05-macros.html | 0.692 | doc.rust-lang.org/book/print.html | 0.692 | doc.rust-lang.org/book/ch20-05-macros.html | 0.644 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.716 | doc.rust-lang.org/book/ch20-05-macros.html | 0.716 | doc.rust-lang.org/book/print.html | 0.660 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.716 | doc.rust-lang.org/book/ch20-05-macros.html | 0.716 | doc.rust-lang.org/book/print.html | 0.660 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.679 | doc.rust-lang.org/stable/book/print.html | 0.679 | doc.rust-lang.org/stable/book/print.html | 0.645 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.679 | doc.rust-lang.org/book/ch20-05-macros.html | 0.679 | doc.rust-lang.org/book/print.html | 0.645 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.679 | doc.rust-lang.org/book/print.html | 0.679 | doc.rust-lang.org/stable/book/print.html | 0.645 |
| playwright | #1 | doc.rust-lang.org/book/ch20-05-macros.html | 0.679 | doc.rust-lang.org/book/print.html | 0.679 | doc.rust-lang.org/book/ch20-05-macros.html | 0.645 |


**Q8: How do declarative macros compare to functions in Rust?**
*(expects URL containing: `ch20-05-macros.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.711 | doc.rust-lang.org/book/ch20-05-macros.html | 0.711 | doc.rust-lang.org/book/ch20-05-macros.html | 0.681 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch20-05-macros.html | 0.749 | doc.rust-lang.org/book/print.html | 0.749 | doc.rust-lang.org/book/ch20-05-macros.html | 0.639 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch20-05-macros.html | 0.749 | doc.rust-lang.org/book/print.html | 0.749 | doc.rust-lang.org/book/ch20-05-macros.html | 0.639 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.720 | doc.rust-lang.org/book/print.html | 0.720 | doc.rust-lang.org/stable/book/print.html | 0.639 |
| crawlee | #1 | doc.rust-lang.org/book/ch20-05-macros.html | 0.720 | doc.rust-lang.org/book/print.html | 0.720 | doc.rust-lang.org/book/ch20-05-macros.html | 0.675 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.720 | doc.rust-lang.org/stable/book/print.html | 0.720 | doc.rust-lang.org/stable/book/print.html | 0.639 |
| playwright | #1 | doc.rust-lang.org/book/ch20-05-macros.html | 0.720 | doc.rust-lang.org/book/print.html | 0.720 | doc.rust-lang.org/book/ch20-05-macros.html | 0.675 |


**Q9: How do I set up a Crates.io account to publish my crate?**
*(expects URL containing: `ch14-02-publishing-to-crates-io.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.616 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.616 | doc.rust-lang.org/book/ch14-00-more-about-cargo.ht | 0.588 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.689 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.689 | doc.rust-lang.org/cargo/reference/publishing.html | 0.656 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.689 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.689 | doc.rust-lang.org/cargo/reference/publishing.html | 0.656 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.694 | doc.rust-lang.org/book/print.html | 0.694 | doc.rust-lang.org/cargo/reference/publishing.html | 0.681 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.694 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.694 | doc.rust-lang.org/cargo/reference/publishing.html | 0.611 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.694 | doc.rust-lang.org/book/print.html | 0.694 | doc.rust-lang.org/cargo/reference/publishing.html | 0.665 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.694 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.694 | doc.rust-lang.org/cargo/reference/publishing.html | 0.611 |


**Q10: What command do I run to generate HTML documentation from documentation comments in Rust?**
*(expects URL containing: `ch14-02-publishing-to-crates-io.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.677 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.615 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.585 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.676 | doc.rust-lang.org/book/print.html | 0.676 | doc.rust-lang.org/book/print.html | 0.601 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.676 | doc.rust-lang.org/book/print.html | 0.676 | doc.rust-lang.org/book/print.html | 0.601 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.676 | doc.rust-lang.org/book/print.html | 0.676 | doc.rust-lang.org/book/print.html | 0.591 |
| crawlee | #1 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.676 | doc.rust-lang.org/book/print.html | 0.676 | doc.rust-lang.org/book/print.html | 0.591 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.676 | doc.rust-lang.org/stable/book/print.html | 0.676 | doc.rust-lang.org/book/print.html | 0.591 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.676 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.676 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.591 |


**Q11: What are enums in Rust?**
*(expects URL containing: `ch06-00-enums.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #12 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.656 | doc.rust-lang.org/book/ch06-03-if-let.html | 0.597 | doc.rust-lang.org/book/print.html | 0.597 |
| crawl4ai | #4 | doc.rust-lang.org/book/print.html | 0.683 | doc.rust-lang.org/stable/book/ch06-01-defining-an- | 0.641 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.641 |
| crawl4ai-raw | #4 | doc.rust-lang.org/book/print.html | 0.683 | doc.rust-lang.org/stable/book/ch06-01-defining-an- | 0.641 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.641 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.681 | doc.rust-lang.org/book/print.html | 0.681 | doc.rust-lang.org/stable/book/print.html | 0.591 |
| crawlee | #8 | doc.rust-lang.org/book/print.html | 0.681 | doc.rust-lang.org/stable/book/ch06-01-defining-an- | 0.648 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.648 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.681 | doc.rust-lang.org/book/print.html | 0.681 | doc.rust-lang.org/book/print.html | 0.591 |
| playwright | #8 | doc.rust-lang.org/book/print.html | 0.681 | doc.rust-lang.org/stable/book/ch06-01-defining-an- | 0.648 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.648 |


**Q12: What is the purpose of the `Option` enum?**
*(expects URL containing: `ch06-00-enums.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #11 | doc.rust-lang.org/book/print.html | 0.557 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.557 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.551 |
| crawl4ai | #27 | doc.rust-lang.org/stable/book/ch06-01-defining-an- | 0.605 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.604 | doc.rust-lang.org/book/print.html | 0.604 |
| crawl4ai-raw | #27 | doc.rust-lang.org/stable/book/ch06-01-defining-an- | 0.605 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.604 | doc.rust-lang.org/book/print.html | 0.604 |
| scrapy+md | miss | doc.rust-lang.org/std/option/enum.Option.html | 0.596 | doc.rust-lang.org/stable/book/print.html | 0.557 | doc.rust-lang.org/book/print.html | 0.557 |
| crawlee | #30 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.575 | doc.rust-lang.org/stable/book/ch06-01-defining-an- | 0.575 | doc.rust-lang.org/book/print.html | 0.557 |
| colly+md | miss | doc.rust-lang.org/std/option/enum.Option.html | 0.574 | doc.rust-lang.org/std/option/enum.Option.html#meth | 0.574 | doc.rust-lang.org/stable/book/print.html | 0.557 |
| playwright | #30 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.575 | doc.rust-lang.org/stable/book/ch06-01-defining-an- | 0.575 | doc.rust-lang.org/book/print.html | 0.557 |


**Q13: What are the tradeoffs of using threads for concurrency?**
*(expects URL containing: `ch17-06-futures-tasks-threads.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/ch16-01-threads.html | 0.546 | doc.rust-lang.org/book/ch17-06-futures-tasks-threa | 0.536 | doc.rust-lang.org/book/ch17-02-concurrency-with-as | 0.527 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch17-06-futures-tasks-threa | 0.549 | doc.rust-lang.org/book/print.html | 0.549 | doc.rust-lang.org/book/ch17-06-futures-tasks-threa | 0.527 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch17-06-futures-tasks-threa | 0.549 | doc.rust-lang.org/book/print.html | 0.549 | doc.rust-lang.org/book/ch17-06-futures-tasks-threa | 0.527 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.519 | doc.rust-lang.org/stable/book/print.html | 0.519 | doc.rust-lang.org/stable/book/print.html | 0.498 |
| crawlee | #1 | doc.rust-lang.org/book/ch17-06-futures-tasks-threa | 0.529 | doc.rust-lang.org/book/print.html | 0.519 | doc.rust-lang.org/book/print.html | 0.498 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.519 | doc.rust-lang.org/stable/book/print.html | 0.519 | doc.rust-lang.org/stable/book/print.html | 0.498 |
| playwright | #1 | doc.rust-lang.org/book/ch17-06-futures-tasks-threa | 0.529 | doc.rust-lang.org/book/print.html | 0.519 | doc.rust-lang.org/book/print.html | 0.498 |


**Q14: When should I choose async over threads for concurrent operations?**
*(expects URL containing: `ch17-06-futures-tasks-threads.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/ch17-02-concurrency-with-as | 0.623 | doc.rust-lang.org/book/ch17-06-futures-tasks-threa | 0.564 | doc.rust-lang.org/book/print.html | 0.553 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch17-06-futures-tasks-threa | 0.611 | doc.rust-lang.org/book/print.html | 0.611 | doc.rust-lang.org/book/print.html | 0.569 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch17-06-futures-tasks-threa | 0.611 | doc.rust-lang.org/book/print.html | 0.611 | doc.rust-lang.org/book/print.html | 0.569 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.553 | doc.rust-lang.org/book/print.html | 0.553 | doc.rust-lang.org/stable/book/print.html | 0.545 |
| crawlee | #1 | doc.rust-lang.org/book/ch17-06-futures-tasks-threa | 0.569 | doc.rust-lang.org/book/print.html | 0.553 | doc.rust-lang.org/book/print.html | 0.545 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.553 | doc.rust-lang.org/book/print.html | 0.553 | doc.rust-lang.org/stable/book/print.html | 0.545 |
| playwright | #1 | doc.rust-lang.org/book/ch17-06-futures-tasks-threa | 0.569 | doc.rust-lang.org/book/print.html | 0.553 | doc.rust-lang.org/book/ch17-00-async-await.html | 0.545 |


**Q15: How do I print error messages to standard error in Rust?**
*(expects URL containing: `ch12-06-writing-to-stderr-instead-of-stdout.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/ch09-00-error-handling.html | 0.582 | doc.rust-lang.org/book/ch12-06-writing-to-stderr-i | 0.573 | doc.rust-lang.org/book/print.html | 0.543 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch12-06-writing-to-stderr-i | 0.598 | doc.rust-lang.org/book/print.html | 0.598 | doc.rust-lang.org/stable/book/ch12-06-writing-to-s | 0.598 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch12-06-writing-to-stderr-i | 0.598 | doc.rust-lang.org/book/print.html | 0.598 | doc.rust-lang.org/stable/book/ch12-06-writing-to-s | 0.598 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.603 | doc.rust-lang.org/stable/book/print.html | 0.603 | doc.rust-lang.org/stable/book/print.html | 0.544 |
| crawlee | #1 | doc.rust-lang.org/book/ch12-06-writing-to-stderr-i | 0.603 | doc.rust-lang.org/stable/book/ch12-06-writing-to-s | 0.603 | doc.rust-lang.org/book/print.html | 0.603 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.603 | doc.rust-lang.org/stable/book/print.html | 0.603 | doc.rust-lang.org/stable/book/print.html | 0.543 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.603 | doc.rust-lang.org/book/ch12-06-writing-to-stderr-i | 0.603 | doc.rust-lang.org/stable/book/ch12-06-writing-to-s | 0.603 |


**Q16: What command do I use to redirect standard output to a file in Rust?**
*(expects URL containing: `ch12-06-writing-to-stderr-instead-of-stdout.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch12-06-writing-to-stderr-i | 0.545 | doc.rust-lang.org/book/print.html | 0.509 | doc.rust-lang.org/book/ch12-06-writing-to-stderr-i | 0.494 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch12-06-writing-to-s | 0.550 | doc.rust-lang.org/book/ch12-06-writing-to-stderr-i | 0.550 | doc.rust-lang.org/book/ch12-06-writing-to-stderr-i | 0.549 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch12-06-writing-to-s | 0.550 | doc.rust-lang.org/book/ch12-06-writing-to-stderr-i | 0.550 | doc.rust-lang.org/book/ch12-06-writing-to-stderr-i | 0.549 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.553 | doc.rust-lang.org/stable/book/print.html | 0.553 | doc.rust-lang.org/book/print.html | 0.506 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.553 | doc.rust-lang.org/stable/book/ch12-06-writing-to-s | 0.553 | doc.rust-lang.org/book/ch12-06-writing-to-stderr-i | 0.553 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.553 | doc.rust-lang.org/book/print.html | 0.553 | doc.rust-lang.org/book/print.html | 0.506 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.553 | doc.rust-lang.org/book/ch12-06-writing-to-stderr-i | 0.553 | doc.rust-lang.org/stable/book/ch12-06-writing-to-s | 0.553 |


**Q17: How do you define a struct in Rust?**
*(expects URL containing: `ch05-02-example-structs.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | doc.rust-lang.org/book/ch05-00-structs.html | 0.693 | doc.rust-lang.org/book/print.html | 0.655 | doc.rust-lang.org/book/ch05-02-example-structs.htm | 0.620 |
| crawl4ai | #19 | doc.rust-lang.org/book/print.html | 0.675 | doc.rust-lang.org/book/print.html | 0.649 | doc.rust-lang.org/book/ch05-00-structs.html | 0.630 |
| crawl4ai-raw | #19 | doc.rust-lang.org/book/print.html | 0.675 | doc.rust-lang.org/book/print.html | 0.649 | doc.rust-lang.org/book/ch05-00-structs.html | 0.630 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.662 | doc.rust-lang.org/stable/book/print.html | 0.662 | doc.rust-lang.org/stable/book/print.html | 0.642 |
| crawlee | #20 | doc.rust-lang.org/book/print.html | 0.662 | doc.rust-lang.org/book/print.html | 0.642 | doc.rust-lang.org/book/ch05-03-method-syntax.html | 0.625 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.662 | doc.rust-lang.org/stable/book/print.html | 0.662 | doc.rust-lang.org/stable/book/print.html | 0.642 |
| playwright | #21 | doc.rust-lang.org/book/print.html | 0.662 | doc.rust-lang.org/book/print.html | 0.642 | doc.rust-lang.org/stable/book/ch05-03-method-synta | 0.625 |


**Q18: What is the purpose of the `#[derive(Debug)]` attribute in a struct?**
*(expects URL containing: `ch05-02-example-structs.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.614 | doc.rust-lang.org/book/ch05-02-example-structs.htm | 0.614 | doc.rust-lang.org/book/ch05-02-example-structs.htm | 0.577 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch05-02-example-stru | 0.566 | doc.rust-lang.org/book/ch05-02-example-structs.htm | 0.566 | doc.rust-lang.org/book/print.html | 0.565 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch05-02-example-stru | 0.566 | doc.rust-lang.org/book/ch05-02-example-structs.htm | 0.566 | doc.rust-lang.org/book/print.html | 0.565 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.568 | doc.rust-lang.org/stable/book/print.html | 0.568 | doc.rust-lang.org/book/print.html | 0.550 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.568 | doc.rust-lang.org/stable/book/ch05-02-example-stru | 0.568 | doc.rust-lang.org/book/ch05-02-example-structs.htm | 0.568 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.568 | doc.rust-lang.org/stable/book/print.html | 0.568 | doc.rust-lang.org/stable/book/print.html | 0.550 |
| playwright | #1 | doc.rust-lang.org/book/ch05-02-example-structs.htm | 0.568 | doc.rust-lang.org/book/print.html | 0.568 | doc.rust-lang.org/stable/book/ch05-02-example-stru | 0.568 |


**Q19: What command line tool will we build in this chapter?**
*(expects URL containing: `ch12-00-an-io-project.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch12-00-an-io-project.html | 0.543 | doc.rust-lang.org/book/print.html | 0.524 | doc.rust-lang.org/book/print.html | 0.467 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.525 | doc.rust-lang.org/stable/book/ch12-00-an-io-projec | 0.493 | doc.rust-lang.org/book/ch12-00-an-io-project.html | 0.493 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.525 | doc.rust-lang.org/stable/book/ch12-00-an-io-projec | 0.493 | doc.rust-lang.org/book/ch12-00-an-io-project.html | 0.493 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.524 | doc.rust-lang.org/book/print.html | 0.524 | doc.rust-lang.org/stable/book/print.html | 0.466 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.524 | doc.rust-lang.org/book/ch12-00-an-io-project.html | 0.479 | doc.rust-lang.org/stable/book/ch12-00-an-io-projec | 0.479 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.524 | doc.rust-lang.org/stable/book/print.html | 0.524 | doc.rust-lang.org/stable/book/print.html | 0.466 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.524 | doc.rust-lang.org/book/ch12-00-an-io-project.html | 0.479 | doc.rust-lang.org/stable/book/ch12-00-an-io-projec | 0.479 |


**Q20: What features will our command line tool use from the terminal?**
*(expects URL containing: `ch12-00-an-io-project.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch12-00-an-io-project.html | 0.433 | doc.rust-lang.org/book/print.html | 0.404 | doc.rust-lang.org/book/print.html | 0.397 |
| crawl4ai | #3 | doc.rust-lang.org/stable/book/ch12-05-working-with | 0.433 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.433 | doc.rust-lang.org/book/ch12-00-an-io-project.html | 0.419 |
| crawl4ai-raw | #3 | doc.rust-lang.org/stable/book/ch12-05-working-with | 0.433 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.433 | doc.rust-lang.org/book/ch12-00-an-io-project.html | 0.419 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.404 | doc.rust-lang.org/stable/book/print.html | 0.404 | doc.rust-lang.org/stable/book/print.html | 0.400 |
| crawlee | #4 | doc.rust-lang.org/rustc/tests/index.html | 0.446 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.436 | doc.rust-lang.org/stable/book/ch12-05-working-with | 0.436 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.404 | doc.rust-lang.org/stable/book/print.html | 0.404 | doc.rust-lang.org/book/ch01-01-installation.html | 0.400 |
| playwright | #4 | doc.rust-lang.org/rustc/tests/index.html | 0.446 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.436 | doc.rust-lang.org/stable/book/ch12-05-working-with | 0.436 |


**Q21: What is Cargo in Rust?**
*(expects URL containing: `ch01-03-hello-cargo.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.651 | doc.rust-lang.org/book/print.html | 0.640 | doc.rust-lang.org/book/print.html | 0.572 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.632 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.597 | doc.rust-lang.org/stable/book/ch01-03-hello-cargo. | 0.597 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.632 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.597 | doc.rust-lang.org/stable/book/ch01-03-hello-cargo. | 0.597 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.639 | doc.rust-lang.org/book/print.html | 0.639 | doc.rust-lang.org/nightly/cargo/reference/environm | 0.588 |
| crawlee | #3 | doc.rust-lang.org/book/print.html | 0.639 | doc.rust-lang.org/cargo/ | 0.598 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.596 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.639 | doc.rust-lang.org/book/print.html | 0.639 | doc.rust-lang.org/cargo/ | 0.582 |
| playwright | #3 | doc.rust-lang.org/book/print.html | 0.639 | doc.rust-lang.org/cargo/ | 0.598 | doc.rust-lang.org/stable/book/ch01-03-hello-cargo. | 0.596 |


**Q22: How do you create a new project using Cargo?**
*(expects URL containing: `ch01-03-hello-cargo.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.726 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.726 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.656 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch01-03-hello-cargo. | 0.729 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.729 | doc.rust-lang.org/book/print.html | 0.729 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch01-03-hello-cargo. | 0.729 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.729 | doc.rust-lang.org/book/print.html | 0.729 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.732 | doc.rust-lang.org/stable/book/print.html | 0.732 | doc.rust-lang.org/stable/book/print.html | 0.653 |
| crawlee | #1 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.732 | doc.rust-lang.org/book/print.html | 0.732 | doc.rust-lang.org/stable/book/ch01-03-hello-cargo. | 0.732 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.732 | doc.rust-lang.org/stable/book/print.html | 0.732 | doc.rust-lang.org/book/print.html | 0.653 |
| playwright | #1 | doc.rust-lang.org/stable/book/ch01-03-hello-cargo. | 0.732 | doc.rust-lang.org/book/print.html | 0.732 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.732 |


**Q23: What are the two main profiles in Cargo?**
*(expects URL containing: `ch14-01-release-profiles.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | doc.rust-lang.org/book/print.html | 0.578 | doc.rust-lang.org/book/print.html | 0.541 | doc.rust-lang.org/book/ch14-00-more-about-cargo.ht | 0.535 |
| crawl4ai | #7 | doc.rust-lang.org/cargo/reference/profiles.html | 0.622 | doc.rust-lang.org/book/print.html | 0.587 | doc.rust-lang.org/cargo/reference/profiles.html | 0.572 |
| crawl4ai-raw | #7 | doc.rust-lang.org/cargo/reference/profiles.html | 0.622 | doc.rust-lang.org/book/print.html | 0.587 | doc.rust-lang.org/cargo/reference/profiles.html | 0.572 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.587 | doc.rust-lang.org/book/print.html | 0.587 | doc.rust-lang.org/cargo/reference/profiles.html | 0.564 |
| crawlee | #8 | doc.rust-lang.org/cargo/reference/profiles.html | 0.643 | doc.rust-lang.org/cargo/reference/profiles.html | 0.587 | doc.rust-lang.org/cargo/reference/profiles.html | 0.587 |
| colly+md | miss | doc.rust-lang.org/cargo/reference/profiles.html | 0.636 | doc.rust-lang.org/stable/book/print.html | 0.587 | doc.rust-lang.org/book/print.html | 0.587 |
| playwright | #8 | doc.rust-lang.org/cargo/reference/profiles.html | 0.643 | doc.rust-lang.org/cargo/reference/profiles.html | 0.587 | doc.rust-lang.org/cargo/reference/profiles.html | 0.587 |


**Q24: How can you customize the `opt-level` setting in the `dev` profile?**
*(expects URL containing: `ch14-01-release-profiles.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.671 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.669 | doc.rust-lang.org/book/print.html | 0.646 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.684 | doc.rust-lang.org/book/print.html | 0.649 | doc.rust-lang.org/cargo/reference/profiles.html | 0.617 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.684 | doc.rust-lang.org/book/print.html | 0.649 | doc.rust-lang.org/cargo/reference/profiles.html | 0.617 |
| scrapy+md | miss | doc.rust-lang.org/cargo/reference/profiles.html | 0.650 | doc.rust-lang.org/book/print.html | 0.648 | doc.rust-lang.org/stable/book/print.html | 0.648 |
| crawlee | #1 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.655 | doc.rust-lang.org/book/print.html | 0.648 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.585 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.648 | doc.rust-lang.org/stable/book/print.html | 0.648 | doc.rust-lang.org/cargo/reference/profiles.html | 0.618 |
| playwright | #1 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.655 | doc.rust-lang.org/book/print.html | 0.648 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.585 |


**Q25: How do you bring a module into scope with the use keyword?**
*(expects URL containing: `ch07-04-bringing-paths-into-scope-with-the-use-keyword.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | doc.rust-lang.org/book/ch07-02-defining-modules-to | 0.627 | doc.rust-lang.org/book/print.html | 0.605 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.590 |
| crawl4ai | #4 | doc.rust-lang.org/book/print.html | 0.577 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.552 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.552 |
| crawl4ai-raw | #4 | doc.rust-lang.org/book/print.html | 0.577 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.552 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.552 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.587 | doc.rust-lang.org/stable/book/print.html | 0.587 | doc.rust-lang.org/book/print.html | 0.526 |
| crawlee | #4 | doc.rust-lang.org/book/print.html | 0.587 | doc.rust-lang.org/book/ch07-00-managing-growing-pr | 0.552 | doc.rust-lang.org/stable/book/ch07-00-managing-gro | 0.552 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.587 | doc.rust-lang.org/stable/book/print.html | 0.587 | doc.rust-lang.org/book/print.html | 0.526 |
| playwright | #4 | doc.rust-lang.org/book/print.html | 0.587 | doc.rust-lang.org/book/ch07-00-managing-growing-pr | 0.552 | doc.rust-lang.org/stable/book/ch07-00-managing-gro | 0.552 |


**Q26: What is the purpose of the pub use statement in Rust?**
*(expects URL containing: `ch07-04-bringing-paths-into-scope-with-the-use-keyword.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | doc.rust-lang.org/book/print.html | 0.560 | doc.rust-lang.org/book/ch07-03-paths-for-referring | 0.560 | doc.rust-lang.org/book/print.html | 0.557 |
| crawl4ai | #4 | doc.rust-lang.org/book/ch07-03-paths-for-referring | 0.568 | doc.rust-lang.org/book/print.html | 0.568 | doc.rust-lang.org/stable/book/ch07-03-paths-for-re | 0.568 |
| crawl4ai-raw | #4 | doc.rust-lang.org/book/ch07-03-paths-for-referring | 0.568 | doc.rust-lang.org/book/print.html | 0.568 | doc.rust-lang.org/stable/book/ch07-03-paths-for-re | 0.568 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.564 | doc.rust-lang.org/stable/book/print.html | 0.564 | doc.rust-lang.org/stable/book/print.html | 0.562 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.564 | doc.rust-lang.org/stable/book/ch07-04-bringing-pat | 0.564 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.564 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.564 | doc.rust-lang.org/stable/book/print.html | 0.564 | doc.rust-lang.org/book/print.html | 0.562 |
| playwright | #1 | doc.rust-lang.org/stable/book/ch07-04-bringing-pat | 0.564 | doc.rust-lang.org/book/print.html | 0.564 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.564 |


**Q27: What are the features of Rust's module system?**
*(expects URL containing: `ch07-00-managing-growing-projects-with-packages-crates-and-modules.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.654 | doc.rust-lang.org/book/ch07-00-managing-growing-pr | 0.590 | doc.rust-lang.org/book/print.html | 0.576 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch07-00-managing-gro | 0.626 | doc.rust-lang.org/book/ch07-00-managing-growing-pr | 0.626 | doc.rust-lang.org/book/print.html | 0.617 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch07-00-managing-gro | 0.626 | doc.rust-lang.org/book/ch07-00-managing-growing-pr | 0.626 | doc.rust-lang.org/book/print.html | 0.617 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.654 | doc.rust-lang.org/stable/book/print.html | 0.654 | doc.rust-lang.org/stable/book/print.html | 0.576 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.654 | doc.rust-lang.org/stable/book/ch07-00-managing-gro | 0.606 | doc.rust-lang.org/book/ch07-00-managing-growing-pr | 0.606 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.654 | doc.rust-lang.org/book/print.html | 0.654 | doc.rust-lang.org/stable/book/print.html | 0.576 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.654 | doc.rust-lang.org/book/ch07-00-managing-growing-pr | 0.606 | doc.rust-lang.org/stable/book/ch07-00-managing-gro | 0.606 |


**Q28: How can you manage code organization in Rust?**
*(expects URL containing: `ch07-00-managing-growing-projects-with-packages-crates-and-modules.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.657 | doc.rust-lang.org/book/ch07-00-managing-growing-pr | 0.643 | doc.rust-lang.org/book/ch11-03-test-organization.h | 0.559 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.682 | doc.rust-lang.org/book/ch07-00-managing-growing-pr | 0.633 | doc.rust-lang.org/stable/book/ch07-00-managing-gro | 0.633 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.682 | doc.rust-lang.org/book/ch07-00-managing-growing-pr | 0.633 | doc.rust-lang.org/stable/book/ch07-00-managing-gro | 0.633 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.657 | doc.rust-lang.org/stable/book/print.html | 0.657 | doc.rust-lang.org/book/print.html | 0.558 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.657 | doc.rust-lang.org/stable/book/ch07-00-managing-gro | 0.646 | doc.rust-lang.org/book/ch07-00-managing-growing-pr | 0.646 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.657 | doc.rust-lang.org/book/print.html | 0.657 | doc.rust-lang.org/book/print.html | 0.558 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.657 | doc.rust-lang.org/stable/book/ch07-00-managing-gro | 0.646 | doc.rust-lang.org/book/ch07-00-managing-growing-pr | 0.646 |


**Q29: What is the purpose of the `search` function in the `minigrep` program?**
*(expects URL containing: `ch12-04-testing-the-librarys-functionality.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch12-04-testing-the-library | 0.547 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.540 | doc.rust-lang.org/book/print.html | 0.529 |
| crawl4ai | #17 | doc.rust-lang.org/stable/book/ch12-03-improving-er | 0.573 | doc.rust-lang.org/book/ch12-03-improving-error-han | 0.572 | doc.rust-lang.org/book/print.html | 0.572 |
| crawl4ai-raw | #17 | doc.rust-lang.org/stable/book/ch12-03-improving-er | 0.573 | doc.rust-lang.org/book/ch12-03-improving-error-han | 0.572 | doc.rust-lang.org/book/print.html | 0.572 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.585 | doc.rust-lang.org/stable/book/print.html | 0.585 | doc.rust-lang.org/stable/book/print.html | 0.523 |
| crawlee | #20 | doc.rust-lang.org/stable/book/ch12-03-improving-er | 0.585 | doc.rust-lang.org/book/print.html | 0.585 | doc.rust-lang.org/book/ch12-03-improving-error-han | 0.585 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.585 | doc.rust-lang.org/stable/book/print.html | 0.585 | doc.rust-lang.org/stable/book/print.html | 0.523 |
| playwright | #20 | doc.rust-lang.org/book/print.html | 0.585 | doc.rust-lang.org/book/ch12-03-improving-error-han | 0.585 | doc.rust-lang.org/stable/book/ch12-03-improving-er | 0.585 |


**Q30: How do you write a failing test for the `search` function?**
*(expects URL containing: `ch12-04-testing-the-librarys-functionality.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.626 | doc.rust-lang.org/book/ch12-04-testing-the-library | 0.609 | doc.rust-lang.org/book/print.html | 0.609 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch12-04-testing-the- | 0.636 | doc.rust-lang.org/book/ch12-04-testing-the-library | 0.635 | doc.rust-lang.org/book/print.html | 0.635 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch12-04-testing-the- | 0.636 | doc.rust-lang.org/book/ch12-04-testing-the-library | 0.635 | doc.rust-lang.org/book/print.html | 0.635 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.633 | doc.rust-lang.org/book/print.html | 0.633 | doc.rust-lang.org/book/print.html | 0.616 |
| crawlee | #1 | doc.rust-lang.org/stable/book/ch12-04-testing-the- | 0.633 | doc.rust-lang.org/book/print.html | 0.633 | doc.rust-lang.org/book/ch12-04-testing-the-library | 0.633 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.633 | doc.rust-lang.org/stable/book/print.html | 0.633 | doc.rust-lang.org/stable/book/print.html | 0.616 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.633 | doc.rust-lang.org/book/ch12-04-testing-the-library | 0.633 | doc.rust-lang.org/stable/book/ch12-04-testing-the- | 0.633 |


**Q31: What are the three collections discussed in this chapter?**
*(expects URL containing: `ch08-00-common-collections.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch08-00-common-collections. | 0.492 | doc.rust-lang.org/book/print.html | 0.438 | doc.rust-lang.org/book/print.html | 0.344 |
| crawl4ai | #3 | doc.rust-lang.org/book/print.html | 0.430 | doc.rust-lang.org/std/collections/index.html | 0.429 | doc.rust-lang.org/stable/book/ch08-00-common-colle | 0.427 |
| crawl4ai-raw | #3 | doc.rust-lang.org/book/print.html | 0.430 | doc.rust-lang.org/std/collections/index.html | 0.429 | doc.rust-lang.org/stable/book/ch08-00-common-colle | 0.427 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.438 | doc.rust-lang.org/stable/book/print.html | 0.438 | doc.rust-lang.org/std/collections/index.html | 0.392 |
| crawlee | #4 | doc.rust-lang.org/book/print.html | 0.438 | doc.rust-lang.org/std/collections/index.html | 0.418 | doc.rust-lang.org/std/collections/index.html | 0.405 |
| colly+md | miss | doc.rust-lang.org/std/collections/index.html | 0.456 | doc.rust-lang.org/book/print.html | 0.438 | doc.rust-lang.org/stable/book/print.html | 0.438 |
| playwright | #4 | doc.rust-lang.org/book/print.html | 0.438 | doc.rust-lang.org/std/collections/index.html | 0.418 | doc.rust-lang.org/std/collections/index.html | 0.405 |


**Q32: How does a vector differ from built-in array and tuple types in Rust?**
*(expects URL containing: `ch08-00-common-collections.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch08-00-common-collections. | 0.603 | doc.rust-lang.org/book/ch03-02-data-types.html | 0.597 | doc.rust-lang.org/book/print.html | 0.597 |
| crawl4ai | miss | doc.rust-lang.org/book/ch08-01-vectors.html | 0.620 | doc.rust-lang.org/stable/book/ch08-01-vectors.html | 0.620 | doc.rust-lang.org/book/print.html | 0.605 |
| crawl4ai-raw | miss | doc.rust-lang.org/book/ch08-01-vectors.html | 0.620 | doc.rust-lang.org/stable/book/ch08-01-vectors.html | 0.620 | doc.rust-lang.org/book/print.html | 0.605 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.598 | doc.rust-lang.org/stable/book/print.html | 0.598 | doc.rust-lang.org/book/print.html | 0.597 |
| crawlee | miss | doc.rust-lang.org/book/ch08-01-vectors.html | 0.605 | doc.rust-lang.org/stable/book/ch08-01-vectors.html | 0.605 | doc.rust-lang.org/book/print.html | 0.598 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.598 | doc.rust-lang.org/stable/book/print.html | 0.598 | doc.rust-lang.org/book/print.html | 0.597 |
| playwright | miss | doc.rust-lang.org/book/ch08-01-vectors.html | 0.605 | doc.rust-lang.org/stable/book/ch08-01-vectors.html | 0.605 | doc.rust-lang.org/book/print.html | 0.598 |


**Q33: What is Rust's most unique feature?**
*(expects URL containing: `ch04-00-understanding-ownership.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | doc.rust-lang.org/book/ch00-00-introduction.html | 0.533 | doc.rust-lang.org/book/print.html | 0.533 | doc.rust-lang.org/book/ch18-01-what-is-oo.html | 0.526 |
| crawl4ai | #21 | doc.rust-lang.org/stable/book/ch00-00-introduction | 0.535 | doc.rust-lang.org/book/ch00-00-introduction.html | 0.535 | doc.rust-lang.org/book/print.html | 0.535 |
| crawl4ai-raw | #21 | doc.rust-lang.org/stable/book/ch00-00-introduction | 0.535 | doc.rust-lang.org/book/ch00-00-introduction.html | 0.535 | doc.rust-lang.org/book/print.html | 0.535 |
| scrapy+md | miss | doc.rust-lang.org/book/ch00-00-introduction.html | 0.533 | doc.rust-lang.org/stable/book/ch00-00-introduction | 0.533 | doc.rust-lang.org/stable/book/print.html | 0.533 |
| crawlee | #13 | doc.rust-lang.org/book/ch20-01-unsafe-rust.html | 0.546 | doc.rust-lang.org/book/ch18-01-what-is-oo.html | 0.534 | doc.rust-lang.org/book/print.html | 0.533 |
| colly+md | miss | doc.rust-lang.org/book/ch00-00-introduction.html | 0.545 | doc.rust-lang.org/stable/book/print.html | 0.533 | doc.rust-lang.org/book/print.html | 0.533 |
| playwright | #13 | doc.rust-lang.org/book/ch20-01-unsafe-rust.html | 0.546 | doc.rust-lang.org/book/ch18-01-what-is-oo.html | 0.534 | doc.rust-lang.org/book/ch00-00-introduction.html | 0.533 |


**Q34: How does ownership in Rust enable memory safety without a garbage collector?**
*(expects URL containing: `ch04-00-understanding-ownership.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch04-00-understanding-owner | 0.672 | doc.rust-lang.org/book/ch04-01-what-is-ownership.h | 0.657 | doc.rust-lang.org/book/ch20-01-unsafe-rust.html | 0.585 |
| crawl4ai | #21 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.584 | doc.rust-lang.org/book/print.html | 0.584 | doc.rust-lang.org/book/print.html | 0.579 |
| crawl4ai-raw | #21 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.584 | doc.rust-lang.org/book/print.html | 0.584 | doc.rust-lang.org/book/print.html | 0.579 |
| scrapy+md | miss | doc.rust-lang.org/nomicon/leaking.html | 0.603 | doc.rust-lang.org/stable/book/print.html | 0.579 | doc.rust-lang.org/book/print.html | 0.579 |
| crawlee | #39 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.579 | doc.rust-lang.org/book/print.html | 0.579 | doc.rust-lang.org/book/print.html | 0.578 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.579 | doc.rust-lang.org/stable/book/print.html | 0.579 | doc.rust-lang.org/stable/book/print.html | 0.579 |
| playwright | #39 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.579 | doc.rust-lang.org/book/print.html | 0.579 | doc.rust-lang.org/book/print.html | 0.578 |


**Q35: How can I enable case-insensitive searching in minigrep?**
*(expects URL containing: `ch12-05-working-with-environment-variables.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.573 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.562 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.531 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch12-05-working-with | 0.548 | doc.rust-lang.org/book/print.html | 0.548 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.548 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch12-05-working-with | 0.548 | doc.rust-lang.org/book/print.html | 0.548 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.548 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.529 | doc.rust-lang.org/stable/book/print.html | 0.529 | doc.rust-lang.org/book/print.html | 0.497 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.529 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.529 | doc.rust-lang.org/stable/book/ch12-05-working-with | 0.529 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.529 | doc.rust-lang.org/book/print.html | 0.529 | doc.rust-lang.org/stable/book/print.html | 0.497 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.529 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.529 | doc.rust-lang.org/stable/book/ch12-05-working-with | 0.529 |


**Q36: What function is used to check if the IGNORE_CASE environment variable is set?**
*(expects URL containing: `ch12-05-working-with-environment-variables.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.516 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.516 | doc.rust-lang.org/book/print.html | 0.451 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.636 | doc.rust-lang.org/stable/book/ch12-05-working-with | 0.636 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.636 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.636 | doc.rust-lang.org/stable/book/ch12-05-working-with | 0.636 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.636 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.507 | doc.rust-lang.org/book/print.html | 0.507 | doc.rust-lang.org/stable/book/print.html | 0.492 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.507 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.507 | doc.rust-lang.org/stable/book/ch12-05-working-with | 0.507 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.507 | doc.rust-lang.org/book/print.html | 0.507 | doc.rust-lang.org/book/print.html | 0.492 |
| playwright | #1 | doc.rust-lang.org/book/ch12-05-working-with-enviro | 0.507 | doc.rust-lang.org/book/print.html | 0.507 | doc.rust-lang.org/stable/book/ch12-05-working-with | 0.507 |


**Q37: What are atomic types used for in Rust?**
*(expects URL containing: `atomic`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | doc.rust-lang.org/book/ch03-02-data-types.html | 0.622 | doc.rust-lang.org/book/ch03-02-data-types.html | 0.609 | doc.rust-lang.org/book/print.html | 0.609 |
| crawl4ai | #1 | doc.rust-lang.org/std/sync/atomic/index.html | 0.658 | doc.rust-lang.org/std/sync/atomic/index.html | 0.650 | doc.rust-lang.org/std/sync/atomic/index.html | 0.634 |
| crawl4ai-raw | #1 | doc.rust-lang.org/std/sync/atomic/index.html | 0.658 | doc.rust-lang.org/std/sync/atomic/index.html | 0.650 | doc.rust-lang.org/std/sync/atomic/index.html | 0.634 |
| scrapy+md | #1 | doc.rust-lang.org/std/sync/atomic/index.html | 0.626 | doc.rust-lang.org/std/sync/atomic/index.html | 0.616 | doc.rust-lang.org/stable/book/print.html | 0.611 |
| crawlee | #1 | doc.rust-lang.org/std/sync/atomic/index.html | 0.654 | doc.rust-lang.org/std/sync/atomic/index.html | 0.626 | doc.rust-lang.org/std/sync/atomic/index.html | 0.616 |
| colly+md | #1 | doc.rust-lang.org/std/sync/atomic/index.html | 0.644 | doc.rust-lang.org/std/sync/atomic/index.html | 0.626 | doc.rust-lang.org/std/sync/atomic/index.html | 0.616 |
| playwright | #1 | doc.rust-lang.org/std/sync/atomic/index.html | 0.654 | doc.rust-lang.org/std/sync/atomic/index.html | 0.626 | doc.rust-lang.org/std/sync/atomic/index.html | 0.616 |


**Q38: Which atomic types are defined in the atomic module?**
*(expects URL containing: `atomic`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | doc.rust-lang.org/book/appendix-01-keywords.html | 0.387 | doc.rust-lang.org/book/print.html | 0.387 | doc.rust-lang.org/book/ch20-03-advanced-types.html | 0.381 |
| crawl4ai | #1 | doc.rust-lang.org/std/sync/atomic/index.html | 0.603 | doc.rust-lang.org/std/sync/atomic/index.html | 0.570 | doc.rust-lang.org/std/sync/atomic/index.html | 0.484 |
| crawl4ai-raw | #1 | doc.rust-lang.org/std/sync/atomic/index.html | 0.603 | doc.rust-lang.org/std/sync/atomic/index.html | 0.570 | doc.rust-lang.org/std/sync/atomic/index.html | 0.484 |
| scrapy+md | #1 | doc.rust-lang.org/std/sync/atomic/index.html | 0.546 | doc.rust-lang.org/std/sync/atomic/index.html | 0.511 | doc.rust-lang.org/std/sync/atomic/index.html | 0.485 |
| crawlee | #1 | doc.rust-lang.org/std/sync/atomic/index.html | 0.605 | doc.rust-lang.org/std/sync/atomic/index.html | 0.546 | doc.rust-lang.org/std/sync/atomic/index.html | 0.485 |
| colly+md | #1 | doc.rust-lang.org/std/sync/atomic/index.html | 0.593 | doc.rust-lang.org/std/sync/atomic/index.html | 0.546 | doc.rust-lang.org/std/sync/atomic/index.html | 0.485 |
| playwright | #1 | doc.rust-lang.org/std/sync/atomic/index.html | 0.605 | doc.rust-lang.org/std/sync/atomic/index.html | 0.546 | doc.rust-lang.org/std/sync/atomic/index.html | 0.485 |


**Q39: What is the purpose of the `trpl::block_on` function in async Rust?**
*(expects URL containing: `ch17-02-concurrency-with-async.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #10 | doc.rust-lang.org/book/print.html | 0.591 | doc.rust-lang.org/book/ch17-01-futures-and-syntax. | 0.591 | doc.rust-lang.org/book/print.html | 0.564 |
| crawl4ai | #10 | doc.rust-lang.org/book/ch17-01-futures-and-syntax. | 0.615 | doc.rust-lang.org/book/print.html | 0.615 | doc.rust-lang.org/book/ch17-03-more-futures.html | 0.607 |
| crawl4ai-raw | #10 | doc.rust-lang.org/book/ch17-01-futures-and-syntax. | 0.615 | doc.rust-lang.org/book/print.html | 0.615 | doc.rust-lang.org/book/ch17-03-more-futures.html | 0.607 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.650 | doc.rust-lang.org/book/print.html | 0.650 | doc.rust-lang.org/book/print.html | 0.568 |
| crawlee | #5 | doc.rust-lang.org/book/ch17-01-futures-and-syntax. | 0.650 | doc.rust-lang.org/book/print.html | 0.650 | doc.rust-lang.org/book/ch17-01-futures-and-syntax. | 0.568 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.650 | doc.rust-lang.org/book/print.html | 0.650 | doc.rust-lang.org/book/print.html | 0.568 |
| playwright | #5 | doc.rust-lang.org/book/print.html | 0.650 | doc.rust-lang.org/book/ch17-01-futures-and-syntax. | 0.650 | doc.rust-lang.org/book/ch17-01-futures-and-syntax. | 0.568 |


**Q40: How does the `trpl::join` function differ from using `await` on individual futures?**
*(expects URL containing: `ch17-02-concurrency-with-async.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch17-02-concurrency-with-as | 0.686 | doc.rust-lang.org/book/print.html | 0.686 | doc.rust-lang.org/book/print.html | 0.593 |
| crawl4ai | #4 | doc.rust-lang.org/book/print.html | 0.660 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.660 | doc.rust-lang.org/book/print.html | 0.642 |
| crawl4ai-raw | #4 | doc.rust-lang.org/book/print.html | 0.660 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.660 | doc.rust-lang.org/book/print.html | 0.642 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.661 | doc.rust-lang.org/book/print.html | 0.661 | doc.rust-lang.org/book/print.html | 0.652 |
| crawlee | #1 | doc.rust-lang.org/book/ch17-02-concurrency-with-as | 0.661 | doc.rust-lang.org/book/print.html | 0.661 | doc.rust-lang.org/book/print.html | 0.652 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.661 | doc.rust-lang.org/stable/book/print.html | 0.661 | doc.rust-lang.org/book/print.html | 0.652 |
| playwright | #1 | doc.rust-lang.org/book/ch17-02-concurrency-with-as | 0.661 | doc.rust-lang.org/book/print.html | 0.661 | doc.rust-lang.org/book/print.html | 0.652 |


**Q41: What version of Rust does this book assume you are using?**
*(expects URL containing: `title-page.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | doc.rust-lang.org/book/ | 0.680 | doc.rust-lang.org/book/print.html | 0.680 | doc.rust-lang.org/book/appendix-05-editions.html | 0.651 |
| crawl4ai | #9 | doc.rust-lang.org/book/appendix-05-editions.html | 0.655 | doc.rust-lang.org/book/print.html | 0.655 | doc.rust-lang.org/stable/book/ch00-00-introduction | 0.636 |
| crawl4ai-raw | #9 | doc.rust-lang.org/book/appendix-05-editions.html | 0.655 | doc.rust-lang.org/book/print.html | 0.655 | doc.rust-lang.org/stable/book/ch00-00-introduction | 0.636 |
| scrapy+md | #2 | doc.rust-lang.org/book/ | 0.680 | doc.rust-lang.org/book/title-page.html | 0.680 | doc.rust-lang.org/book/ | 0.680 |
| crawlee | #9 | doc.rust-lang.org/book/appendix-05-editions.html | 0.656 | doc.rust-lang.org/book/appendix-05-editions.html | 0.640 | doc.rust-lang.org/stable/book/ch00-00-introduction | 0.636 |
| colly+md | #28 | doc.rust-lang.org/stable/book/appendix-05-editions | 0.656 | doc.rust-lang.org/book/appendix-05-editions.html | 0.656 | doc.rust-lang.org/book/ch00-00-introduction.html | 0.636 |
| playwright | #9 | doc.rust-lang.org/book/appendix-05-editions.html | 0.656 | doc.rust-lang.org/book/appendix-05-editions.html | 0.640 | doc.rust-lang.org/stable/book/ch00-00-introduction | 0.636 |


**Q42: Where can you find community translations of the Rust book?**
*(expects URL containing: `title-page.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | doc.rust-lang.org/book/ | 0.627 | doc.rust-lang.org/book/print.html | 0.627 | doc.rust-lang.org/book/print.html | 0.566 |
| crawl4ai | #5 | doc.rust-lang.org/book/appendix-06-translation.htm | 0.614 | doc.rust-lang.org/book/print.html | 0.584 | doc.rust-lang.org/stable/book/ | 0.581 |
| crawl4ai-raw | #5 | doc.rust-lang.org/book/appendix-06-translation.htm | 0.614 | doc.rust-lang.org/book/print.html | 0.584 | doc.rust-lang.org/stable/book/ | 0.581 |
| scrapy+md | #3 | doc.rust-lang.org/book/ | 0.627 | doc.rust-lang.org/book/print.html | 0.627 | doc.rust-lang.org/stable/book/title-page.html | 0.627 |
| crawlee | #4 | doc.rust-lang.org/book/appendix-06-translation.htm | 0.632 | doc.rust-lang.org/book/print.html | 0.593 | doc.rust-lang.org/book/ | 0.592 |
| colly+md | #13 | doc.rust-lang.org/stable/book/appendix-06-translat | 0.597 | doc.rust-lang.org/book/appendix-06-translation.htm | 0.597 | doc.rust-lang.org/stable/book/print.html | 0.567 |
| playwright | #5 | doc.rust-lang.org/book/appendix-06-translation.htm | 0.632 | doc.rust-lang.org/book/print.html | 0.593 | doc.rust-lang.org/book/ | 0.592 |


**Q43: What is the state pattern in object-oriented design?**
*(expects URL containing: `ch18-03-oo-design-patterns.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch18-03-oo-design-patterns. | 0.616 | doc.rust-lang.org/book/print.html | 0.586 | doc.rust-lang.org/book/ch18-03-oo-design-patterns. | 0.547 |
| crawl4ai | #3 | doc.rust-lang.org/book/print.html | 0.591 | doc.rust-lang.org/book/print.html | 0.512 | doc.rust-lang.org/book/ch18-03-oo-design-patterns. | 0.512 |
| crawl4ai-raw | #3 | doc.rust-lang.org/book/print.html | 0.591 | doc.rust-lang.org/book/print.html | 0.512 | doc.rust-lang.org/book/ch18-03-oo-design-patterns. | 0.512 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.586 | doc.rust-lang.org/book/print.html | 0.586 | doc.rust-lang.org/book/print.html | 0.547 |
| crawlee | #3 | doc.rust-lang.org/book/print.html | 0.586 | doc.rust-lang.org/book/print.html | 0.547 | doc.rust-lang.org/book/ch18-03-oo-design-patterns. | 0.547 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.586 | doc.rust-lang.org/stable/book/print.html | 0.586 | doc.rust-lang.org/book/print.html | 0.547 |
| playwright | #3 | doc.rust-lang.org/book/print.html | 0.586 | doc.rust-lang.org/book/print.html | 0.547 | doc.rust-lang.org/book/ch18-03-oo-design-patterns. | 0.547 |


**Q44: How does the `request_review` method change a post's state?**
*(expects URL containing: `ch18-03-oo-design-patterns.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.726 | doc.rust-lang.org/book/ch18-03-oo-design-patterns. | 0.726 | doc.rust-lang.org/book/print.html | 0.672 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.727 | doc.rust-lang.org/book/ch18-03-oo-design-patterns. | 0.727 | doc.rust-lang.org/book/print.html | 0.668 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.727 | doc.rust-lang.org/book/ch18-03-oo-design-patterns. | 0.727 | doc.rust-lang.org/book/print.html | 0.668 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.644 | doc.rust-lang.org/book/print.html | 0.644 | doc.rust-lang.org/book/print.html | 0.627 |
| crawlee | #1 | doc.rust-lang.org/book/ch18-03-oo-design-patterns. | 0.644 | doc.rust-lang.org/book/print.html | 0.644 | doc.rust-lang.org/book/print.html | 0.627 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.644 | doc.rust-lang.org/stable/book/print.html | 0.644 | doc.rust-lang.org/book/print.html | 0.627 |
| playwright | #1 | doc.rust-lang.org/book/ch18-03-oo-design-patterns. | 0.645 | doc.rust-lang.org/book/print.html | 0.645 | doc.rust-lang.org/book/ch18-03-oo-design-patterns. | 0.627 |


**Q45: What are patterns in Rust?**
*(expects URL containing: `ch19-00-patterns.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.748 | doc.rust-lang.org/book/print.html | 0.723 | doc.rust-lang.org/book/ch19-01-all-the-places-for- | 0.644 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.723 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.705 | doc.rust-lang.org/book/ch19-01-all-the-places-for- | 0.664 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.723 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.705 | doc.rust-lang.org/book/ch19-01-all-the-places-for- | 0.664 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.723 | doc.rust-lang.org/stable/book/print.html | 0.723 | doc.rust-lang.org/book/print.html | 0.626 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.723 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.685 | doc.rust-lang.org/book/ch19-01-all-the-places-for- | 0.646 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.723 | doc.rust-lang.org/book/print.html | 0.723 | doc.rust-lang.org/book/print.html | 0.626 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.723 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.685 | doc.rust-lang.org/book/ch19-01-all-the-places-for- | 0.646 |


**Q46: What components can a pattern consist of?**
*(expects URL containing: `ch19-00-patterns.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.530 | doc.rust-lang.org/book/ch19-03-pattern-syntax.html | 0.508 | doc.rust-lang.org/book/print.html | 0.508 |
| crawl4ai | #19 | doc.rust-lang.org/book/print.html | 0.474 | doc.rust-lang.org/book/print.html | 0.470 | doc.rust-lang.org/book/ch19-01-all-the-places-for- | 0.467 |
| crawl4ai-raw | #19 | doc.rust-lang.org/book/print.html | 0.474 | doc.rust-lang.org/book/print.html | 0.470 | doc.rust-lang.org/book/ch19-01-all-the-places-for- | 0.467 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.472 | doc.rust-lang.org/book/print.html | 0.472 | doc.rust-lang.org/book/print.html | 0.471 |
| crawlee | #27 | doc.rust-lang.org/book/print.html | 0.472 | doc.rust-lang.org/book/print.html | 0.471 | doc.rust-lang.org/book/ch19-03-pattern-syntax.html | 0.463 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.472 | doc.rust-lang.org/stable/book/print.html | 0.472 | doc.rust-lang.org/book/print.html | 0.471 |
| playwright | #27 | doc.rust-lang.org/book/print.html | 0.472 | doc.rust-lang.org/book/print.html | 0.471 | doc.rust-lang.org/book/ch19-03-pattern-syntax.html | 0.463 |


**Q47: What is a mutex and how does it control access to data?**
*(expects URL containing: `ch16-03-shared-state.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.589 | doc.rust-lang.org/book/print.html | 0.589 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.559 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.593 | doc.rust-lang.org/book/print.html | 0.593 | doc.rust-lang.org/book/print.html | 0.558 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.593 | doc.rust-lang.org/book/print.html | 0.593 | doc.rust-lang.org/book/print.html | 0.558 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.589 | doc.rust-lang.org/book/print.html | 0.589 | doc.rust-lang.org/stable/book/print.html | 0.541 |
| crawlee | #1 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.589 | doc.rust-lang.org/book/print.html | 0.589 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.541 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.589 | doc.rust-lang.org/stable/book/print.html | 0.589 | doc.rust-lang.org/stable/book/print.html | 0.541 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.589 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.589 | doc.rust-lang.org/book/print.html | 0.541 |


**Q48: Why is `Rc<T>` not safe to share across threads in Rust?**
*(expects URL containing: `ch16-03-shared-state.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/ch15-04-rc.html | 0.659 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.649 | doc.rust-lang.org/book/print.html | 0.649 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.657 | doc.rust-lang.org/book/print.html | 0.657 | doc.rust-lang.org/book/ch15-04-rc.html | 0.620 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.657 | doc.rust-lang.org/book/print.html | 0.657 | doc.rust-lang.org/book/ch15-04-rc.html | 0.620 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.649 | doc.rust-lang.org/book/print.html | 0.649 | doc.rust-lang.org/stable/book/print.html | 0.623 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.649 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.649 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.623 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.649 | doc.rust-lang.org/book/print.html | 0.649 | doc.rust-lang.org/stable/book/print.html | 0.623 |
| playwright | #1 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.649 | doc.rust-lang.org/book/print.html | 0.649 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.623 |


**Q49: How do you declare a module in Rust?**
*(expects URL containing: `ch07-02-defining-modules-to-control-scope-and-privacy.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | doc.rust-lang.org/book/print.html | 0.608 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.588 | doc.rust-lang.org/book/print.html | 0.585 |
| crawl4ai | #15 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.598 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.598 | doc.rust-lang.org/book/ch07-03-paths-for-referring | 0.597 |
| crawl4ai-raw | #15 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.598 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.598 | doc.rust-lang.org/book/ch07-03-paths-for-referring | 0.597 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.608 | doc.rust-lang.org/book/print.html | 0.608 | doc.rust-lang.org/stable/book/print.html | 0.588 |
| crawlee | #8 | doc.rust-lang.org/book/print.html | 0.608 | doc.rust-lang.org/book/print.html | 0.588 | doc.rust-lang.org/book/ch07-03-paths-for-referring | 0.588 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.608 | doc.rust-lang.org/stable/book/print.html | 0.608 | doc.rust-lang.org/stable/book/print.html | 0.588 |
| playwright | #8 | doc.rust-lang.org/book/print.html | 0.608 | doc.rust-lang.org/stable/book/ch07-03-paths-for-re | 0.588 | doc.rust-lang.org/book/ch07-03-paths-for-referring | 0.588 |


**Q50: What is the default visibility of items within a module?**
*(expects URL containing: `ch07-02-defining-modules-to-control-scope-and-privacy.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | doc.rust-lang.org/book/ch07-03-paths-for-referring | 0.484 | doc.rust-lang.org/book/print.html | 0.483 | doc.rust-lang.org/book/ch07-02-defining-modules-to | 0.392 |
| crawl4ai | #9 | doc.rust-lang.org/book/ch07-03-paths-for-referring | 0.388 | doc.rust-lang.org/book/print.html | 0.388 | doc.rust-lang.org/stable/book/ch07-03-paths-for-re | 0.388 |
| crawl4ai-raw | #9 | doc.rust-lang.org/book/ch07-03-paths-for-referring | 0.388 | doc.rust-lang.org/book/print.html | 0.388 | doc.rust-lang.org/stable/book/ch07-03-paths-for-re | 0.388 |
| scrapy+md | miss | doc.rust-lang.org/reference/items/traits.html | 0.383 | doc.rust-lang.org/book/print.html | 0.366 | doc.rust-lang.org/stable/book/print.html | 0.366 |
| crawlee | #7 | doc.rust-lang.org/book/print.html | 0.366 | doc.rust-lang.org/stable/book/ch07-03-paths-for-re | 0.366 | doc.rust-lang.org/book/ch07-03-paths-for-referring | 0.366 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.366 | doc.rust-lang.org/stable/book/print.html | 0.366 | doc.rust-lang.org/reference/items/traits.html#dyn- | 0.364 |
| playwright | #7 | doc.rust-lang.org/stable/book/ch07-03-paths-for-re | 0.366 | doc.rust-lang.org/book/print.html | 0.366 | doc.rust-lang.org/book/ch07-03-paths-for-referring | 0.366 |


**Q51: What is a Vec in Rust?**
*(expects URL containing: `struct.Vec.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | doc.rust-lang.org/book/print.html | 0.532 | doc.rust-lang.org/book/ch08-01-vectors.html | 0.532 | doc.rust-lang.org/book/ch08-01-vectors.html | 0.514 |
| crawl4ai | #1 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.675 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.649 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.612 |
| crawl4ai-raw | #1 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.675 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.649 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.612 |
| scrapy+md | #2 | doc.rust-lang.org/nomicon/vec/vec.html | 0.651 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.576 | doc.rust-lang.org/stable/book/print.html | 0.557 |
| crawlee | #1 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.645 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.627 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.576 |
| colly+md | #1 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.652 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.622 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.577 |
| playwright | #1 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.645 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.627 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.576 |


**Q52: How do you create a new empty Vec in Rust?**
*(expects URL containing: `struct.Vec.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | doc.rust-lang.org/book/ch08-01-vectors.html | 0.525 | doc.rust-lang.org/book/print.html | 0.525 | doc.rust-lang.org/book/ch08-01-vectors.html | 0.502 |
| crawl4ai | #1 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.625 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.611 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.608 |
| crawl4ai-raw | #1 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.625 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.611 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.608 |
| scrapy+md | #2 | doc.rust-lang.org/nomicon/vec/vec.html | 0.625 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.571 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.537 |
| crawlee | #1 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.591 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.579 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.571 |
| colly+md | #1 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.599 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.576 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.571 |
| playwright | #1 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.591 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.579 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.571 |


**Q53: What does the `Debug` trait enable in Rust?**
*(expects URL containing: `appendix-03-derivable-traits.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #10 | doc.rust-lang.org/book/ch05-02-example-structs.htm | 0.626 | doc.rust-lang.org/book/print.html | 0.626 | doc.rust-lang.org/book/print.html | 0.590 |
| crawl4ai | #23 | doc.rust-lang.org/book/ch05-02-example-structs.htm | 0.629 | doc.rust-lang.org/stable/book/ch05-02-example-stru | 0.629 | doc.rust-lang.org/book/print.html | 0.629 |
| crawl4ai-raw | #23 | doc.rust-lang.org/book/ch05-02-example-structs.htm | 0.629 | doc.rust-lang.org/stable/book/ch05-02-example-stru | 0.629 | doc.rust-lang.org/book/print.html | 0.629 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.646 | doc.rust-lang.org/book/print.html | 0.646 | doc.rust-lang.org/book/print.html | 0.570 |
| crawlee | #20 | doc.rust-lang.org/stable/book/ch05-02-example-stru | 0.646 | doc.rust-lang.org/book/print.html | 0.646 | doc.rust-lang.org/book/ch05-02-example-structs.htm | 0.646 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.646 | doc.rust-lang.org/stable/book/print.html | 0.646 | doc.rust-lang.org/cargo/reference/profiles.html | 0.579 |
| playwright | #19 | doc.rust-lang.org/book/print.html | 0.646 | doc.rust-lang.org/book/ch05-02-example-structs.htm | 0.646 | doc.rust-lang.org/stable/book/ch05-02-example-stru | 0.646 |


**Q54: What is the purpose of the `Default` trait in Rust?**
*(expects URL containing: `appendix-03-derivable-traits.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | doc.rust-lang.org/book/print.html | 0.576 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.576 | doc.rust-lang.org/book/print.html | 0.566 |
| crawl4ai | #1 | doc.rust-lang.org/book/appendix-03-derivable-trait | 0.616 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.571 | doc.rust-lang.org/book/print.html | 0.571 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/appendix-03-derivable-trait | 0.616 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.571 | doc.rust-lang.org/book/print.html | 0.571 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.586 | doc.rust-lang.org/book/print.html | 0.586 | doc.rust-lang.org/book/print.html | 0.558 |
| crawlee | #6 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.586 | doc.rust-lang.org/book/print.html | 0.586 | doc.rust-lang.org/book/print.html | 0.558 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.586 | doc.rust-lang.org/book/print.html | 0.586 | doc.rust-lang.org/stable/book/print.html | 0.558 |
| playwright | #6 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.586 | doc.rust-lang.org/book/print.html | 0.586 | doc.rust-lang.org/book/print.html | 0.558 |


**Q55: What programming concepts are covered in this chapter?**
*(expects URL containing: `ch03-00-common-programming-concepts.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch03-00-common-programming- | 0.551 | doc.rust-lang.org/book/print.html | 0.521 | doc.rust-lang.org/book/ch00-00-introduction.html | 0.521 |
| crawl4ai | #9 | doc.rust-lang.org/book/print.html | 0.523 | doc.rust-lang.org/stable/book/ch00-00-introduction | 0.523 | doc.rust-lang.org/book/ch00-00-introduction.html | 0.523 |
| crawl4ai-raw | #9 | doc.rust-lang.org/book/print.html | 0.523 | doc.rust-lang.org/stable/book/ch00-00-introduction | 0.523 | doc.rust-lang.org/book/ch00-00-introduction.html | 0.523 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/ch00-00-introduction | 0.521 | doc.rust-lang.org/book/print.html | 0.521 | doc.rust-lang.org/stable/book/print.html | 0.521 |
| crawlee | #10 | doc.rust-lang.org/stable/book/ch00-00-introduction | 0.521 | doc.rust-lang.org/book/print.html | 0.521 | doc.rust-lang.org/book/ch00-00-introduction.html | 0.521 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.521 | doc.rust-lang.org/book/print.html | 0.521 | doc.rust-lang.org/book/ch00-00-introduction.html | 0.521 |
| playwright | #10 | doc.rust-lang.org/stable/book/ch00-00-introduction | 0.521 | doc.rust-lang.org/book/ch00-00-introduction.html | 0.521 | doc.rust-lang.org/book/print.html | 0.521 |


**Q56: What are keywords in the Rust programming language?**
*(expects URL containing: `ch03-00-common-programming-concepts.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/appendix-01-keywords.html | 0.684 | doc.rust-lang.org/book/ch03-00-common-programming- | 0.683 | doc.rust-lang.org/book/print.html | 0.664 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch03-00-common-programming- | 0.665 | doc.rust-lang.org/stable/book/ch03-00-common-progr | 0.665 | doc.rust-lang.org/book/appendix-01-keywords.html | 0.642 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch03-00-common-programming- | 0.665 | doc.rust-lang.org/stable/book/ch03-00-common-progr | 0.665 | doc.rust-lang.org/book/appendix-01-keywords.html | 0.642 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.666 | doc.rust-lang.org/stable/book/print.html | 0.666 | doc.rust-lang.org/stable/book/print.html | 0.628 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.666 | doc.rust-lang.org/book/ch03-00-common-programming- | 0.660 | doc.rust-lang.org/stable/book/ch03-00-common-progr | 0.660 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.666 | doc.rust-lang.org/book/print.html | 0.666 | doc.rust-lang.org/stable/book/print.html | 0.628 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.666 | doc.rust-lang.org/book/ch03-00-common-programming- | 0.660 | doc.rust-lang.org/stable/book/ch03-00-common-progr | 0.660 |


**Q57: What are the three collections discussed in Rust's standard library?**
*(expects URL containing: `ch08-00-common-collections.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch08-00-common-collections. | 0.714 | doc.rust-lang.org/book/print.html | 0.616 | doc.rust-lang.org/book/appendix-00.html | 0.530 |
| crawl4ai | #2 | doc.rust-lang.org/std/collections/index.html | 0.700 | doc.rust-lang.org/stable/book/ch08-00-common-colle | 0.634 | doc.rust-lang.org/book/ch08-00-common-collections. | 0.634 |
| crawl4ai-raw | #2 | doc.rust-lang.org/std/collections/index.html | 0.700 | doc.rust-lang.org/stable/book/ch08-00-common-colle | 0.634 | doc.rust-lang.org/book/ch08-00-common-collections. | 0.634 |
| scrapy+md | miss | doc.rust-lang.org/std/collections/index.html | 0.627 | doc.rust-lang.org/book/print.html | 0.616 | doc.rust-lang.org/stable/book/print.html | 0.616 |
| crawlee | #3 | doc.rust-lang.org/std/collections/index.html | 0.682 | doc.rust-lang.org/std/collections/index.html | 0.652 | doc.rust-lang.org/book/ch08-00-common-collections. | 0.623 |
| colly+md | miss | doc.rust-lang.org/std/collections/index.html | 0.678 | doc.rust-lang.org/book/print.html | 0.616 | doc.rust-lang.org/stable/book/print.html | 0.616 |
| playwright | #3 | doc.rust-lang.org/std/collections/index.html | 0.682 | doc.rust-lang.org/std/collections/index.html | 0.652 | doc.rust-lang.org/book/ch08-00-common-collections. | 0.623 |


**Q58: How does a vector differ from built-in array and tuple types in Rust?**
*(expects URL containing: `ch08-00-common-collections.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch08-00-common-collections. | 0.603 | doc.rust-lang.org/book/ch03-02-data-types.html | 0.597 | doc.rust-lang.org/book/print.html | 0.597 |
| crawl4ai | miss | doc.rust-lang.org/book/ch08-01-vectors.html | 0.620 | doc.rust-lang.org/stable/book/ch08-01-vectors.html | 0.620 | doc.rust-lang.org/book/print.html | 0.605 |
| crawl4ai-raw | miss | doc.rust-lang.org/book/ch08-01-vectors.html | 0.620 | doc.rust-lang.org/stable/book/ch08-01-vectors.html | 0.620 | doc.rust-lang.org/book/print.html | 0.605 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.598 | doc.rust-lang.org/stable/book/print.html | 0.598 | doc.rust-lang.org/book/print.html | 0.597 |
| crawlee | miss | doc.rust-lang.org/book/ch08-01-vectors.html | 0.605 | doc.rust-lang.org/stable/book/ch08-01-vectors.html | 0.605 | doc.rust-lang.org/book/print.html | 0.598 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.598 | doc.rust-lang.org/stable/book/print.html | 0.598 | doc.rust-lang.org/book/print.html | 0.597 |
| playwright | miss | doc.rust-lang.org/book/ch08-01-vectors.html | 0.605 | doc.rust-lang.org/stable/book/ch08-01-vectors.html | 0.605 | doc.rust-lang.org/book/print.html | 0.598 |


**Q59: What command do I use to upload a crate to crates.io?**
*(expects URL containing: `publishing.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | doc.rust-lang.org/book/ch14-00-more-about-cargo.ht | 0.556 | doc.rust-lang.org/book/print.html | 0.518 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.518 |
| crawl4ai | #3 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.531 | doc.rust-lang.org/book/print.html | 0.531 | doc.rust-lang.org/cargo/reference/publishing.html | 0.524 |
| crawl4ai-raw | #3 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.531 | doc.rust-lang.org/book/print.html | 0.531 | doc.rust-lang.org/cargo/reference/publishing.html | 0.524 |
| scrapy+md | #1 | doc.rust-lang.org/cargo/reference/publishing.html | 0.539 | doc.rust-lang.org/cargo/reference/publishing.html | 0.539 | doc.rust-lang.org/stable/book/print.html | 0.532 |
| crawlee | #1 | doc.rust-lang.org/cargo/reference/publishing.html | 0.539 | doc.rust-lang.org/book/print.html | 0.532 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.532 |
| colly+md | #3 | doc.rust-lang.org/book/print.html | 0.532 | doc.rust-lang.org/stable/book/print.html | 0.532 | doc.rust-lang.org/cargo/reference/publishing.html | 0.528 |
| playwright | #1 | doc.rust-lang.org/cargo/reference/publishing.html | 0.539 | doc.rust-lang.org/book/print.html | 0.532 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.532 |


**Q60: How do I revoke an API token on crates.io?**
*(expects URL containing: `publishing.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | doc.rust-lang.org/book/print.html | 0.495 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.495 | doc.rust-lang.org/book/print.html | 0.397 |
| crawl4ai | #3 | doc.rust-lang.org/book/print.html | 0.538 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.538 | doc.rust-lang.org/cargo/reference/publishing.html | 0.472 |
| crawl4ai-raw | #3 | doc.rust-lang.org/book/print.html | 0.538 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.538 | doc.rust-lang.org/cargo/reference/publishing.html | 0.472 |
| scrapy+md | #3 | doc.rust-lang.org/stable/book/print.html | 0.538 | doc.rust-lang.org/book/print.html | 0.538 | doc.rust-lang.org/cargo/reference/publishing.html | 0.513 |
| crawlee | #3 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.538 | doc.rust-lang.org/book/print.html | 0.538 | doc.rust-lang.org/cargo/reference/publishing.html | 0.459 |
| colly+md | #3 | doc.rust-lang.org/stable/book/print.html | 0.538 | doc.rust-lang.org/book/print.html | 0.538 | doc.rust-lang.org/cargo/reference/publishing.html | 0.478 |
| playwright | #3 | doc.rust-lang.org/book/print.html | 0.538 | doc.rust-lang.org/book/ch14-02-publishing-to-crate | 0.538 | doc.rust-lang.org/cargo/reference/publishing.html | 0.459 |


</details>

## smittenkitchen

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai-raw | 85% (34/40) | 95% (38/40) | 98% (39/40) | 98% (39/40) | 98% (39/40) | 0.897 | 773 | 200 |
| playwright | 85% (34/40) | 88% (35/40) | 95% (38/40) | 98% (39/40) | 100% (40/40) | 0.885 | 3029 | 200 |
| crawl4ai | 80% (32/40) | 95% (38/40) | 98% (39/40) | 98% (39/40) | 98% (39/40) | 0.876 | 773 | 200 |
| crawlee | 70% (28/40) | 88% (35/40) | 88% (35/40) | 88% (35/40) | 88% (35/40) | 0.767 | 4167 | 203 |
| colly+md | 62% (25/40) | 75% (30/40) | 75% (30/40) | 80% (32/40) | 80% (32/40) | 0.674 | 3708 | 199 |
| markcrawl | 18% (7/40) | 22% (9/40) | 25% (10/40) | 32% (13/40) | 35% (14/40) | 0.213 | 10115 | 200 |
| scrapy+md | 2% (1/40) | 2% (1/40) | 5% (2/40) | 5% (2/40) | 5% (2/40) | 0.030 | 18860 | 138 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for smittenkitchen</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What are some recipes featured in the greens category?**
*(expects URL containing: `greens`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2022/11/green-angel-hair-with-g | 0.584 | smittenkitchen.com/2013/01/pasta-and-white-beans-w | 0.552 | smittenkitchen.com/2012/04/pasta-with-garlicky-bro | 0.545 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/vegetable/greens/esca | 0.535 | smittenkitchen.com/./recipes/vegetable/greens/?for | 0.513 | smittenkitchen.com/./recipes/vegetable/greens/esca | 0.506 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/vegetable/greens/esca | 0.535 | smittenkitchen.com/./recipes/vegetable/greens/?for | 0.513 | smittenkitchen.com/./recipes/vegetable/greens/arug | 0.506 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.529 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.493 | smittenkitchen.com/recipes/ | 0.470 |
| crawlee | #1 | smittenkitchen.com/./recipes/vegetable/greens/?for | 0.525 | smittenkitchen.com/./recipes/vegetable/green-beans | 0.496 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.493 |
| colly+md | #1 | smittenkitchen.com/recipes/vegetable/greens/?forma | 0.570 | smittenkitchen.com/recipes/vegetable/greens/spinac | 0.495 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.493 |
| playwright | #1 | smittenkitchen.com/recipes/vegetable/greens/?forma | 0.575 | smittenkitchen.com/recipes/vegetable/green-beans/? | 0.522 | smittenkitchen.com/recipes/vegetable/greens/spinac | 0.496 |


**Q2: What is the first recipe listed on the greens page?**
*(expects URL containing: `greens`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2022/11/green-angel-hair-with-g | 0.552 | smittenkitchen.com/2012/04/pasta-with-garlicky-bro | 0.540 | smittenkitchen.com/2013/01/pasta-and-white-beans-w | 0.518 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/vegetable/greens/arug | 0.526 | smittenkitchen.com/./recipes/vegetable/greens/swis | 0.521 | smittenkitchen.com/./recipes/vegetable/greens/esca | 0.517 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/vegetable/greens/arug | 0.526 | smittenkitchen.com/./recipes/vegetable/greens/swis | 0.521 | smittenkitchen.com/./recipes/vegetable/greens/endi | 0.516 |
| scrapy+md | miss | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.491 | smittenkitchen.com/2017/09/pizza-beans/ | 0.469 | smittenkitchen.com/recipes/ | 0.454 |
| crawlee | #1 | smittenkitchen.com/./recipes/vegetable/greens/?for | 0.503 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.492 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.491 |
| colly+md | #1 | smittenkitchen.com/recipes/vegetable/greens/?forma | 0.515 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.492 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.491 |
| playwright | #1 | smittenkitchen.com/recipes/vegetable/greens/?forma | 0.518 | smittenkitchen.com/recipes/vegetable/green-beans/? | 0.471 | smittenkitchen.com/recipes/vegetable/greens/spinac | 0.446 |


**Q3: What does the Smitten Kitchen newsletter include?**
*(expects URL containing: `subscribe`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/subscribe/ | 0.689 | smittenkitchen.com/2025/09/cabbage-and-halloumi-sk | 0.624 | smittenkitchen.com/privacy-policy/ | 0.606 |
| crawl4ai | #1 | smittenkitchen.com/subscribe/ | 0.648 | smittenkitchen.com/subscribe/ | 0.631 | smittenkitchen.com/about/ | 0.614 |
| crawl4ai-raw | #1 | smittenkitchen.com/subscribe/ | 0.648 | smittenkitchen.com/subscribe/ | 0.631 | smittenkitchen.com/about/ | 0.614 |
| scrapy+md | miss | smittenkitchen.com/privacy-policy/ | 0.579 | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.519 | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.519 |
| crawlee | #1 | smittenkitchen.com/subscribe/ | 0.675 | smittenkitchen.com/privacy-policy/ | 0.645 | smittenkitchen.com/subscribe/ | 0.618 |
| colly+md | #1 | smittenkitchen.com/subscribe/ | 0.620 | smittenkitchen.com/subscribe/ | 0.618 | smittenkitchen.com/subscribe/ | 0.601 |
| playwright | #1 | smittenkitchen.com/subscribe/ | 0.620 | smittenkitchen.com/subscribe/ | 0.618 | smittenkitchen.com/about/ | 0.613 |


**Q4: How can I unsubscribe from the Smitten Kitchen newsletter?**
*(expects URL containing: `subscribe`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | smittenkitchen.com/privacy-policy/ | 0.592 | smittenkitchen.com/subscribe/ | 0.585 | smittenkitchen.com/subscribe/ | 0.570 |
| crawl4ai | #1 | smittenkitchen.com/subscribe/ | 0.589 | smittenkitchen.com/subscribe/ | 0.584 | smittenkitchen.com/subscribe/ | 0.562 |
| crawl4ai-raw | #1 | smittenkitchen.com/subscribe/ | 0.589 | smittenkitchen.com/subscribe/ | 0.584 | smittenkitchen.com/subscribe/ | 0.562 |
| scrapy+md | miss | smittenkitchen.com/privacy-policy/ | 0.555 | smittenkitchen.com/2007/02/knotted-and-stacked-dis | 0.416 | smittenkitchen.com/2007/02/knotted-and-stacked-dis | 0.415 |
| crawlee | #2 | smittenkitchen.com/privacy-policy/ | 0.575 | smittenkitchen.com/subscribe/ | 0.571 | smittenkitchen.com/subscribe/ | 0.568 |
| colly+md | #1 | smittenkitchen.com/subscribe/ | 0.571 | smittenkitchen.com/subscribe/ | 0.561 | smittenkitchen.com/subscribe/ | 0.560 |
| playwright | #1 | smittenkitchen.com/subscribe/ | 0.571 | smittenkitchen.com/subscribe/ | 0.561 | smittenkitchen.com/subscribe/ | 0.560 |


**Q5: What are some recipes that include bananas?**
*(expects URL containing: `bananas`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2014/03/double-chocolate-banana | 0.606 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.598 | smittenkitchen.com/2014/03/double-chocolate-banana | 0.594 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/fruit/bananas/?format | 0.464 | smittenkitchen.com/about/faq/ | 0.415 | smittenkitchen.com/ | 0.407 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/fruit/bananas/?format | 0.465 | smittenkitchen.com/about/faq/ | 0.415 | smittenkitchen.com/ | 0.407 |
| scrapy+md | miss | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.579 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.570 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.569 |
| crawlee | miss | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.654 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.600 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.571 |
| colly+md | #3 | smittenkitchen.com/2026/02/banana-chocolate-chip-c | 0.585 | smittenkitchen.com/2026/02/banana-chocolate-chip-c | 0.584 | smittenkitchen.com/recipes/fruit/bananas/ | 0.580 |
| playwright | #1 | smittenkitchen.com/recipes/fruit/bananas/?format=p | 0.578 | smittenkitchen.com/recipes/sweets/everyday-cakes/? | 0.448 | smittenkitchen.com/recipes/sweets/cake/?format=pho | 0.433 |


**Q6: What are some breakfast recipes available on Smitten Kitchen?**
*(expects URL containing: `breakfast`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2020/10/morning-glory-breakfast | 0.632 | smittenkitchen.com/2025/05/eggs-florentine/ | 0.584 | smittenkitchen.com/2009/12/how-to-host-brunch-and- | 0.583 |
| crawl4ai | #2 | smittenkitchen.com/recipes/ | 0.615 | smittenkitchen.com/./recipes/course/breakfast/?for | 0.615 | smittenkitchen.com/./recipes/course/pancakes/?form | 0.611 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/course/breakfast/?for | 0.615 | smittenkitchen.com/./recipes/course/pancakes/?form | 0.612 | smittenkitchen.com/travel/ten-days-in-ireland/ | 0.608 |
| scrapy+md | #1 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.547 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.542 | smittenkitchen.com/2007/02/sour-cream-bran-muffins | 0.542 |
| crawlee | #1 | smittenkitchen.com/./recipes/course/breakfast/?for | 0.617 | smittenkitchen.com/./recipes/ingredient/eggs/?form | 0.604 | smittenkitchen.com/./recipes/holiday/easter/?forma | 0.602 |
| colly+md | miss | smittenkitchen.com/recipes/course/brunch/?format=p | 0.628 | smittenkitchen.com/recipes/ingredient/eggs/?format | 0.619 | smittenkitchen.com/recipes/course/scones-biscuits/ | 0.612 |
| playwright | #1 | smittenkitchen.com/recipes/course/breakfast/?forma | 0.650 | smittenkitchen.com/recipes/course/brunch/?format=p | 0.625 | smittenkitchen.com/recipes/course/pancakes/?format | 0.623 |


**Q7: What are some meat recipes available on Smitten Kitchen?**
*(expects URL containing: `meat`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2016/02/everyday-meatballs/ | 0.605 | smittenkitchen.com/2020/10/morning-glory-breakfast | 0.576 | smittenkitchen.com/2016/02/everyday-meatballs/ | 0.575 |
| crawl4ai | #2 | smittenkitchen.com/recipes/ | 0.642 | smittenkitchen.com/./recipes/ingredient/meat/turke | 0.634 | smittenkitchen.com/./recipes/ingredient/meat/lamb/ | 0.634 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/ingredient/meat/turke | 0.634 | smittenkitchen.com/./recipes/ingredient/meat/lamb/ | 0.632 | smittenkitchen.com/./recipes/ingredient/meat/?form | 0.632 |
| scrapy+md | #5 | smittenkitchen.com/2017/09/pizza-beans/ | 0.535 | smittenkitchen.com/recipes/ | 0.532 | smittenkitchen.com/recipes/ | 0.532 |
| crawlee | #1 | smittenkitchen.com/./recipes/ingredient/meat/?form | 0.639 | smittenkitchen.com/./recipes/ingredient/meat/lamb/ | 0.616 | smittenkitchen.com/./recipes/ingredient/meat/turke | 0.615 |
| colly+md | #1 | smittenkitchen.com/recipes/ingredient/meat/?format | 0.653 | smittenkitchen.com/recipes/ingredient/meat/ | 0.653 | smittenkitchen.com/recipes/ingredient/meat/beef/?f | 0.636 |
| playwright | #1 | smittenkitchen.com/recipes/ingredient/meat/?format | 0.648 | smittenkitchen.com/recipes/ingredient/meat/beef/?f | 0.636 | smittenkitchen.com/recipes | 0.621 |


**Q8: What is the main focus of the Smitten Kitchen blog?**
*(expects URL containing: `about`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.600 | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.578 | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.575 |
| crawl4ai | #1 | smittenkitchen.com/about/ | 0.653 | smittenkitchen.com/about/ | 0.645 | smittenkitchen.com/about/ | 0.609 |
| crawl4ai-raw | #1 | smittenkitchen.com/about/ | 0.653 | smittenkitchen.com/about/ | 0.645 | smittenkitchen.com/about/ | 0.609 |
| scrapy+md | miss | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.503 | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.503 | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.503 |
| crawlee | #1 | smittenkitchen.com/about/ | 0.678 | smittenkitchen.com/about/ | 0.638 | smittenkitchen.com/./recipes/cuisine/middle-easter | 0.613 |
| colly+md | miss | smittenkitchen.com/books/ | 0.609 | smittenkitchen.com/recipes/best-of-smitten-kitchen | 0.606 | smittenkitchen.com/recipes/ | 0.596 |
| playwright | #1 | smittenkitchen.com/about/ | 0.665 | smittenkitchen.com/about/ | 0.638 | smittenkitchen.com/book/ | 0.607 |


**Q9: Who is the author of Smitten Kitchen and what is her background?**
*(expects URL containing: `about`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/books/ | 0.573 | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.554 | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.547 |
| crawl4ai | #1 | smittenkitchen.com/about/faq/ | 0.601 | smittenkitchen.com/about/ | 0.586 | smittenkitchen.com/about/ | 0.578 |
| crawl4ai-raw | #1 | smittenkitchen.com/about/faq/ | 0.601 | smittenkitchen.com/about/ | 0.586 | smittenkitchen.com/about/ | 0.578 |
| scrapy+md | miss | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.472 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.472 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.472 |
| crawlee | #3 | smittenkitchen.com/book/ | 0.595 | smittenkitchen.com/books/ | 0.595 | smittenkitchen.com/about/ | 0.582 |
| colly+md | #3 | smittenkitchen.com/books/ | 0.596 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.530 | smittenkitchen.com/about/faq/ | 0.523 |
| playwright | #2 | smittenkitchen.com/book/ | 0.594 | smittenkitchen.com/about/ | 0.578 | smittenkitchen.com/about/ | 0.575 |


**Q10: What were the main goals of the trip to London?**
*(expects URL containing: `five-days-in-london`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.400 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.390 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.363 |
| crawl4ai | #1 | smittenkitchen.com/travel/five-days-in-london/ | 0.497 | smittenkitchen.com/travel/five-days-in-london/ | 0.477 | smittenkitchen.com/travel/five-days-in-london/ | 0.469 |
| crawl4ai-raw | #1 | smittenkitchen.com/travel/five-days-in-london/ | 0.497 | smittenkitchen.com/travel/five-days-in-london/ | 0.477 | smittenkitchen.com/travel/five-days-in-london/ | 0.469 |
| scrapy+md | miss | smittenkitchen.com/2022/03/castle-breakfast/ | 0.242 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.227 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.190 |
| crawlee | #1 | smittenkitchen.com/travel/five-days-in-london/ | 0.487 | smittenkitchen.com/travel/five-days-in-london/ | 0.486 | smittenkitchen.com/travel/five-days-in-london/ | 0.483 |
| colly+md | #1 | smittenkitchen.com/travel/five-days-in-london/ | 0.487 | smittenkitchen.com/travel/five-days-in-london/ | 0.486 | smittenkitchen.com/travel/five-days-in-london/ | 0.483 |
| playwright | #1 | smittenkitchen.com/travel/five-days-in-london/ | 0.487 | smittenkitchen.com/travel/five-days-in-london/ | 0.486 | smittenkitchen.com/travel/five-days-in-london/ | 0.483 |


**Q11: Which restaurant had the best fish and chips according to the author?**
*(expects URL containing: `five-days-in-london`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2014/11/smoked-whitefish-dip-wi | 0.451 | smittenkitchen.com/2014/11/smoked-whitefish-dip-wi | 0.430 | smittenkitchen.com/2014/11/smoked-whitefish-dip-wi | 0.419 |
| crawl4ai | #2 | smittenkitchen.com/travel/debs-new-york/ | 0.415 | smittenkitchen.com/travel/five-days-in-london/ | 0.408 | smittenkitchen.com/travel/nine-days-in-scotland/ | 0.400 |
| crawl4ai-raw | #2 | smittenkitchen.com/travel/debs-new-york/ | 0.415 | smittenkitchen.com/travel/five-days-in-london/ | 0.408 | smittenkitchen.com/travel/nine-days-in-scotland/ | 0.400 |
| scrapy+md | miss | smittenkitchen.com/2007/02/sour-cream-bran-muffins | 0.362 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.340 | smittenkitchen.com/2010/01/best-cocoa-brownies/?re | 0.332 |
| crawlee | #3 | smittenkitchen.com/travel/debs-new-york/ | 0.406 | smittenkitchen.com/travel/nine-days-in-scotland/ | 0.403 | smittenkitchen.com/travel/five-days-in-london/ | 0.395 |
| colly+md | #3 | smittenkitchen.com/travel/debs-new-york/ | 0.406 | smittenkitchen.com/recipes/ingredient/seafood/?for | 0.399 | smittenkitchen.com/travel/five-days-in-london/ | 0.395 |
| playwright | #4 | smittenkitchen.com/travel/debs-new-york/ | 0.406 | smittenkitchen.com/travel/nine-days-in-scotland/ | 0.403 | smittenkitchen.com/recipes/ingredient/seafood/?for | 0.397 |


**Q12: What are some recommended restaurants in Barcelona from the trip to Spain?**
*(expects URL containing: `a-few-favorites-from-spain`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/travel/four-days-in-nice-france | 0.433 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.421 | smittenkitchen.com/travel/debs-new-york/ | 0.418 |
| crawl4ai | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.657 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.636 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.574 |
| crawl4ai-raw | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.657 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.636 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.574 |
| scrapy+md | miss | smittenkitchen.com/2007/02/sour-cream-bran-muffins | 0.349 | smittenkitchen.com/2012/08/mediterranean-baked-fet | 0.326 | smittenkitchen.com/2007/02/sour-cream-bran-muffins | 0.322 |
| crawlee | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.722 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.617 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.607 |
| colly+md | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.722 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.617 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.613 |
| playwright | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.722 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.617 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.613 |


**Q13: What is a notable meal mentioned from the Hostal de la Granota in Costa Brava?**
*(expects URL containing: `a-few-favorites-from-spain`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2010/03/romesco-potatoes/ | 0.453 | smittenkitchen.com/2010/03/spinach-and-chickpeas/ | 0.450 | smittenkitchen.com/2010/03/romesco-potatoes/ | 0.442 |
| crawl4ai | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.594 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.575 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.523 |
| crawl4ai-raw | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.594 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.575 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.523 |
| scrapy+md | miss | smittenkitchen.com/2022/03/castle-breakfast/ | 0.397 | smittenkitchen.com/2017/09/pizza-beans/ | 0.395 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.386 |
| crawlee | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.560 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.522 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.493 |
| colly+md | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.560 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.522 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.510 |
| playwright | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.560 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.522 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.510 |


**Q14: What items are included in the Smitten Kitchen shop?**
*(expects URL containing: `shop`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/books/ | 0.556 | smittenkitchen.com/books/ | 0.544 | smittenkitchen.com/books/ | 0.530 |
| crawl4ai | #1 | smittenkitchen.com/shop/ | 0.612 | smittenkitchen.com/about/ | 0.607 | smittenkitchen.com/recipes/ | 0.602 |
| crawl4ai-raw | #1 | smittenkitchen.com/shop/ | 0.612 | smittenkitchen.com/about/ | 0.607 | smittenkitchen.com/contact/ | 0.588 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.481 | smittenkitchen.com/recipes/ | 0.479 | smittenkitchen.com/privacy-policy/ | 0.429 |
| crawlee | #1 | smittenkitchen.com/shop/ | 0.644 | smittenkitchen.com/./recipes/holiday/food-gifts/?f | 0.606 | smittenkitchen.com/book/ | 0.594 |
| colly+md | #1 | smittenkitchen.com/shop/ | 0.644 | smittenkitchen.com/books/ | 0.595 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.592 |
| playwright | #1 | smittenkitchen.com/shop/ | 0.644 | smittenkitchen.com/book/ | 0.594 | smittenkitchen.com/about/ | 0.587 |


**Q15: Where can I find kitchen supply stores that ship domestically?**
*(expects URL containing: `shop`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/books/ | 0.363 | smittenkitchen.com/subscribe/ | 0.312 | smittenkitchen.com/2017/06/best-hot-fudge-sauce/ | 0.311 |
| crawl4ai | #1 | smittenkitchen.com/shop/ | 0.379 | smittenkitchen.com/shop/ | 0.358 | smittenkitchen.com/reading/cookbook-index/ | 0.344 |
| crawl4ai-raw | #1 | smittenkitchen.com/shop/ | 0.389 | smittenkitchen.com/shop/ | 0.358 | smittenkitchen.com/reading/cookbook-index/ | 0.344 |
| scrapy+md | miss | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.268 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.266 | smittenkitchen.com/2015/02/pecan-sticky-buns-news/ | 0.258 |
| crawlee | #1 | smittenkitchen.com/shop/ | 0.431 | smittenkitchen.com/shop/ | 0.399 | smittenkitchen.com/reading/cookbook-index/ | 0.338 |
| colly+md | #1 | smittenkitchen.com/shop/ | 0.431 | smittenkitchen.com/shop/ | 0.399 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.345 |
| playwright | #1 | smittenkitchen.com/shop/ | 0.431 | smittenkitchen.com/shop/ | 0.399 | smittenkitchen.com/reading/cookbook-index/ | 0.338 |


**Q16: What are some Russian recipes available on Smitten Kitchen?**
*(expects URL containing: `russian`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | smittenkitchen.com/2014/11/smoked-whitefish-dip-wi | 0.559 | smittenkitchen.com/2014/01/warm-lentil-and-potato- | 0.556 | smittenkitchen.com/2006/12/russian-tea-cakes/ | 0.552 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/cuisine/russian/?form | 0.650 | smittenkitchen.com/recipes/ | 0.626 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.605 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/cuisine/russian/?form | 0.650 | smittenkitchen.com/recipes/ | 0.607 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.606 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.535 | smittenkitchen.com/recipes/ | 0.523 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.502 |
| crawlee | #1 | smittenkitchen.com/./recipes/cuisine/russian/?form | 0.660 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.604 | smittenkitchen.com/./recipes/savory-projects/?form | 0.592 |
| colly+md | #1 | smittenkitchen.com/recipes/cuisine/russian/?format | 0.691 | smittenkitchen.com/recipes/ | 0.605 | smittenkitchen.com/recipes/course/dumplings/?forma | 0.591 |
| playwright | #1 | smittenkitchen.com/recipes/cuisine/russian/?format | 0.692 | smittenkitchen.com/recipes/ | 0.606 | smittenkitchen.com/recipes | 0.606 |


**Q17: When was the Russian cuisine page first published?**
*(expects URL containing: `russian`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2006/12/russian-tea-cakes/ | 0.470 | smittenkitchen.com/2014/11/smoked-whitefish-dip-wi | 0.447 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.445 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/cuisine/russian/?form | 0.453 | smittenkitchen.com/./recipes/cuisine/russian/?form | 0.449 | smittenkitchen.com/about/faq/ | 0.432 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/cuisine/russian/?form | 0.452 | smittenkitchen.com/./recipes/cuisine/russian/?form | 0.450 | smittenkitchen.com/about/faq/ | 0.432 |
| scrapy+md | miss | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.443 | smittenkitchen.com/recipes/ | 0.411 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.402 |
| crawlee | #1 | smittenkitchen.com/./recipes/cuisine/russian/?form | 0.489 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.421 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.413 |
| colly+md | #1 | smittenkitchen.com/recipes/cuisine/russian/?format | 0.502 | smittenkitchen.com/2026/02/miso-chicken-and-rice/# | 0.443 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.443 |
| playwright | #1 | smittenkitchen.com/recipes/cuisine/russian/?format | 0.504 | smittenkitchen.com/recipes/cuisine/russian/?format | 0.410 | smittenkitchen.com/ | 0.408 |


**Q18: What are some recipes that are freezer friendly?**
*(expects URL containing: `freezer-friendly`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2025/02/ziti-chickpeas-with-sau | 0.499 | smittenkitchen.com/2023/09/chicken-rice-with-butte | 0.492 | smittenkitchen.com/2012/03/raspberry-coconut-macar | 0.492 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/method/freezer-friend | 0.488 | smittenkitchen.com/./recipes/sweets/ice-cream-sorb | 0.441 | smittenkitchen.com/about/faq/ | 0.439 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/method/freezer-friend | 0.489 | smittenkitchen.com/./recipes/sweets/ice-cream-sorb | 0.441 | smittenkitchen.com/about/faq/ | 0.439 |
| scrapy+md | miss | smittenkitchen.com/2017/09/pizza-beans/ | 0.483 | smittenkitchen.com/2017/09/pizza-beans/ | 0.477 | smittenkitchen.com/2006/11/chocolate-chip-sour-cre | 0.475 |
| crawlee | #3 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.552 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.546 | smittenkitchen.com/./recipes/method/freezer-friend | 0.529 |
| colly+md | #1 | smittenkitchen.com/recipes/method/freezer-friendly | 0.582 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.552 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.546 |
| playwright | #1 | smittenkitchen.com/recipes/method/freezer-friendly | 0.583 | smittenkitchen.com/recipes | 0.466 | smittenkitchen.com/recipes/ | 0.466 |


**Q19: What are some dumpling recipes available on Smitten Kitchen?**
*(expects URL containing: `dumplings`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2013/05/spring-vegetable-potsti | 0.634 | smittenkitchen.com/2007/02/on-obsessiveness-and-ol | 0.620 | smittenkitchen.com/2007/02/on-obsessiveness-and-ol | 0.616 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.625 | smittenkitchen.com/./recipes/cuisine/chinese/?form | 0.599 | smittenkitchen.com/./recipes/method/instant-pot/?f | 0.582 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.625 | smittenkitchen.com/./recipes/cuisine/chinese/?form | 0.599 | smittenkitchen.com/./recipes/method/instant-pot/?f | 0.583 |
| scrapy+md | miss | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.496 | smittenkitchen.com/2007/02/sour-cream-bran-muffins | 0.496 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.496 |
| crawlee | #1 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.638 | smittenkitchen.com/./recipes/cuisine/chinese/?form | 0.583 | smittenkitchen.com/./recipes/method/instant-pot/?f | 0.567 |
| colly+md | #1 | smittenkitchen.com/recipes/course/dumplings/?forma | 0.659 | smittenkitchen.com/recipes/cuisine/chinese/?format | 0.573 | smittenkitchen.com/recipes/ | 0.552 |
| playwright | #1 | smittenkitchen.com/recipes/course/dumplings/?forma | 0.660 | smittenkitchen.com/recipes/cuisine/chinese/?format | 0.574 | smittenkitchen.com/recipes/ | 0.552 |


**Q20: When was the dumpling recipe page first published?**
*(expects URL containing: `dumplings`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2007/02/on-obsessiveness-and-ol | 0.613 | smittenkitchen.com/2013/05/spring-vegetable-potsti | 0.600 | smittenkitchen.com/2007/02/on-obsessiveness-and-ol | 0.599 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.476 | smittenkitchen.com/ | 0.450 | smittenkitchen.com/subscribe/ | 0.450 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.475 | smittenkitchen.com/ | 0.450 | smittenkitchen.com/subscribe/ | 0.450 |
| scrapy+md | miss | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.464 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.464 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.464 |
| crawlee | #1 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.480 | smittenkitchen.com/?random&timestamp=1777919490717 | 0.464 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.455 |
| colly+md | #1 | smittenkitchen.com/recipes/course/dumplings/?forma | 0.477 | smittenkitchen.com/2026/02/miso-chicken-and-rice/# | 0.460 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.460 |
| playwright | #1 | smittenkitchen.com/recipes/course/dumplings/?forma | 0.478 | smittenkitchen.com/events/ | 0.440 | smittenkitchen.com/subscribe/ | 0.436 |


**Q21: What is a recipe featured on the quick recipes page?**
*(expects URL containing: `quick`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #13 | smittenkitchen.com/2020/10/morning-glory-breakfast | 0.476 | smittenkitchen.com/2007/07/pearl-couscous-with-oli | 0.471 | smittenkitchen.com/2012/04/pasta-with-garlicky-bro | 0.470 |
| crawl4ai | #3 | smittenkitchen.com/./recipes/method/instant-pot/?f | 0.505 | smittenkitchen.com/about/faq/ | 0.500 | smittenkitchen.com/./recipes/quick/?format=photo | 0.490 |
| crawl4ai-raw | #3 | smittenkitchen.com/./recipes/method/instant-pot/?f | 0.505 | smittenkitchen.com/about/faq/ | 0.500 | smittenkitchen.com/./recipes/quick/?format=photo | 0.490 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.544 | smittenkitchen.com/2007/02/sour-cream-bran-muffins | 0.482 | smittenkitchen.com/2006/11/chocolate-chip-sour-cre | 0.479 |
| crawlee | miss | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.491 | smittenkitchen.com/./recipes/method/instant-pot/?f | 0.489 | smittenkitchen.com/./recipes/savory-projects/?form | 0.478 |
| colly+md | #7 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.496 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.496 | smittenkitchen.com/2026/04/sidecar/ | 0.491 |
| playwright | #14 | smittenkitchen.com/recipes | 0.488 | smittenkitchen.com/recipes/ | 0.488 | smittenkitchen.com/about/faq/ | 0.477 |


**Q22: How can I view the quick recipes in a list format?**
*(expects URL containing: `quick`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #8 | smittenkitchen.com/2007/07/pearl-couscous-with-oli | 0.454 | smittenkitchen.com/2008/11/chickpea-salad-with-roa | 0.432 | smittenkitchen.com/2025/08/double-chocolate-zucchi | 0.428 |
| crawl4ai | #39 | smittenkitchen.com/about/faq/ | 0.489 | smittenkitchen.com/about/faq/ | 0.474 | smittenkitchen.com/./recipes/method/instant-pot/?f | 0.463 |
| crawl4ai-raw | #36 | smittenkitchen.com/about/faq/ | 0.489 | smittenkitchen.com/about/faq/ | 0.474 | smittenkitchen.com/./recipes/method/instant-pot/?f | 0.463 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.514 | smittenkitchen.com/recipes/ | 0.478 | smittenkitchen.com/2017/09/pizza-beans/ | 0.457 |
| crawlee | #30 | smittenkitchen.com/./recipes/method/instant-pot/?f | 0.476 | smittenkitchen.com/recipes/ | 0.472 | smittenkitchen.com/./recipes/method/freezer-friend | 0.463 |
| colly+md | #6 | smittenkitchen.com/recipes/ | 0.493 | smittenkitchen.com/2025/05/one-pan-ditalini-and-pe | 0.484 | smittenkitchen.com/recipes/ | 0.483 |
| playwright | #7 | smittenkitchen.com/recipes | 0.493 | smittenkitchen.com/recipes/ | 0.493 | smittenkitchen.com/recipes | 0.484 |


**Q23: What is a recipe featured on the picnics page?**
*(expects URL containing: `picnics`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2015/05/pasta-salad-with-roaste | 0.571 | smittenkitchen.com/2015/05/pasta-salad-with-roaste | 0.543 | smittenkitchen.com/2016/09/magic-apple-plum-cobble | 0.524 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/course/picnics/?forma | 0.519 | smittenkitchen.com/./recipes/fruit/pineapple/?form | 0.516 | smittenkitchen.com/about/faq/ | 0.511 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/course/picnics/?forma | 0.519 | smittenkitchen.com/./recipes/fruit/pineapple/?form | 0.516 | smittenkitchen.com/about/faq/ | 0.511 |
| scrapy+md | miss | smittenkitchen.com/2012/08/mediterranean-baked-fet | 0.540 | smittenkitchen.com/2006/11/chocolate-chip-sour-cre | 0.531 | smittenkitchen.com/recipes/ | 0.530 |
| crawlee | #1 | smittenkitchen.com/./recipes/course/picnics/?forma | 0.533 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.528 | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.513 |
| colly+md | #1 | smittenkitchen.com/recipes/course/picnics/?format= | 0.548 | smittenkitchen.com/2026/04/sidecar/ | 0.536 | smittenkitchen.com/2026/04/sidecar/#comments | 0.536 |
| playwright | #1 | smittenkitchen.com/recipes/course/picnics/?format= | 0.551 | smittenkitchen.com/recipes | 0.530 | smittenkitchen.com/recipes/ | 0.530 |


**Q24: How many recipes are listed under the picnics category?**
*(expects URL containing: `picnics`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2015/05/pasta-salad-with-roaste | 0.541 | smittenkitchen.com/2015/05/pasta-salad-with-roaste | 0.526 | smittenkitchen.com/2009/01/warm-butternut-squash-a | 0.500 |
| crawl4ai | #5 | smittenkitchen.com/recipes/ | 0.491 | smittenkitchen.com/recipes/ | 0.489 | smittenkitchen.com/recipes/ | 0.485 |
| crawl4ai-raw | #5 | smittenkitchen.com/recipes/ | 0.495 | smittenkitchen.com/recipes/ | 0.491 | smittenkitchen.com/recipes/ | 0.485 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.585 | smittenkitchen.com/recipes/ | 0.578 | smittenkitchen.com/2012/08/mediterranean-baked-fet | 0.481 |
| crawlee | #3 | smittenkitchen.com/recipes/ | 0.501 | smittenkitchen.com/recipes/ | 0.486 | smittenkitchen.com/./recipes/course/picnics/?forma | 0.486 |
| colly+md | #3 | smittenkitchen.com/recipes/ | 0.554 | smittenkitchen.com/recipes/ | 0.546 | smittenkitchen.com/recipes/course/picnics/?format= | 0.522 |
| playwright | #5 | smittenkitchen.com/recipes | 0.554 | smittenkitchen.com/recipes/ | 0.554 | smittenkitchen.com/recipes/ | 0.546 |


**Q25: What are some recommended places to eat in Paris during a short trip?**
*(expects URL containing: `a-few-trips-to-paris`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.542 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.515 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.505 |
| crawl4ai | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.529 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.523 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.516 |
| crawl4ai-raw | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.529 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.523 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.516 |
| scrapy+md | miss | smittenkitchen.com/2007/02/sour-cream-bran-muffins | 0.310 | smittenkitchen.com/2007/02/sour-cream-bran-muffins | 0.305 | smittenkitchen.com/2008/04/cauliflower-bean-and-fe | 0.282 |
| crawlee | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.542 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.515 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.505 |
| colly+md | miss | smittenkitchen.com/travel/48-hours-in-new-orleans/ | 0.450 | smittenkitchen.com/travel/48-hours-in-new-orleans/ | 0.448 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.431 |
| playwright | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.542 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.515 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.505 |


**Q26: What activities are suggested for acclimating to Paris on the first evening?**
*(expects URL containing: `a-few-trips-to-paris`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.534 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.490 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.481 |
| crawl4ai | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.567 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.515 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.499 |
| crawl4ai-raw | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.567 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.515 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.499 |
| scrapy+md | miss | smittenkitchen.com/2007/02/knotted-and-stacked-dis | 0.257 | smittenkitchen.com/2007/02/knotted-and-stacked-dis | 0.257 | smittenkitchen.com/2007/02/knotted-and-stacked-dis | 0.257 |
| crawlee | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.534 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.492 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.481 |
| colly+md | miss | smittenkitchen.com/travel/48-hours-in-new-orleans/ | 0.406 | smittenkitchen.com/travel/48-hours-in-new-orleans/ | 0.385 | smittenkitchen.com/travel/48-hours-in-new-orleans/ | 0.356 |
| playwright | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.534 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.492 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.481 |


**Q27: What are some pancake recipes available on Smitten Kitchen?**
*(expects URL containing: `pancakes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2020/10/morning-glory-breakfast | 0.586 | smittenkitchen.com/2020/04/layered-yogurt-flatbrea | 0.560 | smittenkitchen.com/books/ | 0.545 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/course/pancakes/?form | 0.624 | smittenkitchen.com/recipes/ | 0.595 | smittenkitchen.com/./recipes/cuisine/austrian/?for | 0.594 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/course/pancakes/?form | 0.624 | smittenkitchen.com/./recipes/cuisine/austrian/?for | 0.594 | smittenkitchen.com/./recipes/vegetable/greens/swis | 0.588 |
| scrapy+md | miss | smittenkitchen.com/2006/11/chocolate-chip-sour-cre | 0.518 | smittenkitchen.com/recipes/ | 0.516 | smittenkitchen.com/2007/02/sour-cream-bran-muffins | 0.515 |
| crawlee | #1 | smittenkitchen.com/./recipes/course/pancakes/?form | 0.629 | smittenkitchen.com/./recipes/course/waffles/?forma | 0.582 | smittenkitchen.com/./recipes/holiday/easter/?forma | 0.580 |
| colly+md | miss | smittenkitchen.com/recipes/ | 0.597 | smittenkitchen.com/recipes/sweets/everyday-cakes/? | 0.587 | smittenkitchen.com/recipes/sweets/everyday-cakes/ | 0.587 |
| playwright | #1 | smittenkitchen.com/recipes/course/pancakes/?format | 0.681 | smittenkitchen.com/recipes/ | 0.599 | smittenkitchen.com/recipes | 0.599 |


**Q28: When was the pancake recipe page first published?**
*(expects URL containing: `pancakes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2007/03/rich-buttermilk-waffles | 0.530 | smittenkitchen.com/2007/03/rich-buttermilk-waffles | 0.516 | smittenkitchen.com/2007/03/rich-buttermilk-waffles | 0.513 |
| crawl4ai | #2 | smittenkitchen.com/about/faq/ | 0.481 | smittenkitchen.com/./recipes/course/pancakes/?form | 0.476 | smittenkitchen.com/about/faq/ | 0.474 |
| crawl4ai-raw | #3 | smittenkitchen.com/about/faq/ | 0.481 | smittenkitchen.com/about/faq/ | 0.474 | smittenkitchen.com/./recipes/course/pancakes/?form | 0.474 |
| scrapy+md | miss | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.514 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.514 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.514 |
| crawlee | #1 | smittenkitchen.com/./recipes/course/pancakes/?form | 0.485 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.475 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.468 |
| colly+md | miss | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.490 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.490 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.488 |
| playwright | #1 | smittenkitchen.com/recipes/course/pancakes/?format | 0.512 | smittenkitchen.com/about/faq/ | 0.448 | smittenkitchen.com/about/faq/ | 0.442 |


**Q29: What are some recipes that include bourbon?**
*(expects URL containing: `bourbon`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2007/10/pumpkin-bread-pudding/ | 0.537 | smittenkitchen.com/2006/11/blondies/ | 0.495 | smittenkitchen.com/2007/10/pumpkin-bread-pudding/ | 0.484 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/ingredient/bourbon/?f | 0.444 | smittenkitchen.com/./recipes/ingredient/bourbon/?f | 0.433 | smittenkitchen.com/ | 0.367 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/ingredient/bourbon/?f | 0.445 | smittenkitchen.com/./recipes/ingredient/bourbon/?f | 0.434 | smittenkitchen.com/ | 0.367 |
| scrapy+md | miss | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.482 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.482 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.482 |
| crawlee | #1 | smittenkitchen.com/./recipes/ingredient/bourbon/?f | 0.483 | smittenkitchen.com/ | 0.431 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.427 |
| colly+md | miss | smittenkitchen.com/2026/04/sidecar/#comments | 0.459 | smittenkitchen.com/2026/04/sidecar/ | 0.459 | smittenkitchen.com/ | 0.430 |
| playwright | #1 | smittenkitchen.com/recipes/ingredient/bourbon/?for | 0.566 | smittenkitchen.com/recipes/sweets/bars-brownies-bl | 0.426 | smittenkitchen.com/recipes/sweets/candy/?format=ph | 0.420 |


**Q30: When was the bourbon recipe page first published?**
*(expects URL containing: `bourbon`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2006/11/blondies/ | 0.481 | smittenkitchen.com/2007/10/pumpkin-bread-pudding/ | 0.460 | smittenkitchen.com/2025/06/slushy-paper-plane/ | 0.457 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/ingredient/bourbon/?f | 0.462 | smittenkitchen.com/./recipes/ingredient/bourbon/?f | 0.409 | smittenkitchen.com/./recipes/course/drinks/?format | 0.394 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/ingredient/bourbon/?f | 0.463 | smittenkitchen.com/./recipes/ingredient/bourbon/?f | 0.409 | smittenkitchen.com/./recipes/course/drinks/?format | 0.395 |
| scrapy+md | miss | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.502 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.502 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.502 |
| crawlee | #2 | smittenkitchen.com/ | 0.478 | smittenkitchen.com/./recipes/ingredient/bourbon/?f | 0.467 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.432 |
| colly+md | miss | smittenkitchen.com/ | 0.475 | smittenkitchen.com/2025/06/slushy-paper-plane/ | 0.467 | smittenkitchen.com/2025/06/slushy-paper-plane/ | 0.461 |
| playwright | #1 | smittenkitchen.com/recipes/ingredient/bourbon/?for | 0.499 | smittenkitchen.com/ | 0.462 | smittenkitchen.com/about/faq/ | 0.389 |


**Q31: What are some seafood recipes available on Smitten Kitchen?**
*(expects URL containing: `seafood`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2014/11/smoked-whitefish-dip-wi | 0.577 | smittenkitchen.com/2014/11/smoked-whitefish-dip-wi | 0.565 | smittenkitchen.com/2014/11/smoked-whitefish-dip-wi | 0.557 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/ingredient/seafood/?f | 0.633 | smittenkitchen.com/recipes/ | 0.618 | smittenkitchen.com/travel/six-days-in-iceland/ | 0.609 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/ingredient/seafood/?f | 0.634 | smittenkitchen.com/travel/six-days-in-iceland/ | 0.609 | smittenkitchen.com/about/ | 0.605 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.509 | smittenkitchen.com/recipes/ | 0.501 | smittenkitchen.com/2021/02/baked-feta-with-tomatoe | 0.499 |
| crawlee | #1 | smittenkitchen.com/./recipes/ingredient/seafood/?f | 0.624 | smittenkitchen.com/about/ | 0.600 | smittenkitchen.com/./recipes/course/appetizers/?fo | 0.587 |
| colly+md | #1 | smittenkitchen.com/recipes/ingredient/seafood/?for | 0.653 | smittenkitchen.com/recipes/best-of-smitten-kitchen | 0.600 | smittenkitchen.com/recipes/ | 0.597 |
| playwright | #1 | smittenkitchen.com/recipes/ingredient/seafood/?for | 0.652 | smittenkitchen.com/about/ | 0.599 | smittenkitchen.com/recipes/ | 0.598 |


**Q32: How can I make garlic wine and butter steamed clams?**
*(expects URL containing: `seafood`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2011/01/chard-and-white-bean-st | 0.496 | smittenkitchen.com/2022/11/green-angel-hair-with-g | 0.495 | smittenkitchen.com/2006/08/moules-frites/ | 0.468 |
| crawl4ai | #2 | smittenkitchen.com/./recipes/cuisine/portuguese/?f | 0.374 | smittenkitchen.com/./recipes/ingredient/seafood/?f | 0.360 | smittenkitchen.com/./recipes/vegetable/artichokes/ | 0.328 |
| crawl4ai-raw | #2 | smittenkitchen.com/./recipes/cuisine/portuguese/?f | 0.374 | smittenkitchen.com/./recipes/ingredient/seafood/?f | 0.361 | smittenkitchen.com/./recipes/vegetable/artichokes/ | 0.327 |
| scrapy+md | miss | smittenkitchen.com/2012/08/charred-pepper-steak-sa | 0.451 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.409 | smittenkitchen.com/2012/08/charred-pepper-steak-sa | 0.393 |
| crawlee | #3 | smittenkitchen.com/./recipes/cuisine/portuguese/?f | 0.410 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.409 | smittenkitchen.com/./recipes/ingredient/seafood/?f | 0.404 |
| colly+md | #3 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.409 | smittenkitchen.com/2026/02/miso-chicken-and-rice/# | 0.409 | smittenkitchen.com/recipes/ingredient/seafood/?for | 0.399 |
| playwright | #1 | smittenkitchen.com/recipes/ingredient/seafood/?for | 0.399 | smittenkitchen.com/recipes/cuisine/portuguese/?for | 0.393 | smittenkitchen.com/?random&timestamp=1777948695303 | 0.364 |


**Q33: What are some Middle Eastern recipes available on Smitten Kitchen?**
*(expects URL containing: `middle-eastern`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2017/07/hummus-heaped-with-toma | 0.599 | smittenkitchen.com/2014/08/smoky-eggplant-dip/ | 0.598 | smittenkitchen.com/2014/08/smoky-eggplant-dip/ | 0.562 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/cuisine/middle-easter | 0.626 | smittenkitchen.com/./recipes/cuisine/israeli/?form | 0.610 | smittenkitchen.com/recipes/ | 0.603 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/cuisine/middle-easter | 0.626 | smittenkitchen.com/./recipes/cuisine/israeli/?form | 0.611 | smittenkitchen.com/./recipes/ingredient/meat/lamb/ | 0.598 |
| scrapy+md | miss | smittenkitchen.com/2021/02/baked-feta-with-tomatoe | 0.533 | smittenkitchen.com/2021/02/baked-feta-with-tomatoe | 0.526 | smittenkitchen.com/recipes/ | 0.517 |
| crawlee | #1 | smittenkitchen.com/./recipes/cuisine/middle-easter | 0.634 | smittenkitchen.com/./recipes/cuisine/israeli/?form | 0.597 | smittenkitchen.com/./recipes/ingredient/meat/lamb/ | 0.591 |
| colly+md | #1 | smittenkitchen.com/recipes/cuisine/middle-eastern/ | 0.654 | smittenkitchen.com/recipes/cuisine/israeli/?format | 0.589 | smittenkitchen.com/recipes/best-of-smitten-kitchen | 0.582 |
| playwright | #1 | smittenkitchen.com/recipes/cuisine/middle-eastern/ | 0.652 | smittenkitchen.com/recipes/holiday/ramadan/?format | 0.596 | smittenkitchen.com/recipes/cuisine/jewish/?format= | 0.592 |


**Q34: What is the first recipe listed in the Middle Eastern category?**
*(expects URL containing: `middle-eastern`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2007/07/pearl-couscous-with-oli | 0.546 | smittenkitchen.com/2007/07/pearl-couscous-with-oli | 0.524 | smittenkitchen.com/2007/07/pearl-couscous-with-oli | 0.520 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/cuisine/middle-easter | 0.481 | smittenkitchen.com/./recipes/cuisine/israeli/?form | 0.469 | smittenkitchen.com/./recipes/ingredient/meat/lamb/ | 0.456 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/cuisine/middle-easter | 0.481 | smittenkitchen.com/./recipes/cuisine/israeli/?form | 0.469 | smittenkitchen.com/./recipes/ingredient/meat/lamb/ | 0.455 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.543 | smittenkitchen.com/2014/04/lamb-meatballs-with-fet | 0.468 | smittenkitchen.com/2014/04/lamb-meatballs-with-fet | 0.465 |
| crawlee | #1 | smittenkitchen.com/./recipes/cuisine/middle-easter | 0.484 | smittenkitchen.com/./recipes/cuisine/north-african | 0.451 | smittenkitchen.com/./recipes/cuisine/israeli/?form | 0.450 |
| colly+md | #1 | smittenkitchen.com/recipes/cuisine/middle-eastern/ | 0.523 | smittenkitchen.com/recipes/ | 0.485 | smittenkitchen.com/recipes/cuisine/israeli/?format | 0.468 |
| playwright | #1 | smittenkitchen.com/recipes/cuisine/middle-eastern/ | 0.523 | smittenkitchen.com/recipes | 0.485 | smittenkitchen.com/recipes/ | 0.485 |


**Q35: What are some recipes that include eggplant?**
*(expects URL containing: `eggplant`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2014/08/smoky-eggplant-dip/ | 0.643 | smittenkitchen.com/2014/08/smoky-eggplant-dip/ | 0.589 | smittenkitchen.com/2019/08/black-pepper-tofu-and-e | 0.581 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/vegetable/eggplant/?f | 0.456 | smittenkitchen.com/videos/ | 0.412 | smittenkitchen.com/./recipes/ingredient/meat/lamb/ | 0.409 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/vegetable/eggplant/?f | 0.458 | smittenkitchen.com/videos/ | 0.412 | smittenkitchen.com/./recipes/ingredient/meat/lamb/ | 0.408 |
| scrapy+md | miss | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.497 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.497 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.497 |
| crawlee | #1 | smittenkitchen.com/./recipes/vegetable/eggplant/?f | 0.480 | smittenkitchen.com/2025/05/one-pan-ditalini-and-pe | 0.464 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.452 |
| colly+md | #1 | smittenkitchen.com/recipes/vegetable/eggplant/?for | 0.562 | smittenkitchen.com/2025/05/one-pan-ditalini-and-pe | 0.452 | smittenkitchen.com/recipes/ingredient/eggs/?format | 0.444 |
| playwright | #4 | smittenkitchen.com/?random&timestamp=1777948695303 | 0.654 | smittenkitchen.com/?random&timestamp=1777948695303 | 0.630 | smittenkitchen.com/?random&timestamp=1777948695303 | 0.572 |


**Q36: What are some recipes included in the Savory Projects category?**
*(expects URL containing: `savory-projects`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2025/05/one-pan-ditalini-and-pe | 0.507 | smittenkitchen.com/2014/01/warm-lentil-and-potato- | 0.506 | smittenkitchen.com/2020/10/morning-glory-breakfast | 0.504 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/savory-projects/?form | 0.576 | smittenkitchen.com/./recipes/sweets/sweet-projects | 0.557 | smittenkitchen.com/./recipes/course/savory-condime | 0.557 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/savory-projects/?form | 0.574 | smittenkitchen.com/./recipes/sweets/sweet-projects | 0.558 | smittenkitchen.com/./recipes/course/savory-condime | 0.557 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.599 | smittenkitchen.com/recipes/ | 0.559 | smittenkitchen.com/2018/10/even-more-perfect-apple | 0.503 |
| crawlee | #1 | smittenkitchen.com/./recipes/savory-projects/?form | 0.561 | smittenkitchen.com/./recipes/course/savory-condime | 0.525 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.525 |
| colly+md | #1 | smittenkitchen.com/recipes/savory-projects/?format | 0.612 | smittenkitchen.com/recipes/ | 0.578 | smittenkitchen.com/recipes/ | 0.552 |
| playwright | #1 | smittenkitchen.com/recipes/savory-projects/?format | 0.614 | smittenkitchen.com/recipes | 0.578 | smittenkitchen.com/recipes/ | 0.578 |


**Q37: What type of recipes are categorized under Savory Projects?**
*(expects URL containing: `savory-projects`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2008/10/twice-baked-shortbread- | 0.481 | smittenkitchen.com/2013/06/pickled-vegetable-sandw | 0.476 | smittenkitchen.com/2010/01/southwestern-pulled-bri | 0.471 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/savory-projects/?form | 0.526 | smittenkitchen.com/./recipes/sweets/sweet-projects | 0.513 | smittenkitchen.com/./recipes/course/savory-condime | 0.502 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/savory-projects/?form | 0.526 | smittenkitchen.com/./recipes/sweets/sweet-projects | 0.513 | smittenkitchen.com/./recipes/course/savory-condime | 0.502 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.589 | smittenkitchen.com/recipes/ | 0.546 | smittenkitchen.com/2007/02/knotted-and-stacked-dis | 0.476 |
| crawlee | #1 | smittenkitchen.com/./recipes/savory-projects/?form | 0.532 | smittenkitchen.com/./recipes/sweets/sweet-projects | 0.493 | smittenkitchen.com/./recipes/course/savory-condime | 0.492 |
| colly+md | #1 | smittenkitchen.com/recipes/savory-projects/?format | 0.587 | smittenkitchen.com/recipes/ | 0.548 | smittenkitchen.com/recipes/ | 0.533 |
| playwright | #1 | smittenkitchen.com/recipes/savory-projects/?format | 0.589 | smittenkitchen.com/recipes/ | 0.547 | smittenkitchen.com/recipes | 0.547 |


**Q38: What are some recipes that include cheese?**
*(expects URL containing: `cheese`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #7 | smittenkitchen.com/2011/03/whole-wheat-goldfish-cr | 0.550 | smittenkitchen.com/2025/02/ziti-chickpeas-with-sau | 0.501 | smittenkitchen.com/2011/03/the-best-baked-spinach/ | 0.496 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/ingredient/cheese/?fo | 0.405 | smittenkitchen.com/./recipes/ingredient/cheese/?fo | 0.377 | smittenkitchen.com/./recipes/vegetable/greens/?for | 0.377 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/ingredient/cheese/?fo | 0.405 | smittenkitchen.com/./recipes/ingredient/cheese/?fo | 0.379 | smittenkitchen.com/./recipes/vegetable/greens/?for | 0.376 |
| scrapy+md | miss | smittenkitchen.com/2017/09/pizza-beans/ | 0.470 | smittenkitchen.com/2012/08/mediterranean-baked-fet | 0.468 | smittenkitchen.com/recipes/ | 0.464 |
| crawlee | #1 | smittenkitchen.com/./recipes/ingredient/cheese/?fo | 0.411 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.403 | smittenkitchen.com/2025/05/one-pan-ditalini-and-pe | 0.395 |
| colly+md | #1 | smittenkitchen.com/recipes/ingredient/cheese/?form | 0.468 | smittenkitchen.com/recipes/ | 0.427 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.409 |
| playwright | #1 | smittenkitchen.com/recipes/ingredient/cheese/?form | 0.468 | smittenkitchen.com/recipes/ | 0.427 | smittenkitchen.com/recipes | 0.427 |


**Q39: What are some recipes that include kale?**
*(expects URL containing: `kale`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #10 | smittenkitchen.com/2013/01/lentil-soup-with-sausag | 0.531 | smittenkitchen.com/2012/07/bacon-corn-hash/ | 0.504 | smittenkitchen.com/2011/03/the-best-baked-spinach/ | 0.499 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/vegetable/greens/kale | 0.492 | smittenkitchen.com/./recipes/vegetable/greens/kale | 0.490 | smittenkitchen.com/recipes/ | 0.456 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/vegetable/greens/kale | 0.490 | smittenkitchen.com/./recipes/vegetable/greens/kale | 0.490 | smittenkitchen.com/recipes/ | 0.466 |
| scrapy+md | miss | smittenkitchen.com/2021/02/baked-feta-with-tomatoe | 0.513 | smittenkitchen.com/2017/09/pizza-beans/ | 0.497 | smittenkitchen.com/2008/04/cauliflower-bean-and-fe | 0.495 |
| crawlee | miss | smittenkitchen.com/recipes/ | 0.492 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.472 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.460 |
| colly+md | #1 | smittenkitchen.com/recipes/vegetable/greens/kale/? | 0.591 | smittenkitchen.com/2025/12/winter-cabbage-salad-wi | 0.475 | smittenkitchen.com/recipes/vegetable/brussels-spro | 0.472 |
| playwright | #1 | smittenkitchen.com/recipes/vegetable/greens/kale/? | 0.595 | smittenkitchen.com/recipes/vegetable/brussels-spro | 0.472 | smittenkitchen.com/recipes/vegetable/greens/swiss- | 0.468 |


**Q40: When was the kale recipe page first published?**
*(expects URL containing: `kale`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | smittenkitchen.com/2011/01/chard-and-white-bean-st | 0.521 | smittenkitchen.com/2025/05/eggs-florentine/ | 0.495 | smittenkitchen.com/2025/05/challah-french-toast/ | 0.495 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/vegetable/greens/kale | 0.570 | smittenkitchen.com/./recipes/vegetable/greens/kale | 0.522 | smittenkitchen.com/./recipes/vegetable/greens/arug | 0.502 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/vegetable/greens/kale | 0.568 | smittenkitchen.com/./recipes/vegetable/greens/kale | 0.521 | smittenkitchen.com/./recipes/vegetable/greens/arug | 0.502 |
| scrapy+md | miss | smittenkitchen.com/2021/02/baked-feta-with-tomatoe | 0.542 | smittenkitchen.com/2017/09/pizza-beans/ | 0.510 | smittenkitchen.com/2017/09/pizza-beans/ | 0.500 |
| crawlee | miss | smittenkitchen.com/recipes/ | 0.505 | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.499 | smittenkitchen.com/about/faq/ | 0.480 |
| colly+md | #1 | smittenkitchen.com/recipes/vegetable/greens/kale/? | 0.578 | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.485 | smittenkitchen.com/about/faq/ | 0.480 |
| playwright | #1 | smittenkitchen.com/recipes/vegetable/greens/kale/? | 0.586 | smittenkitchen.com/about/faq/ | 0.480 | smittenkitchen.com/about/faq/ | 0.463 |


</details>

## stripe-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai-raw | 71% (41/58) | 90% (52/58) | 91% (53/58) | 97% (56/58) | 100% (58/58) | 0.808 | 3564 | 499 |
| crawl4ai | 69% (40/58) | 86% (50/58) | 90% (52/58) | 93% (54/58) | 97% (56/58) | 0.783 | 2651 | 500 |
| crawlee | 67% (39/58) | 86% (50/58) | 91% (53/58) | 97% (56/58) | 98% (57/58) | 0.780 | 30214 | 500 |
| playwright | 67% (39/58) | 84% (49/58) | 91% (53/58) | 97% (56/58) | 98% (57/58) | 0.778 | 30229 | 500 |
| colly+md | 40% (23/58) | 45% (26/58) | 52% (30/58) | 52% (30/58) | 55% (32/58) | 0.435 | 31125 | 499 |
| markcrawl | 19% (11/58) | 26% (15/58) | 34% (20/58) | 41% (24/58) | 43% (25/58) | 0.254 | 1904 | 489 |
| scrapy+md | 14% (8/58) | 22% (13/58) | 29% (17/58) | 31% (18/58) | 36% (21/58) | 0.193 | 14882 | 500 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for stripe-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is the purpose of the Elements object in Stripe.js?**
*(expects URL containing: `create_payment_element`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/accept-a-payment-synchron | 0.689 | docs.stripe.com/payments/bank-transfers/accept-a-p | 0.678 | docs.stripe.com/payments/accept-a-payment?api-inte | 0.672 |
| crawl4ai | miss | docs.stripe.com/payments/elements | 0.683 | docs.stripe.com/payments/elements | 0.659 | docs.stripe.com/payments/elements/link-authenticat | 0.652 |
| crawl4ai-raw | #1 | docs.stripe.com/js/elements_object/create_payment_ | 0.708 | docs.stripe.com/js | 0.703 | docs.stripe.com/js/element/other_element | 0.697 |
| scrapy+md | #28 | docs.stripe.com/js/tokens/create_token?type=cvc_up | 0.718 | docs.stripe.com/js/element/other_element?type=card | 0.717 | docs.stripe.com/js/elements_object/create_element? | 0.717 |
| crawlee | #6 | docs.stripe.com/elements/address-element | 0.700 | docs.stripe.com/payments/mobile/address-element | 0.700 | docs.stripe.com/payments/link/elements-link | 0.699 |
| colly+md | miss | docs.stripe.com/js | 0.702 | docs.stripe.com/js#stripe-create-payment-method | 0.702 | docs.stripe.com/js#stripe-handle-card-action | 0.702 |
| playwright | #10 | docs.stripe.com/payments/mobile/address-element | 0.700 | docs.stripe.com/elements/address-element | 0.700 | docs.stripe.com/payments/link/elements-link | 0.699 |


**Q2: How do you create an Elements instance using Stripe.js?**
*(expects URL containing: `create_payment_element`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/accept-a-payment-synchron | 0.722 | docs.stripe.com/payments/without-card-authenticati | 0.706 | docs.stripe.com/payments/elements | 0.681 |
| crawl4ai | miss | docs.stripe.com/payments/elements | 0.682 | docs.stripe.com/payments/elements | 0.673 | docs.stripe.com/elements/express-checkout-element/ | 0.667 |
| crawl4ai-raw | #2 | docs.stripe.com/js/element/other_element | 0.732 | docs.stripe.com/js/elements_object/create_payment_ | 0.730 | docs.stripe.com/js | 0.730 |
| scrapy+md | #5 | docs.stripe.com/js/setup_intents/confirm_card_setu | 0.728 | docs.stripe.com/js/elements/submit | 0.728 | docs.stripe.com/js/elements_object/update | 0.728 |
| crawlee | #2 | docs.stripe.com/js | 0.738 | docs.stripe.com/js/elements_object/create_payment_ | 0.736 | docs.stripe.com/js/elements_object/create_payment_ | 0.730 |
| colly+md | miss | docs.stripe.com/js | 0.728 | docs.stripe.com/js#stripe-confirm-card-payment | 0.728 | docs.stripe.com/js#stripe-create-payment-method | 0.728 |
| playwright | #4 | docs.stripe.com/js | 0.738 | docs.stripe.com/js/element/other_element | 0.730 | docs.stripe.com/js | 0.730 |


**Q3: What is prebilling in Stripe subscriptions?**
*(expects URL containing: `prebilling`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/pay-with-balance | 0.547 | docs.stripe.com/payments/checkout/build-subscripti | 0.537 | docs.stripe.com/payments/advanced/build-subscripti | 0.536 |
| crawl4ai | #1 | docs.stripe.com/billing/subscriptions/prebilling | 0.707 | docs.stripe.com/billing/subscriptions/prebilling | 0.675 | docs.stripe.com/billing/subscriptions/prebilling | 0.662 |
| crawl4ai-raw | #1 | docs.stripe.com/billing/subscriptions/prebilling | 0.707 | docs.stripe.com/billing/subscriptions/prebilling | 0.675 | docs.stripe.com/billing/subscriptions/prebilling | 0.662 |
| scrapy+md | miss | docs.stripe.com/billing/subscriptions/mixed-interv | 0.599 | docs.stripe.com/llms.txt | 0.596 | docs.stripe.com/billing/subscriptions/billing-mode | 0.583 |
| crawlee | #2 | docs.stripe.com/connect/subscriptions | 0.671 | docs.stripe.com/billing/subscriptions/prebilling | 0.665 | docs.stripe.com/billing/subscriptions/prebilling | 0.660 |
| colly+md | miss | docs.stripe.com/connect/subscriptions | 0.671 | docs.stripe.com/billing/subscriptions/overview | 0.640 | docs.stripe.com/subscriptions | 0.638 |
| playwright | #2 | docs.stripe.com/connect/subscriptions | 0.671 | docs.stripe.com/billing/subscriptions/prebilling | 0.662 | docs.stripe.com/billing/subscriptions/prebilling | 0.659 |


**Q4: What are the limitations of using prebilling?**
*(expects URL containing: `prebilling`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/checkout/billing-cycle | 0.472 | docs.stripe.com/payments/blik/save-during-payment | 0.452 | docs.stripe.com/payments/payment-element/custom-pa | 0.444 |
| crawl4ai | #1 | docs.stripe.com/billing/subscriptions/prebilling | 0.704 | docs.stripe.com/billing/subscriptions/prebilling | 0.656 | docs.stripe.com/billing/subscriptions/prebilling | 0.497 |
| crawl4ai-raw | #1 | docs.stripe.com/billing/subscriptions/prebilling | 0.703 | docs.stripe.com/billing/subscriptions/prebilling | 0.656 | docs.stripe.com/billing/subscriptions/prebilling | 0.497 |
| scrapy+md | miss | docs.stripe.com/billing/subscriptions/billing-mode | 0.499 | docs.stripe.com/billing/subscriptions/billing-mode | 0.467 | docs.stripe.com/llms.txt | 0.463 |
| crawlee | #1 | docs.stripe.com/billing/subscriptions/prebilling | 0.683 | docs.stripe.com/billing/subscriptions/prebilling | 0.640 | docs.stripe.com/billing/subscriptions/prebilling | 0.555 |
| colly+md | miss | docs.stripe.com/changelog | 0.496 | docs.stripe.com/billing/subscriptions/change | 0.492 | docs.stripe.com/changelog | 0.487 |
| playwright | #1 | docs.stripe.com/billing/subscriptions/prebilling | 0.683 | docs.stripe.com/billing/subscriptions/prebilling | 0.640 | docs.stripe.com/billing/subscriptions/prebilling | 0.559 |


**Q5: What are the common use cases for Financial Connections?**
*(expects URL containing: `use-cases`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/ach-direct-debit | 0.449 | docs.stripe.com/payments/ach-direct-debit/accept-a | 0.444 | docs.stripe.com/payments/customer-balance/migratin | 0.433 |
| crawl4ai | #1 | docs.stripe.com/financial-connections/use-cases | 0.742 | docs.stripe.com/financial-connections/other-data-p | 0.679 | docs.stripe.com/financial-connections | 0.661 |
| crawl4ai-raw | #1 | docs.stripe.com/financial-connections/use-cases | 0.742 | docs.stripe.com/financial-connections/other-data-p | 0.679 | docs.stripe.com/financial-connections | 0.661 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.559 | docs.stripe.com/llms.txt | 0.468 | docs.stripe.com/llms.txt | 0.465 |
| crawlee | #1 | docs.stripe.com/financial-connections/use-cases | 0.731 | docs.stripe.com/financial-connections/other-data-p | 0.686 | docs.stripe.com/financial-connections/use-cases | 0.674 |
| colly+md | #16 | docs.stripe.com/financial-connections | 0.626 | docs.stripe.com/financial-connections/connect-payo | 0.604 | docs.stripe.com/financial-connections | 0.558 |
| playwright | #1 | docs.stripe.com/financial-connections/use-cases | 0.731 | docs.stripe.com/financial-connections/other-data-p | 0.686 | docs.stripe.com/financial-connections/use-cases | 0.674 |


**Q6: How can Financial Connections help improve payment reliability for ACH Direct Debit payments?**
*(expects URL containing: `use-cases`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/ach-direct-debit/accept-a | 0.617 | docs.stripe.com/payments/ach-direct-debit | 0.609 | docs.stripe.com/payments/ach-direct-debit/set-up-p | 0.601 |
| crawl4ai | #2 | docs.stripe.com/financial-connections/ach-direct-d | 0.666 | docs.stripe.com/financial-connections/use-cases | 0.665 | docs.stripe.com/payments/ach-direct-debit | 0.626 |
| crawl4ai-raw | #2 | docs.stripe.com/financial-connections/ach-direct-d | 0.666 | docs.stripe.com/financial-connections/use-cases | 0.665 | docs.stripe.com/payments/ach-direct-debit | 0.626 |
| scrapy+md | miss | docs.stripe.com/payments/ach-direct-debit/accept-a | 0.617 | docs.stripe.com/payments/ach-direct-debit/accept-a | 0.586 | docs.stripe.com/payments/ach-direct-debit/accept-a | 0.566 |
| crawlee | #2 | docs.stripe.com/financial-connections/ach-direct-d | 0.686 | docs.stripe.com/financial-connections/use-cases | 0.650 | docs.stripe.com/financial-connections/use-cases | 0.635 |
| colly+md | miss | docs.stripe.com/payments/ach-direct-debit | 0.609 | docs.stripe.com/payments/ach-direct-debit | 0.606 | docs.stripe.com/financial-connections | 0.602 |
| playwright | #2 | docs.stripe.com/financial-connections/ach-direct-d | 0.686 | docs.stripe.com/financial-connections/use-cases | 0.651 | docs.stripe.com/financial-connections/use-cases | 0.635 |


**Q7: How can I create a test invoice in Stripe?**
*(expects URL containing: `invoices`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | docs.stripe.com/payments/checkout/receipts | 0.655 | docs.stripe.com/payments/advanced/receipts | 0.653 | docs.stripe.com/payments/advanced/receipts | 0.606 |
| crawl4ai | #1 | docs.stripe.com/get-started/use-cases/invoices | 0.740 | docs.stripe.com/payments/advanced/receipts | 0.659 | docs.stripe.com/payments/advanced/receipts?payment | 0.659 |
| crawl4ai-raw | #1 | docs.stripe.com/get-started/use-cases/invoices | 0.740 | docs.stripe.com/payments/advanced/receipts | 0.659 | docs.stripe.com/payments/advanced/receipts?payment | 0.659 |
| scrapy+md | #27 | docs.stripe.com/invoicing/integration/testing | 0.713 | docs.stripe.com/invoicing/integration/testing | 0.635 | docs.stripe.com/connect/testing | 0.622 |
| crawlee | #1 | docs.stripe.com/get-started/use-cases/invoices | 0.744 | docs.stripe.com/invoicing | 0.713 | docs.stripe.com/invoicing/no-code-guide | 0.691 |
| colly+md | #1 | docs.stripe.com/get-started/use-cases/invoices | 0.744 | docs.stripe.com/invoicing | 0.713 | docs.stripe.com/invoicing/no-code-guide | 0.691 |
| playwright | #1 | docs.stripe.com/get-started/use-cases/invoices | 0.744 | docs.stripe.com/invoicing | 0.713 | docs.stripe.com/invoicing/no-code-guide | 0.691 |


**Q8: What steps do I need to follow to enable Direct Debit retries for invoices?**
*(expects URL containing: `invoices`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #48 | docs.stripe.com/payments/au-becs-debit | 0.614 | docs.stripe.com/payments/nz-bank-account | 0.612 | docs.stripe.com/payments/bacs-debit/accept-a-payme | 0.601 |
| crawl4ai | #6 | docs.stripe.com/invoicing/automatic-collection | 0.631 | docs.stripe.com/payments/pay-with-balance | 0.565 | docs.stripe.com/payments/nz-bank-account | 0.560 |
| crawl4ai-raw | #6 | docs.stripe.com/invoicing/automatic-collection | 0.631 | docs.stripe.com/payments/pay-with-balance | 0.565 | docs.stripe.com/payments/nz-bank-account | 0.560 |
| scrapy+md | miss | docs.stripe.com/invoicing/automatic-collection | 0.610 | docs.stripe.com/connect/saas/tasks/service-fee | 0.569 | docs.stripe.com/invoicing/automatic-collection | 0.550 |
| crawlee | #4 | docs.stripe.com/invoicing/automatic-collection | 0.610 | docs.stripe.com/payments/pay-with-balance | 0.569 | docs.stripe.com/payments/nz-bank-account | 0.559 |
| colly+md | #3 | docs.stripe.com/invoicing/automatic-collection | 0.595 | docs.stripe.com/payments/pay-with-balance | 0.569 | docs.stripe.com/get-started/use-cases/invoices | 0.552 |
| playwright | #4 | docs.stripe.com/invoicing/automatic-collection | 0.610 | docs.stripe.com/payments/pay-with-balance | 0.569 | docs.stripe.com/payments/nz-bank-account | 0.562 |


**Q9: How do I create a payment link using the Stripe Dashboard?**
*(expects URL containing: `create`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/managed-payments/use-paym | 0.702 | docs.stripe.com/payments/payment-method-configurat | 0.652 | docs.stripe.com/payments/link/checkout-link | 0.643 |
| crawl4ai | #2 | docs.stripe.com/get-started/use-cases/startup | 0.729 | docs.stripe.com/payment-links/create | 0.699 | docs.stripe.com/no-code/get-started | 0.673 |
| crawl4ai-raw | #2 | docs.stripe.com/get-started/use-cases/startup | 0.729 | docs.stripe.com/payment-links/create | 0.699 | docs.stripe.com/no-code/get-started | 0.673 |
| scrapy+md | #15 | docs.stripe.com/payments/managed-payments/use-paym | 0.693 | docs.stripe.com/payments/managed-payments/use-paym | 0.669 | docs.stripe.com/llms.txt | 0.642 |
| crawlee | #1 | docs.stripe.com/payment-links/create | 0.828 | docs.stripe.com/invoicing/dashboard#create-invoice | 0.751 | docs.stripe.com/payment-links/post-payment#send-em | 0.728 |
| colly+md | #1 | docs.stripe.com/payment-links/create#api | 0.828 | docs.stripe.com/payment-links/create | 0.828 | docs.stripe.com/invoicing/dashboard#create-invoice | 0.751 |
| playwright | #1 | docs.stripe.com/payment-links/create | 0.828 | docs.stripe.com/invoicing/dashboard | 0.751 | docs.stripe.com/payment-links/post-payment | 0.728 |


**Q10: What pricing models does Payment Links support?**
*(expects URL containing: `create`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/wallets/link | 0.591 | docs.stripe.com/payments/link/link-payment-methods | 0.588 | docs.stripe.com/payments/currencies/localize-price | 0.564 |
| crawl4ai | #2 | docs.stripe.com/payments/link/link-payment-methods | 0.616 | docs.stripe.com/payment-links/create | 0.603 | docs.stripe.com/payments/link/link-payment-methods | 0.602 |
| crawl4ai-raw | #2 | docs.stripe.com/payments/link/link-payment-methods | 0.616 | docs.stripe.com/payment-links/create | 0.603 | docs.stripe.com/payments/link/link-payment-methods | 0.602 |
| scrapy+md | #5 | docs.stripe.com/llms.txt | 0.589 | docs.stripe.com/payments/managed-payments/use-paym | 0.579 | docs.stripe.com/llms.txt | 0.570 |
| crawlee | #2 | docs.stripe.com/billing/subscriptions/design-an-in | 0.606 | docs.stripe.com/payment-links/create | 0.604 | docs.stripe.com/invoicing | 0.604 |
| colly+md | #1 | docs.stripe.com/payment-links/create | 0.605 | docs.stripe.com/payment-links/create#api | 0.605 | docs.stripe.com/invoicing | 0.604 |
| playwright | #2 | docs.stripe.com/billing/subscriptions/design-an-in | 0.606 | docs.stripe.com/payment-links/create | 0.604 | docs.stripe.com/payment-links | 0.604 |


**Q11: What is the purpose of the Tax ID Element?**
*(expects URL containing: `tax-id-element`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/advanced/tax | 0.528 | docs.stripe.com/payments/advanced/tax | 0.515 | docs.stripe.com/payments/advanced/tax | 0.503 |
| crawl4ai | #1 | docs.stripe.com/elements/tax-id-element | 0.644 | docs.stripe.com/tax/custom | 0.631 | docs.stripe.com/tax/custom | 0.586 |
| crawl4ai-raw | #1 | docs.stripe.com/elements/tax-id-element | 0.644 | docs.stripe.com/js/element/other_element | 0.640 | docs.stripe.com/js/elements_object/create_payment_ | 0.639 |
| scrapy+md | miss | docs.stripe.com/js/elements_object/create_element? | 0.592 | docs.stripe.com/js/element/other_element?type=card | 0.592 | docs.stripe.com/js/custom_checkout/init | 0.592 |
| crawlee | #1 | docs.stripe.com/elements/tax-id-element | 0.705 | docs.stripe.com/js/elements_object/create_payment_ | 0.633 | docs.stripe.com/js | 0.633 |
| colly+md | miss | docs.stripe.com/tax/custom | 0.620 | docs.stripe.com/js#stripe-create-payment-method | 0.592 | docs.stripe.com/js#stripe-handle-card-action | 0.592 |
| playwright | #1 | docs.stripe.com/elements/tax-id-element | 0.705 | docs.stripe.com/js | 0.637 | docs.stripe.com/js | 0.626 |


**Q12: In which countries does the Tax ID Element support tax ID collection?**
*(expects URL containing: `tax-id-element`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/advanced/tax | 0.559 | docs.stripe.com/payments/advanced/tax | 0.550 | docs.stripe.com/payments/advanced/tax | 0.539 |
| crawl4ai | #1 | docs.stripe.com/elements/tax-id-element | 0.681 | docs.stripe.com/tax/custom | 0.655 | docs.stripe.com/payments/advanced/tax | 0.626 |
| crawl4ai-raw | #1 | docs.stripe.com/elements/tax-id-element | 0.681 | docs.stripe.com/tax/custom | 0.655 | docs.stripe.com/payments/advanced/tax | 0.626 |
| scrapy+md | miss | docs.stripe.com/tax/checkout/tax-ids | 0.558 | docs.stripe.com/tax/checkout/tax-ids | 0.545 | docs.stripe.com/tax/checkout/tax-ids | 0.539 |
| crawlee | #1 | docs.stripe.com/elements/tax-id-element | 0.673 | docs.stripe.com/elements/tax-id-element | 0.607 | docs.stripe.com/elements/tax-id-element | 0.600 |
| colly+md | miss | docs.stripe.com/tax/custom | 0.575 | docs.stripe.com/tax/custom | 0.567 | docs.stripe.com/tax/custom | 0.562 |
| playwright | #1 | docs.stripe.com/elements/tax-id-element | 0.673 | docs.stripe.com/elements/tax-id-element | 0.607 | docs.stripe.com/payments/advanced/tax | 0.604 |


**Q13: How can I collect a customer email address for Link authentication?**
*(expects URL containing: `save-and-reuse`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #6 | docs.stripe.com/payments/link/add-link-elements-in | 0.637 | docs.stripe.com/payments/link/add-link-elements-in | 0.631 | docs.stripe.com/payments/link/link-authentication- | 0.616 |
| crawl4ai | #3 | docs.stripe.com/payments/link/add-link-elements-in | 0.624 | docs.stripe.com/payments/link/add-link-elements-in | 0.581 | docs.stripe.com/payments/link/save-and-reuse | 0.581 |
| crawl4ai-raw | #3 | docs.stripe.com/payments/link/add-link-elements-in | 0.624 | docs.stripe.com/payments/link/add-link-elements-in | 0.581 | docs.stripe.com/payments/link/save-and-reuse | 0.581 |
| scrapy+md | #3 | docs.stripe.com/payments/link/add-link-elements-in | 0.636 | docs.stripe.com/payments/link/add-link-elements-in | 0.631 | docs.stripe.com/payments/link/save-and-reuse | 0.595 |
| crawlee | #2 | docs.stripe.com/payments/link/add-link-elements-in | 0.631 | docs.stripe.com/payments/link/save-and-reuse | 0.607 | docs.stripe.com/payments/link/save-and-reuse | 0.554 |
| colly+md | miss | docs.stripe.com/payments/link/add-link-elements-in | 0.631 | docs.stripe.com/payments/link/add-link-elements-in | 0.552 | docs.stripe.com/payments/link/add-link-elements-in | 0.538 |
| playwright | #2 | docs.stripe.com/payments/link/add-link-elements-in | 0.631 | docs.stripe.com/payments/link/save-and-reuse | 0.607 | docs.stripe.com/payments/link/save-and-reuse | 0.554 |


**Q14: What is a SetupIntent in the context of setting up future payments with Link?**
*(expects URL containing: `save-and-reuse`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | docs.stripe.com/payments/setup-intents | 0.659 | docs.stripe.com/payments/payment-methods/payment-m | 0.637 | docs.stripe.com/payments/paymentintents/lifecycle | 0.615 |
| crawl4ai | #5 | docs.stripe.com/payments/setup-intents | 0.634 | docs.stripe.com/payments/payment-methods/payment-m | 0.631 | docs.stripe.com/payments/setup-intents | 0.627 |
| crawl4ai-raw | #8 | docs.stripe.com/payments/setup-intents | 0.634 | docs.stripe.com/payments/payment-methods/payment-m | 0.631 | docs.stripe.com/payments/setup-intents | 0.627 |
| scrapy+md | #2 | docs.stripe.com/payments/setup-intents | 0.650 | docs.stripe.com/payments/link/save-and-reuse | 0.626 | docs.stripe.com/api/setup_intents/retrieve | 0.615 |
| crawlee | #10 | docs.stripe.com/api/setup_intents/object | 0.708 | docs.stripe.com/api/setup_intents/create | 0.708 | docs.stripe.com/api/setup_intents/object | 0.688 |
| colly+md | #16 | docs.stripe.com/api/setup/intents | 0.708 | docs.stripe.com/api/setup/intents/object#setup/int | 0.688 | docs.stripe.com/api/setup/intents | 0.673 |
| playwright | #10 | docs.stripe.com/api/setup_intents/create | 0.708 | docs.stripe.com/api/setup_intents/object | 0.708 | docs.stripe.com/api/setup_intents/object | 0.688 |


**Q15: How can I fund my storage balance with an external bank account?**
*(expects URL containing: `fund-balance`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/balances | 0.465 | docs.stripe.com/payments/customer-balance/funding- | 0.437 | docs.stripe.com/payments/balances | 0.431 |
| crawl4ai | #1 | docs.stripe.com/global-payouts/fund-balance | 0.619 | docs.stripe.com/global-payouts/fund-balance | 0.582 | docs.stripe.com/global-payouts/fund-balance | 0.579 |
| crawl4ai-raw | #1 | docs.stripe.com/global-payouts/fund-balance | 0.619 | docs.stripe.com/global-payouts/fund-balance | 0.582 | docs.stripe.com/global-payouts/fund-balance | 0.579 |
| scrapy+md | miss | docs.stripe.com/api/external_accounts?api-version= | 0.503 | docs.stripe.com/payments/customer-balance/funding- | 0.492 | docs.stripe.com/api/external_account_bank_accounts | 0.486 |
| crawlee | #1 | docs.stripe.com/global-payouts/fund-balance | 0.652 | docs.stripe.com/global-payouts/fund-balance | 0.610 | docs.stripe.com/global-payouts/fund-balance | 0.576 |
| colly+md | miss | docs.stripe.com/treasury | 0.561 | docs.stripe.com/get-started/account/add-funds | 0.489 | docs.stripe.com/issuing/funding/balance | 0.477 |
| playwright | #1 | docs.stripe.com/global-payouts/fund-balance | 0.652 | docs.stripe.com/global-payouts/fund-balance | 0.610 | docs.stripe.com/global-payouts/fund-balance | 0.576 |


**Q16: What are the funding limits when pulling funds from an external bank account?**
*(expects URL containing: `fund-balance`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/payto | 0.455 | docs.stripe.com/payments/bank-transfers | 0.454 | docs.stripe.com/payments/payto | 0.453 |
| crawl4ai | #1 | docs.stripe.com/global-payouts/fund-balance | 0.600 | docs.stripe.com/treasury | 0.546 | docs.stripe.com/global-payouts/fund-balance | 0.503 |
| crawl4ai-raw | #1 | docs.stripe.com/global-payouts/fund-balance | 0.600 | docs.stripe.com/treasury | 0.546 | docs.stripe.com/global-payouts/fund-balance | 0.503 |
| scrapy+md | miss | docs.stripe.com/api/external_accounts?api-version= | 0.473 | docs.stripe.com/api/external_accounts?api-version= | 0.459 | docs.stripe.com/api/external_account_bank_accounts | 0.459 |
| crawlee | #1 | docs.stripe.com/global-payouts/fund-balance | 0.598 | docs.stripe.com/treasury | 0.565 | docs.stripe.com/global-payouts/fund-balance | 0.496 |
| colly+md | miss | docs.stripe.com/treasury | 0.565 | docs.stripe.com/issuing/funding/balance | 0.483 | docs.stripe.com/treasury | 0.476 |
| playwright | #1 | docs.stripe.com/global-payouts/fund-balance | 0.598 | docs.stripe.com/treasury | 0.565 | docs.stripe.com/global-payouts/fund-balance | 0.496 |


**Q17: What types of companies can you incorporate using Stripe Atlas?**
*(expects URL containing: `company-types`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/alma | 0.501 | docs.stripe.com/payments | 0.465 | docs.stripe.com/payments/kriya | 0.449 |
| crawl4ai | #2 | docs.stripe.com/atlas/signup | 0.738 | docs.stripe.com/atlas/company-types | 0.727 | docs.stripe.com/atlas | 0.710 |
| crawl4ai-raw | #2 | docs.stripe.com/atlas/signup | 0.738 | docs.stripe.com/atlas/company-types | 0.727 | docs.stripe.com/atlas | 0.710 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.571 | docs.stripe.com/payments | 0.513 | docs.stripe.com/llms.txt | 0.482 |
| crawlee | #2 | docs.stripe.com/atlas/signup | 0.736 | docs.stripe.com/atlas/company-types | 0.705 | docs.stripe.com/llms.txt | 0.701 |
| colly+md | miss | docs.stripe.com/atlas | 0.690 | docs.stripe.com/atlas | 0.683 | docs.stripe.com/atlas/payments-business-bank | 0.658 |
| playwright | #2 | docs.stripe.com/atlas/signup | 0.736 | docs.stripe.com/atlas/company-types | 0.705 | docs.stripe.com/llms.txt | 0.701 |


**Q18: What are the tax implications of incorporating near the end of a calendar year?**
*(expects URL containing: `company-types`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/managed-payments/tax-comp | 0.338 | docs.stripe.com/payments/managed-payments/eligibil | 0.291 | docs.stripe.com/payments/managed-payments/tax-comp | 0.272 |
| crawl4ai | #1 | docs.stripe.com/atlas/company-types | 0.698 | docs.stripe.com/atlas/business-taxes | 0.527 | docs.stripe.com/atlas/business-taxes | 0.512 |
| crawl4ai-raw | #1 | docs.stripe.com/atlas/company-types | 0.698 | docs.stripe.com/atlas/business-taxes | 0.527 | docs.stripe.com/atlas/business-taxes | 0.512 |
| scrapy+md | miss | docs.stripe.com/tax/reports | 0.334 | docs.stripe.com/revenue-recognition/methodology/su | 0.329 | docs.stripe.com/invoicing/taxes?dashboard-or-api=d | 0.322 |
| crawlee | #1 | docs.stripe.com/atlas/company-types | 0.711 | docs.stripe.com/atlas/company-types | 0.605 | docs.stripe.com/atlas/business-taxes | 0.562 |
| colly+md | miss | docs.stripe.com/atlas/83b-elections-non-us-founder | 0.468 | docs.stripe.com/atlas/accept-payments | 0.435 | docs.stripe.com/atlas/indian-founder-guide | 0.413 |
| playwright | #1 | docs.stripe.com/atlas/company-types | 0.717 | docs.stripe.com/atlas/business-taxes | 0.562 | docs.stripe.com/atlas/company-types | 0.560 |


**Q19: What is a dispute in the context of Stripe?**
*(expects URL containing: `disputes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #16 | docs.stripe.com/payments/affirm | 0.664 | docs.stripe.com/payments/zip | 0.664 | docs.stripe.com/payments/cash-app-pay | 0.650 |
| crawl4ai | #1 | docs.stripe.com/disputes | 0.743 | docs.stripe.com/disputes/responding | 0.721 | docs.stripe.com/disputes | 0.684 |
| crawl4ai-raw | #1 | docs.stripe.com/disputes | 0.743 | docs.stripe.com/disputes/responding | 0.721 | docs.stripe.com/disputes | 0.684 |
| scrapy+md | #1 | docs.stripe.com/connect/saas/tasks/refunds-dispute | 0.667 | docs.stripe.com/disputes/categories | 0.642 | docs.stripe.com/disputes/set-up-smart-disputes | 0.639 |
| crawlee | #1 | docs.stripe.com/disputes | 0.863 | docs.stripe.com/disputes/how-disputes-work | 0.840 | docs.stripe.com/disputes/responding#decide | 0.777 |
| colly+md | #1 | docs.stripe.com/disputes | 0.863 | docs.stripe.com/disputes/how-disputes-work | 0.840 | docs.stripe.com/disputes/responding | 0.777 |
| playwright | #1 | docs.stripe.com/disputes | 0.863 | docs.stripe.com/disputes/responding | 0.777 | docs.stripe.com/disputes/best-practices | 0.724 |


**Q20: How does Stripe guide users through the dispute response process?**
*(expects URL containing: `disputes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #7 | docs.stripe.com/payments/affirm | 0.685 | docs.stripe.com/payments/zip | 0.671 | docs.stripe.com/payments/revolut-pay | 0.662 |
| crawl4ai | #1 | docs.stripe.com/disputes | 0.780 | docs.stripe.com/disputes | 0.751 | docs.stripe.com/disputes/responding | 0.748 |
| crawl4ai-raw | #1 | docs.stripe.com/disputes | 0.780 | docs.stripe.com/disputes | 0.751 | docs.stripe.com/disputes/responding | 0.748 |
| scrapy+md | #1 | docs.stripe.com/connect/saas/tasks/refunds-dispute | 0.686 | docs.stripe.com/disputes/smart-disputes/auto-respo | 0.686 | docs.stripe.com/disputes/set-up-smart-disputes | 0.670 |
| crawlee | #1 | docs.stripe.com/disputes/responding#decide | 0.809 | docs.stripe.com/disputes/how-disputes-work | 0.753 | docs.stripe.com/disputes/responding#decide | 0.745 |
| colly+md | #1 | docs.stripe.com/disputes/responding | 0.809 | docs.stripe.com/disputes/responding#decide | 0.809 | docs.stripe.com/disputes | 0.779 |
| playwright | #1 | docs.stripe.com/disputes/responding | 0.809 | docs.stripe.com/disputes/responding | 0.745 | docs.stripe.com/disputes/responding | 0.738 |


**Q21: What financing types does Stripe Capital offer?**
*(expects URL containing: `overview`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.stripe.com/payments/affirm | 0.563 | docs.stripe.com/payments/payment-methods/overview | 0.556 | docs.stripe.com/payments | 0.519 |
| crawl4ai | #3 | docs.stripe.com/capital/how-stripe-capital-works | 0.720 | docs.stripe.com/capital/how-stripe-capital-works | 0.717 | docs.stripe.com/capital/overview | 0.714 |
| crawl4ai-raw | #3 | docs.stripe.com/capital/how-stripe-capital-works | 0.720 | docs.stripe.com/capital/how-stripe-capital-works | 0.717 | docs.stripe.com/capital/overview | 0.714 |
| scrapy+md | #23 | docs.stripe.com/llms.txt | 0.615 | docs.stripe.com/llms.txt | 0.611 | docs.stripe.com/disputes/prevention/advanced-fraud | 0.545 |
| crawlee | #3 | docs.stripe.com/capital/how-stripe-capital-works | 0.734 | docs.stripe.com/capital/how-stripe-capital-works | 0.717 | docs.stripe.com/capital/overview | 0.716 |
| colly+md | #4 | docs.stripe.com/capital/how-stripe-capital-works | 0.734 | docs.stripe.com/capital/how-stripe-capital-works | 0.722 | docs.stripe.com/capital/how-capital-for-platforms- | 0.715 |
| playwright | #3 | docs.stripe.com/capital/how-stripe-capital-works | 0.734 | docs.stripe.com/capital/how-stripe-capital-works | 0.717 | docs.stripe.com/capital/overview | 0.716 |


**Q22: How can I access my Capital financing offers?**
*(expects URL containing: `overview`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #6 | docs.stripe.com/payments/affirm | 0.413 | docs.stripe.com/payments/afterpay-clearpay | 0.384 | docs.stripe.com/payments/customer-balance/funding- | 0.383 |
| crawl4ai | #1 | docs.stripe.com/capital/overview | 0.639 | docs.stripe.com/capital/how-capital-for-platforms- | 0.627 | docs.stripe.com/capital/how-stripe-capital-works | 0.617 |
| crawl4ai-raw | #1 | docs.stripe.com/capital/overview | 0.639 | docs.stripe.com/capital/how-capital-for-platforms- | 0.627 | docs.stripe.com/capital/how-stripe-capital-works | 0.617 |
| scrapy+md | #47 | docs.stripe.com/llms.txt | 0.499 | docs.stripe.com/llms.txt | 0.486 | docs.stripe.com/payments/customer-balance/funding- | 0.382 |
| crawlee | #1 | docs.stripe.com/capital/overview | 0.627 | docs.stripe.com/capital/how-capital-for-platforms- | 0.613 | docs.stripe.com/capital/how-stripe-capital-works | 0.608 |
| colly+md | #1 | docs.stripe.com/capital/overview | 0.632 | docs.stripe.com/capital/overview#capital-for-platf | 0.632 | docs.stripe.com/capital/how-stripe-capital-works | 0.608 |
| playwright | #1 | docs.stripe.com/capital/overview | 0.632 | docs.stripe.com/capital/how-capital-for-platforms- | 0.613 | docs.stripe.com/capital/how-stripe-capital-works | 0.608 |


**Q23: What are voucher payment methods used for?**
*(expects URL containing: `vouchers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/vouchers | 0.646 | docs.stripe.com/payments/vouchers | 0.559 | docs.stripe.com/payments/payment-methods/overview | 0.528 |
| crawl4ai | #1 | docs.stripe.com/payments/vouchers | 0.669 | docs.stripe.com/payments/vouchers | 0.582 | docs.stripe.com/payments/multibanco | 0.510 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/vouchers | 0.669 | docs.stripe.com/payments/vouchers | 0.583 | docs.stripe.com/payments/multibanco | 0.511 |
| scrapy+md | miss | docs.stripe.com/payments/oxxo/accept-a-payment | 0.452 | docs.stripe.com/invoicing/integration/testing | 0.429 | docs.stripe.com/payments/a-b-testing | 0.424 |
| crawlee | #1 | docs.stripe.com/payments/vouchers | 0.659 | docs.stripe.com/payments/vouchers | 0.572 | docs.stripe.com/payments/vouchers | 0.571 |
| colly+md | miss | docs.stripe.com/payments/multibanco | 0.516 | docs.stripe.com/payments/multibanco | 0.509 | docs.stripe.com/payments/payment-methods/overview | 0.462 |
| playwright | #1 | docs.stripe.com/payments/vouchers | 0.659 | docs.stripe.com/payments/vouchers | 0.572 | docs.stripe.com/payments/vouchers | 0.571 |


**Q24: What happens when a customer chooses a voucher method for payment?**
*(expects URL containing: `vouchers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/vouchers | 0.654 | docs.stripe.com/payments/vouchers | 0.559 | docs.stripe.com/payments/oxxo/accept-a-payment | 0.526 |
| crawl4ai | #1 | docs.stripe.com/payments/vouchers | 0.626 | docs.stripe.com/payments/vouchers | 0.588 | docs.stripe.com/payments/multibanco | 0.515 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/vouchers | 0.626 | docs.stripe.com/payments/vouchers | 0.588 | docs.stripe.com/payments/multibanco | 0.515 |
| scrapy+md | miss | docs.stripe.com/payments/oxxo/accept-a-payment | 0.529 | docs.stripe.com/billing/subscriptions/coupons | 0.440 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.439 |
| crawlee | #1 | docs.stripe.com/payments/vouchers | 0.625 | docs.stripe.com/payments/vouchers | 0.578 | docs.stripe.com/payments/vouchers | 0.558 |
| colly+md | miss | docs.stripe.com/payments/multibanco | 0.521 | docs.stripe.com/payments/accept-a-payment?payment- | 0.486 | docs.stripe.com/payments/accept-a-payment?payment- | 0.486 |
| playwright | #1 | docs.stripe.com/payments/vouchers | 0.625 | docs.stripe.com/payments/vouchers | 0.578 | docs.stripe.com/payments/vouchers | 0.558 |


**Q25: What is Pix and how does it work?**
*(expects URL containing: `pix`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/pix | 0.566 | docs.stripe.com/payments/link/pix | 0.566 | docs.stripe.com/payments/pix | 0.559 |
| crawl4ai | #1 | docs.stripe.com/payments/pix | 0.583 | docs.stripe.com/payments/pix | 0.570 | docs.stripe.com/payments/pix | 0.518 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/pix | 0.582 | docs.stripe.com/payments/pix | 0.570 | docs.stripe.com/payments/pix | 0.518 |
| scrapy+md | miss | docs.stripe.com/js/tokens/create_token?type=pii | 0.430 | docs.stripe.com/js/element/other_element?type=card | 0.430 | docs.stripe.com/js/appendix/supported_locales | 0.430 |
| crawlee | #1 | docs.stripe.com/payments/pix | 0.578 | docs.stripe.com/payments/pix | 0.560 | docs.stripe.com/payments/pix | 0.513 |
| colly+md | #1 | docs.stripe.com/payments/pix | 0.579 | docs.stripe.com/payments/pix | 0.540 | docs.stripe.com/payments/pix | 0.500 |
| playwright | #1 | docs.stripe.com/payments/pix | 0.578 | docs.stripe.com/payments/pix | 0.560 | docs.stripe.com/payments/pix | 0.506 |


**Q26: What are the transaction limits for Pix payments?**
*(expects URL containing: `pix`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/pix | 0.653 | docs.stripe.com/payments/pix | 0.567 | docs.stripe.com/payments/link/pix | 0.560 |
| crawl4ai | #1 | docs.stripe.com/payments/pix | 0.665 | docs.stripe.com/payments/pix | 0.613 | docs.stripe.com/payments/pix | 0.606 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/pix | 0.665 | docs.stripe.com/payments/pix | 0.613 | docs.stripe.com/payments/pix | 0.606 |
| scrapy+md | miss | docs.stripe.com/payments/upi | 0.512 | docs.stripe.com/payments/place-a-hold-on-a-payment | 0.436 | docs.stripe.com/js/elements/submit | 0.435 |
| crawlee | #1 | docs.stripe.com/payments/pix | 0.651 | docs.stripe.com/payments/pix | 0.650 | docs.stripe.com/payments/pix | 0.609 |
| colly+md | #1 | docs.stripe.com/payments/pix | 0.651 | docs.stripe.com/payments/pix | 0.650 | docs.stripe.com/payments/pix | 0.598 |
| playwright | #1 | docs.stripe.com/payments/pix | 0.651 | docs.stripe.com/payments/pix | 0.650 | docs.stripe.com/payments/pix | 0.603 |


**Q27: How can I securely accept payments online with Stripe?**
*(expects URL containing: `accept-a-payment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.stripe.com/payments/payment-intents/three-d-s | 0.627 | docs.stripe.com/payments/accept-a-payment-synchron | 0.605 | docs.stripe.com/payments/save-and-reuse?platform=w | 0.603 |
| crawl4ai | #2 | docs.stripe.com/secure-remote-commerce | 0.639 | docs.stripe.com/payments/accept-a-payment | 0.635 | docs.stripe.com/payments/accept-a-payment?platform | 0.635 |
| crawl4ai-raw | #2 | docs.stripe.com/secure-remote-commerce | 0.639 | docs.stripe.com/payments/accept-a-payment?platform | 0.635 | docs.stripe.com/payments/accept-a-payment?payment- | 0.635 |
| scrapy+md | #3 | docs.stripe.com/get-started/data-migrations/pan-im | 0.641 | docs.stripe.com/payments/3d-secure/authentication- | 0.635 | docs.stripe.com/payments/accept-a-payment?payment- | 0.618 |
| crawlee | #4 | docs.stripe.com/security | 0.737 | docs.stripe.com/payments/3d-secure | 0.711 | docs.stripe.com/payments/online-payments | 0.706 |
| colly+md | #5 | docs.stripe.com/security | 0.737 | docs.stripe.com/payments/3d-secure | 0.711 | docs.stripe.com/payments/online-payments#compare-f | 0.706 |
| playwright | #4 | docs.stripe.com/security | 0.737 | docs.stripe.com/payments/3d-secure | 0.711 | docs.stripe.com/payments/online-payments | 0.706 |


**Q28: What should I do if a payment fails or is canceled during the Checkout process?**
*(expects URL containing: `accept-a-payment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/accept-a-payment?payment- | 0.602 | docs.stripe.com/payments/existing-customers | 0.584 | docs.stripe.com/payments/accept-a-payment | 0.580 |
| crawl4ai | #1 | docs.stripe.com/payments/accept-a-payment?payment- | 0.596 | docs.stripe.com/refunds | 0.593 | docs.stripe.com/payments/accept-a-payment?payment- | 0.581 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/accept-a-payment?payment- | 0.596 | docs.stripe.com/refunds | 0.593 | docs.stripe.com/payments/accept-a-payment?payment- | 0.581 |
| scrapy+md | #3 | docs.stripe.com/refunds?dashboard-or-api=dashboard | 0.578 | docs.stripe.com/refunds?dashboard-or-api=api | 0.578 | docs.stripe.com/payments/accept-a-payment?platform | 0.576 |
| crawlee | #1 | docs.stripe.com/payments/accept-a-payment?payment- | 0.602 | docs.stripe.com/refunds | 0.584 | docs.stripe.com/payments/accept-a-payment?payment- | 0.578 |
| colly+md | #1 | docs.stripe.com/payments/accept-a-payment?payment- | 0.602 | docs.stripe.com/refunds#cancel-payment | 0.598 | docs.stripe.com/refunds | 0.598 |
| playwright | #1 | docs.stripe.com/payments/accept-a-payment?payment- | 0.602 | docs.stripe.com/refunds | 0.584 | docs.stripe.com/payments/accept-a-payment?platform | 0.578 |


**Q29: What are the options for processing payments with third-party payment processors using Stripe Billing?**
*(expects URL containing: `third-party-payment-processing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/payment-intents/three-d-s | 0.586 | docs.stripe.com/payments/advanced/collect-addition | 0.578 | docs.stripe.com/payments/klarna/migrate | 0.575 |
| crawl4ai | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.674 | docs.stripe.com/billing/subscriptions/third-party- | 0.629 | docs.stripe.com/payments/payment-methods/integrati | 0.610 |
| crawl4ai-raw | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.674 | docs.stripe.com/billing/subscriptions/third-party- | 0.629 | docs.stripe.com/payments/payment-methods/integrati | 0.610 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.592 | docs.stripe.com/get-started/data-migrations/pan-im | 0.587 | docs.stripe.com/llms.txt | 0.574 |
| crawlee | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.723 | docs.stripe.com/payments/payment-methods/integrati | 0.715 | docs.stripe.com/billing/subscriptions/third-party- | 0.684 |
| colly+md | miss | docs.stripe.com/payments/payment-methods/integrati | 0.715 | docs.stripe.com/payments/payment-methods/integrati | 0.715 | docs.stripe.com/payments/payment-methods/integrati | 0.715 |
| playwright | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.723 | docs.stripe.com/payments/payment-methods/integrati | 0.715 | docs.stripe.com/billing/subscriptions/third-party- | 0.684 |


**Q30: What are the limitations when integrating with a third-party payment processor?**
*(expects URL containing: `third-party-payment-processing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/payment-methods/custom-pa | 0.576 | docs.stripe.com/payments/more-payment-scenarios | 0.523 | docs.stripe.com/payments/forwarding-third-party-pr | 0.523 |
| crawl4ai | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.631 | docs.stripe.com/payments/payment-methods/custom-pa | 0.578 | docs.stripe.com/payments/more-payment-scenarios | 0.573 |
| crawl4ai-raw | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.631 | docs.stripe.com/payments/payment-methods/custom-pa | 0.578 | docs.stripe.com/payments/more-payment-scenarios | 0.573 |
| scrapy+md | miss | docs.stripe.com/terminal/network-requirements | 0.519 | docs.stripe.com/llms.txt | 0.516 | docs.stripe.com/disputes/prevention/card-testing | 0.516 |
| crawlee | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.666 | docs.stripe.com/billing/subscriptions/third-party- | 0.630 | docs.stripe.com/payments/payment-methods/custom-pa | 0.576 |
| colly+md | miss | docs.stripe.com/payments/payment-methods/payment-m | 0.546 | docs.stripe.com/payments/payment-methods/payment-m | 0.546 | docs.stripe.com/payments/payment-methods/payment-m | 0.546 |
| playwright | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.666 | docs.stripe.com/billing/subscriptions/third-party- | 0.630 | docs.stripe.com/payments/payment-methods/custom-pa | 0.576 |


**Q31: What features does the Stripe extension for Visual Studio Code provide?**
*(expects URL containing: `stripe-vscode`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/checkout/how-checkout-wor | 0.502 | docs.stripe.com/payments/elements | 0.492 | docs.stripe.com/payments/payment-methods/overview | 0.489 |
| crawl4ai | #1 | docs.stripe.com/stripe-vscode | 0.756 | docs.stripe.com/stripe-vscode | 0.716 | docs.stripe.com/stripe-vscode | 0.669 |
| crawl4ai-raw | #1 | docs.stripe.com/stripe-vscode | 0.756 | docs.stripe.com/stripe-vscode | 0.716 | docs.stripe.com/stripe-vscode | 0.669 |
| scrapy+md | miss | docs.stripe.com/stripe-apps/ui-extension-developer | 0.596 | docs.stripe.com/building-with-ai | 0.570 | docs.stripe.com/stripe-apps/how-ui-extensions-work | 0.565 |
| crawlee | #1 | docs.stripe.com/stripe-vscode | 0.804 | docs.stripe.com/stripe-vscode | 0.736 | docs.stripe.com/stripe-vscode | 0.703 |
| colly+md | #1 | docs.stripe.com/stripe-vscode | 0.804 | docs.stripe.com/stripe-vscode | 0.708 | docs.stripe.com/stripe-vscode | 0.622 |
| playwright | #1 | docs.stripe.com/stripe-vscode | 0.804 | docs.stripe.com/stripe-vscode | 0.736 | docs.stripe.com/stripe-vscode | 0.703 |


**Q32: How can I trigger and forward webhook events using Stripe for VS Code?**
*(expects URL containing: `stripe-vscode`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/bacs-debit/accept-a-payme | 0.581 | docs.stripe.com/payments/bacs-debit/accept-a-payme | 0.571 | docs.stripe.com/payments/advanced/build-subscripti | 0.560 |
| crawl4ai | #1 | docs.stripe.com/stripe-vscode | 0.673 | docs.stripe.com/webhooks | 0.672 | docs.stripe.com/stripe-vscode | 0.661 |
| crawl4ai-raw | #1 | docs.stripe.com/stripe-vscode | 0.673 | docs.stripe.com/webhooks | 0.672 | docs.stripe.com/stripe-vscode | 0.661 |
| scrapy+md | miss | docs.stripe.com/stripe-cli/triggers | 0.640 | docs.stripe.com/webhooks/handling-payment-events | 0.619 | docs.stripe.com/webhooks/handling-payment-events | 0.608 |
| crawlee | #1 | docs.stripe.com/stripe-vscode | 0.698 | docs.stripe.com/webhooks/quickstart | 0.697 | docs.stripe.com/stripe-vscode | 0.694 |
| colly+md | #1 | docs.stripe.com/stripe-vscode | 0.712 | docs.stripe.com/webhooks/quickstart | 0.695 | docs.stripe.com/stripe-vscode | 0.694 |
| playwright | #1 | docs.stripe.com/stripe-vscode | 0.698 | docs.stripe.com/webhooks/quickstart | 0.697 | docs.stripe.com/stripe-vscode | 0.694 |


**Q33: How can I create tax rates in Stripe?**
*(expects URL containing: `tax-rates`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/checkout/use-manual-tax-r | 0.746 | docs.stripe.com/payments/checkout/use-manual-tax-r | 0.735 | docs.stripe.com/payments/checkout/use-manual-tax-r | 0.697 |
| crawl4ai | #1 | docs.stripe.com/tax/tax-rates | 0.800 | docs.stripe.com/tax/tax-rates | 0.799 | docs.stripe.com/tax | 0.697 |
| crawl4ai-raw | #1 | docs.stripe.com/tax/tax-rates | 0.800 | docs.stripe.com/tax/tax-rates | 0.799 | docs.stripe.com/tax | 0.697 |
| scrapy+md | miss | docs.stripe.com/invoicing/taxes?dashboard-or-api=d | 0.708 | docs.stripe.com/tax/invoicing/tax-ids | 0.655 | docs.stripe.com/invoicing/taxes?dashboard-or-api=d | 0.646 |
| crawlee | #1 | docs.stripe.com/tax/tax-rates | 0.846 | docs.stripe.com/tax/tax-rates | 0.809 | docs.stripe.com/tax/set-up | 0.777 |
| colly+md | #1 | docs.stripe.com/tax/tax-rates | 0.846 | docs.stripe.com/tax/tax-rates | 0.810 | docs.stripe.com/tax/set-up | 0.777 |
| playwright | #1 | docs.stripe.com/tax/tax-rates | 0.846 | docs.stripe.com/tax/tax-rates | 0.809 | docs.stripe.com/tax/set-up | 0.777 |


**Q34: What are the required properties for creating a tax rate?**
*(expects URL containing: `tax-rates`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/checkout/use-manual-tax-r | 0.589 | docs.stripe.com/payments/checkout/use-manual-tax-r | 0.536 | docs.stripe.com/payments/checkout/use-manual-tax-r | 0.503 |
| crawl4ai | #1 | docs.stripe.com/tax/tax-rates | 0.619 | docs.stripe.com/tax/tax-rates | 0.562 | docs.stripe.com/tax/tax-rates | 0.537 |
| crawl4ai-raw | #1 | docs.stripe.com/tax/tax-rates | 0.619 | docs.stripe.com/tax/tax-rates | 0.562 | docs.stripe.com/tax/tax-rates | 0.537 |
| scrapy+md | miss | docs.stripe.com/reports/report-types/tax | 0.468 | docs.stripe.com/js/payment_intents/create_radar_se | 0.467 | docs.stripe.com/js/elements_object/create_element? | 0.467 |
| crawlee | #1 | docs.stripe.com/tax/tax-rates | 0.597 | docs.stripe.com/tax/tax-rates | 0.592 | docs.stripe.com/api/customers | 0.577 |
| colly+md | #1 | docs.stripe.com/tax/tax-rates | 0.597 | docs.stripe.com/tax/tax-rates | 0.588 | docs.stripe.com/changelog/dahlia/2026-04-22/adds-e | 0.579 |
| playwright | #1 | docs.stripe.com/tax/tax-rates | 0.597 | docs.stripe.com/tax/tax-rates | 0.592 | docs.stripe.com/api/customers | 0.577 |


**Q35: What is UPI and how does it work?**
*(expects URL containing: `upi`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/upi | 0.601 | docs.stripe.com/payments/link/upi | 0.569 | docs.stripe.com/payments/upi | 0.555 |
| crawl4ai | #1 | docs.stripe.com/payments/upi | 0.601 | docs.stripe.com/payments/upi | 0.522 | docs.stripe.com/glossary | 0.434 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/upi | 0.601 | docs.stripe.com/payments/upi | 0.522 | docs.stripe.com/js/element/other_element | 0.441 |
| scrapy+md | #1 | docs.stripe.com/payments/upi | 0.596 | docs.stripe.com/payments/upi | 0.540 | docs.stripe.com/payments/upi/accept-a-payment | 0.505 |
| crawlee | #1 | docs.stripe.com/payments/upi | 0.594 | docs.stripe.com/payments/upi | 0.540 | docs.stripe.com/payments/upi | 0.479 |
| colly+md | #1 | docs.stripe.com/changelog/dahlia/2026-03-25/adds-s | 0.480 | docs.stripe.com/glossary | 0.434 | docs.stripe.com/changelog/dahlia/2026-03-25/adds-s | 0.419 |
| playwright | #1 | docs.stripe.com/payments/upi | 0.594 | docs.stripe.com/payments/upi | 0.521 | docs.stripe.com/payments/upi | 0.472 |


**Q36: What are the transaction limits for UPI payments?**
*(expects URL containing: `upi`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/upi | 0.632 | docs.stripe.com/payments/upi | 0.566 | docs.stripe.com/payments/upi/accept-a-payment | 0.560 |
| crawl4ai | #1 | docs.stripe.com/payments/upi | 0.648 | docs.stripe.com/payments/upi | 0.619 | docs.stripe.com/payments/upi | 0.543 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/upi | 0.648 | docs.stripe.com/payments/upi | 0.619 | docs.stripe.com/payments/upi | 0.543 |
| scrapy+md | #1 | docs.stripe.com/payments/upi | 0.656 | docs.stripe.com/payments/upi | 0.618 | docs.stripe.com/payments/upi | 0.549 |
| crawlee | #1 | docs.stripe.com/payments/upi | 0.658 | docs.stripe.com/payments/upi | 0.618 | docs.stripe.com/payments/upi | 0.549 |
| colly+md | #1 | docs.stripe.com/changelog/dahlia/2026-03-25/adds-s | 0.511 | docs.stripe.com/changelog | 0.485 | docs.stripe.com/currencies#minimum-and-maximum-cha | 0.471 |
| playwright | #1 | docs.stripe.com/payments/upi | 0.659 | docs.stripe.com/payments/upi | 0.618 | docs.stripe.com/payments/upi | 0.535 |


**Q37: How can I fulfill orders using the Checkout Sessions API?**
*(expects URL containing: `fulfillment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/checkout/migration | 0.632 | docs.stripe.com/payments/checkout/migration | 0.632 | docs.stripe.com/payments/multicapture | 0.624 |
| crawl4ai | #11 | docs.stripe.com/api/checkout/sessions/object | 0.669 | docs.stripe.com/api/checkout/sessions/create | 0.669 | docs.stripe.com/api/checkout/sessions | 0.669 |
| crawl4ai-raw | #11 | docs.stripe.com/api/checkout/sessions/create | 0.669 | docs.stripe.com/api/checkout/sessions/object | 0.669 | docs.stripe.com/api/checkout/sessions | 0.669 |
| scrapy+md | #1 | docs.stripe.com/checkout/fulfillment?payment-ui=st | 0.616 | docs.stripe.com/billing/subscriptions/ideal | 0.595 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.593 |
| crawlee | #18 | docs.stripe.com/payments/quickstart-checkout-sessi | 0.746 | docs.stripe.com/api/checkout/sessions/create | 0.720 | docs.stripe.com/api/checkout/sessions | 0.675 |
| colly+md | #24 | docs.stripe.com/payments/checkout-sessions | 0.772 | docs.stripe.com/payments/quickstart-checkout-sessi | 0.746 | docs.stripe.com/api/checkout/sessions/create#creat | 0.720 |
| playwright | #18 | docs.stripe.com/payments/quickstart-checkout-sessi | 0.746 | docs.stripe.com/api/checkout/sessions/create | 0.720 | docs.stripe.com/api/checkout/sessions | 0.675 |


**Q38: What is the recommended method for automating fulfillment in Stripe?**
*(expects URL containing: `fulfillment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/save-and-reuse?platform=w | 0.547 | docs.stripe.com/payments/advanced/dashboard-paymen | 0.543 | docs.stripe.com/payments/dashboard-payment-methods | 0.543 |
| crawl4ai | #1 | docs.stripe.com/checkout/fulfillment | 0.621 | docs.stripe.com/checkout/fulfillment | 0.607 | docs.stripe.com/checkout/fulfillment | 0.576 |
| crawl4ai-raw | #1 | docs.stripe.com/checkout/fulfillment | 0.621 | docs.stripe.com/checkout/fulfillment | 0.607 | docs.stripe.com/checkout/fulfillment | 0.576 |
| scrapy+md | #4 | docs.stripe.com/billing/automations | 0.595 | docs.stripe.com/connect/saas/tasks/enable-in-conte | 0.565 | docs.stripe.com/payments/checkout/adjustable-quant | 0.563 |
| crawlee | #2 | docs.stripe.com/billing/revenue-recovery/customer- | 0.677 | docs.stripe.com/checkout/fulfillment | 0.661 | docs.stripe.com/workflows | 0.596 |
| colly+md | #2 | docs.stripe.com/billing/revenue-recovery/customer- | 0.678 | docs.stripe.com/checkout/fulfillment | 0.661 | docs.stripe.com/workflows | 0.596 |
| playwright | #2 | docs.stripe.com/billing/revenue-recovery/customer- | 0.678 | docs.stripe.com/checkout/fulfillment | 0.661 | docs.stripe.com/workflows | 0.596 |


**Q39: How can I view a payout's status in the Stripe Dashboard?**
*(expects URL containing: `manage-payouts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/payment-intents/verifying | 0.552 | docs.stripe.com/payments/checkout/client | 0.549 | docs.stripe.com/payments/analytics | 0.526 |
| crawl4ai | #1 | docs.stripe.com/global-payouts/manage-payouts | 0.748 | docs.stripe.com/bank-reconciliation | 0.711 | docs.stripe.com/global-payouts/manage-payouts | 0.707 |
| crawl4ai-raw | #1 | docs.stripe.com/global-payouts/manage-payouts | 0.748 | docs.stripe.com/bank-reconciliation | 0.711 | docs.stripe.com/global-payouts/manage-payouts | 0.707 |
| scrapy+md | miss | docs.stripe.com/payouts/reconciliation | 0.672 | docs.stripe.com/payouts/instant-payouts | 0.649 | docs.stripe.com/payouts/trace-id | 0.614 |
| crawlee | #3 | docs.stripe.com/bank-reconciliation | 0.709 | docs.stripe.com/payouts/instant-payouts | 0.705 | docs.stripe.com/global-payouts/manage-payouts | 0.697 |
| colly+md | #3 | docs.stripe.com/bank-reconciliation | 0.709 | docs.stripe.com/payouts/instant-payouts | 0.705 | docs.stripe.com/global-payouts/manage-payouts | 0.692 |
| playwright | #2 | docs.stripe.com/bank-reconciliation | 0.709 | docs.stripe.com/global-payouts/manage-payouts | 0.706 | docs.stripe.com/payouts/instant-payouts | 0.705 |


**Q40: What should I do if a payout has been returned due to incorrect destination information?**
*(expects URL containing: `manage-payouts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/link/upi | 0.467 | docs.stripe.com/payments/bank-transfers | 0.401 | docs.stripe.com/payments/bank-transfers | 0.397 |
| crawl4ai | #1 | docs.stripe.com/global-payouts/manage-payouts | 0.604 | docs.stripe.com/payouts | 0.496 | docs.stripe.com/global-payouts/manage-payouts | 0.475 |
| crawl4ai-raw | #1 | docs.stripe.com/global-payouts/manage-payouts | 0.604 | docs.stripe.com/payouts | 0.496 | docs.stripe.com/global-payouts/manage-payouts | 0.475 |
| scrapy+md | miss | docs.stripe.com/payouts/reconciliation | 0.461 | docs.stripe.com/payouts/trace-id | 0.460 | docs.stripe.com/reports/payout-reconciliation | 0.428 |
| crawlee | #1 | docs.stripe.com/global-payouts/manage-payouts | 0.595 | docs.stripe.com/payouts | 0.484 | docs.stripe.com/global-payouts/manage-payouts | 0.475 |
| colly+md | #1 | docs.stripe.com/global-payouts/manage-payouts | 0.595 | docs.stripe.com/payouts | 0.484 | docs.stripe.com/global-payouts/manage-payouts | 0.478 |
| playwright | #1 | docs.stripe.com/global-payouts/manage-payouts | 0.595 | docs.stripe.com/payouts | 0.484 | docs.stripe.com/global-payouts/manage-payouts | 0.474 |


**Q41: How do I enable tax ID collection for new customers in Checkout?**
*(expects URL containing: `tax-ids`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/advanced/tax | 0.702 | docs.stripe.com/payments/advanced/tax | 0.653 | docs.stripe.com/payments/advanced/tax | 0.616 |
| crawl4ai | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.781 | docs.stripe.com/tax/checkout/tax-ids | 0.760 | docs.stripe.com/tax/checkout/tax-ids | 0.686 |
| crawl4ai-raw | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.780 | docs.stripe.com/tax/checkout/tax-ids | 0.760 | docs.stripe.com/tax/checkout/tax-ids | 0.686 |
| scrapy+md | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.768 | docs.stripe.com/tax/checkout/tax-ids | 0.752 | docs.stripe.com/tax/checkout/tax-ids | 0.671 |
| crawlee | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.752 | docs.stripe.com/tax/checkout/tax-ids | 0.743 | docs.stripe.com/tax/checkout/tax-ids | 0.699 |
| colly+md | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.748 | docs.stripe.com/tax/checkout/tax-ids | 0.743 | docs.stripe.com/tax/checkout/tax-ids | 0.699 |
| playwright | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.752 | docs.stripe.com/tax/checkout/tax-ids | 0.743 | docs.stripe.com/tax/checkout/tax-ids | 0.699 |


**Q42: What types of tax IDs can Checkout collect in different regions?**
*(expects URL containing: `tax-ids`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/advanced/tax | 0.638 | docs.stripe.com/payments/advanced/tax | 0.614 | docs.stripe.com/payments/advanced/tax | 0.602 |
| crawl4ai | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.738 | docs.stripe.com/tax/checkout/tax-ids | 0.687 | docs.stripe.com/tax/checkout/tax-ids | 0.684 |
| crawl4ai-raw | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.738 | docs.stripe.com/tax/checkout/tax-ids | 0.686 | docs.stripe.com/tax/checkout/tax-ids | 0.684 |
| scrapy+md | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.718 | docs.stripe.com/tax/checkout/tax-ids | 0.680 | docs.stripe.com/tax/checkout/tax-ids | 0.673 |
| crawlee | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.728 | docs.stripe.com/tax/checkout/tax-ids | 0.718 | docs.stripe.com/tax/checkout/tax-ids | 0.680 |
| colly+md | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.717 | docs.stripe.com/tax/checkout/tax-ids | 0.680 | docs.stripe.com/tax/checkout/tax-ids | 0.661 |
| playwright | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.728 | docs.stripe.com/tax/checkout/tax-ids | 0.718 | docs.stripe.com/tax/checkout/tax-ids | 0.680 |


**Q43: How can I add funds to my stablecoin balance?**
*(expects URL containing: `stablecoins`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | docs.stripe.com/payments/accept-stablecoin-payment | 0.544 | docs.stripe.com/payments/stablecoin-payments | 0.522 | docs.stripe.com/payments/stablecoin-payments | 0.508 |
| crawl4ai | #1 | docs.stripe.com/treasury/stablecoins | 0.627 | docs.stripe.com/treasury/stablecoins | 0.603 | docs.stripe.com/treasury/stablecoins | 0.583 |
| crawl4ai-raw | #1 | docs.stripe.com/treasury/stablecoins | 0.627 | docs.stripe.com/treasury/stablecoins | 0.603 | docs.stripe.com/treasury/stablecoins | 0.583 |
| scrapy+md | #11 | docs.stripe.com/payments/accept-stablecoin-payment | 0.587 | docs.stripe.com/payments/deposit-mode-stablecoin-p | 0.563 | docs.stripe.com/payments/accept-stablecoin-payment | 0.482 |
| crawlee | #1 | docs.stripe.com/treasury/stablecoins | 0.624 | docs.stripe.com/treasury/stablecoins | 0.624 | docs.stripe.com/treasury/stablecoins | 0.622 |
| colly+md | miss | docs.stripe.com/get-started/account/add-funds | 0.580 | docs.stripe.com/payments/stablecoin-payments | 0.578 | docs.stripe.com/connect/top-ups | 0.577 |
| playwright | #1 | docs.stripe.com/treasury/stablecoins | 0.624 | docs.stripe.com/treasury/stablecoins | 0.624 | docs.stripe.com/treasury/stablecoins | 0.622 |


**Q44: What currencies are supported for stablecoin payouts?**
*(expects URL containing: `stablecoins`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | docs.stripe.com/payments/stablecoin-payments | 0.587 | docs.stripe.com/payments/accept-stablecoin-payment | 0.550 | docs.stripe.com/payments/stablecoin-payments | 0.524 |
| crawl4ai | #1 | docs.stripe.com/treasury/stablecoins | 0.690 | docs.stripe.com/connect/stablecoin-payouts | 0.637 | docs.stripe.com/payments/stablecoin-payments | 0.624 |
| crawl4ai-raw | #1 | docs.stripe.com/treasury/stablecoins | 0.690 | docs.stripe.com/connect/stablecoin-payouts | 0.637 | docs.stripe.com/payments/stablecoin-payments | 0.624 |
| scrapy+md | #18 | docs.stripe.com/payments/accept-stablecoin-payment | 0.570 | docs.stripe.com/payments/deposit-mode-stablecoin-p | 0.533 | docs.stripe.com/payments/currencies/settlement-pay | 0.496 |
| crawlee | #1 | docs.stripe.com/treasury/stablecoins | 0.679 | docs.stripe.com/connect/stablecoin-payouts | 0.638 | docs.stripe.com/payments/stablecoin-payments | 0.618 |
| colly+md | miss | docs.stripe.com/connect/stablecoin-payouts | 0.638 | docs.stripe.com/payments/stablecoin-payments | 0.618 | docs.stripe.com/connect/stablecoin-payouts | 0.611 |
| playwright | #1 | docs.stripe.com/treasury/stablecoins | 0.679 | docs.stripe.com/connect/stablecoin-payouts | 0.638 | docs.stripe.com/payments/stablecoin-payments | 0.618 |


**Q45: What documents does Atlas use to incorporate your company?**
*(expects URL containing: `incorporation-documents`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/managed-payments/tax-comp | 0.341 | docs.stripe.com/payments/advanced/tax | 0.321 | docs.stripe.com/payments/bizum | 0.314 |
| crawl4ai | #1 | docs.stripe.com/atlas/incorporation-documents | 0.811 | docs.stripe.com/atlas/signup | 0.758 | docs.stripe.com/atlas/incorporation-documents | 0.738 |
| crawl4ai-raw | #1 | docs.stripe.com/atlas/incorporation-documents | 0.811 | docs.stripe.com/atlas/signup | 0.758 | docs.stripe.com/atlas/incorporation-documents | 0.738 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.429 | docs.stripe.com/connect/networked-onboarding | 0.346 | docs.stripe.com/connect/account-tokens | 0.344 |
| crawlee | #1 | docs.stripe.com/atlas/incorporation-documents | 0.800 | docs.stripe.com/atlas/signup | 0.752 | docs.stripe.com/atlas/signup | 0.719 |
| colly+md | miss | docs.stripe.com/atlas/indian-founder-guide | 0.668 | docs.stripe.com/atlas | 0.649 | docs.stripe.com/atlas/indian-founder-guide | 0.646 |
| playwright | #1 | docs.stripe.com/atlas/incorporation-documents | 0.800 | docs.stripe.com/atlas/signup | 0.752 | docs.stripe.com/atlas/incorporation-documents | 0.732 |


**Q46: What is the purpose of the Certificate of Incorporation?**
*(expects URL containing: `incorporation-documents`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/ideal | 0.253 | docs.stripe.com/payments/bacs-debit/mandate-collec | 0.239 | docs.stripe.com/payments/payment-methods/custom-pa | 0.237 |
| crawl4ai | #1 | docs.stripe.com/atlas/incorporation-documents | 0.463 | docs.stripe.com/atlas/signup | 0.410 | docs.stripe.com/atlas/signup | 0.394 |
| crawl4ai-raw | #1 | docs.stripe.com/atlas/incorporation-documents | 0.463 | docs.stripe.com/atlas/signup | 0.410 | docs.stripe.com/atlas/signup | 0.394 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.250 | docs.stripe.com/llms.txt | 0.246 | docs.stripe.com/connect/testing | 0.243 |
| crawlee | #1 | docs.stripe.com/atlas/incorporation-documents | 0.452 | docs.stripe.com/atlas/incorporation-documents | 0.397 | docs.stripe.com/atlas/signup | 0.394 |
| colly+md | miss | docs.stripe.com/atlas/83b-elections-non-us-founder | 0.361 | docs.stripe.com/atlas | 0.360 | docs.stripe.com/atlas | 0.355 |
| playwright | #1 | docs.stripe.com/atlas/incorporation-documents | 0.452 | docs.stripe.com/atlas/incorporation-documents | 0.406 | docs.stripe.com/atlas/incorporation-documents | 0.397 |


**Q47: What countries is Stripe Issuing available in?**
*(expects URL containing: `issuing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/cards | 0.664 | docs.stripe.com/payments/cards | 0.595 | docs.stripe.com/payments/payment-methods/overview | 0.583 |
| crawl4ai | #4 | docs.stripe.com/payments/cards | 0.674 | docs.stripe.com/identity | 0.665 | docs.stripe.com/currencies | 0.662 |
| crawl4ai-raw | #4 | docs.stripe.com/payments/cards | 0.674 | docs.stripe.com/identity | 0.665 | docs.stripe.com/currencies | 0.662 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.650 | docs.stripe.com/terminal/payments/regional?integra | 0.644 | docs.stripe.com/terminal/payments/regional?integra | 0.644 |
| crawlee | #3 | docs.stripe.com/payments/cards | 0.664 | docs.stripe.com/currencies#presentment-currencies | 0.662 | docs.stripe.com/issuing | 0.659 |
| colly+md | #4 | docs.stripe.com/payments/cards#supported-card-bran | 0.664 | docs.stripe.com/payments/cards | 0.664 | docs.stripe.com/currencies#minimum-and-maximum-cha | 0.662 |
| playwright | #3 | docs.stripe.com/payments/cards | 0.664 | docs.stripe.com/currencies | 0.662 | docs.stripe.com/issuing | 0.659 |


**Q48: What features does Stripe Issuing offer for managing purchases?**
*(expects URL containing: `issuing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/checkout/how-checkout-wor | 0.574 | docs.stripe.com/payments/quickstart-checkout-sessi | 0.574 | docs.stripe.com/payments/payment-methods/overview | 0.574 |
| crawl4ai | #2 | docs.stripe.com/llms.txt | 0.668 | docs.stripe.com/issuing | 0.651 | docs.stripe.com/issuing/funding/balance | 0.647 |
| crawl4ai-raw | #2 | docs.stripe.com/llms.txt | 0.668 | docs.stripe.com/issuing | 0.651 | docs.stripe.com/issuing/funding/balance | 0.647 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.654 | docs.stripe.com/llms.txt | 0.596 | docs.stripe.com/payments/installments | 0.582 |
| crawlee | #1 | docs.stripe.com/issuing | 0.675 | docs.stripe.com/llms.txt | 0.668 | docs.stripe.com/issuing | 0.652 |
| colly+md | #1 | docs.stripe.com/issuing | 0.675 | docs.stripe.com/issuing | 0.652 | docs.stripe.com/issuing/for-your-business | 0.648 |
| playwright | #1 | docs.stripe.com/issuing | 0.675 | docs.stripe.com/llms.txt | 0.668 | docs.stripe.com/issuing | 0.652 |


**Q49: What are the additional fees for accepting payments with installments in Mexico?**
*(expects URL containing: `mx-installments`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/mx-installments | 0.718 | docs.stripe.com/payments/mx-installments | 0.708 | docs.stripe.com/payments/mx-installments | 0.633 |
| crawl4ai | #1 | docs.stripe.com/payments/mx-installments | 0.717 | docs.stripe.com/payments/mx-installments | 0.717 | docs.stripe.com/payments/mx-installments | 0.684 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/mx-installments | 0.717 | docs.stripe.com/payments/mx-installments | 0.717 | docs.stripe.com/payments/mx-installments | 0.684 |
| scrapy+md | miss | docs.stripe.com/payments/installments | 0.583 | docs.stripe.com/payments/oxxo/accept-a-payment | 0.513 | docs.stripe.com/payments/oxxo/accept-a-payment | 0.508 |
| crawlee | #1 | docs.stripe.com/payments/mx-installments | 0.738 | docs.stripe.com/payments/mx-installments | 0.718 | docs.stripe.com/payments/mx-installments | 0.618 |
| colly+md | miss | docs.stripe.com/payments/installments | 0.602 | docs.stripe.com/recurring-payments#enable-customer | 0.545 | docs.stripe.com/recurring-payments#recurring-donat | 0.544 |
| playwright | #1 | docs.stripe.com/payments/mx-installments | 0.738 | docs.stripe.com/payments/mx-installments | 0.718 | docs.stripe.com/payments/mx-installments | 0.626 |


**Q50: What are the requirements for using installments (meses sin intereses) with Stripe in Mexico?**
*(expects URL containing: `mx-installments`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/mx-installments | 0.812 | docs.stripe.com/payments/mx-installments | 0.786 | docs.stripe.com/payments/meses-sin-intereses/accep | 0.713 |
| crawl4ai | #1 | docs.stripe.com/payments/mx-installments | 0.836 | docs.stripe.com/payments/mx-installments | 0.798 | docs.stripe.com/payments/mx-installments | 0.717 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/mx-installments | 0.836 | docs.stripe.com/payments/mx-installments | 0.798 | docs.stripe.com/payments/mx-installments | 0.717 |
| scrapy+md | miss | docs.stripe.com/payments/installments | 0.635 | docs.stripe.com/payments/oxxo/accept-a-payment | 0.562 | docs.stripe.com/payments/oxxo/accept-a-payment | 0.550 |
| crawlee | #1 | docs.stripe.com/payments/mx-installments | 0.836 | docs.stripe.com/payments/mx-installments | 0.812 | docs.stripe.com/payments/mx-installments | 0.797 |
| colly+md | miss | docs.stripe.com/payments/installments | 0.631 | docs.stripe.com/payments/installments | 0.614 | docs.stripe.com/recurring-payments#enable-customer | 0.599 |
| playwright | #1 | docs.stripe.com/payments/mx-installments | 0.836 | docs.stripe.com/payments/mx-installments | 0.812 | docs.stripe.com/payments/mx-installments | 0.797 |


**Q51: What is the purpose of the Stripebot web crawler?**
*(expects URL containing: `stripebot-crawler`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/checkout/how-checkout-wor | 0.494 | docs.stripe.com/payments/payment-intents/three-d-s | 0.480 | docs.stripe.com/payments/pix/accept-a-payment | 0.473 |
| crawl4ai | #1 | docs.stripe.com/stripebot-crawler | 0.757 | docs.stripe.com/stripebot-crawler | 0.629 | docs.stripe.com/samples | 0.509 |
| crawl4ai-raw | #1 | docs.stripe.com/stripebot-crawler | 0.757 | docs.stripe.com/stripebot-crawler | 0.629 | docs.stripe.com/samples | 0.509 |
| scrapy+md | miss | docs.stripe.com/search | 0.509 | docs.stripe.com/connect/saas/tasks/enable-in-conte | 0.505 | docs.stripe.com/cli/fixtures | 0.497 |
| crawlee | #1 | docs.stripe.com/stripebot-crawler | 0.848 | docs.stripe.com/stripebot-crawler | 0.742 | docs.stripe.com/stripebot-crawler | 0.624 |
| colly+md | #1 | docs.stripe.com/stripebot-crawler | 0.848 | docs.stripe.com/stripebot-crawler | 0.732 | docs.stripe.com/stripebot-crawler | 0.621 |
| playwright | #1 | docs.stripe.com/stripebot-crawler | 0.848 | docs.stripe.com/stripebot-crawler | 0.742 | docs.stripe.com/stripebot-crawler | 0.622 |


**Q52: How can I verify that a web crawler accessing my server is Stripebot?**
*(expects URL containing: `stripebot-crawler`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/orchestration/route-payme | 0.533 | docs.stripe.com/payments/bacs-debit/accept-a-payme | 0.510 | docs.stripe.com/payments/payment-intents/three-d-s | 0.510 |
| crawl4ai | #1 | docs.stripe.com/stripebot-crawler | 0.769 | docs.stripe.com/stripebot-crawler | 0.666 | docs.stripe.com/webhooks | 0.538 |
| crawl4ai-raw | #1 | docs.stripe.com/stripebot-crawler | 0.769 | docs.stripe.com/stripebot-crawler | 0.666 | docs.stripe.com/webhooks | 0.538 |
| scrapy+md | miss | docs.stripe.com/connect/saas/tasks/enable-in-conte | 0.546 | docs.stripe.com/disputes/prevention/advanced-fraud | 0.531 | docs.stripe.com/webhooks/handling-payment-events | 0.515 |
| crawlee | #1 | docs.stripe.com/stripebot-crawler | 0.754 | docs.stripe.com/stripebot-crawler | 0.752 | docs.stripe.com/stripebot-crawler | 0.654 |
| colly+md | #1 | docs.stripe.com/stripebot-crawler | 0.752 | docs.stripe.com/stripebot-crawler | 0.752 | docs.stripe.com/stripebot-crawler | 0.648 |
| playwright | #1 | docs.stripe.com/stripebot-crawler | 0.754 | docs.stripe.com/stripebot-crawler | 0.752 | docs.stripe.com/stripebot-crawler | 0.656 |


**Q53: How can I securely accept payments online with Stripe?**
*(expects URL containing: `accept-a-payment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.stripe.com/payments/payment-intents/three-d-s | 0.627 | docs.stripe.com/payments/accept-a-payment-synchron | 0.605 | docs.stripe.com/payments/save-and-reuse?platform=w | 0.603 |
| crawl4ai | #2 | docs.stripe.com/secure-remote-commerce | 0.639 | docs.stripe.com/payments/accept-a-payment | 0.635 | docs.stripe.com/payments/accept-a-payment?platform | 0.635 |
| crawl4ai-raw | #2 | docs.stripe.com/secure-remote-commerce | 0.639 | docs.stripe.com/payments/accept-a-payment?platform | 0.635 | docs.stripe.com/payments/accept-a-payment?payment- | 0.635 |
| scrapy+md | #3 | docs.stripe.com/get-started/data-migrations/pan-im | 0.641 | docs.stripe.com/payments/3d-secure/authentication- | 0.635 | docs.stripe.com/payments/accept-a-payment?payment- | 0.618 |
| crawlee | #4 | docs.stripe.com/security | 0.737 | docs.stripe.com/payments/3d-secure | 0.711 | docs.stripe.com/payments/online-payments | 0.706 |
| colly+md | #5 | docs.stripe.com/security | 0.737 | docs.stripe.com/payments/3d-secure | 0.711 | docs.stripe.com/payments/online-payments#compare-f | 0.706 |
| playwright | #4 | docs.stripe.com/security | 0.737 | docs.stripe.com/payments/3d-secure | 0.711 | docs.stripe.com/payments/online-payments | 0.706 |


**Q54: What is a Checkout Session in Stripe?**
*(expects URL containing: `accept-a-payment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.770 | docs.stripe.com/payments/checkout/save-and-reuse?p | 0.734 | docs.stripe.com/payments/bacs-debit/accept-a-payme | 0.721 |
| crawl4ai | #20 | docs.stripe.com/api/checkout/sessions/create | 0.756 | docs.stripe.com/api/checkout/sessions/object | 0.756 | docs.stripe.com/api/checkout/sessions | 0.756 |
| crawl4ai-raw | #20 | docs.stripe.com/api/checkout/sessions | 0.756 | docs.stripe.com/api/checkout/sessions/create | 0.756 | docs.stripe.com/api/checkout/sessions/object | 0.756 |
| scrapy+md | #10 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.703 | docs.stripe.com/api/checkout/sessions/line_items | 0.700 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.694 |
| crawlee | #34 | docs.stripe.com/api/checkout/sessions/create | 0.851 | docs.stripe.com/api/checkout/sessions/object#check | 0.840 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.798 |
| colly+md | #41 | docs.stripe.com/api/checkout/sessions/create#creat | 0.851 | docs.stripe.com/api/checkout/sessions/create#creat | 0.851 | docs.stripe.com/api/checkout/sessions/create#creat | 0.851 |
| playwright | #29 | docs.stripe.com/api/checkout/sessions/create | 0.851 | docs.stripe.com/api/checkout/sessions/object | 0.840 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.798 |


**Q55: How can I access consolidated reports for multiple accounts in my organization?**
*(expects URL containing: `multiple-accounts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/analytics/acceptance | 0.394 | docs.stripe.com/payments/analytics/optimization | 0.388 | docs.stripe.com/payments/analytics/acceptance | 0.385 |
| crawl4ai | #1 | docs.stripe.com/reports/multiple-accounts | 0.688 | docs.stripe.com/reports/multiple-accounts | 0.594 | docs.stripe.com/reports/options | 0.466 |
| crawl4ai-raw | #1 | docs.stripe.com/reports/multiple-accounts | 0.688 | docs.stripe.com/reports/multiple-accounts | 0.594 | docs.stripe.com/reports/options | 0.466 |
| scrapy+md | miss | docs.stripe.com/reports/report-types/connect | 0.515 | docs.stripe.com/reports/options | 0.474 | docs.stripe.com/reports/report-types/connect | 0.474 |
| crawlee | #1 | docs.stripe.com/reports/multiple-accounts | 0.723 | docs.stripe.com/reports/multiple-accounts | 0.565 | docs.stripe.com/reports/multiple-accounts | 0.536 |
| colly+md | #1 | docs.stripe.com/reports/multiple-accounts | 0.721 | docs.stripe.com/reports/multiple-accounts | 0.631 | docs.stripe.com/reports/multiple-accounts | 0.541 |
| playwright | #1 | docs.stripe.com/reports/multiple-accounts | 0.723 | docs.stripe.com/reports/multiple-accounts | 0.574 | docs.stripe.com/reports/multiple-accounts | 0.536 |


**Q56: What are the file size limits for downloading reports from multiple accounts?**
*(expects URL containing: `multiple-accounts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/payto | 0.396 | docs.stripe.com/payments/analytics/acceptance | 0.377 | docs.stripe.com/payments/payto | 0.354 |
| crawl4ai | #1 | docs.stripe.com/reports/multiple-accounts | 0.575 | docs.stripe.com/reports/multiple-accounts | 0.463 | docs.stripe.com/tax/reports | 0.428 |
| crawl4ai-raw | #1 | docs.stripe.com/reports/multiple-accounts | 0.575 | docs.stripe.com/reports/multiple-accounts | 0.463 | docs.stripe.com/tax/reports | 0.428 |
| scrapy+md | miss | docs.stripe.com/reports/report-types/connect | 0.478 | docs.stripe.com/reports/api | 0.436 | docs.stripe.com/reports/payout-reconciliation | 0.407 |
| crawlee | #1 | docs.stripe.com/reports/multiple-accounts | 0.656 | docs.stripe.com/reports/multiple-accounts | 0.573 | docs.stripe.com/reports/multiple-accounts | 0.547 |
| colly+md | #1 | docs.stripe.com/reports/multiple-accounts | 0.700 | docs.stripe.com/reports/multiple-accounts | 0.553 | docs.stripe.com/reports/multiple-accounts | 0.513 |
| playwright | #1 | docs.stripe.com/reports/multiple-accounts | 0.689 | docs.stripe.com/reports/multiple-accounts | 0.566 | docs.stripe.com/reports/multiple-accounts | 0.547 |


**Q57: How do I enable Link in my payment method settings?**
*(expects URL containing: `link-payment-integrations`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #8 | docs.stripe.com/payments/link/card-element-link | 0.688 | docs.stripe.com/payments/link/checkout-link | 0.662 | docs.stripe.com/payments/link/link-payment-methods | 0.652 |
| crawl4ai | #6 | docs.stripe.com/payments/link/link-payment-methods | 0.689 | docs.stripe.com/payments/link/checkout-link | 0.680 | docs.stripe.com/payments/link/invoicing | 0.679 |
| crawl4ai-raw | #6 | docs.stripe.com/payments/link/link-payment-methods | 0.689 | docs.stripe.com/payments/link/checkout-link | 0.680 | docs.stripe.com/payments/link/invoicing | 0.679 |
| scrapy+md | #4 | docs.stripe.com/payments/link/card-element-link | 0.688 | docs.stripe.com/payments/link/invoicing | 0.658 | docs.stripe.com/payments/link/payment-request-butt | 0.654 |
| crawlee | #6 | docs.stripe.com/payments/link/checkout-link | 0.670 | docs.stripe.com/payments/link | 0.661 | docs.stripe.com/payments/link/link-payment-methods | 0.655 |
| colly+md | miss | docs.stripe.com/payments/link | 0.661 | docs.stripe.com/payments/link/link-payment-methods | 0.655 | docs.stripe.com/payments/link/link-payment-methods | 0.652 |
| playwright | #6 | docs.stripe.com/payments/link/checkout-link | 0.667 | docs.stripe.com/payments/link | 0.661 | docs.stripe.com/payments/link/invoicing | 0.658 |


**Q58: What types of payment methods are supported by Link?**
*(expects URL containing: `link-payment-integrations`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | docs.stripe.com/payments/wallets/link | 0.740 | docs.stripe.com/payments/link/link-payment-methods | 0.728 | docs.stripe.com/payments/link | 0.705 |
| crawl4ai | #3 | docs.stripe.com/payments/link/link-payment-methods | 0.769 | docs.stripe.com/payments/link/link-payment-methods | 0.737 | docs.stripe.com/payments/link/link-payment-integra | 0.723 |
| crawl4ai-raw | #3 | docs.stripe.com/payments/link/link-payment-methods | 0.769 | docs.stripe.com/payments/link/link-payment-methods | 0.737 | docs.stripe.com/payments/link/link-payment-integra | 0.723 |
| scrapy+md | #1 | docs.stripe.com/payments/link/link-payment-integra | 0.712 | docs.stripe.com/llms.txt | 0.712 | docs.stripe.com/payments/link/link-payment-integra | 0.704 |
| crawlee | #2 | docs.stripe.com/payments/link/link-payment-methods | 0.745 | docs.stripe.com/payments/link/link-payment-integra | 0.706 | docs.stripe.com/payments/link/link-payment-integra | 0.702 |
| colly+md | miss | docs.stripe.com/payments/link/link-payment-methods | 0.745 | docs.stripe.com/payments/wallets/link | 0.714 | docs.stripe.com/payments/link | 0.702 |
| playwright | #2 | docs.stripe.com/payments/link/link-payment-methods | 0.745 | docs.stripe.com/payments/link/link-payment-integra | 0.712 | docs.stripe.com/payments/link/link-payment-integra | 0.702 |


</details>

## Methodology

- **Queries:** 557 across 11 sites, categorized by type (api-function, code-example, conceptual, structured-data, factual-lookup, cross-page, navigation, js-rendered)
- **Embedding model:** `text-embedding-3-small` (1536 dimensions)
- **Chunking:** Markdown-aware, 400 word max, 50 word overlap
- **Retrieval modes:** Embedding (cosine), BM25 (Okapi), Hybrid (RRF k=60), Reranked (`cross-encoder/ms-marco-MiniLM-L-6-v2`)
- **Retrieval:** Hit rate reported at K = 1, 3, 5, 10, 20, plus MRR
- **Reranking:** Top-50 candidates from hybrid search, reranked to top-20
- **Chunk sensitivity:** Tested at ~256tok, ~512tok, ~1024tok
- **Confidence intervals:** Wilson score interval (95%)
- **Same chunking and embedding** for all tools — only extraction quality varies
- **No fine-tuning or tool-specific optimization** — identical pipeline for all

See [METHODOLOGY.md](METHODOLOGY.md) for full test setup, tool configurations,
and fairness decisions.

## See also

- [QUALITY_COMPARISON.md](QUALITY_COMPARISON.md) — content quality differences that wash out at retrieval time but affect downstream answers
- [ANSWER_QUALITY.md](ANSWER_QUALITY.md) — where the LLM's final answers diverge despite similar retrieval
- [COST_AT_SCALE.md](COST_AT_SCALE.md) — the dollar impact of chunk count differences (2x chunks = 2x embedding cost)
- [METHODOLOGY.md](METHODOLOGY.md) — full test setup, tool configurations, and fairness decisions

