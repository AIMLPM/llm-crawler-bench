# v1.4 Release Notes — methodology hardening for HN credibility

<!-- DS-14 deliverable. Skeleton landed pre-Gate-4; numbers backfilled
after DS-8 retrieval + answer-quality re-run completes. -->

## Headline

_Backfill from DS-8 leaderboard diff after Gate 4 lands. Per the spec's
SC-9, this section MUST lead with markcrawl's per-dimension deltas
v1.3 → v1.4 — including any negative ones — before the supporting
methodology changes._

## What changed since v1.3

The v1.4 cycle is methodology hardening for hostile-reviewer credibility.
Five concrete additions, three internal cleanups, one query-set rebuild.

### Five concrete additions

- **Page-level MRR (DS-1)** — collapse all chunks-per-URL to a single
  rank using DS-2 normalized URLs as the dedup key. Removes the
  chunk-density gaming signal where a tool emitting more chunks per
  page would otherwise outrank a tool emitting fewer chunks for the
  same canonical content.
- **URL normalization for matching (DS-2)** — strip locale subdomain
  prefixes (he., de., ar., zh-cn., en-us., …), drop UTM/lang/locale/
  random query params, drop the fragment, lowercase host + path
  before substring-matching. Eliminates v1.3 false positives where
  a query term inside `?ref=<term>` or fragment text counted as a hit.
- **QUERY_AUDIT.csv (DS-3)** — every (query × tool × top-5-rank) chunk
  emitted with its cosine score, raw URL, normalized URL, is_hit flag,
  and `page_rank_after_collapse`. Reviewers can spot-check any number
  without re-running the benchmark.
- **LLM-generated, LLM-verified query set (DS-6)** — replaces v1.3's
  hand-written queries (the conflict-of-interest the cycle is fixing).
  gpt-4o-mini drafts 1-2 questions per sampled URL; a separate
  gpt-4o-mini API invocation with no shared context window verifies
  each draft. No human in the acceptance loop. Final set: 591 queries
  across 11 sites at 97% verifier first-pass.
- **Cost calculator with sensitivity sweep (DS-11)** — `tools/cost_calculator.py`
  with adjustable pricing inputs and a ±50% sweep across each input
  reporting whether the per-tool ranking shifts. Default-pricing
  ranking is robust to ±50% on every individual input.

### Three internal cleanups

- **DS-13b checkpoint key fix** — retrieval_checkpoints filename now
  includes the embedder slug. Prevents the silent stale-cache failure
  where a re-run with a different EMBEDDING_MODEL would emit reports
  byte-identical to the prior embedder's run.
- **Self-healing page-MRR recompute on checkpoint load** — closes the
  staleness window between methodology fixes and re-rendered reports
  (`--report-only` always reflects current code rather than what was
  cached at smoke time).
- **Author + single-trial caveat disclosure (DS-4)** — METHODOLOGY.md
  gains "Author and conflict-of-interest disclosure" + "Single-trial
  measurement" sections. Every comparative report banner links back.

### One query-set rebuild

- v1.3 had 104 hand-written queries (8-20 per site) authored by the
  maintainer of one of the compared tools (markcrawl). The conflict
  of interest is real — even with good intent, the v1.3 set fails
  the "resistant to motivated reasoning" bar.
- v1.4 has 591 LLM-generated, LLM-verified queries (typically ~50-60
  per site) with no human author in the acceptance loop. Generation
  runs against pre-processed page content (chrome-stripped, capped at
  24K chars). Verifier rationale uses two distinct prefixes
  (`answer-not-in-page` for normal rejection, `page-broken` for
  sampler issues — zero of the latter in the canonical set).

## v1.4 query set is English-only by sampler design

**The framing paragraph the user wrote, preserved verbatim for the
methodology section** — kept here so DS-14's polishing doesn't lose
the key insight:

> v1.4 query set is English-only by sampler design — URLs from
> locale-prefixed subdomains (e.g., `ko.react.dev`, `ar.react.dev`)
> are filtered before sampling. This preserves apples-to-apples
> comparability with v1.3's English-only set and avoids a per-tool
> fairness confound (tools that crawl locale mirrors would have
> asymmetric advantage on multilingual queries). Multilingual RAG
> evaluation is deferred to v1.5 as an explicit, opt-in evaluation
> dimension.

