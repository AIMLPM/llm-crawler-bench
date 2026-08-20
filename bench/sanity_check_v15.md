# v1.5 DS-2 Calibration Audit

- **Date**: 2026-08-17T09:08:40.503264+00:00
- **Prompt**: `specs/v15-judge-prompt-v5.md` (sha256: ca1be4c3232b4e3a...)
- **Haiku model**: `claude-sonnet-4-5-20250929`
- **gpt-4o-mini snapshot**: `gpt-4o-mini-2024-07-18`
- **Ground-truth rows used**: 300 / 373 filled
- **Deterministic pre-classifier**: fired on 10 rows (facet/mirror/thin); SC-3 computed on the combined system (prefilter + LLM judge), matching --full-pool composition

## Haiku results

- Multi-call self-disagreement: **0.00%** (gate: <5%)
- Cohen's kappa: **0.6097**
- Per-class agreement (majority vote): HELPFUL=**92.86%**, NON-HELPFUL=**95.0%** (gate: ≥85%)
- Per-site ground-truth agreement (gate: ≥90% each):
  - newegg: **93.00%**
  - propublica: **91.00%**
  - rust-book: **95.00%**
- **All Haiku gates pass: True**

## gpt-4o-mini results

- Multi-call self-disagreement: **0.00%** (gate: <5%)
- Cohen's kappa: **0.7273**
- Per-class agreement: HELPFUL=**99.29%**, NON-HELPFUL=**65.0%** (gate: ≥85%)
- Per-site ground-truth agreement (gate: ≥90% each):
  - newegg: **97.00%**
  - propublica: **99.00%**
  - rust-book: **95.00%**
- **All gpt-4o-mini gates pass: False**

## Canonical model pick

Pick rule: higher per-site ground-truth agreement (Haiku tiebreak default).
- Haiku avg per-site agreement: **93.00%**
- gpt-4o-mini avg per-site agreement: **97.00%**
- **Canonical**: `gpt4omini`

## API spend (exact, from provider usage fields)

- Sonnet: **$2.8242** over 870 calls (in 589,362 / out 34,582 / cache-write 2,032 / cache-read 1,765,808 tok)
- gpt-4o-mini: **$0.2236** over 870 calls (in 2,103,456 / out 28,406 / cached-in 1,453,184 tok)
- **Total: $3.0478**

## Next step

- One or more SC-3 gates failed. Iterate the prompt to v3 (sharpen failure-mode language, add an example for the offending class), then re-run `--calibration`.
- Spec allows up to 3 prompt iterations (per `specs/v15-judge-prompt-v1.md`). After 3 failed iterations, escalate to chat.md.
