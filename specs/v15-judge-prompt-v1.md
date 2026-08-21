---
artifact: judge_prompt
version: v1
date: 2026-05-11
models:
  primary_haiku: claude-haiku-4-5-20251001
  secondary_gpt4omini: gpt-4o-mini (current GA snapshot, resolved at universe-build time per spec DS-2)
model_agnostic: true
temperature: 0
parent_spec: specs/v15-helpful-pages-universe.md
status: draft
---

# v1.5 Helpful-Pages Judge Prompt — v1 (model-agnostic, dual-model use)

This is a **separately versioned, diff-reviewable artifact**. The prompt below is consumed by `tools/judge_helpful_pages.py` to classify each URL in the v1.5 reference corpora as `helpful` or `non-helpful` for RAG query generation. When a calibration audit reveals systematic prompt failure (under EITHER judge model), the next iteration lands at `specs/v15-judge-prompt-v2.md` (and so on); the universe manifest records which prompt version judged the corpus.

**Dual-model usage (DS-2 amendment, 2026-05-12).** The same prompt is sent to BOTH judge models — primary Haiku (`claude-haiku-4-5-20251001`) and secondary gpt-4o-mini (snapshot resolved at universe-build time). The prompt is intentionally model-agnostic: no Claude-specific or OpenAI-specific instructions, no system-role assumptions, no proprietary directive syntax. If the calibration audit at SC-3 reveals one model interprets the prompt materially differently from the other (per-class agreement gap >5 pp), that surfaces as a prompt-design issue rather than a model-choice issue, and the prompt is iterated.

The classification powers two downstream artifacts:
- `bench/helpful_pages/<site>.json` — merged canonical universe of pages from which queries are sampled (canonical pick per SC-3 calibration)
- `bench/helpful_pages_disagreement.csv` — per-URL disagreement rows for cross-model methodology validation
- `tools/intersection_set.py` — intersection-set sibling report computes MRR only on `intersection ⊂ helpful-pages` (under the canonical model)

A loose prompt produces a contaminated universe (boilerplate inflates intersection MRR; nav pages produce nonsensical queries). A strict prompt under-covers substantive content (API references with sparse prose may be wrongly rejected). The calibration audit (SC-3) is the gate that catches both failure modes before full-pool application — applied independently to BOTH models.

## Prompt body (sent to BOTH judge models, model-agnostic)

```
You are classifying whether a single web page contains substantive
content that a user might ask RAG-style questions about.

A "helpful" page contains:
- Documentation, articles, recipes, product descriptions, reference
  entries, tutorials, blog posts, news stories, how-tos
- API reference pages with explanations, parameters, examples (even
  if mostly tables or code blocks — they are reference material)
- Pages that answer questions on their own topic
- A real user reading this page might want to ask questions about
  its content

A "non-helpful" page contains:
- Site navigation, top menus, footer link dumps, sitemaps
- Search results, filter combinations, faceted-browse pages,
  pagination archives
- Login, signup, password reset, account settings, checkout flows
- Error pages, 404s, redirect-only pages
- Category/tag/author/date INDEX pages with no substantive own
  content (just lists of links to other pages — the linked pages
  might be helpful, but the index itself is not)
- Empty pages or near-empty pages (fewer than ~100 words of own
  content after stripping nav/footer chrome)
- Cookie banners, GDPR notices, terms-of-service, privacy policies
  (informational but not RAG-query material for the site's purpose)
- Localized mirror pages of other content (filtered separately;
  flag as non-helpful if encountered)

URL: {url}
Title: {title}
Content snippet (first 2000 chars after chrome-strip): {content}

Output exactly two lines:

Line 1: HELPFUL or NON-HELPFUL
Line 2: One of the prefixed rationales below (one sentence).

If HELPFUL, prefix with one of:
  helpful-docs:        — documentation page (API reference, guide, tutorial)
  helpful-article:     — article, blog post, news story, opinion piece
  helpful-reference:   — entry in a structured reference (recipe, product, glossary, person, etc.)
  helpful-howto:       — step-by-step instructions (tutorial, guide, walkthrough)
  helpful-other:       — substantive content not fitting above (note in rationale)

If NON-HELPFUL, prefix with one of:
  non-helpful-nav:        — navigation, menu, sitemap, link-dump
  non-helpful-index:      — category/tag/author index with no own content
  non-helpful-search:     — search results, filter, pagination
  non-helpful-account:    — login, signup, settings, checkout
  non-helpful-error:      — error page, 404, redirect-only
  non-helpful-empty:      — too thin to query (< ~100 words own content)
  non-helpful-meta:       — cookie banner, ToS, privacy policy
  non-helpful-mirror:     — localized mirror of other content
  non-helpful-other:      — non-substantive not fitting above (note in rationale)

Examples:

URL: https://huggingface.co/docs/transformers/model_doc/bert
Title: BERT — Hugging Face transformers documentation
HELPFUL
helpful-docs: Reference documentation for the BERT model with class signatures, parameters, and usage examples.

URL: https://newegg.com/c/computer-systems
Title: Computer Systems - Newegg.com
NON-HELPFUL
non-helpful-index: Category landing page consisting of product tile grid with no substantive own content; the linked product pages would be helpful but this index is not.

URL: https://propublica.org/article/how-medicare-billing-works
Title: How Medicare Billing Actually Works | ProPublica
HELPFUL
helpful-article: Investigative article explaining Medicare billing mechanics with sourced examples — a user might ask questions about the topics covered.

URL: https://example.com/account/settings
Title: Account Settings
NON-HELPFUL
non-helpful-account: Account settings UI page with no informational content.

URL: https://docs.example.com/api/reference/get-user
Title: GET /user — API Reference
HELPFUL
helpful-docs: API endpoint reference with parameters, response schema, and example. Even though it is mostly structured data, this is reference material a user would ask about.

Now classify the URL above. Output exactly two lines.
```

