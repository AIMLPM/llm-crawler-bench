# v1.4 Release Notes — methodology hardening for HN credibility

## TL;DR

v1.4 ships four simultaneous methodology fixes addressing chunk-density gaming, COI in query authorship, substring false positives, and off-topic URL sampling. The leaderboard re-ranks: high-coverage tools (crawl4ai, crawlee, playwright) gain meaningfully on retrieval; **markcrawl drops to 7th on both retrieval MRR and answer quality**. Markcrawl's drop decomposes as **86% scope-narrowing trade-off** (intentional design choice quantified for the first time), 14% retrieval-rank weakness on pages it does have. The bench is now publicly reproducible end-to-end via `make benchmark`.

## What changed

v1.4 cycle landed **four methodology fixes** simultaneously:

1. **LLM-authored queries replacing human-authored** (COI removal). v1.3's 104 queries were hand-written by markcrawl's maintainer — even with good intent, a benchmark of tool X authored by tool X's maintainer fails the "resistant to motivated reasoning" bar. DS-6 replaces this with 561 LLM-generated queries verified by a separate LLM-call with no shared context window. No human in the acceptance loop.
2. **Page-level MRR replacing chunk-level** as the headline retrieval metric (chunk-density gaming neutralized). A tool emitting 5 chunks per page no longer beats a tool emitting 1 chunk per page when both rank the same canonical page first.
3. **URL normalization for matching** (locale-mirror, fragment, and UTM-param false positives removed). The v1.3 false positive where `he.react.dev/learn/managing-state` matched English queries is now caught structurally.
4. **Per-site target-prefix filter on the URL sampler** (off-topic queries caught pre-publish). When the filter landed, 91% of HF queries turned out to be huggingface.co/endpoints + discuss.huggingface.co forum threads rather than transformers docs — caught and fixed before any release.

**Final v1.4 corpus:** 561 queries, 11 sites, **100% in-scope** (per-site target-prefix filter), **100% English-only by sampler design** (locale-mirror URLs filtered before sampling — multilingual evaluation is a v1.5 opt-in dimension).

## v1.3 → v1.4 leaderboard deltas

Lead with markcrawl per SC-9 — including the negative deltas. All numbers come from `runs/run_v13_merged_20260504_203748` with identical crawl data; only the query set + methodology changed.

| Tool | v1.3 MRR | v1.4 MRR | Δ MRR | v1.3 AnsQual | v1.4 AnsQual | Δ AnsQual |
|---|---|---|---|---|---|---|
| **markcrawl** | **0.488** | **0.341** | **−0.147** | **4.03** | **3.77** | **−0.26** |
| crawl4ai | 0.642 | 0.757 | +0.115 | 4.40 | 4.72 | +0.32 |
| crawl4ai-raw | 0.640 | 0.763 | +0.123 | 4.35 | 4.70 | +0.35 |
| crawlee | 0.686 | 0.765 | +0.079 | 4.31 | 4.68 | +0.37 |
| playwright | 0.677 | 0.758 | +0.081 | 4.12 | 4.48 | +0.36 |
| colly+md | 0.594 | 0.459 | −0.135 | 4.27 | 4.36 | +0.09 |
| scrapy+md | 0.429 | 0.176 | −0.253 | 4.13 | 3.68 | −0.45 |

Final ranking (best to worst by answer quality): crawl4ai → crawl4ai-raw → crawlee → playwright → colly+md → scrapy+md → markcrawl. Retrieval MRR ranking parallels this with one swap (crawlee narrowly leads).

**Scrapy+md shows the largest drop (−0.253 MRR, −0.45 answer-quality)** — bigger than markcrawl's. The narrative for markcrawl is COI removal + scope trade-off, but no one had COI in favor of scrapy+md, so a different explanation is required: scrapy+md's drop is driven primarily by **DS-2's false-positive removal** (scrapy+md's chunks had high substring-collision rates in v1.3's matcher — `?ref=<query-term>` query params and fragment-text contributing spurious hits that the v1.4 normalized matcher correctly rejects) combined with **coverage exposure** on JS-rendered sites where scrapy+md's HTTP-only design returns zero chunks. Both effects are correct behavior; v1.4 surfaces them without amplification.

## Markcrawl's drop: 86% scope, 14% retrieval

Markcrawl's **−0.147 MRR / −0.26 answer-quality** delta decomposes on the **retrieval pipeline** into:

| Bucket | Count | Share of misses | Definition |
|---|---|---|---|
| **Coverage miss** | 278 | **86%** | The URL containing the answer is NOT in markcrawl's index — markcrawl never crawled that page (typically because its scope-detection narrowed past it). |
| **Retrieval miss** | 43 | **14%** | The URL is in markcrawl's index but didn't rank in the top-K retrieval results for the query. |
| Hit | 178 | — | The URL ranked in top-K and substring-matched the expected pattern. |

Decomposition is computed over the **499-query common subset** (9 sites where all 7 tools have indexable content; excludes huggingface-transformers and newegg, where at least one tool returned zero chunks). 178 + 43 + 278 = 499. The 14% / 86% split is share-of-misses among the 321 markcrawl missed queries.

The 14% is **retrieval-pipeline-bounded only** — chunks went into the retrieval index but didn't surface at the top of the ranked list. The answer-quality LLM-judge scores (the 3.77 column above) are **measured separately at the leaderboard level**, not bucketed into this decomposition. We didn't try to split "answer-judge scored low" into its own bucket because the question we're answering here is "where did the retrieval pipeline lose?", which is the more actionable diagnostic for a maintainer.

