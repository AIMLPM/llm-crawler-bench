# v1.5 DS-2 Calibration Audit

- **Date**: 2026-08-17T08:12:06.065396+00:00
- **Prompt**: `specs/v15-judge-prompt-v4.md` (sha256: d15c3712f375035b...)
- **Haiku model**: `claude-sonnet-4-5-20250929`
- **gpt-4o-mini snapshot**: `gpt-4o-mini-2024-07-18`
- **Ground-truth rows used**: 300 / 373 filled

## Haiku results

- Multi-call self-disagreement: **0.00%** (gate: <5%)
- Cohen's kappa: **0.5392**
- Per-class agreement (majority vote): HELPFUL=**96.43%**, NON-HELPFUL=**60.0%** (gate: ≥85%)
- Per-site ground-truth agreement (gate: ≥90% each):
  - newegg: **95.00%**
  - propublica: **92.00%**
  - rust-book: **95.00%**
- **All Haiku gates pass: False**

## gpt-4o-mini results

- Multi-call self-disagreement: **0.00%** (gate: <5%)
- Cohen's kappa: **0.1477**
- Per-class agreement: HELPFUL=**99.29%**, NON-HELPFUL=**10.0%** (gate: ≥85%)
- Per-site ground-truth agreement (gate: ≥90% each):
  - newegg: **91.00%**
  - propublica: **94.00%**
  - rust-book: **95.00%**
- **All gpt-4o-mini gates pass: False**

## Canonical model pick

Pick rule: higher per-site ground-truth agreement (Haiku tiebreak default).
- Haiku avg per-site agreement: **94.00%**
- gpt-4o-mini avg per-site agreement: **93.33%**
- **Canonical**: `haiku`

## API spend (exact, from provider usage fields)

- Sonnet: **$2.8419** over 900 calls (in 617,157 / out 35,021 / cache-write 1,701 / cache-read 1,529,199 tok)
- gpt-4o-mini: **$0.2049** over 900 calls (in 1,918,962 / out 29,380 / cached-in 1,340,800 tok)
- **Total: $3.0468**

## Next step

- One or more SC-3 gates failed. Iterate the prompt to v3 (sharpen failure-mode language, add an example for the offending class), then re-run `--calibration`.
- Spec allows up to 3 prompt iterations (per `specs/v15-judge-prompt-v1.md`). After 3 failed iterations, escalate to chat.md.