## Why this prompt shape (notes for the calibration auditor)

- **Two-line output** is parseable without ambiguity. Line 1 is the binary classification; line 2 is the prefixed rationale category. The prefix convention mirrors v1.4's DS-6 verifier (`answer-not-in-page:` / `page-broken:`), which the team is already familiar with.
- **API-reference-as-helpful is explicit** because it's the most likely systematic-failure case. A loose prompt would call API pages non-helpful for being "mostly tables." We pre-empt this in both the helpful list and the examples.
- **Index-pages-as-non-helpful is explicit** because they are the most likely contamination source for the intersection set. Almost every tool crawls the root index and category pages; if those count as helpful, intersection MRR gets inflated by trivial title matches.
- **Localized mirrors are flagged** even though the v1.5 sampler also has `is_locale_mirror_url()` filtering — defense in depth.
- **Cookie banners / ToS / privacy** are explicitly non-helpful even though they are informational. They are not what users ask the site about.

## Calibration acceptance thresholds (from spec SC-3, dual-model)

All THREE thresholds must be met by EACH MODEL INDEPENDENTLY for prompt lock; they catch different failure modes at the same difficulty level:

- **Per-site ground-truth agreement ≥90%** on each of the 4 calibration sites (huggingface-transformers, newegg, propublica, rust-book) — catches systematic miscalibration vs ground truth.
- **Multi-call self-agreement on the same 400 calibration pages, 3 calls: <5% disagreement** on binary classification — catches random softness.
- **Per-class agreement ≥85%** on each binary class (helpful, non-helpful) — prevents class imbalance from hiding minority-class miscalibration. Reported alongside Cohen's kappa per site in `reports/methodology_validation.md` ("almost perfect" per Landis-Koch convention is κ ≥ 0.8).

If any threshold fails on EITHER model:
1. Identify the specific failure mode (which model, false-helpful or false-non-helpful, on which content shapes, on which calibration site).
2. Sharpen the prompt — add explicit rule, add example, or refine category definition. Both models share the prompt; iteration affects both calibrations.
3. Increment version: this file becomes `specs/v15-judge-prompt-v2.md`.
4. Re-run calibration on the same 400 pages with BOTH models.
5. Repeat up to 3 iterations. After 3 failed iterations:
   - If BOTH models still fail similarly → prompt cannot be salvaged with current design; escalate to chat.md for joint redesign review.
   - If only gpt-4o-mini fails → escape hatch: drop gpt-4o-mini, set `canonical = "haiku"`, mark SC-14's `v15x_can_drop_to_single_cheap` as `"blocked — gpt-4o-mini failed calibration"`, and render the templated disclosure paragraph below in `reports/methodology_validation.md` (the paragraph is gated on this case firing; absent otherwise):

     > v1.5.0 attempted dual-model judge validation. After N prompt iterations, gpt-4o-mini failed to meet the ≥90% ground-truth agreement / <5% multi-call / ≥85% per-class threshold on calibration site M. The methodology proceeds with Haiku-only judgment for v1.5.0 publication; v1.5.x may re-attempt validation with a revised prompt or an alternative cheap-model candidate. SC-14 cannot be evaluated this cycle.

   - If only Haiku fails → methodology emergency (Haiku is the locked canonical); escalate to chat.md for joint design review immediately.

## Per-site sanity check thresholds (from spec SC-4)

After full-pool application:
- Per-site helpful ratio < 5% → flag for prompt review (likely systematic over-rejection)
- Per-site helpful ratio > 95% → flag for prompt review (likely systematic over-acceptance)
- Manual eyeball: 10 lowest-confidence accepts + 10 highest-confidence rejects per site

Confidence proxy: Haiku does not natively return per-call confidence. We approximate by re-judging a **sampled subset** (20 URLs/site × 11 sites = 220 URLs) once more (440 extra calls = ~$0.11) and flagging URLs where the two calls disagreed as "low confidence." Disagreement = "low confidence." Full-pool double-call (~$30) is explicitly out of scope for v1.5 — revisit in v1.5.x only if the sanity-check sample surfaces systematic confidence problems. Documented as `tools/judge_helpful_pages.py --confidence-sample-mode`.

## Prompt-version migration

When a successor (`v15-judge-prompt-v2.md` etc.) supersedes this version:
1. The new version's frontmatter `parent_spec` field still points to `specs/v15-helpful-pages-universe.md`
2. A `changelog` section in the new version cites which calibration failure or sanity-check finding drove the iteration
3. Universe rebuild is required (full-pool re-judgment under the new prompt) — DO NOT mix outputs from different prompt versions in a single corpus
4. The universe manifest's `judge_prompt_version` field reflects the new version's path + sha256