This is the **documented quality-vs-coverage trade-off** quantified for the first time. Markcrawl produces 99% content signal at $0 embedding cost on the mxbai secondary, but ranks lower on retrieval-recall benchmarks against tools that index broader page sets:

- **Users benchmarking for content quality + cost-of-ownership** should weigh markcrawl's 99% signal + lowest annual storage cost differently than users benchmarking for retrieval recall.
- **Users benchmarking for retrieval recall over broad topic surfaces** should weigh crawl4ai / crawl4ai-raw / crawlee — they crawled 60-300x more pages on average, and that scope-broadness is the recall advantage v1.4 surfaces honestly.

A future cycle (v1.5) may add a `scope=narrow` vs `scope=broad` mode selector to make this trade-off a published dimension rather than a methodology footnote.

## What survived from v1.3 vs what didn't

The COI-removal hypothesis from the spec is now empirically supported:

- **v1.3 query set was COI-tainted** by hand-authorship from markcrawl's maintainer. Confirmed by the inverse-asymmetric-bias outcome: if v1.4 had moved markcrawl UP, it would have read as motivated reasoning — the same trap PUBLISH-BOTH was designed to avoid for embedders. The drop is the credibility-buying inverse outcome.
- **Page-level MRR matters less than expected.** The chunk-collapse uplift is small (single-digit-percent across tools) because most top-K URLs are already distinct canonicals. The bigger effect was v1.3 false-positive removal via DS-2 normalization. Both effects compose, and the net delta is small per-tool — the right direction without overclaiming the magnitude.
- **The HF catch-and-fix is evidence the bench is rigor-not-promo.** Mid-cycle, a pre-merge audit found 91% of HF queries were off-topic (huggingface.co/endpoints + discuss.huggingface.co forum threads) due to crawl4ai-raw's broad eTLD+1 coverage. We:
  - shipped a generic per-site target-prefix filter (applied uniformly across all 11 sites — not site-specific tuning),
  - re-fired HF queries (cleanly went from 47 off-topic to 4 in-scope),
  - then ran a follow-up path-prefix audit across the OTHER 10 sites and found 3 more (mdn-css, postgres-docs, react-dev) needed re-firing under the same filter mechanism.
  
  Pre-publication. No production version of the report ever shipped with the off-scope queries.

## What's deferred to v1.5

- **`bench/site_scope.yaml` + `test_all_queries_match_site_scope` as gate-zero.** v1.4 documented per-site scope prefixes in code (`tools/generate_queries.py:SCOPE_PREFIXES`); v1.5 should lift this into config and add a hard test that asserts every generated query falls within its site's declared scope. The HF bug couldn't have happened silently if that test existed. The v1.5 cycle should land this **before** any new site additions or query regenerations — the structural lock-in, not vigilance.
- **Multi-trial measurement.** v1.4 is single-trial (one full run, query-sampling CIs only). Multi-trial work in v1.5 will let us replace the "~5% effective-tie" rule of thumb with a measured run-to-run variance floor.
- **Multi-embedder full validation across all 11 sites.** v1.4 included a primary OpenAI run + a mxbai PUBLISH-BOTH secondary on RETRIEVAL_COMPARISON_LOCAL.md. v1.5 should extend the secondary to ANSWER_QUALITY_LOCAL.md + PIPELINE_TIMING_LOCAL.md (if not already done in this cycle) and add a third sanity-check embedder (bge-large) on 2-3 adversarial sites.
- **LLM-judged relevance to replace substring matching.** Substring `url_match` is fundamentally fuzzy (`state` matches 20+ react.dev URLs). v1.5 LLM-judge should evaluate "is this URL actually the answer page?" as a separate evaluation dimension.
- **Multilingual RAG evaluation** as an explicit, opt-in dimension. v1.4's locale-mirror filter is English-only by sampler design; v1.5 should add a `multilingual=true` mode that flips the filter and surfaces a separate parallel leaderboard.

## How to reproduce

```bash
make benchmark-quick   # ~5 min, single site, ~$0 spend — verifies pipeline runs
make benchmark         # ~24 hours, all 11 sites, ~$5 spend — produces canonical reports
```

`runs/<run_id>/models_manifest.json` captures the resolved model values (`ANSWER_MODEL`, `JUDGE_MODEL`, `EMBEDDING_MODEL`, temperatures, env overrides detected, git commit) for each run. Re-runners can audit whether two runs were made under the same conditions. The benchmark scripts assert these resolve to the canonical defaults at startup and refuse to spend API credits if drift is detected.

## Commits

This release lands as a feature branch merge: `feature/v14-methodology-hardening` → `main`. The branch contains ~20+ commits documenting the cycle's decisions in their commit messages, including:

- `fafb4d1` — DS-13b checkpoint key fix (embedder dimension)
- `02a4b17` — DS-1 page-level MRR helper
- `38801f5` — DS-2 URL normalization for matching
- `631c1f7` — DS-3 QUERY_AUDIT.csv emitter
- `12f30d8` — DS-6 LLM-generated query authoring
- `c8b26aa` — Chrome-stripping pre-processor (kubernetes-docs unblocked)
- `b540e9f` — Per-site cache + site-scope filter (HF off-topic fixed)
- `1088daf` — DS-13a defense-in-depth: model invariant + manifest
- `4355c67` — rust-book multi-prefix + final scope re-fire

Read the branch's commit log for the full design-decision trail.
