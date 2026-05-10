---
spec_version: 2
name: v1.4 Methodology Hardening — HN-credibility pass
status: draft
size: L
date: 2026-05-06
branch: feature/v14-methodology-hardening
depends_on: []
affected_code:
  - benchmark_retrieval.py
  - benchmark_answer_quality.py
  - benchmark_pipeline.py
  - reports/METHODOLOGY.md
  - reports/SPEED_COMPARISON.md
  - reports/QUALITY_COMPARISON.md
  - reports/RETRIEVAL_COMPARISON.md
  - reports/ANSWER_QUALITY.md
  - reports/PIPELINE_TIMING.md
  - reports/COST_AT_SCALE.md
  - sites/pool_v1.yaml
  - tools/generate_queries.py (new)
  - tools/cost_calculator.py (new)
  - tools/page_level_mrr.py (new)
  - reports/QUERY_AUDIT.csv (new artifact)
constitution_reviewed: false
---

# v1.4 Methodology Hardening — HN-credibility pass

## Problem Statement

The v1.3 benchmark numbers are technically correct but methodologically vulnerable to a determined hostile reviewer (HN, IR researchers, ex-Google search). The biggest concrete weaknesses:

1. **Conflict-of-interest in query authorship** — queries were hand-written by the maintainer of the tool being measured (markcrawl). Even with good intent, this fails the "resistant to motivated reasoning" bar.
2. **Chunk-density gaming** — current MRR rewards crawlers that emit more chunks per page. Markcrawl's clean output (30K chunks) is penalized vs nav-bloated output (58-65K chunks) even when content quality is higher.
3. **Pattern-match ground truth** — `url_match` substring matching produced false positives like `he.react.dev/` (Hebrew locale) counted as a hit for English queries.
4. **No reproducibility artifact** — every claim in reports is currently "trust me." HN reviewers expect a single command that regenerates the numbers.
5. **Cost numbers are hand-waved** — `$4,505/yr` bakes in many unstated assumptions (queries/day, embedding price, dedup ratio); reviewers can't audit.
6. **No leaderboard diff vs prior version** — without showing how methodology changes affected the ranking, reviewers will compute the diff themselves and accuse us of burying improvements that hurt markcrawl.

If shipped publicly without addressing these, the response will be predictable: "you wrote queries to favor your tool, MRR is sensitive to chunking, cost is hand-waving, can't reproduce." The bar isn't "is this honest" — it's "is this resistant to motivated reasoning."

**Out of scope:** Multi-trial measurement (deferred to v1.5 — single-trial constraint imposed by current hardware, documented as a caveat). LLM-judge for ground truth (deferred to v1.5 — expensive). Full multi-embedder validation (deferred to v1.5 — single sanity-check on 2 sites is included). External human-authored queries (deferred — LLM-generated + LLM-verified is the v1.4 acceptable substitute).

## Solution Summary

Two-phase delivery. **Tier 1** (1-2 days) lands purely additive credibility improvements: page-level MRR alongside chunk-level, URL normalization, per-query audit CSV, author-disclosure section in METHODOLOGY, prominent single-trial caveat on every report. **Tier 2** (2-3 days) lands the deeper methodology changes: LLM-generated + LLM-verified query set replacing hand-written queries, Hit@1/@3/@5/@10 reported alongside MRR, anti-gaming methodology section, cost calculator with sensitivity analysis, single-secondary-embedder sanity check on 2 sites, reproducibility artifact (`make benchmark`), v1.3→v1.4 leaderboard-diff release note. The single biggest credibility move is removing all human authors from the query-acceptance loop (Refinement 1 to original plan); the single biggest methodological-maturity signal is leading the v1.4 release with the leaderboard diff, even when it makes markcrawl look worse.

## Success Criteria

