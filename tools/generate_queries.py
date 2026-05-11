#!/usr/bin/env python3
"""DS-6: LLM-generated, LLM-verified query authoring (v1.4).

For each site:
  1. Sample N random URLs from crawl4ai-raw's pages.jsonl (highest-coverage
     tool — gives the broadest topic surface across all 11 sites)
  2. For each URL, call gpt-4o-mini to draft 1-2 questions answerable from
     the page content
  3. For each draft, call a SEPARATE gpt-4o-mini API invocation (fresh
     context window, no shared messages, no prior turns) to verify
     answerability
  4. Accept queries judged answerable, reject the rest
  5. Write accepted queries to queries/v14_queries.json
  6. Write rejected drafts + verifier rationale to queries/v14_rejected.json

Removes the COI inherent in v1.3's hand-written queries (authored by the
same person who maintains markcrawl). Critical: NO human reviews the
output queries before they enter the benchmark. Fixes to query quality
happen at the prompt/code level via regeneration, never at the
individual-query level — see specs/v14-methodology-hardening.md
"Inspection vs. curation".

Usage:
    # Single-site smoke (Gate 3a)
    python tools/generate_queries.py --run run_v13_merged_20260504_203748 \\
        --sites rust-book

    # Full-pool generation (Gate 3b)
    python tools/generate_queries.py --run run_v13_merged_20260504_203748
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlsplit

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# Load .env so OPENAI_API_KEY etc. are available (matches benchmark_retrieval.py).
try:
    from dotenv import load_dotenv

    load_dotenv(_REPO_ROOT / ".env")
except ImportError:
    pass

logger = logging.getLogger(__name__)

GENERATION_MODEL = os.environ.get("GENERATION_MODEL", "gpt-4o-mini")
VERIFICATION_MODEL = os.environ.get("VERIFICATION_MODEL", "gpt-4o-mini")
SAMPLE_URLS_PER_SITE = 30
MAX_QUERIES_PER_URL = 2
# 24000 chars ≈ 6000 tokens. crawl4ai-raw output for documentation sites
# typically prepends ~4000 chars of navigation chrome (keyboard-shortcut
# headers + full TOC) before substantive content; an 8000 cap was clipping
# off most real content. 24000 covers ~95% of doc pages end-to-end at a
# trivial extra cost (~$0.02 per Gate 3a iteration vs the 8K version).
MAX_PAGE_CHARS = 24000
MAX_TOKENS_GEN = 200
MAX_TOKENS_VERIFY = 100


GENERATION_PROMPT = """You are creating retrieval-benchmark questions from a documentation page.

Read the page content below and draft 1-2 questions that meet ALL of these:
1. The answer is **literally present in the substantive content** of this
   specific page — not just plausible from general knowledge of the topic.
2. The question is about the page's main topic, not navigation chrome,
   sidebar links, page headers/footers, or "see also" cross-references.
3. A real user reading this page might ask the question.
4. Concise — phrase as a user would type into a search box.
5. The two questions cover different aspects of the page (no near-duplicates).

If you cannot find at least one question whose answer is LITERALLY in
the substantive page content, return an empty array: []
This is normal for navigation pages, sitemap pages, login walls, redirect
stubs, 404 pages, or pages whose content is mostly chrome.

Return ONLY a JSON array of strings, like:
["First question?", "Second question?"]

## Page URL
{url}

## Page Content
{content}

## Questions JSON"""


VERIFICATION_PROMPT = """You are evaluating whether a question can be answered from the given page content.

Return ONLY a JSON object with this exact shape:
{{"answerable": true, "rationale": "one short sentence"}}
or
{{"answerable": false, "rationale": "one short sentence"}}

Be strict: only return true if the answer is **clearly and literally
present** in the content (not merely "the page is on this general topic").

When returning false, the rationale **must start with one of these two
prefixes** so downstream tooling can distinguish the two failure modes:

- `"answer-not-in-page: ..."` — the page has substantive content but
  this specific question's answer is not present. Normal verifier
  rejection; the sampler did its job (the page exists), the question
  just doesn't fit this URL.

- `"page-broken: ..."` — the page itself is broken: literally empty,
  sitemap, login wall, redirect stub, 404 page, or navigation-only
  with no substantive prose. Signals a SAMPLER issue (the URL should
  not have been picked).

Do NOT use any other rationale prefix. Do NOT use "page is empty" — it
is ambiguous between the two cases.

## Page URL
{url}

## Page Content
{content}

## Question
{query}

## Verdict JSON"""


_LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")


