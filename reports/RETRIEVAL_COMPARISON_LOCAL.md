# Retrieval Quality Comparison
<!-- style: v2, 2026-05-06 -->

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

**104 queries** across 11 sites.
Hit rate = correct source page in top-K results. Higher is better.
Summary tables use the **88-query common subset** (9 sites) so all tools are compared on identical queries. Sites excluded: huggingface-transformers, newegg (not all tools have data). Per-site tables show full results.

## Quick summary: best retrieval mode per tool

For each tool, the mode with the highest MRR. Most readers can stop here.

| Tool | Best mode | Hit@10 | MRR |
|---|---|---|---|
| crawlee | embedding | 77% (68/88) ±9% | 0.666 |
| playwright | embedding | 78% (69/88) ±8% | 0.640 |
| crawl4ai | embedding | 75% (66/88) ±9% | 0.633 |
| crawl4ai-raw | embedding | 75% (66/88) ±9% | 0.633 |
| colly+md | embedding | 68% (60/88) ±10% | 0.547 |
| markcrawl | embedding | 61% (54/88) ±10% | 0.531 |
| scrapy+md | reranked | 45% (40/88) ±10% | 0.352 |

> **Column definitions:** **Best mode** = retrieval strategy that maximizes MRR for this tool. **Hit@10** = correct source page in top 10 results. **MRR** = Mean Reciprocal Rank (1/rank of correct result, averaged).

## Summary: retrieval modes compared

_Computed over 88 queries on 9 common sites (ikea, kubernetes-docs, mdn-css, postgres-docs, propublica, react-dev, rust-book, smittenkitchen, stripe-docs)._

| Tool | Mode | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR |
|---|---|---|---|---|---|---|---|
| crawlee | embedding | 60% (53/88) ±10% | 72% (63/88) ±9% | 75% (66/88) ±9% | 77% (68/88) ±9% | 77% (68/88) ±9% | 0.666 |
| playwright | embedding | 57% (50/88) ±10% | 69% (61/88) ±9% | 73% (64/88) ±9% | 78% (69/88) ±8% | 80% (70/88) ±8% | 0.640 |
| crawl4ai | embedding | 55% (48/88) ±10% | 70% (62/88) ±9% | 72% (63/88) ±9% | 75% (66/88) ±9% | 77% (68/88) ±9% | 0.633 |
| crawl4ai-raw | embedding | 55% (48/88) ±10% | 70% (62/88) ±9% | 72% (63/88) ±9% | 75% (66/88) ±9% | 76% (67/88) ±9% | 0.633 |
| colly+md | embedding | 49% (43/88) ±10% | 57% (50/88) ±10% | 61% (54/88) ±10% | 68% (60/88) ±10% | 72% (63/88) ±9% | 0.547 |
| markcrawl | embedding | 45% (40/88) ±10% | 61% (54/88) ±10% | 61% (54/88) ±10% | 61% (54/88) ±10% | 65% (57/88) ±10% | 0.531 |
| scrapy+md | embedding | 32% (28/88) ±10% | 36% (32/88) ±10% | 39% (34/88) ±10% | 41% (36/88) ±10% | 44% (39/88) ±10% | 0.351 |
| markcrawl | bm25 | 20% (18/88) ±8% | 32% (28/88) ±10% | 41% (36/88) ±10% | 51% (45/88) ±10% | 58% (51/88) ±10% | 0.300 |
| scrapy+md | bm25 | 25% (22/88) ±9% | 33% (29/88) ±10% | 35% (31/88) ±10% | 39% (34/88) ±10% | 44% (39/88) ±10% | 0.299 |
| crawlee | bm25 | 20% (18/88) ±8% | 30% (26/88) ±9% | 39% (34/88) ±10% | 53% (47/88) ±10% | 57% (50/88) ±10% | 0.291 |
| crawl4ai | bm25 | 19% (17/88) ±8% | 30% (26/88) ±9% | 40% (35/88) ±10% | 49% (43/88) ±10% | 55% (48/88) ±10% | 0.281 |
| crawl4ai-raw | bm25 | 18% (16/88) ±8% | 30% (26/88) ±9% | 39% (34/88) ±10% | 48% (42/88) ±10% | 55% (48/88) ±10% | 0.276 |
| playwright | bm25 | 18% (16/88) ±8% | 31% (27/88) ±9% | 38% (33/88) ±10% | 51% (45/88) ±10% | 56% (49/88) ±10% | 0.273 |
| colly+md | bm25 | 17% (15/88) ±8% | 27% (24/88) ±9% | 30% (26/88) ±9% | 42% (37/88) ±10% | 49% (43/88) ±10% | 0.243 |
| crawlee | hybrid | 45% (40/88) ±10% | 59% (52/88) ±10% | 66% (58/88) ±10% | 75% (66/88) ±9% | 78% (69/88) ±8% | 0.543 |
| crawl4ai-raw | hybrid | 43% (38/88) ±10% | 60% (53/88) ±10% | 68% (60/88) ±10% | 72% (63/88) ±9% | 76% (67/88) ±9% | 0.542 |
| crawl4ai | hybrid | 41% (36/88) ±10% | 59% (52/88) ±10% | 66% (58/88) ±10% | 72% (63/88) ±9% | 77% (68/88) ±9% | 0.529 |
| playwright | hybrid | 43% (38/88) ±10% | 58% (51/88) ±10% | 62% (55/88) ±10% | 73% (64/88) ±9% | 78% (69/88) ±8% | 0.524 |
| colly+md | hybrid | 36% (32/88) ±10% | 51% (45/88) ±10% | 52% (46/88) ±10% | 58% (51/88) ±10% | 70% (62/88) ±9% | 0.449 |
| markcrawl | hybrid | 31% (27/88) ±9% | 50% (44/88) ±10% | 55% (48/88) ±10% | 60% (53/88) ±10% | 62% (55/88) ±10% | 0.419 |
| scrapy+md | hybrid | 28% (25/88) ±9% | 39% (34/88) ±10% | 42% (37/88) ±10% | 43% (38/88) ±10% | 44% (39/88) ±10% | 0.339 |
| crawlee | reranked | 40% (35/88) ±10% | 61% (54/88) ±10% | 70% (62/88) ±9% | 76% (67/88) ±9% | 78% (69/88) ±8% | 0.523 |
| playwright | reranked | 36% (32/88) ±10% | 60% (53/88) ±10% | 69% (61/88) ±9% | 76% (67/88) ±9% | 78% (69/88) ±8% | 0.500 |
| crawl4ai-raw | reranked | 34% (30/88) ±10% | 56% (49/88) ±10% | 67% (59/88) ±10% | 74% (65/88) ±9% | 80% (70/88) ±8% | 0.473 |
| crawl4ai | reranked | 33% (29/88) ±10% | 57% (50/88) ±10% | 66% (58/88) ±10% | 74% (65/88) ±9% | 81% (71/88) ±8% | 0.469 |
| colly+md | reranked | 35% (31/88) ±10% | 58% (51/88) ±10% | 60% (53/88) ±10% | 67% (59/88) ±10% | 74% (65/88) ±9% | 0.469 |
| markcrawl | reranked | 36% (32/88) ±10% | 50% (44/88) ±10% | 57% (50/88) ±10% | 62% (55/88) ±10% | 64% (56/88) ±10% | 0.450 |
| scrapy+md | reranked | 30% (26/88) ±9% | 39% (34/88) ±10% | 43% (38/88) ±10% | 45% (40/88) ±10% | 47% (41/88) ±10% | 0.352 |

> **Column definitions:** **Hit@K** = percentage of queries where the correct source page appeared in the top K results (shown as % with raw counts). **MRR** (Mean Reciprocal Rank) = average of 1/rank for correct results (1.0 = always rank 1, 0.5 = always rank 2). **Mode** = retrieval strategy used (see definitions above).

## Summary: embedding-only (hit rate at multiple K values)

_Computed over 88 queries on 9 common sites._

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Avg words |
|---|---|---|---|---|---|---|---|---|
| crawlee | 60% (53/88) ±10% | 72% (63/88) ±9% | 75% (66/88) ±9% | 77% (68/88) ±9% | 77% (68/88) ±9% | 0.666 | 58912 | 382 |
| playwright | 57% (50/88) ±10% | 69% (61/88) ±9% | 73% (64/88) ±9% | 78% (69/88) ±8% | 80% (70/88) ±8% | 0.640 | 56855 | 382 |
| crawl4ai | 55% (48/88) ±10% | 70% (62/88) ±9% | 72% (63/88) ±9% | 75% (66/88) ±9% | 77% (68/88) ±9% | 0.633 | 24400 | 345 |
| crawl4ai-raw | 55% (48/88) ±10% | 70% (62/88) ±9% | 72% (63/88) ±9% | 75% (66/88) ±9% | 76% (67/88) ±9% | 0.633 | 25245 | 344 |
| colly+md | 49% (43/88) ±10% | 57% (50/88) ±10% | 61% (54/88) ±10% | 68% (60/88) ±10% | 72% (63/88) ±9% | 0.547 | 59078 | 385 |
| markcrawl | 45% (40/88) ±10% | 61% (54/88) ±10% | 61% (54/88) ±10% | 61% (54/88) ±10% | 65% (57/88) ±10% | 0.531 | 27193 | 334 |
| scrapy+md | 32% (28/88) ±10% | 36% (32/88) ±10% | 39% (34/88) ±10% | 41% (36/88) ±10% | 44% (39/88) ±10% | 0.351 | 46141 | 364 |

> **Column definitions:** **Hit@K** = correct source page in top K results. **MRR** = Mean Reciprocal Rank (1/rank of correct result, averaged). **Chunks** = total chunks produced by this tool (across all pages in common sites). **Avg words** = mean words per chunk.

## What this means

Tools span MRR 0.351-0.666 on embedding mode (a 0.315 spread). Tools crawl similar pages from the same seed URLs, and we apply identical chunking and embedding pipelines, but extraction differences -- see [content quality](QUALITY_COMPARISON.md) -- show up at retrieval time.

**Retrieval mode matters more than crawler choice.** Embedding search beats BM25 by roughly 2x on MRR across all tools. Hybrid and reranked modes fall between the two. Choosing the right retrieval strategy will improve your RAG pipeline far more than switching crawlers.

**The noise-vs-recall trade-off.** Noisier tools (crawlee, playwright) have slightly higher hit rates, but they produce 2x the chunks of leaner tools (markcrawl, scrapy+md). More chunks means higher embedding and storage costs with diminishing retrieval returns. See [COST_AT_SCALE.md](COST_AT_SCALE.md) for the dollar impact.

**For most use cases, pick your crawler based on speed and cost, not retrieval quality.** The differences here are within confidence intervals. Where crawler choice _does_ matter is content quality and downstream answer quality -- see [ANSWER_QUALITY.md](ANSWER_QUALITY.md).

## Per-category breakdown (embedding mode)

Query categories reveal where crawlers actually differ. Categories like `js-rendered` and `structured-data` stress-test browser rendering and table extraction, while `api-function` and `conceptual` queries test basic content retrieval.

| Category | Tool | Hit@10 | MRR | Queries |
|---|---|---|---|---|
| api-function | playwright | 89% (25/28) | 0.681 | 28 |
| api-function | crawlee | 89% (25/28) | 0.677 | 28 |
| api-function | colly+md | 86% (24/28) | 0.646 | 28 |
| api-function | crawl4ai | 82% (23/28) | 0.642 | 28 |
| api-function | crawl4ai-raw | 82% (23/28) | 0.639 | 28 |
| api-function | markcrawl | 50% (14/28) | 0.426 | 28 |
| api-function | scrapy+md | 46% (13/28) | 0.363 | 28 |
| code-example | colly+md | 100% (4/4) | 1.000 | 4 |
| code-example | playwright | 100% (4/4) | 1.000 | 4 |
| code-example | crawlee | 100% (4/4) | 0.875 | 4 |
| code-example | scrapy+md | 100% (4/4) | 0.812 | 4 |
| code-example | markcrawl | 100% (4/4) | 0.750 | 4 |
| code-example | crawl4ai | 100% (4/4) | 0.479 | 4 |
| code-example | crawl4ai-raw | 100% (4/4) | 0.479 | 4 |
| conceptual | crawl4ai | 100% (27/27) | 0.944 | 27 |
| conceptual | crawl4ai-raw | 100% (27/27) | 0.944 | 27 |
| conceptual | crawlee | 100% (27/27) | 0.892 | 27 |
| conceptual | playwright | 100% (27/27) | 0.843 | 27 |
| conceptual | markcrawl | 93% (25/27) | 0.772 | 27 |
| conceptual | colly+md | 74% (20/27) | 0.584 | 27 |
| conceptual | scrapy+md | 37% (10/27) | 0.282 | 27 |
| cross-page | crawl4ai | 100% (14/14) | 0.581 | 14 |
| cross-page | crawl4ai-raw | 100% (14/14) | 0.581 | 14 |
| cross-page | playwright | 86% (12/14) | 0.525 | 14 |
| cross-page | colly+md | 79% (11/14) | 0.444 | 14 |
| cross-page | crawlee | 64% (9/14) | 0.506 | 14 |
| cross-page | markcrawl | 57% (8/14) | 0.457 | 14 |
| cross-page | scrapy+md | 29% (4/14) | 0.162 | 14 |
| factual-lookup | markcrawl | 50% (5/10) | 0.406 | 10 |
| factual-lookup | scrapy+md | 40% (4/10) | 0.400 | 10 |
| factual-lookup | crawlee | 20% (2/10) | 0.200 | 10 |
| factual-lookup | colly+md | 20% (2/10) | 0.200 | 10 |
| factual-lookup | playwright | 10% (1/10) | 0.020 | 10 |
| factual-lookup | crawl4ai | 0% (0/10) | 0.000 | 10 |
| factual-lookup | crawl4ai-raw | 0% (0/10) | 0.000 | 10 |
| js-rendered | scrapy+md | 100% (5/5) | 0.720 | 5 |
| js-rendered | crawl4ai | 80% (4/5) | 0.442 | 5 |
| js-rendered | crawl4ai-raw | 80% (4/5) | 0.442 | 5 |
| js-rendered | crawlee | 60% (3/5) | 0.600 | 5 |
| js-rendered | playwright | 60% (3/5) | 0.600 | 5 |
| js-rendered | colly+md | 60% (3/5) | 0.422 | 5 |
| js-rendered | markcrawl | 20% (1/5) | 0.100 | 5 |


### Best tool per category

| Category | Best tool | Hit@10 | Spread |
|---|---|---|---|
| api-function | crawlee | 89% | 43% |
| code-example | markcrawl | 100% | 0% |
| conceptual | crawl4ai | 100% | 63% |
| cross-page | crawl4ai | 100% | 71% |
| factual-lookup | markcrawl | 50% | 50% |
| js-rendered | scrapy+md | 100% | 80% |

_Spread = difference between best and worst tool. High spread categories are where crawler choice matters most._


