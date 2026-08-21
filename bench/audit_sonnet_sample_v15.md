# v1.5 DS-2 — Sonnet audit of the gpt-4o-mini universe

- **Date**: 2026-08-20T05:16:31.432865+00:00
- **Auditor**: `claude-sonnet-4-5-20250929` re-judging `gpt-4o-mini-2024-07-18`
- **Sample**: 966 unbiased + 34 targeted (seed 42)
- **Spend**: **$2.3748**

## Stratum A — unbiased estimate (headline)

- Agreement with mini: **73.71%** (894 comparable rows)
- **Over-inclusion** (mini HELPFUL, Sonnet NON-HELPFUL): **30.59%** (234/765)
- Under-inclusion (mini NON-HELPFUL, Sonnet HELPFUL): 0.78% (1/129)

| Site | n | Agreement | Over-inclusion |
|---|---|---|---|
| ikea | 20 | 75.0% | 26.32% |
| kubernetes-docs | 161 | 55.28% | 61.74% |
| mdn-css | 151 | 62.91% | 67.47% |
| newegg | 6 | 66.67% | 40.0% |
| postgres-docs | 140 | 92.14% | 8.03% |
| propublica | 142 | 86.62% | 13.57% |
| pytorch-docs | 109 | 59.63% | 40.74% |
| react-dev | 8 | 100.0% | 0.0% |
| rust-book | 11 | 81.82% | 20.0% |
| smittenkitchen | 30 | 100.0% | 0.0% |
| stripe-docs | 116 | 79.31% | 21.43% |

## Stratum B — targeted worst case (NOT part of the estimate)

Patterns: `/_modules/`, `/_sources/`, `/src/`, `/genindex`, `/py-modindex`, `/modindex`, `/search` — rubric-NON-HELPFUL shapes mini is known to pass.

- Over-inclusion on these patterns: **None%** (0/0)
- Agreement: None% of 0 comparable rows

## How to read this

Stratum A bounds how much the published helpful-pages universe is inflated by
the cheap judge. Inflation applies to every crawler equally (the universe is the
denominator for Coverage-of-Helpful), so leaderboard ORDERING is unaffected;
absolute coverage percentages carry this as a known bias. Stratum B is the
worst case on the specific shapes mini mishandles, reported separately so it
cannot inflate the headline number.

