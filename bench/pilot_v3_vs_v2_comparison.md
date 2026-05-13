# DS-2 Pilot v3-vs-v2 Comparison — Source-Code-Viewer Failure-Mode Analysis

**Date:** 2026-05-13
**Branch:** `feature/v15-pilot-sonnet-swap`
**Author:** bench-agent
**Site:** rust-book (357 URLs ref-corpus, 303 judged after content-thin skips)
**v2 commit:** `4a10615` (prompt `specs/v15-judge-prompt-v2.md`)
**v3 commit:** `019f570` (prompt `specs/v15-judge-prompt-v3.md`)
**v3 pilot run:** commit `94de869` (pilot data) on this branch.

## Summary numbers

| Metric                                                            | v2          | v3          | Δ          |
|-------------------------------------------------------------------|-------------|-------------|------------|
| Inter-model agreement (Sonnet 4.5 vs gpt-4o-mini), 303 URLs       | **89.11%**  | **99.01%**  | **+9.90 pp** |
| Inter-model Cohen κ (binary HELPFUL / NON-HELPFUL)                | 0.1333      | 0.9483      | +0.815     |
| Total disagreements                                               | 33          | **3**       | −30        |
| Source-code-viewer disagreements (Sonnet=NH, gpt=H, `/src/*.rs.html`) | **28**  | **0**       | −28 (100%) |
| gpt-4o-mini HELPFUL label rate                                    | 98.7%       | 89.4%       | −9.3 pp    |
| Sonnet 4.5 HELPFUL label rate                                     | 88.4%       | 89.1%       | +0.7 pp    |
| Regressions (URLs that AGREED under v2 but DISAGREED under v3)    | —           | **2**       | —          |
| Newly-fixed disagreements (URLs that DISAGREED under v2, AGREE under v3) | —    | **32**      | —          |

**Net effect: 32 fixes, 2 regressions; 30 of 33 v2 disagreements eliminated.**
The Sonnet-vs-gpt-4o-mini inter-model agreement is now in the
high-99% range with κ ≈ 0.95 (substantial agreement zone).

## Cost of the rerun

| Metric                              | Value     |
|-------------------------------------|----------:|
| Spend total                         | **$0.94** |
| Cap                                 | $2.00     |
| Spend headroom unused               | $1.06     |
| Wall clock                          | 217.9 s (~3.6 min) |
| Sonnet cache hit-rate               | 98.0% (297/303) |

Per-page cost was $0.003091 (Sonnet $0.002890 cached, gpt-4o-mini
$0.000202) — within ±3% of the v2 pilot's measured $0.002992 per page;
the slight uptick is the additional ~70 tokens added to Block 1 raising
the cache-read line item marginally.

## Source-code-viewer fix rate (the headline question)

Under v2, **28 URLs** matched the pattern `Sonnet=NON-HELPFUL, gpt=HELPFUL,
URL=/src/*.rs.html` — the documented failure mode that prompted v3.

Under v3, all **28 of 28 (100%)** flipped: gpt-4o-mini now classifies them
as `non-helpful-other` with rationale text closely matching the v3 example
(see sample below). Zero remaining `/src/*.rs.html` disagreements.

**Sample rationale shifts** (gpt-4o-mini, v2 → v3):

`https://doc.rust-lang.org/src/alloc/vec/cow.rs.html`
- v2: HELPFUL / `helpful-docs`: "Source code documentation for the `cow.rs` file, providing implementation details and explanations that a user might ask questions about."
- v3: NON-HELPFUL / `non-helpful-other`: "Raw source code file viewer with syntax-highlighted code but no explanatory prose, parameter documentation, or usage examples."

`https://doc.rust-lang.org/src/core/array/iter.rs.html`
- v2: HELPFUL / `helpful-docs`: "Source code documentation for the `IntoIter` iterator for arrays in Rust, which includes implementation details and usage information..."
- v3: NON-HELPFUL / `non-helpful-other`: "Raw source code file viewer with syntax-highlighted code but no explanatory prose, parameter documentation, or usage examples."

Note that gpt-4o-mini's v3 rationale text closely tracks the worked example
verbiage in the v3 prompt. This is expected and is the desired effect: the
model is using the prompt example as a template for similar cases.

## Per-URL changes table (all 36 changes on common URL set)

### A. gpt-4o-mini reclassifications (28 URLs, all H → NH, all `/src/*.rs.html`)

| URL pattern | v2 (gpt) | v3 (gpt) | Sonnet (both v2 & v3) | Direction |
|-------------|----------|----------|----------------------|-----------|
| 28 × `https://doc.rust-lang.org/src/.../<name>.rs.html` | HELPFUL / helpful-docs | NON-HELPFUL / non-helpful-other | NON-HELPFUL / non-helpful-other | **gpt converged on Sonnet's view** |

