# Retrieval Quality Comparison
<!-- style: v2, 2026-04-23 -->

Crawler choice barely matters for retrieval — retrieval mode matters more.

Does each tool's output produce embeddings that answer real questions?
This benchmark chunks each tool's crawl output, embeds it with
`text-embedding-3-small`, and measures retrieval across four modes:

- **Embedding**: Cosine similarity on OpenAI embeddings
- **BM25**: Keyword search (Okapi BM25)
- **Hybrid**: Embedding + BM25 fused via Reciprocal Rank Fusion
- **Reranked**: Hybrid candidates reranked by `cross-encoder/ms-marco-MiniLM-L-6-v2`

**149 queries** across 12 sites.
Hit rate = correct source page in top-K results. Higher is better.
Summary tables use the **139-query common subset** (11 sites) so all tools are compared on identical queries. Sites excluded: gen2fund (not all tools have data). Per-site tables show full results.

## Quick summary: best retrieval mode per tool

For each tool, the mode with the highest MRR. Most readers can stop here.

| Tool | Best mode | Hit@10 | MRR |
|---|---|---|---|
| markcrawl | embedding | 82% (114/139) ±6% | 0.789 |

> **Column definitions:** **Best mode** = retrieval strategy that maximizes MRR for this tool. **Hit@10** = correct source page in top 10 results. **MRR** = Mean Reciprocal Rank (1/rank of correct result, averaged).

## Summary: retrieval modes compared

_Computed over 139 queries on 11 common sites (blog-engineering, books-toscrape, brex, fastapi-docs, python-docs, quotes-toscrape, react-dev, stripe-docs, supabase-docs, tailwind-docs, wikipedia-python)._

| Tool | Mode | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR |
|---|---|---|---|---|---|---|---|
| markcrawl | embedding | 77% (107/139) ±7% | 81% (112/139) ±7% | 81% (113/139) ±6% | 82% (114/139) ±6% | 82% (114/139) ±6% | 0.789 |
| markcrawl | bm25 | 29% (41/139) ±7% | 49% (68/139) ±8% | 54% (75/139) ±8% | 58% (81/139) ±8% | 68% (94/139) ±8% | 0.406 |
| markcrawl | hybrid | 59% (82/139) ±8% | 75% (104/139) ±7% | 76% (106/139) ±7% | 82% (114/139) ±6% | 82% (114/139) ±6% | 0.672 |

> **Column definitions:** **Hit@K** = percentage of queries where the correct source page appeared in the top K results (shown as % with raw counts). **MRR** (Mean Reciprocal Rank) = average of 1/rank for correct results (1.0 = always rank 1, 0.5 = always rank 2). **Mode** = retrieval strategy used (see definitions above).

## Summary: embedding-only (hit rate at multiple K values)

_Computed over 139 queries on 11 common sites._

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Avg words |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 77% (107/139) ±7% | 81% (112/139) ±7% | 81% (113/139) ±6% | 82% (114/139) ±6% | 82% (114/139) ±6% | 0.789 | 30148 | 142 |

> **Column definitions:** **Hit@K** = correct source page in top K results. **MRR** = Mean Reciprocal Rank (1/rank of correct result, averaged). **Chunks** = total chunks produced by this tool (across all pages in common sites). **Avg words** = mean words per chunk.

## What this means

All tools perform within a narrow band (MRR 0.789-0.789 on embedding mode). This is expected: tools crawl similar pages from the same seed URLs, and we apply identical chunking and embedding pipelines. The extraction differences that matter for [content quality](QUALITY_COMPARISON.md) largely wash out at retrieval time.

**Retrieval mode matters more than crawler choice.** Embedding search beats BM25 by roughly 2x on MRR across all tools. Hybrid and reranked modes fall between the two. Choosing the right retrieval strategy will improve your RAG pipeline far more than switching crawlers.

**The noise-vs-recall trade-off.** Noisier tools (crawlee, playwright) have slightly higher hit rates, but they produce 2x the chunks of leaner tools (markcrawl, scrapy+md). More chunks means higher embedding and storage costs with diminishing retrieval returns. See [COST_AT_SCALE.md](COST_AT_SCALE.md) for the dollar impact.

**For most use cases, pick your crawler based on speed and cost, not retrieval quality.** The differences here are within confidence intervals. Where crawler choice _does_ matter is content quality and downstream answer quality -- see [ANSWER_QUALITY.md](ANSWER_QUALITY.md).

## Per-category breakdown (embedding mode)

Query categories reveal where crawlers actually differ. Categories like `js-rendered` and `structured-data` stress-test browser rendering and table extraction, while `api-function` and `conceptual` queries test basic content retrieval.

| Category | Tool | Hit@10 | MRR | Queries |
|---|---|---|---|---|
| api-function | markcrawl | 85% (46/54) | 0.779 | 54 |
| code-example | markcrawl | 100% (11/11) | 1.000 | 11 |
| conceptual | markcrawl | 89% (33/37) | 0.814 | 37 |
| cross-page | markcrawl | 40% (2/5) | 0.400 | 5 |
| factual-lookup | markcrawl | 61% (11/18) | 0.611 | 18 |
| js-rendered | markcrawl | 100% (5/5) | 0.900 | 5 |
| navigation | markcrawl | 100% (1/1) | 1.000 | 1 |
| structured-data | markcrawl | 100% (8/8) | 1.000 | 8 |


### Best tool per category

| Category | Best tool | Hit@10 | Spread |
|---|---|---|---|
| api-function | markcrawl | 85% | 0% |
| code-example | markcrawl | 100% | 0% |
| conceptual | markcrawl | 89% | 0% |
| cross-page | markcrawl | 40% | 0% |
| factual-lookup | markcrawl | 61% | 0% |
| js-rendered | markcrawl | 100% | 0% |
| navigation | markcrawl | 100% | 0% |
| structured-data | markcrawl | 100% | 0% |

_Spread = difference between best and worst tool. High spread categories are where crawler choice matters most._


