# Retrieval Quality Comparison
<!-- style: v2, 2026-05-05 -->

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

**104 queries** across 11 sites.
Hit rate = correct source page in top-K results. Higher is better.
Summary tables use the **88-query common subset** (9 sites) so all tools are compared on identical queries. Sites excluded: huggingface-transformers, newegg (not all tools have data). Per-site tables show full results.

## Quick summary: best retrieval mode per tool

For each tool, the mode with the highest MRR. Most readers can stop here.

| Tool | Best mode | Hit@10 | MRR |
|---|---|---|---|
| crawlee | embedding | 84% (74/88) ±8% | 0.686 |
| playwright | embedding | 84% (74/88) ±8% | 0.677 |
| crawl4ai | embedding | 78% (69/88) ±8% | 0.642 |
| crawl4ai-raw | embedding | 78% (69/88) ±8% | 0.640 |
| colly+md | embedding | 75% (66/88) ±9% | 0.594 |
| markcrawl | embedding | 62% (55/88) ±10% | 0.488 |
| scrapy+md | embedding | 47% (41/88) ±10% | 0.429 |

> **Column definitions:** **Best mode** = retrieval strategy that maximizes MRR for this tool. **Hit@10** = correct source page in top 10 results. **MRR** = Mean Reciprocal Rank (1/rank of correct result, averaged).

## Summary: retrieval modes compared

_Computed over 88 queries on 9 common sites (ikea, kubernetes-docs, mdn-css, postgres-docs, propublica, react-dev, rust-book, smittenkitchen, stripe-docs)._

| Tool | Mode | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR |
|---|---|---|---|---|---|---|---|
| crawlee | embedding | 59% (52/88) ±10% | 75% (66/88) ±9% | 81% (71/88) ±8% | 84% (74/88) ±8% | 85% (75/88) ±7% | 0.686 |
| playwright | embedding | 58% (51/88) ±10% | 74% (65/88) ±9% | 81% (71/88) ±8% | 84% (74/88) ±8% | 84% (74/88) ±8% | 0.677 |
| crawl4ai | embedding | 56% (49/88) ±10% | 72% (63/88) ±9% | 76% (67/88) ±9% | 78% (69/88) ±8% | 82% (72/88) ±8% | 0.642 |
| crawl4ai-raw | embedding | 56% (49/88) ±10% | 72% (63/88) ±9% | 76% (67/88) ±9% | 78% (69/88) ±8% | 82% (72/88) ±8% | 0.640 |
| colly+md | embedding | 51% (45/88) ±10% | 65% (57/88) ±10% | 72% (63/88) ±9% | 75% (66/88) ±9% | 76% (67/88) ±9% | 0.594 |
| markcrawl | embedding | 42% (37/88) ±10% | 52% (46/88) ±10% | 59% (52/88) ±10% | 62% (55/88) ±10% | 62% (55/88) ±10% | 0.488 |
| scrapy+md | embedding | 41% (36/88) ±10% | 44% (39/88) ±10% | 45% (40/88) ±10% | 47% (41/88) ±10% | 49% (43/88) ±10% | 0.429 |
| markcrawl | bm25 | 20% (18/88) ±8% | 32% (28/88) ±10% | 41% (36/88) ±10% | 51% (45/88) ±10% | 58% (51/88) ±10% | 0.300 |
| scrapy+md | bm25 | 25% (22/88) ±9% | 33% (29/88) ±10% | 35% (31/88) ±10% | 39% (34/88) ±10% | 44% (39/88) ±10% | 0.299 |
| crawlee | bm25 | 20% (18/88) ±8% | 30% (26/88) ±9% | 39% (34/88) ±10% | 53% (47/88) ±10% | 57% (50/88) ±10% | 0.291 |
| crawl4ai | bm25 | 19% (17/88) ±8% | 30% (26/88) ±9% | 40% (35/88) ±10% | 49% (43/88) ±10% | 55% (48/88) ±10% | 0.281 |
| crawl4ai-raw | bm25 | 18% (16/88) ±8% | 30% (26/88) ±9% | 39% (34/88) ±10% | 48% (42/88) ±10% | 55% (48/88) ±10% | 0.276 |
| playwright | bm25 | 18% (16/88) ±8% | 31% (27/88) ±9% | 38% (33/88) ±10% | 51% (45/88) ±10% | 56% (49/88) ±10% | 0.273 |
| colly+md | bm25 | 17% (15/88) ±8% | 27% (24/88) ±9% | 30% (26/88) ±9% | 42% (37/88) ±10% | 49% (43/88) ±10% | 0.243 |
| crawlee | hybrid | 47% (41/88) ±10% | 66% (58/88) ±10% | 73% (64/88) ±9% | 81% (71/88) ±8% | 85% (75/88) ±7% | 0.581 |
| crawl4ai | hybrid | 47% (41/88) ±10% | 61% (54/88) ±10% | 68% (60/88) ±10% | 77% (68/88) ±9% | 82% (72/88) ±8% | 0.561 |
| crawl4ai-raw | hybrid | 45% (40/88) ±10% | 61% (54/88) ±10% | 68% (60/88) ±10% | 77% (68/88) ±9% | 82% (72/88) ±8% | 0.556 |
| playwright | hybrid | 42% (37/88) ±10% | 65% (57/88) ±10% | 73% (64/88) ±9% | 81% (71/88) ±8% | 85% (75/88) ±7% | 0.553 |
| colly+md | hybrid | 42% (37/88) ±10% | 58% (51/88) ±10% | 60% (53/88) ±10% | 68% (60/88) ±10% | 75% (66/88) ±9% | 0.510 |
| markcrawl | hybrid | 34% (30/88) ±10% | 51% (45/88) ±10% | 55% (48/88) ±10% | 60% (53/88) ±10% | 64% (56/88) ±10% | 0.438 |
| scrapy+md | hybrid | 35% (31/88) ±10% | 41% (36/88) ±10% | 44% (39/88) ±10% | 48% (42/88) ±10% | 51% (45/88) ±10% | 0.395 |
| playwright | reranked | 44% (39/88) ±10% | 64% (56/88) ±10% | 70% (62/88) ±9% | 77% (68/88) ±9% | 83% (73/88) ±8% | 0.554 |
| crawlee | reranked | 41% (36/88) ±10% | 62% (55/88) ±10% | 70% (62/88) ±9% | 78% (69/88) ±8% | 82% (72/88) ±8% | 0.537 |
| crawl4ai-raw | reranked | 39% (34/88) ±10% | 62% (55/88) ±10% | 70% (62/88) ±9% | 76% (67/88) ±9% | 83% (73/88) ±8% | 0.520 |
| crawl4ai | reranked | 38% (33/88) ±10% | 62% (55/88) ±10% | 70% (62/88) ±9% | 77% (68/88) ±9% | 83% (73/88) ±8% | 0.512 |
| colly+md | reranked | 36% (32/88) ±10% | 59% (52/88) ±10% | 64% (56/88) ±10% | 68% (60/88) ±10% | 72% (63/88) ±9% | 0.488 |
| markcrawl | reranked | 38% (33/88) ±10% | 48% (42/88) ±10% | 57% (50/88) ±10% | 62% (55/88) ±10% | 62% (55/88) ±10% | 0.451 |
| scrapy+md | reranked | 31% (27/88) ±9% | 40% (35/88) ±10% | 44% (39/88) ±10% | 48% (42/88) ±10% | 49% (43/88) ±10% | 0.364 |

> **Column definitions:** **Hit@K** = percentage of queries where the correct source page appeared in the top K results (shown as % with raw counts). **MRR** (Mean Reciprocal Rank) = average of 1/rank for correct results (1.0 = always rank 1, 0.5 = always rank 2). **Mode** = retrieval strategy used (see definitions above).

## Summary: embedding-only (hit rate at multiple K values)

_Computed over 88 queries on 9 common sites._

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Avg words |
|---|---|---|---|---|---|---|---|---|
| crawlee | 59% (52/88) ±10% | 75% (66/88) ±9% | 81% (71/88) ±8% | 84% (74/88) ±8% | 85% (75/88) ±7% | 0.686 | 58912 | 382 |
| playwright | 58% (51/88) ±10% | 74% (65/88) ±9% | 81% (71/88) ±8% | 84% (74/88) ±8% | 84% (74/88) ±8% | 0.677 | 56855 | 382 |
| crawl4ai | 56% (49/88) ±10% | 72% (63/88) ±9% | 76% (67/88) ±9% | 78% (69/88) ±8% | 82% (72/88) ±8% | 0.642 | 24400 | 345 |
| crawl4ai-raw | 56% (49/88) ±10% | 72% (63/88) ±9% | 76% (67/88) ±9% | 78% (69/88) ±8% | 82% (72/88) ±8% | 0.640 | 25245 | 344 |
| colly+md | 51% (45/88) ±10% | 65% (57/88) ±10% | 72% (63/88) ±9% | 75% (66/88) ±9% | 76% (67/88) ±9% | 0.594 | 59078 | 385 |
| markcrawl | 42% (37/88) ±10% | 52% (46/88) ±10% | 59% (52/88) ±10% | 62% (55/88) ±10% | 62% (55/88) ±10% | 0.488 | 27193 | 334 |
| scrapy+md | 41% (36/88) ±10% | 44% (39/88) ±10% | 45% (40/88) ±10% | 47% (41/88) ±10% | 49% (43/88) ±10% | 0.429 | 46141 | 364 |

> **Column definitions:** **Hit@K** = correct source page in top K results. **MRR** = Mean Reciprocal Rank (1/rank of correct result, averaged). **Chunks** = total chunks produced by this tool (across all pages in common sites). **Avg words** = mean words per chunk.

## What this means

Tools span MRR 0.429-0.686 on embedding mode (a 0.257 spread). Tools crawl similar pages from the same seed URLs, and we apply identical chunking and embedding pipelines, but extraction differences -- see [content quality](QUALITY_COMPARISON.md) -- show up at retrieval time.

**Retrieval mode matters more than crawler choice.** Embedding search beats BM25 by roughly 2x on MRR across all tools. Hybrid and reranked modes fall between the two. Choosing the right retrieval strategy will improve your RAG pipeline far more than switching crawlers.

**The noise-vs-recall trade-off.** Noisier tools (crawlee, playwright) have slightly higher hit rates, but they produce 2x the chunks of leaner tools (markcrawl, scrapy+md). More chunks means higher embedding and storage costs with diminishing retrieval returns. See [COST_AT_SCALE.md](COST_AT_SCALE.md) for the dollar impact.

**For most use cases, pick your crawler based on speed and cost, not retrieval quality.** The differences here are within confidence intervals. Where crawler choice _does_ matter is content quality and downstream answer quality -- see [ANSWER_QUALITY.md](ANSWER_QUALITY.md).

## Per-category breakdown (embedding mode)

Query categories reveal where crawlers actually differ. Categories like `js-rendered` and `structured-data` stress-test browser rendering and table extraction, while `api-function` and `conceptual` queries test basic content retrieval.

| Category | Tool | Hit@10 | MRR | Queries |
|---|---|---|---|---|
| api-function | playwright | 89% (25/28) | 0.751 | 28 |
| api-function | crawlee | 89% (25/28) | 0.727 | 28 |
| api-function | colly+md | 86% (24/28) | 0.735 | 28 |
| api-function | crawl4ai-raw | 86% (24/28) | 0.696 | 28 |
| api-function | crawl4ai | 86% (24/28) | 0.696 | 28 |
| api-function | scrapy+md | 57% (16/28) | 0.521 | 28 |
| api-function | markcrawl | 50% (14/28) | 0.414 | 28 |
| code-example | scrapy+md | 100% (4/4) | 1.000 | 4 |
| code-example | crawl4ai | 100% (4/4) | 0.875 | 4 |
| code-example | crawl4ai-raw | 100% (4/4) | 0.875 | 4 |
| code-example | crawlee | 100% (4/4) | 0.750 | 4 |
| code-example | colly+md | 100% (4/4) | 0.750 | 4 |
| code-example | playwright | 100% (4/4) | 0.750 | 4 |
| code-example | markcrawl | 100% (4/4) | 0.631 | 4 |
| conceptual | crawlee | 100% (27/27) | 0.839 | 27 |
| conceptual | playwright | 100% (27/27) | 0.788 | 27 |
| conceptual | crawl4ai | 100% (27/27) | 0.777 | 27 |
| conceptual | crawl4ai-raw | 100% (27/27) | 0.777 | 27 |
| conceptual | markcrawl | 93% (25/27) | 0.759 | 27 |
| conceptual | colly+md | 74% (20/27) | 0.562 | 27 |
| conceptual | scrapy+md | 41% (11/27) | 0.285 | 27 |
| cross-page | playwright | 100% (14/14) | 0.806 | 14 |
| cross-page | crawlee | 100% (14/14) | 0.740 | 14 |
| cross-page | crawl4ai | 100% (14/14) | 0.676 | 14 |
| cross-page | crawl4ai-raw | 100% (14/14) | 0.664 | 14 |
| cross-page | colly+md | 93% (13/14) | 0.686 | 14 |
| cross-page | markcrawl | 57% (8/14) | 0.214 | 14 |
| cross-page | scrapy+md | 36% (5/14) | 0.291 | 14 |
| factual-lookup | markcrawl | 50% (5/10) | 0.433 | 10 |
| factual-lookup | scrapy+md | 40% (4/10) | 0.400 | 10 |
| factual-lookup | crawlee | 20% (2/10) | 0.200 | 10 |
| factual-lookup | colly+md | 20% (2/10) | 0.200 | 10 |
| factual-lookup | playwright | 10% (1/10) | 0.100 | 10 |
| factual-lookup | crawl4ai | 0% (0/10) | 0.000 | 10 |
| factual-lookup | crawl4ai-raw | 0% (0/10) | 0.000 | 10 |
| js-rendered | scrapy+md | 100% (5/5) | 0.678 | 5 |
| js-rendered | crawl4ai | 80% (4/5) | 0.614 | 5 |
| js-rendered | crawl4ai-raw | 80% (4/5) | 0.614 | 5 |
| js-rendered | crawlee | 80% (4/5) | 0.395 | 5 |
| js-rendered | playwright | 80% (4/5) | 0.395 | 5 |
| js-rendered | colly+md | 80% (4/5) | 0.380 | 5 |
| js-rendered | markcrawl | 20% (1/5) | 0.200 | 5 |


### Best tool per category

| Category | Best tool | Hit@10 | Spread |
|---|---|---|---|
| api-function | crawlee | 89% | 39% |
| code-example | markcrawl | 100% | 0% |
| conceptual | crawl4ai | 100% | 59% |
| cross-page | crawl4ai | 100% | 64% |
| factual-lookup | markcrawl | 50% | 50% |
| js-rendered | scrapy+md | 100% | 80% |

_Spread = difference between best and worst tool. High spread categories are where crawler choice matters most._