def _is_link_dominated(line: str, threshold: float = 0.30) -> bool:
    """Heuristic: a line is "link-dominated" (nav chrome) if removing all
    markdown links leaves less than `threshold` of its non-whitespace text.

    Catches TOC entries (`* [Chapter 1](url)`), locale-link blocks
    (`[Spanish](url)`), version selectors (`[v1.36](url) | [v1.35](url)`),
    nav lists. Doesn't flag prose with inline links — those keep most of
    their non-whitespace text after link removal.

    Blank lines return False (neutral)."""
    stripped = line.strip()
    if not stripped:
        return False
    raw_nonws = sum(1 for c in stripped if not c.isspace())
    if raw_nonws == 0:
        return False
    without_links = _LINK_PATTERN.sub("", line).strip()
    rem_nonws = sum(1 for c in without_links if not c.isspace())
    return (rem_nonws / raw_nonws) < threshold


def strip_nav_chrome(text: str, min_run: int = 5) -> str:
    """Strip runs of ≥ `min_run` consecutive link-dominated lines from
    page text BEFORE it reaches the MAX_PAGE_CHARS cap. Generic across
    sites (no per-site config) — designed to attack the common pattern
    where documentation sites prepend ~5K-50K chars of site nav, locale
    links, version selectors, and recursive TOC before substantive
    content begins.

    Blank lines inside a nav block are treated as neutral (don't count
    toward `min_run`, don't break the run). The whole run including
    interleaved blanks is dropped together.

    Short nav runs (< `min_run`) are preserved — those are likely
    inline link clusters in prose, not a chrome block."""
    lines = text.split("\n")
    out_lines: list[str] = []
    pending: list[str] = []
    nav_count_in_run = 0

    for line in lines:
        if not line.strip():
            # Blank line — neutral. Add to pending IF a run is forming.
            if nav_count_in_run > 0:
                pending.append(line)
            else:
                out_lines.append(line)
        elif _is_link_dominated(line):
            pending.append(line)
            nav_count_in_run += 1
        else:
            # Non-nav line — flush pending
            if nav_count_in_run >= min_run:
                pass  # drop the entire run
            else:
                out_lines.extend(pending)
            pending = []
            nav_count_in_run = 0
            out_lines.append(line)

    # Tail: same flush logic
    if nav_count_in_run >= min_run:
        pass
    else:
        out_lines.extend(pending)

    return "\n".join(out_lines)


# Locale subdomain prefixes that mark a URL as a translated mirror of an
# English canonical. Synced with benchmark_retrieval.py:_LOCALE_SUBDOMAIN_PREFIXES;
# duplicated here to avoid a circular import (generate_queries.py is a sibling
# script, not a benchmark_retrieval consumer).
_LOCALE_SUBDOMAIN_PREFIXES = frozenset([
    "af", "ar", "az", "be", "bg", "bn", "bs", "ca", "cs", "da", "de", "el",
    "en", "eo", "es", "et", "eu", "fa", "fi", "fr", "ga", "gl", "he", "hi",
    "hr", "hu", "hy", "id", "is", "it", "ja", "ka", "kk", "km", "kn", "ko",
    "ky", "la", "lt", "lv", "mk", "ml", "mn", "mr", "ms", "mt", "my", "nb",
    "ne", "nl", "nn", "no", "pa", "pl", "ps", "pt", "ro", "ru", "sa", "si",
    "sk", "sl", "sq", "sr", "sv", "sw", "ta", "te", "th", "tl", "tr", "uk",
    "ur", "uz", "vi", "zh",
    "zh-cn", "zh-tw", "zh-hk", "zh-hans", "zh-hant",
    "en-us", "en-gb", "en-ca", "en-au",
    "pt-br", "pt-pt",
    "es-mx", "es-ar", "es-es", "es-419",
    "fr-ca", "fr-fr",
    "de-de", "de-at", "de-ch",
])