## react-dev

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| scrapy+md | 81% (13/16) | 94% (15/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.884 | 1259 | 216 |
| crawl4ai | 75% (12/16) | 81% (13/16) | 88% (14/16) | 94% (15/16) | 94% (15/16) | 0.810 | 3210 | 500 |
| crawl4ai-raw | 75% (12/16) | 81% (13/16) | 88% (14/16) | 94% (15/16) | 94% (15/16) | 0.810 | 3210 | 500 |
| crawlee | 62% (10/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.766 | 3063 | 217 |
| playwright | 62% (10/16) | 88% (14/16) | 88% (14/16) | 100% (16/16) | 100% (16/16) | 0.750 | 3067 | 221 |
| colly+md | 62% (10/16) | 81% (13/16) | 94% (15/16) | 94% (15/16) | 100% (16/16) | 0.741 | 5083 | 292 |
| markcrawl | 44% (7/16) | 56% (9/16) | 56% (9/16) | 56% (9/16) | 56% (9/16) | 0.500 | 419 | 51 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for react-dev</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do I manage state in a React component?** [conceptual]
*(expects URL containing: `state`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/managing-state | 0.792 | react.dev/learn/state-a-components-memory | 0.791 | react.dev/learn/sharing-state-between-components | 0.786 |
| crawl4ai | #1 | react.dev/reference/react/useState | 0.797 | react.dev/learn/managing-state | 0.792 | de.react.dev/learn/managing-state | 0.791 |
| crawl4ai-raw | #1 | react.dev/reference/react/useState | 0.797 | react.dev/learn/managing-state | 0.792 | de.react.dev/learn/managing-state | 0.791 |
| scrapy+md | #1 | react.dev/learn/managing-state | 0.792 | react.dev/learn/state-a-components-memory | 0.791 | react.dev/learn/state-a-components-memory | 0.782 |
| crawlee | #1 | react.dev/reference/react/useState | 0.807 | react.dev/learn/state-a-components-memory | 0.791 | react.dev/learn/reacting-to-input-with-state | 0.784 |
| colly+md | #1 | react.dev/reference/react/useState#setstate | 0.807 | react.dev/reference/react/useState#updating-state- | 0.807 | react.dev/reference/react/useState#storing-informa | 0.807 |
| playwright | #1 | react.dev/reference/react/useState | 0.807 | react.dev/learn/state-a-components-memory | 0.791 | react.dev/learn/state-a-components-memory | 0.782 |


**Q2: How does the useEffect hook work in React?** [api-function]
*(expects URL containing: `useEffect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/state-a-components-memory | 0.791 | react.dev/learn/reusing-logic-with-custom-hooks | 0.784 | react.dev/learn/reusing-logic-with-custom-hooks | 0.782 |
| crawl4ai | #1 | react.dev/reference/react/useEffectEvent | 0.798 | react.dev/learn/reusing-logic-with-custom-hooks | 0.796 | react.dev/learn/state-a-components-memory | 0.793 |
| crawl4ai-raw | #1 | react.dev/reference/react/useEffectEvent | 0.798 | react.dev/learn/reusing-logic-with-custom-hooks | 0.796 | react.dev/learn/state-a-components-memory | 0.793 |
| scrapy+md | #1 | react.dev/reference/react/useEffect | 0.827 | react.dev/reference/react/useEffectEvent | 0.792 | react.dev/learn/state-a-components-memory | 0.791 |
| crawlee | #4 | react.dev/learn/state-a-components-memory | 0.791 | react.dev/learn/reusing-logic-with-custom-hooks | 0.788 | react.dev/learn/state-a-components-memory | 0.787 |
| colly+md | #5 | react.dev/learn/state-a-components-memory#anatomy- | 0.791 | react.dev/learn/state-a-components-memory | 0.791 | react.dev/learn/state-a-components-memory#anatomy- | 0.787 |
| playwright | #3 | react.dev/learn/state-a-components-memory | 0.791 | react.dev/learn/state-a-components-memory | 0.787 | react.dev/reference/react/useEffect | 0.786 |


**Q3: How do I create and use context in React?** [api-function]
*(expects URL containing: `useContext`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/passing-data-deeply-with-context | 0.820 | react.dev/learn/passing-data-deeply-with-context | 0.793 | react.dev/learn/passing-data-deeply-with-context | 0.792 |
| crawl4ai | #1 | react.dev/reference/react/createContext | 0.826 | react.dev/learn/passing-data-deeply-with-context | 0.822 | react.dev/learn/passing-data-deeply-with-context | 0.814 |
| crawl4ai-raw | #1 | react.dev/reference/react/createContext | 0.826 | react.dev/learn/passing-data-deeply-with-context | 0.822 | react.dev/learn/passing-data-deeply-with-context | 0.814 |
| scrapy+md | #1 | react.dev/reference/react/createContext | 0.826 | react.dev/reference/react/createContext | 0.820 | react.dev/learn/passing-data-deeply-with-context | 0.820 |
| crawlee | #1 | react.dev/reference/react/createContext | 0.827 | react.dev/learn/passing-data-deeply-with-context | 0.820 | react.dev/reference/react/useContext | 0.814 |
| colly+md | #1 | react.dev/reference/react/createContext | 0.827 | react.dev/learn/passing-data-deeply-with-context#s | 0.820 | react.dev/learn/passing-data-deeply-with-context | 0.820 |
| playwright | #1 | react.dev/reference/react/createContext | 0.827 | react.dev/learn/passing-data-deeply-with-context | 0.820 | react.dev/reference/react/useContext | 0.814 |


**Q4: What is JSX and how does React use it?** [conceptual]
*(expects URL containing: `writing-markup-with-jsx`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/writing-markup-with-jsx | 0.837 | react.dev/learn/state-as-a-snapshot | 0.789 | react.dev/learn/describing-the-ui | 0.785 |
| crawl4ai | #1 | react.dev/learn/writing-markup-with-jsx | 0.821 | vi.react.dev/ | 0.804 | ar.react.dev/ | 0.804 |
| crawl4ai-raw | #1 | react.dev/learn/writing-markup-with-jsx | 0.821 | vi.react.dev/ | 0.804 | ar.react.dev/ | 0.804 |
| scrapy+md | #1 | react.dev/learn/writing-markup-with-jsx | 0.828 | legacy.reactjs.org/blog/2020/09/22/introducing-the | 0.809 | react.dev/ | 0.808 |
| crawlee | #1 | react.dev/learn/writing-markup-with-jsx | 0.838 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.816 | react.dev/ | 0.808 |
| colly+md | #1 | react.dev/learn/writing-markup-with-jsx | 0.838 | react.dev/ | 0.808 | react.dev/learn/lifecycle-of-reactive-effects#what | 0.807 |
| playwright | #1 | react.dev/learn/writing-markup-with-jsx | 0.838 | react.dev/link/new-jsx-transform | 0.809 | react.dev/ | 0.808 |


**Q5: How do I render lists and use keys in React?** [code-example]
*(expects URL containing: `rendering-lists`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | react.dev/learn | 0.812 | react.dev/learn/rendering-lists | 0.811 | react.dev/learn/rendering-lists | 0.798 |
| crawl4ai | #6 | react.dev/learn | 0.822 | 18.react.dev/learn | 0.820 | az.react.dev/learn | 0.819 |
| crawl4ai-raw | #6 | react.dev/learn | 0.822 | 18.react.dev/learn | 0.820 | az.react.dev/learn | 0.819 |
| scrapy+md | #1 | react.dev/learn/rendering-lists | 0.819 | react.dev/learn | 0.812 | react.dev/learn | 0.812 |
| crawlee | #1 | react.dev/learn/rendering-lists | 0.823 | react.dev/learn/rendering-lists | 0.776 | react.dev/reference/react/cloneElement | 0.769 |
| colly+md | #1 | react.dev/learn/rendering-lists#keeping-list-items | 0.823 | react.dev/learn/rendering-lists | 0.823 | react.dev/learn/describing-the-ui | 0.800 |
| playwright | #1 | react.dev/learn/rendering-lists | 0.823 | react.dev/learn/describing-the-ui | 0.800 | react.dev/learn/rendering-lists | 0.776 |


**Q6: How do I use the useRef hook in React?** [api-function]
*(expects URL containing: `useRef`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/referencing-values-with-refs | 0.771 | react.dev/learn/manipulating-the-dom-with-refs | 0.766 | react.dev/learn/manipulating-the-dom-with-refs | 0.760 |
| crawl4ai | #1 | react.dev/reference/react/useRef | 0.799 | react.dev/learn/referencing-values-with-refs | 0.769 | react.dev/reference/react/hooks | 0.768 |
| crawl4ai-raw | #1 | react.dev/reference/react/useRef | 0.799 | react.dev/learn/referencing-values-with-refs | 0.769 | react.dev/reference/react/hooks | 0.768 |
| scrapy+md | #1 | react.dev/reference/react/useRef | 0.815 | react.dev/learn/referencing-values-with-refs | 0.783 | react.dev/learn/manipulating-the-dom-with-refs | 0.752 |
| crawlee | #1 | react.dev/reference/react/useRef | 0.813 | react.dev/learn/referencing-values-with-refs | 0.783 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.775 |
| colly+md | #1 | react.dev/reference/react/useRef | 0.813 | react.dev/reference/react/useRef#returns | 0.813 | react.dev/reference/react/useRef#reference | 0.813 |
| playwright | #1 | react.dev/reference/react/useRef | 0.813 | react.dev/learn/referencing-values-with-refs | 0.783 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.775 |


**Q7: How do I pass props between React components?** [conceptual]
*(expects URL containing: `passing-props`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/passing-props-to-a-component | 0.817 | react.dev/learn/passing-props-to-a-component | 0.771 | react.dev/learn/sharing-state-between-components | 0.767 |
| crawl4ai | #1 | react.dev/learn/passing-props-to-a-component | 0.806 | react.dev/learn/passing-props-to-a-component | 0.791 | react.dev/learn | 0.787 |
| crawl4ai-raw | #1 | react.dev/learn/passing-props-to-a-component | 0.806 | react.dev/learn/passing-props-to-a-component | 0.791 | react.dev/learn | 0.787 |
| scrapy+md | #1 | react.dev/learn/passing-props-to-a-component | 0.822 | react.dev/learn/thinking-in-react | 0.767 | react.dev/learn/state-a-components-memory | 0.760 |
| crawlee | #1 | react.dev/learn/passing-props-to-a-component | 0.799 | react.dev/learn/sharing-state-between-components | 0.774 | react.dev/learn/passing-props-to-a-component | 0.771 |
| colly+md | #1 | react.dev/learn/passing-props-to-a-component#passi | 0.819 | react.dev/learn/passing-props-to-a-component | 0.819 | react.dev/learn/sharing-state-between-components | 0.774 |
| playwright | #1 | react.dev/learn/passing-props-to-a-component | 0.819 | react.dev/learn/sharing-state-between-components | 0.774 | react.dev/learn/thinking-in-react | 0.767 |


**Q8: How do I conditionally render content in React?** [code-example]
*(expects URL containing: `conditional-rendering`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/conditional-rendering | 0.799 | react.dev/learn/describing-the-ui | 0.797 | react.dev/learn | 0.783 |
| crawl4ai | #4 | react.dev/learn | 0.811 | az.react.dev/learn | 0.807 | 18.react.dev/learn | 0.805 |
| crawl4ai-raw | #4 | react.dev/learn | 0.811 | az.react.dev/learn | 0.807 | 18.react.dev/learn | 0.805 |
| scrapy+md | #1 | react.dev/learn/conditional-rendering | 0.804 | react.dev/learn/describing-the-ui | 0.797 | react.dev/learn | 0.783 |
| crawlee | #2 | react.dev/learn/describing-the-ui | 0.796 | react.dev/learn/conditional-rendering | 0.779 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.774 |
| colly+md | #1 | react.dev/learn/conditional-rendering | 0.795 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.774 | react.dev/learn/conditional-rendering | 0.764 |
| playwright | #1 | react.dev/learn/conditional-rendering | 0.795 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.774 | react.dev/learn/conditional-rendering | 0.764 |


**Q9: What is the useMemo hook for in React?** [api-function]
*(expects URL containing: `useMemo`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/typescript | 0.802 | react.dev/learn/reusing-logic-with-custom-hooks | 0.768 | react.dev/learn/reusing-logic-with-custom-hooks | 0.747 |
| crawl4ai | #1 | react.dev/reference/react/useMemo | 0.826 | react.dev/reference/react/useMemo | 0.823 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.814 |
| crawl4ai-raw | #1 | react.dev/reference/react/useMemo | 0.826 | react.dev/reference/react/useMemo | 0.823 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.814 |
| scrapy+md | #1 | react.dev/reference/react/useMemo | 0.857 | react.dev/reference/react/useMemo | 0.826 | react.dev/reference/react/useCallback | 0.802 |
| crawlee | #1 | react.dev/reference/react/useMemo | 0.841 | react.dev/reference/react/useMemo | 0.836 | react.dev/reference/react/useMemo | 0.820 |
| colly+md | #1 | react.dev/reference/react/useMemo#how-to-tell-if-a | 0.841 | react.dev/reference/react/useMemo | 0.841 | react.dev/reference/react/useMemo#how-to-tell-if-a | 0.836 |
| playwright | #1 | react.dev/reference/react/useMemo | 0.841 | react.dev/reference/react/useMemo | 0.836 | react.dev/reference/react/useMemo | 0.820 |


**Q10: How do I use the useState hook in React?** [api-function]
*(expects URL containing: `useState`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn | 0.820 | react.dev/learn/state-a-components-memory | 0.807 | react.dev/learn/state-a-components-memory | 0.805 |
| crawl4ai | #21 | he.react.dev/learn | 0.823 | react.dev/learn | 0.819 | az.react.dev/learn | 0.816 |
| crawl4ai-raw | #21 | he.react.dev/learn | 0.823 | react.dev/learn | 0.819 | az.react.dev/learn | 0.816 |
| scrapy+md | #7 | react.dev/learn | 0.820 | react.dev/learn | 0.820 | react.dev/learn/state-a-components-memory | 0.807 |
| crawlee | #6 | react.dev/learn | 0.820 | react.dev/learn/state-a-components-memory | 0.807 | react.dev/learn | 0.805 |
| colly+md | #3 | react.dev/learn | 0.820 | react.dev/learn#components | 0.820 | react.dev/learn/state-a-components-memory#anatomy- | 0.807 |
| playwright | #6 | react.dev/learn | 0.820 | react.dev/learn/state-a-components-memory | 0.807 | react.dev/learn | 0.805 |


**Q11: How do I use the useCallback hook in React?** [api-function]
*(expects URL containing: `useCallback`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn | 0.781 | react.dev/learn/reusing-logic-with-custom-hooks | 0.776 | react.dev/learn/state-a-components-memory | 0.768 |
| crawl4ai | #1 | react.dev/reference/react/useCallback | 0.817 | react.dev/reference/react/useCallback | 0.810 | react.dev/reference/react/useCallback | 0.801 |
| crawl4ai-raw | #1 | react.dev/reference/react/useCallback | 0.817 | react.dev/reference/react/useCallback | 0.810 | react.dev/reference/react/useCallback | 0.801 |
| scrapy+md | #1 | react.dev/reference/react/useCallback | 0.833 | react.dev/reference/react/useMemo | 0.789 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.783 |
| crawlee | #1 | react.dev/reference/react/useCallback | 0.818 | react.dev/reference/react/useCallback | 0.812 | react.dev/reference/react/useCallback | 0.803 |
| colly+md | #1 | react.dev/reference/react/useCallback | 0.818 | react.dev/reference/react/useCallback | 0.812 | react.dev/reference/react/useCallback | 0.803 |
| playwright | #1 | react.dev/reference/react/useCallback | 0.818 | react.dev/reference/react/useCallback | 0.812 | react.dev/reference/react/useCallback | 0.803 |


**Q12: How do I use the useReducer hook in React?** [api-function]
*(expects URL containing: `useReducer`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/extracting-state-logic-into-a-redu | 0.851 | react.dev/learn/typescript | 0.792 | react.dev/learn/extracting-state-logic-into-a-redu | 0.772 |
| crawl4ai | #2 | react.dev/learn/extracting-state-logic-into-a-redu | 0.842 | react.dev/reference/react/useReducer | 0.812 | react.dev/reference/react/useReducer | 0.806 |
| crawl4ai-raw | #2 | react.dev/learn/extracting-state-logic-into-a-redu | 0.842 | react.dev/reference/react/useReducer | 0.812 | react.dev/reference/react/useReducer | 0.806 |
| scrapy+md | #2 | react.dev/learn/extracting-state-logic-into-a-redu | 0.848 | react.dev/reference/react/useReducer | 0.828 | react.dev/learn/typescript | 0.792 |
| crawlee | #2 | react.dev/learn/extracting-state-logic-into-a-redu | 0.848 | react.dev/reference/react/useReducer | 0.819 | react.dev/reference/react/useReducer | 0.794 |
| colly+md | #2 | react.dev/learn/extracting-state-logic-into-a-redu | 0.848 | react.dev/reference/react/useReducer | 0.819 | react.dev/reference/react/useReducer | 0.794 |
| playwright | #2 | react.dev/learn/extracting-state-logic-into-a-redu | 0.848 | react.dev/reference/react/useReducer | 0.819 | react.dev/reference/react/useReducer | 0.794 |


**Q13: How do I handle events like clicks in React?** [code-example]
*(expects URL containing: `responding-to-events`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/responding-to-events | 0.821 | react.dev/learn/responding-to-events | 0.812 | react.dev/learn/adding-interactivity | 0.804 |
| crawl4ai | #1 | react.dev/learn/responding-to-events | 0.827 | he.react.dev/learn | 0.812 | react.dev/learn/responding-to-events | 0.811 |
| crawl4ai-raw | #1 | react.dev/learn/responding-to-events | 0.827 | he.react.dev/learn | 0.812 | react.dev/learn/responding-to-events | 0.811 |
| scrapy+md | #1 | react.dev/learn/responding-to-events | 0.824 | react.dev/learn/responding-to-events | 0.812 | react.dev/learn/adding-interactivity | 0.806 |
| crawlee | #1 | react.dev/learn/responding-to-events | 0.811 | react.dev/learn | 0.800 | react.dev/learn/adding-interactivity | 0.799 |
| colly+md | #1 | react.dev/learn/responding-to-events#passing-event | 0.816 | react.dev/learn/responding-to-events | 0.816 | react.dev/learn/responding-to-events | 0.812 |
| playwright | #1 | react.dev/learn/responding-to-events | 0.816 | react.dev/learn/responding-to-events | 0.812 | react.dev/learn | 0.800 |


**Q14: What is the Suspense component in React?** [api-function]
*(expects URL containing: `Suspense`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/conditional-rendering | 0.684 | react.dev/learn/lifecycle-of-reactive-effects | 0.668 | react.dev/learn/lifecycle-of-reactive-effects | 0.668 |
| crawl4ai | #1 | react.dev/reference/react/Suspense | 0.836 | react.dev/blog/2022/03/29/react-v18 | 0.817 | react.dev/reference/react/Suspense | 0.803 |
| crawl4ai-raw | #1 | react.dev/reference/react/Suspense | 0.836 | react.dev/blog/2022/03/29/react-v18 | 0.817 | react.dev/reference/react/Suspense | 0.803 |
| scrapy+md | #1 | react.dev/reference/react/Suspense | 0.812 | react.dev/blog/2022/03/29/react-v18 | 0.805 | react.dev/reference/react/Suspense | 0.804 |
| crawlee | #2 | react.dev/blog/2022/03/29/react-v18 | 0.805 | react.dev/reference/react/Suspense | 0.803 | react.dev/reference/react/Activity | 0.795 |
| colly+md | #2 | react.dev/blog/2022/03/29/react-v18 | 0.805 | react.dev/blog/2022/03/29/react-v18#suspense-in-da | 0.805 | react.dev/reference/react/Suspense | 0.803 |
| playwright | #2 | react.dev/blog/2022/03/29/react-v18 | 0.805 | react.dev/reference/react/Suspense | 0.803 | react.dev/reference/react/Activity | 0.795 |


**Q15: How do I add interactivity to React components?** [conceptual]
*(expects URL containing: `adding-interactivity`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/adding-interactivity | 0.792 | react.dev/learn/your-first-component | 0.781 | react.dev/learn/tutorial-tic-tac-toe | 0.764 |
| crawl4ai | #1 | react.dev/learn/adding-interactivity | 0.816 | de.react.dev/learn/adding-interactivity | 0.812 | 18.react.dev/learn/adding-interactivity | 0.803 |
| crawl4ai-raw | #1 | react.dev/learn/adding-interactivity | 0.816 | de.react.dev/learn/adding-interactivity | 0.812 | 18.react.dev/learn/adding-interactivity | 0.803 |
| scrapy+md | #1 | react.dev/learn/adding-interactivity | 0.806 | react.dev/learn/state-a-components-memory | 0.781 | react.dev/learn/your-first-component | 0.781 |
| crawlee | #1 | react.dev/learn/adding-interactivity | 0.795 | react.dev/learn/your-first-component | 0.787 | react.dev/learn/state-a-components-memory | 0.781 |
| colly+md | #13 | react.dev/learn/your-first-component#components-ui | 0.787 | react.dev/learn/your-first-component#nesting-and-o | 0.787 | react.dev/learn/your-first-component | 0.787 |
| playwright | #6 | react.dev/learn/your-first-component | 0.787 | react.dev/learn/your-first-component | 0.781 | react.dev/learn/responding-to-events | 0.777 |


**Q16: How do I install and set up a new React project?** [conceptual]
*(expects URL containing: `installation`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | react.dev/learn/add-react-to-an-existing-project | 0.780 | react.dev/learn/installation | 0.776 | react.dev/learn/setup | 0.761 |
| crawl4ai | #1 | 18.react.dev/learn/installation | 0.813 | he.react.dev/learn/installation | 0.812 | az.react.dev/learn/installation | 0.809 |
| crawl4ai-raw | #1 | 18.react.dev/learn/installation | 0.813 | he.react.dev/learn/installation | 0.812 | az.react.dev/learn/installation | 0.809 |
| scrapy+md | #2 | react.dev/learn/add-react-to-an-existing-project | 0.794 | react.dev/learn/installation | 0.778 | react.dev/learn/add-react-to-an-existing-project | 0.778 |
| crawlee | #3 | react.dev/learn/add-react-to-an-existing-project | 0.778 | react.dev/reference/react-compiler/compiling-libra | 0.771 | react.dev/learn/react-compiler/installation | 0.768 |
| colly+md | #4 | react.dev/learn/add-react-to-an-existing-project | 0.778 | react.dev/learn/add-react-to-an-existing-project#u | 0.778 | react.dev/reference/react-compiler/compiling-libra | 0.771 |
| playwright | #3 | react.dev/learn/add-react-to-an-existing-project | 0.778 | react.dev/reference/react-compiler/compiling-libra | 0.771 | react.dev/learn/react-compiler/installation | 0.768 |


</details>

## stripe-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawlee | 61% (11/18) | 67% (12/18) | 72% (13/18) | 78% (14/18) | 78% (14/18) | 0.653 | 30214 | 500 |
| playwright | 61% (11/18) | 67% (12/18) | 72% (13/18) | 78% (14/18) | 78% (14/18) | 0.651 | 30229 | 500 |
| colly+md | 50% (9/18) | 61% (11/18) | 67% (12/18) | 72% (13/18) | 72% (13/18) | 0.569 | 31125 | 499 |
| scrapy+md | 39% (7/18) | 50% (9/18) | 56% (10/18) | 61% (11/18) | 61% (11/18) | 0.465 | 14882 | 500 |
| crawl4ai | 33% (6/18) | 56% (10/18) | 56% (10/18) | 61% (11/18) | 67% (12/18) | 0.461 | 2651 | 500 |
| crawl4ai-raw | 33% (6/18) | 56% (10/18) | 56% (10/18) | 61% (11/18) | 61% (11/18) | 0.457 | 3564 | 499 |
| markcrawl | 17% (3/18) | 39% (7/18) | 39% (7/18) | 39% (7/18) | 39% (7/18) | 0.269 | 1904 | 489 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for stripe-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do I create a payment intent with Stripe?** [api-function]
*(expects URL containing: `payment-intent`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/payment-intents | 0.842 | docs.stripe.com/payments/accept-a-payment-deferred | 0.815 | docs.stripe.com/payments/ach-direct-debit/migratin | 0.814 |
| crawl4ai | #12 | docs.stripe.com/payments-api/tour | 0.803 | docs.stripe.com/api/payment_intents | 0.796 | docs.stripe.com/api/payment_intents | 0.791 |
| crawl4ai-raw | #42 | docs.stripe.com/js/elements_object/create_payment_ | 0.810 | docs.stripe.com/js/elements_object/create_payment_ | 0.809 | docs.stripe.com/js/element/other_element | 0.804 |
| scrapy+md | miss | docs.stripe.com/payments-api/tour | 0.814 | docs.stripe.com/js/appendix/supported_browsers | 0.807 | docs.stripe.com/js/payment_methods/create_payment_ | 0.807 |
| crawlee | #3 | docs.stripe.com/api/payment_intents | 0.897 | docs.stripe.com/api/payment_intents/create | 0.878 | docs.stripe.com/payments/payment-intents | 0.864 |
| colly+md | #3 | docs.stripe.com/api/payment/intents | 0.897 | docs.stripe.com/api/payment/intents/create | 0.878 | docs.stripe.com/payments/payment-intents | 0.864 |
| playwright | #3 | docs.stripe.com/api/payment_intents | 0.897 | docs.stripe.com/api/payment_intents/create | 0.878 | docs.stripe.com/payments/payment-intents | 0.864 |


**Q2: How do I handle webhooks from Stripe?** [api-function]
*(expects URL containing: `webhook`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/managed-payments/set-up-m | 0.761 | docs.stripe.com/payments/payment-intents/verifying | 0.759 | docs.stripe.com/payments/checkout/custom-success-p | 0.741 |
| crawl4ai | #1 | docs.stripe.com/webhooks | 0.803 | docs.stripe.com/webhooks | 0.789 | docs.stripe.com/payments/advanced/build-subscripti | 0.784 |
| crawl4ai-raw | #1 | docs.stripe.com/webhooks | 0.803 | docs.stripe.com/webhooks | 0.789 | docs.stripe.com/payments/advanced/build-subscripti | 0.784 |
| scrapy+md | #2 | docs.stripe.com/billing/subscriptions/build-subscr | 0.785 | docs.stripe.com/webhooks/handling-payment-events | 0.775 | docs.stripe.com/cli | 0.762 |
| crawlee | #1 | docs.stripe.com/billing/subscriptions/webhooks | 0.872 | docs.stripe.com/webhooks/quickstart | 0.871 | docs.stripe.com/webhooks/handling-payment-events | 0.870 |
| colly+md | #1 | docs.stripe.com/webhooks/quickstart | 0.871 | docs.stripe.com/webhooks/handling-payment-events | 0.870 | docs.stripe.com/webhooks#verify-events | 0.825 |
| playwright | #1 | docs.stripe.com/billing/subscriptions/webhooks | 0.872 | docs.stripe.com/webhooks/quickstart | 0.871 | docs.stripe.com/webhooks/handling-payment-events | 0.870 |


**Q3: How do I set up Stripe subscriptions?** [api-function]
*(expects URL containing: `subscription`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/subscriptions | 0.807 | docs.stripe.com/payments/advanced/build-subscripti | 0.793 | docs.stripe.com/payments/checkout/build-subscripti | 0.784 |
| crawl4ai | #2 | docs.stripe.com/billing/quickstart | 0.798 | docs.stripe.com/payments/advanced/build-subscripti | 0.795 | docs.stripe.com/billing/subscriptions/design-an-in | 0.785 |
| crawl4ai-raw | #2 | docs.stripe.com/billing/quickstart | 0.798 | docs.stripe.com/payments/advanced/build-subscripti | 0.795 | docs.stripe.com/billing/subscriptions/design-an-in | 0.785 |
| scrapy+md | #1 | docs.stripe.com/billing/subscriptions/import-subsc | 0.798 | docs.stripe.com/billing/subscriptions/build-subscr | 0.793 | docs.stripe.com/billing/subscriptions/build-subscr | 0.790 |
| crawlee | #1 | docs.stripe.com/connect/subscriptions | 0.870 | docs.stripe.com/billing/subscriptions/overview | 0.862 | docs.stripe.com/billing/subscriptions/creating | 0.862 |
| colly+md | #1 | docs.stripe.com/connect/subscriptions | 0.870 | docs.stripe.com/billing/subscriptions/overview | 0.862 | docs.stripe.com/payments/subscriptions | 0.860 |
| playwright | #1 | docs.stripe.com/connect/subscriptions | 0.870 | docs.stripe.com/billing/subscriptions/overview | 0.862 | docs.stripe.com/billing/subscriptions/creating | 0.862 |


**Q4: How do I authenticate with the Stripe API?** [api-function]
*(expects URL containing: `authentication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | docs.stripe.com/payments/setup-intents | 0.746 | docs.stripe.com/payments/cash-app-pay/accept-a-pay | 0.729 | docs.stripe.com/payments/without-card-authenticati | 0.725 |
| crawl4ai | miss | docs.stripe.com/api | 0.796 | docs.stripe.com/payments/link/save-and-reuse | 0.757 | docs.stripe.com/file-upload | 0.757 |
| crawl4ai-raw | miss | docs.stripe.com/api | 0.796 | docs.stripe.com/payments/link/save-and-reuse | 0.757 | docs.stripe.com/file-upload | 0.757 |
| scrapy+md | miss | docs.stripe.com/building-extensions | 0.799 | docs.stripe.com/building-extensions | 0.771 | docs.stripe.com/api/tokens/create_cvc_update | 0.770 |
| crawlee | #6 | docs.stripe.com/api/v2/core/accounts/create#v2_cre | 0.821 | docs.stripe.com/keys | 0.813 | docs.stripe.com/connect/accounts-v2 | 0.796 |
| colly+md | #23 | docs.stripe.com/keys | 0.813 | docs.stripe.com/keys#test-live-modes | 0.813 | docs.stripe.com/api#retrieve/payment/intent | 0.809 |
| playwright | #7 | docs.stripe.com/api/v2/core/accounts/create | 0.821 | docs.stripe.com/keys | 0.813 | docs.stripe.com/api | 0.809 |


**Q5: How do I handle errors in the Stripe API?** [api-function]
*(expects URL containing: `error-handling`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/finalize-payments-on-the- | 0.777 | docs.stripe.com/payments/accept-a-payment-deferred | 0.776 | docs.stripe.com/payments/payment-intents/upgrade-t | 0.771 |
| crawl4ai | miss | docs.stripe.com/api | 0.786 | docs.stripe.com/api | 0.766 | docs.stripe.com/connect/saas/quickstart | 0.748 |
| crawl4ai-raw | miss | docs.stripe.com/api | 0.786 | docs.stripe.com/api | 0.766 | docs.stripe.com/connect/saas/quickstart | 0.748 |
| scrapy+md | miss | docs.stripe.com/error-low-level | 0.825 | docs.stripe.com/error-low-level | 0.778 | docs.stripe.com/payments/finalize-payments-on-the- | 0.773 |
| crawlee | miss | docs.stripe.com/api#charge_object-receipt_number | 0.807 | docs.stripe.com/api#charge_object-receipt_number | 0.806 | docs.stripe.com/connect/get-started-connect-embedd | 0.797 |
| colly+md | miss | docs.stripe.com/disputes/api | 0.832 | docs.stripe.com/api#refund/object | 0.810 | docs.stripe.com/api#update/payment/intent | 0.810 |
| playwright | miss | docs.stripe.com/api | 0.807 | docs.stripe.com/api | 0.807 | docs.stripe.com/api | 0.801 |


**Q6: How do I process refunds with Stripe?** [api-function]
*(expects URL containing: `refund`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/customer-balance/refundin | 0.845 | docs.stripe.com/payments/affirm | 0.825 | docs.stripe.com/payments/konbini/accept-a-payment | 0.818 |
| crawl4ai | #1 | docs.stripe.com/refunds | 0.853 | docs.stripe.com/payments/affirm | 0.825 | docs.stripe.com/payment-links/post-payment | 0.821 |
| crawl4ai-raw | #1 | docs.stripe.com/refunds | 0.853 | docs.stripe.com/payments/affirm | 0.825 | docs.stripe.com/payment-links/post-payment | 0.821 |
| scrapy+md | #1 | docs.stripe.com/refunds?dashboard-or-api=dashboard | 0.857 | docs.stripe.com/refunds?dashboard-or-api=api | 0.830 | docs.stripe.com/invoicing/automatic-reconciliation | 0.806 |
| crawlee | #1 | docs.stripe.com/api/refunds | 0.883 | docs.stripe.com/refunds | 0.863 | docs.stripe.com/refunds | 0.857 |
| colly+md | #1 | docs.stripe.com/api/refunds | 0.883 | docs.stripe.com/refunds#cancel-payment | 0.863 | docs.stripe.com/refunds | 0.863 |
| playwright | #1 | docs.stripe.com/api/refunds | 0.883 | docs.stripe.com/refunds | 0.863 | docs.stripe.com/refunds | 0.857 |


**Q7: How do I use Stripe checkout for payments?** [js-rendered]
*(expects URL containing: `checkout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.stripe.com/payments/accept-a-payment | 0.832 | docs.stripe.com/payments/accept-a-payment?api-inte | 0.829 | docs.stripe.com/payments/accept-a-payment?payment- | 0.829 |
| crawl4ai | #6 | docs.stripe.com/upgrades/manage-payment-methods | 0.827 | docs.stripe.com/payments/advanced | 0.821 | docs.stripe.com/get-started/use-cases/saas-subscri | 0.821 |
| crawl4ai-raw | #6 | docs.stripe.com/upgrades/manage-payment-methods | 0.827 | docs.stripe.com/payments/advanced | 0.821 | docs.stripe.com/get-started/use-cases/saas-subscri | 0.821 |
| scrapy+md | #2 | docs.stripe.com/connect/dynamic-payment-methods | 0.812 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.809 | docs.stripe.com/llms.txt | 0.807 |
| crawlee | #1 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.850 | docs.stripe.com/payments/advanced/payment-methods/ | 0.849 | docs.stripe.com/payments/checkout/payment-methods | 0.849 |
| colly+md | #1 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.850 | docs.stripe.com/payments/payment-intents/migration | 0.830 | docs.stripe.com/upgrades/manage-payment-methods | 0.827 |
| playwright | #1 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.850 | docs.stripe.com/payments/checkout/payment-methods | 0.849 | docs.stripe.com/payments/advanced/payment-methods/ | 0.849 |


**Q8: How do I test Stripe payments in development?** [code-example]
*(expects URL containing: `testing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.stripe.com/payments/mobilepay/accept-a-paymen | 0.797 | docs.stripe.com/payments/a-b-testing | 0.780 | docs.stripe.com/payments/accept-stablecoin-payment | 0.775 |
| crawl4ai | #2 | docs.stripe.com/get-started/test-developer-integra | 0.826 | docs.stripe.com/testing | 0.811 | docs.stripe.com/testing | 0.799 |
| crawl4ai-raw | #2 | docs.stripe.com/get-started/test-developer-integra | 0.826 | docs.stripe.com/testing | 0.811 | docs.stripe.com/testing | 0.799 |
| scrapy+md | #4 | docs.stripe.com/get-started/test-developer-integra | 0.826 | docs.stripe.com/get-started/development-environmen | 0.794 | docs.stripe.com/get-started/test-developer-integra | 0.788 |
| crawlee | #1 | docs.stripe.com/payments/a-b-testing | 0.831 | docs.stripe.com/global-payouts/testing | 0.809 | docs.stripe.com/connect/marketplace/quickstart | 0.804 |
| colly+md | #1 | docs.stripe.com/payments/a-b-testing | 0.831 | docs.stripe.com/connect/marketplace/quickstart | 0.804 | docs.stripe.com/connect/build-full-embedded-integr | 0.800 |
| playwright | #1 | docs.stripe.com/payments/a-b-testing | 0.831 | docs.stripe.com/global-payouts/testing | 0.809 | docs.stripe.com/connect/marketplace/quickstart | 0.804 |


**Q9: What are Stripe Connect and platform payments?** [conceptual]
*(expects URL containing: `connect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.stripe.com/payments/pay-with-balance | 0.788 | docs.stripe.com/payments/payment-methods/payment-m | 0.754 | docs.stripe.com/payments/cash-app-pay | 0.749 |
| crawl4ai | #2 | docs.stripe.com/glossary | 0.808 | docs.stripe.com/connect/dynamic-payment-methods | 0.790 | docs.stripe.com/connect | 0.790 |
| crawl4ai-raw | #2 | docs.stripe.com/glossary | 0.808 | docs.stripe.com/connect/dynamic-payment-methods | 0.790 | docs.stripe.com/connect | 0.790 |
| scrapy+md | #1 | docs.stripe.com/connect/platform-controls-for-stri | 0.804 | docs.stripe.com/connect/dynamic-payment-methods | 0.787 | docs.stripe.com/connect/charges | 0.780 |
| crawlee | #1 | docs.stripe.com/connect | 0.844 | docs.stripe.com/payments/payment-methods/payment-m | 0.817 | docs.stripe.com/connect | 0.796 |
| colly+md | #1 | docs.stripe.com/connect | 0.844 | docs.stripe.com/connect/destination-charges | 0.795 | docs.stripe.com/connect/destination-charges#issue- | 0.795 |
| playwright | #1 | docs.stripe.com/connect | 0.844 | docs.stripe.com/payments/payment-methods/payment-m | 0.817 | docs.stripe.com/connect/destination-charges?platfo | 0.795 |


**Q10: How do I set up usage-based billing with Stripe?** [js-rendered]
*(expects URL containing: `usage-based`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/setup-intents | 0.761 | docs.stripe.com/payments/subscriptions | 0.758 | docs.stripe.com/payments/advanced/build-subscripti | 0.754 |
| crawl4ai | miss | docs.stripe.com/llms.txt | 0.798 | docs.stripe.com/billing/subscriptions/billing-cycl | 0.792 | docs.stripe.com/connect/subscriptions | 0.785 |
| crawl4ai-raw | miss | docs.stripe.com/llms.txt | 0.798 | docs.stripe.com/billing/subscriptions/billing-cycl | 0.792 | docs.stripe.com/connect/subscriptions | 0.785 |
| scrapy+md | #1 | docs.stripe.com/billing/subscriptions/usage-based- | 0.842 | docs.stripe.com/billing/subscriptions/usage-based- | 0.830 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.828 |
| crawlee | miss | docs.stripe.com/billing | 0.851 | docs.stripe.com/billing/collection-method | 0.813 | docs.stripe.com/connect/subscriptions | 0.804 |
| colly+md | miss | docs.stripe.com/billing | 0.851 | docs.stripe.com/connect/subscriptions | 0.804 | docs.stripe.com/no-code/get-started | 0.789 |
| playwright | miss | docs.stripe.com/billing | 0.851 | docs.stripe.com/billing/collection-method | 0.813 | docs.stripe.com/connect/subscriptions | 0.804 |


**Q11: How do I manage Stripe API keys?** [api-function]
*(expects URL containing: `keys`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/advanced/dynamically-upda | 0.765 | docs.stripe.com/payments/mobile/accept-payment?int | 0.752 | docs.stripe.com/payments/vault-and-forward | 0.743 |
| crawl4ai | #2 | docs.stripe.com/get-started/api-request | 0.836 | docs.stripe.com/keys | 0.825 | docs.stripe.com/keys-best-practices | 0.820 |
| crawl4ai-raw | #2 | docs.stripe.com/get-started/api-request | 0.836 | docs.stripe.com/keys | 0.825 | docs.stripe.com/keys-best-practices | 0.817 |
| scrapy+md | #35 | docs.stripe.com/get-started/api-request | 0.832 | docs.stripe.com/js/appendix/supported_browsers | 0.825 | docs.stripe.com/js/payment_request/create | 0.825 |
| crawlee | #1 | docs.stripe.com/keys | 0.916 | docs.stripe.com/keys-best-practices | 0.871 | docs.stripe.com/keys | 0.838 |
| colly+md | #2 | docs.stripe.com/sandboxes/dashboard/manage-access# | 0.920 | docs.stripe.com/keys | 0.916 | docs.stripe.com/keys#test-live-modes | 0.916 |
| playwright | #1 | docs.stripe.com/keys | 0.916 | docs.stripe.com/keys-best-practices | 0.871 | docs.stripe.com/keys | 0.838 |


**Q12: How do I handle Stripe rate limits?** [api-function]
*(expects URL containing: `rate-limits`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/cards/surcharge | 0.746 | docs.stripe.com/payments/bank-transfers/accept-a-p | 0.739 | docs.stripe.com/payments/afterpay-clearpay | 0.727 |
| crawl4ai | miss | docs.stripe.com/connect/instant-payouts | 0.744 | docs.stripe.com/payments/afterpay-clearpay | 0.727 | docs.stripe.com/payouts/minimum-balances-for-autom | 0.724 |
| crawl4ai-raw | miss | docs.stripe.com/connect/instant-payouts | 0.744 | docs.stripe.com/payments/afterpay-clearpay | 0.727 | docs.stripe.com/payouts/minimum-balances-for-autom | 0.724 |
| scrapy+md | miss | docs.stripe.com/payouts/minimum-balances-for-autom | 0.725 | docs.stripe.com/billing/subscriptions/usage-based- | 0.719 | docs.stripe.com/payments/currencies/localize-price | 0.718 |
| crawlee | miss | docs.stripe.com/testing | 0.777 | docs.stripe.com/payments/currencies/localize-price | 0.759 | docs.stripe.com/payments/cards/surcharge | 0.747 |
| colly+md | miss | docs.stripe.com/testing | 0.777 | docs.stripe.com/testing#cards | 0.777 | docs.stripe.com/payments/currencies/localize-price | 0.760 |
| playwright | miss | docs.stripe.com/testing | 0.777 | docs.stripe.com/payments/currencies/localize-price | 0.760 | docs.stripe.com/payments/cards/surcharge | 0.747 |


**Q13: How do I use metadata with Stripe objects?** [api-function]
*(expects URL containing: `metadata`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/payment-line-items/flexib | 0.697 | docs.stripe.com/payments/payment-intents | 0.692 | docs.stripe.com/payments/payment-line-items/flexib | 0.688 |
| crawl4ai | miss | docs.stripe.com/api | 0.783 | docs.stripe.com/api | 0.744 | docs.stripe.com/api/accounts/update | 0.743 |
| crawl4ai-raw | miss | docs.stripe.com/api | 0.783 | docs.stripe.com/api | 0.744 | docs.stripe.com/api/accounts/update | 0.743 |
| scrapy+md | miss | docs.stripe.com/api/errors/handling | 0.796 | docs.stripe.com/expand | 0.766 | docs.stripe.com/api/external_account_cards?api-ver | 0.760 |
| crawlee | #1 | docs.stripe.com/industry-metadata | 0.823 | docs.stripe.com/custom-objects | 0.802 | docs.stripe.com/ | 0.800 |
| colly+md | #1 | docs.stripe.com/industry-metadata | 0.822 | docs.stripe.com/changelog/dahlia/2026-03-25/adds-m | 0.814 | docs.stripe.com/custom-objects | 0.802 |
| playwright | #1 | docs.stripe.com/industry-metadata | 0.823 | docs.stripe.com/custom-objects | 0.802 | docs.stripe.com/ | 0.800 |


**Q14: How do I set up Apple Pay with Stripe?** [js-rendered]
*(expects URL containing: `apple-pay`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/accept-a-payment?payment- | 0.818 | docs.stripe.com/payments/accept-a-payment?payment- | 0.815 | docs.stripe.com/payments/mobile/save-card-without- | 0.813 |
| crawl4ai | #1 | docs.stripe.com/apple-pay | 0.847 | docs.stripe.com/elements/customer-sheet | 0.815 | docs.stripe.com/apple-pay | 0.813 |
| crawl4ai-raw | #1 | docs.stripe.com/apple-pay | 0.847 | docs.stripe.com/elements/customer-sheet | 0.815 | docs.stripe.com/apple-pay | 0.813 |
| scrapy+md | #1 | docs.stripe.com/apple-pay?platform=react-native | 0.817 | docs.stripe.com/mobile/digital-goods/checkout | 0.816 | docs.stripe.com/apple-pay?platform=react-native | 0.815 |
| crawlee | #1 | docs.stripe.com/apple-pay | 0.897 | docs.stripe.com/apple-pay | 0.864 | docs.stripe.com/apple-pay | 0.847 |
| colly+md | #1 | docs.stripe.com/apple-pay | 0.897 | docs.stripe.com/apple-pay | 0.864 | docs.stripe.com/apple-pay | 0.846 |
| playwright | #1 | docs.stripe.com/apple-pay | 0.897 | docs.stripe.com/apple-pay | 0.864 | docs.stripe.com/apple-pay | 0.847 |


**Q15: How do I issue cards with Stripe Issuing?** [api-function]
*(expects URL containing: `issuing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/mobile/save-card-without- | 0.710 | docs.stripe.com/payments/orchestration/rules | 0.709 | docs.stripe.com/payments/use-cases/get-started | 0.708 |
| crawl4ai | #1 | docs.stripe.com/issuing | 0.814 | docs.stripe.com/llms.txt | 0.782 | docs.stripe.com/get-started/use-cases/in-person-pa | 0.753 |
| crawl4ai-raw | #1 | docs.stripe.com/issuing | 0.814 | docs.stripe.com/llms.txt | 0.782 | docs.stripe.com/get-started/use-cases/in-person-pa | 0.753 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.773 | docs.stripe.com/llms.txt | 0.745 | docs.stripe.com/get-started/data-migrations/pan-im | 0.738 |
| crawlee | #1 | docs.stripe.com/issuing | 0.855 | docs.stripe.com/issuing | 0.814 | docs.stripe.com/issuing/connect | 0.810 |
| colly+md | #1 | docs.stripe.com/issuing | 0.855 | docs.stripe.com/issuing | 0.814 | docs.stripe.com/issuing/for-your-business | 0.806 |
| playwright | #1 | docs.stripe.com/issuing | 0.855 | docs.stripe.com/issuing | 0.814 | docs.stripe.com/issuing/connect | 0.810 |


**Q16: How do I recover failed subscription payments?** [js-rendered]
*(expects URL containing: `revenue-recovery`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/pay-with-balance | 0.752 | docs.stripe.com/payments/checkout/build-subscripti | 0.748 | docs.stripe.com/payments/pay-with-balance | 0.727 |
| crawl4ai | #23 | docs.stripe.com/api/subscriptions | 0.756 | docs.stripe.com/billing/subscriptions/webhooks | 0.755 | docs.stripe.com/billing/collection-method | 0.754 |
| crawl4ai-raw | #23 | docs.stripe.com/api/subscriptions | 0.756 | docs.stripe.com/billing/subscriptions/webhooks | 0.755 | docs.stripe.com/billing/collection-method | 0.754 |
| scrapy+md | #10 | docs.stripe.com/connect/saas/tasks/service-fee | 0.752 | docs.stripe.com/billing/subscriptions/build-subscr | 0.748 | docs.stripe.com/payments/checkout/build-subscripti | 0.748 |
| crawlee | miss | docs.stripe.com/billing/collection-method | 0.767 | docs.stripe.com/billing/subscriptions/build-subscr | 0.767 | docs.stripe.com/billing/subscriptions/build-subscr | 0.767 |
| colly+md | miss | docs.stripe.com/billing/subscriptions/build-subscr | 0.767 | docs.stripe.com/billing/subscriptions/build-subscr | 0.761 | docs.stripe.com/billing/subscriptions/build-subscr | 0.758 |
| playwright | miss | docs.stripe.com/billing/collection-method | 0.767 | docs.stripe.com/billing/subscriptions/build-subscr | 0.767 | docs.stripe.com/billing/subscriptions/build-subscr | 0.767 |


**Q17: How does Stripe handle tax calculation for billing?** [js-rendered]
*(expects URL containing: `billing/taxes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/advanced/tax | 0.793 | docs.stripe.com/payments/checkout/taxes | 0.783 | docs.stripe.com/payments/managed-payments/tax-comp | 0.761 |
| crawl4ai | #1 | docs.stripe.com/billing/taxes/collect-taxes | 0.822 | docs.stripe.com/tax/custom | 0.816 | docs.stripe.com/tax | 0.809 |
| crawl4ai-raw | #1 | docs.stripe.com/billing/taxes/collect-taxes | 0.822 | docs.stripe.com/tax/custom | 0.816 | docs.stripe.com/tax | 0.809 |
| scrapy+md | #1 | docs.stripe.com/billing/taxes/collect-taxes | 0.824 | docs.stripe.com/revenue-recognition/methodology/su | 0.792 | docs.stripe.com/invoicing/taxes?dashboard-or-api=d | 0.786 |
| crawlee | #1 | docs.stripe.com/billing/taxes/collect-taxes | 0.826 | docs.stripe.com/tax/custom | 0.822 | docs.stripe.com/billing | 0.819 |
| colly+md | #9 | docs.stripe.com/tax/custom | 0.822 | docs.stripe.com/billing | 0.819 | docs.stripe.com/tax/custom | 0.816 |
| playwright | #1 | docs.stripe.com/billing/taxes/collect-taxes | 0.826 | docs.stripe.com/tax/custom | 0.822 | docs.stripe.com/billing | 0.819 |


**Q18: How do I migrate data to Stripe?** [conceptual]
*(expects URL containing: `data-migrations`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/customer-balance/standard | 0.761 | docs.stripe.com/payments/ach-direct-debit/migratin | 0.757 | docs.stripe.com/payments/bacs-debit/export-data | 0.753 |
| crawl4ai | #1 | docs.stripe.com/get-started/data-migrations/overvi | 0.802 | docs.stripe.com/get-started/data-migrations/overvi | 0.797 | docs.stripe.com/stripe-data | 0.780 |
| crawl4ai-raw | #1 | docs.stripe.com/get-started/data-migrations/overvi | 0.802 | docs.stripe.com/get-started/data-migrations/overvi | 0.797 | docs.stripe.com/stripe-data | 0.780 |
| scrapy+md | #1 | docs.stripe.com/get-started/data-migrations/pan-im | 0.793 | docs.stripe.com/get-started/data-migrations/pan-im | 0.782 | docs.stripe.com/get-started/data-migrations/pan-im | 0.781 |
| crawlee | #4 | docs.stripe.com/billing/taxes/migration | 0.832 | docs.stripe.com/payments/checkout/migration | 0.820 | docs.stripe.com/stripe-data | 0.813 |
| colly+md | #4 | docs.stripe.com/billing/taxes/migration | 0.832 | docs.stripe.com/payments/checkout/migration | 0.820 | docs.stripe.com/stripe-data | 0.813 |
| playwright | #4 | docs.stripe.com/billing/taxes/migration | 0.832 | docs.stripe.com/payments/checkout/migration | 0.820 | docs.stripe.com/stripe-data | 0.813 |


</details>

## huggingface-transformers

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| scrapy+md | 38% (3/8) | 50% (4/8) | 50% (4/8) | 62% (5/8) | 75% (6/8) | 0.465 | 6346 | 240 |
| markcrawl | 25% (2/8) | 38% (3/8) | 50% (4/8) | 62% (5/8) | 62% (5/8) | 0.339 | 4518 | 300 |
| crawl4ai-raw | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.125 | 1018 | 295 |
| crawlee | 0% (0/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.062 | 67 | 16 |
| playwright | 0% (0/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.053 | 356 | 300 |
| crawl4ai | — | — | — | — | — | — | — | — |
| colly+md | — | — | — | — | — | — | — | — |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for huggingface-transformers</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do I use the Pipeline class for inference in Transformers?** [api-function]
*(expects URL containing: `pipeline_tutorial`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | huggingface.co/docs/transformers/v5.8.0/en/main_cl | 0.802 | huggingface.co/docs/transformers/v5.8.0/en/model_d | 0.780 | huggingface.co/docs/transformers/quicktour | 0.766 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | miss | huggingface.co/docs/transformers/index | 0.702 | huggingface.co/docs/transformers/index | 0.698 | huggingface.co/mistralai/Mistral-Small-4-119B-2603 | 0.676 |
| scrapy+md | #13 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.798 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.771 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.756 |
| crawlee | miss | huggingface.co/docs/transformers/quicktour | 0.766 | huggingface.co/docs/transformers/quicktour | 0.737 | huggingface.co/docs/transformers/index | 0.721 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/docs/transformers/quicktour | 0.766 | huggingface.co/docs/transformers/quicktour | 0.721 | huggingface.co/docs/transformers/quicktour | 0.712 |


**Q2: How do I train a model with the Hugging Face Trainer?** [api-function]
*(expects URL containing: `trainer`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | huggingface.co/docs/transformers/v5.8.0/en/model_d | 0.686 | huggingface.co/docs/transformers/v5.8.0/en/model_d | 0.668 | huggingface.co/docs/transformers/v5.8.0/en/tasks/t | 0.659 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | miss | discuss.huggingface.co/c/models/13 | 0.729 | discuss.huggingface.co/c/show-and-tell/65 | 0.717 | discuss.huggingface.co/c/spaces/24 | 0.716 |
| scrapy+md | #23 | huggingface.co/learn/llm-course/chapter0/1 | 0.679 | huggingface.co/google-t5/t5-base | 0.647 | huggingface.co/learn/llm-course/chapter1/1?fw=pt | 0.645 |
| crawlee | miss | huggingface.co/docs/transformers/quicktour | 0.671 | huggingface.co/docs/transformers/index | 0.640 | huggingface.co/docs/transformers/quicktour | 0.635 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/docs/transformers/quicktour | 0.735 | huggingface.co/docs/transformers/quicktour | 0.633 | huggingface.co/ | 0.620 |


**Q3: How do I generate text with a large language model?** [api-function]
*(expects URL containing: `llm_tutorial`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | huggingface.co/docs/transformers/llm_tutorial | 0.741 | huggingface.co/docs/transformers/v5.8.0/en/model_d | 0.738 | huggingface.co/docs/transformers/v5.8.0/en/main_cl | 0.727 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | miss | endpoints.huggingface.co/catalog?task=text-generat | 0.675 | huggingface.co/unsloth/Qwen3.5-9B-GGUF | 0.656 | huggingface.co/unsloth/Qwen3.5-35B-A3B-GGUF | 0.656 |
| scrapy+md | #1 | huggingface.co/docs/transformers/llm_tutorial | 0.743 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.726 | huggingface.co/docs/transformers/llm_tutorial | 0.726 |
| crawlee | miss | huggingface.co/docs/transformers/quicktour | 0.716 | huggingface.co/docs/transformers/index | 0.651 | huggingface.co/docs/transformers/quicktour | 0.636 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/docs/transformers/quicktour | 0.716 | huggingface.co/docs/transformers/index | 0.637 | huggingface.co/docs/transformers/quicktour | 0.636 |


**Q4: What are the design principles behind the Transformers library?** [conceptual]
*(expects URL containing: `philosophy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #8 | huggingface.co/docs/transformers/main/en/index | 0.741 | huggingface.co/docs/transformers/index | 0.741 | huggingface.co/docs/transformers/v5.8.0/en/index | 0.741 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | miss | huggingface.co/docs/transformers/index | 0.789 | huggingface.co/docs/transformers/index | 0.692 | huggingface.co/docs | 0.630 |
| scrapy+md | #2 | huggingface.co/docs/transformers/index | 0.737 | huggingface.co/docs/transformers/philosophy | 0.680 | huggingface.co/docs/transformers/index | 0.675 |
| crawlee | miss | huggingface.co/docs/transformers/index | 0.789 | huggingface.co/docs/transformers/index | 0.686 | huggingface.co/docs/transformers/quicktour | 0.678 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #43 | huggingface.co/docs/transformers/index | 0.737 | huggingface.co/docs/transformers/quicktour | 0.675 | huggingface.co/docs/transformers/quicktour | 0.661 |


**Q5: What models are supported in the Transformers library?** [cross-page]
*(expects URL containing: `models_timeline`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | huggingface.co/docs/transformers/v5.8.0/en/model_d | 0.770 | huggingface.co/docs/transformers/v5.8.0/en/index | 0.767 | huggingface.co/docs/transformers/main/en/index | 0.767 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | miss | huggingface.co/docs/transformers/index | 0.779 | huggingface.co/docs/transformers/index | 0.776 | huggingface.co/docs/transformers/index | 0.707 |
| scrapy+md | miss | huggingface.co/docs/transformers/index | 0.761 | huggingface.co/docs/transformers/index | 0.718 | huggingface.co/docs/transformers/model_doc/marian | 0.716 |
| crawlee | miss | huggingface.co/docs/transformers/index | 0.781 | huggingface.co/docs/transformers/index | 0.778 | huggingface.co/docs/transformers/quicktour | 0.727 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #23 | huggingface.co/docs/transformers/index | 0.761 | huggingface.co/docs/transformers/quicktour | 0.729 | huggingface.co/docs/transformers/quicktour | 0.713 |


**Q6: What is the Pipeline API reference in Transformers?** [api-function]
*(expects URL containing: `main_classes/pipelines`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | huggingface.co/docs/transformers/v5.8.0/en/main_cl | 0.771 | huggingface.co/docs/transformers/v5.8.0/en/main_cl | 0.763 | huggingface.co/docs/transformers/v5.8.0/en/main_cl | 0.757 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | miss | huggingface.co/docs/transformers/index | 0.674 | huggingface.co/docs/transformers/index | 0.647 | huggingface.co/docs/transformers/index | 0.640 |
| scrapy+md | #1 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.783 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.770 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.762 |
| crawlee | miss | huggingface.co/docs/transformers/index | 0.672 | huggingface.co/docs/transformers/quicktour | 0.670 | huggingface.co/docs/transformers/quicktour | 0.657 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #44 | huggingface.co/docs/transformers/quicktour | 0.670 | huggingface.co/docs/transformers/quicktour | 0.660 | huggingface.co/docs/transformers/peft | 0.646 |


**Q7: What does the Trainer class support for distributed training?** [api-function]
*(expects URL containing: `main_classes/trainer`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | huggingface.co/docs/transformers/quicktour | 0.681 | huggingface.co/docs/transformers/main/en/quicktour | 0.681 | huggingface.co/docs/transformers/v5.8.0/en/quickto | 0.681 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | miss | huggingface.co/docs | 0.636 | huggingface.co/docs/transformers/index | 0.621 | huggingface.co/unsloth/Qwen3.5-35B-A3B-GGUF | 0.603 |
| scrapy+md | #1 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.659 | huggingface.co/docs/tokenizers/python/latest/api/r | 0.654 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.653 |
| crawlee | miss | huggingface.co/docs/transformers/quicktour | 0.668 | huggingface.co/docs/transformers/peft | 0.668 | huggingface.co/docs | 0.628 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/docs/transformers/peft | 0.688 | huggingface.co/docs/transformers/quicktour | 0.653 | huggingface.co/docs | 0.628 |


**Q8: What is the Hugging Face Transformers library?** [conceptual]
*(expects URL containing: `transformers/index`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | huggingface.co/docs/transformers/v5.8.0/en/model_d | 0.778 | huggingface.co/docs/transformers/v5.8.0/en/model_d | 0.771 | huggingface.co/docs/transformers/index | 0.741 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | #1 | huggingface.co/docs/transformers/index | 0.824 | huggingface.co/models | 0.818 | huggingface.co/docs/transformers/index | 0.795 |
| scrapy+md | #10 | huggingface.co/learn/llm-course/th/chapter0/1 | 0.757 | huggingface.co/learn/llm-course/th/chapter1/1 | 0.751 | huggingface.co/learn/llm-course/th/chapter1/10 | 0.745 |
| crawlee | #2 | huggingface.co/docs/transformers/quicktour | 0.796 | huggingface.co/docs/transformers/index | 0.782 | huggingface.co/docs/transformers/index | 0.744 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #3 | huggingface.co/docs/transformers/quicktour | 0.809 | huggingface.co/models?library=transformers&sort=tr | 0.763 | huggingface.co/docs/transformers/index | 0.744 |


</details>

## kubernetes-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 7922 | 400 |
| crawl4ai | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 6822 | 400 |
| crawl4ai-raw | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 6822 | 400 |
| crawlee | 88% (7/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.938 | 6813 | 400 |
| colly+md | 88% (7/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.938 | 6743 | 399 |
| playwright | 88% (7/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.938 | 6812 | 400 |
| scrapy+md | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0% (0/8) | 12% (1/8) | 0.006 | 3507 | 315 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for kubernetes-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is a Kubernetes pod and what does it represent?** [conceptual]
*(expects URL containing: `workloads/pods`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.826 | kubernetes.io/docs/concepts/workloads/pods/_print/ | 0.815 | kubernetes.io/docs/concepts/workloads/ | 0.805 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.829 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.797 | v1-35.docs.kubernetes.io/docs/concepts/ | 0.796 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.829 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.797 | v1-35.docs.kubernetes.io/docs/concepts/ | 0.796 |
| scrapy+md | miss | kubernetes.io/docs/concepts/ | 0.788 | kubernetes.io/docs/reference/glossary/?all=true | 0.786 | kubernetes.io/docs/concepts/_print/ | 0.783 |
| crawlee | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.830 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.797 | kubernetes.io/docs/concepts/containers/ | 0.790 |
| colly+md | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.830 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.797 | kubernetes.io/pl/docs/concepts/ | 0.790 |
| playwright | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.830 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.797 | kubernetes.io/docs/concepts/containers/ | 0.790 |


**Q2: How do Kubernetes Deployments manage replicas and rollouts?** [api-function]
*(expects URL containing: `controllers/deployment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.854 | kubernetes.io/docs/concepts/_print/ | 0.847 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.847 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.847 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.816 | kubernetes.io/docs/concepts/workloads/management/ | 0.800 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.847 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.816 | kubernetes.io/docs/concepts/workloads/management/ | 0.800 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.847 | kubernetes.io/docs/concepts/_print/ | 0.816 | kubernetes.io/docs/concepts/_print/ | 0.800 |
| crawlee | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.852 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.816 | kubernetes.io/docs/concepts/workloads/management/ | 0.800 |
| colly+md | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.852 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.816 | kubernetes.io/docs/concepts/workloads/management/ | 0.800 |
| playwright | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.852 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.816 | kubernetes.io/docs/concepts/workloads/management/ | 0.800 |


**Q3: What is a Kubernetes Service and how does it expose pods?** [conceptual]
*(expects URL containing: `services-networking/service`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.909 | kubernetes.io/docs/concepts/services-networking/_p | 0.873 | kubernetes.io/docs/concepts/_print/ | 0.868 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.872 | kubernetes.io/docs/concepts/services-networking/se | 0.808 | kubernetes.io/docs/concepts/services-networking/se | 0.800 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.872 | kubernetes.io/docs/concepts/services-networking/se | 0.808 | kubernetes.io/docs/concepts/services-networking/se | 0.800 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.868 | kubernetes.io/docs/concepts/_print/ | 0.813 | kubernetes.io/docs/concepts/_print/ | 0.807 |
| crawlee | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.877 | kubernetes.io/docs/concepts/services-networking/se | 0.813 | kubernetes.io/docs/concepts/services-networking/se | 0.807 |
| colly+md | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.877 | kubernetes.io/docs/concepts/services-networking/se | 0.813 | kubernetes.io/docs/concepts/services-networking/se | 0.807 |
| playwright | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.877 | kubernetes.io/docs/concepts/services-networking/se | 0.813 | kubernetes.io/docs/concepts/services-networking/se | 0.807 |


**Q4: How do I use ConfigMaps to inject configuration into pods?** [api-function]
*(expects URL containing: `configuration/configmap`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.845 | kubernetes.io/docs/concepts/configuration/_print/ | 0.835 | kubernetes.io/docs/concepts/_print/ | 0.835 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/configuration/configma | 0.832 | kubernetes.io/docs/concepts/configuration/configma | 0.807 | kubernetes.io/docs/concepts/configuration/configma | 0.797 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/configuration/configma | 0.832 | kubernetes.io/docs/concepts/configuration/configma | 0.807 | kubernetes.io/docs/concepts/configuration/configma | 0.797 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.835 | kubernetes.io/docs/concepts/_print/ | 0.797 | kubernetes.io/docs/concepts/_print/ | 0.775 |
| crawlee | #1 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.837 | kubernetes.io/docs/concepts/configuration/configma | 0.835 | kubernetes.io/docs/concepts/configuration/configma | 0.808 |
| colly+md | #1 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.837 | kubernetes.io/docs/concepts/configuration/configma | 0.835 | kubernetes.io/docs/concepts/configuration/configma | 0.808 |
| playwright | #1 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.837 | kubernetes.io/docs/concepts/configuration/configma | 0.835 | kubernetes.io/docs/concepts/configuration/configma | 0.808 |


**Q5: How do I manage Secrets in Kubernetes?** [api-function]
*(expects URL containing: `configuration/secret`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/security/secrets-good- | 0.863 | kubernetes.io/docs/concepts/_print/ | 0.850 | kubernetes.io/docs/concepts/security/_print/ | 0.850 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/configuration/secret/ | 0.854 | kubernetes.io/docs/concepts/security/secrets-good- | 0.854 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.837 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/configuration/secret/ | 0.854 | kubernetes.io/docs/concepts/security/secrets-good- | 0.854 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.837 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.850 | kubernetes.io/docs/concepts/_print/ | 0.845 | kubernetes.io/docs/concepts/_print/ | 0.824 |
| crawlee | #1 | kubernetes.io/docs/concepts/security/secrets-good- | 0.855 | kubernetes.io/docs/concepts/configuration/secret/ | 0.854 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.838 |
| colly+md | #1 | kubernetes.io/docs/concepts/security/secrets-good- | 0.855 | kubernetes.io/docs/concepts/configuration/secret/ | 0.854 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.838 |
| playwright | #1 | kubernetes.io/docs/concepts/security/secrets-good- | 0.855 | kubernetes.io/docs/concepts/configuration/secret/ | 0.854 | kubernetes.io/docs/tasks/configmap-secret/managing | 0.838 |


**Q6: What are namespaces in Kubernetes and when should I use them?** [conceptual]
*(expects URL containing: `working-with-objects/namespaces`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/overview/working-with- | 0.875 | kubernetes.io/docs/tutorials/cluster-management/na | 0.847 | kubernetes.io/docs/tutorials/cluster-management/na | 0.837 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/overview/working-with- | 0.859 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.850 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.825 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/overview/working-with- | 0.859 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.850 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.825 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.824 | kubernetes.io/docs/concepts/_print/ | 0.823 | kubernetes.io/docs/concepts/_print/ | 0.804 |
| crawlee | #1 | kubernetes.io/docs/concepts/overview/working-with- | 0.859 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.851 | kubernetes.io/docs/concepts/overview/working-with- | 0.827 |
| colly+md | #1 | kubernetes.io/docs/concepts/overview/working-with- | 0.859 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.851 | kubernetes.io/docs/concepts/overview/working-with- | 0.827 |
| playwright | #1 | kubernetes.io/docs/concepts/overview/working-with- | 0.859 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.851 | kubernetes.io/docs/concepts/overview/working-with- | 0.827 |


**Q7: How does Kubernetes Ingress route external traffic?** [conceptual]
*(expects URL containing: `services-networking/ingress`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.817 | kubernetes.io/docs/reference/networking/virtual-ip | 0.805 | kubernetes.io/docs/concepts/services-networking/_p | 0.797 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.818 | kubernetes.io/docs/concepts/services-networking/se | 0.780 | kubernetes.io/docs/concepts/services-networking/in | 0.777 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.818 | kubernetes.io/docs/concepts/services-networking/se | 0.780 | kubernetes.io/docs/concepts/services-networking/in | 0.777 |
| scrapy+md | #20 | kubernetes.io/docs/concepts/_print/ | 0.796 | kubernetes.io/docs/concepts/_print/ | 0.794 | kubernetes.io/docs/concepts/_print/ | 0.790 |
| crawlee | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.814 | kubernetes.io/docs/concepts/services-networking/se | 0.786 | kubernetes.io/docs/concepts/services-networking/se | 0.781 |
| colly+md | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.814 | kubernetes.io/docs/concepts/services-networking/se | 0.786 | kubernetes.io/docs/concepts/services-networking/se | 0.781 |
| playwright | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.814 | kubernetes.io/docs/concepts/services-networking/se | 0.786 | kubernetes.io/docs/concepts/services-networking/se | 0.781 |


**Q8: What is a StatefulSet and when do I need one?** [api-function]
*(expects URL containing: `controllers/statefulset`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.794 | kubernetes.io/docs/tutorials/stateful-application/ | 0.736 | kubernetes.io/docs/reference/generated/kubernetes- | 0.725 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.749 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.747 | kubernetes.io/docs/tasks/run-application/delete-st | 0.694 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.749 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.747 | kubernetes.io/docs/tasks/run-application/delete-st | 0.694 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.701 | kubernetes.io/zh-cn/feed.xml | 0.698 | kubernetes.io/docs/concepts/_print/ | 0.695 |
| crawlee | #2 | kubernetes.io/docs/tasks/run-application/force-del | 0.745 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.743 | kubernetes.io/docs/tasks/run-application/run-repli | 0.693 |
| colly+md | #2 | kubernetes.io/docs/tasks/run-application/force-del | 0.745 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.743 | kubernetes.io/docs/tasks/debug/debug-application/d | 0.688 |
| playwright | #2 | kubernetes.io/docs/tasks/run-application/force-del | 0.745 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.743 | kubernetes.io/docs/tasks/run-application/run-repli | 0.693 |


</details>

## postgres-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawlee | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 1226 | 400 |
| colly+md | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 1115 | 401 |
| playwright | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 1216 | 400 |
| crawl4ai | 75% (6/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.875 | 1193 | 400 |
| crawl4ai-raw | 75% (6/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.875 | 1193 | 400 |
| markcrawl | 62% (5/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.792 | 2348 | 400 |
| scrapy+md | 25% (2/8) | 25% (2/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.275 | 1531 | 394 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for postgres-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What data types does PostgreSQL support?** [cross-page]
*(expects URL containing: `datatype`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/datatype.html | 0.801 | www.postgresql.org/docs/current/datatype.html | 0.788 | www.postgresql.org/docs/current/typeconv-overview. | 0.786 |
| crawl4ai | #2 | www.postgresql.org/about/ | 0.818 | www.postgresql.org/docs/18/datatype.html | 0.788 | www.postgresql.org/docs/current/datatype.html | 0.788 |
| crawl4ai-raw | #2 | www.postgresql.org/about/ | 0.818 | www.postgresql.org/docs/18/datatype.html | 0.788 | www.postgresql.org/docs/current/datatype.html | 0.788 |
| scrapy+md | #5 | www.postgresql.org/docs/7.4/ddl-constraints.html | 0.790 | www.postgresql.org/docs/8.0/ddl-constraints.html | 0.788 | www.postgresql.org/docs/9.2/multibyte.html | 0.780 |
| crawlee | #1 | www.postgresql.org/docs/18/datatype.html | 0.801 | www.postgresql.org/docs/current/datatype.html | 0.801 | www.postgresql.org/docs/17/datatype.html | 0.801 |
| colly+md | #1 | www.postgresql.org/docs/17/datatype.html | 0.801 | www.postgresql.org/docs/current/datatype.html | 0.801 | www.postgresql.org/docs/18/datatype.html | 0.801 |
| playwright | #1 | www.postgresql.org/docs/current/datatype.html | 0.801 | www.postgresql.org/docs/18/datatype.html | 0.801 | www.postgresql.org/docs/17/datatype.html | 0.801 |


**Q2: What is the SQL syntax for queries in PostgreSQL?** [conceptual]
*(expects URL containing: `sql-syntax`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | www.postgresql.org/docs/current/sql.html | 0.775 | www.postgresql.org/docs/current/sql-syntax-lexical | 0.763 | www.postgresql.org/docs/current/sql-select.html | 0.762 |
| crawl4ai | #1 | www.postgresql.org/docs/17/sql-syntax.html | 0.801 | www.postgresql.org/docs/current/sql-syntax.html | 0.800 | www.postgresql.org/docs/18/sql-syntax.html | 0.800 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/sql-syntax.html | 0.801 | www.postgresql.org/docs/current/sql-syntax.html | 0.800 | www.postgresql.org/docs/18/sql-syntax.html | 0.800 |
| scrapy+md | miss | www.postgresql.org/docs/7.4/sql.html | 0.772 | www.postgresql.org/docs/7.4/queries.html | 0.762 | www.postgresql.org/docs/8.3/tutorial-sql-intro.htm | 0.753 |
| crawlee | #1 | www.postgresql.org/docs/current/sql-syntax.html | 0.813 | www.postgresql.org/docs/18/sql-syntax.html | 0.813 | www.postgresql.org/docs/17/sql-syntax.html | 0.809 |
| colly+md | #1 | www.postgresql.org/docs/current/sql-syntax.html | 0.813 | www.postgresql.org/docs/18/sql-syntax.html | 0.813 | www.postgresql.org/docs/16/sql-syntax.html | 0.811 |
| playwright | #1 | www.postgresql.org/docs/current/sql-syntax.html | 0.813 | www.postgresql.org/docs/18/sql-syntax.html | 0.813 | www.postgresql.org/docs/17/sql-syntax.html | 0.809 |


**Q3: How do indexes work in PostgreSQL?** [conceptual]
*(expects URL containing: `indexes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/indexes-index-only | 0.790 | www.postgresql.org/docs/current/sql-createindex.ht | 0.788 | www.postgresql.org/docs/current/indexes-index-only | 0.785 |
| crawl4ai | #1 | www.postgresql.org/docs/18/indexes.html | 0.809 | www.postgresql.org/docs/current/indexes.html | 0.809 | www.postgresql.org/docs/17/indexes.html | 0.808 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/indexes.html | 0.809 | www.postgresql.org/docs/current/indexes.html | 0.809 | www.postgresql.org/docs/17/indexes.html | 0.808 |
| scrapy+md | miss | www.postgresql.org/docs/7.4/sql-reindex.html | 0.764 | www.postgresql.org/docs/7.4/sql-reindex.html | 0.738 | www.postgresql.org/docs/7.4/sql-explain.html | 0.738 |
| crawlee | #1 | www.postgresql.org/docs/current/indexes.html | 0.809 | www.postgresql.org/docs/18/indexes.html | 0.809 | www.postgresql.org/docs/17/indexes.html | 0.807 |
| colly+md | #1 | www.postgresql.org/docs/16/indexes.html | 0.811 | www.postgresql.org/docs/18/indexes.html | 0.809 | www.postgresql.org/docs/current/indexes.html | 0.809 |
| playwright | #1 | www.postgresql.org/docs/current/indexes.html | 0.809 | www.postgresql.org/docs/18/indexes.html | 0.809 | www.postgresql.org/docs/17/indexes.html | 0.807 |


**Q4: How does MVCC concurrency control work in PostgreSQL?** [conceptual]
*(expects URL containing: `mvcc`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | www.postgresql.org/docs/current/storage-hot.html | 0.768 | www.postgresql.org/docs/current/applevel-consisten | 0.738 | www.postgresql.org/docs/current/mvcc.html | 0.720 |
| crawl4ai | #1 | www.postgresql.org/docs/17/mvcc.html | 0.743 | www.postgresql.org/docs/18/mvcc.html | 0.740 | www.postgresql.org/docs/current/mvcc.html | 0.740 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/mvcc.html | 0.743 | www.postgresql.org/docs/18/mvcc.html | 0.740 | www.postgresql.org/docs/current/mvcc.html | 0.740 |
| scrapy+md | #1 | www.postgresql.org/docs/8.0/mvcc.html | 0.856 | www.postgresql.org/docs/7.1/sql-set-transaction.ht | 0.704 | www.postgresql.org/docs/8.0/mvcc.html | 0.697 |
| crawlee | #1 | www.postgresql.org/docs/17/mvcc.html | 0.742 | www.postgresql.org/docs/current/mvcc.html | 0.739 | www.postgresql.org/docs/18/mvcc.html | 0.739 |
| colly+md | #1 | www.postgresql.org/docs/16/mvcc.html | 0.746 | www.postgresql.org/docs/17/mvcc.html | 0.742 | www.postgresql.org/docs/18/mvcc.html | 0.739 |
| playwright | #1 | www.postgresql.org/docs/17/mvcc.html | 0.742 | www.postgresql.org/docs/18/mvcc.html | 0.739 | www.postgresql.org/docs/current/mvcc.html | 0.739 |


**Q5: How do transactions work in PostgreSQL?** [conceptual]
*(expects URL containing: `transactions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | www.postgresql.org/docs/current/logicaldecoding-ex | 0.757 | www.postgresql.org/docs/current/plpgsql-transactio | 0.744 | www.postgresql.org/docs/current/sql-prepare-transa | 0.739 |
| crawl4ai | #1 | www.postgresql.org/docs/current/transactions.html | 0.780 | www.postgresql.org/docs/18/transactions.html | 0.780 | www.postgresql.org/docs/current/sql-commands.html | 0.760 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/transactions.html | 0.780 | www.postgresql.org/docs/18/transactions.html | 0.780 | www.postgresql.org/docs/current/sql-commands.html | 0.760 |
| scrapy+md | miss | www.postgresql.org/docs/7.4/sql-begin.html | 0.775 | www.postgresql.org/docs/7.4/sql-begin.html | 0.762 | www.postgresql.org/docs/9.0/sql-rollback-to.html | 0.759 |
| crawlee | #1 | www.postgresql.org/docs/18/transactions.html | 0.761 | www.postgresql.org/docs/current/transactions.html | 0.761 | www.postgresql.org/docs/18/sql-commands.html | 0.750 |
| colly+md | #1 | www.postgresql.org/docs/current/transactions.html | 0.761 | www.postgresql.org/docs/current/sql-commands.html | 0.750 | www.postgresql.org/docs/18/sql-commands.html | 0.750 |
| playwright | #1 | www.postgresql.org/docs/current/transactions.html | 0.761 | www.postgresql.org/docs/18/transactions.html | 0.761 | www.postgresql.org/docs/18/sql-commands.html | 0.750 |


**Q6: How do I set up logical replication in PostgreSQL?** [api-function]
*(expects URL containing: `logical-replication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.842 | www.postgresql.org/docs/current/logical-replicatio | 0.777 | www.postgresql.org/docs/current/sql-createsubscrip | 0.777 |
| crawl4ai | #1 | www.postgresql.org/docs/18/logical-replication.htm | 0.836 | www.postgresql.org/docs/current/logical-replicatio | 0.836 | www.postgresql.org/docs/17/logical-replication.htm | 0.826 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.836 | www.postgresql.org/docs/18/logical-replication.htm | 0.836 | www.postgresql.org/docs/17/logical-replication.htm | 0.826 |
| scrapy+md | miss | www.postgresql.org/docs/7.3/app-psql.html | 0.716 | www.postgresql.org/docs/9.1/upgrading.html | 0.701 | www.postgresql.org/docs/7.3/app-psql.html | 0.694 |
| crawlee | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.842 | www.postgresql.org/docs/18/logical-replication.htm | 0.842 | www.postgresql.org/docs/17/logical-replication.htm | 0.840 |
| colly+md | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.842 | www.postgresql.org/docs/18/logical-replication.htm | 0.842 | www.postgresql.org/docs/17/logical-replication.htm | 0.840 |
| playwright | #1 | www.postgresql.org/docs/18/logical-replication.htm | 0.842 | www.postgresql.org/docs/current/logical-replicatio | 0.842 | www.postgresql.org/docs/17/logical-replication.htm | 0.840 |


**Q7: What built-in functions and operators are available in PostgreSQL?** [cross-page]
*(expects URL containing: `functions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/functions.html | 0.826 | www.postgresql.org/docs/current/sql-expressions.ht | 0.813 | www.postgresql.org/docs/current/sql-createopclass. | 0.792 |
| crawl4ai | #1 | www.postgresql.org/docs/17/functions.html | 0.831 | www.postgresql.org/docs/18/functions.html | 0.831 | www.postgresql.org/docs/current/functions.html | 0.831 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/functions.html | 0.831 | www.postgresql.org/docs/17/functions.html | 0.831 | www.postgresql.org/docs/18/functions.html | 0.831 |
| scrapy+md | #1 | www.postgresql.org/docs/8.1/functions.html | 0.854 | www.postgresql.org/docs/7.3/functions.html | 0.807 | www.postgresql.org/docs/7.4/sql.html | 0.789 |
| crawlee | #1 | www.postgresql.org/docs/current/functions.html | 0.822 | www.postgresql.org/docs/17/functions.html | 0.822 | www.postgresql.org/docs/18/functions.html | 0.822 |
| colly+md | #1 | www.postgresql.org/docs/current/functions.html | 0.822 | www.postgresql.org/docs/17/functions.html | 0.822 | www.postgresql.org/docs/18/functions.html | 0.822 |
| playwright | #1 | www.postgresql.org/docs/current/functions.html | 0.822 | www.postgresql.org/docs/17/functions.html | 0.822 | www.postgresql.org/docs/18/functions.html | 0.822 |


**Q8: How do I use full text search in PostgreSQL?** [api-function]
*(expects URL containing: `textsearch`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/textsearch-control | 0.783 | www.postgresql.org/docs/current/textsearch-configu | 0.764 | www.postgresql.org/docs/current/pgtrgm.html | 0.757 |
| crawl4ai | #2 | www.postgresql.org/docs/current/pgtrgm.html | 0.747 | www.postgresql.org/docs/17/textsearch.html | 0.742 | www.postgresql.org/docs/18/textsearch.html | 0.740 |
| crawl4ai-raw | #2 | www.postgresql.org/docs/current/pgtrgm.html | 0.747 | www.postgresql.org/docs/17/textsearch.html | 0.742 | www.postgresql.org/docs/current/textsearch.html | 0.740 |
| scrapy+md | miss | www.postgresql.org/docs/8.3/tsearch2.html | 0.744 | www.postgresql.org/docs/8.4/tsearch2.html | 0.744 | www.postgresql.org/docs/9.3/tsearch2.html | 0.741 |
| crawlee | #1 | www.postgresql.org/docs/17/textsearch.html | 0.787 | www.postgresql.org/docs/18/textsearch.html | 0.785 | www.postgresql.org/docs/current/textsearch.html | 0.785 |
| colly+md | #1 | www.postgresql.org/docs/16/textsearch.html | 0.788 | www.postgresql.org/docs/17/textsearch.html | 0.787 | www.postgresql.org/docs/18/textsearch.html | 0.785 |
| playwright | #1 | www.postgresql.org/docs/17/textsearch.html | 0.787 | www.postgresql.org/docs/current/textsearch.html | 0.785 | www.postgresql.org/docs/18/textsearch.html | 0.785 |


</details>

## mdn-css

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai | 75% (6/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.812 | 3864 | 300 |
| crawl4ai-raw | 75% (6/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.812 | 3864 | 300 |
| crawlee | 75% (6/8) | 75% (6/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.775 | 3891 | 300 |
| playwright | 62% (5/8) | 75% (6/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.719 | 4168 | 300 |
| markcrawl | 50% (4/8) | 62% (5/8) | 62% (5/8) | 62% (5/8) | 75% (6/8) | 0.573 | 1006 | 300 |
| colly+md | 50% (4/8) | 50% (4/8) | 50% (4/8) | 75% (6/8) | 75% (6/8) | 0.535 | 4190 | 289 |
| scrapy+md | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.125 | 621 | 300 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for mdn-css</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How does the CSS display property work?** [api-function]
*(expects URL containing: `CSS/Reference/Properties/display`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #12 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.766 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.761 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.746 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.774 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.763 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.750 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.774 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.763 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.750 |
| scrapy+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.750 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.724 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.722 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.774 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.763 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.746 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.779 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.767 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.760 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.779 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.767 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.760 |


**Q2: How do I use flexbox for page layout?** [conceptual]
*(expects URL containing: `Flexible_box_layout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.812 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.801 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.792 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.802 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.794 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.793 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.802 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.794 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.793 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.708 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.683 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.682 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.802 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.794 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.793 |
| colly+md | #9 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.811 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.810 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.806 |
| playwright | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.811 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.804 | developer.mozilla.org/en-US/docs/Web/CSS/How_to/La | 0.795 |


**Q3: How does CSS Grid layout work?** [conceptual]
*(expects URL containing: `Grid_layout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.856 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.851 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.849 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.848 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.812 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.807 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.848 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.812 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.807 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.773 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.722 | developer.mozilla.org/en-US/docs/Web/CSS | 0.708 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.840 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.814 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.807 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.839 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.833 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.828 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.834 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.820 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.819 |


**Q4: What is the CSS box model?** [conceptual]
*(expects URL containing: `Box_model`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.806 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.773 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.765 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.820 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.792 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.779 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.820 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.792 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.779 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.673 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.671 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.667 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.817 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.807 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.774 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.786 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.784 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.782 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.817 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.807 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.774 |


**Q5: How does the CSS margin property work?** [api-function]
*(expects URL containing: `Reference/Properties/margin`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.811 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.803 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.801 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.793 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.765 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.761 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.793 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.765 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.761 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.689 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.687 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.686 |
| crawlee | #5 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.786 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.762 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.753 |
| colly+md | #6 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.789 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.778 | developer.mozilla.org/en-US/docs/Learn/web/develop | 0.762 |
| playwright | #4 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.786 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.762 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.749 |


**Q6: How does CSS specificity determine which rules win?** [conceptual]
*(expects URL containing: `Cascade/Specificity`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.737 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.726 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.724 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.813 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.775 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.770 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.813 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.775 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.770 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.693 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.678 | developer.mozilla.org/en-US/docs/Web/CSS | 0.676 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.814 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.775 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.770 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.816 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.775 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.763 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.818 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.770 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.763 |


**Q7: How does the :hover pseudo-class work in CSS?** [api-function]
*(expects URL containing: `Selectors/:hover`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.842 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.789 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.768 |
| crawl4ai | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.791 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.778 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.769 |
| crawl4ai-raw | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.791 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.778 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.769 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.757 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.729 | developer.mozilla.org/zh-CN/docs/Web/HTTP/Referenc | 0.701 |
| crawlee | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.799 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.778 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.765 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.778 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.775 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.771 |
| playwright | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.816 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.771 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.765 |


**Q8: How do I create CSS animations?** [conceptual]
*(expects URL containing: `Animations/Using`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.815 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.761 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.756 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.790 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.777 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.763 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.790 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.777 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.763 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.701 | developer.mozilla.org/en-US/docs/Web/CSS | 0.698 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.652 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.780 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.766 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.760 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/API/Web/Anima | 0.765 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sc | 0.760 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.757 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.780 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Mo | 0.766 | developer.mozilla.org/en-US/docs/Web/API/Web_Anima | 0.765 |


</details>

## rust-book

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 62% (5/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.812 | 1287 | 112 |
| crawl4ai | 62% (5/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.792 | 2702 | 200 |
| crawl4ai-raw | 62% (5/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.792 | 2702 | 200 |
| crawlee | 50% (4/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.729 | 2829 | 200 |
| playwright | 50% (4/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.729 | 2829 | 200 |
| colly+md | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0% (0/8) | 12% (1/8) | 0.011 | 1976 | 54 |
| scrapy+md | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0% (0/8) | 12% (1/8) | 0.007 | 2978 | 199 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for rust-book</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is ownership in Rust?** [conceptual]
*(expects URL containing: `ch04-01-what-is-ownership`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch04-00-understanding-owner | 0.887 | doc.rust-lang.org/book/ch04-01-what-is-ownership.h | 0.884 | doc.rust-lang.org/book/print.html | 0.840 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch04-00-understandin | 0.840 | doc.rust-lang.org/book/ch04-00-understanding-owner | 0.840 | doc.rust-lang.org/book/ch04-01-what-is-ownership.h | 0.814 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch04-00-understandin | 0.840 | doc.rust-lang.org/book/ch04-00-understanding-owner | 0.840 | doc.rust-lang.org/book/ch04-01-what-is-ownership.h | 0.814 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.816 | doc.rust-lang.org/book/print.html | 0.816 | doc.rust-lang.org/stable/book/print.html | 0.795 |
| crawlee | #1 | doc.rust-lang.org/stable/book/ch04-01-what-is-owne | 0.834 | doc.rust-lang.org/book/ch04-01-what-is-ownership.h | 0.834 | doc.rust-lang.org/book/ch04-01-what-is-ownership.h | 0.816 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.816 | doc.rust-lang.org/book/print.html | 0.816 | doc.rust-lang.org/book/print.html | 0.795 |
| playwright | #1 | doc.rust-lang.org/book/ch04-01-what-is-ownership.h | 0.834 | doc.rust-lang.org/stable/book/ch04-01-what-is-owne | 0.834 | doc.rust-lang.org/stable/book/ch04-01-what-is-owne | 0.816 |


**Q2: How do references and borrowing work in Rust?** [conceptual]
*(expects URL containing: `ch04-02-references-and-borrowing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.848 | doc.rust-lang.org/book/ch04-02-references-and-borr | 0.848 | doc.rust-lang.org/book/print.html | 0.823 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch04-02-references-and-borr | 0.822 | doc.rust-lang.org/book/print.html | 0.822 | doc.rust-lang.org/stable/book/ch04-02-references-a | 0.822 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch04-02-references-and-borr | 0.822 | doc.rust-lang.org/book/print.html | 0.822 | doc.rust-lang.org/stable/book/ch04-02-references-a | 0.822 |
| scrapy+md | miss | doc.rust-lang.org/nomicon/references.html | 0.826 | doc.rust-lang.org/stable/book/print.html | 0.824 | doc.rust-lang.org/book/print.html | 0.824 |
| crawlee | #1 | doc.rust-lang.org/book/ch04-02-references-and-borr | 0.824 | doc.rust-lang.org/book/print.html | 0.824 | doc.rust-lang.org/stable/book/ch04-02-references-a | 0.824 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.824 | doc.rust-lang.org/stable/book/print.html | 0.824 | doc.rust-lang.org/book/print.html | 0.815 |
| playwright | #1 | doc.rust-lang.org/stable/book/ch04-02-references-a | 0.824 | doc.rust-lang.org/book/print.html | 0.824 | doc.rust-lang.org/book/ch04-02-references-and-borr | 0.824 |


**Q3: How do I define structs in Rust?** [api-function]
*(expects URL containing: `ch05-01-defining-structs`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.833 | doc.rust-lang.org/book/ch05-00-structs.html | 0.830 | doc.rust-lang.org/book/ch05-01-defining-structs.ht | 0.786 |
| crawl4ai | #3 | doc.rust-lang.org/book/print.html | 0.851 | doc.rust-lang.org/book/print.html | 0.832 | doc.rust-lang.org/book/ch05-00-structs.html | 0.824 |
| crawl4ai-raw | #3 | doc.rust-lang.org/book/print.html | 0.851 | doc.rust-lang.org/book/print.html | 0.832 | doc.rust-lang.org/book/ch05-00-structs.html | 0.824 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.855 | doc.rust-lang.org/stable/book/print.html | 0.855 | doc.rust-lang.org/stable/book/print.html | 0.831 |
| crawlee | #3 | doc.rust-lang.org/book/print.html | 0.855 | doc.rust-lang.org/book/print.html | 0.831 | doc.rust-lang.org/stable/book/ch05-00-structs.html | 0.815 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.855 | doc.rust-lang.org/stable/book/print.html | 0.855 | doc.rust-lang.org/stable/book/print.html | 0.831 |
| playwright | #3 | doc.rust-lang.org/book/print.html | 0.855 | doc.rust-lang.org/book/print.html | 0.831 | doc.rust-lang.org/stable/book/ch05-00-structs.html | 0.815 |


**Q4: How do enums work in Rust?** [conceptual]
*(expects URL containing: `ch06-01-defining-an-enum`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.817 | doc.rust-lang.org/book/print.html | 0.811 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.797 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch06-00-enums.html | 0.833 | doc.rust-lang.org/stable/book/ch06-00-enums.html | 0.833 | doc.rust-lang.org/stable/book/ch06-01-defining-an- | 0.821 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch06-00-enums.html | 0.833 | doc.rust-lang.org/stable/book/ch06-00-enums.html | 0.833 | doc.rust-lang.org/stable/book/ch06-01-defining-an- | 0.821 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.813 | doc.rust-lang.org/book/print.html | 0.813 | doc.rust-lang.org/stable/book/print.html | 0.810 |
| crawlee | #1 | doc.rust-lang.org/stable/book/ch06-00-enums.html | 0.813 | doc.rust-lang.org/book/ch06-00-enums.html | 0.813 | doc.rust-lang.org/book/print.html | 0.813 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.813 | doc.rust-lang.org/book/print.html | 0.813 | doc.rust-lang.org/stable/book/print.html | 0.810 |
| playwright | #1 | doc.rust-lang.org/book/ch06-00-enums.html | 0.813 | doc.rust-lang.org/stable/book/ch06-00-enums.html | 0.813 | doc.rust-lang.org/book/print.html | 0.813 |


**Q5: How do I use generics in Rust?** [conceptual]
*(expects URL containing: `ch10-01-syntax`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.830 | doc.rust-lang.org/book/ch10-00-generics.html | 0.823 | doc.rust-lang.org/book/ch20-03-advanced-types.html | 0.788 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.828 | doc.rust-lang.org/stable/book/ch10-00-generics.htm | 0.817 | doc.rust-lang.org/book/ch10-00-generics.html | 0.817 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.828 | doc.rust-lang.org/stable/book/ch10-00-generics.htm | 0.817 | doc.rust-lang.org/book/ch10-00-generics.html | 0.817 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.830 | doc.rust-lang.org/stable/book/print.html | 0.830 | doc.rust-lang.org/stable/book/print.html | 0.773 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.830 | doc.rust-lang.org/book/ch10-00-generics.html | 0.788 | doc.rust-lang.org/stable/book/ch10-00-generics.htm | 0.788 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.830 | doc.rust-lang.org/book/print.html | 0.830 | doc.rust-lang.org/stable/book/print.html | 0.773 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.830 | doc.rust-lang.org/stable/book/ch10-00-generics.htm | 0.788 | doc.rust-lang.org/book/ch10-00-generics.html | 0.788 |


**Q6: What are traits in Rust and how do I define them?** [conceptual]
*(expects URL containing: `ch10-02-traits`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.810 | doc.rust-lang.org/book/appendix-03-derivable-trait | 0.799 | doc.rust-lang.org/book/print.html | 0.796 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.814 | doc.rust-lang.org/book/ch10-02-traits.html | 0.811 | doc.rust-lang.org/stable/book/ch10-02-traits.html | 0.811 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch17-05-traits-for-async.ht | 0.814 | doc.rust-lang.org/book/ch10-02-traits.html | 0.811 | doc.rust-lang.org/stable/book/ch10-02-traits.html | 0.811 |
| scrapy+md | #18 | doc.rust-lang.org/stable/book/print.html | 0.811 | doc.rust-lang.org/book/print.html | 0.811 | doc.rust-lang.org/stable/book/print.html | 0.787 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.811 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.798 | doc.rust-lang.org/reference/items/traits.html#dyn- | 0.789 |
| colly+md | #11 | doc.rust-lang.org/stable/book/print.html | 0.811 | doc.rust-lang.org/book/print.html | 0.811 | doc.rust-lang.org/book/print.html | 0.787 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.811 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.798 | doc.rust-lang.org/reference/items/traits.html | 0.789 |


**Q7: How do closures work in Rust?** [conceptual]
*(expects URL containing: `ch13-01-closures`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch13-01-closures.html | 0.882 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.816 | doc.rust-lang.org/book/print.html | 0.816 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.847 | doc.rust-lang.org/book/ch13-01-closures.html | 0.839 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.823 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.847 | doc.rust-lang.org/book/ch13-01-closures.html | 0.839 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.823 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.873 | doc.rust-lang.org/book/print.html | 0.873 | doc.rust-lang.org/nomicon/hrtb.html | 0.813 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.873 | doc.rust-lang.org/book/ch13-01-closures.html | 0.818 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.812 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.873 | doc.rust-lang.org/book/print.html | 0.873 | doc.rust-lang.org/stable/book/print.html | 0.812 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.873 | doc.rust-lang.org/book/ch13-01-closures.html | 0.818 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.812 |


**Q8: How do I handle errors with Result in Rust?** [conceptual]
*(expects URL containing: `ch09`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch09-00-error-handling.html | 0.803 | doc.rust-lang.org/book/print.html | 0.797 | doc.rust-lang.org/book/ch02-00-guessing-game-tutor | 0.797 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch09-02-recoverable-errors- | 0.800 | doc.rust-lang.org/book/print.html | 0.800 | doc.rust-lang.org/stable/book/ch09-02-recoverable- | 0.800 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch09-02-recoverable-errors- | 0.800 | doc.rust-lang.org/book/print.html | 0.800 | doc.rust-lang.org/stable/book/ch09-02-recoverable- | 0.800 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.792 | doc.rust-lang.org/stable/book/print.html | 0.792 | doc.rust-lang.org/book/print.html | 0.784 |
| crawlee | #1 | doc.rust-lang.org/stable/book/ch09-02-recoverable- | 0.792 | doc.rust-lang.org/book/print.html | 0.792 | doc.rust-lang.org/book/ch09-02-recoverable-errors- | 0.792 |
| colly+md | miss | doc.rust-lang.org/stable/book/print.html | 0.792 | doc.rust-lang.org/book/print.html | 0.792 | doc.rust-lang.org/stable/book/print.html | 0.784 |
| playwright | #1 | doc.rust-lang.org/book/ch09-02-recoverable-errors- | 0.792 | doc.rust-lang.org/book/print.html | 0.792 | doc.rust-lang.org/stable/book/ch09-02-recoverable- | 0.792 |


</details>

## smittenkitchen

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 62% (5/8) | 62% (5/8) | 62% (5/8) | 62% (5/8) | 75% (6/8) | 0.634 | 10115 | 200 |
| colly+md | 38% (3/8) | 38% (3/8) | 38% (3/8) | 50% (4/8) | 50% (4/8) | 0.389 | 3708 | 199 |
| crawl4ai | 12% (1/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.250 | 773 | 200 |
| crawl4ai-raw | 12% (1/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.250 | 773 | 200 |
| scrapy+md | 25% (2/8) | 25% (2/8) | 25% (2/8) | 25% (2/8) | 25% (2/8) | 0.250 | 18860 | 138 |
| crawlee | 25% (2/8) | 25% (2/8) | 25% (2/8) | 25% (2/8) | 25% (2/8) | 0.250 | 4167 | 203 |
| playwright | 0% (0/8) | 0% (0/8) | 0% (0/8) | 25% (2/8) | 25% (2/8) | 0.033 | 3029 | 200 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for smittenkitchen</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do you make world peace cookies?** [factual-lookup]
*(expects URL containing: `world-peace-cookies`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2007/01/world-peace-cookies/ | 0.812 | smittenkitchen.com/2007/01/world-peace-cookies/ | 0.792 | smittenkitchen.com/2007/01/world-peace-cookies/ | 0.760 |
| crawl4ai | miss | smittenkitchen.com/about/faq/ | 0.601 | smittenkitchen.com/subscribe/ | 0.578 | smittenkitchen.com/about/faq/ | 0.572 |
| crawl4ai-raw | miss | smittenkitchen.com/about/faq/ | 0.601 | smittenkitchen.com/subscribe/ | 0.578 | smittenkitchen.com/about/faq/ | 0.572 |
| scrapy+md | miss | smittenkitchen.com/2006/11/chocolate-chip-sour-cre | 0.636 | smittenkitchen.com/2010/01/best-cocoa-brownies/?re | 0.629 | smittenkitchen.com/2010/01/best-cocoa-brownies/?re | 0.629 |
| crawlee | miss | smittenkitchen.com/?random&timestamp=1777919490717 | 0.624 | smittenkitchen.com/?random&timestamp=1777919490717 | 0.622 | smittenkitchen.com/?random&timestamp=1777919490717 | 0.620 |
| colly+md | miss | smittenkitchen.com/2026/02/banana-chocolate-chip-c | 0.631 | smittenkitchen.com/2026/02/banana-chocolate-chip-c | 0.631 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.600 |
| playwright | miss | smittenkitchen.com/about/faq/ | 0.576 | smittenkitchen.com/about/faq/ | 0.575 | smittenkitchen.com/about/faq/ | 0.560 |


**Q2: What's the recipe for miso chicken and rice?** [factual-lookup]
*(expects URL containing: `miso-chicken-and-rice`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.787 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.782 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.774 |
| crawl4ai | miss | smittenkitchen.com/./recipes/ingredient/meat/chick | 0.661 | smittenkitchen.com/./recipes/ingredient/grain/?for | 0.655 | smittenkitchen.com/subscribe/ | 0.648 |
| crawl4ai-raw | miss | smittenkitchen.com/./recipes/ingredient/meat/chick | 0.661 | smittenkitchen.com/./recipes/ingredient/grain/?for | 0.655 | smittenkitchen.com/subscribe/ | 0.648 |
| scrapy+md | #1 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.819 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.811 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.784 |
| crawlee | #1 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.819 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.811 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.782 |
| colly+md | #1 | smittenkitchen.com/2026/02/miso-chicken-and-rice/# | 0.819 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.819 | smittenkitchen.com/2026/02/miso-chicken-and-rice/# | 0.811 |
| playwright | miss | smittenkitchen.com/subscribe/ | 0.641 | smittenkitchen.com/ | 0.628 | smittenkitchen.com/recipes/ingredient/meat/chicken | 0.595 |


**Q3: How do I make ultimate banana bread?** [factual-lookup]
*(expects URL containing: `ultimate-banana-bread`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.810 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.802 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.791 |
| crawl4ai | miss | smittenkitchen.com/./recipes/fruit/bananas/?format | 0.615 | smittenkitchen.com/about/faq/ | 0.574 | smittenkitchen.com/about/faq/ | 0.548 |
| crawl4ai-raw | miss | smittenkitchen.com/./recipes/fruit/bananas/?format | 0.615 | smittenkitchen.com/about/faq/ | 0.574 | smittenkitchen.com/about/faq/ | 0.548 |
| scrapy+md | #1 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.804 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.803 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.798 |
| crawlee | #1 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.804 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.796 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.795 |
| colly+md | #1 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.804 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.803 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.798 |
| playwright | miss | smittenkitchen.com/about/faq/ | 0.590 | smittenkitchen.com/events/ | 0.578 | smittenkitchen.com/about/faq/ | 0.553 |


**Q4: What's the skillet-baked macaroni and cheese recipe?** [factual-lookup]
*(expects URL containing: `skillet-baked-macaroni-and-cheese`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2014/04/dark-chocolate-coconut- | 0.675 | smittenkitchen.com/2015/01/mushroom-marsala-pasta- | 0.666 | smittenkitchen.com/2012/03/raspberry-coconut-macar | 0.663 |
| crawl4ai | miss | smittenkitchen.com/./recipes/ingredient/cheese/?fo | 0.607 | smittenkitchen.com/ | 0.607 | smittenkitchen.com/about/faq/ | 0.595 |
| crawl4ai-raw | miss | smittenkitchen.com/./recipes/ingredient/cheese/?fo | 0.607 | smittenkitchen.com/ | 0.607 | smittenkitchen.com/about/faq/ | 0.595 |
| scrapy+md | miss | smittenkitchen.com/2012/02/lasagna-bolognese/ | 0.646 | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.646 | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.646 |
| crawlee | miss | smittenkitchen.com/?random&timestamp=1777919490717 | 0.643 | smittenkitchen.com/2025/05/one-pan-ditalini-and-pe | 0.635 | smittenkitchen.com/2018/05/pasta-salad-with-roaste | 0.632 |
| colly+md | miss | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.636 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.636 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.632 |
| playwright | miss | smittenkitchen.com/subscribe/ | 0.610 | smittenkitchen.com/?random&timestamp=1777948695303 | 0.605 | smittenkitchen.com/ | 0.600 |


**Q5: What vegan recipes are available on Smitten Kitchen?** [cross-page]
*(expects URL containing: `diet/vegan`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.685 | smittenkitchen.com/2019/08/black-pepper-tofu-and-e | 0.684 | smittenkitchen.com/subscribe/ | 0.676 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/diet/vegan/?format=ph | 0.753 | smittenkitchen.com/./recipes/ingredient/tofu/?form | 0.750 | smittenkitchen.com/./recipes/diet/vegetarian/?form | 0.738 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/diet/vegan/?format=ph | 0.753 | smittenkitchen.com/./recipes/ingredient/tofu/?form | 0.750 | smittenkitchen.com/./recipes/diet/vegetarian/?form | 0.738 |
| scrapy+md | miss | smittenkitchen.com/2017/09/pizza-beans/ | 0.715 | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.715 | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.714 |
| crawlee | miss | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.697 | smittenkitchen.com/subscribe/ | 0.693 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.690 |
| colly+md | miss | smittenkitchen.com/2015/04/obsessively-good-avocad | 0.712 | smittenkitchen.com/recipes/ | 0.704 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.704 |
| playwright | #49 | smittenkitchen.com/recipes | 0.704 | smittenkitchen.com/recipes/ | 0.704 | smittenkitchen.com/subscribe/ | 0.693 |


**Q6: Show me cookie recipes** [cross-page]
*(expects URL containing: `sweets/cookie`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2007/12/peanut-butter-cookies/ | 0.753 | smittenkitchen.com/2019/12/unfussy-sugar-cookies/ | 0.744 | smittenkitchen.com/2019/12/unfussy-sugar-cookies/ | 0.742 |
| crawl4ai | #2 | smittenkitchen.com/about/faq/ | 0.691 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.675 | smittenkitchen.com/about/faq/ | 0.661 |
| crawl4ai-raw | #2 | smittenkitchen.com/about/faq/ | 0.691 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.675 | smittenkitchen.com/about/faq/ | 0.661 |
| scrapy+md | miss | smittenkitchen.com/2012/08/mediterranean-baked-fet | 0.675 | smittenkitchen.com/2015/02/pecan-sticky-buns-news/ | 0.663 | smittenkitchen.com/recipes/ | 0.660 |
| crawlee | miss | smittenkitchen.com/?random&timestamp=1777919490717 | 0.696 | smittenkitchen.com/?random&timestamp=1777919490717 | 0.687 | smittenkitchen.com/?random&timestamp=1777919490717 | 0.686 |
| colly+md | #9 | smittenkitchen.com/about/faq/ | 0.676 | smittenkitchen.com/subscribe/ | 0.672 | smittenkitchen.com/subscribe/ | 0.669 |
| playwright | #10 | smittenkitchen.com/about/faq/ | 0.676 | smittenkitchen.com/subscribe/ | 0.672 | smittenkitchen.com/subscribe/ | 0.669 |


**Q7: How do you make pumpkin basque cheesecake?** [factual-lookup]
*(expects URL containing: `pumpkin-basque-cheesecake`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2025/11/pumpkin-basque-cheeseca | 0.870 | smittenkitchen.com/2025/11/pumpkin-basque-cheeseca | 0.824 | smittenkitchen.com/2025/11/pumpkin-basque-cheeseca | 0.820 |
| crawl4ai | miss | smittenkitchen.com/ | 0.628 | smittenkitchen.com/./recipes/sweets/cake/?format=p | 0.609 | smittenkitchen.com/about/faq/ | 0.581 |
| crawl4ai-raw | miss | smittenkitchen.com/ | 0.628 | smittenkitchen.com/./recipes/sweets/cake/?format=p | 0.609 | smittenkitchen.com/about/faq/ | 0.581 |
| scrapy+md | miss | smittenkitchen.com/2006/11/chocolate-chip-sour-cre | 0.654 | smittenkitchen.com/2006/11/chocolate-chip-sour-cre | 0.638 | smittenkitchen.com/2012/08/mediterranean-baked-fet | 0.603 |
| crawlee | miss | smittenkitchen.com/2022/04/lemon-cream-meringues/ | 0.613 | smittenkitchen.com/2008/04/lemon-yogurt-anything-c | 0.612 | smittenkitchen.com/2008/04/lemon-yogurt-anything-c | 0.605 |
| colly+md | miss | smittenkitchen.com/2025/12/winter-cabbage-salad-wi | 0.616 | smittenkitchen.com/2022/04/lemon-cream-meringues/ | 0.613 | smittenkitchen.com/events/ | 0.604 |
| playwright | miss | smittenkitchen.com/events/ | 0.604 | smittenkitchen.com/recipes/sweets/cake/?format=pho | 0.577 | smittenkitchen.com/about/faq/ | 0.559 |


**Q8: What recipes are good for winter?** [cross-page]
*(expects URL containing: `season/winter`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #14 | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.686 | smittenkitchen.com/2013/01/lentil-soup-with-sausag | 0.657 | smittenkitchen.com/2016/09/baked-alaska-smitten-ki | 0.656 |
| crawl4ai | #2 | smittenkitchen.com/ | 0.668 | smittenkitchen.com/./recipes/season/winter/?format | 0.652 | smittenkitchen.com/ | 0.622 |
| crawl4ai-raw | #2 | smittenkitchen.com/ | 0.668 | smittenkitchen.com/./recipes/season/winter/?format | 0.652 | smittenkitchen.com/ | 0.622 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.646 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.636 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.636 |
| crawlee | miss | smittenkitchen.com/ | 0.646 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.641 | smittenkitchen.com/ | 0.640 |
| colly+md | #1 | smittenkitchen.com/2025/12/winter-cabbage-salad-wi | 0.645 | smittenkitchen.com/ | 0.642 | smittenkitchen.com/2020/04/how-i-stock-the-smitten | 0.641 |
| playwright | #7 | smittenkitchen.com/ | 0.641 | smittenkitchen.com/ | 0.640 | smittenkitchen.com/recipes | 0.626 |


</details>

## ikea

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| playwright | 38% (3/8) | 38% (3/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 0.400 | 3308 | 200 |
| crawlee | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 4610 | 203 |
| crawl4ai | 25% (2/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.292 | 1622 | 200 |
| crawl4ai-raw | 25% (2/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.292 | 1554 | 200 |
| scrapy+md | 25% (2/8) | 25% (2/8) | 25% (2/8) | 25% (2/8) | 25% (2/8) | 0.250 | 1107 | 194 |
| colly+md | 12% (1/8) | 25% (2/8) | 25% (2/8) | 25% (2/8) | 38% (3/8) | 0.198 | 2942 | 200 |
| markcrawl | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0% (0/8) | 12% (1/8) | 0.007 | 928 | 200 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for ikea</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How much does the MALM bed frame cost at IKEA?** [factual-lookup]
*(expects URL containing: `malm-bed-frame`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/rooms/bedroom/ | 0.700 | www.ikea.com/us/en/rooms/bedroom/ | 0.693 | www.ikea.com/us/en/p/stockholm-mirror-walnut-venee | 0.692 |
| crawl4ai | miss | www.ikea.com/us/en/p/malm-high-bed-frame-2-storage | 0.767 | www.ikea.com/us/en/p/malm-high-bed-frame-2-storage | 0.760 | www.ikea.com/us/en/rooms/bedroom/how-to/teenage-be | 0.742 |
| crawl4ai-raw | miss | www.ikea.com/us/en/rooms/bedroom/how-to/teenage-be | 0.742 | www.ikea.com/us/en/cat/beds-bm003/ | 0.737 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.736 |
| scrapy+md | miss | www.ikea.com/us/en/cat/hemnes-bedroom-series-58619 | 0.678 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.666 | www.ikea.com/us/en/cat/picture-photo-frames-18746/ | 0.666 |
| crawlee | miss | www.ikea.com/us/en/p/malm-high-bed-frame-2-storage | 0.797 | www.ikea.com/us/en/p/malm-high-bed-frame-2-storage | 0.754 | www.ikea.com/us/en/cat/beds-bm003/ | 0.751 |
| colly+md | miss | www.ikea.com/us/en/cat/beds-bm003/ | 0.784 | www.ikea.com/us/en/cat/beds-with-mattresses-includ | 0.763 | www.ikea.com/us/en/cat/beds-bm003/ | 0.748 |
| playwright | miss | www.ikea.com/us/en/cat/beds-bm003/ | 0.763 | www.ikea.com/us/en/cat/beds-bm003/ | 0.747 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.736 |


**Q2: What's the price of the SLATTUM upholstered bed frame?** [factual-lookup]
*(expects URL containing: `slattum-upholstered-bed`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/rooms/bedroom/ | 0.686 | www.ikea.com/us/en/p/inndyr-storage-bench-nordvall | 0.651 | www.ikea.com/us/en/p/inndyr-storage-bench-nordvall | 0.646 |
| crawl4ai | miss | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.740 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.731 | www.ikea.com/us/en/p/malm-high-bed-frame-2-storage | 0.718 |
| crawl4ai-raw | miss | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.740 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.731 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.709 |
| scrapy+md | miss | www.ikea.com/us/en/cat/hemnes-bedroom-series-58619 | 0.684 | www.ikea.com/us/en/cat/picture-photo-frames-18746/ | 0.666 | www.ikea.com/us/en/cat/picture-photo-frames-18746/ | 0.659 |
| crawlee | miss | www.ikea.com/us/en/rooms/bedroom/ | 0.757 | www.ikea.com/us/en/cat/beds-bm003/ | 0.744 | www.ikea.com/us/en/cat/beds-bm003/ | 0.732 |
| colly+md | miss | www.ikea.com/us/en/cat/bed-slats-24827/ | 0.771 | www.ikea.com/us/en/cat/beds-bm003/ | 0.763 | www.ikea.com/us/en/cat/beds-bm003/ | 0.744 |
| playwright | miss | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.777 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.746 | www.ikea.com/us/en/cat/beds-bm003/ | 0.728 |


**Q3: Tell me about the HEMNES 8-drawer dresser** [factual-lookup]
*(expects URL containing: `hemnes-8-drawer-dresser`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #17 | www.ikea.com/us/en/ | 0.730 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.725 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.725 |
| crawl4ai | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.810 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.776 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.763 |
| crawl4ai-raw | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.840 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.802 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.763 |
| scrapy+md | #1 | www.ikea.com/us/en/cat/hemnes-bedroom-series-58619 | 0.804 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.798 | www.ikea.com/us/en/cat/patar-series-36839/ | 0.784 |
| crawlee | miss | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.798 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.773 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.773 |
| colly+md | miss | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.798 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.773 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.773 |
| playwright | #5 | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.798 | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.772 | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.756 |


**Q4: What's the price of the RAST 3-drawer dresser?** [factual-lookup]
*(expects URL containing: `rast-3-drawer-dresser`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.695 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.694 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.680 |
| crawl4ai | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.759 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.758 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.745 |
| crawl4ai-raw | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.748 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.743 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.741 |
| scrapy+md | miss | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.753 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.731 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.723 |
| crawlee | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.757 | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.748 | www.ikea.com/us/en/cat/gullaberg-series-700613/ | 0.748 |
| colly+md | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.753 | www.ikea.com/us/en/cat/gullaberg-series-700613/ | 0.749 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.743 |
| playwright | miss | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.717 | www.ikea.com/us/en/ | 0.713 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.694 |


**Q5: What bed frames does IKEA sell?** [cross-page]
*(expects URL containing: `cat/beds`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/customer-service/product-suppor | 0.716 | www.ikea.com/us/en/ | 0.697 | www.ikea.com/us/en/rooms/bedroom/ | 0.695 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.748 | www.ikea.com/us/en/cat/beds-bm003/ | 0.741 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.740 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/beds-bm003/ | 0.752 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.748 | www.ikea.com/us/en/cat/beds-bm003/ | 0.741 |
| scrapy+md | miss | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.717 | www.ikea.com/us/en/cat/patar-series-36839/ | 0.716 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.714 |
| crawlee | #1 | www.ikea.com/us/en/cat/beds-bm003/ | 0.812 | www.ikea.com/us/en/cat/beds-bm003/ | 0.769 | www.ikea.com/us/en/p/gladstad-upholstered-bed-4-st | 0.744 |
| colly+md | #1 | www.ikea.com/us/en/cat/beds-bm003/ | 0.774 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.766 | www.ikea.com/us/en/cat/beds-with-mattresses-includ | 0.760 |
| playwright | #1 | www.ikea.com/us/en/cat/beds-bm003/ | 0.812 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.775 | www.ikea.com/us/en/cat/beds-bm003/ | 0.769 |


**Q6: Show me IKEA's sofa and armchair selection** [cross-page]
*(expects URL containing: `cat/sofas-armchairs`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/rooms/living-room/ | 0.829 | www.ikea.com/us/en/rooms/living-room/ | 0.795 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.790 |
| crawl4ai | #3 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.810 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.809 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.808 |
| crawl4ai-raw | #3 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.810 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.809 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.808 |
| scrapy+md | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.762 | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.759 | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.758 |
| crawlee | #1 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.869 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.813 | www.ikea.com/us/en/rooms/living-room/ | 0.805 |
| colly+md | #2 | www.ikea.com/us/en/rooms/living-room/ | 0.828 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.814 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.813 |
| playwright | #1 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.869 | www.ikea.com/us/en/rooms/living-room/ | 0.828 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.811 |


**Q7: What dressers and storage drawers does IKEA offer?** [cross-page]
*(expects URL containing: `cat/dressers-storage-drawers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.798 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.786 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.786 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.807 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.804 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.798 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.807 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.804 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.798 |
| scrapy+md | miss | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.794 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.791 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.787 |
| crawlee | #1 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.881 | www.ikea.com/us/en/rooms/bedroom/how-to/5-tidy-tip | 0.810 | www.ikea.com/us/en/cat/armoires-wardrobes-19053/ | 0.804 |
| colly+md | #12 | www.ikea.com/us/en/p/knarrevik-nightstand-black-20 | 0.827 | www.ikea.com/us/en/p/storklinta-nightstand-gray-gr | 0.817 | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.794 |
| playwright | #1 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.881 | www.ikea.com/us/en/cat/armoires-wardrobes-19053/ | 0.804 | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.794 |


**Q8: How much is the STOREMOLLA 8-drawer dresser at IKEA?** [factual-lookup]
*(expects URL containing: `storemolla-8-drawer-dresser`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/furniture-fu001/ | 0.753 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.746 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.735 |
| crawl4ai | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.789 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.773 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.763 |
| crawl4ai-raw | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.798 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.780 | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.769 |
| scrapy+md | #1 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.859 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.795 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.783 |
| crawlee | miss | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.771 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.766 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.760 |
| colly+md | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.768 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.765 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.760 |
| playwright | miss | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.756 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.746 | www.ikea.com/us/en/cat/backsplashes-wall-panels-19 | 0.741 |


</details>

## newegg

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| colly+md | 12% (1/8) | 12% (1/8) | 25% (2/8) | 25% (2/8) | 38% (3/8) | 0.163 | 6574 | 165 |
| crawl4ai | 0% (0/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.062 | 5857 | 200 |
| crawl4ai-raw | 0% (0/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.062 | 5856 | 200 |
| playwright | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0.003 | 1195 | 200 |
| markcrawl | — | — | — | — | — | — | — | — |
| scrapy+md | — | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — | — |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for newegg</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What graphics cards are available at Newegg?** [cross-page]
*(expects URL containing: `GPUs-Video-Graphics-Cards`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #2 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.818 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.785 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.782 |
| crawl4ai-raw | #2 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.818 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.785 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.782 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #1 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.802 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.802 | www.newegg.com/ | 0.771 |
| playwright | miss | www.newegg.com/ | 0.771 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.704 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.704 |


**Q2: What laptops does Newegg sell?** [cross-page]
*(expects URL containing: `Laptops-Notebooks`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | miss | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.766 | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.754 | www.newegg.com/All-in-One-Computer/SubCategory/ID- | 0.750 |
| crawl4ai-raw | miss | www.newegg.com/Desktop-Computer/SubCategory/ID-10 | 0.766 | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.754 | www.newegg.com/All-in-One-Computer/SubCategory/ID- | 0.750 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #4 | www.newegg.com/Laptop-Notebook/Category/ID-223 | 0.799 | www.newegg.com/d/Best-Sellers/All-Laptop/s/ID-32 | 0.794 | www.newegg.com/d/Best-Sellers/Laptop-Notebook/c/ID | 0.792 |
| playwright | #41 | www.newegg.com/ | 0.757 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.686 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.686 |


**Q3: How much does the AMD Ryzen 7 9800X3D CPU cost?** [factual-lookup]
*(expects URL containing: `ryzen-7-9800x3d`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | miss | www.newegg.com/insider/how-to-choose-the-best-desk | 0.746 | www.newegg.com/Desktop-CPU-Processor/SubCategory/I | 0.725 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.721 |
| crawl4ai-raw | miss | www.newegg.com/insider/how-to-choose-the-best-desk | 0.746 | www.newegg.com/Desktop-CPU-Processor/SubCategory/I | 0.725 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.720 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/p/pl?d=CPU&mid1=PageSEO | 0.768 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.762 | www.newegg.com/AMD-CPU-Free-Storage/EventSaleStore | 0.758 |
| playwright | miss | www.newegg.com/insider/how-to-choose-the-best-desk | 0.685 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.678 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.678 |


**Q4: What is the price of the Intel Core i9-14900K?** [factual-lookup]
*(expects URL containing: `i9-14900k`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | miss | www.newegg.com/Desktop-CPU-Processor/SubCategory/I | 0.748 | www.newegg.com/CPU-Processor/Category/ID-34 | 0.740 | www.newegg.com/Mobile-CPU-Processor/SubCategory/ID | 0.739 |
| crawl4ai-raw | miss | www.newegg.com/Desktop-CPU-Processor/SubCategory/I | 0.748 | www.newegg.com/CPU-Processor/Category/ID-34 | 0.740 | www.newegg.com/Mobile-CPU-Processor/SubCategory/ID | 0.739 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/p/pl?d=CPU&mid1=PageSEO | 0.767 | www.newegg.com/p/pl?d=CPU&mid1=PageSEO | 0.746 | www.newegg.com/d/Best-Sellers/CPU-Processor/c/ID-3 | 0.744 |
| playwright | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.688 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.688 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.683 |


**Q5: Tell me about the GIGABYTE GeForce RTX 5090 graphics card** [factual-lookup]
*(expects URL containing: `gv-n5090gaming`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | miss | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.787 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.779 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.755 |
| crawl4ai-raw | miss | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.787 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.779 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.755 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.785 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.785 | www.newegg.com/p/pl?N=100006740%2050001314 | 0.784 |
| playwright | miss | www.newegg.com/ | 0.708 | www.newegg.com/ | 0.678 | www.newegg.com/ | 0.673 |


**Q6: How much does the SAPPHIRE Radeon RX 9070 XT cost?** [factual-lookup]
*(expects URL containing: `radeon-rx-9070-xt`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | miss | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.770 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.734 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.732 |
| crawl4ai-raw | miss | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.770 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.734 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.732 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/best-sellers?cm/sp=Head/Navigatio | 0.762 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.755 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.755 |
| playwright | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.680 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.680 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.595 |


**Q7: What ASUS TUF gaming laptops are available on Newegg?** [factual-lookup]
*(expects URL containing: `asus-tuf-gaming`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | miss | www.newegg.com/Computer-Systems/Store/ID-3 | 0.750 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.705 | www.newegg.com/asus-nuc-configurator?cm_sp=hamburg | 0.700 |
| crawl4ai-raw | miss | www.newegg.com/Computer-Systems/Store/ID-3 | 0.751 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.705 | www.newegg.com/asus-nuc-configurator?cm_sp=hamburg | 0.700 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/best-sellers?cm/sp=Head/Navigatio | 0.771 | www.newegg.com/Gaming-Laptops/SubCategory/ID-3365? | 0.766 | www.newegg.com/d/best-sellers?cm/sp=Head/Navigatio | 0.762 |
| playwright | miss | www.newegg.com/asus-nuc-configurator?cm_sp=hamburg | 0.702 | www.newegg.com/ | 0.700 | www.newegg.com/asus-nuc-configurator?cm_sp=hamburg | 0.694 |


**Q8: What electronics categories does Newegg offer?** [cross-page]
*(expects URL containing: `Electronics/Store`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | miss | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.760 | www.newegg.com/RCA-Cables/SubCategory/ID-2831 | 0.724 | www.newegg.com/server-system-configurator/ | 0.720 |
| crawl4ai-raw | miss | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.760 | www.newegg.com/RCA-Cables/SubCategory/ID-2831 | 0.724 | www.newegg.com/server-system-configurator | 0.720 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #19 | www.newegg.com/ | 0.778 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.760 | www.newegg.com/corporate/about | 0.748 |
| playwright | miss | www.newegg.com/ | 0.778 | www.newegg.com/ | 0.712 | www.newegg.com/ | 0.683 |


</details>

## propublica

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 50% (3/6) | 67% (4/6) | 67% (4/6) | 67% (4/6) | 67% (4/6) | 0.556 | 1264 | 150 |
| crawl4ai | 33% (2/6) | 33% (2/6) | 33% (2/6) | 50% (3/6) | 67% (4/6) | 0.383 | 1563 | 149 |
| crawl4ai-raw | 33% (2/6) | 33% (2/6) | 33% (2/6) | 50% (3/6) | 67% (4/6) | 0.383 | 1563 | 149 |
| crawlee | 33% (2/6) | 33% (2/6) | 33% (2/6) | 33% (2/6) | 33% (2/6) | 0.348 | 2099 | 150 |
| playwright | 33% (2/6) | 33% (2/6) | 33% (2/6) | 33% (2/6) | 50% (3/6) | 0.348 | 2197 | 150 |
| colly+md | 17% (1/6) | 17% (1/6) | 33% (2/6) | 67% (4/6) | 67% (4/6) | 0.253 | 2196 | 150 |
| scrapy+md | 17% (1/6) | 17% (1/6) | 17% (1/6) | 17% (1/6) | 33% (2/6) | 0.179 | 1396 | 146 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for propublica</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What ProPublica investigations cover criminal justice?** [cross-page]
*(expects URL containing: `criminal-justice`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-investigatio | 0.633 | www.propublica.org/article/propublica-investigativ | 0.617 | www.propublica.org/article/why-local-state-police- | 0.614 |
| crawl4ai | #47 | www.propublica.org/about | 0.674 | www.propublica.org/ | 0.674 | www.propublica.org | 0.674 |
| crawl4ai-raw | #47 | www.propublica.org/about | 0.674 | www.propublica.org/ | 0.674 | www.propublica.org | 0.674 |
| scrapy+md | miss | www.propublica.org/tips/ | 0.678 | www.propublica.org/getinvolved/send-propublica-sto | 0.650 | www.propublica.org/ | 0.632 |
| crawlee | #24 | www.propublica.org/about | 0.675 | www.propublica.org/impact | 0.646 | www.propublica.org/series/busted | 0.640 |
| colly+md | miss | www.propublica.org/ | 0.670 | www.propublica.org/article/la-inspector-general-lo | 0.656 | www.propublica.org/article/historic-preservation-e | 0.639 |
| playwright | #26 | www.propublica.org/about | 0.675 | www.propublica.org/impact | 0.646 | www.propublica.org/series/busted | 0.640 |


**Q2: What is ProPublica reporting about healthcare?** [cross-page]
*(expects URL containing: `health`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.propublica.org/article/averhealth-drug-testing | 0.704 | www.propublica.org/article/rx-inspector-reshaping- | 0.689 | www.propublica.org/article/averhealth-drug-testing | 0.651 |
| crawl4ai | #14 | www.propublica.org/article/propublica-and-the-conn | 0.685 | www.propublica.org/about | 0.682 | www.propublica.org/datastore | 0.679 |
| crawl4ai-raw | #14 | www.propublica.org/article/propublica-and-the-conn | 0.685 | www.propublica.org/about | 0.682 | www.propublica.org/datastore | 0.679 |
| scrapy+md | #14 | www.propublica.org/legal | 0.675 | www.propublica.org/reports/page/2 | 0.674 | www.propublica.org/getinvolved/send-propublica-sto | 0.672 |
| crawlee | miss | www.propublica.org/getinvolved | 0.692 | www.propublica.org/about | 0.684 | www.propublica.org/impact | 0.677 |
| colly+md | #7 | www.propublica.org/article/propublica-files-lawsui | 0.707 | projects.propublica.org/datastore/ | 0.685 | www.propublica.org/article/propublica-files-lawsui | 0.684 |
| playwright | miss | www.propublica.org/getinvolved | 0.692 | www.propublica.org/about | 0.684 | www.propublica.org/datastore | 0.684 |


**Q3: What ProPublica articles discuss politics and government accountability?** [cross-page]
*(expects URL containing: `politics`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-reaching-out | 0.677 | www.propublica.org/article/propublica-most-read-st | 0.663 | www.propublica.org/article/propublica-most-read-st | 0.661 |
| crawl4ai | #26 | www.propublica.org/about | 0.729 | www.propublica.org/atpropublica/propublica-selects | 0.729 | www.propublica.org/article/second-trump-presidency | 0.708 |
| crawl4ai-raw | #26 | www.propublica.org/about | 0.729 | www.propublica.org/atpropublica/propublica-selects | 0.729 | www.propublica.org/article/second-trump-presidency | 0.708 |
| scrapy+md | miss | www.propublica.org/getinvolved/send-propublica-sto | 0.721 | www.propublica.org/ | 0.705 | www.propublica.org/tips/ | 0.699 |
| crawlee | miss | www.propublica.org/about | 0.727 | www.propublica.org/article/second-trump-presidency | 0.708 | www.propublica.org/local-initiatives | 0.708 |
| colly+md | miss | www.propublica.org/ | 0.705 | www.propublica.org/people/brooke-stephenson | 0.702 | www.propublica.org/tips/#postalmail | 0.700 |
| playwright | miss | www.propublica.org/about | 0.727 | www.propublica.org/article/second-trump-presidency | 0.708 | www.propublica.org/local-initiatives | 0.708 |


**Q4: What environmental or climate investigations does ProPublica have?** [cross-page]
*(expects URL containing: `climate`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.propublica.org/article/federal-judicial-center | 0.647 | www.propublica.org/article/climate-change-alec-leo | 0.628 | www.propublica.org/article/climate-change-alec-leo | 0.611 |
| crawl4ai | #1 | www.propublica.org/article/climate-science-oil-gas | 0.681 | www.propublica.org/nerds | 0.680 | www.propublica.org/people/abrahm-lustgarten | 0.679 |
| crawl4ai-raw | #1 | www.propublica.org/article/climate-science-oil-gas | 0.681 | www.propublica.org/nerds | 0.680 | www.propublica.org/people/abrahm-lustgarten | 0.679 |
| scrapy+md | miss | www.propublica.org/tips/ | 0.657 | www.propublica.org/topics/environment | 0.650 | www.propublica.org/topics/environment | 0.641 |
| crawlee | #1 | www.propublica.org/article/climate-science-oil-gas | 0.673 | www.propublica.org/atpropublica/propublica-selects | 0.660 | www.propublica.org/article/second-trump-presidency | 0.656 |
| colly+md | #8 | www.propublica.org/people/abrahm-lustgarten | 0.675 | www.propublica.org/people/abrahm-lustgarten/page/3 | 0.675 | job-boards.greenhouse.io/propublica | 0.658 |
| playwright | #1 | www.propublica.org/article/climate-science-oil-gas | 0.673 | www.propublica.org/atpropublica/propublica-selects | 0.660 | www.propublica.org/jobs | 0.658 |


**Q5: What ProPublica stories cover immigration?** [cross-page]
*(expects URL containing: `immigration`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | www.propublica.org/article/habeas-petitions-immigr | 0.743 | www.propublica.org/article/ice-dilley-ninos-cartas | 0.732 | www.propublica.org/article/american-kids-detained- | 0.726 |
| crawl4ai | #6 | www.propublica.org/people/melissa-sanchez | 0.774 | www.propublica.org/article/second-trump-presidency | 0.750 | www.propublica.org/article/second-trump-presidency | 0.713 |
| crawl4ai-raw | #6 | www.propublica.org/people/melissa-sanchez | 0.774 | www.propublica.org/article/second-trump-presidency | 0.750 | www.propublica.org/article/second-trump-presidency | 0.713 |
| scrapy+md | miss | www.propublica.org/ | 0.707 | www.propublica.org/article/propublica-emerging-rep | 0.706 | www.propublica.org/people/sarahbeth-maney | 0.705 |
| crawlee | #21 | www.propublica.org/people/sarahbeth-maney | 0.734 | www.propublica.org/people/gabriel-sandoval | 0.733 | www.propublica.org/people/melissa-sanchez | 0.732 |
| colly+md | #4 | www.propublica.org/people/perla-trevizo | 0.736 | www.propublica.org/article/propublica-and-the-conn | 0.719 | www.propublica.org/article/historic-preservation-e | 0.713 |
| playwright | #20 | www.propublica.org/people/sarahbeth-maney | 0.734 | www.propublica.org/people/melissa-sanchez | 0.732 | www.propublica.org/article/second-trump-presidency | 0.727 |


**Q6: What is the main ProPublica homepage with featured stories?** [cross-page]
*(expects URL containing: `propublica.org/`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.propublica.org/article/propublica-most-read-st | 0.655 | www.propublica.org/article/propublica-investigatio | 0.648 | www.propublica.org/article/propublica-most-read-st | 0.646 |
| crawl4ai | #1 | www.propublica.org/about | 0.703 | www.propublica.org/steal-our-stories | 0.684 | www.propublica.org/advertising | 0.682 |
| crawl4ai-raw | #1 | www.propublica.org/about | 0.703 | www.propublica.org/steal-our-stories | 0.684 | www.propublica.org/advertising | 0.682 |
| scrapy+md | #1 | www.propublica.org/ | 0.704 | www.propublica.org/getinvolved/send-propublica-sto | 0.703 | www.propublica.org/getinvolved/send-propublica-sto | 0.695 |
| crawlee | #1 | www.propublica.org/ | 0.704 | www.propublica.org/about | 0.704 | www.propublica.org/newsletters | 0.695 |
| colly+md | #1 | www.propublica.org/ | 0.704 | www.propublica.org/newsletters | 0.687 | projects.propublica.org/datastore/ | 0.686 |
| playwright | #1 | www.propublica.org/ | 0.704 | www.propublica.org/about | 0.704 | www.propublica.org/newsletters | 0.691 |


</details>

## Methodology

- **Queries:** 104 across 11 sites, categorized by type (api-function, code-example, conceptual, structured-data, factual-lookup, cross-page, navigation, js-rendered)
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

