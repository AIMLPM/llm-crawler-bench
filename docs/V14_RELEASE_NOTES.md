# v1.4 Release Notes — methodology hardening for HN credibility

## TL;DR

v1.4 ships four simultaneous methodology fixes addressing chunk-density gaming, COI in query authorship, substring false positives, and off-topic URL sampling. The leaderboard re-ranks: high-coverage tools (crawl4ai, crawlee, playwright) gain meaningfully on retrieval; **markcrawl drops to 7th on both retrieval MRR and answer quality, and is 3rd on cost under the OpenAI fairness contract** (crawl4ai-raw 1st at $3,787/yr, markcrawl 3rd at $4,755/yr, mid-scale). Markcrawl's retrieval drop decomposes as **86% scope-narrowing trade-off** (intentional design choice quantified for the first time), 14% retrieval-rank weakness on pages it does have. Two methodologically-interesting findings emerge alongside the headline: (a) **the COI in v1.3's hand-written queries was bigger than we had quantified** — the same query authorship that boosted markcrawl on answer quality also produced the May 6 mxbai asymmetric-bias finding, which does not survive v1.4's LLM-authored queries; and (b) **a previously-unobserved retrieval-vs-answer-quality decoupling under embedder choice** (markcrawl alone has a non-negative mxbai answer-quality delta even after the retrieval asymmetry vanishes; single-trial, flagged for v1.5 multi-trial). The bench is now publicly reproducible end-to-end via `make benchmark`.

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

**Per-query audit of the 43 retrieval-bucket misses surfaces two sub-categories worth disclosing:**

- **~9-12 are aggregator-page pollution** (a markcrawl-side URL-filter bug, not a retrieval-algorithm weakness). Markcrawl is returning `/print.html` (rust-book — 49% of top-5 slots) and `/_print/` (kubernetes-docs — 39% of top-5 slots) in places where the canonical-content page should appear. All five competitors except scrapy+md return 0% `/_print/` on kubernetes-docs. Fix shipping in markcrawl v0.11.1; expected MRR lift +0.02-0.04 on the 9-site pool concentrated on rust-book and kubernetes-docs.
- **~18-20 are substring-match false negatives** (single-reviewer categorization; precise count subject to disagreement, qualitative finding robust) — the bench's `url_match` substring matcher counts these as misses, but the chunk markcrawl returned is semantically more relevant than the canonical pattern URL. Examples: kubernetes-docs query "role of kube-scheduler" → markcrawl returned the kube-scheduler doc page at rank 1, but the pattern points to the architecture overview; stripe-docs query "What is a Checkout Session?" → markcrawl returned the checkout-sessions doc, pattern points to accept-a-payment; mdn-css query on logical-properties → markcrawl returned the writing-modes guide, pattern points elsewhere. **The 14% bucket overstates retrieval-pipeline weakness because substring matching counts some semantically-correct retrievals as misses.** v1.5 LLM-judged relevance (already on the deferral list) will tighten this estimate. The remaining ~13-16 are likely genuine retrieval-rank misses.

The 14% number is the load-bearing metric; the sub-bucketing tells maintainers where to look. The 86% coverage finding is unaffected by these caveats — coverage misses are independent of substring matching since the URL is absent from the index entirely.

The 14% is **retrieval-pipeline-bounded only** — chunks went into the retrieval index but didn't surface at the top of the ranked list. The answer-quality LLM-judge scores (the 3.77 column above) are **measured separately at the leaderboard level**, not bucketed into this decomposition. We didn't try to split "answer-judge scored low" into its own bucket because the question we're answering here is "where did the retrieval pipeline lose?", which is the more actionable diagnostic for a maintainer.

This is the **documented quality-vs-coverage trade-off** quantified for the first time. Markcrawl produces 99% content signal under its shipping local-embedder default ($0 embedding cost — the mxbai-embed-large-v1 model runs on CPU/MPS), but ranks lower on retrieval-recall benchmarks against tools that index broader page sets:

- **Users benchmarking for retrieval recall over broad topic surfaces** should weigh crawl4ai / crawl4ai-raw / crawlee — they crawled 60-300x more pages on average, and that scope-broadness is the recall advantage v1.4 surfaces honestly.
- **Users benchmarking for content quality + retrieval rank under markcrawl's shipping default** should consider the PUBLISH-BOTH secondary leaderboard: under `mxbai-embed-large-v1` (markcrawl's default since v0.10.1), markcrawl ranks higher on retrieval MRR (asymmetric-bias finding: +0.043 MRR while every other tool drops −0.007 to −0.077). See `reports/RETRIEVAL_COMPARISON_LOCAL.md`.