- **SC-1** — **Given** a v1.4 retrieval run, **When** RETRIEVAL_COMPARISON.md is generated, **Then** every site section reports BOTH chunk-level MRR (current) and page-level MRR (new), with the page-level computed by collapsing all chunks per URL into a single rank before computing MRR.
- **SC-2** — **Given** a query whose `url_match` is `state`, **When** retrieval matches a chunk from `he.react.dev/learn/managing-state`, **Then** the chunk is NOT counted as a hit because locale-prefixed URLs are normalized to their canonical hostname before matching. The same rule applies to `de.`, `es.`, `fr.`, `ja.`, `zh.`, etc.
- **SC-3** — **Given** any v1.4 retrieval run, **When** the run completes, **Then** `reports/QUERY_AUDIT.csv` is written containing one row per (query, tool, rank) with columns `[query_id, query_text, site, tool, rank, url, cosine_score, is_hit, url_match_pattern]` for ranks 1-5. Anyone can spot-check claims by reading the CSV.
- **SC-4** — **Given** v1.4 reports are generated, **When** a reader opens METHODOLOGY.md, **Then** they find an "Author and conflict-of-interest disclosure" section explicitly naming who wrote queries / runners / methodology and stating the LLM-only query verification process. They also find the prominent single-trial caveat on every report header.
- **SC-5** — **Given** v1.4 query-set generation, **When** `tools/generate_queries.py` runs, **Then** it samples URLs from the highest-coverage tool's pages.jsonl per site, calls gpt-4o-mini to draft 1-2 questions per URL, AND verifies each draft query with a second independent gpt-4o-mini invocation (no prior context, no human reviewer in the acceptance loop). Rejected queries are logged with rationale; accepted queries are written to `queries/v14_queries.json`.
- **SC-6** — **Given** v1.4 retrieval results, **When** RETRIEVAL_COMPARISON.md renders the per-tool table, **Then** Hit@1, Hit@3, Hit@5, Hit@10 are ALL shown (currently only Hit@10 + MRR), with explanatory text noting Hit@1 is least density-sensitive and MRR most.
- **SC-7** — **Given** v1.4 METHODOLOGY.md, **When** read, **Then** it contains an explicit "Anti-gaming" section enumerating known attacks (chunk-density inflation, locale duplication, URL-text injection, hub-page inflation, embedder favoritism, COI) with the defense applied or noted limitation for each.
- **SC-8** — **Given** a fresh checkout, **When** the user runs `make benchmark` (or `docker compose run benchmark`), **Then** the entire pipeline (crawl → quality → retrieval → answer-quality → pipeline) runs end-to-end against the v1.4 query set and produces the same final reports modulo network noise (recorded in commit `<hash>`).
- **SC-9** — **Given** v1.4 release notes, **When** published, **Then** they lead with a v1.3→v1.4 leaderboard diff table showing every tool's per-dimension delta (e.g., "markcrawl chunk-MRR 0.488 → page-Hit@1 0.X; Δ−0.Y vs v1.3"). If markcrawl looks worse on any dimension, the writeup leads with that delta.
- **SC-10** — **Given** v1.4 cost claims, **When** a reader opens COST_AT_SCALE.md, **Then** they find a `tools/cost_calculator.py` script (or equivalent spreadsheet) with adjustable inputs (queries/day, embedding price, chunk count, dedup ratio) AND a sensitivity table showing how the ranking shifts when each input moves ±50%.
- **SC-11** — **Given** v1.4 retrieval methodology, **When** anyone questions whether the leaderboard depends on the embedder choice, **Then** METHODOLOGY.md cites the **full-set mxbai validation already completed** (Kendall's Tau=+0.952 aggregate; per-site median Tau=+0.476 with range -0.048 to +0.952; asymmetric directional bias: markcrawl +0.043 vs all 6 other tools -0.007 to -0.077) AND optional adversarial-3-site sanity check with `BAAI/bge-large-en-v1.5` (rust-book + react-dev + postgres-docs). The conclusion is documented as **PUBLISH-BOTH, not switch**: OpenAI 3-small remains primary because of (a) v1.3 comparability, (b) asymmetric bias would compromise credibility if we switched. mxbai is a peer-published secondary leaderboard, never mixed with primary. Full multi-embedder validation across all 11 sites with bge-large is explicitly deferred to v1.5.
- **SC-12** — **Given** v1.4 supports a fully-local-embedder mode, **When** a user runs `EMBEDDING_MODEL=mixedbread-ai/mxbai-embed-large-v1 make benchmark` (no `OPENAI_API_KEY` for embedding), **Then** the entire pipeline (retrieval + answer-quality + pipeline) runs end-to-end producing a **parallel secondary report set** (`reports/*_LOCAL.md`) with $0 embedding cost (only LLM-judge cost remains). The local-embedder path is documented in METHODOLOGY.md as a first-class secondary alongside the OpenAI primary, NOT a per-tool dispatch (still applied globally to all 7 tools — same embedder per run, same fairness guarantee). **The two leaderboards never mix — each leaderboard uses one embedder for all tools, preserving the fairness contract.**
- **SC-13** — **Given** the v1.4 mxbai validation pass produced an asymmetric directional bias (markcrawl gains +0.043 MRR while all 6 other tools lose between -0.007 and -0.077), **When** METHODOLOGY.md explains the embedder-choice decision, **Then** it surfaces this finding **explicitly and prominently** (not buried), with the rationale: "We considered switching primary embedder to mxbai (aggregate Tau=0.952 → SAFE-TO-SWITCH) and chose not to, because the directional bias favors markcrawl. Switching would look like motivated reasoning even if the leaderboard is technically stable. OpenAI 3-small remains primary; mxbai secondary is provided for the $0-cost scenario." Per-site Tau distribution (median 0.476, range -0.048 to 0.952) is also documented to qualify the "embedder doesn't matter" claim — it doesn't matter at the *aggregate* level, but per-site ordering shifts measurably with embedder choice.

## Flow

```
v1.3 ship (current)
       │
       ▼
Tier 1 (1-2 days, purely additive)
  ├─ page_level_mrr.py helper          (DS-1)
  ├─ URL normalization in retrieval    (DS-2)
  ├─ QUERY_AUDIT.csv emitter            (DS-3)
  ├─ METHODOLOGY: COI + single-trial   (DS-4)
  ├─ Re-run retrieval (no re-crawl)    (DS-5)
  └─ Tier 1 commit + interim reports
       │
       ▼
Tier 2 (2-3 days, methodology overhaul)
  ├─ generate_queries.py (LLM gen+verify) (DS-6)
  ├─ Human-out-of-loop verification       (DS-6 sub)
  ├─ Replace TEST_QUERIES with v14 set    (DS-7)
  ├─ Re-run retrieval + answer_quality    (DS-8)
  ├─ Hit@1/@3/@5/@10 reporting            (DS-9)
  ├─ Anti-gaming section in METHODOLOGY   (DS-10)
  ├─ tools/cost_calculator.py + sensitivity (DS-11)
  ├─ Two-secondary-embedder 3-site sanity (DS-12 — adversarial site selection)
  ├─ Pre-flight MPS batch-size tuning      (DS-13c — optional)
  ├─ Fix retrieval checkpoint key (embedder)(DS-13b — prerequisite)
  ├─ Fully-local-embedder mode (1st-class)  (DS-13a)
  ├─ Reproducibility artifact (make/docker) (DS-13)
  └─ v1.3→v1.4 leaderboard diff release note (DS-14)
       │
       ▼
v1.4 ship (HN-credibility ready)
```

## Implementation Roadmap

This section sequences the DS items from `## Detailed Steps` into smoke-test-gated phases. The phasing is operational guidance for execution; the DS items themselves remain the specifications for what each gate produces. Added 2026-05-10 to lock in the gate ordering and the human-inspection checkpoints (Gate 3a + 3b) that are not visible in the `## Flow` diagram.

### Smoke-test gates

```
Gate 0  prerequisite           DS-13b                       ~30 min, $0
   │
   ▼
Gate 1  Tier 1 build           DS-1, DS-2, DS-3, DS-4       ~1 day, $0
   │
   ▼
Gate 2  Tier 1 end-to-end      DS-5                         ~30 min, ~$0.05
   │
   ▼
Gate 3a single-site DS-6       DS-6 (one site)              ~10 min, ~$0.30
   │       ← user inspection checkpoint
   ▼
Gate 3b full-pool DS-6         DS-6 (all 11 sites)          ~30 min, ~$5
   │       ← user inspection checkpoint
   ▼
Gate 4  v1.4 numbers           DS-7, DS-8, DS-9             ~2-3 hrs, ~$8
   │
   ▼
Gate 5  docs + tooling         DS-10, DS-11, DS-14          ~half day, $0
   │
   ▼
Gate 6  PUBLISH-BOTH + repro   DS-13c, DS-12, DS-13a, DS-13 ~1-2 days, $0-8
   │
   ▼
v1.4 ship
```

### Gate-by-gate

**Gate 0 — Prerequisite checkpoint-key fix (DS-13b).** No subsequent gate is meaningful without this — re-running `benchmark_retrieval.py` with a different `EMBEDDING_MODEL` silently loads the prior embedder's cached vectors and emits an "updated" report byte-identical to the old one. Verified empirically 2026-05-05. Smoke: `tests/test_checkpoint_key.py` — load with mismatched embedder slug returns `None`.

**Gate 1 — Tier 1 additive instrumentation (DS-1, DS-2, DS-3, DS-4).** Purely additive: new helper module, new normalization function, new CSV writer, new METHODOLOGY section + per-report banner. None of these change existing numbers. Each lands with its own unit test (`tests/test_page_level_mrr.py`, `tests/test_url_normalization.py`, `tests/test_audit_csv.py`); DS-4 lands with `python lint_reports.py` clean.

**Gate 2 — First end-to-end smoke (DS-5).** Re-run `benchmark_retrieval.py --run run_v13_merged_20260504_203748` against the existing crawl data with the existing v1.3 query set. Verifies Gate 1 wires together. Chunk-level MRR should match v1.3 within rounding (no methodology change yet — just additive instrumentation). Page-level MRR is the new column. `QUERY_AUDIT.csv` populates with ~104 queries × 7 tools × 5 ≈ 3640 rows.

**Gate 3a — Single-site DS-6 with user inspection.** Run `tools/generate_queries.py` on **one site** (suggest `rust-book` — small, technical, mixes prose with API ref so it stresses both modes). ~$0.30, ~20-30 candidate queries. Output a markdown table to chat: `URL | sampled offset | generated draft | verifier verdict | rationale | url_match pattern`. User reviews to catch plumbing bugs (LLM returning malformed JSON, sampler not random, verifier always returning Y, etc.) before committing to the full-pool spend. **Inspection-vs-curation bright line applies — see Technical Decisions row.**

**Gate 3b — Full-pool DS-6 with user inspection.** Once Gate 3a passes, run for all 11 sites. ~150-200 accepted queries, ~$5. User reviews per-site summary (counts + 5 random accepted + 3 random rejected per site) for site-specific weirdness (e.g. `mdn-css` queries clustering on one property, `stripe-docs` verifier too strict). Same bright line.

**Gate 4 — v1.4 numbers (DS-7, DS-8, DS-9).** Refactor `TEST_QUERIES` to load from `queries/v14_queries.json` (DS-7), re-run retrieval + answer-quality on existing merged dir with the new query set (DS-8), render Hit@1/@3/@5/@10 (DS-9). ~2-3 hrs wall, ~$8.

**Gate 5 — Docs and tooling (DS-10, DS-11, DS-14).** Anti-gaming METHODOLOGY section, cost calculator + sensitivity table, v1.3→v1.4 release notes leading with markcrawl deltas (negative ones first). No new compute spend; manual review only.

**Gate 6 — PUBLISH-BOTH + reproducibility (DS-13c, DS-12, DS-13a, DS-13).** Optional MPS batch-size tune (DS-13c) decides DS-12 scope (3-site adversarial vs 11-site full bge-large). Run mxbai + bge-large secondary (DS-12). Complete the PUBLISH-BOTH secondaries: `ANSWER_QUALITY_LOCAL.md` + `PIPELINE_TIMING_LOCAL.md` + METHODOLOGY section leading with markcrawl's +0.043 asymmetric-bias finding (DS-13a — satisfies SC-13). Add `make benchmark` + `make benchmark-quick` targets (DS-13). Final smoke: `make benchmark-quick` on a single site exits clean.

### Inspection vs. curation: the bright line for Gates 3a / 3b

The whole point of DS-6 (LLM gen + LLM verify) is to remove human authorship of queries — the COI v1.3 was vulnerable to. Human inspection of generated queries before the full DS-8 run does NOT re-introduce COI provided the rule is respected: **fixes happen at the prompt/code level, not at the individual-query level.**

| Feedback type | Verdict | Action |
|---|---|---|
| "The verifier is accepting nonsense" | OK | Fix verification prompt; regenerate ALL queries (all sites) |
| "Sampler isn't random" | OK | Fix sampler code; regenerate ALL queries |
| "LLM only generates factual lookups, no conceptual queries" | OK | Adjust generation prompt; regenerate ALL queries |
| "Site X has 0 accepted queries — broken" | OK | Investigate root cause (no extractable content? prompt mismatched site?); fix + regenerate ALL |
| "These 3 specific queries are unfair, drop them" | NOT OK | Re-introduces COI even if intent benign |
| "Replace this query with this better one I wrote" | NOT OK | Re-introduces human authorship — the exact thing v1.4 removes |

If a regeneration is triggered by Gate 3a or 3b feedback, the cost is paid again (~$0.30 single-site, ~$5 full-pool). The audit trail then captures: "we ran the LLM-only pipeline, inspected for setup bugs, fixed N issues at the prompt level, regenerated everything from scratch, accepted second pass." This reads as more rigorous than a one-shot run, not less.

The motivation is engineering hygiene, not curation: a 20+ hour benchmark + LLM-judge run is too expensive to commit to without a smoke verification of the input pipeline. The cost of the inspection gate is bounded; the cost of discovering the verifier was broken after DS-8 completes is not.

## Detailed Steps

### DS-1: Implement `tools/page_level_mrr.py`
- [ ] **Status**
  - What: Helper module that takes existing per-chunk retrieval results and computes page-level MRR by collapsing multiple chunks per URL into a single rank (the best rank achieved by any chunk from that URL). Imports cleanly into `benchmark_retrieval.py` so the report can render both chunk-level and page-level columns.
  - Actor: Claude Code
  - Input: List of `RetrievalResult` objects (chunk-level), list of queries with `url_match` patterns.
  - Output: `{tool: {site: {"chunk_mrr": float, "page_mrr": float, "chunk_hit_at_k": dict, "page_hit_at_k": dict}}}`
  - Evidence: _pending_
  - Test: _pending_
  - On failure: If page-level MRR helper raises, fall back to chunk-level only with a logged warning. Don't block report regeneration.

### DS-2: Add URL normalization in `benchmark_retrieval.py`
- [ ] **Status**
  - What: Add `_normalize_url_for_matching(url) -> str` that strips locale subdomain prefixes (`he.`, `de.`, `es.`, `fr.`, `ja.`, `zh.`, `ko.`, `pt.`, `ru.`, `ar.`, `it.`, `hi.`, etc. — full ISO-639-1 set), strips query parameters (`?utm_*`, `?lang=`, `?random=`), and lowercases. Apply this before evaluating `url_match` against the page URL. Document the normalization rules inline.
  - Actor: Claude Code
  - Input: Raw URL from `pages.jsonl` (e.g. `https://he.react.dev/learn/managing-state?utm_source=foo`)
  - Output: Normalized URL for matching (e.g. `https://react.dev/learn/managing-state`)
  - Evidence: _pending_
  - Test: _pending_ (unit test verifying ~10 known false-positive URLs from v1.3 no longer count as hits)
  - On failure: If normalization raises (malformed URL), use raw URL with a logged warning. Don't lose the chunk.

### DS-3: Emit `reports/QUERY_AUDIT.csv` from retrieval
- [ ] **Status**
  - What: After `benchmark_retrieval.py` finishes scoring, write a CSV with one row per (query × tool × rank-1-to-5) containing: `query_id, query_text, site, tool, rank, url, cosine_score, is_hit, url_match_pattern, normalized_url`. This becomes the audit artifact for any reviewer questioning a specific number.
  - Actor: Claude Code
  - Input: All retrieval results across all tools and queries.
  - Output: `reports/QUERY_AUDIT.csv` (~104 queries × 7 tools × 5 ranks ≈ 3,640 rows for v1.3-sized query set).
  - Evidence: _pending_
  - Test: _pending_ (CSV opens cleanly in Excel/Google Sheets, has expected column headers, row count matches `queries × tools × 5`).
  - On failure: If CSV write fails, log the failure but do not abort report generation — the CSV is an audit artifact, not load-bearing for the headline numbers.

### DS-4: METHODOLOGY.md — author disclosure + single-trial caveat
- [ ] **Status**
  - What: Add new section "Author and conflict-of-interest disclosure" near the top of METHODOLOGY.md naming who wrote queries (was: paulsave for v1.3; now: gpt-4o-mini-generated + gpt-4o-mini-verified for v1.4), runners, methodology, and the markcrawl tool itself. Add prominent banner at the top of every report file: "**Single-trial measurement.** Network jitter, WAF state, and server load add ±N% noise to per-site numbers. Confidence intervals reflect query-set sampling only, not run-to-run variance. Multi-trial validation is v1.5 work — see METHODOLOGY.md."
  - Actor: Claude Code
  - Input: Current METHODOLOGY.md, list of all reports/*.md files.
  - Output: Updated METHODOLOGY.md + banner on each report.
  - Evidence: _pending_
  - Test: _pending_ (lint_reports.py passes; banner present on all 6 v1.3 reports).
  - On failure: Manual re-edit if linter rejects the banner format.

### DS-5: Re-run retrieval for Tier 1 interim numbers (no re-crawl, no re-embed)
- [ ] **Status**
  - What: Re-run `benchmark_retrieval.py` with the new normalization + page-level MRR + audit CSV emission against the existing merged dir + existing TEST_QUERIES. This produces interim Tier 1 numbers (chunk-level + page-level + locale-stripped) on the v1.3 query set so we can see the page-level MRR delta in isolation BEFORE swapping in the new v1.4 query set.
  - Actor: Claude Code
  - Input: `runs/run_v13_merged_20260504_203748/` (existing crawl data), `embed_cache/` (existing embeddings).
  - Output: Updated `reports/RETRIEVAL_COMPARISON.md` with both chunk-level and page-level MRR.
  - Evidence: _pending_
  - Test: _pending_
  - On failure: If page-level MRR helper has a bug, ship Tier 1 with chunk-level only + logged warning, fix in follow-up.

### DS-6: `tools/generate_queries.py` — LLM gen + LLM verify, no human in loop
- [ ] **Status**
  - What: Standalone script that for each site (a) samples 30-50 random URLs from `crawl4ai-raw`'s pages.jsonl (highest-coverage tool — gives the broadest topic surface), (b) for each URL, calls gpt-4o-mini with the page content asking it to draft 1-2 questions answerable from the content, (c) for each draft query, calls a SEPARATE gpt-4o-mini invocation (fresh context, no prior turns) with the URL's content + the query asking "is this query answerable from this content? Y/N + 1-line rationale", (d) accepts queries judged Y, rejects N, (e) writes accepted queries to `queries/v14_queries.json`. Critical: NO human reviews the queries before they go into the benchmark — that re-introduces the COI we're trying to remove.
  - Actor: Claude Code (script implementation), gpt-4o-mini (query generation + verification)
  - Input: `runs/run_v13_merged_20260504_203748/crawl4ai-raw/<site>/pages.jsonl` for each site, OPENAI_API_KEY.
  - Output: `queries/v14_queries.json` (per-site lists of accepted queries), `queries/v14_rejected.json` (rejected drafts with rationale, kept for transparency).
  - Evidence: _pending_
  - Test: _pending_ (script produces ≥150 accepted queries across 11 sites; rejection-rate logged and reasonable; cost ≤ $5).
  - On failure: If verification rejects too many queries (e.g. <100 accepted total), tune the verification prompt OR sample more URLs per site. If the API call rate-limits, retry with exponential backoff.

### DS-7: Replace `TEST_QUERIES` in benchmark_retrieval.py with v1.4 set
- [ ] **Status**
  - What: Load `queries/v14_queries.json` at runtime and use it as the source of truth for `TEST_QUERIES`. Keep the v1.3 hand-written set in `queries/v13_queries.json` for diff/reproducibility.
  - Actor: Claude Code
  - Input: `queries/v14_queries.json`
  - Output: `benchmark_retrieval.py` modified to load from JSON; v1.3 hand-written queries archived to `queries/v13_queries.json`.
  - Evidence: _pending_
  - Test: _pending_ (unit test: TEST_QUERIES loads ≥150 queries across 11 sites without crash).
  - On failure: If JSON loading fails, fall back to v1.3 hand-written queries with a logged warning.

### DS-8: Re-run retrieval + answer-quality with v1.4 query set
- [ ] **Status**
  - What: Run `benchmark_retrieval.py` then `benchmark_answer_quality.py` on the existing merged dir but with the new TEST_QUERIES. Some chunks already cached (good); new query embeddings are uncached (cost ≈ $0.10). Answer-quality will be a full re-run (LLM cost ≈ $5-10 for 200 queries × 7 tools).
  - Actor: Claude Code
  - Input: New TEST_QUERIES, existing merged crawl data + embed cache.
  - Output: `reports/RETRIEVAL_COMPARISON.md` and `reports/ANSWER_QUALITY.md` with v1.4 numbers.
  - Evidence: _pending_
  - Test: _pending_
  - On failure: If rate-limited mid-run, the existing checkpoint mechanism resumes. If a tool crashes, log + continue with remaining tools.

### DS-9: Report Hit@1, Hit@3, Hit@5, Hit@10 alongside MRR
- [ ] **Status**
  - What: Update `benchmark_retrieval.py` report generation to include all four Hit@K columns in both the per-tool summary table AND per-site tables. Add a methodology note: "Hit@1 is least sensitive to chunk density (each chunk competes for one slot); Hit@10 is most sensitive (more chunks = more chances)."
  - Actor: Claude Code
  - Input: Existing retrieval results structure (already has hit_at_k for K=1,3,5,10,20 — just need to render).
  - Output: Updated tables in RETRIEVAL_COMPARISON.md.
  - Evidence: _pending_
  - Test: _pending_ (lint_reports.py passes; tables have all 4 K columns).
  - On failure: Cosmetic — fix in next commit.

### DS-10: METHODOLOGY.md — explicit "Anti-gaming" section
- [ ] **Status**
  - What: Add new section enumerating 6 known gaming attacks (chunk-density inflation, locale duplication, URL-text injection, hub-page inflation, embedder favoritism, author conflict-of-interest) with the defense applied (or limitation noted) for each. Format as a table for skim-ability.
  - Actor: Claude Code
  - Input: Anti-gaming analysis from v1.3 cycle conversations.
  - Output: New "Anti-gaming" section in METHODOLOGY.md.
  - Evidence: _pending_
  - Test: _pending_ (lint_reports.py passes).
  - On failure: Cosmetic — fix in next commit.

### DS-11: `tools/cost_calculator.py` + sensitivity analysis
- [ ] **Status**
  - What: Standalone Python script with adjustable inputs (queries/day, embedding model + price, LLM model + input/output prices, dedup ratio, pages crawled per year). Outputs per-tool annual cost. Also runs a sensitivity sweep: for each input, vary by ±50% and report how the ranking changes. Embed the result table in COST_AT_SCALE.md.
  - Actor: Claude Code
  - Input: Per-tool chunk counts + token counts from `runs/run_v13_merged_20260504_203748/pipeline_timings.json`, current pricing constants.
  - Output: `tools/cost_calculator.py` + sensitivity table appended to COST_AT_SCALE.md.
  - Evidence: _pending_
  - Test: _pending_ (script runs with default args + at least 3 sensitivity scenarios; outputs match COST_AT_SCALE.md numbers when defaults are used).
  - On failure: Ship calculator without sensitivity table if the sweep is buggy; fix sweep in follow-up.

### DS-12: Two-secondary-embedder sanity check on 3 adversarial sites
- [ ] **Status**
  - What: Run TWO secondary embedders (mxbai + bge-large) on 3 sites picked for adversarial coverage of the leaderboard outcome: **rust-book** (markcrawl wins, fast static site), **react-dev** (markcrawl loses badly to scrapy+md, tests the "embedder doesn't favor markcrawl" claim), **postgres-docs** (tight 4-tool cluster, tests stability in the squeezed range). Choosing all-markcrawl-wins sites would only verify the easy direction; including a markcrawl-loses site is the credibility-buying move. Commands:
    1. `EMBEDDING_MODEL=mixedbread-ai/mxbai-embed-large-v1 python benchmark_retrieval.py --sites rust-book,react-dev,postgres-docs --run run_v13_merged_20260504_203748 --output reports/RETRIEVAL_SANITY_MXBAI.md`
    2. `EMBEDDING_MODEL=BAAI/bge-large-en-v1.5 python benchmark_retrieval.py --sites rust-book,react-dev,postgres-docs --run run_v13_merged_20260504_203748 --output reports/RETRIEVAL_SANITY_BGE.md`
  - Run `tools/compare_embedders.py` against both pairings. Document deltas in METHODOLOGY.md "Embedder sensitivity" subsection. If both secondaries preserve top-3 ordering on all 3 sites — including react-dev where markcrawl loses — the claim "embedder choice doesn't determine the leaderboard" is much stronger than testing 3 sites markcrawl wins.
  - Actor: Claude Code
  - Input: Existing merged dir, mxbai model bundled with markcrawl install, bge-large auto-downloaded by sentence-transformers (~1.3GB).
  - Output: `reports/RETRIEVAL_SANITY_MXBAI.md`, `reports/RETRIEVAL_SANITY_BGE.md`, paragraph in METHODOLOGY.md citing both.
  - Evidence: _pending_
  - Test: _pending_
  - On failure: If mxbai or bge-large produces dramatically different ranking, document honestly — do NOT suppress the finding. The honest disclosure is itself a credibility signal.

  **Empirical note (validation pass 2026-05-05/06):** the full-set mxbai validation (DS-13a-prep) revealed that retrieval_checkpoints don't include the embedder name in the cache key (DS-13b), causing a silent stale-cache hit. This must be fixed BEFORE running DS-12 or DS-13a, otherwise the secondary-embedder reports come out byte-identical to primary. mxbai-large @ batch_size=32 on M-series MPS sustains ~17 chunks/sec; full 324K-chunk pass takes ~12h wall-time. Three-site sanity check at ~5-6K chunks per tool × 3 sites × 7 tools ≈ ~110K chunks total ≈ 1.5-2h per embedder at current rate. **Pre-flight optimization (DS-13c) may cut that significantly.**

### DS-13c: Pre-flight MPS batch-size optimization (optional, 10-30 min)
- [ ] **Status**
  - What: Before running DS-12 or DS-13a, measure mxbai-large throughput at `batch_size=32` (current default) vs `batch_size=64` vs `batch_size=128` on a fixed 1000-chunk sample. mxbai-large is GPU-underutilized at batch_size=32 on Apple Silicon (typical workload achieves 50-150 chunks/sec for this model class; we measured 17). If batch_size=128 gives 2-3× speedup, bge-large becomes affordable as a FULL 11-site pass (~5-6h) rather than 3-site sanity-only — fully closing the "we tested three embedders" claim with no caveats. If batch_size=128 hits MPS memory pressure or doesn't help, fall back to the 3-site sanity-check plan in DS-12.
  - Actor: Claude Code
  - Input: Existing merged dir; sentence-transformers SentenceTransformer constructor + `encode(batch_size=N)` parameter at `benchmark_retrieval.py:1096`.
  - Output: 3-line decision: "batch_size=N gives X chunks/sec → DS-12 sanity-check OR DS-13a-bge full pass." Append result to METHODOLOGY.md "Embedder sensitivity" as a methodological footnote ("we tuned batch size before validation; final batch_size=N achieves X chunks/sec on M-series MPS").
  - Evidence: _pending_
  - Test: _pending_ (timing measurement script + decision-log line in METHODOLOGY).
  - On failure: If batch_size>32 OOMs or crashes, default to batch_size=32 + 3-site sanity check (current DS-12 plan).

### DS-13b: Fix retrieval_checkpoints key to include embedder name (PREREQUISITE for DS-13a)
- [ ] **Status**
  - What: Currently retrieval_checkpoints filename pattern is `<run>__<tool>__<site>__~<chunk-size>tok.json` — does NOT include the embedder name. This causes a silent stale-cache hit when re-running with a different `EMBEDDING_MODEL` env var: the script loads the old retrieval results computed against the previous embedder's vectors and writes a "new" report with the old numbers. We hit this empirically on 2026-05-05 during the v1.4 mxbai validation pass — the first run produced a `_LOCAL.md` report byte-identical to the OpenAI primary except for the embedder-name string, because all 72 (tool, site) checkpoints loaded from the OpenAI run. Fix: include `EMBEDDING_MODEL` (or a short hash of it) in the checkpoint filename. New pattern: `<run>__<embedder-slug>__<tool>__<site>__~<chunk-size>tok.json`. Existing checkpoints are not migrated — they get treated as a different embedder and naturally bypassed.
  - Actor: Claude Code
  - Input: `benchmark_retrieval.py` checkpoint save/load logic.
  - Output: Modified checkpoint filename pattern; existing OpenAI checkpoints still load (their slug remains `text-embedding-3-small`); mxbai runs write to a separate slugged file.
  - Evidence: _pending_
  - Test: _pending_ (unit test: load_checkpoint("openai-key", ...) returns None when only mxbai-key checkpoint exists; integration test: re-run validation v2 produces non-identical _LOCAL.md report).
  - On failure: If filename change breaks compatibility with on-disk checkpoints, document the migration step in METHODOLOGY (one-time `rm retrieval_checkpoints/*.json` after upgrade — or migration helper that prepends old slug).

### DS-13a: Fully-local-embedder mode (PUBLISH-BOTH secondary, never primary in v1.4)
- [ ] **Status**
  - What: Run the full pipeline once with `EMBEDDING_MODEL=mixedbread-ai/mxbai-embed-large-v1` to produce a complete **parallel secondary report set** (`reports/*_LOCAL.md`) covering retrieval, answer-quality, and pipeline-timing. **The two leaderboards never mix** — each is internally consistent (one embedder, all 7 tools). Document in METHODOLOGY.md "Embedder choice and the PUBLISH-BOTH decision":
    1. Lead with the asymmetric-bias finding (markcrawl +0.043 MRR, all 6 others -0.007 to -0.077; aggregate Tau=+0.952; per-site median Tau=+0.476).
    2. State the rationale explicitly: "We considered switching primary to mxbai because aggregate Tau passes the SAFE-TO-SWITCH threshold (≥0.85). We chose not to. The directional bias favors markcrawl, and switching would look like motivated reasoning even if the math is stable. OpenAI 3-small remains primary."
    3. Frame mxbai as a peer-published secondary: "$0-embedding-cost variant; same fairness guarantee within the secondary leaderboard; useful for users who want zero-API workflow."
    4. Surface the per-site Tau range honestly: "Aggregate stability (Tau=0.952) hides per-site variance — 7 of 11 sites fall in PUBLISH-BOTH (0.6-0.85) or KEEP-OPENAI (<0.6) per-site bands. This is documented but does not change the headline."
  Update `tools/cost_calculator.py` with a `--local-embedder` flag that zeros the embedding-cost line.
  - Actor: Claude Code
  - Input: mxbai model already bundled with markcrawl 0.10.x install (~640MB on disk plus ~500MB sentence-transformers + torch); existing merged crawl dir; gpt-4o-mini for answer-quality (still uses LLM, separate from embedding choice).
  - Output: `reports/RETRIEVAL_COMPARISON_LOCAL.md` (already produced 2026-05-06 from validation pass — Tau analysis complete; report stays as the secondary), `reports/ANSWER_QUALITY_LOCAL.md`, `reports/PIPELINE_TIMING_LOCAL.md` (yet to produce); new "Embedder choice and the PUBLISH-BOTH decision" subsection in METHODOLOGY.md leading with asymmetric-bias finding; cost calculator `--local-embedder` flag.
  - Evidence: _pending_
  - Test: _pending_ (full pipeline runs to completion under `EMBEDDING_MODEL=mixedbread-ai/mxbai-embed-large-v1`; resulting `_LOCAL` reports have non-empty per-tool tables; embedding cost in cost_calculator output reads $0 for the LOCAL variant; METHODOLOGY.md leads asymmetric-bias finding with markcrawl's +0.043 NUMBER FIRST, not buried).
  - On failure: If mxbai install on the host venv is broken, document the failure mode and ship without the local secondary reports (don't block v1.4 on it). The _LOCAL reports are additive; primary OpenAI reports are the headline.

  **Validation result already in hand (2026-05-06):**
  ```
  Aggregate Kendall's Tau (7-tool overall MRR):  +0.952  → SAFE-TO-SWITCH (math)
  Per-site Tau median:                            +0.476
  Per-site Tau range:                             -0.048 (propublica) to +0.952 (react-dev)
  Per-tool MRR delta (mxbai − openai):
    markcrawl       +0.043  ↑   ← only tool that gains
    crawl4ai-raw    -0.007  ↓
    crawl4ai        -0.009  ↓
    crawlee         -0.020  ↓
    playwright      -0.037  ↓
    colly+md        -0.047  ↓
    scrapy+md       -0.077  ↓
  Decision: PUBLISH-BOTH, OpenAI primary (asymmetric bias unrecoverable for credibility).
  ```

### DS-13: Reproducibility artifact — `make benchmark` / `docker compose run benchmark`
- [ ] **Status**
  - What: Add Makefile target `benchmark` that runs the full pipeline end-to-end: `preflight.py --smoke-test` → `run_benchmarks.sh` → `benchmark_quality.py` → `benchmark_retrieval.py` → `benchmark_answer_quality.py` → `benchmark_pipeline.py` → `generate_readme.py`. Also produce a Dockerfile (existing or new) that pins all crawler versions and Python deps. Document in README "to reproduce v1.4 numbers: `docker compose run benchmark`".
  - Actor: Claude Code
  - Input: Existing `run_benchmarks.sh`, individual benchmark scripts, Dockerfile (verify presence).
  - Output: Makefile target + verified Dockerfile + reproduction-instructions section in README.
  - Evidence: _pending_
  - Test: _pending_ (running `make benchmark` end-to-end on a fresh checkout produces non-empty reports — does NOT need to match exact numbers due to network noise; just needs to complete without crashing).
  - On failure: If Docker has issues, ship Makefile-only path + document Docker as TODO.

### DS-14: v1.3→v1.4 leaderboard diff release note
- [ ] **Status**
  - What: Write `docs/V14_RELEASE_NOTES.md` (or commit message body for the v1.4 commit). LEAD with a table showing every tool's per-dimension delta v1.3 → v1.4 (chunk-MRR vs page-MRR-Hit@1, content signal, answer quality, cost). If markcrawl drops on any dimension, that delta goes FIRST in the table. Explicitly call out the methodology fix that caused each shift. End with "leaderboard fixed itself by these methodology improvements" framing.
  - Actor: Claude Code (drafts), human (reviews framing — but not numbers — before publishing)
  - Input: v1.3 final reports (current main), v1.4 final reports (post-DS-1-through-13).
  - Output: `docs/V14_RELEASE_NOTES.md` ready to publish + commit message reusing same content.
  - Evidence: _pending_
  - Test: _pending_ (manual review: the table genuinely leads with markcrawl's deltas, including any negative ones; framing is not defensive).
  - On failure: Iterate framing until it passes the "would HN respect this?" sniff test.

## Edge Cases

- **What happens if mxbai sanity check shifts the leaderboard?** Document the shift honestly in METHODOLOGY.md "Embedder sensitivity" subsection. Do NOT change the headline numbers; primary embedder remains text-embedding-3-small. If shift is large (>10% MRR delta), elevate to "v1.5 must include multi-embedder validation."
- **What if LLM verification rejects too many queries (e.g. <100 accepted across 11 sites)?** Tune the verification prompt to be less strict (e.g. accept "partially answerable") OR sample more URLs per site (50 → 100). If still <100, document the limitation and proceed with what we have.
- **What if URL normalization breaks a legitimate hit (e.g. a site genuinely uses subdomains for separate content, not locales)?** Maintain an opt-out list per site in `sites/pool_v1.yaml` ("disable_locale_normalization: true"). Default ON; opt out per-site only when justified.
- **What if `make benchmark` end-to-end takes more than 24 hours?** Document expected wall-time prominently. Provide `make benchmark-quick` (1 site, 1 iteration) as the smoke-test path.
- **What if a tool's runner has been updated upstream and the pinned version diverges from current behavior?** The Dockerfile pins versions. The host venv is documented in METHODOLOGY.md as best-effort for non-Docker users.
- **What if the new query set contains a query that's actually unanswerable from any tool's crawl?** Acceptable — measures coverage gaps. Would surface as "all 7 tools = miss at @10" in QUERY_AUDIT.csv. Could be a useful signal for v1.5 site-pool refinement.
- **What if an HN reviewer asks for the FULL chunk database to verify embeddings?** Out of scope for v1.4 — embed cache is 19+ GB. Document the embedder name + version + chunk text → embedding is reproducible from source.

## Artifacts / Output

```
specs/
└── v14-methodology-hardening.md     (this spec)

queries/
├── v13_queries.json                 (archived v1.3 hand-written)
├── v14_queries.json                 (LLM-generated, LLM-verified)
└── v14_rejected.json                (rejected drafts + rationale)

tools/
├── generate_queries.py              (DS-6)
├── cost_calculator.py               (DS-11)
└── page_level_mrr.py                (DS-1)

reports/
├── QUERY_AUDIT.csv                  (DS-3 — new)
├── RETRIEVAL_SANITY_MXBAI.md        (DS-12 — new)
├── METHODOLOGY.md                   (DS-4, DS-10, DS-12 sections — modified)
├── RETRIEVAL_COMPARISON.md          (DS-1, DS-9 — modified)
├── ANSWER_QUALITY.md                (DS-8 — modified)
├── COST_AT_SCALE.md                 (DS-11 — modified)
├── QUALITY_COMPARISON.md            (banner only — modified)
├── SPEED_COMPARISON.md              (banner only — modified)
└── PIPELINE_TIMING.md               (banner only — modified)

docs/
└── V14_RELEASE_NOTES.md             (DS-14 — new)

(repo root)
├── Makefile                         (DS-13 — new target)
└── README.md                        (DS-13 — modified, add reproduction section)
```

| # | Artifact | Description | Consumed by |
|---|----------|-------------|-------------|
| 1 | `queries/v14_queries.json` | LLM-gen + LLM-verified query set, ~150-200 queries | `benchmark_retrieval.py`, `benchmark_answer_quality.py` |
| 2 | `reports/QUERY_AUDIT.csv` | Every (query × tool × rank-1-to-5) hit with URLs + scores | Audit by reviewers; reproducibility check |
| 3 | `tools/page_level_mrr.py` | Helper computing page-level MRR by collapsing chunks per URL | `benchmark_retrieval.py` |
| 4 | `tools/generate_queries.py` | LLM-generated, LLM-verified query authoring pipeline | One-shot per benchmark cycle (run for v1.4, archive) |
| 5 | `tools/cost_calculator.py` | Cost calculator with sensitivity analysis | `COST_AT_SCALE.md`; reviewer audit |
| 6 | `reports/RETRIEVAL_SANITY_MXBAI.md` | Secondary-embedder sanity check on 2 sites | `METHODOLOGY.md` "Embedder sensitivity" claim |
| 7 | `docs/V14_RELEASE_NOTES.md` | v1.3→v1.4 leaderboard diff with markcrawl-deltas leading | Public ship; HN/Twitter post |

## Data / State Changes

| Entity / Source | Operation | Fields affected | Notes |
|----------------|-----------|-----------------|-------|
| `benchmark_retrieval.py:122` `TEST_QUERIES` dict | Replace | site key → list of {query, url_match, page_match, category, description} | Hand-written → JSON-loaded from `queries/v14_queries.json` |
| `embed_cache/` | Append (cache hits where chunks unchanged) | New entries for new query embeddings | ~$0.10 OpenAI cost for ~200 new query embeddings |
| `retrieval_checkpoints/` | Replace | Per (tool, site) | New checkpoints for v1.4 query set |
| `answer_quality_checkpoints/` | Replace | Per (tool, site) | New LLM-generated answers for v1.4 queries |
| `pyproject.toml` | No change | — | (markcrawl pin already at >=0.10.5) |
| `sites/pool_v1.yaml` | Optional | Add `disable_locale_normalization: bool` per-site | Default off; opt-in only |

## Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Page-level MRR formula | "Best rank achieved by any chunk from URL X" | Conservative — gives the URL the benefit of its best-performing chunk. Alternatives (e.g. average chunk rank) would penalize URLs with both great and poor chunks; benchmark cares whether the user finds the page at all. |
| URL normalization scope | Locale subdomain prefixes (ISO-639-1 set) + `?utm_*` / `?lang=` / `?random=` query params | Covers the actual false-positive observed in v1.3 (`he.react.dev`); doesn't go so broad that legitimate subdomains (e.g. `docs.stripe.com` vs `support.stripe.com`) collapse. |
| Query verification model | gpt-4o-mini, separate invocation, no prior turns | Cheap (~$5 total), removes human COI from the loop. NOT using a different model from generation (gpt-4o-mini for both) because we want to measure "is this query answerable" not "do two different LLMs agree" — the simpler design is more defensible. |
| Source for query URL sampling | crawl4ai-raw's pages.jsonl (highest coverage) | Provides the broadest topic surface across sites. Using the SAME tool's output as the query source for ALL tools' benchmarking is fine (it's not the tool we're judging on the queries). |
| Whether to retry queries rejected by verification | No | Rejected queries logged in `queries/v14_rejected.json` for transparency but not retried. Retry would re-introduce verifier-bias (we'd keep tweaking until enough pass). |
| Tier 1 vs Tier 2 ship boundary | Tier 1 ships as interim commit; Tier 2 ships as the v1.4 release | Tier 1 is purely additive (page-level alongside chunk-level) — won't break anything if Tier 2 is delayed. Tier 2 changes the query set, which is the headline methodology change. |
| Cost calculator format | Python script + sensitivity table in markdown | Spreadsheet would require external hosting; Python script lives in the repo, runs anywhere with stdlib only. |
| Reproducibility primary path | Makefile target | Docker is secondary because Docker setup adds friction for users who already have the venv. Docker required for "exact reproducibility" claim; Makefile sufficient for "run it yourself". |
| Where v1.3 query set lives post-migration | `queries/v13_queries.json` | Preserved for diff/reproducibility. The v1.3 commit history also has it inline in `benchmark_retrieval.py` — both forms accessible. |
| Retrieval checkpoint key | Include embedder slug in filename (DS-13b) | Without this, swapping `EMBEDDING_MODEL` produces a stale-cache silent failure (verified empirically 2026-05-05 — `_LOCAL.md` report came out byte-identical to OpenAI primary because all 72 cached checkpoints loaded). Embedder-keyed filenames are the minimum viable fix; alternatives (separate cache dirs per embedder) considered but rejected as more disruptive. |
| Local embedder choice | `mixedbread-ai/mxbai-embed-large-v1` | Bundled with markcrawl 0.10.x install (no extra setup for users who already have markcrawl). Top-tier MTEB scores for its size. Detection: model name contains `/` → routed to `_embed_sentence_transformer`. |
| Local embedder dispatch policy | Global (env var swaps for ALL tools simultaneously), not per-tool | Per-tool dispatch was explicitly ruled out earlier in the v1.3 cycle (memory: `feedback_global_embedder_only.md`). The fairness guarantee — "every tool gets the same embedder" — is preserved. The local-embedder mode is a methodology variant, not a per-tool advantage for markcrawl. |
| Embedder leaderboard structure (v1.4) | PUBLISH-BOTH — OpenAI primary + mxbai secondary, never mixed | Validation Tau=+0.952 aggregate would technically permit switching, BUT directional bias is asymmetric (markcrawl gains +0.043 MRR, every other tool loses). Switching primary would look like motivated reasoning even if the math passes. PUBLISH-BOTH preserves v1.3 comparability AND surfaces the $0-cost story AND blocks the obvious credibility attack ("you switched embedders to favor your tool"). Mixing embedders within a single leaderboard would destroy the fairness contract — explicitly disallowed. |
| Asymmetric-bias disclosure | Lead with it in METHODOLOGY, not bury it | The instinct is to hide "markcrawl gains more from mxbai than competitors" because it sounds suspicious. Surfacing it explicitly with the rationale ("we considered switching and chose not to") is the credibility-buying move. Without it, hostile reviewers compute the delta themselves and accuse us of burying it; with it, the disclosure itself is evidence we thought hard about confounds. |
| Setup-verification gates (3a / 3b) | One-site smoke + full-pool review with user inspection before DS-8 commits to the full retrieval + answer-quality run | Catches plumbing bugs (malformed LLM output, sampler not random, verifier saturation, site-specific failures) before paying for a 20+ hour benchmark + LLM-judge run. Does NOT re-introduce COI provided fixes happen at the prompt/code level only — NEVER at the individual-query level. See "Inspection vs. curation" subsection in Implementation Roadmap for the explicit allow/deny list. |

## Cost / Performance

| Operation | Provider | Paid via | Estimated cost |
|-----------|----------|----------|---------------|
| Tier 1 retrieval re-run (v1.3 queries, normalized URLs, page-level MRR) | OpenAI text-embedding-3-small | API credits | ~$0.05 (mostly cache hits) |
| DS-6 query generation (~30 URLs × 11 sites × 1.5 queries) | OpenAI gpt-4o-mini | API credits | ~$2.00 |
| DS-6 query verification (~500 candidates, separate invocation) | OpenAI gpt-4o-mini | API credits | ~$3.00 |
| DS-8 retrieval re-run (v1.4 queries) | OpenAI text-embedding-3-small | API credits | ~$0.10 (new query embeddings only) |
| DS-8 answer-quality re-run (200 queries × 7 tools × 2 LLM calls each) | OpenAI gpt-4o-mini | API credits | ~$8.00 |
| DS-12 mxbai sanity check on 2 sites | Local sentence-transformers | CPU only | $0 |
| DS-13a fully-local-embedder full-pipeline run (secondary _LOCAL reports) | Local sentence-transformers + OpenAI gpt-4o-mini for LLM-judge only | API credits (LLM only) | ~$8.00 (embedding $0) |
| **Total estimated v1.4 cost (primary OpenAI path only)** | — | API credits | **~$13.50** |
| **Total estimated v1.4 cost (primary + DS-13a local-embedder secondary)** | — | API credits | **~$21.50** |
| **Wall time (single-trial constraint)** | — | — | ~2-3 hours retrieval + ~1-2 hours answer-quality + dev time (~2 days) |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Page-level MRR shows markcrawl performs WORSE than chunk-level | Medium | Low | This IS the credibility-buying outcome; lead the release notes with it (DS-14). |
| LLM-generated queries are too easy or too varied | Medium | Medium | Verification step rejects unanswerable queries. If generated queries cluster too narrow, expand sampling URLs from 30 → 50 per site. |
| URL normalization breaks legitimate hits | Low | Low | Opt-out per site via pool_v1.yaml. Audit `QUERY_AUDIT.csv` for unexpected drops. |
| Reproducibility artifact requires hours of wall-time | High | Low | Document expected wall-time prominently. Provide `make benchmark-quick` for smoke verification. |
| Mxbai sanity check shows leaderboard is embedder-dependent | Low | High (credibility) | Honest disclosure. If shift is large, elevate to "v1.5 must run multi-embedder" rather than hide. |
| DS-13a local-embedder full pipeline takes hours on CPU (no GPU on dev machine) | Medium | Low | Document the wall-time; mxbai-large is ~335M params and CPU-bottlenecked at ~50 chunks/sec. Estimated wall-time ~30-90 minutes for the full chunk set. Acceptable for an opt-in secondary path. |
| OpenAI rate-limit during DS-8 re-runs | Medium | Low | Existing checkpoint mechanism resumes. Tighten retry backoff if needed. |
| New v1.4 query set takes 4× longer to write/test than estimated | Medium | Medium | Tier 1 ships independently — interim commit produces page-level MRR + audit CSV even if Tier 2 slips. |
| Author of this spec (Claude) is also the author of v1.3 methodology | Inherent | Inherent | Acknowledged in DS-4 disclosure. The COI-removal step (DS-6) doesn't remove COI of the spec itself — only of the queries. Spec review by user is the human-in-the-loop check. |

## Evidence

| ID | Claim | Files | Build | Test Suite | Test File(s) | Result |
|----|-------|-------|-------|------------|--------------|--------|
| V-1 | SC-1 (page-level MRR alongside chunk-level) | `tools/page_level_mrr.py`, `benchmark_retrieval.py` (rendering) | `python -m pytest tests/test_page_level_mrr.py` | `test:tier1` | `tests/test_page_level_mrr.py` | _pending_ |
| V-2 | SC-2 (URL normalization removes locale false positives) | `benchmark_retrieval.py:_normalize_url_for_matching` | `python -m pytest tests/test_url_normalization.py` | `test:tier1` | `tests/test_url_normalization.py` | _pending_ |
| V-3 | SC-3 (QUERY_AUDIT.csv emitted with all required columns) | `benchmark_retrieval.py` (write_audit_csv) | `python benchmark_retrieval.py --run <run> && head -3 reports/QUERY_AUDIT.csv` | `test:tier1` | `tests/test_audit_csv.py` | _pending_ |
| V-4 | SC-4 (METHODOLOGY has author disclosure + single-trial banner) | `reports/METHODOLOGY.md`, all `reports/*.md` | `python lint_reports.py` | N/A (linter) | `lint_reports.py` | _pending_ |
| V-5 | SC-5 (LLM-only query verification) | `tools/generate_queries.py`, `queries/v14_queries.json`, `queries/v14_rejected.json` | `python tools/generate_queries.py --dry-run` | `test:tier2` | `tests/test_generate_queries.py` | _pending_ |
| V-6 | SC-6 (Hit@1, @3, @5, @10 in report) | `benchmark_retrieval.py` (report rendering) | `python lint_reports.py` | N/A (linter + grep) | `tests/test_report_format.py` | _pending_ |
| V-7 | SC-7 (Anti-gaming section in METHODOLOGY) | `reports/METHODOLOGY.md` | `python lint_reports.py` | N/A | grep | _pending_ |
| V-8 | SC-8 (`make benchmark` reproducibility) | `Makefile`, `Dockerfile`, `README.md` | `make benchmark-quick` | `test:integration` | end-to-end smoke | _pending_ |
| V-9 | SC-9 (V14_RELEASE_NOTES.md leads with markcrawl deltas) | `docs/V14_RELEASE_NOTES.md` | manual review | N/A | N/A — content review | _pending_ |
| V-10 | SC-10 (cost calculator + sensitivity) | `tools/cost_calculator.py`, `reports/COST_AT_SCALE.md` (sensitivity table) | `python tools/cost_calculator.py --defaults && python tools/cost_calculator.py --sensitivity` | `test:tier2` | `tests/test_cost_calculator.py` | _pending_ |
| V-11 | SC-11 (mxbai sanity check claim) | `reports/RETRIEVAL_SANITY_MXBAI.md`, `reports/METHODOLOGY.md` (Embedder sensitivity subsection) | `EMBEDDING_MODEL=mixedbread-ai/mxbai-embed-large-v1 python benchmark_retrieval.py --sites rust-book,huggingface-transformers --output reports/RETRIEVAL_SANITY_MXBAI.md` | N/A | manual diff vs primary | _pending_ |
| V-12a | SC-12 (fully-local-embedder mode supported across all phases, PUBLISH-BOTH never-mixed) | `benchmark_retrieval.py:_embed_sentence_transformer`, `reports/RETRIEVAL_COMPARISON_LOCAL.md`, `reports/ANSWER_QUALITY_LOCAL.md`, `reports/PIPELINE_TIMING_LOCAL.md`, `reports/METHODOLOGY.md` (Embedder choice subsection), `tools/cost_calculator.py --local-embedder` | `EMBEDDING_MODEL=mixedbread-ai/mxbai-embed-large-v1 make benchmark` end-to-end | N/A | manual review of _LOCAL reports + cost calculator output + verification that primary and secondary are never mixed in any leaderboard table | _pending_ |
| V-13a | SC-13 (asymmetric-bias finding leads METHODOLOGY, not buried) | `reports/METHODOLOGY.md` "Embedder choice and the PUBLISH-BOTH decision" subsection | `python lint_reports.py` + manual review (`grep -A 5 "asymmetric"` finds the markcrawl-favorable delta in the LEADING paragraph, not later) | N/A | content review | _pending_ |
| V-12b | DS-13b (retrieval checkpoint key includes embedder) | `benchmark_retrieval.py` (checkpoint save/load filename pattern) | unit test in `tests/test_checkpoint_key.py` (load returns None for mismatched embedder) | `test:tier2` | `tests/test_checkpoint_key.py` | _pending_ |
| V-12 | DS-6 (LLM verification has no human in acceptance loop) | `tools/generate_queries.py` source code review | manual code audit | N/A | code review | _pending_ |
| V-13 | DS-14 (release notes reviewed) | `docs/V14_RELEASE_NOTES.md`, public-post draft | manual review | N/A | content review | _pending_ |

**Rules:**
- V-1 through V-11 map 1:1 to SC-1 through SC-11.
- V-12 and V-13 cover process claims (no-human-in-loop, release-note framing) that aren't testable via code but ARE auditable via review.
- After implementation, no `_pending_` should remain in covered rows.

## Open Questions

0. **Should the local-embedder path (DS-13a) become the default in v1.5?** RESOLVED for v1.4: PUBLISH-BOTH, OpenAI primary, mxbai never-mixed secondary. The asymmetric directional bias finding (markcrawl +0.043 vs others' -0.007 to -0.077) means switching primary in v1.4 is unrecoverable from a credibility standpoint, even though aggregate Tau=0.952. v1.5 may revisit if (a) multi-trial measurements show the bias is run-to-run noise, OR (b) bge-large full-set validation shows mxbai's bias was idiosyncratic to that one model.
1. **Does the LLM-verification prompt reject queries even when the answer is in the page but requires reasoning?** If yes, this biases toward shallow factual queries vs conceptual queries. Need to test verification on ~10 queries spanning categories (api-function, conceptual, code-example, factual-lookup) before locking in the prompt.
2. **Should the v1.4 query set fully replace v1.3, or add to it?** Replacing is cleaner methodologically (no contamination from author-written queries). Adding gives more queries (better statistical power) but reintroduces COI in the additive subset. Default to **replace** unless v1.4 generation produces too few queries (<100).
3. **Where do `queries/*.json` live?** New `queries/` directory at repo root, or under `sites/`, or under `benchmark_data/`? Default to repo root `queries/` for discoverability; can move if it conflicts with existing structure.
4. **Should `make benchmark` regenerate the full crawl, or use cached crawl data?** Full regen is the "true reproducibility" claim but takes hours and hammers the sites. Default: `make benchmark` uses cached crawl (`runs/run_v13_merged_*`) and only re-runs downstream phases. `make benchmark-from-scratch` available for full regen including crawl.
5. **Public release path — GitHub release? HN post? blog?** Out of scope for this spec (this spec is the methodology hardening, not the launch). DS-14 produces the release notes; *when* and *where* to publish is a separate decision.