# Per-site canonical scope prefix — what the site name PROMISES the
# queries to be about. Filters out off-topic content the source-tool
# (crawl4ai-raw) may have crawled at the eTLD+1 level. Set explicitly
# per site to avoid silently accepting whatever the seed URL implies;
# methodology-clean truth-in-labeling, not site-specific tuning.
#
# Caught 2026-05-11: 91% of HF queries were off-topic (62% endpoints.
# huggingface.co product UI, 30% discuss.huggingface.co forum) because
# crawl4ai-raw on HF crawled the broader huggingface.co eTLD+1. The
# scope filter blocks this at the sampler level.
# Values are EITHER a string prefix OR a tuple of prefixes (when a site
# exposes its canonical content under multiple URL paths — e.g., rust-book
# is published at both /book/ and /stable/book/ which are the same content
# version-pinned, both are legitimately "the book").
SCOPE_PREFIXES: dict[str, str | tuple[str, ...]] = {
    "react-dev":               "https://react.dev",
    "stripe-docs":             "https://docs.stripe.com",
    "huggingface-transformers": "https://huggingface.co/docs/transformers",
    "kubernetes-docs":         "https://kubernetes.io/docs",
    "postgres-docs":           "https://www.postgresql.org/docs",
    "mdn-css":                 "https://developer.mozilla.org/en-US/docs/Web/CSS",
    "rust-book":               ("https://doc.rust-lang.org/book",
                                "https://doc.rust-lang.org/stable/book"),
    "newegg":                  "https://www.newegg.com",
    "ikea":                    "https://www.ikea.com",
    "smittenkitchen":          "https://smittenkitchen.com",
    "propublica":              "https://www.propublica.org",
}


def is_in_site_scope(url: str, site: str) -> bool:
    """True if url falls within the canonical scope prefix(es) for `site`.

    The scope is what the site name PROMISES the queries to be about —
    e.g., huggingface-transformers means "the transformers docs," not
    "the entire huggingface.co eTLD+1 including endpoints.huggingface.co
    product UI or discuss.huggingface.co forum threads."

    Multiple prefixes per site are supported via tuple values (rust-book
    accepts both /book and /stable/book — same content version-pinned).

    Sites without an explicit SCOPE_PREFIXES entry are permissive
    (accept any URL) so new sites don't get silently blocked before
    their scope is set."""
    if not isinstance(url, str):
        return False
    prefix = SCOPE_PREFIXES.get(site)
    if not prefix:
        return True
    if isinstance(prefix, str):
        return url.startswith(prefix)
    # Tuple of prefixes — accept if URL matches any
    return any(url.startswith(p) for p in prefix)


def is_locale_mirror_url(url: str) -> bool:
    """True if the URL's leftmost subdomain is a known locale prefix
    (ar.react.dev, ko.react.dev, zh-cn.react.dev, etc.).

    Used by `load_pages_for_site` to filter out locale-mirror URLs
    before sampling. v1.4 sampler is English-only-by-design — keeping
    locale mirrors in the sample pool would produce queries in the
    page's native language, creating a per-tool fairness confound
    (tools that crawl locale mirrors get asymmetric advantage on
    multilingual queries). Multilingual RAG evaluation deferred to
    v1.5 as an explicit, opt-in evaluation dimension."""
    if not isinstance(url, str):
        return False
    try:
        netloc = urlsplit(url).netloc.lower()
    except (ValueError, AttributeError):
        return False
    if "." not in netloc:
        return False
    first = netloc.partition(".")[0]
    return first in _LOCALE_SUBDOMAIN_PREFIXES


def load_pages_for_site(run_dir: Path, tool: str, site: str) -> list[dict]:
    """Load pages.jsonl for a (tool, site) combination, skipping malformed
    lines AND filtering out (a) locale-mirror URLs (v1.4 English-only
    sampler) and (b) URLs outside the site's canonical scope prefix
    (v1.4 truth-in-labeling — see SCOPE_PREFIXES)."""
    path = run_dir / tool / site / "pages.jsonl"
    if not path.exists():
        return []
    pages = []
    locale_filtered = 0
    scope_filtered = 0
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                page = json.loads(line)
            except json.JSONDecodeError:
                continue
            url = page.get("url", "")
            if is_locale_mirror_url(url):
                locale_filtered += 1
                continue
            if not is_in_site_scope(url, site):
                scope_filtered += 1
                continue
            pages.append(page)
    if locale_filtered:
        logger.info(f"  filtered {locale_filtered} locale-mirror URLs from {site} pool")
    if scope_filtered:
        logger.info(f"  filtered {scope_filtered} out-of-scope URLs from {site} pool "
                    f"(kept only {SCOPE_PREFIXES.get(site, '<no scope>')}*)")
    return pages


def call_llm(client, prompt: str, model: str, max_tokens: int) -> str:
    """Single LLM call with exponential-backoff retries. Returns "" on failure."""
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0,
                timeout=30,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt * 2)
            else:
                logger.warning(f"LLM call failed after 3 attempts: {e}")
                return ""