A future cycle (v1.5) may add a `scope=narrow` vs `scope=broad` mode selector to make this trade-off a published dimension rather than a methodology footnote.

## PUBLISH-BOTH at v1.4 — asymmetric-bias narrative reshape

The May 6 mxbai validation under v1.3's hand-written queries showed markcrawl as the only tool with a positive mxbai delta (+0.043 MRR vs OpenAI), with every competitor scoring lower under mxbai. We attributed this to embedder-side asymmetry favoring markcrawl's clean-chunk output, and chose PUBLISH-BOTH (parallel never-mixed leaderboards) rather than switch primary to mxbai — the asymmetric bias would have read as motivated reasoning.

**Re-running the same mxbai validation under v1.4's LLM-authored queries reshapes that finding.** Per-tool deltas under both query sets:

### Retrieval MRR delta (mxbai − OpenAI), best-mode per tool, 9-site common subset

| Tool | May 6 Δ (v1.3 queries) | v1.4 Δ | Direction |
|---|---|---|---|
| markcrawl | +0.043 | **+0.002** | gain collapsed to noise |
| crawl4ai | −0.009 | **+0.011** | flipped to positive |
| crawl4ai-raw | −0.007 | **+0.007** | flipped to positive |
| scrapy+md | −0.077 | **+0.003** | flipped to positive |
| colly+md | −0.047 | −0.022 | smaller negative |
| playwright | −0.037 | −0.036 | unchanged |
| crawlee | −0.020 | **−0.058** | larger negative |

### Answer-quality delta (mxbai − OpenAI), 11-site corpus, gpt-4o-mini judge

| Tool | v1.4 Δ AnsQual | Direction |
|---|---|---|
| markcrawl | +0.02 | small positive (within single-trial LLM-judge noise; see caveat) |
| crawl4ai | −0.05 | negative |
| crawl4ai-raw | −0.04 | negative |
| crawlee | **−0.20** | **largest negative — independent finding, see below** |
| playwright | −0.08 | negative |
| colly+md | −0.10 | negative |
| scrapy+md | −0.09 | negative |

**What this means: the May 6 retrieval-side asymmetric-bias finding does not survive the methodology hardening.** The most plausible single contributor is the COI removal — v1.3's hand-written queries (authored by markcrawl's maintainer) may have phrased questions in ways that aligned with patterns mxbai captured more strongly than text-embedding-3-small for markcrawl-output chunks specifically. Removing the COI in DS-6's LLM-authored query set largely neutralized the apparent retrieval bias.

**The COI was bigger than we had quantified — but it's not the whole story.** The v1.4 retrieval pattern is not uniform convergence to zero: crawlee's mxbai delta moved further negative (−0.020 → −0.058), and crawl4ai / crawl4ai-raw / scrapy+md flipped to small positives. This suggests the v1.4 query distribution interacts with embedder choice in ways that aren't reducible to a single "COI-was-the-source" mechanism. Multi-trial measurement in v1.5 should help disentangle.

**Answer quality preserves a markcrawl-favorable pattern that retrieval mostly lost.** On answer quality at v1.4, markcrawl is the only tool with a non-negative mxbai delta. This suggests a mechanistic decoupling: at similar MRR levels, the embedder choice still affects WHICH chunks rank in the top-K, even when the COUNT of relevant chunks retrieved is similar. Markcrawl's chunks are designed to maximize answer-relevant content density per token (its stated product goal), so when mxbai's ranking surfaces those chunks, the downstream LLM scores higher. **MRR measures whether some relevant chunk was found; answer quality measures the specific chunks' content density.** The decoupling appears mechanistic rather than accidental, though multi-trial v1.5 measurement is required to confirm.

**Single-trial caveat applies extra strongly to this finding.** v1.4 numbers are single-trial; the LLM-judge noise floor at site-pool level is approximately ±0.02-0.03. Markcrawl's +0.02 answer-quality delta is directionally clean but within that noise band. Per-tool retrieval-delta magnitudes < ~0.02 (the small flips: crawl4ai −0.009 → +0.011, crawl4ai-raw −0.007 → +0.007) are similarly within plausible single-trial variance and may not be real reversals. Multi-trial measurement (v1.5) will produce CI bounds on each delta. The large effects (markcrawl's gain collapse, scrapy+md's magnitude collapse, crawlee's growing negative on retrieval, crawlee's −0.20 on answer quality) are robustly outside a plausible single-trial noise floor.

**Crawlee's −0.20 answer-quality regression is the largest mxbai effect at v1.4 and worth flagging independently.** This isn't a markcrawl-side story — it's an embedder/tool interaction where mxbai consistently surfaces lower-quality crawlee chunks than text-embedding-3-small does. We don't have a clean mechanism yet and flag this for v1.5 multi-trial confirmation + chunk-content inspection. If the effect holds, it could be a useful methodology paper in itself (chunk-shape / embedder-affinity interactions).

