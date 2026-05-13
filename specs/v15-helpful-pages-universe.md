---
spec_version: 2
name: v1.5 Helpful-Pages Universe — anchor-bias removal + decomposed leaderboard
status: draft
size: L
date: 2026-05-11
branch: feature/v15-helpful-pages-universe
depends_on: [v14-methodology-hardening]
affected_code:
  - benchmark_retrieval.py
  - reports/METHODOLOGY.md
  - reports/RETRIEVAL_COMPARISON.md
  - reports/RETRIEVAL_INTERSECTION.md (new artifact)
  - reports/COVERAGE_PER_SITE.md (new artifact)
  - reports/methodology_validation.md (new artifact — dual-judge cross-check report)
  - tools/generate_queries.py
  - tools/build_reference_corpus.py (new)
  - tools/judge_helpful_pages.py (new — dual-model: Haiku + gpt-4o-mini)
  - tools/intersection_set.py (new)
  - bench/reference_corpora/<site>/urls.txt (new git-tracked artifact, 11 files)
  - bench/helpful_pages/<site>.json (new git-tracked artifact, 11 files; dual-model schema)
  - bench/helpful_pages_disagreement.csv (new git-tracked artifact — per-URL disagreement rows)
  - bench/universe_manifest.json (new git-tracked artifact; includes judge_models + inter_model_agreement)
  - specs/v15-judge-prompt-v1.md (new versioned prompt artifact; model-agnostic)
  - queries/v15_queries.json (new)
  - queries/v15_intersection_queries.json (new)
constitution_reviewed: false
---

# v1.5 Helpful-Pages Universe — anchor-bias removal + decomposed leaderboard

## Problem Statement

The v1.4 cycle hardened methodology along every axis EXCEPT the one structural assumption that determines what "good crawl coverage" means: the test universe is anchored to a single tool's `pages.jsonl` (currently `crawl4ai-raw`). Three concrete consequences:

1. **Coverage = strategy alignment, not coverage.** When `generate_queries.py` samples URLs from crawl4ai-raw's output and asks "which tools' indexes contain this URL," it implicitly measures "which tools chose to crawl the URLs crawl4ai-raw chose." A tool with a deliberately conservative scope (markcrawl, with same-domain bounds + filter rules) takes the full coverage hit even if its retrieval pipeline is competitive. The v1.4 86% coverage / 14% retrieval decomposition pointed directly at this — 86% of markcrawl's drop is "didn't crawl the answer URL," only 14% is pipeline quality.

2. **Re-anchor flips the rankings.** Re-anchor on crawlee instead of crawl4ai-raw and the rankings shift. The user reading the leaderboard cannot tell how much the anchor matters because we publish only the post-anchor ranking. The human framed this as "luck of the draw" — not a robust statistical measurement of crawl quality but of crawl-strategy alignment with one specific tool's discovery pattern.

3. **Multi-trial measurement isn't actually possible.** v1.4 deferred multi-trial to v1.5 with a vague "we need CI bounds." The deeper reason it isn't possible today: each trial would re-sample LLM-generated queries from a freshly-crawled corpus, conflating three sources of variance — query-set variance, crawler-determinism variance, and retrieval variance. Without a fixed test universe, multi-trial measurements compound noise rather than isolate retrieval quality. v1.5's universe-fixing is the prerequisite for v1.5.1 multi-trial.

If shipped publicly without addressing this, the response from a determined hostile reviewer will be: "your coverage metric measures alignment with crawl4ai-raw's discovery strategy, not coverage of the site's actual content. Re-run with a different anchor and tell us how the ranking changes." We will not have a defensible answer.

**Out of scope:** Multi-trial measurement (deferred to v1.5.1 — universe-fixing in v1.5 is the enabler; CI-bounds infrastructure ships next). LLM-judged (query, returned-chunk) relevance to replace substring matching at retrieval time (deferred to v1.5.1 — separate body of work, doesn't depend on universe). Multilingual RAG eval (deferred indefinitely — explicit opt-in dimension when there's user demand). `scope=narrow` vs `scope=broad` selector (candidate, not commitment — re-evaluate after v1.5 ships).

## Solution Summary

Three-stage universe construction, decomposed leaderboard, intersection-set sibling report.

**Stage 1 — Universe enumeration per site.** Define the test universe ONCE per site, independently of any benchmarked tool. Preference order: (a) site `sitemap.xml` if present (fresh fetch, deduped + normalized via `_normalize_url_for_matching`), (b) union of v1.4's per-tool `pages.jsonl` files (capped per site, e.g., ≤5000 URLs after dedup), (c) **no fresh single-tool reference crawl** — that just relocates the anchor. Output: `bench/reference_corpora/<site>/urls.txt`, git-tracked, ~2.6 MB total across 11 sites.

**Stage 2 — Helpful-pages relevance filter (dual-model judging).** Per URL: fetch + TWO independent classifications — primary Haiku (`claude-haiku-4-5-20251001`) and secondary gpt-4o-mini (current GA snapshot, see DS-2 model lock). Both models receive the same model-agnostic prompt at `specs/v15-judge-prompt-v1.md`. The dual-judge serves two purposes: (a) cross-model methodology validation for v1.5.0 (defends against "why this judge?" reviewer attack), (b) forward-looking decision data for whether v1.5.x cycles can drop to a single cheaper judge (SC-12). Output: `bench/helpful_pages/<site>.json` (dual-model schema), git-tracked, plus `bench/helpful_pages_disagreement.csv` (per-URL disagreement rows). Calibration audit on 100 hand-judged pages × 4 representative sites against BOTH models before full-pool application. Both models must independently pass: per-site ground-truth agreement ≥90% AND multi-call disagreement <5% AND per-class agreement ≥85% on each binary class (helpful, non-helpful) — the per-class floor prevents class-imbalance hiding miscalibration. Canonical pick = the model with higher overall ground-truth agreement on the calibration set (tiebreak → Haiku). Per-site sanity check after full-pool with double-call confidence proxy on a 20-URL/site sample (~$0.11 total) applied to the canonical model only.

**Stage 3 — Query generation from helpful set.** Replace `generate_queries.py`'s crawl4ai-raw sampling with sampling from `bench/helpful_pages/<site>.json`. Carry over v1.4's DS-6 verifier (LLM-generated + LLM-verified, no human in acceptance loop). Output: `queries/v15_queries.json`.

**Decomposed leaderboard (primary).** For each (tool, site), report three numbers:

- **Coverage of helpful** = (helpful pages in tool's index) / (total helpful pages for the site). Absolute counts published alongside percentages.
- **Retrieval-on-covered MRR** = MRR on queries where the answer URL IS in the tool's index.
- **End-to-end MRR (headline)** = MRR over the full helpful-pages query set; un-crawled-page queries score 0 (implicit coverage penalty).

**Intersection-set sibling report.** Pages crawled by all 7 tools (with ≥10 pages on the site for tool inclusion in that site's intersection definition), filtered through helpful-pages, form the "luck-of-the-draw-removed" baseline. Sibling report `RETRIEVAL_INTERSECTION.md` published alongside the primary, NOT mixed with the leaderboard. Strict 7-way intersection aggregated to pool-level (~100-200 queries across 11 sites) for CI-meaningful N.

**Reproducibility manifest.** `bench/universe_manifest.json` records: sitemap fetch date per site (or "union-of-tools fallback, run_id=<X>"), helpful-pages judge prompt version + BOTH judge model versions (Haiku + gpt-4o-mini), canonical-pick choice and rationale, full-pool inter-model agreement (overall + per-site), per-site helpful-pages count + URL list hash, intersection-set definition + size per site + pool-level. Same defense-in-depth shape as v1.4's `models_manifest.json`.

**Multi-trial enabler framing.** v1.5 ships as single-trial with a fixed universe. v1.5.1 ships first multi-trial cycle once CI-bounds infra lands. The point: with a fixed universe, multi-trial finally isolates retrieval variance cleanly rather than compounding query-set + crawler-determinism + retrieval noise.

## Success Criteria

- **SC-1** — **Given** a v1.5 cycle, **When** `bench/reference_corpora/<site>/urls.txt` is built, **Then** every site's URL list comes from either (a) a fresh `sitemap.xml` fetch (with `fetch_date` recorded in the manifest), or (b) the deduped+normalized union of all 7 v1.4 tools' `pages.jsonl` files (with the source `run_id` recorded in the manifest). No site's universe comes from a single fresh tool-specific reference crawl.

- **SC-2** — **Given** the helpful-pages judge runs on the universe (dual-model: Haiku + gpt-4o-mini), **When** results land at `bench/helpful_pages/<site>.json`, **Then** each entry contains the dual-model schema: `[url, haiku: {classification, rationale, judged_at, judge_call_id}, gpt4omini: {classification, rationale, judged_at, judge_call_id}, canonical: "haiku"|"gpt4omini", agreement: bool, judge_prompt_version, haiku_model_version, gpt4omini_model_version]`. Per-URL disagreement rows (where `agreement == false`) also land in `bench/helpful_pages_disagreement.csv` with both rationales for review. The judge prompt itself lives at `specs/v15-judge-prompt-v1.md` as a versioned, diff-reviewable artifact — the prompt is model-agnostic (validated in DS-2 calibration that both models follow the two-line output discipline).

- **SC-3** — **Given** the dual-model calibration audit, **When** complete, **Then** 100 hand-judged pages × 4 representative sites (3 content-shape sites + rust-book as small-corpus check) have been compared independently against BOTH Haiku's AND gpt-4o-mini's classifications, AND each model independently meets THREE thresholds: per-site ground-truth agreement ≥90% AND multi-call self-agreement check at 3× shows <5% disagreement AND per-class agreement ≥85% on each binary class (helpful, non-helpful). The three thresholds catch different failure modes — the ≥90% bar catches systematic miscalibration; the <5% bar catches random softness; the per-class ≥85% bar prevents class imbalance from hiding minority-class miscalibration (e.g., if helpful pages are 80% of the universe, a model could hit 90% raw agreement while being only 50% accurate on the non-helpful class). Canonical model = the one with higher overall ground-truth agreement on the calibration set; tiebreak → Haiku (status-quo default per v1.5 spec lock). If either model fails any threshold, the spec branches: (a) if the prompt is at fault (both models fail similarly), iterate the prompt and re-run both calibrations; (b) if only one model fails, the canonical pick defaults to the passing model and SC-14 marks `v15x_can_drop_to_single_cheap` as "blocked — <failed-model> failed calibration." Audit results stored at `bench/calibration_audit_v15.csv` (both models' per-page outputs alongside ground truth).

- **SC-4** — **Given** the helpful-pages judge has run on the full universe, **When** per-site sanity check is performed, **Then** for each site: (a) total helpful-pages count is recorded, (b) the 10 lowest-confidence accepts and 10 highest-confidence rejects are eyeballed for systematic prompt failures, (c) any site whose helpful-pages set is <5% or >95% of universe URLs is flagged for prompt review (likely indicates a content-shape failure of the prompt on that site). Sanity-check log stored at `bench/sanity_check_v15.md`.

- **SC-5** — **Given** v1.5 query generation, **When** `tools/generate_queries.py` runs, **Then** it samples URLs from `bench/helpful_pages/<site>.json` (NOT from any tool's `pages.jsonl`), drafts queries via gpt-4o-mini, verifies with a separate independent gpt-4o-mini invocation (no shared context, same DS-6 pattern from v1.4), and writes accepted queries to `queries/v15_queries.json`. Rejected queries land in `queries/v15_rejected.json` with rationale prefixes (`answer-not-in-page:` or `page-broken:`, same DS-6 conventions).

- **SC-6** — **Given** v1.5 retrieval results, **When** RETRIEVAL_COMPARISON.md is generated, **Then** every per-tool row reports THREE metrics: (a) **Coverage of helpful** as both percentage AND absolute count (e.g., "43% (1,800 / 4,200)"), (b) **Retrieval-on-covered MRR**, (c) **End-to-end MRR** as the headline-ranked column. Sort order is by End-to-end MRR descending.

- **SC-7** — **Given** v1.5 retrieval results, **When** `RETRIEVAL_INTERSECTION.md` is generated, **Then** it contains: (a) intersection-set definition + per-site sizes + pool-level size, (b) per-tool intersection MRR, (c) explicit warning when pool-level N < 80 ("intersection MRR has wide CI at this measurement resolution"), (d) note that intersection-set is filtered through helpful-pages (i.e., intersection ∩ helpful-pages, not raw intersection), (e) explicit "this is a sibling reference, not the primary leaderboard" framing at the top.

- **SC-8** — **Given** any v1.5 cycle, **When** `bench/universe_manifest.json` is read, **Then** it contains: (a) per-site `sitemap_fetch_date` OR `union_of_tools_run_id` (mutually exclusive — one of the two), (b) `judge_prompt_version` + top-level `judge_models` object (`primary_haiku` / `secondary_gpt4omini` versions + `canonical_choice` + `canonical_chose_by` rationale), (c) top-level `inter_model_agreement` object (`overall_pct`, per-site `<site>: pct`, `per_class_min_pct` for helpful/non-helpful, `v15x_can_drop_to_single_cheap` boolean per SC-14 evaluation), (d) per-site `helpful_pages_count` (under the canonical model) + `url_list_sha256`, (e) intersection-set sizes (per-site + pool-level), (f) git commit at run time. Sufficient to reproduce or compare two cycles' universes AND to evaluate the gpt-4o-mini-viability rule.

- **SC-9** — **Given** v1.5 METHODOLOGY.md, **When** read, **Then** the "Anti-gaming" section has been extended with the v1.5-specific defenses: anchor-tool gaming (defense: universe is anchor-independent), helpful-pages judge gaming (defense: prompt is versioned + calibration-audited + multi-call agreement-checked), intersection-set boilerplate inflation (defense: intersection ⊂ helpful-pages). The per-site limitations section discloses: "helpful-pages count = (sitemap OR union-of-tools-discovered) ∩ LLM-judged-helpful, NOT all substantive content the site contains."

- **SC-10** — **Given** v1.5 release notes, **When** published, **Then** they lead with the v1.4→v1.5 leaderboard delta showing every tool's per-dimension change (coverage %, retrieval-on-covered MRR, end-to-end MRR, intersection MRR). If markcrawl looks worse on any dimension under the new universe, the writeup leads with that delta — same v1.4 discipline applied to v1.5.

- **SC-11** — **Given** v1.5 ships as single-trial, **When** METHODOLOGY.md explains the multi-trial roadmap, **Then** it states explicitly: "v1.5 = locked-foundation single-trial; v1.5.1 = first multi-trial cycle once CI-bounds infrastructure lands." The reasoning is documented: with a fixed universe, multi-trial finally isolates retrieval variance cleanly rather than compounding query-set + crawler-determinism + retrieval noise.

- **SC-12** — **Given** the helpful-pages corpora and `universe_manifest.json` are produced, **When** committed, **Then** they are git-tracked under `bench/reference_corpora/` and `bench/helpful_pages/` (NOT local-only artifacts). Reproducibility claims about v1.5 numbers must be verifiable without re-fetching sitemaps that may have changed.

- **SC-13** — **Given** PUBLISH-BOTH primary + secondary embedders are still in scope, **When** v1.5 reports are generated, **Then** the helpful-pages universe is shared across primary and secondary (universe is anchor-independent, not embedder-specific). Both `RETRIEVAL_COMPARISON.md` (primary, OpenAI text-embedding-3-small) and `RETRIEVAL_COMPARISON_LOCAL.md` (secondary, mxbai) report the three-metric decomposition over the same helpful-pages set.

- **SC-14 (gpt-4o-mini viability criterion)** — **Given** the full-pool dual-model judging completes, **When** `bench/universe_manifest.json` records inter-model agreement statistics, **Then** the decision rule for whether v1.5.x cycles can drop to gpt-4o-mini-only is evaluated and recorded as a boolean + rationale:

  | Inter-model agreement (full pool) | Per-site min agreement | Per-class min agreement | Action in v1.5.x |
  |---|---|---|---|
  | ≥95% AND | ≥90% on all 11 sites AND | ≥85% on each of helpful / non-helpful | v1.5.x cycles MAY drop to gpt-4o-mini-only |
  | ≥85% AND | ≥75% on all 11 sites AND | ≥80% on each class | Targeted dual-judge required on identified high-disagreement strata; otherwise gpt-4o-mini-only OK |
  | <85% OR | <75% on any site OR | <80% on any class | Keep full dual-judge in v1.5.x; investigate divergence and refine prompt or model choice |

  The criterion is published in `reports/methodology_validation.md` as part of the v1.5.0 release, with the disagreement-row analysis (top sites contributing to disagreement, content-shape patterns in disagreements). The per-class agreement floor matches SC-3's calibration bar — both prevent class-imbalance hiding miscalibration in either calibration or full-pool agreement. The boolean result feeds the `v15x_can_drop_to_single_cheap` field in the universe manifest. PREREQUISITE: both models must have passed SC-3 calibration; if gpt-4o-mini fails SC-3, SC-14 records `blocked — gpt-4o-mini failed calibration` and v1.5.x cycles continue with Haiku-only by default.

## Flow

```
v1.4 ship (current — main, tagged bench-v1.4)
       │
       ▼
DS-0: Spec doc (this file) + judge prompt v1 artifact
       │
       ▼
DS-1: Reference corpora per site (sitemap-or-union-of-tools)
       │  ├─ Per-site: sitemap.xml fetch attempt
       │  ├─ Fallback: union of v1.4 tools' pages.jsonl
       │  └─ Output: bench/reference_corpora/<site>/urls.txt (11 files, git-tracked)
       │
       ▼
DS-2: Helpful-pages judge implementation + calibration audit
       │  ├─ Build tools/judge_helpful_pages.py
       │  ├─ Calibration: 100 hand-judged × 3 sites
       │  ├─ Multi-call agreement check (3× on calibration set)
       │  ├─ Prompt iteration if needed (2-3 expected)
       │  ├─ Full-pool application (~$28 spend)
       │  └─ Per-site sanity check + audit log
       │
       ▼
DS-3: generate_queries.py rewrite (sample from helpful-pages)
       │
       ▼
DS-4: Three-metric decomposition in benchmark_retrieval.py
       │  ├─ Coverage of helpful (% + absolute counts)
       │  ├─ Retrieval-on-covered MRR
       │  └─ End-to-end MRR (headline)
       │
       ▼
DS-5: Intersection-set computation + RETRIEVAL_INTERSECTION.md sibling
       │  ├─ tools/intersection_set.py: pages ∩ all-tools, ≥10-page threshold
       │  ├─ Filter intersection ⊂ helpful-pages
       │  ├─ Aggregate to pool-level (CI-meaningful N)
       │  └─ Sibling report renderer
       │
       ▼
DS-6: Intersection query generation (re-uses DS-3 machinery)
       │  └─ Output: queries/v15_intersection_queries.json
       │
       ▼
DS-7: Reproducibility manifest extensions (universe_manifest.json)
       │
       ▼
DS-8: METHODOLOGY.md + per-site limitations + anti-gaming additions
       │
       ▼
DS-9: First v1.5 publication run + v1.4→v1.5 leaderboard delta release notes
       │
       ▼
v1.5 ship (anchor-bias removed; decomposed leaderboard; multi-trial-ready foundation)
       │
       ▼
v1.5.1 (first multi-trial cycle, separate spec)
```

## Implementation Roadmap

### Smoke-test gates

Each gate ends with a `make benchmark-quick` smoke run on a single site (rust-book) to catch integration regressions before the next gate starts. Gates that are pure additions (DS-1, DS-2 corpus build) skip smoke; gates that touch retrieval semantics (DS-4, DS-5, DS-6) MUST smoke before commit.

### Gate-by-gate

| Day | Gate | Deliverable | Output | Smoke required |
|---|---|---|---|---|
| 0 | G0 | DS-0 — spec doc + judge prompt artifact | `specs/v15-helpful-pages-universe.md` + `specs/v15-judge-prompt-v1.md` | n/a (no code) |
| 1-3 | G1 | DS-1 — reference corpora per site | `bench/reference_corpora/<site>/urls.txt` × 11 | n/a (build-only) |
| 3-5 | G2 | DS-2 — dual-model helpful-pages judge + calibration | `bench/helpful_pages/<site>.json` × 11 (dual-model) + `bench/helpful_pages_disagreement.csv` + `bench/calibration_audit_v15.csv` + `bench/sanity_check_v15.md` + `reports/methodology_validation.md` | n/a (data artifact) |
| 6 | G3 | DS-3 — generate_queries.py rewrite | `queries/v15_queries.json` + `queries/v15_rejected.json` | yes (verify retrieval still loads queries) |
| 7 | G4a + G4b | DS-5 + DS-6 in parallel — intersection sibling | `tools/intersection_set.py` + `RETRIEVAL_INTERSECTION.md` + `queries/v15_intersection_queries.json` | yes (single-site smoke on rust-book) |
| 8 | G5 | DS-4 — three-metric decomposition in primary | `RETRIEVAL_COMPARISON.md` schema update + `COVERAGE_PER_SITE.md` (new) | yes (full smoke) |
| 8 | G6 | DS-7 — universe_manifest.json | `bench/universe_manifest.json` | n/a (manifest-only) |
| 9 | G7 | Smoke validation (`make benchmark-quick` on 1-2 sites) | Confirms integration end-to-end | yes |
| 10-12 | G8 | DS-9 — first v1.5 publication run + release notes + DS-8 docs | Full 11-site v1.5 cycle + `docs/V15_RELEASE_NOTES.md` + METHODOLOGY.md updates | n/a (this IS the publication run) |

Critical path: DS-1 → DS-2 → DS-3 → DS-4. DS-5 + DS-6 parallel after DS-3. DS-7 + DS-8 land alongside DS-4. DS-9 is the publication gate.

### Pre-merge 6+1 gate (mirrors v1.4)

Before merging `feature/v15-helpful-pages-universe` to `main`:

1. `pytest tests/ -q` — all green (existing 203 + new v1.5 tests)
2. `lint_reports.py` — all 12+ reports pass (10 existing + RETRIEVAL_INTERSECTION + COVERAGE_PER_SITE)
3. `check_invariants.py` — all green
4. `bench/universe_manifest.json` — exists + populated for primary AND `_LOCAL` if PUBLISH-BOTH-secondary ran
5. Calibration + sanity check + methodology-validation artifacts (`calibration_audit_v15.csv`, `sanity_check_v15.md`, `helpful_pages_disagreement.csv`, `reports/methodology_validation.md`) — exist + meet SC-3/SC-4/SC-14 thresholds (or SC-14 records `blocked` per asymmetric-failure rule)
6. `git diff --stat` review against the cycle scope
7. `make benchmark-quick` — full integration smoke on rust-book, exits 0

## Detailed Steps

### DS-0: Spec doc (this file) + judge prompt v1 artifact

This document. Plus a sibling `specs/v15-judge-prompt-v1.md` containing the helpful-pages judge prompt as a separately versioned, diff-reviewable artifact. The judge prompt evolves across v1.5.x cycles independently of the methodology spec; pinning each version in its own file keeps prompt diffs reviewable in isolation.

Acceptance: both files committed on `feature/v15-helpful-pages-universe`. Posted to `chat.md` for markcrawl-agent review before any code in DS-1+ lands.

### DS-1: Build reference corpora per site

`tools/build_reference_corpus.py` — per site:

1. Attempt to fetch `<site>/sitemap.xml` (and `sitemap_index.xml`, recursive). Respect robots.txt + 3-attempt backoff. If success: parse `<loc>` elements, normalize via `_normalize_url_for_matching`, dedup. If URL count > 10000, **random-sample 10000 with a fixed seed** (recorded in the manifest as `sitemap_url_sample_seed: <int>`) — preserves determinism across rebuilds while bounding cost symmetrically across sites. Asymmetric raising of the cap for one large site (HF transformers, ~25k URLs) would inflate that site's full-pool spend disproportionately. Per-site limitations note required for any sampled site: "Sitemap had ~25k URLs; v1.5 random-samples 10k with seed N for cost control." Record `sitemap_fetch_date` for the manifest.
2. If sitemap missing OR yields fewer than 50 URLs (likely stale/incomplete): fall back to union-of-tools. Read all 7 v1.4 tools' `pages.jsonl` for the site from the canonical v1.4 run (`run_v13_merged_20260504_203748`), extract URLs, normalize, dedup, cap at 5000, record `union_of_tools_run_id` for the manifest.
3. Write `bench/reference_corpora/<site>/urls.txt` (one URL per line, alphabetical for git-diff stability) + `bench/reference_corpora/<site>/source.json` (records which path was used + counts).

Output: 11 site directories, ~2.6 MB total, git-tracked.

Per-site site list comes from `sites/pool_v1.yaml` (same 11-site pool as v1.4).

Acceptance: SC-1 met. All 11 sites have a `urls.txt` with ≥50 URLs. Source recorded per site.

### DS-2: Dual-model helpful-pages judge + calibration audit

`tools/judge_helpful_pages.py` — per URL in each site's reference corpus, runs BOTH primary (Haiku) and secondary (gpt-4o-mini) classifications:

1. Fetch URL with the existing crawl4ai-raw fetcher (consistent fetcher for all judged content; we are not benchmarking the fetcher here, just feeding the judge consistent input). Strip nav chrome via `strip_nav_chrome()` (re-using v1.4's DS-6 helper). Truncate to first 2000 chars after chrome-strip.
2. Call Haiku (`claude-haiku-4-5-20251001`) with the prompt at `specs/v15-judge-prompt-v1.md`. Temperature=0.
3. Call gpt-4o-mini (model snapshot pinned to current GA at universe-build time — see Model lock note below) with the SAME prompt. Temperature=0. The prompt is model-agnostic; DS-2 calibration validates both models follow the two-line output discipline.
4. Sequential per-URL (NOT parallel across models). Sequential ordering keeps rate-limit accounting simple per provider; the bench is not latency-sensitive (universe build is offline). Per-call back-off is the existing tenacity retry pattern; if either provider's request fails after retries, that URL is skipped and logged for re-judgment (do NOT silently fall back to single-model on a sampled URL).
5. Write `bench/helpful_pages/<site>.json` in the dual-model schema (per SC-2): each entry has both models' outputs, the canonical pick (set per-corpus from calibration result), the agreement boolean, prompt version, both model versions, and timestamps.
6. Emit per-URL disagreement rows (where `agreement == false`) to `bench/helpful_pages_disagreement.csv` for the methodology-validation report.

**Model lock — both judges:**

- **Primary (Haiku):** `claude-haiku-4-5-20251001` (pinned per Q2 resolution).
- **Secondary (gpt-4o-mini):** pinned at universe-build time to OpenAI's current GA snapshot for gpt-4o-mini. Implementation MUST query the OpenAI API at build time to resolve the snapshot ID (e.g., `gpt-4o-mini-2024-07-18` if still available, else the current replacement) and record the exact snapshot ID in the manifest. If the proposed snapshot is deprecated/retired, the resolver picks the next-available `gpt-4o-mini-*` GA model; if none, DS-2 falls back to Haiku-only and SC-14 records `blocked — gpt-4o-mini snapshot unavailable`.

**External dependency note (escalation-worthy at universe-build time):** This step adds an OpenAI API key requirement to the universe-build flow. OpenAI keys are already required for query generation (DS-3 uses gpt-4o-mini) and embeddings (DS-4), so this is not a new external dependency in the v1.5.0 pipeline — but it IS a new dependency on the specific `judge_helpful_pages.py` tool, which previously was Anthropic-only.

**Pre-calibration cost validation (FIRST action of DS-2):**

Before the calibration run itself, fire a 10-page sanity check against BOTH Haiku and gpt-4o-mini to record actual per-call input/output token counts for each provider. Cost: ~$0.005 total (Haiku $0.0025 + gpt-4o-mini ~$0.0015). Records grounded per-page measurements so the full-pool projection isn't an estimate. If actual cost across both models exceeds the $30 budget cap by >20% at the 10-page check (i.e., projects to >$36 full-pool combined), escalate to chat.md before proceeding with calibration.

**Calibration audit (BEFORE full-pool) — DUAL-MODEL:**

1. Pick 4 representative sites covering content-shape diversity + a small-corpus check: docs (`huggingface-transformers`), ecommerce (`newegg`), blog (`propublica`), small-corpus (`rust-book`, ~423 URLs — surfaces the edge case where helpful ratio is high simply because the site is naturally dense).
2. For each: hand-classify 100 random URLs from its reference corpus → store ground truth at `bench/calibration_ground_truth_v15.csv`.
3. Run BOTH judges on those 400 URLs (independent runs, neither model sees the other's output). Compute, FOR EACH MODEL INDEPENDENTLY: per-site agreement %, per-site false-helpful + false-non-helpful counts, per-class agreement % (helpful / non-helpful separately).
4. Multi-call agreement check FOR EACH MODEL: re-run each judge 2 more times on the same 400 URLs (3 total calls per model). Compute pairwise disagreement %. Document version bumps as `v15-judge-prompt-v1.md` → `v15-judge-prompt-v2.md` etc. (a prompt iteration triggers re-calibration of BOTH models).
5. Lock the prompt version when EACH MODEL INDEPENDENTLY meets THREE thresholds: per-site ground-truth agreement ≥90% on each of the 4 calibration sites AND multi-call self-disagreement <5% AND per-class agreement ≥85% on each binary class.
6. **Canonical pick:** the model with higher overall ground-truth agreement on the 400-URL calibration set. Record in `bench/universe_manifest.json` under `judge_models.canonical_choice` with `canonical_chose_by: "calibration_ground_truth_agreement"`. If tied within 0.5 pp, tiebreak → `haiku` (status-quo per spec lock).
7. **Asymmetric failure handling:** If only one model fails calibration, the canonical pick defaults to the passing model and SC-14 records `blocked — <failed-model> failed calibration`. v1.5.x cycles continue with the passing model only; no SC-14 viability evaluation against the failed model. If both models fail similarly, the prompt is at fault — iterate per (5) above. If both models fail differently, escalate to chat.md for joint review of whether the disagreement is prompt or content.

**Full-pool application — budget cap framing:** Budget cap = $30 (covers Haiku full-pool ~$15 + gpt-4o-mini full-pool ~$6 + calibration audits on both ~$1 + sanity-check confidence proxy ~$0.11 + headroom). Hard escalation threshold = $50 per Risk Assessment R5. The dual-model cost increment over single-judge is ~$5 marginal in v1.5.0 (offset by potential ~$10/cycle savings in v1.5.x if SC-14 thresholds met). If the 10-page validation projects full-pool combined cost >$36, escalate before firing.

**Per-site sanity check (AFTER full-pool) — applied to canonical model only:**

1. Per site: count helpful pages under the canonical model, compute helpful/total ratio.
2. **Confidence proxy via double-call on the sanity-check sample only (not full-pool).** For each site, sample 20 URLs (random across the full URL set), re-judge each one once more under the canonical model, and flag the URLs where the two calls disagreed as "low confidence." Cost: 20 URLs × 11 sites × 2 calls = 440 extra calls under the canonical model = ~$0.11 total. This is a 4th call per page on a sampled subset, NOT a 2nd call across all pages — full-pool double-call would be ~$30 and is explicitly out of scope for v1.5 (revisit in v1.5.x if sanity check surfaces systematic confidence problems).
3. Eyeball 10 lowest-confidence (= disagreed) accepts + 10 highest-confidence (= consistent across calls) rejects per site.
4. Flag any site where helpful ratio is <5% or >95% as likely prompt failure on that site's content shape. If flagged: re-prompt or accept-with-disclosure in METHODOLOGY.md.
5. Document in `bench/sanity_check_v15.md`.

**Cross-model methodology validation (NEW for dual-model amendment):**

After full-pool dual-model judging completes, generate `reports/methodology_validation.md`:

1. Overall inter-model agreement %, per-site inter-model agreement %, per-class min agreement %.
2. SC-14 evaluation: which row of the criterion table applies; the resulting `v15x_can_drop_to_single_cheap` boolean.
3. Disagreement analysis from `bench/helpful_pages_disagreement.csv`: top 3 sites by disagreement count, content-shape patterns (e.g., "47% of disagreements are on API-reference pages where Haiku says helpful and gpt-4o-mini says non-helpful").
4. Recommendation for v1.5.x cycles: drop to gpt-4o-mini-only / targeted dual-judge / keep full dual-judge.

Acceptance: SC-2, SC-3, SC-4, SC-14 met.

### DS-3: `generate_queries.py` rewrite

Rewrite the URL-sampling step in `tools/generate_queries.py` to read from `bench/helpful_pages/<site>.json` (filter where `classification == "helpful"`) instead of from `crawl4ai-raw`'s `pages.jsonl`. Carry over the existing v1.4 DS-6 verifier logic verbatim.

Other changes:
- `SCOPE_PREFIXES` no longer needed (helpful-pages is already site-scoped via the reference corpus). Mark as deprecated; remove in v1.5.1.
- `is_locale_mirror_url()` filter still applies (locale-mirror URLs may sneak in via sitemap; keep the filter).
- `strip_nav_chrome()` still applies to the page content fed to the LLM for query generation.

Output: `queries/v15_queries.json` + `queries/v15_rejected.json`.

Acceptance: SC-5 met. Query count target: ~500-700 across 11 sites (similar density to v1.4's 561). 100% in-scope by construction (helpful-pages is the universe).

### DS-4: Three-metric decomposition in `benchmark_retrieval.py`

Extend `benchmark_retrieval.py` to compute and report all three metrics per (tool, site):

1. **Coverage of helpful** — for each tool's `pages.jsonl`, normalize URLs via `_normalize_url_for_matching`, intersect with `bench/helpful_pages/<site>.json` filtered to `helpful`. Coverage = |intersection| / |helpful_pages|. Report both as percentage AND absolute count: `"43% (1,800 / 4,200)"`.

2. **Retrieval-on-covered MRR** — for each query whose answer URL is in the tool's index (i.e., the tool has the page), compute page-level MRR. For queries whose answer URL is NOT in the tool's index, exclude from this metric.

3. **End-to-end MRR (headline)** — for each query in the full helpful-pages query set, compute page-level MRR, scoring 0 for queries whose answer URL is not in the tool's index. This is the headline-ranked column.

Schema changes:
- `RetrievalModeResult` dataclass: add `coverage_pct`, `coverage_count`, `coverage_total`, `retrieval_on_covered_mrr`, `end_to_end_mrr`.
- `ToolSiteRetrievalResult`: same.
- Checkpoint key: include `helpful_pages_url_list_sha256` so universe changes invalidate cache.

Report changes:
- `RETRIEVAL_COMPARISON.md`: add the three-metric column. Sort by end-to-end MRR descending.
- New file `COVERAGE_PER_SITE.md`: per-site coverage breakdown with absolute counts.

Acceptance: SC-6 met.

### DS-5: Intersection-set + `RETRIEVAL_INTERSECTION.md`

`tools/intersection_set.py`:

1. For each site: load all 7 tools' v1.4 `pages.jsonl`. Tools with <10 pages on the site are excluded from THAT site's intersection definition (record exclusion in the manifest). Compute intersection of normalized URLs across remaining tools.
2. Filter intersection ⊂ `bench/helpful_pages/<site>.json` (`classification == "helpful"`). This is the per-site intersection-helpful set.
3. Per-site intersection-helpful counts feed into pool-level aggregation.

Sibling report `reports/RETRIEVAL_INTERSECTION.md`:

- Header: explicit "this is a sibling reference report, NOT the primary leaderboard. It isolates retrieval pipeline quality from coverage strategy by computing MRR only on pages every tool crawled."
- Intersection-set definition section: how it was computed, per-site sizes, pool-level size.
- Per-tool intersection MRR (over `queries/v15_intersection_queries.json` from DS-6). Sorted by MRR descending.
- Warning at top if pool-level N < 80: "intersection MRR has wide CI at this measurement resolution."
- Excluded-tools note: "tools excluded from a site's intersection (had <10 pages there): ..."

Acceptance: SC-7 met.

### DS-6: Intersection query generation

Re-use DS-3's machinery, but sample URLs from the per-site intersection-helpful set (output of DS-5) instead of from `bench/helpful_pages/<site>.json`. Same DS-6 verifier from v1.4. Output: `queries/v15_intersection_queries.json` (~100-200 queries pool-level expected).

Acceptance: queries land + load successfully in DS-5's intersection MRR computation.

### DS-7: `bench/universe_manifest.json`

Single git-tracked manifest with dual-model judging fields:

```json
{
  "universe_built_at": "2026-05-XXTYY:ZZ:00Z",
  "judge_prompt_version": "specs/v15-judge-prompt-v1.md (sha256: ...)",
  "judge_models": {
    "primary_haiku": "claude-haiku-4-5-20251001",
    "secondary_gpt4omini": "gpt-4o-mini-2024-07-18",
    "canonical_choice": "haiku",
    "canonical_chose_by": "calibration_ground_truth_agreement",
    "calibration_haiku_overall_pct": 92.5,
    "calibration_gpt4omini_overall_pct": 91.0
  },
  "inter_model_agreement": {
    "overall_pct": 94.2,
    "per_site": {
      "huggingface-transformers": 95.1,
      "newegg": 88.4,
      "propublica": 93.7,
      "rust-book": 96.2,
      "stripe-docs": 95.5,
      "kubernetes-docs": 94.8,
      "postgres-docs": 95.3,
      "mdn-css": 93.9,
      "smittenkitchen": 92.1,
      "react-dev": 94.5,
      "ikea": 89.2
    },
    "per_class_min_pct": {
      "helpful": 92.0,
      "non_helpful": 87.5
    },
    "v15x_can_drop_to_single_cheap": false,
    "v15x_decision_rationale": "Per-site min agreement (88.4% on newegg) below 90% threshold — targeted dual-judge required on ecommerce-shaped strata; gpt-4o-mini-only not yet validated for v1.5.x cycles."
  },
  "git_commit": "<sha at build time>",
  "sites": {
    "rust-book": {
      "source": "sitemap",
      "sitemap_fetch_date": "2026-05-XX",
      "sitemap_url_sample_seed": null,
      "url_list_sha256": "...",
      "url_count": 423,
      "helpful_pages_count": 387,
      "helpful_pages_count_haiku": 387,
      "helpful_pages_count_gpt4omini": 392,
      "intersection_size": 215,
      "intersection_excluded_tools": []
    },
    "huggingface-transformers": {
      "source": "sitemap",
      "sitemap_fetch_date": "2026-05-XX",
      "sitemap_url_sample_seed": 42,
      "sitemap_url_total_pre_sample": 25410,
      "url_list_sha256": "...",
      "url_count": 10000,
      "helpful_pages_count": 8214,
      "helpful_pages_count_haiku": 8214,
      "helpful_pages_count_gpt4omini": 8095,
      "intersection_size": 1872,
      "intersection_excluded_tools": []
    },
    "newegg": {
      "source": "union_of_tools",
      "union_of_tools_run_id": "run_v13_merged_20260504_203748",
      "url_list_sha256": "...",
      "url_count": 1820,
      "helpful_pages_count": 1234,
      "helpful_pages_count_haiku": 1234,
      "helpful_pages_count_gpt4omini": 1389,
      "intersection_size": 89,
      "intersection_excluded_tools": ["colly+md"]
    }
  },
  "intersection_pool_total": 1432
}
```

Schema notes:
- `helpful_pages_count` is the count under the canonical model (the count consumed by DS-3 query generation + DS-4 retrieval). `helpful_pages_count_haiku` / `helpful_pages_count_gpt4omini` are recorded alongside for cross-check.
- `inter_model_agreement.per_class_min_pct` lets a reader see whether 95% overall agreement is hiding a minority-class miscalibration (relevant per the SC-3 per-class floor).
- `v15x_can_drop_to_single_cheap` is the SC-14 decision rule result.
- `v15x_decision_rationale` is a human-readable string explaining which threshold passed/failed; published in `reports/methodology_validation.md` verbatim.

Acceptance: SC-8 met. Manifest written by `tools/build_reference_corpus.py` + extended by `tools/judge_helpful_pages.py` (dual-model fields + agreement stats + SC-14 decision) + extended by `tools/intersection_set.py`. Each tool merges its section atomically (same pattern as v1.4 `models_manifest.py`).

### DS-8: METHODOLOGY.md + per-site limitations + anti-gaming additions

Append to METHODOLOGY.md:

1. **"Helpful-pages universe" section** explaining the three-stage construction + the anchor-bias problem v1.5 fixes + dual-model judging rationale (cross-validation + forward-looking model-choice criterion).
2. **Anti-gaming table additions** (parallel shape to v1.4's anti-gaming table):
   - Anchor-tool gaming: defense = universe is anchor-independent (sitemap or union-of-tools).
   - Helpful-pages judge gaming: defense = prompt is versioned + calibration-audited + multi-call agreement-checked + cross-validated against a second independent LLM judge (Haiku + gpt-4o-mini); disagreement rows published as `bench/helpful_pages_disagreement.csv`.
   - Single-judge model bias: defense = dual-model judging with per-site agreement statistics published; SC-14 criterion for whether future cycles may drop to a single cheaper judge.
   - Intersection-set boilerplate inflation: defense = intersection ⊂ helpful-pages (under the canonical model).
3. **Per-site limitations section**: "helpful-pages count = (sitemap OR union-of-tools-discovered) ∩ LLM-judged-helpful (under the canonical model), NOT all substantive content the site contains. Sites with sitemap incompleteness or systematic union-of-tools blindspots will have helpful-pages sets that under-cover the site. Sites with high inter-model judge disagreement (below SC-14 per-site thresholds) are flagged in `reports/methodology_validation.md` and warrant dual-judge in subsequent cycles."
4. **Multi-trial roadmap paragraph**: "v1.5 = locked-foundation single-trial; v1.5.1 = first multi-trial cycle."
5. **Dual-judge methodology section**: Brief explainer of why two judges (defends "why this model?" attack; produces forward-looking decision data) + pointer to `reports/methodology_validation.md` + the SC-14 criterion table.

Acceptance: SC-9, SC-11 met.

### DS-9: First v1.5 publication run + release notes

Run the full v1.5 cycle on all 11 sites under primary embedder (OpenAI text-embedding-3-small). Re-fire under PUBLISH-BOTH secondary (mxbai) — universe is shared across embedders, only retrieval re-runs.

Generate `docs/V15_RELEASE_NOTES.md` with:

1. TL;DR — one-line answer (e.g., "v1.5 ships anchor-bias-free leaderboard; markcrawl moves from 7th to Xth on End-to-end MRR; coverage gap explicitly visible").
2. v1.4→v1.5 leaderboard delta table (all 7 tools × 4 dimensions: coverage, retrieval-on-covered, end-to-end, intersection).
3. What changed methodologically (helpful-pages universe + decomposition + intersection sibling).
4. What survived (PUBLISH-BOTH; OpenAI primary; LLM-gen+verify queries; cost calculator).
5. What's deferred to v1.5.1 (multi-trial measurement; LLM-judged retrieval relevance).
6. Anti-gaming additions (the three new defenses).
7. How to reproduce (`make benchmark` against v1.5 universe; `bench/universe_manifest.json` as the audit trail).

Acceptance: SC-10 met. PUBLISH-BOTH symmetry preserved (primary + `_LOCAL` reports for retrieval, intersection, coverage).

## Edge Cases

- **Sitemap gives a different URL set across cycles.** Expected — sites add/remove pages. The manifest's `sitemap_fetch_date` makes this auditable. Year-over-year leaderboard comparison requires either (a) re-using the prior universe (frozen via git history) or (b) explicitly noting the universe changed and how.
- **Union-of-tools fallback misses content all tools missed.** Honest limitation, disclosed in METHODOLOGY.md per-site limitations. Cannot be solved without a fresh single-tool reference crawl, which we explicitly reject as anchor-relocation.
- **Site with very small helpful-pages set (e.g., <50 pages).** Per-site MRR has wide variance. Report site-level helpful-pages count alongside MRR so reader can judge CI implications.
- **Tool with zero pages on a site (e.g., colly+md on WAF-blocked site).** Coverage = 0%, end-to-end MRR = 0 for that site, retrieval-on-covered MRR undefined (no covered pages). Report "n/a" for retrieval-on-covered; use 0 for end-to-end. Excluded from that site's intersection definition.
- **All 7 tools fail on a site.** Intersection = ∅, no intersection queries from that site. Site contributes 0 to all tools on end-to-end. Disclose in per-site limitations: "<site> excluded from intersection set due to universal tool failure."
- **Helpful-pages judge inconsistency on a borderline page.** Multi-call agreement check at calibration catches systematic softness. For runtime per-page inconsistency: temp=0 + first-call-wins + version recorded in manifest. Document the limitation; multi-trial v1.5.1 can revisit.
- **Sitemap robots.txt block.** If `robots.txt` disallows sitemap fetch, fall through to union-of-tools fallback. Record `sitemap_fetch_status: blocked_by_robots` in manifest.
- **Universe changes mid-cycle (rare but possible: someone re-runs `build_reference_corpus.py` after queries are generated).** Checkpoint key includes `helpful_pages_url_list_sha256`; mid-cycle change invalidates retrieval cache and forces re-run. Loud failure preferred over silent drift.

## Artifacts / Output

New files (all git-tracked unless noted):

- `specs/v15-helpful-pages-universe.md` (this file)
- `specs/v15-judge-prompt-v1.md` (judge prompt artifact, separately versioned; model-agnostic)
- `tools/build_reference_corpus.py`
- `tools/judge_helpful_pages.py` (dual-model: Haiku + gpt-4o-mini, sequential per-URL)
- `tools/intersection_set.py`
- `bench/reference_corpora/<site>/urls.txt` × 11
- `bench/reference_corpora/<site>/source.json` × 11
- `bench/helpful_pages/<site>.json` × 11 (dual-model schema per SC-2)
- `bench/helpful_pages_disagreement.csv` (per-URL inter-model disagreement rows + both rationales)
- `bench/calibration_ground_truth_v15.csv` (400 hand-judged pages — 100 × 4 calibration sites)
- `bench/calibration_audit_v15.csv` (BOTH judges' results vs ground truth + multi-call agreement per model)
- `bench/sanity_check_v15.md` (per-site sanity check log, canonical model)
- `bench/universe_manifest.json` (includes `judge_models` + `inter_model_agreement` + `v15x_can_drop_to_single_cheap`)
- `queries/v15_queries.json`
- `queries/v15_rejected.json`
- `queries/v15_intersection_queries.json`
- `reports/RETRIEVAL_INTERSECTION.md` (new)
- `reports/COVERAGE_PER_SITE.md` (new)
- `reports/methodology_validation.md` (new — dual-judge cross-check, disagreement analysis, SC-14 decision)
- `docs/V15_RELEASE_NOTES.md`

Modified files:
- `tools/generate_queries.py` (DS-3: sample from helpful-pages)
- `benchmark_retrieval.py` (DS-4: three-metric decomposition; DS-5 intersection queries support)
- `reports/METHODOLOGY.md` (DS-8: helpful-pages section + anti-gaming additions + per-site limitations + multi-trial roadmap)
- `reports/RETRIEVAL_COMPARISON.md` (DS-4: schema update)
- `Makefile` (`benchmark` target dependencies update)
- `lint_reports.py` (validate new reports against style guide)
- `self_improvement/check_invariants.py` (add v1.5 invariants: universe_manifest exists, helpful-pages corpora exist, etc.)

## Risk Assessment

- **R1 (high → med):** Helpful-pages judge has systematic bias that we don't catch in calibration. Mitigation: 4-site calibration covers content-shape diversity; per-site sanity check on 10/10 lowest/highest confidence; flagged-site review process; prompt versioned for diff-reviewable iteration. **DUAL-MODEL JUDGING REDUCES THIS RISK:** systematic single-model bias is detected as inter-model disagreement and surfaced in `bench/helpful_pages_disagreement.csv` + `reports/methodology_validation.md`. Risk drops from high to medium because the cross-model check catches single-model bias that single-judge calibration would miss.
- **R2 (med):** Sitemap+union-of-tools universe still under-covers some sites. Mitigation: honest per-site limitations disclosure; not claimed as "all substantive content."
- **R3 (med):** Intersection pool-level N too small for useful CI bounds. Mitigation: warn at N<80; if persistent, relax to ≥6-of-7 in v1.5.1 (don't relax for v1.5 publication).
- **R4 (low):** Re-fetching sitemaps in future cycles produces incomparable universes. Mitigation: git-tracked corpora + manifest's `sitemap_fetch_date` make universe diffs auditable.
- **R5 (low):** Calibration + full-pool cost overruns ($30 budget). Mitigation: 10-page validation FIRST action of DS-2; cap at $50 hard escalation; if blown, investigate prompt/cache before approving. Dual-model adds ~$5 marginal expected.
- **R6 (low — new, dual-model):** gpt-4o-mini snapshot is deprecated or rate-limited at universe-build time. Mitigation: model resolver picks current GA snapshot at build time; if unavailable, DS-2 falls back to Haiku-only and SC-14 records `blocked — gpt-4o-mini snapshot unavailable`. Sequential per-URL judging keeps rate-limit accounting simple per provider.
- **R7 (low — new, dual-model):** Calibration fails on one model but passes on the other (asymmetric failure). Mitigation: canonical defaults to passing model; SC-14 records `blocked — <failed-model> failed calibration`; v1.5.x cycles continue with the passing model only; no methodology degradation vs single-judge baseline.

## Resolved decisions (Q1-Q5, resolved 2026-05-11 in chat.md round-trip)

Audit trail preserved here so a future reader can see the deliberation that shaped the spec body above.

1. **Calibration site selection — RESOLVED.** Four sites: `huggingface-transformers` (docs), `newegg` (ecommerce), `propublica` (blog), `rust-book` (small-corpus check). Rust-book added on markcrawl-agent's suggestion to surface the edge case where helpful ratio is naturally high simply because the site is content-dense. Cost increment ~$0.075. Baked into DS-2 + SC-3.
2. **Haiku model lock — RESOLVED.** Pin to `claude-haiku-4-5-20251001` for v1.5. Drift assertion at universe-build time mirrors v1.4 `models_manifest.json` defense-in-depth.
3. **Per-page cost validation — RESOLVED.** 10-page sanity check is the FIRST action of DS-2 (after ground-truth hand-judging, before calibration run). $0.0025 spend. If projection >$36 (>20% over $30 cap), escalate to chat.md before proceeding. Baked into DS-2.
4. **Sitemap URL cap — RESOLVED.** Random-sample-with-fixed-seed at 10000. Manifest field `sitemap_url_sample_seed: <int>` records the seed. Symmetric across sites; cost-bounded; deterministic across rebuilds. Per-site limitations note required for any sampled site. Baked into DS-1 + DS-7 manifest schema.
5. **Universe rebuild cadence — RESOLVED.** Reuse by default. Concrete rebuild triggers: (a) any site's sitemap returns >20% URL delta vs the recorded list, (b) v1.5.x version adds/removes a site, (c) judge prompt version bumps. Baked into DS-8 (METHODOLOGY.md update).

## Amendment changelog

### Amended 2026-05-12: dual-model judging extension (markcrawl-agent chat.md proposal accepted by bench-agent)

**Source:** markcrawl-agent chat.md proposal at `2026-05-12T19:30:00Z`, accepted by bench-agent at `2026-05-12T20:00:00Z` (this commit) with three refinements (R-A per-class agreement floor, R-B practical implementation notes, R-C gpt-4o-mini snapshot resolver).

**Background.** paulsave directive (relayed via markcrawl-agent): prove or refute that future v1.5.x cycles can run gpt-4o-mini-only without methodology degradation. The dual-judge in v1.5.0 is the validation experiment that determines whether v1.5.1+ can drop to a single cheaper judge.

**Changes made in this amendment:**

1. **DS-2 extended from single-judge (Haiku) to dual-model (Haiku + gpt-4o-mini).** Both models receive the same model-agnostic prompt at `specs/v15-judge-prompt-v1.md`. Sequential per-URL (not parallel across models) to keep rate-limit accounting simple per provider. gpt-4o-mini snapshot resolved at universe-build time; if unavailable, falls back to Haiku-only and SC-14 records `blocked — gpt-4o-mini snapshot unavailable`.

2. **SC-2 schema extended** to dual-model: each `bench/helpful_pages/<site>.json` entry stores both models' outputs, the canonical pick, the agreement boolean, both model versions, and the prompt version. New artifact `bench/helpful_pages_disagreement.csv` for disagreement-row analysis.

3. **SC-3 calibration extended:** each model is independently calibrated against the same 400 hand-judged pages. Both must independently meet THREE thresholds (added per-class agreement ≥85% to prevent class-imbalance hiding miscalibration): per-site ≥90% / multi-call <5% / per-class ≥85%. Canonical = higher overall agreement on calibration set; tiebreak → Haiku.

4. **SC-8 manifest schema extended** with `judge_models` (versions + canonical choice + rationale + per-model calibration scores) and `inter_model_agreement` (overall + per-site + per-class min + SC-14 boolean).

5. **SC-14 added (gpt-4o-mini viability criterion):** three-row decision rule (≥95%/≥90%/≥85% per-class → drop OK; ≥85%/≥75%/≥80% → targeted dual-judge; below → keep dual). Result + rationale published in `reports/methodology_validation.md`. Per-class floor matches SC-3.

6. **DS-7 manifest example** updated with `judge_models` + `inter_model_agreement` + per-site `helpful_pages_count_haiku` / `helpful_pages_count_gpt4omini` fields.

7. **DS-8 anti-gaming table** extended with single-judge-bias defense (dual-model cross-check) + dual-judge methodology section.

8. **Artifacts list** extended with `bench/helpful_pages_disagreement.csv` + `reports/methodology_validation.md`.

9. **Risk Assessment:** R1 dropped from high → med (dual-model catches single-model bias). New R6 (gpt-4o-mini snapshot availability) and R7 (asymmetric calibration failure) added as low-risk with mitigations.

**Cost impact:** Budget cap remains $30 (unchanged). Expected full-pool spend rises from ~$15 (Haiku-only) to ~$20 (dual-model). Hard escalation threshold remains $50.

**bench-agent's three refinements** to the markcrawl-agent proposal:

- **R-A — Per-class agreement floor (≥85% on each binary class).** Class imbalance can hide miscalibration (e.g., 80% helpful → 80% raw agreement baseline). Added to SC-3, SC-14, and the manifest schema.
- **R-B — Practical implementation notes.** Sequential per-URL judging (no parallel-across-models complexity); OpenAI key dependency note (already required for queries + embeddings, so not a new external dep at v1.5.0 level); asymmetric-failure handling rule (canonical defaults to passing model; SC-14 marks blocked); both calibrations must pass independently.
- **R-C — gpt-4o-mini snapshot resolver.** `gpt-4o-mini-2024-07-18` may be deprecated by 2026-05-12; resolver picks current GA at universe-build time; falls back gracefully if no `gpt-4o-mini-*` GA model available.

**No counter proposed.** Amendment accepted as a strict improvement on the locked spec — methodology becomes empirically defensible (defends "why this judge?" reviewer attack) and produces forward-looking decision data for v1.5.x cost optimization at trivial marginal spend ($5).