def parse_json_list(text: str) -> list[str]:
    """Extract a JSON list of strings from a possibly-markdown-wrapped response."""
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        result = json.loads(text)
        if isinstance(result, list):
            return [str(x).strip() for x in result if isinstance(x, str) and x.strip()]
    except json.JSONDecodeError:
        pass
    return []


def parse_verdict(text: str) -> dict:
    """Extract verdict JSON from a possibly-markdown-wrapped response.

    Returns {"answerable": bool, "rationale": str}. Defaults to rejection
    on parse failure so malformed output doesn't sneak past verification."""
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        result = json.loads(text)
        if isinstance(result, dict):
            return {
                "answerable": bool(result.get("answerable", False)),
                "rationale": str(result.get("rationale", "")),
            }
    except json.JSONDecodeError:
        pass
    return {"answerable": False, "rationale": "verifier returned malformed JSON"}


def derive_url_match(url: str) -> str:
    """Derive a default url_match pattern — the last meaningful path segment.

    Reviewers can replace this with a more specific pattern, but it gives a
    reasonable default that tests "did retrieval find the right page?"
    """
    try:
        parts = urlsplit(url).path.rstrip("/").split("/")
        for seg in reversed(parts):
            if seg and seg.lower() not in ("index", "index.html", ""):
                return seg
    except (ValueError, AttributeError):
        pass
    return ""


def first_path_segment(url: str) -> str:
    """First non-empty path segment — used by the diversity check
    (≥10 distinct path-basepaths in 30 sampled URLs per the spec)."""
    try:
        parts = urlsplit(url).path.split("/")
        for seg in parts:
            if seg:
                return seg
    except (ValueError, AttributeError):
        pass
    return ""


