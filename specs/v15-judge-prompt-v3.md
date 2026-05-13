---
artifact: judge_prompt
version: v3
date: 2026-05-13
models:
  primary: claude-sonnet-4-5-20250929
  secondary: gpt-4o-mini (current GA snapshot, resolved at universe-build time)
model_agnostic: true
temperature: 0
parent_spec: specs/v15-helpful-pages-universe.md
predecessor: specs/v15-judge-prompt-v2.md
status: draft
---

# v1.5 Helpful-Pages Judge Prompt — v3 (raw-source-viewer worked example)

## Changelog from v2 → v3 (2026-05-13)

**Source of refinement.** The DS-2 pilot (commit `4a10615` on
`feature/v15-pilot-sonnet-swap`) ran the v2 prompt on rust-book +
huggingface-transformers with Sonnet 4.5 (primary) and gpt-4o-mini
(secondary). Inter-model agreement on rust-book was 89.11% (270/303).
Of the 33 disagreements, **27 (≈82%) were concentrated on a single
URL pattern: raw source-code-viewer pages** (`/src/*.rs.html`).
On those URLs Sonnet 4.5 correctly classified as `non-helpful-other`
("raw source code file viewer with syntax-highlighted code but no
explanatory prose, parameter documentation, or usage examples"),
while gpt-4o-mini classified them as `helpful-docs`.

This is a generic methodology gap, not rust-book-specific. Any site
with a "view source" mode (rust-book, GitHub blob views, mdn snippet
viewers, etc.) produces the same failure shape. The v2 prompt's
DECISION GUIDANCE rule ("API reference pages are HELPFUL even when
mostly tables, parameter lists, or code blocks — they are reference
material") unintentionally over-extends to raw source viewers, which
contain code but lack the explanatory prose / parameter docs / usage
examples that distinguish rendered API reference from raw
implementation source.

**v3 change set.**

1. Adds ONE new worked example after the existing 5 (generic
   source-code-viewer pattern; URL anonymized to
   `docs.example.com/src/iter/fuse.rs.html` so it is not
   rust-book-specific).
2. Adds ONE one-line note in the DECISION GUIDANCE section pointing
   to the new sixth example.

No other byte changes in Block 1; Block 2 unchanged.

**Why this refinement is methodologically defensible.**

- **(a) The pattern is generic.** Source-code viewers exist on many
  sites in the universe (docs.rs uses `/src/`, GitHub blob views,
  mdn snippets, GitLab's tree view, etc.). The example is anonymized
  to a generic `docs.example.com` host so the prompt does not encode
  rust-book-specific signal. The pattern that distinguishes raw
  source-viewer from rendered API ref (presence of explanatory prose,
  parameter docs, usage examples vs. just syntax-highlighted source)
  is the universal feature.
- **(b) Calibration audit on hand-judged ground truth is the
  validation gate.** This v3 prompt is a candidate; whether it passes
  is decided by SC-3 calibration against the 4-site hand-judged
  ground truth (`bench/calibration_ground_truth_v15.csv`), not by
  one site's pilot.
- **(c) The change is spec-tracked + diff-reviewable.** v3 is a
  separate file from v2; the universe manifest records
  `judge_prompt_version: specs/v15-judge-prompt-v3.md` with its
  sha256 alongside the v2 lineage. Any audit can diff v2 vs v3 to
  see exactly the one example added and the one decision-guidance
  line added.

**Calibration implication.** Per spec SC-3, prompt iteration requires
full-pool re-judgment when v3 is selected as the canonical prompt.
The DS-2 pilot is re-fired on rust-book only to test whether v3
fixes the source-code-viewer failure on gpt-4o-mini (the cheap
secondary). If it does AND a regression check on the other 270
already-agreed URLs is clean, v3 becomes the candidate prompt for
the gpt-4o-mini-only v1.5.1+ unlock path. The 4-site hand-judged
ground truth calibration remains the gating artifact for full-pool
fire.

**Token count.** Block 1 grew from ~1168 tokens (v2) to ~1230 tokens
(v3) per the added example (~62 tokens). Still ≥1024 tokens, so
Anthropic prompt cache compatibility is preserved.

## Prompt structure (two user-message content blocks)

### Block 1 — static cacheable prefix

This block is sent as a single user-message content block with `cache_control: {"type": "ephemeral"}`. The Anthropic API stores this prefix on cache-write (25% premium) and reads it back at 10% input cost for subsequent calls within the 5-minute TTL window.

Verified ≥1024 tokens at v3 lock time (tiktoken cl100k_base + Anthropic count_tokens API).

```
You are classifying whether a single web page contains substantive
content that a user might ask RAG-style questions about. You will be
given a URL, a page title, and a content snippet at the end of this
message. Output exactly two lines per the format described below.

DEFINITIONS

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

OUTPUT FORMAT

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

DECISION GUIDANCE

When in doubt between helpful-other and non-helpful-other, ask: would a real
user reading this page think to type a substantive question about the page's
own subject matter (as opposed to a question about the site itself or about
navigation)? If yes, helpful-other; if no, non-helpful-other.

Index/landing pages are NON-HELPFUL even when they list links to helpful
pages — the index itself contains no own content. Reference: the second
example below (newegg category page).

API reference pages are HELPFUL even when mostly tables, parameter lists,
or code blocks — they are reference material a user would ask questions
about (parameters, response schemas, etc.). Reference: the fifth example.

Raw source code viewer pages (e.g., `/src/...*.rs.html`, GitHub blob views,
"view source" panels) are NON-HELPFUL even though they contain code — they
lack the explanatory prose / parameter documentation / usage examples that
distinguish rendered API reference from raw implementation source. Reference:
the sixth example below.

EXAMPLES

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

URL: https://docs.example.com/src/iter/fuse.rs.html
Title: fuse.rs.html — source
NON-HELPFUL
non-helpful-other: Raw source code file viewer with syntax-highlighted code but no explanatory prose, parameter documentation, or usage examples. Users would query the rendered docs (e.g., /std/iter/struct.Fuse.html), not the raw `.rs.html` source view.
```

### Block 2 — per-URL variable suffix

This block is NOT cached; it changes for every URL judged. The cached prefix above remains valid as long as Block 1 is byte-identical between calls (it is).

```
URL: {url}
Title: {title}
Content snippet (first 2000 chars after chrome-strip): {content}

Now classify this URL. Output exactly two lines per the format above.
```

## Why this prompt shape (notes for the calibration auditor)

Identical to v2 except for the one additional worked example and the one decision-guidance line. The example is anonymized (`docs.example.com/src/iter/fuse.rs.html`) so the prompt does not encode rust-book-specific signal; the same pattern (`/src/...*.rs.html` or analogous "view source" URL shapes) appears across many docs sites.

The v3 nudge is the kind of refinement a v2 calibration audit would normally produce — the DS-2 pilot surfaced a generic failure mode (raw source-viewer pages classified as helpful-docs by the weaker secondary judge), and the prompt is updated with one targeted example + one decision-guidance pointer to address it. The pattern is generic enough that this should not be characterizable as overfitting to rust-book.

## Calibration acceptance thresholds (from spec SC-3, dual-model)

Identical to v1/v2. Both models must independently pass:
- Per-site ground-truth agreement ≥90% on each of the 4 calibration sites
- Multi-call self-agreement <5% disagreement (3 calls per URL, 400 URLs)
- Per-class agreement ≥85% on each binary class

## Per-site sanity check thresholds (from spec SC-4)

Identical to v1/v2.

## Prompt-version migration

v3 supersedes v2 as the candidate for full-pool judgment **if and only if** SC-3 calibration on the 4-site hand-judged ground truth passes. Universe manifest's `judge_prompt_version` field records `specs/v15-judge-prompt-v3.md` + its sha256 when v3 is selected. Calibration audit fires against v3; v1 + v2 are preserved for diff review.
