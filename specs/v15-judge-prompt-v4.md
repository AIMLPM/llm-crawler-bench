---
artifact: judge_prompt
version: v4
date: 2026-08-16
models:
  primary: claude-sonnet-4-5-20250929
  secondary: gpt-4o-mini (current GA snapshot, resolved at universe-build time)
model_agnostic: true
temperature: 0
parent_spec: specs/v15-helpful-pages-universe.md
predecessor: specs/v15-judge-prompt-v3.md
status: draft
---

# v1.5 Helpful-Pages Judge Prompt — v4 (product-listing pages)

## Changelog from v3 → v4 (2026-08-16)

**Source of refinement.** During the hand-judging of
`bench/calibration_ground_truth_v15.csv`, the benchmark owner (paulsave)
made a definitional ruling that contradicts the v1–v3 rubric: **category
browse pages that display concrete product data (product names, prices,
spec snippets) ARE helpful** — their own listing content answers
RAG-style questions ("what server motherboards does this store carry,
at what price"). The v1–v3 worked example #2 (a newegg category page,
labeled NON-HELPFUL) encoded the opposite and is replaced.

The boundary of the ruling: **facet/filter permutations of a listing
remain NON-HELPFUL.** URL query parameters that select a subset of an
existing listing (e.g. `?N=...`, `?filter=...`, `?page=2`) produce
near-duplicate views of the parent listing; counting them would explode
the helpful-pages universe with combinatorial variants of the same
products and dilute the coverage metric. Pure tracking parameters
(`utm_*`, `cm_sp`, `ref`) do not make a page a facet permutation.

Non-ecommerce index pages are unaffected: a table of contents, tag
archive, or author page whose own content is only links/bare titles
remains NON-HELPFUL (non-helpful-index). The distinguishing feature is
whether the listing itself DISPLAYS substantive data.

**v4 change set.**

1. DEFINITIONS, helpful list: adds a product-listing bullet.
2. DEFINITIONS, non-helpful list: narrows the index bullet to
   link-only/no-data indexes; the search bullet names facet
   permutations explicitly.
3. OUTPUT FORMAT: adds the `helpful-listing:` rationale prefix.
4. DECISION GUIDANCE: replaces the "Index/landing pages are
   NON-HELPFUL" paragraph with two paragraphs — the data-in-listing
   test and the facet-vs-tracking-parameter rule.
5. EXAMPLES: example #2 (newegg category page) flips NON-HELPFUL →
   HELPFUL (helpful-listing); a new seventh example (anonymized
   facet-permutation URL) anchors the NON-HELPFUL side of the
   boundary.

Block 2 unchanged.

**Why this refinement is methodologically defensible.**

- **(a) Direction of amendment is human → rubric.** v3's refinement was
  pilot-driven (judge-disagreement analysis); v4's is ground-truth-
  driven: the human judge who defines calibration truth ruled the
  rubric's definition wrong for e-commerce listings. Amending the
  rubric to match human judgment is the correct direction — the
  alternative (ground truth that contradicts the rubric the judges
  follow) would make SC-3 calibration fail for definitional rather
  than model-capability reasons.
- **(b) The pattern is generic.** Product-listing pages with concrete
  data exist across e-commerce (newegg, ikea, amazon-like sites) and
  structured-catalog sites generally. The new seventh example is
  anonymized to `shop.example.com` so the prompt does not encode
  calibration-set answers.
- **(c) Calibration audit on hand-judged ground truth remains the
  validation gate.** v4 is a candidate; whether it passes is decided
  by SC-3 calibration against the hand-judged ground truth, not by
  the ruling itself.
- **(d) The change is spec-tracked + diff-reviewable.** v4 is a
  separate file; the universe manifest records
  `judge_prompt_version: specs/v15-judge-prompt-v4.md` with its
  sha256 alongside the v1–v3 lineage.

**Calibration implication.** Per spec SC-3, prompt iteration requires
re-validation: the cheap check is a re-pilot on newegg (the affected
site) to confirm inter-model agreement holds across the new
listing-vs-facet boundary, followed by full calibration against the
hand-judged ground truth. v4 supersedes v3 as the full-pool candidate
**if and only if** SC-3 passes.

**Ground-truth provenance note.** The calibration CSV for this cycle is
Fable-5-drafted and human-verified (see
`bench/calibration_drafts_fable.json` meta). The v4 amendment
originated from the human verification pass, not from the model drafts
(the drafts initially followed v3 and were re-mapped after the ruling).

**Token count.** Block 1 grows from ~1230 tokens (v3) to ~1390 tokens
(v4) per the added bullet, guidance paragraphs, and seventh example.
Still ≥1024 tokens, so Anthropic prompt cache compatibility is
preserved. Verify with count_tokens at v4 lock time.

## Prompt structure (two user-message content blocks)

### Block 1 — static cacheable prefix

This block is sent as a single user-message content block with `cache_control: {"type": "ephemeral"}`. The Anthropic API stores this prefix on cache-write (25% premium) and reads it back at 10% input cost for subsequent calls within the 5-minute TTL window.

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

Identical to v3 except for the product-listing amendment (change set
above). The seventh example is anonymized (`shop.example.com`) so the
prompt does not encode calibration-set answers; the facet-parameter
pattern (`?N=`, `?filter=`, `?page=`) is generic across faceted
e-commerce and catalog sites. Example #2 retains the newegg URL it has
carried since v1 — only its verdict and rationale change, per the
owner's definitional ruling.

## Calibration acceptance thresholds (from spec SC-3, dual-model)

Identical to v1/v2/v3. Both models must independently pass:
- Per-site ground-truth agreement ≥90% on each of the 4 calibration sites
- Multi-call self-agreement <5% disagreement (3 calls per URL, 400 URLs)
- Per-class agreement ≥85% on each binary class

## Per-site sanity check thresholds (from spec SC-4)

Identical to v1/v2/v3.

## Prompt-version migration

v4 supersedes v3 as the candidate for full-pool judgment **if and only
if** SC-3 calibration on the hand-judged ground truth passes. Universe
manifest's `judge_prompt_version` field records
`specs/v15-judge-prompt-v4.md` + its sha256 when v4 is selected.
Calibration audit fires against v4; v1–v3 are preserved for diff review.