## quotes-toscrape

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 38% (3/8) | 0.375 | 24 | 15 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for quotes-toscrape</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What did Albert Einstein say about thinking and the world?** [factual-lookup]
*(expects URL containing: `author/Albert-Einstein`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | quotes.toscrape.com/tag/thinking/page/1/ | 0.560 | quotes.toscrape.com/ | 0.479 | quotes.toscrape.com/tag/life/page/1/ | 0.460 |


**Q2: Which quotes are tagged with 'change'?** [cross-page]
*(expects URL containing: `tag/change`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | quotes.toscrape.com/tag/thinking/page/1/ | 0.527 | quotes.toscrape.com/ | 0.501 | quotes.toscrape.com/tag/life/page/1/ | 0.487 |


**Q3: What did Steve Martin say about sunshine?** [factual-lookup]
*(expects URL containing: `author/Steve-Martin`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | quotes.toscrape.com/ | 0.379 | quotes.toscrape.com/tag/life/page/1/ | 0.332 | quotes.toscrape.com/tag/life/page/1/ | 0.312 |


**Q4: What quotes are about thinking deeply?** [cross-page]
*(expects URL containing: `tag/thinking`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | quotes.toscrape.com/tag/thinking/page/1/ | 0.588 | quotes.toscrape.com/ | 0.570 | quotes.toscrape.com/tag/life/page/1/ | 0.519 |


**Q5: What did Eleanor Roosevelt say about life?** [factual-lookup]
*(expects URL containing: `author/Eleanor-Roosevelt`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | quotes.toscrape.com/author/Eleanor-Roosevelt | 0.612 | quotes.toscrape.com/tag/life/page/1/ | 0.523 | quotes.toscrape.com/tag/life/page/1/ | 0.514 |


**Q6: Which quotes are tagged about choices and abilities?** [cross-page]
*(expects URL containing: `tag/abilities`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | quotes.toscrape.com/tag/life/page/1/ | 0.533 | quotes.toscrape.com/ | 0.517 | quotes.toscrape.com/page/2/ | 0.498 |


**Q7: What quotes are about friendship?** [cross-page]
*(expects URL containing: `tag/friendship`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | quotes.toscrape.com/page/2/ | 0.638 | quotes.toscrape.com/page/2/ | 0.568 | quotes.toscrape.com/ | 0.541 |


**Q8: What are the quotes about love?** [cross-page]
*(expects URL containing: `tag/love`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | quotes.toscrape.com/tag/love/ | 0.649 | quotes.toscrape.com/tag/love/ | 0.639 | quotes.toscrape.com/page/2/ | 0.611 |


</details>

## books-toscrape

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 100% (10/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 1.000 | 249 | 60 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for books-toscrape</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What mystery and thriller books are in the catalog?** [structured-data]
*(expects URL containing: `category/books/mystery`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/myster | 0.548 | books.toscrape.com/catalogue/category/books/myster | 0.528 | books.toscrape.com/catalogue/category/books/myster | 0.502 |


**Q2: What science fiction books are available?** [structured-data]
*(expects URL containing: `category/books/science-fiction`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/scienc | 0.563 | books.toscrape.com/catalogue/category/books/scienc | 0.530 | books.toscrape.com/catalogue/category/books/scienc | 0.508 |


**Q3: What is the book Sharp Objects about?** [factual-lookup]
*(expects URL containing: `sharp-objects`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.701 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.668 | books.toscrape.com/catalogue/sharp-objects_997/ind | 0.569 |


**Q4: What biography books are in the catalog?** [structured-data]
*(expects URL containing: `category/books/biography`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/autobi | 0.422 | books.toscrape.com/ | 0.408 | books.toscrape.com/ | 0.405 |


**Q5: What horror books are in the catalog?** [structured-data]
*(expects URL containing: `category/books/horror`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/horror | 0.550 | books.toscrape.com/catalogue/category/books/thrill | 0.444 | books.toscrape.com/ | 0.436 |


**Q6: What poetry books can I find?** [structured-data]
*(expects URL containing: `category/books/poetry`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/poetry | 0.547 | books.toscrape.com/catalogue/category/books/poetry | 0.543 | books.toscrape.com/catalogue/category/books/poetry | 0.528 |


**Q7: What fantasy books are in the bookstore?** [structured-data]
*(expects URL containing: `category/books/fantasy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/fantas | 0.497 | books.toscrape.com/catalogue/category/books/fantas | 0.493 | books.toscrape.com/catalogue/category/books/fantas | 0.468 |


**Q8: What philosophy books are available to read?** [structured-data]
*(expects URL containing: `category/books/philosophy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/philos | 0.517 | books.toscrape.com/catalogue/libertarianism-for-be | 0.401 | books.toscrape.com/catalogue/category/books/psycho | 0.398 |


**Q9: What is the book Sapiens about?** [factual-lookup]
*(expects URL containing: `sapiens`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.682 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.664 | books.toscrape.com/catalogue/sapiens-a-brief-histo | 0.664 |


**Q10: What romance novels are available?** [structured-data]
*(expects URL containing: `category/books/romance`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | books.toscrape.com/catalogue/category/books/romanc | 0.505 | books.toscrape.com/catalogue/category/books/romanc | 0.461 | books.toscrape.com/catalogue/category/books/womens | 0.454 |


</details>

## fastapi-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 95% (19/20) | 95% (19/20) | 95% (19/20) | 100% (20/20) | 100% (20/20) | 0.958 | 3474 | 156 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for fastapi-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do I add authentication to a FastAPI endpoint?** [api-function]
*(expects URL containing: `security`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/security/ | 0.656 | fastapi.tiangolo.com/advanced/security/http-basic- | 0.654 | fastapi.tiangolo.com/tutorial/security/ | 0.643 |


**Q2: How do I define query parameters in the FastAPI reference?** [api-function]
*(expects URL containing: `reference/fastapi`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/reference/parameters/ | 0.735 | fastapi.tiangolo.com/reference/parameters/ | 0.734 | fastapi.tiangolo.com/reference/parameters/ | 0.726 |


**Q3: How does FastAPI handle JSON encoding and base64 bytes?** [code-example]
*(expects URL containing: `json-base64-bytes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.735 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.665 | fastapi.tiangolo.com/advanced/json-base64-bytes/ | 0.636 |


**Q4: How do I use OAuth2 with password flow in FastAPI?** [code-example]
*(expects URL containing: `simple-oauth2`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ | 0.722 | fastapi.tiangolo.com/advanced/security/oauth2-scop | 0.710 | fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ | 0.705 |


**Q5: How do I use WebSockets in FastAPI?** [api-function]
*(expects URL containing: `websockets`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/advanced/websockets/ | 0.838 | fastapi.tiangolo.com/advanced/websockets/ | 0.808 | fastapi.tiangolo.com/advanced/websockets/ | 0.794 |


**Q6: How do I define nested Pydantic models for request bodies?** [code-example]
*(expects URL containing: `body-nested-models`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.683 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.662 | fastapi.tiangolo.com/tutorial/body-nested-models/ | 0.623 |


**Q7: How do I use middleware in FastAPI?** [api-function]
*(expects URL containing: `middleware`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/middleware/ | 0.759 | fastapi.tiangolo.com/tutorial/middleware/ | 0.738 | fastapi.tiangolo.com/tutorial/middleware/ | 0.736 |


**Q8: How do I deploy FastAPI to the cloud?** [conceptual]
*(expects URL containing: `deployment`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/deployment/cloud/ | 0.754 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.749 | fastapi.tiangolo.com/deployment/fastapicloud/ | 0.732 |


**Q9: How do I handle file uploads in FastAPI?** [api-function]
*(expects URL containing: `request-files`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/request-files/ | 0.718 | fastapi.tiangolo.com/tutorial/request-files/ | 0.649 | fastapi.tiangolo.com/tutorial/request-files/ | 0.645 |


**Q10: How do I write async tests for FastAPI applications?** [code-example]
*(expects URL containing: `async-tests`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/advanced/async-tests/ | 0.753 | fastapi.tiangolo.com/advanced/async-tests/ | 0.734 | fastapi.tiangolo.com/advanced/async-tests/ | 0.707 |


**Q11: How do I use Jinja2 templates in FastAPI?** [code-example]
*(expects URL containing: `templating`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/reference/templating/ | 0.788 | fastapi.tiangolo.com/reference/templating/ | 0.743 | fastapi.tiangolo.com/advanced/templates/ | 0.741 |


**Q12: How do I use dependency injection in FastAPI?** [conceptual]
*(expects URL containing: `dependencies`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.751 | fastapi.tiangolo.com/tutorial/dependencies/ | 0.694 | fastapi.tiangolo.com/tutorial/dependencies/classes | 0.674 |


**Q13: How do I return custom response classes in FastAPI?** [api-function]
*(expects URL containing: `custom-response`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #6 | fastapi.tiangolo.com/reference/responses/ | 0.740 | fastapi.tiangolo.com/reference/responses/ | 0.723 | fastapi.tiangolo.com/reference/responses/ | 0.717 |


**Q14: How do I configure CORS in FastAPI?** [api-function]
*(expects URL containing: `cors`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/cors/ | 0.670 | fastapi.tiangolo.com/tutorial/cors/ | 0.670 | fastapi.tiangolo.com/tutorial/cors/ | 0.657 |


**Q15: How do I use path parameters in FastAPI?** [api-function]
*(expects URL containing: `path-params`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/path-params/ | 0.735 | fastapi.tiangolo.com/tutorial/path-params/ | 0.689 | fastapi.tiangolo.com/tutorial/path-operation-confi | 0.685 |


**Q16: How do I run FastAPI with Docker?** [conceptual]
*(expects URL containing: `docker`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/deployment/docker/ | 0.725 | fastapi.tiangolo.com/deployment/docker/ | 0.685 | fastapi.tiangolo.com/deployment/docker/ | 0.679 |


**Q17: How do I configure FastAPI application settings?** [code-example]
*(expects URL containing: `settings`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/advanced/settings/ | 0.716 | fastapi.tiangolo.com/advanced/settings/ | 0.691 | fastapi.tiangolo.com/advanced/settings/ | 0.649 |


**Q18: How do I use background tasks in FastAPI?** [api-function]
*(expects URL containing: `background-tasks`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/background-tasks/ | 0.764 | fastapi.tiangolo.com/tutorial/background-tasks/ | 0.738 | fastapi.tiangolo.com/reference/background/ | 0.726 |


**Q19: What are the first steps to create a FastAPI application?** [conceptual]
*(expects URL containing: `first-steps`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.722 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.713 | fastapi.tiangolo.com/tutorial/first-steps/ | 0.708 |


**Q20: How do I handle errors and exceptions in FastAPI?** [api-function]
*(expects URL containing: `handling-errors`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | fastapi.tiangolo.com/tutorial/handling-errors/ | 0.699 | fastapi.tiangolo.com/reference/exceptions/ | 0.697 | fastapi.tiangolo.com/tutorial/handling-errors/ | 0.661 |


</details>

## python-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 74% (14/19) | 84% (16/19) | 84% (16/19) | 84% (16/19) | 84% (16/19) | 0.772 | 9021 | 500 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for python-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: What new features were added in Python 3.10?** [factual-lookup]
*(expects URL containing: `whatsnew/3.10`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/whatsnew/3.10.html | 0.764 | docs.python.org/3.10/whatsnew/3.10.html | 0.747 | docs.python.org/3.10/whatsnew/3.10.html | 0.715 |


**Q2: What does the term 'decorator' mean in Python?** [factual-lookup]
*(expects URL containing: `glossary`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/glossary.html | 0.528 | docs.python.org/3.8/glossary.html | 0.527 | docs.python.org/3.10/whatsnew/2.4.html | 0.512 |


**Q3: How do I report a bug in Python?** [factual-lookup]
*(expects URL containing: `bugs`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/bugs.html | 0.641 | docs.python.org/3.8/bugs.html | 0.640 | docs.python.org/3.11/bugs.html | 0.638 |


**Q4: What is Python's glossary definition of a generator?** [factual-lookup]
*(expects URL containing: `glossary`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.14/glossary.html | 0.573 | docs.python.org/3.10/glossary.html | 0.566 | docs.python.org/3.11/glossary.html | 0.558 |


**Q5: What is the Python module index?** [navigation]
*(expects URL containing: `py-modindex`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.11/py-modindex.html | 0.807 | docs.python.org/3.10/py-modindex.html | 0.806 | docs.python.org/3.8/py-modindex.html | 0.806 |


**Q6: What does the term 'iterable' mean in Python?** [factual-lookup]
*(expects URL containing: `glossary`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/glossary.html | 0.553 | docs.python.org/3.8/glossary.html | 0.550 | docs.python.org/3.10/library/itertools.html | 0.547 |


**Q7: How do I install and configure Python on my system?** [conceptual]
*(expects URL containing: `using`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | docs.python.org/3.10/tutorial/interpreter.html | 0.534 | docs.python.org/3.13/installing/index.html | 0.531 | docs.python.org/3.11/using/index.html | 0.531 |


**Q8: How do I use the os module for file and directory operations?** [api-function]
*(expects URL containing: `library/os`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #3 | docs.python.org/3.10/library/filesys.html | 0.611 | docs.python.org/3.10/library/allos.html | 0.522 | docs.python.org/3.10/library/os.path.html | 0.507 |


**Q9: How do I use pathlib for filesystem paths in Python?** [api-function]
*(expects URL containing: `library/pathlib`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/library/pathlib.html | 0.540 | docs.python.org/3.10/whatsnew/3.4.html | 0.532 | docs.python.org/3.10/library/pathlib.html | 0.516 |


**Q10: How do I parse and generate JSON in Python?** [api-function]
*(expects URL containing: `library/json`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/library/json.html | 0.475 | docs.python.org/3.10/library/json.html | 0.472 | docs.python.org/3.10/library/json.html | 0.453 |


**Q11: How do I use asyncio for async programming in Python?** [api-function]
*(expects URL containing: `library/asyncio`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/library/asyncio-dev.html | 0.685 | docs.python.org/3.10/library/asyncio-dev.html | 0.652 | docs.python.org/3.10/library/asyncio-dev.html | 0.644 |


**Q12: How do I use type hints and the typing module in Python?** [api-function]
*(expects URL containing: `library/typing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/library/typing.html | 0.661 | docs.python.org/3.10/library/typing.html | 0.655 | docs.python.org/3.10/library/typing.html | 0.650 |


**Q13: How do I work with dates and times using the datetime module?** [api-function]
*(expects URL containing: `library/datetime`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.python.org/3.10/library/time.html | 0.544 | docs.python.org/3.10/library/time.html | 0.539 | docs.python.org/3.10/library/time.html | 0.526 |


**Q14: How do I use Python's logging module?** [api-function]
*(expects URL containing: `library/logging`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/library/logging.html | 0.595 | docs.python.org/3.10/howto/logging.html | 0.587 | docs.python.org/3.10/howto/logging.html | 0.570 |


**Q15: How do I write unit tests with the unittest module?** [code-example]
*(expects URL containing: `library/unittest`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/library/unittest.mock-example | 0.510 | docs.python.org/3.10/library/unittest.mock-example | 0.487 | docs.python.org/3.10/library/unittest.mock.html | 0.461 |


**Q16: How do I use Python dataclasses?** [api-function]
*(expects URL containing: `library/dataclasses`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.python.org/3.10/whatsnew/3.7.html | 0.595 | docs.python.org/3.10/tutorial/classes.html | 0.579 | docs.python.org/3.10/tutorial/classes.html | 0.557 |


**Q17: How do I use itertools for efficient iteration in Python?** [api-function]
*(expects URL containing: `library/itertools`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/library/itertools.html | 0.600 | docs.python.org/3.10/library/itertools.html | 0.593 | docs.python.org/3.10/library/itertools.html | 0.593 |


**Q18: How does Python's data model work with special methods?** [conceptual]
*(expects URL containing: `reference/datamodel`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.python.org/3.10/reference/datamodel.html | 0.573 | docs.python.org/3.10/reference/datamodel.html | 0.539 | docs.python.org/3.10/reference/datamodel.html | 0.535 |


**Q19: What are Python's compound statements like if, for, and with?** [conceptual]
*(expects URL containing: `reference/compound_stmts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.python.org/3.10/tutorial/controlflow.html | 0.573 | docs.python.org/3.10/tutorial/controlflow.html | 0.535 | docs.python.org/3.10/tutorial/controlflow.html | 0.535 |


</details>

## react-dev

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 100% (16/16) | 100% (16/16) | 100% (16/16) | 100% (16/16) | 100% (16/16) | 1.000 | 3696 | 221 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for react-dev</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do I manage state in a React component?** [conceptual]
*(expects URL containing: `state`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/managing-state | 0.727 | react.dev/learn/preserving-and-resetting-state | 0.717 | react.dev/learn/managing-state | 0.716 |


**Q2: How does the useEffect hook work in React?** [api-function]
*(expects URL containing: `useEffect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useEffect | 0.733 | react.dev/reference/react/useEffect | 0.717 | react.dev/reference/react/useEffect | 0.695 |


**Q3: How do I create and use context in React?** [api-function]
*(expects URL containing: `useContext`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/passing-data-deeply-with-context | 0.718 | react.dev/reference/react/createContext | 0.712 | react.dev/learn/passing-data-deeply-with-context | 0.710 |


**Q4: What is JSX and how does React use it?** [conceptual]
*(expects URL containing: `writing-markup-with-jsx`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/writing-markup-with-jsx | 0.737 | react.dev/learn/javascript-in-jsx-with-curly-brace | 0.696 | react.dev/learn/writing-markup-with-jsx | 0.676 |


**Q5: How do I render lists and use keys in React?** [code-example]
*(expects URL containing: `rendering-lists`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/rendering-lists | 0.739 | react.dev/learn/rendering-lists | 0.733 | react.dev/learn/rendering-lists | 0.728 |


**Q6: How do I use the useRef hook in React?** [api-function]
*(expects URL containing: `useRef`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useRef | 0.818 | react.dev/reference/react/useRef | 0.773 | react.dev/reference/react/useRef | 0.766 |


**Q7: How do I pass props between React components?** [conceptual]
*(expects URL containing: `passing-props`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/passing-props-to-a-component | 0.768 | react.dev/learn/passing-props-to-a-component | 0.752 | react.dev/learn/passing-data-deeply-with-context | 0.681 |


**Q8: How do I conditionally render content in React?** [code-example]
*(expects URL containing: `conditional-rendering`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/conditional-rendering | 0.733 | react.dev/learn/conditional-rendering | 0.694 | react.dev/learn/conditional-rendering | 0.684 |


**Q9: What is the useMemo hook for in React?** [api-function]
*(expects URL containing: `useMemo`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useMemo | 0.765 | react.dev/reference/react/useMemo | 0.755 | react.dev/reference/react/useMemo | 0.719 |


**Q10: How do I use the useState hook in React?** [api-function]
*(expects URL containing: `useState`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useState | 0.734 | react.dev/reference/react/useState | 0.728 | react.dev/reference/react/useState | 0.711 |


**Q11: How do I use the useCallback hook in React?** [api-function]
*(expects URL containing: `useCallback`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useCallback | 0.794 | react.dev/reference/react/useCallback | 0.771 | react.dev/reference/react/useCallback | 0.739 |


**Q12: How do I use the useReducer hook in React?** [api-function]
*(expects URL containing: `useReducer`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/useReducer | 0.812 | react.dev/reference/react/useReducer | 0.799 | react.dev/reference/react/useReducer | 0.763 |


**Q13: How do I handle events like clicks in React?** [code-example]
*(expects URL containing: `responding-to-events`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/responding-to-events | 0.706 | react.dev/learn/responding-to-events | 0.681 | react.dev/learn/responding-to-events | 0.672 |


**Q14: What is the Suspense component in React?** [api-function]
*(expects URL containing: `Suspense`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/reference/react/Suspense | 0.716 | react.dev/blog/2022/03/29/react-v18 | 0.685 | react.dev/reference/react/Suspense | 0.676 |


**Q15: How do I add interactivity to React components?** [conceptual]
*(expects URL containing: `adding-interactivity`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/adding-interactivity | 0.754 | react.dev/ | 0.742 | react.dev/learn/adding-interactivity | 0.742 |


**Q16: How do I install and set up a new React project?** [conceptual]
*(expects URL containing: `installation`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | react.dev/learn/installation | 0.705 | react.dev/learn/add-react-to-an-existing-project | 0.693 | react.dev/learn/add-react-to-an-existing-project | 0.692 |


</details>

## wikipedia-python

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 20% (2/10) | 20% (2/10) | 20% (2/10) | 20% (2/10) | 20% (2/10) | 0.200 | 1277 | 50 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for wikipedia-python</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: Who created the Python programming language?** [factual-lookup]
*(expects URL containing: `Python_(programming_language)`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | en.wikipedia.org/wiki/Python_(programming_language | 0.509 | en.wikipedia.org/wiki/Python_(programming_language | 0.503 | en.wikipedia.org/wiki/Python_(programming_language | 0.482 |


**Q2: What is the Python Software Foundation?** [factual-lookup]
*(expects URL containing: `Python_Software_Foundation`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/List_of_free_and_open-source | 0.484 | en.wikipedia.org/wiki/List_of_free_and_open-source | 0.463 | en.wikipedia.org/wiki/List_of_free_and_open-source | 0.442 |


**Q3: Who is Guido van Rossum?** [factual-lookup]
*(expects URL containing: `Guido_van_Rossum`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.454 | en.wikipedia.org/wiki/Python_(programming_language | 0.407 | en.wikipedia.org/wiki/Python_(programming_language | 0.403 |


**Q4: What is CPython and how does it work?** [factual-lookup]
*(expects URL containing: `CPython`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.462 | en.wikipedia.org/wiki/CircuitPython | 0.444 | en.wikipedia.org/wiki/Python_(programming_language | 0.438 |


**Q5: How does Python compare to other programming languages?** [conceptual]
*(expects URL containing: `Comparison_of_programming_languages`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Python_(programming_language | 0.589 | en.wikipedia.org/wiki/Python_(programming_language | 0.569 | en.wikipedia.org/wiki/Python_(programming_language | 0.555 |


**Q6: What is NumPy and what is it used for?** [factual-lookup]
*(expects URL containing: `NumPy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Mlpy | 0.393 | en.wikipedia.org/wiki/MNE-Python | 0.374 | en.wikipedia.org/wiki/Python_(programming_language | 0.365 |


**Q7: What is SQLAlchemy and how is it used with Python?** [factual-lookup]
*(expects URL containing: `SQLAlchemy`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Python-Ogre | 0.315 | en.wikipedia.org/wiki/Python_(programming_language | 0.311 | en.wikipedia.org/wiki/Python_(programming_language | 0.310 |


**Q8: What is metaprogramming in computer science?** [conceptual]
*(expects URL containing: `Metaprogramming`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Imperative_programming | 0.499 | en.wikipedia.org/wiki/Imperative_programming | 0.497 | en.wikipedia.org/wiki/Imperative_programming | 0.473 |


**Q9: What are list comprehensions in programming?** [conceptual]
*(expects URL containing: `List_comprehension`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | en.wikipedia.org/wiki/List_comprehension | 0.684 | en.wikipedia.org/wiki/List_comprehension | 0.684 | en.wikipedia.org/wiki/List_comprehension | 0.618 |


**Q10: How does memory management work in programming?** [conceptual]
*(expects URL containing: `Memory_management`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | en.wikipedia.org/wiki/Strongly_typed | 0.469 | en.wikipedia.org/wiki/Imperative_programming | 0.461 | en.wikipedia.org/wiki/Imperative_programming | 0.435 |


</details>

## stripe-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 72% (13/18) | 78% (14/18) | 78% (14/18) | 78% (14/18) | 78% (14/18) | 0.757 | 3738 | 500 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for stripe-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do I create a payment intent with Stripe?** [api-function]
*(expects URL containing: `payment-intent`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | docs.stripe.com/upgrades/manage-payment-methods | 0.687 | docs.stripe.com/apple-pay | 0.680 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.601 |


**Q2: How do I handle webhooks from Stripe?** [api-function]
*(expects URL containing: `webhook`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/subscriptions/webhooks | 0.687 | docs.stripe.com/error-handling | 0.673 | docs.stripe.com/billing/subscriptions/webhooks | 0.653 |


**Q3: How do I set up Stripe subscriptions?** [api-function]
*(expects URL containing: `subscription`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/subscriptions/build-subscr | 0.691 | docs.stripe.com/billing/subscriptions/paypal | 0.689 | docs.stripe.com/billing/subscriptions/build-subscr | 0.687 |


**Q4: How do I authenticate with the Stripe API?** [api-function]
*(expects URL containing: `authentication`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #26 | docs.stripe.com/keys | 0.605 | docs.stripe.com/agentic-commerce/protocol | 0.599 | docs.stripe.com/get-started/account/set-up | 0.599 |


**Q5: How do I handle errors in the Stripe API?** [api-function]
*(expects URL containing: `error-handling`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/error-handling | 0.705 | docs.stripe.com/error-handling | 0.695 | docs.stripe.com/error-low-level | 0.690 |


**Q6: How do I process refunds with Stripe?** [api-function]
*(expects URL containing: `refund`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #23 | docs.stripe.com/billing/subscriptions/third-party- | 0.701 | docs.stripe.com/billing/taxes/collect-taxes | 0.625 | docs.stripe.com/ach-deprecated | 0.609 |


**Q7: How do I use Stripe checkout for payments?** [js-rendered]
*(expects URL containing: `checkout`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | docs.stripe.com/billing/subscriptions/stablecoins | 0.638 | docs.stripe.com/billing/subscriptions/build-subscr | 0.629 | docs.stripe.com/billing/subscriptions/build-subscr | 0.625 |


**Q8: How do I test Stripe payments in development?** [code-example]
*(expects URL containing: `testing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/testing | 0.671 | docs.stripe.com/billing/testing | 0.656 | docs.stripe.com/billing/testing | 0.652 |


**Q9: What are Stripe Connect and platform payments?** [conceptual]
*(expects URL containing: `connect`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #27 | docs.stripe.com/get-started/account/orgs/setup | 0.641 | docs.stripe.com/capital/how-capital-for-platforms- | 0.636 | docs.stripe.com/capital/how-stripe-capital-works | 0.631 |


**Q10: How do I set up usage-based billing with Stripe?** [js-rendered]
*(expects URL containing: `usage-based`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.745 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.740 | docs.stripe.com/billing/subscriptions/usage-based/ | 0.735 |


**Q11: How do I manage Stripe API keys?** [api-function]
*(expects URL containing: `keys`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/keys-best-practices | 0.725 | docs.stripe.com/keys-best-practices | 0.716 | docs.stripe.com/keys-best-practices | 0.716 |


**Q12: How do I handle Stripe rate limits?** [api-function]
*(expects URL containing: `rate-limits`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/rate-limits | 0.742 | docs.stripe.com/rate-limits | 0.734 | docs.stripe.com/rate-limits | 0.728 |


**Q13: How do I use metadata with Stripe objects?** [api-function]
*(expects URL containing: `metadata`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/metadata/use-cases | 0.749 | docs.stripe.com/metadata/use-cases | 0.748 | docs.stripe.com/metadata | 0.719 |


**Q14: How do I set up Apple Pay with Stripe?** [js-rendered]
*(expects URL containing: `apple-pay`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/apple-pay | 0.729 | docs.stripe.com/apple-pay | 0.709 | docs.stripe.com/apple-pay | 0.705 |


**Q15: How do I issue cards with Stripe Issuing?** [api-function]
*(expects URL containing: `issuing`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/issuing/integration-guides/b2b-pay | 0.665 | docs.stripe.com/issuing/integration-guides/fleet | 0.653 | docs.stripe.com/issuing/sample-app | 0.648 |


**Q16: How do I recover failed subscription payments?** [js-rendered]
*(expects URL containing: `revenue-recovery`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/revenue-recovery | 0.584 | docs.stripe.com/billing/revenue-recovery/recovery- | 0.572 | docs.stripe.com/billing/revenue-recovery | 0.562 |


**Q17: How does Stripe handle tax calculation for billing?** [js-rendered]
*(expects URL containing: `billing/taxes`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/billing/taxes/tax-rates | 0.700 | docs.stripe.com/billing/taxes/collect-taxes | 0.692 | docs.stripe.com/billing/taxes/collect-taxes | 0.677 |


**Q18: How do I migrate data to Stripe?** [conceptual]
*(expects URL containing: `data-migrations`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | docs.stripe.com/get-started/data-migrations/pan-ex | 0.686 | docs.stripe.com/get-started/data-migrations/pan-im | 0.685 | docs.stripe.com/get-started/data-migrations/pan-im | 0.678 |


</details>

## blog-engineering

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 75% (6/8) | 88% (7/8) | 100% (8/8) | 100% (8/8) | 100% (8/8) | 0.844 | 3151 | 200 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for blog-engineering</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How does GitHub handle Kubernetes at scale?** [conceptual]
*(expects URL containing: `engineering/`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | github.blog/engineering/infrastructure/kubernetes- | 0.724 | github.blog/engineering/infrastructure/kubernetes- | 0.721 | github.blog/engineering/infrastructure/kubernetes- | 0.690 |


**Q2: How does GitHub protect against DDoS attacks?** [conceptual]
*(expects URL containing: `engineering/`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | github.blog/news-insights/company-news/ddos-incide | 0.672 | github.blog/news-insights/company-news/ddos-incide | 0.663 | github.blog/news-insights/company-news/ddos-incide | 0.662 |


**Q3: How does GitHub handle MySQL database operations?** [conceptual]
*(expects URL containing: `engineering/`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | github.blog/engineering/infrastructure/orchestrato | 0.667 | github.blog/engineering/infrastructure/orchestrato | 0.645 | github.blog/engineering/infrastructure/context-awa | 0.599 |


**Q4: How does GitHub handle load balancing?** [conceptual]
*(expects URL containing: `engineering/`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | github.blog/engineering/infrastructure/glb-directo | 0.688 | github.blog/engineering/infrastructure/glb-directo | 0.630 | github.blog/engineering/infrastructure/glb-directo | 0.622 |


**Q5: What is GitHub's approach to platform security?** [conceptual]
*(expects URL containing: `platform-security`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #4 | github.blog/security/subresource-integrity/ | 0.639 | github.blog/latest/ | 0.613 | github.blog/latest/ | 0.610 |


**Q6: How does GitHub optimize its architecture?** [conceptual]
*(expects URL containing: `architecture-optimization`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | github.blog/engineering/architecture-optimization/ | 0.646 | github.blog/engineering/infrastructure/evolution-o | 0.639 | github.blog/engineering/infrastructure/evolution-o | 0.634 |


**Q7: What engineering principles does GitHub follow?** [conceptual]
*(expects URL containing: `engineering-principles`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | github.blog/engineering/engineering-principles/mov | 0.663 | github.blog/engineering/engineering-principles/mov | 0.655 | github.blog/engineering/engineering-principles/mov | 0.654 |


**Q8: How does GitHub improve user experience?** [conceptual]
*(expects URL containing: `user-experience`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | github.blog/engineering/architecture-optimization/ | 0.649 | github.blog/engineering/user-experience/topics/ | 0.624 | github.blog/news-insights/the-library/smooth-suppo | 0.621 |


</details>

## gen2fund

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — | — |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for gen2fund</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: Where does Gen2 Fund have offices in the United States?** [factual-lookup]
*(expects URL containing: `locations/united-states`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |


**Q2: How does Gen2 Fund handle AML and KYC compliance?** [api-function]
*(expects URL containing: `aml-kyc`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |


**Q3: What cash management and treasury services does Gen2 Fund offer?** [conceptual]
*(expects URL containing: `cash-management-treasury`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |


**Q4: Does Gen2 Fund work with emerging fund managers?** [conceptual]
*(expects URL containing: `emerging-managers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |


**Q5: Where is Gen2 Fund's Canada office?** [factual-lookup]
*(expects URL containing: `locations/canada`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |


**Q6: How did AI chatbots perform against private equity experts in Gen2's study?** [conceptual]
*(expects URL containing: `ai-chatbots-vs-pe-experts`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |


**Q7: What services does Gen2 Fund offer for mega fund managers with complex needs?** [conceptual]
*(expects URL containing: `services/mega-managers-complexity`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |


**Q8: Where can I find Gen2 Fund's regulatory public disclosures?** [factual-lookup]
*(expects URL containing: `regulatory/regulatory-public-disclosure`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |


**Q9: What does Gen2 Fund offer for private equity clients?** [conceptual]
*(expects URL containing: `client-sectors/private-equity`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |


**Q10: Where is Gen2 Fund's report on digitizing private equity?** [factual-lookup]
*(expects URL containing: `digitizing-private-equity-report`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | — | — | — | — | — | — | — |


</details>

## brex

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 100% (10/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 1.000 | 3683 | 150 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for brex</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do I manage virtual bookkeeping at my business?** [conceptual]
*(expects URL containing: `virtual-bookkeeping`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.brex.com/spend-trends/accounting/virtual-bookk | 0.695 | www.brex.com/spend-trends/accounting/virtual-bookk | 0.695 | www.brex.com/spend-trends/accounting/virtual-bookk | 0.691 |


**Q2: What are alternatives and competitors to Mercury business banking?** [factual-lookup]
*(expects URL containing: `mercury-alternatives-and-competitors`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.brex.com/spend-trends/business-banking/mercury | 0.822 | www.brex.com/spend-trends/business-banking/mercury | 0.812 | www.brex.com/spend-trends/business-banking/mercury | 0.799 |


**Q3: How do I get a DUNS number for my business?** [conceptual]
*(expects URL containing: `how-to-get-a-duns-number-for-my-business`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.brex.com/spend-trends/startup/how-to-get-a-dun | 0.779 | www.brex.com/spend-trends/startup/how-to-get-a-dun | 0.770 | www.brex.com/spend-trends/startup/how-to-get-a-dun | 0.763 |


**Q4: How do I create an expense report at my company?** [conceptual]
*(expects URL containing: `how-to-create-an-expense-report`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.brex.com/spend-trends/expense-management/how-t | 0.715 | www.brex.com/spend-trends/expense-management/how-t | 0.674 | www.brex.com/spend-trends/expense-management/how-t | 0.674 |


**Q5: What is Brex's cash flow management guide?** [conceptual]
*(expects URL containing: `cash-flow-management-guide`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.brex.com/spend-trends/cash-flow-management/cas | 0.743 | www.brex.com/spend-trends/cash-flow-management/cas | 0.727 | www.brex.com/spend-trends/cash-flow-management/cas | 0.726 |


**Q6: How does Brex handle ACH transfers?** [api-function]
*(expects URL containing: `support/ach-transfers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.brex.com/support/ach-transfers | 0.752 | www.brex.com/support/ach-transfers | 0.739 | www.brex.com/support/ach-transfers | 0.728 |


**Q7: What are business lines of credit for startups?** [conceptual]
*(expects URL containing: `business-lines-of-credit-for-startups`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.brex.com/spend-trends/business-banking/busines | 0.803 | www.brex.com/spend-trends/business-banking/busines | 0.799 | www.brex.com/spend-trends/business-banking/busines | 0.794 |


**Q8: How do I manage budgets and spend limits in Brex?** [api-function]
*(expects URL containing: `manage-budgets-and-spend-limits`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.brex.com/support/manage-budgets-and-spend-limi | 0.836 | www.brex.com/support/manage-budgets-and-spend-limi | 0.791 | www.brex.com/support/manage-budgets-and-spend-limi | 0.746 |


**Q9: How does Brex help companies get IPO ready?** [conceptual]
*(expects URL containing: `how-brex-helps-companies-get-ipo-ready`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.brex.com/journal/how-brex-helps-companies-get- | 0.855 | www.brex.com/journal/how-brex-helps-companies-get- | 0.814 | www.brex.com/journal/how-brex-helps-companies-get- | 0.807 |


**Q10: What is Brex's procure-to-pay solution?** [conceptual]
*(expects URL containing: `procurement/procure-to-pay`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | www.brex.com/spend-trends/procurement/procure-to-p | 0.691 | www.brex.com/spend-trends/procurement/procure-to-p | 0.686 | www.brex.com/spend-trends/procurement/procure-to-p | 0.683 |


</details>

## supabase-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 50% (5/10) | 50% (5/10) | 50% (5/10) | 50% (5/10) | 50% (5/10) | 0.500 | 382 | 300 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for supabase-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do automatic embeddings work in Supabase?** [api-function]
*(expects URL containing: `features/automatic-embeddings`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | supabase.com/blog/ai-inference-now-available-in-su | 0.603 | supabase.com/blog/supabase-ai-assistant-v2 | 0.554 | supabase.com/blog/chatgpt-plugins-support-postgres | 0.522 |


**Q2: How does Supabase's database branching feature work?** [api-function]
*(expects URL containing: `features/branching`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | supabase.com/blog/supabase-branching | 0.710 | supabase.com/blog/branching-publicly-available | 0.657 | supabase.com/blog/supabase-local-dev | 0.595 |


**Q3: How do I use Deno edge functions in Supabase?** [api-function]
*(expects URL containing: `features/deno-edge-functions`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | supabase.com/blog/edge-runtime-self-hosted-deno-fu | 0.670 | supabase.com/blog/supabase-dynamic-functions | 0.646 | supabase.com/blog/supabase-edge-functions | 0.628 |


**Q4: What are foreign data wrappers in Supabase?** [api-function]
*(expects URL containing: `features/foreign-data-wrappers`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | supabase.com/blog/postgres-foreign-data-wrappers-w | 0.665 | supabase.com/blog/calendars-in-postgres-using-fore | 0.618 | supabase.com/blog/postgres-foreign-data-wrappers-r | 0.614 |


**Q5: How does Supabase handle database backups?** [api-function]
*(expects URL containing: `features/database-backups`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | supabase.com/blog/supabase-beta-march-2021 | 0.601 | supabase.com/blog/supabase-cli | 0.597 | supabase.com/alternatives/supabase-vs-firebase | 0.593 |


**Q6: How does Supabase compare to Firebase?** [factual-lookup]
*(expects URL containing: `alternatives/supabase-vs-firebase`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | supabase.com/alternatives/supabase-vs-firebase | 0.810 | supabase.com/alternatives/supabase-vs-firebase | 0.807 | supabase.com/alternatives/supabase-vs-firebase | 0.803 |


**Q7: How did Mobbin scale to 200,000 users on Supabase?** [conceptual]
*(expects URL containing: `mobbin-supabase-200000-users`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | supabase.com/blog/mobbin-supabase-200000-users | 0.705 | supabase.com/blog/mobbin-supabase-200000-users | 0.683 | supabase.com/blog/mobbin-supabase-200000-users | 0.670 |


**Q8: How did Epsilon3 self-host Supabase?** [conceptual]
*(expects URL containing: `epsilon3-self-hosting`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | supabase.com/blog/epsilon3-self-hosting | 0.733 | supabase.com/blog/epsilon3-self-hosting | 0.685 | supabase.com/blog/epsilon3-self-hosting | 0.662 |


**Q9: Does Supabase have a Python client library?** [api-function]
*(expects URL containing: `features/client-library-python`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | supabase.com/blog/python-support | 0.782 | supabase.com/blog/loading-data-supabase-python | 0.655 | supabase.com/blog/improved-dx | 0.609 |


**Q10: Can Supabase transform images on the fly?** [api-function]
*(expects URL containing: `features/image-transformations`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | miss | supabase.com/blog/storage-image-resizing-smart-cdn | 0.622 | supabase.com/blog/storage-v3-resumable-uploads | 0.559 | supabase.com/blog/supabase-dashboard-performance | 0.528 |


</details>

## tailwind-docs

| Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
|---|---|---|---|---|---|---|---|---|
| markcrawl | 90% (9/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 100% (10/10) | 0.950 | 1453 | 200 |

> **Chunks** = total chunks from this tool for this site. **Pages** = pages crawled. Hit rates shown as % (hits/total queries).

<details>
<summary>Query-by-query results for tailwind-docs</summary>

> **Hit** = rank position where correct page appeared (#1 = top result, 'miss' = not in top 20). **Score** = cosine similarity between query embedding and chunk embedding.

**Q1: How do I set perspective on an element in Tailwind CSS?** [api-function]
*(expects URL containing: `docs/perspective`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | tailwindcss.com/docs/perspective | 0.689 | tailwindcss.com/docs/perspective-origin | 0.678 | tailwindcss.com/docs/responsive-design | 0.588 |


**Q2: How do I apply margin utilities in Tailwind?** [api-function]
*(expects URL containing: `docs/margin`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | tailwindcss.com/docs/margin | 0.730 | tailwindcss.com/docs/margin | 0.724 | tailwindcss.com/docs/margin | 0.670 |


**Q3: How do I control flex basis in Tailwind?** [api-function]
*(expects URL containing: `docs/flex-basis`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | tailwindcss.com/docs/flex-basis | 0.674 | tailwindcss.com/docs/flex-basis | 0.641 | tailwindcss.com/docs/flex-basis | 0.625 |


**Q4: How do I use hover and focus variants in Tailwind?** [conceptual]
*(expects URL containing: `docs/hover-focus-and-other-states`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | tailwindcss.com/docs/hover-focus-and-other-states | 0.765 | tailwindcss.com/docs/hover-focus-and-other-states | 0.754 | tailwindcss.com/docs/hover-focus-and-other-states | 0.754 |


**Q5: How do I define grid auto columns in Tailwind?** [api-function]
*(expects URL containing: `docs/grid-auto-columns`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | tailwindcss.com/docs/grid-auto-columns | 0.735 | tailwindcss.com/docs/grid-template-columns | 0.687 | tailwindcss.com/docs/columns | 0.685 |


**Q6: How do I transform text case (uppercase, lowercase) in Tailwind?** [api-function]
*(expects URL containing: `docs/text-transform`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | tailwindcss.com/docs/text-transform | 0.730 | tailwindcss.com/docs/translate | 0.582 | tailwindcss.com/docs/transform | 0.563 |


**Q7: How do I control background image size in Tailwind?** [api-function]
*(expects URL containing: `docs/background-size`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | tailwindcss.com/docs/background-size | 0.671 | tailwindcss.com/docs/background-image | 0.617 | tailwindcss.com/docs/background-image | 0.613 |


**Q8: How do I apply a backdrop blur filter in Tailwind?** [api-function]
*(expects URL containing: `docs/backdrop-filter-blur`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #2 | tailwindcss.com/docs/backdrop-filter | 0.678 | tailwindcss.com/docs/backdrop-filter-blur | 0.667 | tailwindcss.com/docs/backdrop-filter-grayscale | 0.604 |


**Q9: How do I install Tailwind using the CLI?** [conceptual]
*(expects URL containing: `docs/installation/tailwind-cli`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | tailwindcss.com/docs/installation/tailwind-cli | 0.759 | tailwindcss.com/docs/installation/using-postcss | 0.600 | tailwindcss.com/docs/upgrade-guide | 0.566 |


**Q10: How do I specify which CSS properties transition in Tailwind?** [api-function]
*(expects URL containing: `docs/transition-property`)*

| Tool | Hit | Top-1 URL | Score | Top-2 URL | Score | Top-3 URL | Score |
|---|---|---|---|---|---|---|---|
| markcrawl | #1 | tailwindcss.com/docs/transition-property | 0.805 | tailwindcss.com/docs/transition-property | 0.756 | tailwindcss.com/docs/transition-property | 0.747 |


</details>

## Methodology

- **Queries:** 149 across 12 sites, categorized by type (api-function, code-example, conceptual, structured-data, factual-lookup, cross-page, navigation, js-rendered)
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

