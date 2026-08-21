---
artifact: judge_prompt
version: v5
date: 2026-08-17
models:
  primary: claude-sonnet-4-5-20250929
  secondary: gpt-4o-mini (current GA snapshot, resolved at universe-build time)
model_agnostic: true
temperature: 0
parent_spec: specs/v15-helpful-pages-universe.md
predecessor: specs/v15-judge-prompt-v4.md
status: draft
---

# v1.5 Helpful-Pages Judge Prompt — v5 (chapter-stub + reader-callout examples)

## Changelog from v4 → v5 (2026-08-17)

**Source of refinement.** Round-2 calibration (v4 prompt + listing-aware
snippets, exact spend $3.0468) passed the per-site gate on all three
sites for both models (newegg 95/91, propublica 92/94, rust-book 95/95)
and self-agreement (0.00% both), but FAILED the per-class NON-HELPFUL
gate (Sonnet 12/20, gpt-4o-mini 2/20). Miss analysis over the 20
NON-HELPFUL ground-truth rows showed four mechanical patterns (facet
URLs, language mirrors, thin stubs — now handled by the Stage-2a
deterministic pre-classifier, see below) and two genuinely
LLM-judgeable patterns that both models miss:

1. **mdBook chapter-opener stubs** (`chNN-00-*.html`): roadmap pages
   with only a few sentences previewing the chapter's sub-pages. Judges
   read them as book documentation pages (helpful-docs); the rubric's
   <100-words-own-content rule makes them non-helpful-empty. Missed by
   both models on all such rows whose chrome-inflated word counts
   escape the deterministic thin rule.
2. **Reader-callout / story-submission pages** ("share your story",
   "help us report on X"): engagement forms with only a solicitation
   paragraph, hosted at /article/ URLs. gpt-4o-mini labels them
   helpful-article from URL shape + headline.

**v5 change set.** Adds TWO worked examples (eighth: chapter-opener
stub; ninth: reader-callout page) and TWO decision-guidance lines
pointing at them. No other Block 1 changes; Block 2 unchanged.

**Companion change — Stage-2a deterministic pre-classifier** (in
`tools/judge_helpful_pages.py`, not in this prompt): facet/filter
URL permutations, language-mirror pages, and <100-word thin pages are
decided mechanically BEFORE the LLM judge, and SC-3 is computed on the
combined system (prefilter + judge) — the same composition that runs
in --full-pool. The rubric already treats these as mechanical
("filtered separately" for mirrors; the owner's facet exclusion; the
explicit word-count rule). Validated on the 300-row ground truth:
11 fires, 0 false fires.

**Iteration accounting.** This is prompt iteration #3 under SC-3
(v2→v3 source-viewer, v3→v4 owner listing ruling, v4→v5 this). Per
spec, a further failure escalates to chat.md rather than iterating
again.

**Token count.** Block 1 grows ~120 tokens over v4 (~1510 total).
Still ≥1024; cache compatibility preserved.

## Prompt structure (two user-message content blocks)

### Block 1 — static cacheable prefix

Sent with `cache_control: {"type": "ephemeral"}` (Anthropic) / auto-cached (OpenAI).

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
- Product-listing / category browse pages that display concrete
  product data in the listing itself (product names with prices,
  spec snippets) — the listing content answers "what does this
  store carry, and at what price"
- Pages that answer questions on their own topic
- A real user reading this page might want to ask questions about
  its content

A "non-helpful" page contains:
- Site navigation, top menus, footer link dumps, sitemaps
- Search results, filter/facet permutations of a listing, pagination
  archives
- Login, signup, password reset, account settings, checkout flows
- Error pages, 404s, redirect-only pages
- Category/tag/author/date INDEX pages whose own content is ONLY
  links or bare titles — no substantive data (no prices,
  descriptions, or spec data) displayed in the listing itself
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
  helpful-listing:     — product-listing / category browse page displaying concrete product data (names, prices, specs)
  helpful-other:       — substantive content not fitting above (note in rationale)

If NON-HELPFUL, prefix with one of:
  non-helpful-nav:        — navigation, menu, sitemap, link-dump
  non-helpful-index:      — index page whose own content is only links/bare titles (no data)
  non-helpful-search:     — search results, filter/facet permutation, pagination
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