## react-dev

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| scrapy+md | 88% (14/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.898 | 1259 | 216 |
| crawl4ai | 81% (13/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.863 | 3210 | 500 |
| crawl4ai-raw | 81% (13/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.863 | 3210 | 500 |
| crawlee | 75% (12/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 100% (16/16) | 0.856 | 3063 | 217 |
| playwright | 62% (10/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.776 | 3067 | 221 |
| colly+md | 62% (10/16) | 88% (14/16) | 94% (15/16) | 100% (16/16) | 100% (16/16) | 0.762 | 5083 | 292 |
| markcrawl | 44% (7/16) | 50% (8/16) | 56% (9/16) | 56% (9/16) | 56% (9/16) | 0.484 | 419 | 51 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for react-dev</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do I manage state in a React component?** [conceptual]
*(expects URL containing: `state`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/reacting-to-input-with-state | 0.681 | react.dev/learn/managing-state | 0.667 | react.dev/learn/preserving-and-resetting-state | 0.651 |
| crawl4ai | #1 | he.react.dev/learn/managing-state | 0.680 | az.react.dev/learn/managing-state | 0.679 | de.react.dev/learn/managing-state | 0.678 |
| crawl4ai-raw | #1 | he.react.dev/learn/managing-state | 0.680 | az.react.dev/learn/managing-state | 0.678 | de.react.dev/learn/managing-state | 0.678 |
| scrapy+md | #1 | react.dev/learn/preserving-and-resetting-state | 0.679 | react.dev/learn/choosing-the-state-structure | 0.678 | react.dev/learn/managing-state | 0.674 |
| crawlee | #1 | react.dev/learn/reacting-to-input-with-state | 0.668 | react.dev/learn/state-a-components-memory | 0.647 | react.dev/learn/managing-state | 0.645 |
| colly+md | #1 | react.dev/learn/reacting-to-input-with-state | 0.672 | react.dev/learn/managing-state | 0.669 | react.dev/learn/state-a-components-memory | 0.647 |
| playwright | #1 | react.dev/learn/reacting-to-input-with-state | 0.672 | react.dev/learn/managing-state | 0.669 | react.dev/learn/state-a-components-memory | 0.647 |


**Q2: How does the useEffect hook work in React?** [api-function]
*(expects URL containing: `useEffect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/reusing-logic-with-custom-hooks | 0.606 | react.dev/learn/reusing-logic-with-custom-hooks | 0.588 | react.dev/learn/you-might-not-need-an-effect | 0.588 |
| crawl4ai | #1 | react.dev/reference/react/useEffect | 0.616 | react.dev/reference/react/useEffect | 0.615 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.610 |
| crawl4ai-raw | #1 | react.dev/reference/react/useEffect | 0.616 | react.dev/reference/react/useEffect | 0.615 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.610 |
| scrapy+md | #1 | react.dev/reference/react/useEffect | 0.630 | react.dev/reference/eslint-plugin-react-hooks/lint | 0.608 | react.dev/learn/reusing-logic-with-custom-hooks | 0.606 |
| crawlee | #1 | react.dev/reference/react/useEffect | 0.623 | react.dev/learn/reusing-logic-with-custom-hooks | 0.608 | react.dev/learn/reusing-logic-with-custom-hooks | 0.606 |
| colly+md | #1 | react.dev/reference/react/useEffect | 0.623 | react.dev/reference/react/useEffect#reference | 0.623 | react.dev/learn/reusing-logic-with-custom-hooks | 0.608 |
| playwright | #1 | react.dev/reference/react/useEffect | 0.623 | react.dev/learn/reusing-logic-with-custom-hooks | 0.608 | react.dev/learn/reusing-logic-with-custom-hooks | 0.606 |


**Q3: How do I create and use context in React?** [api-function]
*(expects URL containing: `useContext`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/passing-data-deeply-with-context | 0.685 | react.dev/learn/passing-data-deeply-with-context | 0.667 | react.dev/learn/passing-data-deeply-with-context | 0.651 |
| crawl4ai | #1 | react.dev/reference/react/createContext | 0.737 | react.dev/learn/passing-data-deeply-with-context | 0.719 | react.dev/reference/react/createContext | 0.718 |
| crawl4ai-raw | #1 | react.dev/reference/react/createContext | 0.737 | react.dev/learn/passing-data-deeply-with-context | 0.719 | react.dev/reference/react/createContext | 0.718 |
| scrapy+md | #1 | react.dev/reference/react/createContext | 0.710 | react.dev/learn/passing-data-deeply-with-context | 0.685 | react.dev/learn/passing-data-deeply-with-context | 0.672 |
| crawlee | #1 | react.dev/reference/react/createContext | 0.721 | react.dev/reference/react/createContext | 0.710 | react.dev/learn/passing-data-deeply-with-context | 0.701 |
| colly+md | #1 | react.dev/reference/react/createContext | 0.721 | react.dev/reference/react/createContext | 0.710 | react.dev/learn/passing-data-deeply-with-context#s | 0.701 |
| playwright | #1 | react.dev/reference/react/createContext | 0.721 | react.dev/reference/react/createContext | 0.710 | react.dev/learn/passing-data-deeply-with-context | 0.701 |


**Q4: What is JSX and how does React use it?** [conceptual]
*(expects URL containing: `writing-markup-with-jsx`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/writing-markup-with-jsx | 0.675 | react.dev/learn/writing-markup-with-jsx | 0.635 | react.dev/learn | 0.633 |
| crawl4ai | #1 | react.dev/learn/writing-markup-with-jsx | 0.685 | react.dev/learn/writing-markup-with-jsx | 0.661 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.647 |
| crawl4ai-raw | #1 | react.dev/learn/writing-markup-with-jsx | 0.685 | react.dev/learn/writing-markup-with-jsx | 0.661 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.647 |
| scrapy+md | #1 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.662 | react.dev/learn/writing-markup-with-jsx | 0.651 | react.dev/learn/writing-markup-with-jsx | 0.639 |
| crawlee | #1 | react.dev/learn/writing-markup-with-jsx | 0.725 | react.dev/learn/writing-markup-with-jsx | 0.663 | react.dev/learn/writing-markup-with-jsx | 0.656 |
| colly+md | #1 | react.dev/learn/writing-markup-with-jsx | 0.725 | react.dev/learn/writing-markup-with-jsx | 0.663 | react.dev/learn/writing-markup-with-jsx | 0.656 |
| playwright | #1 | react.dev/learn/writing-markup-with-jsx | 0.725 | react.dev/learn/writing-markup-with-jsx | 0.663 | react.dev/learn/writing-markup-with-jsx | 0.656 |


**Q5: How do I render lists and use keys in React?** [code-example]
*(expects URL containing: `rendering-lists`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/rendering-lists | 0.661 | react.dev/learn/tutorial-tic-tac-toe | 0.638 | react.dev/learn/rendering-lists | 0.627 |
| crawl4ai | #2 | react.dev/learn/tutorial-tic-tac-toe | 0.700 | react.dev/learn/rendering-lists | 0.694 | react.dev/learn/rendering-lists | 0.669 |
| crawl4ai-raw | #2 | react.dev/learn/tutorial-tic-tac-toe | 0.700 | react.dev/learn/rendering-lists | 0.694 | react.dev/learn/rendering-lists | 0.669 |
| scrapy+md | #1 | react.dev/learn/rendering-lists | 0.658 | react.dev/learn/rendering-lists | 0.649 | react.dev/learn/tutorial-tic-tac-toe | 0.638 |
| crawlee | #2 | react.dev/learn/tutorial-tic-tac-toe | 0.666 | react.dev/learn/rendering-lists | 0.658 | react.dev/learn/tutorial-tic-tac-toe | 0.638 |
| colly+md | #2 | react.dev/learn/tutorial-tic-tac-toe | 0.666 | react.dev/learn/rendering-lists | 0.658 | react.dev/learn/rendering-lists#keeping-list-items | 0.658 |
| playwright | #2 | react.dev/learn/tutorial-tic-tac-toe | 0.666 | react.dev/learn/rendering-lists | 0.657 | react.dev/learn/tutorial-tic-tac-toe | 0.638 |


**Q6: How do I use the useRef hook in React?** [api-function]
*(expects URL containing: `useRef`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/manipulating-the-dom-with-refs | 0.711 | react.dev/learn/referencing-values-with-refs | 0.634 | react.dev/learn/referencing-values-with-refs | 0.629 |
| crawl4ai | #1 | react.dev/reference/react/useRef | 0.666 | react.dev/learn/referencing-values-with-refs | 0.660 | react.dev/learn/referencing-values-with-refs | 0.657 |
| crawl4ai-raw | #1 | react.dev/reference/react/useRef | 0.666 | react.dev/learn/referencing-values-with-refs | 0.660 | react.dev/learn/referencing-values-with-refs | 0.657 |
| scrapy+md | #1 | react.dev/reference/react/useRef | 0.705 | react.dev/reference/react/useRef | 0.659 | react.dev/learn/referencing-values-with-refs | 0.639 |
| crawlee | #2 | react.dev/learn/manipulating-the-dom-with-refs | 0.673 | react.dev/reference/react/useRef | 0.667 | react.dev/reference/react/useRef | 0.661 |
| colly+md | #2 | react.dev/learn/manipulating-the-dom-with-refs | 0.673 | react.dev/reference/react/useRef#reference | 0.667 | react.dev/reference/react/useRef#returns | 0.667 |
| playwright | #2 | react.dev/learn/manipulating-the-dom-with-refs | 0.673 | react.dev/reference/react/useRef | 0.667 | react.dev/learn/manipulating-the-dom-with-refs | 0.661 |


**Q7: How do I pass props between React components?** [conceptual]
*(expects URL containing: `passing-props`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/passing-props-to-a-component | 0.634 | react.dev/learn/passing-data-deeply-with-context | 0.619 | react.dev/learn/passing-props-to-a-component | 0.598 |
| crawl4ai | #1 | react.dev/learn/passing-props-to-a-component | 0.698 | react.dev/learn/passing-data-deeply-with-context | 0.664 | react.dev/learn/passing-props-to-a-component | 0.659 |
| crawl4ai-raw | #1 | react.dev/learn/passing-props-to-a-component | 0.698 | react.dev/learn/passing-data-deeply-with-context | 0.664 | react.dev/learn/passing-props-to-a-component | 0.659 |
| scrapy+md | #1 | react.dev/learn/passing-props-to-a-component | 0.671 | react.dev/learn/passing-data-deeply-with-context | 0.622 | react.dev/learn/sharing-state-between-components | 0.598 |
| crawlee | #1 | react.dev/learn/passing-props-to-a-component | 0.683 | react.dev/learn/passing-data-deeply-with-context | 0.668 | react.dev/learn/passing-data-deeply-with-context | 0.643 |
| colly+md | #4 | react.dev/learn/passing-data-deeply-with-context#s | 0.668 | react.dev/learn/passing-data-deeply-with-context#s | 0.668 | react.dev/learn/passing-data-deeply-with-context | 0.668 |
| playwright | #2 | react.dev/learn/passing-data-deeply-with-context | 0.668 | react.dev/learn/passing-props-to-a-component | 0.667 | react.dev/learn/passing-data-deeply-with-context | 0.643 |


**Q8: How do I conditionally render content in React?** [code-example]
*(expects URL containing: `conditional-rendering`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | react.dev/learn/describing-the-ui | 0.595 | react.dev/learn/conditional-rendering | 0.595 | react.dev/learn/conditional-rendering | 0.561 |
| crawl4ai | #1 | react.dev/learn/conditional-rendering | 0.619 | de.react.dev/learn/describing-the-ui | 0.599 | react.dev/learn/conditional-rendering | 0.597 |
| crawl4ai-raw | #1 | react.dev/learn/conditional-rendering | 0.619 | de.react.dev/learn/describing-the-ui | 0.599 | react.dev/learn/conditional-rendering | 0.597 |
| scrapy+md | #1 | react.dev/learn/conditional-rendering | 0.621 | react.dev/learn/describing-the-ui | 0.595 | react.dev/learn/conditional-rendering | 0.559 |
| crawlee | #1 | react.dev/learn/conditional-rendering | 0.601 | react.dev/learn/describing-the-ui | 0.593 | react.dev/learn/conditional-rendering | 0.566 |
| colly+md | #1 | react.dev/learn/conditional-rendering | 0.627 | react.dev/learn/conditional-rendering | 0.567 | react.dev/learn/conditional-rendering | 0.566 |
| playwright | #1 | react.dev/learn/conditional-rendering | 0.629 | react.dev/learn/conditional-rendering | 0.567 | react.dev/learn/conditional-rendering | 0.566 |


**Q9: What is the useMemo hook for in React?** [api-function]
*(expects URL containing: `useMemo`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/typescript | 0.602 | react.dev/learn/you-might-not-need-an-effect | 0.602 | react.dev/learn/react-compiler/introduction | 0.541 |
| crawl4ai | #1 | react.dev/reference/react/useMemo | 0.666 | react.dev/reference/react/useMemo | 0.662 | react.dev/reference/react/useMemo | 0.651 |
| crawl4ai-raw | #1 | react.dev/reference/react/useMemo | 0.666 | react.dev/reference/react/useMemo | 0.662 | react.dev/reference/react/useMemo | 0.651 |
| scrapy+md | #1 | react.dev/reference/react/useMemo | 0.652 | react.dev/reference/react/useMemo | 0.617 | react.dev/reference/react/useMemo | 0.608 |
| crawlee | #1 | react.dev/reference/react/useMemo | 0.677 | react.dev/reference/react/useMemo | 0.648 | react.dev/reference/react/useMemo | 0.632 |
| colly+md | #1 | react.dev/reference/react/useMemo#how-to-tell-if-a | 0.677 | react.dev/reference/react/useMemo | 0.677 | react.dev/reference/react/useMemo | 0.648 |
| playwright | #1 | react.dev/reference/react/useMemo | 0.677 | react.dev/reference/react/useMemo | 0.648 | react.dev/reference/react/useMemo | 0.632 |


**Q10: How do I use the useState hook in React?** [api-function]
*(expects URL containing: `useState`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/state-a-components-memory | 0.654 | react.dev/learn | 0.648 | react.dev/learn/state-a-components-memory | 0.642 |
| crawl4ai | #9 | react.dev/learn/state-a-components-memory | 0.665 | react.dev/learn/state-a-components-memory | 0.663 | react.dev/learn/state-a-components-memory | 0.661 |
| crawl4ai-raw | #9 | react.dev/learn/state-a-components-memory | 0.665 | react.dev/learn/state-a-components-memory | 0.663 | react.dev/learn/state-a-components-memory | 0.661 |
| scrapy+md | #4 | react.dev/learn/state-a-components-memory | 0.653 | react.dev/learn | 0.648 | react.dev/learn | 0.648 |
| crawlee | #5 | react.dev/learn/state-a-components-memory | 0.653 | react.dev/learn | 0.648 | react.dev/learn/state-a-components-memory | 0.646 |
| colly+md | #2 | react.dev/learn/state-a-components-memory | 0.653 | react.dev/learn/state-a-components-memory#anatomy- | 0.653 | react.dev/learn | 0.648 |
| playwright | #6 | react.dev/learn/state-a-components-memory | 0.653 | react.dev/learn | 0.648 | react.dev/learn/state-a-components-memory | 0.646 |


**Q11: How do I use the useCallback hook in React?** [api-function]
*(expects URL containing: `useCallback`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/typescript | 0.636 | react.dev/learn/manipulating-the-dom-with-refs | 0.541 | react.dev/learn/reusing-logic-with-custom-hooks | 0.536 |
| crawl4ai | #1 | react.dev/reference/react/useCallback | 0.668 | react.dev/reference/react/useCallback | 0.643 | react.dev/reference/react/useCallback | 0.629 |
| crawl4ai-raw | #1 | react.dev/reference/react/useCallback | 0.668 | react.dev/reference/react/useCallback | 0.643 | react.dev/reference/react/useCallback | 0.629 |
| scrapy+md | #1 | react.dev/reference/react/useCallback | 0.639 | react.dev/learn/typescript | 0.634 | react.dev/reference/react/useCallback | 0.613 |
| crawlee | #1 | react.dev/reference/react/useCallback | 0.661 | react.dev/learn/typescript | 0.634 | react.dev/reference/react/useCallback | 0.629 |
| colly+md | #1 | react.dev/reference/react/useCallback | 0.661 | react.dev/learn/typescript#further-learning | 0.634 | react.dev/learn/typescript#example-hooks | 0.634 |
| playwright | #1 | react.dev/reference/react/useCallback | 0.661 | react.dev/learn/typescript | 0.634 | react.dev/reference/react/useCallback | 0.629 |


**Q12: How do I use the useReducer hook in React?** [api-function]
*(expects URL containing: `useReducer`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/typescript | 0.654 | react.dev/learn/extracting-state-logic-into-a-redu | 0.621 | react.dev/learn/extracting-state-logic-into-a-redu | 0.610 |
| crawl4ai | #1 | react.dev/reference/react/useReducer | 0.714 | react.dev/reference/react/useReducer | 0.699 | react.dev/reference/react/useReducer | 0.695 |
| crawl4ai-raw | #1 | react.dev/reference/react/useReducer | 0.714 | react.dev/reference/react/useReducer | 0.699 | react.dev/reference/react/useReducer | 0.695 |
| scrapy+md | #1 | react.dev/reference/react/useReducer | 0.695 | react.dev/reference/react/useReducer | 0.693 | react.dev/reference/react/useReducer | 0.663 |
| crawlee | #1 | react.dev/reference/react/useReducer | 0.723 | react.dev/reference/react/useReducer | 0.704 | react.dev/reference/react/useReducer | 0.684 |
| colly+md | #1 | react.dev/reference/react/useReducer | 0.723 | react.dev/reference/react/useReducer | 0.703 | react.dev/reference/react/useReducer | 0.684 |
| playwright | #1 | react.dev/reference/react/useReducer | 0.723 | react.dev/reference/react/useReducer | 0.703 | react.dev/reference/react/useReducer | 0.684 |


**Q13: How do I handle events like clicks in React?** [code-example]
*(expects URL containing: `responding-to-events`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/responding-to-events | 0.627 | react.dev/learn | 0.607 | react.dev/learn/responding-to-events | 0.590 |
| crawl4ai | #1 | react.dev/learn/responding-to-events | 0.658 | az.react.dev/learn | 0.624 | 18.react.dev/learn | 0.622 |
| crawl4ai-raw | #1 | react.dev/learn/responding-to-events | 0.658 | az.react.dev/learn | 0.624 | 18.react.dev/learn | 0.622 |
| scrapy+md | #1 | react.dev/learn/responding-to-events | 0.658 | react.dev/learn/adding-interactivity | 0.611 | react.dev/learn | 0.606 |
| crawlee | #1 | react.dev/learn/responding-to-events | 0.653 | react.dev/learn/responding-to-events | 0.598 | react.dev/learn/tutorial-tic-tac-toe | 0.590 |
| colly+md | #1 | react.dev/learn/responding-to-events | 0.631 | react.dev/learn/responding-to-events#passing-event | 0.631 | react.dev/learn/responding-to-events | 0.598 |
| playwright | #1 | react.dev/learn/responding-to-events | 0.631 | react.dev/learn/responding-to-events | 0.598 | react.dev/learn/tutorial-tic-tac-toe | 0.590 |


**Q14: What is the Suspense component in React?** [api-function]
*(expects URL containing: `Suspense`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | react.dev/learn/creating-a-react-app | 0.568 | react.dev/learn/synchronizing-with-effects | 0.537 | react.dev/learn/reacting-to-input-with-state | 0.533 |
| crawl4ai | #1 | react.dev/reference/react/Suspense | 0.693 | react.dev/reference/react/Suspense | 0.686 | react.dev/reference/react/Suspense | 0.673 |
| crawl4ai-raw | #1 | react.dev/reference/react/Suspense | 0.693 | react.dev/reference/react/Suspense | 0.686 | react.dev/reference/react/Suspense | 0.673 |
| scrapy+md | #1 | react.dev/reference/react/Suspense | 0.657 | react.dev/reference/react/Suspense | 0.656 | react.dev/reference/react/Suspense | 0.649 |
| crawlee | #1 | react.dev/reference/react/Suspense | 0.677 | react.dev/reference/react/Suspense | 0.647 | react.dev/reference/react/Activity | 0.647 |
| colly+md | #1 | react.dev/reference/react/Suspense | 0.677 | react.dev/reference/react/Suspense | 0.647 | react.dev/reference/react/Activity | 0.647 |
| playwright | #1 | react.dev/reference/react/Suspense | 0.677 | react.dev/reference/react/Suspense | 0.647 | react.dev/reference/react/Activity | 0.647 |


**Q15: How do I add interactivity to React components?** [conceptual]
*(expects URL containing: `adding-interactivity`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/adding-interactivity | 0.633 | react.dev/learn/responding-to-events | 0.606 | react.dev/learn/render-and-commit | 0.594 |
| crawl4ai | #1 | de.react.dev/learn/adding-interactivity | 0.683 | react.dev/learn/adding-interactivity | 0.675 | he.react.dev/learn/adding-interactivity | 0.663 |
| crawl4ai-raw | #1 | de.react.dev/learn/adding-interactivity | 0.683 | react.dev/learn/adding-interactivity | 0.675 | he.react.dev/learn/adding-interactivity | 0.663 |
| scrapy+md | #1 | react.dev/learn/adding-interactivity | 0.704 | react.dev/learn/responding-to-events | 0.675 | react.dev/learn/render-and-commit | 0.663 |
| crawlee | #1 | react.dev/learn/adding-interactivity | 0.637 | react.dev/reference/rsc/server-components | 0.623 | react.dev/learn/render-and-commit | 0.618 |
| colly+md | #9 | react.dev/learn/responding-to-events | 0.632 | react.dev/learn/responding-to-events#passing-event | 0.632 | react.dev/reference/rsc/server-components | 0.622 |
| playwright | #4 | react.dev/learn/responding-to-events | 0.633 | react.dev/reference/rsc/server-components | 0.623 | react.dev/learn/render-and-commit | 0.618 |


**Q16: How do I install and set up a new React project?** [conceptual]
*(expects URL containing: `installation`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | react.dev/learn/build-a-react-app-from-scratch | 0.657 | react.dev/learn/setup | 0.639 | react.dev/learn/add-react-to-an-existing-project | 0.618 |
| crawl4ai | #5 | az.react.dev/learn/add-react-to-an-existing-projec | 0.701 | 18.react.dev/learn/add-react-to-an-existing-projec | 0.698 | he.react.dev/learn/add-react-to-an-existing-projec | 0.698 |
| crawl4ai-raw | #5 | az.react.dev/learn/add-react-to-an-existing-projec | 0.701 | 18.react.dev/learn/add-react-to-an-existing-projec | 0.698 | he.react.dev/learn/add-react-to-an-existing-projec | 0.698 |
| scrapy+md | #8 | react.dev/learn/add-react-to-an-existing-project | 0.657 | react.dev/learn/build-a-react-app-from-scratch | 0.657 | react.dev/learn/creating-a-react-app | 0.652 |
| crawlee | #2 | react.dev/learn/add-react-to-an-existing-project | 0.657 | react.dev/learn/installation | 0.602 | react.dev/learn/build-a-react-app-from-scratch | 0.598 |
| colly+md | #3 | react.dev/learn/add-react-to-an-existing-project#u | 0.657 | react.dev/learn/add-react-to-an-existing-project | 0.657 | react.dev/learn/installation#try-react | 0.602 |
| playwright | #2 | react.dev/learn/add-react-to-an-existing-project | 0.657 | react.dev/learn/installation | 0.602 | react.dev/learn/build-a-react-app-from-scratch | 0.597 |


</details>

## stripe-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| scrapy+md | 56% (10/18) | 72% (13/18) | 72% (13/18) | 72% (13/18) | 78% (14/18) | 0.623 | 14882 | 500 |
| crawl4ai-raw | 56% (10/18) | 67% (12/18) | 67% (12/18) | 67% (12/18) | 72% (13/18) | 0.616 | 3564 | 499 |
| crawl4ai | 56% (10/18) | 67% (12/18) | 67% (12/18) | 67% (12/18) | 72% (13/18) | 0.616 | 2651 | 500 |
| crawlee | 39% (7/18) | 72% (13/18) | 78% (14/18) | 83% (15/18) | 83% (15/18) | 0.556 | 30214 | 500 |
| colly+md | 39% (7/18) | 67% (12/18) | 83% (15/18) | 83% (15/18) | 83% (15/18) | 0.552 | 31125 | 499 |
| playwright | 39% (7/18) | 67% (12/18) | 78% (14/18) | 83% (15/18) | 83% (15/18) | 0.549 | 30229 | 500 |
| markcrawl | 17% (3/18) | 17% (3/18) | 28% (5/18) | 33% (6/18) | 33% (6/18) | 0.201 | 1904 | 489 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for stripe-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do I create a payment intent with Stripe?** [api-function]
*(expects URL containing: `payment-intent`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/payment-intents | 0.776 | docs.stripe.com/payments/mobile/accept-payment-emb | 0.725 | docs.stripe.com/payments/payment-element/migration | 0.710 |
| crawl4ai | #1 | docs.stripe.com/payments/payment-intents | 0.717 | docs.stripe.com/payments/accept-a-payment?api-inte | 0.711 | docs.stripe.com/payments/payment-element/migration | 0.706 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/payment-intents | 0.717 | docs.stripe.com/payments/accept-a-payment?api-inte | 0.711 | docs.stripe.com/payments/payment-element/migration | 0.706 |
| scrapy+md | #1 | docs.stripe.com/payments/payment-intents | 0.721 | docs.stripe.com/payments/accept-a-payment-deferred | 0.704 | docs.stripe.com/payments/payment-element/migration | 0.702 |
| crawlee | #2 | docs.stripe.com/api/payment_intents/create | 0.846 | docs.stripe.com/payments/payment-intents | 0.769 | docs.stripe.com/payments/accept-a-payment-deferred | 0.758 |
| colly+md | #2 | docs.stripe.com/api/payment/intents/create | 0.846 | docs.stripe.com/payments/payment-intents | 0.769 | docs.stripe.com/api/payment/intents/confirm#confir | 0.750 |
| playwright | #2 | docs.stripe.com/api/payment_intents/create | 0.846 | docs.stripe.com/payments/payment-intents | 0.769 | docs.stripe.com/payments/accept-a-payment-deferred | 0.758 |


**Q2: How do I handle webhooks from Stripe?** [api-function]
*(expects URL containing: `webhook`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/managed-payments/set-up-m | 0.642 | docs.stripe.com/payments/bacs-debit/accept-a-payme | 0.638 | docs.stripe.com/payments/payment-methods | 0.636 |
| crawl4ai | #1 | docs.stripe.com/webhooks | 0.710 | docs.stripe.com/webhooks/handling-payment-events | 0.705 | docs.stripe.com/webhooks | 0.673 |
| crawl4ai-raw | #1 | docs.stripe.com/webhooks | 0.710 | docs.stripe.com/webhooks/handling-payment-events | 0.705 | docs.stripe.com/webhooks | 0.673 |
| scrapy+md | #1 | docs.stripe.com/webhooks/handling-payment-events | 0.698 | docs.stripe.com/mobile/digital-goods/checkout | 0.642 | docs.stripe.com/payments/managed-payments/set-up-m | 0.642 |
| crawlee | #1 | docs.stripe.com/webhooks/handling-payment-events | 0.789 | docs.stripe.com/billing/subscriptions/webhooks | 0.770 | docs.stripe.com/webhooks/quickstart | 0.738 |
| colly+md | #1 | docs.stripe.com/webhooks/handling-payment-events | 0.789 | docs.stripe.com/webhooks/quickstart | 0.736 | docs.stripe.com/webhooks | 0.719 |
| playwright | #1 | docs.stripe.com/webhooks/handling-payment-events | 0.789 | docs.stripe.com/billing/subscriptions/webhooks | 0.770 | docs.stripe.com/webhooks/quickstart | 0.738 |


**Q3: How do I set up Stripe subscriptions?** [api-function]
*(expects URL containing: `subscription`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #5 | docs.stripe.com/payments/save-and-reuse?platform=w | 0.675 | docs.stripe.com/payments/managed-payments/set-up | 0.634 | docs.stripe.com/payments/mobile/save-card-without- | 0.621 |
| crawl4ai | #1 | docs.stripe.com/billing/subscriptions/build-subscr | 0.682 | docs.stripe.com/billing/subscriptions/build-subscr | 0.682 | docs.stripe.com/billing/subscriptions/build-subscr | 0.682 |
| crawl4ai-raw | #1 | docs.stripe.com/billing/subscriptions/build-subscr | 0.682 | docs.stripe.com/billing/subscriptions/build-subscr | 0.682 | docs.stripe.com/billing/subscriptions/build-subscr | 0.682 |
| scrapy+md | #1 | docs.stripe.com/billing/subscriptions/build-subscr | 0.662 | docs.stripe.com/billing/subscriptions/build-subscr | 0.657 | docs.stripe.com/payments/checkout/build-subscripti | 0.645 |
| crawlee | #1 | docs.stripe.com/subscriptions | 0.782 | docs.stripe.com/payments/subscriptions | 0.782 | docs.stripe.com/billing/subscriptions/build-subscr | 0.773 |
| colly+md | #1 | docs.stripe.com/subscriptions | 0.782 | docs.stripe.com/payments/subscriptions | 0.782 | docs.stripe.com/billing/subscriptions/build-subscr | 0.773 |
| playwright | #1 | docs.stripe.com/subscriptions | 0.782 | docs.stripe.com/payments/subscriptions | 0.782 | docs.stripe.com/billing/subscriptions/build-subscr | 0.773 |


**Q4: How do I authenticate with the Stripe API?** [api-function]
*(expects URL containing: `authentication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #7 | docs.stripe.com/payments/save-and-reuse?platform=w | 0.589 | docs.stripe.com/payments/accept-a-payment-synchron | 0.577 | docs.stripe.com/payments/accept-a-payment-synchron | 0.570 |
| crawl4ai | #46 | docs.stripe.com/payments/link/save-and-reuse | 0.612 | docs.stripe.com/connect/required-verification-info | 0.611 | docs.stripe.com/keys | 0.604 |
| crawl4ai-raw | #45 | docs.stripe.com/payments/link/save-and-reuse | 0.612 | docs.stripe.com/connect/required-verification-info | 0.611 | docs.stripe.com/keys | 0.604 |
| scrapy+md | #1 | docs.stripe.com/payments/3d-secure/authentication- | 0.601 | docs.stripe.com/payments/link/save-and-reuse | 0.601 | docs.stripe.com/connect/account-tokens | 0.593 |
| crawlee | #2 | docs.stripe.com/payments/3d-secure | 0.735 | docs.stripe.com/payments/without-card-authenticati | 0.701 | docs.stripe.com/payments/mobile/without-card-authe | 0.701 |
| colly+md | #2 | docs.stripe.com/payments/3d-secure | 0.735 | docs.stripe.com/payment-authentication/writing-que | 0.702 | docs.stripe.com/strong-customer-authentication | 0.684 |
| playwright | #2 | docs.stripe.com/payments/3d-secure | 0.735 | docs.stripe.com/payments/without-card-authenticati | 0.701 | docs.stripe.com/payments/mobile/without-card-authe | 0.701 |


**Q5: How do I handle errors in the Stripe API?** [api-function]
*(expects URL containing: `error-handling`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/save-card-without-authent | 0.602 | docs.stripe.com/payments/save-card-without-authent | 0.599 | docs.stripe.com/payments/without-card-authenticati | 0.590 |
| crawl4ai | miss | docs.stripe.com/api | 0.572 | docs.stripe.com/api | 0.560 | docs.stripe.com/refunds | 0.560 |
| crawl4ai-raw | miss | docs.stripe.com/api | 0.572 | docs.stripe.com/api | 0.560 | docs.stripe.com/refunds | 0.560 |
| scrapy+md | miss | docs.stripe.com/error-low-level | 0.704 | docs.stripe.com/error-low-level | 0.611 | docs.stripe.com/error-low-level | 0.595 |
| crawlee | miss | docs.stripe.com/api/events#events | 0.602 | docs.stripe.com/disputes/responding#decide | 0.600 | docs.stripe.com/api/refunds | 0.596 |
| colly+md | miss | docs.stripe.com/get-started/checklist/go-live | 0.635 | docs.stripe.com/disputes/api | 0.634 | docs.stripe.com/payments/wallets/link | 0.603 |
| playwright | miss | docs.stripe.com/api/events | 0.602 | docs.stripe.com/disputes/responding | 0.600 | docs.stripe.com/api/refunds | 0.596 |


**Q6: How do I process refunds with Stripe?** [api-function]
*(expects URL containing: `refund`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/customer-balance/refundin | 0.664 | docs.stripe.com/payments/affirm | 0.636 | docs.stripe.com/payments/revolut-pay | 0.633 |
| crawl4ai | #2 | docs.stripe.com/billing/subscriptions/third-party- | 0.665 | docs.stripe.com/refunds | 0.665 | docs.stripe.com/refunds | 0.649 |
| crawl4ai-raw | #2 | docs.stripe.com/billing/subscriptions/third-party- | 0.665 | docs.stripe.com/refunds | 0.665 | docs.stripe.com/refunds | 0.649 |
| scrapy+md | #1 | docs.stripe.com/refunds?dashboard-or-api=api | 0.679 | docs.stripe.com/refunds?dashboard-or-api=dashboard | 0.656 | docs.stripe.com/refunds?dashboard-or-api=dashboard | 0.639 |
| crawlee | #1 | docs.stripe.com/api/refunds | 0.778 | docs.stripe.com/refunds | 0.714 | docs.stripe.com/billing/subscriptions/third-party- | 0.659 |
| colly+md | #1 | docs.stripe.com/api/refunds | 0.778 | docs.stripe.com/refunds | 0.714 | docs.stripe.com/refunds#cancel-payment | 0.714 |
| playwright | #1 | docs.stripe.com/api/refunds | 0.778 | docs.stripe.com/refunds | 0.714 | docs.stripe.com/billing/subscriptions/third-party- | 0.659 |


**Q7: How do I use Stripe checkout for payments?** [js-rendered]
*(expects URL containing: `checkout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/payments/checkout/save-and-reuse?p | 0.696 | docs.stripe.com/payments/accept-a-payment | 0.693 | docs.stripe.com/payments/ideal/save-during-payment | 0.675 |
| crawl4ai | #1 | docs.stripe.com/payments/checkout/save-and-reuse | 0.695 | docs.stripe.com/llms.txt | 0.686 | docs.stripe.com/payments/checkout/save-during-paym | 0.685 |
| crawl4ai-raw | #1 | docs.stripe.com/payments/checkout/save-and-reuse | 0.695 | docs.stripe.com/llms.txt | 0.686 | docs.stripe.com/payments/checkout/save-during-paym | 0.685 |
| scrapy+md | #1 | docs.stripe.com/payments/accept-a-payment?payment- | 0.668 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.667 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.667 |
| crawlee | #3 | docs.stripe.com/payments/online-payments | 0.731 | docs.stripe.com/payments/upi | 0.708 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.700 |
| colly+md | #5 | docs.stripe.com/payments/paypay | 0.736 | docs.stripe.com/payments/online-payments | 0.731 | docs.stripe.com/payments/online-payments#compare-f | 0.731 |
| playwright | #3 | docs.stripe.com/payments/online-payments | 0.731 | docs.stripe.com/payments/upi | 0.708 | docs.stripe.com/payments/checkout/how-checkout-wor | 0.700 |


**Q8: How do I test Stripe payments in development?** [code-example]
*(expects URL containing: `testing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #41 | docs.stripe.com/payments/advanced/dashboard-paymen | 0.653 | docs.stripe.com/payments/dashboard-payment-methods | 0.653 | docs.stripe.com/payments/kr-card/set-up-future-pay | 0.641 |
| crawl4ai | #1 | docs.stripe.com/testing | 0.725 | docs.stripe.com/get-started/test-developer-integra | 0.676 | docs.stripe.com/connect/direct-charges | 0.673 |
| crawl4ai-raw | #1 | docs.stripe.com/testing | 0.725 | docs.stripe.com/get-started/test-developer-integra | 0.676 | docs.stripe.com/connect/direct-charges | 0.673 |
| scrapy+md | #1 | docs.stripe.com/connect/testing | 0.670 | docs.stripe.com/get-started/test-developer-integra | 0.669 | docs.stripe.com/payments/managed-payments/set-up | 0.658 |
| crawlee | #2 | docs.stripe.com/get-started/development-environmen | 0.707 | docs.stripe.com/testing | 0.692 | docs.stripe.com/financial-connections/testing | 0.687 |
| colly+md | #2 | docs.stripe.com/get-started/development-environmen | 0.707 | docs.stripe.com/testing#cards | 0.690 | docs.stripe.com/testing | 0.690 |
| playwright | #2 | docs.stripe.com/get-started/development-environmen | 0.706 | docs.stripe.com/financial-connections/testing | 0.687 | docs.stripe.com/testing | 0.676 |


**Q9: What are Stripe Connect and platform payments?** [conceptual]
*(expects URL containing: `connect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | docs.stripe.com/payments/pay-with-balance | 0.648 | docs.stripe.com/payments/pay-by-bank | 0.609 | docs.stripe.com/payments/bank-transfers | 0.598 |
| crawl4ai | #1 | docs.stripe.com/connect | 0.732 | docs.stripe.com/connect | 0.728 | docs.stripe.com/glossary | 0.690 |
| crawl4ai-raw | #1 | docs.stripe.com/connect | 0.732 | docs.stripe.com/connect | 0.728 | docs.stripe.com/glossary | 0.690 |
| scrapy+md | #2 | docs.stripe.com/payments/link/payment-request-butt | 0.683 | docs.stripe.com/connect/platform-controls-for-stri | 0.666 | docs.stripe.com/connect/connect-embedded-component | 0.663 |
| crawlee | #1 | docs.stripe.com/connect | 0.759 | docs.stripe.com/connect/build-full-embedded-integr | 0.756 | docs.stripe.com/connect | 0.717 |
| colly+md | #1 | docs.stripe.com/connect | 0.759 | docs.stripe.com/connect/build-full-embedded-integr | 0.756 | docs.stripe.com/connect | 0.713 |
| playwright | #1 | docs.stripe.com/connect | 0.759 | docs.stripe.com/connect/build-full-embedded-integr | 0.756 | docs.stripe.com/connect | 0.713 |


**Q10: How do I set up usage-based billing with Stripe?** [js-rendered]
*(expects URL containing: `usage-based`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/save-and-reuse?platform=w | 0.601 | docs.stripe.com/payments/checkout/build-subscripti | 0.594 | docs.stripe.com/payments/setup-intents | 0.590 |
| crawl4ai | miss | docs.stripe.com/llms.txt | 0.656 | docs.stripe.com/billing/subscriptions/prebilling | 0.620 | docs.stripe.com/billing/subscriptions/billing-cycl | 0.618 |
| crawl4ai-raw | miss | docs.stripe.com/llms.txt | 0.656 | docs.stripe.com/billing/subscriptions/prebilling | 0.620 | docs.stripe.com/billing/subscriptions/billing-cycl | 0.618 |
| scrapy+md | #1 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.708 | docs.stripe.com/billing/subscriptions/usage-based- | 0.686 | docs.stripe.com/billing/subscriptions/usage-based- | 0.665 |
| crawlee | miss | docs.stripe.com/tax/set-up | 0.671 | docs.stripe.com/billing | 0.661 | docs.stripe.com/llms.txt | 0.656 |
| colly+md | miss | docs.stripe.com/tax/set-up | 0.671 | docs.stripe.com/get-started/account/set-up | 0.664 | docs.stripe.com/get-started/account/set-up#public- | 0.664 |
| playwright | miss | docs.stripe.com/tax/set-up | 0.671 | docs.stripe.com/billing | 0.661 | docs.stripe.com/llms.txt | 0.656 |


**Q11: How do I manage Stripe API keys?** [api-function]
*(expects URL containing: `keys`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/mobile/accept-payment?int | 0.541 | docs.stripe.com/payments/vault-and-forward | 0.518 | docs.stripe.com/payments/save-and-reuse?platform=w | 0.511 |
| crawl4ai | #1 | docs.stripe.com/keys-best-practices | 0.763 | docs.stripe.com/keys | 0.745 | docs.stripe.com/get-started/api-request | 0.717 |
| crawl4ai-raw | #1 | docs.stripe.com/keys-best-practices | 0.763 | docs.stripe.com/keys | 0.745 | docs.stripe.com/get-started/api-request | 0.717 |
| scrapy+md | #3 | docs.stripe.com/get-started/api-request | 0.724 | docs.stripe.com/get-started/api-request | 0.656 | docs.stripe.com/stripe-cli/keys | 0.655 |
| crawlee | #1 | docs.stripe.com/keys-best-practices | 0.832 | docs.stripe.com/keys | 0.724 | docs.stripe.com/keys-best-practices | 0.718 |
| colly+md | #1 | docs.stripe.com/keys-best-practices | 0.832 | docs.stripe.com/sandboxes/dashboard/manage-access# | 0.819 | docs.stripe.com/keys/restricted-api-keys | 0.755 |
| playwright | #1 | docs.stripe.com/keys-best-practices | 0.832 | docs.stripe.com/keys | 0.724 | docs.stripe.com/keys | 0.705 |


**Q12: How do I handle Stripe rate limits?** [api-function]
*(expects URL containing: `rate-limits`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/without-card-authenticati | 0.528 | docs.stripe.com/payments/incremental-authorization | 0.523 | docs.stripe.com/payments/save-card-without-authent | 0.522 |
| crawl4ai | miss | docs.stripe.com/tax/tax-rates | 0.567 | docs.stripe.com/currencies | 0.547 | docs.stripe.com/payments/upi | 0.547 |
| crawl4ai-raw | miss | docs.stripe.com/tax/tax-rates | 0.567 | docs.stripe.com/currencies | 0.548 | docs.stripe.com/payments/upi | 0.547 |
| scrapy+md | miss | docs.stripe.com/disputes/prevention/card-testing | 0.563 | docs.stripe.com/payments/upi | 0.552 | docs.stripe.com/declines | 0.541 |
| crawlee | miss | docs.stripe.com/tax/tax-rates | 0.625 | docs.stripe.com/money-management | 0.608 | docs.stripe.com/global-payouts/pricing | 0.603 |
| colly+md | miss | docs.stripe.com/tax/tax-rates | 0.625 | docs.stripe.com/changelog/dahlia/2026-03-25/issuin | 0.618 | docs.stripe.com/money-management | 0.608 |
| playwright | miss | docs.stripe.com/tax/tax-rates | 0.625 | docs.stripe.com/money-management | 0.608 | docs.stripe.com/global-payouts/pricing | 0.603 |


**Q13: How do I use metadata with Stripe objects?** [api-function]
*(expects URL containing: `metadata`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/charges-api | 0.617 | docs.stripe.com/payments/payment-intents | 0.612 | docs.stripe.com/payments/checkout/embedded-analyti | 0.517 |
| crawl4ai | miss | docs.stripe.com/api | 0.756 | docs.stripe.com/api | 0.646 | docs.stripe.com/payments/payment-intents | 0.627 |
| crawl4ai-raw | miss | docs.stripe.com/api | 0.756 | docs.stripe.com/api | 0.646 | docs.stripe.com/payments/payment-intents | 0.627 |
| scrapy+md | miss | docs.stripe.com/api/errors/handling | 0.735 | docs.stripe.com/api/errors/handling | 0.717 | docs.stripe.com/payments/payment-intents | 0.621 |
| crawlee | #3 | docs.stripe.com/custom-objects | 0.676 | docs.stripe.com/billing/subscriptions/analytics | 0.636 | docs.stripe.com/industry-metadata | 0.635 |
| colly+md | #3 | docs.stripe.com/api/idempotent/requests | 0.740 | docs.stripe.com/custom-objects | 0.676 | docs.stripe.com/changelog/dahlia/2026-03-25/adds-m | 0.666 |
| playwright | #5 | docs.stripe.com/api | 0.730 | docs.stripe.com/custom-objects | 0.676 | docs.stripe.com/api | 0.639 |


**Q14: How do I set up Apple Pay with Stripe?** [js-rendered]
*(expects URL containing: `apple-pay`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/mobile/save-card-without- | 0.625 | docs.stripe.com/payments/accept-a-payment | 0.619 | docs.stripe.com/payments/mobile/accept-payment?pla | 0.613 |
| crawl4ai | #1 | docs.stripe.com/apple-pay | 0.711 | docs.stripe.com/apple-pay | 0.699 | docs.stripe.com/apple-pay | 0.686 |
| crawl4ai-raw | #1 | docs.stripe.com/apple-pay | 0.711 | docs.stripe.com/apple-pay | 0.699 | docs.stripe.com/apple-pay | 0.686 |
| scrapy+md | #1 | docs.stripe.com/apple-pay?platform=react-native | 0.694 | docs.stripe.com/apple-pay?platform=react-native | 0.692 | docs.stripe.com/apple-pay/cartes-bancaires | 0.668 |
| crawlee | #1 | docs.stripe.com/apple-pay | 0.748 | docs.stripe.com/apple-pay | 0.696 | docs.stripe.com/apple-pay | 0.688 |
| colly+md | #1 | docs.stripe.com/apple-pay | 0.748 | docs.stripe.com/apple-pay/cartes-bancaires | 0.728 | docs.stripe.com/apple-pay | 0.708 |
| playwright | #1 | docs.stripe.com/apple-pay | 0.748 | docs.stripe.com/apple-pay | 0.696 | docs.stripe.com/apple-pay | 0.688 |


**Q15: How do I issue cards with Stripe Issuing?** [api-function]
*(expects URL containing: `issuing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/cards | 0.571 | docs.stripe.com/payments/payment-intents/three-d-s | 0.555 | docs.stripe.com/payments/save-card-without-authent | 0.553 |
| crawl4ai | #2 | docs.stripe.com/llms.txt | 0.750 | docs.stripe.com/issuing/stablecoin-cards-for-finan | 0.736 | docs.stripe.com/issuing | 0.723 |
| crawl4ai-raw | #2 | docs.stripe.com/llms.txt | 0.750 | docs.stripe.com/issuing/stablecoin-cards-for-finan | 0.736 | docs.stripe.com/issuing | 0.723 |
| scrapy+md | miss | docs.stripe.com/llms.txt | 0.719 | docs.stripe.com/llms.txt | 0.644 | docs.stripe.com/co-badged-cards-compliance | 0.588 |
| crawlee | #1 | docs.stripe.com/issuing | 0.752 | docs.stripe.com/llms.txt | 0.750 | docs.stripe.com/issuing/stablecoin-cards-for-finan | 0.741 |
| colly+md | #1 | docs.stripe.com/issuing | 0.752 | docs.stripe.com/issuing | 0.724 | docs.stripe.com/issuing/for-your-business | 0.691 |
| playwright | #1 | docs.stripe.com/issuing | 0.752 | docs.stripe.com/llms.txt | 0.750 | docs.stripe.com/issuing/stablecoin-cards-for-finan | 0.741 |


**Q16: How do I recover failed subscription payments?** [js-rendered]
*(expects URL containing: `revenue-recovery`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/pay-with-balance | 0.521 | docs.stripe.com/payments/paypal/set-up-future-paym | 0.473 | docs.stripe.com/payments/sepa-debit | 0.462 |
| crawl4ai | #1 | docs.stripe.com/billing/revenue-recovery | 0.542 | docs.stripe.com/billing/subscriptions/cancel | 0.538 | docs.stripe.com/billing/subscriptions/webhooks | 0.514 |
| crawl4ai-raw | #1 | docs.stripe.com/billing/revenue-recovery | 0.542 | docs.stripe.com/billing/subscriptions/cancel | 0.538 | docs.stripe.com/billing/subscriptions/webhooks | 0.514 |
| scrapy+md | #18 | docs.stripe.com/india-recurring-payments | 0.538 | docs.stripe.com/india-recurring-payments?integrati | 0.538 | docs.stripe.com/connect/saas/tasks/service-fee | 0.521 |
| crawlee | #7 | docs.stripe.com/billing/collection-method | 0.576 | docs.stripe.com/payments/pay-with-balance | 0.521 | docs.stripe.com/billing/subscriptions/cancel | 0.521 |
| colly+md | #5 | docs.stripe.com/payments/pay-with-balance | 0.521 | docs.stripe.com/payments/pay-with-balance | 0.498 | docs.stripe.com/billing/subscriptions/change | 0.496 |
| playwright | #7 | docs.stripe.com/billing/collection-method | 0.576 | docs.stripe.com/payments/pay-with-balance | 0.521 | docs.stripe.com/billing/subscriptions/cancel | 0.521 |


**Q17: How does Stripe handle tax calculation for billing?** [js-rendered]
*(expects URL containing: `billing/taxes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/advanced/tax | 0.653 | docs.stripe.com/payments/checkout/taxes | 0.651 | docs.stripe.com/payments/checkout/use-manual-tax-r | 0.651 |
| crawl4ai | #14 | docs.stripe.com/tax/custom | 0.708 | docs.stripe.com/tax/checkout | 0.701 | docs.stripe.com/tax/tax-rates | 0.697 |
| crawl4ai-raw | #14 | docs.stripe.com/tax/custom | 0.708 | docs.stripe.com/tax/checkout | 0.701 | docs.stripe.com/tax/tax-rates | 0.697 |
| scrapy+md | #3 | docs.stripe.com/invoicing/taxes?dashboard-or-api=d | 0.700 | docs.stripe.com/llms.txt | 0.649 | docs.stripe.com/billing/taxes/collect-taxes | 0.643 |
| crawlee | #2 | docs.stripe.com/tax/set-up | 0.744 | docs.stripe.com/billing/taxes/migration | 0.718 | docs.stripe.com/tax/reports | 0.717 |
| colly+md | #2 | docs.stripe.com/tax/set-up | 0.744 | docs.stripe.com/billing/taxes/migration | 0.718 | docs.stripe.com/tax/reports | 0.717 |
| playwright | #2 | docs.stripe.com/tax/set-up | 0.744 | docs.stripe.com/billing/taxes/migration | 0.718 | docs.stripe.com/tax/reports | 0.717 |


**Q18: How do I migrate data to Stripe?** [conceptual]
*(expects URL containing: `data-migrations`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/payments/ach-direct-debit/migratin | 0.654 | docs.stripe.com/payments/checkout/migration | 0.638 | docs.stripe.com/payments/nz-bank-account/migrate-f | 0.621 |
| crawl4ai | #1 | docs.stripe.com/get-started/data-migrations/overvi | 0.705 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.676 | docs.stripe.com/billing/taxes/migration | 0.654 |
| crawl4ai-raw | #1 | docs.stripe.com/get-started/data-migrations/overvi | 0.705 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.676 | docs.stripe.com/billing/taxes/migration | 0.654 |
| scrapy+md | #1 | docs.stripe.com/get-started/data-migrations/pan-im | 0.757 | docs.stripe.com/connect/migrate-to-stripe | 0.718 | docs.stripe.com/get-started/data-migrations/pan-im | 0.691 |
| crawlee | #5 | docs.stripe.com/billing/taxes/migration | 0.771 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.752 | docs.stripe.com/payments/checkout/migration | 0.735 |
| colly+md | #5 | docs.stripe.com/billing/taxes/migration | 0.771 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.752 | docs.stripe.com/payments/checkout/migration | 0.735 |
| playwright | #5 | docs.stripe.com/billing/taxes/migration | 0.771 | docs.stripe.com/billing/subscriptions/migrate-subs | 0.752 | docs.stripe.com/payments/checkout/migration | 0.735 |


</details>

## huggingface-transformers

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 88% (7/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.906 | 4518 | 300 |
| scrapy+md | 75% (6/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.812 | 6346 | 240 |
| playwright | 12% (1/8) | 12% (1/8) | 25% (2/8) | 25% (2/8) | 25% (2/8) | 0.154 | 356 | 300 |
| crawlee | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.125 | 67 | 16 |
| crawl4ai-raw | 0% (0/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.062 | 1018 | 295 |
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
| markcrawl | #1 | huggingface.co/docs/transformers/pipeline_tutorial | 0.636 | huggingface.co/docs/transformers/v5.8.0/en/pipelin | 0.636 | huggingface.co/docs/transformers/v5.8.0/en/main_cl | 0.623 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | miss | huggingface.co/docs/transformers/index | 0.520 | huggingface.co/docs/transformers/index | 0.455 | huggingface.co/docs/transformers/index | 0.453 |
| scrapy+md | #2 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.663 | huggingface.co/docs/transformers/pipeline_tutorial | 0.655 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.579 |
| crawlee | miss | huggingface.co/docs/transformers/quicktour | 0.534 | huggingface.co/docs/transformers/index | 0.516 | huggingface.co/docs/transformers/quicktour | 0.489 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/docs/transformers/quicktour | 0.534 | huggingface.co/docs/transformers/quicktour | 0.508 | huggingface.co/docs/transformers/quicktour | 0.505 |


**Q2: How do I train a model with the Hugging Face Trainer?** [api-function]
*(expects URL containing: `trainer`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | huggingface.co/docs/transformers/v5.8.0/en/trainer | 0.560 | huggingface.co/docs/transformers/trainer | 0.560 | huggingface.co/docs/transformers/v5.8.0/en/index | 0.534 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | miss | huggingface.co/join | 0.571 | huggingface.co/google/gemma-4-26B-A4B-it | 0.566 | huggingface.co/docs/transformers/installation | 0.562 |
| scrapy+md | #1 | huggingface.co/docs/transformers/trainer | 0.539 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.507 | huggingface.co/support | 0.464 |
| crawlee | miss | huggingface.co/docs/transformers/quicktour | 0.508 | huggingface.co/docs/transformers/quicktour | 0.502 | huggingface.co/docs/transformers/quicktour | 0.485 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #35 | huggingface.co/docs/transformers/quicktour | 0.514 | huggingface.co/docs/transformers/quicktour | 0.504 | huggingface.co/docs/transformers/quicktour | 0.498 |


**Q3: How do I generate text with a large language model?** [api-function]
*(expects URL containing: `llm_tutorial`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | huggingface.co/docs/transformers/llm_tutorial | 0.547 | huggingface.co/docs/transformers/v5.8.0/en/tasks/l | 0.531 | huggingface.co/docs/transformers/llm_tutorial | 0.514 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | miss | huggingface.co/unsloth/Qwen3.5-35B-A3B-GGUF | 0.499 | huggingface.co/unsloth/Qwen3.5-9B-GGUF | 0.499 | huggingface.co/google/gemma-4-26B-A4B-it | 0.493 |
| scrapy+md | #1 | huggingface.co/docs/transformers/llm_tutorial | 0.578 | huggingface.co/docs/transformers/llm_tutorial | 0.514 | huggingface.co/facebook/mbart-large-cc25 | 0.511 |
| crawlee | miss | huggingface.co/docs/transformers/quicktour | 0.460 | huggingface.co/models | 0.443 | huggingface.co/docs/transformers/index | 0.431 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/docs/transformers/quicktour | 0.460 | huggingface.co/models | 0.436 | huggingface.co/models | 0.434 |


**Q4: What are the design principles behind the Transformers library?** [conceptual]
*(expects URL containing: `philosophy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | huggingface.co/docs/transformers/v5.8.0/en/philoso | 0.606 | huggingface.co/docs/transformers/philosophy | 0.606 | huggingface.co/docs/transformers/index | 0.588 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | miss | huggingface.co/docs/transformers/index | 0.589 | huggingface.co/docs/transformers/index | 0.582 | huggingface.co/docs/transformers/index | 0.503 |
| scrapy+md | #1 | huggingface.co/docs/transformers/philosophy | 0.610 | huggingface.co/docs/transformers/index | 0.601 | huggingface.co/docs/transformers/index | 0.567 |
| crawlee | miss | huggingface.co/docs/transformers/index | 0.568 | huggingface.co/docs/transformers/index | 0.543 | huggingface.co/docs/transformers/index | 0.487 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/docs/transformers/index | 0.587 | huggingface.co/docs/transformers/index | 0.547 | huggingface.co/docs/transformers/quicktour | 0.504 |


**Q5: What models are supported in the Transformers library?** [cross-page]
*(expects URL containing: `models_timeline`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | huggingface.co/docs/transformers/index | 0.648 | huggingface.co/docs/transformers/v5.8.0/en/index | 0.648 | huggingface.co/docs/transformers/main/en/index | 0.642 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | miss | huggingface.co/docs/transformers/index | 0.634 | huggingface.co/docs/transformers/index | 0.563 | huggingface.co/docs/transformers/index | 0.556 |
| scrapy+md | miss | huggingface.co/docs/transformers/index | 0.663 | huggingface.co/docs/transformers/philosophy | 0.584 | huggingface.co/docs/transformers/index | 0.575 |
| crawlee | miss | huggingface.co/docs/transformers/index | 0.631 | huggingface.co/docs/transformers/index | 0.533 | huggingface.co/docs/transformers/installation | 0.528 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #5 | huggingface.co/docs/transformers/index | 0.647 | huggingface.co/docs/transformers/index | 0.567 | huggingface.co/docs/transformers/quicktour | 0.537 |


**Q6: What is the Pipeline API reference in Transformers?** [api-function]
*(expects URL containing: `main_classes/pipelines`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | huggingface.co/docs/transformers/v5.8.0/en/main_cl | 0.675 | huggingface.co/docs/transformers/pipeline_tutorial | 0.662 | huggingface.co/docs/transformers/v5.8.0/en/pipelin | 0.662 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | miss | huggingface.co/docs/transformers/index | 0.575 | huggingface.co/docs/transformers/index | 0.533 | huggingface.co/docs/transformers/installation | 0.529 |
| scrapy+md | #1 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.683 | huggingface.co/docs/transformers/pipeline_tutorial | 0.664 | huggingface.co/docs/transformers/pipeline_tutorial | 0.587 |
| crawlee | miss | huggingface.co/docs/transformers/index | 0.564 | huggingface.co/docs/transformers/installation | 0.496 | huggingface.co/docs/transformers/index | 0.494 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/docs/transformers/index | 0.557 | huggingface.co/docs/transformers/quicktour | 0.521 | huggingface.co/docs/transformers/installation | 0.496 |


**Q7: What does the Trainer class support for distributed training?** [api-function]
*(expects URL containing: `main_classes/trainer`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | huggingface.co/docs/transformers/v5.8.0/en/main_cl | 0.571 | huggingface.co/docs/transformers/v5.8.0/en/trainer | 0.549 | huggingface.co/docs/transformers/trainer | 0.549 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | miss | huggingface.co/docs/transformers/index | 0.398 | huggingface.co/docs | 0.368 | discuss.huggingface.co/u/dinods | 0.357 |
| scrapy+md | #1 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.570 | huggingface.co/docs/transformers/trainer | 0.523 | huggingface.co/docs/transformers/v5.7.0/en/main_cl | 0.488 |
| crawlee | miss | huggingface.co/docs/transformers/quicktour | 0.441 | huggingface.co/docs/transformers/quicktour | 0.439 | huggingface.co/docs/transformers/peft | 0.423 |
| colly+md | — | — | — | — | — | — | — |
| playwright | miss | huggingface.co/docs/transformers/quicktour | 0.441 | huggingface.co/docs/transformers/peft | 0.440 | huggingface.co/docs/transformers/quicktour | 0.429 |


**Q8: What is the Hugging Face Transformers library?** [conceptual]
*(expects URL containing: `transformers/index`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | huggingface.co/docs/transformers/index | 0.573 | huggingface.co/docs/transformers/v5.8.0/en/index | 0.573 | huggingface.co/docs/transformers/v5.8.0/en/model_d | 0.571 |
| crawl4ai | — | — | — | — | — | — | — |
| crawl4ai-raw | #2 | huggingface.co/docs/transformers/installation | 0.635 | huggingface.co/docs/transformers/index | 0.629 | huggingface.co/docs/transformers/index | 0.593 |
| scrapy+md | #1 | huggingface.co/docs/transformers/index | 0.542 | huggingface.co/docs/transformers/index | 0.523 | huggingface.co/docs/transformers/philosophy | 0.507 |
| crawlee | #1 | huggingface.co/docs/transformers/index | 0.562 | huggingface.co/docs/transformers/index | 0.515 | huggingface.co/docs/transformers/quicktour | 0.509 |
| colly+md | — | — | — | — | — | — | — |
| playwright | #1 | huggingface.co/docs/transformers/index | 0.556 | huggingface.co/docs/transformers/index | 0.529 | huggingface.co/docs/transformers/quicktour | 0.488 |


</details>

## kubernetes-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawl4ai | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 6822 | 400 |
| crawl4ai-raw | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 6822 | 400 |
| crawlee | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 6813 | 400 |
| colly+md | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 6743 | 399 |
| playwright | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 1.000 | 6812 | 400 |
| markcrawl | 75% (6/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.823 | 7922 | 400 |
| scrapy+md | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.129 | 3507 | 315 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for kubernetes-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is a Kubernetes pod and what does it represent?** [conceptual]
*(expects URL containing: `workloads/pods`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.657 | kubernetes.io/docs/concepts/workloads/pods/_print/ | 0.649 | kubernetes.io/docs/concepts/workloads/_print/ | 0.636 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.673 | kubernetes.io/docs/concepts/workloads/pods/ | 0.629 | kubernetes.io/docs/concepts/workloads/pods/advance | 0.605 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.673 | kubernetes.io/docs/concepts/workloads/pods/ | 0.629 | kubernetes.io/docs/concepts/workloads/pods/advance | 0.605 |
| scrapy+md | miss | kubernetes.io/uk/docs/reference/glossary/ | 0.672 | kubernetes.io/docs/concepts/_print/ | 0.640 | kubernetes.io/de/docs/_print/ | 0.612 |
| crawlee | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.657 | kubernetes.io/docs/concepts/workloads/pods/ | 0.586 | kubernetes.io/ru/docs/concepts/ | 0.574 |
| colly+md | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.657 | kubernetes.io/docs/concepts/workloads/pods/ | 0.586 | kubernetes.io/ru/docs/concepts/ | 0.574 |
| playwright | #1 | kubernetes.io/docs/concepts/workloads/pods/ | 0.657 | kubernetes.io/docs/concepts/workloads/pods/ | 0.586 | kubernetes.io/ru/docs/concepts/ | 0.574 |


**Q2: How do Kubernetes Deployments manage replicas and rollouts?** [api-function]
*(expects URL containing: `controllers/deployment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | kubernetes.io/docs/concepts/_print/ | 0.701 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.701 | kubernetes.io/docs/concepts/workloads/_print/ | 0.701 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.689 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.668 | kubernetes.io/docs/concepts/workloads/management/ | 0.662 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.689 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.668 | kubernetes.io/docs/concepts/workloads/management/ | 0.662 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.701 | kubernetes.io/docs/concepts/_print/ | 0.668 | kubernetes.io/docs/concepts/_print/ | 0.662 |
| crawlee | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.679 | kubernetes.io/docs/concepts/workloads/management/ | 0.668 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.662 |
| colly+md | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.679 | kubernetes.io/docs/concepts/workloads/management/ | 0.668 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.662 |
| playwright | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.679 | kubernetes.io/docs/concepts/workloads/management/ | 0.668 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.662 |


**Q3: What is a Kubernetes Service and how does it expose pods?** [conceptual]
*(expects URL containing: `services-networking/service`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.744 | kubernetes.io/docs/concepts/_print/ | 0.720 | kubernetes.io/docs/concepts/services-networking/_p | 0.714 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.680 | kubernetes.io/docs/concepts/services-networking/se | 0.675 | kubernetes.io/docs/concepts/services-networking/se | 0.608 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.680 | kubernetes.io/docs/concepts/services-networking/se | 0.675 | kubernetes.io/docs/concepts/services-networking/se | 0.608 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.720 | kubernetes.io/docs/concepts/_print/ | 0.668 | kubernetes.io/de/docs/_print/ | 0.638 |
| crawlee | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.682 | kubernetes.io/docs/concepts/services-networking/se | 0.668 | kubernetes.io/docs/tasks/access-application-cluste | 0.627 |
| colly+md | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.682 | kubernetes.io/docs/concepts/services-networking/se | 0.668 | kubernetes.io/docs/tasks/access-application-cluste | 0.627 |
| playwright | #1 | kubernetes.io/docs/concepts/services-networking/se | 0.682 | kubernetes.io/docs/concepts/services-networking/se | 0.668 | kubernetes.io/docs/tasks/access-application-cluste | 0.627 |


**Q4: How do I use ConfigMaps to inject configuration into pods?** [api-function]
*(expects URL containing: `configuration/configmap`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.730 | kubernetes.io/docs/concepts/configuration/configma | 0.716 | kubernetes.io/docs/concepts/_print/ | 0.680 |
| crawl4ai | #1 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.690 | kubernetes.io/docs/concepts/configuration/configma | 0.672 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.654 |
| crawl4ai-raw | #1 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.690 | kubernetes.io/docs/concepts/configuration/configma | 0.672 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.654 |
| scrapy+md | #1 | kubernetes.io/it/docs/concepts/configuration/confi | 0.684 | kubernetes.io/it/docs/_print/ | 0.684 | kubernetes.io/it/docs/concepts/configuration/_prin | 0.684 |
| crawlee | #1 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.670 | kubernetes.io/docs/concepts/configuration/configma | 0.669 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.648 |
| colly+md | #1 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.670 | kubernetes.io/docs/concepts/configuration/configma | 0.669 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.648 |
| playwright | #1 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.670 | kubernetes.io/docs/concepts/configuration/configma | 0.669 | kubernetes.io/docs/tasks/configure-pod-container/c | 0.648 |


**Q5: How do I manage Secrets in Kubernetes?** [api-function]
*(expects URL containing: `configuration/secret`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/configuration/secret/ | 0.751 | kubernetes.io/docs/concepts/configuration/secret/ | 0.729 | kubernetes.io/docs/concepts/configuration/_print/ | 0.729 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/configuration/secret/ | 0.794 | kubernetes.io/docs/concepts/configuration/secret/ | 0.731 | kubernetes.io/docs/tasks/inject-data-application/d | 0.708 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/configuration/secret/ | 0.794 | kubernetes.io/docs/concepts/configuration/secret/ | 0.731 | kubernetes.io/docs/tasks/inject-data-application/d | 0.708 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.731 | kubernetes.io/docs/concepts/_print/ | 0.724 | kubernetes.io/docs/concepts/_print/ | 0.672 |
| crawlee | #1 | kubernetes.io/docs/concepts/configuration/secret/ | 0.772 | kubernetes.io/docs/concepts/configuration/secret/ | 0.731 | kubernetes.io/docs/concepts/security/secrets-good- | 0.710 |
| colly+md | #1 | kubernetes.io/docs/concepts/configuration/secret/ | 0.772 | kubernetes.io/docs/concepts/configuration/secret/ | 0.731 | kubernetes.io/docs/concepts/security/secrets-good- | 0.710 |
| playwright | #1 | kubernetes.io/docs/concepts/configuration/secret/ | 0.772 | kubernetes.io/docs/concepts/configuration/secret/ | 0.731 | kubernetes.io/docs/concepts/security/secrets-good- | 0.710 |


**Q6: What are namespaces in Kubernetes and when should I use them?** [conceptual]
*(expects URL containing: `working-with-objects/namespaces`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/overview/working-with- | 0.762 | kubernetes.io/docs/tutorials/cluster-management/na | 0.712 | kubernetes.io/docs/concepts/_print/ | 0.708 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/overview/working-with- | 0.746 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.683 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.682 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/overview/working-with- | 0.746 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.683 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.682 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.707 | kubernetes.io/docs/concepts/_print/ | 0.662 | kubernetes.io/docs/concepts/_print/ | 0.661 |
| crawlee | #1 | kubernetes.io/docs/concepts/overview/working-with- | 0.744 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.674 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.673 |
| colly+md | #1 | kubernetes.io/docs/concepts/overview/working-with- | 0.744 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.674 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.673 |
| playwright | #1 | kubernetes.io/docs/concepts/overview/working-with- | 0.744 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.674 | kubernetes.io/docs/tasks/administer-cluster/namesp | 0.673 |


**Q7: How does Kubernetes Ingress route external traffic?** [conceptual]
*(expects URL containing: `services-networking/ingress`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | kubernetes.io/docs/concepts/services-networking/_p | 0.656 | kubernetes.io/docs/concepts/_print/ | 0.656 | kubernetes.io/docs/concepts/services-networking/in | 0.632 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.626 | kubernetes.io/docs/concepts/services-networking/in | 0.620 | kubernetes.io/docs/concepts/services-networking/in | 0.590 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.626 | kubernetes.io/docs/concepts/services-networking/in | 0.620 | kubernetes.io/docs/concepts/services-networking/in | 0.590 |
| scrapy+md | #32 | kubernetes.io/docs/concepts/_print/ | 0.654 | kubernetes.io/docs/concepts/_print/ | 0.620 | kubernetes.io/docs/concepts/_print/ | 0.571 |
| crawlee | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.632 | kubernetes.io/docs/concepts/services-networking/in | 0.620 | kubernetes.io/docs/concepts/services-networking/in | 0.590 |
| colly+md | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.632 | kubernetes.io/docs/concepts/services-networking/in | 0.620 | kubernetes.io/docs/concepts/services-networking/in | 0.590 |
| playwright | #1 | kubernetes.io/docs/concepts/services-networking/in | 0.632 | kubernetes.io/docs/concepts/services-networking/in | 0.620 | kubernetes.io/docs/concepts/services-networking/in | 0.590 |


**Q8: What is a StatefulSet and when do I need one?** [api-function]
*(expects URL containing: `controllers/statefulset`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.677 | kubernetes.io/docs/concepts/_print/ | 0.585 | kubernetes.io/docs/concepts/workloads/_print/ | 0.585 |
| crawl4ai | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.586 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.550 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.468 |
| crawl4ai-raw | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.586 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.550 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.468 |
| scrapy+md | miss | kubernetes.io/docs/concepts/_print/ | 0.584 | kubernetes.io/docs/concepts/_print/ | 0.543 | kubernetes.io/docs/concepts/_print/ | 0.468 |
| crawlee | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.587 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.549 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.496 |
| colly+md | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.587 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.549 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.496 |
| playwright | #1 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.587 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.549 | kubernetes.io/docs/concepts/workloads/controllers/ | 0.496 |


</details>

## postgres-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawlee | 88% (7/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.906 | 1226 | 400 |
| playwright | 88% (7/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.906 | 1216 | 400 |
| colly+md | 88% (7/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.900 | 1115 | 401 |
| markcrawl | 62% (5/8) | 88% (7/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 0.750 | 2348 | 400 |
| crawl4ai | 50% (4/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.656 | 1193 | 400 |
| crawl4ai-raw | 50% (4/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.656 | 1193 | 400 |
| scrapy+md | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 1531 | 394 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for postgres-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What data types does PostgreSQL support?** [cross-page]
*(expects URL containing: `datatype`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | www.postgresql.org/docs/current/extend-type-system | 0.654 | www.postgresql.org/docs/current/datatype.html | 0.638 | www.postgresql.org/docs/current/typeconv-overview. | 0.636 |
| crawl4ai | #1 | www.postgresql.org/docs/17/datatype.html | 0.696 | www.postgresql.org/docs/18/datatype.html | 0.696 | www.postgresql.org/docs/current/datatype.html | 0.696 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/datatype.html | 0.696 | www.postgresql.org/docs/17/datatype.html | 0.696 | www.postgresql.org/docs/current/datatype.html | 0.696 |
| scrapy+md | #1 | www.postgresql.org/docs/9.1/datatype-datetime.html | 0.615 | www.postgresql.org/docs/8.0/multibyte.html | 0.592 | www.postgresql.org/docs/9.2/multibyte.html | 0.576 |
| crawlee | #1 | www.postgresql.org/docs/18/datatype.html | 0.696 | www.postgresql.org/docs/current/datatype.html | 0.696 | www.postgresql.org/docs/17/datatype.html | 0.693 |
| colly+md | #1 | www.postgresql.org/docs/18/datatype.html | 0.696 | www.postgresql.org/docs/current/datatype.html | 0.696 | www.postgresql.org/docs/17/datatype.html | 0.693 |
| playwright | #1 | www.postgresql.org/docs/18/datatype.html | 0.696 | www.postgresql.org/docs/current/datatype.html | 0.696 | www.postgresql.org/docs/17/datatype.html | 0.693 |


**Q2: What is the SQL syntax for queries in PostgreSQL?** [conceptual]
*(expects URL containing: `sql-syntax`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #6 | www.postgresql.org/docs/current/sql.html | 0.637 | www.postgresql.org/docs/current/sql-commands.html | 0.615 | www.postgresql.org/docs/current/sql.html | 0.609 |
| crawl4ai | #4 | www.postgresql.org/docs/current/sql.html | 0.647 | www.postgresql.org/docs/18/sql.html | 0.647 | www.postgresql.org/docs/17/sql.html | 0.643 |
| crawl4ai-raw | #4 | www.postgresql.org/docs/18/sql.html | 0.647 | www.postgresql.org/docs/current/sql.html | 0.647 | www.postgresql.org/docs/17/sql.html | 0.643 |
| scrapy+md | miss | www.postgresql.org/docs/7.4/sql.html | 0.641 | www.postgresql.org/docs/7.2/biblio.html | 0.583 | www.postgresql.org/docs/7.1/biblio.html | 0.578 |
| crawlee | #4 | www.postgresql.org/docs/18/sql.html | 0.637 | www.postgresql.org/docs/current/sql.html | 0.637 | www.postgresql.org/docs/17/sql.html | 0.634 |
| colly+md | #5 | www.postgresql.org/docs/current/sql.html | 0.637 | www.postgresql.org/docs/18/sql.html | 0.637 | www.postgresql.org/docs/17/sql.html | 0.634 |
| playwright | #4 | www.postgresql.org/docs/18/sql.html | 0.637 | www.postgresql.org/docs/current/sql.html | 0.637 | www.postgresql.org/docs/17/sql.html | 0.634 |


**Q3: How do indexes work in PostgreSQL?** [conceptual]
*(expects URL containing: `indexes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/indexes-index-only | 0.628 | www.postgresql.org/docs/current/indexes-index-only | 0.616 | www.postgresql.org/docs/current/indexes-types.html | 0.611 |
| crawl4ai | #3 | www.postgresql.org/docs/18/indexam.html | 0.570 | www.postgresql.org/docs/current/indexam.html | 0.570 | www.postgresql.org/docs/18/indexes.html | 0.547 |
| crawl4ai-raw | #3 | www.postgresql.org/docs/18/indexam.html | 0.570 | www.postgresql.org/docs/current/indexam.html | 0.570 | www.postgresql.org/docs/18/indexes.html | 0.547 |
| scrapy+md | miss | www.postgresql.org/docs/7.4/sql-cluster.html | 0.542 | www.postgresql.org/docs/7.4/sql-reindex.html | 0.508 | www.postgresql.org/docs/7.4/sql-reindex.html | 0.502 |
| crawlee | #1 | www.postgresql.org/docs/current/indexes.html | 0.599 | www.postgresql.org/docs/18/indexes.html | 0.598 | www.postgresql.org/docs/17/indexes.html | 0.594 |
| colly+md | #1 | www.postgresql.org/docs/18/indexes.html | 0.599 | www.postgresql.org/docs/current/indexes.html | 0.598 | www.postgresql.org/docs/17/indexes.html | 0.594 |
| playwright | #1 | www.postgresql.org/docs/current/indexes.html | 0.599 | www.postgresql.org/docs/18/indexes.html | 0.599 | www.postgresql.org/docs/17/indexes.html | 0.594 |


**Q4: How does MVCC concurrency control work in PostgreSQL?** [conceptual]
*(expects URL containing: `mvcc`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/mvcc.html | 0.580 | www.postgresql.org/docs/current/mvcc-caveats.html | 0.562 | www.postgresql.org/docs/current/applevel-consisten | 0.560 |
| crawl4ai | #3 | www.postgresql.org/docs/current/glossary.html | 0.451 | www.postgresql.org/docs/18/glossary.html | 0.449 | www.postgresql.org/docs/18/mvcc.html | 0.444 |
| crawl4ai-raw | #3 | www.postgresql.org/docs/current/glossary.html | 0.451 | www.postgresql.org/docs/18/glossary.html | 0.449 | www.postgresql.org/docs/18/mvcc.html | 0.444 |
| scrapy+md | #1 | www.postgresql.org/docs/8.0/mvcc.html | 0.675 | www.postgresql.org/docs/8.0/mvcc.html | 0.549 | www.postgresql.org/docs/7.1/sql-set-transaction.ht | 0.451 |
| crawlee | #1 | www.postgresql.org/docs/18/mvcc.html | 0.578 | www.postgresql.org/docs/current/mvcc.html | 0.578 | www.postgresql.org/docs/17/mvcc.html | 0.572 |
| colly+md | #1 | www.postgresql.org/docs/current/mvcc.html | 0.578 | www.postgresql.org/docs/18/mvcc.html | 0.578 | www.postgresql.org/docs/17/mvcc.html | 0.572 |
| playwright | #1 | www.postgresql.org/docs/current/mvcc.html | 0.578 | www.postgresql.org/docs/18/mvcc.html | 0.578 | www.postgresql.org/docs/17/mvcc.html | 0.572 |


**Q5: How do transactions work in PostgreSQL?** [conceptual]
*(expects URL containing: `transactions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/plpgsql-transactio | 0.606 | www.postgresql.org/docs/current/glossary.html | 0.569 | www.postgresql.org/docs/current/transaction-id.htm | 0.561 |
| crawl4ai | #3 | www.postgresql.org/docs/current/reference.html | 0.567 | www.postgresql.org/docs/18/reference.html | 0.567 | www.postgresql.org/docs/current/transactions.html | 0.560 |
| crawl4ai-raw | #3 | www.postgresql.org/docs/current/reference.html | 0.567 | www.postgresql.org/docs/18/reference.html | 0.567 | www.postgresql.org/docs/18/transactions.html | 0.560 |
| scrapy+md | miss | www.postgresql.org/docs/7.4/sql-begin.html | 0.594 | www.postgresql.org/docs/8.0/mvcc.html | 0.574 | www.postgresql.org/docs/7.4/sql-begin.html | 0.568 |
| crawlee | #1 | www.postgresql.org/docs/18/transactions.html | 0.620 | www.postgresql.org/docs/current/transactions.html | 0.620 | www.postgresql.org/docs/17/tutorial.html | 0.583 |
| colly+md | #1 | www.postgresql.org/docs/current/transactions.html | 0.620 | www.postgresql.org/docs/18/tutorial.html | 0.583 | www.postgresql.org/docs/16/tutorial.html | 0.583 |
| playwright | #1 | www.postgresql.org/docs/18/transactions.html | 0.620 | www.postgresql.org/docs/current/transactions.html | 0.620 | www.postgresql.org/docs/current/tutorial.html | 0.583 |


**Q6: How do I set up logical replication in PostgreSQL?** [api-function]
*(expects URL containing: `logical-replication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.701 | www.postgresql.org/docs/current/logicaldecoding-ex | 0.578 | www.postgresql.org/docs/current/warm-standby.html | 0.572 |
| crawl4ai | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.706 | www.postgresql.org/docs/18/logical-replication.htm | 0.706 | www.postgresql.org/docs/17/logical-replication.htm | 0.701 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/18/logical-replication.htm | 0.706 | www.postgresql.org/docs/current/logical-replicatio | 0.706 | www.postgresql.org/docs/17/logical-replication.htm | 0.701 |
| scrapy+md | miss | www.postgresql.org/docs/9.2/runtime-config-logging | 0.474 | www.postgresql.org/docs/9.1/upgrading.html | 0.465 | www.postgresql.org/docs/9.1/upgrading.html | 0.448 |
| crawlee | #1 | www.postgresql.org/docs/current/logical-replicatio | 0.696 | www.postgresql.org/docs/18/logical-replication.htm | 0.695 | www.postgresql.org/docs/18/logical-replication.htm | 0.688 |
| colly+md | #1 | www.postgresql.org/docs/18/logical-replication.htm | 0.696 | www.postgresql.org/docs/current/logical-replicatio | 0.695 | www.postgresql.org/docs/current/logical-replicatio | 0.688 |
| playwright | #1 | www.postgresql.org/docs/18/logical-replication.htm | 0.696 | www.postgresql.org/docs/current/logical-replicatio | 0.696 | www.postgresql.org/docs/current/logical-replicatio | 0.688 |


**Q7: What built-in functions and operators are available in PostgreSQL?** [cross-page]
*(expects URL containing: `functions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | www.postgresql.org/docs/current/plpgsql-overview.h | 0.641 | www.postgresql.org/docs/current/tutorial-agg.html | 0.632 | www.postgresql.org/docs/current/functions.html | 0.623 |
| crawl4ai | #1 | www.postgresql.org/docs/17/functions.html | 0.658 | www.postgresql.org/docs/current/functions.html | 0.658 | www.postgresql.org/docs/18/functions.html | 0.658 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/17/functions.html | 0.658 | www.postgresql.org/docs/18/functions.html | 0.658 | www.postgresql.org/docs/current/functions.html | 0.658 |
| scrapy+md | #1 | www.postgresql.org/docs/8.1/functions.html | 0.720 | www.postgresql.org/docs/7.3/functions.html | 0.716 | www.postgresql.org/docs/7.3/functions.html | 0.667 |
| crawlee | #1 | www.postgresql.org/docs/current/functions.html | 0.706 | www.postgresql.org/docs/18/functions.html | 0.706 | www.postgresql.org/docs/17/functions.html | 0.700 |
| colly+md | #1 | www.postgresql.org/docs/18/functions.html | 0.706 | www.postgresql.org/docs/current/functions.html | 0.706 | www.postgresql.org/docs/16/functions.html | 0.702 |
| playwright | #1 | www.postgresql.org/docs/18/functions.html | 0.706 | www.postgresql.org/docs/current/functions.html | 0.706 | www.postgresql.org/docs/17/functions.html | 0.700 |


**Q8: How do I use full text search in PostgreSQL?** [api-function]
*(expects URL containing: `textsearch`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.postgresql.org/docs/current/textsearch-psql.ht | 0.588 | www.postgresql.org/docs/current/textsearch-control | 0.587 | www.postgresql.org/docs/current/textsearch-configu | 0.548 |
| crawl4ai | #1 | www.postgresql.org/docs/18/textsearch.html | 0.545 | www.postgresql.org/docs/current/textsearch.html | 0.545 | www.postgresql.org/docs/17/textsearch.html | 0.544 |
| crawl4ai-raw | #1 | www.postgresql.org/docs/current/textsearch.html | 0.545 | www.postgresql.org/docs/18/textsearch.html | 0.545 | www.postgresql.org/docs/17/textsearch.html | 0.544 |
| scrapy+md | miss | www.postgresql.org/docs/8.4/tsearch2.html | 0.505 | www.postgresql.org/docs/8.3/tsearch2.html | 0.504 | www.postgresql.org/docs/9.6/tsearch2.html | 0.499 |
| crawlee | #1 | www.postgresql.org/docs/current/textsearch.html | 0.701 | www.postgresql.org/docs/18/textsearch.html | 0.701 | www.postgresql.org/docs/17/textsearch.html | 0.697 |
| colly+md | #1 | www.postgresql.org/docs/18/textsearch.html | 0.701 | www.postgresql.org/docs/current/textsearch.html | 0.701 | www.postgresql.org/docs/17/textsearch.html | 0.698 |
| playwright | #1 | www.postgresql.org/docs/current/textsearch.html | 0.701 | www.postgresql.org/docs/18/textsearch.html | 0.701 | www.postgresql.org/docs/17/textsearch.html | 0.698 |


</details>

## mdn-css

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| playwright | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.875 | 4168 | 300 |
| crawlee | 75% (6/8) | 75% (6/8) | 75% (6/8) | 88% (7/8) | 88% (7/8) | 0.768 | 3891 | 300 |
| crawl4ai | 62% (5/8) | 75% (6/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.713 | 3864 | 300 |
| crawl4ai-raw | 62% (5/8) | 75% (6/8) | 88% (7/8) | 88% (7/8) | 88% (7/8) | 0.713 | 3864 | 300 |
| markcrawl | 62% (5/8) | 75% (6/8) | 75% (6/8) | 75% (6/8) | 75% (6/8) | 0.688 | 1006 | 300 |
| colly+md | 50% (4/8) | 50% (4/8) | 62% (5/8) | 62% (5/8) | 75% (6/8) | 0.540 | 4190 | 289 |
| scrapy+md | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.125 | 621 | 300 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for mdn-css</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How does the CSS display property work?** [api-function]
*(expects URL containing: `CSS/Reference/Properties/display`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ro | 0.568 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.564 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Pr | 0.563 |
| crawl4ai | #5 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.588 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.583 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.579 |
| crawl4ai-raw | #5 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.588 | developer.mozilla.org/en-US/docs/Web/CSS/Guides | 0.583 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.579 |
| scrapy+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.596 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.546 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.523 |
| crawlee | #7 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.571 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.568 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Co | 0.565 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.607 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.599 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.581 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.581 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.573 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Sy | 0.571 |


**Q2: How do I use flexbox for page layout?** [conceptual]
*(expects URL containing: `Flexible_box_layout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.612 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.591 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.586 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.613 | developer.mozilla.org/en-US/docs/Web/CSS/How_to/La | 0.601 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.594 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.613 | developer.mozilla.org/en-US/docs/Web/CSS/How_to/La | 0.601 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.594 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.489 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.422 | developer.mozilla.org/en-US/docs/Web/CSS | 0.412 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.622 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.610 | developer.mozilla.org/en-US/docs/Web/CSS/How_to/La | 0.604 |
| colly+md | #15 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.622 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.616 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.609 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.622 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.622 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.616 |


**Q3: How does CSS Grid layout work?** [conceptual]
*(expects URL containing: `Grid_layout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.720 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.703 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.630 |
| crawl4ai | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.682 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.658 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.656 |
| crawl4ai-raw | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.682 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.658 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.656 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.534 | developer.mozilla.org/en-US/docs/Web/CSS | 0.512 | developer.mozilla.org/en-US/docs/Web/CSS | 0.456 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.656 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.650 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.647 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.678 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.671 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.656 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.667 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.656 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Gr | 0.656 |


**Q4: What is the CSS box model?** [conceptual]
*(expects URL containing: `Box_model`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.640 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.637 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Fl | 0.627 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.647 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.629 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.648 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.632 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.629 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.535 | developer.mozilla.org/en-US/docs/Web/CSS | 0.462 | developer.mozilla.org/en-US/docs/Web/CSS | 0.459 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.678 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.627 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.623 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.652 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.652 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.648 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.678 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.627 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.623 |


**Q5: How does the CSS margin property work?** [api-function]
*(expects URL containing: `Reference/Properties/margin`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.641 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.625 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.614 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.627 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.557 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.542 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.627 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.557 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.542 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.449 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.440 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.418 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.631 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.566 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.548 |
| colly+md | #4 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.563 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.541 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.538 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.631 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Bo | 0.566 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Di | 0.564 |


**Q6: How does CSS specificity determine which rules win?** [conceptual]
*(expects URL containing: `Cascade/Specificity`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.530 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ne | 0.527 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.516 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.675 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.674 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.665 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.675 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.674 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.665 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.442 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.433 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cu | 0.427 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.677 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.647 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.620 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.621 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.620 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.618 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.702 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.621 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ca | 0.620 |


**Q7: How does the :hover pseudo-class work in CSS?** [api-function]
*(expects URL containing: `Selectors/:hover`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.700 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.549 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.545 |
| crawl4ai | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.579 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.556 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.547 |
| crawl4ai-raw | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.579 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.556 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.547 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/API/CSSFuncti | 0.423 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ea | 0.422 | developer.mozilla.org/en-US/docs/Web/HTML/Referenc | 0.420 |
| crawlee | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.544 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.540 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.536 |
| colly+md | miss | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.649 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Ps | 0.571 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.547 |
| playwright | miss | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Se | 0.552 | developer.mozilla.org/en-US/docs/Web/CSS/Reference | 0.551 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/Tr | 0.549 |


**Q8: How do I create CSS animations?** [conceptual]
*(expects URL containing: `Animations/Using`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.694 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.598 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.596 |
| crawl4ai | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.664 | developer.mozilla.org/en-US/docs/Web/API/Web_Anima | 0.614 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.606 |
| crawl4ai-raw | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.664 | developer.mozilla.org/en-US/docs/Web/API/Web_Anima | 0.614 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.606 |
| scrapy+md | miss | developer.mozilla.org/en-US/docs/Web/CSS | 0.486 | developer.mozilla.org/en-US/docs/Web/CSS | 0.480 | developer.mozilla.org/en-US/docs/Learn_web_develop | 0.465 |
| crawlee | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.664 | developer.mozilla.org/en-US/docs/Web/API/Web_Anima | 0.612 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.604 |
| colly+md | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.630 | developer.mozilla.org/en-US/docs/Web/API/Web/Anima | 0.611 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.593 |
| playwright | #1 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.664 | developer.mozilla.org/en-US/docs/Web/API/Web_Anima | 0.611 | developer.mozilla.org/en-US/docs/Web/CSS/Guides/An | 0.609 |


</details>

## rust-book

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 75% (6/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.875 | 1287 | 112 |
| crawl4ai | 50% (4/8) | 75% (6/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 0.650 | 2702 | 200 |
| crawl4ai-raw | 50% (4/8) | 75% (6/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 0.650 | 2702 | 200 |
| crawlee | 38% (3/8) | 75% (6/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 0.608 | 2829 | 200 |
| playwright | 38% (3/8) | 75% (6/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 0.594 | 2829 | 200 |
| scrapy+md | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.128 | 2978 | 199 |
| colly+md | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.125 | 1976 | 54 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for rust-book</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What is ownership in Rust?** [conceptual]
*(expects URL containing: `ch04-01-what-is-ownership`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch04-01-what-is-ownership.h | 0.767 | doc.rust-lang.org/book/ch04-00-understanding-owner | 0.728 | doc.rust-lang.org/book/print.html | 0.651 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch04-00-understandin | 0.655 | doc.rust-lang.org/book/ch04-00-understanding-owner | 0.655 | doc.rust-lang.org/book/ch04-01-what-is-ownership.h | 0.646 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch04-00-understandin | 0.655 | doc.rust-lang.org/book/ch04-00-understanding-owner | 0.655 | doc.rust-lang.org/book/ch04-01-what-is-ownership.h | 0.646 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.635 | doc.rust-lang.org/stable/book/print.html | 0.635 | doc.rust-lang.org/stable/book/print.html | 0.616 |
| crawlee | #1 | doc.rust-lang.org/stable/book/ch04-01-what-is-owne | 0.672 | doc.rust-lang.org/book/ch04-01-what-is-ownership.h | 0.672 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.635 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.635 | doc.rust-lang.org/stable/book/print.html | 0.635 | doc.rust-lang.org/book/print.html | 0.616 |
| playwright | #1 | doc.rust-lang.org/book/ch04-01-what-is-ownership.h | 0.672 | doc.rust-lang.org/stable/book/ch04-01-what-is-owne | 0.672 | doc.rust-lang.org/book/ch16-03-shared-state.html | 0.635 |


**Q2: How do references and borrowing work in Rust?** [conceptual]
*(expects URL containing: `ch04-02-references-and-borrowing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.636 | doc.rust-lang.org/book/ch04-02-references-and-borr | 0.636 | doc.rust-lang.org/book/ch10-03-lifetime-syntax.htm | 0.634 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch04-02-references-a | 0.630 | doc.rust-lang.org/book/print.html | 0.628 | doc.rust-lang.org/book/ch04-02-references-and-borr | 0.628 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch04-02-references-a | 0.630 | doc.rust-lang.org/book/print.html | 0.628 | doc.rust-lang.org/book/ch04-02-references-and-borr | 0.628 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.618 | doc.rust-lang.org/stable/book/print.html | 0.618 | doc.rust-lang.org/nomicon/lifetimes.html | 0.617 |
| crawlee | #5 | doc.rust-lang.org/book/ch10-03-lifetime-syntax.htm | 0.618 | doc.rust-lang.org/book/print.html | 0.618 | doc.rust-lang.org/stable/book/ch10-03-lifetime-syn | 0.618 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.618 | doc.rust-lang.org/stable/book/print.html | 0.618 | doc.rust-lang.org/stable/book/print.html | 0.609 |
| playwright | #4 | doc.rust-lang.org/book/print.html | 0.618 | doc.rust-lang.org/stable/book/ch10-03-lifetime-syn | 0.618 | doc.rust-lang.org/book/ch10-03-lifetime-syntax.htm | 0.618 |


**Q3: How do I define structs in Rust?** [api-function]
*(expects URL containing: `ch05-01-defining-structs`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch05-00-structs.html | 0.675 | doc.rust-lang.org/book/print.html | 0.629 | doc.rust-lang.org/book/ch05-02-example-structs.htm | 0.623 |
| crawl4ai | #6 | doc.rust-lang.org/book/print.html | 0.653 | doc.rust-lang.org/book/print.html | 0.633 | doc.rust-lang.org/stable/book/ch05-03-method-synta | 0.618 |
| crawl4ai-raw | #6 | doc.rust-lang.org/book/print.html | 0.653 | doc.rust-lang.org/book/print.html | 0.633 | doc.rust-lang.org/stable/book/ch05-03-method-synta | 0.618 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.640 | doc.rust-lang.org/book/print.html | 0.640 | doc.rust-lang.org/stable/book/print.html | 0.628 |
| crawlee | #6 | doc.rust-lang.org/book/print.html | 0.640 | doc.rust-lang.org/book/print.html | 0.628 | doc.rust-lang.org/stable/book/ch05-03-method-synta | 0.627 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.640 | doc.rust-lang.org/stable/book/print.html | 0.640 | doc.rust-lang.org/book/print.html | 0.628 |
| playwright | #6 | doc.rust-lang.org/book/print.html | 0.640 | doc.rust-lang.org/book/print.html | 0.628 | doc.rust-lang.org/book/ch05-03-method-syntax.html | 0.627 |


**Q4: How do enums work in Rust?** [conceptual]
*(expects URL containing: `ch06-01-defining-an-enum`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.648 | doc.rust-lang.org/book/print.html | 0.606 | doc.rust-lang.org/book/print.html | 0.605 |
| crawl4ai | #2 | doc.rust-lang.org/book/print.html | 0.681 | doc.rust-lang.org/stable/book/ch06-01-defining-an- | 0.635 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.635 |
| crawl4ai-raw | #2 | doc.rust-lang.org/book/print.html | 0.681 | doc.rust-lang.org/stable/book/ch06-01-defining-an- | 0.635 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.635 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.680 | doc.rust-lang.org/stable/book/print.html | 0.680 | doc.rust-lang.org/stable/book/print.html | 0.603 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.680 | doc.rust-lang.org/stable/book/ch06-01-defining-an- | 0.642 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.642 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.680 | doc.rust-lang.org/stable/book/print.html | 0.680 | doc.rust-lang.org/stable/book/print.html | 0.603 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.680 | doc.rust-lang.org/stable/book/ch06-01-defining-an- | 0.642 | doc.rust-lang.org/book/ch06-01-defining-an-enum.ht | 0.642 |


**Q5: How do I use generics in Rust?** [conceptual]
*(expects URL containing: `ch10-01-syntax`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch10-00-generics.html | 0.633 | doc.rust-lang.org/book/print.html | 0.629 | doc.rust-lang.org/book/print.html | 0.620 |
| crawl4ai | #3 | doc.rust-lang.org/book/print.html | 0.649 | doc.rust-lang.org/book/print.html | 0.631 | doc.rust-lang.org/book/ch10-01-syntax.html | 0.631 |
| crawl4ai-raw | #3 | doc.rust-lang.org/book/print.html | 0.649 | doc.rust-lang.org/book/print.html | 0.631 | doc.rust-lang.org/book/ch10-01-syntax.html | 0.631 |
| scrapy+md | miss | doc.rust-lang.org/book/print.html | 0.629 | doc.rust-lang.org/stable/book/print.html | 0.629 | doc.rust-lang.org/stable/book/print.html | 0.619 |
| crawlee | #1 | doc.rust-lang.org/stable/book/ch10-01-syntax.html | 0.644 | doc.rust-lang.org/book/ch10-01-syntax.html | 0.644 | doc.rust-lang.org/book/print.html | 0.629 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.629 | doc.rust-lang.org/stable/book/print.html | 0.629 | doc.rust-lang.org/book/print.html | 0.619 |
| playwright | #1 | doc.rust-lang.org/stable/book/ch10-01-syntax.html | 0.644 | doc.rust-lang.org/book/ch10-01-syntax.html | 0.644 | doc.rust-lang.org/book/print.html | 0.629 |


**Q6: What are traits in Rust and how do I define them?** [conceptual]
*(expects URL containing: `ch10-02-traits`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | doc.rust-lang.org/book/print.html | 0.613 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.610 | doc.rust-lang.org/book/print.html | 0.573 |
| crawl4ai | #1 | doc.rust-lang.org/stable/book/ch10-02-traits.html | 0.699 | doc.rust-lang.org/book/ch10-02-traits.html | 0.699 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.663 |
| crawl4ai-raw | #1 | doc.rust-lang.org/stable/book/ch10-02-traits.html | 0.699 | doc.rust-lang.org/book/ch10-02-traits.html | 0.699 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.663 |
| scrapy+md | #1 | doc.rust-lang.org/reference/items/traits.html | 0.585 | doc.rust-lang.org/stable/book/print.html | 0.574 | doc.rust-lang.org/book/print.html | 0.574 |
| crawlee | #1 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.655 | doc.rust-lang.org/stable/book/ch10-02-traits.html | 0.623 | doc.rust-lang.org/book/ch10-02-traits.html | 0.623 |
| colly+md | #1 | doc.rust-lang.org/reference/items/traits.html#dyn- | 0.616 | doc.rust-lang.org/stable/book/print.html | 0.574 | doc.rust-lang.org/book/print.html | 0.574 |
| playwright | #1 | doc.rust-lang.org/book/ch20-02-advanced-traits.htm | 0.655 | doc.rust-lang.org/stable/book/ch10-02-traits.html | 0.623 | doc.rust-lang.org/book/ch10-02-traits.html | 0.623 |


**Q7: How do closures work in Rust?** [conceptual]
*(expects URL containing: `ch13-01-closures`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch13-01-closures.html | 0.760 | doc.rust-lang.org/book/print.html | 0.625 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.625 |
| crawl4ai | #1 | doc.rust-lang.org/book/ch13-01-closures.html | 0.629 | doc.rust-lang.org/book/print.html | 0.629 | doc.rust-lang.org/book/ch13-01-closures.html | 0.619 |
| crawl4ai-raw | #1 | doc.rust-lang.org/book/ch13-01-closures.html | 0.629 | doc.rust-lang.org/book/print.html | 0.629 | doc.rust-lang.org/book/ch13-01-closures.html | 0.619 |
| scrapy+md | miss | doc.rust-lang.org/stable/book/print.html | 0.661 | doc.rust-lang.org/book/print.html | 0.661 | doc.rust-lang.org/stable/book/print.html | 0.623 |
| crawlee | #2 | doc.rust-lang.org/book/print.html | 0.661 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.626 | doc.rust-lang.org/book/ch13-01-closures.html | 0.623 |
| colly+md | miss | doc.rust-lang.org/book/print.html | 0.661 | doc.rust-lang.org/stable/book/print.html | 0.661 | doc.rust-lang.org/book/print.html | 0.623 |
| playwright | #2 | doc.rust-lang.org/book/print.html | 0.661 | doc.rust-lang.org/book/ch20-04-advanced-functions- | 0.626 | doc.rust-lang.org/book/ch13-01-closures.html | 0.623 |


**Q8: How do I handle errors with Result in Rust?** [conceptual]
*(expects URL containing: `ch09`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | doc.rust-lang.org/book/ch09-02-recoverable-errors- | 0.630 | doc.rust-lang.org/book/ch09-00-error-handling.html | 0.627 | doc.rust-lang.org/book/print.html | 0.592 |
| crawl4ai | #5 | doc.rust-lang.org/std/result/enum.Result.html | 0.656 | doc.rust-lang.org/book/print.html | 0.614 | doc.rust-lang.org/std/result/enum.Result.html | 0.586 |
| crawl4ai-raw | #5 | doc.rust-lang.org/std/result/enum.Result.html | 0.656 | doc.rust-lang.org/book/print.html | 0.614 | doc.rust-lang.org/std/result/enum.Result.html | 0.586 |
| scrapy+md | #39 | doc.rust-lang.org/std/result/enum.Result.html | 0.621 | doc.rust-lang.org/book/print.html | 0.570 | doc.rust-lang.org/stable/book/print.html | 0.570 |
| crawlee | #2 | doc.rust-lang.org/std/result/enum.Result.html | 0.642 | doc.rust-lang.org/stable/book/ch09-03-to-panic-or- | 0.571 | doc.rust-lang.org/book/print.html | 0.570 |
| colly+md | miss | doc.rust-lang.org/std/result/enum.Result.html#meth | 0.619 | doc.rust-lang.org/std/result/enum.Result.html | 0.619 | doc.rust-lang.org/book/print.html | 0.570 |
| playwright | #3 | doc.rust-lang.org/std/result/enum.Result.html | 0.642 | doc.rust-lang.org/book/print.html | 0.570 | doc.rust-lang.org/book/ch09-03-to-panic-or-not-to- | 0.570 |


</details>

## smittenkitchen

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 50% (4/8) | 62% (5/8) | 62% (5/8) | 62% (5/8) | 62% (5/8) | 0.566 | 10115 | 200 |
| colly+md | 38% (3/8) | 50% (4/8) | 50% (4/8) | 62% (5/8) | 62% (5/8) | 0.458 | 3708 | 199 |
| crawlee | 38% (3/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 62% (5/8) | 0.446 | 4167 | 203 |
| playwright | 25% (2/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.312 | 3029 | 200 |
| scrapy+md | 25% (2/8) | 25% (2/8) | 25% (2/8) | 25% (2/8) | 25% (2/8) | 0.250 | 18860 | 138 |
| crawl4ai | 12% (1/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.229 | 773 | 200 |
| crawl4ai-raw | 12% (1/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.229 | 773 | 200 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for smittenkitchen</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do you make world peace cookies?** [factual-lookup]
*(expects URL containing: `world-peace-cookies`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2007/01/world-peace-cookies/ | 0.674 | smittenkitchen.com/2007/01/world-peace-cookies/ | 0.674 | smittenkitchen.com/2007/01/world-peace-cookies/ | 0.673 |
| crawl4ai | miss | smittenkitchen.com/./recipes/ingredient/peanut-but | 0.337 | smittenkitchen.com/about/faq/ | 0.335 | smittenkitchen.com/cooking-conversions/ | 0.334 |
| crawl4ai-raw | miss | smittenkitchen.com/./recipes/ingredient/peanut-but | 0.337 | smittenkitchen.com/about/faq/ | 0.335 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.335 |
| scrapy+md | miss | smittenkitchen.com/2007/02/knotted-and-stacked-dis | 0.414 | smittenkitchen.com/2007/02/knotted-and-stacked-dis | 0.414 | smittenkitchen.com/2007/02/knotted-and-stacked-dis | 0.414 |
| crawlee | miss | smittenkitchen.com/?random&timestamp=1777919490717 | 0.423 | smittenkitchen.com/?random&timestamp=1777919490717 | 0.416 | smittenkitchen.com/?random&timestamp=1777919490717 | 0.416 |
| colly+md | miss | smittenkitchen.com/2022/04/lemon-cream-meringues/ | 0.366 | smittenkitchen.com/2025/05/one-pan-ditalini-and-pe | 0.360 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.359 |
| playwright | miss | smittenkitchen.com/events/ | 0.346 | smittenkitchen.com/events/ | 0.330 | smittenkitchen.com/about/faq/ | 0.328 |


**Q2: What's the recipe for miso chicken and rice?** [factual-lookup]
*(expects URL containing: `miso-chicken-and-rice`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.688 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.640 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.617 |
| crawl4ai | miss | smittenkitchen.com/ | 0.545 | smittenkitchen.com/./recipes/ingredient/grain/?for | 0.362 | smittenkitchen.com/./recipes/ingredient/meat/chick | 0.356 |
| crawl4ai-raw | miss | smittenkitchen.com/ | 0.545 | smittenkitchen.com/./recipes/ingredient/grain/?for | 0.361 | smittenkitchen.com/./recipes/ingredient/meat/chick | 0.357 |
| scrapy+md | #1 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.636 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.615 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.609 |
| crawlee | #1 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.636 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.632 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.624 |
| colly+md | #1 | smittenkitchen.com/2026/02/miso-chicken-and-rice/# | 0.636 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.636 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.615 |
| playwright | miss | smittenkitchen.com/recipes/ingredient/grain/?forma | 0.431 | smittenkitchen.com/recipes/ingredient/meat/chicken | 0.430 | smittenkitchen.com/ | 0.416 |


**Q3: How do I make ultimate banana bread?** [factual-lookup]
*(expects URL containing: `ultimate-banana-bread`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.679 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.664 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.644 |
| crawl4ai | miss | smittenkitchen.com/./recipes/fruit/bananas/?format | 0.383 | smittenkitchen.com/about/faq/ | 0.368 | smittenkitchen.com/cooking-conversions/ | 0.357 |
| crawl4ai-raw | miss | smittenkitchen.com/./recipes/fruit/bananas/?format | 0.384 | smittenkitchen.com/about/faq/ | 0.368 | smittenkitchen.com/cooking-conversions/ | 0.358 |
| scrapy+md | #1 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.720 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.679 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.675 |
| crawlee | #1 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.720 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.676 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.673 |
| colly+md | #1 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.720 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.679 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.675 |
| playwright | miss | smittenkitchen.com/recipes/fruit/bananas/?format=p | 0.427 | smittenkitchen.com/recipes/course/muffin/?format=p | 0.363 | smittenkitchen.com/recipes/sweets/everyday-cakes/? | 0.342 |


**Q4: What's the skillet-baked macaroni and cheese recipe?** [factual-lookup]
*(expects URL containing: `skillet-baked-macaroni-and-cheese`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/2024/05/black-bean-and-vegetabl | 0.481 | smittenkitchen.com/2011/03/whole-wheat-goldfish-cr | 0.474 | smittenkitchen.com/2025/11/crunchy-brown-butter-ba | 0.446 |
| crawl4ai | miss | smittenkitchen.com/./recipes/ingredient/cheese/?fo | 0.375 | smittenkitchen.com/./recipes/method/casserole/?for | 0.372 | smittenkitchen.com/./recipes/method/casserole/?for | 0.365 |
| crawl4ai-raw | miss | smittenkitchen.com/./recipes/ingredient/cheese/?fo | 0.375 | smittenkitchen.com/./recipes/method/casserole/?for | 0.372 | smittenkitchen.com/./recipes/method/casserole/?for | 0.363 |
| scrapy+md | miss | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.408 | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.408 | smittenkitchen.com/2012/02/lasagna-bolognese/ | 0.408 |
| crawlee | miss | smittenkitchen.com/?random&timestamp=1777919490717 | 0.420 | smittenkitchen.com/./recipes/ingredient/cheese/?fo | 0.415 | smittenkitchen.com/2025/05/one-pan-ditalini-and-pe | 0.403 |
| colly+md | miss | smittenkitchen.com/recipes/ingredient/cheese/?form | 0.391 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.390 | smittenkitchen.com/2026/01/simple-crispy-pan-pizza | 0.390 |
| playwright | miss | smittenkitchen.com/recipes/ingredient/cheese/?form | 0.393 | smittenkitchen.com/recipes/course/pasta/?format=ph | 0.385 | smittenkitchen.com/recipes/method/casserole/?forma | 0.368 |


**Q5: What vegan recipes are available on Smitten Kitchen?** [cross-page]
*(expects URL containing: `diet/vegan`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | smittenkitchen.com/books/ | 0.558 | smittenkitchen.com/2014/01/warm-lentil-and-potato- | 0.557 | smittenkitchen.com/2020/10/morning-glory-breakfast | 0.552 |
| crawl4ai | #2 | smittenkitchen.com/recipes/ | 0.629 | smittenkitchen.com/./recipes/diet/vegan/?format=ph | 0.618 | smittenkitchen.com/./recipes/ingredient/tofu/?form | 0.614 |
| crawl4ai-raw | #2 | smittenkitchen.com/recipes/ | 0.618 | smittenkitchen.com/./recipes/diet/vegan/?format=ph | 0.618 | smittenkitchen.com/./recipes/ingredient/tofu/?form | 0.614 |
| scrapy+md | miss | smittenkitchen.com/2017/09/pizza-beans/ | 0.518 | smittenkitchen.com/recipes/ | 0.508 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.506 |
| crawlee | #1 | smittenkitchen.com/./recipes/diet/vegan/?format=ph | 0.606 | smittenkitchen.com/./recipes/ingredient/pantry/?fo | 0.599 | smittenkitchen.com/about/ | 0.598 |
| colly+md | #1 | smittenkitchen.com/recipes/diet/vegan/?format=phot | 0.633 | smittenkitchen.com/recipes/diet/vegetarian/?format | 0.611 | smittenkitchen.com/recipes/diet/vegetarian/ | 0.611 |
| playwright | #1 | smittenkitchen.com/recipes/diet/vegan/?format=phot | 0.629 | smittenkitchen.com/recipes/diet/vegetarian/?format | 0.608 | smittenkitchen.com/recipes/ingredient/tofu/?format | 0.599 |


**Q6: Show me cookie recipes** [cross-page]
*(expects URL containing: `sweets/cookie`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | smittenkitchen.com/2008/12/pecan-sandies/ | 0.553 | smittenkitchen.com/2007/12/peanut-butter-cookies/ | 0.552 | smittenkitchen.com/2007/12/peanut-butter-cookies/ | 0.550 |
| crawl4ai | #1 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.486 | smittenkitchen.com/./recipes/ingredient/brown-butt | 0.469 | smittenkitchen.com/./recipes/sweets/doughnut/?form | 0.469 |
| crawl4ai-raw | #1 | smittenkitchen.com/./recipes/sweets/cookie/?format | 0.487 | smittenkitchen.com/./recipes/ingredient/brown-butt | 0.471 | smittenkitchen.com/./recipes/sweets/doughnut/?form | 0.469 |
| scrapy+md | miss | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.529 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.529 | smittenkitchen.com/2012/08/my-favorite-brownies/?r | 0.529 |
| crawlee | #14 | smittenkitchen.com/?random&timestamp=1777919490717 | 0.524 | smittenkitchen.com/?random&timestamp=1777919490717 | 0.508 | smittenkitchen.com/?random&timestamp=1777919490717 | 0.508 |
| colly+md | #6 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.507 | smittenkitchen.com/2022/03/castle-breakfast/ | 0.491 | smittenkitchen.com/2026/02/banana-chocolate-chip-c | 0.491 |
| playwright | #1 | smittenkitchen.com/recipes/sweets/cookie/?format=p | 0.486 | smittenkitchen.com/recipes/holiday/food-gifts/?for | 0.448 | smittenkitchen.com/recipes/sweets/cake/?format=pho | 0.445 |


**Q7: How do you make pumpkin basque cheesecake?** [factual-lookup]
*(expects URL containing: `pumpkin-basque-cheesecake`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | smittenkitchen.com/2025/11/pumpkin-basque-cheeseca | 0.728 | smittenkitchen.com/2025/11/pumpkin-basque-cheeseca | 0.723 | smittenkitchen.com/2025/11/pumpkin-basque-cheeseca | 0.716 |
| crawl4ai | miss | smittenkitchen.com/./recipes/season/fall/?format=p | 0.360 | smittenkitchen.com/./recipes/sweets/cake/?format=p | 0.355 | smittenkitchen.com/./recipes/holiday/thanksgiving/ | 0.352 |
| crawl4ai-raw | miss | smittenkitchen.com/./recipes/season/fall/?format=p | 0.360 | smittenkitchen.com/./recipes/sweets/cake/?format=p | 0.356 | smittenkitchen.com/./recipes/holiday/thanksgiving/ | 0.351 |
| scrapy+md | miss | smittenkitchen.com/2010/01/best-cocoa-brownies/?re | 0.483 | smittenkitchen.com/2010/01/best-cocoa-brownies/?re | 0.483 | smittenkitchen.com/2010/01/best-cocoa-brownies/?re | 0.483 |
| crawlee | miss | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.419 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.404 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.404 |
| colly+md | miss | smittenkitchen.com/recipes/vegetable/winter-squash | 0.477 | smittenkitchen.com/2025/12/winter-cabbage-salad-wi | 0.474 | smittenkitchen.com/2020/03/ultimate-banana-bread/ | 0.419 |
| playwright | miss | smittenkitchen.com/recipes/holiday/thanksgiving/?f | 0.394 | smittenkitchen.com/recipes/season/fall/?format=pho | 0.378 | smittenkitchen.com/recipes/sweets/cake/?format=pho | 0.367 |


**Q8: What recipes are good for winter?** [cross-page]
*(expects URL containing: `season/winter`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #39 | smittenkitchen.com/2013/01/lentil-soup-with-sausag | 0.545 | smittenkitchen.com/2007/11/curried-lentils-and-swe | 0.524 | smittenkitchen.com/2013/01/lentil-soup-with-sausag | 0.520 |
| crawl4ai | #3 | smittenkitchen.com/ | 0.465 | smittenkitchen.com/ | 0.460 | smittenkitchen.com/./recipes/season/winter/?format | 0.458 |
| crawl4ai-raw | #3 | smittenkitchen.com/ | 0.465 | smittenkitchen.com/ | 0.460 | smittenkitchen.com/./recipes/season/winter/?format | 0.458 |
| scrapy+md | miss | smittenkitchen.com/recipes/ | 0.493 | smittenkitchen.com/recipes/ | 0.479 | smittenkitchen.com/2012/02/lasagna-bolognese/?repl | 0.462 |
| crawlee | #2 | smittenkitchen.com/ | 0.527 | smittenkitchen.com/./recipes/season/winter/?format | 0.479 | smittenkitchen.com/2026/02/miso-chicken-and-rice/ | 0.476 |
| colly+md | #2 | smittenkitchen.com/ | 0.527 | smittenkitchen.com/recipes/season/winter/?format=p | 0.508 | smittenkitchen.com/recipes/vegetable/winter-squash | 0.501 |
| playwright | #2 | smittenkitchen.com/ | 0.527 | smittenkitchen.com/recipes/season/winter/?format=p | 0.510 | smittenkitchen.com/recipes/method/freezer-friendly | 0.476 |


</details>

## ikea

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| playwright | 50% (4/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 50% (4/8) | 0.500 | 3308 | 200 |
| crawlee | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 4610 | 203 |
| colly+md | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 2942 | 200 |
| crawl4ai | 25% (2/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.312 | 1622 | 200 |
| crawl4ai-raw | 25% (2/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.292 | 1554 | 200 |
| scrapy+md | 25% (2/8) | 25% (2/8) | 25% (2/8) | 25% (2/8) | 25% (2/8) | 0.250 | 1107 | 194 |
| markcrawl | 0% (0/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.042 | 928 | 200 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for ikea</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How much does the MALM bed frame cost at IKEA?** [factual-lookup]
*(expects URL containing: `malm-bed-frame`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/customer-service/product-suppor | 0.532 | www.ikea.com/us/en/rooms/bedroom/ | 0.519 | www.ikea.com/us/en/customer-service/product-suppor | 0.514 |
| crawl4ai | miss | www.ikea.com/us/en/p/malm-high-bed-frame-2-storage | 0.650 | www.ikea.com/us/en/p/malm-high-bed-frame-2-storage | 0.644 | www.ikea.com/us/en/p/malm-high-bed-frame-2-storage | 0.642 |
| crawl4ai-raw | miss | www.ikea.com/us/en/cat/beds-bm003/ | 0.603 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.600 | www.ikea.com/us/en/cat/storklinta-series-700569/ | 0.585 |
| scrapy+md | miss | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.532 | www.ikea.com/us/en/cat/hemnes-bedroom-series-58619 | 0.513 | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.511 |
| crawlee | miss | www.ikea.com/us/en/cat/beds-bm003/ | 0.636 | www.ikea.com/us/en/p/malm-high-bed-frame-2-storage | 0.635 | www.ikea.com/us/en/cat/beds-bm003/ | 0.632 |
| colly+md | miss | www.ikea.com/us/en/cat/beds-bm003/ | 0.636 | www.ikea.com/us/en/cat/beds-with-mattresses-includ | 0.634 | www.ikea.com/us/en/cat/beds-bm003/ | 0.609 |
| playwright | miss | www.ikea.com/us/en/cat/beds-bm003/ | 0.632 | www.ikea.com/us/en/cat/beds-bm003/ | 0.556 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.552 |


**Q2: What's the price of the SLATTUM upholstered bed frame?** [factual-lookup]
*(expects URL containing: `slattum-upholstered-bed`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/saltsjoebaden-3-seat-sofa-ton | 0.479 | www.ikea.com/us/en/p/saltsjoebaden-3-seat-sofa-ton | 0.476 | www.ikea.com/us/en/p/stockholm-2025-bench-with-pad | 0.473 |
| crawl4ai | miss | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.606 | www.ikea.com/us/en/p/malm-high-bed-frame-2-storage | 0.598 | www.ikea.com/us/en/p/malm-high-bed-frame-2-storage | 0.594 |
| crawl4ai-raw | miss | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.606 | www.ikea.com/us/en/cat/beds-bm003/ | 0.516 | www.ikea.com/us/en/cat/beds-bm003/ | 0.514 |
| scrapy+md | miss | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.512 | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.499 | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.481 |
| crawlee | miss | www.ikea.com/us/en/cat/beds-bm003/ | 0.587 | www.ikea.com/us/en/cat/beds-bm003/ | 0.582 | www.ikea.com/us/en/p/malm-high-bed-frame-2-storage | 0.550 |
| colly+md | miss | www.ikea.com/us/en/cat/beds-bm003/ | 0.600 | www.ikea.com/us/en/cat/beds-bm003/ | 0.599 | www.ikea.com/us/en/cat/bed-slats-24827/ | 0.574 |
| playwright | miss | www.ikea.com/us/en/cat/beds-bm003/ | 0.546 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.529 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.524 |


**Q3: Tell me about the HEMNES 8-drawer dresser** [factual-lookup]
*(expects URL containing: `hemnes-8-drawer-dresser`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.573 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.541 | www.ikea.com/us/en/p/hemnes-bench-gray-70349011/ | 0.537 |
| crawl4ai | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.601 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.599 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-w | 0.594 |
| crawl4ai-raw | miss | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-gray | 0.629 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-gray | 0.624 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.624 |
| scrapy+md | #1 | www.ikea.com/us/en/cat/hemnes-bedroom-series-58619 | 0.619 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.611 | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.610 |
| crawlee | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-w | 0.573 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.571 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.571 |
| colly+md | miss | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-gray | 0.640 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.635 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.635 |
| playwright | #1 | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.637 | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.575 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.570 |


**Q4: What's the price of the RAST 3-drawer dresser?** [factual-lookup]
*(expects URL containing: `rast-3-drawer-dresser`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.543 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.504 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.478 |
| crawl4ai | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.605 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.592 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.579 |
| crawl4ai-raw | miss | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.604 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.598 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.581 |
| scrapy+md | miss | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.526 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.515 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.506 |
| crawlee | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.595 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.562 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.558 |
| colly+md | miss | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.580 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.572 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-d | 0.571 |
| playwright | miss | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.523 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-w | 0.521 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-g | 0.520 |


**Q5: What bed frames does IKEA sell?** [cross-page]
*(expects URL containing: `cat/beds`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/ | 0.570 | www.ikea.com/us/en/rooms/bedroom/ | 0.535 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.530 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/beds-bm003/ | 0.677 | www.ikea.com/us/en/cat/beds-bm003/ | 0.663 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.654 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/beds-bm003/ | 0.695 | www.ikea.com/us/en/cat/beds-bm003/ | 0.663 | www.ikea.com/us/en/cat/baby-kids-bc001/ | 0.654 |
| scrapy+md | miss | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.560 | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.558 | www.ikea.com/us/en/p/hemnes-daybed-frame-with-3-dr | 0.543 |
| crawlee | #1 | www.ikea.com/us/en/cat/beds-bm003/ | 0.774 | www.ikea.com/us/en/cat/beds-bm003/ | 0.650 | www.ikea.com/us/en/cat/products-products/ | 0.632 |
| colly+md | #1 | www.ikea.com/us/en/cat/beds-bm003/ | 0.653 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.643 | www.ikea.com/us/en/cat/beds-bm003/ | 0.633 |
| playwright | #1 | www.ikea.com/us/en/cat/beds-bm003/ | 0.774 | www.ikea.com/us/en/cat/beds-mattresses-bm001/ | 0.670 | www.ikea.com/us/en/cat/beds-bm003/ | 0.650 |


**Q6: Show me IKEA's sofa and armchair selection** [cross-page]
*(expects URL containing: `cat/sofas-armchairs`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/rooms/living-room/ | 0.679 | www.ikea.com/us/en/p/saltsjoebaden-3-seat-sofa-ton | 0.623 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.605 |
| crawl4ai | #2 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.704 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.698 | www.ikea.com/us/en/cat/armchairs-chaises-fu006/ | 0.696 |
| crawl4ai-raw | #3 | www.ikea.com/us/en/cat/armchairs-chaises-fu006/ | 0.718 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.704 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.698 |
| scrapy+md | miss | www.ikea.com/us/en/cat/sofa-covers-10664/ | 0.604 | www.ikea.com/us/en/cat/dining-chairs-25219/ | 0.598 | www.ikea.com/us/en/cat/chair-covers-25223/f/white- | 0.582 |
| crawlee | #1 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.766 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.705 | www.ikea.com/us/en/cat/armchairs-chaises-fu006/ | 0.675 |
| colly+md | #1 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.727 | www.ikea.com/us/en/cat/armchairs-chaises-fu006/ | 0.674 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.650 |
| playwright | #1 | www.ikea.com/us/en/cat/sofas-armchairs-700640/ | 0.766 | www.ikea.com/us/en/cat/sofas-sectionals-fu003/ | 0.705 | www.ikea.com/us/en/cat/armchairs-chaises-fu006/ | 0.675 |


**Q7: What dressers and storage drawers does IKEA offer?** [cross-page]
*(expects URL containing: `cat/dressers-storage-drawers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.673 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.629 | www.ikea.com/us/en/cat/furniture-fu001/ | 0.619 |
| crawl4ai | #1 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.737 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.671 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.664 |
| crawl4ai-raw | #1 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.737 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.671 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.663 |
| scrapy+md | miss | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.650 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.632 | www.ikea.com/us/en/cat/makeup-vanities-dressing-ta | 0.610 |
| crawlee | #1 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.747 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.707 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.696 |
| colly+md | #1 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.698 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.632 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-o | 0.629 |
| playwright | #1 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.747 | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.707 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.695 |


**Q8: How much is the STOREMOLLA 8-drawer dresser at IKEA?** [factual-lookup]
*(expects URL containing: `storemolla-8-drawer-dresser`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.ikea.com/us/en/customer-service/product-suppor | 0.561 | www.ikea.com/us/en/customer-service/product-suppor | 0.535 | www.ikea.com/us/en/p/storklinta-3-drawer-dresser-g | 0.534 |
| crawl4ai | miss | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.608 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.604 | www.ikea.com/us/en/p/malm-dressing-table-white-102 | 0.597 |
| crawl4ai-raw | miss | www.ikea.com/us/en/cat/storage-organization-st001/ | 0.608 | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.590 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-gray | 0.587 |
| scrapy+md | #1 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.733 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-l | 0.680 | www.ikea.com/us/en/p/storemolla-8-drawer-dresser-g | 0.656 |
| crawlee | miss | www.ikea.com/us/en/p/malm-dressing-table-white-102 | 0.596 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.588 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-o | 0.587 |
| colly+md | miss | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-blac | 0.594 | www.ikea.com/us/en/p/brimnes-3-drawer-dresser-whit | 0.592 | www.ikea.com/us/en/p/storklinta-4-drawer-dresser-d | 0.590 |
| playwright | miss | www.ikea.com/us/en/cat/dressers-storage-drawers-st | 0.573 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-o | 0.566 | www.ikea.com/us/en/p/storklinta-6-drawer-dresser-d | 0.566 |


</details>

## newegg

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| colly+md | 12% (1/8) | 12% (1/8) | 25% (2/8) | 25% (2/8) | 25% (2/8) | 0.160 | 6574 | 165 |
| crawl4ai | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.125 | 5857 | 200 |
| crawl4ai-raw | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 12% (1/8) | 0.125 | 5856 | 200 |
| markcrawl | — | — | — | — | — | — | — | — |
| scrapy+md | — | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — | — |
| playwright | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0% (0/8) | 0.000 | 1195 | 200 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for newegg</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What graphics cards are available at Newegg?** [cross-page]
*(expects URL containing: `GPUs-Video-Graphics-Cards`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | #1 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.668 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.664 | www.newegg.com/Video-Card-Accessories/SubCategory/ | 0.625 |
| crawl4ai-raw | #1 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.668 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.664 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.626 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #1 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.615 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.615 | www.newegg.com/d/Best-Sellers/GPU-Video-Graphics-D | 0.603 |
| playwright | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.534 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.533 | www.newegg.com/ | 0.528 |


**Q2: What laptops does Newegg sell?** [cross-page]
*(expects URL containing: `Laptops-Notebooks`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | miss | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.630 | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.622 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.576 |
| crawl4ai-raw | miss | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.630 | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.622 | www.newegg.com/Computer-Systems/Store/ID-3 | 0.576 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #32 | www.newegg.com/All-Laptop/SubCategory/ID-32/Page-3 | 0.686 | www.newegg.com/All-Laptop/SubCategory/ID-32/Page-6 | 0.686 | www.newegg.com/All-Laptop/SubCategory/ID-32/Page-7 | 0.672 |
| playwright | miss | www.newegg.com/ | 0.547 | www.newegg.com/ | 0.546 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.499 |


**Q3: How much does the AMD Ryzen 7 9800X3D CPU cost?** [factual-lookup]
*(expects URL containing: `ryzen-7-9800x3d`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | miss | www.newegg.com/CPU-Processor/Category/ID-34 | 0.637 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.619 | www.newegg.com/CPU-Processor/Category/ID-34 | 0.613 |
| crawl4ai-raw | miss | www.newegg.com/CPU-Processor/Category/ID-34 | 0.637 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.615 | www.newegg.com/CPU-Processor/Category/ID-34 | 0.613 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/p/pl?d=CPU&mid1=PageSEO | 0.646 | www.newegg.com/p/pl?d=CPU&mid1=PageSEO | 0.623 | www.newegg.com/d/Best-Sellers/CPU-Processor/c/ID-3 | 0.620 |
| playwright | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.594 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.594 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.586 |


**Q4: What is the price of the Intel Core i9-14900K?** [factual-lookup]
*(expects URL containing: `i9-14900k`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | miss | www.newegg.com/CPU-Processor/Category/ID-34 | 0.601 | www.newegg.com/CPU-Processor/Category/ID-34 | 0.599 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.588 |
| crawl4ai-raw | miss | www.newegg.com/CPU-Processor/Category/ID-34 | 0.600 | www.newegg.com/CPU-Processor/Category/ID-34 | 0.599 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.586 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/CPU-Processor/c/ID-3 | 0.631 | www.newegg.com/d/best-sellers?cm/sp=Head/Navigatio | 0.612 | www.newegg.com/All-Laptop/SubCategory/ID-32/Page-6 | 0.598 |
| playwright | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.558 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.558 | www.newegg.com/ | 0.539 |


**Q5: Tell me about the GIGABYTE GeForce RTX 5090 graphics card** [factual-lookup]
*(expects URL containing: `gv-n5090gaming`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | miss | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.674 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.662 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.621 |
| crawl4ai-raw | miss | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.674 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.662 | www.newegg.com/GPU-Video-Graphics-Device/Category/ | 0.621 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/GPU-Video-Graphics-D | 0.711 | www.newegg.com/d/Best-Sellers/GPU-Video-Graphics-D | 0.693 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.649 |
| playwright | miss | www.newegg.com/ | 0.508 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.495 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.495 |


**Q6: How much does the SAPPHIRE Radeon RX 9070 XT cost?** [factual-lookup]
*(expects URL containing: `radeon-rx-9070-xt`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | miss | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.578 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.574 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.570 |
| crawl4ai-raw | miss | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.578 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.573 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.570 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/d/Best-Sellers/GPU-Video-Graphics-D | 0.590 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.572 | www.newegg.com/GPUs-Video-Graphics-Cards/SubCatego | 0.572 |
| playwright | miss | www.newegg.com/promotions/nepro/23-1322/index.html | 0.571 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.571 | www.newegg.com/promotions/nepro/23-1322/index.html | 0.450 |


**Q7: What ASUS TUF gaming laptops are available on Newegg?** [factual-lookup]
*(expects URL containing: `asus-tuf-gaming`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | miss | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.602 | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.596 | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.587 |
| crawl4ai-raw | miss | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.602 | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.596 | www.newegg.com/tools/laptop-finder?cm_sp=hamburger | 0.587 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | miss | www.newegg.com/p/pl?N=100006740%2050001315&mid1=Pa | 0.660 | www.newegg.com/Gaming-Laptops/SubCategory/ID-3365? | 0.656 | www.newegg.com/Gaming-Laptops/SubCategory/ID-3365? | 0.653 |
| playwright | miss | www.newegg.com/asus-nuc-configurator?cm_sp=hamburg | 0.552 | www.newegg.com/ | 0.513 | www.newegg.com/ | 0.506 |


**Q8: What electronics categories does Newegg offer?** [cross-page]
*(expects URL containing: `Electronics/Store`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |
| crawl4ai | miss | www.newegg.com/ | 0.685 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.641 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.628 |
| crawl4ai-raw | miss | www.newegg.com/ | 0.685 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.641 | www.newegg.com/Everyday-Saving-Trending-Deals/Even | 0.627 |
| scrapy+md | — | — | — | — | — | — | — |
| crawlee | — | — | — | — | — | — | — |
| colly+md | #4 | www.newegg.com/ | 0.675 | www.newegg.com/ | 0.663 | www.newegg.com/Newegg-Deals/EventSaleStore/ID-9447 | 0.630 |
| playwright | miss | www.newegg.com/ | 0.675 | www.newegg.com/ | 0.664 | www.newegg.com/ | 0.590 |


</details>

## propublica

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| crawlee | 50% (3/6) | 67% (4/6) | 83% (5/6) | 83% (5/6) | 83% (5/6) | 0.632 | 2099 | 150 |
| playwright | 50% (3/6) | 67% (4/6) | 83% (5/6) | 83% (5/6) | 83% (5/6) | 0.632 | 2197 | 150 |
| crawl4ai | 33% (2/6) | 67% (4/6) | 67% (4/6) | 67% (4/6) | 100% (6/6) | 0.523 | 1563 | 149 |
| crawl4ai-raw | 33% (2/6) | 67% (4/6) | 67% (4/6) | 67% (4/6) | 100% (6/6) | 0.523 | 1563 | 149 |
| colly+md | 33% (2/6) | 67% (4/6) | 67% (4/6) | 83% (5/6) | 83% (5/6) | 0.489 | 2196 | 150 |
| scrapy+md | 33% (2/6) | 33% (2/6) | 33% (2/6) | 33% (2/6) | 50% (3/6) | 0.345 | 1396 | 146 |
| markcrawl | 17% (1/6) | 17% (1/6) | 50% (3/6) | 67% (4/6) | 67% (4/6) | 0.274 | 1264 | 150 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for propublica</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What ProPublica investigations cover criminal justice?** [cross-page]
*(expects URL containing: `criminal-justice`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-most-read-st | 0.544 | www.propublica.org/article/propublica-investigatio | 0.525 | www.propublica.org/article/propublica-investigatio | 0.516 |
| crawl4ai | #1 | www.propublica.org/topics/criminal-justice | 0.644 | www.propublica.org/about | 0.615 | www.propublica.org/collaborate | 0.608 |
| crawl4ai-raw | #1 | www.propublica.org/topics/criminal-justice | 0.644 | www.propublica.org/about | 0.615 | www.propublica.org/collaborate | 0.608 |
| scrapy+md | miss | www.propublica.org/reports/page/2 | 0.575 | www.propublica.org/article/how-does-journalism-wor | 0.572 | www.propublica.org/article/how-does-journalism-wor | 0.570 |
| crawlee | #1 | www.propublica.org/topics/criminal-justice | 0.684 | www.propublica.org/advertising | 0.625 | www.propublica.org/press-releases | 0.625 |
| colly+md | miss | www.propublica.org/article/columbia-university-rob | 0.623 | www.propublica.org/article/joseph-schwartz-trump-p | 0.617 | www.propublica.org/article/nike-jobs-indonesia-liv | 0.615 |
| playwright | #1 | www.propublica.org/topics/criminal-justice | 0.684 | www.propublica.org/press-releases | 0.625 | www.propublica.org/advertising | 0.625 |


**Q2: What is ProPublica reporting about healthcare?** [cross-page]
*(expects URL containing: `health`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #7 | www.propublica.org/article/propublica-most-read-st | 0.570 | www.propublica.org/article/rx-inspector-reshaping- | 0.548 | www.propublica.org/article/prospect-medical-malpra | 0.541 |
| crawl4ai | #2 | www.propublica.org/about | 0.615 | www.propublica.org/topics/health-care | 0.603 | www.propublica.org/topics/health-care | 0.586 |
| crawl4ai-raw | #2 | www.propublica.org/about | 0.615 | www.propublica.org/topics/health-care | 0.603 | www.propublica.org/topics/health-care | 0.586 |
| scrapy+md | #1 | www.propublica.org/topics/health-insurance/page/2 | 0.621 | www.propublica.org/reports/page/2 | 0.571 | www.propublica.org/people/maya-miller/page/8 | 0.567 |
| crawlee | #4 | www.propublica.org/advertising | 0.596 | www.propublica.org/press-releases | 0.596 | www.propublica.org/about | 0.592 |
| colly+md | #2 | www.propublica.org/article/nike-jobs-indonesia-liv | 0.598 | www.propublica.org/topics/mental-health | 0.596 | www.propublica.org/article/propublica-files-lawsui | 0.587 |
| playwright | #4 | www.propublica.org/press-releases | 0.596 | www.propublica.org/advertising | 0.596 | www.propublica.org/about | 0.592 |


**Q3: What ProPublica articles discuss politics and government accountability?** [cross-page]
*(expects URL containing: `politics`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | www.propublica.org/article/propublica-most-read-st | 0.572 | www.propublica.org/article/propublica-reaching-out | 0.512 | www.propublica.org/article/propublica-most-read-st | 0.502 |
| crawl4ai | #13 | www.propublica.org/about | 0.648 | www.propublica.org/atpropublica/propublica-selects | 0.635 | www.propublica.org/local-initiatives | 0.612 |
| crawl4ai-raw | #13 | www.propublica.org/about | 0.648 | www.propublica.org/atpropublica/propublica-selects | 0.635 | www.propublica.org/local-initiatives | 0.612 |
| scrapy+md | miss | www.propublica.org/reports/page/2 | 0.638 | www.propublica.org/media-center | 0.611 | www.propublica.org/reports | 0.604 |
| crawlee | #1 | www.propublica.org/topics/politics | 0.628 | www.propublica.org/about | 0.625 | www.propublica.org/reports | 0.610 |
| colly+md | #3 | www.propublica.org/impact | 0.602 | www.propublica.org/tips/federal-workers/ | 0.599 | www.propublica.org/topics/politics | 0.597 |
| playwright | #1 | www.propublica.org/topics/politics | 0.628 | www.propublica.org/about | 0.625 | www.propublica.org/reports | 0.610 |


**Q4: What environmental or climate investigations does ProPublica have?** [cross-page]
*(expects URL containing: `climate`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | www.propublica.org/article/propublica-most-read-st | 0.519 | www.propublica.org/article/propublica-investigatio | 0.467 | www.propublica.org/article/propublica-reaching-out | 0.464 |
| crawl4ai | #17 | www.propublica.org/people/abrahm-lustgarten | 0.647 | www.propublica.org/people/abrahm-lustgarten | 0.605 | www.propublica.org/about | 0.598 |
| crawl4ai-raw | #17 | www.propublica.org/people/abrahm-lustgarten | 0.647 | www.propublica.org/people/abrahm-lustgarten | 0.605 | www.propublica.org/about | 0.598 |
| scrapy+md | miss | www.propublica.org/reports/page/2 | 0.600 | www.propublica.org/media-center | 0.550 | www.propublica.org/article/how-does-journalism-wor | 0.543 |
| crawlee | #25 | www.propublica.org/people/abrahm-lustgarten | 0.624 | www.propublica.org/atpropublica/propublica-selects | 0.606 | www.propublica.org/collaborate | 0.592 |
| colly+md | #10 | www.propublica.org/people/abrahm-lustgarten | 0.615 | www.propublica.org/people/abrahm-lustgarten/page/3 | 0.615 | www.propublica.org/impact | 0.579 |
| playwright | #25 | www.propublica.org/people/abrahm-lustgarten | 0.624 | www.propublica.org/atpropublica/propublica-selects | 0.606 | www.propublica.org/collaborate | 0.592 |


**Q5: What ProPublica stories cover immigration?** [cross-page]
*(expects URL containing: `immigration`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | www.propublica.org/article/propublica-most-read-st | 0.651 | www.propublica.org/article/trump-familia-deportaci | 0.650 | www.propublica.org/article/trump-family-deportatio | 0.629 |
| crawl4ai | #2 | www.propublica.org/people/melissa-sanchez | 0.660 | www.propublica.org/article/trump-immigration-scams | 0.634 | www.propublica.org/people/melissa-sanchez | 0.629 |
| crawl4ai-raw | #2 | www.propublica.org/people/melissa-sanchez | 0.660 | www.propublica.org/article/trump-immigration-scams | 0.634 | www.propublica.org/people/melissa-sanchez | 0.629 |
| scrapy+md | #14 | www.propublica.org/article/trump-mass-deportation- | 0.634 | www.propublica.org/article/trump-mass-deportation- | 0.603 | www.propublica.org/ | 0.583 |
| crawlee | #2 | www.propublica.org/people/melissa-sanchez | 0.620 | www.propublica.org/article/trump-immigration-scams | 0.613 | www.propublica.org/people/melissa-sanchez | 0.609 |
| colly+md | #1 | www.propublica.org/series/the-new-immigration | 0.682 | www.propublica.org/series/inside-the-border-patrol | 0.663 | www.propublica.org/article/caught-in-crackdown-tru | 0.646 |
| playwright | #2 | www.propublica.org/people/melissa-sanchez | 0.620 | www.propublica.org/article/trump-immigration-scams | 0.613 | www.propublica.org/people/melissa-sanchez | 0.609 |


**Q6: What is the main ProPublica homepage with featured stories?** [cross-page]
*(expects URL containing: `propublica.org/`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.propublica.org/article/propublica-most-read-st | 0.556 | www.propublica.org/article/propublica-investigatio | 0.475 | www.propublica.org/article/propublica-reaching-out | 0.462 |
| crawl4ai | #1 | www.propublica.org/about | 0.659 | www.propublica.org/impact | 0.614 | www.propublica.org/collaborate | 0.614 |
| crawl4ai-raw | #1 | www.propublica.org/about | 0.659 | www.propublica.org/impact | 0.614 | www.propublica.org/collaborate | 0.614 |
| scrapy+md | #1 | www.propublica.org/media-center | 0.605 | www.propublica.org/steal-our-stories | 0.599 | www.propublica.org/reports/page/2 | 0.587 |
| crawlee | #1 | www.propublica.org/about | 0.636 | www.propublica.org/about | 0.621 | www.propublica.org/steal-our-stories | 0.613 |
| colly+md | #1 | www.propublica.org/ | 0.606 | www.propublica.org/newsletters | 0.596 | www.propublica.org/awards | 0.596 |
| playwright | #1 | www.propublica.org/about | 0.636 | www.propublica.org/about | 0.622 | www.propublica.org/steal-our-stories | 0.613 |


</details>

## Methodology

- **Queries:** 104 across 11 sites, categorized by type (api-function, code-example, conceptual, structured-data, factual-lookup, cross-page, navigation, js-rendered)
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

