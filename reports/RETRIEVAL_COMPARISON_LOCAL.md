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
`mixedbread-ai/mxbai-embed-large-v1`, and measures retrieval across four modes:

- **Embedding**: Cosine similarity on OpenAI embeddings
- **BM25**: Keyword search (Okapi BM25)
- **Hybrid**: Embedding + BM25 fused via Reciprocal Rank Fusion
- **Reranked**: Hybrid candidates reranked by `cross-encoder/ms-marco-MiniLM-L-6-v2`

**561 queries** across 11 sites.
Hit rate = correct source page in top-K results. Higher is better.
Summary tables use the **499-query common subset** (9 sites) so all tools are compared on identical queries. Sites excluded: huggingface-transformers, newegg (not all tools have data). Per-site tables show full results.

## Quick summary: best retrieval mode per tool

For each tool, the mode with the highest MRR. Most readers can stop here.

| Tool | Best mode | Hit@1 | Hit@3 | Hit@5 | Hit@10 | MRR | Page MRR |
|---|---|---|---|---|---|---|---|
| crawl4ai-raw | embedding | 68% (341/499) ±4% | 83% (412/499) ±3% | 88% (439/499) ±3% | 92% (460/499) ±2% | 0.770 | 0.780 |
| crawl4ai | embedding | 69% (342/499) ±4% | 82% (410/499) ±3% | 87% (434/499) ±3% | 91% (455/499) ±2% | 0.768 | 0.777 |
| playwright | reranked | 62% (309/499) ±4% | 79% (396/499) ±4% | 85% (423/499) ±3% | 89% (443/499) ±3% | 0.722 | 0.731 |
| crawlee | hybrid | 62% (307/499) ±4% | 77% (384/499) ±4% | 82% (409/499) ±3% | 87% (434/499) ±3% | 0.707 | 0.716 |
| colly+md | reranked | 39% (193/499) ±4% | 47% (235/499) ±4% | 49% (247/499) ±4% | 53% (265/499) ±4% | 0.437 | 0.444 |
| markcrawl | hybrid | 29% (143/499) ±4% | 39% (195/499) ±4% | 41% (204/499) ±4% | 44% (221/499) ±4% | 0.343 | 0.349 |
| scrapy+md | embedding | 16% (82/499) ±3% | 19% (95/499) ±3% | 19% (97/499) ±3% | 21% (104/499) ±4% | 0.179 | 0.181 |

> **Column definitions:** **Best mode** = retrieval strategy that maximizes MRR for this tool. **Hit@K** = % of queries where the correct source page appeared in the top K (chunk-level). **MRR** (chunk-level) = Mean Reciprocal Rank across all retrieved chunks. **Page MRR** (DS-1) = MRR after collapsing chunks-per-URL to unique pages — removes the chunk-density gaming signal where a tool emitting more chunks per page would otherwise rank ahead at the same content.

> **Density sensitivity (DS-9):** Hit@1 is the LEAST chunk-density-sensitive (each chunk competes for one slot, so emitting more chunks doesn't help unless the first one is right). Hit@10 is the MOST sensitive (more chunks = more chances to land somewhere in the top 10). MRR sits between the two. Page MRR removes the density signal entirely — read it as the chunk-density-corrected MRR.

## Summary: retrieval modes compared

_Computed over 499 queries on 9 common sites (ikea, kubernetes-docs, mdn-css, postgres-docs, propublica, react-dev, rust-book, smittenkitchen, stripe-docs)._

| Tool | Mode | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Page MRR |
|---|---|---|---|---|---|---|---|---|
| crawl4ai-raw | embedding | 68% (341/499) ±4% | 83% (412/499) ±3% | 88% (439/499) ±3% | 92% (460/499) ±2% | 95% (476/499) ±2% | 0.770 | 0.780 |
| crawl4ai | embedding | 69% (342/499) ±4% | 82% (410/499) ±3% | 87% (434/499) ±3% | 91% (455/499) ±2% | 95% (472/499) ±2% | 0.768 | 0.777 |
| playwright | embedding | 60% (301/499) ±4% | 74% (371/499) ±4% | 81% (402/499) ±3% | 87% (432/499) ±3% | 90% (451/499) ±3% | 0.694 | 0.707 |
| crawlee | embedding | 59% (295/499) ±4% | 74% (367/499) ±4% | 78% (389/499) ±4% | 84% (418/499) ±3% | 86% (431/499) ±3% | 0.678 | 0.692 |
| colly+md | embedding | 37% (183/499) ±4% | 44% (222/499) ±4% | 47% (235/499) ±4% | 51% (252/499) ±4% | 52% (261/499) ±4% | 0.414 | 0.423 |
| markcrawl | embedding | 29% (144/499) ±4% | 38% (189/499) ±4% | 40% (202/499) ±4% | 43% (215/499) ±4% | 44% (221/499) ±4% | 0.341 | 0.347 |
| scrapy+md | embedding | 16% (82/499) ±3% | 19% (95/499) ±3% | 19% (97/499) ±3% | 21% (104/499) ±4% | 22% (108/499) ±4% | 0.179 | 0.181 |
| crawlee | bm25 | 46% (229/499) ±4% | 64% (318/499) ±4% | 70% (347/499) ±4% | 78% (389/499) ±4% | 84% (417/499) ±3% | 0.569 | 0.585 |
| crawl4ai-raw | bm25 | 44% (218/499) ±4% | 65% (325/499) ±4% | 71% (352/499) ±4% | 78% (390/499) ±4% | 83% (414/499) ±3% | 0.558 | 0.572 |
| crawl4ai | bm25 | 44% (220/499) ±4% | 65% (323/499) ±4% | 70% (349/499) ±4% | 78% (388/499) ±4% | 82% (409/499) ±3% | 0.557 | 0.572 |
| playwright | bm25 | 44% (220/499) ±4% | 62% (309/499) ±4% | 68% (337/499) ±4% | 76% (381/499) ±4% | 82% (407/499) ±3% | 0.550 | 0.568 |
| colly+md | bm25 | 26% (128/499) ±4% | 34% (168/499) ±4% | 37% (187/499) ±4% | 41% (207/499) ±4% | 46% (230/499) ±4% | 0.308 | 0.325 |
| markcrawl | bm25 | 21% (104/499) ±4% | 30% (152/499) ±4% | 35% (174/499) ±4% | 39% (194/499) ±4% | 42% (208/499) ±4% | 0.271 | 0.276 |
| scrapy+md | bm25 | 11% (56/499) ±3% | 15% (73/499) ±3% | 17% (84/499) ±3% | 18% (89/499) ±3% | 19% (97/499) ±3% | 0.135 | 0.139 |
| crawl4ai-raw | hybrid | 68% (338/499) ±4% | 82% (408/499) ±3% | 88% (438/499) ±3% | 93% (462/499) ±2% | 96% (481/499) ±2% | 0.765 | 0.776 |
| crawl4ai | hybrid | 67% (336/499) ±4% | 82% (407/499) ±3% | 87% (436/499) ±3% | 92% (458/499) ±2% | 96% (477/499) ±2% | 0.761 | 0.771 |
| playwright | hybrid | 62% (309/499) ±4% | 78% (390/499) ±4% | 83% (416/499) ±3% | 88% (440/499) ±3% | 91% (456/499) ±2% | 0.713 | 0.726 |
| crawlee | hybrid | 62% (307/499) ±4% | 77% (384/499) ±4% | 82% (409/499) ±3% | 87% (434/499) ±3% | 90% (451/499) ±3% | 0.707 | 0.716 |
| colly+md | hybrid | 38% (188/499) ±4% | 45% (223/499) ±4% | 48% (239/499) ±4% | 52% (257/499) ±4% | 54% (267/499) ±4% | 0.420 | 0.431 |
| markcrawl | hybrid | 29% (143/499) ±4% | 39% (195/499) ±4% | 41% (204/499) ±4% | 44% (221/499) ±4% | 46% (228/499) ±4% | 0.343 | 0.349 |
| scrapy+md | hybrid | 17% (83/499) ±3% | 18% (92/499) ±3% | 19% (95/499) ±3% | 21% (105/499) ±4% | 22% (109/499) ±4% | 0.178 | 0.182 |
| crawl4ai-raw | reranked | 65% (323/499) ±4% | 81% (403/499) ±3% | 86% (430/499) ±3% | 93% (462/499) ±2% | 96% (480/499) ±2% | 0.745 | 0.754 |
| crawl4ai | reranked | 64% (321/499) ±4% | 81% (402/499) ±3% | 85% (426/499) ±3% | 92% (458/499) ±2% | 95% (475/499) ±2% | 0.740 | 0.749 |
| playwright | reranked | 62% (309/499) ±4% | 79% (396/499) ±4% | 85% (423/499) ±3% | 89% (443/499) ±3% | 92% (458/499) ±2% | 0.722 | 0.731 |
| crawlee | reranked | 59% (295/499) ±4% | 77% (386/499) ±4% | 82% (409/499) ±3% | 86% (428/499) ±3% | 89% (443/499) ±3% | 0.696 | 0.704 |
| colly+md | reranked | 39% (193/499) ±4% | 47% (235/499) ±4% | 49% (247/499) ±4% | 53% (265/499) ±4% | 55% (273/499) ±4% | 0.437 | 0.444 |
| markcrawl | reranked | 29% (144/499) ±4% | 38% (191/499) ±4% | 41% (206/499) ±4% | 43% (215/499) ±4% | 45% (223/499) ±4% | 0.341 | 0.344 |
| scrapy+md | reranked | 15% (74/499) ±3% | 18% (91/499) ±3% | 20% (98/499) ±3% | 21% (104/499) ±4% | 22% (109/499) ±4% | 0.168 | 0.172 |

> **Column definitions:** **Hit@K** = percentage of queries where the correct source page appeared in the top K results (shown as % with raw counts). **MRR** (Mean Reciprocal Rank, chunk-level) = average of 1/rank for correct results across the chunk-ordered top-K (1.0 = always rank 1, 0.5 = always rank 2). **Page MRR** (DS-1, page-level) = MRR after collapsing multiple chunks per URL into a single rank — neutralises chunk-density inflation. Page MRR ≥ MRR by construction; the gap measures how much chunk-density was inflating the chunk-level number. **Mode** = retrieval strategy used (see definitions above).

## Summary: embedding-only (hit rate at multiple K values)

_Computed over 499 queries on 9 common sites._

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Avg words |
|---|---|---|---|---|---|---|---|---|
| crawl4ai-raw | 68% (341/499) ±4% | 83% (412/499) ±3% | 88% (439/499) ±3% | 92% (460/499) ±2% | 95% (476/499) ±2% | 0.770 | 25245 | 344 |
| crawl4ai | 69% (342/499) ±4% | 82% (410/499) ±3% | 87% (434/499) ±3% | 91% (455/499) ±2% | 95% (472/499) ±2% | 0.768 | 24400 | 345 |
| playwright | 60% (301/499) ±4% | 74% (371/499) ±4% | 81% (402/499) ±3% | 87% (432/499) ±3% | 90% (451/499) ±3% | 0.694 | 56855 | 382 |
| crawlee | 59% (295/499) ±4% | 74% (367/499) ±4% | 78% (389/499) ±4% | 84% (418/499) ±3% | 86% (431/499) ±3% | 0.678 | 58912 | 382 |
| colly+md | 37% (183/499) ±4% | 44% (222/499) ±4% | 47% (235/499) ±4% | 51% (252/499) ±4% | 52% (261/499) ±4% | 0.414 | 59078 | 385 |
| markcrawl | 29% (144/499) ±4% | 38% (189/499) ±4% | 40% (202/499) ±4% | 43% (215/499) ±4% | 44% (221/499) ±4% | 0.341 | 27193 | 334 |
| scrapy+md | 16% (82/499) ±3% | 19% (95/499) ±3% | 19% (97/499) ±3% | 21% (104/499) ±4% | 22% (108/499) ±4% | 0.179 | 46141 | 364 |

> **Column definitions:** **Hit@K** = correct source page in top K results. **MRR** = Mean Reciprocal Rank (1/rank of correct result, averaged). **Chunks** = total chunks produced by this tool (across all pages in common sites). **Avg words** = mean words per chunk.

## What this means

Tools span MRR 0.179-0.770 on embedding mode (a 0.591 spread). Tools crawl similar pages from the same seed URLs, and we apply identical chunking and embedding pipelines, but extraction differences -- see [content quality](QUALITY_COMPARISON.md) -- show up at retrieval time.

**Retrieval mode matters more than crawler choice.** Embedding search beats BM25 by roughly 2x on MRR across all tools. Hybrid and reranked modes fall between the two. Choosing the right retrieval strategy will improve your RAG pipeline far more than switching crawlers.

**The noise-vs-recall trade-off.** Noisier tools (crawlee, playwright) have slightly higher hit rates, but they produce 2x the chunks of leaner tools (markcrawl, scrapy+md). More chunks means higher embedding and storage costs with diminishing retrieval returns. See [COST_AT_SCALE.md](COST_AT_SCALE.md) for the dollar impact.

**For most use cases, pick your crawler based on speed and cost, not retrieval quality.** The differences here are within confidence intervals. Where crawler choice _does_ matter is content quality and downstream answer quality -- see [ANSWER_QUALITY.md](ANSWER_QUALITY.md).

## huggingface-transformers

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 100% (4/4) | 100% (4/4) | 100% (4/4) | 100% (4/4) | 100% (4/4) | 1.000 | 4518 | 300 |
| crawlee | 100% (4/4) | 100% (4/4) | 100% (4/4) | 100% (4/4) | 100% (4/4) | 1.000 | 67 | 16 |
| playwright | 100% (4/4) | 100% (4/4) | 100% (4/4) | 100% (4/4) | 100% (4/4) | 1.000 | 356 | 300 |
| crawl4ai-raw | 75% (3/4) | 75% (3/4) | 100% (4/4) | 100% (4/4) | 100% (4/4) | 0.800 | 1018 | 295 |
| scrapy+md | 50% (2/4) | 75% (3/4) | 75% (3/4) | 75% (3/4) | 75% (3/4) | 0.583 | 6346 | 240 |
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
| markcrawl | #1 | huggingface.co/docs/transformers/v5.8.0/en/install | 0.744 | huggingface.co/docs/transformers/installation | 0.744 | huggingface.co/docs/transformers/v5.8.0/en/model_d | 0.691 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | #1 | huggingface.co/docs/transformers/installation | 0.790 | huggingface.co/docs/transformers/installation | 0.716 | huggingface.co/mistralai/Mistral-Small-4-119B-2603 | 0.703 |
| scrapy+md | #3 | huggingface.co/learn/llm-course/chapter0/1 | 0.699 | huggingface.co/learn/llm-course/chapter0/1 | 0.679 | huggingface.co/docs/tokenizers/python/latest/_sour | 0.641 |
| crawlee | #1 | huggingface.co/docs/transformers/installation | 0.844 | huggingface.co/docs/transformers/installation | 0.729 | huggingface.co/docs/transformers/installation | 0.648 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | huggingface.co/docs/transformers/installation | 0.844 | huggingface.co/docs/transformers/installation | 0.729 | huggingface.co/docs/transformers/quicktour | 0.657 |


**Q2: How can I set up Transformers for offline usage?**
*(expects URL containing: `installation`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | huggingface.co/docs/transformers/installation | 0.700 | huggingface.co/docs/transformers/v5.8.0/en/install | 0.700 | huggingface.co/docs/transformers/v5.8.0/en/model_d | 0.676 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | #5 | huggingface.co/unsloth/Qwen3.5-9B-GGUF | 0.654 | huggingface.co/mistralai/Mistral-Small-4-119B-2603 | 0.651 | huggingface.co/google/gemma-4-26B-A4B-it | 0.634 |
| scrapy+md | miss | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.656 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.655 | huggingface.co/learn/llm-course/chapter0/1 | 0.646 |
| crawlee | #1 | huggingface.co/docs/transformers/installation | 0.679 | huggingface.co/docs/transformers/quicktour | 0.644 | huggingface.co/docs/transformers/installation | 0.639 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | huggingface.co/docs/transformers/installation | 0.679 | huggingface.co/docs/transformers/quicktour | 0.640 | huggingface.co/docs/transformers/installation | 0.639 |


**Q3: What are the main design principles of Transformers?**
*(expects URL containing: `transformers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | huggingface.co/docs/transformers/main/en/index | 0.655 | huggingface.co/docs/transformers/index | 0.655 | huggingface.co/docs/transformers/v5.8.0/en/index | 0.655 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | #1 | huggingface.co/docs/transformers/index | 0.707 | huggingface.co/docs/transformers/index | 0.583 | huggingface.co/mistralai/Mistral-Small-4-119B-2603 | 0.551 |
| scrapy+md | #1 | huggingface.co/docs/transformers/index | 0.650 | huggingface.co/docs/transformers/philosophy | 0.599 | huggingface.co/docs/transformers/index | 0.592 |
| crawlee | #1 | huggingface.co/docs/transformers/index | 0.701 | huggingface.co/docs/transformers/quicktour | 0.582 | huggingface.co/docs/transformers/index | 0.581 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | huggingface.co/docs/transformers/index | 0.650 | huggingface.co/docs/transformers/quicktour | 0.572 | huggingface.co/docs/transformers/quicktour | 0.565 |


**Q4: What features does Transformers provide for inference or training?**
*(expects URL containing: `transformers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | huggingface.co/docs/transformers/v5.8.0/en/index | 0.757 | huggingface.co/docs/transformers/index | 0.757 | huggingface.co/docs/transformers/main/en/index | 0.757 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | #1 | huggingface.co/docs/transformers/index | 0.739 | huggingface.co/docs/transformers/index | 0.738 | huggingface.co/docs/transformers/index | 0.651 |
| scrapy+md | #1 | huggingface.co/docs/transformers/index | 0.754 | huggingface.co/docs/transformers/model_doc/bart | 0.691 | huggingface.co/docs/transformers/trainer | 0.690 |
| crawlee | #1 | huggingface.co/docs/transformers/index | 0.758 | huggingface.co/docs/transformers/index | 0.738 | huggingface.co/docs/transformers/quicktour | 0.716 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | huggingface.co/docs/transformers/index | 0.754 | huggingface.co/docs/transformers/quicktour | 0.702 | huggingface.co/docs/transformers/quicktour | 0.701 |


</details>

## ikea

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai-raw | 65% (39/60) | 85% (51/60) | 90% (54/60) | 93% (56/60) | 97% (58/60) | 0.762 | 1554 | 200 |
| crawl4ai | 65% (39/60) | 82% (49/60) | 83% (50/60) | 88% (53/60) | 93% (56/60) | 0.738 | 1622 | 200 |
| crawlee | 52% (31/60) | 60% (36/60) | 67% (40/60) | 72% (43/60) | 73% (44/60) | 0.580 | 4610 | 203 |
| playwright | 48% (29/60) | 58% (35/60) | 67% (40/60) | 70% (42/60) | 73% (44/60) | 0.555 | 3308 | 200 |
| colly+md | 28% (17/60) | 43% (26/60) | 45% (27/60) | 45% (27/60) | 48% (29/60) | 0.356 | 2942 | 200 |
| markcrawl | 23% (14/60) | 28% (17/60) | 30% (18/60) | 32% (19/60) | 33% (20/60) | 0.268 | 928 | 200 |
| scrapy+md | 12% (7/60) | 12% (7/60) | 12% (7/60) | 12% (7/60) | 12% (7/60) | 0.117 | 1107 | 194 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for ikea</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is the price of the NÄSINGE extendable table?**
*(expects URL containing: `furniture-fu001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #11 | www.ikea.com/us/en/customer-service/product-suppor | 0.681 | www.ikea.com/us/en/cat/outdoor-patio-furniture-od0 | 0.653 | www.ikea.com/us/en/cat/sundsoe-series-700601/ | 0.625 |
| crawl4ai | #5 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.786 | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.782 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.738 |
| crawl4ai-raw | #5 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.786 | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.753 | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.748 |
| scrapy+md | #25 | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.776 | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.754 | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.745 |
| crawlee | #33 | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.774 | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.744 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.733 |
| colly+md | miss | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.772 | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.771 | www.ikea.com/us/en/cat/extendable-tables-21829/ | 0.749 |
| playwright | #50 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.728 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.720 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.718 |


**Q2: What features does the STORKLINTA series offer?**
*(expects URL containing: `furniture-fu001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.651 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.648 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.623 |
| crawl4ai | #8 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.671 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.670 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.662 |
| crawl4ai-raw | #5 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.671 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.670 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.662 |
| scrapy+md | #1 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.625 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.623 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.609 |
| crawlee | #29 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.671 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.670 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.667 |
| colly+md | #5 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.684 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.671 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.670 |
| playwright | #3 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.671 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.669 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.655 |


**Q3: What is the height and diameter of the PÅDRAG vase?**
*(expects URL containing: `padrag-vase-clear-glass-10470991`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/pomp-vase-candle-holder-clear | 0.726 | www.ikea.com/us/en/p/stockholm-2025-vase-black-105 | 0.670 | www.ikea.com/us/en/cat/vases-bowls-10769/ | 0.666 |
| crawl4ai | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.829 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.731 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.721 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.788 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.749 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.721 |
| scrapy+md | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.829 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.721 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.668 |
| crawlee | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.829 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.733 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.731 |
| colly+md | miss | www.ikea.com/us/en/cat/outdoor-pots-plants-31787/ | 0.588 | www.ikea.com/us/en/customer-service/product-suppor | 0.559 | www.ikea.com/us/en/p/vittskaer-2-seat-section-for- | 0.558 |
| playwright | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.829 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.733 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.728 |


**Q4: Who is the designer of the PÅDRAG vase?**
*(expects URL containing: `padrag-vase-clear-glass-10470991`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/vases-bowls-10769/ | 0.627 | www.ikea.com/us/en/p/stockholm-2025-vase-black-105 | 0.601 | www.ikea.com/us/en/cat/vases-10776/ | 0.595 |
| crawl4ai | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.729 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.661 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.654 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.675 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.670 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.651 |
| scrapy+md | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.729 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.634 | www.ikea.com/us/en/p/skogstundra-vase-light-blue-0 | 0.587 |
| crawlee | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.729 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.668 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.665 |
| colly+md | miss | www.ikea.com/us/en/p/holmerud-side-table-dark-brow | 0.515 | www.ikea.com/us/en/customer-service/product-suppor | 0.515 | www.ikea.com/us/en/cat/outdoor-pots-plants-31787/ | 0.514 |
| playwright | #1 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.729 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.667 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.664 |


**Q5: What are the different types of ottomans available at IKEA?**
*(expects URL containing: `ottomans-20926`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.782 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.765 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.751 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.781 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.770 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.759 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.781 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.765 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.753 |
| scrapy+md | miss | www.ikea.com/us/en/cat/hemnes-bedroom-series-58619 | 0.676 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.671 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.669 |
| crawlee | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.794 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.783 | www.ikea.com/us/en/cat/products-products/ | 0.752 |
| colly+md | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.746 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.743 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.743 |
| playwright | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.794 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.783 | www.ikea.com/us/en/cat/products-products/ | 0.752 |


**Q6: What is the price of the FÖRLUNDA Pouffe?**
*(expects URL containing: `ottomans-20926`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #25 | www.ikea.com/us/en/p/stockholm-2025-glass-20592440 | 0.626 | www.ikea.com/us/en/cat/scented-candles-10783/ | 0.624 | www.ikea.com/us/en/p/dryck-blabaer-blueberry-syrup | 0.618 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.712 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.641 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.639 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.712 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.667 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.646 |
| scrapy+md | miss | www.ikea.com/us/en/cat/dining-chairs-25219/ | 0.627 | www.ikea.com/us/en/campaigns/ikea-binging-with-bab | 0.620 | www.ikea.com/us/en/cat/mugs-cups-16045/ | 0.618 |
| crawlee | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.672 | www.ikea.com/us/en/cat/themes-themes/ | 0.654 | www.ikea.com/us/en/cat/tables-chairs-fu002/ | 0.638 |
| colly+md | #1 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.694 | www.ikea.com/us/en/cat/sleeper-sofas-10663/ | 0.645 | www.ikea.com/us/en/cat/ottomans-20926/ | 0.639 |
| playwright | miss | www.ikea.com/us/en/cat/stockholm-collection-11989/ | 0.635 | www.ikea.com/us/en/cat/stockholm-collection-11989/ | 0.628 | www.ikea.com/us/en/cat/stockholm-collection-11989/ | 0.620 |


**Q7: How many points do IKEA Family members collect for every $1 spent?**
*(expects URL containing: `rewards`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.838 | www.ikea.com/us/en/customer-service/terms-conditio | 0.833 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.815 |
| crawl4ai | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.848 | www.ikea.com/us/en/p/naesinge-chair-white-tibbleby | 0.827 | www.ikea.com/us/en/ikea-family/benefits/ | 0.824 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.848 | www.ikea.com/us/en/p/perjohan-stool-with-storage-p | 0.830 | www.ikea.com/us/en/p/naesinge-chair-dark-brown-sta | 0.827 |
| scrapy+md | miss | www.ikea.com/us/en/customer-service/privacy-policy | 0.856 | www.ikea.com/us/en/ikea-family/?itm_campaign=assur | 0.841 | www.ikea.com/us/en/customer-service/services/assem | 0.834 |
| crawlee | #28 | www.ikea.com/us/en/cat/sleeper-sofas-10663/ | 0.834 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.834 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.834 |
| colly+md | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.825 | www.ikea.com/us/en/ikea-family/ | 0.808 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.759 |
| playwright | #28 | www.ikea.com/us/en/cat/chair-pads-20542/ | 0.834 | www.ikea.com/us/en/cat/sleeper-sofas-10663/ | 0.834 | www.ikea.com/us/en/circular/buy-back/ | 0.834 |


**Q8: What actions can earn you points in the IKEA Family rewards program?**
*(expects URL containing: `rewards`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.857 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.842 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.834 |
| crawl4ai | #3 | www.ikea.com/us/en/ikea-family/ | 0.833 | www.ikea.com/us/en/ikea-family/benefits/ | 0.833 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.833 |
| crawl4ai-raw | #2 | www.ikea.com/us/en/ikea-family/benefits/ | 0.833 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.833 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.830 |
| scrapy+md | miss | www.ikea.com/us/en/customer-service/ikea-family-te | 0.842 | www.ikea.com/us/en/ikea-family/?itm_campaign=assur | 0.826 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.814 |
| crawlee | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.826 | www.ikea.com/us/en/ikea-family/ | 0.795 | www.ikea.com/us/en/cat/cooktops-20812/ | 0.786 |
| colly+md | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.826 | www.ikea.com/us/en/ikea-family/ | 0.795 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.768 |
| playwright | #1 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.826 | www.ikea.com/us/en/ikea-family/ | 0.795 | www.ikea.com/us/en/cat/cabinet-knobs-handles-pulls | 0.786 |


**Q9: What is the current offer for IKEA Family members on points collection?**
*(expects URL containing: `offers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #21 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.849 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.846 | www.ikea.com/us/en/ikea-family/ | 0.841 |
| crawl4ai | #8 | www.ikea.com/us/en/ikea-family/ | 0.849 | www.ikea.com/us/en/ikea-family/benefits/ | 0.849 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.847 |
| crawl4ai-raw | #6 | www.ikea.com/us/en/ikea-family/benefits/ | 0.849 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.847 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.841 |
| scrapy+md | miss | www.ikea.com/us/en/ikea-family/?itm_campaign=assur | 0.861 | www.ikea.com/us/en/customer-service/privacy-policy | 0.847 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.846 |
| crawlee | miss | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.842 | www.ikea.com/us/en/cat/beds-bm003/ | 0.828 | www.ikea.com/us/en/cat/armchairs-chaises-fu006/ | 0.828 |
| colly+md | miss | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.842 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.831 | www.ikea.com/us/en/ikea-family/ | 0.807 |
| playwright | #4 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.842 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.828 | www.ikea.com/us/en/circular/buy-back/ | 0.828 |


**Q10: What discounts are available on sofas and sectionals?**
*(expects URL containing: `offers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | www.ikea.com/us/en/rooms/living-room/ | 0.813 | www.ikea.com/us/en/offers/ | 0.774 | www.ikea.com/us/en/ | 0.769 |
| crawl4ai | #2 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.771 | www.ikea.com/us/en/offers/ | 0.770 | www.ikea.com/us/en/offers/ | 0.766 |
| crawl4ai-raw | #2 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.771 | www.ikea.com/us/en/offers/ | 0.770 | www.ikea.com/us/en/offers/ | 0.766 |
| scrapy+md | miss | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.714 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.702 | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.699 |
| crawlee | #3 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.806 | www.ikea.com/us/en/cat/sleeper-sofas-10663/ | 0.797 | www.ikea.com/us/en/offers/ | 0.776 |
| colly+md | #1 | www.ikea.com/us/en/offers/ | 0.776 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.762 | www.ikea.com/us/en/rooms/living-room/ | 0.758 |
| playwright | #1 | www.ikea.com/us/en/offers/ | 0.776 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.769 | www.ikea.com/us/en/offers/family-offers/?filters=f | 0.759 |


**Q11: What warranty is offered for SEKTION kitchens?**
*(expects URL containing: `sektion-kitchen-ka005`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/customer-service/returns-claims | 0.691 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.618 | www.ikea.com/us/en/ikea-business/network/ | 0.611 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.779 | www.ikea.com/us/en/customer-service/returns-claims | 0.762 | www.ikea.com/us/en/customer-service/returns-claims | 0.684 |
| crawl4ai-raw | #2 | www.ikea.com/us/en/customer-service/returns-claims | 0.762 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.760 | www.ikea.com/us/en/customer-service/returns-claims | 0.684 |
| scrapy+md | miss | www.ikea.com/us/en/customer-service/terms-conditio | 0.617 | www.ikea.com/us/en/cat/bathroom-ba001/ | 0.609 | www.ikea.com/us/en/customer-service/ikea-for-busin | 0.599 |
| crawlee | #2 | www.ikea.com/us/en/customer-service/returns-claims | 0.784 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.741 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.704 |
| colly+md | #2 | www.ikea.com/us/en/customer-service/returns-claims | 0.784 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.714 | www.ikea.com/us/en/customer-service/returns-claims | 0.693 |
| playwright | #4 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.806 | www.ikea.com/us/en/customer-service/returns-claims | 0.784 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.760 |


**Q12: What types of products are included in the SEKTION kitchen system?**
*(expects URL containing: `sektion-kitchen-ka005`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/products-products/ | 0.636 | www.ikea.com/us/en/cat/choices-for-change-700575/ | 0.631 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.629 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.787 | www.ikea.com/us/en/cat/kitchen-cabinets-700292/ | 0.724 | www.ikea.com/us/en/cat/kitchens-ka003/ | 0.714 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.787 | www.ikea.com/us/en/cat/kitchens-ka003/ | 0.714 | www.ikea.com/us/en/rooms/kitchen/ | 0.709 |
| scrapy+md | miss | www.ikea.com/us/en/cat/cooking-accessories-15927/ | 0.657 | www.ikea.com/us/en/p/faergklar-baking-serving-dish | 0.640 | www.ikea.com/us/en/cat/patar-series-36839/ | 0.639 |
| crawlee | #1 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.837 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.769 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.714 |
| colly+md | #1 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.783 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.689 | www.ikea.com/us/en/cat/kitchen-cabinets-700292/ | 0.681 |
| playwright | #1 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.837 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.769 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.718 |


**Q13: What are the dimensions of the STORKLINTA 4-drawer dresser?**
*(expects URL containing: `storklinta-4-drawer-dresser-oak-effect-anchor-unlock-function-20559290`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.774 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.769 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.764 |
| crawl4ai | #2 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.813 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.810 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.800 |
| crawl4ai-raw | #3 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.813 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.811 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.810 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.795 | www.ikea.com/us/en/cat/patar-series-36839/ | 0.766 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.762 |
| crawlee | #5 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.830 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.814 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.799 |
| colly+md | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.812 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.799 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.795 |
| playwright | miss | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.778 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.768 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.766 |


**Q14: What safety feature does the STORKLINTA 4-drawer dresser include to reduce tip-over risk?**
*(expects URL containing: `storklinta-4-drawer-dresser-oak-effect-anchor-unlock-function-20559290`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.857 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.802 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.753 |
| crawl4ai | #2 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.802 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.802 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.801 |
| crawl4ai-raw | #2 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.802 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.802 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.801 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.713 | www.ikea.com/us/en/cat/patar-series-36839/ | 0.699 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.695 |
| crawlee | #5 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.823 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.806 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.805 |
| colly+md | miss | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.806 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.805 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.805 |
| playwright | miss | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.797 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.794 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.793 |


**Q15: What are some tips for organizing a dresser?**
*(expects URL containing: `5-tidy-tips-how-to-organize-a-dresser-pub64488700`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.863 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.819 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.795 |
| crawl4ai | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.834 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.777 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.776 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.834 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.777 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.776 |
| scrapy+md | miss | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.712 | www.ikea.com/us/en/cat/basket-drawer-units-46081/ | 0.710 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.698 |
| crawlee | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.796 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.792 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.783 |
| colly+md | miss | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.874 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.820 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.753 |
| playwright | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.874 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.792 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.773 |


**Q16: How can I use clothes boxes to keep items ordered in a dresser?**
*(expects URL containing: `5-tidy-tips-how-to-organize-a-dresser-pub64488700`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.820 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.807 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.796 |
| crawl4ai | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.803 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.774 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.769 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.803 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.774 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.769 |
| scrapy+md | miss | www.ikea.com/us/en/cat/basket-drawer-units-46081/ | 0.721 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.715 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.711 |
| crawlee | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.796 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.787 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.736 |
| colly+md | miss | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.834 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.755 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.749 |
| playwright | #1 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.834 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.755 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.736 |


**Q17: What are the dimensions of the DYTÅG curtains?**
*(expects URL containing: `dytag-curtains-1-pair-white-with-heading-tape-00466715`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/customer-service/product-suppor | 0.587 | www.ikea.com/us/en/p/daecksbat-led-wall-lamp-hardw | 0.568 | www.ikea.com/us/en/p/daecksbat-led-wall-lamp-hardw | 0.565 |
| crawl4ai | #1 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.782 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.769 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.763 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.782 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.778 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.769 |
| scrapy+md | miss | www.ikea.com/us/en/p/vinterfint-pre-cut-fabric-chr | 0.585 | www.ikea.com/us/en/p/turbokastanj-mirror-red-50566 | 0.582 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.571 |
| crawlee | #1 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.799 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.782 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.775 |
| colly+md | miss | www.ikea.com/us/en/cat/curtains-10700/ | 0.737 | www.ikea.com/us/en/cat/curtains-10700/ | 0.682 | www.ikea.com/us/en/cat/curtains-10700/ | 0.676 |
| playwright | miss | www.ikea.com/us/en/cat/curtains-10700/ | 0.741 | www.ikea.com/us/en/campaigns/shop-marketplace-pub0 | 0.689 | www.ikea.com/us/en/campaigns/shop-marketplace-pub0 | 0.681 |


**Q18: What material are the DYTÅG curtains made of?**
*(expects URL containing: `dytag-curtains-1-pair-white-with-heading-tape-00466715`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/customer-service/product-suppor | 0.561 | www.ikea.com/us/en/p/stockholm-mirror-walnut-venee | 0.558 | www.ikea.com/us/en/p/esseboda-bench-with-storage-k | 0.551 |
| crawl4ai | #1 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.770 | www.ikea.com/us/en/cat/curtains-10700/ | 0.760 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.759 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.770 | www.ikea.com/us/en/cat/curtains-10700/ | 0.761 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.761 |
| scrapy+md | miss | www.ikea.com/us/en/p/klippbraecka-pre-cut-fabric-w | 0.595 | www.ikea.com/us/en/p/turbokastanj-mirror-red-50566 | 0.579 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.572 |
| crawlee | #1 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.782 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.760 | www.ikea.com/us/en/p/dytag-curtains-1-pair-white-w | 0.758 |
| colly+md | miss | www.ikea.com/us/en/cat/curtains-10700/ | 0.715 | www.ikea.com/us/en/cat/curtains-10700/ | 0.654 | www.ikea.com/us/en/cat/curtains-10700/ | 0.652 |
| playwright | miss | www.ikea.com/us/en/cat/curtains-10700/ | 0.723 | www.ikea.com/us/en/campaigns/shop-marketplace-pub0 | 0.683 | www.ikea.com/us/en/campaigns/shop-marketplace-pub0 | 0.672 |


**Q19: What types of refrigerators does IKEA offer?**
*(expects URL containing: `fridges-freezers-20822`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/ideas/tips-for-more-sustainable | 0.666 | www.ikea.com/us/en/cat/products-products/ | 0.654 | www.ikea.com/us/en/customer-service/product-suppor | 0.643 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.760 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.745 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.744 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.760 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.751 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.750 |
| scrapy+md | miss | www.ikea.com/us/en/cat/cube-storage-55012/ | 0.638 | www.ikea.com/us/en/customer-service/shopping-at-ik | 0.637 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.631 |
| crawlee | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.817 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.760 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.732 |
| colly+md | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.746 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.740 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.731 |
| playwright | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.817 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.760 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.733 |


**Q20: How can I ensure my new fridge fits in my kitchen space?**
*(expects URL containing: `fridges-freezers-20822`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.692 | www.ikea.com/us/en/planners/ | 0.682 | www.ikea.com/us/en/cat/cookware-tableware-kt001/ | 0.661 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.824 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.761 | www.ikea.com/us/en/rooms/kitchen/ | 0.746 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.824 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.761 | www.ikea.com/us/en/rooms/kitchen/ | 0.746 |
| scrapy+md | miss | www.ikea.com/us/en/cat/ikea-365-food-storage-49524 | 0.703 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.692 | www.ikea.com/us/en/campaigns/ikea-binging-with-bab | 0.689 |
| crawlee | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.824 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.761 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.733 |
| colly+md | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.792 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.790 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.768 |
| playwright | #1 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.824 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.761 | www.ikea.com/us/en/cat/fridges-freezers-20822/ | 0.733 |


**Q21: What is the range of values for IKEA Gift Cards?**
*(expects URL containing: `gift-cards-pub3d1efe50`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.776 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.739 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.727 |
| crawl4ai | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.793 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.719 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.715 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.793 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.719 | www.ikea.com/us/en/customer-service/payment-option | 0.718 |
| scrapy+md | miss | www.ikea.com/us/en/customer-service/ikea-family-te | 0.726 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.726 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.705 |
| crawlee | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.739 | www.ikea.com/us/en/customer-service/faq/ | 0.724 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.709 |
| colly+md | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.739 | www.ikea.com/us/en/customer-service/faq/ | 0.724 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.700 |
| playwright | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.739 | www.ikea.com/us/en/customer-service/faq/ | 0.724 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.700 |


**Q22: How can I check the balance of my IKEA Gift Card?**
*(expects URL containing: `gift-cards-pub3d1efe50`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.788 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.782 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.756 |
| crawl4ai | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.873 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.800 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.793 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.873 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.800 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.793 |
| scrapy+md | miss | www.ikea.com/us/en/ikea-family/?itm_campaign=assur | 0.724 | www.ikea.com/us/en/p/faergklar-mug-matte-green-404 | 0.706 | www.ikea.com/us/en/customer-service/services/finan | 0.706 |
| crawlee | #1 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.827 | www.ikea.com/us/en/customer-service/faq/ | 0.811 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.756 |
| colly+md | #2 | www.ikea.com/us/en/customer-service/faq/ | 0.811 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.782 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.756 |
| playwright | #2 | www.ikea.com/us/en/customer-service/faq/ | 0.811 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.782 | www.ikea.com/us/en/customer-service/gift-cards-pub | 0.756 |


**Q23: What is the price of the SNIGLAR Crib?**
*(expects URL containing: `baby-kids-bc001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/customer-service/product-suppor | 0.626 | www.ikea.com/us/en/customer-service/product-suppor | 0.611 | www.ikea.com/us/en/customer-service/product-suppor | 0.598 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.739 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.682 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.649 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.739 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.682 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.649 |
| scrapy+md | miss | www.ikea.com/us/en/cat/play-tents-20484/ | 0.629 | www.ikea.com/us/en/rooms/childrens-room/ | 0.625 | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.624 |
| crawlee | miss | www.ikea.com/us/en/rooms/bedroom/ | 0.650 | www.ikea.com/us/en/rooms/bedroom/ | 0.644 | www.ikea.com/us/en/rooms/childrens-room/how-to/org | 0.642 |
| colly+md | miss | www.ikea.com/us/en/cat/sleeper-sofas-10663/ | 0.648 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.642 | www.ikea.com/us/en/cat/sleeper-sofas-10663/ | 0.637 |
| playwright | #1 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.737 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.722 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.664 |


**Q24: What materials are used in children's mattresses at IKEA?**
*(expects URL containing: `baby-kids-bc001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/customer-service/product-suppor | 0.707 | www.ikea.com/us/en/safety-at-home/ | 0.685 | www.ikea.com/us/en/cat/physical-play-18736/?filter | 0.682 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.756 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.748 | www.ikea.com/us/en/cat/beds-bm003/ | 0.730 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.756 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.748 | www.ikea.com/us/en/cat/beds-bm003/ | 0.745 |
| scrapy+md | miss | www.ikea.com/us/en/rooms/childrens-room/ | 0.736 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.731 | www.ikea.com/us/en/p/underhalla-cards-w-letters-nu | 0.730 |
| crawlee | miss | www.ikea.com/us/en/cat/kids-furniture-18767/ | 0.755 | www.ikea.com/us/en/ideas/ | 0.738 | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.731 |
| colly+md | miss | www.ikea.com/us/en/rooms/childrens-room/ | 0.752 | www.ikea.com/us/en/ideas/ | 0.738 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.737 |
| playwright | #1 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.812 | www.ikea.com/us/en/cat/kids-furniture-18767/ | 0.755 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.743 |


**Q25: What types of storage solutions are included in the BRIMNES series?**
*(expects URL containing: `brimnes-series-700496`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.664 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.650 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.637 |
| crawl4ai | #2 | www.ikea.com/us/en/p/brimnes-bookcase-black-403012 | 0.735 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.720 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.716 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.737 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.716 | www.ikea.com/us/en/p/brimnes-bookcase-black-403012 | 0.716 |
| scrapy+md | miss | www.ikea.com/us/en/cat/patar-series-36839/ | 0.641 | www.ikea.com/us/en/cat/sideboards-buffets-10412/ | 0.636 | www.ikea.com/us/en/p/omar-shelving-unit-with-3-bas | 0.621 |
| crawlee | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.762 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.704 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.672 |
| colly+md | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.679 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.672 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.668 |
| playwright | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.762 | www.ikea.com/us/en/cat/besta-storage-system-46053/ | 0.670 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.667 |


**Q26: How many items are available in the BRIMNES series?**
*(expects URL containing: `brimnes-series-700496`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.594 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.573 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.563 |
| crawl4ai | #2 | www.ikea.com/us/en/p/brimnes-bookcase-black-403012 | 0.686 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.685 | www.ikea.com/us/en/p/brimnes-bookcase-white-903012 | 0.668 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.675 | www.ikea.com/us/en/p/brimnes-bookcase-white-903012 | 0.668 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.660 |
| scrapy+md | miss | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.587 | www.ikea.com/us/en/cat/faergklar-series-57249/ | 0.556 | www.ikea.com/us/en/cat/godmiddag-series-62069/ | 0.554 |
| crawlee | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.749 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.655 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.635 |
| colly+md | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.667 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.654 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.646 |
| playwright | #1 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.749 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.618 | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.587 |


**Q27: What personal data do we collect from parents using Småland?**
*(expects URL containing: `ikea-smaland-privacy-notice-pubf7ed5e70`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.758 | www.ikea.com/us/en/customer-service/privacy-policy | 0.642 | www.ikea.com/us/en/customer-service/privacy-policy | 0.621 |
| crawl4ai | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.773 | www.ikea.com/us/en/customer-service/privacy-policy | 0.761 | www.ikea.com/us/en/customer-service/privacy-policy | 0.755 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.773 | www.ikea.com/us/en/customer-service/privacy-policy | 0.761 | www.ikea.com/us/en/customer-service/privacy-policy | 0.755 |
| scrapy+md | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.773 | www.ikea.com/us/en/customer-service/privacy-policy | 0.768 | www.ikea.com/us/en/customer-service/privacy-policy | 0.753 |
| crawlee | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.773 | www.ikea.com/us/en/customer-service/privacy-policy | 0.764 | www.ikea.com/us/en/customer-service/privacy-policy | 0.753 |
| colly+md | miss | www.ikea.com/us/en/customer-service/privacy-policy | 0.773 | www.ikea.com/us/en/customer-service/privacy-policy | 0.764 | www.ikea.com/us/en/customer-service/privacy-policy | 0.753 |
| playwright | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.773 | www.ikea.com/us/en/customer-service/privacy-policy | 0.764 | www.ikea.com/us/en/customer-service/privacy-policy | 0.753 |


**Q28: How long does IKEA retain personal data provided in connection with Småland?**
*(expects URL containing: `ikea-smaland-privacy-notice-pubf7ed5e70`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.798 | www.ikea.com/us/en/customer-service/ikea-for-busin | 0.765 | www.ikea.com/us/en/customer-service/privacy-policy | 0.757 |
| crawl4ai | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.836 | www.ikea.com/us/en/customer-service/privacy-policy | 0.793 | www.ikea.com/us/en/customer-service/privacy-policy | 0.780 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.836 | www.ikea.com/us/en/customer-service/privacy-policy | 0.793 | www.ikea.com/us/en/customer-service/privacy-policy | 0.780 |
| scrapy+md | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.847 | www.ikea.com/us/en/customer-service/privacy-policy | 0.820 | www.ikea.com/us/en/customer-service/privacy-policy | 0.796 |
| crawlee | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.837 | www.ikea.com/us/en/customer-service/privacy-policy | 0.820 | www.ikea.com/us/en/customer-service/privacy-policy | 0.796 |
| colly+md | miss | www.ikea.com/us/en/customer-service/privacy-policy | 0.837 | www.ikea.com/us/en/customer-service/privacy-policy | 0.820 | www.ikea.com/us/en/customer-service/privacy-policy | 0.796 |
| playwright | #1 | www.ikea.com/us/en/customer-service/privacy-policy | 0.837 | www.ikea.com/us/en/customer-service/privacy-policy | 0.820 | www.ikea.com/us/en/customer-service/privacy-policy | 0.796 |


**Q29: What discounts do IKEA Family members receive?**
*(expects URL containing: `family-offers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/customer-service/ikea-family-te | 0.808 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.804 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.802 |
| crawl4ai | #2 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.805 | www.ikea.com/us/en/offers/family-offers/ | 0.805 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.803 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/offers/family-offers/ | 0.807 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.805 | www.ikea.com/us/en/offers/family-offers/?filters=f | 0.805 |
| scrapy+md | miss | www.ikea.com/us/en/customer-service/ikea-family-te | 0.805 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.803 | www.ikea.com/us/en/customer-service/ikea-family-te | 0.801 |
| crawlee | miss | www.ikea.com/us/en/ikea-family/ | 0.790 | www.ikea.com/us/en/ikea-business/network/  | 0.785 | www.ikea.com/us/en/ikea-family/ | 0.777 |
| colly+md | miss | www.ikea.com/us/en/ikea-family/ | 0.790 | www.ikea.com/us/en/ikea-business/network/ | 0.785 | www.ikea.com/us/en/ikea-family/ | 0.777 |
| playwright | #1 | www.ikea.com/us/en/offers/family-offers/ | 0.810 | www.ikea.com/us/en/offers/family-offers/?filters=f | 0.810 | www.ikea.com/us/en/offers/family-offers/?filters=f | 0.810 |


**Q30: How many points do IKEA Family members collect for every dollar spent?**
*(expects URL containing: `family-offers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.860 | www.ikea.com/us/en/customer-service/terms-conditio | 0.841 | www.ikea.com/us/en/ikea-family/ | 0.827 |
| crawl4ai | #20 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.857 | www.ikea.com/us/en/ikea-family/benefits/ | 0.841 | www.ikea.com/us/en/ikea-family/ | 0.841 |
| crawl4ai-raw | #16 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.857 | www.ikea.com/us/en/ikea-family/benefits/ | 0.841 | www.ikea.com/us/en/p/perjohan-stool-with-storage-p | 0.838 |
| scrapy+md | miss | www.ikea.com/us/en/customer-service/privacy-policy | 0.856 | www.ikea.com/us/en/ikea-family/?itm_campaign=assur | 0.849 | www.ikea.com/us/en/customer-service/services/assem | 0.837 |
| crawlee | miss | www.ikea.com/us/en/cat/ottomans-20926/ | 0.834 | www.ikea.com/us/en/customer-service/services/finan | 0.834 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.834 |
| colly+md | miss | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.829 | www.ikea.com/us/en/ikea-family/ | 0.811 | www.ikea.com/us/en/ikea-family/benefits/rewards/ | 0.772 |
| playwright | #17 | www.ikea.com/us/en/campaigns/ikea-mothers-day-pubb | 0.834 | www.ikea.com/us/en/cat/ovens-20810/ | 0.834 | www.ikea.com/us/en/cat/desk-lamps-20502/ | 0.834 |


**Q31: What is the price of the STORKLINTA 6-drawer dresser?**
*(expects URL containing: `storklinta-series-700569`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.790 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.779 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.765 |
| crawl4ai | #14 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.821 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.812 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.812 |
| crawl4ai-raw | #5 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.813 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.812 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.811 |
| scrapy+md | miss | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.799 | www.ikea.com/us/en/cat/patar-series-36839/ | 0.799 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.796 |
| crawlee | #1 | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.832 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.827 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.811 |
| colly+md | #15 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.811 | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.799 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.796 |
| playwright | #10 | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.799 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.787 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.783 |


**Q32: What safety feature does the STORKLINTA chest of drawers have?**
*(expects URL containing: `storklinta-series-700569`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.874 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.802 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.801 |
| crawl4ai | #26 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.874 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.869 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.869 |
| crawl4ai-raw | #34 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.874 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.869 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.869 |
| scrapy+md | miss | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.756 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.754 | www.ikea.com/us/en/cat/patar-series-36839/ | 0.749 |
| crawlee | #22 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.886 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.874 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.872 |
| colly+md | #12 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.874 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.872 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.869 |
| playwright | #3 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.869 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.860 | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.859 |


**Q33: What types of outdoor products are available at IKEA?**
*(expects URL containing: `outdoor-od001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.823 | www.ikea.com/us/en/rooms/outdoor/ | 0.815 | www.ikea.com/us/en/cat/outdoor-accessories-34203/ | 0.809 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.803 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.787 | www.ikea.com/us/en/cat/products-products/ | 0.777 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.803 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.787 | www.ikea.com/us/en/cat/products-products/ | 0.777 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.720 | www.ikea.com/us/en/customer-service/shopping-at-ik | 0.690 | www.ikea.com/us/en/p/kragsta-nesting-tables-set-of | 0.688 |
| crawlee | miss | www.ikea.com/us/en/cat/products-products/ | 0.817 | www.ikea.com/us/en/cat/products-products/ | 0.747 | www.ikea.com/us/en/p/sundsoe-folding-chair-bright- | 0.741 |
| colly+md | #3 | www.ikea.com/us/en/cat/outdoor-accessories-34203/ | 0.805 | www.ikea.com/us/en/rooms/outdoor/ | 0.805 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.803 |
| playwright | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.852 | www.ikea.com/us/en/cat/products-products/ | 0.818 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.803 |


**Q34: What is the price of the HAVSTEN Loveseat, outdoor?**
*(expects URL containing: `outdoor-od001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #8 | www.ikea.com/us/en/cat/outdoor-patio-lounge-chairs | 0.734 | www.ikea.com/us/en/cat/outdoor-patio-lounge-chairs | 0.729 | www.ikea.com/us/en/cat/outdoor-patio-lounge-chairs | 0.722 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.773 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.724 | www.ikea.com/us/en/cat/armchairs-chaises-fu006/ | 0.707 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.773 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.724 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.705 |
| scrapy+md | miss | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.699 | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.693 | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.687 |
| crawlee | miss | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.735 | www.ikea.com/us/en/p/vittskaer-armchair-plastic-ra | 0.698 | www.ikea.com/us/en/rooms/living-room/ | 0.694 |
| colly+md | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.784 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.775 | www.ikea.com/us/en/cat/outdoor-patio-furniture-od0 | 0.746 |
| playwright | #1 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.784 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.775 | www.ikea.com/us/en/cat/outdoor-od001/ | 0.712 |


**Q35: What are some themes available at IKEA?**
*(expects URL containing: `themes-themes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/rooms/ | 0.780 | www.ikea.com/us/en/cat/products-products/ | 0.762 | www.ikea.com/us/en/cat/home-decor-de001/ | 0.760 |
| crawl4ai | miss | www.ikea.com/us/en/ideas/ | 0.764 | www.ikea.com/us/en/ideas/ | 0.756 | www.ikea.com/us/en/p/knarrevik-nightstand-black-20 | 0.753 |
| crawl4ai-raw | miss | www.ikea.com/us/en/ideas/ | 0.756 | www.ikea.com/us/en/ideas/ | 0.754 | www.ikea.com/us/en/p/knarrevik-nightstand-black-20 | 0.753 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.735 | www.ikea.com/us/en/customer-service/shopping-at-ik | 0.729 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.723 |
| crawlee | #31 | www.ikea.com/us/en/cat/home-decor-de001/ | 0.830 | www.ikea.com/us/en/cat/wall-decor-10757/ | 0.826 | www.ikea.com/us/en/cat/products-products/ | 0.818 |
| colly+md | #2 | www.ikea.com/us/en/cat/home-decor-de001/ | 0.792 | www.ikea.com/us/en/cat/themes-themes/ | 0.773 | www.ikea.com/us/en/cat/wall-decor-10757/ | 0.770 |
| playwright | #1 | www.ikea.com/us/en/cat/themes-themes/ | 0.940 | www.ikea.com/us/en/cat/home-decor-de001/ | 0.830 | www.ikea.com/us/en/cat/wall-decor-10757/ | 0.826 |


**Q36: What materials does IKEA prefer for their products?**
*(expects URL containing: `themes-themes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.729 | www.ikea.com/us/en/cat/products-products/ | 0.721 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.698 |
| crawl4ai | #3 | www.ikea.com/us/en/cat/furniture-fu001/?page=2 | 0.755 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.755 | www.ikea.com/us/en/cat/themes-themes/ | 0.736 |
| crawl4ai-raw | #2 | www.ikea.com/us/en/cat/furniture-fu001/?page=2 | 0.755 | www.ikea.com/us/en/cat/themes-themes/ | 0.736 | www.ikea.com/us/en/p/kleppstad-wardrobe-with-slidi | 0.735 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.754 | www.ikea.com/us/en/p/glattis-tray-brass-color-7035 | 0.716 | www.ikea.com/us/en/p/omar-bottle-shelving-unit-s49 | 0.704 |
| crawlee | #5 | www.ikea.com/us/en/cat/products-products/ | 0.790 | www.ikea.com/us/en/favorites/ | 0.767 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.754 |
| colly+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.754 | www.ikea.com/us/en/p/kleppstad-wardrobe-with-slidi | 0.744 | www.ikea.com/us/en/p/smagoera-shelf-unit-white-604 | 0.742 |
| playwright | #7 | www.ikea.com/us/en/cat/products-products/ | 0.790 | www.ikea.com/us/en/favorites/ | 0.767 | www.ikea.com/us/en/shoppingcart/ | 0.754 |


**Q37: What are the dimensions of the STORKLINTA 3-drawer dresser?**
*(expects URL containing: `storklinta-3-drawer-dresser-gray-green-anchor-unlock-function-80574645`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.800 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.794 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.762 |
| crawl4ai | #1 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.808 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.806 | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.805 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.808 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.806 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.795 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.784 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.773 | www.ikea.com/us/en/cat/patar-series-36839/ | 0.772 |
| crawlee | #7 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.825 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.824 | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.800 |
| colly+md | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.803 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-w | 0.790 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.788 |
| playwright | miss | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.778 | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.773 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.770 |


**Q38: What safety feature does the STORKLINTA 3-drawer dresser include?**
*(expects URL containing: `storklinta-3-drawer-dresser-gray-green-anchor-unlock-function-80574645`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.816 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.813 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.807 |
| crawl4ai | #1 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.813 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.809 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.807 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.813 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.809 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.807 |
| scrapy+md | miss | www.ikea.com/us/en/cat/patar-series-36839/ | 0.753 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.744 | www.ikea.com/us/en/cat/patar-series-36839/ | 0.737 |
| crawlee | #2 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.830 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.813 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.809 |
| colly+md | miss | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.836 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.813 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.809 |
| playwright | miss | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.809 | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.803 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.795 |


**Q39: What is the price of the GLADELIG plate in gray?**
*(expects URL containing: `gladelig-plate-gray-10600756`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/serveware-16043/?filters=f- | 0.656 | www.ikea.com/us/en/cat/serveware-16043/?filters=f- | 0.645 | www.ikea.com/us/en/cat/serveware-16043/?filters=f- | 0.635 |
| crawl4ai | #1 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.725 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.720 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.708 |
| crawl4ai-raw | #2 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.720 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.705 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.694 |
| scrapy+md | miss | www.ikea.com/us/en/cat/serving-bowls-20619/ | 0.660 | www.ikea.com/us/en/cat/dinnerware-sets-31781/ | 0.651 | www.ikea.com/us/en/cat/dinnerware-sets-31781/ | 0.647 |
| crawlee | #1 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.754 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.754 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.738 |
| colly+md | miss | www.ikea.com/us/en/rooms/kitchen/ | 0.669 | www.ikea.com/us/en/cat/stockholm-collection-11989/ | 0.651 | www.ikea.com/us/en/cat/nightstands-20656/ | 0.639 |
| playwright | miss | www.ikea.com/us/en/rooms/kitchen/ | 0.669 | www.ikea.com/us/en/cat/stockholm-collection-11989/ | 0.651 | www.ikea.com/us/en/rooms/bedroom/how-to/teenage-be | 0.636 |


**Q40: What materials is the GLADELIG plate made of?**
*(expects URL containing: `gladelig-plate-gray-10600756`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/serveware-16043/?filters=f- | 0.649 | www.ikea.com/us/en/cat/serveware-16043/?filters=f- | 0.626 | www.ikea.com/us/en/cat/cookware-tableware-kt001/ | 0.607 |
| crawl4ai | #1 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.727 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.677 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.668 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.679 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.670 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.669 |
| scrapy+md | miss | www.ikea.com/us/en/campaigns/ikea-binging-with-bab | 0.627 | www.ikea.com/us/en/campaigns/ikea-binging-with-bab | 0.615 | www.ikea.com/us/en/cat/dinnerware-sets-31781/ | 0.593 |
| crawlee | #1 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.697 | www.ikea.com/us/en/p/gladelig-plate-gray-10600756/ | 0.696 | www.ikea.com/us/en/p/gladelig-deep-plate-bowl-dark | 0.693 |
| colly+md | miss | www.ikea.com/us/en/p/smagoera-shelf-unit-white-604 | 0.570 | www.ikea.com/us/en/cat/nightstands-20656/ | 0.563 | www.ikea.com/us/en/p/kleppstad-wardrobe-with-slidi | 0.561 |
| playwright | miss | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.567 | www.ikea.com/us/en/cat/cookware-tableware-kt001/ | 0.564 | www.ikea.com/us/en/p/lack-wall-shelf-unit-black-br | 0.560 |


**Q41: What are the dimensions of the LOHALS rug?**
*(expects URL containing: `lohals-rug-flatwoven-natural-00277395`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/rugs-10653/ | 0.676 | www.ikea.com/us/en/cat/rugs-10653/ | 0.666 | www.ikea.com/us/en/cat/rugs-10653/ | 0.657 |
| crawl4ai | #1 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.743 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.716 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.707 |
| crawl4ai-raw | #2 | www.ikea.com/us/en/cat/rugs-10653/ | 0.756 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.743 | www.ikea.com/us/en/cat/rugs-10653/ | 0.720 |
| scrapy+md | miss | www.ikea.com/us/en/cat/place-mats-coasters-20539/ | 0.583 | www.ikea.com/us/en/cat/place-mats-coasters-20539/f | 0.571 | www.ikea.com/us/en/customer-service/returns-claims | 0.566 |
| crawlee | #1 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.767 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.743 | www.ikea.com/us/en/cat/rugs-10653/ | 0.710 |
| colly+md | miss | www.ikea.com/us/en/cat/rugs-10653/ | 0.702 | www.ikea.com/us/en/cat/rugs-10653/ | 0.674 | www.ikea.com/us/en/cat/rugs-10653/ | 0.671 |
| playwright | #1 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.761 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.743 | www.ikea.com/us/en/campaigns/dream-lineup-pub85251 | 0.709 |


**Q42: What material is the LOHALS rug made from?**
*(expects URL containing: `lohals-rug-flatwoven-natural-00277395`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/rugs-10653/ | 0.681 | www.ikea.com/us/en/cat/rugs-10653/ | 0.674 | www.ikea.com/us/en/cat/rugs-10653/ | 0.666 |
| crawl4ai | #1 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.739 | www.ikea.com/us/en/cat/rugs-10653/ | 0.715 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.689 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.734 | www.ikea.com/us/en/cat/rugs-10653/ | 0.722 | www.ikea.com/us/en/cat/rugs-10653/ | 0.720 |
| scrapy+md | miss | www.ikea.com/us/en/cat/place-mats-coasters-20539/ | 0.585 | www.ikea.com/us/en/cat/place-mats-coasters-20539/f | 0.576 | www.ikea.com/us/en/p/stamsill-coaster-water-hyacin | 0.576 |
| crawlee | #1 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.740 | www.ikea.com/us/en/ | 0.688 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.680 |
| colly+md | miss | www.ikea.com/us/en/cat/rugs-10653/ | 0.661 | www.ikea.com/us/en/cat/rugs-10653/ | 0.657 | www.ikea.com/us/en/cat/rugs-10653/ | 0.644 |
| playwright | #1 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.735 | www.ikea.com/us/en/campaigns/dream-lineup-pub85251 | 0.717 | www.ikea.com/us/en/p/lohals-rug-flatwoven-natural- | 0.663 |


**Q43: What types of kitchen systems does IKEA offer?**
*(expects URL containing: `kitchen-appliances-ka001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/products-products/ | 0.730 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.705 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.691 |
| crawl4ai | #2 | www.ikea.com/us/en/rooms/kitchen/ | 0.766 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.754 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.747 |
| crawl4ai-raw | #2 | www.ikea.com/us/en/rooms/kitchen/ | 0.766 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.754 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.746 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.696 | www.ikea.com/us/en/cat/dishwashers-20825/ | 0.683 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.675 |
| crawlee | miss | www.ikea.com/us/en/cat/kitchens-ka003/ | 0.873 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.785 | www.ikea.com/us/en/cat/kitchen-cabinets-700292/ | 0.779 |
| colly+md | miss | www.ikea.com/us/en/rooms/kitchen/ | 0.754 | www.ikea.com/us/en/rooms/kitchen/ | 0.734 | www.ikea.com/us/en/cat/cooktops-20812/ | 0.723 |
| playwright | #2 | www.ikea.com/us/en/cat/kitchens-ka003/ | 0.873 | www.ikea.com/us/en/cat/kitchen-appliances-ka001/ | 0.796 | www.ikea.com/us/en/cat/sektion-kitchen-ka005/ | 0.785 |


**Q44: How can I book an appointment with a kitchen expert at IKEA?**
*(expects URL containing: `kitchen-appliances-ka001`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/planners/ | 0.718 | www.ikea.com/us/en/planners/ | 0.713 | www.ikea.com/us/en/customer-service/ | 0.708 |
| crawl4ai | #18 | www.ikea.com/us/en/customer-service/faq/ | 0.783 | www.ikea.com/us/en/customer-service/faq/ | 0.731 | www.ikea.com/us/en/planners/ | 0.724 |
| crawl4ai-raw | #18 | www.ikea.com/us/en/customer-service/faq/ | 0.783 | www.ikea.com/us/en/customer-service/faq/ | 0.731 | www.ikea.com/us/en/planners/ | 0.724 |
| scrapy+md | miss | www.ikea.com/us/en/customer-service/contact-us/ | 0.696 | www.ikea.com/us/en/customer-service/shopping-at-ik | 0.690 | www.ikea.com/us/en/customer-service/shopping-at-ik | 0.690 |
| crawlee | miss | www.ikea.com/us/en/customer-service/faq/ | 0.820 | www.ikea.com/us/en/planners/ | 0.756 | www.ikea.com/us/en/planners/?itm_campaign=assuranc | 0.756 |
| colly+md | miss | www.ikea.com/us/en/customer-service/faq/ | 0.820 | www.ikea.com/us/en/planners/ | 0.756 | www.ikea.com/us/en/planners/?itm/campaign=assuranc | 0.756 |
| playwright | #20 | www.ikea.com/us/en/customer-service/faq/ | 0.820 | www.ikea.com/us/en/customer-service/services/inter | 0.765 | www.ikea.com/us/en/planners/ | 0.756 |


**Q45: What is the starting cost for IKEA's delivery service?**
*(expects URL containing: `services`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | www.ikea.com/us/en/campaigns/dream-lineup-pub85251 | 0.820 | www.ikea.com/us/en/customer-service/services/deliv | 0.812 | www.ikea.com/us/en/customer-service/services/deliv | 0.798 |
| crawl4ai | #1 | www.ikea.com/us/en/customer-service/services/deliv | 0.809 | www.ikea.com/us/en/customer-service/services/deliv | 0.785 | www.ikea.com/us/en/customer-service/services/deliv | 0.782 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/customer-service/services/deliv | 0.809 | www.ikea.com/us/en/customer-service/services/deliv | 0.785 | www.ikea.com/us/en/customer-service/services/deliv | 0.781 |
| scrapy+md | #1 | www.ikea.com/us/en/customer-service/services/deliv | 0.805 | www.ikea.com/us/en/customer-service/services/deliv | 0.805 | www.ikea.com/us/en/customer-service/services/deliv | 0.800 |
| crawlee | #1 | www.ikea.com/us/en/customer-service/services/deliv | 0.803 | www.ikea.com/us/en/customer-service/services/deliv | 0.800 | www.ikea.com/us/en/customer-service/services/deliv | 0.784 |
| colly+md | #1 | www.ikea.com/us/en/customer-service/services/deliv | 0.805 | www.ikea.com/us/en/customer-service/services/deliv | 0.803 | www.ikea.com/us/en/customer-service/services/deliv | 0.800 |
| playwright | #1 | www.ikea.com/us/en/customer-service/services/deliv | 0.803 | www.ikea.com/us/en/customer-service/services/deliv | 0.803 | www.ikea.com/us/en/customer-service/services/deliv | 0.800 |


**Q46: Does IKEA offer assembly service for their products?**
*(expects URL containing: `services`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/customer-service/services/ | 0.782 | www.ikea.com/us/en/customer-service/ | 0.744 | www.ikea.com/us/en/customer-service/faq/ | 0.732 |
| crawl4ai | #1 | www.ikea.com/us/en/customer-service/services/ | 0.798 | www.ikea.com/us/en/customer-service/services/assem | 0.775 | www.ikea.com/us/en/customer-service/faq/ | 0.769 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/customer-service/services/ | 0.798 | www.ikea.com/us/en/customer-service/services/assem | 0.775 | www.ikea.com/us/en/customer-service/services/assem | 0.769 |
| scrapy+md | #1 | www.ikea.com/us/en/customer-service/services/assem | 0.773 | www.ikea.com/us/en/customer-service/contact-us/ | 0.738 | www.ikea.com/us/en/customer-service/services/assem | 0.737 |
| crawlee | #2 | www.ikea.com/us/en/customer-service/faq/ | 0.796 | www.ikea.com/us/en/customer-service/services/assem | 0.794 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-w | 0.794 |
| colly+md | #2 | www.ikea.com/us/en/customer-service/faq/ | 0.796 | www.ikea.com/us/en/customer-service/services/assem | 0.794 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-w | 0.794 |
| playwright | #2 | www.ikea.com/us/en/customer-service/faq/ | 0.796 | www.ikea.com/us/en/customer-service/services/assem | 0.794 | www.ikea.com/us/en/customer-service/services/ | 0.786 |


**Q47: What is one way to extend your countertop in a small kitchen?**
*(expects URL containing: `maximising-kitchen-space-for-more-room-to-cook-pub969bcf40`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/cabinet-knobs-handles-pulls | 0.635 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.630 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.620 |
| crawl4ai | #1 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.750 | www.ikea.com/us/en/rooms/kitchen/ | 0.665 | www.ikea.com/us/en/rooms/kitchen/ | 0.665 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.750 | www.ikea.com/us/en/rooms/kitchen/ | 0.665 | www.ikea.com/us/en/rooms/kitchen/ | 0.665 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.620 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.606 | www.ikea.com/us/en/cat/wall-shelves-10398/ | 0.603 |
| crawlee | #8 | www.ikea.com/us/en/rooms/kitchen/ | 0.671 | www.ikea.com/us/en/cat/kitchen-countertops-24264/ | 0.670 | www.ikea.com/us/en/cat/kitchen-countertops-24264/ | 0.654 |
| colly+md | miss | www.ikea.com/us/en/rooms/kitchen/ | 0.671 | www.ikea.com/us/en/cat/kitchen-countertops-24264/ | 0.667 | www.ikea.com/us/en/cat/kitchen-countertops-24264/ | 0.650 |
| playwright | #5 | www.ikea.com/us/en/rooms/kitchen/ | 0.671 | www.ikea.com/us/en/cat/home-improvement-hi001/ | 0.658 | www.ikea.com/us/en/cat/kitchen-countertops-24264/ | 0.650 |


**Q48: How can you add more storage under your wall cabinets?**
*(expects URL containing: `maximising-kitchen-space-for-more-room-to-cook-pub969bcf40`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.676 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.658 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.645 |
| crawl4ai | #1 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.708 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.694 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.672 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.708 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.694 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.672 |
| scrapy+md | miss | www.ikea.com/us/en/cat/wall-shelves-10398/ | 0.675 | www.ikea.com/us/en/cat/wall-shelves-10398/ | 0.671 | www.ikea.com/us/en/cat/sideboards-buffets-10412/ | 0.638 |
| crawlee | #5 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.698 | www.ikea.com/us/en/rooms/kitchen/ | 0.664 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.664 |
| colly+md | miss | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.701 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.700 | www.ikea.com/us/en/cat/storage-cabinets-10385/ | 0.667 |
| playwright | #1 | www.ikea.com/us/en/rooms/kitchen/how-to/maximising | 0.701 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.684 | www.ikea.com/us/en/cat/home-improvement-hi001/ | 0.673 |


**Q49: What are the dimensions of the BRIMNES 3-drawer dresser?**
*(expects URL containing: `brimnes-3-drawer-dresser-black-20574243`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.678 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.674 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.670 |
| crawl4ai | miss | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.739 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.725 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.722 |
| crawl4ai-raw | #2 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-gray | 0.828 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.821 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.818 |
| scrapy+md | miss | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.673 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.673 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.667 |
| crawlee | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.720 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.716 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.685 |
| colly+md | #2 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.819 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.819 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-gray | 0.798 |
| playwright | miss | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.685 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.685 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.665 |


**Q50: What is the price of the BRIMNES 3-drawer dresser?**
*(expects URL containing: `brimnes-3-drawer-dresser-black-20574243`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.702 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.702 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.674 |
| crawl4ai | miss | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.773 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.751 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.749 |
| crawl4ai-raw | #2 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.793 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.778 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-gray | 0.775 |
| scrapy+md | miss | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.716 | www.ikea.com/us/en/cat/patar-series-36839/ | 0.709 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.706 |
| crawlee | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.762 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.749 | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.727 |
| colly+md | #1 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.815 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.813 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.808 |
| playwright | miss | www.ikea.com/us/en/ | 0.691 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.691 | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.682 |


**Q51: What types of storage solutions are available for hallways?**
*(expects URL containing: `hallway`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.749 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.728 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.715 |
| crawl4ai | #1 | www.ikea.com/us/en/rooms/hallway/ | 0.750 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.737 | www.ikea.com/us/en/rooms/hallway/ | 0.731 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/rooms/hallway/ | 0.750 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.737 | www.ikea.com/us/en/rooms/hallway/ | 0.731 |
| scrapy+md | miss | www.ikea.com/us/en/cat/cube-storage-55012/ | 0.698 | www.ikea.com/us/en/p/omar-shelving-unit-with-3-bas | 0.685 | www.ikea.com/us/en/p/omar-shelf-unit-galvanized-00 | 0.671 |
| crawlee | #2 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.752 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.751 | www.ikea.com/us/en/cat/brimnes-series-700496/ | 0.740 |
| colly+md | #3 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.752 | www.ikea.com/us/en/cat/storage-cabinets-10385/ | 0.744 | www.ikea.com/us/en/rooms/hallway/ | 0.733 |
| playwright | #2 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.752 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.751 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.736 |


**Q52: How can I create a welcoming entryway with smart storage?**
*(expects URL containing: `hallway`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.703 | www.ikea.com/us/en/rooms/hallway/how-to/family-hal | 0.702 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.691 |
| crawl4ai | #1 | www.ikea.com/us/en/rooms/hallway/ | 0.718 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.708 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.703 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/rooms/hallway/ | 0.718 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.708 | www.ikea.com/us/en/cat/display-storage-cabinets-st | 0.703 |
| scrapy+md | miss | www.ikea.com/us/en/cat/patar-series-36839/ | 0.717 | www.ikea.com/us/en/cat/patar-series-36839/ | 0.672 | www.ikea.com/us/en/customer-service/shopping-at-ik | 0.669 |
| crawlee | #1 | www.ikea.com/us/en/rooms/hallway/ | 0.712 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.710 | www.ikea.com/us/en/p/pax-storklinta-wardrobe-combi | 0.709 |
| colly+md | #3 | www.ikea.com/us/en/cat/storage-solution-systems-46 | 0.729 | www.ikea.com/us/en/cat/sideboards-buffets-sofa-tab | 0.715 | www.ikea.com/us/en/rooms/hallway/ | 0.714 |
| playwright | #1 | www.ikea.com/us/en/rooms/hallway/ | 0.714 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.710 | www.ikea.com/us/en/cat/besta-storage-system-46053/ | 0.708 |


**Q53: What is the price of the GÅTEBO microwave oven?**
*(expects URL containing: `microwave-ovens-microwave-combo-ovens-20815`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/serveware-16043/?filters=f- | 0.577 | www.ikea.com/us/en/cat/batskaer-series-700500/ | 0.559 | www.ikea.com/us/en/p/stockholm-2025-tealight-holde | 0.558 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.766 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.751 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.693 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.751 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.750 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.705 |
| scrapy+md | miss | www.ikea.com/us/en/cat/upplaga-series-45243/ | 0.603 | www.ikea.com/us/en/cat/hoestagille-collection-7005 | 0.600 | www.ikea.com/us/en/cat/serving-bowls-20619/ | 0.597 |
| crawlee | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.817 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.722 | www.ikea.com/us/en/cat/ovens-20810/ | 0.661 |
| colly+md | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.735 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.710 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.651 |
| playwright | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.773 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.755 | www.ikea.com/us/en/cat/ovens-20810/ | 0.661 |


**Q54: What are the differences between microwave ovens and microwave oven combos?**
*(expects URL containing: `microwave-ovens-microwave-combo-ovens-20815`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.523 | www.ikea.com/us/en/cat/cabinet-knobs-handles-pulls | 0.504 | www.ikea.com/us/en/cat/batskaer-series-700500/ | 0.502 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.799 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.651 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.622 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.744 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.645 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.641 |
| scrapy+md | miss | www.ikea.com/us/en/cat/cooking-accessories-15927/ | 0.535 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.523 | www.ikea.com/us/en/p/faergklar-baking-serving-dish | 0.516 |
| crawlee | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.766 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.729 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.722 |
| colly+md | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.799 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.711 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.667 |
| playwright | #1 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.766 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.724 | www.ikea.com/us/en/cat/microwave-ovens-microwave-c | 0.722 |


**Q55: What are the dimensions of the STORKLINTA 6-drawer dresser?**
*(expects URL containing: `storklinta-6-drawer-dresser-dark-brown-oak-effect-anchor-unlock-function-70559278`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.777 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.760 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.756 |
| crawl4ai | #3 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.810 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.808 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.804 |
| crawl4ai-raw | #3 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.810 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.808 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.804 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.779 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.779 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.757 |
| crawlee | #8 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.816 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.804 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.801 |
| colly+md | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.797 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.787 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.785 |
| playwright | #4 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.787 | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.779 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.775 |


**Q56: What safety feature does the STORKLINTA 6-drawer dresser include?**
*(expects URL containing: `storklinta-6-drawer-dresser-dark-brown-oak-effect-anchor-unlock-function-70559278`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.805 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.801 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.783 |
| crawl4ai | #9 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.806 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.805 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.801 |
| crawl4ai-raw | #8 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.806 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.805 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-w | 0.801 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.745 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.742 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.738 |
| crawlee | #13 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.824 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.806 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.806 |
| colly+md | miss | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.834 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.806 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.805 |
| playwright | #4 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.806 | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.794 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.789 |


**Q57: What features do the desk chairs have that support comfort during work?**
*(expects URL containing: `desk-chairs-20652`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.679 | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.631 | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.620 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.732 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.726 | www.ikea.com/us/en/cat/workspace-desks-chairs-fu00 | 0.694 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.732 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.723 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.720 |
| scrapy+md | miss | www.ikea.com/us/en/cat/chair-pads-20542/ | 0.684 | www.ikea.com/us/en/p/laektare-chair-cover-gunnared | 0.670 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.657 |
| crawlee | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.732 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.728 | www.ikea.com/us/en/cat/workspace-desks-chairs-fu00 | 0.728 |
| colly+md | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.732 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.730 | www.ikea.com/us/en/cat/workspace-desks-chairs-fu00 | 0.708 |
| playwright | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.732 | www.ikea.com/us/en/cat/workspace-desks-chairs-fu00 | 0.728 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.715 |


**Q58: What is the price of the MULLSJÖ swivel chair?**
*(expects URL containing: `desk-chairs-20652`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.713 | www.ikea.com/us/en/cat/upholstered-chairs-25221/ | 0.680 | www.ikea.com/us/en/cat/outdoor-patio-lounge-chairs | 0.671 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.778 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.734 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.719 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.778 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.725 | www.ikea.com/us/en/cat/dining-chairs-25219/ | 0.709 |
| scrapy+md | miss | www.ikea.com/us/en/cat/dining-chairs-25219/ | 0.739 | www.ikea.com/us/en/cat/dining-chairs-25219/ | 0.722 | www.ikea.com/us/en/cat/nytillverkad-collection-620 | 0.667 |
| crawlee | #1 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.810 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.741 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.732 |
| colly+md | #2 | www.ikea.com/us/en/cat/dining-chairs-25219/ | 0.757 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.756 | www.ikea.com/us/en/cat/desk-chairs-20652/ | 0.743 |
| playwright | #40 | www.ikea.com/us/en/cat/workspace-desks-chairs-fu00 | 0.737 | www.ikea.com/us/en/cat/workspace-desks-chairs-fu00 | 0.725 | www.ikea.com/us/en/cat/tables-chairs-fu002/ | 0.699 |


**Q59: What is the material of the KALAS plate?**
*(expects URL containing: `kalas-plate-mixed-colors-80461380`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/cookware-tableware-kt001/ | 0.537 | www.ikea.com/us/en/cat/serveware-16043/?filters=f- | 0.532 | www.ikea.com/us/en/cat/serveware-16043/?filters=f- | 0.531 |
| crawl4ai | #1 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.648 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.643 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.631 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.648 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.643 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.641 |
| scrapy+md | miss | www.ikea.com/us/en/p/upplaga-mug-white-80443800/ | 0.556 | www.ikea.com/us/en/p/godmiddag-serving-plate-white | 0.551 | www.ikea.com/us/en/p/stamsill-coaster-water-hyacin | 0.550 |
| crawlee | #1 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.693 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.639 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.631 |
| colly+md | miss | www.ikea.com/us/en/rooms/dining/how-to/how-to-prol | 0.527 | www.ikea.com/us/en/rooms/dining/how-to/how-to-prol | 0.518 | www.ikea.com/us/en/p/kleppstad-wardrobe-with-slidi | 0.517 |
| playwright | miss | www.ikea.com/us/en/rooms/dining/how-to/how-to-prol | 0.527 | www.ikea.com/us/en/p/padrag-vase-clear-glass-10470 | 0.523 | www.ikea.com/us/en/cat/cookware-tableware-kt001/ | 0.522 |


**Q60: What is the diameter of the KALAS plate?**
*(expects URL containing: `kalas-plate-mixed-colors-80461380`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/klipplax-glass-clear-glass-50 | 0.542 | www.ikea.com/us/en/p/stockholm-2025-bowl-dark-blue | 0.539 | www.ikea.com/us/en/cat/serveware-16043/?filters=f- | 0.538 |
| crawl4ai | #1 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.694 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.668 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.653 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.694 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.668 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.653 |
| scrapy+md | miss | www.ikea.com/us/en/p/godmiddag-serving-plate-white | 0.589 | www.ikea.com/us/en/p/godmiddag-serving-plate-white | 0.580 | www.ikea.com/us/en/p/godmiddag-serving-bowl-white- | 0.572 |
| crawlee | #1 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.730 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.669 | www.ikea.com/us/en/p/kalas-plate-mixed-colors-8046 | 0.626 |
| colly+md | miss | www.ikea.com/us/en/cat/kallax-series-27534/ | 0.522 | www.ikea.com/us/en/cat/outdoor-kitchens-700349/ | 0.520 | www.ikea.com/us/en/cat/stockholm-collection-11989/ | 0.519 |
| playwright | miss | www.ikea.com/us/en/cat/outdoor-kitchens-700349/ | 0.534 | www.ikea.com/us/en/p/naesinge-extendable-table-dar | 0.523 | www.ikea.com/us/en/cat/stockholm-collection-11989/ | 0.519 |


</details>

## kubernetes-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawlee | 79% (45/57) | 91% (52/57) | 91% (52/57) | 93% (53/57) | 93% (53/57) | 0.852 | 6813 | 400 |
| playwright | 79% (45/57) | 91% (52/57) | 91% (52/57) | 91% (52/57) | 93% (53/57) | 0.851 | 6812 | 400 |
| crawl4ai | 74% (42/57) | 86% (49/57) | 88% (50/57) | 91% (52/57) | 91% (52/57) | 0.800 | 6822 | 400 |
| crawl4ai-raw | 74% (42/57) | 86% (49/57) | 88% (50/57) | 91% (52/57) | 91% (52/57) | 0.800 | 6822 | 400 |
| colly+md | 70% (40/57) | 81% (46/57) | 81% (46/57) | 81% (46/57) | 82% (47/57) | 0.755 | 6743 | 399 |
| markcrawl | 51% (29/57) | 61% (35/57) | 68% (39/57) | 70% (40/57) | 70% (40/57) | 0.578 | 7922 | 400 |
| scrapy+md | 2% (1/57) | 5% (3/57) | 5% (3/57) | 7% (4/57) | 9% (5/57) | 0.039 | 3507 | 315 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for kubernetes-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is the purpose of the Topology Manager in Kubernetes?**
*(expects URL containing: `resource-managers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/workloads/resource-man | 0.823 | kubernetes.io/docs/concepts/services-networking/to | 0.792 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.773 |
| crawl4ai | #8 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.853 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.821 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.807 |
| crawl4ai-raw | #8 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.853 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.821 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.807 |
| scrapy+md | miss | kubernetes.io/feed.xml | 0.786 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.781 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.772 |
| crawlee | #10 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.856 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.823 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.807 |
| colly+md | #11 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.856 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.823 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.807 |
| playwright | #11 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.856 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.823 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.807 |


**Q2: What are the two available policies for the CPU Manager in Kubernetes?**
*(expects URL containing: `resource-managers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.838 | kubernetes.io/docs/concepts/workloads/resource-man | 0.819 | kubernetes.io/docs/concepts/_print/ | 0.819 |
| crawl4ai | #3 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.844 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.815 | kubernetes.io/docs/concepts/workloads/resource-man | 0.809 |
| crawl4ai-raw | #3 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.844 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.815 | kubernetes.io/docs/concepts/workloads/resource-man | 0.809 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.819 | kubernetes.io/docs/concepts/_print/ | 0.809 | kubernetes.io/docs/concepts/_print/ | 0.809 |
| crawlee | #3 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.842 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.815 | kubernetes.io/docs/concepts/workloads/resource-man | 0.809 |
| colly+md | #3 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.842 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.815 | kubernetes.io/docs/concepts/workloads/resource-man | 0.809 |
| playwright | #3 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.842 | kubernetes.io/docs/tasks/administer-cluster/cpu-ma | 0.815 | kubernetes.io/docs/concepts/workloads/resource-man | 0.809 |


**Q3: How do I list the current namespaces in a Kubernetes cluster?**
*(expects URL containing: `namespaces`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tutorials/cluster-management/na | 0.811 | kubernetes.io/docs/tutorials/cluster-management/na | 0.802 | kubernetes.io/docs/concepts/overview/working-with- | 0.779 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.796 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.794 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.788 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.796 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.794 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.788 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.776 | kubernetes.io/zh-cn/feed.xml | 0.761 | kubernetes.io/feed.xml | 0.753 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.799 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.795 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.794 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.804 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.799 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.794 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.804 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.799 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.794 |


**Q4: What command do I use to delete a namespace in Kubernetes?**
*(expects URL containing: `namespaces`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #6 | kubernetes.io/docs/concepts/overview/working-with- | 0.781 | kubernetes.io/docs/concepts/overview/_print/ | 0.779 | kubernetes.io/docs/concepts/_print/ | 0.778 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.817 | kubernetes.io/docs/tasks/administer-cluster/use-ca | 0.780 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.771 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.817 | kubernetes.io/docs/tasks/administer-cluster/use-ca | 0.780 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.771 |
| scrapy+md | miss | kubernetes.io/zh-cn/docs/reference/access-authn-au | 0.796 | kubernetes.io/fr/docs/reference/kubectl/quick-refe | 0.776 | kubernetes.io/fr/docs/reference/kubectl/_print/ | 0.776 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.818 | kubernetes.io/docs/tasks/administer-cluster/use-ca | 0.780 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.771 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.818 | kubernetes.io/docs/tasks/administer-cluster/use-ca | 0.780 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.771 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.818 | kubernetes.io/docs/tasks/administer-cluster/use-ca | 0.780 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.771 |


**Q5: What is a VolumeSnapshot in Kubernetes?**
*(expects URL containing: `volume-snapshots`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.897 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.869 | kubernetes.io/docs/concepts/storage/_print/ | 0.855 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.872 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.864 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.804 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.872 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.864 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.804 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.848 | kubernetes.io/docs/concepts/_print/ | 0.804 | kubernetes.io/docs/concepts/_print/ | 0.796 |
| crawlee | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.874 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.854 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.809 |
| colly+md | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.874 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.854 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.809 |
| playwright | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.874 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.854 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.809 |


**Q6: How can you provision a new volume from a snapshot?**
*(expects URL containing: `volume-snapshots`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.796 | kubernetes.io/docs/concepts/_print/ | 0.793 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.793 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.789 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.772 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.726 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.789 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.772 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.726 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.789 | kubernetes.io/docs/concepts/_print/ | 0.756 | kubernetes.io/docs/concepts/_print/ | 0.741 |
| crawlee | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.791 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.789 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.726 |
| colly+md | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.791 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.789 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.726 |
| playwright | #1 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.791 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.789 | kubernetes.io/docs/concepts/storage/volume-snapsho | 0.726 |


**Q7: How do you create a namespace for default CPU limits?**
*(expects URL containing: `cpu-default-namespace`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/tasks/administer-cluster/manage | 0.750 | kubernetes.io/docs/concepts/_print/ | 0.733 | kubernetes.io/docs/concepts/policy/_print/ | 0.733 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.764 | kubernetes.io/docs/tasks/configure-pod-container/r | 0.749 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.739 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.764 | kubernetes.io/docs/tasks/configure-pod-container/r | 0.749 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.739 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.732 | kubernetes.io/feed.xml | 0.714 | kubernetes.io/docs/concepts/_print/ | 0.707 |
| crawlee | #2 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.786 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.764 | kubernetes.io/docs/tasks/configure-pod-container/r | 0.763 |
| colly+md | miss | kubernetes.io/docs/tasks/administer-cluster/manage | 0.786 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.764 | kubernetes.io/docs/tasks/configure-pod-container/r | 0.763 |
| playwright | #2 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.786 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.764 | kubernetes.io/docs/tasks/configure-pod-container/r | 0.763 |


**Q8: What are the default CPU request and limit values applied by the control plane?**
*(expects URL containing: `cpu-default-namespace`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/reference/command-line-tools-re | 0.710 | kubernetes.io/docs/concepts/workloads/pods/ | 0.707 | kubernetes.io/docs/concepts/_print/ | 0.707 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.723 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.713 | kubernetes.io/docs/concepts/workloads/pods/ | 0.706 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.723 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.713 | kubernetes.io/docs/concepts/workloads/pods/ | 0.706 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.707 | kubernetes.io/docs/concepts/_print/ | 0.701 | kubernetes.io/docs/concepts/_print/ | 0.699 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.726 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.713 | kubernetes.io/docs/concepts/workloads/pods/ | 0.707 |
| colly+md | miss | kubernetes.io/docs/tasks/administer-cluster/manage | 0.726 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.713 | kubernetes.io/docs/concepts/workloads/pods/ | 0.707 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.726 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.713 | kubernetes.io/docs/concepts/workloads/pods/ | 0.707 |


**Q9: What are some examples of API objects that act as policies in Kubernetes?**
*(expects URL containing: `policy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/policy/_print/ | 0.845 | kubernetes.io/docs/concepts/policy/ | 0.840 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.796 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/policy/ | 0.849 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.785 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.784 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/policy/ | 0.849 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.785 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.784 |
| scrapy+md | miss | kubernetes.io/it/docs/reference/glossary/?all=true | 0.795 | kubernetes.io/docs/concepts/_print/ | 0.788 | kubernetes.io/docs/reference/glossary/?all=true | 0.787 |
| crawlee | #1 | kubernetes.io/docs/concepts/policy/ | 0.838 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.788 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.784 |
| colly+md | #1 | kubernetes.io/docs/concepts/policy/ | 0.838 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.788 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.784 |
| playwright | #1 | kubernetes.io/docs/concepts/policy/ | 0.838 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.788 | kubernetes.io/docs/concepts/extend-kubernetes/ | 0.784 |


**Q10: How do dynamic admission controllers apply policies on API requests?**
*(expects URL containing: `policy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/policy/ | 0.819 | kubernetes.io/docs/concepts/_print/ | 0.805 | kubernetes.io/docs/concepts/policy/_print/ | 0.791 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/policy/ | 0.804 | kubernetes.io/docs/concepts/security/controlling-a | 0.744 | kubernetes.io/docs/concepts/security/security-chec | 0.694 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/policy/ | 0.804 | kubernetes.io/docs/concepts/security/controlling-a | 0.744 | kubernetes.io/docs/concepts/security/security-chec | 0.694 |
| scrapy+md | #35 | kubernetes.io/docs/concepts/_print/ | 0.805 | kubernetes.io/docs/concepts/_print/ | 0.745 | kubernetes.io/hi/docs/_print/ | 0.726 |
| crawlee | #1 | kubernetes.io/docs/concepts/policy/ | 0.819 | kubernetes.io/docs/concepts/security/controlling-a | 0.745 | kubernetes.io/docs/tasks/administer-cluster/quota- | 0.726 |
| colly+md | #1 | kubernetes.io/docs/concepts/policy/ | 0.819 | kubernetes.io/docs/concepts/security/controlling-a | 0.745 | kubernetes.io/docs/tasks/administer-cluster/quota- | 0.726 |
| playwright | #1 | kubernetes.io/docs/concepts/policy/ | 0.819 | kubernetes.io/docs/concepts/security/controlling-a | 0.745 | kubernetes.io/docs/tasks/administer-cluster/quota- | 0.726 |


**Q11: What are the two options for configuring the topology of highly available Kubernetes clusters?**
*(expects URL containing: `ha-topology`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.819 | kubernetes.io/docs/setup/production-environment/ | 0.789 | kubernetes.io/docs/concepts/scheduling-eviction/_p | 0.788 |
| crawl4ai | #21 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.818 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.810 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.790 |
| crawl4ai-raw | #21 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.818 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.810 | kubernetes.io/docs/tasks/administer-cluster/topolo | 0.790 |
| scrapy+md | miss | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.818 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.815 | kubernetes.io/feed.xml | 0.787 |
| crawlee | #2 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.818 | kubernetes.io/docs/setup/production-environment/to | 0.811 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.810 |
| colly+md | #2 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.818 | kubernetes.io/docs/setup/production-environment/to | 0.811 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.810 |
| playwright | #2 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.818 | kubernetes.io/docs/setup/production-environment/to | 0.811 | kubernetes.io/docs/concepts/scheduling-eviction/to | 0.810 |


**Q12: What is the minimum number of control plane nodes required for a stacked HA cluster?**
*(expects URL containing: `ha-topology`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/setup/production-environment/ | 0.707 | kubernetes.io/docs/concepts/architecture/ | 0.689 | kubernetes.io/docs/setup/production-environment/ | 0.682 |
| crawl4ai | #1 | kubernetes.io/docs/setup/production-environment/to | 0.753 | kubernetes.io/docs/setup/production-environment/ | 0.707 | kubernetes.io/docs/setup/production-environment/to | 0.704 |
| crawl4ai-raw | #1 | kubernetes.io/docs/setup/production-environment/to | 0.753 | kubernetes.io/docs/setup/production-environment/ | 0.707 | kubernetes.io/docs/setup/production-environment/to | 0.704 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.670 | kubernetes.io/feed.xml | 0.666 | kubernetes.io/docs/concepts/_print/ | 0.666 |
| crawlee | #1 | kubernetes.io/docs/setup/production-environment/to | 0.749 | kubernetes.io/docs/setup/production-environment/to | 0.740 | kubernetes.io/docs/setup/best-practices/cluster-la | 0.710 |
| colly+md | #1 | kubernetes.io/docs/setup/production-environment/to | 0.749 | kubernetes.io/docs/setup/production-environment/to | 0.740 | kubernetes.io/docs/setup/best-practices/cluster-la | 0.710 |
| playwright | #1 | kubernetes.io/docs/setup/production-environment/to | 0.749 | kubernetes.io/docs/setup/production-environment/to | 0.740 | kubernetes.io/docs/setup/best-practices/cluster-la | 0.710 |


**Q13: How can I create Secret objects using kubectl?**
*(expects URL containing: `configmap-secret`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.866 | kubernetes.io/docs/reference/kubectl/generated/kub | 0.832 | kubernetes.io/docs/reference/kubectl/generated/kub | 0.822 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.829 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.815 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.799 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.829 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.815 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.799 |
| scrapy+md | miss | kubernetes.io/docs/reference/generated/kubectl/kub | 0.805 | kubernetes.io/docs/reference/generated/kubectl/kub | 0.784 | kubernetes.io/docs/reference/generated/kubectl/kub | 0.783 |
| crawlee | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.829 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.815 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.801 |
| colly+md | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.829 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.815 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.801 |
| playwright | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.829 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.815 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.801 |


**Q14: What file format can be used to create Secret objects in Kubernetes?**
*(expects URL containing: `configmap-secret`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | kubernetes.io/docs/reference/kubectl/generated/kub | 0.835 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.813 | kubernetes.io/docs/reference/generated/kubernetes- | 0.808 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.846 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.827 | kubernetes.io/docs/tasks/configure-pod-container/p | 0.813 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.846 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.827 | kubernetes.io/docs/tasks/configure-pod-container/p | 0.813 |
| scrapy+md | miss | kubernetes.io/docs/reference/generated/kubectl/kub | 0.816 | kubernetes.io/docs/concepts/_print/ | 0.796 | kubernetes.io/docs/concepts/_print/ | 0.792 |
| crawlee | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.848 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.827 | kubernetes.io/docs/tasks/configure-pod-container/p | 0.813 |
| colly+md | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.848 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.827 | kubernetes.io/docs/tasks/configure-pod-container/p | 0.813 |
| playwright | #1 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.848 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.827 | kubernetes.io/docs/tasks/configure-pod-container/p | 0.813 |


**Q15: What is a service account in Kubernetes?**
*(expects URL containing: `service-accounts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.902 | kubernetes.io/docs/concepts/security/_print/ | 0.897 | kubernetes.io/docs/concepts/_print/ | 0.897 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.893 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.835 | kubernetes.io/docs/concepts/security/service-accou | 0.820 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.893 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.835 | kubernetes.io/docs/concepts/security/service-accou | 0.820 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.897 | kubernetes.io/docs/concepts/_print/ | 0.819 | kubernetes.io/docs/concepts/_print/ | 0.815 |
| crawlee | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.891 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.836 | kubernetes.io/docs/concepts/security/service-accou | 0.819 |
| colly+md | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.891 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.836 | kubernetes.io/docs/concepts/security/service-accou | 0.819 |
| playwright | #1 | kubernetes.io/docs/concepts/security/service-accou | 0.891 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.836 | kubernetes.io/docs/concepts/security/service-accou | 0.819 |


**Q16: How do you assign a ServiceAccount to a Pod?**
*(expects URL containing: `service-accounts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | kubernetes.io/docs/reference/kubernetes-api/worklo | 0.801 | kubernetes.io/docs/concepts/security/service-accou | 0.799 | kubernetes.io/docs/concepts/security/_print/ | 0.799 |
| crawl4ai | #2 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.815 | kubernetes.io/docs/concepts/security/service-accou | 0.799 | kubernetes.io/docs/concepts/security/service-accou | 0.781 |
| crawl4ai-raw | #2 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.815 | kubernetes.io/docs/concepts/security/service-accou | 0.799 | kubernetes.io/docs/concepts/security/service-accou | 0.781 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.799 | kubernetes.io/docs/concepts/_print/ | 0.780 | kubernetes.io/docs/concepts/_print/ | 0.759 |
| crawlee | #2 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.814 | kubernetes.io/docs/concepts/security/service-accou | 0.799 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.781 |
| colly+md | #2 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.814 | kubernetes.io/docs/concepts/security/service-accou | 0.799 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.781 |
| playwright | #2 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.814 | kubernetes.io/docs/concepts/security/service-accou | 0.799 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.781 |


**Q17: What is required for an Ingress to work in a Kubernetes cluster?**
*(expects URL containing: `ingress-controllers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.854 | kubernetes.io/docs/concepts/services-networking/in | 0.834 | kubernetes.io/docs/concepts/_print/ | 0.823 |
| crawl4ai | #6 | kubernetes.io/docs/concepts/services-networking/in | 0.822 | kubernetes.io/docs/concepts/services-networking/in | 0.813 | v1-32.docs.kubernetes.io/docs/concepts/ | 0.791 |
| crawl4ai-raw | #6 | kubernetes.io/docs/concepts/services-networking/in | 0.822 | kubernetes.io/docs/concepts/services-networking/in | 0.813 | v1-32.docs.kubernetes.io/docs/concepts/ | 0.791 |
| scrapy+md | #15 | kubernetes.io/docs/concepts/_print/ | 0.822 | kubernetes.io/docs/concepts/_print/ | 0.792 | kubernetes.io/docs/concepts/_print/ | 0.792 |
| crawlee | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.860 | kubernetes.io/docs/concepts/services-networking/in | 0.827 | kubernetes.io/docs/concepts/services-networking/in | 0.819 |
| colly+md | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.860 | kubernetes.io/docs/concepts/services-networking/in | 0.827 | kubernetes.io/docs/concepts/services-networking/in | 0.819 |
| playwright | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.860 | kubernetes.io/docs/concepts/services-networking/in | 0.827 | kubernetes.io/docs/concepts/services-networking/in | 0.819 |


**Q18: Which ingress controllers are supported and maintained by the Kubernetes project?**
*(expects URL containing: `ingress-controllers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.878 | kubernetes.io/docs/concepts/services-networking/_p | 0.850 | kubernetes.io/docs/concepts/_print/ | 0.850 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.846 | kubernetes.io/docs/concepts/services-networking/in | 0.834 | kubernetes.io/docs/concepts/services-networking/in | 0.814 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.846 | kubernetes.io/docs/concepts/services-networking/in | 0.834 | kubernetes.io/docs/concepts/services-networking/in | 0.814 |
| scrapy+md | #9 | kubernetes.io/docs/concepts/_print/ | 0.850 | kubernetes.io/docs/concepts/_print/ | 0.825 | kubernetes.io/docs/concepts/_print/ | 0.824 |
| crawlee | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.863 | kubernetes.io/docs/concepts/services-networking/in | 0.850 | kubernetes.io/docs/concepts/services-networking/in | 0.821 |
| colly+md | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.863 | kubernetes.io/docs/concepts/services-networking/in | 0.850 | kubernetes.io/docs/concepts/services-networking/in | 0.824 |
| playwright | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.863 | kubernetes.io/docs/concepts/services-networking/in | 0.850 | kubernetes.io/docs/concepts/services-networking/in | 0.821 |


**Q19: What is a workload in Kubernetes?**
*(expects URL containing: `workloads`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/workloads/ | 0.832 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.790 | kubernetes.io/docs/concepts/_print/ | 0.790 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/workloads/ | 0.775 | kubernetes.io/vi/docs/concepts/ | 0.774 | kubernetes.io/docs/concepts/workloads/podgroup-api | 0.760 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/workloads/ | 0.775 | kubernetes.io/vi/docs/concepts/ | 0.774 | kubernetes.io/docs/concepts/workloads/podgroup-api | 0.760 |
| scrapy+md | miss | kubernetes.io/feed.xml | 0.805 | kubernetes.io/zh-cn/feed.xml | 0.801 | kubernetes.io/docs/concepts/_print/ | 0.790 |
| crawlee | #1 | kubernetes.io/docs/concepts/workloads/ | 0.805 | kubernetes.io/docs/concepts/workloads/ | 0.792 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.792 |
| colly+md | #1 | kubernetes.io/docs/concepts/workloads/ | 0.805 | kubernetes.io/docs/concepts/workloads/ | 0.792 | kubernetes.io/docs/concepts/workloads/ | 0.789 |
| playwright | #1 | kubernetes.io/docs/concepts/workloads/ | 0.805 | kubernetes.io/docs/concepts/workloads/ | 0.792 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.792 |


**Q20: What are the built-in workload resources provided by Kubernetes?**
*(expects URL containing: `workloads`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | kubernetes.io/docs/concepts/_print/ | 0.803 | kubernetes.io/docs/concepts/workloads/ | 0.797 | kubernetes.io/docs/concepts/workloads/_print/ | 0.797 |
| crawl4ai | #5 | kubernetes.io/vi/docs/concepts/ | 0.791 | kubernetes.io/docs/setup/production-environment/ | 0.768 | kubernetes.io/docs/tasks/administer-cluster/migrat | 0.767 |
| crawl4ai-raw | #5 | kubernetes.io/vi/docs/concepts/ | 0.791 | kubernetes.io/docs/setup/production-environment/ | 0.768 | kubernetes.io/docs/tasks/administer-cluster/migrat | 0.767 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.803 | kubernetes.io/feed.xml | 0.794 | kubernetes.io/zh-cn/feed.xml | 0.781 |
| crawlee | #1 | kubernetes.io/docs/concepts/workloads/ | 0.806 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.781 | kubernetes.io/docs/concepts/configuration/manage-r | 0.764 |
| colly+md | #1 | kubernetes.io/docs/concepts/workloads/ | 0.797 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.773 | kubernetes.io/docs/concepts/configuration/manage-r | 0.764 |
| playwright | #1 | kubernetes.io/docs/concepts/workloads/ | 0.806 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.781 | kubernetes.io/docs/concepts/configuration/manage-r | 0.764 |


**Q21: What does this page provide a list of?**
*(expects URL containing: `turnkey-solutions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/reference/generated/kubernetes- | 0.593 | kubernetes.io/docs/reference/generated/kubernetes- | 0.592 | kubernetes.io/docs/reference/generated/kubernetes- | 0.592 |
| crawl4ai | miss | kubernetes.io/docs/concepts/overview/working-with- | 0.575 | kubernetes.io/docs/tasks/debug/debug-application/ | 0.574 | kubernetes.io/pl/docs/concepts/ | 0.571 |
| crawl4ai-raw | miss | kubernetes.io/docs/concepts/overview/working-with- | 0.575 | kubernetes.io/docs/tasks/debug/debug-application/ | 0.574 | kubernetes.io/pl/docs/concepts/ | 0.571 |
| scrapy+md | miss | kubernetes.io/feed.xml | 0.619 | kubernetes.io/de/docs/sitemap/ | 0.592 | kubernetes.io/feed.xml | 0.575 |
| crawlee | miss | kubernetes.io/docs/tasks/manage-kubernetes-objects | 0.552 | kubernetes.io/ja/docs/concepts/ | 0.541 | kubernetes.io/ja/docs/concepts/ | 0.540 |
| colly+md | miss | kubernetes.io/docs/tasks/manage-kubernetes-objects | 0.552 | kubernetes.io/docs/concepts/security/application-s | 0.552 | kubernetes.io/docs/concepts/security/security-chec | 0.546 |
| playwright | miss | kubernetes.io/docs/tasks/manage-kubernetes-objects | 0.552 | kubernetes.io/docs/concepts/security/application-s | 0.552 | kubernetes.io/docs/concepts/security/security-chec | 0.546 |


**Q22: How can I learn to install and set up production-ready clusters from the providers listed?**
*(expects URL containing: `turnkey-solutions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/setup/production-environment/ | 0.777 | kubernetes.io/docs/concepts/_print/ | 0.773 | kubernetes.io/docs/setup/production-environment/ | 0.761 |
| crawl4ai | miss | kubernetes.io/docs/setup/learning-environment/ | 0.768 | kubernetes.io/docs/setup/learning-environment/ | 0.766 | kubernetes.io/docs/setup/production-environment/to | 0.766 |
| crawl4ai-raw | miss | kubernetes.io/docs/setup/learning-environment/ | 0.768 | kubernetes.io/docs/setup/learning-environment/ | 0.766 | kubernetes.io/docs/setup/production-environment/to | 0.766 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.773 | kubernetes.io/feed.xml | 0.748 | kubernetes.io/zh-cn/feed.xml | 0.738 |
| crawlee | #24 | kubernetes.io/docs/setup/ | 0.786 | kubernetes.io/docs/setup/production-environment/ | 0.776 | kubernetes.io/docs/setup/learning-environment/ | 0.768 |
| colly+md | #23 | kubernetes.io/docs/setup/ | 0.786 | kubernetes.io/docs/setup/production-environment/ | 0.776 | kubernetes.io/docs/setup/production-environment/to | 0.764 |
| playwright | #24 | kubernetes.io/docs/setup/ | 0.786 | kubernetes.io/docs/setup/production-environment/ | 0.776 | kubernetes.io/docs/setup/learning-environment/ | 0.768 |


**Q23: What is the recommended approach for providing kubelet parameters?**
*(expects URL containing: `kubelet-config-file`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/reference/command-line-tools-re | 0.735 | kubernetes.io/docs/reference/generated/kubernetes- | 0.733 | kubernetes.io/docs/reference/command-line-tools-re | 0.732 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.778 | kubernetes.io/docs/setup/production-environment/to | 0.735 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.719 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.778 | kubernetes.io/docs/setup/production-environment/to | 0.735 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.719 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.695 | kubernetes.io/ru/releases/download/ | 0.682 | kubernetes.io/ru/releases/_print/ | 0.682 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.776 | kubernetes.io/docs/setup/production-environment/to | 0.735 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.719 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.776 | kubernetes.io/docs/setup/production-environment/to | 0.735 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.724 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.776 | kubernetes.io/docs/setup/production-environment/to | 0.735 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.724 |


**Q24: What format must the kubelet configuration file be in?**
*(expects URL containing: `kubelet-config-file`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/reference/node/kubelet-files/ | 0.783 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.760 | kubernetes.io/docs/reference/command-line-tools-re | 0.760 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.813 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.809 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.763 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.813 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.809 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.763 |
| scrapy+md | miss | kubernetes.io/feed.xml | 0.801 | kubernetes.io/feed.xml | 0.742 | kubernetes.io/feed.xml | 0.726 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.813 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.809 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.763 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.813 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.809 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.763 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.813 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.809 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.763 |


**Q25: What are the four sections of the debugging guide?**
*(expects URL containing: `debug`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tasks/debug/debug-application/ | 0.634 | kubernetes.io/docs/contribute/style/style-guide/ | 0.629 | kubernetes.io/docs/contribute/style/page-content-t | 0.611 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/windo | 0.651 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.643 | kubernetes.io/docs/tasks/debug/debug-application/ | 0.626 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/windo | 0.651 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.643 | kubernetes.io/docs/tasks/debug/debug-application/ | 0.626 |
| scrapy+md | miss | kubernetes.io/feed.xml | 0.603 | kubernetes.io/feed.xml | 0.602 | kubernetes.io/docs/reference/generated/kubectl/kub | 0.594 |
| crawlee | #1 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.639 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.636 | kubernetes.io/docs/tasks/debug/debug-cluster/local | 0.632 |
| colly+md | #1 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.639 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.636 | kubernetes.io/docs/tasks/debug/debug-cluster/local | 0.632 |
| playwright | #1 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.639 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.636 | kubernetes.io/docs/tasks/debug/debug-cluster/local | 0.632 |


**Q26: How can I get help if my question isn't covered in the documentation?**
*(expects URL containing: `debug`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/contribute/review/reviewing-prs | 0.618 | kubernetes.io/docs/reference/generated/kubernetes- | 0.614 | kubernetes.io/docs/reference/generated/kubernetes- | 0.611 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/debug/ | 0.624 | kubernetes.io/docs/tasks/debug/ | 0.613 | kubernetes.io/docs/tasks/configmap-secret/ | 0.603 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/debug/ | 0.624 | kubernetes.io/docs/tasks/debug/ | 0.613 | kubernetes.io/docs/tasks/configmap-secret/ | 0.603 |
| scrapy+md | miss | kubernetes.io/fr/docs/reference/issues-security/ | 0.620 | kubernetes.io/fr/docs/tutorials/services/ | 0.612 | kubernetes.io/fr/docs/reference/kubernetes-api/ | 0.599 |
| crawlee | #1 | kubernetes.io/docs/tasks/debug/ | 0.606 | kubernetes.io/docs/tasks/debug/ | 0.599 | kubernetes.io/docs/concepts/cluster-administration | 0.594 |
| colly+md | #1 | kubernetes.io/docs/tasks/debug/ | 0.606 | kubernetes.io/docs/tasks/debug/ | 0.599 | kubernetes.io/docs/concepts/cluster-administration | 0.594 |
| playwright | #1 | kubernetes.io/docs/tasks/debug/ | 0.606 | kubernetes.io/docs/tasks/debug/ | 0.599 | kubernetes.io/docs/concepts/cluster-administration | 0.594 |


**Q27: What should I do if `kubeadm join` from v1.18 cannot join a cluster created by kubeadm v1.17?**
*(expects URL containing: `troubleshooting-kubeadm`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/setup/production-environment/to | 0.836 | kubernetes.io/docs/reference/setup-tools/kubeadm/k | 0.767 | kubernetes.io/docs/tasks/debug/debug-cluster/troub | 0.742 |
| crawl4ai | #1 | kubernetes.io/docs/setup/production-environment/to | 0.835 | kubernetes.io/docs/tasks/administer-cluster/kubead | 0.757 | kubernetes.io/docs/tasks/configure-pod-container/a | 0.749 |
| crawl4ai-raw | #1 | kubernetes.io/docs/setup/production-environment/to | 0.835 | kubernetes.io/docs/tasks/administer-cluster/kubead | 0.757 | kubernetes.io/docs/tasks/configure-pod-container/a | 0.749 |
| scrapy+md | miss | kubernetes.io/feed.xml | 0.734 | kubernetes.io/docs/concepts/_print/ | 0.721 | kubernetes.io/feed.xml | 0.704 |
| crawlee | #1 | kubernetes.io/docs/setup/production-environment/to | 0.835 | kubernetes.io/docs/tasks/administer-cluster/kubead | 0.759 | kubernetes.io/docs/setup/production-environment/to | 0.754 |
| colly+md | miss | kubernetes.io/docs/setup/production-environment/to | 0.835 | kubernetes.io/docs/tasks/administer-cluster/kubead | 0.759 | kubernetes.io/docs/setup/production-environment/to | 0.754 |
| playwright | #1 | kubernetes.io/docs/setup/production-environment/to | 0.835 | kubernetes.io/docs/tasks/administer-cluster/kubead | 0.759 | kubernetes.io/docs/setup/production-environment/to | 0.754 |


**Q28: How can I resolve the issue of `coredns` pods being in `CrashLoopBackOff` or `Error` state?**
*(expects URL containing: `troubleshooting-kubeadm`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/setup/production-environment/to | 0.823 | kubernetes.io/docs/setup/production-environment/to | 0.812 | kubernetes.io/docs/concepts/workloads/_print/ | 0.794 |
| crawl4ai | #1 | kubernetes.io/docs/setup/production-environment/to | 0.808 | kubernetes.io/docs/setup/production-environment/to | 0.786 | kubernetes.io/docs/concepts/workloads/pods/pod-lif | 0.778 |
| crawl4ai-raw | #1 | kubernetes.io/docs/setup/production-environment/to | 0.808 | kubernetes.io/docs/setup/production-environment/to | 0.786 | kubernetes.io/docs/concepts/workloads/pods/pod-lif | 0.778 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.794 | kubernetes.io/blog/2023/08/16/kubernetes-1-28-non- | 0.728 | kubernetes.io/docs/concepts/_print/ | 0.724 |
| crawlee | #1 | kubernetes.io/docs/setup/production-environment/to | 0.808 | kubernetes.io/docs/concepts/workloads/pods/pod-lif | 0.794 | kubernetes.io/docs/setup/production-environment/to | 0.785 |
| colly+md | miss | kubernetes.io/docs/setup/production-environment/to | 0.808 | kubernetes.io/docs/concepts/workloads/pods/pod-lif | 0.794 | kubernetes.io/docs/setup/production-environment/to | 0.785 |
| playwright | #1 | kubernetes.io/docs/setup/production-environment/to | 0.808 | kubernetes.io/docs/concepts/workloads/pods/pod-lif | 0.794 | kubernetes.io/docs/setup/production-environment/to | 0.785 |


**Q29: What is the default operating mode for connections from nodes to the control plane?**
*(expects URL containing: `control-plane-node-communication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.733 | kubernetes.io/docs/concepts/_print/ | 0.733 | kubernetes.io/docs/concepts/architecture/_print/ | 0.733 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.734 | kubernetes.io/docs/tasks/administer-cluster/kubead | 0.712 | kubernetes.io/docs/tasks/administer-cluster/kubead | 0.704 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.734 | kubernetes.io/docs/tasks/administer-cluster/kubead | 0.712 | kubernetes.io/docs/tasks/administer-cluster/kubead | 0.704 |
| scrapy+md | #2 | kubernetes.io/docs/concepts/_print/ | 0.733 | kubernetes.io/it/docs/concepts/architecture/contro | 0.709 | kubernetes.io/docs/concepts/_print/ | 0.706 |
| crawlee | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.733 | kubernetes.io/docs/tasks/administer-cluster/kubead | 0.726 | kubernetes.io/docs/tasks/administer-cluster/kubead | 0.709 |
| colly+md | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.733 | kubernetes.io/docs/tasks/administer-cluster/kubead | 0.726 | kubernetes.io/docs/tasks/administer-cluster/kubead | 0.709 |
| playwright | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.733 | kubernetes.io/docs/tasks/administer-cluster/kubead | 0.726 | kubernetes.io/docs/tasks/administer-cluster/kubead | 0.709 |


**Q30: How does the Konnectivity service improve control plane to node communication?**
*(expects URL containing: `control-plane-node-communication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | kubernetes.io/docs/concepts/architecture/_print/ | 0.736 | kubernetes.io/docs/concepts/architecture/control-p | 0.736 | kubernetes.io/docs/concepts/_print/ | 0.736 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.736 | kubernetes.io/docs/concepts/architecture/control-p | 0.701 | kubernetes.io/docs/concepts/services-networking/se | 0.677 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.736 | kubernetes.io/docs/concepts/architecture/control-p | 0.701 | kubernetes.io/docs/concepts/services-networking/se | 0.677 |
| scrapy+md | #2 | kubernetes.io/docs/concepts/_print/ | 0.736 | kubernetes.io/it/docs/concepts/architecture/contro | 0.702 | kubernetes.io/docs/concepts/_print/ | 0.688 |
| crawlee | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.736 | kubernetes.io/docs/concepts/architecture/control-p | 0.705 | kubernetes.io/docs/concepts/architecture/control-p | 0.703 |
| colly+md | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.736 | kubernetes.io/docs/concepts/architecture/control-p | 0.709 | kubernetes.io/docs/concepts/architecture/control-p | 0.703 |
| playwright | #1 | kubernetes.io/docs/concepts/architecture/control-p | 0.736 | kubernetes.io/docs/concepts/architecture/control-p | 0.709 | kubernetes.io/docs/concepts/architecture/control-p | 0.703 |


**Q31: What are the two sorts of isolation for a pod in Kubernetes NetworkPolicies?**
*(expects URL containing: `network-policies`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.817 | kubernetes.io/docs/concepts/services-networking/_p | 0.817 | kubernetes.io/docs/concepts/_print/ | 0.817 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.817 | kubernetes.io/docs/concepts/services-networking/ne | 0.807 | kubernetes.io/docs/concepts/services-networking/ne | 0.806 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.817 | kubernetes.io/docs/concepts/services-networking/ne | 0.807 | kubernetes.io/docs/concepts/services-networking/ne | 0.806 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.817 | kubernetes.io/docs/concepts/_print/ | 0.806 | kubernetes.io/blog/2021/10/05/nsa-cisa-kubernetes- | 0.805 |
| crawlee | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.817 | kubernetes.io/docs/concepts/services-networking/ne | 0.806 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.793 |
| colly+md | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.817 | kubernetes.io/docs/concepts/services-networking/ne | 0.806 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.793 |
| playwright | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.817 | kubernetes.io/docs/concepts/services-networking/ne | 0.806 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.793 |


**Q32: What must be used to implement NetworkPolicies in a Kubernetes cluster?**
*(expects URL containing: `network-policies`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.861 | kubernetes.io/docs/concepts/_print/ | 0.835 | kubernetes.io/docs/concepts/services-networking/ne | 0.835 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.851 | kubernetes.io/docs/concepts/services-networking/ | 0.844 | kubernetes.io/docs/concepts/services-networking/ne | 0.835 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.851 | kubernetes.io/docs/concepts/services-networking/ | 0.844 | kubernetes.io/docs/concepts/services-networking/ne | 0.835 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.835 | kubernetes.io/docs/concepts/_print/ | 0.810 | kubernetes.io/hi/docs/reference/glossary/?all=true | 0.809 |
| crawlee | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.851 | kubernetes.io/docs/concepts/services-networking/ne | 0.835 | kubernetes.io/docs/tasks/administer-cluster/declar | 0.813 |
| colly+md | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.851 | kubernetes.io/docs/concepts/services-networking/ne | 0.835 | kubernetes.io/docs/tasks/administer-cluster/declar | 0.813 |
| playwright | #1 | kubernetes.io/docs/concepts/services-networking/ne | 0.851 | kubernetes.io/docs/concepts/services-networking/ne | 0.835 | kubernetes.io/docs/tasks/administer-cluster/declar | 0.813 |


**Q33: What is the principle of least privilege in RBAC?**
*(expects URL containing: `rbac-good-practices`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.681 | kubernetes.io/docs/concepts/security/_print/ | 0.681 | kubernetes.io/docs/concepts/_print/ | 0.681 |
| crawl4ai | #2 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.681 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.638 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.637 |
| crawl4ai-raw | #2 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.681 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.638 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.637 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.681 | kubernetes.io/docs/concepts/_print/ | 0.646 | kubernetes.io/docs/concepts/_print/ | 0.638 |
| crawlee | #2 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.681 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.638 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.636 |
| colly+md | #2 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.681 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.638 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.636 |
| playwright | #2 | kubernetes.io/docs/concepts/security/multi-tenancy | 0.681 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.638 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.636 |


**Q34: How can users escalate their privileges in Kubernetes RBAC?**
*(expects URL containing: `rbac-good-practices`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.854 | kubernetes.io/docs/concepts/_print/ | 0.854 | kubernetes.io/docs/concepts/security/_print/ | 0.854 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.854 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.828 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.807 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.854 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.828 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.807 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.854 | kubernetes.io/docs/concepts/_print/ | 0.828 | kubernetes.io/docs/concepts/_print/ | 0.807 |
| crawlee | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.854 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.828 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.807 |
| colly+md | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.854 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.828 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.807 |
| playwright | #1 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.854 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.828 | kubernetes.io/docs/concepts/security/rbac-good-pra | 0.807 |


**Q35: How can pods created by a Job communicate with each other using hostnames?**
*(expects URL containing: `job-with-pod-to-pod-communication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/concepts/_print/ | 0.783 | kubernetes.io/docs/concepts/services-networking/_p | 0.783 | kubernetes.io/docs/concepts/services-networking/dn | 0.783 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.843 | kubernetes.io/docs/tasks/job/parallel-processing-e | 0.786 | kubernetes.io/docs/tasks/configure-pod-container/u | 0.782 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.843 | kubernetes.io/docs/tasks/job/parallel-processing-e | 0.786 | kubernetes.io/docs/tasks/configure-pod-container/u | 0.782 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.780 | kubernetes.io/docs/concepts/_print/ | 0.768 | kubernetes.io/docs/concepts/_print/ | 0.765 |
| crawlee | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.843 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.826 | kubernetes.io/docs/tasks/configure-pod-container/u | 0.790 |
| colly+md | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.843 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.826 | kubernetes.io/docs/tasks/configure-pod-container/u | 0.790 |
| playwright | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.843 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.826 | kubernetes.io/docs/tasks/configure-pod-container/u | 0.790 |


**Q36: What is the required configuration for a headless Service in a Job with pod-to-pod communication?**
*(expects URL containing: `job-with-pod-to-pod-communication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/concepts/_print/ | 0.731 | kubernetes.io/docs/concepts/services-networking/se | 0.731 | kubernetes.io/docs/concepts/services-networking/_p | 0.731 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.833 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.803 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.781 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.833 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.803 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.781 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.731 | kubernetes.io/zh-cn/feed.xml | 0.726 | kubernetes.io/docs/concepts/_print/ | 0.722 |
| crawlee | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.833 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.764 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.759 |
| colly+md | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.833 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.764 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.759 |
| playwright | #1 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.833 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.764 | kubernetes.io/docs/tasks/job/job-with-pod-to-pod-c | 0.759 |


**Q37: What is Node Problem Detector?**
*(expects URL containing: `monitor-node-health`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/concepts/_print/ | 0.631 | kubernetes.io/docs/concepts/scheduling-eviction/_p | 0.631 | kubernetes.io/docs/tasks/debug/debug-cluster/ | 0.626 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.784 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.728 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.714 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.784 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.728 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.714 |
| scrapy+md | miss | kubernetes.io/de/docs/_print/ | 0.643 | kubernetes.io/zh-cn/feed.xml | 0.632 | kubernetes.io/docs/concepts/_print/ | 0.631 |
| crawlee | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.786 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.723 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.706 |
| colly+md | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.786 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.723 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.706 |
| playwright | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.786 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.723 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.706 |


**Q38: How can you enable Node Problem Detector using kubectl?**
*(expects URL containing: `monitor-node-health`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/tasks/debug/debug-cluster/troub | 0.780 | kubernetes.io/docs/tasks/debug/debug-cluster/ | 0.774 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.757 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.852 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.820 | kubernetes.io/docs/tasks/debug/debug-cluster/ | 0.789 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.852 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.820 | kubernetes.io/docs/tasks/debug/debug-cluster/ | 0.789 |
| scrapy+md | miss | kubernetes.io/feed.xml | 0.746 | kubernetes.io/docs/concepts/_print/ | 0.733 | kubernetes.io/zh-cn/feed.xml | 0.730 |
| crawlee | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.856 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.822 | kubernetes.io/docs/tasks/debug/debug-cluster/ | 0.801 |
| colly+md | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.856 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.822 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.791 |
| playwright | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.856 | kubernetes.io/docs/tasks/debug/debug-cluster/monit | 0.822 | kubernetes.io/docs/tasks/debug/debug-cluster/ | 0.801 |


**Q39: What command is used to safely evict all pods from a node before maintenance?**
*(expects URL containing: `safely-drain-node`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.817 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.804 | kubernetes.io/docs/concepts/workloads/pods/_print/ | 0.800 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.809 | kubernetes.io/docs/concepts/workloads/pods/disrupt | 0.801 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.791 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.809 | kubernetes.io/docs/concepts/workloads/pods/disrupt | 0.801 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.791 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.800 | kubernetes.io/docs/concepts/scheduling-eviction/ta | 0.765 | kubernetes.io/docs/concepts/_print/ | 0.765 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.809 | kubernetes.io/docs/concepts/workloads/pods/disrupt | 0.800 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.791 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.808 | kubernetes.io/docs/concepts/workloads/pods/disrupt | 0.800 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.791 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.809 | kubernetes.io/docs/concepts/workloads/pods/disrupt | 0.800 | kubernetes.io/docs/tasks/administer-cluster/safely | 0.791 |


**Q40: What should you configure to ensure workloads remain available during maintenance?**
*(expects URL containing: `safely-drain-node`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/concepts/workloads/_print/ | 0.676 | kubernetes.io/docs/concepts/workloads/ | 0.676 | kubernetes.io/docs/concepts/_print/ | 0.672 |
| crawl4ai | #27 | kubernetes.io/docs/concepts/cluster-administration | 0.664 | kubernetes.io/docs/concepts/workloads/ | 0.659 | kubernetes.io/docs/concepts/cluster-administration | 0.653 |
| crawl4ai-raw | #27 | kubernetes.io/docs/concepts/cluster-administration | 0.664 | kubernetes.io/docs/concepts/workloads/ | 0.659 | kubernetes.io/docs/concepts/cluster-administration | 0.653 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.672 | kubernetes.io/docs/concepts/_print/ | 0.664 | kubernetes.io/docs/concepts/_print/ | 0.653 |
| crawlee | #31 | kubernetes.io/docs/concepts/workloads/ | 0.675 | kubernetes.io/docs/concepts/cluster-administration | 0.664 | kubernetes.io/docs/concepts/workloads/ | 0.656 |
| colly+md | #28 | kubernetes.io/docs/concepts/workloads/ | 0.676 | kubernetes.io/docs/concepts/cluster-administration | 0.664 | kubernetes.io/docs/concepts/cluster-administration | 0.653 |
| playwright | #30 | kubernetes.io/docs/concepts/workloads/ | 0.675 | kubernetes.io/docs/concepts/cluster-administration | 0.664 | kubernetes.io/docs/concepts/workloads/ | 0.656 |


**Q41: What is Kubernetes?**
*(expects URL containing: `concepts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/overview/ | 0.893 | kubernetes.io/docs/concepts/overview/_print/ | 0.862 | kubernetes.io/docs/concepts/_print/ | 0.833 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/overview/ | 0.824 | v1-35.docs.kubernetes.io/docs/concepts/ | 0.823 | kubernetes.io/docs/concepts/ | 0.813 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/overview/ | 0.824 | v1-35.docs.kubernetes.io/docs/concepts/ | 0.823 | kubernetes.io/docs/concepts/ | 0.813 |
| scrapy+md | #1 | kubernetes.io/docs/concepts/_print/ | 0.833 | kubernetes.io/docs/concepts/_print/ | 0.820 | kubernetes.io/docs/concepts/ | 0.812 |
| crawlee | #1 | kubernetes.io/docs/concepts/overview/ | 0.833 | kubernetes.io/docs/concepts/ | 0.832 | kubernetes.io/docs/concepts/overview/ | 0.820 |
| colly+md | #1 | kubernetes.io/docs/concepts/overview/ | 0.833 | kubernetes.io/docs/concepts/ | 0.832 | kubernetes.io/docs/concepts/overview/ | 0.820 |
| playwright | #1 | kubernetes.io/docs/concepts/overview/ | 0.833 | kubernetes.io/docs/concepts/ | 0.832 | kubernetes.io/docs/concepts/overview/ | 0.820 |


**Q42: How do I change the default StorageClass in Kubernetes?**
*(expects URL containing: `change-default-storage-class`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/concepts/storage/_print/ | 0.816 | kubernetes.io/docs/concepts/_print/ | 0.816 | kubernetes.io/docs/concepts/storage/storage-classe | 0.816 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.856 | kubernetes.io/docs/tasks/administer-cluster/change | 0.826 | kubernetes.io/docs/concepts/storage/storage-classe | 0.816 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.856 | kubernetes.io/docs/tasks/administer-cluster/change | 0.826 | kubernetes.io/docs/concepts/storage/storage-classe | 0.816 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.816 | kubernetes.io/docs/concepts/_print/ | 0.782 | kubernetes.io/docs/concepts/_print/ | 0.782 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.885 | kubernetes.io/docs/tasks/administer-cluster/change | 0.867 | kubernetes.io/docs/tasks/administer-cluster/change | 0.856 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.885 | kubernetes.io/docs/tasks/administer-cluster/change | 0.856 | kubernetes.io/docs/tasks/administer-cluster/change | 0.851 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.885 | kubernetes.io/docs/tasks/administer-cluster/change | 0.856 | kubernetes.io/docs/tasks/administer-cluster/change | 0.851 |


**Q43: Why might I want to change the default StorageClass?**
*(expects URL containing: `change-default-storage-class`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | kubernetes.io/docs/concepts/_print/ | 0.724 | kubernetes.io/docs/concepts/storage/_print/ | 0.724 | kubernetes.io/docs/concepts/storage/storage-classe | 0.724 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.758 | kubernetes.io/docs/tasks/administer-cluster/change | 0.742 | kubernetes.io/docs/concepts/storage/persistent-vol | 0.721 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.758 | kubernetes.io/docs/tasks/administer-cluster/change | 0.742 | kubernetes.io/docs/concepts/storage/persistent-vol | 0.721 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.724 | kubernetes.io/docs/concepts/_print/ | 0.721 | kubernetes.io/docs/concepts/_print/ | 0.708 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.795 | kubernetes.io/docs/tasks/administer-cluster/change | 0.756 | kubernetes.io/docs/tasks/administer-cluster/change | 0.742 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.795 | kubernetes.io/docs/tasks/administer-cluster/change | 0.742 | kubernetes.io/docs/tasks/administer-cluster/change | 0.741 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/change | 0.795 | kubernetes.io/docs/tasks/administer-cluster/change | 0.742 | kubernetes.io/docs/tasks/administer-cluster/change | 0.741 |


**Q44: What is a kubeconfig file?**
*(expects URL containing: `organize-cluster-access-kubeconfig`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.832 | kubernetes.io/docs/reference/setup-tools/kubeadm/k | 0.821 | kubernetes.io/docs/reference/setup-tools/kubeadm/k | 0.789 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.816 | kubernetes.io/docs/concepts/configuration/organize | 0.787 | kubernetes.io/docs/concepts/configuration/organize | 0.747 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.816 | kubernetes.io/docs/concepts/configuration/organize | 0.787 | kubernetes.io/docs/concepts/configuration/organize | 0.747 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.783 | kubernetes.io/docs/concepts/_print/ | 0.756 | kubernetes.io/feed.xml | 0.732 |
| crawlee | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.816 | kubernetes.io/docs/concepts/configuration/organize | 0.783 | kubernetes.io/docs/tasks/access-application-cluste | 0.774 |
| colly+md | miss | kubernetes.io/docs/concepts/configuration/organize | 0.816 | kubernetes.io/docs/concepts/configuration/organize | 0.783 | kubernetes.io/docs/tasks/access-application-cluste | 0.774 |
| playwright | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.816 | kubernetes.io/docs/concepts/configuration/organize | 0.783 | kubernetes.io/docs/tasks/access-application-cluste | 0.774 |


**Q45: How does kubectl determine which kubeconfig file to use?**
*(expects URL containing: `organize-cluster-access-kubeconfig`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.804 | kubernetes.io/docs/concepts/configuration/_print/ | 0.804 | kubernetes.io/docs/concepts/_print/ | 0.804 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.788 | kubernetes.io/docs/concepts/configuration/organize | 0.787 | kubernetes.io/docs/concepts/configuration/organize | 0.742 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.788 | kubernetes.io/docs/concepts/configuration/organize | 0.787 | kubernetes.io/docs/concepts/configuration/organize | 0.742 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.804 | kubernetes.io/docs/concepts/_print/ | 0.743 | kubernetes.io/docs/reference/generated/kubectl/kub | 0.734 |
| crawlee | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.804 | kubernetes.io/docs/concepts/configuration/organize | 0.789 | kubernetes.io/docs/concepts/configuration/organize | 0.743 |
| colly+md | miss | kubernetes.io/docs/concepts/configuration/organize | 0.804 | kubernetes.io/docs/concepts/configuration/organize | 0.789 | kubernetes.io/docs/concepts/configuration/organize | 0.743 |
| playwright | #1 | kubernetes.io/docs/concepts/configuration/organize | 0.804 | kubernetes.io/docs/concepts/configuration/organize | 0.789 | kubernetes.io/docs/concepts/configuration/organize | 0.743 |


**Q46: What is dynamic volume provisioning in Kubernetes?**
*(expects URL containing: `dynamic-provisioning`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.885 | kubernetes.io/docs/concepts/storage/_print/ | 0.831 | kubernetes.io/docs/concepts/_print/ | 0.831 |
| crawl4ai | #3 | kubernetes.io/docs/concepts/storage/persistent-vol | 0.798 | kubernetes.io/docs/concepts/storage/storage-classe | 0.784 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.781 |
| crawl4ai-raw | #3 | kubernetes.io/docs/concepts/storage/persistent-vol | 0.798 | kubernetes.io/docs/concepts/storage/storage-classe | 0.784 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.781 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.830 | kubernetes.io/docs/concepts/_print/ | 0.799 | kubernetes.io/uk/docs/reference/glossary/ | 0.788 |
| crawlee | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.831 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.830 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.824 |
| colly+md | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.831 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.830 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.801 |
| playwright | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.831 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.830 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.801 |


**Q47: How can a cluster administrator enable dynamic provisioning?**
*(expects URL containing: `dynamic-provisioning`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.789 | kubernetes.io/docs/concepts/_print/ | 0.773 | kubernetes.io/docs/concepts/storage/_print/ | 0.773 |
| crawl4ai | #3 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.752 | kubernetes.io/docs/concepts/scheduling-eviction/dy | 0.752 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.751 |
| crawl4ai-raw | #3 | kubernetes.io/docs/tasks/administer-cluster/kubele | 0.752 | kubernetes.io/docs/concepts/scheduling-eviction/dy | 0.752 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.751 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.774 | kubernetes.io/docs/concepts/_print/ | 0.737 | kubernetes.io/feed.xml | 0.731 |
| crawlee | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.774 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.770 | kubernetes.io/docs/concepts/cluster-administration | 0.746 |
| colly+md | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.774 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.770 | kubernetes.io/docs/concepts/cluster-administration | 0.746 |
| playwright | #1 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.774 | kubernetes.io/docs/concepts/storage/dynamic-provis | 0.770 | kubernetes.io/docs/concepts/cluster-administration | 0.746 |


**Q48: What command-line flag is used to enable the API Priority and Fairness feature?**
*(expects URL containing: `flow-control`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | kubernetes.io/docs/concepts/cluster-administration | 0.812 | kubernetes.io/docs/concepts/_print/ | 0.812 | kubernetes.io/docs/concepts/cluster-administration | 0.809 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.811 | kubernetes.io/docs/concepts/cluster-administration | 0.754 | kubernetes.io/docs/concepts/cluster-administration | 0.734 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.811 | kubernetes.io/docs/concepts/cluster-administration | 0.754 | kubernetes.io/docs/concepts/cluster-administration | 0.734 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.809 | kubernetes.io/docs/concepts/_print/ | 0.753 | kubernetes.io/docs/concepts/_print/ | 0.709 |
| crawlee | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.809 | kubernetes.io/docs/concepts/cluster-administration | 0.753 | kubernetes.io/docs/concepts/cluster-administration | 0.739 |
| colly+md | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.809 | kubernetes.io/docs/concepts/cluster-administration | 0.753 | kubernetes.io/docs/concepts/cluster-administration | 0.735 |
| playwright | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.809 | kubernetes.io/docs/concepts/cluster-administration | 0.753 | kubernetes.io/docs/concepts/cluster-administration | 0.735 |


**Q49: What are the two types of resources involved in the flow control API?**
*(expects URL containing: `flow-control`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | kubernetes.io/docs/reference/generated/kubernetes- | 0.724 | kubernetes.io/docs/reference/generated/kubernetes- | 0.723 | kubernetes.io/docs/reference/generated/kubernetes- | 0.708 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.703 | kubernetes.io/docs/concepts/extend-kubernetes/api- | 0.681 | kubernetes.io/docs/concepts/extend-kubernetes/api- | 0.677 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.703 | kubernetes.io/docs/concepts/extend-kubernetes/api- | 0.681 | kubernetes.io/docs/concepts/extend-kubernetes/api- | 0.677 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.703 | kubernetes.io/docs/concepts/_print/ | 0.680 | kubernetes.io/ko/docs/reference/glossary/?all=true | 0.678 |
| crawlee | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.703 | kubernetes.io/docs/concepts/extend-kubernetes/api- | 0.681 | kubernetes.io/docs/concepts/cluster-administration | 0.680 |
| colly+md | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.703 | kubernetes.io/docs/concepts/extend-kubernetes/api- | 0.681 | kubernetes.io/docs/concepts/cluster-administration | 0.680 |
| playwright | #1 | kubernetes.io/docs/concepts/cluster-administration | 0.703 | kubernetes.io/docs/concepts/extend-kubernetes/api- | 0.681 | kubernetes.io/docs/concepts/cluster-administration | 0.680 |


**Q50: What are the main components of a Kubernetes cluster?**
*(expects URL containing: `architecture`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | kubernetes.io/docs/concepts/overview/components/ | 0.898 | kubernetes.io/docs/concepts/_print/ | 0.893 | kubernetes.io/docs/concepts/overview/_print/ | 0.892 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/architecture/ | 0.831 | v1-35.docs.kubernetes.io/docs/concepts/ | 0.790 | kubernetes.io/docs/concepts/ | 0.788 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/architecture/ | 0.831 | v1-35.docs.kubernetes.io/docs/concepts/ | 0.790 | kubernetes.io/docs/concepts/ | 0.788 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.895 | kubernetes.io/docs/concepts/_print/ | 0.835 | kubernetes.io/it/docs/concepts/overview/components | 0.803 |
| crawlee | #2 | kubernetes.io/docs/concepts/overview/components/ | 0.895 | kubernetes.io/docs/concepts/architecture/ | 0.849 | kubernetes.io/docs/concepts/overview/components/ | 0.807 |
| colly+md | #2 | kubernetes.io/docs/concepts/overview/components/ | 0.895 | kubernetes.io/docs/concepts/architecture/ | 0.849 | kubernetes.io/docs/concepts/overview/components/ | 0.807 |
| playwright | #2 | kubernetes.io/docs/concepts/overview/components/ | 0.895 | kubernetes.io/docs/concepts/architecture/ | 0.849 | kubernetes.io/docs/concepts/overview/components/ | 0.807 |


**Q51: What is the role of the kube-scheduler in a Kubernetes cluster?**
*(expects URL containing: `architecture`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #50 | kubernetes.io/docs/reference/command-line-tools-re | 0.872 | kubernetes.io/docs/concepts/scheduling-eviction/sc | 0.841 | kubernetes.io/docs/concepts/scheduling-eviction/ku | 0.838 |
| crawl4ai | #24 | kubernetes.io/docs/concepts/security/hardening-gui | 0.795 | kubernetes.io/docs/concepts/scheduling-eviction/sc | 0.794 | kubernetes.io/docs/concepts/scheduling-eviction/sc | 0.788 |
| crawl4ai-raw | #24 | kubernetes.io/docs/concepts/security/hardening-gui | 0.795 | kubernetes.io/docs/concepts/scheduling-eviction/sc | 0.794 | kubernetes.io/docs/concepts/scheduling-eviction/sc | 0.788 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.837 | kubernetes.io/feed.xml | 0.804 | kubernetes.io/docs/concepts/_print/ | 0.793 |
| crawlee | #31 | kubernetes.io/docs/concepts/scheduling-eviction/ku | 0.846 | kubernetes.io/docs/concepts/security/hardening-gui | 0.795 | kubernetes.io/docs/concepts/scheduling-eviction/sc | 0.795 |
| colly+md | #31 | kubernetes.io/docs/concepts/scheduling-eviction/ku | 0.846 | kubernetes.io/docs/concepts/security/hardening-gui | 0.795 | kubernetes.io/docs/concepts/scheduling-eviction/sc | 0.795 |
| playwright | #31 | kubernetes.io/docs/concepts/scheduling-eviction/ku | 0.846 | kubernetes.io/docs/concepts/security/hardening-gui | 0.795 | kubernetes.io/docs/concepts/scheduling-eviction/sc | 0.795 |


**Q52: What is the purpose of Kubernetes auditing?**
*(expects URL containing: `audit`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.876 | kubernetes.io/docs/concepts/security/_print/ | 0.821 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.779 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.850 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.778 | kubernetes.io/docs/concepts/security/cloud-native- | 0.760 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.850 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.778 | kubernetes.io/docs/concepts/security/cloud-native- | 0.760 |
| scrapy+md | miss | kubernetes.io/blog/2021/10/05/nsa-cisa-kubernetes- | 0.817 | kubernetes.io/blog/2021/12/09/pod-security-admissi | 0.779 | kubernetes.io/docs/concepts/_print/ | 0.743 |
| crawlee | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.849 | kubernetes.io/docs/concepts/security/ | 0.821 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.790 |
| colly+md | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.849 | kubernetes.io/docs/concepts/security/ | 0.821 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.778 |
| playwright | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.849 | kubernetes.io/docs/concepts/security/ | 0.821 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.778 |


**Q53: What are the defined stages for audit events in Kubernetes?**
*(expects URL containing: `audit`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.866 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.794 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.779 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.857 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.794 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.788 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.857 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.794 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.788 |
| scrapy+md | miss | kubernetes.io/blog/2021/12/09/pod-security-admissi | 0.760 | kubernetes.io/blog/2021/10/05/nsa-cisa-kubernetes- | 0.742 | kubernetes.io/blog/2021/10/05/nsa-cisa-kubernetes- | 0.739 |
| crawlee | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.856 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.794 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.780 |
| colly+md | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.856 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.794 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.780 |
| playwright | #1 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.856 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.794 | kubernetes.io/docs/tasks/debug/debug-cluster/audit | 0.780 |


**Q54: What is the example YAML file used to deploy a simple webserver application running inside a Windows container?**
*(expects URL containing: `user-guide`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.823 | kubernetes.io/docs/concepts/_print/ | 0.762 | kubernetes.io/docs/concepts/windows/_print/ | 0.762 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.772 | kubernetes.io/docs/concepts/workloads/pods/init-co | 0.731 | kubernetes.io/docs/tasks/debug/debug-cluster/windo | 0.730 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.772 | kubernetes.io/docs/concepts/workloads/pods/init-co | 0.731 | kubernetes.io/docs/tasks/debug/debug-cluster/windo | 0.730 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.761 | kubernetes.io/zh-cn/feed.xml | 0.736 | kubernetes.io/docs/concepts/_print/ | 0.731 |
| crawlee | #1 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.770 | kubernetes.io/docs/concepts/workloads/pods/init-co | 0.731 | kubernetes.io/docs/tasks/manage-kubernetes-objects | 0.717 |
| colly+md | #1 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.770 | kubernetes.io/docs/concepts/workloads/pods/init-co | 0.731 | kubernetes.io/docs/tasks/manage-kubernetes-objects | 0.717 |
| playwright | #1 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.770 | kubernetes.io/docs/concepts/workloads/pods/init-co | 0.731 | kubernetes.io/docs/tasks/manage-kubernetes-objects | 0.717 |


**Q55: How can Windows container workloads be configured to use Group Managed Service Accounts (GMSA)?**
*(expects URL containing: `user-guide`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.796 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.781 | kubernetes.io/docs/concepts/_print/ | 0.764 |
| crawl4ai | #2 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.783 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.764 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.751 |
| crawl4ai-raw | #2 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.783 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.764 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.751 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.764 | kubernetes.io/zh-cn/docs/reference/kubernetes-api/ | 0.701 | kubernetes.io/docs/concepts/_print/ | 0.685 |
| crawlee | #2 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.783 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.764 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.751 |
| colly+md | #2 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.783 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.764 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.751 |
| playwright | #2 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.783 | kubernetes.io/docs/concepts/windows/user-guide/ | 0.764 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.751 |


**Q56: How do I define a default memory resource limit for a namespace?**
*(expects URL containing: `manage-resources`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.751 | kubernetes.io/docs/reference/generated/kubernetes- | 0.715 | kubernetes.io/docs/tasks/configure-pod-container/a | 0.707 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.756 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.740 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.726 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.756 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.740 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.726 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.698 | kubernetes.io/docs/concepts/_print/ | 0.694 | kubernetes.io/docs/reference/generated/kubectl/kub | 0.692 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.777 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.760 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.744 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.777 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.760 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.744 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.777 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.760 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.744 |


**Q57: What is the purpose of configuring overall memory and CPU resource limits for a namespace?**
*(expects URL containing: `manage-resources`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.802 | kubernetes.io/docs/concepts/policy/_print/ | 0.729 | kubernetes.io/docs/tasks/configure-pod-container/a | 0.728 |
| crawl4ai | #2 | kubernetes.io/docs/tasks/configure-pod-container/r | 0.769 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.745 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.740 |
| crawl4ai-raw | #2 | kubernetes.io/docs/tasks/configure-pod-container/r | 0.769 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.745 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.740 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.724 | kubernetes.io/docs/concepts/_print/ | 0.722 | kubernetes.io/docs/concepts/_print/ | 0.716 |
| crawlee | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.819 | kubernetes.io/docs/tasks/configure-pod-container/r | 0.784 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.756 |
| colly+md | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.819 | kubernetes.io/docs/tasks/configure-pod-container/r | 0.784 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.756 |
| playwright | #1 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.819 | kubernetes.io/docs/tasks/configure-pod-container/r | 0.784 | kubernetes.io/docs/tasks/administer-cluster/manage | 0.756 |


</details>

## mdn-css

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai | 83% (50/60) | 93% (56/60) | 98% (59/60) | 100% (60/60) | 100% (60/60) | 0.892 | 3864 | 300 |
| crawl4ai-raw | 83% (50/60) | 93% (56/60) | 98% (59/60) | 100% (60/60) | 100% (60/60) | 0.892 | 3864 | 300 |
| crawlee | 82% (49/60) | 95% (57/60) | 98% (59/60) | 100% (60/60) | 100% (60/60) | 0.891 | 3891 | 300 |
| playwright | 80% (48/60) | 92% (55/60) | 97% (58/60) | 100% (60/60) | 100% (60/60) | 0.870 | 4168 | 300 |
| markcrawl | 28% (17/60) | 35% (21/60) | 35% (21/60) | 38% (23/60) | 42% (25/60) | 0.317 | 1006 | 300 |
| colly+md | 15% (9/60) | 20% (12/60) | 20% (12/60) | 23% (14/60) | 23% (14/60) | 0.172 | 4190 | 289 |
| scrapy+md | 3% (2/60) | 3% (2/60) | 3% (2/60) | 3% (2/60) | 3% (2/60) | 0.033 | 621 | 300 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for mdn-css</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is masonry layout in CSS?**
*(expects URL containing: `Masonry_layout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.864 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.779 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.764 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.824 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.802 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.785 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.824 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.802 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.785 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.691 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.670 | developer.mozilla.org/en-US/docs/Web/CSS | 0.664 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.811 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.789 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.776 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.775 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.772 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.750 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.803 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.789 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.789 |


**Q2: How do you create a masonry layout using CSS?**
*(expects URL containing: `Masonry_layout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.822 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.812 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.773 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.803 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.785 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.776 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.803 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.785 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.776 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS | 0.700 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.697 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.686 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.797 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.780 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.768 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.794 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.764 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.761 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.806 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.780 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.780 |


**Q3: What properties are used to define scroll snapping in CSS?**
*(expects URL containing: `Basic_concepts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.905 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.859 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.848 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.857 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.836 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.817 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.857 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.836 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.817 |
| scrapy+md | miss | developer.mozilla.org/ja/docs/Web/CSS/Reference/Pr | 0.729 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.688 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.665 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.872 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.825 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.823 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.885 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.832 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.825 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.863 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.832 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.825 |


**Q4: What does the scroll-snap-type property determine?**
*(expects URL containing: `Basic_concepts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.843 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.828 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.819 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.815 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.808 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.791 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.815 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.808 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.791 |
| scrapy+md | miss | developer.mozilla.org/ja/docs/Web/CSS/Reference/Pr | 0.697 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.621 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.615 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.816 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.809 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.805 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.833 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.809 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.795 |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.809 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.801 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.795 |


**Q5: What are OpenType features in fonts?**
*(expects URL containing: `OpenType_fonts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.775 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.704 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.699 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.820 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.812 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.775 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.820 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.812 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.775 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/HTML/Referenc | 0.592 | developer.mozilla.org/ja/docs/Web/CSS/Reference/Pr | 0.586 | developer.mozilla.org/fr/docs/Web/JavaScript/Refer | 0.583 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.811 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.792 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.775 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.803 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.775 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.724 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.803 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.792 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.775 |


**Q6: How can I enable ligatures in CSS?**
*(expects URL containing: `OpenType_fonts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.723 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.705 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.704 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.759 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.722 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.704 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.759 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.722 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.704 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.692 | developer.mozilla.org/en-US/docs/Web/HTML/Referenc | 0.660 | developer.mozilla.org/en-US/docs/Web/CSS | 0.646 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.758 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.722 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.711 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.742 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.701 | developer.mozilla.org/en-US/docs/Learn/web/develop | 0.698 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.742 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fo | 0.711 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.698 |


**Q7: What does the border-radius CSS property do?**
*(expects URL containing: `border-radius`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #7 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.841 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.841 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.823 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.819 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.793 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.819 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.793 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.702 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.670 | developer.mozilla.org/en-US/docs/Web/HTML/Referenc | 0.664 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.829 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.788 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.860 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.795 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.791 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.817 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.809 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.793 |


**Q8: How can you specify multiple radii using the border-radius property?**
*(expects URL containing: `border-radius`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.761 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.760 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.735 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.768 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.756 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.728 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.768 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.756 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.728 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.648 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.644 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.617 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.774 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.767 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.733 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.785 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.767 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.735 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.767 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.762 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.741 |


**Q9: What properties control breaks inside boxes in a multicol layout?**
*(expects URL containing: `Handling_content_breaks`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/How_to/La | 0.757 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.733 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.725 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.784 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.778 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.777 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.784 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.778 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.777 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.683 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.649 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.648 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.807 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.787 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fr | 0.763 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.804 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.788 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.764 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.787 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.777 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.764 |


**Q10: How can you prevent a caption from being separated from its image in a multicol layout?**
*(expects URL containing: `Handling_content_breaks`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/How_to/La | 0.713 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.674 | developer.mozilla.org/en-US/docs/Web/CSS/How_to/La | 0.660 |
| crawl4ai | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.708 | developer.mozilla.org/en-US/docs/Web/CSS/How_to/La | 0.690 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.688 |
| crawl4ai-raw | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.708 | developer.mozilla.org/en-US/docs/Web/CSS/How_to/La | 0.690 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.688 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.618 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.611 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.603 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.702 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.695 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.692 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.743 | developer.mozilla.org/en-US/docs/Web/CSS/How/to/La | 0.717 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.712 |
| playwright | #4 | developer.mozilla.org/en-US/docs/Web/CSS/How_to/La | 0.717 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.712 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.703 |


**Q11: What properties does the CSS borders and box decorations module provide?**
*(expects URL containing: `Borders_and_box_decorations`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.851 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.792 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.788 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.845 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.845 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.843 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.845 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.845 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.843 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.755 | developer.mozilla.org/en-US/docs/Web/CSS | 0.735 | developer.mozilla.org/zh-CN/docs/Web/HTTP/Referenc | 0.707 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.851 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.841 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.840 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.851 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.817 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.807 |
| playwright | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.851 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.812 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.808 |


**Q12: What new features does the CSS borders and box decorations module level 4 introduce?**
*(expects URL containing: `Borders_and_box_decorations`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.813 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.778 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.777 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.852 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.814 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.814 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.852 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.814 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.814 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.740 | developer.mozilla.org/en-US/docs/Web/CSS | 0.732 | developer.mozilla.org/en-US/docs/Web/CSS | 0.700 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.813 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.804 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.801 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.813 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.789 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.780 |
| playwright | #9 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.813 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.789 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.789 |


**Q13: What are the six keywords accepted by the <timeline-range-name> value type?**
*(expects URL containing: `Timeline_range_names`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.744 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.711 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.654 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.705 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.658 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.658 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.705 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.658 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.658 |
| scrapy+md | miss | developer.mozilla.org/fr/docs/Web/JavaScript/Refer | 0.593 | developer.mozilla.org/ja/docs/Web/JavaScript/Refer | 0.593 | developer.mozilla.org/en-US/docs/Web/JavaScript/Re | 0.587 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.703 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.683 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.669 |
| colly+md | miss | developer.mozilla.org/ru/docs/Web/CSS | 0.635 | developer.mozilla.org/ko/docs/Web/CSS | 0.629 | developer.mozilla.org/zh-TW/docs/Web/CSS | 0.628 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.742 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.683 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.651 |


**Q14: How does the 'contain' named timeline range function in relation to the scrollport?**
*(expects URL containing: `Timeline_range_names`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.800 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.764 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.739 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.827 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.793 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.790 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.827 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.793 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.790 |
| scrapy+md | miss | developer.mozilla.org/ja/docs/Web/CSS/Reference/Pr | 0.663 | developer.mozilla.org/ja/docs/Web/CSS/Reference/Pr | 0.640 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.636 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.817 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.790 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.781 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.775 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.772 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.757 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.799 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.794 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.772 |


**Q15: How do browsers handle CSS errors when they encounter invalid values or missing semicolons?**
*(expects URL containing: `Error_handling`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.749 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.728 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.726 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.855 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.831 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.855 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.831 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.730 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.702 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.699 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.868 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.831 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.834 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.830 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.825 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.868 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.830 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.830 |


**Q16: What happens to a CSS declaration block if it contains an invalid selector?**
*(expects URL containing: `Error_handling`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ne | 0.780 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.729 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.725 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.845 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.839 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.808 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.845 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.839 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.808 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.685 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.684 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.683 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.845 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.838 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.808 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.838 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.810 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.838 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.810 |


**Q17: What is the alignment container in multi-column layout?**
*(expects URL containing: `In_multi-column_layout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.759 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.757 | developer.mozilla.org/en-US/docs/Web/CSS/How_to/La | 0.753 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.844 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.807 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.796 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.844 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.807 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.796 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.682 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.665 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.639 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.845 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.803 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.780 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.843 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.794 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.781 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.845 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.803 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.780 |


**Q18: How does the column-gap property behave in multi-column layout?**
*(expects URL containing: `In_multi-column_layout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.792 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.785 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.854 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.799 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.799 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.854 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.799 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.799 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.660 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.657 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.643 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.845 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.804 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.795 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.814 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.814 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.798 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.845 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.804 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mu | 0.787 |


**Q19: What is the initial viewport?**
*(expects URL containing: `Viewport_concepts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.748 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.714 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.701 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.728 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.712 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.675 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.728 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.712 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.675 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/API/VideoFram | 0.586 | developer.mozilla.org/de/docs/Web/SVG/Reference/At | 0.580 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.556 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.753 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.701 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.675 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.753 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.701 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.661 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.753 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.701 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.675 |


**Q20: How does the viewport meta tag affect the actual viewport?**
*(expects URL containing: `Viewport_concepts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.776 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.739 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.738 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.771 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.747 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.732 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.771 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.747 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Vi | 0.732 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.632 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.628 | developer.mozilla.org/en-US/docs/Web/HTML/Referenc | 0.625 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.777 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.747 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.738 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.777 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.740 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.738 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.777 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.740 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.738 |


**Q21: What are the most commonly-used CSS data types?**
*(expects URL containing: `Data_types`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.801 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.769 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.832 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.799 | developer.mozilla.org/en-US/docs/Web/CSS | 0.790 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.832 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.799 | developer.mozilla.org/en-US/docs/Web/CSS | 0.790 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.735 | developer.mozilla.org/en-US/docs/Web/CSS | 0.719 | developer.mozilla.org/en-US/docs/Web/HTML/Referenc | 0.712 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.824 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.796 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.772 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.807 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.796 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.780 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.824 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.796 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.771 |


**Q22: How are CSS data types denoted in formal CSS syntax?**
*(expects URL containing: `Data_types`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.855 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.842 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.812 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.858 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.839 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.830 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.858 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.839 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.830 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.758 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.745 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.745 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.871 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.839 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.831 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.882 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.831 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.806 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.871 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.838 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.831 |


**Q23: What are the basic building blocks of CSS syntax?**
*(expects URL containing: `Introduction`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #24 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.793 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.761 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.760 |
| crawl4ai | #4 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.799 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.798 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.788 |
| crawl4ai-raw | #4 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.799 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.798 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.788 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.761 | developer.mozilla.org/en-US/docs/Web/CSS | 0.742 | developer.mozilla.org/en-US/docs/Web/CSS | 0.734 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.784 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.781 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.778 |
| colly+md | #6 | developer.mozilla.org/en-US/docs/Learn/web/develop | 0.793 | developer.mozilla.org/en-US/docs/Learn/web/develop | 0.777 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.776 |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.784 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.781 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.781 |


**Q24: What is a CSS declaration and how is it structured?**
*(expects URL containing: `Introduction`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #12 | developer.mozilla.org/en-US/docs/Web/CSS | 0.804 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.779 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.776 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.814 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.782 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.814 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.782 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS | 0.784 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.749 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.718 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.806 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.801 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.777 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.822 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.805 | developer.mozilla.org/en-US/docs/Learn/web/develop | 0.791 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.806 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.801 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.791 |


**Q25: What property is used to set a threshold for opacity when creating shapes from images?**
*(expects URL containing: `From_images`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.812 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.809 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.761 |
| crawl4ai | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.798 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.757 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.754 |
| crawl4ai-raw | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.798 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.757 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.754 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.657 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.639 | developer.mozilla.org/de/docs/Web/SVG/Reference/At | 0.633 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.798 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.781 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.757 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.835 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.783 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.856 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.783 |


**Q26: How can you create shapes using a CSS gradient?**
*(expects URL containing: `From_images`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.777 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.735 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.728 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.819 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.802 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.788 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.819 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.802 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.788 |
| scrapy+md | miss | developer.mozilla.org/de/docs/Web/SVG/Reference/At | 0.722 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.683 | developer.mozilla.org/en-US/docs/Web/CSS | 0.665 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.813 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.807 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.790 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.811 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.802 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.797 |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.808 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.797 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.785 |


**Q27: What does the CSS scoping module define?**
*(expects URL containing: `Scoping`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.788 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.768 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.767 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.803 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.772 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.760 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.803 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.772 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.760 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.740 | developer.mozilla.org/en-US/docs/Web/CSS | 0.719 | developer.mozilla.org/en-US/docs/Web/CSS | 0.717 |
| crawlee | #4 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.788 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.768 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.766 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.839 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.788 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.768 |
| playwright | #4 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.788 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.768 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.766 |


**Q28: How do selectors behave within a shadow tree in CSS?**
*(expects URL containing: `Scoping`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.747 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.730 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.727 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.772 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.755 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.726 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.772 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.755 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.726 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.687 | developer.mozilla.org/zh-CN/docs/Web/HTTP/Referenc | 0.660 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.647 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.764 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.747 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.726 |
| colly+md | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sh | 0.756 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.747 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.744 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.764 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.747 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.732 |


**Q29: What does the CSS counter styles module allow you to define?**
*(expects URL containing: `Counter_styles`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.850 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.816 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.808 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.868 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.847 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.830 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.868 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.847 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.830 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.728 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.728 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.708 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.869 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Li | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.831 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.859 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Li | 0.846 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.801 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.869 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Li | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.831 |


**Q30: How many descriptors does the @counter-style rule define?**
*(expects URL containing: `Counter_styles`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #6 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.713 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.710 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.707 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.732 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.710 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.695 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.732 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.710 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.695 |
| scrapy+md | miss | developer.mozilla.org/ja/docs/Web/JavaScript/Refer | 0.648 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.642 | developer.mozilla.org/ko/docs/Web/JavaScript/Refer | 0.628 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Li | 0.747 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.743 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.741 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.691 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.674 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.673 |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Li | 0.747 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.743 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.741 |


**Q31: What is CSS typed arithmetic?**
*(expects URL containing: `Using_typed_arithmetic`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.822 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.799 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.770 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.848 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.800 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.794 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.848 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.800 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.794 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.692 | developer.mozilla.org/en-US/docs/Web/HTML/Referenc | 0.685 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.682 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.831 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.805 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.774 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.756 | developer.mozilla.org/zh-TW/docs/Web/CSS | 0.749 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.852 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.812 |


**Q32: How does division work in CSS typed arithmetic?**
*(expects URL containing: `Using_typed_arithmetic`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.818 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.786 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.766 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.833 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.831 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.813 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.833 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.831 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.813 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.678 | developer.mozilla.org/en-US/docs/Web/HTML/Referenc | 0.650 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.649 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.845 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.838 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.813 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.736 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.722 | developer.mozilla.org/zh-TW/docs/Web/CSS | 0.718 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.838 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.838 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.831 |


**Q33: What is a replaced element in CSS?**
*(expects URL containing: `Replaced_element_properties`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.826 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.746 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.731 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.794 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.716 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.711 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.794 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.716 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.711 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.743 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.717 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.698 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.798 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.745 | developer.mozilla.org/en-US/docs/Web/HTML/Referenc | 0.715 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.817 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.767 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.735 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.798 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.745 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.737 |


**Q34: How does the object-fit property affect replaced elements?**
*(expects URL containing: `Replaced_element_properties`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.806 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.803 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.752 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.808 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.750 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.737 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.808 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.750 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.737 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.794 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.697 | developer.mozilla.org/fr/docs/Web/JavaScript/Refer | 0.658 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.760 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.741 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.807 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.760 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.760 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.807 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.760 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Im | 0.741 |


**Q35: What are the logical properties used for sizing elements in CSS?**
*(expects URL containing: `Sizing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.835 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.811 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.799 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.819 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.817 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.814 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.819 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.817 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.814 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.716 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.713 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.706 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.834 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.824 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.809 |
| colly+md | #6 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.818 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.791 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.834 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.826 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.818 |


**Q36: How do inline-size and block-size relate to width and height in a horizontal writing mode?**
*(expects URL containing: `Sizing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.823 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.786 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.733 |
| crawl4ai | #7 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.807 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/In | 0.802 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.802 |
| crawl4ai-raw | #7 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.807 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/In | 0.802 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.802 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.688 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.678 | developer.mozilla.org/en-US/docs/Web/JavaScript/Re | 0.655 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/In | 0.814 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.814 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.803 |
| colly+md | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.812 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.802 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.797 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.836 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.812 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Wr | 0.798 |


**Q37: What are at-rules in CSS?**
*(expects URL containing: `At-rules`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.891 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.824 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.822 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.855 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.854 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.816 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.855 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.854 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.816 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.746 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.691 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.687 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.852 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.835 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.816 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.869 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.828 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ne | 0.808 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.855 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.835 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.828 |


**Q38: How do at-rules begin in CSS?**
*(expects URL containing: `At-rules`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.852 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.850 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ne | 0.796 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.818 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.814 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.804 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.818 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.814 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.804 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.726 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.712 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.683 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.818 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.804 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.798 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.841 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.815 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ne | 0.793 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.819 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.815 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.798 |


**Q39: What does the Color mixer tool allow you to do?**
*(expects URL containing: `Color_mixer`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.747 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.722 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.696 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.765 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.745 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.765 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.745 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.629 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.605 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.605 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.769 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.734 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.715 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.741 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.715 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.708 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.780 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.747 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.741 |


**Q40: How can you change the percentages of each input color in the Color mixer?**
*(expects URL containing: `Color_mixer`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.787 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.771 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.734 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.778 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.745 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.734 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.778 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.745 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.734 |
| scrapy+md | miss | developer.mozilla.org/zh-CN/docs/Web/HTTP/Referenc | 0.634 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.633 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.621 |
| crawlee | #4 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.781 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.734 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.718 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.781 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.736 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.735 |
| playwright | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.771 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.764 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.736 |


**Q41: What does the `subgrid` value do in CSS grid layout?**
*(expects URL containing: `Subgrid`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.770 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.766 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.762 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.821 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.811 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.806 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.821 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.811 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.806 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.721 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.686 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.684 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.823 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.806 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.803 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.827 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.821 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.827 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.821 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.817 |


**Q42: How does the `gap` property behave in a subgrid?**
*(expects URL containing: `Subgrid`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.707 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.703 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.667 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.775 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.757 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.737 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.775 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.757 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.737 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.597 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.575 | developer.mozilla.org/en-US/docs/Web/SVG/Reference | 0.567 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.777 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.772 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.737 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.767 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.756 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.741 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.767 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.756 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.741 |


**Q43: What does the CSS box alignment module specify?**
*(expects URL containing: `Box_alignment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.820 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.815 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.794 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.834 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.834 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.830 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.834 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.834 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.830 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.738 | developer.mozilla.org/ja/docs/Web/CSS/Reference/Pr | 0.695 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.688 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.841 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.828 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.812 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.807 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.805 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.804 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.841 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.828 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.817 |


**Q44: How is alignment linked to writing modes in CSS?**
*(expects URL containing: `Box_alignment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #13 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Wr | 0.829 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.787 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.779 |
| crawl4ai | #5 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.824 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.800 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.799 |
| crawl4ai-raw | #5 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.824 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.800 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.799 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.733 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.716 | developer.mozilla.org/en-US/docs/Web/CSS | 0.704 |
| crawlee | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.824 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.811 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.802 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.822 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.805 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.804 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.811 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.805 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Wr | 0.799 |


**Q45: What properties control alignment in flexbox?**
*(expects URL containing: `Aligning_items`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.809 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.794 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.791 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.831 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.823 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.821 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.831 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.823 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.821 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.690 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.663 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.636 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.829 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.826 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.821 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.828 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.827 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.826 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.843 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.826 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.811 |


**Q46: How does the align-items property affect flex items on the cross axis?**
*(expects URL containing: `Aligning_items`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.803 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.776 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.767 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.852 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.847 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.827 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.852 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.847 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.827 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.639 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.634 | developer.mozilla.org/en-US/docs/Web/HTML/Referenc | 0.620 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.854 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.852 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.843 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.851 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.833 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.805 |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.833 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.820 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.805 |


**Q47: What do logical properties and values in CSS define?**
*(expects URL containing: `Basic_concepts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.804 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Va | 0.795 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.783 |
| crawl4ai | #4 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.902 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.838 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.828 |
| crawl4ai-raw | #4 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.902 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.838 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.828 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.740 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.723 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.714 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.826 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.813 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.799 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.787 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.786 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.826 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.813 |


**Q48: How do logical properties help with different writing modes in CSS?**
*(expects URL containing: `Basic_concepts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.825 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.809 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.791 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.820 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.820 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.837 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.820 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.820 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.729 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.723 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.718 |
| crawlee | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.834 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.828 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.823 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.829 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.823 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.819 |
| playwright | #4 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.830 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.829 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.828 |


**Q49: What are the logical properties for floating and positioning in CSS?**
*(expects URL containing: `Floating_and_positioning`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.792 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.771 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.764 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.812 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.780 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.812 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.780 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.687 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.687 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.672 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.808 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.795 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.762 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.761 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.754 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.808 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.795 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.779 |


**Q50: How do the inset properties relate to positioned layout in CSS?**
*(expects URL containing: `Floating_and_positioning`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.798 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.797 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.797 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.807 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Po | 0.789 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.784 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.807 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Po | 0.789 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.784 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.700 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.683 | developer.mozilla.org/en-US/docs/Web/CSS | 0.650 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.807 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Po | 0.792 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.783 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Po | 0.790 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.783 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.767 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Lo | 0.796 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Po | 0.792 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.783 |


**Q51: What does the CSS basic user interface module allow you to define?**
*(expects URL containing: `Basic_user_interface`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.822 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.772 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.769 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.815 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.806 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.783 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.815 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.806 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.783 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS | 0.740 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.739 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.734 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.809 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.794 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.790 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Learn/web/develop | 0.784 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.781 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.769 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.835 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.794 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.790 |


**Q52: How can basic user interface properties improve user experience and accessibility?**
*(expects URL containing: `Basic_user_interface`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.672 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/CS | 0.649 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.649 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.743 | developer.mozilla.org/en-US/docs/Web/Accessibility | 0.721 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.707 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.743 | developer.mozilla.org/en-US/docs/Web/Accessibility | 0.721 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.707 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/HTML/Referenc | 0.656 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.652 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.639 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.777 | developer.mozilla.org/en-US/docs/Web/Accessibility | 0.721 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.698 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.708 | developer.mozilla.org/en-US/docs/Web/Accessibility | 0.705 | developer.mozilla.org/en-US/docs/Web/Accessibility | 0.697 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.758 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ba | 0.749 | developer.mozilla.org/en-US/docs/Web/Accessibility | 0.721 |


**Q53: What is the purpose of using the `@media` at-rule in CSS for printing?**
*(expects URL containing: `Printing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.825 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.792 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.778 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.816 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.787 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.763 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.816 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.787 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.763 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.690 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.684 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.678 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.809 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.786 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.766 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.785 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.744 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.742 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.791 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.778 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.766 |


**Q54: How can the `@page` at-rule be used in CSS for printed pages?**
*(expects URL containing: `Printing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.801 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.799 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.798 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.815 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.767 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.749 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.815 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.767 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.749 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.670 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.667 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.666 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.814 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.772 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.748 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.764 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.742 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.738 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.801 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.748 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pa | 0.748 |


**Q55: What are CSS custom properties used for?**
*(expects URL containing: `Cascading_variables`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.839 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.831 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.830 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.846 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.845 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.840 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.846 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.845 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.840 |
| scrapy+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.825 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.804 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.783 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.846 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.845 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.843 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.848 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.843 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.826 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.848 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.843 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.843 |


**Q56: How do custom properties simplify complex CSS rules?**
*(expects URL containing: `Cascading_variables`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.829 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.815 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.801 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.796 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.791 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.790 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.796 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.791 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.790 |
| scrapy+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.783 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.759 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.753 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.801 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.796 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.790 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.806 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.790 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.787 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.801 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.798 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.790 |


**Q57: What does the CSS containment module define?**
*(expects URL containing: `Containment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.839 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.788 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.784 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.813 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.783 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.772 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.813 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.783 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.772 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.734 | developer.mozilla.org/en-US/docs/Web/CSS | 0.725 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.693 |
| crawlee | #7 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.788 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.784 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.784 |
| colly+md | #3 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.788 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.784 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.755 |
| playwright | #7 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.788 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.784 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.784 |


**Q58: How do container queries differ from media queries?**
*(expects URL containing: `Containment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.821 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.814 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.769 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.798 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.790 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.787 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.798 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.790 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.787 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.632 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.623 | developer.mozilla.org/en-US/docs/Web/API/VideoFram | 0.619 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.806 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.795 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.795 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.800 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.769 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.747 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.806 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Me | 0.793 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.788 |


**Q59: What is the syntax for the text-shadow property in CSS?**
*(expects URL containing: `Text_shadows`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.775 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.762 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.754 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.819 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.815 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.805 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.819 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.815 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.805 |
| scrapy+md | miss | developer.mozilla.org/zh-CN/docs/Web/HTTP/Referenc | 0.725 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.701 | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.682 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.828 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.815 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.788 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.842 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.840 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.816 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.838 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.823 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.808 |


**Q60: How can you apply multiple shadows to the same text?**
*(expects URL containing: `Text_shadows`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.667 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.659 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.659 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.802 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.755 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.802 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.755 |
| scrapy+md | miss | developer.mozilla.org/zh-CN/docs/Web/HTTP/Referenc | 0.644 | developer.mozilla.org/ja/docs/Web/CSS/Reference/Pr | 0.619 | developer.mozilla.org/de/docs/Web/SVG/Reference/At | 0.616 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.809 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.804 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.755 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.802 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.799 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.757 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.856 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Te | 0.820 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.755 |


</details>

## newegg

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai | 53% (31/58) | 84% (49/58) | 90% (52/58) | 95% (55/58) | 98% (57/58) | 0.687 | 5857 | 200 |
| crawl4ai-raw | 52% (30/58) | 83% (48/58) | 90% (52/58) | 97% (56/58) | 98% (57/58) | 0.677 | 5856 | 200 |
| colly+md | 7% (4/58) | 14% (8/58) | 16% (9/58) | 17% (10/58) | 22% (13/58) | 0.113 | 6574 | 165 |
| playwright | 0% (0/58) | 0% (0/58) | 0% (0/58) | 0% (0/58) | 0% (0/58) | 0.001 | 1195 | 200 |
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
| crawl4ai | #4 | www.newegg.com/Fans-PC-Cooling/Category/ID-11 | 0.721 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.676 | www.newegg.com/tools/custom-pc-builder?cm_sp=hambu | 0.666 |
| crawl4ai-raw | #4 | www.newegg.com/Fans-PC-Cooling/Category/ID-11 | 0.721 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.676 | www.newegg.com/tools/custom-pc-builder?cm_sp=hambu | 0.666 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/bitecool-15-6/p/1TS-00GJ-00016 | 0.669 | www.newegg.com/bitecool-15-6/p/1TS-00GJ-00016#IsFe | 0.669 | www.newegg.com/tools/custom-pc-builder?cm/sp=Head/ | 0.666 |
| playwright | miss | www.newegg.com/insider/how-to-choose-the-best-desk | 0.684 | www.newegg.com/ | 0.659 | www.newegg.com/ | 0.602 |


**Q2: What types of products can I find under DIY Cooling?**
*(expects URL containing: `ID-3635`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #4 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.740 | www.newegg.com/Fans-PC-Cooling/Category/ID-11 | 0.729 | www.newegg.com/tools/custom-pc-builder?cm_sp=hambu | 0.709 |
| crawl4ai-raw | #4 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.740 | www.newegg.com/Fans-PC-Cooling/Category/ID-11 | 0.729 | www.newegg.com/tools/custom-pc-builder?cm_sp=hambu | 0.709 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/tools/custom-pc-builder?cm/sp=Head/ | 0.709 | www.newegg.com/tools/custom-pc-builder?cm/sp=Head/ | 0.705 | www.newegg.com/bitecool-15-6/p/1TS-00GJ-00016#IsFe | 0.702 |
| playwright | miss | www.newegg.com/insider/how-to-choose-the-best-desk | 0.742 | www.newegg.com/ | 0.724 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.676 |


**Q3: What brands of USB / IEEE-1394 Firewire Adapters are available?**
*(expects URL containing: `ID-3025`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.796 | www.newegg.com/Adapters-Gender-Changers/Category/I | 0.785 | www.newegg.com/Adapter-Gender-Changer/Category/ID- | 0.785 |
| crawl4ai-raw | #1 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.796 | www.newegg.com/Adapter-Gender-Changer/Category/ID- | 0.785 | www.newegg.com/Adapters-Gender-Changers/Category/I | 0.785 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Laptop-Notebook/Category/ID-223 | 0.661 | www.newegg.com/p/pl?N=100006740%2050001315&mid1=Pa | 0.652 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.652 |
| playwright | miss | www.newegg.com/ | 0.660 | www.newegg.com/ | 0.657 | www.newegg.com/ | 0.623 |


**Q4: What is the price range for USB / IEEE-1394 Firewire Adapters on Newegg?**
*(expects URL containing: `ID-3025`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.816 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.814 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.813 |
| crawl4ai-raw | #1 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.816 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.814 | www.newegg.com/USB-IEEE-1394-Firewire-Adapters/Sub | 0.813 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Shell-Shocker/EventSaleStore/ID-103 | 0.704 | www.newegg.com/Shell-Shocker/EventSaleStore/ID-103 | 0.704 | www.newegg.com/Shell-Shocker/EventSaleStore/ID-103 | 0.704 |
| playwright | miss | www.newegg.com/ | 0.680 | www.newegg.com/ | 0.669 | www.newegg.com/ | 0.664 |


**Q5: What types of desktop computers are available on Newegg?**
*(expects URL containing: `ID-228`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #7 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.824 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.777 | www.newegg.com/All-in-One-Computer/SubCategory/ID- | 0.777 |
| crawl4ai-raw | #7 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.824 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.777 | www.newegg.com/All-in-One-Computer/SubCategory/ID- | 0.777 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Computer-Systems/Store/ID-3 | 0.754 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.746 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.743 |
| playwright | miss | www.newegg.com/ | 0.728 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.714 | www.newegg.com/ | 0.691 |


**Q6: What brands of desktop computers can I find on Newegg?**
*(expects URL containing: `ID-228`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #3 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.847 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.779 | www.newegg.com/Desktop-Computer/Category/ID-228 | 0.758 |
| crawl4ai-raw | #3 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.847 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.779 | www.newegg.com/Desktop-Computer/Category/ID-228 | 0.758 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/ | 0.751 | www.newegg.com/DELL/BrandStore/ID-10772 | 0.750 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.750 |
| playwright | miss | www.newegg.com/ | 0.751 | www.newegg.com/ | 0.712 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.690 |


**Q7: What types of fan controllers are available in the Controller Panels category?**
*(expects URL containing: `ID-11`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.753 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.748 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.738 |
| crawl4ai-raw | #1 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.753 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.748 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.738 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.677 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.665 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.665 |
| playwright | miss | www.newegg.com/ | 0.633 | www.newegg.com/ | 0.577 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.550 |


**Q8: Which brands are featured in the Controller Panels section?**
*(expects URL containing: `ID-11`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.699 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.688 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.682 |
| crawl4ai-raw | #1 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.699 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.688 | www.newegg.com/Controller-Panels/SubCategory/ID-11 | 0.682 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #40 | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.679 | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.674 | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.670 |
| playwright | miss | www.newegg.com/ | 0.614 | www.newegg.com/ | 0.606 | www.newegg.com/Server-Memory/SubCategory/ID-541 | 0.600 |


**Q9: What brands of barebone PCs are available on Newegg?**
*(expects URL containing: `ID-3`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Barebone-PCs/SubCategory/ID-3 | 0.801 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.790 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.779 |
| crawl4ai-raw | #1 | www.newegg.com/Barebone-PCs/SubCategory/ID-3 | 0.801 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.790 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.779 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #2 | www.newegg.com/p/pl?d=AI+NPU&mid1=PageSEO | 0.712 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.701 | www.newegg.com/All-Laptop/SubCategory/ID-32 | 0.700 |
| playwright | #43 | www.newegg.com/ | 0.698 | www.newegg.com/ | 0.696 | www.newegg.com/asus-nuc-configurator?cm_sp=hamburg | 0.693 |


**Q10: What is the maximum RAM support for the Shuttle XPC slim DH610 Barebone System?**
*(expects URL containing: `ID-3`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #3 | www.newegg.com/System-Specific-Memory/SubCategory/ | 0.691 | www.newegg.com/Embedded-Solutions/SubCategory/ID-4 | 0.675 | www.newegg.com/CPU-Processor/Category/ID-34 | 0.671 |
| crawl4ai-raw | #3 | www.newegg.com/System-Specific-Memory/SubCategory/ | 0.691 | www.newegg.com/Embedded-Solutions/SubCategory/ID-4 | 0.675 | www.newegg.com/CPU-Processor/Category/ID-34 | 0.670 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #43 | www.newegg.com/p/pl?d=CPU&mid1=PageSEO | 0.665 | www.newegg.com/d/Best-Sellers/Motherboard/c/ID-20 | 0.664 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.660 |
| playwright | miss | www.newegg.com/ | 0.626 | www.newegg.com/ | 0.597 | www.newegg.com/ | 0.593 |


**Q11: What are the types of products available in the Barebone / Mini Computers category?**
*(expects URL containing: `ID-3`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.862 | www.newegg.com/Mini-PC-Barebone/SubCategory/ID-309 | 0.838 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.826 |
| crawl4ai-raw | #1 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.862 | www.newegg.com/Mini-PC-Barebone/SubCategory/ID-309 | 0.838 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.826 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/p/pl?d=NPU&mid1=PageSEO | 0.709 | www.newegg.com/p/pl?d=NPU&mid1=PageSEO | 0.700 | www.newegg.com/p/pl?d=AI+NPU&mid1=PageSEO | 0.700 |
| playwright | miss | www.newegg.com/ | 0.714 | www.newegg.com/asus-nuc-configurator?cm_sp=hamburg | 0.676 | www.newegg.com/ | 0.653 |


**Q12: What is the price of the ASUS NUC 16 Pro Mini Gaming PC?**
*(expects URL containing: `ID-3`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.816 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.814 | www.newegg.com/Mini-PC-Barebone/SubCategory/ID-309 | 0.801 |
| crawl4ai-raw | #1 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.816 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.814 | www.newegg.com/Mini-PC-Barebone/SubCategory/ID-309 | 0.801 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #14 | www.newegg.com/ASUS/BrandStore/ID-1315 | 0.782 | www.newegg.com/p/pl?N=4889 | 0.774 | www.newegg.com/p/pl?N=4889 | 0.759 |
| playwright | miss | www.newegg.com/asus-nuc-configurator?cm_sp=hamburg | 0.763 | www.newegg.com/asus-nuc-configurator?cm_sp=hamburg | 0.738 | www.newegg.com/asus-nuc-configurator?cm_sp=hamburg | 0.734 |


**Q13: What types of memory are available on the Newegg Deals page?**
*(expects URL containing: `ID-9447`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #13 | www.newegg.com/Memory/Category/ID-17 | 0.793 | www.newegg.com/System-Specific-Memory/SubCategory/ | 0.777 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.768 |
| crawl4ai-raw | #13 | www.newegg.com/Memory/Category/ID-17 | 0.793 | www.newegg.com/System-Specific-Memory/SubCategory/ | 0.777 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.768 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #6 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.802 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.767 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.758 |
| playwright | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.725 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.725 | www.newegg.com/ | 0.715 |


**Q14: Which brands of desktop memory can be found in the Newegg Deals section?**
*(expects URL containing: `ID-9447`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #11 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.778 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.766 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.762 |
| crawl4ai-raw | #9 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.778 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.765 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.762 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #3 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.789 | www.newegg.com/ | 0.756 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.746 |
| playwright | miss | www.newegg.com/ | 0.756 | www.newegg.com/ | 0.714 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.681 |


**Q15: What types of audio/video splitters are available?**
*(expects URL containing: `ID-3050`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.741 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.704 | www.newegg.com/Audio-Video-Switch/SubCategory/ID-3 | 0.694 |
| crawl4ai-raw | #1 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.741 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.704 | www.newegg.com/Audio-Video-Switch/SubCategory/ID-3 | 0.694 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/p/pl?d=NPU&mid1=PageSEO | 0.632 | www.newegg.com/d/Best-Sellers/Components-Storage/t | 0.614 | www.newegg.com/d/Best-Sellers/Motherboard/c/ID-20 | 0.605 |
| playwright | miss | www.newegg.com/ | 0.631 | www.newegg.com/ | 0.597 | www.newegg.com/ | 0.593 |


**Q16: Which brands are featured for audio/video splitters?**
*(expects URL containing: `ID-3050`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.722 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.710 | www.newegg.com/3-5mm-2-5mm-Stereo-Cables/SubCatego | 0.703 |
| crawl4ai-raw | #1 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.722 | www.newegg.com/Audio-Video-Splitters/SubCategory/I | 0.710 | www.newegg.com/3-5mm-2-5mm-Stereo-Cables/SubCatego | 0.703 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.636 | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.633 | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.633 |
| playwright | miss | www.newegg.com/ | 0.656 | www.newegg.com/ | 0.630 | www.newegg.com/ | 0.629 |


**Q17: What brands are available for computer accessories?**
*(expects URL containing: `pl`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/p/pl?N=100006519+4016 | 0.753 | www.newegg.com/p/pl?N=100006640+4016 | 0.741 | www.newegg.com/p/pl?N=100006640+4016 | 0.739 |
| crawl4ai-raw | #1 | www.newegg.com/p/pl?N=100006519+4016 | 0.753 | www.newegg.com/p/pl?N=100006640+4016 | 0.741 | www.newegg.com/p/pl?N=100006640+4016 | 0.739 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #15 | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.771 | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.771 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.759 |
| playwright | miss | www.newegg.com/ | 0.757 | www.newegg.com/ | 0.742 | www.newegg.com/ | 0.723 |


**Q18: What is the model number of the refurbished ASUS ROG Ryujin III 240mm ARGB liquid CPU cooler?**
*(expects URL containing: `pl`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/p/pl?N=100006640+4016 | 0.803 | www.newegg.com/p/pl?N=100006640+4016 | 0.752 | www.newegg.com/Water-Liquid-Cooling/SubCategory/ID | 0.693 |
| crawl4ai-raw | #1 | www.newegg.com/p/pl?N=100006640+4016 | 0.803 | www.newegg.com/p/pl?N=100006640+4016 | 0.752 | www.newegg.com/Water-Liquid-Cooling/SubCategory/ID | 0.695 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #15 | www.newegg.com/Newegg-Select/EventSaleStore/ID-183 | 0.688 | www.newegg.com/category | 0.683 | www.newegg.com/MSI/BrandStore/ID-1312 | 0.674 |
| playwright | miss | www.newegg.com/ | 0.709 | www.newegg.com/ | 0.626 | www.newegg.com/ | 0.619 |


**Q19: What brands of audio adapters are available on Newegg?**
*(expects URL containing: `ID-3020`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.797 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.785 | www.newegg.com/Sound-Card-Accessories/SubCategory/ | 0.781 |
| crawl4ai-raw | #2 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.797 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.785 | www.newegg.com/Sound-Card-Accessories/SubCategory/ | 0.781 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/Components-Storage/t | 0.724 | www.newegg.com/ | 0.722 | www.newegg.com/Gaming-Laptops/SubCategory/ID-3365? | 0.701 |
| playwright | miss | www.newegg.com/ | 0.722 | www.newegg.com/ | 0.705 | www.newegg.com/ | 0.695 |


**Q20: What is the price range for audio adapters on Newegg?**
*(expects URL containing: `ID-3020`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/Sound-Card-Accessories/SubCategory/ | 0.786 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.781 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.780 |
| crawl4ai-raw | #2 | www.newegg.com/Sound-Card-Accessories/SubCategory/ | 0.786 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.781 | www.newegg.com/Audio-Adapters/SubCategory/ID-3020 | 0.780 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.729 | www.newegg.com/d/Best-Sellers/Components-Storage/t | 0.712 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.711 |
| playwright | miss | www.newegg.com/ | 0.693 | www.newegg.com/ | 0.673 | www.newegg.com/ | 0.670 |


**Q21: What brands are available for data adapters?**
*(expects URL containing: `ID-3021`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.755 | www.newegg.com/Other-Adapters-Gender-Changers/SubC | 0.735 | www.newegg.com/Other-Adapters-Gender-Changers/SubC | 0.724 |
| crawl4ai-raw | #1 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.755 | www.newegg.com/Other-Adapters-Gender-Changers/SubC | 0.735 | www.newegg.com/Other-Adapters-Gender-Changers/SubC | 0.724 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/DELL/BrandStore/ID-10772 | 0.683 | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.683 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.680 |
| playwright | miss | www.newegg.com/ | 0.654 | www.newegg.com/ | 0.653 | www.newegg.com/ | 0.633 |


**Q22: What is the price range for data adapters on Newegg?**
*(expects URL containing: `ID-3021`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.758 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.755 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.752 |
| crawl4ai-raw | #1 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.758 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.755 | www.newegg.com/Data-Adapters/SubCategory/ID-3021 | 0.752 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/DELL/BrandStore/ID-10772 | 0.724 | www.newegg.com/Newegg-Select/EventSaleStore/ID-183 | 0.707 | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.700 |
| playwright | miss | www.newegg.com/ | 0.695 | www.newegg.com/ | 0.694 | www.newegg.com/ | 0.689 |


**Q23: What brands of power supplies are available on Newegg?**
*(expects URL containing: `ID-58`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Power-Supplies/SubCategory/ID-58 | 0.781 | www.newegg.com/Power-Inverters/SubCategory/ID-536 | 0.778 | www.newegg.com/tools/power-supply-calculator | 0.778 |
| crawl4ai-raw | #2 | www.newegg.com/Power-Supply/Category/ID-32 | 0.781 | www.newegg.com/Power-Supplies/SubCategory/ID-58 | 0.781 | www.newegg.com/Power-Inverters/SubCategory/ID-536 | 0.778 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.772 | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.766 | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.755 |
| playwright | miss | www.newegg.com/ | 0.739 | www.newegg.com/ | 0.720 | www.newegg.com/ | 0.680 |


**Q24: What types of power supply connectors are listed on the page?**
*(expects URL containing: `ID-58`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #3 | www.newegg.com/Server-Power-Supplies/SubCategory/I | 0.746 | www.newegg.com/Server-Power-Supplies/SubCategory/I | 0.743 | www.newegg.com/Power-Supplies/SubCategory/ID-58 | 0.741 |
| crawl4ai-raw | #3 | www.newegg.com/Server-Power-Supplies/SubCategory/I | 0.746 | www.newegg.com/Server-Power-Supplies/SubCategory/I | 0.743 | www.newegg.com/Power-Supplies/SubCategory/ID-58 | 0.741 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.723 | www.newegg.com/Newegg-Select/EventSaleStore/ID-183 | 0.721 | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.718 |
| playwright | miss | www.newegg.com/ | 0.698 | www.newegg.com/ | 0.689 | www.newegg.com/ | 0.630 |


**Q25: What brands of duplicators are available on this page?**
*(expects URL containing: `ID-528`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.694 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.678 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.678 |
| crawl4ai-raw | #1 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.694 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.678 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.678 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.631 | www.newegg.com/d/Best-Sellers/Office-Solutions/t/I | 0.615 | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.606 |
| playwright | miss | www.newegg.com/ | 0.610 | www.newegg.com/ | 0.602 | www.newegg.com/ | 0.563 |


**Q26: What types of duplicators can I find listed on this page?**
*(expects URL containing: `ID-528`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.708 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.704 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.693 |
| crawl4ai-raw | #1 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.708 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.704 | www.newegg.com/Duplicators/SubCategory/ID-528 | 0.693 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/ProductSort/BrandList?Depa=0 | 0.602 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.600 | www.newegg.com/d/Best-Sellers/Office-Solutions/t/I | 0.599 |
| playwright | miss | www.newegg.com/ | 0.619 | www.newegg.com/ | 0.602 | www.newegg.com/ | 0.583 |


**Q27: What brands are available for server and workstation systems?**
*(expects URL containing: `ID-386`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/Server-Chassis/SubCategory/ID-412 | 0.765 | www.newegg.com/Server-Workstation-System/SubCatego | 0.746 | www.newegg.com/Server-Workstation-System/SubCatego | 0.743 |
| crawl4ai-raw | #2 | www.newegg.com/Server-Chassis/SubCategory/ID-412 | 0.765 | www.newegg.com/Server-Workstation-System/SubCatego | 0.746 | www.newegg.com/Server-Workstation-System/SubCatego | 0.743 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.726 | www.newegg.com/p/pl?d=NPU&mid1=PageSEO | 0.716 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.713 |
| playwright | miss | www.newegg.com/ | 0.700 | www.newegg.com/ | 0.695 | www.newegg.com/server-system-configurator/ | 0.664 |


**Q28: What types of server and workstation systems are listed?**
*(expects URL containing: `ID-386`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/Server-Components/Category/ID-449 | 0.728 | www.newegg.com/Server-Workstation-System/SubCatego | 0.718 | www.newegg.com/server-system-configurator | 0.715 |
| crawl4ai-raw | #2 | www.newegg.com/Server-Components/Category/ID-449 | 0.728 | www.newegg.com/Server-Workstation-System/SubCatego | 0.718 | www.newegg.com/server-system-configurator | 0.715 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.702 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.699 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.695 |
| playwright | miss | www.newegg.com/ | 0.712 | www.newegg.com/server-system-configurator/ | 0.687 | www.newegg.com/ | 0.684 |


**Q29: What brands of power extension cords are available on Newegg?**
*(expects URL containing: `ID-2829`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #3 | www.newegg.com/Computer-Power-Extension-Cords/SubC | 0.815 | www.newegg.com/Computer-Power-Extension-Cords/SubC | 0.811 | www.newegg.com/Power-Extension-Cords/SubCategory/I | 0.807 |
| crawl4ai-raw | #3 | www.newegg.com/Computer-Power-Extension-Cords/SubC | 0.815 | www.newegg.com/Computer-Power-Extension-Cords/SubC | 0.811 | www.newegg.com/Power-Extension-Cords/SubCategory/I | 0.807 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/ | 0.721 | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.718 | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.717 |
| playwright | miss | www.newegg.com/ | 0.737 | www.newegg.com/ | 0.721 | www.newegg.com/ | 0.705 |


**Q30: What types of power extension cords can I find on Newegg?**
*(expects URL containing: `ID-2829`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #7 | www.newegg.com/Computer-Power-Extension-Cords/SubC | 0.827 | www.newegg.com/Computer-Power-Extension-Cords/SubC | 0.815 | www.newegg.com/Computer-Power-Extension-Cords/SubC | 0.809 |
| crawl4ai-raw | #7 | www.newegg.com/Computer-Power-Extension-Cords/SubC | 0.827 | www.newegg.com/Computer-Power-Extension-Cords/SubC | 0.815 | www.newegg.com/Computer-Power-Extension-Cords/SubC | 0.809 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.734 | www.newegg.com/d/Best-Sellers/Server-Components/t/ | 0.721 | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.714 |
| playwright | miss | www.newegg.com/ | 0.756 | www.newegg.com/ | 0.725 | www.newegg.com/ | 0.703 |


**Q31: What brands of power distribution units are available?**
*(expects URL containing: `ID-1042`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/Power-Protection/Category/ID-314 | 0.716 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.709 | www.newegg.com/Power-Protection/Category/ID-314 | 0.700 |
| crawl4ai-raw | #2 | www.newegg.com/Power-Protection/Category/ID-314 | 0.716 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.709 | www.newegg.com/Power-Protection/Category/ID-314 | 0.700 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.638 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.637 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.634 |
| playwright | miss | www.newegg.com/ | 0.635 | www.newegg.com/ | 0.608 | www.newegg.com/ | 0.601 |


**Q32: What is the input voltage for the CyberPower PDU15B10R?**
*(expects URL containing: `ID-1042`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/Battery-Backup-UPS/SubCategory/ID-7 | 0.712 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.708 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.696 |
| crawl4ai-raw | #2 | www.newegg.com/Battery-Backup-UPS/SubCategory/ID-7 | 0.712 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.708 | www.newegg.com/Power-Distribution-Unit/SubCategory | 0.696 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.681 | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.681 | www.newegg.com/d/Best-Sellers/Power-Supply/c/ID-32 | 0.644 |
| playwright | miss | www.newegg.com/ | 0.627 | www.newegg.com/ | 0.565 | www.newegg.com/ | 0.560 |


**Q33: What brands of hard drive adapters are available on Newegg?**
*(expects URL containing: `ID-3022`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Hard-Drive-Adapters/SubCategory/ID- | 0.790 | www.newegg.com/p/pl?N=100006670+4016 | 0.769 | www.newegg.com/Portable-External-Hard-Drives/SubCa | 0.764 |
| crawl4ai-raw | #1 | www.newegg.com/Hard-Drive-Adapters/SubCategory/ID- | 0.794 | www.newegg.com/p/pl?N=100006670+4016 | 0.769 | www.newegg.com/Portable-External-Hard-Drives/SubCa | 0.764 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/DELL/BrandStore/ID-10772 | 0.741 | www.newegg.com/ | 0.721 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.720 |
| playwright | miss | www.newegg.com/ | 0.721 | www.newegg.com/ | 0.680 | www.newegg.com/ | 0.675 |


**Q34: What is the price range for hard drive adapters on Newegg?**
*(expects URL containing: `ID-3022`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Hard-Drive-Adapters/SubCategory/ID- | 0.808 | www.newegg.com/Desktop-External-Hard-Drives/SubCat | 0.789 | www.newegg.com/Portable-External-Hard-Drives/SubCa | 0.788 |
| crawl4ai-raw | #1 | www.newegg.com/Hard-Drive-Adapters/SubCategory/ID- | 0.808 | www.newegg.com/Desktop-External-Hard-Drives/SubCat | 0.789 | www.newegg.com/Portable-External-Hard-Drives/SubCa | 0.788 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Newegg-Select/EventSaleStore/ID-183 | 0.734 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.720 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.712 |
| playwright | miss | www.newegg.com/ | 0.702 | www.newegg.com/ | 0.687 | www.newegg.com/ | 0.678 |


**Q35: What brands of crypto mining equipment are available on Newegg?**
*(expects URL containing: `ID-3924`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.798 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.769 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.763 |
| crawl4ai-raw | #1 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.798 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.769 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.763 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/ | 0.730 | www.newegg.com/p/pl?d=AI+NPU&mid1=PageSEO | 0.713 | www.newegg.com/corporate/about | 0.703 |
| playwright | miss | www.newegg.com/ | 0.730 | www.newegg.com/ | 0.676 | www.newegg.com/ | 0.676 |


**Q36: What is the hashrate of the Stellapex Bitcoin Solo Miner NerdMiner V2?**
*(expects URL containing: `ID-3924`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.778 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.762 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.744 |
| crawl4ai-raw | #1 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.778 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.762 | www.newegg.com/Crypto-Mining/SubCategory/ID-3924 | 0.744 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/CPU-Processor/c/ID-3 | 0.573 | www.newegg.com/d/Best-Sellers/CPU-Processor/c/ID-3 | 0.548 | www.newegg.com/p/pl?N=100006740%20601439322 | 0.547 |
| playwright | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.507 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.507 | www.newegg.com/ | 0.507 |


**Q37: What brands are available for external CD/DVD/Blu-Ray drives?**
*(expects URL containing: `ID-420`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/Blu-Ray-Drives/SubCategory/ID-598 | 0.821 | www.newegg.com/External-CD-DVD-Blu-Ray-Drives/SubC | 0.793 | www.newegg.com/Blu-Ray-Burners/SubCategory/ID-600 | 0.783 |
| crawl4ai-raw | #2 | www.newegg.com/Blu-Ray-Drives/SubCategory/ID-598 | 0.821 | www.newegg.com/External-CD-DVD-Blu-Ray-Drives/SubC | 0.793 | www.newegg.com/Blu-Ray-Burners/SubCategory/ID-600 | 0.783 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Laptop-Notebook/Category/ID-223 | 0.688 | www.newegg.com/category | 0.686 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.674 |
| playwright | miss | www.newegg.com/ | 0.709 | www.newegg.com/ | 0.652 | www.newegg.com/ | 0.637 |


**Q38: What types of external drives can I find on this page?**
*(expects URL containing: `ID-420`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | miss | www.newegg.com/Portable-External-Hard-Drives/SubCa | 0.733 | www.newegg.com/Hard-Drive-SSD-Enclosures/SubCatego | 0.712 | www.newegg.com/Desktop-External-Hard-Drives/SubCat | 0.712 |
| crawl4ai-raw | #34 | www.newegg.com/Portable-External-Hard-Drives/SubCa | 0.733 | www.newegg.com/Hard-Drive-SSD-Enclosures/SubCatego | 0.712 | www.newegg.com/Desktop-External-Hard-Drives/SubCat | 0.712 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/category | 0.707 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.706 | www.newegg.com/Lenovo/BrandStore/ID-10418 | 0.672 |
| playwright | miss | www.newegg.com/ | 0.673 | www.newegg.com/ | 0.653 | www.newegg.com/ | 0.643 |


**Q39: What brands of sound cards are available on Newegg?**
*(expects URL containing: `ID-57`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #3 | www.newegg.com/Sound-Card-Accessories/SubCategory/ | 0.814 | www.newegg.com/Sound-Card/Category/ID-36 | 0.799 | www.newegg.com/Sound-Card/SubCategory/ID-57 | 0.794 |
| crawl4ai-raw | #3 | www.newegg.com/Sound-Card-Accessories/SubCategory/ | 0.814 | www.newegg.com/Sound-Card/Category/ID-36 | 0.799 | www.newegg.com/Sound-Card/SubCategory/ID-57 | 0.794 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/ | 0.739 | www.newegg.com/d/Best-Sellers/Components-Storage/t | 0.716 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.709 |
| playwright | miss | www.newegg.com/ | 0.739 | www.newegg.com/ | 0.653 | www.newegg.com/ | 0.647 |


**Q40: What is the SNR of the Creative Sound Blaster Audigy Fx V2?**
*(expects URL containing: `ID-57`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Sound-Card/SubCategory/ID-57 | 0.772 | www.newegg.com/Sound-Card/Category/ID-36 | 0.752 | www.newegg.com/Sound-Card/Category/ID-36 | 0.740 |
| crawl4ai-raw | #1 | www.newegg.com/Sound-Card/SubCategory/ID-57 | 0.772 | www.newegg.com/Sound-Card/Category/ID-36 | 0.752 | www.newegg.com/Sound-Card/Category/ID-36 | 0.740 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/Components-Storage/t | 0.656 | www.newegg.com/d/Best-Sellers/Motherboard/c/ID-20 | 0.643 | www.newegg.com/Shell-Shocker/EventSaleStore/ID-103 | 0.628 |
| playwright | miss | www.newegg.com/ | 0.589 | www.newegg.com/ | 0.537 | www.newegg.com/ | 0.529 |


**Q41: What types of RAM are available on Newegg?**
*(expects URL containing: `ID-17`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/Motherboard/Category/ID-20 | 0.774 | www.newegg.com/Memory/Category/ID-17 | 0.771 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.764 |
| crawl4ai-raw | #2 | www.newegg.com/Motherboard/Category/ID-20 | 0.774 | www.newegg.com/Memory/Category/ID-17 | 0.771 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.764 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #1 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.771 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.755 | www.newegg.com/Newegg-Select/EventSaleStore/ID-183 | 0.746 |
| playwright | miss | www.newegg.com/ | 0.696 | www.newegg.com/ | 0.692 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.683 |


**Q42: What is the maximum capacity per module for DDR4 RAM?**
*(expects URL containing: `ID-17`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Memory/Category/ID-17 | 0.782 | www.newegg.com/System-Specific-Memory/SubCategory/ | 0.775 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.773 |
| crawl4ai-raw | #1 | www.newegg.com/Memory/Category/ID-17 | 0.782 | www.newegg.com/System-Specific-Memory/SubCategory/ | 0.775 | www.newegg.com/Desktop-Memory/SubCategory/ID-147 | 0.773 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #2 | www.newegg.com/DELL/BrandStore/ID-10772 | 0.720 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.700 | www.newegg.com/d/Best-Sellers/Memory/c/ID-17 | 0.689 |
| playwright | miss | www.newegg.com/ | 0.617 | www.newegg.com/ | 0.592 | www.newegg.com/ | 0.563 |


**Q43: What types of GPUs are available on this page?**
*(expects URL containing: `ID-9447`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #3 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.767 | www.newegg.com/Workstation-Graphics-Cards/SubCateg | 0.762 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.755 |
| crawl4ai-raw | #3 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.767 | www.newegg.com/Workstation-Graphics-Cards/SubCateg | 0.762 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.755 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.784 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.784 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.775 |
| playwright | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.696 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.696 | www.newegg.com/ | 0.666 |


**Q44: What is the maximum resolution supported by the graphics cards listed?**
*(expects URL containing: `ID-9447`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #3 | www.newegg.com/Workstation-Graphics-Cards/SubCateg | 0.746 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.739 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.739 |
| crawl4ai-raw | #3 | www.newegg.com/Workstation-Graphics-Cards/SubCateg | 0.746 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.739 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.739 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/GPU-Video-Graphics-D | 0.776 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.768 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.768 |
| playwright | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.658 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.658 | www.newegg.com/ | 0.648 |


**Q45: What brands of gaming desktop PCs are available?**
*(expects URL containing: `ID-3742`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.809 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.785 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.770 |
| crawl4ai-raw | #2 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.809 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.785 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.770 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #1 | www.newegg.com/d/Best-Sellers/Gaming-Desktop-PC/s/ | 0.766 | www.newegg.com/tools/custom-pc-builder/showcase/fe | 0.747 | www.newegg.com/d/Best-Sellers/Gaming-Desktop-PC/s/ | 0.742 |
| playwright | miss | www.newegg.com/ | 0.694 | www.newegg.com/asus-nuc-configurator?cm_sp=hamburg | 0.692 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.687 |


**Q46: What types of cooling systems are offered for gaming desktop PCs?**
*(expects URL containing: `ID-3742`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.760 | www.newegg.com/CPU-Air-Coolers/SubCategory/ID-574 | 0.751 | www.newegg.com/CPU-Fans-Heatsinks/SubCategory/ID-5 | 0.751 |
| crawl4ai-raw | #1 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.760 | www.newegg.com/CPU-Fans-Heatsinks/SubCategory/ID-5 | 0.751 | www.newegg.com/CPU-Air-Coolers/SubCategory/ID-574 | 0.751 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #2 | www.newegg.com/tools/custom-pc-builder?cm/sp=Head/ | 0.721 | www.newegg.com/d/Best-Sellers/Gaming-Desktop-PC/s/ | 0.720 | www.newegg.com/d/Best-Sellers/Gaming-Desktop-PC/s/ | 0.711 |
| playwright | miss | www.newegg.com/insider/how-to-choose-the-best-desk | 0.701 | www.newegg.com/ | 0.696 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.693 |


**Q47: What types of gaming PC systems are available?**
*(expects URL containing: `ID-3`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.784 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.753 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.745 |
| crawl4ai-raw | #1 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.784 | www.newegg.com/Gaming-Desktop-PC/SubCategory/ID-37 | 0.753 | www.newegg.com/Barebone-Mini-Computers/Category/ID | 0.745 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #1 | www.newegg.com/d/Best-Sellers/Gaming-Desktop-PC/s/ | 0.738 | www.newegg.com/tools/custom-pc-builder/showcase/fe | 0.736 | www.newegg.com/d/Best-Sellers/Gaming-Desktop-PC/s/ | 0.730 |
| playwright | miss | www.newegg.com/asus-nuc-configurator?cm_sp=hamburg | 0.686 | www.newegg.com/ | 0.674 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.664 |


**Q48: What are the categories of desktop systems listed on the page?**
*(expects URL containing: `ID-3`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #4 | www.newegg.com/Desktop-Computer/Category/ID-228 | 0.736 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.710 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.707 |
| crawl4ai-raw | #4 | www.newegg.com/Desktop-Computer/Category/ID-228 | 0.736 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.710 | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.707 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #1 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.738 | www.newegg.com/DELL/BrandStore/ID-10772 | 0.734 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.720 |
| playwright | #40 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.719 | www.newegg.com/ | 0.673 | www.newegg.com/ | 0.658 |


**Q49: What brands are available for memory and chipset cooling?**
*(expects URL containing: `ID-572`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.807 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.776 | www.newegg.com/Fans-PC-Cooling/Category/ID-11 | 0.760 |
| crawl4ai-raw | #1 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.807 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.776 | www.newegg.com/Fans-PC-Cooling/Category/ID-11 | 0.760 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.712 | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.712 | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.700 |
| playwright | miss | www.newegg.com/insider/how-to-choose-the-best-desk | 0.705 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.694 | www.newegg.com/ | 0.691 |


**Q50: What types of products are included in the memory and chipset cooling category?**
*(expects URL containing: `ID-572`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.810 | www.newegg.com/ | 0.756 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.742 |
| crawl4ai-raw | #1 | www.newegg.com/Memory-Chipset-Cooling/SubCategory/ | 0.810 | www.newegg.com/ | 0.756 | www.newegg.com/tools/nas-builder?cm_sp=hamburger-_ | 0.742 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.697 | www.newegg.com/Clearance-Store/EventSaleStore/ID-6 | 0.697 | www.newegg.com/Newegg-Select/EventSaleStore/ID-183 | 0.692 |
| playwright | miss | www.newegg.com/ | 0.716 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.696 | www.newegg.com/insider/how-to-choose-the-best-desk | 0.690 |


**Q51: What types of SSD form factors are available?**
*(expects URL containing: `ID-9447`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #8 | www.newegg.com/Internal-SSDs/SubCategory/ID-636 | 0.765 | www.newegg.com/SSD/Category/ID-119 | 0.760 | www.newegg.com/SSD/Category/ID-119 | 0.760 |
| crawl4ai-raw | #9 | www.newegg.com/Internal-SSDs/SubCategory/ID-636 | 0.765 | www.newegg.com/SSD/Category/ID-119 | 0.760 | www.newegg.com/SSD/Category/ID-119 | 0.760 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #4 | www.newegg.com/MSI/BrandStore/ID-1312 | 0.745 | www.newegg.com/MSI/BrandStore/ID-1312 | 0.741 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.729 |
| playwright | miss | www.newegg.com/ | 0.674 | www.newegg.com/ | 0.666 | www.newegg.com/ | 0.665 |


**Q52: Which brands of SSDs are featured on this page?**
*(expects URL containing: `ID-9447`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #3 | www.newegg.com/Internal-SSDs/SubCategory/ID-636 | 0.768 | www.newegg.com/USB-Flash-Drives/SubCategory/ID-522 | 0.751 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.751 |
| crawl4ai-raw | #4 | www.newegg.com/Internal-SSDs/SubCategory/ID-636 | 0.768 | www.newegg.com/USB-Flash-Drives/SubCategory/ID-522 | 0.754 | www.newegg.com/SSD/Category/ID-119 | 0.751 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #27 | www.newegg.com/Laptop-Notebook/Category/ID-223 | 0.758 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.745 | www.newegg.com/tools/custom-pc-builder/showcase/fe | 0.742 |
| playwright | miss | www.newegg.com/ | 0.670 | www.newegg.com/ | 0.668 | www.newegg.com/ | 0.665 |


**Q53: What types of DVI cables are available?**
*(expects URL containing: `ID-2814`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.807 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.803 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.789 |
| crawl4ai-raw | #1 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.807 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.803 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.789 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/p/pl?d=NPU&mid1=PageSEO | 0.698 | www.newegg.com/Lenovo/BrandStore/ID-10418 | 0.677 | www.newegg.com/Newegg-Select/EventSaleStore/ID-183 | 0.675 |
| playwright | miss | www.newegg.com/ | 0.696 | www.newegg.com/ | 0.660 | www.newegg.com/ | 0.622 |


**Q54: Which brands offer DVI cables on this page?**
*(expects URL containing: `ID-2814`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.771 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.768 | www.newegg.com/HDMI-Cables/SubCategory/ID-2809 | 0.757 |
| crawl4ai-raw | #1 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.771 | www.newegg.com/DVI-Cables/SubCategory/ID-2814 | 0.768 | www.newegg.com/HDMI-Cables/SubCategory/ID-2809 | 0.757 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.692 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.692 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.674 |
| playwright | miss | www.newegg.com/ | 0.692 | www.newegg.com/ | 0.670 | www.newegg.com/ | 0.658 |


**Q55: What brands of enterprise SSDs are available on Newegg?**
*(expects URL containing: `ID-2021`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Enterprise-SSDs/SubCategory/ID-2021 | 0.799 | www.newegg.com/Enterprise-SSDs/SubCategory/ID-2021 | 0.770 | www.newegg.com/Enterprise-SSDs/SubCategory/ID-2021 | 0.767 |
| crawl4ai-raw | #1 | www.newegg.com/Enterprise-SSDs/SubCategory/ID-2021 | 0.799 | www.newegg.com/Enterprise-SSDs/SubCategory/ID-2021 | 0.770 | www.newegg.com/Enterprise-SSDs/SubCategory/ID-2021 | 0.767 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/Gaming-Laptops/SubCategory/ID-3365? | 0.753 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.750 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.748 |
| playwright | miss | www.newegg.com/ | 0.676 | www.newegg.com/ | 0.663 | www.newegg.com/ | 0.654 |


**Q56: What is the maximum sequential read speed of the Micron SSD 2500 PCIe Gen4 NVMe SSD?**
*(expects URL containing: `ID-2021`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #3 | www.newegg.com/SSD/Category/ID-119 | 0.762 | www.newegg.com/Internal-SSDs/SubCategory/ID-636 | 0.760 | www.newegg.com/Enterprise-SSDs/SubCategory/ID-2021 | 0.745 |
| crawl4ai-raw | #3 | www.newegg.com/SSD/Category/ID-119 | 0.762 | www.newegg.com/Internal-SSDs/SubCategory/ID-636 | 0.760 | www.newegg.com/Enterprise-SSDs/SubCategory/ID-2021 | 0.745 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.734 | www.newegg.com/MSI/BrandStore/ID-1312 | 0.730 | www.newegg.com/d/Best-Sellers/SSD/c/ID-119 | 0.724 |
| playwright | miss | www.newegg.com/ | 0.615 | www.newegg.com/ | 0.600 | www.newegg.com/ | 0.580 |


**Q57: What brands are available for laptop add-on cards?**
*(expects URL containing: `ID-421`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.770 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.738 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.729 |
| crawl4ai-raw | #1 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.770 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.738 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.729 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/DELL/BrandStore/ID-10772 | 0.716 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.701 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.701 |
| playwright | miss | www.newegg.com/ | 0.700 | www.newegg.com/ | 0.671 | www.newegg.com/ | 0.660 |


**Q58: What is the price range for laptop add-on cards on Newegg?**
*(expects URL containing: `ID-421`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.796 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.771 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.769 |
| crawl4ai-raw | #1 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.796 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.771 | www.newegg.com/Laptop-Add-on-Cards/SubCategory/ID- | 0.769 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/Gaming-Laptops/s/ID- | 0.773 | www.newegg.com/Business-Laptops/SubCategory/ID-341 | 0.769 | www.newegg.com/p/pl?d=AI-ready+laptops&mid1=PageSE | 0.759 |
| playwright | miss | www.newegg.com/ | 0.748 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.708 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.708 |


</details>

## postgres-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| colly+md | 72% (36/50) | 80% (40/50) | 84% (42/50) | 86% (43/50) | 88% (44/50) | 0.772 | 1115 | 401 |
| crawlee | 72% (36/50) | 80% (40/50) | 80% (40/50) | 88% (44/50) | 88% (44/50) | 0.768 | 1226 | 400 |
| playwright | 72% (36/50) | 80% (40/50) | 80% (40/50) | 88% (44/50) | 88% (44/50) | 0.767 | 1216 | 400 |
| crawl4ai | 70% (35/50) | 78% (39/50) | 82% (41/50) | 88% (44/50) | 92% (46/50) | 0.759 | 1193 | 400 |
| crawl4ai-raw | 70% (35/50) | 78% (39/50) | 82% (41/50) | 88% (44/50) | 92% (46/50) | 0.759 | 1193 | 400 |
| markcrawl | 30% (15/50) | 38% (19/50) | 48% (24/50) | 48% (24/50) | 48% (24/50) | 0.362 | 2348 | 400 |
| scrapy+md | 8% (4/50) | 8% (4/50) | 8% (4/50) | 8% (4/50) | 8% (4/50) | 0.080 | 1531 | 394 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for postgres-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What does this chapter provide an overview of?**
*(expects URL containing: `storage.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/overview.html | 0.608 | www.postgresql.org/docs/current/textsearch.html | 0.576 | www.postgresql.org/docs/current/managing-databases | 0.567 |
| crawl4ai | miss | www.postgresql.org/docs/18/overview.html | 0.565 | www.postgresql.org/docs/current/overview.html | 0.565 | www.postgresql.org/docs/current/catalogs.html | 0.522 |
| crawl4ai-raw | miss | www.postgresql.org/docs/18/overview.html | 0.565 | www.postgresql.org/docs/current/overview.html | 0.565 | www.postgresql.org/docs/current/catalogs.html | 0.522 |
| scrapy+md | miss | www.postgresql.org/docs/7.3/doc-style.html | 0.539 | www.postgresql.org/docs/7.1/doc-sources.html | 0.526 | www.postgresql.org/docs/7.3/doc-sources.html | 0.518 |
| crawlee | miss | www.postgresql.org/docs/18/overview.html | 0.541 | www.postgresql.org/docs/current/overview.html | 0.541 | www.postgresql.org/docs/17/tutorial-start.html | 0.539 |
| colly+md | miss | www.postgresql.org/docs/current/overview.html | 0.541 | www.postgresql.org/docs/16/tutorial-start.html | 0.540 | www.postgresql.org/docs/17/tutorial-start.html | 0.539 |
| playwright | miss | www.postgresql.org/docs/18/overview.html | 0.541 | www.postgresql.org/docs/current/overview.html | 0.541 | www.postgresql.org/docs/17/tutorial-start.html | 0.539 |


**Q2: What is the main topic of Chapter 66?**
*(expects URL containing: `storage.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | www.postgresql.org/docs/current/textsearch.html | 0.497 | www.postgresql.org/docs/current/protocol-flow.html | 0.490 | www.postgresql.org/docs/current/runtime-config-wal | 0.468 |
| crawl4ai | miss | www.postgresql.org/list/pgsql-general/ | 0.452 | www.postgresql.org/docs/18/reference.html | 0.450 | www.postgresql.org/docs/current/reference.html | 0.450 |
| crawl4ai-raw | miss | www.postgresql.org/list/pgsql-general/ | 0.452 | www.postgresql.org/docs/current/reference.html | 0.450 | www.postgresql.org/docs/18/reference.html | 0.450 |
| scrapy+md | miss | www.postgresql.org/docs/7.1/doc-sources.html | 0.430 | www.postgresql.org/docs/13/tcn.html | 0.426 | www.postgresql.org/docs/7.2/doc-sources.html | 0.423 |
| crawlee | #38 | www.postgresql.org/docs/current/reference.html | 0.450 | www.postgresql.org/docs/18/reference.html | 0.450 | www.postgresql.org/docs/18/tutorial.html | 0.447 |
| colly+md | #34 | www.postgresql.org/docs/current/reference.html | 0.450 | www.postgresql.org/docs/18/reference.html | 0.450 | www.postgresql.org/docs/18/tutorial.html | 0.447 |
| playwright | #38 | www.postgresql.org/docs/18/reference.html | 0.450 | www.postgresql.org/docs/current/reference.html | 0.450 | www.postgresql.org/docs/18/tutorial.html | 0.447 |


**Q3: What is PostgreSQL?**
*(expects URL containing: `intro-whatis.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/app-postgres.html | 0.749 | www.postgresql.org/docs/current/glossary.html | 0.746 | www.postgresql.org/docs/current/app-postgres.html | 0.744 |
| crawl4ai | #2 | www.postgresql.org/about/ | 0.819 | www.postgresql.org/docs/17/intro-whatis.html | 0.816 | www.postgresql.org/docs/current/intro-whatis.html | 0.814 |
| crawl4ai-raw | #2 | www.postgresql.org/about/ | 0.819 | www.postgresql.org/docs/17/intro-whatis.html | 0.816 | www.postgresql.org/docs/current/intro-whatis.html | 0.814 |
| scrapy+md | miss | www.postgresql.org/docs/current/ | 0.764 | www.postgresql.org/docs/7.3/developer.html | 0.755 | www.postgresql.org/docs/9.0/ddl-others.html | 0.742 |
| crawlee | #2 | www.postgresql.org/about/ | 0.835 | www.postgresql.org/docs/17/intro-whatis.html | 0.813 | www.postgresql.org/docs/current/intro-whatis.html | 0.810 |
| colly+md | #2 | www.postgresql.org/about/ | 0.835 | www.postgresql.org/docs/16/intro-whatis.html | 0.817 | www.postgresql.org/docs/17/intro-whatis.html | 0.813 |
| playwright | #2 | www.postgresql.org/about/ | 0.835 | www.postgresql.org/docs/17/intro-whatis.html | 0.813 | www.postgresql.org/docs/18/intro-whatis.html | 0.810 |


**Q4: What type of database management system is PostgreSQL?**
*(expects URL containing: `intro-whatis.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/app-postgres.html | 0.749 | www.postgresql.org/docs/current/app-postgres.html | 0.749 | www.postgresql.org/docs/current/index.html | 0.735 |
| crawl4ai | #2 | www.postgresql.org/about/ | 0.803 | www.postgresql.org/docs/17/intro-whatis.html | 0.800 | www.postgresql.org/docs/18/intro-whatis.html | 0.799 |
| crawl4ai-raw | #2 | www.postgresql.org/about/ | 0.803 | www.postgresql.org/docs/17/intro-whatis.html | 0.800 | www.postgresql.org/docs/18/intro-whatis.html | 0.799 |
| scrapy+md | miss | www.postgresql.org/docs/current/ | 0.749 | www.postgresql.org/docs/9.0/ddl-others.html | 0.727 | www.postgresql.org/docs/7.3/developer.html | 0.726 |
| crawlee | #1 | www.postgresql.org/docs/17/intro-whatis.html | 0.799 | www.postgresql.org/docs/current/intro-whatis.html | 0.796 | www.postgresql.org/docs/18/intro-whatis.html | 0.796 |
| colly+md | #1 | www.postgresql.org/docs/17/intro-whatis.html | 0.799 | www.postgresql.org/docs/16/intro-whatis.html | 0.798 | www.postgresql.org/docs/18/intro-whatis.html | 0.796 |
| playwright | #1 | www.postgresql.org/docs/17/intro-whatis.html | 0.799 | www.postgresql.org/docs/18/intro-whatis.html | 0.796 | www.postgresql.org/docs/current/intro-whatis.html | 0.796 |


**Q5: What does this chapter provide an overview of?**
*(expects URL containing: `overview.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/overview.html | 0.608 | www.postgresql.org/docs/current/textsearch.html | 0.576 | www.postgresql.org/docs/current/managing-databases | 0.567 |
| crawl4ai | #1 | www.postgresql.org/docs/18/overview.html | 0.565 | www.postgresql.org/docs/current/overview.html | 0.565 | www.postgresql.org/docs/current/catalogs.html | 0.522 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/overview.html | 0.565 | www.postgresql.org/docs/current/overview.html | 0.565 | www.postgresql.org/docs/current/catalogs.html | 0.522 |
| scrapy+md | miss | www.postgresql.org/docs/7.3/doc-style.html | 0.539 | www.postgresql.org/docs/7.1/doc-sources.html | 0.526 | www.postgresql.org/docs/7.3/doc-sources.html | 0.518 |
| crawlee | #1 | www.postgresql.org/docs/18/overview.html | 0.541 | www.postgresql.org/docs/current/overview.html | 0.541 | www.postgresql.org/docs/17/tutorial-start.html | 0.539 |
| colly+md | #1 | www.postgresql.org/docs/current/overview.html | 0.541 | www.postgresql.org/docs/16/tutorial-start.html | 0.540 | www.postgresql.org/docs/17/tutorial-start.html | 0.539 |
| playwright | #1 | www.postgresql.org/docs/18/overview.html | 0.541 | www.postgresql.org/docs/current/overview.html | 0.541 | www.postgresql.org/docs/17/tutorial-start.html | 0.539 |


**Q6: What should you understand after reading the following sections of this chapter?**
*(expects URL containing: `overview.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | www.postgresql.org/docs/current/contrib.html | 0.584 | www.postgresql.org/docs/current/overview.html | 0.572 | www.postgresql.org/docs/current/sql-explain.html | 0.570 |
| crawl4ai | #3 | www.postgresql.org/docs/18/contrib.html | 0.559 | www.postgresql.org/docs/current/contrib.html | 0.559 | www.postgresql.org/docs/18/overview.html | 0.552 |
| crawl4ai-raw | #3 | www.postgresql.org/docs/current/contrib.html | 0.559 | www.postgresql.org/docs/18/contrib.html | 0.559 | www.postgresql.org/docs/18/overview.html | 0.552 |
| scrapy+md | miss | www.postgresql.org/docs/7.4/sql-explain.html | 0.545 | www.postgresql.org/docs/7.3/doc-style.html | 0.536 | www.postgresql.org/docs/8.0/admin.html | 0.533 |
| crawlee | miss | www.postgresql.org/docs/18/contrib.html | 0.590 | www.postgresql.org/docs/current/contrib.html | 0.590 | www.postgresql.org/docs/18/ddl.html | 0.551 |
| colly+md | miss | www.postgresql.org/docs/current/contrib.html | 0.590 | www.postgresql.org/docs/16/ddl.html | 0.553 | www.postgresql.org/docs/17/ddl.html | 0.551 |
| playwright | miss | www.postgresql.org/docs/18/contrib.html | 0.590 | www.postgresql.org/docs/current/contrib.html | 0.590 | www.postgresql.org/docs/17/ddl.html | 0.551 |


**Q7: What does the information schema consist of?**
*(expects URL containing: `information-schema.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/information-schema | 0.696 | www.postgresql.org/docs/current/ddl.html | 0.634 | www.postgresql.org/docs/current/functions-info.htm | 0.632 |
| crawl4ai | #7 | www.postgresql.org/docs/18/reference.html | 0.617 | www.postgresql.org/docs/current/reference.html | 0.617 | www.postgresql.org/docs/18/glossary.html | 0.615 |
| crawl4ai-raw | #7 | www.postgresql.org/docs/18/reference.html | 0.617 | www.postgresql.org/docs/current/reference.html | 0.617 | www.postgresql.org/docs/18/glossary.html | 0.615 |
| scrapy+md | miss | www.postgresql.org/docs/9.0/ddl.html | 0.614 | www.postgresql.org/docs/9.3/functions-info.html | 0.613 | www.postgresql.org/docs/9.0/ddl-schemas.html | 0.612 |
| crawlee | #10 | www.postgresql.org/docs/17/ddl.html | 0.646 | www.postgresql.org/docs/current/ddl.html | 0.646 | www.postgresql.org/docs/18/ddl.html | 0.646 |
| colly+md | #9 | www.postgresql.org/docs/16/ddl.html | 0.653 | www.postgresql.org/docs/current/ddl.html | 0.646 | www.postgresql.org/docs/17/ddl.html | 0.646 |
| playwright | #10 | www.postgresql.org/docs/18/ddl.html | 0.646 | www.postgresql.org/docs/17/ddl.html | 0.646 | www.postgresql.org/docs/current/ddl.html | 0.646 |


**Q8: Why might a standard-compliant query return several rows when querying for constraint information?**
*(expects URL containing: `information-schema.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #33 | www.postgresql.org/docs/current/sql-select.html | 0.763 | www.postgresql.org/docs/current/sql-insert.html | 0.729 | www.postgresql.org/docs/current/sql-createdomain.h | 0.724 |
| crawl4ai | #1 | www.postgresql.org/docs/18/information-schema.html | 0.774 | www.postgresql.org/docs/current/information-schema | 0.774 | www.postgresql.org/docs/17/information-schema.html | 0.774 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/information-schema.html | 0.774 | www.postgresql.org/docs/current/information-schema | 0.774 | www.postgresql.org/docs/17/information-schema.html | 0.774 |
| scrapy+md | miss | www.postgresql.org/docs/7.4/sql-createtable.html | 0.711 | www.postgresql.org/docs/7.4/sql-select.html | 0.709 | www.postgresql.org/docs/8.0/ddl-constraints.html | 0.705 |
| crawlee | #1 | www.postgresql.org/docs/18/information-schema.html | 0.773 | www.postgresql.org/docs/current/information-schema | 0.773 | www.postgresql.org/docs/17/information-schema.html | 0.773 |
| colly+md | #1 | www.postgresql.org/docs/current/information-schema | 0.773 | www.postgresql.org/docs/18/information-schema.html | 0.773 | www.postgresql.org/docs/17/information-schema.html | 0.773 |
| playwright | #1 | www.postgresql.org/docs/current/information-schema | 0.773 | www.postgresql.org/docs/17/information-schema.html | 0.773 | www.postgresql.org/docs/18/information-schema.html | 0.773 |


**Q9: What is the customary TCP port number for servers supporting the PostgreSQL protocol?**
*(expects URL containing: `protocol.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #23 | www.postgresql.org/docs/current/runtime-config-con | 0.775 | www.postgresql.org/docs/current/ssh-tunnels.html | 0.746 | www.postgresql.org/docs/current/app-pg-dumpall.htm | 0.745 |
| crawl4ai | #1 | www.postgresql.org/docs/current/protocol.html | 0.767 | www.postgresql.org/docs/18/protocol.html | 0.767 | www.postgresql.org/docs/18/acronyms.html | 0.734 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/protocol.html | 0.767 | www.postgresql.org/docs/18/protocol.html | 0.767 | www.postgresql.org/docs/18/acronyms.html | 0.734 |
| scrapy+md | miss | www.postgresql.org/docs/9.2/libpq-connect.html | 0.741 | www.postgresql.org/docs/9.2/libpq-connect.html | 0.739 | www.postgresql.org/docs/9.2/libpq-envars.html | 0.738 |
| crawlee | #1 | www.postgresql.org/docs/current/protocol.html | 0.760 | www.postgresql.org/docs/18/protocol.html | 0.760 | www.postgresql.org/about/featurematrix/ | 0.734 |
| colly+md | #1 | www.postgresql.org/docs/current/protocol.html | 0.760 | www.postgresql.org/about/featurematrix/ | 0.734 | www.postgresql.org/docs/16/libpq.html | 0.729 |
| playwright | #1 | www.postgresql.org/docs/current/protocol.html | 0.760 | www.postgresql.org/docs/18/protocol.html | 0.760 | www.postgresql.org/about/featurematrix/ | 0.734 |


**Q10: What version of the protocol was introduced in PostgreSQL version 18?**
*(expects URL containing: `protocol.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | www.postgresql.org/docs/current/libpq-connect.html | 0.752 | www.postgresql.org/docs/current/protocol.html | 0.741 | www.postgresql.org/docs/current/index.html | 0.721 |
| crawl4ai | #1 | www.postgresql.org/docs/current/protocol.html | 0.789 | www.postgresql.org/docs/18/protocol.html | 0.789 | www.postgresql.org/docs/current/source.html | 0.781 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/protocol.html | 0.789 | www.postgresql.org/docs/18/protocol.html | 0.789 | www.postgresql.org/docs/current/source.html | 0.781 |
| scrapy+md | miss | www.postgresql.org/docs/current/sspi-auth.html | 0.797 | www.postgresql.org/docs/18/tcn.html | 0.785 | www.postgresql.org/docs/current/bookindex.html | 0.780 |
| crawlee | #1 | www.postgresql.org/docs/18/protocol.html | 0.819 | www.postgresql.org/docs/current/protocol.html | 0.819 | www.postgresql.org/docs/18/source.html | 0.779 |
| colly+md | #1 | www.postgresql.org/docs/current/protocol.html | 0.819 | www.postgresql.org/docs/current/source.html | 0.779 | www.postgresql.org/docs/18/spi.html | 0.776 |
| playwright | #1 | www.postgresql.org/docs/current/protocol.html | 0.819 | www.postgresql.org/docs/18/protocol.html | 0.819 | www.postgresql.org/docs/current/source.html | 0.779 |


**Q11: What is the purpose of logical decoding in PostgreSQL?**
*(expects URL containing: `logicaldecoding.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | www.postgresql.org/docs/current/logicaldecoding-ex | 0.783 | www.postgresql.org/docs/current/logicaldecoding-ex | 0.777 | www.postgresql.org/docs/current/logicaldecoding.ht | 0.761 |
| crawl4ai | #1 | www.postgresql.org/docs/current/logicaldecoding.ht | 0.765 | www.postgresql.org/docs/18/logicaldecoding.html | 0.765 | www.postgresql.org/docs/18/replication-origins.htm | 0.730 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/logicaldecoding.ht | 0.765 | www.postgresql.org/docs/18/logicaldecoding.html | 0.765 | www.postgresql.org/docs/18/replication-origins.htm | 0.730 |
| scrapy+md | miss | www.postgresql.org/docs/12/test-decoding.html | 0.802 | www.postgresql.org/docs/15/test-decoding.html | 0.800 | www.postgresql.org/docs/11/test-decoding.html | 0.800 |
| crawlee | #1 | www.postgresql.org/docs/17/logicaldecoding.html | 0.774 | www.postgresql.org/docs/18/logicaldecoding.html | 0.771 | www.postgresql.org/docs/current/logicaldecoding.ht | 0.771 |
| colly+md | #1 | www.postgresql.org/docs/current/logicaldecoding.ht | 0.771 | www.postgresql.org/docs/18/logicaldecoding.html | 0.771 | www.postgresql.org/docs/18/logicaldecoding.html | 0.766 |
| playwright | #1 | www.postgresql.org/docs/current/logicaldecoding.ht | 0.771 | www.postgresql.org/docs/18/logicaldecoding.html | 0.771 | www.postgresql.org/docs/18/logicaldecoding.html | 0.766 |


**Q12: How are changes streamed in logical decoding?**
*(expects URL containing: `logicaldecoding.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | www.postgresql.org/docs/current/logicaldecoding-ex | 0.746 | www.postgresql.org/docs/current/logicaldecoding-st | 0.741 | www.postgresql.org/docs/current/logicaldecoding-st | 0.730 |
| crawl4ai | #1 | www.postgresql.org/docs/current/logicaldecoding.ht | 0.680 | www.postgresql.org/docs/18/logicaldecoding.html | 0.680 | www.postgresql.org/docs/18/replication-origins.htm | 0.673 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/logicaldecoding.ht | 0.680 | www.postgresql.org/docs/18/logicaldecoding.html | 0.680 | www.postgresql.org/docs/18/replication-origins.htm | 0.673 |
| scrapy+md | miss | www.postgresql.org/docs/15/test-decoding.html | 0.710 | www.postgresql.org/docs/14/test-decoding.html | 0.709 | www.postgresql.org/docs/18/test-decoding.html | 0.700 |
| crawlee | #1 | www.postgresql.org/docs/current/logicaldecoding.ht | 0.731 | www.postgresql.org/docs/18/logicaldecoding.html | 0.731 | www.postgresql.org/docs/17/logicaldecoding.html | 0.731 |
| colly+md | #1 | www.postgresql.org/docs/current/logicaldecoding.ht | 0.731 | www.postgresql.org/docs/18/logicaldecoding.html | 0.731 | www.postgresql.org/docs/current/contrib.html | 0.664 |
| playwright | #1 | www.postgresql.org/docs/18/logicaldecoding.html | 0.731 | www.postgresql.org/docs/current/logicaldecoding.ht | 0.731 | www.postgresql.org/docs/current/contrib.html | 0.664 |


**Q13: What are the four procedural languages available in the standard PostgreSQL distribution?**
*(expects URL containing: `xplang.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/xplang.html | 0.839 | www.postgresql.org/docs/current/xfunc-pl.html | 0.805 | www.postgresql.org/docs/current/index.html | 0.787 |
| crawl4ai | #1 | www.postgresql.org/docs/17/xplang.html | 0.841 | www.postgresql.org/docs/18/xplang.html | 0.840 | www.postgresql.org/docs/current/xplang.html | 0.840 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/xplang.html | 0.841 | www.postgresql.org/docs/18/xplang.html | 0.840 | www.postgresql.org/docs/current/xplang.html | 0.840 |
| scrapy+md | miss | www.postgresql.org/docs/current/ | 0.793 | www.postgresql.org/docs/9.0/server-programming.htm | 0.783 | www.postgresql.org/docs/9.1/plpython-python23.html | 0.754 |
| crawlee | #1 | www.postgresql.org/docs/17/xplang.html | 0.841 | www.postgresql.org/docs/current/xplang.html | 0.839 | www.postgresql.org/docs/18/xplang.html | 0.839 |
| colly+md | #1 | www.postgresql.org/docs/17/xplang.html | 0.841 | www.postgresql.org/docs/18/xplang.html | 0.839 | www.postgresql.org/docs/current/xplang.html | 0.839 |
| playwright | #1 | www.postgresql.org/docs/17/xplang.html | 0.841 | www.postgresql.org/docs/current/xplang.html | 0.839 | www.postgresql.org/docs/18/xplang.html | 0.839 |


**Q14: How does PostgreSQL handle functions written in procedural languages?**
*(expects URL containing: `xplang.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/xplang.html | 0.817 | www.postgresql.org/docs/current/xfunc-pl.html | 0.809 | www.postgresql.org/docs/current/sql-createlanguage | 0.807 |
| crawl4ai | #1 | www.postgresql.org/docs/17/xplang.html | 0.848 | www.postgresql.org/docs/current/xplang.html | 0.846 | www.postgresql.org/docs/18/xplang.html | 0.846 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/xplang.html | 0.848 | www.postgresql.org/docs/current/xplang.html | 0.846 | www.postgresql.org/docs/18/xplang.html | 0.846 |
| scrapy+md | miss | www.postgresql.org/docs/9.0/server-programming.htm | 0.800 | www.postgresql.org/docs/current/ | 0.797 | www.postgresql.org/docs/7.4/sql.html | 0.782 |
| crawlee | #1 | www.postgresql.org/docs/17/xplang.html | 0.830 | www.postgresql.org/docs/current/xplang.html | 0.828 | www.postgresql.org/docs/18/xplang.html | 0.828 |
| colly+md | #1 | www.postgresql.org/docs/17/xplang.html | 0.830 | www.postgresql.org/docs/current/xplang.html | 0.828 | www.postgresql.org/docs/18/xplang.html | 0.828 |
| playwright | #1 | www.postgresql.org/docs/17/xplang.html | 0.830 | www.postgresql.org/docs/current/xplang.html | 0.828 | www.postgresql.org/docs/18/xplang.html | 0.828 |


**Q15: What resources are available for PostgreSQL besides the documentation?**
*(expects URL containing: `resources.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/index.html | 0.800 | www.postgresql.org/docs/current/contrib.html | 0.786 | www.postgresql.org/docs/current/sql.html | 0.771 |
| crawl4ai | #7 | www.postgresql.org/docs/18/docguide.html | 0.839 | www.postgresql.org/docs/current/docguide.html | 0.839 | www.postgresql.org/docs/8.4/index.html | 0.831 |
| crawl4ai-raw | #7 | www.postgresql.org/docs/current/docguide.html | 0.839 | www.postgresql.org/docs/18/docguide.html | 0.839 | www.postgresql.org/docs/8.4/index.html | 0.831 |
| scrapy+md | miss | www.postgresql.org/docs/7.1/docguide.html | 0.846 | www.postgresql.org/docs/7.3/biblio.html | 0.829 | www.postgresql.org/docs/7.2/biblio.html | 0.828 |
| crawlee | #10 | www.postgresql.org/docs/online-resources/ | 0.851 | www.postgresql.org/docs/8.3/index.html | 0.835 | www.postgresql.org/docs/7.4/index.html | 0.831 |
| colly+md | #5 | www.postgresql.org/docs/online-resources/ | 0.851 | www.postgresql.org/docs/8.3/index.html | 0.835 | www.postgresql.org/docs/7.4/index.html | 0.831 |
| playwright | #10 | www.postgresql.org/docs/online-resources/ | 0.851 | www.postgresql.org/docs/8.3/index.html | 0.835 | www.postgresql.org/docs/7.4/index.html | 0.831 |


**Q16: How can I contribute to the PostgreSQL community?**
*(expects URL containing: `resources.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/runtime-config-rep | 0.682 | www.postgresql.org/docs/current/extend-pgxs.html | 0.673 | www.postgresql.org/docs/current/admin.html | 0.671 |
| crawl4ai | #11 | www.postgresql.org/about/donate/ | 0.798 | www.postgresql.org/developer/related-projects/ | 0.794 | www.postgresql.org/about/donate_pg_org/ | 0.792 |
| crawl4ai-raw | #11 | www.postgresql.org/about/donate/ | 0.798 | www.postgresql.org/developer/related-projects/ | 0.794 | www.postgresql.org/about/donate_pg_org/ | 0.792 |
| scrapy+md | miss | www.postgresql.org/community/user-groups/ | 0.770 | www.postgresql.org/about/policies/npos/ | 0.756 | www.postgresql.org/about/contact/ | 0.750 |
| crawlee | #34 | www.postgresql.org/about/donate/ | 0.810 | www.postgresql.org/about/donate_pg_org/ | 0.803 | www.postgresql.org/community/ | 0.800 |
| colly+md | #29 | www.postgresql.org/about/donate/ | 0.810 | www.postgresql.org/about/donate/pg/org/ | 0.803 | www.postgresql.org/community/ | 0.800 |
| playwright | #35 | www.postgresql.org/community/ | 0.810 | www.postgresql.org/about/donate/ | 0.810 | www.postgresql.org/about/donate_pg_org/ | 0.803 |


**Q17: What is the title of the book authored by Jesús Espino?**
*(expects URL containing: `books`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/functions-enum.htm | 0.411 | www.postgresql.org/docs/current/textsearch-feature | 0.397 | www.postgresql.org/docs/current/datetime-julian-da | 0.396 |
| crawl4ai | #1 | www.postgresql.org/docs/books/ | 0.459 | www.postgresql.org/docs/books/ | 0.446 | www.postgresql.org/docs/books/ | 0.435 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/books/ | 0.459 | www.postgresql.org/docs/books/ | 0.446 | www.postgresql.org/docs/books/ | 0.435 |
| scrapy+md | miss | www.postgresql.org/docs/current/sql-createpublicat | 0.377 | www.postgresql.org/docs/current/bookindex.html | 0.371 | www.postgresql.org/docs/7.1/docguide.html | 0.368 |
| crawlee | #1 | www.postgresql.org/docs/books/ | 0.442 | www.postgresql.org/docs/books/ | 0.432 | www.postgresql.org/docs/books/ | 0.432 |
| colly+md | #1 | www.postgresql.org/docs/books/ | 0.442 | www.postgresql.org/docs/books/ | 0.432 | www.postgresql.org/docs/books/ | 0.432 |
| playwright | #1 | www.postgresql.org/docs/books/ | 0.442 | www.postgresql.org/docs/books/ | 0.432 | www.postgresql.org/docs/books/ | 0.432 |


**Q18: Who are the authors of the book 'PostgreSQL 16 Administration Cookbook'?**
*(expects URL containing: `books`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/contrib.html | 0.701 | www.postgresql.org/docs/current/index.html | 0.700 | www.postgresql.org/docs/current/admin.html | 0.697 |
| crawl4ai | #1 | www.postgresql.org/docs/books/ | 0.773 | www.postgresql.org/docs/books/ | 0.767 | www.postgresql.org/docs/books/ | 0.766 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/books/ | 0.773 | www.postgresql.org/docs/books/ | 0.767 | www.postgresql.org/docs/books/ | 0.766 |
| scrapy+md | miss | www.postgresql.org/docs/7.1/biblio.html | 0.734 | www.postgresql.org/docs/current/biblio.html | 0.721 | www.postgresql.org/docs/8.1/biblio.html | 0.709 |
| crawlee | #1 | www.postgresql.org/docs/books/ | 0.791 | www.postgresql.org/docs/books/ | 0.787 | www.postgresql.org/docs/books/ | 0.766 |
| colly+md | #1 | www.postgresql.org/docs/books/ | 0.791 | www.postgresql.org/docs/books/ | 0.787 | www.postgresql.org/docs/books/ | 0.766 |
| playwright | #1 | www.postgresql.org/docs/books/ | 0.791 | www.postgresql.org/docs/books/ | 0.787 | www.postgresql.org/docs/books/ | 0.766 |


**Q19: What are the facilities PostgreSQL has for evaluating mixed-type expressions?**
*(expects URL containing: `typeconv.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/typeconv.html | 0.771 | www.postgresql.org/docs/current/typeconv-oper.html | 0.754 | www.postgresql.org/docs/current/typeconv-overview. | 0.749 |
| crawl4ai | #1 | www.postgresql.org/docs/current/typeconv.html | 0.789 | www.postgresql.org/docs/18/typeconv.html | 0.789 | www.postgresql.org/docs/17/typeconv.html | 0.789 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/typeconv.html | 0.789 | www.postgresql.org/docs/18/typeconv.html | 0.789 | www.postgresql.org/docs/17/typeconv.html | 0.789 |
| scrapy+md | miss | www.postgresql.org/docs/8.1/functions.html | 0.766 | www.postgresql.org/docs/7.4/sql.html | 0.758 | www.postgresql.org/docs/7.3/functions.html | 0.757 |
| crawlee | #1 | www.postgresql.org/docs/current/typeconv.html | 0.773 | www.postgresql.org/docs/18/typeconv.html | 0.773 | www.postgresql.org/docs/17/typeconv.html | 0.770 |
| colly+md | #1 | www.postgresql.org/docs/16/typeconv.html | 0.774 | www.postgresql.org/docs/current/typeconv.html | 0.773 | www.postgresql.org/docs/18/typeconv.html | 0.773 |
| playwright | #1 | www.postgresql.org/docs/current/typeconv.html | 0.773 | www.postgresql.org/docs/18/typeconv.html | 0.773 | www.postgresql.org/docs/17/typeconv.html | 0.770 |


**Q20: How can explicit type conversion affect the results of a query in PostgreSQL?**
*(expects URL containing: `typeconv.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/typeconv.html | 0.798 | www.postgresql.org/docs/current/typeconv-union-cas | 0.782 | www.postgresql.org/docs/current/sql-createtype.htm | 0.779 |
| crawl4ai | #1 | www.postgresql.org/docs/17/typeconv.html | 0.798 | www.postgresql.org/docs/18/typeconv.html | 0.798 | www.postgresql.org/docs/current/typeconv.html | 0.798 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/typeconv.html | 0.798 | www.postgresql.org/docs/18/typeconv.html | 0.798 | www.postgresql.org/docs/current/typeconv.html | 0.798 |
| scrapy+md | miss | www.postgresql.org/docs/7.4/sql-select.html | 0.752 | www.postgresql.org/docs/9.0/datatype-oid.html | 0.741 | www.postgresql.org/docs/9.2/multibyte.html | 0.735 |
| crawlee | #1 | www.postgresql.org/docs/current/typeconv.html | 0.799 | www.postgresql.org/docs/18/typeconv.html | 0.799 | www.postgresql.org/docs/17/typeconv.html | 0.798 |
| colly+md | #1 | www.postgresql.org/docs/current/typeconv.html | 0.799 | www.postgresql.org/docs/18/typeconv.html | 0.799 | www.postgresql.org/docs/17/typeconv.html | 0.798 |
| playwright | #1 | www.postgresql.org/docs/current/typeconv.html | 0.799 | www.postgresql.org/docs/18/typeconv.html | 0.799 | www.postgresql.org/docs/17/typeconv.html | 0.798 |


**Q21: What are the three fundamentally different approaches to backing up PostgreSQL data?**
*(expects URL containing: `backup.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/continuous-archivi | 0.747 | www.postgresql.org/docs/current/continuous-archivi | 0.726 | www.postgresql.org/docs/current/continuous-archivi | 0.719 |
| crawl4ai | #1 | www.postgresql.org/docs/17/backup.html | 0.824 | www.postgresql.org/docs/current/backup.html | 0.824 | www.postgresql.org/docs/18/backup.html | 0.824 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/backup.html | 0.824 | www.postgresql.org/docs/current/backup.html | 0.824 | www.postgresql.org/docs/18/backup.html | 0.824 |
| scrapy+md | #1 | www.postgresql.org/docs/8.0/backup.html | 0.816 | www.postgresql.org/docs/8.0/backup.html | 0.769 | www.postgresql.org/docs/8.0/backup.html | 0.726 |
| crawlee | #1 | www.postgresql.org/docs/18/backup.html | 0.788 | www.postgresql.org/docs/current/backup.html | 0.788 | www.postgresql.org/docs/17/backup.html | 0.787 |
| colly+md | #1 | www.postgresql.org/docs/16/backup.html | 0.803 | www.postgresql.org/docs/current/backup.html | 0.788 | www.postgresql.org/docs/18/backup.html | 0.788 |
| playwright | #1 | www.postgresql.org/docs/18/backup.html | 0.788 | www.postgresql.org/docs/current/backup.html | 0.788 | www.postgresql.org/docs/17/backup.html | 0.787 |


**Q22: What is the importance of backing up PostgreSQL databases regularly?**
*(expects URL containing: `backup.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/continuous-archivi | 0.736 | www.postgresql.org/docs/current/continuous-archivi | 0.733 | www.postgresql.org/docs/current/wal-reliability.ht | 0.732 |
| crawl4ai | #1 | www.postgresql.org/docs/17/backup.html | 0.761 | www.postgresql.org/docs/18/backup.html | 0.760 | www.postgresql.org/docs/current/backup.html | 0.760 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/backup.html | 0.761 | www.postgresql.org/docs/18/backup.html | 0.760 | www.postgresql.org/docs/current/backup.html | 0.760 |
| scrapy+md | #1 | www.postgresql.org/docs/8.0/backup.html | 0.740 | www.postgresql.org/docs/8.0/admin.html | 0.714 | www.postgresql.org/docs/8.0/maintenance.html | 0.707 |
| crawlee | #1 | www.postgresql.org/docs/18/backup.html | 0.724 | www.postgresql.org/docs/current/backup.html | 0.724 | www.postgresql.org/docs/17/backup.html | 0.723 |
| colly+md | #1 | www.postgresql.org/docs/16/backup.html | 0.735 | www.postgresql.org/docs/16/maintenance.html | 0.725 | www.postgresql.org/docs/18/backup.html | 0.724 |
| playwright | #1 | www.postgresql.org/docs/18/backup.html | 0.724 | www.postgresql.org/docs/current/backup.html | 0.724 | www.postgresql.org/docs/17/backup.html | 0.723 |


**Q23: What is the recommended way to install PostgreSQL for users of the system?**
*(expects URL containing: `install-binaries.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/install-make.html | 0.812 | www.postgresql.org/docs/current/install-make.html | 0.773 | www.postgresql.org/docs/current/install-make.html | 0.759 |
| crawl4ai | #1 | www.postgresql.org/docs/17/install-binaries.html | 0.833 | www.postgresql.org/docs/current/install-binaries.h | 0.832 | www.postgresql.org/docs/18/install-binaries.html | 0.832 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/install-binaries.html | 0.833 | www.postgresql.org/docs/current/install-binaries.h | 0.832 | www.postgresql.org/docs/18/install-binaries.html | 0.832 |
| scrapy+md | miss | www.postgresql.org/docs/9.1/install-procedure.html | 0.816 | www.postgresql.org/docs/9.1/install-procedure.html | 0.798 | www.postgresql.org/docs/9.1/install-procedure.html | 0.760 |
| crawlee | #2 | www.postgresql.org/download/linux/redhat | 0.816 | www.postgresql.org/docs/current/install-binaries.h | 0.809 | www.postgresql.org/docs/18/install-binaries.html | 0.809 |
| colly+md | #2 | www.postgresql.org/download/linux/redhat/ | 0.816 | www.postgresql.org/docs/16/install-binaries.html | 0.811 | www.postgresql.org/docs/current/install-binaries.h | 0.809 |
| playwright | #2 | www.postgresql.org/download/linux/redhat | 0.816 | www.postgresql.org/docs/18/install-binaries.html | 0.809 | www.postgresql.org/docs/current/install-binaries.h | 0.809 |


**Q24: Where can I find an updated list of platforms providing binary packages for PostgreSQL?**
*(expects URL containing: `install-binaries.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/pgupgrade.html | 0.777 | www.postgresql.org/docs/current/runtime-config-com | 0.751 | www.postgresql.org/docs/current/install-make.html | 0.741 |
| crawl4ai | #1 | www.postgresql.org/docs/18/install-binaries.html | 0.830 | www.postgresql.org/docs/current/install-binaries.h | 0.830 | www.postgresql.org/docs/17/install-binaries.html | 0.830 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/install-binaries.html | 0.830 | www.postgresql.org/docs/current/install-binaries.h | 0.830 | www.postgresql.org/docs/17/install-binaries.html | 0.830 |
| scrapy+md | miss | www.postgresql.org/docs/7.3/release-0-03.html | 0.787 | www.postgresql.org/docs/7.2/release-0-03.html | 0.787 | www.postgresql.org/docs/7.4/release-0-03.html | 0.787 |
| crawlee | #2 | www.postgresql.org/download/ | 0.836 | www.postgresql.org/docs/current/install-binaries.h | 0.819 | www.postgresql.org/docs/18/install-binaries.html | 0.819 |
| colly+md | #2 | www.postgresql.org/download/ | 0.836 | www.postgresql.org/docs/18/install-binaries.html | 0.819 | www.postgresql.org/docs/current/install-binaries.h | 0.819 |
| playwright | #2 | www.postgresql.org/download/ | 0.836 | www.postgresql.org/docs/18/install-binaries.html | 0.819 | www.postgresql.org/docs/current/install-binaries.h | 0.819 |


**Q25: What is the process by which the database server establishes the identity of the client?**
*(expects URL containing: `client-authentication.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/connect-estab.html | 0.714 | www.postgresql.org/docs/current/manage-ag-createdb | 0.669 | www.postgresql.org/docs/current/manage-ag-createdb | 0.667 |
| crawl4ai | #1 | www.postgresql.org/docs/17/client-authentication.h | 0.713 | www.postgresql.org/docs/current/client-authenticat | 0.713 | www.postgresql.org/docs/18/client-authentication.h | 0.713 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/client-authentication.h | 0.713 | www.postgresql.org/docs/current/client-authenticat | 0.713 | www.postgresql.org/docs/18/client-authentication.h | 0.713 |
| scrapy+md | miss | www.postgresql.org/docs/current/database-roles.htm | 0.719 | www.postgresql.org/docs/current/database-roles.htm | 0.688 | www.postgresql.org/docs/8.3/sql-createrole.html | 0.664 |
| crawlee | #1 | www.postgresql.org/docs/17/client-authentication.h | 0.712 | www.postgresql.org/docs/18/client-authentication.h | 0.712 | www.postgresql.org/docs/current/client-authenticat | 0.712 |
| colly+md | #1 | www.postgresql.org/docs/16/client-authentication.h | 0.714 | www.postgresql.org/docs/18/client-authentication.h | 0.712 | www.postgresql.org/docs/17/client-authentication.h | 0.712 |
| playwright | #1 | www.postgresql.org/docs/17/client-authentication.h | 0.712 | www.postgresql.org/docs/18/client-authentication.h | 0.712 | www.postgresql.org/docs/current/client-authenticat | 0.712 |


**Q26: How does PostgreSQL determine which database users can connect?**
*(expects URL containing: `client-authentication.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/manage-ag-overview | 0.762 | www.postgresql.org/docs/current/app-psql.html | 0.756 | www.postgresql.org/docs/current/runtime-config-con | 0.751 |
| crawl4ai | #1 | www.postgresql.org/docs/18/client-authentication.h | 0.819 | www.postgresql.org/docs/17/client-authentication.h | 0.819 | www.postgresql.org/docs/current/client-authenticat | 0.819 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/client-authentication.h | 0.819 | www.postgresql.org/docs/current/client-authenticat | 0.819 | www.postgresql.org/docs/17/client-authentication.h | 0.819 |
| scrapy+md | miss | www.postgresql.org/docs/current/database-roles.htm | 0.774 | www.postgresql.org/docs/8.3/app-psql.html | 0.750 | www.postgresql.org/docs/9.2/libpq-envars.html | 0.738 |
| crawlee | #1 | www.postgresql.org/docs/17/client-authentication.h | 0.816 | www.postgresql.org/docs/current/client-authenticat | 0.816 | www.postgresql.org/docs/18/client-authentication.h | 0.816 |
| colly+md | #1 | www.postgresql.org/docs/18/client-authentication.h | 0.816 | www.postgresql.org/docs/current/client-authenticat | 0.816 | www.postgresql.org/docs/17/client-authentication.h | 0.816 |
| playwright | #1 | www.postgresql.org/docs/current/client-authenticat | 0.816 | www.postgresql.org/docs/17/client-authentication.h | 0.816 | www.postgresql.org/docs/18/client-authentication.h | 0.816 |


**Q27: What is the difference between a warm standby server and a hot standby server?**
*(expects URL containing: `high-availability.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | www.postgresql.org/docs/current/warm-standby.html | 0.666 | www.postgresql.org/docs/current/runtime-config-rep | 0.648 | www.postgresql.org/docs/current/warm-standby.html | 0.645 |
| crawl4ai | #1 | www.postgresql.org/docs/current/high-availability. | 0.671 | www.postgresql.org/docs/18/high-availability.html | 0.671 | www.postgresql.org/docs/17/high-availability.html | 0.671 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/high-availability. | 0.671 | www.postgresql.org/docs/18/high-availability.html | 0.671 | www.postgresql.org/docs/17/high-availability.html | 0.671 |
| scrapy+md | miss | www.postgresql.org/docs/current/bookindex.html | 0.588 | www.postgresql.org/docs/7.4/app-pg-ctl.html | 0.552 | www.postgresql.org/docs/8.1/app-pg-ctl.html | 0.544 |
| crawlee | #1 | www.postgresql.org/docs/18/high-availability.html | 0.674 | www.postgresql.org/docs/current/high-availability. | 0.674 | www.postgresql.org/docs/17/high-availability.html | 0.674 |
| colly+md | #1 | www.postgresql.org/docs/16/high-availability.html | 0.674 | www.postgresql.org/docs/17/high-availability.html | 0.674 | www.postgresql.org/docs/current/high-availability. | 0.674 |
| playwright | #1 | www.postgresql.org/docs/current/high-availability. | 0.674 | www.postgresql.org/docs/18/high-availability.html | 0.674 | www.postgresql.org/docs/17/high-availability.html | 0.674 |


**Q28: How do synchronous and asynchronous solutions differ in terms of data propagation?**
*(expects URL containing: `high-availability.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/high-availability. | 0.729 | www.postgresql.org/docs/current/protocol-flow.html | 0.623 | www.postgresql.org/docs/current/wal-async-commit.h | 0.622 |
| crawl4ai | #1 | www.postgresql.org/docs/current/high-availability. | 0.659 | www.postgresql.org/docs/17/high-availability.html | 0.659 | www.postgresql.org/docs/18/high-availability.html | 0.659 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/high-availability.html | 0.659 | www.postgresql.org/docs/current/high-availability. | 0.659 | www.postgresql.org/docs/17/high-availability.html | 0.659 |
| scrapy+md | miss | www.postgresql.org/docs/9.4/test-shm-mq.html | 0.559 | www.postgresql.org/docs/7.4/libpq-fastpath.html | 0.544 | www.postgresql.org/docs/9.2/runtime-config-resourc | 0.541 |
| crawlee | #1 | www.postgresql.org/docs/current/high-availability. | 0.646 | www.postgresql.org/docs/18/high-availability.html | 0.646 | www.postgresql.org/docs/17/high-availability.html | 0.646 |
| colly+md | #1 | www.postgresql.org/docs/16/high-availability.html | 0.646 | www.postgresql.org/docs/current/high-availability. | 0.646 | www.postgresql.org/docs/17/high-availability.html | 0.646 |
| playwright | #1 | www.postgresql.org/docs/18/high-availability.html | 0.646 | www.postgresql.org/docs/17/high-availability.html | 0.646 | www.postgresql.org/docs/current/high-availability. | 0.646 |


**Q29: What are the components required for OAuth validator modules in PostgreSQL?**
*(expects URL containing: `oauth-validators.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/runtime-config-con | 0.761 | www.postgresql.org/docs/current/libpq-connect.html | 0.753 | www.postgresql.org/docs/current/runtime-config-con | 0.724 |
| crawl4ai | #1 | www.postgresql.org/docs/current/oauth-validators.h | 0.869 | www.postgresql.org/docs/18/oauth-validators.html | 0.869 | www.postgresql.org/about/featurematrix/ | 0.714 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/oauth-validators.h | 0.869 | www.postgresql.org/docs/18/oauth-validators.html | 0.869 | www.postgresql.org/about/featurematrix/ | 0.714 |
| scrapy+md | miss | www.postgresql.org/docs/7.4/libpq-pgpass.html | 0.693 | www.postgresql.org/docs/9.2/libpq-connect.html | 0.690 | www.postgresql.org/docs/9.3/sql-set-session-author | 0.688 |
| crawlee | #1 | www.postgresql.org/docs/current/oauth-validators.h | 0.864 | www.postgresql.org/docs/18/oauth-validators.html | 0.864 | www.postgresql.org/docs/current/plhandler.html | 0.711 |
| colly+md | #1 | www.postgresql.org/docs/current/oauth-validators.h | 0.864 | www.postgresql.org/docs/18/oauth-validators.html | 0.864 | www.postgresql.org/docs/current/plhandler.html | 0.711 |
| playwright | #1 | www.postgresql.org/docs/current/oauth-validators.h | 0.864 | www.postgresql.org/docs/18/oauth-validators.html | 0.864 | www.postgresql.org/docs/current/plhandler.html | 0.711 |


**Q30: Why is correct implementation of OAuth validator modules crucial for server safety?**
*(expects URL containing: `oauth-validators.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/runtime-config-con | 0.675 | www.postgresql.org/docs/current/libpq-connect.html | 0.674 | www.postgresql.org/docs/current/libpq-connect.html | 0.663 |
| crawl4ai | #1 | www.postgresql.org/docs/current/oauth-validators.h | 0.757 | www.postgresql.org/docs/18/oauth-validators.html | 0.757 | www.postgresql.org/about/featurematrix/ | 0.651 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/oauth-validators.html | 0.757 | www.postgresql.org/docs/current/oauth-validators.h | 0.757 | www.postgresql.org/about/featurematrix/ | 0.651 |
| scrapy+md | miss | www.postgresql.org/docs/current/sslinfo.html | 0.621 | www.postgresql.org/docs/9.2/libpq-connect.html | 0.599 | www.postgresql.org/docs/7.3/release.html | 0.581 |
| crawlee | #1 | www.postgresql.org/docs/current/oauth-validators.h | 0.743 | www.postgresql.org/docs/18/oauth-validators.html | 0.743 | www.postgresql.org/docs/18/plhandler.html | 0.666 |
| colly+md | #1 | www.postgresql.org/docs/current/oauth-validators.h | 0.743 | www.postgresql.org/docs/18/oauth-validators.html | 0.743 | www.postgresql.org/docs/current/plhandler.html | 0.666 |
| playwright | #1 | www.postgresql.org/docs/current/oauth-validators.h | 0.743 | www.postgresql.org/docs/18/oauth-validators.html | 0.743 | www.postgresql.org/docs/current/plhandler.html | 0.666 |


**Q31: What does Part IV of the PostgreSQL documentation describe?**
*(expects URL containing: `client-interfaces.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/contrib.html | 0.788 | www.postgresql.org/docs/current/internals.html | 0.788 | www.postgresql.org/docs/current/index.html | 0.778 |
| crawl4ai | #26 | www.postgresql.org/docs/17/preface.html | 0.832 | www.postgresql.org/docs/18/preface.html | 0.832 | www.postgresql.org/docs/current/preface.html | 0.832 |
| crawl4ai-raw | #26 | www.postgresql.org/docs/17/preface.html | 0.832 | www.postgresql.org/docs/current/preface.html | 0.832 | www.postgresql.org/docs/18/preface.html | 0.832 |
| scrapy+md | #41 | www.postgresql.org/docs/7.4/sql.html | 0.816 | www.postgresql.org/docs/7.3/developer.html | 0.815 | www.postgresql.org/docs/8.4/sql-comment.html | 0.797 |
| crawlee | #31 | www.postgresql.org/docs/17/preface.html | 0.833 | www.postgresql.org/docs/8.4/index.html | 0.831 | www.postgresql.org/docs/current/preface.html | 0.830 |
| colly+md | #32 | www.postgresql.org/docs/17/preface.html | 0.833 | www.postgresql.org/docs/8.4/index.html | 0.831 | www.postgresql.org/docs/current/preface.html | 0.830 |
| playwright | #31 | www.postgresql.org/docs/17/preface.html | 0.833 | www.postgresql.org/docs/8.4/index.html | 0.831 | www.postgresql.org/docs/18/preface.html | 0.830 |


**Q32: What should readers of this part be familiar with?**
*(expects URL containing: `client-interfaces.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/textsearch.html | 0.516 | www.postgresql.org/docs/current/logical-replicatio | 0.501 | www.postgresql.org/docs/current/indexes-opclass.ht | 0.500 |
| crawl4ai | miss | www.postgresql.org/list/pgsql-general/ | 0.517 | www.postgresql.org/docs/books/ | 0.516 | www.postgresql.org/docs/books/ | 0.501 |
| crawl4ai-raw | miss | www.postgresql.org/list/pgsql-general/ | 0.517 | www.postgresql.org/docs/books/ | 0.516 | www.postgresql.org/docs/books/ | 0.501 |
| scrapy+md | miss | www.postgresql.org/docs/7.1/docguide.html | 0.490 | www.postgresql.org/docs/7.3/doc-style.html | 0.489 | www.postgresql.org/docs/8.0/admin.html | 0.487 |
| crawlee | miss | www.postgresql.org/docs/books/ | 0.508 | www.postgresql.org/docs/current/contrib.html | 0.502 | www.postgresql.org/docs/18/contrib.html | 0.502 |
| colly+md | miss | www.postgresql.org/docs/books/ | 0.508 | www.postgresql.org/docs/current/contrib.html | 0.502 | www.postgresql.org/docs/books/ | 0.499 |
| playwright | miss | www.postgresql.org/docs/books/ | 0.508 | www.postgresql.org/docs/current/contrib.html | 0.502 | www.postgresql.org/docs/18/contrib.html | 0.502 |


**Q33: How do I set up and run the PostgreSQL database server?**
*(expects URL containing: `runtime.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | www.postgresql.org/docs/current/install-make.html | 0.779 | www.postgresql.org/docs/current/runtime.html | 0.772 | www.postgresql.org/docs/current/app-initdb.html | 0.757 |
| crawl4ai | #2 | www.postgresql.org/docs/17/admin.html | 0.761 | www.postgresql.org/docs/18/runtime.html | 0.759 | www.postgresql.org/docs/current/runtime.html | 0.759 |
| crawl4ai-raw | #2 | www.postgresql.org/docs/17/admin.html | 0.761 | www.postgresql.org/docs/18/runtime.html | 0.759 | www.postgresql.org/docs/current/runtime.html | 0.759 |
| scrapy+md | miss | www.postgresql.org/docs/7.2/app-vacuumdb.html | 0.756 | www.postgresql.org/docs/7.3/reference-server.html | 0.753 | www.postgresql.org/docs/9.1/install-procedure.html | 0.747 |
| crawlee | #1 | www.postgresql.org/docs/17/runtime.html | 0.805 | www.postgresql.org/docs/current/runtime.html | 0.805 | www.postgresql.org/docs/18/runtime.html | 0.805 |
| colly+md | #1 | www.postgresql.org/docs/16/runtime.html | 0.809 | www.postgresql.org/docs/current/runtime.html | 0.805 | www.postgresql.org/docs/18/runtime.html | 0.805 |
| playwright | #1 | www.postgresql.org/docs/18/runtime.html | 0.805 | www.postgresql.org/docs/current/runtime.html | 0.805 | www.postgresql.org/docs/17/runtime.html | 0.805 |


**Q34: What should I do if I am using a pre-packaged version of PostgreSQL?**
*(expects URL containing: `runtime.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #45 | www.postgresql.org/docs/current/install-make.html | 0.776 | www.postgresql.org/docs/current/extend-pgxs.html | 0.762 | www.postgresql.org/docs/current/pgupgrade.html | 0.757 |
| crawl4ai | #6 | www.postgresql.org/download/linux/debian/ | 0.799 | www.postgresql.org/download/linux/ubuntu | 0.799 | www.postgresql.org/docs/17/install-binaries.html | 0.788 |
| crawl4ai-raw | #6 | www.postgresql.org/download/linux/debian/ | 0.799 | www.postgresql.org/download/linux/ubuntu | 0.799 | www.postgresql.org/docs/17/install-binaries.html | 0.788 |
| scrapy+md | miss | www.postgresql.org/docs/9.1/install-procedure.html | 0.785 | www.postgresql.org/docs/7.3/reference-client.html | 0.779 | www.postgresql.org/docs/9.1/sql-createextension.ht | 0.771 |
| crawlee | #9 | www.postgresql.org/download/linux/debian/ | 0.799 | www.postgresql.org/download/linux/ubuntu | 0.799 | www.postgresql.org/docs/17/bug-reporting.html | 0.777 |
| colly+md | #11 | www.postgresql.org/download/linux/debian/ | 0.799 | www.postgresql.org/download/linux/ubuntu/ | 0.799 | www.postgresql.org/docs/17/bug-reporting.html | 0.777 |
| playwright | #9 | www.postgresql.org/download/linux/ubuntu | 0.799 | www.postgresql.org/download/linux/debian/ | 0.799 | www.postgresql.org/docs/17/bug-reporting.html | 0.777 |


**Q35: What is the primary purpose of the backup manifest generated by pg_basebackup?**
*(expects URL containing: `backup-manifest-format.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/internals.html | 0.776 | www.postgresql.org/docs/current/appendixes.html | 0.743 | www.postgresql.org/docs/current/continuous-archivi | 0.718 |
| crawl4ai | #1 | www.postgresql.org/docs/current/backup-manifest-fo | 0.838 | www.postgresql.org/docs/18/backup-manifest-format. | 0.838 | www.postgresql.org/docs/18/internals.html | 0.790 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/backup-manifest-fo | 0.838 | www.postgresql.org/docs/18/backup-manifest-format. | 0.838 | www.postgresql.org/docs/18/internals.html | 0.790 |
| scrapy+md | miss | www.postgresql.org/docs/8.0/backup.html | 0.706 | www.postgresql.org/docs/current/bookindex.html | 0.680 | www.postgresql.org/docs/8.0/backup.html | 0.677 |
| crawlee | #1 | www.postgresql.org/docs/18/backup-manifest-format. | 0.811 | www.postgresql.org/docs/current/backup-manifest-fo | 0.811 | www.postgresql.org/docs/18/internals.html | 0.771 |
| colly+md | #1 | www.postgresql.org/docs/current/backup-manifest-fo | 0.811 | www.postgresql.org/docs/current/internals.html | 0.771 | www.postgresql.org/docs/current/appendixes.html | 0.735 |
| playwright | #1 | www.postgresql.org/docs/current/backup-manifest-fo | 0.811 | www.postgresql.org/docs/18/backup-manifest-format. | 0.811 | www.postgresql.org/docs/18/internals.html | 0.771 |


**Q36: What format is the backup manifest encoded in?**
*(expects URL containing: `backup-manifest-format.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/internals.html | 0.683 | www.postgresql.org/docs/current/appendixes.html | 0.643 | www.postgresql.org/docs/current/continuous-archivi | 0.639 |
| crawl4ai | #1 | www.postgresql.org/docs/18/backup-manifest-format. | 0.776 | www.postgresql.org/docs/current/backup-manifest-fo | 0.776 | www.postgresql.org/docs/current/internals.html | 0.699 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/backup-manifest-format. | 0.776 | www.postgresql.org/docs/current/backup-manifest-fo | 0.776 | www.postgresql.org/docs/current/internals.html | 0.699 |
| scrapy+md | miss | www.postgresql.org/docs/7.1/sql-copy.html | 0.631 | www.postgresql.org/docs/7.4/sql-copy.html | 0.625 | www.postgresql.org/docs/7.3/doc-build.html | 0.624 |
| crawlee | #1 | www.postgresql.org/docs/current/backup-manifest-fo | 0.771 | www.postgresql.org/docs/18/backup-manifest-format. | 0.771 | www.postgresql.org/docs/18/internals.html | 0.671 |
| colly+md | #1 | www.postgresql.org/docs/current/backup-manifest-fo | 0.771 | www.postgresql.org/docs/current/internals.html | 0.671 | www.postgresql.org/about/featurematrix/ | 0.656 |
| playwright | #1 | www.postgresql.org/docs/18/backup-manifest-format. | 0.771 | www.postgresql.org/docs/current/backup-manifest-fo | 0.771 | www.postgresql.org/docs/18/internals.html | 0.671 |


**Q37: What factors can affect query performance in PostgreSQL?**
*(expects URL containing: `performance-tips.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/performance-tips.h | 0.728 | www.postgresql.org/docs/current/indexes-partial.ht | 0.716 | www.postgresql.org/docs/current/populate.html | 0.694 |
| crawl4ai | #1 | www.postgresql.org/docs/18/performance-tips.html | 0.719 | www.postgresql.org/docs/current/performance-tips.h | 0.719 | www.postgresql.org/docs/17/performance-tips.html | 0.719 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/performance-tips.html | 0.719 | www.postgresql.org/docs/current/performance-tips.h | 0.719 | www.postgresql.org/docs/17/performance-tips.html | 0.719 |
| scrapy+md | miss | www.postgresql.org/docs/8.2/biblio.html | 0.705 | www.postgresql.org/docs/7.2/biblio.html | 0.704 | www.postgresql.org/docs/7.3/biblio.html | 0.704 |
| crawlee | #1 | www.postgresql.org/docs/current/performance-tips.h | 0.701 | www.postgresql.org/docs/18/performance-tips.html | 0.701 | www.postgresql.org/docs/17/performance-tips.html | 0.698 |
| colly+md | #1 | www.postgresql.org/docs/16/performance-tips.html | 0.702 | www.postgresql.org/docs/18/performance-tips.html | 0.701 | www.postgresql.org/docs/current/performance-tips.h | 0.701 |
| playwright | #1 | www.postgresql.org/docs/18/performance-tips.html | 0.701 | www.postgresql.org/docs/current/performance-tips.h | 0.701 | www.postgresql.org/docs/17/performance-tips.html | 0.698 |


**Q38: What does this chapter provide hints about regarding PostgreSQL performance?**
*(expects URL containing: `performance-tips.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/performance-tips.h | 0.807 | www.postgresql.org/docs/current/contrib.html | 0.773 | www.postgresql.org/docs/current/planner-stats.html | 0.738 |
| crawl4ai | #1 | www.postgresql.org/docs/17/performance-tips.html | 0.818 | www.postgresql.org/docs/current/performance-tips.h | 0.816 | www.postgresql.org/docs/18/performance-tips.html | 0.816 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/performance-tips.html | 0.818 | www.postgresql.org/docs/18/performance-tips.html | 0.816 | www.postgresql.org/docs/current/performance-tips.h | 0.816 |
| scrapy+md | miss | www.postgresql.org/docs/7.4/sql-explain.html | 0.752 | www.postgresql.org/docs/8.2/biblio.html | 0.743 | www.postgresql.org/docs/7.3/developer.html | 0.741 |
| crawlee | #1 | www.postgresql.org/docs/17/performance-tips.html | 0.797 | www.postgresql.org/docs/18/performance-tips.html | 0.795 | www.postgresql.org/docs/current/performance-tips.h | 0.795 |
| colly+md | #1 | www.postgresql.org/docs/16/performance-tips.html | 0.800 | www.postgresql.org/docs/17/performance-tips.html | 0.797 | www.postgresql.org/docs/current/performance-tips.h | 0.795 |
| playwright | #1 | www.postgresql.org/docs/17/performance-tips.html | 0.797 | www.postgresql.org/docs/18/performance-tips.html | 0.795 | www.postgresql.org/docs/current/performance-tips.h | 0.795 |


**Q39: What tools are available for monitoring database activity?**
*(expects URL containing: `monitoring.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/monitoring.html | 0.791 | www.postgresql.org/docs/current/diskusage.html | 0.713 | www.postgresql.org/docs/current/runtime-config-sta | 0.696 |
| crawl4ai | #5 | www.postgresql.org/about/news/pgedge-launches-ai-d | 0.693 | www.postgresql.org/docs/18/maintenance.html | 0.677 | www.postgresql.org/docs/17/maintenance.html | 0.677 |
| crawl4ai-raw | #5 | www.postgresql.org/about/news/pgedge-launches-ai-d | 0.693 | www.postgresql.org/docs/18/maintenance.html | 0.677 | www.postgresql.org/docs/17/maintenance.html | 0.677 |
| scrapy+md | miss | www.postgresql.org/docs/8.0/admin.html | 0.689 | www.postgresql.org/docs/current/bookindex.html | 0.674 | www.postgresql.org/docs/9.1/dynamic-trace.html | 0.672 |
| crawlee | #1 | www.postgresql.org/docs/current/monitoring.html | 0.700 | www.postgresql.org/docs/18/monitoring.html | 0.700 | www.postgresql.org/docs/17/monitoring.html | 0.700 |
| colly+md | #1 | www.postgresql.org/docs/16/monitoring.html | 0.702 | www.postgresql.org/docs/current/monitoring.html | 0.700 | www.postgresql.org/docs/18/monitoring.html | 0.700 |
| playwright | #1 | www.postgresql.org/docs/18/monitoring.html | 0.700 | www.postgresql.org/docs/current/monitoring.html | 0.700 | www.postgresql.org/docs/17/monitoring.html | 0.700 |


**Q40: What command can be used to investigate a poorly-performing query in PostgreSQL?**
*(expects URL containing: `monitoring.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #26 | www.postgresql.org/docs/current/runtime-config-rep | 0.732 | www.postgresql.org/docs/current/app-psql.html | 0.721 | www.postgresql.org/docs/current/indexes-partial.ht | 0.716 |
| crawl4ai | #1 | www.postgresql.org/docs/17/monitoring.html | 0.761 | www.postgresql.org/docs/current/monitoring.html | 0.761 | www.postgresql.org/docs/18/monitoring.html | 0.761 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/monitoring.html | 0.761 | www.postgresql.org/docs/17/monitoring.html | 0.761 | www.postgresql.org/docs/18/monitoring.html | 0.761 |
| scrapy+md | miss | www.postgresql.org/docs/7.4/sql-explain.html | 0.722 | www.postgresql.org/docs/7.4/sql-explain.html | 0.715 | www.postgresql.org/docs/7.4/sql-explain.html | 0.714 |
| crawlee | #1 | www.postgresql.org/docs/current/monitoring.html | 0.761 | www.postgresql.org/docs/18/monitoring.html | 0.761 | www.postgresql.org/docs/17/monitoring.html | 0.761 |
| colly+md | #1 | www.postgresql.org/docs/16/monitoring.html | 0.762 | www.postgresql.org/docs/current/monitoring.html | 0.761 | www.postgresql.org/docs/17/monitoring.html | 0.761 |
| playwright | #1 | www.postgresql.org/docs/current/monitoring.html | 0.761 | www.postgresql.org/docs/18/monitoring.html | 0.761 | www.postgresql.org/docs/17/monitoring.html | 0.761 |


**Q41: What does PostgreSQL use for date/time input support?**
*(expects URL containing: `datetime-appendix.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | www.postgresql.org/docs/current/datatype-datetime. | 0.862 | www.postgresql.org/docs/current/datatype-datetime. | 0.832 | www.postgresql.org/docs/current/datatype-datetime. | 0.822 |
| crawl4ai | #1 | www.postgresql.org/docs/current/datetime-appendix. | 0.853 | www.postgresql.org/docs/18/datetime-appendix.html | 0.853 | www.postgresql.org/docs/current/bookindex.html | 0.766 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/datetime-appendix.html | 0.853 | www.postgresql.org/docs/current/datetime-appendix. | 0.853 | www.postgresql.org/docs/current/bookindex.html | 0.766 |
| scrapy+md | miss | www.postgresql.org/docs/9.1/datatype-datetime.html | 0.843 | www.postgresql.org/docs/9.1/datatype-datetime.html | 0.829 | www.postgresql.org/docs/9.1/datatype-datetime.html | 0.821 |
| crawlee | #1 | www.postgresql.org/docs/18/datetime-appendix.html | 0.832 | www.postgresql.org/docs/current/datetime-appendix. | 0.832 | www.postgresql.org/docs/current/datatype.html | 0.809 |
| colly+md | #1 | www.postgresql.org/docs/current/datetime-appendix. | 0.832 | www.postgresql.org/docs/17/datatype.html | 0.809 | www.postgresql.org/docs/16/datatype.html | 0.809 |
| playwright | #1 | www.postgresql.org/docs/current/datetime-appendix. | 0.832 | www.postgresql.org/docs/18/datetime-appendix.html | 0.832 | www.postgresql.org/docs/17/datatype.html | 0.809 |


**Q42: What information does the appendix include about the parser's lookup tables?**
*(expects URL containing: `datetime-appendix.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/datetime-appendix. | 0.686 | www.postgresql.org/docs/current/functions-textsear | 0.682 | www.postgresql.org/docs/current/contrib.html | 0.681 |
| crawl4ai | #15 | www.postgresql.org/docs/current/contrib.html | 0.648 | www.postgresql.org/docs/18/contrib.html | 0.648 | www.postgresql.org/docs/18/appendixes.html | 0.647 |
| crawl4ai-raw | #15 | www.postgresql.org/docs/current/contrib.html | 0.648 | www.postgresql.org/docs/18/contrib.html | 0.648 | www.postgresql.org/docs/18/appendixes.html | 0.647 |
| scrapy+md | miss | www.postgresql.org/docs/7.1/sql-copy.html | 0.644 | www.postgresql.org/docs/8.4/test-parser.html | 0.639 | www.postgresql.org/docs/8.3/test-parser.html | 0.636 |
| crawlee | #7 | www.postgresql.org/docs/current/contrib.html | 0.673 | www.postgresql.org/docs/18/contrib.html | 0.673 | www.postgresql.org/docs/18/appendixes.html | 0.651 |
| colly+md | #4 | www.postgresql.org/docs/current/contrib.html | 0.673 | www.postgresql.org/docs/current/appendixes.html | 0.651 | www.postgresql.org/docs/current/contrib.html | 0.638 |
| playwright | #7 | www.postgresql.org/docs/18/contrib.html | 0.673 | www.postgresql.org/docs/current/contrib.html | 0.673 | www.postgresql.org/docs/18/appendixes.html | 0.651 |


**Q43: What was the initial implementation year of the POSTGRES project?**
*(expects URL containing: `history.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/index.html | 0.739 | www.postgresql.org/docs/current/app-postgres.html | 0.718 | www.postgresql.org/docs/current/internals.html | 0.711 |
| crawl4ai | #1 | www.postgresql.org/docs/18/history.html | 0.846 | www.postgresql.org/docs/current/history.html | 0.844 | www.postgresql.org/docs/17/history.html | 0.827 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/history.html | 0.846 | www.postgresql.org/docs/current/history.html | 0.844 | www.postgresql.org/docs/17/history.html | 0.827 |
| scrapy+md | miss | www.postgresql.org/docs/current/biblio.html | 0.748 | www.postgresql.org/docs/7.3/release-1-0.html | 0.737 | www.postgresql.org/docs/8.2/biblio.html | 0.736 |
| crawlee | #1 | www.postgresql.org/docs/current/history.html | 0.853 | www.postgresql.org/docs/18/history.html | 0.853 | www.postgresql.org/docs/17/history.html | 0.841 |
| colly+md | #1 | www.postgresql.org/docs/current/history.html | 0.853 | www.postgresql.org/docs/18/history.html | 0.853 | www.postgresql.org/docs/16/history.html | 0.841 |
| playwright | #1 | www.postgresql.org/docs/current/history.html | 0.853 | www.postgresql.org/docs/18/history.html | 0.853 | www.postgresql.org/docs/17/history.html | 0.841 |


**Q44: What major enhancements were made in Postgres95 compared to POSTGRES, Version 4.2?**
*(expects URL containing: `history.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.postgresql.org/docs/current/contrib.html | 0.721 | www.postgresql.org/docs/current/internals.html | 0.713 | www.postgresql.org/docs/current/index.html | 0.706 |
| crawl4ai | #1 | www.postgresql.org/docs/17/history.html | 0.828 | www.postgresql.org/docs/18/history.html | 0.828 | www.postgresql.org/docs/current/history.html | 0.828 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/history.html | 0.828 | www.postgresql.org/docs/17/history.html | 0.828 | www.postgresql.org/docs/current/history.html | 0.828 |
| scrapy+md | miss | www.postgresql.org/docs/7.3/release-0-02.html | 0.761 | www.postgresql.org/docs/8.1/release-0-03.html | 0.751 | www.postgresql.org/docs/8.0/release-0-03.html | 0.750 |
| crawlee | #1 | www.postgresql.org/docs/18/history.html | 0.828 | www.postgresql.org/docs/current/history.html | 0.828 | www.postgresql.org/docs/17/history.html | 0.828 |
| colly+md | #1 | www.postgresql.org/docs/17/history.html | 0.828 | www.postgresql.org/docs/current/history.html | 0.828 | www.postgresql.org/docs/18/history.html | 0.828 |
| playwright | #1 | www.postgresql.org/docs/18/history.html | 0.828 | www.postgresql.org/docs/17/history.html | 0.828 | www.postgresql.org/docs/current/history.html | 0.828 |


**Q45: What is PL/Tcl?**
*(expects URL containing: `pltcl.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | www.postgresql.org/docs/current/pltcl-overview.htm | 0.759 | www.postgresql.org/docs/current/pltcl-functions.ht | 0.711 | www.postgresql.org/docs/current/pltcl-overview.htm | 0.709 |
| crawl4ai | #4 | www.postgresql.org/docs/17/server-programming.html | 0.652 | www.postgresql.org/docs/current/server-programming | 0.649 | www.postgresql.org/docs/18/server-programming.html | 0.649 |
| crawl4ai-raw | #4 | www.postgresql.org/docs/17/server-programming.html | 0.652 | www.postgresql.org/docs/current/server-programming | 0.649 | www.postgresql.org/docs/18/server-programming.html | 0.649 |
| scrapy+md | miss | www.postgresql.org/docs/9.1/install-procedure.html | 0.624 | www.postgresql.org/docs/7.3/app-pgtclsh.html | 0.553 | www.postgresql.org/docs/current/bookindex.html | 0.545 |
| crawlee | #3 | www.postgresql.org/docs/current/server-programming | 0.654 | www.postgresql.org/docs/18/server-programming.html | 0.654 | www.postgresql.org/docs/17/pltcl.html | 0.653 |
| colly+md | #3 | www.postgresql.org/docs/18/server-programming.html | 0.654 | www.postgresql.org/docs/current/server-programming | 0.654 | www.postgresql.org/docs/18/pltcl.html | 0.650 |
| playwright | #3 | www.postgresql.org/docs/18/server-programming.html | 0.654 | www.postgresql.org/docs/current/server-programming | 0.654 | www.postgresql.org/docs/17/pltcl.html | 0.653 |


**Q46: What language does PL/Tcl enable to write PostgreSQL functions and procedures?**
*(expects URL containing: `pltcl.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #32 | www.postgresql.org/docs/current/pltcl-overview.htm | 0.848 | www.postgresql.org/docs/current/plperl.html | 0.834 | www.postgresql.org/docs/current/xplang.html | 0.821 |
| crawl4ai | #1 | www.postgresql.org/docs/18/pltcl.html | 0.886 | www.postgresql.org/docs/current/pltcl.html | 0.886 | www.postgresql.org/docs/17/pltcl.html | 0.886 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/pltcl.html | 0.886 | www.postgresql.org/docs/current/pltcl.html | 0.886 | www.postgresql.org/docs/17/pltcl.html | 0.886 |
| scrapy+md | miss | www.postgresql.org/docs/current/ | 0.804 | www.postgresql.org/docs/7.3/app-pgtclsh.html | 0.797 | www.postgresql.org/docs/9.0/server-programming.htm | 0.786 |
| crawlee | #1 | www.postgresql.org/docs/current/pltcl.html | 0.886 | www.postgresql.org/docs/18/pltcl.html | 0.886 | www.postgresql.org/docs/17/pltcl.html | 0.885 |
| colly+md | #1 | www.postgresql.org/docs/current/pltcl.html | 0.886 | www.postgresql.org/docs/18/pltcl.html | 0.886 | www.postgresql.org/docs/current/plperl.html | 0.838 |
| playwright | #1 | www.postgresql.org/docs/18/pltcl.html | 0.886 | www.postgresql.org/docs/current/pltcl.html | 0.886 | www.postgresql.org/docs/17/pltcl.html | 0.885 |


**Q47: What topics are covered in Part II of the SQL Language documentation?**
*(expects URL containing: `sql.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/sql.html | 0.836 | www.postgresql.org/docs/current/sql.html | 0.794 | www.postgresql.org/docs/current/extend.html | 0.776 |
| crawl4ai | #1 | www.postgresql.org/docs/18/sql.html | 0.840 | www.postgresql.org/docs/current/sql.html | 0.840 | www.postgresql.org/docs/17/sql.html | 0.840 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/sql.html | 0.840 | www.postgresql.org/docs/18/sql.html | 0.840 | www.postgresql.org/docs/17/sql.html | 0.840 |
| scrapy+md | #1 | www.postgresql.org/docs/7.4/sql.html | 0.809 | www.postgresql.org/docs/7.1/biblio.html | 0.775 | www.postgresql.org/docs/current/ | 0.770 |
| crawlee | #1 | www.postgresql.org/docs/18/sql.html | 0.838 | www.postgresql.org/docs/current/sql.html | 0.838 | www.postgresql.org/docs/17/sql.html | 0.838 |
| colly+md | #1 | www.postgresql.org/docs/18/sql.html | 0.838 | www.postgresql.org/docs/current/sql.html | 0.838 | www.postgresql.org/docs/17/sql.html | 0.838 |
| playwright | #1 | www.postgresql.org/docs/current/sql.html | 0.838 | www.postgresql.org/docs/18/sql.html | 0.838 | www.postgresql.org/docs/17/sql.html | 0.838 |


**Q48: What is the recommended way to enter SQL commands in PostgreSQL?**
*(expects URL containing: `sql.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/app-psql.html | 0.809 | www.postgresql.org/docs/current/plpgsql-statements | 0.793 | www.postgresql.org/docs/current/app-psql.html | 0.792 |
| crawl4ai | #1 | www.postgresql.org/docs/current/sql.html | 0.806 | www.postgresql.org/docs/18/sql.html | 0.806 | www.postgresql.org/docs/17/sql.html | 0.804 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/sql.html | 0.806 | www.postgresql.org/docs/18/sql.html | 0.806 | www.postgresql.org/docs/17/sql.html | 0.804 |
| scrapy+md | #1 | www.postgresql.org/docs/8.3/app-psql.html | 0.817 | www.postgresql.org/docs/8.3/app-psql.html | 0.814 | www.postgresql.org/docs/8.3/tutorial-sql-intro.htm | 0.809 |
| crawlee | #1 | www.postgresql.org/docs/current/sql.html | 0.806 | www.postgresql.org/docs/18/sql.html | 0.806 | www.postgresql.org/docs/17/sql.html | 0.805 |
| colly+md | #1 | www.postgresql.org/docs/18/sql.html | 0.806 | www.postgresql.org/docs/current/sql.html | 0.806 | www.postgresql.org/docs/17/sql.html | 0.805 |
| playwright | #1 | www.postgresql.org/docs/current/sql.html | 0.806 | www.postgresql.org/docs/18/sql.html | 0.806 | www.postgresql.org/docs/17/sql.html | 0.805 |


**Q49: What is logical replication in PostgreSQL?**
*(expects URL containing: `logical-replication.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.907 | www.postgresql.org/docs/current/logicaldecoding-ex | 0.796 | www.postgresql.org/docs/current/logicaldecoding-ex | 0.786 |
| crawl4ai | #1 | www.postgresql.org/docs/18/logical-replication.htm | 0.882 | www.postgresql.org/docs/current/logical-replicatio | 0.882 | www.postgresql.org/docs/17/logical-replication.htm | 0.879 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.882 | www.postgresql.org/docs/18/logical-replication.htm | 0.882 | www.postgresql.org/docs/17/logical-replication.htm | 0.879 |
| scrapy+md | miss | www.postgresql.org/docs/current/ | 0.696 | www.postgresql.org/docs/current/sql-createpublicat | 0.694 | www.postgresql.org/docs/12/test-decoding.html | 0.681 |
| crawlee | #1 | www.postgresql.org/docs/18/logical-replication.htm | 0.884 | www.postgresql.org/docs/current/logical-replicatio | 0.884 | www.postgresql.org/docs/17/logical-replication.htm | 0.882 |
| colly+md | #1 | www.postgresql.org/docs/16/logical-replication.htm | 0.887 | www.postgresql.org/docs/current/logical-replicatio | 0.884 | www.postgresql.org/docs/18/logical-replication.htm | 0.884 |
| playwright | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.884 | www.postgresql.org/docs/18/logical-replication.htm | 0.884 | www.postgresql.org/docs/17/logical-replication.htm | 0.882 |


**Q50: What are the typical use-cases for logical replication?**
*(expects URL containing: `logical-replication.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.799 | www.postgresql.org/docs/current/logical-replicatio | 0.740 | www.postgresql.org/docs/current/logical-replicatio | 0.727 |
| crawl4ai | #1 | www.postgresql.org/docs/17/logical-replication.htm | 0.788 | www.postgresql.org/docs/18/logical-replication.htm | 0.771 | www.postgresql.org/docs/current/logical-replicatio | 0.771 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/logical-replication.htm | 0.788 | www.postgresql.org/docs/current/logical-replicatio | 0.771 | www.postgresql.org/docs/18/logical-replication.htm | 0.771 |
| scrapy+md | miss | www.postgresql.org/docs/current/sql-createpublicat | 0.620 | www.postgresql.org/docs/current/bookindex.html | 0.608 | www.postgresql.org/docs/7.1/biblio.html | 0.608 |
| crawlee | #1 | www.postgresql.org/docs/17/logical-replication.htm | 0.782 | www.postgresql.org/docs/18/logical-replication.htm | 0.772 | www.postgresql.org/docs/current/logical-replicatio | 0.772 |
| colly+md | #1 | www.postgresql.org/docs/16/logical-replication.htm | 0.792 | www.postgresql.org/docs/17/logical-replication.htm | 0.782 | www.postgresql.org/docs/18/logical-replication.htm | 0.772 |
| playwright | #1 | www.postgresql.org/docs/17/logical-replication.htm | 0.782 | www.postgresql.org/docs/current/logical-replicatio | 0.772 | www.postgresql.org/docs/18/logical-replication.htm | 0.772 |


</details>

## propublica

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| playwright | 54% (30/56) | 66% (37/56) | 77% (43/56) | 84% (47/56) | 89% (50/56) | 0.623 | 2197 | 150 |
| crawl4ai | 54% (30/56) | 66% (37/56) | 71% (40/56) | 75% (42/56) | 84% (47/56) | 0.608 | 1563 | 149 |
| crawl4ai-raw | 54% (30/56) | 66% (37/56) | 71% (40/56) | 75% (42/56) | 84% (47/56) | 0.608 | 1563 | 149 |
| crawlee | 52% (29/56) | 66% (37/56) | 73% (41/56) | 80% (45/56) | 86% (48/56) | 0.601 | 2099 | 150 |
| colly+md | 14% (8/56) | 18% (10/56) | 20% (11/56) | 21% (12/56) | 23% (13/56) | 0.170 | 2196 | 150 |
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
| markcrawl | miss | www.propublica.org/article/propublica-investigatio | 0.505 | www.propublica.org/article/propublica-investigatio | 0.490 | www.propublica.org/article/fda-generic-drug-equiva | 0.481 |
| crawl4ai | miss | www.propublica.org/people/logan-jaffe | 0.540 | www.propublica.org/people/anna-maria-barry-jester | 0.540 | www.propublica.org/people/sharon-lerner | 0.537 |
| crawl4ai-raw | miss | www.propublica.org/people/logan-jaffe | 0.540 | www.propublica.org/people/anna-maria-barry-jester | 0.540 | www.propublica.org/people/sharon-lerner | 0.537 |
| scrapy+md | miss | www.propublica.org/people/chris-alcantara | 0.533 | www.propublica.org/people/sandhya-kambhampati | 0.531 | www.propublica.org/people/rob-davis | 0.529 |
| crawlee | #14 | www.propublica.org/people/anna-maria-barry-jester | 0.525 | www.propublica.org/people/sharon-lerner | 0.522 | www.propublica.org/article/tribal-colleges-univers | 0.521 |
| colly+md | miss | www.propublica.org/people/sharon-lerner | 0.522 | www.propublica.org/people/mary-hudetz | 0.521 | www.propublica.org/article/how-virginia-college-ex | 0.521 |
| playwright | #12 | www.propublica.org/people/anna-maria-barry-jester | 0.525 | www.propublica.org/people/sharon-lerner | 0.522 | www.propublica.org/article/tribal-colleges-univers | 0.521 |


**Q2: What is the title of the article published on March 14, 2024?**
*(expects URL containing: `brandi-kellam`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigatio | 0.563 | www.propublica.org/article/propublica-most-read-st | 0.560 | www.propublica.org/article/propublica-most-read-st | 0.560 |
| crawl4ai | miss | www.propublica.org/people/propublica | 0.575 | www.propublica.org/archive | 0.575 | www.propublica.org/newsapps | 0.572 |
| crawl4ai-raw | miss | www.propublica.org/people/propublica | 0.575 | www.propublica.org/archive | 0.575 | www.propublica.org/newsapps | 0.572 |
| scrapy+md | miss | www.propublica.org/people/maya-miller | 0.563 | www.propublica.org/article/omaha-nebraska-lead-sup | 0.563 | www.propublica.org/article/students-propublica-and | 0.561 |
| crawlee | miss | www.propublica.org/newsapps | 0.603 | www.propublica.org/newsapps | 0.597 | www.propublica.org/press-releases | 0.586 |
| colly+md | miss | www.propublica.org/newsapps | 0.603 | www.propublica.org/newsapps | 0.597 | www.propublica.org/people/abrahm-lustgarten/page/3 | 0.594 |
| playwright | miss | www.propublica.org/newsapps | 0.603 | www.propublica.org/newsapps | 0.597 | www.propublica.org/press-releases | 0.586 |


**Q3: What is the main focus of ProPublica's criminal justice coverage?**
*(expects URL containing: `criminal-justice`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigativ | 0.639 | www.propublica.org/article/albuquerque-homelessnes | 0.629 | www.propublica.org/article/propublica-investigatio | 0.612 |
| crawl4ai | #47 | www.propublica.org/about | 0.696 | www.propublica.org/ | 0.680 | www.propublica.org | 0.680 |
| crawl4ai-raw | #47 | www.propublica.org/about | 0.696 | www.propublica.org/ | 0.680 | www.propublica.org | 0.680 |
| scrapy+md | miss | www.propublica.org/getinvolved/send-propublica-sto | 0.676 | www.propublica.org/ | 0.668 | www.propublica.org/tips/ | 0.666 |
| crawlee | miss | www.propublica.org/about | 0.697 | www.propublica.org/impact | 0.673 | www.propublica.org/local-initiatives | 0.662 |
| colly+md | miss | www.propublica.org/ | 0.688 | www.propublica.org/article/historic-preservation-e | 0.665 | www.propublica.org/ | 0.661 |
| playwright | miss | www.propublica.org/about | 0.697 | www.propublica.org/impact | 0.673 | www.propublica.org/local-initiatives | 0.662 |


**Q4: What issues are highlighted in the featured stories on the criminal justice page?**
*(expects URL containing: `criminal-justice`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigatio | 0.609 | www.propublica.org/article/propublica-investigatio | 0.584 | www.propublica.org/article/wisconsin-corey-stingle | 0.575 |
| crawl4ai | #1 | www.propublica.org/topics/criminal-justice | 0.629 | www.propublica.org/ | 0.622 | www.propublica.org | 0.622 |
| crawl4ai-raw | #1 | www.propublica.org/topics/criminal-justice | 0.629 | www.propublica.org/ | 0.622 | www.propublica.org | 0.622 |
| scrapy+md | miss | www.propublica.org/topics/courts | 0.639 | www.propublica.org/ | 0.597 | www.propublica.org/topics/education | 0.589 |
| crawlee | #8 | www.propublica.org/local-reporting-network | 0.636 | www.propublica.org/article/propublica-and-the-conn | 0.636 | www.propublica.org/article/trump-social-security-s | 0.634 |
| colly+md | miss | www.propublica.org/article/art-martinez-de-vara-da | 0.632 | www.propublica.org/topics/racial-justice | 0.619 | www.propublica.org/ | 0.616 |
| playwright | #8 | www.propublica.org/local-reporting-network | 0.636 | www.propublica.org/local-reporting-network/ | 0.636 | www.propublica.org/article/propublica-and-the-conn | 0.636 |


**Q5: What is Francesca D’Annunzio's role at ProPublica?**
*(expects URL containing: `francesca-dannunzio`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/averhealth-drug-testing | 0.565 | www.propublica.org/article/propublica-investigatio | 0.561 | www.propublica.org/article/propublica-reaching-out | 0.560 |
| crawl4ai | #3 | www.propublica.org/staff | 0.677 | www.propublica.org/staff | 0.646 | www.propublica.org/people/francesca-dannunzio | 0.633 |
| crawl4ai-raw | #3 | www.propublica.org/staff | 0.677 | www.propublica.org/staff | 0.646 | www.propublica.org/people/francesca-dannunzio | 0.633 |
| scrapy+md | miss | www.propublica.org/tips/ | 0.635 | www.propublica.org/getinvolved/send-propublica-sto | 0.604 | www.propublica.org/people/talia-buford/page/3 | 0.600 |
| crawlee | #3 | www.propublica.org/staff | 0.658 | www.propublica.org/staff | 0.651 | www.propublica.org/people/francesca-dannunzio | 0.638 |
| colly+md | miss | job-boards.greenhouse.io/propublica | 0.660 | www.propublica.org/staff | 0.658 | www.propublica.org/staff | 0.651 |
| playwright | #4 | www.propublica.org/jobs | 0.660 | www.propublica.org/staff | 0.658 | www.propublica.org/staff | 0.651 |


**Q6: What is the topic of Francesca D’Annunzio's featured post from May 1, 2026?**
*(expects URL containing: `francesca-dannunzio`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/life-inside-ice-dilley- | 0.554 | www.propublica.org/article/ice-dilley-ninos-cartas | 0.538 | www.propublica.org/article/propublica-most-read-st | 0.536 |
| crawl4ai | #1 | www.propublica.org/people/francesca-dannunzio | 0.588 | www.propublica.org/newsapps | 0.582 | www.propublica.org/newsapps | 0.578 |
| crawl4ai-raw | #1 | www.propublica.org/people/francesca-dannunzio | 0.588 | www.propublica.org/newsapps | 0.582 | www.propublica.org/newsapps | 0.578 |
| scrapy+md | miss | www.propublica.org/people/talia-buford/page/2 | 0.588 | www.propublica.org/people/bernice-yeung/page/2 | 0.572 | www.propublica.org/people/chris-alcantara | 0.571 |
| crawlee | #1 | www.propublica.org/people/francesca-dannunzio | 0.645 | www.propublica.org/newsapps | 0.587 | www.propublica.org/people/anna-clark | 0.576 |
| colly+md | miss | www.propublica.org/newsapps | 0.587 | www.propublica.org/newsapps | 0.575 | www.propublica.org/awards/pulitzer-prize-for-publi | 0.561 |
| playwright | #1 | www.propublica.org/people/francesca-dannunzio | 0.645 | www.propublica.org/newsapps | 0.587 | www.propublica.org/people/anna-clark | 0.576 |


**Q7: What states does the ProPublica Midwest team cover?**
*(expects URL containing: `midwest`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigativ | 0.562 | www.propublica.org/article/save-voter-citizenship- | 0.543 | www.propublica.org/article/why-local-state-police- | 0.541 |
| crawl4ai | #1 | www.propublica.org/midwest | 0.734 | www.propublica.org/local-initiatives | 0.719 | www.propublica.org/midwest | 0.702 |
| crawl4ai-raw | #1 | www.propublica.org/midwest | 0.734 | www.propublica.org/local-initiatives | 0.719 | www.propublica.org/midwest | 0.702 |
| scrapy+md | miss | www.propublica.org/series/the-tax-divide | 0.593 | www.propublica.org/article/how-does-journalism-wor | 0.591 | www.propublica.org/article/how-does-journalism-wor | 0.590 |
| crawlee | #5 | www.propublica.org/local-initiatives | 0.705 | www.propublica.org/local-initiatives | 0.654 | www.propublica.org/partners | 0.653 |
| colly+md | #2 | projects.propublica.org/datastore/ | 0.658 | www.propublica.org/midwest | 0.649 | www.propublica.org/midwest | 0.648 |
| playwright | #5 | www.propublica.org/local-initiatives | 0.705 | www.propublica.org/local-initiatives | 0.654 | www.propublica.org/partners | 0.653 |


**Q8: Who is the Midwest Editor for ProPublica?**
*(expects URL containing: `midwest`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigativ | 0.623 | www.propublica.org/article/propublica-investigativ | 0.620 | www.propublica.org/article/propublica-investigativ | 0.597 |
| crawl4ai | #1 | www.propublica.org/midwest | 0.721 | www.propublica.org/diversity | 0.706 | www.propublica.org/local-initiatives | 0.705 |
| crawl4ai-raw | #1 | www.propublica.org/midwest | 0.721 | www.propublica.org/diversity | 0.706 | www.propublica.org/local-initiatives | 0.705 |
| scrapy+md | miss | www.propublica.org/article/how-does-journalism-wor | 0.675 | www.propublica.org/people/talia-buford/page/4 | 0.666 | www.propublica.org/series/the-tax-divide | 0.662 |
| crawlee | #5 | www.propublica.org/staff | 0.714 | www.propublica.org/staff | 0.702 | www.propublica.org/staff | 0.697 |
| colly+md | #6 | www.propublica.org/staff | 0.702 | www.propublica.org/staff | 0.697 | www.propublica.org/staff | 0.694 |
| playwright | #5 | www.propublica.org/staff | 0.714 | www.propublica.org/staff | 0.702 | www.propublica.org/staff | 0.697 |


**Q9: What happened to A.L. Martin High School during desegregation in Thomasville?**
*(expects URL containing: `thomasville-alabama-segregation-academies`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/trump-education-departm | 0.551 | www.propublica.org/article/hugo-holland-louisiana- | 0.545 | www.propublica.org/article/trump-education-departm | 0.530 |
| crawl4ai | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.817 | www.propublica.org/article/thomasville-alabama-seg | 0.773 | www.propublica.org/article/thomasville-alabama-seg | 0.772 |
| crawl4ai-raw | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.817 | www.propublica.org/article/thomasville-alabama-seg | 0.773 | www.propublica.org/article/thomasville-alabama-seg | 0.772 |
| scrapy+md | miss | www.propublica.org/article/hugo-holland-louisiana- | 0.520 | www.propublica.org/getinvolved/help-propublica-rep | 0.502 | www.propublica.org/article/hugo-holland-louisiana- | 0.485 |
| crawlee | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.781 | www.propublica.org/article/thomasville-alabama-seg | 0.773 | www.propublica.org/article/thomasville-alabama-seg | 0.765 |
| colly+md | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.781 | www.propublica.org/article/thomasville-alabama-seg | 0.776 | www.propublica.org/article/thomasville-alabama-seg | 0.773 |
| playwright | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.781 | www.propublica.org/article/thomasville-alabama-seg | 0.773 | www.propublica.org/article/thomasville-alabama-seg | 0.765 |


**Q10: How did Black students in Thomasville respond to the conditions at Thomasville High after the merger?**
*(expects URL containing: `thomasville-alabama-segregation-academies`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/trump-education-departm | 0.556 | www.propublica.org/article/trump-education-departm | 0.554 | www.propublica.org/article/trump-education-departm | 0.540 |
| crawl4ai | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.767 | www.propublica.org/article/thomasville-alabama-seg | 0.764 | www.propublica.org/article/thomasville-alabama-seg | 0.756 |
| crawl4ai-raw | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.767 | www.propublica.org/article/thomasville-alabama-seg | 0.764 | www.propublica.org/article/thomasville-alabama-seg | 0.756 |
| scrapy+md | miss | www.propublica.org/article/our-journalists-stopped | 0.510 | www.propublica.org/people/sarahbeth-maney | 0.502 | www.propublica.org/getinvolved/help-propublica-rep | 0.501 |
| crawlee | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.763 | www.propublica.org/article/thomasville-alabama-seg | 0.758 | www.propublica.org/article/thomasville-alabama-seg | 0.756 |
| colly+md | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.763 | www.propublica.org/article/thomasville-alabama-seg | 0.758 | www.propublica.org/article/thomasville-alabama-seg | 0.756 |
| playwright | #1 | www.propublica.org/article/thomasville-alabama-seg | 0.763 | www.propublica.org/article/thomasville-alabama-seg | 0.758 | www.propublica.org/article/thomasville-alabama-seg | 0.756 |


**Q11: What recent award did ProPublica and The Connecticut Mirror win?**
*(expects URL containing: `archive`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/year-in-photos-illustra | 0.594 | www.propublica.org/article/propublica-most-read-st | 0.586 | www.propublica.org/article/propublica-most-read-st | 0.581 |
| crawl4ai | #17 | www.propublica.org/feeds/propublica/main | 0.765 | www.propublica.org/article/propublica-and-the-conn | 0.751 | www.propublica.org/article/propublica-and-the-conn | 0.732 |
| crawl4ai-raw | #17 | www.propublica.org/feeds/propublica/main | 0.765 | www.propublica.org/article/propublica-and-the-conn | 0.751 | www.propublica.org/article/propublica-and-the-conn | 0.732 |
| scrapy+md | miss | www.propublica.org/ | 0.845 | www.propublica.org/ | 0.716 | www.propublica.org/article/propublica-emerging-rep | 0.635 |
| crawlee | #20 | www.propublica.org/feeds/propublica/main | 0.802 | www.propublica.org/article/propublica-and-the-conn | 0.751 | www.propublica.org/article/propublica-and-the-conn | 0.750 |
| colly+md | miss | www.propublica.org/article/propublica-and-the-conn | 0.768 | www.propublica.org/ | 0.754 | www.propublica.org/article/propublica-and-the-conn | 0.750 |
| playwright | #20 | www.propublica.org/feeds/propublica/main | 0.802 | www.propublica.org/article/propublica-and-the-conn | 0.751 | www.propublica.org/article/propublica-and-the-conn | 0.750 |


**Q12: What is the focus of the Connecticut Senate's new towing reforms?**
*(expects URL containing: `dave-altimari`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/connecticut-towing-dmv- | 0.782 | www.propublica.org/article/connecticut-towing-dmv- | 0.777 | www.propublica.org/article/connecticut-towing-dmv- | 0.760 |
| crawl4ai | #2 | www.propublica.org/feeds/propublica/main | 0.774 | www.propublica.org/people/dave-altimari | 0.769 | www.propublica.org/article/connecticut-towing-refo | 0.765 |
| crawl4ai-raw | #2 | www.propublica.org/feeds/propublica/main | 0.774 | www.propublica.org/people/dave-altimari | 0.769 | www.propublica.org/article/connecticut-towing-refo | 0.765 |
| scrapy+md | miss | www.propublica.org/ | 0.576 | www.propublica.org/ | 0.516 | www.propublica.org/article/homeless-encampment-rem | 0.515 |
| crawlee | #4 | www.propublica.org/feeds/propublica/main | 0.802 | www.propublica.org/feeds/propublica/main | 0.799 | www.propublica.org/article/connecticut-towing-refo | 0.765 |
| colly+md | miss | www.propublica.org/article/connecticut-towing-refo | 0.765 | www.propublica.org/article/connecticut-towing-refo | 0.757 | www.propublica.org/article/connecticut-towing-refo | 0.729 |
| playwright | #4 | www.propublica.org/feeds/propublica/main | 0.802 | www.propublica.org/feeds/propublica/main | 0.799 | www.propublica.org/article/connecticut-towing-refo | 0.765 |


**Q13: What issues are Connecticut towing companies facing with the new law?**
*(expects URL containing: `dave-altimari`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/connecticut-towing-dmv- | 0.788 | www.propublica.org/article/connecticut-towing-dmv- | 0.779 | www.propublica.org/article/connecticut-towing-dmv- | 0.768 |
| crawl4ai | #15 | www.propublica.org/feeds/propublica/main | 0.784 | www.propublica.org/article/propublica-and-the-conn | 0.767 | www.propublica.org/feeds/propublica/main | 0.757 |
| crawl4ai-raw | #15 | www.propublica.org/feeds/propublica/main | 0.784 | www.propublica.org/article/propublica-and-the-conn | 0.767 | www.propublica.org/feeds/propublica/main | 0.757 |
| scrapy+md | miss | www.propublica.org/ | 0.551 | www.propublica.org/people/agnel-philip | 0.549 | www.propublica.org/article/homeless-encampment-rem | 0.548 |
| crawlee | #3 | www.propublica.org/feeds/propublica/main | 0.802 | www.propublica.org/feeds/propublica/main | 0.777 | www.propublica.org/people/dave-altimari | 0.772 |
| colly+md | miss | www.propublica.org/article/connecticut-towing-refo | 0.755 | www.propublica.org/article/connecticut-towing-refo | 0.748 | www.propublica.org/article/propublica-and-the-conn | 0.724 |
| playwright | #3 | www.propublica.org/feeds/propublica/main | 0.802 | www.propublica.org/feeds/propublica/main | 0.777 | www.propublica.org/people/dave-altimari | 0.772 |


**Q14: What role did James Johnson's photographs play in the investigation of the Shoe Lane community's displacement?**
*(expects URL containing: `family-photos-of-shoe-lane-destruction`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/minneapolis-immigration | 0.483 | www.propublica.org/article/year-in-photos-illustra | 0.476 | www.propublica.org/article/jackson-mississippi-syn | 0.474 |
| crawl4ai | #1 | www.propublica.org/article/family-photos-of-shoe-l | 0.724 | www.propublica.org/article/family-photos-of-shoe-l | 0.712 | www.propublica.org/article/family-photos-of-shoe-l | 0.708 |
| crawl4ai-raw | #1 | www.propublica.org/article/family-photos-of-shoe-l | 0.724 | www.propublica.org/article/family-photos-of-shoe-l | 0.712 | www.propublica.org/article/family-photos-of-shoe-l | 0.708 |
| scrapy+md | miss | www.propublica.org/people/sarahbeth-maney | 0.561 | www.propublica.org/people/sarahbeth-maney | 0.540 | www.propublica.org/article/how-photographers-sough | 0.500 |
| crawlee | #1 | www.propublica.org/article/family-photos-of-shoe-l | 0.734 | www.propublica.org/article/family-photos-of-shoe-l | 0.724 | www.propublica.org/article/family-photos-of-shoe-l | 0.695 |
| colly+md | #1 | www.propublica.org/article/family-photos-of-shoe-l | 0.734 | www.propublica.org/article/family-photos-of-shoe-l | 0.724 | www.propublica.org/article/how-virginia-college-ex | 0.717 |
| playwright | #1 | www.propublica.org/article/family-photos-of-shoe-l | 0.734 | www.propublica.org/article/family-photos-of-shoe-l | 0.724 | www.propublica.org/article/family-photos-of-shoe-l | 0.695 |


**Q15: What actions did Christopher Newport University take regarding the Shoe Lane area in 1961?**
*(expects URL containing: `family-photos-of-shoe-lane-destruction`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/jackson-mississippi-syn | 0.487 | www.propublica.org/article/institute-of-museum-and | 0.472 | www.propublica.org/article/trump-education-departm | 0.453 |
| crawl4ai | #3 | www.propublica.org/article/christopher-newport-uni | 0.785 | www.propublica.org/article/christopher-newport-uni | 0.742 | www.propublica.org/article/family-photos-of-shoe-l | 0.726 |
| crawl4ai-raw | #3 | www.propublica.org/article/christopher-newport-uni | 0.785 | www.propublica.org/article/christopher-newport-uni | 0.742 | www.propublica.org/article/family-photos-of-shoe-l | 0.726 |
| scrapy+md | miss | www.propublica.org/getinvolved/help-propublica-rep | 0.465 | www.propublica.org/topics/education | 0.457 | www.propublica.org/people/rob-davis/page/2 | 0.450 |
| crawlee | #1 | www.propublica.org/article/family-photos-of-shoe-l | 0.799 | www.propublica.org/article/christopher-newport-uni | 0.785 | www.propublica.org/article/christopher-newport-uni | 0.777 |
| colly+md | #1 | www.propublica.org/article/family-photos-of-shoe-l | 0.799 | www.propublica.org/article/christopher-newport-uni | 0.785 | www.propublica.org/article/how-virginia-college-ex | 0.780 |
| playwright | #1 | www.propublica.org/article/family-photos-of-shoe-l | 0.799 | www.propublica.org/article/christopher-newport-uni | 0.785 | www.propublica.org/article/christopher-newport-uni | 0.777 |


**Q16: What are some featured posts by Wendi C. Thomas?**
*(expects URL containing: `wendi-thomas`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/life-inside-ice-dilley- | 0.486 | www.propublica.org/article/habeas-petitions-immigr | 0.475 | www.propublica.org/article/propublica-investigatio | 0.475 |
| crawl4ai | #11 | www.propublica.org/people/anna-clark | 0.550 | www.propublica.org/people/logan-jaffe | 0.543 | www.propublica.org/people/anna-maria-barry-jester | 0.533 |
| crawl4ai-raw | #11 | www.propublica.org/people/anna-clark | 0.550 | www.propublica.org/people/logan-jaffe | 0.543 | www.propublica.org/people/anna-maria-barry-jester | 0.533 |
| scrapy+md | miss | www.propublica.org/people/talia-buford/page/2 | 0.532 | www.propublica.org/people/nicole-santa-cruz | 0.529 | www.propublica.org/people/chris-alcantara | 0.520 |
| crawlee | #8 | www.propublica.org/atpropublica/propublica-selects | 0.589 | www.propublica.org/people/anna-maria-barry-jester | 0.541 | www.propublica.org/people/jennifer-berry-hawes | 0.532 |
| colly+md | miss | www.propublica.org/article/how-virginia-college-ex | 0.519 | www.propublica.org/people/mary-hudetz | 0.517 | www.propublica.org/topics/racial-justice | 0.514 |
| playwright | #7 | www.propublica.org/atpropublica/propublica-selects | 0.589 | www.propublica.org/people/anna-maria-barry-jester | 0.541 | www.propublica.org/people/jennifer-berry-hawes | 0.532 |


**Q17: What is the date of the article about Trump's Memphis Crime Task Force?**
*(expects URL containing: `wendi-thomas`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/memphis-safe-task-force | 0.801 | www.propublica.org/article/memphis-safe-task-force | 0.779 | www.propublica.org/article/memphis-safe-task-force | 0.772 |
| crawl4ai | #5 | www.propublica.org/article/memphis-safe-task-force | 0.802 | www.propublica.org/article/memphis-safe-task-force | 0.783 | www.propublica.org/article/memphis-safe-task-force | 0.777 |
| crawl4ai-raw | #5 | www.propublica.org/article/memphis-safe-task-force | 0.802 | www.propublica.org/article/memphis-safe-task-force | 0.783 | www.propublica.org/article/memphis-safe-task-force | 0.777 |
| scrapy+md | miss | www.propublica.org/article/trump-mass-deportation- | 0.613 | www.propublica.org/article/our-journalists-stopped | 0.611 | www.propublica.org/article/trump-mass-deportation- | 0.607 |
| crawlee | #8 | www.propublica.org/article/memphis-safe-task-force | 0.827 | www.propublica.org/article/memphis-safe-task-force | 0.816 | www.propublica.org/article/memphis-safe-task-force | 0.777 |
| colly+md | miss | www.propublica.org/people/mollie-simon | 0.700 | www.propublica.org/article/caught-in-crackdown-tru | 0.697 | www.propublica.org/article/black-children-were-jai | 0.694 |
| playwright | #8 | www.propublica.org/article/memphis-safe-task-force | 0.827 | www.propublica.org/article/memphis-safe-task-force | 0.816 | www.propublica.org/article/memphis-safe-task-force | 0.777 |


**Q18: What is the main focus of the investigation in the Juvenile Injustice series?**
*(expects URL containing: `juvenile-injustice-tennessee`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/wisconsin-corey-stingle | 0.576 | www.propublica.org/article/wisconsin-corey-stingle | 0.554 | www.propublica.org/article/wisconsin-corey-stingle | 0.548 |
| crawl4ai | #3 | www.propublica.org/article/propublica-suing-depart | 0.572 | www.propublica.org/series/schoolyard-sheriffs | 0.565 | www.propublica.org/series/juvenile-injustice-tenne | 0.563 |
| crawl4ai-raw | #3 | www.propublica.org/article/propublica-suing-depart | 0.572 | www.propublica.org/series/schoolyard-sheriffs | 0.565 | www.propublica.org/series/juvenile-injustice-tenne | 0.562 |
| scrapy+md | miss | www.propublica.org/article/when-it-comes-to-rape-j | 0.553 | www.propublica.org/article/meet-propublicas-2021-d | 0.532 | www.propublica.org/article/hugo-holland-louisiana- | 0.532 |
| crawlee | #4 | www.propublica.org/topics/criminal-justice | 0.613 | www.propublica.org/series/schoolyard-sheriffs | 0.557 | www.propublica.org/midwest | 0.554 |
| colly+md | #21 | www.propublica.org/article/black-children-were-jai | 0.624 | www.propublica.org/article/black-children-were-jai | 0.613 | www.propublica.org/article/black-children-were-jai | 0.611 |
| playwright | #4 | www.propublica.org/topics/criminal-justice | 0.613 | www.propublica.org/series/schoolyard-sheriffs | 0.557 | www.propublica.org/midwest | 0.554 |


**Q19: What was the largest known domestic slave sale in United States history?**
*(expects URL containing: `charleston-slave-auction-historical-marker`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/hugo-holland-louisiana- | 0.491 | www.propublica.org/article/trump-education-departm | 0.488 | www.propublica.org/article/hugo-holland-louisiana- | 0.463 |
| crawl4ai | #1 | www.propublica.org/article/charleston-slave-auctio | 0.754 | www.propublica.org/article/charleston-slave-auctio | 0.708 | www.propublica.org/article/charleston-slave-auctio | 0.681 |
| crawl4ai-raw | #1 | www.propublica.org/article/charleston-slave-auctio | 0.754 | www.propublica.org/article/charleston-slave-auctio | 0.708 | www.propublica.org/article/charleston-slave-auctio | 0.681 |
| scrapy+md | miss | www.propublica.org/article/hugo-holland-louisiana- | 0.470 | www.propublica.org/article/trump-hud-weakening-enf | 0.445 | www.propublica.org/article/bird-flu-airborne-usda- | 0.440 |
| crawlee | #1 | www.propublica.org/article/charleston-slave-auctio | 0.748 | www.propublica.org/article/charleston-slave-auctio | 0.689 | www.propublica.org/article/charleston-slave-auctio | 0.681 |
| colly+md | miss | www.propublica.org/topics/racial-justice | 0.610 | www.propublica.org/article/how-to-report-on-repatr | 0.601 | www.propublica.org/article/lawmakers-propose-600-m | 0.601 |
| playwright | #1 | www.propublica.org/article/charleston-slave-auctio | 0.748 | www.propublica.org/article/charleston-slave-auctio | 0.689 | www.propublica.org/article/charleston-slave-auctio | 0.681 |


**Q20: Who was responsible for the discovery of the ad for the sale of 600 enslaved people?**
*(expects URL containing: `charleston-slave-auction-historical-marker`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/grupo-especial-de-segur | 0.472 | www.propublica.org/article/trump-education-departm | 0.468 | www.propublica.org/article/jackson-mississippi-syn | 0.465 |
| crawl4ai | #1 | www.propublica.org/article/charleston-slave-auctio | 0.712 | www.propublica.org/article/charleston-slave-auctio | 0.709 | www.propublica.org/article/charleston-slave-auctio | 0.703 |
| crawl4ai-raw | #1 | www.propublica.org/article/charleston-slave-auctio | 0.712 | www.propublica.org/article/charleston-slave-auctio | 0.709 | www.propublica.org/article/charleston-slave-auctio | 0.703 |
| scrapy+md | miss | www.propublica.org/article/hugo-holland-louisiana- | 0.478 | www.propublica.org/article/our-journalists-stopped | 0.475 | www.propublica.org/article/our-journalists-stopped | 0.469 |
| crawlee | #1 | www.propublica.org/article/charleston-slave-auctio | 0.720 | www.propublica.org/article/charleston-slave-auctio | 0.712 | www.propublica.org/article/charleston-slave-auctio | 0.708 |
| colly+md | miss | www.propublica.org/topics/racial-justice | 0.661 | www.propublica.org/article/how-virginia-college-ex | 0.528 | www.propublica.org/article/new-bill-seeks-to-remov | 0.523 |
| playwright | #1 | www.propublica.org/article/charleston-slave-auctio | 0.720 | www.propublica.org/article/charleston-slave-auctio | 0.712 | www.propublica.org/article/charleston-slave-auctio | 0.708 |


**Q21: What topics does Anna Clark cover in her reporting?**
*(expects URL containing: `anna-clark`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigatio | 0.524 | www.propublica.org/article/propublica-most-read-st | 0.522 | www.propublica.org/article/propublica-investigatio | 0.511 |
| crawl4ai | #1 | www.propublica.org/people/anna-clark | 0.712 | www.propublica.org/article/michigan-solar-farms-he | 0.590 | www.propublica.org/feeds/propublica/main | 0.582 |
| crawl4ai-raw | #1 | www.propublica.org/people/anna-clark | 0.712 | www.propublica.org/article/michigan-solar-farms-he | 0.590 | www.propublica.org/feeds/propublica/main | 0.582 |
| scrapy+md | miss | www.propublica.org/article/meet-propublicas-2022-s | 0.565 | www.propublica.org/article/meet-propublicas-2021-d | 0.565 | www.propublica.org/article/meet-propublicas-2021-d | 0.565 |
| crawlee | #1 | www.propublica.org/people/anna-clark | 0.668 | www.propublica.org/people/anna-clark | 0.590 | www.propublica.org/article/propublica-and-the-conn | 0.582 |
| colly+md | miss | www.propublica.org/article/propublica-and-the-conn | 0.582 | www.propublica.org/article/water-aquifers-groundwa | 0.579 | www.propublica.org/article/propublica-and-the-conn | 0.566 |
| playwright | #1 | www.propublica.org/people/anna-clark | 0.668 | www.propublica.org/people/anna-clark | 0.590 | www.propublica.org/article/propublica-and-the-conn | 0.582 |


**Q22: What is the title of Anna Clark's book that won the Hillman Prize for Book Journalism?**
*(expects URL containing: `anna-clark`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/fda-generic-drug-equiva | 0.463 | www.propublica.org/article/propublica-reaching-out | 0.455 | www.propublica.org/article/propublica-reaching-out | 0.452 |
| crawl4ai | #1 | www.propublica.org/people/anna-clark | 0.618 | www.propublica.org/feeds/propublica/main | 0.527 | www.propublica.org/feeds/propublica/main | 0.525 |
| crawl4ai-raw | #1 | www.propublica.org/people/anna-clark | 0.618 | www.propublica.org/feeds/propublica/main | 0.527 | www.propublica.org/feeds/propublica/main | 0.525 |
| scrapy+md | miss | www.propublica.org/article/meet-propublicas-2022-s | 0.532 | www.propublica.org/ | 0.523 | www.propublica.org/article/meet-propublicas-2022-s | 0.514 |
| crawlee | #1 | www.propublica.org/people/anna-clark | 0.562 | www.propublica.org/article/propublica-and-the-conn | 0.525 | www.propublica.org/leadership | 0.515 |
| colly+md | miss | www.propublica.org/article/propublica-and-the-conn | 0.525 | www.propublica.org/article/propublica-and-the-conn | 0.505 | www.propublica.org/article/propublica-and-the-conn | 0.502 |
| playwright | #1 | www.propublica.org/people/anna-clark | 0.562 | www.propublica.org/article/propublica-and-the-conn | 0.525 | www.propublica.org/leadership | 0.515 |


**Q23: How many people filed claims against Purdue Pharma for opioid-related harm?**
*(expects URL containing: `purdue-settlement-leaves-opioid-victims-behind`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/rx-inspector-reshaping- | 0.574 | www.propublica.org/article/rx-inspector-reshaping- | 0.568 | www.propublica.org/article/rx-inspector-reshaping- | 0.566 |
| crawl4ai | #1 | www.propublica.org/article/purdue-settlement-leave | 0.758 | www.propublica.org/article/purdue-settlement-leave | 0.757 | www.propublica.org/feeds/propublica/main | 0.746 |
| crawl4ai-raw | #1 | www.propublica.org/article/purdue-settlement-leave | 0.758 | www.propublica.org/article/purdue-settlement-leave | 0.757 | www.propublica.org/feeds/propublica/main | 0.746 |
| scrapy+md | miss | www.propublica.org/ | 0.597 | www.propublica.org/people/maya-miller/page/8 | 0.570 | www.propublica.org/article/rx-inspector-fda-generi | 0.570 |
| crawlee | #1 | www.propublica.org/article/purdue-settlement-leave | 0.757 | www.propublica.org/article/purdue-settlement-leave | 0.743 | www.propublica.org/feeds/propublica/main | 0.742 |
| colly+md | miss | www.propublica.org/ | 0.634 | www.propublica.org/article/veterans-affairs-mental | 0.602 | www.propublica.org/article/propublica-files-lawsui | 0.602 |
| playwright | #1 | www.propublica.org/article/purdue-settlement-leave | 0.757 | www.propublica.org/article/purdue-settlement-leave | 0.743 | www.propublica.org/feeds/propublica/main | 0.742 |


**Q24: What significant provision was removed from the new Purdue settlement plan that affected victims' ability to prove their claims?**
*(expects URL containing: `purdue-settlement-leaves-opioid-victims-behind`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/oklahoma-survivors-act- | 0.603 | www.propublica.org/article/minnesota-mandated-repo | 0.594 | www.propublica.org/article/columbia-university-new | 0.568 |
| crawl4ai | #1 | www.propublica.org/article/purdue-settlement-leave | 0.773 | www.propublica.org/feeds/propublica/main | 0.765 | www.propublica.org/article/purdue-settlement-leave | 0.756 |
| crawl4ai-raw | #1 | www.propublica.org/article/purdue-settlement-leave | 0.773 | www.propublica.org/feeds/propublica/main | 0.765 | www.propublica.org/article/purdue-settlement-leave | 0.756 |
| scrapy+md | miss | www.propublica.org/ | 0.577 | www.propublica.org/article/trump-hud-weakening-enf | 0.556 | www.propublica.org/article/when-it-comes-to-rape-j | 0.539 |
| crawlee | #1 | www.propublica.org/article/purdue-settlement-leave | 0.787 | www.propublica.org/article/purdue-settlement-leave | 0.773 | www.propublica.org/feeds/propublica/main | 0.772 |
| colly+md | miss | www.propublica.org/ | 0.591 | www.propublica.org/article/veterans-affairs-mental | 0.576 | www.propublica.org/article/propublica-files-lawsui | 0.576 |
| playwright | #1 | www.propublica.org/article/purdue-settlement-leave | 0.787 | www.propublica.org/article/purdue-settlement-leave | 0.773 | www.propublica.org/feeds/propublica/main | 0.772 |


**Q25: What topics does Anna Maria Barry-Jester report on?**
*(expects URL containing: `anna-maria-barry-jester`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/habeas-petitions-immigr | 0.482 | www.propublica.org/article/propublica-investigatio | 0.481 | www.propublica.org/article/ice-dilley-ninos-cartas | 0.477 |
| crawl4ai | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.665 | www.propublica.org/people/anna-clark | 0.577 | www.propublica.org/article/second-trump-presidency | 0.570 |
| crawl4ai-raw | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.665 | www.propublica.org/people/anna-clark | 0.577 | www.propublica.org/article/second-trump-presidency | 0.570 |
| scrapy+md | miss | www.propublica.org/article/meet-propublicas-2021-d | 0.540 | www.propublica.org/article/meet-propublicas-2021-d | 0.535 | www.propublica.org/people/maryam-jameel/page/4 | 0.531 |
| crawlee | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.641 | www.propublica.org/people/anna-maria-barry-jester | 0.589 | www.propublica.org/article/syphilis-south-dakota-g | 0.560 |
| colly+md | miss | www.propublica.org/people/doug-bock-clark | 0.540 | www.propublica.org/article/propublica-and-the-conn | 0.529 | www.propublica.org/people/sharon-lerner | 0.528 |
| playwright | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.641 | www.propublica.org/people/anna-maria-barry-jester | 0.589 | www.propublica.org/article/syphilis-south-dakota-g | 0.560 |


**Q26: What awards has Anna Maria Barry-Jester received for her work?**
*(expects URL containing: `anna-maria-barry-jester`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/oklahoma-survivors-act- | 0.413 | www.propublica.org/article/vida-dentro-ice-dilley- | 0.408 | www.propublica.org/article/oklahoma-survivors-act- | 0.398 |
| crawl4ai | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.520 | www.propublica.org/leadership | 0.455 | www.propublica.org/leadership | 0.455 |
| crawl4ai-raw | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.520 | www.propublica.org/leadership | 0.455 | www.propublica.org/leadership | 0.455 |
| scrapy+md | miss | www.propublica.org/article/meet-propublicas-2022-s | 0.443 | www.propublica.org/article/meet-propublicas-2021-d | 0.439 | www.propublica.org/people/sarahbeth-maney | 0.424 |
| crawlee | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.533 | www.propublica.org/people/anna-maria-barry-jester | 0.497 | www.propublica.org/leadership | 0.478 |
| colly+md | miss | www.propublica.org/people/doug-bock-clark | 0.441 | www.propublica.org/article/propublica-and-the-conn | 0.428 | www.propublica.org/atpropublica/the-rise-and-fall- | 0.419 |
| playwright | #1 | www.propublica.org/people/anna-maria-barry-jester | 0.533 | www.propublica.org/people/anna-maria-barry-jester | 0.497 | www.propublica.org/leadership | 0.478 |


**Q27: How can I share my experience seeking payment from the opioid settlement trusts?**
*(expects URL containing: `purdue-endo-mallinckrodt-opioid-settlement-callout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/kentucky-addiction-reco | 0.580 | www.propublica.org/article/kentucky-addiction-reco | 0.575 | www.propublica.org/article/kentucky-addiction-reco | 0.541 |
| crawl4ai | #1 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.689 | www.propublica.org/feeds/propublica/main | 0.684 | www.propublica.org/article/purdue-settlement-leave | 0.679 |
| crawl4ai-raw | #1 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.689 | www.propublica.org/feeds/propublica/main | 0.684 | www.propublica.org/article/purdue-settlement-leave | 0.679 |
| scrapy+md | miss | www.propublica.org/article/our-journalists-stopped | 0.650 | www.propublica.org/article/our-journalists-stopped | 0.620 | www.propublica.org/article/our-journalists-stopped | 0.618 |
| crawlee | #1 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.689 | www.propublica.org/article/purdue-settlement-leave | 0.679 | www.propublica.org/article/purdue-settlement-leave | 0.666 |
| colly+md | miss | www.propublica.org/ | 0.604 | www.propublica.org/article/trump-doj-colony-ridge- | 0.591 | projects.propublica.org/datastore/ | 0.586 |
| playwright | #1 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.689 | www.propublica.org/article/purdue-settlement-leave | 0.679 | www.propublica.org/article/purdue-settlement-leave | 0.666 |


**Q28: What is the focus of ProPublica and The Philadelphia Inquirer's investigation regarding opioid victims?**
*(expects URL containing: `purdue-endo-mallinckrodt-opioid-settlement-callout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigatio | 0.631 | www.propublica.org/article/averhealth-drug-testing | 0.625 | www.propublica.org/article/drug-testing-thresholds | 0.624 |
| crawl4ai | #4 | www.propublica.org/getinvolved | 0.767 | www.propublica.org/ | 0.759 | www.propublica.org | 0.759 |
| crawl4ai-raw | #4 | www.propublica.org/getinvolved | 0.767 | www.propublica.org | 0.759 | www.propublica.org/ | 0.759 |
| scrapy+md | miss | www.propublica.org/tips/ | 0.663 | www.propublica.org/ | 0.657 | www.propublica.org/ | 0.653 |
| crawlee | #1 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.769 | www.propublica.org/local-reporting-network | 0.745 | www.propublica.org/ | 0.695 |
| colly+md | miss | www.propublica.org/ | 0.695 | www.propublica.org/ | 0.673 | www.propublica.org/ | 0.657 |
| playwright | #1 | www.propublica.org/getinvolved/purdue-endo-mallinc | 0.769 | www.propublica.org/local-reporting-network | 0.745 | www.propublica.org/local-reporting-network/ | 0.745 |


**Q29: What is the purpose of the task force created by Newport News and Christopher Newport University?**
*(expects URL containing: `christopher-newport-university-black-community-uprooted-task-force`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/connecticut-towing-dmv- | 0.545 | www.propublica.org/article/memphis-safe-task-force | 0.499 | www.propublica.org/article/connecticut-towing-dmv- | 0.482 |
| crawl4ai | #1 | www.propublica.org/article/christopher-newport-uni | 0.759 | www.propublica.org/article/christopher-newport-uni | 0.726 | www.propublica.org/article/christopher-newport-uni | 0.708 |
| crawl4ai-raw | #1 | www.propublica.org/article/christopher-newport-uni | 0.759 | www.propublica.org/article/christopher-newport-uni | 0.726 | www.propublica.org/article/christopher-newport-uni | 0.708 |
| scrapy+md | miss | www.propublica.org/article/meet-propublicas-2022-s | 0.505 | www.propublica.org/article/meet-propublicas-2022-s | 0.505 | www.propublica.org/people/talia-buford/page/2 | 0.489 |
| crawlee | #1 | www.propublica.org/article/christopher-newport-uni | 0.731 | www.propublica.org/article/christopher-newport-uni | 0.726 | www.propublica.org/article/christopher-newport-uni | 0.715 |
| colly+md | miss | www.propublica.org/article/christopher-newport-uni | 0.731 | www.propublica.org/article/christopher-newport-uni | 0.715 | www.propublica.org/article/christopher-newport-uni | 0.714 |
| playwright | #1 | www.propublica.org/article/christopher-newport-uni | 0.731 | www.propublica.org/article/christopher-newport-uni | 0.726 | www.propublica.org/article/christopher-newport-uni | 0.715 |


**Q30: How did the expansion of Christopher Newport University affect the Shoe Lane neighborhood?**
*(expects URL containing: `christopher-newport-university-black-community-uprooted-task-force`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/kentucky-addiction-reco | 0.464 | www.propublica.org/article/north-carolina-legislat | 0.464 | www.propublica.org/article/nike-jobs-indonesia-liv | 0.455 |
| crawl4ai | #1 | www.propublica.org/article/christopher-newport-uni | 0.782 | www.propublica.org/article/christopher-newport-uni | 0.773 | www.propublica.org/article/family-photos-of-shoe-l | 0.743 |
| crawl4ai-raw | #1 | www.propublica.org/article/christopher-newport-uni | 0.782 | www.propublica.org/article/christopher-newport-uni | 0.773 | www.propublica.org/article/family-photos-of-shoe-l | 0.743 |
| scrapy+md | miss | www.propublica.org/people/rob-davis/page/2 | 0.497 | www.propublica.org/people/rob-davis | 0.481 | www.propublica.org/article/meet-propublicas-2021-d | 0.480 |
| crawlee | #1 | www.propublica.org/article/christopher-newport-uni | 0.793 | www.propublica.org/article/family-photos-of-shoe-l | 0.789 | www.propublica.org/article/christopher-newport-uni | 0.782 |
| colly+md | miss | www.propublica.org/article/how-virginia-college-ex | 0.793 | www.propublica.org/article/christopher-newport-uni | 0.793 | www.propublica.org/article/family-photos-of-shoe-l | 0.789 |
| playwright | #1 | www.propublica.org/article/christopher-newport-uni | 0.793 | www.propublica.org/article/family-photos-of-shoe-l | 0.789 | www.propublica.org/article/christopher-newport-uni | 0.782 |


**Q31: What topics does Abrahm Lustgarten report on?**
*(expects URL containing: `abrahm-lustgarten`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-most-read-st | 0.476 | www.propublica.org/article/propublica-reaching-out | 0.475 | www.propublica.org/article/propublica-most-read-st | 0.456 |
| crawl4ai | #1 | www.propublica.org/people/abrahm-lustgarten | 0.658 | www.propublica.org/article/climate-science-oil-gas | 0.525 | www.propublica.org/people/abrahm-lustgarten | 0.522 |
| crawl4ai-raw | #1 | www.propublica.org/people/abrahm-lustgarten | 0.658 | www.propublica.org/article/climate-science-oil-gas | 0.525 | www.propublica.org/people/abrahm-lustgarten | 0.522 |
| scrapy+md | miss | www.propublica.org/people/rob-davis/page/2 | 0.515 | www.propublica.org/article/meet-propublicas-2021-d | 0.510 | www.propublica.org/article/meet-propublicas-2022-s | 0.506 |
| crawlee | #1 | www.propublica.org/people/abrahm-lustgarten | 0.637 | www.propublica.org/people/joel-jacobs | 0.519 | www.propublica.org/people/eli-hager | 0.513 |
| colly+md | #1 | www.propublica.org/people/abrahm-lustgarten | 0.630 | www.propublica.org/people/abrahm-lustgarten/page/3 | 0.630 | www.propublica.org/people/doug-bock-clark | 0.523 |
| playwright | #1 | www.propublica.org/people/abrahm-lustgarten | 0.637 | www.propublica.org/people/joel-jacobs | 0.519 | www.propublica.org/people/eli-hager | 0.513 |


**Q32: What awards has Abrahm Lustgarten received for his reporting?**
*(expects URL containing: `abrahm-lustgarten`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/year-in-photos-illustra | 0.484 | www.propublica.org/article/propublica-most-read-st | 0.457 | www.propublica.org/article/propublica-reaching-out | 0.456 |
| crawl4ai | #1 | www.propublica.org/people/abrahm-lustgarten | 0.636 | www.propublica.org/atpropublica/propublica-selects | 0.586 | www.propublica.org/leadership | 0.577 |
| crawl4ai-raw | #1 | www.propublica.org/people/abrahm-lustgarten | 0.636 | www.propublica.org/atpropublica/propublica-selects | 0.586 | www.propublica.org/leadership | 0.577 |
| scrapy+md | miss | www.propublica.org/ | 0.540 | www.propublica.org/article/meet-propublicas-2021-d | 0.527 | www.propublica.org/ | 0.524 |
| crawlee | #1 | www.propublica.org/people/abrahm-lustgarten | 0.640 | www.propublica.org/atpropublica/propublica-selects | 0.583 | www.propublica.org/leadership | 0.577 |
| colly+md | #1 | www.propublica.org/people/abrahm-lustgarten | 0.609 | www.propublica.org/people/abrahm-lustgarten/page/3 | 0.609 | www.propublica.org/people/doug-bock-clark | 0.570 |
| playwright | #1 | www.propublica.org/people/abrahm-lustgarten | 0.640 | www.propublica.org/atpropublica/propublica-selects | 0.583 | www.propublica.org/leadership | 0.577 |


**Q33: What is the role ProPublica is hiring for in partnership with On-Ramps?**
*(expects URL containing: `jobs`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/averhealth-drug-testing | 0.614 | www.propublica.org/article/propublica-investigativ | 0.610 | www.propublica.org/article/propublica-investigativ | 0.602 |
| crawl4ai | #1 | www.propublica.org/jobs | 0.703 | www.propublica.org/collaborate | 0.666 | www.propublica.org/about | 0.641 |
| crawl4ai-raw | #1 | www.propublica.org/jobs | 0.703 | www.propublica.org/collaborate | 0.666 | www.propublica.org/about | 0.641 |
| scrapy+md | miss | www.propublica.org/article/hand-picked-mentors-and | 0.667 | www.propublica.org/tips/ | 0.658 | www.propublica.org/getinvolved/send-propublica-sto | 0.642 |
| crawlee | miss | www.propublica.org/article/propublica-and-the-conn | 0.650 | www.propublica.org/collaborate | 0.648 | www.propublica.org/about | 0.643 |
| colly+md | miss | job-boards.greenhouse.io/propublica | 0.768 | job-boards.greenhouse.io/propublica | 0.688 | www.propublica.org/article/propublica-and-the-conn | 0.650 |
| playwright | #1 | www.propublica.org/jobs | 0.768 | www.propublica.org/jobs | 0.688 | www.propublica.org/article/propublica-and-the-conn | 0.650 |


**Q34: How can I receive job opportunities at ProPublica directly in my inbox?**
*(expects URL containing: `jobs`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigativ | 0.706 | www.propublica.org/article/ice-dilley-children-let | 0.600 | www.propublica.org/article/propublica-reaching-out | 0.588 |
| crawl4ai | #18 | www.propublica.org/support/other-ways-to-give | 0.686 | www.propublica.org/contact | 0.684 | www.propublica.org/collaborate | 0.684 |
| crawl4ai-raw | #18 | www.propublica.org/support/other-ways-to-give | 0.686 | www.propublica.org/contact | 0.684 | www.propublica.org/collaborate | 0.684 |
| scrapy+md | miss | www.propublica.org/legal | 0.711 | www.propublica.org/article/hand-picked-mentors-and | 0.680 | www.propublica.org/article/students-propublica-and | 0.678 |
| crawlee | miss | www.propublica.org/tips/ | 0.713 | www.propublica.org/legal | 0.711 | www.propublica.org/ | 0.681 |
| colly+md | miss | www.propublica.org/tips/#submit | 0.713 | www.propublica.org/tips/#common-questions | 0.713 | www.propublica.org/tips/ | 0.713 |
| playwright | #4 | www.propublica.org/tips | 0.713 | www.propublica.org/tips/ | 0.713 | www.propublica.org/legal | 0.711 |


**Q35: What insights does ProPublica seek from current and former inspectors general?**
*(expects URL containing: `an-open-letter-to-the-inspectors-general-community`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/nursing-home-inspect-da | 0.614 | www.propublica.org/article/nursing-home-inspect-da | 0.608 | www.propublica.org/article/trump-administration-fi | 0.607 |
| crawl4ai | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.740 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.668 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.659 |
| crawl4ai-raw | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.740 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.668 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.659 |
| scrapy+md | miss | www.propublica.org/tips/ | 0.662 | www.propublica.org/ | 0.629 | www.propublica.org/article/how-we-compiled-trump-t | 0.617 |
| crawlee | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.736 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.698 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.696 |
| colly+md | miss | www.propublica.org/getinvolved/an-open-letter-to-t | 0.736 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.733 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.687 |
| playwright | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.736 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.698 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.696 |


**Q36: What concerns have been expressed about the new federal government watchdogs?**
*(expects URL containing: `an-open-letter-to-the-inspectors-general-community`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/h-2a-visa-farmworker-ex | 0.614 | www.propublica.org/article/institute-of-museum-and | 0.587 | www.propublica.org/article/trump-cia-law-enforceme | 0.570 |
| crawl4ai | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.584 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.582 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.581 |
| crawl4ai-raw | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.584 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.582 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.581 |
| scrapy+md | miss | www.propublica.org/article/homeland-security-crcl- | 0.567 | www.propublica.org/article/homeland-security-crcl- | 0.551 | www.propublica.org/article/north-carolina-legislat | 0.546 |
| crawlee | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.587 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.584 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.578 |
| colly+md | miss | www.propublica.org/getinvolved/an-open-letter-to-t | 0.587 | www.propublica.org/article/federal-government-ai-c | 0.585 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.583 |
| playwright | #1 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.587 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.584 | www.propublica.org/getinvolved/an-open-letter-to-t | 0.578 |


**Q37: What are some featured posts by Jason Trahan?**
*(expects URL containing: `jason-trahan`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigatio | 0.485 | www.propublica.org/article/life-inside-ice-dilley- | 0.478 | www.propublica.org/article/habeas-petitions-immigr | 0.475 |
| crawl4ai | #21 | www.propublica.org/people/hannah-allam | 0.529 | www.propublica.org/people/anna-clark | 0.529 | www.propublica.org/people/logan-jaffe | 0.513 |
| crawl4ai-raw | #21 | www.propublica.org/people/hannah-allam | 0.529 | www.propublica.org/people/anna-clark | 0.529 | www.propublica.org/people/logan-jaffe | 0.513 |
| scrapy+md | miss | www.propublica.org/people/rob-davis/page/2 | 0.527 | www.propublica.org/people/chris-alcantara | 0.525 | www.propublica.org/people/rob-davis | 0.521 |
| crawlee | #1 | www.propublica.org/people/jason-trahan | 0.515 | www.propublica.org/series/segregation-now | 0.513 | www.propublica.org/article/tribal-colleges-univers | 0.513 |
| colly+md | miss | www.propublica.org/people/perla-trevizo | 0.523 | www.propublica.org/article/how-virginia-college-ex | 0.513 | www.propublica.org/people/doug-bock-clark | 0.507 |
| playwright | #1 | www.propublica.org/people/jason-trahan | 0.515 | www.propublica.org/article/tribal-colleges-univers | 0.513 | www.propublica.org/people/joel-jacobs | 0.507 |


**Q38: What is the topic of Jason Trahan's post published on April 27, 2026?**
*(expects URL containing: `jason-trahan`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/life-inside-ice-dilley- | 0.535 | www.propublica.org/article/propublica-most-read-st | 0.515 | www.propublica.org/article/washington-renewable-en | 0.513 |
| crawl4ai | miss | www.propublica.org/archive | 0.605 | www.propublica.org/newsapps | 0.572 | www.propublica.org/feeds/propublica/main | 0.567 |
| crawl4ai-raw | miss | www.propublica.org/archive | 0.605 | www.propublica.org/newsapps | 0.572 | www.propublica.org/feeds/propublica/main | 0.567 |
| scrapy+md | miss | www.propublica.org/topics/environment | 0.561 | www.propublica.org/topics/taxes | 0.558 | www.propublica.org/article/meet-propublicas-2022-s | 0.554 |
| crawlee | #3 | www.propublica.org/newsapps | 0.574 | www.propublica.org/archive | 0.560 | www.propublica.org/people/jason-trahan | 0.559 |
| colly+md | miss | www.propublica.org/people/abrahm-lustgarten/page/3 | 0.587 | www.propublica.org/newsapps | 0.574 | www.propublica.org/newsapps | 0.558 |
| playwright | #3 | www.propublica.org/newsapps | 0.574 | www.propublica.org/archive | 0.560 | www.propublica.org/people/jason-trahan | 0.559 |


**Q39: What is the main focus of ProPublica's politics section?**
*(expects URL containing: `politics`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-most-read-st | 0.661 | www.propublica.org/article/propublica-most-read-st | 0.650 | www.propublica.org/article/propublica-investigativ | 0.621 |
| crawl4ai | miss | www.propublica.org/about | 0.719 | www.propublica.org/diversity | 0.677 | www.propublica.org/atpropublica/propublica-selects | 0.675 |
| crawl4ai-raw | miss | www.propublica.org/about | 0.719 | www.propublica.org/diversity | 0.677 | www.propublica.org/atpropublica/propublica-selects | 0.675 |
| scrapy+md | miss | www.propublica.org/getinvolved/send-propublica-sto | 0.709 | www.propublica.org/ | 0.685 | www.propublica.org/tips/ | 0.676 |
| crawlee | miss | www.propublica.org/about | 0.720 | www.propublica.org/ | 0.685 | www.propublica.org/local-initiatives | 0.676 |
| colly+md | miss | job-boards.greenhouse.io/propublica | 0.697 | www.propublica.org/ | 0.687 | www.propublica.org/ | 0.685 |
| playwright | miss | www.propublica.org/about | 0.720 | www.propublica.org/jobs | 0.697 | www.propublica.org/ | 0.685 |


**Q40: What are some featured stories in the politics section of ProPublica?**
*(expects URL containing: `politics`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-most-read-st | 0.691 | www.propublica.org/article/propublica-most-read-st | 0.686 | www.propublica.org/article/propublica-investigatio | 0.657 |
| crawl4ai | #40 | www.propublica.org/about | 0.707 | www.propublica.org/article/second-trump-presidency | 0.702 | www.propublica.org/atpropublica/propublica-selects | 0.693 |
| crawl4ai-raw | #40 | www.propublica.org/about | 0.707 | www.propublica.org/article/second-trump-presidency | 0.702 | www.propublica.org/atpropublica/propublica-selects | 0.693 |
| scrapy+md | miss | www.propublica.org/ | 0.736 | www.propublica.org/article/voters-help-us-report-o | 0.703 | www.propublica.org/getinvolved/send-propublica-sto | 0.697 |
| crawlee | miss | www.propublica.org/ | 0.736 | www.propublica.org/about | 0.707 | www.propublica.org/getinvolved | 0.703 |
| colly+md | miss | www.propublica.org/ | 0.736 | www.propublica.org/people/brooke-stephenson | 0.704 | www.propublica.org/ | 0.702 |
| playwright | miss | www.propublica.org/ | 0.736 | www.propublica.org/about | 0.707 | www.propublica.org/getinvolved | 0.703 |


**Q41: What experiences did Cookie have while desegregating a white high school?**
*(expects URL containing: `cookie-zoe-macon-georgia-school-segregation-documentary`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/trump-education-departm | 0.582 | www.propublica.org/article/trump-education-departm | 0.581 | www.propublica.org/article/trump-education-departm | 0.578 |
| crawl4ai | #3 | www.propublica.org/article/macon-georgia-segregati | 0.810 | www.propublica.org/article/macon-georgia-segregati | 0.808 | www.propublica.org/article/cookie-zoe-macon-georgi | 0.787 |
| crawl4ai-raw | #3 | www.propublica.org/article/macon-georgia-segregati | 0.810 | www.propublica.org/article/macon-georgia-segregati | 0.808 | www.propublica.org/article/cookie-zoe-macon-georgi | 0.787 |
| scrapy+md | miss | www.propublica.org/topics/education | 0.569 | www.propublica.org/getinvolved/help-propublica-rep | 0.557 | www.propublica.org/article/meet-propublicas-2022-s | 0.533 |
| crawlee | #3 | www.propublica.org/article/macon-georgia-segregati | 0.810 | www.propublica.org/article/macon-georgia-segregati | 0.800 | www.propublica.org/article/cookie-zoe-macon-georgi | 0.795 |
| colly+md | miss | www.propublica.org/article/cookie-zoe-macon-georgi | 0.796 | www.propublica.org/article/cookie-zoe-macon-georgi | 0.744 | www.propublica.org/article/cookie-zoe-macon-georgi | 0.713 |
| playwright | #3 | www.propublica.org/article/macon-georgia-segregati | 0.810 | www.propublica.org/article/macon-georgia-segregati | 0.800 | www.propublica.org/article/cookie-zoe-macon-georgi | 0.795 |


**Q42: What school does Zo’e Johnson attend and why did her family choose it?**
*(expects URL containing: `cookie-zoe-macon-georgia-school-segregation-documentary`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/life-inside-ice-dilley- | 0.473 | www.propublica.org/article/ice-dilley-maria-antoni | 0.473 | www.propublica.org/article/ice-dilley-children-let | 0.466 |
| crawl4ai | #10 | www.propublica.org/article/macon-georgia-segregati | 0.664 | www.propublica.org/article/macon-georgia-segregati | 0.660 | www.propublica.org/article/macon-georgia-segregati | 0.657 |
| crawl4ai-raw | #10 | www.propublica.org/article/macon-georgia-segregati | 0.664 | www.propublica.org/article/macon-georgia-segregati | 0.660 | www.propublica.org/article/macon-georgia-segregati | 0.657 |
| scrapy+md | miss | www.propublica.org/article/meet-propublicas-2021-d | 0.522 | www.propublica.org/people/sarahbeth-maney | 0.517 | www.propublica.org/article/meet-propublicas-2021-d | 0.511 |
| crawlee | #6 | www.propublica.org/article/macon-georgia-segregati | 0.701 | www.propublica.org/article/macon-georgia-segregati | 0.665 | www.propublica.org/article/macon-georgia-segregati | 0.656 |
| colly+md | miss | www.propublica.org/article/cookie-zoe-macon-georgi | 0.650 | www.propublica.org/article/cookie-zoe-macon-georgi | 0.649 | www.propublica.org/article/cookie-zoe-macon-georgi | 0.598 |
| playwright | #6 | www.propublica.org/article/macon-georgia-segregati | 0.701 | www.propublica.org/article/macon-georgia-segregati | 0.665 | www.propublica.org/article/macon-georgia-segregati | 0.656 |


**Q43: What is the main focus of ProPublica's Racial Justice topic?**
*(expects URL containing: `racial-justice`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/sheriff-jerry-sheridan- | 0.618 | www.propublica.org/article/wisconsin-corey-stingle | 0.615 | www.propublica.org/article/sheriff-jerry-sheridan- | 0.603 |
| crawl4ai | #28 | www.propublica.org/awards | 0.728 | www.propublica.org/ai-principles | 0.728 | www.propublica.org/atpropublica/propublica-selects | 0.728 |
| crawl4ai-raw | #28 | www.propublica.org/awards | 0.728 | www.propublica.org/atpropublica/propublica-selects | 0.728 | www.propublica.org/local-initiatives | 0.728 |
| scrapy+md | miss | www.propublica.org/diversity | 0.694 | www.propublica.org/getinvolved/help-propublica-rep | 0.664 | www.propublica.org/tips/ | 0.662 |
| crawlee | #31 | www.propublica.org/advertising | 0.720 | www.propublica.org/press-releases | 0.720 | www.propublica.org/media-center | 0.717 |
| colly+md | #5 | www.propublica.org/article/historic-preservation-e | 0.736 | www.propublica.org/article/nike-jobs-indonesia-liv | 0.720 | www.propublica.org/article/la-inspector-general-lo | 0.709 |
| playwright | #30 | www.propublica.org/advertising | 0.720 | www.propublica.org/press-releases | 0.720 | www.propublica.org/media-center | 0.717 |


**Q44: How many Native American ancestors were returned to tribes in 2024 according to ProPublica's reporting?**
*(expects URL containing: `racial-justice`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/gallup-mckinley-native- | 0.583 | www.propublica.org/article/trump-family-deportatio | 0.580 | www.propublica.org/article/trump-family-deportatio | 0.579 |
| crawl4ai | #11 | www.propublica.org/article/native-american-remains | 0.774 | www.propublica.org/article/native-american-remains | 0.745 | www.propublica.org/article/native-american-remains | 0.727 |
| crawl4ai-raw | #11 | www.propublica.org/article/native-american-remains | 0.774 | www.propublica.org/article/native-american-remains | 0.745 | www.propublica.org/article/native-american-remains | 0.727 |
| scrapy+md | miss | www.propublica.org/article/trump-mass-deportation- | 0.564 | www.propublica.org/diversity | 0.558 | www.propublica.org/article/salmonella-chicken-usda | 0.550 |
| crawlee | #15 | www.propublica.org/article/native-american-remains | 0.822 | www.propublica.org/article/native-american-remains | 0.749 | www.propublica.org/article/native-american-remains | 0.707 |
| colly+md | #16 | www.propublica.org/article/how-to-report-on-repatr | 0.690 | www.propublica.org/article/how-to-report-on-repatr | 0.686 | www.propublica.org/article/how-to-report-on-repatr | 0.682 |
| playwright | #15 | www.propublica.org/article/native-american-remains | 0.822 | www.propublica.org/article/native-american-remains | 0.749 | www.propublica.org/article/native-american-remains | 0.707 |


**Q45: What is the main focus of the 'Segregation Now' series?**
*(expects URL containing: `segregation-now`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/trump-education-departm | 0.556 | www.propublica.org/article/trump-education-departm | 0.550 | www.propublica.org/article/trump-education-departm | 0.546 |
| crawl4ai | #2 | www.propublica.org/article/cookie-zoe-macon-georgi | 0.660 | www.propublica.org/series/segregation-now | 0.657 | www.propublica.org/series/segregation-now | 0.649 |
| crawl4ai-raw | #2 | www.propublica.org/article/cookie-zoe-macon-georgi | 0.660 | www.propublica.org/series/segregation-now | 0.657 | www.propublica.org/series/segregation-now | 0.649 |
| scrapy+md | miss | www.propublica.org/article/trump-hud-weakening-enf | 0.625 | www.propublica.org/topics/education | 0.587 | www.propublica.org/article/meet-propublicas-2021-d | 0.583 |
| crawlee | #1 | www.propublica.org/series/segregation-now | 0.747 | www.propublica.org/series/segregation-now | 0.700 | www.propublica.org/article/segregation-academies-p | 0.668 |
| colly+md | #1 | www.propublica.org/series/segregation-now | 0.747 | www.propublica.org/series/segregation-now | 0.700 | www.propublica.org/topics/racial-justice | 0.650 |
| playwright | #1 | www.propublica.org/series/segregation-now | 0.747 | www.propublica.org/series/segregation-now | 0.700 | www.propublica.org/article/segregation-academies-p | 0.668 |


**Q46: How many stories have been published in the 'Segregation Now' series since 2012?**
*(expects URL containing: `segregation-now`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/jackson-mississippi-syn | 0.533 | www.propublica.org/article/trump-education-departm | 0.532 | www.propublica.org/article/trump-education-departm | 0.532 |
| crawl4ai | #3 | www.propublica.org/article/wilcox-county-alabama-s | 0.618 | www.propublica.org/people/sarahbeth-maney | 0.591 | www.propublica.org/series/segregation-now | 0.591 |
| crawl4ai-raw | #3 | www.propublica.org/article/wilcox-county-alabama-s | 0.618 | www.propublica.org/people/sarahbeth-maney | 0.591 | www.propublica.org/series/segregation-now | 0.591 |
| scrapy+md | miss | www.propublica.org/people/sarahbeth-maney | 0.594 | www.propublica.org/article/meet-propublicas-2021-d | 0.589 | www.propublica.org/article/meet-propublicas-2022-s | 0.576 |
| crawlee | #1 | www.propublica.org/series/segregation-now | 0.688 | www.propublica.org/article/wilcox-county-alabama-s | 0.622 | www.propublica.org/series/segregation-now | 0.617 |
| colly+md | #1 | www.propublica.org/series/segregation-now | 0.688 | www.propublica.org/series/segregation-now | 0.617 | www.propublica.org/series/segregation-now | 0.615 |
| playwright | #1 | www.propublica.org/series/segregation-now | 0.688 | www.propublica.org/article/wilcox-county-alabama-s | 0.622 | www.propublica.org/series/segregation-now | 0.617 |


**Q47: What is the principal yardstick for ProPublica's success?**
*(expects URL containing: `impact`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #18 | www.propublica.org/article/averhealth-drug-testing | 0.628 | www.propublica.org/article/propublica-investigativ | 0.583 | www.propublica.org/article/propublica-reaching-out | 0.575 |
| crawl4ai | miss | www.propublica.org/about | 0.666 | www.propublica.org/code-of-ethics | 0.657 | www.propublica.org/staff | 0.635 |
| crawl4ai-raw | miss | www.propublica.org/about | 0.666 | www.propublica.org/code-of-ethics | 0.657 | www.propublica.org/staff | 0.635 |
| scrapy+md | miss | www.propublica.org/getinvolved/send-propublica-sto | 0.675 | www.propublica.org/tips/ | 0.673 | www.propublica.org/code-of-ethics | 0.657 |
| crawlee | #47 | www.propublica.org/about | 0.671 | www.propublica.org/code-of-ethics | 0.657 | www.propublica.org/atpropublica/propublica-selects | 0.635 |
| colly+md | #44 | job-boards.greenhouse.io/propublica | 0.666 | www.propublica.org/code-of-ethics | 0.657 | www.propublica.org/staff | 0.624 |
| playwright | #49 | www.propublica.org/about | 0.671 | www.propublica.org/jobs | 0.666 | www.propublica.org/code-of-ethics | 0.657 |


**Q48: How has ProPublica's reporting influenced legislation regarding abortion access?**
*(expects URL containing: `impact`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.propublica.org/article/propublica-investigatio | 0.718 | www.propublica.org/article/propublica-investigatio | 0.657 | www.propublica.org/article/texas-medical-board-abo | 0.653 |
| crawl4ai | #1 | www.propublica.org/impact | 0.768 | www.propublica.org/impact | 0.723 | www.propublica.org/about | 0.680 |
| crawl4ai-raw | #1 | www.propublica.org/impact | 0.768 | www.propublica.org/impact | 0.723 | www.propublica.org/about | 0.680 |
| scrapy+md | miss | www.propublica.org/getinvolved/send-propublica-sto | 0.666 | www.propublica.org/tips/ | 0.657 | www.propublica.org/article/your-free-range-organic | 0.639 |
| crawlee | #1 | www.propublica.org/impact | 0.703 | www.propublica.org/about | 0.683 | www.propublica.org/getinvolved | 0.677 |
| colly+md | #2 | www.propublica.org/article/high-risk-pregnancies-c | 0.707 | www.propublica.org/impact | 0.679 | www.propublica.org/impact | 0.661 |
| playwright | #1 | www.propublica.org/impact | 0.703 | www.propublica.org/about | 0.683 | www.propublica.org/getinvolved | 0.677 |


**Q49: How can I donate online to ProPublica?**
*(expects URL containing: `other-ways-to-give`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigativ | 0.646 | www.propublica.org/article/trump-administration-fi | 0.615 | www.propublica.org/article/propublica-investigativ | 0.574 |
| crawl4ai | #1 | www.propublica.org/support/other-ways-to-give | 0.790 | www.propublica.org/support/other-ways-to-give | 0.785 | www.propublica.org/support/other-ways-to-give | 0.778 |
| crawl4ai-raw | #1 | www.propublica.org/support/other-ways-to-give | 0.790 | www.propublica.org/support/other-ways-to-give | 0.785 | www.propublica.org/support/other-ways-to-give | 0.778 |
| scrapy+md | #1 | www.propublica.org/support/other-ways-to-give | 0.807 | www.propublica.org/support/manage-recurring | 0.776 | www.propublica.org/support/other-ways-to-give | 0.776 |
| crawlee | #1 | www.propublica.org/support/other-ways-to-give | 0.782 | www.propublica.org/support/other-ways-to-give | 0.770 | www.propublica.org/tips/ | 0.760 |
| colly+md | miss | www.propublica.org/tips/#signal | 0.760 | www.propublica.org/tips/#submit | 0.760 | www.propublica.org/tips/#postalmail | 0.760 |
| playwright | #1 | www.propublica.org/support/other-ways-to-give | 0.782 | www.propublica.org/support/other-ways-to-give | 0.770 | www.propublica.org/tips | 0.760 |


**Q50: What information do I need to include when making a gift in my estate plans for ProPublica?**
*(expects URL containing: `other-ways-to-give`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/trump-administration-fi | 0.581 | www.propublica.org/article/propublica-investigativ | 0.580 | www.propublica.org/article/trump-administration-fi | 0.573 |
| crawl4ai | #1 | www.propublica.org/support/other-ways-to-give | 0.790 | www.propublica.org/support/other-ways-to-give | 0.715 | www.propublica.org/legal | 0.703 |
| crawl4ai-raw | #1 | www.propublica.org/support/other-ways-to-give | 0.790 | www.propublica.org/support/other-ways-to-give | 0.715 | www.propublica.org/legal | 0.703 |
| scrapy+md | #1 | www.propublica.org/support/other-ways-to-give | 0.765 | www.propublica.org/support/other-ways-to-give | 0.764 | www.propublica.org/support/other-ways-to-give | 0.722 |
| crawlee | #1 | www.propublica.org/support/other-ways-to-give | 0.765 | www.propublica.org/support/other-ways-to-give | 0.741 | www.propublica.org/support/other-ways-to-give | 0.714 |
| colly+md | miss | www.propublica.org/code-of-ethics | 0.690 | www.propublica.org/tips/ | 0.662 | www.propublica.org/tips/#submit | 0.662 |
| playwright | #1 | www.propublica.org/support/other-ways-to-give | 0.765 | www.propublica.org/support/other-ways-to-give | 0.741 | www.propublica.org/support/other-ways-to-give | 0.714 |


**Q51: What topics does Sarahbeth Maney cover as a photojournalist?**
*(expects URL containing: `sarahbeth-maney`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/year-in-photos-illustra | 0.531 | www.propublica.org/article/year-in-photos-illustra | 0.520 | www.propublica.org/article/propublica-most-read-st | 0.518 |
| crawl4ai | #1 | www.propublica.org/people/sarahbeth-maney | 0.749 | www.propublica.org/people/sarahbeth-maney | 0.641 | www.propublica.org/people/jennifer-berry-hawes | 0.576 |
| crawl4ai-raw | #1 | www.propublica.org/people/sarahbeth-maney | 0.749 | www.propublica.org/people/sarahbeth-maney | 0.641 | www.propublica.org/people/jennifer-berry-hawes | 0.576 |
| scrapy+md | #1 | www.propublica.org/people/sarahbeth-maney | 0.802 | www.propublica.org/people/sarahbeth-maney | 0.662 | www.propublica.org/article/meet-propublicas-2021-d | 0.634 |
| crawlee | #1 | www.propublica.org/people/sarahbeth-maney | 0.769 | www.propublica.org/people/sarahbeth-maney | 0.662 | www.propublica.org/people/sarahbeth-maney | 0.610 |
| colly+md | miss | www.propublica.org/staff | 0.578 | www.propublica.org/ | 0.554 | www.propublica.org/people/doug-bock-clark | 0.547 |
| playwright | #1 | www.propublica.org/people/sarahbeth-maney | 0.769 | www.propublica.org/people/sarahbeth-maney | 0.662 | www.propublica.org/people/sarahbeth-maney | 0.610 |


**Q52: What notable awards has Sarahbeth Maney received for her work?**
*(expects URL containing: `sarahbeth-maney`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/year-in-photos-illustra | 0.395 | www.propublica.org/article/oklahoma-survivors-act- | 0.390 | www.propublica.org/article/year-in-photos-illustra | 0.388 |
| crawl4ai | #1 | www.propublica.org/people/sarahbeth-maney | 0.611 | www.propublica.org/people/sarahbeth-maney | 0.477 | www.propublica.org/people/jennifer-berry-hawes | 0.466 |
| crawl4ai-raw | #1 | www.propublica.org/people/sarahbeth-maney | 0.611 | www.propublica.org/people/sarahbeth-maney | 0.477 | www.propublica.org/people/jennifer-berry-hawes | 0.466 |
| scrapy+md | #1 | www.propublica.org/people/sarahbeth-maney | 0.665 | www.propublica.org/people/sarahbeth-maney | 0.501 | www.propublica.org/article/meet-propublicas-2021-d | 0.496 |
| crawlee | #1 | www.propublica.org/people/sarahbeth-maney | 0.618 | www.propublica.org/people/sarahbeth-maney | 0.504 | www.propublica.org/people/sarahbeth-maney | 0.501 |
| colly+md | miss | www.propublica.org/staff | 0.478 | www.propublica.org/people/doug-bock-clark | 0.466 | www.propublica.org/awards | 0.459 |
| playwright | #1 | www.propublica.org/people/sarahbeth-maney | 0.618 | www.propublica.org/people/sarahbeth-maney | 0.504 | www.propublica.org/people/sarahbeth-maney | 0.501 |


**Q53: What types of donations does ProPublica accept?**
*(expects URL containing: `gift-acceptance-practices`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/trump-administration-fi | 0.612 | www.propublica.org/article/propublica-investigativ | 0.604 | www.propublica.org/article/trump-administration-fi | 0.583 |
| crawl4ai | #6 | www.propublica.org/legal | 0.769 | www.propublica.org/support/other-ways-to-give | 0.759 | www.propublica.org/supporters | 0.758 |
| crawl4ai-raw | #6 | www.propublica.org/legal | 0.769 | www.propublica.org/support/other-ways-to-give | 0.759 | www.propublica.org/supporters | 0.758 |
| scrapy+md | miss | www.propublica.org/support/other-ways-to-give | 0.791 | www.propublica.org/legal | 0.750 | www.propublica.org/support/other-ways-to-give | 0.741 |
| crawlee | #3 | www.propublica.org/legal | 0.750 | www.propublica.org/support/other-ways-to-give | 0.737 | www.propublica.org/gift-acceptance-practices | 0.730 |
| colly+md | miss | www.propublica.org/code-of-ethics | 0.697 | www.propublica.org/tips/#submit | 0.673 | www.propublica.org/tips/#common-questions | 0.673 |
| playwright | #3 | www.propublica.org/legal | 0.750 | www.propublica.org/support/other-ways-to-give | 0.737 | www.propublica.org/gift-acceptance-practices | 0.730 |


**Q54: What restrictions are placed on donations to ProPublica?**
*(expects URL containing: `gift-acceptance-practices`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/oregon-campaign-finance | 0.637 | www.propublica.org/article/propublica-investigativ | 0.613 | www.propublica.org/article/trump-administration-fi | 0.601 |
| crawl4ai | #5 | www.propublica.org/legal | 0.757 | www.propublica.org/support/other-ways-to-give | 0.733 | www.propublica.org/support/other-ways-to-give | 0.723 |
| crawl4ai-raw | #5 | www.propublica.org/legal | 0.757 | www.propublica.org/support/other-ways-to-give | 0.733 | www.propublica.org/support/other-ways-to-give | 0.723 |
| scrapy+md | miss | www.propublica.org/support/other-ways-to-give | 0.752 | www.propublica.org/legal | 0.751 | www.propublica.org/code-of-ethics | 0.736 |
| crawlee | #3 | www.propublica.org/legal | 0.751 | www.propublica.org/code-of-ethics | 0.736 | www.propublica.org/gift-acceptance-practices | 0.716 |
| colly+md | miss | www.propublica.org/code-of-ethics | 0.736 | www.propublica.org/code-of-ethics | 0.666 | www.propublica.org/code-of-ethics | 0.655 |
| playwright | #3 | www.propublica.org/legal | 0.751 | www.propublica.org/code-of-ethics | 0.736 | www.propublica.org/gift-acceptance-practices | 0.716 |


**Q55: What is Nat Lash's role at ProPublica?**
*(expects URL containing: `nat-lash`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigativ | 0.572 | www.propublica.org/article/trump-administration-fi | 0.565 | www.propublica.org/article/propublica-investigativ | 0.562 |
| crawl4ai | #1 | www.propublica.org/people/nat-lash | 0.673 | www.propublica.org/staff | 0.621 | www.propublica.org/jobs | 0.617 |
| crawl4ai-raw | #1 | www.propublica.org/people/nat-lash | 0.673 | www.propublica.org/staff | 0.621 | www.propublica.org/jobs | 0.617 |
| scrapy+md | miss | www.propublica.org/tips/ | 0.634 | www.propublica.org/people/agnel-philip | 0.599 | www.propublica.org/article/hand-picked-mentors-and | 0.595 |
| crawlee | #2 | www.propublica.org/article/segregation-academies-p | 0.803 | www.propublica.org/people/nat-lash | 0.702 | www.propublica.org/people/nat-lash | 0.671 |
| colly+md | miss | job-boards.greenhouse.io/propublica | 0.647 | www.propublica.org/staff | 0.619 | www.propublica.org/staff | 0.613 |
| playwright | #2 | www.propublica.org/article/segregation-academies-p | 0.803 | www.propublica.org/people/nat-lash | 0.702 | www.propublica.org/people/nat-lash | 0.671 |


**Q56: What is the title of the featured post by Nat Lash published on March 31, 2026?**
*(expects URL containing: `nat-lash`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigatio | 0.568 | www.propublica.org/article/propublica-most-read-st | 0.553 | www.propublica.org/article/propublica-most-read-st | 0.551 |
| crawl4ai | #1 | www.propublica.org/people/nat-lash | 0.636 | www.propublica.org/newsapps | 0.594 | www.propublica.org/people/j-david-mcswane | 0.589 |
| crawl4ai-raw | #1 | www.propublica.org/people/nat-lash | 0.636 | www.propublica.org/newsapps | 0.594 | www.propublica.org/people/j-david-mcswane | 0.589 |
| scrapy+md | miss | www.propublica.org/people/nate-schweber | 0.580 | www.propublica.org/people/chris-alcantara | 0.579 | www.propublica.org/topics/democracy/page/3 | 0.575 |
| crawlee | #2 | www.propublica.org/article/segregation-academies-p | 0.709 | www.propublica.org/people/nat-lash | 0.685 | www.propublica.org/newsapps | 0.606 |
| colly+md | miss | www.propublica.org/newsapps | 0.606 | www.propublica.org/people/sharon-lerner | 0.587 | www.propublica.org/newsapps | 0.584 |
| playwright | #2 | www.propublica.org/article/segregation-academies-p | 0.709 | www.propublica.org/people/nat-lash | 0.685 | www.propublica.org/newsapps | 0.606 |


</details>

## react-dev

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| scrapy+md | 86% (50/58) | 97% (56/58) | 98% (57/58) | 98% (57/58) | 100% (58/58) | 0.916 | 1259 | 216 |
| crawlee | 72% (42/58) | 88% (51/58) | 90% (52/58) | 97% (56/58) | 100% (58/58) | 0.812 | 3063 | 217 |
| playwright | 72% (42/58) | 88% (51/58) | 90% (52/58) | 97% (56/58) | 100% (58/58) | 0.811 | 3067 | 221 |
| crawl4ai | 72% (42/58) | 86% (50/58) | 91% (53/58) | 95% (55/58) | 100% (58/58) | 0.811 | 3210 | 500 |
| crawl4ai-raw | 72% (42/58) | 86% (50/58) | 91% (53/58) | 95% (55/58) | 100% (58/58) | 0.811 | 3210 | 500 |
| colly+md | 74% (43/58) | 84% (49/58) | 88% (51/58) | 95% (55/58) | 98% (57/58) | 0.809 | 5083 | 292 |
| markcrawl | 21% (12/58) | 26% (15/58) | 26% (15/58) | 26% (15/58) | 28% (16/58) | 0.234 | 419 | 51 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for react-dev</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is the purpose of the `useSyncExternalStore` hook?**
*(expects URL containing: `useSyncExternalStore`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/typescript | 0.692 | react.dev/learn/removing-effect-dependencies | 0.685 | react.dev/learn/typescript | 0.683 |
| crawl4ai | #1 | react.dev/reference/react/useSyncExternalStore | 0.769 | react.dev/reference/react/useSyncExternalStore | 0.762 | react.dev/reference/react/useSyncExternalStore | 0.761 |
| crawl4ai-raw | #1 | react.dev/reference/react/useSyncExternalStore | 0.769 | react.dev/reference/react/useSyncExternalStore | 0.762 | react.dev/reference/react/useSyncExternalStore | 0.761 |
| scrapy+md | #1 | react.dev/reference/react/useSyncExternalStore | 0.830 | react.dev/reference/react/useSyncExternalStore | 0.758 | react.dev/reference/react/useSyncExternalStore | 0.754 |
| crawlee | #1 | react.dev/reference/react/useSyncExternalStore | 0.773 | react.dev/reference/react/useSyncExternalStore | 0.762 | react.dev/reference/react/useSyncExternalStore | 0.758 |
| colly+md | #1 | react.dev/reference/react/useSyncExternalStore | 0.773 | react.dev/reference/react/useSyncExternalStore | 0.762 | react.dev/reference/react/useSyncExternalStore | 0.758 |
| playwright | #1 | react.dev/reference/react/useSyncExternalStore | 0.773 | react.dev/reference/react/useSyncExternalStore | 0.762 | react.dev/reference/react/useSyncExternalStore | 0.758 |


**Q2: What functions do you need to pass as arguments to `useSyncExternalStore`?**
*(expects URL containing: `useSyncExternalStore`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/typescript | 0.691 | react.dev/learn/typescript | 0.668 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.664 |
| crawl4ai | #1 | react.dev/reference/react/useSyncExternalStore | 0.761 | react.dev/reference/react/useSyncExternalStore | 0.751 | react.dev/reference/react/useSyncExternalStore | 0.750 |
| crawl4ai-raw | #1 | react.dev/reference/react/useSyncExternalStore | 0.761 | react.dev/reference/react/useSyncExternalStore | 0.751 | react.dev/reference/react/useSyncExternalStore | 0.750 |
| scrapy+md | #1 | react.dev/reference/react/useSyncExternalStore | 0.806 | react.dev/reference/react/useSyncExternalStore | 0.747 | react.dev/reference/react/useSyncExternalStore | 0.729 |
| crawlee | #1 | react.dev/reference/react/useSyncExternalStore | 0.760 | react.dev/reference/react/useSyncExternalStore | 0.747 | react.dev/reference/react/useSyncExternalStore | 0.741 |
| colly+md | #1 | react.dev/reference/react/useSyncExternalStore | 0.760 | react.dev/reference/react/useSyncExternalStore | 0.747 | react.dev/reference/react/useSyncExternalStore | 0.741 |
| playwright | #1 | react.dev/reference/react/useSyncExternalStore | 0.760 | react.dev/reference/react/useSyncExternalStore | 0.747 | react.dev/reference/react/useSyncExternalStore | 0.741 |


**Q3: How do you combine a reducer with context in React?**
*(expects URL containing: `scaling-up-with-reducer-and-context`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.837 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.833 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.814 |
| crawl4ai | #1 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.837 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.831 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.828 |
| crawl4ai-raw | #1 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.837 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.831 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.828 |
| scrapy+md | #1 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.837 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.833 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.820 |
| crawlee | #1 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.827 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.817 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.812 |
| colly+md | #1 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.849 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.833 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.812 |
| playwright | #1 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.849 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.833 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.812 |


**Q4: What are the steps to create a context for managing tasks?**
*(expects URL containing: `scaling-up-with-reducer-and-context`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.690 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.688 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.675 |
| crawl4ai | #1 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.682 | fr.react.dev/learn/managing-state | 0.678 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.677 |
| crawl4ai-raw | #1 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.682 | fr.react.dev/learn/managing-state | 0.678 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.677 |
| scrapy+md | #1 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.690 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.688 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.675 |
| crawlee | #2 | react.dev/learn/passing-data-deeply-with-context | 0.714 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.688 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.679 |
| colly+md | #4 | react.dev/learn/passing-data-deeply-with-context#s | 0.714 | react.dev/learn/passing-data-deeply-with-context#s | 0.714 | react.dev/learn/passing-data-deeply-with-context | 0.714 |
| playwright | #2 | react.dev/learn/passing-data-deeply-with-context | 0.714 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.690 | react.dev/learn/scaling-up-with-reducer-and-contex | 0.688 |


**Q5: What new features will React 18 include?**
*(expects URL containing: `the-plan-for-react-18`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn | 0.644 | react.dev/learn/setup | 0.643 | react.dev/learn/adding-interactivity | 0.638 |
| crawl4ai | #1 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.796 | react.dev/blog/2022/03/29/react-v18 | 0.785 | zh-hans.react.dev/versions | 0.762 |
| crawl4ai-raw | #1 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.796 | react.dev/blog/2022/03/29/react-v18 | 0.785 | zh-hans.react.dev/versions | 0.762 |
| scrapy+md | #1 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.804 | react.dev/blog/2022/03/29/react-v18 | 0.791 | react.dev/blog/2025/10/01/react-19-2 | 0.787 |
| crawlee | #2 | react.dev/blog/2024/02/15/react-labs-what-we-have- | 0.763 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.762 | react.dev/blog/2021/12/17/react-conf-2021-recap | 0.758 |
| colly+md | #2 | react.dev/blog/2024/02/15/react-labs-what-we-have- | 0.763 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.762 | react.dev/blog/2021/12/17/react-conf-2021-recap | 0.758 |
| playwright | #2 | react.dev/blog/2024/02/15/react-labs-what-we-have- | 0.763 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.762 | react.dev/blog/2021/12/17/react-conf-2021-recap | 0.758 |


**Q6: How can I try React 18 Alpha today?**
*(expects URL containing: `the-plan-for-react-18`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/installation | 0.668 | react.dev/learn/add-react-to-an-existing-project | 0.645 | react.dev/learn/react-developer-tools | 0.637 |
| crawl4ai | #1 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.757 | az.react.dev/versions | 0.720 | react.dev/blog/2021/12/17/react-conf-2021-recap | 0.718 |
| crawl4ai-raw | #1 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.757 | az.react.dev/versions | 0.720 | react.dev/blog/2021/12/17/react-conf-2021-recap | 0.718 |
| scrapy+md | #1 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.754 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.710 | react.dev/blog/2022/03/29/react-v18 | 0.701 |
| crawlee | #1 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.754 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.748 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.746 |
| colly+md | #1 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.754 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.748 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.746 |
| playwright | #1 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.754 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.748 | react.dev/blog/2021/06/08/the-plan-for-react-18 | 0.746 |


**Q7: How do you specify the title of the document using the `<title>` component?**
*(expects URL containing: `title`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/passing-data-deeply-with-context | 0.672 | react.dev/learn/passing-data-deeply-with-context | 0.665 | react.dev/learn/passing-data-deeply-with-context | 0.660 |
| crawl4ai | #1 | react.dev/reference/react-dom/components/title | 0.747 | react.dev/reference/react-dom/components/title | 0.733 | react.dev/reference/react-dom/components/meta | 0.709 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/components/title | 0.747 | react.dev/reference/react-dom/components/title | 0.733 | react.dev/reference/react-dom/components/meta | 0.709 |
| scrapy+md | #1 | react.dev/reference/react-dom/components/title | 0.815 | react.dev/reference/react-dom/components/title | 0.795 | react.dev/reference/react-dom/components/meta | 0.698 |
| crawlee | #1 | react.dev/reference/react-dom/components/title | 0.795 | react.dev/reference/react-dom/components/title | 0.739 | react.dev/reference/react/act | 0.721 |
| colly+md | #1 | react.dev/reference/react-dom/components/title | 0.795 | react.dev/reference/react-dom/components/title | 0.739 | react.dev/reference/react/act | 0.721 |
| playwright | #1 | react.dev/reference/react-dom/components/title | 0.795 | react.dev/reference/react-dom/components/title | 0.739 | react.dev/reference/react/act | 0.721 |


**Q8: What special rendering behavior does React have for the `<title>` component?**
*(expects URL containing: `title`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/understanding-your-ui-as-a-tree | 0.732 | react.dev/learn/render-and-commit | 0.731 | react.dev/learn/passing-data-deeply-with-context | 0.731 |
| crawl4ai | #1 | react.dev/reference/react-dom/components/title | 0.860 | react.dev/reference/react-dom/components/title | 0.815 | react.dev/reference/react-dom/components | 0.771 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/components/title | 0.860 | react.dev/reference/react-dom/components/title | 0.815 | react.dev/reference/react-dom/components | 0.771 |
| scrapy+md | #1 | react.dev/reference/react-dom/components/title | 0.864 | react.dev/reference/react-dom/components/title | 0.826 | react.dev/reference/react-dom/components | 0.754 |
| crawlee | #1 | react.dev/reference/react-dom/components/title | 0.864 | react.dev/reference/react-dom/components/title | 0.799 | react.dev/reference/react/ViewTransition | 0.771 |
| colly+md | #1 | react.dev/reference/react-dom/components/title | 0.864 | react.dev/reference/react-dom/components/title | 0.799 | react.dev/reference/react/ViewTransition | 0.771 |
| playwright | #1 | react.dev/reference/react-dom/components/title | 0.864 | react.dev/reference/react-dom/components/title | 0.799 | react.dev/reference/react/ViewTransition | 0.771 |


**Q9: What are Server Functions used for in React?**
*(expects URL containing: `server-functions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/reusing-logic-with-custom-hooks | 0.737 | react.dev/learn/you-might-not-need-an-effect | 0.736 | react.dev/learn/extracting-state-logic-into-a-redu | 0.732 |
| crawl4ai | #2 | react.dev/reference/rsc/server-actions | 0.853 | react.dev/reference/rsc/server-functions | 0.853 | react.dev/reference/rsc/server-actions | 0.834 |
| crawl4ai-raw | #2 | react.dev/reference/rsc/server-actions | 0.853 | react.dev/reference/rsc/server-functions | 0.853 | react.dev/reference/rsc/server-actions | 0.834 |
| scrapy+md | #1 | react.dev/reference/rsc/server-functions | 0.889 | react.dev/reference/rsc/server-functions | 0.832 | react.dev/reference/rsc/use-server | 0.829 |
| crawlee | #2 | react.dev/reference/rsc/server-actions | 0.851 | react.dev/reference/rsc/server-functions | 0.851 | react.dev/reference/rsc/server-actions | 0.832 |
| colly+md | #1 | react.dev/reference/rsc/server-functions | 0.851 | react.dev/reference/rsc/server-functions | 0.832 | react.dev/reference/rsc/use-server | 0.821 |
| playwright | #2 | react.dev/reference/rsc/server-actions | 0.851 | react.dev/reference/rsc/server-functions | 0.851 | react.dev/reference/rsc/server-actions | 0.832 |


**Q10: How do you create a Server Function from a Server Component?**
*(expects URL containing: `server-functions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/reusing-logic-with-custom-hooks | 0.710 | react.dev/learn/reusing-logic-with-custom-hooks | 0.697 | react.dev/learn/removing-effect-dependencies | 0.694 |
| crawl4ai | #1 | react.dev/reference/rsc/server-functions | 0.843 | react.dev/reference/rsc/server-actions | 0.843 | react.dev/reference/rsc/use-server | 0.796 |
| crawl4ai-raw | #1 | react.dev/reference/rsc/server-functions | 0.843 | react.dev/reference/rsc/server-actions | 0.843 | react.dev/reference/rsc/use-server | 0.796 |
| scrapy+md | #1 | react.dev/reference/rsc/server-functions | 0.824 | react.dev/reference/rsc/server-functions | 0.816 | react.dev/blog/2024/12/05/react-19 | 0.781 |
| crawlee | #1 | react.dev/reference/rsc/server-functions | 0.826 | react.dev/reference/rsc/server-actions | 0.826 | react.dev/reference/rsc/server-actions | 0.824 |
| colly+md | #1 | react.dev/reference/rsc/server-functions | 0.826 | react.dev/reference/rsc/server-functions | 0.824 | react.dev/reference/rsc/server-functions | 0.788 |
| playwright | #1 | react.dev/reference/rsc/server-functions | 0.826 | react.dev/reference/rsc/server-actions | 0.826 | react.dev/reference/rsc/server-actions | 0.824 |


**Q11: What is the new domain for the React documentation site?**
*(expects URL containing: `introducing-react-dev`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn | 0.705 | react.dev/learn/your-first-component | 0.684 | react.dev/learn/writing-markup-with-jsx | 0.667 |
| crawl4ai | #1 | react.dev/blog/2023/03/16/introducing-react-dev | 0.795 | he.react.dev/blog/2023/03/16/introducing-react-dev | 0.770 | 18.react.dev/community/docs-contributors | 0.762 |
| crawl4ai-raw | #1 | react.dev/blog/2023/03/16/introducing-react-dev | 0.795 | he.react.dev/blog/2023/03/16/introducing-react-dev | 0.770 | 18.react.dev/community/docs-contributors | 0.762 |
| scrapy+md | #1 | react.dev/blog/2023/03/16/introducing-react-dev | 0.795 | react.dev/blog/2023/03/16/introducing-react-dev | 0.766 | react.dev/community/docs-contributors | 0.749 |
| crawlee | #1 | react.dev/blog/2023/03/16/introducing-react-dev | 0.795 | react.dev/blog/2023/03/16/introducing-react-dev | 0.767 | react.dev/blog/2023/03/16/introducing-react-dev | 0.766 |
| colly+md | #1 | react.dev/blog/2023/03/16/introducing-react-dev | 0.795 | react.dev/blog/2023/03/16/introducing-react-dev | 0.767 | react.dev/blog/2023/03/16/introducing-react-dev | 0.766 |
| playwright | #1 | react.dev/blog/2023/03/16/introducing-react-dev | 0.795 | react.dev/blog/2023/03/16/introducing-react-dev | 0.767 | react.dev/blog/2023/03/16/introducing-react-dev | 0.766 |


**Q12: How does the new documentation teach React differently than the previous version?**
*(expects URL containing: `introducing-react-dev`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn | 0.761 | react.dev/learn/render-and-commit | 0.750 | react.dev/learn/describing-the-ui | 0.738 |
| crawl4ai | #1 | he.react.dev/blog/2023/03/16/introducing-react-dev | 0.806 | react.dev/versions | 0.803 | 18.react.dev/versions | 0.803 |
| crawl4ai-raw | #1 | he.react.dev/blog/2023/03/16/introducing-react-dev | 0.806 | react.dev/versions | 0.803 | 18.react.dev/versions | 0.803 |
| scrapy+md | #1 | react.dev/blog/2023/03/16/introducing-react-dev | 0.811 | react.dev/blog/2021/12/17/react-conf-2021-recap | 0.797 | react.dev/blog/2023/03/16/introducing-react-dev | 0.790 |
| crawlee | #2 | react.dev/blog/2021/12/17/react-conf-2021-recap | 0.797 | react.dev/blog/2023/03/16/introducing-react-dev | 0.790 | react.dev/blog/2023/03/16/introducing-react-dev | 0.789 |
| colly+md | #2 | react.dev/blog/2021/12/17/react-conf-2021-recap | 0.797 | react.dev/blog/2023/03/16/introducing-react-dev | 0.790 | react.dev/blog/2023/03/16/introducing-react-dev | 0.790 |
| playwright | #2 | react.dev/blog/2021/12/17/react-conf-2021-recap | 0.797 | react.dev/blog/2023/03/16/introducing-react-dev | 0.790 | react.dev/blog/2023/03/16/introducing-react-dev | 0.790 |


**Q13: What does the `startTransition` function do?**
*(expects URL containing: `startTransition`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/tutorial-tic-tac-toe | 0.652 | react.dev/learn/tutorial-tic-tac-toe | 0.631 | react.dev/learn/updating-arrays-in-state | 0.616 |
| crawl4ai | #4 | react.dev/reference/react/useTransition | 0.704 | react.dev/reference/react/useTransition | 0.698 | react.dev/reference/react/useTransition | 0.688 |
| crawl4ai-raw | #4 | react.dev/reference/react/useTransition | 0.704 | react.dev/reference/react/useTransition | 0.698 | react.dev/reference/react/useTransition | 0.688 |
| scrapy+md | #1 | react.dev/reference/react/startTransition | 0.752 | react.dev/reference/react/useTransition | 0.741 | react.dev/reference/react/useTransition | 0.710 |
| crawlee | #9 | react.dev/reference/react/useTransition | 0.730 | react.dev/reference/react/useTransition | 0.725 | react.dev/blog/2025/04/23/react-labs-view-transiti | 0.723 |
| colly+md | #9 | react.dev/reference/react/useTransition | 0.730 | react.dev/reference/react/useTransition | 0.725 | react.dev/blog/2025/04/23/react-labs-view-transiti | 0.723 |
| playwright | #9 | react.dev/reference/react/useTransition | 0.730 | react.dev/reference/react/useTransition | 0.725 | react.dev/blog/2025/04/23/react-labs-view-transiti | 0.723 |


**Q14: How do you mark a state update as a Transition in React?**
*(expects URL containing: `startTransition`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/you-might-not-need-an-effect | 0.760 | react.dev/learn/preserving-and-resetting-state | 0.740 | react.dev/learn/preserving-and-resetting-state | 0.732 |
| crawl4ai | #1 | react.dev/reference/react/startTransition | 0.853 | react.dev/reference/react/useTransition | 0.842 | react.dev/reference/react/useTransition | 0.824 |
| crawl4ai-raw | #1 | react.dev/reference/react/startTransition | 0.853 | react.dev/reference/react/useTransition | 0.842 | react.dev/reference/react/useTransition | 0.824 |
| scrapy+md | #1 | react.dev/reference/react/startTransition | 0.853 | react.dev/reference/react/useTransition | 0.845 | react.dev/reference/react/useTransition | 0.830 |
| crawlee | #1 | react.dev/reference/react/startTransition | 0.864 | react.dev/reference/react/useTransition | 0.845 | react.dev/reference/react/useTransition | 0.830 |
| colly+md | #1 | react.dev/reference/react/startTransition | 0.864 | react.dev/reference/react/useTransition | 0.845 | react.dev/reference/react/useTransition | 0.830 |
| playwright | #1 | react.dev/reference/react/startTransition | 0.864 | react.dev/reference/react/useTransition | 0.845 | react.dev/reference/react/useTransition | 0.830 |


**Q15: What are the characteristics of a pure component or hook in React?**
*(expects URL containing: `components-and-hooks-must-be-pure`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/keeping-components-pure | 0.785 | react.dev/learn/describing-the-ui | 0.761 | react.dev/learn/reusing-logic-with-custom-hooks | 0.751 |
| crawl4ai | #2 | react.dev/reference/rules | 0.814 | react.dev/reference/rules/components-and-hooks-mus | 0.792 | reference/react/Component | 0.777 |
| crawl4ai-raw | #2 | react.dev/reference/rules | 0.814 | react.dev/reference/rules/components-and-hooks-mus | 0.792 | reference/react/Component | 0.777 |
| scrapy+md | #1 | react.dev/reference/rules/components-and-hooks-mus | 0.841 | react.dev/reference/rules/react-calls-components-a | 0.776 | react.dev/reference/rules | 0.774 |
| crawlee | #1 | react.dev/reference/rules/components-and-hooks-mus | 0.805 | react.dev/reference/rules | 0.801 | react.dev/reference/rules | 0.790 |
| colly+md | #1 | react.dev/reference/rules/components-and-hooks-mus | 0.805 | react.dev/reference/rules | 0.801 | react.dev/reference/rules | 0.790 |
| playwright | #1 | react.dev/reference/rules/components-and-hooks-mus | 0.805 | react.dev/reference/rules | 0.801 | react.dev/reference/rules | 0.790 |


**Q16: Why should side effects run outside of render in React components?**
*(expects URL containing: `components-and-hooks-must-be-pure`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/keeping-components-pure | 0.800 | react.dev/learn/synchronizing-with-effects | 0.790 | react.dev/learn/synchronizing-with-effects | 0.788 |
| crawl4ai | #1 | react.dev/reference/rules/components-and-hooks-mus | 0.819 | react.dev/reference/rules/components-and-hooks-mus | 0.781 | react.dev/learn/synchronizing-with-effects | 0.775 |
| crawl4ai-raw | #1 | react.dev/reference/rules/components-and-hooks-mus | 0.819 | react.dev/reference/rules/components-and-hooks-mus | 0.781 | react.dev/learn/synchronizing-with-effects | 0.775 |
| scrapy+md | #1 | react.dev/reference/rules/components-and-hooks-mus | 0.824 | react.dev/learn/synchronizing-with-effects | 0.790 | react.dev/learn/synchronizing-with-effects | 0.790 |
| crawlee | #1 | react.dev/reference/rules/components-and-hooks-mus | 0.824 | react.dev/learn/synchronizing-with-effects | 0.790 | react.dev/learn/synchronizing-with-effects | 0.790 |
| colly+md | #1 | react.dev/reference/rules/components-and-hooks-mus | 0.824 | react.dev/learn/synchronizing-with-effects#step-2- | 0.790 | react.dev/learn/synchronizing-with-effects#how-to- | 0.790 |
| playwright | #1 | react.dev/reference/rules/components-and-hooks-mus | 0.824 | react.dev/learn/synchronizing-with-effects | 0.790 | react.dev/learn/synchronizing-with-effects | 0.790 |


**Q17: What does `prerenderToNodeStream` return upon successful rendering?**
*(expects URL containing: `prerenderToNodeStream`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/understanding-your-ui-as-a-tree | 0.674 | react.dev/learn/render-and-commit | 0.666 | react.dev/learn/render-and-commit | 0.658 |
| crawl4ai | #1 | react.dev/reference/react-dom/static/prerenderToNo | 0.758 | react.dev/reference/react-dom/server/renderToStrin | 0.736 | react.dev/reference/react-dom/static/prerender | 0.735 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/static/prerenderToNo | 0.758 | react.dev/reference/react-dom/server/renderToStrin | 0.736 | react.dev/reference/react-dom/static/prerender | 0.735 |
| scrapy+md | #1 | react.dev/reference/react-dom/static/prerenderToNo | 0.764 | react.dev/reference/react-dom/static/resumeAndPrer | 0.756 | react.dev/reference/react-dom/static/prerenderToNo | 0.752 |
| crawlee | #1 | react.dev/reference/react-dom/static/prerenderToNo | 0.764 | react.dev/reference/react-dom/static/resumeAndPrer | 0.756 | react.dev/reference/react-dom/server/renderToStrin | 0.751 |
| colly+md | #1 | react.dev/reference/react-dom/static/prerenderToNo | 0.764 | react.dev/reference/react-dom/static/resumeAndPrer | 0.756 | react.dev/reference/react-dom/server/renderToStrin | 0.751 |
| playwright | #1 | react.dev/reference/react-dom/static/prerenderToNo | 0.764 | react.dev/reference/react-dom/static/resumeAndPrer | 0.756 | react.dev/reference/react-dom/server/renderToStrin | 0.751 |


**Q18: When should I use `prerenderToNodeStream` instead of `renderToString`?**
*(expects URL containing: `prerenderToNodeStream`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/understanding-your-ui-as-a-tree | 0.668 | react.dev/learn/passing-data-deeply-with-context | 0.650 | react.dev/learn/render-and-commit | 0.649 |
| crawl4ai | #2 | react.dev/reference/react-dom/server/renderToStrin | 0.796 | react.dev/reference/react-dom/static/prerenderToNo | 0.746 | react.dev/reference/react-dom/server/renderToStrin | 0.741 |
| crawl4ai-raw | #2 | react.dev/reference/react-dom/server/renderToStrin | 0.796 | react.dev/reference/react-dom/static/prerenderToNo | 0.746 | react.dev/reference/react-dom/server/renderToStrin | 0.741 |
| scrapy+md | #3 | react.dev/reference/react-dom/server/renderToStrin | 0.804 | react.dev/reference/react-dom/server/renderToStrin | 0.770 | react.dev/reference/react-dom/static/prerenderToNo | 0.745 |
| crawlee | #6 | react.dev/reference/react-dom/server/renderToStrin | 0.814 | react.dev/reference/react-dom/server/renderToStrin | 0.786 | react.dev/reference/react-dom/server/renderToStrin | 0.784 |
| colly+md | #6 | react.dev/reference/react-dom/server/renderToStrin | 0.814 | react.dev/reference/react-dom/server/renderToStrin | 0.786 | react.dev/reference/react-dom/server/renderToStrin | 0.784 |
| playwright | #6 | react.dev/reference/react-dom/server/renderToStrin | 0.814 | react.dev/reference/react-dom/server/renderToStrin | 0.786 | react.dev/reference/react-dom/server/renderToStrin | 0.784 |


**Q19: What are the built-in React DOM Hooks?**
*(expects URL containing: `hooks`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/reusing-logic-with-custom-hooks | 0.802 | react.dev/learn/manipulating-the-dom-with-refs | 0.751 | react.dev/learn/reusing-logic-with-custom-hooks | 0.743 |
| crawl4ai | #1 | react.dev/learn/reusing-logic-with-custom-hooks | 0.810 | react.dev/reference/react-dom/components/option | 0.786 | react.dev/reference/react-dom/components | 0.782 |
| crawl4ai-raw | #1 | react.dev/learn/reusing-logic-with-custom-hooks | 0.810 | react.dev/reference/react-dom/components/option | 0.786 | react.dev/reference/react-dom/components | 0.782 |
| scrapy+md | #1 | react.dev/reference/react/hooks | 0.824 | react.dev/reference/react-dom/hooks | 0.799 | react.dev/learn/reusing-logic-with-custom-hooks | 0.791 |
| crawlee | #1 | react.dev/reference/react-dom/hooks | 0.824 | react.dev/learn/reusing-logic-with-custom-hooks | 0.810 | react.dev/reference/react/hooks | 0.796 |
| colly+md | #1 | react.dev/reference/react-dom/hooks | 0.824 | react.dev/reference/react/hooks | 0.796 | react.dev/reference/react-dom/hooks | 0.792 |
| playwright | #1 | react.dev/reference/react-dom/hooks | 0.824 | react.dev/reference/react/hooks | 0.796 | react.dev/reference/react-dom/hooks | 0.792 |


**Q20: What does the useFormStatus hook do?**
*(expects URL containing: `hooks`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/reusing-logic-with-custom-hooks | 0.706 | react.dev/learn/reusing-logic-with-custom-hooks | 0.686 | react.dev/learn/reusing-logic-with-custom-hooks | 0.668 |
| crawl4ai | #1 | react.dev/reference/react-dom/hooks/useFormStatus | 0.801 | react.dev/reference/react-dom/hooks/useFormStatus | 0.783 | react.dev/reference/react-dom/hooks/useFormStatus | 0.776 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/hooks/useFormStatus | 0.801 | react.dev/reference/react-dom/hooks/useFormStatus | 0.783 | react.dev/reference/react-dom/hooks/useFormStatus | 0.776 |
| scrapy+md | #1 | react.dev/reference/react-dom/hooks/useFormStatus | 0.856 | react.dev/reference/react-dom/hooks/useFormStatus | 0.833 | react.dev/reference/react-dom/hooks/useFormStatus | 0.772 |
| crawlee | #1 | react.dev/reference/react-dom/hooks/useFormStatus | 0.835 | react.dev/reference/react-dom/hooks/useFormStatus | 0.807 | react.dev/reference/react-dom/components/form | 0.771 |
| colly+md | #1 | react.dev/reference/react-dom/hooks/useFormStatus | 0.835 | react.dev/reference/react-dom/hooks/useFormStatus | 0.807 | react.dev/reference/react-dom/components/form | 0.771 |
| playwright | #1 | react.dev/reference/react-dom/hooks/useFormStatus | 0.835 | react.dev/reference/react-dom/hooks/useFormStatus | 0.807 | react.dev/reference/react-dom/components/form | 0.771 |


**Q21: What is the purpose of useLayoutEffect?**
*(expects URL containing: `useLayoutEffect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/separating-events-from-effects | 0.696 | react.dev/learn/escape-hatches | 0.685 | react.dev/learn/separating-events-from-effects | 0.682 |
| crawl4ai | #1 | react.dev/reference/react/useLayoutEffect | 0.814 | react.dev/reference/react/useLayoutEffect | 0.788 | react.dev/reference/react/useLayoutEffect | 0.778 |
| crawl4ai-raw | #1 | react.dev/reference/react/useLayoutEffect | 0.814 | react.dev/reference/react/useLayoutEffect | 0.788 | react.dev/reference/react/useLayoutEffect | 0.778 |
| scrapy+md | #1 | react.dev/reference/react/useLayoutEffect | 0.832 | react.dev/reference/react/useLayoutEffect | 0.789 | react.dev/reference/react/useLayoutEffect | 0.780 |
| crawlee | #1 | react.dev/reference/react/useLayoutEffect | 0.790 | react.dev/reference/react/useLayoutEffect | 0.789 | react.dev/reference/react/useLayoutEffect | 0.767 |
| colly+md | #1 | react.dev/reference/react/useLayoutEffect | 0.790 | react.dev/reference/react/useLayoutEffect | 0.789 | react.dev/reference/react/useLayoutEffect | 0.767 |
| playwright | #1 | react.dev/reference/react/useLayoutEffect | 0.790 | react.dev/reference/react/useLayoutEffect | 0.789 | react.dev/reference/react/useLayoutEffect | 0.767 |


**Q22: How does useLayoutEffect differ from useEffect?**
*(expects URL containing: `useLayoutEffect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/separating-events-from-effects | 0.711 | react.dev/learn/separating-events-from-effects | 0.703 | react.dev/learn/separating-events-from-effects | 0.699 |
| crawl4ai | #1 | react.dev/reference/react/useLayoutEffect | 0.792 | react.dev/reference/react/useLayoutEffect | 0.787 | react.dev/reference/react/useLayoutEffect | 0.768 |
| crawl4ai-raw | #1 | react.dev/reference/react/useLayoutEffect | 0.792 | react.dev/reference/react/useLayoutEffect | 0.787 | react.dev/reference/react/useLayoutEffect | 0.768 |
| scrapy+md | #1 | react.dev/reference/react/useLayoutEffect | 0.816 | react.dev/reference/react/useLayoutEffect | 0.778 | react.dev/reference/react/useLayoutEffect | 0.778 |
| crawlee | #1 | react.dev/reference/react/useLayoutEffect | 0.780 | react.dev/reference/react/useLayoutEffect | 0.778 | react.dev/reference/react/useLayoutEffect | 0.778 |
| colly+md | #1 | react.dev/reference/react/useLayoutEffect | 0.780 | react.dev/reference/react/useLayoutEffect | 0.778 | react.dev/reference/react/useLayoutEffect | 0.778 |
| playwright | #1 | react.dev/reference/react/useLayoutEffect | 0.780 | react.dev/reference/react/useLayoutEffect | 0.778 | react.dev/reference/react/useLayoutEffect | 0.778 |


**Q23: How do you pass a string attribute to JSX?**
*(expects URL containing: `javascript-in-jsx-with-curly-braces`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.824 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.808 | react.dev/learn/tutorial-tic-tac-toe | 0.801 |
| crawl4ai | #2 | react.dev/learn/tutorial-tic-tac-toe | 0.795 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.788 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.787 |
| crawl4ai-raw | #2 | react.dev/learn/tutorial-tic-tac-toe | 0.795 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.788 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.787 |
| scrapy+md | #1 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.816 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.810 | react.dev/reference/react-dom/components | 0.782 |
| crawlee | #1 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.819 | react.dev/learn/describing-the-ui | 0.796 | react.dev/learn/tutorial-tic-tac-toe | 0.788 |
| colly+md | #1 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.831 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.831 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.831 |
| playwright | #1 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.831 | react.dev/learn/describing-the-ui | 0.796 | react.dev/learn/tutorial-tic-tac-toe | 0.788 |


**Q24: What is the purpose of using curly braces in JSX?**
*(expects URL containing: `javascript-in-jsx-with-curly-braces`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.814 | react.dev/learn/tutorial-tic-tac-toe | 0.799 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.799 |
| crawl4ai | #1 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.819 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.788 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.786 |
| crawl4ai-raw | #1 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.819 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.788 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.786 |
| scrapy+md | #1 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.814 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.798 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.765 |
| crawlee | #1 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.830 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.824 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.810 |
| colly+md | #1 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.826 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.826 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.826 |
| playwright | #1 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.826 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.822 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.810 |


**Q25: What does the `preconnect` function do?**
*(expects URL containing: `preconnect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/separating-events-from-effects | 0.615 | react.dev/learn/separating-events-from-effects | 0.614 | react.dev/learn/synchronizing-with-effects | 0.601 |
| crawl4ai | #1 | react.dev/reference/react-dom/preconnect | 0.706 | ko.react.dev/learn/escape-hatches | 0.655 | react.dev/reference/react-dom/prefetchDNS | 0.654 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/preconnect | 0.706 | ko.react.dev/learn/escape-hatches | 0.655 | react.dev/reference/react-dom/prefetchDNS | 0.654 |
| scrapy+md | #1 | react.dev/reference/react-dom/preconnect | 0.774 | react.dev/reference/react-dom/preconnect | 0.717 | react.dev/reference/react-dom/prefetchDNS | 0.669 |
| crawlee | #1 | react.dev/reference/react-dom/preconnect | 0.717 | react.dev/reference/react-dom/preconnect | 0.669 | react.dev/reference/react-dom/preconnect | 0.669 |
| colly+md | #1 | react.dev/reference/react-dom/preconnect | 0.717 | react.dev/reference/react-dom/preconnect | 0.669 | react.dev/reference/react-dom/preconnect | 0.669 |
| playwright | #1 | react.dev/reference/react-dom/preconnect | 0.717 | react.dev/reference/react-dom/preconnect | 0.669 | react.dev/reference/react-dom/preconnect | 0.669 |


**Q26: How can you call `preconnect` in an event handler?**
*(expects URL containing: `preconnect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/separating-events-from-effects | 0.699 | react.dev/learn/reusing-logic-with-custom-hooks | 0.677 | react.dev/learn/separating-events-from-effects | 0.665 |
| crawl4ai | #1 | react.dev/reference/react-dom/preconnect | 0.737 | react.dev/learn/separating-events-from-effects | 0.684 | react.dev/reference/react-dom/prefetchDNS | 0.672 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/preconnect | 0.737 | react.dev/learn/separating-events-from-effects | 0.684 | react.dev/reference/react-dom/prefetchDNS | 0.672 |
| scrapy+md | #1 | react.dev/reference/react-dom/preconnect | 0.783 | react.dev/reference/react-dom/preconnect | 0.754 | react.dev/learn/separating-events-from-effects | 0.699 |
| crawlee | #1 | react.dev/reference/react-dom/preconnect | 0.754 | react.dev/learn/escape-hatches | 0.709 | react.dev/learn/separating-events-from-effects | 0.699 |
| colly+md | #1 | react.dev/reference/react-dom/preconnect | 0.754 | react.dev/learn/escape-hatches | 0.709 | react.dev/learn/separating-events-from-effects | 0.699 |
| playwright | #1 | react.dev/reference/react-dom/preconnect | 0.754 | react.dev/learn/escape-hatches | 0.709 | react.dev/learn/separating-events-from-effects | 0.699 |


**Q27: What does `renderToReadableStream` do in React?**
*(expects URL containing: `renderToReadableStream`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/state-as-a-snapshot | 0.715 | react.dev/learn/state-a-components-memory | 0.706 | react.dev/learn/render-and-commit | 0.705 |
| crawl4ai | #4 | react.dev/reference/react/useSyncExternalStore | 0.761 | react.dev/reference/react/useSyncExternalStore | 0.761 | react.dev/reference/react-dom/server/resumeToPipea | 0.759 |
| crawl4ai-raw | #4 | react.dev/reference/react/useSyncExternalStore | 0.761 | react.dev/reference/react/useSyncExternalStore | 0.761 | react.dev/reference/react-dom/server/resumeToPipea | 0.759 |
| scrapy+md | #2 | react.dev/reference/react-dom/server/resume | 0.785 | react.dev/reference/react-dom/server/renderToReada | 0.777 | react.dev/reference/react/useSyncExternalStore | 0.758 |
| crawlee | #3 | react.dev/reference/react-dom/server/resume | 0.764 | react.dev/reference/react/useSyncExternalStore | 0.758 | react.dev/reference/react-dom/server/renderToReada | 0.756 |
| colly+md | #3 | react.dev/reference/react-dom/server/resume | 0.764 | react.dev/reference/react/useSyncExternalStore | 0.758 | react.dev/reference/react-dom/server/renderToReada | 0.756 |
| playwright | #3 | react.dev/reference/react-dom/server/resume | 0.764 | react.dev/reference/react/useSyncExternalStore | 0.758 | react.dev/reference/react-dom/server/renderToReada | 0.756 |


**Q28: What parameters can be passed to the `renderToReadableStream` function?**
*(expects URL containing: `renderToReadableStream`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/extracting-state-logic-into-a-redu | 0.661 | react.dev/learn/extracting-state-logic-into-a-redu | 0.656 | react.dev/learn/updating-arrays-in-state | 0.653 |
| crawl4ai | #12 | react.dev/reference/react/useSyncExternalStore | 0.727 | react.dev/reference/react-dom/server/renderToStrin | 0.727 | react.dev/reference/react-dom/server/resumeToPipea | 0.726 |
| crawl4ai-raw | #12 | react.dev/reference/react/useSyncExternalStore | 0.727 | react.dev/reference/react-dom/server/renderToStrin | 0.727 | react.dev/reference/react-dom/server/resumeToPipea | 0.726 |
| scrapy+md | #1 | react.dev/reference/react-dom/server/renderToReada | 0.731 | react.dev/reference/react-dom/server/resume | 0.730 | react.dev/reference/react-dom/server/renderToPipea | 0.712 |
| crawlee | #1 | react.dev/reference/react-dom/server/renderToReada | 0.755 | react.dev/reference/react-dom/server/renderToPipea | 0.737 | react.dev/reference/react-dom/server/renderToStrin | 0.735 |
| colly+md | #1 | react.dev/reference/react-dom/server/renderToReada | 0.755 | react.dev/reference/react-dom/server/renderToPipea | 0.737 | react.dev/reference/react-dom/server/renderToStrin | 0.735 |
| playwright | #1 | react.dev/reference/react-dom/server/renderToReada | 0.755 | react.dev/reference/react-dom/server/renderToPipea | 0.737 | react.dev/reference/react-dom/server/renderToStrin | 0.735 |


**Q29: What is the recommended way to start building a new app or website with React?**
*(expects URL containing: `creating-a-react-app`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | react.dev/learn/installation | 0.848 | react.dev/learn/creating-a-react-app | 0.832 | react.dev/learn/add-react-to-an-existing-project | 0.827 |
| crawl4ai | #8 | 18.react.dev/learn/installation | 0.837 | tr.react.dev/learn/installation | 0.834 | he.react.dev/learn/installation | 0.833 |
| crawl4ai-raw | #8 | 18.react.dev/learn/installation | 0.837 | tr.react.dev/learn/installation | 0.834 | he.react.dev/learn/installation | 0.833 |
| scrapy+md | #2 | react.dev/learn/installation | 0.845 | react.dev/learn/creating-a-react-app | 0.833 | react.dev/learn/build-a-react-app-from-scratch | 0.828 |
| crawlee | #9 | react.dev/learn/build-a-react-app-from-scratch | 0.829 | react.dev/learn/installation | 0.828 | react.dev/learn/installation | 0.824 |
| colly+md | #13 | react.dev/learn/installation#try-react | 0.832 | react.dev/learn/installation | 0.832 | react.dev/learn/build-a-react-app-from-scratch#con | 0.829 |
| playwright | #8 | react.dev/learn/installation | 0.832 | react.dev/learn/build-a-react-app-from-scratch | 0.829 | react.dev/learn/installation | 0.824 |


**Q30: What command is used to create a new Expo project?**
*(expects URL containing: `creating-a-react-app`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/creating-a-react-app | 0.678 | react.dev/learn/importing-and-exporting-components | 0.634 | react.dev/learn/creating-a-react-app | 0.617 |
| crawl4ai | #1 | tr.react.dev/learn/creating-a-react-app | 0.691 | ko.react.dev/learn/creating-a-react-app | 0.675 | zh-hans.react.dev/learn/creating-a-react-app | 0.674 |
| crawl4ai-raw | #1 | tr.react.dev/learn/creating-a-react-app | 0.691 | ko.react.dev/learn/creating-a-react-app | 0.675 | zh-hans.react.dev/learn/creating-a-react-app | 0.674 |
| scrapy+md | #1 | react.dev/learn/creating-a-react-app | 0.639 | react.dev/blog/2025/02/14/sunsetting-create-react- | 0.635 | react.dev/learn/importing-and-exporting-components | 0.633 |
| crawlee | #1 | react.dev/learn/creating-a-react-app | 0.678 | react.dev/learn/creating-a-react-app | 0.666 | react.dev/learn/installation | 0.643 |
| colly+md | #1 | react.dev/learn/creating-a-react-app | 0.678 | react.dev/learn/creating-a-react-app#full-stack-fr | 0.678 | react.dev/learn/creating-a-react-app | 0.666 |
| playwright | #1 | react.dev/learn/creating-a-react-app | 0.678 | react.dev/learn/creating-a-react-app | 0.666 | react.dev/learn/importing-and-exporting-components | 0.647 |


**Q31: What is the purpose of the `useDebugValue` hook?**
*(expects URL containing: `useDebugValue`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/typescript | 0.704 | react.dev/learn/escape-hatches | 0.690 | react.dev/learn/reusing-logic-with-custom-hooks | 0.685 |
| crawl4ai | #1 | react.dev/reference/react/useDebugValue | 0.755 | az.react.dev/blog/2024/04/25/react-19 | 0.709 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.706 |
| crawl4ai-raw | #1 | react.dev/reference/react/useDebugValue | 0.755 | az.react.dev/blog/2024/04/25/react-19 | 0.709 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.706 |
| scrapy+md | #1 | react.dev/reference/react/useDebugValue | 0.790 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.747 | react.dev/reference/react/useDeferredValue | 0.734 |
| crawlee | #1 | react.dev/reference/react/useDebugValue | 0.763 | react.dev/reference/react/useDebugValue | 0.755 | react.dev/reference/react/useDebugValue | 0.746 |
| colly+md | #1 | react.dev/reference/react/useDebugValue | 0.763 | react.dev/reference/react/useDebugValue | 0.755 | react.dev/reference/react/useDebugValue | 0.746 |
| playwright | #1 | react.dev/reference/react/useDebugValue | 0.763 | react.dev/reference/react/useDebugValue | 0.755 | react.dev/reference/react/useDebugValue | 0.746 |


**Q32: How do you use the optional formatting function with `useDebugValue`?**
*(expects URL containing: `useDebugValue`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/conditional-rendering | 0.675 | react.dev/learn/conditional-rendering | 0.660 | react.dev/learn/conditional-rendering | 0.633 |
| crawl4ai | #1 | react.dev/reference/react/useDebugValue | 0.720 | react.dev/learn/conditional-rendering | 0.663 | az.react.dev/blog/2024/04/25/react-19 | 0.662 |
| crawl4ai-raw | #1 | react.dev/reference/react/useDebugValue | 0.720 | react.dev/learn/conditional-rendering | 0.663 | az.react.dev/blog/2024/04/25/react-19 | 0.662 |
| scrapy+md | #1 | react.dev/reference/react/useDebugValue | 0.721 | react.dev/learn/conditional-rendering | 0.675 | react.dev/reference/react/useDebugValue | 0.662 |
| crawlee | #1 | react.dev/reference/react/useDebugValue | 0.759 | react.dev/reference/react/useDebugValue | 0.715 | react.dev/reference/react/Component | 0.708 |
| colly+md | #1 | react.dev/reference/react/useDebugValue | 0.759 | react.dev/reference/react/useDebugValue | 0.715 | react.dev/reference/react/Component | 0.708 |
| playwright | #1 | react.dev/reference/react/useDebugValue | 0.759 | react.dev/reference/react/useDebugValue | 0.715 | react.dev/reference/react/Component | 0.708 |


**Q33: What does createContext return?**
*(expects URL containing: `createContext`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/typescript | 0.650 | react.dev/learn/passing-data-deeply-with-context | 0.648 | react.dev/learn/passing-data-deeply-with-context | 0.642 |
| crawl4ai | #2 | react.dev/reference/react/useContext | 0.677 | react.dev/reference/react/createContext | 0.675 | de.react.dev/blog/2024/12/05/react-19 | 0.650 |
| crawl4ai-raw | #2 | react.dev/reference/react/useContext | 0.677 | react.dev/reference/react/createContext | 0.675 | de.react.dev/blog/2024/12/05/react-19 | 0.650 |
| scrapy+md | #1 | react.dev/reference/react/createContext | 0.713 | react.dev/reference/react/useContext | 0.688 | react.dev/blog/2024/12/05/react-19 | 0.659 |
| crawlee | #2 | react.dev/reference/react/useContext | 0.704 | react.dev/reference/react/createContext | 0.695 | react.dev/reference/react/createContext | 0.678 |
| colly+md | #2 | react.dev/reference/react/useContext | 0.704 | react.dev/reference/react/createContext | 0.695 | react.dev/reference/react/createContext | 0.678 |
| playwright | #2 | react.dev/reference/react/useContext | 0.704 | react.dev/reference/react/createContext | 0.695 | react.dev/reference/react/createContext | 0.678 |


**Q34: How do you specify the value of a context in a provider?**
*(expects URL containing: `createContext`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/passing-data-deeply-with-context | 0.698 | react.dev/learn/typescript | 0.697 | react.dev/learn/passing-data-deeply-with-context | 0.652 |
| crawl4ai | #1 | react.dev/reference/react/createContext | 0.761 | react.dev/reference/react/useContext | 0.738 | react.dev/reference/react/useContext | 0.726 |
| crawl4ai-raw | #1 | react.dev/reference/react/createContext | 0.761 | react.dev/reference/react/useContext | 0.738 | react.dev/reference/react/useContext | 0.726 |
| scrapy+md | #1 | react.dev/reference/react/createContext | 0.764 | react.dev/reference/react/createContext | 0.738 | react.dev/reference/react/useContext | 0.735 |
| crawlee | #1 | react.dev/reference/react/createContext | 0.784 | react.dev/reference/react/createContext | 0.770 | react.dev/reference/react/useContext | 0.727 |
| colly+md | #1 | react.dev/reference/react/createContext | 0.784 | react.dev/reference/react/createContext | 0.770 | react.dev/reference/react/useContext | 0.727 |
| playwright | #1 | react.dev/reference/react/createContext | 0.784 | react.dev/reference/react/createContext | 0.770 | react.dev/reference/react/useContext | 0.727 |


**Q35: What does the `compilationMode` option control in the React Compiler?**
*(expects URL containing: `compilationMode`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/react-compiler/incremental-adoptio | 0.809 | react.dev/learn/react-compiler/introduction | 0.766 | react.dev/learn/react-compiler/installation | 0.765 |
| crawl4ai | #1 | react.dev/reference/react-compiler/compilationMode | 0.835 | react.dev/reference/react-compiler/configuration | 0.828 | react.dev/reference/react-compiler/compilationMode | 0.809 |
| crawl4ai-raw | #1 | react.dev/reference/react-compiler/compilationMode | 0.835 | react.dev/reference/react-compiler/configuration | 0.828 | react.dev/reference/react-compiler/compilationMode | 0.809 |
| scrapy+md | #1 | react.dev/reference/react-compiler/compilationMode | 0.859 | react.dev/reference/react-compiler/configuration | 0.829 | react.dev/learn/react-compiler/incremental-adoptio | 0.809 |
| crawlee | #1 | react.dev/reference/react-compiler/compilationMode | 0.846 | react.dev/reference/react-compiler/configuration | 0.836 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.815 |
| colly+md | #1 | react.dev/reference/react-compiler/compilationMode | 0.846 | react.dev/reference/react-compiler/configuration | 0.836 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.815 |
| playwright | #1 | react.dev/reference/react-compiler/compilationMode | 0.846 | react.dev/reference/react-compiler/configuration | 0.836 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.815 |


**Q36: What are the different options available for `compilationMode`?**
*(expects URL containing: `compilationMode`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/react-compiler/incremental-adoptio | 0.712 | react.dev/learn/react-compiler/introduction | 0.677 | react.dev/learn/react-compiler/introduction | 0.639 |
| crawl4ai | #2 | react.dev/reference/react-compiler/configuration | 0.714 | react.dev/reference/react-compiler/compilationMode | 0.690 | react.dev/reference/react-compiler/directives | 0.689 |
| crawl4ai-raw | #2 | react.dev/reference/react-compiler/configuration | 0.714 | react.dev/reference/react-compiler/compilationMode | 0.690 | react.dev/reference/react-compiler/directives | 0.689 |
| scrapy+md | #1 | react.dev/reference/react-compiler/compilationMode | 0.729 | react.dev/reference/react-compiler/configuration | 0.715 | react.dev/learn/react-compiler/incremental-adoptio | 0.712 |
| crawlee | #6 | react.dev/learn/react-compiler/incremental-adoptio | 0.725 | react.dev/learn/react-compiler/incremental-adoptio | 0.708 | react.dev/reference/react-compiler/directives/use- | 0.707 |
| colly+md | #6 | react.dev/learn/react-compiler/incremental-adoptio | 0.725 | react.dev/learn/react-compiler/incremental-adoptio | 0.708 | react.dev/reference/react-compiler/directives/use- | 0.707 |
| playwright | #6 | react.dev/learn/react-compiler/incremental-adoptio | 0.725 | react.dev/learn/react-compiler/incremental-adoptio | 0.708 | react.dev/reference/react-compiler/directives/use- | 0.707 |


**Q37: What is the purpose of the `cache` function in React?**
*(expects URL containing: `cache`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/you-might-not-need-an-effect | 0.741 | react.dev/learn/you-might-not-need-an-effect | 0.730 | react.dev/learn/you-might-not-need-an-effect | 0.705 |
| crawl4ai | #1 | react.dev/reference/react/cache | 0.815 | react.dev/reference/react/cache | 0.803 | react.dev/reference/react/useCallback | 0.798 |
| crawl4ai-raw | #1 | react.dev/reference/react/cache | 0.815 | react.dev/reference/react/cache | 0.803 | react.dev/reference/react/useCallback | 0.798 |
| scrapy+md | #1 | react.dev/reference/react/cache | 0.827 | react.dev/reference/react/cache | 0.811 | react.dev/reference/react/cache | 0.804 |
| crawlee | #1 | react.dev/reference/react/cache | 0.804 | react.dev/reference/react/useCallback | 0.798 | react.dev/reference/react/useMemo | 0.796 |
| colly+md | #1 | react.dev/reference/react/cache | 0.804 | react.dev/reference/react/useCallback | 0.798 | react.dev/reference/react/useMemo | 0.796 |
| playwright | #1 | react.dev/reference/react/cache | 0.804 | react.dev/reference/react/useCallback | 0.798 | react.dev/reference/react/useMemo | 0.796 |


**Q38: How does `cache` handle errors when a memoized function throws an error?**
*(expects URL containing: `cache`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/react-compiler/introduction | 0.630 | react.dev/learn/you-might-not-need-an-effect | 0.625 | react.dev/learn/typescript | 0.619 |
| crawl4ai | #1 | react.dev/reference/react/cache | 0.729 | react.dev/reference/react/cache | 0.722 | react.dev/reference/react/cache | 0.689 |
| crawl4ai-raw | #1 | react.dev/reference/react/cache | 0.729 | react.dev/reference/react/cache | 0.722 | react.dev/reference/react/cache | 0.689 |
| scrapy+md | #1 | react.dev/reference/react/cache | 0.744 | react.dev/reference/react/cache | 0.704 | react.dev/reference/react/cache | 0.698 |
| crawlee | #1 | react.dev/reference/react/cache | 0.723 | react.dev/reference/react/cache | 0.718 | react.dev/reference/react/cache | 0.706 |
| colly+md | #1 | react.dev/reference/react/cache | 0.723 | react.dev/reference/react/cache | 0.718 | react.dev/reference/react/cache | 0.706 |
| playwright | #1 | react.dev/reference/react/cache | 0.723 | react.dev/reference/react/cache | 0.718 | react.dev/reference/react/cache | 0.706 |


**Q39: What are the differences between event handlers and Effects in React?**
*(expects URL containing: `separating-events-from-effects`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/separating-events-from-effects | 0.860 | react.dev/learn/separating-events-from-effects | 0.854 | react.dev/learn/synchronizing-with-effects | 0.844 |
| crawl4ai | #1 | react.dev/learn/separating-events-from-effects | 0.856 | react.dev/learn/synchronizing-with-effects | 0.838 | react.dev/learn/separating-events-from-effects | 0.829 |
| crawl4ai-raw | #1 | react.dev/learn/separating-events-from-effects | 0.856 | react.dev/learn/synchronizing-with-effects | 0.838 | react.dev/learn/separating-events-from-effects | 0.829 |
| scrapy+md | #1 | react.dev/learn/separating-events-from-effects | 0.860 | react.dev/learn/separating-events-from-effects | 0.853 | react.dev/learn/synchronizing-with-effects | 0.844 |
| crawlee | #1 | react.dev/learn/separating-events-from-effects | 0.860 | react.dev/learn/separating-events-from-effects | 0.850 | react.dev/learn/synchronizing-with-effects | 0.817 |
| colly+md | #1 | react.dev/learn/separating-events-from-effects#dec | 0.860 | react.dev/learn/separating-events-from-effects#rea | 0.860 | react.dev/learn/separating-events-from-effects | 0.860 |
| playwright | #1 | react.dev/learn/separating-events-from-effects | 0.860 | react.dev/learn/separating-events-from-effects | 0.850 | react.dev/learn/synchronizing-with-effects | 0.817 |


**Q40: How can you extract non-reactive logic from Effects using Effect Events?**
*(expects URL containing: `separating-events-from-effects`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/separating-events-from-effects | 0.754 | react.dev/learn/separating-events-from-effects | 0.738 | react.dev/learn/separating-events-from-effects | 0.717 |
| crawl4ai | #1 | react.dev/learn/separating-events-from-effects | 0.762 | react.dev/learn/separating-events-from-effects | 0.755 | react.dev/learn/separating-events-from-effects | 0.745 |
| crawl4ai-raw | #1 | react.dev/learn/separating-events-from-effects | 0.762 | react.dev/learn/separating-events-from-effects | 0.755 | react.dev/learn/separating-events-from-effects | 0.745 |
| scrapy+md | #1 | react.dev/learn/separating-events-from-effects | 0.759 | react.dev/learn/separating-events-from-effects | 0.754 | react.dev/learn/separating-events-from-effects | 0.738 |
| crawlee | #1 | react.dev/learn/separating-events-from-effects | 0.766 | react.dev/learn/separating-events-from-effects | 0.759 | react.dev/learn/separating-events-from-effects | 0.754 |
| colly+md | #1 | react.dev/learn/separating-events-from-effects#dec | 0.766 | react.dev/learn/separating-events-from-effects#rea | 0.766 | react.dev/learn/separating-events-from-effects | 0.766 |
| playwright | #1 | react.dev/learn/separating-events-from-effects | 0.766 | react.dev/learn/separating-events-from-effects | 0.759 | react.dev/learn/separating-events-from-effects | 0.754 |


**Q41: What are directives used for in React Server Components?**
*(expects URL containing: `directives`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn | 0.686 | react.dev/learn/typescript | 0.683 | react.dev/learn/add-react-to-an-existing-project | 0.677 |
| crawl4ai | #6 | es.react.dev/blog/2024/12/05/react-19 | 0.838 | de.react.dev/blog/2024/12/05/react-19 | 0.837 | react.dev/blog/2024/12/05/react-19 | 0.833 |
| crawl4ai-raw | #6 | es.react.dev/blog/2024/12/05/react-19 | 0.838 | de.react.dev/blog/2024/12/05/react-19 | 0.837 | react.dev/blog/2024/12/05/react-19 | 0.833 |
| scrapy+md | #1 | react.dev/reference/rsc/directives | 0.880 | react.dev/reference/rsc/use-server | 0.824 | react.dev/blog/2024/12/05/react-19 | 0.801 |
| crawlee | #3 | react.dev/blog/2024/12/05/react-19 | 0.838 | react.dev/blog/2024/04/25/react-19#ref-as-a-prop | 0.838 | react.dev/reference/rsc/directives | 0.803 |
| colly+md | #2 | react.dev/blog/2024/12/05/react-19 | 0.838 | react.dev/reference/rsc/directives | 0.803 | react.dev/blog/2024/12/05/react-19 | 0.801 |
| playwright | #3 | react.dev/blog/2024/12/05/react-19 | 0.838 | react.dev/blog/2024/04/25/react-19 | 0.838 | react.dev/reference/rsc/directives | 0.803 |


**Q42: What does the directive 'use client' do?**
*(expects URL containing: `directives`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/separating-events-from-effects | 0.594 | react.dev/learn/separating-events-from-effects | 0.593 | react.dev/learn/reusing-logic-with-custom-hooks | 0.592 |
| crawl4ai | #14 | react.dev/reference/rsc/use-client | 0.739 | react.dev/reference/rsc/use-server | 0.730 | react.dev/reference/rsc/use-client | 0.711 |
| crawl4ai-raw | #14 | react.dev/reference/rsc/use-client | 0.739 | react.dev/reference/rsc/use-server | 0.730 | react.dev/reference/rsc/use-client | 0.711 |
| scrapy+md | #5 | react.dev/reference/rsc/use-client | 0.765 | react.dev/reference/rsc/use-client | 0.750 | react.dev/reference/rsc/use-client | 0.731 |
| crawlee | #13 | react.dev/reference/rsc/use-client | 0.765 | react.dev/reference/rsc/use-client | 0.764 | react.dev/reference/rsc/use-server | 0.762 |
| colly+md | #12 | react.dev/reference/rsc/use-client | 0.765 | react.dev/reference/rsc/use-client | 0.764 | react.dev/reference/rsc/use-server | 0.762 |
| playwright | #13 | react.dev/reference/rsc/use-client | 0.765 | react.dev/reference/rsc/use-client | 0.764 | react.dev/reference/rsc/use-server | 0.762 |


**Q43: What does eslint-plugin-react-hooks help you catch?**
*(expects URL containing: `eslint-plugin-react-hooks`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/reusing-logic-with-custom-hooks | 0.725 | react.dev/learn/reusing-logic-with-custom-hooks | 0.724 | react.dev/learn/lifecycle-of-reactive-effects | 0.718 |
| crawl4ai | #1 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.801 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.785 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.777 |
| crawl4ai-raw | #1 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.801 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.785 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.777 |
| scrapy+md | #1 | react.dev/reference/eslint-plugin-react-hooks | 0.835 | react.dev/reference/rules/rules-of-hooks | 0.778 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.765 |
| crawlee | #1 | react.dev/reference/eslint-plugin-react-hooks | 0.785 | react.dev/reference/rules/rules-of-hooks | 0.779 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.771 |
| colly+md | #1 | react.dev/reference/eslint-plugin-react-hooks | 0.785 | react.dev/reference/rules/rules-of-hooks | 0.779 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.771 |
| playwright | #1 | react.dev/reference/eslint-plugin-react-hooks | 0.785 | react.dev/reference/rules/rules-of-hooks | 0.779 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.771 |


**Q44: What are the recommended rules included in eslint-plugin-react-hooks?**
*(expects URL containing: `eslint-plugin-react-hooks`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/reusing-logic-with-custom-hooks | 0.733 | react.dev/learn/reusing-logic-with-custom-hooks | 0.730 | react.dev/learn/reusing-logic-with-custom-hooks | 0.724 |
| crawl4ai | #1 | react.dev/reference/eslint-plugin-react-hooks | 0.822 | react.dev/reference/rules | 0.811 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.803 |
| crawl4ai-raw | #1 | react.dev/reference/eslint-plugin-react-hooks | 0.822 | react.dev/reference/rules | 0.811 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.803 |
| scrapy+md | #1 | react.dev/reference/eslint-plugin-react-hooks | 0.824 | react.dev/reference/eslint-plugin-react-hooks | 0.816 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.799 |
| crawlee | #1 | react.dev/reference/eslint-plugin-react-hooks | 0.833 | react.dev/reference/eslint-plugin-react-hooks | 0.816 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.815 |
| colly+md | #1 | react.dev/reference/eslint-plugin-react-hooks | 0.833 | react.dev/reference/eslint-plugin-react-hooks | 0.816 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.815 |
| playwright | #1 | react.dev/reference/eslint-plugin-react-hooks | 0.833 | react.dev/reference/eslint-plugin-react-hooks | 0.816 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.815 |


**Q45: What is the purpose of the React Compiler Beta release?**
*(expects URL containing: `react-compiler-beta-release`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/react-compiler/introduction | 0.788 | react.dev/learn/react-compiler | 0.785 | react.dev/learn/react-compiler/incremental-adoptio | 0.761 |
| crawl4ai | #1 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.844 | 18.react.dev/blog/2024/10/21/react-compiler-beta-r | 0.844 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.827 |
| crawl4ai-raw | #1 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.844 | 18.react.dev/blog/2024/10/21/react-compiler-beta-r | 0.844 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.827 |
| scrapy+md | #1 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.863 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.818 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.809 |
| crawlee | #1 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.839 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.827 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.818 |
| colly+md | #1 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.839 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.827 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.818 |
| playwright | #1 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.839 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.827 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.818 |


**Q46: How can developers install the React Compiler ESLint plugin?**
*(expects URL containing: `react-compiler-beta-release`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/react-compiler/installation | 0.810 | react.dev/learn/react-compiler/installation | 0.786 | react.dev/learn/react-compiler/incremental-adoptio | 0.775 |
| crawl4ai | #1 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.872 | 18.react.dev/blog/2024/10/21/react-compiler-beta-r | 0.872 | es.react.dev/blog/2025/04/21/react-compiler-rc | 0.809 |
| crawl4ai-raw | #1 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.872 | 18.react.dev/blog/2024/10/21/react-compiler-beta-r | 0.872 | es.react.dev/blog/2025/04/21/react-compiler-rc | 0.809 |
| scrapy+md | #1 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.870 | react.dev/blog/2025/10/07/react-compiler-1 | 0.844 | react.dev/learn/react-compiler/installation | 0.801 |
| crawlee | #1 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.870 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.868 | react.dev/blog/2025/10/07/react-compiler-1 | 0.844 |
| colly+md | #1 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.870 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.868 | react.dev/blog/2025/10/07/react-compiler-1 | 0.844 |
| playwright | #1 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.870 | react.dev/blog/2024/10/21/react-compiler-beta-rele | 0.868 | react.dev/blog/2025/10/07/react-compiler-1 | 0.844 |


**Q47: Who are some of the contributors to the React documentation?**
*(expects URL containing: `docs-contributors`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn | 0.735 | react.dev/learn/setup | 0.717 | react.dev/learn/describing-the-ui | 0.708 |
| crawl4ai | #1 | react.dev/community/docs-contributors | 0.894 | 18.react.dev/community/docs-contributors | 0.886 | ar.react.dev/community/docs-contributors | 0.883 |
| crawl4ai-raw | #1 | react.dev/community/docs-contributors | 0.894 | 18.react.dev/community/docs-contributors | 0.886 | ar.react.dev/community/docs-contributors | 0.883 |
| scrapy+md | #1 | react.dev/community/docs-contributors | 0.899 | react.dev/community/acknowledgements | 0.866 | react.dev/versions | 0.762 |
| crawlee | #1 | react.dev/community/docs-contributors | 0.813 | react.dev/community/acknowledgements | 0.808 | react.dev/community/docs-contributors | 0.800 |
| colly+md | #1 | react.dev/community/docs-contributors | 0.813 | react.dev/community/acknowledgements | 0.808 | react.dev/community/docs-contributors | 0.800 |
| playwright | #1 | react.dev/community/docs-contributors | 0.813 | react.dev/community/acknowledgements | 0.808 | react.dev/community/docs-contributors | 0.800 |


**Q48: What types of contributions did Rachel Nabors make to the React documentation?**
*(expects URL containing: `docs-contributors`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn | 0.697 | react.dev/learn/describing-the-ui | 0.681 | react.dev/learn/describing-the-ui | 0.674 |
| crawl4ai | #1 | react.dev/community/docs-contributors | 0.792 | 18.react.dev/community/docs-contributors | 0.785 | ar.react.dev/community/docs-contributors | 0.785 |
| crawl4ai-raw | #1 | react.dev/community/docs-contributors | 0.792 | 18.react.dev/community/docs-contributors | 0.785 | ar.react.dev/community/docs-contributors | 0.785 |
| scrapy+md | #1 | react.dev/community/docs-contributors | 0.819 | react.dev/community/acknowledgements | 0.761 | react.dev/blog/2023/03/16/introducing-react-dev | 0.698 |
| crawlee | #1 | react.dev/community/docs-contributors | 0.754 | react.dev/blog/2023/03/16/introducing-react-dev | 0.748 | react.dev/community/acknowledgements | 0.734 |
| colly+md | #1 | react.dev/community/docs-contributors | 0.754 | react.dev/blog/2023/03/16/introducing-react-dev | 0.748 | react.dev/community/acknowledgements | 0.734 |
| playwright | #1 | react.dev/community/docs-contributors | 0.754 | react.dev/blog/2023/03/16/introducing-react-dev | 0.748 | react.dev/community/acknowledgements | 0.734 |


**Q49: How do you make a select box controlled in React?**
*(expects URL containing: `select`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/tutorial-tic-tac-toe | 0.756 | react.dev/learn/tutorial-tic-tac-toe | 0.751 | react.dev/learn/sharing-state-between-components | 0.742 |
| crawl4ai | #1 | react.dev/reference/react-dom/components/select | 0.855 | react.dev/reference/react-dom/components/select | 0.839 | react.dev/reference/react-dom/components/select | 0.823 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/components/select | 0.855 | react.dev/reference/react-dom/components/select | 0.839 | react.dev/reference/react-dom/components/select | 0.823 |
| scrapy+md | #1 | react.dev/reference/react-dom/components/select | 0.861 | react.dev/reference/react-dom/components/select | 0.790 | react.dev/reference/react-dom/components/select | 0.783 |
| crawlee | #1 | react.dev/reference/react-dom/components/select | 0.861 | react.dev/reference/react-dom/components/option | 0.793 | react.dev/reference/react-dom/components/select | 0.790 |
| colly+md | #1 | react.dev/reference/react-dom/components/select | 0.861 | react.dev/reference/react-dom/components/option | 0.796 | react.dev/reference/react-dom/components/select | 0.790 |
| playwright | #1 | react.dev/reference/react-dom/components/select | 0.861 | react.dev/reference/react-dom/components/option | 0.796 | react.dev/reference/react-dom/components/select | 0.790 |


**Q50: What prop do you use to specify the initially selected option in a select box?**
*(expects URL containing: `select`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/you-might-not-need-an-effect | 0.687 | react.dev/learn/you-might-not-need-an-effect | 0.685 | react.dev/learn/tutorial-tic-tac-toe | 0.680 |
| crawl4ai | #1 | react.dev/reference/react-dom/components/select | 0.798 | react.dev/reference/react-dom/components/option | 0.768 | react.dev/reference/react-dom/components/select | 0.759 |
| crawl4ai-raw | #1 | react.dev/reference/react-dom/components/select | 0.798 | react.dev/reference/react-dom/components/option | 0.768 | react.dev/reference/react-dom/components/select | 0.759 |
| scrapy+md | #1 | react.dev/reference/react-dom/components/select | 0.802 | react.dev/reference/react-dom/components/select | 0.789 | react.dev/reference/react-dom/components/option | 0.778 |
| crawlee | #1 | react.dev/reference/react-dom/components/select | 0.807 | react.dev/reference/react-dom/components/select | 0.802 | react.dev/reference/react-dom/components/option | 0.801 |
| colly+md | #1 | react.dev/reference/react-dom/components/select | 0.807 | react.dev/reference/react-dom/components/option | 0.803 | react.dev/reference/react-dom/components/select | 0.802 |
| playwright | #1 | react.dev/reference/react-dom/components/select | 0.807 | react.dev/reference/react-dom/components/option | 0.803 | react.dev/reference/react-dom/components/select | 0.802 |


**Q51: What are the three steps involved in displaying a component on screen in React?**
*(expects URL containing: `render-and-commit`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/render-and-commit | 0.806 | react.dev/learn/describing-the-ui | 0.786 | react.dev/learn/your-first-component | 0.785 |
| crawl4ai | #5 | he.react.dev/learn/describing-the-ui | 0.791 | 18.react.dev/learn/describing-the-ui | 0.787 | az.react.dev/learn/describing-the-ui | 0.786 |
| crawl4ai-raw | #5 | he.react.dev/learn/describing-the-ui | 0.791 | 18.react.dev/learn/describing-the-ui | 0.787 | az.react.dev/learn/describing-the-ui | 0.786 |
| scrapy+md | #1 | react.dev/learn/render-and-commit | 0.808 | react.dev/learn/your-first-component | 0.785 | react.dev/learn/render-and-commit | 0.776 |
| crawlee | #1 | react.dev/learn/render-and-commit | 0.811 | react.dev/learn/render-and-commit | 0.787 | react.dev/learn/your-first-component | 0.785 |
| colly+md | #1 | react.dev/learn/render-and-commit#re-renders-when- | 0.811 | react.dev/learn/render-and-commit | 0.811 | react.dev/learn/render-and-commit#step-3-react-com | 0.811 |
| playwright | #1 | react.dev/learn/render-and-commit | 0.811 | react.dev/learn/describing-the-ui | 0.788 | react.dev/learn/render-and-commit | 0.787 |


**Q52: What triggers a re-render of a component in React?**
*(expects URL containing: `render-and-commit`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/render-and-commit | 0.802 | react.dev/learn/render-and-commit | 0.796 | react.dev/learn/preserving-and-resetting-state | 0.790 |
| crawl4ai | #1 | react.dev/learn/render-and-commit | 0.811 | reference/react/Component | 0.793 | react.dev/reference/react/Component | 0.789 |
| crawl4ai-raw | #1 | react.dev/learn/render-and-commit | 0.811 | reference/react/Component | 0.793 | react.dev/reference/react/Component | 0.789 |
| scrapy+md | #1 | react.dev/learn/render-and-commit | 0.806 | react.dev/learn/render-and-commit | 0.795 | react.dev/learn/preserving-and-resetting-state | 0.792 |
| crawlee | #4 | react.dev/learn/preserving-and-resetting-state | 0.788 | react.dev/reference/react/useState | 0.786 | react.dev/reference/react/Component | 0.784 |
| colly+md | #10 | react.dev/learn/preserving-and-resetting-state#dif | 0.792 | react.dev/learn/preserving-and-resetting-state#opt | 0.792 | react.dev/learn/preserving-and-resetting-state | 0.792 |
| playwright | #5 | react.dev/learn/preserving-and-resetting-state | 0.792 | react.dev/reference/react/useState | 0.786 | react.dev/reference/react/Component | 0.784 |


**Q53: What is state in React?**
*(expects URL containing: `adding-interactivity`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #13 | react.dev/learn/thinking-in-react | 0.793 | react.dev/learn/state-a-components-memory | 0.790 | react.dev/learn/reacting-to-input-with-state | 0.790 |
| crawl4ai | #15 | react.dev/learn/reacting-to-input-with-state | 0.788 | react.dev/learn/state-a-components-memory | 0.774 | react.dev/learn/preserving-and-resetting-state | 0.773 |
| crawl4ai-raw | #15 | react.dev/learn/reacting-to-input-with-state | 0.788 | react.dev/learn/state-a-components-memory | 0.774 | react.dev/learn/preserving-and-resetting-state | 0.773 |
| scrapy+md | #13 | react.dev/learn/reacting-to-input-with-state | 0.793 | react.dev/learn/state-a-components-memory | 0.790 | react.dev/learn/reacting-to-input-with-state | 0.790 |
| crawlee | #20 | react.dev/learn/reacting-to-input-with-state | 0.792 | react.dev/learn/state-a-components-memory | 0.790 | react.dev/reference/react/useState | 0.789 |
| colly+md | #45 | react.dev/learn/preserving-and-resetting-state#dif | 0.795 | react.dev/learn/preserving-and-resetting-state | 0.795 | react.dev/learn/preserving-and-resetting-state#opt | 0.795 |
| playwright | #20 | react.dev/learn/preserving-and-resetting-state | 0.795 | react.dev/learn/state-a-components-memory | 0.790 | react.dev/learn/reacting-to-input-with-state | 0.790 |


**Q54: How do you add event handlers to JSX in React?**
*(expects URL containing: `adding-interactivity`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | react.dev/learn/responding-to-events | 0.885 | react.dev/learn/adding-interactivity | 0.834 | react.dev/learn/responding-to-events | 0.801 |
| crawl4ai | #3 | react.dev/learn/responding-to-events | 0.877 | react.dev/learn/responding-to-events | 0.835 | he.react.dev/learn/adding-interactivity | 0.833 |
| crawl4ai-raw | #3 | react.dev/learn/responding-to-events | 0.877 | react.dev/learn/responding-to-events | 0.835 | he.react.dev/learn/adding-interactivity | 0.833 |
| scrapy+md | #2 | react.dev/learn/responding-to-events | 0.890 | react.dev/learn/adding-interactivity | 0.828 | react.dev/learn/responding-to-events | 0.801 |
| crawlee | #2 | react.dev/learn/responding-to-events | 0.847 | react.dev/learn/adding-interactivity | 0.819 | react.dev/learn/responding-to-events | 0.799 |
| colly+md | #3 | react.dev/learn/responding-to-events | 0.887 | react.dev/learn/responding-to-events#passing-event | 0.887 | react.dev/learn/adding-interactivity | 0.821 |
| playwright | #2 | react.dev/learn/responding-to-events | 0.887 | react.dev/learn/adding-interactivity | 0.821 | react.dev/learn/responding-to-events | 0.801 |


**Q55: What is state in React?**
*(expects URL containing: `state-a-components-memory`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | react.dev/learn/thinking-in-react | 0.793 | react.dev/learn/state-a-components-memory | 0.790 | react.dev/learn/reacting-to-input-with-state | 0.790 |
| crawl4ai | #2 | react.dev/learn/reacting-to-input-with-state | 0.788 | react.dev/learn/state-a-components-memory | 0.774 | react.dev/learn/preserving-and-resetting-state | 0.773 |
| crawl4ai-raw | #2 | react.dev/learn/reacting-to-input-with-state | 0.788 | react.dev/learn/state-a-components-memory | 0.774 | react.dev/learn/preserving-and-resetting-state | 0.773 |
| scrapy+md | #2 | react.dev/learn/reacting-to-input-with-state | 0.793 | react.dev/learn/state-a-components-memory | 0.790 | react.dev/learn/reacting-to-input-with-state | 0.790 |
| crawlee | #2 | react.dev/learn/reacting-to-input-with-state | 0.792 | react.dev/learn/state-a-components-memory | 0.790 | react.dev/reference/react/useState | 0.789 |
| colly+md | #4 | react.dev/learn/preserving-and-resetting-state#dif | 0.795 | react.dev/learn/preserving-and-resetting-state | 0.795 | react.dev/learn/preserving-and-resetting-state#opt | 0.795 |
| playwright | #2 | react.dev/learn/preserving-and-resetting-state | 0.795 | react.dev/learn/state-a-components-memory | 0.790 | react.dev/learn/reacting-to-input-with-state | 0.790 |


**Q56: How do you add a state variable using the useState Hook?**
*(expects URL containing: `state-a-components-memory`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/state-a-components-memory | 0.774 | react.dev/learn/state-a-components-memory | 0.771 | react.dev/learn | 0.766 |
| crawl4ai | #1 | react.dev/learn/state-a-components-memory | 0.790 | react.dev/learn/state-a-components-memory | 0.780 | he.react.dev/learn | 0.763 |
| crawl4ai-raw | #1 | react.dev/learn/state-a-components-memory | 0.790 | react.dev/learn/state-a-components-memory | 0.780 | he.react.dev/learn | 0.763 |
| scrapy+md | #2 | react.dev/reference/react/useState | 0.791 | react.dev/learn/state-a-components-memory | 0.774 | react.dev/learn/state-a-components-memory | 0.771 |
| crawlee | #1 | react.dev/learn/state-a-components-memory | 0.777 | react.dev/learn/state-a-components-memory | 0.774 | react.dev/learn/state-a-components-memory | 0.771 |
| colly+md | #1 | react.dev/learn/state-a-components-memory | 0.777 | react.dev/learn/state-a-components-memory#anatomy- | 0.777 | react.dev/learn/state-a-components-memory#anatomy- | 0.774 |
| playwright | #1 | react.dev/learn/state-a-components-memory | 0.777 | react.dev/learn/state-a-components-memory | 0.774 | react.dev/learn/state-a-components-memory | 0.771 |


**Q57: What does createRef return?**
*(expects URL containing: `createRef`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/manipulating-the-dom-with-refs | 0.637 | react.dev/learn/rendering-lists | 0.637 | react.dev/learn/manipulating-the-dom-with-refs | 0.594 |
| crawl4ai | #1 | react.dev/reference/react/createRef | 0.713 | react.dev/reference/react/createRef | 0.667 | react.dev/reference/react/forwardRef | 0.636 |
| crawl4ai-raw | #1 | react.dev/reference/react/createRef | 0.713 | react.dev/reference/react/createRef | 0.667 | react.dev/reference/react/forwardRef | 0.636 |
| scrapy+md | #1 | react.dev/reference/react/createRef | 0.729 | react.dev/reference/react/forwardRef | 0.639 | react.dev/blog/2024/12/05/react-19 | 0.637 |
| crawlee | #1 | react.dev/reference/react/createRef | 0.708 | react.dev/reference/react/createRef | 0.671 | react.dev/reference/react/forwardRef | 0.663 |
| colly+md | #1 | react.dev/reference/react/createRef | 0.708 | react.dev/reference/react/createRef | 0.671 | react.dev/reference/react/forwardRef | 0.663 |
| playwright | #1 | react.dev/reference/react/createRef | 0.708 | react.dev/reference/react/createRef | 0.671 | react.dev/reference/react/forwardRef | 0.663 |


**Q58: How do you declare a ref in a class component using createRef?**
*(expects URL containing: `createRef`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/referencing-values-with-refs | 0.740 | react.dev/learn/manipulating-the-dom-with-refs | 0.737 | react.dev/learn/escape-hatches | 0.729 |
| crawl4ai | #1 | react.dev/reference/react/createRef | 0.859 | react.dev/reference/react/createRef | 0.796 | react.dev/reference/react/forwardRef | 0.760 |
| crawl4ai-raw | #1 | react.dev/reference/react/createRef | 0.859 | react.dev/reference/react/createRef | 0.796 | react.dev/reference/react/forwardRef | 0.760 |
| scrapy+md | #1 | react.dev/reference/react/createRef | 0.849 | react.dev/reference/react/createRef | 0.781 | react.dev/reference/react/useImperativeHandle | 0.748 |
| crawlee | #1 | react.dev/reference/react/createRef | 0.810 | react.dev/reference/react/createRef | 0.807 | react.dev/reference/react/useRef | 0.794 |
| colly+md | #1 | react.dev/reference/react/createRef | 0.812 | react.dev/reference/react/createRef | 0.807 | react.dev/reference/react/useRef#reference | 0.794 |
| playwright | #1 | react.dev/reference/react/createRef | 0.812 | react.dev/reference/react/createRef | 0.807 | react.dev/reference/react/useRef | 0.794 |


</details>

## rust-book

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 57% (34/60) | 85% (51/60) | 88% (53/60) | 93% (56/60) | 95% (57/60) | 0.714 | 1287 | 112 |
| crawl4ai | 47% (28/60) | 73% (44/60) | 90% (54/60) | 97% (58/60) | 100% (60/60) | 0.648 | 2702 | 200 |
| crawl4ai-raw | 47% (28/60) | 73% (44/60) | 90% (54/60) | 97% (58/60) | 100% (60/60) | 0.648 | 2702 | 200 |
| playwright | 30% (18/60) | 63% (38/60) | 75% (45/60) | 85% (51/60) | 92% (55/60) | 0.504 | 2829 | 200 |
| crawlee | 27% (16/60) | 62% (37/60) | 75% (45/60) | 85% (51/60) | 92% (55/60) | 0.482 | 2829 | 200 |
| colly+md | 5% (3/60) | 5% (3/60) | 5% (3/60) | 7% (4/60) | 7% (4/60) | 0.054 | 1976 | 54 |
| scrapy+md | 3% (2/60) | 5% (3/60) | 5% (3/60) | 10% (6/60) | 10% (6/60) | 0.045 | 2978 | 199 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for rust-book</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is the conventional style for function and variable names in Rust?**
*(expects URL containing: `ch03-03-how-functions-work.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch03-03-how-functions-work. | 0.829 | doc.rust-lang.org/book/ch03-03-how-functions-work. | 0.798 | doc.rust-lang.org/book/print.html | 0.798 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch03-03-how-function | 0.819 | doc.rust-lang.org/book/ch03-03-how-functions-work. | 0.819 | doc.rust-lang.org/reference/items/traits.html | 0.793 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch03-03-how-function | 0.819 | doc.rust-lang.org/book/ch03-03-how-functions-work. | 0.819 | doc.rust-lang.org/reference/items/traits.html | 0.793 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.815 | doc.rust-lang.org/stable/book/print.html | 0.815 | doc.rust-lang.org/stable/book/print.html | 0.789 |
| crawlee | #1 | doc.rust-lang.org/book/ch03-03-how-functions-work. | 0.818 | doc.rust-lang.org/stable/book/ch03-03-how-function | 0.818 | doc.rust-lang.org/book/ch10-01-syntax.html | 0.815 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.815 | doc.rust-lang.org/stable/book/print.html | 0.815 | doc.rust-lang.org/stable/book/print.html | 0.789 |
| playwright | #1 | doc.rust-lang.org/book/ch03-03-how-functions-work. | 0.818 | doc.rust-lang.org/stable/book/ch03-03-how-function | 0.818 | doc.rust-lang.org/book/print.html | 0.815 |


**Q2: How do you define a function in Rust that returns a value?**
*(expects URL containing: `ch03-03-how-functions-work.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.828 | doc.rust-lang.org/book/print.html | 0.828 | doc.rust-lang.org/book/ch03-03-how-functions-work. | 0.817 |
| crawl4ai | #3 | doc.rust-lang.org/book/print.html | 0.828 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.828 | doc.rust-lang.org/book/ch03-03-how-functions-work. | 0.812 |
| crawl4ai-raw | #3 | doc.rust-lang.org/book/print.html | 0.828 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.828 | doc.rust-lang.org/book/ch03-03-how-functions-work. | 0.812 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.817 | doc.rust-lang.org/book/print.html | 0.817 | doc.rust-lang.org/stable/book/print.html | 0.794 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.817 | doc.rust-lang.org/stable/book/ch03-03-how-function | 0.817 | doc.rust-lang.org/book/ch03-03-how-functions-work. | 0.817 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.817 | doc.rust-lang.org/stable/book/print.html | 0.817 | doc.rust-lang.org/book/print.html | 0.794 |
| playwright | #1 | doc.rust-lang.org/stable/book/ch03-03-how-function | 0.817 | doc.rust-lang.org/book/ch03-03-how-functions-work. | 0.817 | doc.rust-lang.org/book/print.html | 0.817 |


**Q3: What does the `cargo install` command do?**
*(expects URL containing: `ch14-04-installing-binaries.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch14-04-installing-binaries | 0.792 | doc.rust-lang.org/book/print.html | 0.788 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.788 |
| crawl4ai | #18 | doc.rust-lang.org/cargo/reference/publishing.html | 0.789 | doc.rust-lang.org/stable/book/ch01-03-hello-cargo. | 0.780 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.780 |
| crawl4ai-raw | #18 | doc.rust-lang.org/cargo/reference/publishing.html | 0.789 | doc.rust-lang.org/stable/book/ch01-03-hello-cargo. | 0.780 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.780 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.788 | doc.rust-lang.org/book/print.html | 0.788 | doc.rust-lang.org/nightly/cargo/commands/cargo-pac | 0.781 |
| crawlee | #15 | doc.rust-lang.org/book/print.html | 0.788 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.788 | doc.rust-lang.org/stable/book/ch01-03-hello-cargo. | 0.788 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.788 | doc.rust-lang.org/stable/book/print.html | 0.788 | doc.rust-lang.org/stable/book/print.html | 0.771 |
| playwright | #15 | doc.rust-lang.org/stable/book/ch01-03-hello-cargo. | 0.788 | doc.rust-lang.org/book/print.html | 0.788 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.788 |


**Q4: Where are binaries installed with `cargo install` stored?**
*(expects URL containing: `ch14-04-installing-binaries.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch14-04-installing-binaries | 0.779 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.743 | doc.rust-lang.org/book/print.html | 0.743 |
| crawl4ai | #7 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/cargo/reference/publishing.html | 0.743 | doc.rust-lang.org/cargo/reference/profiles.html | 0.735 |
| crawl4ai-raw | #7 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/cargo/reference/publishing.html | 0.743 | doc.rust-lang.org/cargo/reference/profiles.html | 0.735 |
| scrapy+md | miss | doc.rust-lang.org/nightly/cargo/reference/environm | 0.745 | doc.rust-lang.org/cargo/CHANGELOG.html | 0.740 | doc.rust-lang.org/nightly/cargo/commands/cargo-pac | 0.737 |
| crawlee | #4 | doc.rust-lang.org/stable/book/ch01-03-hello-cargo. | 0.732 | doc.rust-lang.org/book/print.html | 0.732 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.732 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.732 | doc.rust-lang.org/stable/book/print.html | 0.732 | doc.rust-lang.org/book/print.html | 0.730 |
| playwright | #4 | doc.rust-lang.org/book/print.html | 0.732 | doc.rust-lang.org/stable/book/ch01-03-hello-cargo. | 0.732 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.732 |


**Q5: How do I run tests in parallel using cargo test?**
*(expects URL containing: `ch11-02-running-tests.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch11-02-running-tests.html | 0.851 | doc.rust-lang.org/book/print.html | 0.851 | doc.rust-lang.org/book/ch11-02-running-tests.html | 0.788 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch11-02-running-test | 0.849 | doc.rust-lang.org/book/print.html | 0.849 | doc.rust-lang.org/book/ch11-02-running-tests.html | 0.849 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch11-02-running-test | 0.849 | doc.rust-lang.org/book/print.html | 0.849 | doc.rust-lang.org/book/ch11-02-running-tests.html | 0.849 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.851 | doc.rust-lang.org/stable/book/print.html | 0.851 | doc.rust-lang.org/stable/book/print.html | 0.764 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.851 | doc.rust-lang.org/book/ch11-02-running-tests.html | 0.851 | doc.rust-lang.org/stable/book/ch11-02-running-test | 0.851 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.851 | doc.rust-lang.org/book/print.html | 0.851 | doc.rust-lang.org/book/print.html | 0.764 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.851 | doc.rust-lang.org/stable/book/ch11-02-running-test | 0.851 | doc.rust-lang.org/book/ch11-02-running-tests.html | 0.851 |


**Q6: What command do I use to see output from passing tests?**
*(expects URL containing: `ch11-02-running-tests.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | doc.rust-lang.org/book/ch11-01-writing-tests.html | 0.770 | doc.rust-lang.org/book/print.html | 0.770 | doc.rust-lang.org/book/ch11-02-running-tests.html | 0.735 |
| crawl4ai | #4 | doc.rust-lang.org/stable/book/ch11-03-test-organiz | 0.767 | doc.rust-lang.org/book/print.html | 0.767 | doc.rust-lang.org/book/ch11-03-test-organization.h | 0.767 |
| crawl4ai-raw | #4 | doc.rust-lang.org/stable/book/ch11-03-test-organiz | 0.767 | doc.rust-lang.org/book/print.html | 0.767 | doc.rust-lang.org/book/ch11-03-test-organization.h | 0.767 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.752 | doc.rust-lang.org/stable/book/print.html | 0.752 | doc.rust-lang.org/stable/book/print.html | 0.741 |
| crawlee | #1 | doc.rust-lang.org/book/ch11-02-running-tests.html | 0.752 | doc.rust-lang.org/stable/book/ch11-02-running-test | 0.752 | doc.rust-lang.org/book/print.html | 0.752 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.752 | doc.rust-lang.org/book/print.html | 0.752 | doc.rust-lang.org/stable/book/print.html | 0.741 |
| playwright | #1 | doc.rust-lang.org/book/ch11-02-running-tests.html | 0.752 | doc.rust-lang.org/book/print.html | 0.752 | doc.rust-lang.org/stable/book/ch11-02-running-test | 0.752 |


**Q7: How do you extract the `front_of_house` module to its own file?**
*(expects URL containing: `ch07-05-separating-modules-into-different-files.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.807 | doc.rust-lang.org/book/print.html | 0.755 | doc.rust-lang.org/book/print.html | 0.751 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.785 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.785 | doc.rust-lang.org/book/print.html | 0.785 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.785 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.785 | doc.rust-lang.org/book/print.html | 0.785 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.728 | doc.rust-lang.org/book/print.html | 0.728 | doc.rust-lang.org/stable/book/print.html | 0.723 |
| crawlee | #1 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.728 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.728 | doc.rust-lang.org/book/print.html | 0.728 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.728 | doc.rust-lang.org/book/print.html | 0.728 | doc.rust-lang.org/book/print.html | 0.723 |
| playwright | #1 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.728 | doc.rust-lang.org/book/print.html | 0.728 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.728 |


**Q8: What are the file paths the Rust compiler looks for a module named `front_of_house`?**
*(expects URL containing: `ch07-05-separating-modules-into-different-files.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.852 | doc.rust-lang.org/book/print.html | 0.852 | doc.rust-lang.org/book/ch07-03-paths-for-referring | 0.803 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.866 | doc.rust-lang.org/book/print.html | 0.866 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.866 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.866 | doc.rust-lang.org/book/print.html | 0.866 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.866 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.827 | doc.rust-lang.org/stable/book/print.html | 0.827 | doc.rust-lang.org/stable/book/print.html | 0.793 |
| crawlee | #1 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.827 | doc.rust-lang.org/book/print.html | 0.827 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.827 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.827 | doc.rust-lang.org/book/print.html | 0.827 | doc.rust-lang.org/book/print.html | 0.793 |
| playwright | #1 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.827 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.827 | doc.rust-lang.org/book/print.html | 0.827 |


**Q9: How do you bring a module into the scope of a function using the `use` keyword?**
*(expects URL containing: `ch07-04-bringing-paths-into-scope-with-the-use-keyword.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.800 | doc.rust-lang.org/book/print.html | 0.800 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.798 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.796 | doc.rust-lang.org/stable/book/ch07-04-bringing-pat | 0.796 | doc.rust-lang.org/book/print.html | 0.796 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.796 | doc.rust-lang.org/stable/book/ch07-04-bringing-pat | 0.796 | doc.rust-lang.org/book/print.html | 0.796 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.794 | doc.rust-lang.org/book/print.html | 0.794 | doc.rust-lang.org/book/print.html | 0.777 |
| crawlee | #1 | doc.rust-lang.org/stable/book/ch07-04-bringing-pat | 0.794 | doc.rust-lang.org/book/print.html | 0.794 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.794 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.794 | doc.rust-lang.org/book/print.html | 0.794 | doc.rust-lang.org/stable/book/print.html | 0.777 |
| playwright | #1 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.794 | doc.rust-lang.org/stable/book/ch07-04-bringing-pat | 0.794 | doc.rust-lang.org/book/print.html | 0.794 |


**Q10: What is the purpose of the `pub use` statement in Rust?**
*(expects URL containing: `ch07-04-bringing-paths-into-scope-with-the-use-keyword.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.780 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.771 | doc.rust-lang.org/book/print.html | 0.771 |
| crawl4ai | #4 | doc.rust-lang.org/reference/macros-by-example.html | 0.809 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.780 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.780 |
| crawl4ai-raw | #4 | doc.rust-lang.org/reference/macros-by-example.html | 0.809 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.780 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.780 |
| scrapy+md | miss | doc.rust-lang.org/reference/macros-by-example.html | 0.773 | doc.rust-lang.org/book/print.html | 0.767 | doc.rust-lang.org/stable/book/print.html | 0.767 |
| crawlee | #8 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.785 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.785 | doc.rust-lang.org/reference/macros-by-example.html | 0.773 |
| colly+md | miss | doc.rust-lang.org/reference/macros-by-example.html | 0.773 | doc.rust-lang.org/book/print.html | 0.767 | doc.rust-lang.org/stable/book/print.html | 0.767 |
| playwright | #9 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.785 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.785 | doc.rust-lang.org/reference/macros-by-example.html | 0.773 |


**Q11: How do you create a directory for a Rust project?**
*(expects URL containing: `ch01-02-hello-world.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.798 | doc.rust-lang.org/book/ch01-02-hello-world.html | 0.798 | doc.rust-lang.org/book/ch01-02-hello-world.html | 0.793 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.804 | doc.rust-lang.org/book/ch01-02-hello-world.html | 0.804 | doc.rust-lang.org/stable/book/ch01-02-hello-world. | 0.804 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.804 | doc.rust-lang.org/book/ch01-02-hello-world.html | 0.804 | doc.rust-lang.org/stable/book/ch01-02-hello-world. | 0.804 |
| scrapy+md | #3 | doc.rust-lang.org/stable/book/print.html | 0.792 | doc.rust-lang.org/book/print.html | 0.792 | doc.rust-lang.org/stable/book/ch01-02-hello-world. | 0.792 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.792 | doc.rust-lang.org/stable/book/ch01-02-hello-world. | 0.792 | doc.rust-lang.org/book/ch01-02-hello-world.html | 0.792 |
| colly+md | #1 | doc.rust-lang.org/book/ch01-02-hello-world.html | 0.798 | doc.rust-lang.org/stable/book/print.html | 0.792 | doc.rust-lang.org/book/print.html | 0.792 |
| playwright | #1 | doc.rust-lang.org/book/ch01-02-hello-world.html | 0.792 | doc.rust-lang.org/book/print.html | 0.792 | doc.rust-lang.org/stable/book/ch01-02-hello-world. | 0.792 |


**Q12: What command do you use to compile a Rust program?**
*(expects URL containing: `ch01-02-hello-world.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/ch01-01-installation.html | 0.824 | doc.rust-lang.org/book/ch01-02-hello-world.html | 0.805 | doc.rust-lang.org/book/print.html | 0.805 |
| crawl4ai | #6 | doc.rust-lang.org/stable/book/ch01-01-installation | 0.829 | doc.rust-lang.org/book/ch01-01-installation.html | 0.829 | doc.rust-lang.org/stable/book/ch12-00-an-io-projec | 0.811 |
| crawl4ai-raw | #6 | doc.rust-lang.org/stable/book/ch01-01-installation | 0.829 | doc.rust-lang.org/book/ch01-01-installation.html | 0.829 | doc.rust-lang.org/stable/book/ch12-00-an-io-projec | 0.811 |
| scrapy+md | #7 | doc.rust-lang.org/book/ch01-01-installation.html | 0.826 | doc.rust-lang.org/stable/book/ch01-01-installation | 0.826 | doc.rust-lang.org/book/print.html | 0.807 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.807 | doc.rust-lang.org/stable/book/ch01-02-hello-world. | 0.806 | doc.rust-lang.org/book/ch01-02-hello-world.html | 0.806 |
| colly+md | #6 | doc.rust-lang.org/book/ch01-01-installation.html | 0.807 | doc.rust-lang.org/stable/book/ch01-01-installation | 0.807 | doc.rust-lang.org/stable/book/print.html | 0.807 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.807 | doc.rust-lang.org/book/ch01-02-hello-world.html | 0.806 | doc.rust-lang.org/stable/book/ch01-02-hello-world. | 0.806 |


**Q13: What is a function pointer in Rust?**
*(expects URL containing: `ch20-04-advanced-functions-and-closures.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #7 | doc.rust-lang.org/book/ch15-00-smart-pointers.html | 0.814 | doc.rust-lang.org/book/print.html | 0.808 | doc.rust-lang.org/book/ch03-03-how-functions-work. | 0.803 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.834 | doc.rust-lang.org/book/ch15-00-smart-pointers.html | 0.810 | doc.rust-lang.org/book/print.html | 0.807 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.834 | doc.rust-lang.org/book/ch15-00-smart-pointers.html | 0.810 | doc.rust-lang.org/book/print.html | 0.807 |
| scrapy+md | miss | doc.rust-lang.org/core/primitive.fn.html | 0.810 | doc.rust-lang.org/stable/book/print.html | 0.808 | doc.rust-lang.org/book/print.html | 0.808 |
| crawlee | #22 | doc.rust-lang.org/book/print.html | 0.808 | doc.rust-lang.org/book/print.html | 0.796 | doc.rust-lang.org/book/ch03-03-how-functions-work. | 0.790 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.808 | doc.rust-lang.org/stable/book/print.html | 0.808 | doc.rust-lang.org/stable/book/print.html | 0.796 |
| playwright | #21 | doc.rust-lang.org/book/print.html | 0.808 | doc.rust-lang.org/book/print.html | 0.796 | doc.rust-lang.org/book/ch03-03-how-functions-work. | 0.790 |


**Q14: How can you return a closure from a function in Rust?**
*(expects URL containing: `ch20-04-advanced-functions-and-closures.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.851 | doc.rust-lang.org/book/print.html | 0.851 | doc.rust-lang.org/book/ch13-01-closures.html | 0.816 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.856 | doc.rust-lang.org/book/print.html | 0.856 | doc.rust-lang.org/book/print.html | 0.822 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.856 | doc.rust-lang.org/book/print.html | 0.856 | doc.rust-lang.org/book/print.html | 0.822 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.827 | doc.rust-lang.org/stable/book/print.html | 0.827 | doc.rust-lang.org/book/print.html | 0.823 |
| crawlee | #1 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.827 | doc.rust-lang.org/book/print.html | 0.827 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.823 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.827 | doc.rust-lang.org/book/print.html | 0.827 | doc.rust-lang.org/stable/book/print.html | 0.823 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.827 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.827 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.823 |


**Q15: What are the three kinds of loops in Rust?**
*(expects URL containing: `ch03-05-control-flow.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch03-05-control-flow.html | 0.796 | doc.rust-lang.org/book/print.html | 0.796 | doc.rust-lang.org/book/ch03-05-control-flow.html | 0.765 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch03-05-control-flow | 0.792 | doc.rust-lang.org/book/print.html | 0.792 | doc.rust-lang.org/book/ch03-05-control-flow.html | 0.792 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch03-05-control-flow | 0.792 | doc.rust-lang.org/book/print.html | 0.792 | doc.rust-lang.org/book/ch03-05-control-flow.html | 0.792 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.793 | doc.rust-lang.org/book/print.html | 0.793 | doc.rust-lang.org/book/print.html | 0.778 |
| crawlee | #1 | doc.rust-lang.org/stable/book/ch03-05-control-flow | 0.793 | doc.rust-lang.org/book/print.html | 0.793 | doc.rust-lang.org/book/ch03-05-control-flow.html | 0.793 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.793 | doc.rust-lang.org/book/print.html | 0.793 | doc.rust-lang.org/stable/book/print.html | 0.778 |
| playwright | #1 | doc.rust-lang.org/book/ch03-05-control-flow.html | 0.793 | doc.rust-lang.org/book/print.html | 0.793 | doc.rust-lang.org/stable/book/ch03-05-control-flow | 0.793 |


**Q16: How can you use an `if` expression in a `let` statement?**
*(expects URL containing: `ch03-05-control-flow.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #6 | doc.rust-lang.org/book/ch06-03-if-let.html | 0.779 | doc.rust-lang.org/book/print.html | 0.775 | doc.rust-lang.org/book/print.html | 0.772 |
| crawl4ai | #4 | doc.rust-lang.org/book/print.html | 0.786 | doc.rust-lang.org/stable/book/ch06-03-if-let.html | 0.786 | doc.rust-lang.org/book/ch06-03-if-let.html | 0.786 |
| crawl4ai-raw | #4 | doc.rust-lang.org/book/print.html | 0.786 | doc.rust-lang.org/stable/book/ch06-03-if-let.html | 0.786 | doc.rust-lang.org/book/ch06-03-if-let.html | 0.786 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.778 | doc.rust-lang.org/stable/book/print.html | 0.778 | doc.rust-lang.org/stable/book/print.html | 0.770 |
| crawlee | #4 | doc.rust-lang.org/book/ch19-01-all-the-places-for- | 0.778 | doc.rust-lang.org/book/print.html | 0.778 | doc.rust-lang.org/book/print.html | 0.770 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.778 | doc.rust-lang.org/stable/book/print.html | 0.778 | doc.rust-lang.org/stable/book/print.html | 0.770 |
| playwright | #3 | doc.rust-lang.org/book/ch19-01-all-the-places-for- | 0.778 | doc.rust-lang.org/book/print.html | 0.778 | doc.rust-lang.org/book/ch03-05-control-flow.html | 0.770 |


**Q17: What command line tool will we build in this chapter?**
*(expects URL containing: `ch12-00-an-io-project.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch12-00-an-io-project.html | 0.775 | doc.rust-lang.org/book/print.html | 0.767 | doc.rust-lang.org/book/print.html | 0.721 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.767 | doc.rust-lang.org/stable/book/ch12-00-an-io-projec | 0.765 | doc.rust-lang.org/book/ch12-00-an-io-project.html | 0.765 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.767 | doc.rust-lang.org/stable/book/ch12-00-an-io-projec | 0.765 | doc.rust-lang.org/book/ch12-00-an-io-project.html | 0.765 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.767 | doc.rust-lang.org/book/print.html | 0.767 | doc.rust-lang.org/book/print.html | 0.716 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.767 | doc.rust-lang.org/book/ch12-00-an-io-project.html | 0.741 | doc.rust-lang.org/stable/book/ch12-00-an-io-projec | 0.741 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.767 | doc.rust-lang.org/stable/book/print.html | 0.767 | doc.rust-lang.org/stable/book/print.html | 0.716 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.767 | doc.rust-lang.org/book/ch12-00-an-io-project.html | 0.741 | doc.rust-lang.org/stable/book/ch12-00-an-io-projec | 0.741 |


**Q18: How does the `grep` tool function in terms of its arguments and output?**
*(expects URL containing: `ch12-00-an-io-project.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch12-00-an-io-project.html | 0.705 | doc.rust-lang.org/book/print.html | 0.693 | doc.rust-lang.org/book/print.html | 0.671 |
| crawl4ai | #6 | doc.rust-lang.org/book/print.html | 0.693 | doc.rust-lang.org/std/primitive.str.html | 0.690 | doc.rust-lang.org/book/print.html | 0.678 |
| crawl4ai-raw | #6 | doc.rust-lang.org/book/print.html | 0.693 | doc.rust-lang.org/std/primitive.str.html | 0.690 | doc.rust-lang.org/book/print.html | 0.678 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.693 | doc.rust-lang.org/book/print.html | 0.693 | doc.rust-lang.org/src/core/str/pattern.rs.html | 0.687 |
| crawlee | #38 | doc.rust-lang.org/book/print.html | 0.693 | doc.rust-lang.org/std/primitive.str.html#method.pa | 0.681 | doc.rust-lang.org/std/string/struct.String.html | 0.681 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.693 | doc.rust-lang.org/stable/book/print.html | 0.693 | doc.rust-lang.org/std/string/struct.String.html | 0.681 |
| playwright | #38 | doc.rust-lang.org/book/print.html | 0.693 | doc.rust-lang.org/std/string/struct.String.html | 0.681 | doc.rust-lang.org/std/primitive.str.html | 0.681 |


**Q19: What are the two main profiles in Cargo for building Rust code?**
*(expects URL containing: `ch14-01-release-profiles.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.858 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.849 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.814 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.857 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.849 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.811 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.857 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.849 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.811 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.862 | doc.rust-lang.org/book/print.html | 0.862 | doc.rust-lang.org/cargo/reference/profiles.html | 0.818 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.862 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.842 | doc.rust-lang.org/stable/book/ch01-03-hello-cargo. | 0.811 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.862 | doc.rust-lang.org/book/print.html | 0.862 | doc.rust-lang.org/book/print.html | 0.806 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.862 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.842 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.811 |


**Q20: How can you customize the `opt-level` setting for the `dev` profile in Cargo?**
*(expects URL containing: `ch14-01-release-profiles.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.877 | doc.rust-lang.org/book/print.html | 0.837 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.812 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.870 | doc.rust-lang.org/book/print.html | 0.832 | doc.rust-lang.org/book/print.html | 0.812 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.870 | doc.rust-lang.org/book/print.html | 0.832 | doc.rust-lang.org/book/print.html | 0.812 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.842 | doc.rust-lang.org/stable/book/print.html | 0.842 | doc.rust-lang.org/book/print.html | 0.812 |
| crawlee | #1 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.880 | doc.rust-lang.org/book/print.html | 0.842 | doc.rust-lang.org/book/print.html | 0.812 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.842 | doc.rust-lang.org/stable/book/print.html | 0.842 | doc.rust-lang.org/book/print.html | 0.812 |
| playwright | #1 | doc.rust-lang.org/book/ch14-01-release-profiles.ht | 0.880 | doc.rust-lang.org/book/print.html | 0.842 | doc.rust-lang.org/book/print.html | 0.812 |


**Q21: How can you extend Cargo with new subcommands?**
*(expects URL containing: `ch14-05-extending-cargo.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch14-05-extending-cargo.htm | 0.840 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/book/print.html | 0.726 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch14-05-extending-cargo.htm | 0.774 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/book/ch14-00-more-about-cargo.ht | 0.728 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch14-05-extending-cargo.htm | 0.774 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/book/ch14-00-more-about-cargo.ht | 0.728 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.771 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/nightly/cargo/reference/unstable | 0.726 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/book/ch14-05-extending-cargo.htm | 0.732 | doc.rust-lang.org/book/ch14-05-extending-cargo.htm | 0.730 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.771 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/book/print.html | 0.715 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/book/ch14-05-extending-cargo.htm | 0.732 | doc.rust-lang.org/book/ch14-05-extending-cargo.htm | 0.730 |


**Q22: What is the benefit of using `cargo install` for extensions?**
*(expects URL containing: `ch14-05-extending-cargo.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch14-05-extending-cargo.htm | 0.775 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/book/ch01-03-hello-cargo.html | 0.733 |
| crawl4ai | #8 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/cargo/reference/publishing.html | 0.734 | doc.rust-lang.org/cargo/reference/profiles.html | 0.728 |
| crawl4ai-raw | #8 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/cargo/reference/publishing.html | 0.734 | doc.rust-lang.org/cargo/reference/profiles.html | 0.728 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.771 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/nightly/cargo/reference/environm | 0.731 |
| crawlee | #8 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/cargo/reference/profiles.html | 0.738 | doc.rust-lang.org/cargo/reference/publishing.html | 0.726 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.771 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/book/print.html | 0.720 |
| playwright | #8 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/cargo/reference/profiles.html | 0.738 | doc.rust-lang.org/cargo/reference/publishing.html | 0.726 |


**Q23: What version of Rust does this book assume you are using?**
*(expects URL containing: `book`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/print.html | 0.830 | doc.rust-lang.org/book/ | 0.819 | doc.rust-lang.org/book/print.html | 0.819 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/title-page.html | 0.823 | doc.rust-lang.org/book/title-page.html | 0.823 | doc.rust-lang.org/book/ | 0.823 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/title-page.html | 0.823 | doc.rust-lang.org/book/title-page.html | 0.823 | doc.rust-lang.org/book/ | 0.823 |
| scrapy+md | #1 | doc.rust-lang.org/book/print.html | 0.829 | doc.rust-lang.org/stable/book/print.html | 0.829 | doc.rust-lang.org/book/print.html | 0.828 |
| crawlee | #1 | doc.rust-lang.org/book/print.html | 0.829 | doc.rust-lang.org/book/print.html | 0.828 | doc.rust-lang.org/book/ch00-00-introduction.html | 0.797 |
| colly+md | #1 | doc.rust-lang.org/book/print.html | 0.829 | doc.rust-lang.org/stable/book/print.html | 0.829 | doc.rust-lang.org/book/print.html | 0.828 |
| playwright | #1 | doc.rust-lang.org/book/print.html | 0.829 | doc.rust-lang.org/book/print.html | 0.828 | doc.rust-lang.org/stable/book/ch00-00-introduction | 0.797 |


**Q24: Where can I find instructions on installing or updating Rust?**
*(expects URL containing: `book`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch01-01-installation.html | 0.858 | doc.rust-lang.org/book/print.html | 0.847 | doc.rust-lang.org/book/print.html | 0.821 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch01-01-installation | 0.822 | doc.rust-lang.org/book/ch01-01-installation.html | 0.822 | doc.rust-lang.org/book/print.html | 0.813 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch01-01-installation | 0.822 | doc.rust-lang.org/book/ch01-01-installation.html | 0.822 | doc.rust-lang.org/book/print.html | 0.813 |
| scrapy+md | #1 | doc.rust-lang.org/stable/book/ch01-01-installation | 0.859 | doc.rust-lang.org/book/ch01-01-installation.html | 0.859 | doc.rust-lang.org/book/ch01-01-installation.html | 0.819 |
| crawlee | #1 | doc.rust-lang.org/book/ch01-01-installation.html | 0.823 | doc.rust-lang.org/stable/book/ch01-01-installation | 0.823 | doc.rust-lang.org/book/print.html | 0.819 |
| colly+md | #1 | doc.rust-lang.org/stable/book/print.html | 0.819 | doc.rust-lang.org/book/print.html | 0.819 | doc.rust-lang.org/book/ch01-01-installation.html | 0.817 |
| playwright | #1 | doc.rust-lang.org/stable/book/ch01-01-installation | 0.823 | doc.rust-lang.org/book/ch01-01-installation.html | 0.823 | doc.rust-lang.org/book/print.html | 0.819 |


**Q25: What is the definition of the `Future` trait in Rust?**
*(expects URL containing: `ch17-05-traits-for-async.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.845 | doc.rust-lang.org/book/print.html | 0.845 | doc.rust-lang.org/book/ch17-01-futures-and-syntax. | 0.831 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.845 | doc.rust-lang.org/book/print.html | 0.845 | doc.rust-lang.org/book/print.html | 0.823 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.845 | doc.rust-lang.org/book/print.html | 0.845 | doc.rust-lang.org/book/print.html | 0.823 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.845 | doc.rust-lang.org/book/print.html | 0.845 | doc.rust-lang.org/stable/book/print.html | 0.813 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.845 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.845 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.813 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.845 | doc.rust-lang.org/book/print.html | 0.845 | doc.rust-lang.org/stable/book/print.html | 0.813 |
| playwright | #1 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.845 | doc.rust-lang.org/book/print.html | 0.845 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.813 |


**Q26: How does the `Pin` type relate to the `Unpin` trait in Rust?**
*(expects URL containing: `ch17-05-traits-for-async.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.849 | doc.rust-lang.org/book/print.html | 0.849 | doc.rust-lang.org/book/print.html | 0.829 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.844 | doc.rust-lang.org/book/print.html | 0.844 | doc.rust-lang.org/book/print.html | 0.815 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.844 | doc.rust-lang.org/book/print.html | 0.844 | doc.rust-lang.org/book/print.html | 0.815 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.862 | doc.rust-lang.org/stable/book/print.html | 0.862 | doc.rust-lang.org/core/pin/index.html | 0.851 |
| crawlee | #1 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.862 | doc.rust-lang.org/book/print.html | 0.862 | doc.rust-lang.org/book/print.html | 0.818 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.862 | doc.rust-lang.org/stable/book/print.html | 0.862 | doc.rust-lang.org/book/print.html | 0.818 |
| playwright | #1 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.862 | doc.rust-lang.org/book/print.html | 0.862 | doc.rust-lang.org/book/print.html | 0.818 |


**Q27: What is a struct in Rust?**
*(expects URL containing: `ch05-00-structs.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch05-00-structs.html | 0.866 | doc.rust-lang.org/book/print.html | 0.829 | doc.rust-lang.org/book/ch05-01-defining-structs.ht | 0.791 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.858 | doc.rust-lang.org/stable/book/ch05-00-structs.html | 0.856 | doc.rust-lang.org/book/ch05-00-structs.html | 0.856 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.858 | doc.rust-lang.org/stable/book/ch05-00-structs.html | 0.856 | doc.rust-lang.org/book/ch05-00-structs.html | 0.856 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.858 | doc.rust-lang.org/book/print.html | 0.858 | doc.rust-lang.org/book/print.html | 0.843 |
| crawlee | #3 | doc.rust-lang.org/book/print.html | 0.858 | doc.rust-lang.org/book/print.html | 0.843 | doc.rust-lang.org/book/ch05-00-structs.html | 0.836 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.858 | doc.rust-lang.org/stable/book/print.html | 0.858 | doc.rust-lang.org/book/print.html | 0.843 |
| playwright | #3 | doc.rust-lang.org/book/print.html | 0.858 | doc.rust-lang.org/book/print.html | 0.843 | doc.rust-lang.org/stable/book/ch05-00-structs.html | 0.836 |


**Q28: How do structs compare to tuples in Rust?**
*(expects URL containing: `ch05-00-structs.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | doc.rust-lang.org/book/print.html | 0.801 | doc.rust-lang.org/book/ch05-01-defining-structs.ht | 0.801 | doc.rust-lang.org/book/print.html | 0.788 |
| crawl4ai | #11 | doc.rust-lang.org/book/ch05-01-defining-structs.ht | 0.796 | doc.rust-lang.org/stable/book/ch05-01-defining-str | 0.796 | doc.rust-lang.org/book/print.html | 0.796 |
| crawl4ai-raw | #11 | doc.rust-lang.org/book/ch05-01-defining-structs.ht | 0.796 | doc.rust-lang.org/stable/book/ch05-01-defining-str | 0.796 | doc.rust-lang.org/book/print.html | 0.796 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.803 | doc.rust-lang.org/book/print.html | 0.803 | doc.rust-lang.org/stable/book/print.html | 0.787 |
| crawlee | #29 | doc.rust-lang.org/book/print.html | 0.803 | doc.rust-lang.org/stable/book/ch05-01-defining-str | 0.803 | doc.rust-lang.org/book/ch05-01-defining-structs.ht | 0.803 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.803 | doc.rust-lang.org/stable/book/print.html | 0.803 | doc.rust-lang.org/book/print.html | 0.787 |
| playwright | #29 | doc.rust-lang.org/book/ch05-01-defining-structs.ht | 0.803 | doc.rust-lang.org/book/print.html | 0.803 | doc.rust-lang.org/stable/book/ch05-01-defining-str | 0.803 |


**Q29: What version of Rust does this book assume you are using?**
*(expects URL containing: `title-page.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | doc.rust-lang.org/book/print.html | 0.830 | doc.rust-lang.org/book/ | 0.819 | doc.rust-lang.org/book/print.html | 0.819 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/title-page.html | 0.823 | doc.rust-lang.org/book/title-page.html | 0.823 | doc.rust-lang.org/book/ | 0.823 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/title-page.html | 0.823 | doc.rust-lang.org/book/title-page.html | 0.823 | doc.rust-lang.org/book/ | 0.823 |
| scrapy+md | #9 | doc.rust-lang.org/book/print.html | 0.829 | doc.rust-lang.org/stable/book/print.html | 0.829 | doc.rust-lang.org/book/print.html | 0.828 |
| crawlee | #12 | doc.rust-lang.org/book/print.html | 0.829 | doc.rust-lang.org/book/print.html | 0.828 | doc.rust-lang.org/book/ch00-00-introduction.html | 0.797 |
| colly+md | #39 | doc.rust-lang.org/book/print.html | 0.829 | doc.rust-lang.org/stable/book/print.html | 0.829 | doc.rust-lang.org/book/print.html | 0.828 |
| playwright | #12 | doc.rust-lang.org/book/print.html | 0.829 | doc.rust-lang.org/book/print.html | 0.828 | doc.rust-lang.org/stable/book/ch00-00-introduction | 0.797 |


**Q30: Where can I find community translations of the Rust book?**
*(expects URL containing: `title-page.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | doc.rust-lang.org/book/foreword.html | 0.771 | doc.rust-lang.org/book/ | 0.758 | doc.rust-lang.org/book/print.html | 0.758 |
| crawl4ai | #4 | doc.rust-lang.org/book/appendix-06-translation.htm | 0.788 | doc.rust-lang.org/stable/book/foreword.html | 0.756 | doc.rust-lang.org/book/foreword.html | 0.756 |
| crawl4ai-raw | #4 | doc.rust-lang.org/book/appendix-06-translation.htm | 0.788 | doc.rust-lang.org/stable/book/foreword.html | 0.756 | doc.rust-lang.org/book/foreword.html | 0.756 |
| scrapy+md | #8 | doc.rust-lang.org/book/foreword.html | 0.771 | doc.rust-lang.org/stable/book/foreword.html | 0.771 | doc.rust-lang.org/book/appendix-06-translation.htm | 0.762 |
| crawlee | #20 | doc.rust-lang.org/book/foreword.html | 0.770 | doc.rust-lang.org/stable/book/foreword.html | 0.770 | doc.rust-lang.org/book/ch17-03-more-futures.html | 0.770 |
| colly+md | #42 | doc.rust-lang.org/stable/book/foreword.html | 0.770 | doc.rust-lang.org/book/foreword.html | 0.770 | doc.rust-lang.org/stable/book/print.html | 0.756 |
| playwright | #18 | doc.rust-lang.org/book/foreword.html | 0.770 | doc.rust-lang.org/stable/book/foreword.html | 0.770 | doc.rust-lang.org/book/ch17-06-futures-tasks-threa | 0.770 |


**Q31: What is a trait in Rust?**
*(expects URL containing: `ch10-02-traits.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #12 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.801 | doc.rust-lang.org/book/print.html | 0.771 | doc.rust-lang.org/book/appendix-03-derivable-trait | 0.766 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch10-02-traits.html | 0.792 | doc.rust-lang.org/stable/book/ch10-02-traits.html | 0.792 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.792 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch10-02-traits.html | 0.792 | doc.rust-lang.org/stable/book/ch10-02-traits.html | 0.792 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.792 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.788 | doc.rust-lang.org/stable/book/print.html | 0.788 | doc.rust-lang.org/stable/book/print.html | 0.758 |
| crawlee | #20 | doc.rust-lang.org/book/print.html | 0.788 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.775 | doc.rust-lang.org/reference/items/traits.html#dyn- | 0.772 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.788 | doc.rust-lang.org/stable/book/print.html | 0.788 | doc.rust-lang.org/book/print.html | 0.758 |
| playwright | #20 | doc.rust-lang.org/book/print.html | 0.788 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.775 | doc.rust-lang.org/reference/items/traits.html | 0.772 |


**Q32: How do you implement a trait on a type in Rust?**
*(expects URL containing: `ch10-02-traits.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #7 | doc.rust-lang.org/book/print.html | 0.815 | doc.rust-lang.org/book/appendix-03-derivable-trait | 0.809 | doc.rust-lang.org/book/print.html | 0.792 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.815 | doc.rust-lang.org/book/ch10-02-traits.html | 0.814 | doc.rust-lang.org/stable/book/ch10-02-traits.html | 0.814 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.815 | doc.rust-lang.org/book/ch10-02-traits.html | 0.814 | doc.rust-lang.org/stable/book/ch10-02-traits.html | 0.814 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.815 | doc.rust-lang.org/stable/book/print.html | 0.815 | doc.rust-lang.org/stable/book/print.html | 0.809 |
| crawlee | #8 | doc.rust-lang.org/book/print.html | 0.815 | doc.rust-lang.org/book/print.html | 0.809 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.809 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.815 | doc.rust-lang.org/book/print.html | 0.815 | doc.rust-lang.org/stable/book/print.html | 0.809 |
| playwright | #9 | doc.rust-lang.org/book/print.html | 0.815 | doc.rust-lang.org/book/print.html | 0.809 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.809 |


**Q33: What is the purpose of using a reference in the `calculate_length` function?**
*(expects URL containing: `ch04-02-references-and-borrowing.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch04-02-references-and-borr | 0.829 | doc.rust-lang.org/book/print.html | 0.796 | doc.rust-lang.org/book/print.html | 0.741 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch04-02-references-a | 0.814 | doc.rust-lang.org/book/ch04-02-references-and-borr | 0.814 | doc.rust-lang.org/book/print.html | 0.807 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch04-02-references-a | 0.814 | doc.rust-lang.org/book/ch04-02-references-and-borr | 0.814 | doc.rust-lang.org/book/print.html | 0.807 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.802 | doc.rust-lang.org/stable/book/print.html | 0.802 | doc.rust-lang.org/stable/book/print.html | 0.787 |
| crawlee | #5 | doc.rust-lang.org/book/print.html | 0.802 | doc.rust-lang.org/book/print.html | 0.787 | doc.rust-lang.org/book/ch04-01-what-is-ownership.h | 0.778 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.802 | doc.rust-lang.org/book/print.html | 0.802 | doc.rust-lang.org/stable/book/print.html | 0.787 |
| playwright | #5 | doc.rust-lang.org/book/print.html | 0.802 | doc.rust-lang.org/book/print.html | 0.787 | doc.rust-lang.org/stable/book/ch04-01-what-is-owne | 0.778 |


**Q34: What are the rules of references in Rust?**
*(expects URL containing: `ch04-02-references-and-borrowing.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.812 | doc.rust-lang.org/book/ch04-02-references-and-borr | 0.812 | doc.rust-lang.org/book/print.html | 0.797 |
| crawl4ai | #4 | doc.rust-lang.org/stable/book/ch10-03-lifetime-syn | 0.802 | doc.rust-lang.org/book/ch10-03-lifetime-syntax.htm | 0.802 | doc.rust-lang.org/book/ch15-04-rc.html | 0.782 |
| crawl4ai-raw | #4 | doc.rust-lang.org/stable/book/ch10-03-lifetime-syn | 0.802 | doc.rust-lang.org/book/ch10-03-lifetime-syntax.htm | 0.802 | doc.rust-lang.org/book/ch15-04-rc.html | 0.782 |
| scrapy+md | miss | doc.rust-lang.org/nomicon/references.html | 0.842 | doc.rust-lang.org/stable/book/print.html | 0.800 | doc.rust-lang.org/book/print.html | 0.800 |
| crawlee | #1 | doc.rust-lang.org/book/ch04-02-references-and-borr | 0.800 | doc.rust-lang.org/book/print.html | 0.800 | doc.rust-lang.org/stable/book/ch04-02-references-a | 0.800 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.800 | doc.rust-lang.org/book/print.html | 0.800 | doc.rust-lang.org/book/print.html | 0.790 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.800 | doc.rust-lang.org/stable/book/ch04-02-references-a | 0.800 | doc.rust-lang.org/book/ch04-02-references-and-borr | 0.800 |


**Q35: What is the purpose of the `search` function in the `minigrep` program?**
*(expects URL containing: `ch12-04-testing-the-librarys-functionality.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.793 | doc.rust-lang.org/book/ch12-04-testing-the-library | 0.793 | doc.rust-lang.org/book/print.html | 0.766 |
| crawl4ai | #4 | doc.rust-lang.org/book/ch12-03-improving-error-han | 0.783 | doc.rust-lang.org/book/print.html | 0.783 | doc.rust-lang.org/stable/book/ch12-03-improving-er | 0.783 |
| crawl4ai-raw | #4 | doc.rust-lang.org/book/ch12-03-improving-error-han | 0.783 | doc.rust-lang.org/book/print.html | 0.783 | doc.rust-lang.org/stable/book/ch12-03-improving-er | 0.783 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.776 | doc.rust-lang.org/book/print.html | 0.776 | doc.rust-lang.org/stable/book/print.html | 0.770 |
| crawlee | #7 | doc.rust-lang.org/book/ch12-03-improving-error-han | 0.779 | doc.rust-lang.org/stable/book/ch12-03-improving-er | 0.779 | doc.rust-lang.org/book/print.html | 0.776 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.776 | doc.rust-lang.org/stable/book/print.html | 0.776 | doc.rust-lang.org/stable/book/print.html | 0.770 |
| playwright | #8 | doc.rust-lang.org/stable/book/ch12-03-improving-er | 0.779 | doc.rust-lang.org/book/ch12-03-improving-error-han | 0.779 | doc.rust-lang.org/book/print.html | 0.776 |


**Q36: What are the steps to implement the `search` function using test-driven development?**
*(expects URL containing: `ch12-04-testing-the-librarys-functionality.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch12-04-testing-the-library | 0.815 | doc.rust-lang.org/book/print.html | 0.767 | doc.rust-lang.org/book/ch12-04-testing-the-library | 0.740 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.794 | doc.rust-lang.org/stable/book/ch12-04-testing-the- | 0.762 | doc.rust-lang.org/book/ch12-04-testing-the-library | 0.754 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.794 | doc.rust-lang.org/stable/book/ch12-04-testing-the- | 0.762 | doc.rust-lang.org/book/ch12-04-testing-the-library | 0.754 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.789 | doc.rust-lang.org/stable/book/print.html | 0.789 | doc.rust-lang.org/book/print.html | 0.760 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.789 | doc.rust-lang.org/stable/book/ch12-04-testing-the- | 0.760 | doc.rust-lang.org/book/print.html | 0.760 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.789 | doc.rust-lang.org/stable/book/print.html | 0.789 | doc.rust-lang.org/stable/book/print.html | 0.760 |
| playwright | #3 | doc.rust-lang.org/book/print.html | 0.789 | doc.rust-lang.org/book/print.html | 0.760 | doc.rust-lang.org/book/ch12-04-testing-the-library | 0.760 |


**Q37: What is a workspace in Cargo?**
*(expects URL containing: `ch14-03-cargo-workspaces.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch14-03-cargo-workspaces.ht | 0.809 | doc.rust-lang.org/book/print.html | 0.782 | doc.rust-lang.org/book/ch14-03-cargo-workspaces.ht | 0.750 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.769 | doc.rust-lang.org/book/ch14-03-cargo-workspaces.ht | 0.744 | doc.rust-lang.org/book/print.html | 0.744 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.769 | doc.rust-lang.org/book/ch14-03-cargo-workspaces.ht | 0.744 | doc.rust-lang.org/book/print.html | 0.744 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.794 | doc.rust-lang.org/stable/book/print.html | 0.794 | doc.rust-lang.org/cargo/reference/workspaces.html | 0.782 |
| crawlee | #3 | doc.rust-lang.org/book/print.html | 0.794 | doc.rust-lang.org/book/print.html | 0.746 | doc.rust-lang.org/book/ch14-03-cargo-workspaces.ht | 0.746 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.794 | doc.rust-lang.org/book/print.html | 0.794 | doc.rust-lang.org/stable/book/print.html | 0.746 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.794 | doc.rust-lang.org/book/ch14-03-cargo-workspaces.ht | 0.746 | doc.rust-lang.org/book/print.html | 0.746 |


**Q38: How do you create a new library crate in a workspace?**
*(expects URL containing: `ch14-03-cargo-workspaces.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch14-03-cargo-workspaces.ht | 0.823 | doc.rust-lang.org/book/print.html | 0.796 | doc.rust-lang.org/book/print.html | 0.790 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.820 | doc.rust-lang.org/book/ch14-03-cargo-workspaces.ht | 0.790 | doc.rust-lang.org/book/ch14-03-cargo-workspaces.ht | 0.785 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.820 | doc.rust-lang.org/book/ch14-03-cargo-workspaces.ht | 0.790 | doc.rust-lang.org/book/ch14-03-cargo-workspaces.ht | 0.785 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.804 | doc.rust-lang.org/stable/book/print.html | 0.804 | doc.rust-lang.org/book/print.html | 0.787 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.804 | doc.rust-lang.org/book/ch14-03-cargo-workspaces.ht | 0.790 | doc.rust-lang.org/book/print.html | 0.787 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.804 | doc.rust-lang.org/book/print.html | 0.804 | doc.rust-lang.org/book/print.html | 0.787 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.804 | doc.rust-lang.org/book/ch14-03-cargo-workspaces.ht | 0.790 | doc.rust-lang.org/book/print.html | 0.787 |


**Q39: What is the purpose of the `thread::spawn` function in Rust?**
*(expects URL containing: `ch16-01-threads.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch16-01-threads.html | 0.817 | doc.rust-lang.org/book/print.html | 0.817 | doc.rust-lang.org/book/ch21-02-multithreaded.html | 0.803 |
| crawl4ai | #4 | doc.rust-lang.org/std/thread/struct.Builder.html | 0.860 | doc.rust-lang.org/std/thread/struct.Builder.html | 0.839 | doc.rust-lang.org/std/thread/struct.Builder.html | 0.835 |
| crawl4ai-raw | #4 | doc.rust-lang.org/std/thread/struct.Builder.html | 0.860 | doc.rust-lang.org/std/thread/struct.Builder.html | 0.839 | doc.rust-lang.org/std/thread/struct.Builder.html | 0.835 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.826 | doc.rust-lang.org/book/print.html | 0.826 | doc.rust-lang.org/std/thread/struct.Builder.html | 0.821 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.826 | doc.rust-lang.org/book/ch16-01-threads.html | 0.826 | doc.rust-lang.org/std/thread/struct.Builder.html | 0.826 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.826 | doc.rust-lang.org/book/print.html | 0.826 | doc.rust-lang.org/std/thread/struct.Builder.html#m | 0.807 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.826 | doc.rust-lang.org/book/ch16-01-threads.html | 0.826 | doc.rust-lang.org/std/thread/struct.Builder.html | 0.826 |


**Q40: How can you ensure that a spawned thread finishes before the main thread exits?**
*(expects URL containing: `ch16-01-threads.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.804 | doc.rust-lang.org/book/ch16-01-threads.html | 0.804 | doc.rust-lang.org/book/ch16-01-threads.html | 0.772 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch16-01-threads.html | 0.782 | doc.rust-lang.org/book/print.html | 0.782 | doc.rust-lang.org/book/print.html | 0.768 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch16-01-threads.html | 0.782 | doc.rust-lang.org/book/print.html | 0.782 | doc.rust-lang.org/book/print.html | 0.768 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.782 | doc.rust-lang.org/book/print.html | 0.782 | doc.rust-lang.org/book/print.html | 0.771 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.782 | doc.rust-lang.org/book/ch16-01-threads.html | 0.782 | doc.rust-lang.org/book/ch16-01-threads.html | 0.771 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.782 | doc.rust-lang.org/book/print.html | 0.782 | doc.rust-lang.org/stable/book/print.html | 0.771 |
| playwright | #1 | doc.rust-lang.org/book/ch16-01-threads.html | 0.782 | doc.rust-lang.org/book/print.html | 0.782 | doc.rust-lang.org/book/print.html | 0.771 |


**Q41: What are generics in Rust?**
*(expects URL containing: `ch10-00-generics.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.820 | doc.rust-lang.org/book/ch10-00-generics.html | 0.819 | doc.rust-lang.org/book/print.html | 0.768 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.818 | doc.rust-lang.org/book/ch10-00-generics.html | 0.811 | doc.rust-lang.org/stable/book/ch10-00-generics.htm | 0.811 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.818 | doc.rust-lang.org/book/ch10-00-generics.html | 0.811 | doc.rust-lang.org/stable/book/ch10-00-generics.htm | 0.811 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.820 | doc.rust-lang.org/book/print.html | 0.820 | doc.rust-lang.org/book/print.html | 0.773 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.820 | doc.rust-lang.org/stable/book/ch10-00-generics.htm | 0.787 | doc.rust-lang.org/book/ch10-00-generics.html | 0.787 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.820 | doc.rust-lang.org/book/print.html | 0.820 | doc.rust-lang.org/stable/book/print.html | 0.773 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.820 | doc.rust-lang.org/stable/book/ch10-00-generics.htm | 0.787 | doc.rust-lang.org/book/ch10-00-generics.html | 0.787 |


**Q42: How do you eliminate code duplication using generics?**
*(expects URL containing: `ch10-00-generics.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch10-00-generics.html | 0.796 | doc.rust-lang.org/book/print.html | 0.796 | doc.rust-lang.org/book/print.html | 0.773 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch10-00-generics.html | 0.846 | doc.rust-lang.org/stable/book/ch10-00-generics.htm | 0.846 | doc.rust-lang.org/book/print.html | 0.815 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch10-00-generics.html | 0.846 | doc.rust-lang.org/stable/book/ch10-00-generics.htm | 0.846 | doc.rust-lang.org/book/print.html | 0.815 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.828 | doc.rust-lang.org/book/print.html | 0.828 | doc.rust-lang.org/stable/book/print.html | 0.780 |
| crawlee | #1 | doc.rust-lang.org/book/ch10-00-generics.html | 0.844 | doc.rust-lang.org/stable/book/ch10-00-generics.htm | 0.844 | doc.rust-lang.org/book/print.html | 0.828 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.828 | doc.rust-lang.org/book/print.html | 0.828 | doc.rust-lang.org/book/print.html | 0.780 |
| playwright | #1 | doc.rust-lang.org/book/ch10-00-generics.html | 0.844 | doc.rust-lang.org/stable/book/ch10-00-generics.htm | 0.844 | doc.rust-lang.org/book/print.html | 0.828 |


**Q43: What will we build in the final project of the Rust book?**
*(expects URL containing: `ch21-00-final-project-a-web-server.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | doc.rust-lang.org/book/ | 0.754 | doc.rust-lang.org/book/print.html | 0.754 | doc.rust-lang.org/book/print.html | 0.741 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch21-00-final-project-a-web | 0.768 | doc.rust-lang.org/book/print.html | 0.738 | doc.rust-lang.org/book/print.html | 0.729 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch21-00-final-project-a-web | 0.768 | doc.rust-lang.org/book/print.html | 0.738 | doc.rust-lang.org/book/print.html | 0.729 |
| scrapy+md | miss | doc.rust-lang.org/book/ | 0.754 | doc.rust-lang.org/stable/book/ | 0.754 | doc.rust-lang.org/stable/book/title-page.html | 0.754 |
| crawlee | #4 | doc.rust-lang.org/book/print.html | 0.741 | doc.rust-lang.org/book/foreword.html | 0.740 | doc.rust-lang.org/stable/book/foreword.html | 0.740 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.741 | doc.rust-lang.org/book/print.html | 0.741 | doc.rust-lang.org/book/foreword.html | 0.740 |
| playwright | #4 | doc.rust-lang.org/book/print.html | 0.741 | doc.rust-lang.org/book/foreword.html | 0.740 | doc.rust-lang.org/stable/book/foreword.html | 0.740 |


**Q44: What method will we not be using to build the web server in this chapter?**
*(expects URL containing: `ch21-00-final-project-a-web-server.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | doc.rust-lang.org/book/print.html | 0.700 | doc.rust-lang.org/book/print.html | 0.699 | doc.rust-lang.org/book/ch21-00-final-project-a-web | 0.697 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.710 | doc.rust-lang.org/book/ch21-00-final-project-a-web | 0.696 | doc.rust-lang.org/book/print.html | 0.694 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.710 | doc.rust-lang.org/book/ch21-00-final-project-a-web | 0.696 | doc.rust-lang.org/book/print.html | 0.694 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.702 | doc.rust-lang.org/book/print.html | 0.702 | doc.rust-lang.org/book/print.html | 0.699 |
| crawlee | #4 | doc.rust-lang.org/book/print.html | 0.702 | doc.rust-lang.org/book/print.html | 0.699 | doc.rust-lang.org/book/ch21-01-single-threaded.htm | 0.684 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.702 | doc.rust-lang.org/stable/book/print.html | 0.702 | doc.rust-lang.org/stable/book/print.html | 0.699 |
| playwright | #4 | doc.rust-lang.org/book/print.html | 0.702 | doc.rust-lang.org/book/print.html | 0.699 | doc.rust-lang.org/book/ch21-01-single-threaded.htm | 0.684 |


**Q45: What are patterns in Rust?**
*(expects URL containing: `ch19-00-patterns.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.858 | doc.rust-lang.org/book/print.html | 0.835 | doc.rust-lang.org/book/ch19-01-all-the-places-for- | 0.795 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.835 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.835 | doc.rust-lang.org/book/print.html | 0.778 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.835 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.835 | doc.rust-lang.org/book/print.html | 0.778 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.835 | doc.rust-lang.org/book/print.html | 0.835 | doc.rust-lang.org/book/print.html | 0.778 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.835 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.818 | doc.rust-lang.org/stable/book/ch10-01-syntax.html | 0.784 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.835 | doc.rust-lang.org/book/print.html | 0.835 | doc.rust-lang.org/book/print.html | 0.778 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.835 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.818 | doc.rust-lang.org/stable/book/ch10-01-syntax.html | 0.784 |


**Q46: What components can a pattern consist of?**
*(expects URL containing: `ch19-00-patterns.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.698 | doc.rust-lang.org/book/print.html | 0.694 | doc.rust-lang.org/book/print.html | 0.645 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.698 | doc.rust-lang.org/book/print.html | 0.694 | doc.rust-lang.org/book/ch19-03-pattern-syntax.html | 0.646 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.698 | doc.rust-lang.org/book/print.html | 0.694 | doc.rust-lang.org/book/ch19-03-pattern-syntax.html | 0.646 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.694 | doc.rust-lang.org/stable/book/print.html | 0.694 | doc.rust-lang.org/stable/book/print.html | 0.647 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.694 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.652 | doc.rust-lang.org/book/print.html | 0.647 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.694 | doc.rust-lang.org/book/print.html | 0.694 | doc.rust-lang.org/stable/book/print.html | 0.647 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.694 | doc.rust-lang.org/book/ch19-00-patterns.html | 0.652 | doc.rust-lang.org/book/print.html | 0.647 |


**Q47: What is the difference between iterators and the async channel receiver in Rust?**
*(expects URL containing: `ch17-04-streams.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch17-04-streams.html | 0.833 | doc.rust-lang.org/book/print.html | 0.806 | doc.rust-lang.org/book/print.html | 0.792 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch17-04-streams.html | 0.836 | doc.rust-lang.org/book/print.html | 0.810 | doc.rust-lang.org/book/ch17-04-streams.html | 0.802 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch17-04-streams.html | 0.836 | doc.rust-lang.org/book/print.html | 0.810 | doc.rust-lang.org/book/ch17-04-streams.html | 0.802 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.816 | doc.rust-lang.org/stable/book/print.html | 0.816 | doc.rust-lang.org/book/print.html | 0.797 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.816 | doc.rust-lang.org/book/ch17-04-streams.html | 0.810 | doc.rust-lang.org/book/print.html | 0.797 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.816 | doc.rust-lang.org/book/print.html | 0.816 | doc.rust-lang.org/stable/book/print.html | 0.797 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.816 | doc.rust-lang.org/book/ch17-04-streams.html | 0.810 | doc.rust-lang.org/book/print.html | 0.797 |


**Q48: How can you create a stream from an iterator in Rust?**
*(expects URL containing: `ch17-04-streams.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch17-04-streams.html | 0.839 | doc.rust-lang.org/book/print.html | 0.839 | doc.rust-lang.org/book/ch17-04-streams.html | 0.783 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch17-04-streams.html | 0.823 | doc.rust-lang.org/book/print.html | 0.823 | doc.rust-lang.org/book/ch17-04-streams.html | 0.816 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch17-04-streams.html | 0.823 | doc.rust-lang.org/book/print.html | 0.823 | doc.rust-lang.org/book/ch17-04-streams.html | 0.816 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.838 | doc.rust-lang.org/stable/book/print.html | 0.838 | doc.rust-lang.org/book/print.html | 0.825 |
| crawlee | #3 | doc.rust-lang.org/book/print.html | 0.838 | doc.rust-lang.org/book/print.html | 0.825 | doc.rust-lang.org/book/ch17-04-streams.html | 0.825 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.838 | doc.rust-lang.org/book/print.html | 0.838 | doc.rust-lang.org/book/print.html | 0.825 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.838 | doc.rust-lang.org/book/ch17-04-streams.html | 0.825 | doc.rust-lang.org/book/print.html | 0.825 |


**Q49: How do you read a file in Rust?**
*(expects URL containing: `ch12-02-reading-a-file.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #27 | doc.rust-lang.org/book/ch02-00-guessing-game-tutor | 0.790 | doc.rust-lang.org/book/print.html | 0.790 | doc.rust-lang.org/book/print.html | 0.768 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch12-02-reading-a-fi | 0.832 | doc.rust-lang.org/book/ch12-02-reading-a-file.html | 0.832 | doc.rust-lang.org/std/io/struct.Stdin.html | 0.825 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch12-02-reading-a-fi | 0.832 | doc.rust-lang.org/book/ch12-02-reading-a-file.html | 0.832 | doc.rust-lang.org/std/io/struct.Stdin.html | 0.825 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.772 | doc.rust-lang.org/stable/book/print.html | 0.772 | doc.rust-lang.org/nomicon/ffi.html | 0.768 |
| crawlee | #5 | doc.rust-lang.org/book/print.html | 0.772 | doc.rust-lang.org/std/index.html | 0.772 | doc.rust-lang.org/book/print.html | 0.767 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.772 | doc.rust-lang.org/book/print.html | 0.772 | doc.rust-lang.org/std/index.html | 0.770 |
| playwright | #5 | doc.rust-lang.org/book/print.html | 0.772 | doc.rust-lang.org/std/index.html | 0.772 | doc.rust-lang.org/book/print.html | 0.767 |


**Q50: What is the content of the sample file used for testing?**
*(expects URL containing: `ch12-02-reading-a-file.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.685 | doc.rust-lang.org/book/ch12-02-reading-a-file.html | 0.680 | doc.rust-lang.org/book/ch12-04-testing-the-library | 0.647 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.703 | doc.rust-lang.org/stable/book/ch12-02-reading-a-fi | 0.676 | doc.rust-lang.org/book/ch12-02-reading-a-file.html | 0.676 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.703 | doc.rust-lang.org/stable/book/ch12-02-reading-a-fi | 0.676 | doc.rust-lang.org/book/ch12-02-reading-a-file.html | 0.676 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.700 | doc.rust-lang.org/book/print.html | 0.700 | doc.rust-lang.org/stable/book/print.html | 0.671 |
| crawlee | #28 | doc.rust-lang.org/book/print.html | 0.700 | doc.rust-lang.org/book/print.html | 0.671 | doc.rust-lang.org/book/ch12-04-testing-the-library | 0.671 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.700 | doc.rust-lang.org/book/print.html | 0.700 | doc.rust-lang.org/book/print.html | 0.671 |
| playwright | #28 | doc.rust-lang.org/book/print.html | 0.700 | doc.rust-lang.org/book/ch12-04-testing-the-library | 0.671 | doc.rust-lang.org/book/print.html | 0.671 |


**Q51: How do you bring a module into scope with the use keyword?**
*(expects URL containing: `ch07-04-bringing-paths-into-scope-with-the-use-keyword.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.810 | doc.rust-lang.org/book/print.html | 0.803 | doc.rust-lang.org/book/print.html | 0.789 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.794 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.794 | doc.rust-lang.org/stable/book/ch07-04-bringing-pat | 0.794 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.794 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.794 | doc.rust-lang.org/stable/book/ch07-04-bringing-pat | 0.794 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.792 | doc.rust-lang.org/book/print.html | 0.792 | doc.rust-lang.org/book/print.html | 0.792 |
| crawlee | #1 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.792 | doc.rust-lang.org/book/print.html | 0.792 | doc.rust-lang.org/stable/book/ch07-04-bringing-pat | 0.792 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.792 | doc.rust-lang.org/stable/book/print.html | 0.792 | doc.rust-lang.org/book/print.html | 0.792 |
| playwright | #1 | doc.rust-lang.org/stable/book/ch07-04-bringing-pat | 0.792 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.792 | doc.rust-lang.org/book/print.html | 0.792 |


**Q52: What is the purpose of the pub use statement in Rust?**
*(expects URL containing: `ch07-04-bringing-paths-into-scope-with-the-use-keyword.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.775 | doc.rust-lang.org/book/print.html | 0.770 | doc.rust-lang.org/book/ch07-04-bringing-paths-into | 0.770 |
| crawl4ai | #4 | doc.rust-lang.org/reference/macros-by-example.html | 0.800 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.775 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.775 |
| crawl4ai-raw | #4 | doc.rust-lang.org/reference/macros-by-example.html | 0.800 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.775 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.775 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.769 | doc.rust-lang.org/book/print.html | 0.769 | doc.rust-lang.org/book/print.html | 0.766 |
| crawlee | #8 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.777 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.777 | doc.rust-lang.org/stable/book/ch11-03-test-organiz | 0.773 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.769 | doc.rust-lang.org/stable/book/print.html | 0.769 | doc.rust-lang.org/stable/book/print.html | 0.766 |
| playwright | #9 | doc.rust-lang.org/book/ch07-05-separating-modules- | 0.777 | doc.rust-lang.org/stable/book/ch07-05-separating-m | 0.777 | doc.rust-lang.org/book/ch11-03-test-organization.h | 0.773 |


**Q53: What are the two major categories of errors in Rust?**
*(expects URL containing: `ch09-00-error-handling.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.778 | doc.rust-lang.org/book/ch09-00-error-handling.html | 0.775 | doc.rust-lang.org/book/ch12-03-improving-error-han | 0.762 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch09-00-error-handli | 0.782 | doc.rust-lang.org/book/ch09-00-error-handling.html | 0.782 | doc.rust-lang.org/std/result/enum.Result.html | 0.779 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch09-00-error-handli | 0.782 | doc.rust-lang.org/book/ch09-00-error-handling.html | 0.782 | doc.rust-lang.org/std/result/enum.Result.html | 0.779 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.776 | doc.rust-lang.org/stable/book/print.html | 0.776 | doc.rust-lang.org/book/print.html | 0.762 |
| crawlee | #5 | doc.rust-lang.org/book/print.html | 0.776 | doc.rust-lang.org/book/print.html | 0.762 | doc.rust-lang.org/stable/book/ch12-03-improving-er | 0.762 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.776 | doc.rust-lang.org/stable/book/print.html | 0.776 | doc.rust-lang.org/stable/book/print.html | 0.762 |
| playwright | #5 | doc.rust-lang.org/book/print.html | 0.776 | doc.rust-lang.org/stable/book/ch12-03-improving-er | 0.762 | doc.rust-lang.org/book/print.html | 0.762 |


**Q54: How does Rust handle recoverable errors?**
*(expects URL containing: `ch09-00-error-handling.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch09-00-error-handling.html | 0.847 | doc.rust-lang.org/book/print.html | 0.805 | doc.rust-lang.org/book/print.html | 0.772 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch09-00-error-handling.html | 0.817 | doc.rust-lang.org/stable/book/ch09-00-error-handli | 0.817 | doc.rust-lang.org/book/print.html | 0.808 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch09-00-error-handling.html | 0.817 | doc.rust-lang.org/stable/book/ch09-00-error-handli | 0.817 | doc.rust-lang.org/book/print.html | 0.808 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.805 | doc.rust-lang.org/stable/book/print.html | 0.805 | doc.rust-lang.org/book/print.html | 0.791 |
| crawlee | #7 | doc.rust-lang.org/book/print.html | 0.805 | doc.rust-lang.org/book/print.html | 0.791 | doc.rust-lang.org/stable/book/ch09-02-recoverable- | 0.791 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.805 | doc.rust-lang.org/book/print.html | 0.805 | doc.rust-lang.org/book/print.html | 0.791 |
| playwright | #7 | doc.rust-lang.org/book/print.html | 0.805 | doc.rust-lang.org/book/print.html | 0.791 | doc.rust-lang.org/book/ch09-02-recoverable-errors- | 0.791 |


**Q55: How do you create a new, empty vector in Rust?**
*(expects URL containing: `ch08-01-vectors.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch08-01-vectors.html | 0.786 | doc.rust-lang.org/book/ch08-01-vectors.html | 0.785 | doc.rust-lang.org/book/print.html | 0.785 |
| crawl4ai | #5 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.808 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.802 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.798 |
| crawl4ai-raw | #5 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.808 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.802 | doc.rust-lang.org/std/vec/struct.Vec.html | 0.798 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.791 | doc.rust-lang.org/stable/book/print.html | 0.791 | doc.rust-lang.org/book/print.html | 0.782 |
| crawlee | #1 | doc.rust-lang.org/book/ch08-01-vectors.html | 0.804 | doc.rust-lang.org/stable/book/ch08-01-vectors.html | 0.804 | doc.rust-lang.org/book/print.html | 0.791 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.791 | doc.rust-lang.org/stable/book/print.html | 0.791 | doc.rust-lang.org/book/print.html | 0.782 |
| playwright | #1 | doc.rust-lang.org/stable/book/ch08-01-vectors.html | 0.804 | doc.rust-lang.org/book/ch08-01-vectors.html | 0.804 | doc.rust-lang.org/book/ch08-01-vectors.html | 0.791 |


**Q56: What method is used to add elements to a vector in Rust?**
*(expects URL containing: `ch08-01-vectors.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch08-01-vectors.html | 0.817 | doc.rust-lang.org/book/print.html | 0.817 | doc.rust-lang.org/book/print.html | 0.816 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch08-01-vectors.html | 0.842 | doc.rust-lang.org/book/ch08-01-vectors.html | 0.842 | doc.rust-lang.org/book/print.html | 0.842 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch08-01-vectors.html | 0.842 | doc.rust-lang.org/book/ch08-01-vectors.html | 0.842 | doc.rust-lang.org/book/print.html | 0.842 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.842 | doc.rust-lang.org/book/print.html | 0.842 | doc.rust-lang.org/book/print.html | 0.817 |
| crawlee | #1 | doc.rust-lang.org/book/ch08-01-vectors.html | 0.842 | doc.rust-lang.org/stable/book/ch08-01-vectors.html | 0.842 | doc.rust-lang.org/book/print.html | 0.842 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.842 | doc.rust-lang.org/stable/book/print.html | 0.842 | doc.rust-lang.org/stable/book/print.html | 0.817 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.842 | doc.rust-lang.org/stable/book/ch08-01-vectors.html | 0.842 | doc.rust-lang.org/book/ch08-01-vectors.html | 0.842 |


**Q57: What is the purpose of the `if let` syntax in Rust?**
*(expects URL containing: `ch06-03-if-let.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch06-03-if-let.html | 0.852 | doc.rust-lang.org/book/print.html | 0.851 | doc.rust-lang.org/book/ch06-03-if-let.html | 0.851 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch06-03-if-let.html | 0.835 | doc.rust-lang.org/stable/book/ch06-03-if-let.html | 0.835 | doc.rust-lang.org/book/ch03-05-control-flow.html | 0.828 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch06-03-if-let.html | 0.835 | doc.rust-lang.org/stable/book/ch06-03-if-let.html | 0.835 | doc.rust-lang.org/book/ch03-05-control-flow.html | 0.828 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.820 | doc.rust-lang.org/stable/book/print.html | 0.820 | doc.rust-lang.org/stable/book/print.html | 0.812 |
| crawlee | #26 | doc.rust-lang.org/book/ch03-05-control-flow.html | 0.820 | doc.rust-lang.org/stable/book/ch03-05-control-flow | 0.820 | doc.rust-lang.org/book/print.html | 0.820 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.820 | doc.rust-lang.org/book/print.html | 0.820 | doc.rust-lang.org/book/print.html | 0.812 |
| playwright | #25 | doc.rust-lang.org/stable/book/ch03-05-control-flow | 0.820 | doc.rust-lang.org/book/ch03-05-control-flow.html | 0.820 | doc.rust-lang.org/book/print.html | 0.820 |


**Q58: How does the `let...else` syntax improve control flow in Rust?**
*(expects URL containing: `ch06-03-if-let.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.848 | doc.rust-lang.org/book/ch06-03-if-let.html | 0.848 | doc.rust-lang.org/book/ch06-03-if-let.html | 0.843 |
| crawl4ai | #4 | doc.rust-lang.org/std/option/enum.Option.html | 0.813 | doc.rust-lang.org/book/print.html | 0.813 | doc.rust-lang.org/book/ch03-05-control-flow.html | 0.813 |
| crawl4ai-raw | #4 | doc.rust-lang.org/std/option/enum.Option.html | 0.813 | doc.rust-lang.org/book/print.html | 0.813 | doc.rust-lang.org/book/ch03-05-control-flow.html | 0.813 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.807 | doc.rust-lang.org/stable/book/print.html | 0.807 | doc.rust-lang.org/book/print.html | 0.790 |
| crawlee | #4 | doc.rust-lang.org/stable/book/ch03-05-control-flow | 0.807 | doc.rust-lang.org/book/print.html | 0.807 | doc.rust-lang.org/book/ch03-05-control-flow.html | 0.807 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.807 | doc.rust-lang.org/stable/book/print.html | 0.807 | doc.rust-lang.org/book/print.html | 0.790 |
| playwright | #4 | doc.rust-lang.org/book/print.html | 0.807 | doc.rust-lang.org/book/ch03-05-control-flow.html | 0.807 | doc.rust-lang.org/stable/book/ch03-05-control-flow | 0.807 |


**Q59: What are the keywords currently in use in Rust?**
*(expects URL containing: `appendix-01-keywords.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.837 | doc.rust-lang.org/book/appendix-01-keywords.html | 0.827 | doc.rust-lang.org/book/print.html | 0.816 |
| crawl4ai | #3 | doc.rust-lang.org/book/ch03-00-common-programming- | 0.818 | doc.rust-lang.org/stable/book/ch03-00-common-progr | 0.818 | doc.rust-lang.org/book/appendix-01-keywords.html | 0.812 |
| crawl4ai-raw | #3 | doc.rust-lang.org/book/ch03-00-common-programming- | 0.818 | doc.rust-lang.org/stable/book/ch03-00-common-progr | 0.818 | doc.rust-lang.org/book/appendix-01-keywords.html | 0.812 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.816 | doc.rust-lang.org/stable/book/print.html | 0.816 | doc.rust-lang.org/stable/book/print.html | 0.814 |
| crawlee | #3 | doc.rust-lang.org/book/print.html | 0.816 | doc.rust-lang.org/book/print.html | 0.814 | doc.rust-lang.org/book/appendix-01-keywords.html | 0.814 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.816 | doc.rust-lang.org/stable/book/print.html | 0.816 | doc.rust-lang.org/stable/book/print.html | 0.814 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.816 | doc.rust-lang.org/book/appendix-01-keywords.html | 0.814 | doc.rust-lang.org/book/print.html | 0.814 |


**Q60: How can you use a keyword as an identifier in Rust?**
*(expects URL containing: `appendix-01-keywords.html`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.846 | doc.rust-lang.org/book/appendix-01-keywords.html | 0.846 | doc.rust-lang.org/book/appendix-01-keywords.html | 0.838 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.846 | doc.rust-lang.org/book/appendix-01-keywords.html | 0.846 | doc.rust-lang.org/book/print.html | 0.822 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.846 | doc.rust-lang.org/book/appendix-01-keywords.html | 0.846 | doc.rust-lang.org/book/print.html | 0.822 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.846 | doc.rust-lang.org/book/print.html | 0.846 | doc.rust-lang.org/book/print.html | 0.817 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.846 | doc.rust-lang.org/book/appendix-01-keywords.html | 0.846 | doc.rust-lang.org/book/print.html | 0.817 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.846 | doc.rust-lang.org/stable/book/print.html | 0.846 | doc.rust-lang.org/stable/book/print.html | 0.817 |
| playwright | #1 | doc.rust-lang.org/book/appendix-01-keywords.html | 0.846 | doc.rust-lang.org/book/print.html | 0.846 | doc.rust-lang.org/book/appendix-01-keywords.html | 0.817 |


</details>

## smittenkitchen

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai | 75% (30/40) | 90% (36/40) | 92% (37/40) | 92% (37/40) | 95% (38/40) | 0.828 | 773 | 200 |
| crawl4ai-raw | 75% (30/40) | 90% (36/40) | 92% (37/40) | 92% (37/40) | 95% (38/40) | 0.828 | 773 | 200 |
| playwright | 40% (16/40) | 48% (19/40) | 60% (24/40) | 62% (25/40) | 78% (31/40) | 0.481 | 3029 | 200 |
| colly+md | 25% (10/40) | 35% (14/40) | 40% (16/40) | 50% (20/40) | 50% (20/40) | 0.313 | 3708 | 199 |
| crawlee | 25% (10/40) | 30% (12/40) | 30% (12/40) | 30% (12/40) | 32% (13/40) | 0.277 | 4167 | 203 |
| markcrawl | 18% (7/40) | 28% (11/40) | 28% (11/40) | 30% (12/40) | 30% (12/40) | 0.224 | 10115 | 200 |
| scrapy+md | 2% (1/40) | 2% (1/40) | 5% (2/40) | 5% (2/40) | 5% (2/40) | 0.031 | 18860 | 138 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for smittenkitchen</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What are some recipes featured in the greens category?**
*(expects URL containing: `greens`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2022/11/green-angel-hair-with-g | 0.712 | smittenkitchen.com/2009/12/how-to-host-brunch-and- | 0.678 | smittenkitchen.com/2013/01/pasta-and-white-beans-w | 0.678 |
| crawl4ai | #3 | smittenkitchen.com/./recipes/vegetable/green-beans | 0.662 | smittenkitchen.com/recipes/ | 0.654 | smittenkitchen.com/./recipes/vegetable/greens/esca | 0.648 |
| crawl4ai-raw | #3 | smittenkitchen.com/./recipes/vegetable/green-beans | 0.662 | smittenkitchen.com/recipes/ | 0.656 | smittenkitchen.com/./recipes/vegetable/greens/esca | 0.648 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.646 | smittenkitchen.com/2012/08/mediterranean-baked-fet | 0.639 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.637 |
| crawlee | miss | smittenkitchen.com/recipes/ | 0.668 | smittenkitchen.com/reading/cookbook-index/ | 0.634 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.633 |
| colly+md | miss | smittenkitchen.com/2025/12/winter-cabbage-salad-wi | 0.644 | smittenkitchen.com/recipes/ | 0.643 | smittenkitchen.com/reading/cookbook-index/ | 0.634 |
| playwright | #14 | smittenkitchen.com/recipes/ | 0.643 | smittenkitchen.com/recipes | 0.643 | smittenkitchen.com/reading/cookbook-index/ | 0.634 |


**Q2: What is the first recipe listed on the greens page?**
*(expects URL containing: `greens`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2022/11/green-angel-hair-with-g | 0.728 | smittenkitchen.com/2009/12/how-to-host-brunch-and- | 0.688 | smittenkitchen.com/2022/11/green-angel-hair-with-g | 0.682 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/vegetable/greens/esca | 0.665 | smittenkitchen.com/./recipes/vegetable/green-beans | 0.663 | smittenkitchen.com/./recipes/vegetable/greens/endi | 0.653 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/vegetable/greens/esca | 0.665 | smittenkitchen.com/./recipes/vegetable/green-beans | 0.663 | smittenkitchen.com/./recipes/vegetable/greens/endi | 0.653 |
| scrapy+md | miss | smittenkitchen.com/2012/08/mediterranean-baked-fet | 0.689 | smittenkitchen.com/2012/08/mediterranean-baked-fet | 0.685 | smittenkitchen.com/2008/04/cauliflower-bean-and-fe | 0.676 |
| crawlee | miss | smittenkitchen.com/recipes/ | 0.670 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.666 | smittenkitchen.com/?random&timestamp=1777919490717 | 0.666 |
| colly+md | miss | smittenkitchen.com/2026/04/braised-leeks-and-lenti | 0.684 | smittenkitchen.com/2025/12/winter-cabbage-salad-wi | 0.668 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.667 |
| playwright | #34 | smittenkitchen.com/?random&timestamp=1777948695303 | 0.677 | smittenkitchen.com/subscribe/ | 0.659 | smittenkitchen.com/recipes/ | 0.654 |


**Q3: What does the Smitten Kitchen newsletter include?**
*(expects URL containing: `subscribe`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | smittenkitchen.com/privacy-policy/ | 0.775 | smittenkitchen.com/subscribe/ | 0.750 | smittenkitchen.com/subscribe/ | 0.747 |
| crawl4ai | #2 | smittenkitchen.com/about/faq/ | 0.776 | smittenkitchen.com/subscribe/ | 0.759 | smittenkitchen.com/travel/two-weeks-in-italy/ | 0.751 |
| crawl4ai-raw | #2 | smittenkitchen.com/about/faq/ | 0.776 | smittenkitchen.com/subscribe/ | 0.759 | smittenkitchen.com/travel/two-weeks-in-italy/ | 0.751 |
| scrapy+md | miss | smittenkitchen.com/privacy-policy/ | 0.754 | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.712 | smittenkitchen.com/2012/02/lasagna-bolognese/ | 0.711 |
| crawlee | #1 | smittenkitchen.com/subscribe/ | 0.774 | smittenkitchen.com/about/faq/ | 0.742 | smittenkitchen.com/about/ | 0.733 |
| colly+md | #1 | smittenkitchen.com/subscribe/ | 0.774 | smittenkitchen.com/about/faq/ | 0.742 | smittenkitchen.com/subscribe/ | 0.731 |
| playwright | #1 | smittenkitchen.com/subscribe/ | 0.774 | smittenkitchen.com/about/faq/ | 0.742 | smittenkitchen.com/about/ | 0.733 |


**Q4: How can I unsubscribe from the Smitten Kitchen newsletter?**
*(expects URL containing: `subscribe`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | smittenkitchen.com/privacy-policy/ | 0.752 | smittenkitchen.com/subscribe/ | 0.703 | smittenkitchen.com/subscribe/ | 0.693 |
| crawl4ai | #2 | smittenkitchen.com/about/faq/ | 0.712 | smittenkitchen.com/subscribe/ | 0.685 | smittenkitchen.com/subscribe/ | 0.679 |
| crawl4ai-raw | #2 | smittenkitchen.com/about/faq/ | 0.712 | smittenkitchen.com/subscribe/ | 0.685 | smittenkitchen.com/subscribe/ | 0.679 |
| scrapy+md | miss | smittenkitchen.com/privacy-policy/ | 0.747 | smittenkitchen.com/2007/02/sour-cream-bran-muffins | 0.666 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.659 |
| crawlee | #1 | smittenkitchen.com/subscribe/ | 0.738 | smittenkitchen.com/about/faq/ | 0.713 | smittenkitchen.com/subscribe/ | 0.701 |
| colly+md | #1 | smittenkitchen.com/subscribe/ | 0.738 | smittenkitchen.com/about/faq/ | 0.713 | smittenkitchen.com/subscribe/ | 0.701 |
| playwright | #1 | smittenkitchen.com/subscribe/ | 0.738 | smittenkitchen.com/about/faq/ | 0.713 | smittenkitchen.com/subscribe/ | 0.701 |


**Q5: What are some recipes that include bananas?**
*(expects URL containing: `bananas`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.734 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.702 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.695 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/fruit/bananas/?format | 0.679 | smittenkitchen.com/recipes/ | 0.622 | smittenkitchen.com/./recipes/fruit/orange/?format= | 0.596 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/fruit/bananas/?format | 0.679 | smittenkitchen.com/recipes/ | 0.622 | smittenkitchen.com/./recipes/fruit/orange/?format= | 0.596 |
| scrapy+md | miss | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.703 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.699 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.694 |
| crawlee | miss | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.725 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.703 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.696 |
| colly+md | miss | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.703 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.694 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.690 |
| playwright | #2 | smittenkitchen.com/ | 0.601 | smittenkitchen.com/recipes/fruit/bananas/?format=p | 0.593 | smittenkitchen.com/recipes | 0.592 |


**Q6: What are some breakfast recipes available on Smitten Kitchen?**
*(expects URL containing: `breakfast`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2020/10/morning-glory-breakfast | 0.719 | smittenkitchen.com/2020/10/morning-glory-breakfast | 0.708 | smittenkitchen.com/2010/05/scrambled-egg-toast/ | 0.707 |
| crawl4ai | #4 | smittenkitchen.com/./recipes/course/muffin/?format | 0.764 | smittenkitchen.com/./recipes/course/pancakes/?form | 0.756 | smittenkitchen.com/./recipes/ingredient/eggs/?form | 0.751 |
| crawl4ai-raw | #4 | smittenkitchen.com/./recipes/course/muffin/?format | 0.764 | smittenkitchen.com/./recipes/course/pancakes/?form | 0.756 | smittenkitchen.com/./recipes/ingredient/eggs/?form | 0.751 |
| scrapy+md | #4 | smittenkitchen.com/recipes/ | 0.726 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.724 | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.718 |
| crawlee | #1 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.736 | smittenkitchen.com/2023/07/raspberry-streusel-muff | 0.727 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.717 |
| colly+md | #3 | smittenkitchen.com/recipes/ | 0.728 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.724 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.717 |
| playwright | #4 | smittenkitchen.com/recipes/ | 0.728 | smittenkitchen.com/recipes | 0.728 | smittenkitchen.com/book/ | 0.679 |


**Q7: What are some meat recipes available on Smitten Kitchen?**
*(expects URL containing: `meat`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | smittenkitchen.com/subscribe/ | 0.688 | smittenkitchen.com/2016/02/everyday-meatballs/ | 0.671 | smittenkitchen.com/2018/01/sheet-pan-meatballs-wit | 0.661 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/ingredient/meat/beef/ | 0.768 | smittenkitchen.com/./recipes/ingredient/meat/pork- | 0.757 | smittenkitchen.com/./recipes/ingredient/meat/turke | 0.748 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/ingredient/meat/beef/ | 0.768 | smittenkitchen.com/./recipes/ingredient/meat/pork- | 0.757 | smittenkitchen.com/./recipes/ingredient/meat/turke | 0.748 |
| scrapy+md | #1 | smittenkitchen.com/2014/04/lamb-meatballs-with-fet | 0.726 | smittenkitchen.com/2014/04/lamb-meatballs-with-fet | 0.726 | smittenkitchen.com/2014/04/lamb-meatballs-with-fet | 0.724 |
| crawlee | #50 | smittenkitchen.com/subscribe/ | 0.700 | smittenkitchen.com/recipes/ | 0.696 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.687 |
| colly+md | #5 | smittenkitchen.com/subscribe/ | 0.700 | smittenkitchen.com/recipes/ | 0.681 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.678 |
| playwright | #5 | smittenkitchen.com/subscribe/ | 0.700 | smittenkitchen.com/recipes | 0.681 | smittenkitchen.com/recipes/ | 0.681 |


**Q8: What is the main focus of the Smitten Kitchen blog?**
*(expects URL containing: `about`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.691 | smittenkitchen.com/books/ | 0.690 | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.678 |
| crawl4ai | #1 | smittenkitchen.com/about/faq/ | 0.735 | smittenkitchen.com/./recipes/fruit/mango/?format=p | 0.713 | smittenkitchen.com/./recipes/kid-favorites/?format | 0.713 |
| crawl4ai-raw | #1 | smittenkitchen.com/about/faq/ | 0.735 | smittenkitchen.com/./recipes/fruit/mango/?format=p | 0.713 | smittenkitchen.com/./recipes/kid-favorites/?format | 0.713 |
| scrapy+md | miss | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.709 | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.708 | smittenkitchen.com/2012/02/lasagna-bolognese/ | 0.708 |
| crawlee | #2 | smittenkitchen.com/subscribe/ | 0.707 | smittenkitchen.com/about/ | 0.692 | smittenkitchen.com/about/ | 0.691 |
| colly+md | #8 | smittenkitchen.com/subscribe/ | 0.707 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.701 | smittenkitchen.com/2022/04/lemon-cream-meringues/ | 0.690 |
| playwright | #2 | smittenkitchen.com/subscribe/ | 0.707 | smittenkitchen.com/about/ | 0.692 | smittenkitchen.com/subscribe/ | 0.686 |


**Q9: Who is the author of Smitten Kitchen and what is her background?**
*(expects URL containing: `about`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/books/ | 0.681 | smittenkitchen.com/books/ | 0.676 | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.664 |
| crawl4ai | #2 | smittenkitchen.com/events/ | 0.669 | smittenkitchen.com/about/ | 0.660 | smittenkitchen.com/about/faq/ | 0.653 |
| crawl4ai-raw | #2 | smittenkitchen.com/events/ | 0.669 | smittenkitchen.com/about/ | 0.660 | smittenkitchen.com/about/faq/ | 0.653 |
| scrapy+md | miss | smittenkitchen.com/2017/09/pizza-beans/ | 0.595 | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.582 | smittenkitchen.com/2018/10/even-more-perfect-apple | 0.580 |
| crawlee | #3 | smittenkitchen.com/book/ | 0.666 | smittenkitchen.com/books/ | 0.666 | smittenkitchen.com/about/faq/ | 0.657 |
| colly+md | #1 | smittenkitchen.com/about/faq/ | 0.657 | smittenkitchen.com/books/ | 0.652 | smittenkitchen.com/subscribe/ | 0.639 |
| playwright | #1 | smittenkitchen.com/about/faq/ | 0.657 | smittenkitchen.com/book/ | 0.652 | smittenkitchen.com/about/ | 0.648 |


**Q10: What were the main goals of the trip to London?**
*(expects URL containing: `five-days-in-london`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.517 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.514 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.511 |
| crawl4ai | #1 | smittenkitchen.com/travel/five-days-in-london/ | 0.595 | smittenkitchen.com/travel/five-days-in-london/ | 0.586 | smittenkitchen.com/travel/five-days-in-london/ | 0.583 |
| crawl4ai-raw | #1 | smittenkitchen.com/travel/five-days-in-london/ | 0.595 | smittenkitchen.com/travel/five-days-in-london/ | 0.586 | smittenkitchen.com/travel/five-days-in-london/ | 0.583 |
| scrapy+md | miss | smittenkitchen.com/2022/03/castle-breakfast/ | 0.484 | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.416 | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.416 |
| crawlee | #1 | smittenkitchen.com/travel/five-days-in-london/ | 0.612 | smittenkitchen.com/travel/five-days-in-london/ | 0.611 | smittenkitchen.com/travel/five-days-in-london/ | 0.608 |
| colly+md | #1 | smittenkitchen.com/travel/five-days-in-london/ | 0.612 | smittenkitchen.com/travel/five-days-in-london/ | 0.611 | smittenkitchen.com/travel/five-days-in-london/ | 0.608 |
| playwright | #1 | smittenkitchen.com/travel/five-days-in-london/ | 0.612 | smittenkitchen.com/travel/five-days-in-london/ | 0.611 | smittenkitchen.com/travel/five-days-in-london/ | 0.608 |


**Q11: Which restaurant had the best fish and chips according to the author?**
*(expects URL containing: `five-days-in-london`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2013/10/miso-sweet-potato-and-b | 0.579 | smittenkitchen.com/2011/02/green-bean-salad-with-p | 0.575 | smittenkitchen.com/travel/debs-new-york/ | 0.568 |
| crawl4ai | #20 | smittenkitchen.com/travel/debs-new-york/ | 0.577 | smittenkitchen.com/travel/debs-new-york/ | 0.565 | smittenkitchen.com/travel/debs-new-york/ | 0.565 |
| crawl4ai-raw | #20 | smittenkitchen.com/travel/debs-new-york/ | 0.577 | smittenkitchen.com/travel/debs-new-york/ | 0.565 | smittenkitchen.com/travel/debs-new-york/ | 0.565 |
| scrapy+md | miss | smittenkitchen.com/2007/02/sour-cream-bran-muffins | 0.519 | smittenkitchen.com/2017/09/pizza-beans/ | 0.508 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.504 |
| crawlee | #26 | smittenkitchen.com/travel/debs-new-york/ | 0.577 | smittenkitchen.com/travel/debs-new-york/ | 0.568 | smittenkitchen.com/travel/debs-new-york/ | 0.567 |
| colly+md | #47 | smittenkitchen.com/travel/debs-new-york/ | 0.577 | smittenkitchen.com/travel/debs-new-york/ | 0.568 | smittenkitchen.com/travel/debs-new-york/ | 0.567 |
| playwright | #50 | smittenkitchen.com/travel/debs-new-york/ | 0.577 | smittenkitchen.com/travel/debs-new-york/ | 0.568 | smittenkitchen.com/travel/debs-new-york/ | 0.567 |


**Q12: What are some recommended restaurants in Barcelona from the trip to Spain?**
*(expects URL containing: `a-few-favorites-from-spain`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/travel/debs-new-york/ | 0.574 | smittenkitchen.com/travel/ | 0.572 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.571 |
| crawl4ai | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.713 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.671 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.634 |
| crawl4ai-raw | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.713 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.671 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.634 |
| scrapy+md | miss | smittenkitchen.com/2022/03/castle-breakfast/ | 0.537 | smittenkitchen.com/2021/02/baked-feta-with-tomatoe | 0.533 | smittenkitchen.com/2021/02/baked-feta-with-tomatoe | 0.533 |
| crawlee | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.747 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.740 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.693 |
| colly+md | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.747 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.740 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.693 |
| playwright | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.747 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.740 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.693 |


**Q13: What is a notable meal mentioned from the Hostal de la Granota in Costa Brava?**
*(expects URL containing: `a-few-favorites-from-spain`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2010/03/spinach-and-chickpeas/ | 0.603 | smittenkitchen.com/2013/01/pasta-and-white-beans-w | 0.571 | smittenkitchen.com/2007/07/pearl-couscous-with-oli | 0.566 |
| crawl4ai | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.637 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.632 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.629 |
| crawl4ai-raw | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.637 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.632 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.629 |
| scrapy+md | miss | smittenkitchen.com/2012/08/mediterranean-baked-fet | 0.565 | smittenkitchen.com/2012/08/mediterranean-baked-fet | 0.562 | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.559 |
| crawlee | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.652 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.633 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.624 |
| colly+md | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.652 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.636 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.633 |
| playwright | #1 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.652 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.636 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.633 |


**Q14: What items are included in the Smitten Kitchen shop?**
*(expects URL containing: `shop`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/books/ | 0.653 | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.647 | smittenkitchen.com/books/ | 0.642 |
| crawl4ai | #1 | smittenkitchen.com/shop/ | 0.740 | smittenkitchen.com/shop/ | 0.726 | smittenkitchen.com/about/faq/ | 0.715 |
| crawl4ai-raw | #1 | smittenkitchen.com/shop/ | 0.740 | smittenkitchen.com/about/faq/ | 0.715 | smittenkitchen.com/about/ | 0.698 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.684 | smittenkitchen.com/2017/09/pizza-beans/ | 0.674 | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.674 |
| crawlee | #1 | smittenkitchen.com/shop/ | 0.705 | smittenkitchen.com/shop/ | 0.696 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.686 |
| colly+md | #1 | smittenkitchen.com/shop/ | 0.697 | smittenkitchen.com/shop/ | 0.696 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.686 |
| playwright | #1 | smittenkitchen.com/shop/ | 0.705 | smittenkitchen.com/shop/ | 0.696 | smittenkitchen.com/shop/ | 0.678 |


**Q15: Where can I find kitchen supply stores that ship domestically?**
*(expects URL containing: `shop`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2013/01/carrot-soup-with-tahini | 0.575 | smittenkitchen.com/books/ | 0.565 | smittenkitchen.com/2014/11/pretzel-parker-house-ro | 0.554 |
| crawl4ai | #1 | smittenkitchen.com/shop/ | 0.583 | smittenkitchen.com/about/faq/ | 0.550 | smittenkitchen.com/shop/ | 0.542 |
| crawl4ai-raw | #1 | smittenkitchen.com/shop/ | 0.598 | smittenkitchen.com/shop/ | 0.583 | smittenkitchen.com/about/faq/ | 0.550 |
| scrapy+md | miss | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.518 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.505 | smittenkitchen.com/2008/04/cauliflower-bean-and-fe | 0.496 |
| crawlee | #1 | smittenkitchen.com/shop/ | 0.626 | smittenkitchen.com/shop/ | 0.623 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.604 |
| colly+md | #1 | smittenkitchen.com/shop/ | 0.626 | smittenkitchen.com/shop/ | 0.623 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.604 |
| playwright | #1 | smittenkitchen.com/shop/ | 0.626 | smittenkitchen.com/shop/ | 0.623 | smittenkitchen.com/shop/ | 0.575 |


**Q16: What are some Russian recipes available on Smitten Kitchen?**
*(expects URL containing: `russian`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2006/12/russian-tea-cakes/ | 0.712 | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.697 | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.689 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/cuisine/russian/?form | 0.808 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.731 | smittenkitchen.com/./recipes/course/bread/?format= | 0.716 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/cuisine/russian/?form | 0.808 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.731 | smittenkitchen.com/./recipes/course/bread/?format= | 0.716 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.672 | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.671 | smittenkitchen.com/2021/02/baked-feta-with-tomatoe | 0.666 |
| crawlee | miss | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.675 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.663 | smittenkitchen.com/ | 0.662 |
| colly+md | #1 | smittenkitchen.com/recipes/cuisine/russian/?format | 0.713 | smittenkitchen.com/2022/04/lemon-cream-meringues/ | 0.681 | smittenkitchen.com/ | 0.669 |
| playwright | #1 | smittenkitchen.com/recipes/cuisine/russian/?format | 0.713 | smittenkitchen.com/recipes/ | 0.661 | smittenkitchen.com/recipes | 0.661 |


**Q17: When was the Russian cuisine page first published?**
*(expects URL containing: `russian`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.593 | smittenkitchen.com/2015/01/my-ultimate-chicken-noo | 0.593 | smittenkitchen.com/2006/12/russian-tea-cakes/ | 0.581 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/cuisine/russian/?form | 0.655 | smittenkitchen.com/./recipes/course/savory-condime | 0.595 | smittenkitchen.com/./recipes/course/put-an-egg-on- | 0.588 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/cuisine/russian/?form | 0.655 | smittenkitchen.com/./recipes/course/savory-condime | 0.595 | smittenkitchen.com/./recipes/course/put-an-egg-on- | 0.588 |
| scrapy+md | miss | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.580 | smittenkitchen.com/2021/02/baked-feta-with-tomatoe | 0.580 | smittenkitchen.com/2008/04/cauliflower-bean-and-fe | 0.563 |
| crawlee | miss | smittenkitchen.com/2022/04/lemon-cream-meringues/ | 0.595 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.581 | smittenkitchen.com/reading/ | 0.577 |
| colly+md | #3 | smittenkitchen.com/2022/04/lemon-cream-meringues/ | 0.585 | smittenkitchen.com/2022/04/lemon-cream-meringues/ | 0.583 | smittenkitchen.com/recipes/cuisine/russian/?format | 0.582 |
| playwright | #1 | smittenkitchen.com/recipes/cuisine/russian/?format | 0.583 | smittenkitchen.com/reading/ | 0.581 | smittenkitchen.com/?random&timestamp=1777948695303 | 0.566 |


**Q18: What are some recipes that are freezer friendly?**
*(expects URL containing: `freezer-friendly`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2008/01/lemon-bars/ | 0.704 | smittenkitchen.com/2025/07/chipwich-ice-cream-cake | 0.703 | smittenkitchen.com/2023/04/hash-brown-patties/ | 0.686 |
| crawl4ai | #2 | smittenkitchen.com/subscribe/ | 0.704 | smittenkitchen.com/./recipes/method/freezer-friend | 0.665 | smittenkitchen.com/ | 0.642 |
| crawl4ai-raw | #2 | smittenkitchen.com/subscribe/ | 0.704 | smittenkitchen.com/./recipes/method/freezer-friend | 0.665 | smittenkitchen.com/ | 0.642 |
| scrapy+md | miss | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.699 | smittenkitchen.com/2012/02/lasagna-bolognese/ | 0.699 | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.699 |
| crawlee | miss | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.685 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.685 | smittenkitchen.com/2025/05/one-pan-ditalini-and-pe | 0.682 |
| colly+md | miss | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.685 | smittenkitchen.com/2026/02/miso-chicken-and-rice/# | 0.685 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.685 |
| playwright | #17 | smittenkitchen.com/subscribe/ | 0.658 | smittenkitchen.com/recipes | 0.640 | smittenkitchen.com/recipes/ | 0.640 |


**Q19: What are some dumpling recipes available on Smitten Kitchen?**
*(expects URL containing: `dumplings`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2013/05/spring-vegetable-potsti | 0.722 | smittenkitchen.com/2007/02/on-obsessiveness-and-ol | 0.720 | smittenkitchen.com/2013/05/spring-vegetable-potsti | 0.717 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.753 | smittenkitchen.com/./recipes/ingredient/tofu/?form | 0.708 | smittenkitchen.com/./recipes/cuisine/chinese/?form | 0.691 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.753 | smittenkitchen.com/./recipes/ingredient/tofu/?form | 0.708 | smittenkitchen.com/./recipes/cuisine/chinese/?form | 0.691 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.668 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.652 | smittenkitchen.com/2017/09/pizza-beans/ | 0.651 |
| crawlee | miss | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.655 | smittenkitchen.com/recipes/ | 0.646 | smittenkitchen.com/about/faq/ | 0.646 |
| colly+md | #7 | smittenkitchen.com/recipes/ | 0.674 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.652 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.648 |
| playwright | #5 | smittenkitchen.com/recipes | 0.674 | smittenkitchen.com/recipes/ | 0.674 | smittenkitchen.com/about/faq/ | 0.646 |


**Q20: When was the dumpling recipe page first published?**
*(expects URL containing: `dumplings`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2013/05/spring-vegetable-potsti | 0.664 | smittenkitchen.com/2007/02/on-obsessiveness-and-ol | 0.649 | smittenkitchen.com/2007/02/on-obsessiveness-and-ol | 0.645 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.636 | smittenkitchen.com/./recipes/sweets/ice-cream-sorb | 0.628 | smittenkitchen.com/./recipes/course/savory-condime | 0.623 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/course/dumplings/?for | 0.636 | smittenkitchen.com/./recipes/sweets/ice-cream-sorb | 0.628 | smittenkitchen.com/./recipes/course/savory-condime | 0.623 |
| scrapy+md | miss | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.624 | smittenkitchen.com/2006/11/chocolate-chip-sour-cre | 0.604 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.593 |
| crawlee | miss | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.615 | smittenkitchen.com/./recipes/sweets/pudding/?forma | 0.606 | smittenkitchen.com/./recipes/vegetable/cabbage/?fo | 0.605 |
| colly+md | miss | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.624 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.624 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.624 |
| playwright | miss | smittenkitchen.com/recipes/cuisine/portuguese/?for | 0.607 | smittenkitchen.com/recipes/vegetable/cabbage/?form | 0.607 | smittenkitchen.com/contact/ | 0.606 |


**Q21: What is a recipe featured on the quick recipes page?**
*(expects URL containing: `quick`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/subscribe/ | 0.667 | smittenkitchen.com/2008/10/twice-baked-shortbread- | 0.663 | smittenkitchen.com/subscribe/ | 0.655 |
| crawl4ai | miss | smittenkitchen.com/about/faq/ | 0.690 | smittenkitchen.com/./recipes/method/instant-pot/?f | 0.686 | smittenkitchen.com/about/faq/ | 0.676 |
| crawl4ai-raw | miss | smittenkitchen.com/about/faq/ | 0.690 | smittenkitchen.com/./recipes/method/instant-pot/?f | 0.686 | smittenkitchen.com/about/faq/ | 0.676 |
| scrapy+md | miss | smittenkitchen.com/2016/02/miso-black-sesame-caram | 0.689 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.683 | smittenkitchen.com/2012/02/lasagna-bolognese/ | 0.683 |
| crawlee | miss | smittenkitchen.com/about/faq/ | 0.694 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.681 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.676 |
| colly+md | miss | smittenkitchen.com/about/faq/ | 0.694 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.693 | smittenkitchen.com/2022/04/lemon-cream-meringues/ | 0.683 |
| playwright | miss | smittenkitchen.com/about/faq/ | 0.694 | smittenkitchen.com/?random&timestamp=1777948695303 | 0.680 | smittenkitchen.com/subscribe/ | 0.666 |


**Q22: How can I view the quick recipes in a list format?**
*(expects URL containing: `quick`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/subscribe/ | 0.670 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.662 | smittenkitchen.com/2010/03/spinach-and-chickpeas/ | 0.641 |
| crawl4ai | miss | smittenkitchen.com/about/faq/ | 0.692 | smittenkitchen.com/about/faq/ | 0.680 | smittenkitchen.com/about/faq/ | 0.666 |
| crawl4ai-raw | miss | smittenkitchen.com/about/faq/ | 0.692 | smittenkitchen.com/about/faq/ | 0.680 | smittenkitchen.com/about/faq/ | 0.666 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.662 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.658 | smittenkitchen.com/2016/02/miso-black-sesame-caram | 0.654 |
| crawlee | miss | smittenkitchen.com/about/faq/ | 0.678 | smittenkitchen.com/about/faq/ | 0.675 | smittenkitchen.com/about/faq/ | 0.675 |
| colly+md | miss | smittenkitchen.com/about/faq/ | 0.678 | smittenkitchen.com/about/faq/ | 0.675 | smittenkitchen.com/about/faq/ | 0.675 |
| playwright | miss | smittenkitchen.com/about/faq/ | 0.678 | smittenkitchen.com/about/faq/ | 0.675 | smittenkitchen.com/about/faq/ | 0.675 |


**Q23: What is a recipe featured on the picnics page?**
*(expects URL containing: `picnics`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2015/05/pasta-salad-with-roaste | 0.688 | smittenkitchen.com/2009/12/how-to-host-brunch-and- | 0.670 | smittenkitchen.com/2009/01/warm-butternut-squash-a | 0.667 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/course/picnics/?forma | 0.704 | smittenkitchen.com/./recipes/vegetable/peppers/?fo | 0.703 | smittenkitchen.com/./recipes/course/salad/?format= | 0.702 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/course/picnics/?forma | 0.704 | smittenkitchen.com/./recipes/vegetable/peppers/?fo | 0.703 | smittenkitchen.com/./recipes/course/salad/?format= | 0.702 |
| scrapy+md | miss | smittenkitchen.com/2012/08/charred-pepper-steak-sa | 0.699 | smittenkitchen.com/2008/04/cauliflower-bean-and-fe | 0.694 | smittenkitchen.com/2008/04/cauliflower-bean-and-fe | 0.692 |
| crawlee | miss | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.725 | smittenkitchen.com/?random&timestamp=1777919490717 | 0.687 | smittenkitchen.com/2008/04/lemon-yogurt-anything-c | 0.685 |
| colly+md | miss | smittenkitchen.com/2026/04/braised-leeks-and-lenti | 0.702 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.681 | smittenkitchen.com/2026/02/banana-chocolate-chip-c | 0.680 |
| playwright | #28 | smittenkitchen.com/?random&timestamp=1777948695303 | 0.697 | smittenkitchen.com/recipes/ | 0.668 | smittenkitchen.com/recipes | 0.668 |


**Q24: How many recipes are listed under the picnics category?**
*(expects URL containing: `picnics`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2015/05/pasta-salad-with-roaste | 0.653 | smittenkitchen.com/2016/05/chicken-gyro-salad/ | 0.634 | smittenkitchen.com/2009/12/how-to-host-brunch-and- | 0.629 |
| crawl4ai | #2 | smittenkitchen.com/recipes/ | 0.672 | smittenkitchen.com/./recipes/course/picnics/?forma | 0.670 | smittenkitchen.com/./recipes/course/salad/?format= | 0.658 |
| crawl4ai-raw | #2 | smittenkitchen.com/recipes/ | 0.672 | smittenkitchen.com/./recipes/course/picnics/?forma | 0.670 | smittenkitchen.com/./recipes/course/salad/?format= | 0.658 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.692 | smittenkitchen.com/recipes/ | 0.645 | smittenkitchen.com/2008/04/cauliflower-bean-and-fe | 0.611 |
| crawlee | miss | smittenkitchen.com/recipes/ | 0.672 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.650 | smittenkitchen.com/about/faq/ | 0.619 |
| colly+md | #26 | smittenkitchen.com/recipes/ | 0.679 | smittenkitchen.com/about/faq/ | 0.619 | smittenkitchen.com/recipes/ | 0.617 |
| playwright | #32 | smittenkitchen.com/recipes/ | 0.679 | smittenkitchen.com/recipes | 0.679 | smittenkitchen.com/about/faq/ | 0.619 |


**Q25: What are some recommended places to eat in Paris during a short trip?**
*(expects URL containing: `a-few-trips-to-paris`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.697 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.682 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.675 |
| crawl4ai | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.686 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.665 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.664 |
| crawl4ai-raw | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.686 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.665 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.664 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.538 | smittenkitchen.com/2007/02/sour-cream-bran-muffins | 0.522 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.519 |
| crawlee | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.697 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.682 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.675 |
| colly+md | miss | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.616 | smittenkitchen.com/travel/a-few-favorites-from-spa | 0.609 | smittenkitchen.com/recipes/ | 0.607 |
| playwright | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.697 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.682 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.675 |


**Q26: What activities are suggested for acclimating to Paris on the first evening?**
*(expects URL containing: `a-few-trips-to-paris`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.694 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.642 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.634 |
| crawl4ai | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.633 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.619 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.617 |
| crawl4ai-raw | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.633 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.619 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.617 |
| scrapy+md | miss | smittenkitchen.com/2022/03/castle-breakfast/ | 0.437 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.427 | smittenkitchen.com/2007/02/sour-cream-bran-muffins | 0.424 |
| crawlee | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.694 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.642 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.634 |
| colly+md | miss | smittenkitchen.com/travel/48-hours-in-new-orleans/ | 0.592 | smittenkitchen.com/travel/48-hours-in-new-orleans/ | 0.591 | smittenkitchen.com/travel/48-hours-in-new-orleans/ | 0.549 |
| playwright | #1 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.694 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.642 | smittenkitchen.com/travel/a-few-trips-to-paris/ | 0.634 |


**Q27: What are some pancake recipes available on Smitten Kitchen?**
*(expects URL containing: `pancakes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2006/11/blondies/ | 0.682 | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.664 | smittenkitchen.com/2020/04/layered-yogurt-flatbrea | 0.662 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/course/pancakes/?form | 0.801 | smittenkitchen.com/./recipes/cuisine/austrian/?for | 0.739 | smittenkitchen.com/./recipes/method/sheet-pan/?for | 0.722 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/course/pancakes/?form | 0.801 | smittenkitchen.com/./recipes/cuisine/austrian/?for | 0.739 | smittenkitchen.com/./recipes/method/sheet-pan/?for | 0.722 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.721 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.702 | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.694 |
| crawlee | miss | smittenkitchen.com/2023/07/raspberry-streusel-muff | 0.700 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.694 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.692 |
| colly+md | miss | smittenkitchen.com/recipes/ | 0.717 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.702 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.681 |
| playwright | #3 | smittenkitchen.com/recipes | 0.717 | smittenkitchen.com/recipes/ | 0.717 | smittenkitchen.com/recipes/course/pancakes/?format | 0.697 |


**Q28: When was the pancake recipe page first published?**
*(expects URL containing: `pancakes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.596 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.594 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.594 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/course/pancakes/?form | 0.649 | smittenkitchen.com/./recipes/course/scones-biscuit | 0.632 | smittenkitchen.com/./recipes/course/put-an-egg-on- | 0.626 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/course/pancakes/?form | 0.649 | smittenkitchen.com/./recipes/course/scones-biscuit | 0.632 | smittenkitchen.com/./recipes/course/put-an-egg-on- | 0.626 |
| scrapy+md | miss | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.611 | smittenkitchen.com/2015/02/pecan-sticky-buns-news/ | 0.610 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.609 |
| crawlee | #29 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.615 | smittenkitchen.com/2023/07/raspberry-streusel-muff | 0.615 | smittenkitchen.com/2008/04/lemon-yogurt-anything-c | 0.607 |
| colly+md | miss | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.612 | smittenkitchen.com/2026/02/miso-chicken-and-rice/# | 0.611 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.611 |
| playwright | #11 | smittenkitchen.com/subscribe/ | 0.593 | smittenkitchen.com/recipes/sweets/pudding/?format= | 0.592 | smittenkitchen.com/recipes/vegetable/cabbage/?form | 0.591 |


**Q29: What are some recipes that include bourbon?**
*(expects URL containing: `bourbon`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2006/11/blondies/ | 0.665 | smittenkitchen.com/2012/08/my-favorite-brownies/ | 0.660 | smittenkitchen.com/2006/11/blondies/ | 0.645 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/ingredient/bourbon/?f | 0.686 | smittenkitchen.com/./recipes/sweets/candy/?format= | 0.616 | smittenkitchen.com/./recipes/fruit/orange/?format= | 0.609 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/ingredient/bourbon/?f | 0.686 | smittenkitchen.com/./recipes/sweets/candy/?format= | 0.616 | smittenkitchen.com/./recipes/fruit/orange/?format= | 0.609 |
| scrapy+md | miss | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.709 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.709 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.709 |
| crawlee | miss | smittenkitchen.com/2022/03/castle-breakfast/ | 0.609 | smittenkitchen.com/2008/04/lemon-yogurt-anything-c | 0.601 | smittenkitchen.com/2008/04/lemon-yogurt-anything-c | 0.597 |
| colly+md | miss | smittenkitchen.com/2026/04/sidecar/ | 0.639 | smittenkitchen.com/2026/04/sidecar/#comments | 0.639 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.630 |
| playwright | #1 | smittenkitchen.com/recipes/ingredient/bourbon/?for | 0.633 | smittenkitchen.com/subscribe/ | 0.583 | smittenkitchen.com/subscribe/ | 0.582 |


**Q30: When was the bourbon recipe page first published?**
*(expects URL containing: `bourbon`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2025/06/slushy-paper-plane/ | 0.610 | smittenkitchen.com/2025/06/slushy-paper-plane/ | 0.604 | smittenkitchen.com/2013/08/butterscotch-pudding-po | 0.599 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/ingredient/bourbon/?f | 0.632 | smittenkitchen.com/./recipes/cuisine/israeli/?form | 0.605 | smittenkitchen.com/./recipes/course/savory-condime | 0.602 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/ingredient/bourbon/?f | 0.632 | smittenkitchen.com/./recipes/cuisine/israeli/?form | 0.605 | smittenkitchen.com/./recipes/course/savory-condime | 0.602 |
| scrapy+md | miss | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.595 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.586 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.586 |
| crawlee | #35 | smittenkitchen.com/./recipes/diet/vegetarian/?form | 0.580 | smittenkitchen.com/ | 0.579 | smittenkitchen.com/./recipes/course/salad/?format= | 0.579 |
| colly+md | miss | smittenkitchen.com/2025/06/slushy-paper-plane/ | 0.596 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.595 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.595 |
| playwright | #1 | smittenkitchen.com/recipes/ingredient/bourbon/?for | 0.593 | smittenkitchen.com/recipes/sweets/pudding/?format= | 0.590 | smittenkitchen.com/recipes/ingredient/brown-butter | 0.589 |


**Q31: What are some seafood recipes available on Smitten Kitchen?**
*(expects URL containing: `seafood`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2006/08/moules-frites/ | 0.701 | smittenkitchen.com/2006/08/moules-frites/ | 0.686 | smittenkitchen.com/2006/08/moules-frites/ | 0.684 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/ingredient/seafood/?f | 0.759 | smittenkitchen.com/./recipes/vegetable/mushrooms/? | 0.714 | smittenkitchen.com/./recipes/ingredient/pantry/?fo | 0.712 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/ingredient/seafood/?f | 0.759 | smittenkitchen.com/./recipes/vegetable/mushrooms/? | 0.714 | smittenkitchen.com/./recipes/ingredient/pantry/?fo | 0.712 |
| scrapy+md | miss | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.668 | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.666 | smittenkitchen.com/2012/02/lasagna-bolognese/ | 0.666 |
| crawlee | miss | smittenkitchen.com/about/faq/ | 0.696 | smittenkitchen.com/about/faq/ | 0.660 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.659 |
| colly+md | #3 | smittenkitchen.com/about/faq/ | 0.696 | smittenkitchen.com/recipes/ | 0.668 | smittenkitchen.com/recipes/ingredient/seafood/?for | 0.663 |
| playwright | #4 | smittenkitchen.com/about/faq/ | 0.696 | smittenkitchen.com/recipes | 0.669 | smittenkitchen.com/recipes/ | 0.669 |


**Q32: How can I make garlic wine and butter steamed clams?**
*(expects URL containing: `seafood`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2006/08/moules-frites/ | 0.688 | smittenkitchen.com/2013/01/pasta-and-white-beans-w | 0.673 | smittenkitchen.com/2015/01/mushroom-marsala-pasta- | 0.673 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/ingredient/seafood/?f | 0.647 | smittenkitchen.com/./recipes/cuisine/portuguese/?f | 0.612 | smittenkitchen.com/./recipes/sweets/dessert-sauces | 0.606 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/ingredient/seafood/?f | 0.647 | smittenkitchen.com/./recipes/cuisine/portuguese/?f | 0.612 | smittenkitchen.com/./recipes/sweets/dessert-sauces | 0.606 |
| scrapy+md | miss | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.666 | smittenkitchen.com/2012/02/lasagna-bolognese/ | 0.666 | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.666 |
| crawlee | miss | smittenkitchen.com/2022/04/lemon-cream-meringues/ | 0.645 | smittenkitchen.com/about/faq/ | 0.623 | smittenkitchen.com/?random&timestamp=1777919490717 | 0.620 |
| colly+md | #8 | smittenkitchen.com/2022/04/lemon-cream-meringues/ | 0.645 | smittenkitchen.com/about/faq/ | 0.623 | smittenkitchen.com/2026/02/miso-chicken-and-rice/# | 0.616 |
| playwright | #4 | smittenkitchen.com/?random&timestamp=1777948695303 | 0.623 | smittenkitchen.com/about/faq/ | 0.623 | smittenkitchen.com/recipes/cuisine/portuguese/?for | 0.608 |


**Q33: What are some Middle Eastern recipes available on Smitten Kitchen?**
*(expects URL containing: `middle-eastern`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2016/05/chicken-gyro-salad/ | 0.696 | smittenkitchen.com/2017/07/hummus-heaped-with-toma | 0.694 | smittenkitchen.com/2014/08/smoky-eggplant-dip/ | 0.694 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/cuisine/middle-easter | 0.776 | smittenkitchen.com/./recipes/cuisine/north-african | 0.759 | smittenkitchen.com/./recipes/cuisine/israeli/?form | 0.749 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/cuisine/middle-easter | 0.776 | smittenkitchen.com/./recipes/cuisine/north-african | 0.759 | smittenkitchen.com/./recipes/cuisine/israeli/?form | 0.749 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.718 | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.689 | smittenkitchen.com/recipes/ | 0.687 |
| crawlee | miss | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.665 | smittenkitchen.com/about/faq/ | 0.658 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.653 |
| colly+md | #2 | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.681 | smittenkitchen.com/recipes/cuisine/middle-eastern/ | 0.680 | smittenkitchen.com/recipes/ | 0.680 |
| playwright | #1 | smittenkitchen.com/recipes/cuisine/middle-eastern/ | 0.680 | smittenkitchen.com/recipes/ | 0.680 | smittenkitchen.com/recipes | 0.680 |


**Q34: What is the first recipe listed in the Middle Eastern category?**
*(expects URL containing: `middle-eastern`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2016/05/chicken-gyro-salad/ | 0.643 | smittenkitchen.com/2020/04/layered-yogurt-flatbrea | 0.630 | smittenkitchen.com/2017/07/hummus-heaped-with-toma | 0.629 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/cuisine/middle-easter | 0.646 | smittenkitchen.com/./recipes/cuisine/north-african | 0.625 | smittenkitchen.com/./recipes/ingredient/meat/lamb/ | 0.618 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/cuisine/middle-easter | 0.646 | smittenkitchen.com/./recipes/cuisine/north-african | 0.625 | smittenkitchen.com/./recipes/ingredient/meat/lamb/ | 0.618 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.666 | smittenkitchen.com/2012/08/mediterranean-baked-fet | 0.616 | smittenkitchen.com/2012/08/mediterranean-baked-fet | 0.614 |
| crawlee | #11 | smittenkitchen.com/recipes/ | 0.613 | smittenkitchen.com/reading/ | 0.594 | smittenkitchen.com/?random&timestamp=1777919490717 | 0.585 |
| colly+md | #10 | smittenkitchen.com/recipes/ | 0.619 | smittenkitchen.com/2025/12/winter-cabbage-salad-wi | 0.605 | smittenkitchen.com/2025/12/winter-cabbage-salad-wi | 0.604 |
| playwright | #6 | smittenkitchen.com/recipes | 0.619 | smittenkitchen.com/recipes/ | 0.619 | smittenkitchen.com/recipes | 0.587 |


**Q35: What are some recipes that include eggplant?**
*(expects URL containing: `eggplant`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2008/01/rigatoni-with-eggplant- | 0.706 | smittenkitchen.com/2008/01/rigatoni-with-eggplant- | 0.697 | smittenkitchen.com/2019/08/black-pepper-tofu-and-e | 0.696 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/vegetable/eggplant/?f | 0.680 | smittenkitchen.com/recipes/ | 0.634 | smittenkitchen.com/./recipes/fruit/pomegranate/?fo | 0.633 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/vegetable/eggplant/?f | 0.680 | smittenkitchen.com/recipes/ | 0.635 | smittenkitchen.com/recipes/ | 0.634 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.661 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.647 | smittenkitchen.com/recipes/ | 0.643 |
| crawlee | miss | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.669 | smittenkitchen.com/2025/05/one-pan-ditalini-and-pe | 0.646 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.643 |
| colly+md | #5 | smittenkitchen.com/2025/05/one-pan-ditalini-and-pe | 0.646 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.637 | smittenkitchen.com/recipes/ | 0.635 |
| playwright | #16 | smittenkitchen.com/?random&timestamp=1777948695303 | 0.749 | smittenkitchen.com/?random&timestamp=1777948695303 | 0.697 | smittenkitchen.com/?random&timestamp=1777948695303 | 0.684 |


**Q36: What are some recipes included in the Savory Projects category?**
*(expects URL containing: `savory-projects`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.649 | smittenkitchen.com/2012/12/cashew-butter-balls/ | 0.640 | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.639 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/savory-projects/?form | 0.676 | smittenkitchen.com/./recipes/sweets/wedding-cake/? | 0.673 | smittenkitchen.com/./recipes/course/side-dish/?for | 0.661 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/savory-projects/?form | 0.676 | smittenkitchen.com/./recipes/sweets/wedding-cake/? | 0.673 | smittenkitchen.com/./recipes/course/side-dish/?for | 0.661 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.685 | smittenkitchen.com/recipes/ | 0.676 | smittenkitchen.com/2012/02/lasagna-bolognese/ | 0.638 |
| crawlee | miss | smittenkitchen.com/recipes/ | 0.653 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.641 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.641 |
| colly+md | miss | smittenkitchen.com/recipes/ | 0.679 | smittenkitchen.com/2022/04/lemon-cream-meringues/ | 0.658 | smittenkitchen.com/subscribe/ | 0.636 |
| playwright | #45 | smittenkitchen.com/recipes | 0.679 | smittenkitchen.com/recipes/ | 0.679 | smittenkitchen.com/subscribe/ | 0.636 |


**Q37: What type of recipes are categorized under Savory Projects?**
*(expects URL containing: `savory-projects`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.628 | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.619 | smittenkitchen.com/2014/07/grilled-peach-splits-ne | 0.619 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/savory-projects/?form | 0.645 | smittenkitchen.com/./recipes/sweets/wedding-cake/? | 0.637 | smittenkitchen.com/recipes/ | 0.626 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/savory-projects/?form | 0.645 | smittenkitchen.com/./recipes/sweets/wedding-cake/? | 0.637 | smittenkitchen.com/recipes/ | 0.626 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.658 | smittenkitchen.com/recipes/ | 0.654 | smittenkitchen.com/2017/09/pizza-beans/ | 0.621 |
| crawlee | #26 | smittenkitchen.com/recipes/ | 0.626 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.623 | smittenkitchen.com/?random&timestamp=1777919490717 | 0.614 |
| colly+md | #22 | smittenkitchen.com/recipes/ | 0.649 | smittenkitchen.com/2022/04/lemon-cream-meringues/ | 0.629 | smittenkitchen.com/2025/12/winter-cabbage-salad-wi | 0.617 |
| playwright | #13 | smittenkitchen.com/recipes/ | 0.649 | smittenkitchen.com/recipes | 0.649 | smittenkitchen.com/reading/cookbook-index/ | 0.609 |


**Q38: What are some recipes that include cheese?**
*(expects URL containing: `cheese`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2024/06/easy-basque-cheesecake/ | 0.674 | smittenkitchen.com/2025/11/pumpkin-basque-cheeseca | 0.669 | smittenkitchen.com/2024/06/easy-basque-cheesecake/ | 0.666 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/ingredient/cheese/?fo | 0.644 | smittenkitchen.com/ | 0.630 | smittenkitchen.com/./recipes/vegetable/greens/swis | 0.625 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/ingredient/cheese/?fo | 0.644 | smittenkitchen.com/ | 0.630 | smittenkitchen.com/./recipes/vegetable/greens/swis | 0.625 |
| scrapy+md | miss | smittenkitchen.com/2012/08/mediterranean-baked-fet | 0.666 | smittenkitchen.com/2012/08/mediterranean-baked-fet | 0.658 | smittenkitchen.com/recipes/ | 0.649 |
| crawlee | miss | smittenkitchen.com/2025/05/one-pan-ditalini-and-pe | 0.663 | smittenkitchen.com/2022/04/lemon-cream-meringues/ | 0.626 | smittenkitchen.com/2025/05/one-pan-ditalini-and-pe | 0.623 |
| colly+md | #49 | smittenkitchen.com/2026/04/braised-leeks-and-lenti | 0.636 | smittenkitchen.com/recipes/ | 0.627 | smittenkitchen.com/2022/04/lemon-cream-meringues/ | 0.626 |
| playwright | #18 | smittenkitchen.com/recipes | 0.627 | smittenkitchen.com/recipes/ | 0.627 | smittenkitchen.com/about/faq/ | 0.595 |


**Q39: What are some recipes that include kale?**
*(expects URL containing: `kale`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2025/02/ziti-chickpeas-with-sau | 0.660 | smittenkitchen.com/2011/01/chard-and-white-bean-st | 0.650 | smittenkitchen.com/2020/04/layered-yogurt-flatbrea | 0.649 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/vegetable/greens/kale | 0.702 | smittenkitchen.com/recipes/ | 0.680 | smittenkitchen.com/./recipes/ingredient/pantry/?fo | 0.677 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/vegetable/greens/kale | 0.702 | smittenkitchen.com/recipes/ | 0.684 | smittenkitchen.com/./recipes/ingredient/pantry/?fo | 0.677 |
| scrapy+md | miss | smittenkitchen.com/2017/09/pizza-beans/ | 0.668 | smittenkitchen.com/2017/09/pizza-beans/ | 0.660 | smittenkitchen.com/recipes/ | 0.660 |
| crawlee | miss | smittenkitchen.com/recipes/ | 0.689 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.647 | smittenkitchen.com/2025/05/one-pan-ditalini-and-pe | 0.635 |
| colly+md | #1 | smittenkitchen.com/recipes/vegetable/greens/kale/? | 0.643 | smittenkitchen.com/recipes/ | 0.639 | smittenkitchen.com/2025/05/one-pan-ditalini-and-pe | 0.635 |
| playwright | #1 | smittenkitchen.com/recipes/vegetable/greens/kale/? | 0.645 | smittenkitchen.com/recipes/ | 0.639 | smittenkitchen.com/recipes | 0.639 |


**Q40: When was the kale recipe page first published?**
*(expects URL containing: `kale`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #7 | smittenkitchen.com/2025/05/eggs-florentine/ | 0.636 | smittenkitchen.com/2025/05/challah-french-toast/ | 0.636 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.613 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/vegetable/greens/kale | 0.645 | smittenkitchen.com/./recipes/course/savory-condime | 0.639 | smittenkitchen.com/./recipes/sweets/dessert-sauces | 0.638 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/vegetable/greens/kale | 0.645 | smittenkitchen.com/./recipes/course/savory-condime | 0.639 | smittenkitchen.com/./recipes/sweets/dessert-sauces | 0.638 |
| scrapy+md | miss | smittenkitchen.com/2008/04/cauliflower-bean-and-fe | 0.651 | smittenkitchen.com/2008/04/cauliflower-bean-and-fe | 0.649 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.642 |
| crawlee | miss | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.622 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.621 | smittenkitchen.com/about/faq/ | 0.616 |
| colly+md | miss | smittenkitchen.com/2026/04/braised-leeks-and-lenti | 0.645 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.642 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.642 |
| playwright | #47 | smittenkitchen.com/?random&timestamp=1777948695303 | 0.626 | smittenkitchen.com/about/faq/ | 0.616 | smittenkitchen.com/about/faq/ | 0.604 |


</details>

## stripe-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai | 79% (46/58) | 86% (50/58) | 86% (50/58) | 93% (54/58) | 95% (55/58) | 0.839 | 2651 | 500 |
| crawl4ai-raw | 78% (45/58) | 86% (50/58) | 88% (51/58) | 97% (56/58) | 98% (57/58) | 0.837 | 3564 | 499 |
| crawlee | 64% (37/58) | 78% (45/58) | 83% (48/58) | 93% (54/58) | 97% (56/58) | 0.734 | 30214 | 500 |
| playwright | 64% (37/58) | 76% (44/58) | 83% (48/58) | 95% (55/58) | 97% (56/58) | 0.734 | 30229 | 500 |
| colly+md | 29% (17/58) | 38% (22/58) | 47% (27/58) | 53% (31/58) | 57% (33/58) | 0.366 | 31125 | 499 |
| markcrawl | 26% (15/58) | 33% (19/58) | 34% (20/58) | 43% (25/58) | 43% (25/58) | 0.305 | 1904 | 489 |
| scrapy+md | 19% (11/58) | 26% (15/58) | 26% (15/58) | 31% (18/58) | 34% (20/58) | 0.226 | 14882 | 500 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for stripe-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is the purpose of the Elements object in Stripe.js?**
*(expects URL containing: `create_payment_element`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/elements | 0.784 | docs.stripe.com/payments/accept-a-payment-synchron | 0.774 | docs.stripe.com/payments/bank-transfers/accept-a-p | 0.769 |
| crawl4ai | miss | docs.stripe.com/elements/address-element | 0.760 | docs.stripe.com/payments/link/express-checkout-ele | 0.757 | docs.stripe.com/elements/address-element | 0.742 |
| crawl4ai-raw | #4 | docs.stripe.com/js | 0.847 | docs.stripe.com/js/element/other_element | 0.838 | docs.stripe.com/js/element/other_element | 0.832 |
| scrapy+md | #15 | docs.stripe.com/js/elements_object/update | 0.815 | docs.stripe.com/js/custom_checkout/update_line_ite | 0.815 | docs.stripe.com/js/tokens/create_token?type=cvc_up | 0.815 |
| crawlee | #4 | docs.stripe.com/payments/elements | 0.859 | docs.stripe.com/elements/appearance-api | 0.847 | docs.stripe.com/js | 0.816 |
| colly+md | miss | docs.stripe.com/payments/elements | 0.859 | docs.stripe.com/elements/appearance-api | 0.847 | docs.stripe.com/js#stripe-handle-card-action | 0.815 |
| playwright | #6 | docs.stripe.com/payments/elements | 0.859 | docs.stripe.com/elements/appearance-api | 0.847 | docs.stripe.com/js/element/other_element | 0.819 |


**Q2: How do you create an Elements instance using Stripe.js?**
*(expects URL containing: `create_payment_element`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/accept-a-payment-synchron | 0.781 | docs.stripe.com/payments/elements | 0.772 | docs.stripe.com/payments/without-card-authenticati | 0.758 |
| crawl4ai | miss | docs.stripe.com/payments/link/express-checkout-ele | 0.782 | docs.stripe.com/elements/address-element | 0.742 | docs.stripe.com/payments/advanced/collect-addresse | 0.741 |
| crawl4ai-raw | #2 | docs.stripe.com/js/element/other_element | 0.848 | docs.stripe.com/js/elements_object/create_payment_ | 0.845 | docs.stripe.com/js | 0.845 |
| scrapy+md | #10 | docs.stripe.com/js/custom_checkout/update_line_ite | 0.821 | docs.stripe.com/js/tokens/create_token?type=cvc_up | 0.821 | docs.stripe.com/js/payment_intents/confirm_payment | 0.821 |
| crawlee | #5 | docs.stripe.com/payments/elements | 0.844 | docs.stripe.com/payments/advanced/dynamic-updates | 0.835 | docs.stripe.com/elements/appearance-api | 0.823 |
| colly+md | miss | docs.stripe.com/payments/elements | 0.844 | docs.stripe.com/payments/advanced/dynamic-updates | 0.835 | docs.stripe.com/elements/appearance-api | 0.823 |
| playwright | #5 | docs.stripe.com/payments/elements | 0.844 | docs.stripe.com/payments/advanced/dynamic-updates | 0.835 | docs.stripe.com/js/element/other_element | 0.823 |


**Q3: What is prebilling in Stripe subscriptions?**
*(expects URL containing: `prebilling`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/advanced/build-subscripti | 0.711 | docs.stripe.com/payments/subscriptions | 0.699 | docs.stripe.com/payments/checkout/free-trials | 0.690 |
| crawl4ai | #1 | docs.stripe.com/billing/subscriptions/prebilling | 0.758 | docs.stripe.com/billing/subscriptions/prebilling | 0.757 | docs.stripe.com/llms.txt | 0.752 |
| crawl4ai-raw | #1 | docs.stripe.com/billing/subscriptions/prebilling | 0.758 | docs.stripe.com/billing/subscriptions/prebilling | 0.757 | docs.stripe.com/llms.txt | 0.752 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.732 | docs.stripe.com/api/subscription_items/create | 0.730 | docs.stripe.com/india-recurring-payments?integrati | 0.729 |
| crawlee | #1 | docs.stripe.com/billing/subscriptions/prebilling | 0.782 | docs.stripe.com/billing | 0.762 | docs.stripe.com/billing/subscriptions/prebilling | 0.754 |
| colly+md | miss | docs.stripe.com/billing | 0.762 | docs.stripe.com/connect/subscriptions | 0.745 | docs.stripe.com/billing/subscriptions/overview | 0.739 |
| playwright | #1 | docs.stripe.com/billing/subscriptions/prebilling | 0.782 | docs.stripe.com/billing | 0.762 | docs.stripe.com/billing/subscriptions/prebilling | 0.754 |


**Q4: What are the limitations of using prebilling?**
*(expects URL containing: `prebilling`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/partial-authorization | 0.651 | docs.stripe.com/payments/partial-authorization | 0.643 | docs.stripe.com/payments/off-session-payments | 0.637 |
| crawl4ai | #1 | docs.stripe.com/billing/subscriptions/prebilling | 0.768 | docs.stripe.com/billing/subscriptions/prebilling | 0.668 | docs.stripe.com/billing/subscriptions/subscription | 0.638 |
| crawl4ai-raw | #1 | docs.stripe.com/billing/subscriptions/prebilling | 0.768 | docs.stripe.com/billing/subscriptions/prebilling | 0.668 | docs.stripe.com/billing/subscriptions/subscription | 0.638 |
| scrapy+md | miss | docs.stripe.com/js/appendix/supported_browsers | 0.626 | docs.stripe.com/js/custom_checkout/confirm | 0.626 | docs.stripe.com/js/including | 0.626 |
| crawlee | #1 | docs.stripe.com/billing/subscriptions/prebilling | 0.758 | docs.stripe.com/billing/subscriptions/prebilling | 0.672 | docs.stripe.com/billing/subscriptions/prebilling | 0.662 |
| colly+md | miss | docs.stripe.com/payments/place-a-hold-on-a-payment | 0.659 | docs.stripe.com/billing/subscriptions/subscription | 0.638 | docs.stripe.com/payments/advanced/discounts?paymen | 0.635 |
| playwright | #1 | docs.stripe.com/billing/subscriptions/prebilling | 0.768 | docs.stripe.com/billing/subscriptions/prebilling | 0.672 | docs.stripe.com/billing/subscriptions/prebilling | 0.662 |


**Q5: What are the common use cases for Financial Connections?**
*(expects URL containing: `use-cases`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/ach-direct-debit/accept-a | 0.669 | docs.stripe.com/payments/payment-methods/payment-m | 0.652 | docs.stripe.com/payments/customer-balance/migratin | 0.652 |
| crawl4ai | #1 | docs.stripe.com/financial-connections/use-cases | 0.827 | docs.stripe.com/financial-connections/transactions | 0.780 | docs.stripe.com/financial-connections | 0.777 |
| crawl4ai-raw | #1 | docs.stripe.com/financial-connections/use-cases | 0.827 | docs.stripe.com/financial-connections/transactions | 0.780 | docs.stripe.com/financial-connections | 0.777 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.683 | docs.stripe.com/connect/risk-management/best-pract | 0.678 | docs.stripe.com/llms.txt | 0.677 |
| crawlee | #1 | docs.stripe.com/financial-connections/use-cases | 0.881 | docs.stripe.com/financial-connections/use-cases | 0.812 | docs.stripe.com/financial-connections/other-data-p | 0.782 |
| colly+md | #9 | docs.stripe.com/financial-connections | 0.761 | docs.stripe.com/financial-connections/connect-payo | 0.754 | docs.stripe.com/financial-connections/connect-payo | 0.726 |
| playwright | #1 | docs.stripe.com/financial-connections/use-cases | 0.881 | docs.stripe.com/financial-connections/use-cases | 0.812 | docs.stripe.com/financial-connections/other-data-p | 0.782 |


**Q6: How can Financial Connections help improve payment reliability for ACH Direct Debit payments?**
*(expects URL containing: `use-cases`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/ach-direct-debit | 0.718 | docs.stripe.com/payments/ach-direct-debit/accept-a | 0.712 | docs.stripe.com/payments/ach-direct-debit | 0.707 |
| crawl4ai | #1 | docs.stripe.com/financial-connections/use-cases | 0.774 | docs.stripe.com/financial-connections/ach-direct-d | 0.772 | docs.stripe.com/financial-connections/ach-direct-d | 0.733 |
| crawl4ai-raw | #1 | docs.stripe.com/financial-connections/use-cases | 0.774 | docs.stripe.com/financial-connections/ach-direct-d | 0.772 | docs.stripe.com/financial-connections/ach-direct-d | 0.733 |
| scrapy+md | miss | docs.stripe.com/invoicing/automatic-reconciliation | 0.671 | docs.stripe.com/declines/network-codes | 0.669 | docs.stripe.com/invoicing/automatic-reconciliation | 0.667 |
| crawlee | #1 | docs.stripe.com/financial-connections/use-cases | 0.774 | docs.stripe.com/financial-connections | 0.749 | docs.stripe.com/financial-connections/use-cases | 0.739 |
| colly+md | #48 | docs.stripe.com/financial-connections | 0.744 | docs.stripe.com/payments/ach-direct-debit | 0.728 | docs.stripe.com/payments/ach-direct-debit | 0.718 |
| playwright | #1 | docs.stripe.com/financial-connections/use-cases | 0.774 | docs.stripe.com/financial-connections | 0.746 | docs.stripe.com/financial-connections/ach-direct-d | 0.735 |


**Q7: How can I create a test invoice in Stripe?**
*(expects URL containing: `invoices`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/boleto/set-up-invoices | 0.779 | docs.stripe.com/payments/advanced/receipts | 0.760 | docs.stripe.com/payments/checkout/receipts | 0.755 |
| crawl4ai | #1 | docs.stripe.com/get-started/use-cases/invoices | 0.827 | docs.stripe.com/get-started/use-cases/invoices | 0.814 | docs.stripe.com/invoicing/dashboard | 0.808 |
| crawl4ai-raw | #1 | docs.stripe.com/get-started/use-cases/invoices | 0.827 | docs.stripe.com/get-started/use-cases/invoices | 0.814 | docs.stripe.com/invoicing/dashboard | 0.808 |
| scrapy+md | #3 | docs.stripe.com/invoicing/dashboard | 0.805 | docs.stripe.com/invoicing/integration/testing | 0.788 | docs.stripe.com/api/invoices/create | 0.788 |
| crawlee | #2 | docs.stripe.com/invoicing | 0.841 | docs.stripe.com/api/invoices | 0.830 | docs.stripe.com/get-started/use-cases/invoices | 0.827 |
| colly+md | #2 | docs.stripe.com/invoicing | 0.841 | docs.stripe.com/api/invoices | 0.830 | docs.stripe.com/get-started/use-cases/invoices | 0.827 |
| playwright | #2 | docs.stripe.com/invoicing | 0.841 | docs.stripe.com/api/invoices | 0.830 | docs.stripe.com/get-started/use-cases/invoices | 0.827 |


**Q8: What steps do I need to follow to enable Direct Debit retries for invoices?**
*(expects URL containing: `invoices`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/pay-with-balance | 0.756 | docs.stripe.com/payments/bacs-debit/accept-a-payme | 0.751 | docs.stripe.com/payments/acss-debit | 0.736 |
| crawl4ai | #1 | docs.stripe.com/get-started/use-cases/invoices | 0.792 | docs.stripe.com/invoicing/automatic-collection | 0.772 | docs.stripe.com/payments/pay-with-balance | 0.756 |
| crawl4ai-raw | #1 | docs.stripe.com/get-started/use-cases/invoices | 0.792 | docs.stripe.com/invoicing/automatic-collection | 0.772 | docs.stripe.com/payments/pay-with-balance | 0.756 |
| scrapy+md | miss | docs.stripe.com/invoicing/automatic-collection | 0.771 | docs.stripe.com/connect/saas/tasks/service-fee | 0.756 | docs.stripe.com/api/customers/object | 0.749 |
| crawlee | #2 | docs.stripe.com/invoicing/automatic-collection | 0.804 | docs.stripe.com/get-started/use-cases/invoices | 0.800 | docs.stripe.com/invoicing/automatic-collection | 0.771 |
| colly+md | #2 | docs.stripe.com/invoicing/automatic-collection | 0.804 | docs.stripe.com/get-started/use-cases/invoices | 0.800 | docs.stripe.com/invoicing/automatic-collection | 0.783 |
| playwright | #2 | docs.stripe.com/invoicing/automatic-collection | 0.804 | docs.stripe.com/get-started/use-cases/invoices | 0.800 | docs.stripe.com/invoicing/automatic-collection | 0.771 |


**Q9: How do I create a payment link using the Stripe Dashboard?**
*(expects URL containing: `create`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/managed-payments/use-paym | 0.816 | docs.stripe.com/payments/managed-payments/use-paym | 0.804 | docs.stripe.com/payments/link/mobile-payment-eleme | 0.792 |
| crawl4ai | #2 | docs.stripe.com/get-started/use-cases/startup | 0.855 | docs.stripe.com/payment-links/create | 0.826 | docs.stripe.com/payment-links/create | 0.817 |
| crawl4ai-raw | #2 | docs.stripe.com/get-started/use-cases/startup | 0.855 | docs.stripe.com/payment-links/create | 0.826 | docs.stripe.com/payment-links/create | 0.817 |
| scrapy+md | #3 | docs.stripe.com/payments/managed-payments/use-paym | 0.851 | docs.stripe.com/payment-links/customize | 0.806 | docs.stripe.com/api/payment-link/create | 0.795 |
| crawlee | #1 | docs.stripe.com/payment-links/create | 0.929 | docs.stripe.com/payments/link/link-payment-methods | 0.875 | docs.stripe.com/payments/link/payment-element-link | 0.874 |
| colly+md | #1 | docs.stripe.com/payment-links/create | 0.929 | docs.stripe.com/payment-links/create#api | 0.929 | docs.stripe.com/payments/link/link-payment-methods | 0.875 |
| playwright | #1 | docs.stripe.com/payment-links/create | 0.929 | docs.stripe.com/payments/link/link-payment-methods | 0.875 | docs.stripe.com/payments/link/payment-element-link | 0.874 |


**Q10: What pricing models does Payment Links support?**
*(expects URL containing: `create`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/link/link-payment-methods | 0.796 | docs.stripe.com/payments/link/link-payment-methods | 0.761 | docs.stripe.com/payments/payment-methods/payment-m | 0.751 |
| crawl4ai | #10 | docs.stripe.com/payments/link/link-payment-methods | 0.805 | docs.stripe.com/payments/link/link-payment-integra | 0.784 | docs.stripe.com/payments/link/checkout-link | 0.765 |
| crawl4ai-raw | #10 | docs.stripe.com/payments/link/link-payment-methods | 0.805 | docs.stripe.com/payments/link/link-payment-integra | 0.784 | docs.stripe.com/payments/link/checkout-link | 0.765 |
| scrapy+md | #9 | docs.stripe.com/payments/link/link-payment-integra | 0.784 | docs.stripe.com/payment-links/customize | 0.731 | docs.stripe.com/payment-links/customize | 0.727 |
| crawlee | #16 | docs.stripe.com/payments/link/link-payment-methods | 0.784 | docs.stripe.com/payments/link/link-payment-integra | 0.781 | docs.stripe.com/payments/link/link-payment-methods | 0.763 |
| colly+md | #4 | docs.stripe.com/payments/link/link-payment-methods | 0.784 | docs.stripe.com/payments/link/checkout-link | 0.764 | docs.stripe.com/payments/link/link-payment-methods | 0.761 |
| playwright | #4 | docs.stripe.com/payments/link/link-payment-integra | 0.784 | docs.stripe.com/payments/link/link-payment-methods | 0.784 | docs.stripe.com/payments/link/link-payment-methods | 0.763 |


**Q11: What is the purpose of the Tax ID Element?**
*(expects URL containing: `tax-id-element`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/advanced/tax | 0.702 | docs.stripe.com/payments/advanced/tax | 0.690 | docs.stripe.com/payments/advanced/tax | 0.663 |
| crawl4ai | #1 | docs.stripe.com/elements/tax-id-element | 0.729 | docs.stripe.com/elements/tax-id-element | 0.724 | docs.stripe.com/tax/custom | 0.708 |
| crawl4ai-raw | #7 | docs.stripe.com/js/element/other_element | 0.766 | docs.stripe.com/js | 0.764 | docs.stripe.com/js/elements_object/create_payment_ | 0.763 |
| scrapy+md | miss | docs.stripe.com/js/payment_request/create | 0.790 | docs.stripe.com/js/tokens/create_token?type=cvc_up | 0.790 | docs.stripe.com/js/elements_object/create_element? | 0.790 |
| crawlee | #1 | docs.stripe.com/elements/tax-id-element | 0.829 | docs.stripe.com/js | 0.790 | docs.stripe.com/js/elements_object/create_payment_ | 0.790 |
| colly+md | miss | docs.stripe.com/js | 0.790 | docs.stripe.com/js#stripe-handle-card-action | 0.790 | docs.stripe.com/js#stripe-confirm-card-payment | 0.790 |
| playwright | #1 | docs.stripe.com/elements/tax-id-element | 0.829 | docs.stripe.com/js/element/other_element | 0.794 | docs.stripe.com/js | 0.790 |


**Q12: In which countries does the Tax ID Element support tax ID collection?**
*(expects URL containing: `tax-id-element`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/advanced/tax | 0.732 | docs.stripe.com/payments/advanced/tax | 0.725 | docs.stripe.com/payments/advanced/tax | 0.701 |
| crawl4ai | #1 | docs.stripe.com/elements/tax-id-element | 0.804 | docs.stripe.com/tax/custom | 0.780 | docs.stripe.com/payments/advanced/tax | 0.736 |
| crawl4ai-raw | #1 | docs.stripe.com/elements/tax-id-element | 0.804 | docs.stripe.com/tax/custom | 0.780 | docs.stripe.com/js | 0.745 |
| scrapy+md | miss | docs.stripe.com/tax/checkout/tax-ids | 0.725 | docs.stripe.com/tax/checkout/tax-ids | 0.720 | docs.stripe.com/js/element/other_element?type=card | 0.720 |
| crawlee | #2 | docs.stripe.com/tax/custom | 0.827 | docs.stripe.com/elements/tax-id-element | 0.804 | docs.stripe.com/elements/tax-id-element | 0.777 |
| colly+md | miss | docs.stripe.com/tax/custom | 0.827 | docs.stripe.com/tax/custom | 0.767 | docs.stripe.com/tax/custom | 0.732 |
| playwright | #2 | docs.stripe.com/tax/custom | 0.827 | docs.stripe.com/elements/tax-id-element | 0.804 | docs.stripe.com/elements/tax-id-element | 0.777 |


**Q13: How can I collect a customer email address for Link authentication?**
*(expects URL containing: `save-and-reuse`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #6 | docs.stripe.com/payments/link/add-link-elements-in | 0.797 | docs.stripe.com/payments/link/add-link-elements-in | 0.769 | docs.stripe.com/payments/link/link-authentication- | 0.765 |
| crawl4ai | #2 | docs.stripe.com/payments/link/add-link-elements-in | 0.797 | docs.stripe.com/payments/link/save-and-reuse | 0.746 | docs.stripe.com/payments/link/add-link-elements-in | 0.746 |
| crawl4ai-raw | #2 | docs.stripe.com/payments/link/add-link-elements-in | 0.797 | docs.stripe.com/payments/link/save-and-reuse | 0.746 | docs.stripe.com/payments/link/add-link-elements-in | 0.746 |
| scrapy+md | #3 | docs.stripe.com/payments/link/add-link-elements-in | 0.797 | docs.stripe.com/payments/link/add-link-elements-in | 0.770 | docs.stripe.com/payments/link/save-and-reuse | 0.744 |
| crawlee | #2 | docs.stripe.com/payments/link/add-link-elements-in | 0.797 | docs.stripe.com/payments/link/save-and-reuse | 0.744 | docs.stripe.com/payments/link/save-and-reuse | 0.738 |
| colly+md | #38 | docs.stripe.com/payments/link/add-link-elements-in | 0.797 | docs.stripe.com/payments/link/add-link-elements-in | 0.738 | docs.stripe.com/checkout/quickstart | 0.722 |
| playwright | #2 | docs.stripe.com/payments/link/add-link-elements-in | 0.797 | docs.stripe.com/payments/link/save-and-reuse | 0.744 | docs.stripe.com/payments/link/save-and-reuse | 0.738 |


**Q14: What is a SetupIntent in the context of setting up future payments with Link?**
*(expects URL containing: `save-and-reuse`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #10 | docs.stripe.com/payments/setup-intents | 0.756 | docs.stripe.com/payments/paymentintents/lifecycle | 0.750 | docs.stripe.com/payments/mobile/tap-to-add | 0.744 |
| crawl4ai | #1 | docs.stripe.com/payments/link/save-and-reuse | 0.789 | docs.stripe.com/payments/setup-intents | 0.750 | docs.stripe.com/payments/link/add-link-elements-in | 0.749 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/link/save-and-reuse | 0.789 | docs.stripe.com/js/elements_object/create_payment_ | 0.752 | docs.stripe.com/payments/setup-intents | 0.750 |
| scrapy+md | #1 | docs.stripe.com/payments/link/save-and-reuse | 0.782 | docs.stripe.com/js/setup_intents/confirm_card_setu | 0.779 | docs.stripe.com/js/payment_intents/create_radar_se | 0.779 |
| crawlee | #7 | docs.stripe.com/api/setup_intents/create | 0.812 | docs.stripe.com/api/setup_intents/object | 0.812 | docs.stripe.com/api/setup_intents/object | 0.795 |
| colly+md | miss | docs.stripe.com/api/setup/intents | 0.812 | docs.stripe.com/api/setup/intents | 0.795 | docs.stripe.com/api/setup/intents/object#setup/int | 0.795 |
| playwright | #7 | docs.stripe.com/api/setup_intents/object | 0.812 | docs.stripe.com/api/setup_intents/create | 0.812 | docs.stripe.com/api/setup_intents/object | 0.795 |


**Q15: How can I fund my storage balance with an external bank account?**
*(expects URL containing: `fund-balance`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/balances | 0.683 | docs.stripe.com/payments/customer-balance/funding- | 0.649 | docs.stripe.com/payments/external-payment-methods | 0.641 |
| crawl4ai | #1 | docs.stripe.com/global-payouts/fund-balance | 0.758 | docs.stripe.com/global-payouts/fund-balance | 0.746 | docs.stripe.com/global-payouts/fund-balance | 0.719 |
| crawl4ai-raw | #1 | docs.stripe.com/global-payouts/fund-balance | 0.758 | docs.stripe.com/global-payouts/fund-balance | 0.746 | docs.stripe.com/global-payouts/fund-balance | 0.719 |
| scrapy+md | miss | docs.stripe.com/api/external_accounts?api-version= | 0.659 | docs.stripe.com/api/external_accounts?api-version= | 0.657 | docs.stripe.com/api/external_account_cards/object | 0.654 |
| crawlee | #1 | docs.stripe.com/global-payouts/fund-balance | 0.785 | docs.stripe.com/global-payouts/fund-balance | 0.746 | docs.stripe.com/global-payouts/testing | 0.723 |
| colly+md | miss | docs.stripe.com/issuing/for-your-business | 0.703 | docs.stripe.com/treasury | 0.665 | docs.stripe.com/api/accounts/update#update/account | 0.654 |
| playwright | #1 | docs.stripe.com/global-payouts/fund-balance | 0.785 | docs.stripe.com/global-payouts/fund-balance | 0.746 | docs.stripe.com/global-payouts/testing | 0.723 |


**Q16: What are the funding limits when pulling funds from an external bank account?**
*(expects URL containing: `fund-balance`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/payto | 0.658 | docs.stripe.com/payments/customer-balance/virtual- | 0.645 | docs.stripe.com/payments/payto | 0.634 |
| crawl4ai | #1 | docs.stripe.com/global-payouts/fund-balance | 0.701 | docs.stripe.com/global-payouts/fund-balance | 0.653 | docs.stripe.com/capital/how-stripe-capital-works | 0.637 |
| crawl4ai-raw | #1 | docs.stripe.com/global-payouts/fund-balance | 0.701 | docs.stripe.com/global-payouts/fund-balance | 0.653 | docs.stripe.com/capital/how-stripe-capital-works | 0.637 |
| scrapy+md | miss | docs.stripe.com/api/external_accounts?api-version= | 0.640 | docs.stripe.com/api/external_account_bank_accounts | 0.630 | docs.stripe.com/api/external_accounts?api-version= | 0.611 |
| crawlee | #1 | docs.stripe.com/global-payouts/fund-balance | 0.701 | docs.stripe.com/global-payouts/fund-balance | 0.662 | docs.stripe.com/payments/payto | 0.658 |
| colly+md | miss | docs.stripe.com/api/accounts/update#update/account | 0.645 | docs.stripe.com/capital/how-stripe-capital-works | 0.637 | docs.stripe.com/issuing/funding/balance | 0.629 |
| playwright | #1 | docs.stripe.com/global-payouts/fund-balance | 0.701 | docs.stripe.com/global-payouts/fund-balance | 0.662 | docs.stripe.com/payments/payto | 0.658 |


**Q17: What types of companies can you incorporate using Stripe Atlas?**
*(expects URL containing: `company-types`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/p24 | 0.647 | docs.stripe.com/payments/payment-methods/overview | 0.632 | docs.stripe.com/payments/kriya | 0.625 |
| crawl4ai | #1 | docs.stripe.com/atlas/company-types | 0.810 | docs.stripe.com/atlas/signup | 0.779 | docs.stripe.com/atlas | 0.764 |
| crawl4ai-raw | #1 | docs.stripe.com/atlas/company-types | 0.810 | docs.stripe.com/atlas/signup | 0.779 | docs.stripe.com/atlas | 0.764 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.738 | docs.stripe.com/payments | 0.635 | docs.stripe.com/connect/onboarding | 0.607 |
| crawlee | #1 | docs.stripe.com/atlas/company-types | 0.820 | docs.stripe.com/atlas/signup | 0.771 | docs.stripe.com/atlas/signup | 0.770 |
| colly+md | miss | docs.stripe.com/atlas | 0.762 | docs.stripe.com/atlas/accept-payments | 0.752 | docs.stripe.com/atlas | 0.700 |
| playwright | #1 | docs.stripe.com/atlas/company-types | 0.820 | docs.stripe.com/atlas/signup | 0.771 | docs.stripe.com/atlas/signup | 0.770 |


**Q18: What are the tax implications of incorporating near the end of a calendar year?**
*(expects URL containing: `company-types`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/managed-payments/tax-comp | 0.603 | docs.stripe.com/payments/managed-payments/eligibil | 0.587 | docs.stripe.com/payments/managed-payments/eligibil | 0.585 |
| crawl4ai | #1 | docs.stripe.com/atlas/company-types | 0.830 | docs.stripe.com/atlas/83b-election | 0.718 | docs.stripe.com/atlas/business-taxes | 0.699 |
| crawl4ai-raw | #1 | docs.stripe.com/atlas/company-types | 0.830 | docs.stripe.com/atlas/83b-election | 0.718 | docs.stripe.com/atlas/business-taxes | 0.699 |
| scrapy+md | miss | docs.stripe.com/reports/report-types/tax | 0.622 | docs.stripe.com/reports/report-types/connect | 0.598 | docs.stripe.com/js/payment_request/create | 0.597 |
| crawlee | #1 | docs.stripe.com/atlas/company-types | 0.830 | docs.stripe.com/atlas/company-types | 0.799 | docs.stripe.com/atlas/company-types | 0.796 |
| colly+md | miss | docs.stripe.com/atlas/83b-elections-non-us-founder | 0.646 | docs.stripe.com/atlas | 0.624 | docs.stripe.com/connect/account-capabilities | 0.623 |
| playwright | #1 | docs.stripe.com/atlas/company-types | 0.830 | docs.stripe.com/atlas/company-types | 0.796 | docs.stripe.com/atlas/83b-election | 0.718 |


**Q19: What is a dispute in the context of Stripe?**
*(expects URL containing: `disputes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.stripe.com/payments/wallets/link | 0.747 | docs.stripe.com/payments/klarna/disputes | 0.743 | docs.stripe.com/payments/klarna/disputes | 0.741 |
| crawl4ai | #1 | docs.stripe.com/disputes | 0.799 | docs.stripe.com/disputes | 0.785 | docs.stripe.com/disputes/responding | 0.765 |
| crawl4ai-raw | #1 | docs.stripe.com/disputes | 0.799 | docs.stripe.com/disputes | 0.785 | docs.stripe.com/disputes/responding | 0.765 |
| scrapy+md | #1 | docs.stripe.com/connect/saas/tasks/refunds-dispute | 0.776 | docs.stripe.com/api/disputes/list | 0.760 | docs.stripe.com/api/disputes/object | 0.760 |
| crawlee | #1 | docs.stripe.com/disputes | 0.885 | docs.stripe.com/disputes/how-disputes-work | 0.845 | docs.stripe.com/disputes/responding#decide | 0.836 |
| colly+md | #1 | docs.stripe.com/disputes | 0.885 | docs.stripe.com/disputes/how-disputes-work | 0.845 | docs.stripe.com/disputes/responding#decide | 0.836 |
| playwright | #1 | docs.stripe.com/disputes | 0.885 | docs.stripe.com/disputes/responding | 0.836 | docs.stripe.com/disputes | 0.792 |


**Q20: How does Stripe guide users through the dispute response process?**
*(expects URL containing: `disputes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | docs.stripe.com/payments/wallets/link | 0.782 | docs.stripe.com/payments/affirm | 0.765 | docs.stripe.com/payments/satispay | 0.760 |
| crawl4ai | #1 | docs.stripe.com/disputes | 0.827 | docs.stripe.com/disputes/responding | 0.786 | docs.stripe.com/disputes/responding | 0.780 |
| crawl4ai-raw | #1 | docs.stripe.com/disputes | 0.827 | docs.stripe.com/disputes/responding | 0.786 | docs.stripe.com/disputes/responding | 0.780 |
| scrapy+md | #1 | docs.stripe.com/connect/saas/tasks/refunds-dispute | 0.763 | docs.stripe.com/disputes/categories | 0.761 | docs.stripe.com/api/disputes/update?api-version=20 | 0.760 |
| crawlee | #1 | docs.stripe.com/disputes/responding#decide | 0.847 | docs.stripe.com/disputes/how-disputes-work | 0.818 | docs.stripe.com/disputes/responding#decide | 0.786 |
| colly+md | #1 | docs.stripe.com/disputes/responding#decide | 0.848 | docs.stripe.com/disputes/responding | 0.848 | docs.stripe.com/disputes/api | 0.841 |
| playwright | #1 | docs.stripe.com/disputes/responding | 0.847 | docs.stripe.com/disputes | 0.790 | docs.stripe.com/disputes/responding | 0.786 |


**Q21: What financing types does Stripe Capital offer?**
*(expects URL containing: `overview`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/payment-methods/overview | 0.671 | docs.stripe.com/payments/affirm | 0.666 | docs.stripe.com/payments/customer-balance/funding- | 0.660 |
| crawl4ai | #1 | docs.stripe.com/capital/overview | 0.769 | docs.stripe.com/capital/how-stripe-capital-works | 0.764 | docs.stripe.com/capital/overview | 0.763 |
| crawl4ai-raw | #1 | docs.stripe.com/capital/overview | 0.769 | docs.stripe.com/capital/how-stripe-capital-works | 0.764 | docs.stripe.com/capital/overview | 0.763 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.699 | docs.stripe.com/payments/customer-balance/funding- | 0.657 | docs.stripe.com/connect/charges | 0.656 |
| crawlee | #2 | docs.stripe.com/capital/how-stripe-capital-works | 0.768 | docs.stripe.com/capital/overview | 0.763 | docs.stripe.com/capital/how-capital-for-platforms- | 0.759 |
| colly+md | #3 | docs.stripe.com/capital/how-stripe-capital-works | 0.777 | docs.stripe.com/capital/how-capital-for-platforms- | 0.775 | docs.stripe.com/capital/overview | 0.760 |
| playwright | #2 | docs.stripe.com/capital/how-stripe-capital-works | 0.768 | docs.stripe.com/capital/overview | 0.760 | docs.stripe.com/capital/how-capital-for-platforms- | 0.759 |


**Q22: How can I access my Capital financing offers?**
*(expects URL containing: `overview`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.stripe.com/payments/payto | 0.604 | docs.stripe.com/payments/payment-methods/overview | 0.596 | docs.stripe.com/payments/customer-balance/invoicin | 0.589 |
| crawl4ai | #1 | docs.stripe.com/capital/overview | 0.721 | docs.stripe.com/capital/how-capital-for-platforms- | 0.717 | docs.stripe.com/capital/how-stripe-capital-works | 0.696 |
| crawl4ai-raw | #1 | docs.stripe.com/capital/overview | 0.721 | docs.stripe.com/capital/how-capital-for-platforms- | 0.717 | docs.stripe.com/capital/how-stripe-capital-works | 0.696 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.634 | docs.stripe.com/payments/customer-balance/funding- | 0.600 | docs.stripe.com/api/external_account_bank_accounts | 0.589 |
| crawlee | #3 | docs.stripe.com/capital/how-stripe-capital-works | 0.733 | docs.stripe.com/capital/how-stripe-capital-works | 0.728 | docs.stripe.com/capital/overview | 0.722 |
| colly+md | #4 | docs.stripe.com/capital/how-stripe-capital-works | 0.733 | docs.stripe.com/capital/how-stripe-capital-works | 0.728 | docs.stripe.com/capital/how-capital-for-platforms- | 0.726 |
| playwright | #4 | docs.stripe.com/capital/how-capital-for-platforms- | 0.751 | docs.stripe.com/capital/how-stripe-capital-works | 0.733 | docs.stripe.com/capital/how-stripe-capital-works | 0.728 |


**Q23: What are voucher payment methods used for?**
*(expects URL containing: `vouchers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/vouchers | 0.813 | docs.stripe.com/payments/payment-methods/overview | 0.733 | docs.stripe.com/payments/vouchers | 0.728 |
| crawl4ai | #1 | docs.stripe.com/payments/vouchers | 0.768 | docs.stripe.com/payments/vouchers | 0.715 | docs.stripe.com/payments/multibanco | 0.693 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/vouchers | 0.768 | docs.stripe.com/payments/vouchers | 0.715 | docs.stripe.com/payments/multibanco | 0.693 |
| scrapy+md | miss | docs.stripe.com/payments/oxxo/accept-a-payment | 0.656 | docs.stripe.com/js/payment_intents/create_radar_se | 0.652 | docs.stripe.com/js/tokens/create_token?type=pii | 0.652 |
| crawlee | #1 | docs.stripe.com/payments/vouchers | 0.775 | docs.stripe.com/api/payment_intents/create | 0.710 | docs.stripe.com/payments/vouchers | 0.700 |
| colly+md | miss | docs.stripe.com/api/payment/intents/create | 0.710 | docs.stripe.com/payments/multibanco | 0.699 | docs.stripe.com/payments/payment-methods/overview | 0.681 |
| playwright | #1 | docs.stripe.com/payments/vouchers | 0.775 | docs.stripe.com/api/payment_intents/create | 0.710 | docs.stripe.com/payments/vouchers | 0.700 |


**Q24: What happens when a customer chooses a voucher method for payment?**
*(expects URL containing: `vouchers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/vouchers | 0.805 | docs.stripe.com/payments/vouchers | 0.740 | docs.stripe.com/payments/konbini/accept-a-payment | 0.722 |
| crawl4ai | #1 | docs.stripe.com/payments/vouchers | 0.759 | docs.stripe.com/payments/vouchers | 0.741 | docs.stripe.com/payments/multibanco | 0.728 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/vouchers | 0.759 | docs.stripe.com/payments/vouchers | 0.741 | docs.stripe.com/payments/multibanco | 0.728 |
| scrapy+md | miss | docs.stripe.com/js/payment_intents/confirm_payment | 0.706 | docs.stripe.com/js/appendix/supported_locales | 0.706 | docs.stripe.com/js/element/payment_element | 0.706 |
| crawlee | #1 | docs.stripe.com/payments/vouchers | 0.748 | docs.stripe.com/payments/vouchers | 0.726 | docs.stripe.com/payments/multibanco | 0.720 |
| colly+md | miss | docs.stripe.com/payments/multibanco | 0.720 | docs.stripe.com/js#stripe-handle-card-action | 0.706 | docs.stripe.com/js#stripe-confirm-card-payment | 0.706 |
| playwright | #1 | docs.stripe.com/payments/vouchers | 0.748 | docs.stripe.com/payments/vouchers | 0.726 | docs.stripe.com/payments/multibanco | 0.720 |


**Q25: What is Pix and how does it work?**
*(expects URL containing: `pix`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/pix | 0.709 | docs.stripe.com/payments/link/pix | 0.658 | docs.stripe.com/payments/pix | 0.611 |
| crawl4ai | #1 | docs.stripe.com/payments/pix | 0.625 | docs.stripe.com/payments/pix | 0.568 | docs.stripe.com/payments/pix | 0.558 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/pix | 0.625 | docs.stripe.com/js/element/other_element | 0.574 | docs.stripe.com/js/element/other_element | 0.570 |
| scrapy+md | miss | docs.stripe.com/stripe-apps/components/img?app-sdk | 0.555 | docs.stripe.com/js/elements_object/create_element? | 0.554 | docs.stripe.com/js/appendix/payment_item_object | 0.554 |
| crawlee | #1 | docs.stripe.com/payments/pix | 0.683 | docs.stripe.com/api/setup_intents/create | 0.618 | docs.stripe.com/payments/pix | 0.606 |
| colly+md | #1 | docs.stripe.com/payments/pix | 0.683 | docs.stripe.com/payments/pix | 0.606 | docs.stripe.com/payments/cards/overview | 0.601 |
| playwright | #1 | docs.stripe.com/payments/pix | 0.683 | docs.stripe.com/api/setup_intents/create | 0.618 | docs.stripe.com/payments/pix | 0.606 |


**Q26: What are the transaction limits for Pix payments?**
*(expects URL containing: `pix`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/pix | 0.736 | docs.stripe.com/payments/pix | 0.695 | docs.stripe.com/payments/pix/accept-a-payment | 0.686 |
| crawl4ai | #1 | docs.stripe.com/payments/pix | 0.736 | docs.stripe.com/payments/pix | 0.701 | docs.stripe.com/payments/place-a-hold-on-a-payment | 0.675 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/pix | 0.736 | docs.stripe.com/payments/pix | 0.701 | docs.stripe.com/payments/place-a-hold-on-a-payment | 0.675 |
| scrapy+md | miss | docs.stripe.com/payments/place-a-hold-on-a-payment | 0.677 | docs.stripe.com/payments/overcapture | 0.677 | docs.stripe.com/payments/overcapture | 0.668 |
| crawlee | #1 | docs.stripe.com/payments/pix | 0.749 | docs.stripe.com/payments/pix | 0.739 | docs.stripe.com/payments/pix | 0.706 |
| colly+md | #1 | docs.stripe.com/payments/pix | 0.749 | docs.stripe.com/payments/pix | 0.739 | docs.stripe.com/payments/pix | 0.697 |
| playwright | #1 | docs.stripe.com/payments/pix | 0.749 | docs.stripe.com/payments/pix | 0.739 | docs.stripe.com/payments/pix | 0.698 |


**Q27: How can I securely accept payments online with Stripe?**
*(expects URL containing: `accept-a-payment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/accept-a-payment?payment- | 0.811 | docs.stripe.com/payments/accept-a-payment | 0.809 | docs.stripe.com/payments/accept-a-payment-synchron | 0.803 |
| crawl4ai | #1 | docs.stripe.com/payments/accept-a-payment?payment- | 0.822 | docs.stripe.com/payments/accept-a-payment | 0.822 | docs.stripe.com/payments/accept-a-payment?platform | 0.822 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/accept-a-payment?platform | 0.822 | docs.stripe.com/payments/accept-a-payment | 0.822 | docs.stripe.com/payments/accept-a-payment?payment- | 0.822 |
| scrapy+md | #1 | docs.stripe.com/payments/accept-a-payment?platform | 0.827 | docs.stripe.com/payments/accept-a-payment?integrat | 0.827 | docs.stripe.com/payments/accept-a-payment?payment- | 0.827 |
| crawlee | #7 | docs.stripe.com/payments/online-payments | 0.859 | docs.stripe.com/payments/payment-links | 0.852 | docs.stripe.com/payment-links | 0.852 |
| colly+md | #4 | docs.stripe.com/payments/online-payments#compare-f | 0.859 | docs.stripe.com/payments/online-payments | 0.859 | docs.stripe.com/payment-links | 0.853 |
| playwright | #7 | docs.stripe.com/payments/online-payments | 0.859 | docs.stripe.com/payment-links | 0.852 | docs.stripe.com/payments/payment-links | 0.852 |


**Q28: What should I do if a payment fails or is canceled during the Checkout process?**
*(expects URL containing: `accept-a-payment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/affirm/accept-a-payment | 0.767 | docs.stripe.com/payments/accept-a-payment-deferred | 0.757 | docs.stripe.com/payments/advanced/dashboard-paymen | 0.745 |
| crawl4ai | #7 | docs.stripe.com/payments/dashboard-payment-methods | 0.745 | docs.stripe.com/payments/sepa-debit | 0.742 | docs.stripe.com/refunds | 0.736 |
| crawl4ai-raw | #7 | docs.stripe.com/payments/dashboard-payment-methods | 0.745 | docs.stripe.com/payments/sepa-debit | 0.742 | docs.stripe.com/refunds | 0.736 |
| scrapy+md | #11 | docs.stripe.com/disputes/categories | 0.752 | docs.stripe.com/declines/codes | 0.751 | docs.stripe.com/payments/dashboard-payment-methods | 0.745 |
| crawlee | #11 | docs.stripe.com/payments/dashboard-payment-methods | 0.745 | docs.stripe.com/payments/mobile/accept-payment?int | 0.737 | docs.stripe.com/refunds | 0.736 |
| colly+md | #14 | docs.stripe.com/disputes/reason-codes-defense-requ | 0.739 | docs.stripe.com/refunds | 0.736 | docs.stripe.com/refunds#cancel-payment | 0.736 |
| playwright | #13 | docs.stripe.com/payments/dashboard-payment-methods | 0.745 | docs.stripe.com/payments/mobile/accept-payment?int | 0.737 | docs.stripe.com/refunds | 0.736 |


**Q29: What are the options for processing payments with third-party payment processors using Stripe Billing?**
*(expects URL containing: `third-party-payment-processing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/payment-methods/custom-pa | 0.768 | docs.stripe.com/payments/payment-methods/custom-pa | 0.760 | docs.stripe.com/payments/payment-methods/custom-pa | 0.758 |
| crawl4ai | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.799 | docs.stripe.com/billing/subscriptions/third-party- | 0.779 | docs.stripe.com/payments/more-payment-scenarios | 0.773 |
| crawl4ai-raw | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.799 | docs.stripe.com/billing/subscriptions/third-party- | 0.779 | docs.stripe.com/payments/more-payment-scenarios | 0.773 |
| scrapy+md | miss | docs.stripe.com/get-started/data-migrations/pan-im | 0.753 | docs.stripe.com/terminal/payments/additional-payme | 0.748 | docs.stripe.com/get-started/data-migrations/pan-im | 0.744 |
| crawlee | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.885 | docs.stripe.com/payments/payment-methods/integrati | 0.801 | docs.stripe.com/payments/advanced/payment-methods/ | 0.787 |
| colly+md | miss | docs.stripe.com/payments/payment-methods/integrati | 0.801 | docs.stripe.com/payments/payment-methods/integrati | 0.801 | docs.stripe.com/payments/payment-methods/integrati | 0.801 |
| playwright | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.885 | docs.stripe.com/payments/payment-methods/integrati | 0.801 | docs.stripe.com/payments/advanced/payment-methods/ | 0.787 |


**Q30: What are the limitations when integrating with a third-party payment processor?**
*(expects URL containing: `third-party-payment-processing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/payment-methods/custom-pa | 0.725 | docs.stripe.com/payments/payment-method-configurat | 0.702 | docs.stripe.com/payments/payment-methods/payment-m | 0.702 |
| crawl4ai | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.759 | docs.stripe.com/payments/payment-methods/custom-pa | 0.725 | docs.stripe.com/payments/more-payment-scenarios | 0.707 |
| crawl4ai-raw | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.759 | docs.stripe.com/payments/payment-methods/custom-pa | 0.725 | docs.stripe.com/payments/more-payment-scenarios | 0.707 |
| scrapy+md | miss | docs.stripe.com/get-started/data-migrations/pan-im | 0.703 | docs.stripe.com/payments/link/link-payment-integra | 0.700 | docs.stripe.com/js/setup_intents/confirm_card_setu | 0.696 |
| crawlee | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.808 | docs.stripe.com/billing/subscriptions/third-party- | 0.757 | docs.stripe.com/payments/payment-methods/custom-pa | 0.725 |
| colly+md | miss | docs.stripe.com/payments/place-a-hold-on-a-payment | 0.716 | docs.stripe.com/payments/payment-methods/integrati | 0.708 | docs.stripe.com/payments/payment-methods/integrati | 0.708 |
| playwright | #1 | docs.stripe.com/billing/subscriptions/third-party- | 0.808 | docs.stripe.com/billing/subscriptions/third-party- | 0.757 | docs.stripe.com/payments/payment-methods/custom-pa | 0.725 |


**Q31: What features does the Stripe extension for Visual Studio Code provide?**
*(expects URL containing: `stripe-vscode`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/elements | 0.709 | docs.stripe.com/payments/mobile/accept-payment?pla | 0.694 | docs.stripe.com/payments/mobile/accept-payment-emb | 0.694 |
| crawl4ai | #1 | docs.stripe.com/stripe-vscode | 0.862 | docs.stripe.com/stripe-vscode | 0.813 | docs.stripe.com/stripe-vscode | 0.772 |
| crawl4ai-raw | #1 | docs.stripe.com/stripe-vscode | 0.862 | docs.stripe.com/stripe-vscode | 0.813 | docs.stripe.com/stripe-vscode | 0.772 |
| scrapy+md | miss | docs.stripe.com/stripe-apps/components/img?app-sdk | 0.783 | docs.stripe.com/stripe-apps/components | 0.781 | docs.stripe.com/stripe-apps/ui-extension-developer | 0.780 |
| crawlee | #1 | docs.stripe.com/stripe-vscode | 0.921 | docs.stripe.com/stripe-vscode | 0.813 | docs.stripe.com/stripe-vscode | 0.805 |
| colly+md | #1 | docs.stripe.com/stripe-vscode | 0.921 | docs.stripe.com/stripe-vscode | 0.857 | docs.stripe.com/stripe-vscode | 0.805 |
| playwright | #1 | docs.stripe.com/stripe-vscode | 0.921 | docs.stripe.com/stripe-vscode | 0.813 | docs.stripe.com/stripe-vscode | 0.805 |


**Q32: How can I trigger and forward webhook events using Stripe for VS Code?**
*(expects URL containing: `stripe-vscode`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/managed-payments/set-up-m | 0.744 | docs.stripe.com/payments/payment-element/migration | 0.731 | docs.stripe.com/payments/payment-intents/verifying | 0.729 |
| crawl4ai | #1 | docs.stripe.com/stripe-vscode | 0.869 | docs.stripe.com/webhooks | 0.846 | docs.stripe.com/stripe-vscode | 0.823 |
| crawl4ai-raw | #1 | docs.stripe.com/stripe-vscode | 0.869 | docs.stripe.com/webhooks | 0.846 | docs.stripe.com/stripe-vscode | 0.823 |
| scrapy+md | miss | docs.stripe.com/billing/subscriptions/build-subscr | 0.807 | docs.stripe.com/cli/fixtures | 0.796 | docs.stripe.com/cli | 0.796 |
| crawlee | #4 | docs.stripe.com/webhooks | 0.848 | docs.stripe.com/webhooks/handling-payment-events | 0.847 | docs.stripe.com/webhooks | 0.846 |
| colly+md | #9 | docs.stripe.com/webhooks#verify-events | 0.848 | docs.stripe.com/webhooks | 0.848 | docs.stripe.com/webhooks/handling-payment-events | 0.847 |
| playwright | #4 | docs.stripe.com/webhooks | 0.848 | docs.stripe.com/webhooks/handling-payment-events | 0.847 | docs.stripe.com/webhooks | 0.846 |


**Q33: How can I create tax rates in Stripe?**
*(expects URL containing: `tax-rates`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/checkout/use-manual-tax-r | 0.830 | docs.stripe.com/payments/checkout/use-manual-tax-r | 0.815 | docs.stripe.com/payments/advanced/tax | 0.793 |
| crawl4ai | #1 | docs.stripe.com/tax/tax-rates | 0.864 | docs.stripe.com/tax/set-up | 0.806 | docs.stripe.com/tax/tax-rates | 0.793 |
| crawl4ai-raw | #1 | docs.stripe.com/tax/tax-rates | 0.864 | docs.stripe.com/tax/set-up | 0.806 | docs.stripe.com/tax/tax-rates | 0.793 |
| scrapy+md | miss | docs.stripe.com/billing/taxes/collect-taxes | 0.782 | docs.stripe.com/invoicing/taxes?dashboard-or-api=d | 0.772 | docs.stripe.com/llms.txt | 0.750 |
| crawlee | #1 | docs.stripe.com/tax/tax-rates | 0.852 | docs.stripe.com/tax/set-up | 0.823 | docs.stripe.com/api/tax/settings | 0.817 |
| colly+md | #1 | docs.stripe.com/tax/tax-rates | 0.852 | docs.stripe.com/tax/set-up | 0.823 | docs.stripe.com/api/tax/settings | 0.817 |
| playwright | #1 | docs.stripe.com/tax/tax-rates | 0.852 | docs.stripe.com/tax/set-up | 0.823 | docs.stripe.com/api/tax/settings | 0.817 |


**Q34: What are the required properties for creating a tax rate?**
*(expects URL containing: `tax-rates`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/checkout/use-manual-tax-r | 0.703 | docs.stripe.com/payments/checkout/use-manual-tax-r | 0.638 | docs.stripe.com/payments/checkout/use-manual-tax-r | 0.623 |
| crawl4ai | #1 | docs.stripe.com/tax/tax-rates | 0.714 | docs.stripe.com/tax/tax-rates | 0.628 | docs.stripe.com/tax/tax-rates | 0.619 |
| crawl4ai-raw | #1 | docs.stripe.com/tax/tax-rates | 0.714 | docs.stripe.com/tax/tax-rates | 0.628 | docs.stripe.com/tax/tax-rates | 0.619 |
| scrapy+md | miss | docs.stripe.com/js/elements_object/update | 0.673 | docs.stripe.com/js/element/payment_element | 0.673 | docs.stripe.com/js/payment_intents/create_radar_se | 0.673 |
| crawlee | #1 | docs.stripe.com/tax/tax-rates | 0.708 | docs.stripe.com/tax/tax-rates | 0.690 | docs.stripe.com/js/elements_object/create_payment_ | 0.675 |
| colly+md | #2 | docs.stripe.com/changelog/dahlia/2026-04-22/adds-e | 0.738 | docs.stripe.com/tax/tax-rates | 0.711 | docs.stripe.com/tax/tax-rates | 0.690 |
| playwright | #1 | docs.stripe.com/tax/tax-rates | 0.708 | docs.stripe.com/tax/tax-rates | 0.690 | docs.stripe.com/js/element/other_element | 0.676 |


**Q35: What is UPI and how does it work?**
*(expects URL containing: `upi`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/link/upi | 0.754 | docs.stripe.com/payments/upi | 0.749 | docs.stripe.com/payments/upi/upi-autopay | 0.636 |
| crawl4ai | #1 | docs.stripe.com/payments/upi | 0.662 | docs.stripe.com/payments/upi | 0.579 | docs.stripe.com/customer-management | 0.571 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/upi | 0.662 | docs.stripe.com/payments/upi | 0.579 | docs.stripe.com/customer-management | 0.571 |
| scrapy+md | #1 | docs.stripe.com/payments/upi | 0.664 | docs.stripe.com/payments/upi/upi-autopay | 0.650 | docs.stripe.com/payments/upi/accept-a-payment | 0.618 |
| crawlee | #1 | docs.stripe.com/payments/upi | 0.715 | docs.stripe.com/api/setup_intents/object | 0.631 | docs.stripe.com/api/setup_intents/create | 0.631 |
| colly+md | #1 | docs.stripe.com/changelog/dahlia/2026-03-25/adds-s | 0.673 | docs.stripe.com/api/setup/intents/object#setup/int | 0.631 | docs.stripe.com/api/setup/intents | 0.631 |
| playwright | #1 | docs.stripe.com/payments/upi | 0.715 | docs.stripe.com/api/setup_intents/create | 0.631 | docs.stripe.com/api/setup_intents/object | 0.631 |


**Q36: What are the transaction limits for UPI payments?**
*(expects URL containing: `upi`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/link/upi | 0.716 | docs.stripe.com/payments/upi/upi-autopay | 0.711 | docs.stripe.com/payments/upi | 0.710 |
| crawl4ai | #1 | docs.stripe.com/payments/upi | 0.740 | docs.stripe.com/payments/upi | 0.676 | docs.stripe.com/currencies | 0.644 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/upi | 0.740 | docs.stripe.com/payments/upi | 0.676 | docs.stripe.com/currencies | 0.644 |
| scrapy+md | #1 | docs.stripe.com/payments/upi | 0.734 | docs.stripe.com/payments/upi/upi-autopay | 0.702 | docs.stripe.com/payments/upi | 0.683 |
| crawlee | #1 | docs.stripe.com/payments/upi | 0.758 | docs.stripe.com/payments/upi | 0.733 | docs.stripe.com/payments/upi | 0.729 |
| colly+md | #1 | docs.stripe.com/changelog/dahlia/2026-03-25/adds-s | 0.685 | docs.stripe.com/api/setup/intents/object#setup/int | 0.662 | docs.stripe.com/api/setup/intents | 0.662 |
| playwright | #1 | docs.stripe.com/payments/upi | 0.758 | docs.stripe.com/payments/upi | 0.741 | docs.stripe.com/payments/upi | 0.733 |


**Q37: How can I fulfill orders using the Checkout Sessions API?**
*(expects URL containing: `fulfillment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/checkout | 0.768 | docs.stripe.com/payments/wero/accept-a-payment | 0.766 | docs.stripe.com/payments/advanced/shipping | 0.766 |
| crawl4ai | #1 | docs.stripe.com/checkout/fulfillment | 0.790 | docs.stripe.com/payments/accept-a-payment?payment- | 0.785 | docs.stripe.com/payments/accept-a-payment?platform | 0.785 |
| crawl4ai-raw | #1 | docs.stripe.com/checkout/fulfillment | 0.790 | docs.stripe.com/payments/accept-a-payment?platform | 0.785 | docs.stripe.com/payments/accept-a-payment?payment- | 0.785 |
| scrapy+md | #2 | docs.stripe.com/api/checkout/sessions/line_items | 0.788 | docs.stripe.com/checkout/fulfillment?payment-ui=st | 0.786 | docs.stripe.com/checkout/fulfillment?payment-ui=st | 0.783 |
| crawlee | #6 | docs.stripe.com/api/checkout/sessions | 0.806 | docs.stripe.com/payments/quickstart-checkout-sessi | 0.795 | docs.stripe.com/api/checkout/sessions | 0.788 |
| colly+md | #4 | docs.stripe.com/payments/checkout-sessions | 0.808 | docs.stripe.com/api/checkout/sessions | 0.806 | docs.stripe.com/payments/quickstart-checkout-sessi | 0.795 |
| playwright | #6 | docs.stripe.com/api/checkout/sessions | 0.806 | docs.stripe.com/payments/quickstart-checkout-sessi | 0.795 | docs.stripe.com/api/checkout/sessions | 0.788 |


**Q38: What is the recommended method for automating fulfillment in Stripe?**
*(expects URL containing: `fulfillment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/accept-a-payment?payment- | 0.744 | docs.stripe.com/payments/checkout/adjustable-quant | 0.727 | docs.stripe.com/payments/payment-intents/verifying | 0.726 |
| crawl4ai | #1 | docs.stripe.com/checkout/fulfillment | 0.790 | docs.stripe.com/checkout/fulfillment | 0.773 | docs.stripe.com/payment-links/post-payment | 0.769 |
| crawl4ai-raw | #1 | docs.stripe.com/checkout/fulfillment | 0.790 | docs.stripe.com/checkout/fulfillment | 0.773 | docs.stripe.com/payment-links/post-payment | 0.769 |
| scrapy+md | #1 | docs.stripe.com/checkout/fulfillment?payment-ui=st | 0.800 | docs.stripe.com/checkout/fulfillment?payment-ui=st | 0.758 | docs.stripe.com/billing/subscriptions/ideal | 0.749 |
| crawlee | #1 | docs.stripe.com/checkout/fulfillment | 0.824 | docs.stripe.com/checkout/fulfillment | 0.800 | docs.stripe.com/billing/revenue-recovery/customer- | 0.796 |
| colly+md | #1 | docs.stripe.com/checkout/fulfillment | 0.824 | docs.stripe.com/checkout/fulfillment | 0.800 | docs.stripe.com/billing/revenue-recovery/customer- | 0.796 |
| playwright | #1 | docs.stripe.com/checkout/fulfillment | 0.824 | docs.stripe.com/checkout/fulfillment | 0.800 | docs.stripe.com/billing/revenue-recovery/customer- | 0.796 |


**Q39: How can I view a payout's status in the Stripe Dashboard?**
*(expects URL containing: `manage-payouts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/bank-transfers/accept-a-p | 0.734 | docs.stripe.com/payments/orchestration/route-payme | 0.725 | docs.stripe.com/payments/pay-with-balance | 0.724 |
| crawl4ai | #1 | docs.stripe.com/global-payouts/manage-payouts | 0.841 | docs.stripe.com/bank-reconciliation | 0.838 | docs.stripe.com/global-payouts/manage-payouts | 0.795 |
| crawl4ai-raw | #1 | docs.stripe.com/global-payouts/manage-payouts | 0.841 | docs.stripe.com/bank-reconciliation | 0.838 | docs.stripe.com/global-payouts/manage-payouts | 0.795 |
| scrapy+md | miss | docs.stripe.com/reports/payout-reconciliation | 0.807 | docs.stripe.com/reports/payout-reconciliation | 0.801 | docs.stripe.com/payouts/reconciliation | 0.777 |
| crawlee | #2 | docs.stripe.com/bank-reconciliation | 0.838 | docs.stripe.com/global-payouts/manage-payouts | 0.831 | docs.stripe.com/payouts/instant-payouts | 0.828 |
| colly+md | #2 | docs.stripe.com/bank-reconciliation | 0.838 | docs.stripe.com/global-payouts/manage-payouts | 0.831 | docs.stripe.com/payouts/instant-payouts | 0.828 |
| playwright | #2 | docs.stripe.com/bank-reconciliation | 0.838 | docs.stripe.com/global-payouts/manage-payouts | 0.831 | docs.stripe.com/payouts/instant-payouts | 0.828 |


**Q40: What should I do if a payout has been returned due to incorrect destination information?**
*(expects URL containing: `manage-payouts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/bank-transfers | 0.702 | docs.stripe.com/payments/klarna/disputes | 0.689 | docs.stripe.com/payments/revolut-pay | 0.686 |
| crawl4ai | #1 | docs.stripe.com/global-payouts/manage-payouts | 0.772 | docs.stripe.com/global-payouts/manage-payouts | 0.714 | docs.stripe.com/connect/supported-embedded-compone | 0.701 |
| crawl4ai-raw | #1 | docs.stripe.com/global-payouts/manage-payouts | 0.772 | docs.stripe.com/global-payouts/manage-payouts | 0.714 | docs.stripe.com/connect/supported-embedded-compone | 0.701 |
| scrapy+md | miss | docs.stripe.com/api/refunds/object?rds=1 | 0.712 | docs.stripe.com/api/refunds/object | 0.712 | docs.stripe.com/disputes/categories | 0.701 |
| crawlee | #1 | docs.stripe.com/global-payouts/manage-payouts | 0.772 | docs.stripe.com/connect/supported-embedded-compone | 0.735 | docs.stripe.com/disputes/responding#decide | 0.726 |
| colly+md | #1 | docs.stripe.com/global-payouts/manage-payouts | 0.772 | docs.stripe.com/connect/supported-embedded-compone | 0.737 | docs.stripe.com/disputes/responding | 0.727 |
| playwright | #1 | docs.stripe.com/global-payouts/manage-payouts | 0.772 | docs.stripe.com/connect/supported-embedded-compone | 0.735 | docs.stripe.com/disputes/responding | 0.728 |


**Q41: How do I enable tax ID collection for new customers in Checkout?**
*(expects URL containing: `tax-ids`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/advanced/tax | 0.806 | docs.stripe.com/payments/advanced/tax | 0.766 | docs.stripe.com/payments/advanced/tax | 0.763 |
| crawl4ai | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.855 | docs.stripe.com/tax/checkout/tax-ids | 0.817 | docs.stripe.com/tax/checkout/tax-ids | 0.816 |
| crawl4ai-raw | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.855 | docs.stripe.com/tax/checkout/tax-ids | 0.817 | docs.stripe.com/tax/checkout/tax-ids | 0.816 |
| scrapy+md | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.854 | docs.stripe.com/tax/checkout/tax-ids | 0.816 | docs.stripe.com/tax/checkout/tax-ids | 0.814 |
| crawlee | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.864 | docs.stripe.com/tax/checkout/tax-ids | 0.852 | docs.stripe.com/tax/checkout/tax-ids | 0.841 |
| colly+md | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.861 | docs.stripe.com/tax/checkout/tax-ids | 0.852 | docs.stripe.com/tax/checkout/tax-ids | 0.841 |
| playwright | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.864 | docs.stripe.com/tax/checkout/tax-ids | 0.852 | docs.stripe.com/tax/checkout/tax-ids | 0.841 |


**Q42: What types of tax IDs can Checkout collect in different regions?**
*(expects URL containing: `tax-ids`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/advanced/tax | 0.787 | docs.stripe.com/payments/advanced/tax | 0.712 | docs.stripe.com/payments/advanced/tax | 0.693 |
| crawl4ai | #2 | docs.stripe.com/elements/tax-id-element | 0.751 | docs.stripe.com/tax/checkout/tax-ids | 0.732 | docs.stripe.com/tax/checkout/tax-ids | 0.727 |
| crawl4ai-raw | #2 | docs.stripe.com/elements/tax-id-element | 0.751 | docs.stripe.com/tax/checkout/tax-ids | 0.732 | docs.stripe.com/tax/checkout/tax-ids | 0.727 |
| scrapy+md | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.773 | docs.stripe.com/tax/invoicing/tax-ids | 0.733 | docs.stripe.com/tax/checkout/tax-ids | 0.732 |
| crawlee | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.809 | docs.stripe.com/payments/advanced/tax | 0.787 | docs.stripe.com/elements/tax-id-element | 0.751 |
| colly+md | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.773 | docs.stripe.com/tax/checkout/tax-ids | 0.747 | docs.stripe.com/tax/custom | 0.737 |
| playwright | #1 | docs.stripe.com/tax/checkout/tax-ids | 0.809 | docs.stripe.com/payments/advanced/tax | 0.787 | docs.stripe.com/elements/tax-id-element | 0.751 |


**Q43: How can I add funds to my stablecoin balance?**
*(expects URL containing: `stablecoins`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | docs.stripe.com/payments/accept-stablecoin-payment | 0.703 | docs.stripe.com/payments/stablecoin-payments | 0.699 | docs.stripe.com/payments/link/stablecoins | 0.686 |
| crawl4ai | #1 | docs.stripe.com/treasury/stablecoins | 0.791 | docs.stripe.com/treasury/stablecoins | 0.776 | docs.stripe.com/treasury | 0.766 |
| crawl4ai-raw | #1 | docs.stripe.com/treasury/stablecoins | 0.791 | docs.stripe.com/treasury/stablecoins | 0.776 | docs.stripe.com/treasury | 0.766 |
| scrapy+md | miss | docs.stripe.com/payments/accept-stablecoin-payment | 0.703 | docs.stripe.com/payments/accept-stablecoin-payment | 0.697 | docs.stripe.com/payments/deposit-mode-stablecoin-p | 0.686 |
| crawlee | #1 | docs.stripe.com/treasury/stablecoins | 0.791 | docs.stripe.com/treasury/stablecoins | 0.776 | docs.stripe.com/connect/stablecoin-payouts | 0.770 |
| colly+md | miss | docs.stripe.com/treasury | 0.766 | docs.stripe.com/connect/stablecoin-payouts | 0.763 | docs.stripe.com/connect/top-ups | 0.752 |
| playwright | #1 | docs.stripe.com/treasury/stablecoins | 0.791 | docs.stripe.com/treasury/stablecoins | 0.776 | docs.stripe.com/treasury | 0.766 |


**Q44: What currencies are supported for stablecoin payouts?**
*(expects URL containing: `stablecoins`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.stripe.com/payments/stablecoin-payments | 0.805 | docs.stripe.com/payments/link/stablecoins | 0.781 | docs.stripe.com/payments/accept-stablecoin-payment | 0.757 |
| crawl4ai | #1 | docs.stripe.com/treasury/stablecoins | 0.824 | docs.stripe.com/connect/stablecoin-payouts | 0.782 | docs.stripe.com/connect/stablecoin-payouts | 0.782 |
| crawl4ai-raw | #1 | docs.stripe.com/treasury/stablecoins | 0.824 | docs.stripe.com/connect/stablecoin-payouts | 0.782 | docs.stripe.com/connect/stablecoin-payouts | 0.782 |
| scrapy+md | #21 | docs.stripe.com/payments/accept-stablecoin-payment | 0.754 | docs.stripe.com/payments/accept-stablecoin-payment | 0.750 | docs.stripe.com/connect/saas/tasks/payout | 0.724 |
| crawlee | #1 | docs.stripe.com/treasury/stablecoins | 0.824 | docs.stripe.com/connect/stablecoin-payouts | 0.782 | docs.stripe.com/connect/stablecoin-payouts | 0.757 |
| colly+md | miss | docs.stripe.com/connect/stablecoin-payouts | 0.778 | docs.stripe.com/connect/stablecoin-payouts | 0.757 | docs.stripe.com/currencies#minimum-and-maximum-cha | 0.754 |
| playwright | #1 | docs.stripe.com/treasury/stablecoins | 0.824 | docs.stripe.com/connect/stablecoin-payouts | 0.776 | docs.stripe.com/connect/stablecoin-payouts | 0.757 |


**Q45: What documents does Atlas use to incorporate your company?**
*(expects URL containing: `incorporation-documents`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/managed-payments/eligibil | 0.556 | docs.stripe.com/payments/bacs-debit/mandate-collec | 0.544 | docs.stripe.com/payments/bacs-debit/mandate-collec | 0.536 |
| crawl4ai | #1 | docs.stripe.com/atlas/incorporation-documents | 0.907 | docs.stripe.com/atlas/signup | 0.811 | docs.stripe.com/atlas/incorporation-documents | 0.804 |
| crawl4ai-raw | #1 | docs.stripe.com/atlas/incorporation-documents | 0.907 | docs.stripe.com/atlas/signup | 0.811 | docs.stripe.com/atlas/incorporation-documents | 0.804 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.732 | docs.stripe.com/js/payment_intents/confirm_payment | 0.570 | docs.stripe.com/js/payment_methods/create_payment_ | 0.570 |
| crawlee | #1 | docs.stripe.com/atlas/incorporation-documents | 0.899 | docs.stripe.com/atlas/signup | 0.813 | docs.stripe.com/atlas/signup | 0.810 |
| colly+md | miss | docs.stripe.com/atlas | 0.789 | docs.stripe.com/atlas/accept-payments | 0.758 | docs.stripe.com/atlas/indian-founder-guide | 0.747 |
| playwright | #1 | docs.stripe.com/atlas/incorporation-documents | 0.899 | docs.stripe.com/atlas/signup | 0.813 | docs.stripe.com/atlas/signup | 0.810 |


**Q46: What is the purpose of the Certificate of Incorporation?**
*(expects URL containing: `incorporation-documents`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/managed-payments/eligibil | 0.521 | docs.stripe.com/payments/managed-payments/eligibil | 0.514 | docs.stripe.com/payments/managed-payments/eligibil | 0.509 |
| crawl4ai | #1 | docs.stripe.com/atlas/incorporation-documents | 0.668 | docs.stripe.com/atlas/signup | 0.625 | docs.stripe.com/atlas/company-types | 0.618 |
| crawl4ai-raw | #1 | docs.stripe.com/atlas/incorporation-documents | 0.668 | docs.stripe.com/atlas/signup | 0.625 | docs.stripe.com/atlas/company-types | 0.618 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.584 | docs.stripe.com/js/custom_checkout/create_currency | 0.571 | docs.stripe.com/js/custom_checkout/session_object | 0.571 |
| crawlee | #1 | docs.stripe.com/atlas/incorporation-documents | 0.721 | docs.stripe.com/atlas/incorporation-documents | 0.660 | docs.stripe.com/atlas/signup | 0.657 |
| colly+md | miss | docs.stripe.com/atlas | 0.604 | docs.stripe.com/atlas | 0.591 | docs.stripe.com/api/accounts/update#update/account | 0.587 |
| playwright | #1 | docs.stripe.com/atlas/incorporation-documents | 0.721 | docs.stripe.com/atlas/incorporation-documents | 0.660 | docs.stripe.com/atlas/signup | 0.657 |


**Q47: What countries is Stripe Issuing available in?**
*(expects URL containing: `issuing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/cards | 0.765 | docs.stripe.com/payments/local-markets | 0.720 | docs.stripe.com/payments/cards/surcharge | 0.694 |
| crawl4ai | #8 | docs.stripe.com/payments/cards | 0.765 | docs.stripe.com/currencies | 0.747 | docs.stripe.com/payouts | 0.734 |
| crawl4ai-raw | #8 | docs.stripe.com/payments/cards | 0.765 | docs.stripe.com/currencies | 0.747 | docs.stripe.com/payouts | 0.734 |
| scrapy+md | miss | docs.stripe.com/disputes/prevention/verification | 0.712 | docs.stripe.com/api/country_specs?api-version=2026 | 0.708 | docs.stripe.com/payouts/instant-payouts | 0.705 |
| crawlee | #6 | docs.stripe.com/payments/pay-with-balance | 0.787 | docs.stripe.com/payments/local-markets | 0.767 | docs.stripe.com/payments/cards | 0.765 |
| colly+md | #9 | docs.stripe.com/payments/pay-with-balance | 0.787 | docs.stripe.com/payments/local-markets | 0.767 | docs.stripe.com/payments/cards#supported-card-bran | 0.765 |
| playwright | #7 | docs.stripe.com/payments/pay-with-balance | 0.787 | docs.stripe.com/payments/local-markets | 0.767 | docs.stripe.com/payments/cards | 0.765 |


**Q48: What features does Stripe Issuing offer for managing purchases?**
*(expects URL containing: `issuing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/flexible-payments | 0.779 | docs.stripe.com/payments/mobile | 0.759 | docs.stripe.com/payments/elements | 0.756 |
| crawl4ai | #26 | docs.stripe.com/payments/advanced | 0.780 | docs.stripe.com/payments/checkout/product-catalog | 0.771 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.769 |
| crawl4ai-raw | #24 | docs.stripe.com/payments/advanced | 0.780 | docs.stripe.com/payments/checkout/product-catalog | 0.771 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.769 |
| scrapy+md | miss | docs.stripe.com/payments/checkout/how-checkout-wor | 0.764 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.750 | docs.stripe.com/payments/checkout/update-customer | 0.748 |
| crawlee | miss | docs.stripe.com/payments/advanced/payment-methods/ | 0.792 | docs.stripe.com/payments/checkout/payment-methods | 0.792 | docs.stripe.com/payments/advanced | 0.786 |
| colly+md | #8 | docs.stripe.com/payments/managed-payments | 0.781 | docs.stripe.com/payments/payment-methods/integrati | 0.769 | docs.stripe.com/payments/payment-methods/integrati | 0.769 |
| playwright | miss | docs.stripe.com/payments/advanced/payment-methods/ | 0.792 | docs.stripe.com/payments/checkout/payment-methods | 0.792 | docs.stripe.com/elements/customer-sheet | 0.783 |


**Q49: What are the additional fees for accepting payments with installments in Mexico?**
*(expects URL containing: `mx-installments`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/mx-installments | 0.819 | docs.stripe.com/payments/mx-installments | 0.804 | docs.stripe.com/payments/meses-sin-intereses/accep | 0.757 |
| crawl4ai | #1 | docs.stripe.com/payments/mx-installments | 0.783 | docs.stripe.com/payments/mx-installments | 0.760 | docs.stripe.com/payments/mx-installments | 0.741 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/mx-installments | 0.783 | docs.stripe.com/payments/mx-installments | 0.760 | docs.stripe.com/payments/mx-installments | 0.741 |
| scrapy+md | miss | docs.stripe.com/payments/installments | 0.747 | docs.stripe.com/payments/oxxo/accept-a-payment | 0.656 | docs.stripe.com/connect/custom-accounts | 0.628 |
| crawlee | #1 | docs.stripe.com/payments/mx-installments | 0.804 | docs.stripe.com/payments/mx-installments | 0.797 | docs.stripe.com/payments/mx-installments | 0.793 |
| colly+md | miss | docs.stripe.com/recurring-payments#recurring-donat | 0.776 | docs.stripe.com/recurring-payments#accept-recurrin | 0.776 | docs.stripe.com/recurring-payments | 0.776 |
| playwright | #1 | docs.stripe.com/payments/mx-installments | 0.804 | docs.stripe.com/payments/mx-installments | 0.797 | docs.stripe.com/payments/mx-installments | 0.793 |


**Q50: What are the requirements for using installments (meses sin intereses) with Stripe in Mexico?**
*(expects URL containing: `mx-installments`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/mx-installments | 0.878 | docs.stripe.com/payments/mx-installments | 0.864 | docs.stripe.com/payments/meses-sin-intereses/accep | 0.847 |
| crawl4ai | #1 | docs.stripe.com/payments/mx-installments | 0.854 | docs.stripe.com/payments/mx-installments | 0.845 | docs.stripe.com/payments/mx-installments | 0.776 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/mx-installments | 0.854 | docs.stripe.com/payments/mx-installments | 0.845 | docs.stripe.com/payments/mx-installments | 0.776 |
| scrapy+md | miss | docs.stripe.com/payments/installments | 0.785 | docs.stripe.com/payments/oxxo/accept-a-payment | 0.715 | docs.stripe.com/india-recurring-payments | 0.689 |
| crawlee | #1 | docs.stripe.com/payments/mx-installments | 0.895 | docs.stripe.com/payments/mx-installments | 0.878 | docs.stripe.com/payments/mx-installments | 0.864 |
| colly+md | miss | docs.stripe.com/recurring-payments#installment-pla | 0.765 | docs.stripe.com/recurring-payments#migrate-subscri | 0.765 | docs.stripe.com/recurring-payments#accept-recurrin | 0.765 |
| playwright | #1 | docs.stripe.com/payments/mx-installments | 0.895 | docs.stripe.com/payments/mx-installments | 0.878 | docs.stripe.com/payments/mx-installments | 0.864 |


**Q51: What is the purpose of the Stripebot web crawler?**
*(expects URL containing: `stripebot-crawler`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/bank-transfers/accept-a-p | 0.605 | docs.stripe.com/payments/ideal/save-during-payment | 0.605 | docs.stripe.com/payments/accept-a-payment?api-inte | 0.605 |
| crawl4ai | #1 | docs.stripe.com/stripebot-crawler | 0.828 | docs.stripe.com/stripebot-crawler | 0.757 | docs.stripe.com/samples/identity/redirect | 0.691 |
| crawl4ai-raw | #1 | docs.stripe.com/stripebot-crawler | 0.828 | docs.stripe.com/stripebot-crawler | 0.757 | docs.stripe.com/samples/identity/redirect | 0.691 |
| scrapy+md | miss | docs.stripe.com/disputes/categories | 0.639 | docs.stripe.com/api/terminal/readers/object | 0.636 | docs.stripe.com/cli | 0.635 |
| crawlee | #1 | docs.stripe.com/stripebot-crawler | 0.909 | docs.stripe.com/stripebot-crawler | 0.787 | docs.stripe.com/stripebot-crawler | 0.758 |
| colly+md | #1 | docs.stripe.com/stripebot-crawler | 0.909 | docs.stripe.com/stripebot-crawler | 0.787 | docs.stripe.com/stripebot-crawler | 0.755 |
| playwright | #1 | docs.stripe.com/stripebot-crawler | 0.909 | docs.stripe.com/stripebot-crawler | 0.787 | docs.stripe.com/stripebot-crawler | 0.757 |


**Q52: How can I verify that a web crawler accessing my server is Stripebot?**
*(expects URL containing: `stripebot-crawler`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/ideal/save-during-payment | 0.668 | docs.stripe.com/payments/bank-transfers/accept-a-p | 0.668 | docs.stripe.com/payments/accept-a-payment?api-inte | 0.668 |
| crawl4ai | #1 | docs.stripe.com/stripebot-crawler | 0.831 | docs.stripe.com/stripebot-crawler | 0.813 | docs.stripe.com/samples/identity/redirect | 0.707 |
| crawl4ai-raw | #1 | docs.stripe.com/stripebot-crawler | 0.831 | docs.stripe.com/stripebot-crawler | 0.813 | docs.stripe.com/samples/identity/redirect | 0.707 |
| scrapy+md | miss | docs.stripe.com/disputes/prevention/identifying-fr | 0.676 | docs.stripe.com/error-low-level | 0.671 | docs.stripe.com/js/payment_intents/handle_card_act | 0.669 |
| crawlee | #1 | docs.stripe.com/stripebot-crawler | 0.813 | docs.stripe.com/stripebot-crawler | 0.802 | docs.stripe.com/stripebot-crawler | 0.747 |
| colly+md | #1 | docs.stripe.com/stripebot-crawler | 0.808 | docs.stripe.com/stripebot-crawler | 0.802 | docs.stripe.com/stripebot-crawler | 0.747 |
| playwright | #1 | docs.stripe.com/stripebot-crawler | 0.813 | docs.stripe.com/stripebot-crawler | 0.802 | docs.stripe.com/stripebot-crawler | 0.747 |


**Q53: How can I securely accept payments online with Stripe?**
*(expects URL containing: `accept-a-payment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/accept-a-payment?payment- | 0.811 | docs.stripe.com/payments/accept-a-payment | 0.809 | docs.stripe.com/payments/accept-a-payment-synchron | 0.803 |
| crawl4ai | #1 | docs.stripe.com/payments/accept-a-payment?payment- | 0.822 | docs.stripe.com/payments/accept-a-payment | 0.822 | docs.stripe.com/payments/accept-a-payment?platform | 0.822 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/accept-a-payment?platform | 0.822 | docs.stripe.com/payments/accept-a-payment | 0.822 | docs.stripe.com/payments/accept-a-payment?payment- | 0.822 |
| scrapy+md | #1 | docs.stripe.com/payments/accept-a-payment?platform | 0.827 | docs.stripe.com/payments/accept-a-payment?integrat | 0.827 | docs.stripe.com/payments/accept-a-payment?payment- | 0.827 |
| crawlee | #7 | docs.stripe.com/payments/online-payments | 0.859 | docs.stripe.com/payments/payment-links | 0.852 | docs.stripe.com/payment-links | 0.852 |
| colly+md | #4 | docs.stripe.com/payments/online-payments#compare-f | 0.859 | docs.stripe.com/payments/online-payments | 0.859 | docs.stripe.com/payment-links | 0.853 |
| playwright | #7 | docs.stripe.com/payments/online-payments | 0.859 | docs.stripe.com/payment-links | 0.852 | docs.stripe.com/payments/payment-links | 0.852 |


**Q54: What is a Checkout Session in Stripe?**
*(expects URL containing: `accept-a-payment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #10 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.801 | docs.stripe.com/payments/checkout-sessions | 0.788 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.781 |
| crawl4ai | #11 | docs.stripe.com/api/checkout/sessions/create | 0.818 | docs.stripe.com/api/checkout/sessions/object | 0.818 | docs.stripe.com/api/checkout/sessions | 0.818 |
| crawl4ai-raw | #15 | docs.stripe.com/api/checkout/sessions/object | 0.818 | docs.stripe.com/api/checkout/sessions/create | 0.818 | docs.stripe.com/api/checkout/sessions | 0.818 |
| scrapy+md | #6 | docs.stripe.com/api/checkout/sessions/line_items | 0.817 | docs.stripe.com/api/checkout/sessions/retrieve | 0.808 | docs.stripe.com/api/checkout/sessions/list | 0.804 |
| crawlee | #8 | docs.stripe.com/api/checkout/sessions | 0.920 | docs.stripe.com/api/checkout/sessions/object#check | 0.913 | docs.stripe.com/api/checkout/sessions/create | 0.901 |
| colly+md | #11 | docs.stripe.com/api/checkout/sessions | 0.920 | docs.stripe.com/api/checkout/sessions/object#check | 0.913 | docs.stripe.com/api/checkout/sessions/create | 0.901 |
| playwright | #8 | docs.stripe.com/api/checkout/sessions | 0.920 | docs.stripe.com/api/checkout/sessions/object | 0.913 | docs.stripe.com/api/checkout/sessions/create | 0.901 |


**Q55: How can I access consolidated reports for multiple accounts in my organization?**
*(expects URL containing: `multiple-accounts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/payment-methods/payment-m | 0.602 | docs.stripe.com/payments/bacs-debit/save-bank-deta | 0.586 | docs.stripe.com/payments/analytics/payment-methods | 0.581 |
| crawl4ai | #1 | docs.stripe.com/reports/multiple-accounts | 0.777 | docs.stripe.com/reports/multiple-accounts | 0.694 | docs.stripe.com/reports/options | 0.679 |
| crawl4ai-raw | #1 | docs.stripe.com/reports/multiple-accounts | 0.777 | docs.stripe.com/reports/multiple-accounts | 0.694 | docs.stripe.com/reports/options | 0.679 |
| scrapy+md | miss | docs.stripe.com/reports/options | 0.681 | docs.stripe.com/reports/report-types/connect | 0.677 | docs.stripe.com/stripe-data/query-connect-data | 0.670 |
| crawlee | #1 | docs.stripe.com/reports/multiple-accounts | 0.834 | docs.stripe.com/reports/multiple-accounts | 0.736 | docs.stripe.com/stripe-reports | 0.729 |
| colly+md | #1 | docs.stripe.com/reports/multiple-accounts | 0.827 | docs.stripe.com/reports/multiple-accounts | 0.736 | docs.stripe.com/stripe-reports | 0.729 |
| playwright | #1 | docs.stripe.com/reports/multiple-accounts | 0.834 | docs.stripe.com/reports/multiple-accounts | 0.736 | docs.stripe.com/stripe-reports | 0.729 |


**Q56: What are the file size limits for downloading reports from multiple accounts?**
*(expects URL containing: `multiple-accounts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/payto | 0.564 | docs.stripe.com/payments/payto | 0.557 | docs.stripe.com/payments/managed-payments/eligibil | 0.554 |
| crawl4ai | #1 | docs.stripe.com/reports/multiple-accounts | 0.651 | docs.stripe.com/reports/multiple-accounts | 0.636 | docs.stripe.com/disputes/best-practices | 0.613 |
| crawl4ai-raw | #1 | docs.stripe.com/reports/multiple-accounts | 0.651 | docs.stripe.com/reports/multiple-accounts | 0.636 | docs.stripe.com/disputes/best-practices | 0.613 |
| scrapy+md | miss | docs.stripe.com/reports/api | 0.623 | docs.stripe.com/reports/report-types/connect | 0.620 | docs.stripe.com/reports/api | 0.610 |
| crawlee | #1 | docs.stripe.com/reports/multiple-accounts | 0.815 | docs.stripe.com/reports/multiple-accounts | 0.808 | docs.stripe.com/reports/multiple-accounts | 0.758 |
| colly+md | #1 | docs.stripe.com/reports/multiple-accounts | 0.808 | docs.stripe.com/reports/multiple-accounts | 0.807 | docs.stripe.com/reports/multiple-accounts | 0.683 |
| playwright | #1 | docs.stripe.com/reports/multiple-accounts | 0.825 | docs.stripe.com/reports/multiple-accounts | 0.808 | docs.stripe.com/reports/multiple-accounts | 0.701 |


**Q57: How do I enable Link in my payment method settings?**
*(expects URL containing: `link-payment-integrations`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #9 | docs.stripe.com/payments/link/card-element-link | 0.790 | docs.stripe.com/payments/link/checkout-link | 0.784 | docs.stripe.com/payments/link/link-payment-methods | 0.784 |
| crawl4ai | #6 | docs.stripe.com/payments/link/checkout-link | 0.788 | docs.stripe.com/payments/link/instant-bank-payment | 0.763 | docs.stripe.com/payments/link/link-payment-methods | 0.760 |
| crawl4ai-raw | #6 | docs.stripe.com/payments/link/checkout-link | 0.788 | docs.stripe.com/payments/link/instant-bank-payment | 0.763 | docs.stripe.com/payments/link/link-payment-methods | 0.760 |
| scrapy+md | #42 | docs.stripe.com/payments/link/card-element-link | 0.790 | docs.stripe.com/mobile/digital-goods/payment-links | 0.762 | docs.stripe.com/payments/link/card-element-link | 0.761 |
| crawlee | miss | docs.stripe.com/payments/elements | 0.786 | docs.stripe.com/payments/link/link-payment-methods | 0.786 | docs.stripe.com/payments/link/checkout-link | 0.785 |
| colly+md | miss | docs.stripe.com/payments/elements | 0.786 | docs.stripe.com/changelog/dahlia/2026-03-25/visa-c | 0.783 | docs.stripe.com/changelog/dahlia/2026-03-25/capabi | 0.783 |
| playwright | miss | docs.stripe.com/payments/elements | 0.786 | docs.stripe.com/payments/link/link-payment-methods | 0.784 | docs.stripe.com/payments/link/checkout-link | 0.783 |


**Q58: What types of payment methods are supported by Link?**
*(expects URL containing: `link-payment-integrations`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #7 | docs.stripe.com/payments/link/link-payment-methods | 0.856 | docs.stripe.com/payments/link/link-payment-methods | 0.836 | docs.stripe.com/payments/link | 0.820 |
| crawl4ai | #2 | docs.stripe.com/payments/link/link-payment-methods | 0.853 | docs.stripe.com/payments/link/link-payment-integra | 0.832 | docs.stripe.com/payments/link | 0.812 |
| crawl4ai-raw | #2 | docs.stripe.com/payments/link/link-payment-methods | 0.853 | docs.stripe.com/payments/link/link-payment-integra | 0.832 | docs.stripe.com/payments/link | 0.812 |
| scrapy+md | #1 | docs.stripe.com/payments/link/link-payment-integra | 0.830 | docs.stripe.com/llms.txt | 0.793 | docs.stripe.com/js/setup_intents/confirm_setup | 0.765 |
| crawlee | #2 | docs.stripe.com/payments/link/link-payment-methods | 0.847 | docs.stripe.com/payments/link/link-payment-integra | 0.833 | docs.stripe.com/payments/link/link-payment-methods | 0.832 |
| colly+md | miss | docs.stripe.com/payments/link/link-payment-methods | 0.847 | docs.stripe.com/payments/link/link-payment-methods | 0.827 | docs.stripe.com/payments/wallets/link | 0.818 |
| playwright | #2 | docs.stripe.com/payments/link/link-payment-methods | 0.847 | docs.stripe.com/payments/link/link-payment-integra | 0.830 | docs.stripe.com/payments/link/link-payment-methods | 0.828 |


</details>

## Methodology

- **Queries:** 561 across 11 sites, categorized by type (api-function, code-example, conceptual, structured-data, factual-lookup, cross-page, navigation, js-rendered)
- **Embedding model:** `mixedbread-ai/mxbai-embed-large-v1` (1536 dimensions)
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