Listing pages: the test is whether the listing DISPLAYS substantive data.
A category browse page showing product tiles with names and prices is
HELPFUL (helpful-listing) — its own content answers "what does this store
carry and at what price". An index page that is only links or bare titles
(a table of contents, a tag archive, an author page) is NON-HELPFUL
(non-helpful-index). Reference: the second and seventh examples below.

Facet/filter permutations of a listing (URL query parameters that select a
subset of an existing listing, e.g. `?N=...`, `?filter=...`, `?page=2`) are
NON-HELPFUL (non-helpful-search) even when they display product data — they
are near-duplicate views of the parent listing. Pure tracking parameters
(`utm_*`, `cm_sp`, `ref`) do NOT make a page a facet permutation; ignore
them. Reference: the seventh example below.

API reference pages are HELPFUL even when mostly tables, parameter lists,
or code blocks — they are reference material a user would ask questions
about (parameters, response schemas, etc.). Reference: the fifth example.

Raw source code viewer pages (e.g., `/src/...*.rs.html`, GitHub blob views,
"view source" panels) are NON-HELPFUL even though they contain code — they
lack the explanatory prose / parameter documentation / usage examples that
distinguish rendered API reference from raw implementation source. Reference:
the sixth example below.

Chapter-opener / roadmap pages in books and multi-page guides (often
`chNN-00-*` URLs) that only preview what the chapter's sub-pages cover are
NON-HELPFUL (non-helpful-empty) even though they look like documentation —
the sub-pages carry the content a user would query. A chapter opener that
itself teaches substantive material IS helpful. Reference: the eighth
example below.

Reader-callout / story-submission pages ("share your story", "help us
report on X") are NON-HELPFUL (non-helpful-other) — engagement forms with
only a solicitation paragraph of own content, even when hosted at an
/article/ URL with a headline. Reference: the ninth example below.

EXAMPLES

URL: https://huggingface.co/docs/transformers/model_doc/bert
Title: BERT — Hugging Face transformers documentation
HELPFUL
helpful-docs: Reference documentation for the BERT model with class signatures, parameters, and usage examples.

URL: https://newegg.com/c/computer-systems
Title: Computer Systems - Newegg.com
HELPFUL
helpful-listing: Category browse page displaying product tiles with names, prices, and spec snippets — the listing itself answers what products are carried and at what price.

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

URL: https://shop.example.com/p/pl?N=100006670+4016
Title: Recertified Hard Drives — Shop
NON-HELPFUL
non-helpful-search: Facet permutation of an existing product listing (the `?N=` parameters select a subset of the parent category) — a near-duplicate filtered view, not a distinct queryable listing.

URL: https://docs.example.com/book/ch07-00-managing-growing-projects.html
Title: Managing Growing Projects — The Example Book
NON-HELPFUL
non-helpful-empty: Chapter-opener roadmap page with only a few sentences previewing the chapter's sub-pages; the sub-pages carry the substantive content a user would query.

URL: https://news.example.org/article/share-your-story-medical-bills
Title: Have You Been Affected by Surprise Medical Bills? Share Your Story
NON-HELPFUL
non-helpful-other: Reader-callout page soliciting story submissions — an engagement form with only a solicitation paragraph of own content, despite the /article/ URL and headline.
```

### Block 2 — per-URL variable suffix

Not cached; changes per URL.

```
URL: {url}
Title: {title}
Content snippet (first 2000 chars after chrome-strip): {content}

Now classify this URL. Output exactly two lines per the format above.
```

## Calibration acceptance thresholds (from spec SC-3, dual-model)

Identical to v1–v4, with one amendment: SC-3 is computed on the
**combined system** (Stage-2a deterministic pre-classifier + LLM
judge), matching the --full-pool composition. Both models must
independently pass:
- Per-site ground-truth agreement ≥90% on each calibration site
- Multi-call self-agreement <5% disagreement (3 calls per URL)
- Per-class agreement ≥85% on each binary class

## Prompt-version migration

v5 supersedes v4 as the full-pool candidate **iff** SC-3 passes on the
combined system. Manifest records `judge_prompt_version:
specs/v15-judge-prompt-v5.md` + sha256. v1–v4 preserved for diff
review. This is iteration #3 — a further failure escalates to chat.md.