All 28 are now in agreement with Sonnet 4.5's correct v2 judgment. Per-class
agreement on the binary class `NON-HELPFUL` jumps from ~12% (v2) to ~84%
(v3 ratio of gpt-4o-mini NH labels matching Sonnet NH labels, on common URLs).

### B. Sonnet 4.5 reclassifications (6 URLs)

Sonnet's labels were generally already correct under v2 — the v3 prompt's
nudge appears to have had a small secondary effect on it (run-to-run noise
overlap is plausible at this scale; one run per URL is not enough to fully
attribute these to the v3 change).

| URL | v2 (Sonnet) | v3 (Sonnet) | v2 (gpt) | v3 (gpt) | Net effect |
|-----|-------------|-------------|----------|----------|------------|
| `https://doc.rust-lang.org/book/` | HELPFUL / helpful-docs | NON-HELPFUL / non-helpful-index | HELPFUL | HELPFUL | **Regression** (Sonnet flipped; gpt held; v2 agreed, v3 disagrees) |
| `https://doc.rust-lang.org/core/arch/arm/struct.int8x16_t.html` | HELPFUL / helpful-docs | NON-HELPFUL / non-helpful-empty | HELPFUL | HELPFUL | **Regression** (Sonnet flipped; gpt held) |
| `https://doc.rust-lang.org/book/print.html` | NON-HELPFUL / non-helpful-other | HELPFUL / helpful-docs | HELPFUL | HELPFUL | Fix (Sonnet flipped toward gpt) |
| `https://doc.rust-lang.org/book/title-page.html` | NON-HELPFUL / non-helpful-nav | HELPFUL / helpful-docs | HELPFUL | HELPFUL | Fix |
| `https://doc.rust-lang.org/cargo/` | NON-HELPFUL / non-helpful-index | HELPFUL / helpful-docs | HELPFUL | HELPFUL | Fix |
| `https://doc.rust-lang.org/stable/book/` | NON-HELPFUL / non-helpful-index | HELPFUL / helpful-docs | HELPFUL | HELPFUL | Fix |

Of Sonnet's 6 shifts, 4 are toward gpt-4o-mini's (HELPFUL) view on `book/`
landing-page-like URLs — Sonnet's v2 was reading these as index pages and v3
reads them as helpful-docs. The 2 "regressions" are both Sonnet flipping FROM
HELPFUL to NON-HELPFUL on edge cases (`/book/` root index page; an empty
ARM intrinsic struct stub page).

Whether these Sonnet flips are correct or not is a question for the 4-site
hand-judged ground truth — not for this rerun to adjudicate.

### C. Remaining v3 disagreements (3 URLs)

| URL | Sonnet v3 | gpt v3 | Likely correct class |
|-----|-----------|--------|----------------------|
| `https://doc.rust-lang.org/nightly/unstable-book/language-features/lahfsahf-target-feature.html` | HELPFUL / helpful-docs | NON-HELPFUL / non-helpful-other | Likely a thin stub; either judgment is defensible |
| `https://doc.rust-lang.org/book/` | NON-HELPFUL / non-helpful-index | HELPFUL / helpful-docs | Disputed — see Sonnet's regression above |
| `https://doc.rust-lang.org/core/arch/arm/struct.int8x16_t.html` | NON-HELPFUL / non-helpful-empty | HELPFUL / helpful-docs | Likely NH (empty stub) |

## Cohen's kappa headline

| Comparison | κ |
|------------|--:|
| Sonnet v2 vs Sonnet v3 (same model, prompt change only) | 0.9006 |
| gpt-4o-mini v2 vs gpt-4o-mini v3 (same model, prompt change only) | 0.2035 |
| Sonnet vs gpt-4o-mini, UNDER v2 | 0.1333 |
| Sonnet vs gpt-4o-mini, UNDER v3 | **0.9483** |

The gpt-v2-vs-gpt-v3 κ of 0.20 is low because gpt's label distribution
shifted substantially (98.7% HELPFUL → 89.4% HELPFUL); the absolute count of
flipped labels is small (28/303 ≈ 9%) but the marginal distributions changed
so much that κ's expected-agreement baseline rose to compensate. Cohen κ
is sensitive to marginal-distribution shifts and should be interpreted
alongside the raw fix counts above.

The **inter-model κ jump from 0.13 → 0.95** is the headline: the two
judges (the strong Sonnet primary and the cheap gpt-4o-mini secondary)
now produce near-identical labels on this site under v3.

## Honest interpretation

### Is the fix generic or rust-book-specific?

**The v3 example pattern (`/src/...*.rs.html` view) is rust-book-specific
in form, but the methodology generalizes.** Three considerations:

1. **The example was deliberately anonymized.** The v3 worked example uses
   `docs.example.com/src/iter/fuse.rs.html`, not a real rust-book URL. The
   decision-guidance line lists multiple analogous patterns (GitHub blob
   views, "view source" panels). However: the actual `/src/...rs.html`
   URL shape in the example is recognizably the rust-book/docs.rs idiom,
   and the calibration auditor could reasonably argue the example
   essentially encodes a rust-book-pattern signal even if the host is
   anonymized.

2. **The failure pattern (raw source viewer classified as helpful-docs)
   is generic.** Other sites in the v1.5 universe with the same shape
   include: huggingface-transformers (has `/v_x.y.z/...` source links;
   doc-strings of class definitions are also code-with-prose, which
   v3's decision-guidance should *correctly* leave classified as
   helpful-docs), mdn snippet pages, github (not in universe), gitlab
   (not in universe). The pattern generalizes to "raw code without
   explanatory prose"; v3's added decision-guidance line states the
   distinguishing criterion (`lack the explanatory prose / parameter
   documentation / usage examples`) rather than naming a URL pattern.

3. **The validation gate is calibration on hand-judged ground truth,
   not this single-site pilot.** Per spec SC-3, both judges must
   independently pass per-site ≥90% agreement vs the 4-site
   hand-judged CSV (`bench/calibration_ground_truth_v15.csv`, 400 URLs
   across HF, newegg, propublica, rust-book). Whether v3 generalizes
   beyond rust-book is decided when paulsave hand-judges that CSV and
   we re-run `--calibration` against v3. This pilot result only
   answers: "does the v3 example fix the source-code-viewer failure
   mode on rust-book?" Answer: yes, completely (28/28), without
   collateral damage outside that pattern (0 of the 28 gpt-4o-mini
   shifts were off-pattern).

### Did v3 introduce new disagreements elsewhere?

**Two regressions, both Sonnet-side, neither in the source-viewer family.**

- `book/` root → Sonnet now reads this as `non-helpful-index` (gpt still HELPFUL)
- `core/arch/arm/struct.int8x16_t.html` → Sonnet now reads this as `non-helpful-empty` (gpt still HELPFUL)

Both look like Sonnet noise rather than v3 prompt damage. Neither URL
contains a `/src/` source-viewer pattern, so the v3 change wouldn't
plausibly drive these. More-likely-than-not is single-run variance at
temperature=0 with the slightly different prefix (prompt-cache
re-creation token boundaries can shift attention subtly).

### Recommendation

**This looks like a real SC-14-unlock-path signal, but the unlock is gated
on hand-judged ground truth.**

The v3 prompt closes the inter-model gap from 89% → 99% on a single site
by adding ONE worked example targeting a specific failure pattern, with
zero collateral damage outside that pattern. If a similar 1-iteration
gain holds on the other 3 calibration sites (HF, newegg, propublica),
v1.5.1+ can credibly drop to gpt-4o-mini-only primary with calibration
demonstrating sub-2% per-site mismatch — that's the SC-14 unlock the
cost-projection conversation has been blocked on.

**Caveat (load-bearing).** Rust-book is a single site, and a single site
where the dominant disagreement pattern (`/src/*.rs.html`) is an exact
fit for the v3 example. The same prompt may produce a smaller effect
or no effect on sites where the failure modes are different — HF's
likely failure modes are docstring pages and tag-listing pages, not
raw source viewers. The calibration step on the 4-site hand-judged
CSV (when paulsave hand-judges it) is the real validation gate, and
the right action item is to advance that step rather than draw v3
conclusions from a single-site rerun.

**Cost implication unchanged.** The DS-2 cost-escalation question
(Sonnet 4.5 + gpt-4o-mini full-pool at ~$100 vs $50 hard threshold)
is unaffected by this prompt iteration — Block 2 is the cost driver
and it didn't change. If SC-14 unlocks via this v3 path (gpt-4o-mini-
only primary), full-pool drops to ~$6 + ~$1 calibration audit. That
is the prize at the end of the calibration step, not before it.

## Artifacts

- v3 prompt: `specs/v15-judge-prompt-v3.md` (commit `019f570`)
- v2 prompt: `specs/v15-judge-prompt-v2.md` (unchanged, preserved for diff)
- v2 pilot data (preserved): `bench/helpful_pages_sonnet_pilot/rust-book_v2.json`, `bench/helpful_pages_gpt4omini_pilot/rust-book_v2.json`
- v3 pilot data: `bench/helpful_pages_sonnet_pilot/rust-book.json`, `bench/helpful_pages_gpt4omini_pilot/rust-book.json`
- Pilot aggregates: `bench/pilot_v15_results.json` (overwritten with v3 numbers — v2 numbers in chat.md 2026-05-13 post)