PUBLISH-BOTH still ships (`reports/RETRIEVAL_COMPARISON_LOCAL.md` and `reports/ANSWER_QUALITY_LOCAL.md` are published as parallel never-mixed leaderboards) — but the published rationale shifts from "asymmetric retrieval bias forces PUBLISH-BOTH" to "we ship both for transparency, $0-embedding-cost-pathway publication, and to surface the answer-quality dimension where the asymmetry persists." METHODOLOGY's "Embedder choice and PUBLISH-BOTH decision" section gets a "v1.4 update" note documenting this reshape; the May 6 finding stays in the audit trail as a methodology data point, not as a load-bearing claim.

## Cost methodology note

The cost figures are computed under the fairness contract: OpenAI text-embedding-3-small for every tool, uniformly — the same comparable basis we used for retrieval MRR. Under this contract, markcrawl is 3rd ($4,755/yr at 100K pages × 1K queries/day) behind crawl4ai-raw 1st ($3,787) and crawl4ai 2nd ($3,824). The v1.3 → v1.4 ranking inverted partly because the v1.4 calculator refresh corrected stale chunk counts and partly because tool versions shifted in the cycle (notably crawl4ai's chunker reducing chunks/page on docs sites).

Users running markcrawl with its shipping default (local mxbai-embed-large-v1 since v0.10.1) save ~$7/yr on embedding — but **the cost ranking does not change**: markcrawl is still 3rd at $4,748/yr. Vector-DB storage dominates the cost line on RAG ingestion at this scale, not embedding inference cost. The "$0 local embedding" framing markcrawl shipped with v0.10.1 was a meaningful cost-positioning claim against v0.9.x's OpenAI-only embedder default — but it is **not** sufficient to win cost vs. competitors who produce smaller chunk indices. See `reports/COST_AT_SCALE_LOCAL.md` for the full mxbai-pricing breakdown.

Run `python tools/cost_calculator.py --embedder=local-mxbai --sensitivity` for the mxbai breakdown + ±50% pricing sensitivity.

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
- **Multi-trial measurement.** v1.4 is single-trial (one full run, query-sampling CIs only). Multi-trial work in v1.5 will let us replace the "~5% effective-tie" rule of thumb with a measured run-to-run variance floor — and confirm whether the small mxbai retrieval-delta flips at v1.4 (markcrawl +0.002, crawl4ai +0.011, etc.) are real reversals or within-noise. The large effects (crawlee retrieval −0.058, crawlee answer-quality −0.20, scrapy+md retrieval magnitude collapse) are robust to single-trial noise.
- **Multi-embedder full validation across all 11 sites.** v1.4 ships PUBLISH-BOTH primary OpenAI + mxbai secondary on retrieval, answer-quality, and cost. v1.5 should add a third sanity-check embedder (bge-large) on 2-3 adversarial sites to confirm the v1.4 asymmetric-bias-reshape isn't mxbai-specific.
- **LLM-judged relevance to replace substring matching.** Substring `url_match` is fundamentally fuzzy. ~18-20 of markcrawl's 43 retrieval-bucket misses (40-46%) audit as substring-match false negatives where markcrawl returned semantically more relevant pages than the canonical pattern. v1.5 LLM-judge should evaluate "is this URL actually the answer page?" as a separate evaluation dimension; under that lens the markcrawl 14% retrieval-bucket would shrink materially.
- **Multilingual RAG evaluation** as an explicit, opt-in dimension. v1.4's locale-mirror filter is English-only by sampler design; v1.5 should add a `multilingual=true` mode that flips the filter and surfaces a separate parallel leaderboard.
- **Crawlee/mxbai chunk-shape investigation.** Crawlee shows the largest mxbai answer-quality regression at −0.20, robust to single-trial noise. We don't have a clean mechanism yet. v1.5 should pair multi-trial confirmation with chunk-content inspection (what about crawlee's chunks makes mxbai surface lower-quality content than text-embedding-3-small does?). Could be a methodology paper in itself.
- **Markcrawl v0.11.1 aggregator-page URL filter** (markcrawl-side, not bench-side). markcrawl is returning `/print.html` (rust-book) and `/_print/` (kubernetes-docs) at high rates in v1.4 retrieval; competitors return 0%. ~9-12 of markcrawl's 43 retrieval-bucket misses concentrate on this. Fix expected to lift markcrawl MRR +0.02-0.04 on the 9-site pool. v1.5 bench cycle should re-run after that markcrawl release lands.

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
