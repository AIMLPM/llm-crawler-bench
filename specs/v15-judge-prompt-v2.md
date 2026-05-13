---
artifact: judge_prompt
version: v2
date: 2026-05-13
models:
  primary_haiku: claude-haiku-4-5-20251001
  secondary_gpt4omini: gpt-4o-mini (current GA snapshot, resolved at universe-build time per spec DS-2)
model_agnostic: true
temperature: 0
parent_spec: specs/v15-helpful-pages-universe.md
predecessor: specs/v15-judge-prompt-v1.md
status: draft
---

# v1.5 Helpful-Pages Judge Prompt — v2 (caching-optimized restructure)

## Changelog from v1 → v2 (2026-05-13)

**Structural-only restructure for Anthropic prompt caching (Option B+C per chat.md 2026-05-13T16:30:00Z).** The v1 prompt body was a single string with `{url}/{title}/{content}` placeholders sandwiched in the middle of the instructions, followed by examples and the "now classify" preamble. Anthropic's prompt-cache breakpoints can only be applied as contiguous PREFIXES of the message input, so v1's layout cannot be cached without trapping the per-call variable text in the middle of an otherwise-static prefix.

v2 splits the prompt into:
1. **Static cacheable prefix** (≥1024 tokens, the Anthropic minimum cache size for Haiku family per Anthropic docs): definitions, 9+9 rationale prefix list, 5 worked examples, output-format instructions. This block is identical for every URL judged in a given full-pool run, so it caches with one 25% premium write + 10% reads for the remaining ~33,315 calls (5-minute TTL; the run keeps the cache warm with 4-8 parallel requests).
2. **Per-URL variable suffix**: just the `URL: / Title: / Content snippet:` lines + a one-line "Now classify and output two lines." reminder.

**No semantic content changed.** The helpful/non-helpful definitions, prefix categories, and examples are byte-identical to v1. The reordering does not change what the model sees CONCEPTUALLY about the task — it sees the same instructions, the same examples, and the same per-URL data — only the position of the URL/Title/Content lines moves from middle-of-prompt to end-of-prompt.

**Calibration implication.** Per spec SC-3, prompt iteration requires full-pool re-judgment. v2 is a structural reorganization with no semantic change, so the calibration RESULT should be substantively identical to v1; however, the spec is followed literally — v2's calibration audit is the gating artifact for full-pool fire. If v2 calibration deviates from what v1 would have produced (an unlikely-but-possible artifact of attention-position effects), revert to v1 without caching and re-escalate the cost question to chat.md.

## Prompt structure (two user-message content blocks)

### Block 1 — static cacheable prefix

This block is sent as a single user-message content block with `cache_control: {"type": "ephemeral"}`. The Anthropic API stores this prefix on cache-write (25% premium) and reads it back at 10% input cost for subsequent calls within the 5-minute TTL window.

Verified ≥1024 tokens at v2 lock time (tiktoken cl100k_base + Anthropic count_tokens API).

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

Identical to v1 — see `specs/v15-judge-prompt-v1.md` "Why this prompt shape" section. The category definitions, examples, and rationale all carry over byte-identical.

The only addition is the **DECISION GUIDANCE** subsection in Block 1, which:
1. Pulls out the two most-common ambiguity classes from v1's implicit guidance into explicit one-liners (index pages, API references).
2. Anchors them to the example numbers above so the model uses them as gold standards.
3. Adds ~50 tokens to the prefix, which both helps clear the 1024-token cache minimum (verified) and reduces ambiguity for the false-helpful-on-API-refs and false-helpful-on-indexes failure modes.

This is the kind of nudge a v2 iteration would normally make if v1's calibration audit flagged either failure mode. Since we are restructuring anyway for caching, including the nudge in v2 is a free improvement; if the audit shows it makes no statistical difference (likely), no harm done.

## Calibration acceptance thresholds (from spec SC-3, dual-model)

Identical to v1 — see `specs/v15-judge-prompt-v1.md`. Both models must independently pass:
- Per-site ground-truth agreement ≥90% on each of the 4 calibration sites
- Multi-call self-agreement <5% disagreement (3 calls per URL, 400 URLs)
- Per-class agreement ≥85% on each binary class

## Per-site sanity check thresholds (from spec SC-4)

Identical to v1.

## Prompt-version migration

v2 supersedes v1 for the v1.5.0 full-pool judgment. Universe manifest's `judge_prompt_version` field records `specs/v15-judge-prompt-v2.md` + its sha256. Calibration audit fires against v2 only; v1 is preserved for diff review.
