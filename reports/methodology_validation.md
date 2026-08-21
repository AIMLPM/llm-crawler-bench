# Methodology validation — v1.5

> Populated by `tools/judge_helpful_pages.py --calibration` and `--merge`.
> Manual narrative sections noted below.

## 1. Dual-judge calibration (SC-3)

_Populated after `--calibration`. See `bench/sanity_check_v15.md` for the
machine-readable summary and `bench/calibration_audit_v15.csv` for the
per-row record._

- Prompt version: <fill>
- Iterations used: <fill> / 3
- Canonical pick rationale: <fill>

## 2. Full-pool helpful-pages distribution

_Populated after `--merge`. Per-site helpful / non-helpful / skipped
breakdown lives in `bench/universe_manifest.json` and the per-site files
under `bench/helpful_pages/`._

| site | helpful | non_helpful | skipped |
|------|--------:|------------:|--------:|

## 3. Cross-model disagreement analysis

_Populated after `--merge`. See `bench/helpful_pages_disagreement.csv`
for per-URL rows; this section interprets the systematic disagreement
modes._

- Total disagreement rows: <fill>
- Disagreement rate (% of dual-judged): <fill>
- Top failure mode by content shape: <fill>

## 4. Confidence proxy (SC-4 R-A)

_Populated after `--sanity-confidence`. See `bench/confidence_sample_v15.csv`._

- 20 URLs/site × 11 sites = 220 URLs, two canonical-model calls each
- Disagreement rate: <fill>
- Per-site disagreement breakdown: <fill>

## 5. Reproducibility manifest

_Populated automatically by --merge._

- Universe size: <fill> URLs across 11 sites
- Sitemap sample seed: 42
- Calibration sample seed: 1337
- Sanity-check seed: 17
- Confidence-proxy seed: 7919
- Haiku model: <fill>
- gpt-4o-mini snapshot: <fill>
- Prompt sha256: <fill>
- Universe-build git commit: <fill>

## 6. Hostile-reviewer Q&A defenses

_Manual section — author writes after seeing the calibration + disagreement
results._

- Q: Why this judge model? A: <fill>
- Q: How do we know the prompt isn't sneaking a bias in? A: <fill>
- Q: What if a future GA snapshot rolls forward and changes things? A: <fill>