def generate_for_site(
    client,
    site: str,
    pages: list[dict],
    sample_size: int,
    seed: int,
) -> tuple[list[dict], list[dict]]:
    """Generate + verify queries for one site. Returns (accepted, rejected).

    Each accepted/rejected entry is a dict with: query, url, url_match,
    page_match, category, description, verifier_rationale.
    """
    rng = random.Random(seed + abs(hash(site)) % 1000)

    if not pages:
        logger.warning(f"[{site}] No pages — returning empty")
        return [], []

    sample_n = min(sample_size, len(pages))
    sampled = rng.sample(pages, sample_n)

    distinct_basepaths = {first_path_segment(p.get("url", "")) for p in sampled}
    distinct_basepaths.discard("")
    logger.info(
        f"[{site}] Sampled {sample_n}/{len(pages)} URLs; "
        f"distinct first-path segments: {len(distinct_basepaths)}"
    )

    accepted = []
    rejected = []

    for i, page in enumerate(sampled, 1):
        url = page.get("url", "")
        content = page.get("markdown", "") or page.get("content", "") or page.get("text", "")
        if not content:
            logger.info(f"[{site}] {i}/{sample_n}: skip (empty page content) {url}")
            continue
        # Strip nav/locale/TOC chrome BEFORE applying the char cap so the
        # cap captures substantive content, not chrome. Generic heuristic;
        # no per-site tuning. See strip_nav_chrome docstring.
        content_clean = strip_nav_chrome(content)
        content_capped = content_clean[:MAX_PAGE_CHARS]

        gen_response = call_llm(
            client,
            GENERATION_PROMPT.format(url=url, content=content_capped),
            GENERATION_MODEL,
            MAX_TOKENS_GEN,
        )
        candidates = parse_json_list(gen_response)[:MAX_QUERIES_PER_URL]

        if not candidates:
            logger.info(f"[{site}] {i}/{sample_n}: 0 candidates from {url}")
            continue

        n_accepted_this_url = 0
        for query in candidates:
            verify_response = call_llm(
                client,
                VERIFICATION_PROMPT.format(url=url, content=content_capped, query=query),
                VERIFICATION_MODEL,
                MAX_TOKENS_VERIFY,
            )
            verdict = parse_verdict(verify_response)

            entry = {
                "query": query,
                "url": url,
                "url_match": derive_url_match(url),
                "page_match": "",
                "category": "",
                "description": "",
                "verifier_rationale": verdict["rationale"],
            }
            if verdict["answerable"]:
                accepted.append(entry)
                n_accepted_this_url += 1
            else:
                rejected.append(entry)

        logger.info(
            f"[{site}] {i}/{sample_n}: {len(candidates)} candidates → "
            f"{n_accepted_this_url} accepted, {len(candidates) - n_accepted_this_url} rejected"
        )

    return accepted, rejected


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True, help="Run directory name (e.g. run_v13_merged_20260504_203748)")
    parser.add_argument("--source-tool", default="crawl4ai-raw",
                        help="Tool whose pages.jsonl to sample from (default: crawl4ai-raw — highest coverage)")
    parser.add_argument("--sites", default=None,
                        help="Comma-separated sites (default: all sites available under source-tool)")
    parser.add_argument("--sample-urls", type=int, default=SAMPLE_URLS_PER_SITE,
                        help=f"URLs to sample per site (default: {SAMPLE_URLS_PER_SITE})")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for sampling determinism")
    parser.add_argument("--queries-out", default="queries/v14_queries.json")
    parser.add_argument("--rejected-out", default="queries/v14_rejected.json")
    args = parser.parse_args()

    run_dir = _REPO_ROOT / "runs" / args.run
    if not run_dir.is_dir():
        logger.error(f"Run dir not found: {run_dir}")
        sys.exit(1)

    source_tool_dir = run_dir / args.source_tool
    if not source_tool_dir.is_dir():
        logger.error(f"Source-tool dir not found: {source_tool_dir}")
        sys.exit(1)

    if args.sites:
        sites = [s.strip() for s in args.sites.split(",")]
    else:
        sites = sorted(d.name for d in source_tool_dir.iterdir() if d.is_dir())

    if not os.environ.get("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY env var required")
        sys.exit(1)

    from openai import OpenAI
    client = OpenAI()

    all_accepted = {}
    all_rejected = {}

    for site in sites:
        logger.info(f"\n=== {site} ===")
        pages = load_pages_for_site(run_dir, args.source_tool, site)
        logger.info(f"  {len(pages)} pages available")
        accepted, rejected = generate_for_site(client, site, pages, args.sample_urls, args.seed)
        all_accepted[site] = accepted
        all_rejected[site] = rejected
        first_pass = len(accepted) / (len(accepted) + len(rejected)) if (accepted or rejected) else 0
        logger.info(f"  {site} totals: {len(accepted)} accepted / {len(rejected)} rejected ({first_pass:.0%} first-pass)")

    queries_out = _REPO_ROOT / args.queries_out
    rejected_out = _REPO_ROOT / args.rejected_out
    queries_out.parent.mkdir(parents=True, exist_ok=True)

    # Merge into existing JSON (if any) rather than overwriting wholesale —
    # so a --sites huggingface-transformers re-fire updates only HF's
    # entry without dropping the other 10 sites' queries.
    final_accepted = {}
    if queries_out.is_file():
        try:
            final_accepted = json.loads(queries_out.read_text())
            if not isinstance(final_accepted, dict):
                final_accepted = {}
        except json.JSONDecodeError:
            final_accepted = {}
    final_accepted.update(all_accepted)

    final_rejected = {}
    if rejected_out.is_file():
        try:
            final_rejected = json.loads(rejected_out.read_text())
            if not isinstance(final_rejected, dict):
                final_rejected = {}
        except json.JSONDecodeError:
            final_rejected = {}
    final_rejected.update(all_rejected)

    with open(queries_out, "w") as f:
        json.dump(final_accepted, f, indent=2)
    with open(rejected_out, "w") as f:
        json.dump(final_rejected, f, indent=2)

    total_accepted = sum(len(v) for v in all_accepted.values())
    total_rejected = sum(len(v) for v in all_rejected.values())
    overall_first_pass = total_accepted / (total_accepted + total_rejected) if (total_accepted + total_rejected) else 0
    page_broken_rejections = sum(
        1 for entries in all_rejected.values()
        for e in entries
        if e.get("verifier_rationale", "").lower().startswith("page-broken")
    )
    answer_not_in_page_rejections = sum(
        1 for entries in all_rejected.values()
        for e in entries
        if e.get("verifier_rationale", "").lower().startswith("answer-not-in-page")
    )
    other_rejections = total_rejected - page_broken_rejections - answer_not_in_page_rejections

    logger.info("\n=== TOTAL ===")
    logger.info(f"Accepted: {total_accepted}")
    logger.info(f"Rejected: {total_rejected}")
    logger.info(f"Verifier first-pass rate: {overall_first_pass:.1%}")
    logger.info("  rejection breakdown:")
    logger.info(f"    page-broken (SAMPLER issue, should be 0): {page_broken_rejections}")
    logger.info(f"    answer-not-in-page (normal):              {answer_not_in_page_rejections}")
    logger.info(f"    other / unprefixed (PROMPT-FORMAT issue): {other_rejections}")
    logger.info(f"Wrote {queries_out}")
    logger.info(f"Wrote {rejected_out}")


if __name__ == "__main__":
    main()