The discovery story (worth keeping in the writeup): Gate 3b iteration 2
produced 19 multilingual queries from `react-dev` locale mirrors
(ar./fr./id./ko.). System handled them correctly — text-embedding-3-small
is multilingual, DS-2 normalizes the locale prefixes, the matcher would
hit. But pre-publication review caught that this introduces an
asymmetric advantage: tools that crawl locale mirrors (broad-scope) get
a query set their corpus matches; tools that don't (narrow-scope, like
markcrawl with scope detection) only have English content. That's a
per-tool fairness confound, not a per-site methodology preference. The
filter caught it before publication.

This is the right kind of finding to lead the release notes with: not
"we dropped 19 queries" but "we caught a fairness confound pre-publication."

## Per-dimension deltas v1.3 → v1.4

_Backfill from DS-8 + retrieval re-run output once Gate 4 completes.
Format: per tool, table of (chunk-MRR, page-MRR, Hit@1/3/5/10, answer
quality, content signal, cost). Lead with markcrawl row, including
negative deltas. SC-9 requirement._

| Tool | v1.3 chunk-MRR | v1.4 chunk-MRR | Δ | v1.4 page-MRR | v1.3 answer-quality | v1.4 answer-quality | Δ |
|---|---|---|---|---|---|---|---|
| markcrawl | 0.488 | TBD | TBD | TBD | 4.03 | TBD | TBD |
| crawlee | 0.686 | TBD | TBD | TBD | 4.31 | TBD | TBD |
| ... | | | | | | | |

## Methodology footnotes worth pre-empting

- **"You changed the query set; the v1.3→v1.4 numbers aren't
  comparable."** Correct. The v1.3 set had a structural COI. The v1.4
  set fixes it. The release notes lead with this delta rather than
  buries it. Anyone wanting strict v1.3 comparability can run the
  v1.3 query set against the new code (`queries/v13_queries.json` is
  preserved in the repo for exactly this).
- **"Why gpt-4o-mini for both generation and verification?"** Same-model
  design is simpler and more defensible than two-model. A two-model
  setup measures "do two LLMs agree about answerability," which
  introduces a confound between methodology and model-choice.
  gpt-4o-mini's verifier produces strict, distinguishable rationales
  (answer-not-in-page vs page-broken).
- **"How do you know the queries don't favor markcrawl?"** Three
  defenses: (1) the LLM that generated them has no stake in markcrawl
  winning; (2) the verifier is a separate API call with no shared
  context window — structural separation at the API boundary, not
  prompt boundary; (3) `queries/v14_queries.json` and
  `queries/v14_rejected.json` are committed to the repo so reviewers
  can audit any specific query.
- **"Why is page-MRR uplift so small (single-digit-percent)?"** Two
  effects compose: page-collapse uplift (chunks-per-canonical-page
  collapse to one slot) PARTIALLY OFFSET BY v1.3 false-positive removal
  (chunks that matched via stripped fragment-text or `?ref=` query-text
  no longer count). A tool whose page-MRR drops slightly is one whose
  v1.3 chunk-MRR was inflated by exactly the false positives DS-2
  now removes. See METHODOLOGY anti-gaming section.

## What v1.4 deliberately does NOT do

- Multi-trial measurement (deferred to v1.5 — single-trial constraint
  imposed by current hardware).
- LLM-judge for retrieval ground truth (deferred to v1.5 — substring
  matching is fundamentally fuzzy; LLM judge is the v1.5 escape hatch).
- Multilingual evaluation (deferred to v1.5 as an opt-in dimension —
  v1.4 is English-only by sampler design).
- BEIR integration (deferred to v1.5).

## How to reproduce

```bash
make benchmark-quick   # ~5 min, single site, ~$0 spend — verifies pipeline runs
make benchmark         # ~24h, all 11 sites, full pipeline, ~$5 spend
```

See `reports/METHODOLOGY.md` "Reproducibility" section.
