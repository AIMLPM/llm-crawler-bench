#!/usr/bin/env python3
"""DS-2 (v1.5): Dual-model helpful-pages judge.

Classifies each URL in the v1.5 reference corpora as `helpful` or
`non-helpful` for RAG query generation, using TWO independent judge
models (primary Haiku + secondary gpt-4o-mini) with the same model-
agnostic prompt at `specs/v15-judge-prompt-v3.md` (v3 supersedes v2; v2
remains for audit diff; v1 remains as the un-cached predecessor).

Per the spec amendment (commit 2219a5e), the dual-judge serves two
purposes:
  (a) Cross-model methodology validation for v1.5.0 — defends against
      "why this judge?" hostile-reviewer attack.
  (b) Forward-looking decision data for SC-14 — whether v1.5.x cycles
      can drop to gpt-4o-mini-only without methodology degradation.

Modes:
  --sanity-check        — Dual 10-page sanity check (FIRST action of DS-2).
                          Validates per-call token usage + gpt-4o-mini
                          format compliance. ~$0.005 spend.
  --build-calibration-scaffold
                        — Sample 100 URLs/site × 4 calibration sites =
                          400 URLs. Fetch page text (cache-first, then
                          live HTTP for sitemap-source sites). Write
                          `bench/calibration_ground_truth_v15.csv` with
                          url/title/content_snippet columns + empty
                          `ground_truth` column for paulsave's hand-
                          judging input.

Subsequent modes (NOT in this commit, future DS-2 steps):
  --calibration         — Run dual-judge on the hand-judged 400 URLs,
                          3-call multi-call agreement, lock threshold
                          evaluation.
  --full-pool           — Run dual-judge on all 53,316 reference URLs.
  --merge               — Merge per-model outputs into canonical
                          `bench/helpful_pages/<site>.json`, write
                          disagreement CSV, update manifest.
  --sanity-confidence   — Per-site 20-URL double-call confidence proxy
                          (canonical model only, after full-pool).

Cost bounds (spec DS-2):
  - 10-page sanity:     ~$0.005   (auto, no gate)
  - Full calibration:   ~$1.00    (auto after scaffold + hand-judging)
  - Full-pool dual:     ~$20      (~$15 Haiku + ~$5 gpt-4o-mini)
  - Sanity confidence:  ~$0.11    (canonical only, 20 URLs/site × 11)
  Hard cap: $30 budget, $50 hard escalation (R5).

Snapshot resolver (R-E): gpt-4o-mini snapshot is resolved at universe-
build time via `client.models.list()` — picks the most recent
`gpt-4o-mini-*` GA snapshot. Records exact snapshot ID in manifest.
Falls back to Haiku-only with SC-14 `blocked` if no snapshot available.

Usage:
    # Step 1: 10-page sanity check
    python3 tools/judge_helpful_pages.py --sanity-check

    # Step 2: build calibration scaffold (writes empty ground-truth CSV)
    python3 tools/judge_helpful_pages.py --build-calibration-scaffold

    # ... then escalate to chat.md for paulsave's hand-judging input.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import json
import logging
import random
import re
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Re-use the canonical URL normalizer + chrome stripper from the rest of
# the pipeline so the judge sees the same canonical form retrieval uses.
from benchmark_retrieval import _normalize_url_for_matching  # noqa: E402
from tools.generate_queries import strip_nav_chrome  # noqa: E402

# --- Constants -------------------------------------------------------------

POOL_PATH = REPO_ROOT / "sites" / "pool_v1.yaml"
REF_CORPUS_DIR = REPO_ROOT / "bench" / "reference_corpora"
V14_RUN = REPO_ROOT / "runs" / "run_v13_merged_20260504_203748"

PROMPT_PATH = REPO_ROOT / "specs" / "v15-judge-prompt-v5.md"
PROMPT_PATH_V4 = REPO_ROOT / "specs" / "v15-judge-prompt-v4.md"  # retained for audit diff
PROMPT_PATH_V3 = REPO_ROOT / "specs" / "v15-judge-prompt-v3.md"  # retained for audit diff
PROMPT_PATH_V2 = REPO_ROOT / "specs" / "v15-judge-prompt-v2.md"  # retained for audit diff
PROMPT_PATH_V1 = REPO_ROOT / "specs" / "v15-judge-prompt-v1.md"  # retained for audit diff
MANIFEST_PATH = REPO_ROOT / "bench" / "universe_manifest.json"

# Output directories per spec DS-2 (per-model files + merged canonical).
HAIKU_OUT_DIR = REPO_ROOT / "bench" / "helpful_pages_haiku"
GPT4OMINI_OUT_DIR = REPO_ROOT / "bench" / "helpful_pages_gpt4omini"
CANONICAL_OUT_DIR = REPO_ROOT / "bench" / "helpful_pages"
DISAGREEMENT_CSV = REPO_ROOT / "bench" / "helpful_pages_disagreement.csv"

# Pilot output directories (--pilot mode; 2-site cost-validation run, separate
# from full-pool so the artifacts don't collide with eventual canonical output).
PILOT_PRIMARY_OUT_DIR = REPO_ROOT / "bench" / "helpful_pages_sonnet_pilot"
PILOT_GPT4OMINI_OUT_DIR = REPO_ROOT / "bench" / "helpful_pages_gpt4omini_pilot"
PILOT_RESULTS_PATH = REPO_ROOT / "bench" / "pilot_v15_results.json"
PILOT_SITES = ("rust-book", "huggingface-transformers")
PILOT_COST_CAP_USD = 10.0
PILOT_FULL_POOL_UNIVERSE_SIZE = 33_316  # for projection extrapolation

# Calibration artifacts.
CALIB_GROUND_TRUTH = REPO_ROOT / "bench" / "calibration_ground_truth_v15.csv"
CALIB_AUDIT = REPO_ROOT / "bench" / "calibration_audit_v15.csv"

# Per-spec resolution Q1.
CALIBRATION_SITES = ("huggingface-transformers", "newegg", "propublica", "rust-book")
CALIBRATION_SAMPLE_PER_SITE = 100
CALIBRATION_SAMPLE_SEED = 1337  # Distinct from sitemap seed (42).

# Sanity-check uses 10 URLs from rust-book (small, all-cached, no live fetch).
SANITY_CHECK_SITE = "rust-book"
SANITY_CHECK_N = 10
SANITY_CHECK_SEED = 17

# Per-page content cap (matches DS-2 spec: "first 2000 chars after chrome-strip").
MAX_CONTENT_CHARS = 2000

# Listing-aware snippet upgrade (2026-08-17, post-calibration-failure fix).
_PRICE_RE = re.compile(r"\$[\d,]+\.\d{2}")


def build_judge_snippet(raw_text: str) -> str:
    """First-2000-chars-after-chrome-strip, upgraded to be listing-aware.

    Root cause of the 2026-08-17 calibration failure on newegg: e-commerce
    listing pages bury the product grid tens of thousands of chars below
    nav/cookie chrome, so the head-of-document snippet carried zero product
    data and both judges (correctly, on that evidence) called listing pages
    non-helpful — 35%/25% agreement vs ground truth.

    Rule (generic, no per-site config): if the stripped head has no price
    signal but the raw text contains >=3 price matches, compose the snippet
    from the stripped head plus a window centered on the median price
    position, so the judge sees the listing's own product names + prices.
    Pages without deep price clusters are unaffected (byte-identical to the
    old behavior)."""
    stripped = strip_nav_chrome(raw_text or "")
    head = stripped[:MAX_CONTENT_CHARS]
    if _PRICE_RE.search(head):
        return head
    prices = list(_PRICE_RE.finditer(raw_text or ""))
    if len(prices) < 3:
        return head
    center = prices[len(prices) // 2].start()
    lo = max(0, center - 200)
    window = raw_text[lo:lo + 1380]
    return (head[:550] + "\n[listing content from deeper in page:]\n" + window)[:MAX_CONTENT_CHARS]


# --- Deterministic pre-classifier (Stage 2a, 2026-08-17) -------------------
# Three NON-HELPFUL patterns are mechanical, not judgment calls, and the
# rubric itself treats them as such ("filtered separately" for mirrors; the
# owner's facet-permutation exclusion; the <100-words-own-content rule).
# Judging them with an LLM measured worse than deciding them directly
# (round-2 calibration: per-class NON-HELPFUL 60%/10%), so they are decided
# BEFORE the judge and the SC-3 gates are computed on the combined system.
# All rules are generic — no per-site configuration.

_TRACKING_KEYS = {"utm_source", "utm_medium", "utm_campaign", "utm_content",
                  "utm_term", "ref", "fbclid", "gclid", "cm_sp", "msclkid", "_ga"}
_FACET_KEYS = {"n", "page", "pg", "pagenumber", "filter", "sort", "order"}
_THIN_WORDS = 100
_LANG_MIN_WORDS = 15
_LANG_MIN_PROB = 0.95


def _facet_url(url: str) -> bool:
    """True if the URL query selects a subset of an existing listing
    (facet/filter/pagination params). Tracking params are ignored."""
    from urllib.parse import urlsplit
    query = urlsplit(url).query
    if not query:
        return False
    for pair in query.split("&"):
        key = pair.partition("=")[0].lower()
        if key in _TRACKING_KEYS or key.startswith("utm_"):
            continue
        if key in _FACET_KEYS:
            return True
    return False


def _detect_lang(text: str) -> Optional[str]:
    """Confident language of `text`, or None. Deterministic (seeded)."""
    try:
        from langdetect import DetectorFactory, detect_langs
        DetectorFactory.seed = 0
    except ImportError:
        return None
    sample = re.sub(r"[^A-Za-zÀ-ỹ\s]", " ", text).strip()
    if len(sample.split()) < _LANG_MIN_WORDS:
        return None
    try:
        langs = detect_langs(sample[:1200])
        if langs and langs[0].prob > _LANG_MIN_PROB:
            return langs[0].lang
    except Exception:
        pass
    return None


def deterministic_preclassify(
    url: str,
    snippet: str,
    raw_text: Optional[str],
    site_lang: str = "en",
) -> Optional[Tuple[str, str, str]]:
    """Return (label, category, reason) when the page is mechanically
    NON-HELPFUL, else None (page goes to the LLM judge).

    Rules (validated on the 300-row ground truth: 11 fires, 0 false):
      facet  — listing-subset query params in the URL
      mirror — page language differs from the site's primary language
               (detected on the snippet TAIL, past any leading chrome)
      thin   — <100 words after chrome-strip of the full raw text
               (needs raw_text; skipped when unavailable)
    """
    if _facet_url(url):
        return ("NON-HELPFUL", "non-helpful-search",
                "facet/filter permutation of a listing (URL query params)")
    lang = _detect_lang(snippet[-1000:])
    if lang and lang != site_lang:
        return ("NON-HELPFUL", "non-helpful-mirror",
                f"page language '{lang}' differs from site primary '{site_lang}'")
    if raw_text:
        words = len(strip_nav_chrome(raw_text).split())
        if words < _THIN_WORDS:
            return ("NON-HELPFUL", "non-helpful-empty",
                    f"{words} words own content after chrome-strip (<{_THIN_WORDS})")
    return None

# Model versions (per spec resolved decisions Q2 + R-E snapshot resolver).
# 2026-05-13 amendment: primary judge swapped Haiku 4.5 → Sonnet 4.5.
# Haiku 4.5 silently ignores cache_control on the v2 prefix (verified empirically);
# Sonnet 4.5 cached is cheaper than Haiku 4.5 uncached AND a stronger model.
# See specs/v15-helpful-pages-universe.md "Spec amendment 2026-05-13" block.
PRIMARY_JUDGE_MODEL = "claude-sonnet-4-5-20250929"  # pinned, drift assertion fires on mismatch
HAIKU_MODEL = PRIMARY_JUDGE_MODEL  # deprecated alias retained for cross-file diff hygiene
GPT4OMINI_FAMILY_PREFIX = "gpt-4o-mini"     # resolver picks latest CHAT-only GA snapshot
# Chat-only snapshot pattern: gpt-4o-mini OR gpt-4o-mini-YYYY-MM-DD.
# Rejects audio/realtime/search/transcribe/tts variants that share the prefix.
GPT4OMINI_CHAT_RE = re.compile(r"^gpt-4o-mini(-\d{4}-\d{2}-\d{2})?$")

# HTTP fetch (for sitemap-source calibration sites lacking v1.4 cache).
USER_AGENT = "bench-agent-v1.5/1.0 (+https://github.com/AIMLPM/llm-crawler-benchmarks)"
REQUEST_TIMEOUT_S = 15
FETCH_POLITENESS_S = 0.5

# Two-line judge output regex (tolerant to whitespace + case).
HELPFUL_PATTERN = re.compile(r"^\s*(HELPFUL|NON[\-\s]?HELPFUL)\s*$", re.I)
RATIONALE_PATTERN = re.compile(
    r"^\s*(helpful-(?:docs|article|reference|howto|listing|other)|"
    r"non-helpful-(?:nav|index|search|account|error|empty|meta|mirror|other))"
    r"\s*:\s*(.+?)\s*$",
    re.I,
)


# --- Logging --------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


# --- Data shapes ----------------------------------------------------------


@dataclass
class JudgeResult:
    classification: str         # "HELPFUL" or "NON-HELPFUL" (canonicalized)
    rationale_prefix: str       # e.g. "helpful-docs" or "non-helpful-index"
    rationale_text: str         # the rest after the prefix
    raw_response: str           # full LLM output for debug + audit
    judged_at: str              # ISO timestamp
    judge_call_id: str          # provider call ID for audit
    parse_warning: Optional[str] = None  # set if output wasn't strict-format
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    # Anthropic prompt-cache metering (v2 prompt + cache_control).
    # cache_creation_input_tokens: written on first call (25% premium)
    # cache_read_input_tokens: read on subsequent calls (10% of input cost)
    # input_tokens above is the NON-cached portion (full input on uncached calls).
    cache_creation_input_tokens: Optional[int] = None
    cache_read_input_tokens: Optional[int] = None


# --- Prompt loader --------------------------------------------------------


def load_prompt_blocks() -> Tuple[str, str]:
    """Extract the v3 two-block prompt (cacheable prefix + variable suffix).

    Returns (prefix_block, suffix_template). The prefix is byte-identical
    for every URL judged (cacheable). The suffix is a template with
    `{url}/{title}/{content}` placeholders.

    v3 supersedes v2: adds one source-code-viewer worked example +
    one decision-guidance line. Block 1/Block 2 split structure is
    unchanged. See specs/v15-judge-prompt-v3.md.
    """
    text = PROMPT_PATH.read_text()
    m1 = re.search(r"### Block 1 .*?```\s*\n(.*?)\n```", text, re.DOTALL)
    m2 = re.search(r"### Block 2 .*?```\s*\n(.*?)\n```", text, re.DOTALL)
    if not m1 or not m2:
        raise SystemExit(
            f"Could not extract Block 1 / Block 2 from {PROMPT_PATH}. "
            "Update load_prompt_blocks() if the spec format changed."
        )
    return m1.group(1), m2.group(1)


def load_prompt_template() -> str:
    """Compatibility helper for callers that want the full single-string
    prompt. Concatenates Block 1 + blank line + Block 2 template, which is
    the exact string sent to gpt-4o-mini (which has no API-level cache
    control — its automatic prefix caching is byte-prefix based)."""
    prefix, suffix = load_prompt_blocks()
    return prefix + "\n\n" + suffix


def prompt_sha256() -> str:
    return hashlib.sha256(PROMPT_PATH.read_bytes()).hexdigest()


def format_suffix(template: str, url: str, title: str, content: str) -> str:
    """Substitute placeholders in the per-URL Block 2 suffix.

    DO NOT use str.format — the spec contains literal braces in other
    sections that would break a format pass. Plain .replace() is safe."""
    out = template.replace("{url}", url)
    out = out.replace("{title}", title)
    out = out.replace("{content}", content)
    return out


def format_prompt(template: str, url: str, title: str, content: str) -> str:
    """Back-compat wrapper: substitutes placeholders in a full template.

    Used for callers (e.g. gpt-4o-mini path) that want the entire prompt
    as one string. The Anthropic path uses build_haiku_messages() instead
    to get separate cacheable / variable content blocks."""
    return format_suffix(template, url, title, content)


# --- API clients ----------------------------------------------------------


def _anthropic_client():
    import anthropic
    return anthropic.Anthropic()


# Deprecated alias retained for any external callers / cross-file diff hygiene.
_haiku_client = _anthropic_client


def _openai_client():
    from openai import OpenAI
    return OpenAI()


def resolve_gpt4omini_snapshot(client) -> Optional[str]:
    """R-E: pick the most-recent `gpt-4o-mini` CHAT-only GA snapshot via
    client.models.list(). Returns None if no snapshot available
    (escape-hatch path → SC-14 records `blocked — gpt-4o-mini snapshot
    unavailable`).

    Filter is strict: only `gpt-4o-mini` (alias) and dated chat snapshots
    `gpt-4o-mini-YYYY-MM-DD`. Rejects audio/realtime/search/transcribe/tts
    variants that share the prefix — those break /v1/chat/completions
    with a 404 'not a chat model' error (caught 2026-05-13 during smoke
    test where `gpt-4o-mini-tts-2025-12-15` sorted higher than the
    real chat snapshot)."""
    try:
        models = client.models.list()
    except Exception as e:
        logger.warning(f"OpenAI models.list() failed: {e}")
        return None
    chat_candidates = [m.id for m in models.data if GPT4OMINI_CHAT_RE.match(m.id)]
    if not chat_candidates:
        return None
    # Prefer dated snapshots over the bare alias for reproducibility (alias
    # rolls forward silently). If no dated snapshot, fall back to alias.
    dated = sorted([c for c in chat_candidates if "-20" in c], reverse=True)
    if dated:
        return dated[0]
    return chat_candidates[0]


def build_anthropic_messages(prefix: str, variable: str) -> List[dict]:
    """Build the two-content-block Anthropic message list with cache_control
    applied to the static prefix.

    Returns a single user message with two content blocks:
      [0] = static prefix (cacheable, ephemeral 5-minute TTL)
      [1] = per-URL variable (NOT cached)

    Per Anthropic docs (https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching):
      - cache_control: {"type": "ephemeral"} marks the breakpoint
      - The prefix MUST be ≥1024 tokens for Sonnet family (verified by
        Anthropic count_tokens() — v2 prompt prefix is 1171 tokens)
      - On cache hit: cache_read_input_tokens populated, billed at 10%
      - On cache miss/write: cache_creation_input_tokens populated, billed at 125%
      - input_tokens reflects the NON-cached portion (Block 2) only on hits
    """
    return [{
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prefix,
                "cache_control": {"type": "ephemeral"},
            },
            {
                "type": "text",
                "text": variable,
            },
        ],
    }]


# Deprecated alias retained for any external callers / cross-file diff hygiene.
build_haiku_messages = build_anthropic_messages


def call_primary_judge(client, prefix: str, variable: str) -> JudgeResult:
    """Primary-judge single call (Sonnet 4.5) with retries, using v2 two-block
    messages with cache_control on the static prefix.

    Args:
      prefix: the cacheable Block 1 text (instructions + examples).
      variable: the per-URL Block 2 text (URL/Title/Content filled in).
    """
    messages = build_anthropic_messages(prefix, variable)
    last_err = None
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=PRIMARY_JUDGE_MODEL,
                max_tokens=200,
                temperature=0,
                messages=messages,
            )
            text = resp.content[0].text if resp.content else ""
            usage = resp.usage
            return _parse_response(
                raw_response=text,
                judge_call_id=resp.id,
                input_tokens=getattr(usage, "input_tokens", None),
                output_tokens=getattr(usage, "output_tokens", None),
                cache_creation_input_tokens=getattr(usage, "cache_creation_input_tokens", None),
                cache_read_input_tokens=getattr(usage, "cache_read_input_tokens", None),
            )
        except Exception as e:
            last_err = e
            if attempt < 2:
                time.sleep(2 ** attempt * 2)
    raise RuntimeError(f"primary-judge call failed after 3 attempts: {last_err}")


# Deprecated alias retained for any external callers / cross-file diff hygiene.
call_haiku = call_primary_judge


def call_gpt4omini(client, model_id: str, prompt: str) -> JudgeResult:
    """gpt-4o-mini single-call with retries. Model ID is the resolved
    snapshot (R-E). Back-compat wrapper around call_gpt4omini_with_cache_meta
    that discards the cached-input meter."""
    result, _ = call_gpt4omini_with_cache_meta(client, model_id, prompt)
    return result


def call_gpt4omini_with_cache_meta(
    client, model_id: str, prompt: str
) -> Tuple[JudgeResult, int]:
    """gpt-4o-mini single-call with cache-meta. Returns (result, cached_input_tokens).

    OpenAI auto-caches prompt prefixes ≥1024 tokens and reports the number
    of cached tokens in usage.prompt_tokens_details.cached_tokens. We do
    NOT need to set any explicit cache control — it's transparent."""
    last_err = None
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0,
                timeout=30,
            )
            text = (resp.choices[0].message.content or "").strip()
            cached_tokens = 0
            if resp.usage and getattr(resp.usage, "prompt_tokens_details", None):
                cached_tokens = getattr(resp.usage.prompt_tokens_details, "cached_tokens", 0) or 0
            return (
                _parse_response(
                    raw_response=text,
                    judge_call_id=resp.id,
                    input_tokens=resp.usage.prompt_tokens if resp.usage else None,
                    output_tokens=resp.usage.completion_tokens if resp.usage else None,
                ),
                cached_tokens,
            )
        except Exception as e:
            last_err = e
            if attempt < 2:
                time.sleep(2 ** attempt * 2)
    raise RuntimeError(f"gpt-4o-mini call failed after 3 attempts: {last_err}")


def _parse_response(
    raw_response: str,
    judge_call_id: str,
    input_tokens: Optional[int],
    output_tokens: Optional[int],
    cache_creation_input_tokens: Optional[int] = None,
    cache_read_input_tokens: Optional[int] = None,
) -> JudgeResult:
    """Parse the two-line output contract. Tolerant fallback:
    - Strict: line 1 = HELPFUL/NON-HELPFUL, line 2 = `<prefix>: <text>`
    - Fallback: find HELPFUL/NON-HELPFUL token anywhere in line 1; find
      prefix anywhere in remaining lines; set parse_warning if non-strict.
    """
    lines = [ln for ln in raw_response.split("\n") if ln.strip()]
    parse_warning = None
    classification = None
    rationale_prefix = ""
    rationale_text = ""

    if lines:
        m = HELPFUL_PATTERN.match(lines[0])
        if m:
            tok = m.group(1).upper().replace(" ", "-").replace("--", "-")
            classification = "NON-HELPFUL" if "NON" in tok else "HELPFUL"
        else:
            # Tolerant fallback: search anywhere in line 1.
            m2 = re.search(r"\b(NON[\-\s]?HELPFUL|HELPFUL)\b", lines[0], re.I)
            if m2:
                tok = m2.group(1).upper().replace(" ", "-").replace("--", "-")
                classification = "NON-HELPFUL" if "NON" in tok else "HELPFUL"
                parse_warning = "line1_not_strict"

    if classification and len(lines) >= 2:
        m3 = RATIONALE_PATTERN.match(lines[1])
        if m3:
            rationale_prefix = m3.group(1).lower()
            rationale_text = m3.group(2).strip()
        else:
            # Tolerant: find any prefix anywhere.
            joined = "\n".join(lines[1:])
            m4 = re.search(
                r"(helpful-(?:docs|article|reference|howto|listing|other)|"
                r"non-helpful-(?:nav|index|search|account|error|empty|meta|mirror|other))"
                r"\s*:\s*(.+)",
                joined, re.I | re.DOTALL,
            )
            if m4:
                rationale_prefix = m4.group(1).lower()
                rationale_text = m4.group(2).strip().split("\n")[0]
                parse_warning = (parse_warning or "") + "+rationale_not_strict"
            else:
                rationale_text = " ".join(lines[1:])
                parse_warning = (parse_warning or "") + "+rationale_missing_prefix"

    if classification is None:
        # Total parse failure — record but don't crash.
        classification = "PARSE_FAILURE"
        parse_warning = "could_not_extract_classification"

    return JudgeResult(
        classification=classification,
        rationale_prefix=rationale_prefix,
        rationale_text=rationale_text,
        raw_response=raw_response,
        judged_at=_dt.datetime.now(_dt.UTC).isoformat(),
        judge_call_id=judge_call_id,
        parse_warning=parse_warning,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cache_creation_input_tokens=cache_creation_input_tokens,
        cache_read_input_tokens=cache_read_input_tokens,
    )


# --- Page text loader -----------------------------------------------------


def load_v14_cached_pages(site: str) -> Dict[str, dict]:
    """Load v1.4 crawl4ai-raw pages.jsonl for a site → {normalized_url: page_dict}."""
    cache: Dict[str, dict] = {}
    path = V14_RUN / "crawl4ai-raw" / site / "pages.jsonl"
    if not path.is_file():
        return cache
    with open(path) as f:
        for line in f:
            try:
                p = json.loads(line)
            except json.JSONDecodeError:
                continue
            url = p.get("url")
            if not url:
                continue
            cache[_normalize_url_for_matching(url)] = p
    return cache


def http_fetch_page(url: str) -> Optional[Tuple[str, str]]:
    """Live HTTP fetch for a URL when v1.4 cache lacks it. Returns
    (title, text) or None on failure. Strips HTML tags + extracts text."""
    try:
        headers = {"User-Agent": USER_AGENT, "Accept": "text/html"}
        resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT_S)
        if resp.status_code != 200 or "text/html" not in resp.headers.get("Content-Type", "").lower():
            return None
        html = resp.text
    except requests.RequestException:
        return None

    title_m = re.search(r"<title[^>]*>([^<]*)</title>", html, re.I)
    title = title_m.group(1).strip() if title_m else ""

    # Crude HTML → text. We only need the first ~2000 chars for the judge.
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return (title, text)


def get_page_text(
    url: str,
    cache: Dict[str, dict],
    allow_live_fetch: bool = False,
) -> Optional[Tuple[str, str]]:
    """Return (title, content) for a URL. Try cache first; optionally live
    fetch if not cached. Returns None if unavailable."""
    norm = _normalize_url_for_matching(url)
    if norm in cache:
        page = cache[norm]
        return (page.get("title", "") or "", page.get("text", "") or "")
    if allow_live_fetch:
        time.sleep(FETCH_POLITENESS_S)
        return http_fetch_page(url)
    return None


# --- Modes ----------------------------------------------------------------


def _primary_judge_cost_per_call(
    input_tokens: int,
    output_tokens: int,
    cache_creation: int,
    cache_read: int,
) -> float:
    """Per-call primary-judge cost (Sonnet 4.5) reflecting prompt cache metering.

    Anthropic Sonnet 4.5 pricing per Anthropic docs ($/1M):
      input (non-cached):           $3.00
      cache write 5m TTL (25% prem): $3.75
      cache read (10%):             $0.30
      output:                       $15.00

    Note: input_tokens from the Anthropic API reflects the NON-cached portion
    only (Block 2). cache_creation_input_tokens and cache_read_input_tokens
    are reported separately. Adding them all together avoids double-counting.
    """
    return (
        input_tokens * 3.00
        + cache_creation * 3.75
        + cache_read * 0.30
        + output_tokens * 15.00
    ) / 1_000_000


# Deprecated alias retained for any external callers / cross-file diff hygiene.
_haiku_cost_per_call = _primary_judge_cost_per_call


def _gpt4omini_cost_per_call(
    input_tokens: int,
    output_tokens: int,
    cached_input_tokens: int = 0,
) -> float:
    """Per-call gpt-4o-mini cost. OpenAI auto-caches prefixes ≥1024 tokens
    transparently; cached_input_tokens is reported in usage.prompt_tokens_details
    on cache hits. Pricing per spec ($/1M):
      input (non-cached):  $0.15
      cached input:        $0.075  (50% discount per OpenAI docs)
      output:              $0.60
    """
    non_cached = max(input_tokens - cached_input_tokens, 0)
    return (
        non_cached * 0.15
        + cached_input_tokens * 0.075
        + output_tokens * 0.60
    ) / 1_000_000


def mode_sanity_check(args) -> int:
    """Dual 10-page sanity check (FIRST action of DS-2 per spec).

    v1.5 DS-2 (caching variant): the v2 prompt is sent to Haiku with
    cache_control on the static prefix. The 10-URL run produces 1 cache
    write + 9 cache reads, giving a representative per-call cost
    distribution under warm-cache conditions.

    Output is persisted to bench/sanity_check_v15_cached.json so the
    pre-caching baseline at bench/sanity_check_v15.json stays available
    for diff."""
    cached_variant = getattr(args, "cached", True)  # default new behavior
    logger.info("=" * 60)
    logger.info("DS-2 SANITY CHECK — dual 10-page validation (CACHED)")
    logger.info("=" * 60)
    logger.info(f"Site: {SANITY_CHECK_SITE}; N={SANITY_CHECK_N}; seed={SANITY_CHECK_SEED}")

    # Pick 10 URLs from the calibration site's reference corpus that are
    # ALSO in the v1.4 cache (so no live fetch needed for sanity).
    ref_urls = (REF_CORPUS_DIR / SANITY_CHECK_SITE / "urls.txt").read_text().strip().split("\n")
    cache = load_v14_cached_pages(SANITY_CHECK_SITE)
    in_cache = [u for u in ref_urls if _normalize_url_for_matching(u) in cache]
    logger.info(f"Reference corpus: {len(ref_urls)} URLs; in v1.4 cache: {len(in_cache)}")

    rng = random.Random(SANITY_CHECK_SEED)
    sample = rng.sample(in_cache, min(SANITY_CHECK_N, len(in_cache)))
    logger.info(f"Sampled {len(sample)} URLs for sanity check.")

    prefix_block, suffix_template = load_prompt_blocks()
    prompt_ver = f"{PROMPT_PATH.relative_to(REPO_ROOT)} (sha256: {prompt_sha256()[:16]}...)"

    haiku = _haiku_client()
    openai = _openai_client()
    gpt4omini_model = resolve_gpt4omini_snapshot(openai)
    if not gpt4omini_model:
        logger.error("gpt-4o-mini snapshot resolver returned None — no GA snapshot available.")
        logger.error("Per R-E: SC-14 would record `blocked — gpt-4o-mini snapshot unavailable`.")
        logger.error("Aborting sanity check; fix OpenAI account access or fall back to Haiku-only.")
        return 2
    logger.info(f"Resolved gpt-4o-mini snapshot: {gpt4omini_model}")
    logger.info(f"Haiku model: {HAIKU_MODEL}")
    logger.info(f"Prompt: {prompt_ver}")
    logger.info("")

    results = []
    haiku_input_total = haiku_output_total = 0
    haiku_cache_creation_total = haiku_cache_read_total = 0
    gpt_input_total = gpt_output_total = gpt_cached_input_total = 0
    haiku_cost_total = 0.0
    gpt_cost_total = 0.0
    haiku_parse_warnings = 0
    gpt_parse_warnings = 0

    for i, url in enumerate(sample, 1):
        page = get_page_text(url, cache, allow_live_fetch=False)
        if page is None:
            logger.warning(f"  [{i}/{len(sample)}] SKIP (no content): {url}")
            continue
        title, raw_text = page
        text_clean = strip_nav_chrome(raw_text)
        text_capped = text_clean[:MAX_CONTENT_CHARS]
        if len(text_capped) < 100:
            logger.warning(f"  [{i}/{len(sample)}] SKIP (content too thin <100 chars): {url}")
            continue
        variable = format_suffix(suffix_template, url, title, text_capped)
        # gpt-4o-mini path uses the full concatenated prompt (no API-level
        # cache control; OpenAI auto-caches the prefix bytes ≥1024 tokens).
        full_prompt = prefix_block + "\n\n" + variable

        try:
            haiku_r = call_haiku(haiku, prefix_block, variable)
        except RuntimeError as e:
            logger.error(f"  [{i}/{len(sample)}] Haiku failed: {e}")
            continue
        try:
            gpt_r, gpt_cached_in = call_gpt4omini_with_cache_meta(
                openai, gpt4omini_model, full_prompt
            )
        except RuntimeError as e:
            logger.error(f"  [{i}/{len(sample)}] gpt-4o-mini failed: {e}")
            continue

        # Aggregate token + cost.
        h_in = haiku_r.input_tokens or 0
        h_out = haiku_r.output_tokens or 0
        h_cw = haiku_r.cache_creation_input_tokens or 0
        h_cr = haiku_r.cache_read_input_tokens or 0
        haiku_input_total += h_in
        haiku_output_total += h_out
        haiku_cache_creation_total += h_cw
        haiku_cache_read_total += h_cr
        haiku_cost_total += _haiku_cost_per_call(h_in, h_out, h_cw, h_cr)

        g_in = gpt_r.input_tokens or 0
        g_out = gpt_r.output_tokens or 0
        gpt_input_total += g_in
        gpt_output_total += g_out
        gpt_cached_input_total += gpt_cached_in
        gpt_cost_total += _gpt4omini_cost_per_call(g_in, g_out, gpt_cached_in)

        if haiku_r.parse_warning:
            haiku_parse_warnings += 1
        if gpt_r.parse_warning:
            gpt_parse_warnings += 1

        agree = haiku_r.classification == gpt_r.classification
        agreement_marker = "==" if agree else "!="
        cache_indicator = "C-WRITE" if h_cw else ("C-READ" if h_cr else "C-NONE")
        logger.info(
            f"  [{i}/{len(sample)}] {url[:50]:<50s} "
            f"haiku={haiku_r.classification:<12s} "
            f"{agreement_marker} gpt={gpt_r.classification:<12s} "
            f"[{cache_indicator} cw={h_cw} cr={h_cr}]"
        )
        results.append({
            "url": url,
            "title": title,
            "haiku": asdict(haiku_r),
            "gpt4omini": asdict(gpt_r),
            "gpt4omini_cached_input_tokens": gpt_cached_in,
            "agreement": agree,
        })

    n_judged = len(results)
    if n_judged == 0:
        logger.error("Zero pages judged — sanity check failed.")
        return 2

    # Per-page averages.
    avg_haiku_in = haiku_input_total / n_judged
    avg_haiku_out = haiku_output_total / n_judged
    avg_haiku_cw = haiku_cache_creation_total / n_judged
    avg_haiku_cr = haiku_cache_read_total / n_judged
    avg_haiku_cost = haiku_cost_total / n_judged

    avg_gpt_in = gpt_input_total / n_judged
    avg_gpt_out = gpt_output_total / n_judged
    avg_gpt_cached = gpt_cached_input_total / n_judged
    avg_gpt_cost = gpt_cost_total / n_judged

    combined_avg_cost = avg_haiku_cost + avg_gpt_cost

    # Full-pool projection at v1.5 DS-2 universe size of 33,316 (post-recap).
    universe_size = 33_316

    # Two flavors of projection:
    #   (a) "naive scale" — multiply current per-call cost (mixes 1 write + 9 reads) by N.
    #       Conservative because cache writes are amortized over more calls in a real run.
    #   (b) "amortized" — assume 1 cache write per cache cycle, then all reads, with
    #       writes happening every ~5 min × N_parallel × calls/sec. Hard to bound
    #       without knowing concurrency. We report the naive value; if it's <$36 we
    #       proceed and the real run will likely come in lower.
    projected_full_pool = combined_avg_cost * universe_size

    # For diagnostic clarity, also report what the cost would look like if ALL
    # calls in the full-pool were cache reads (1 amortized write across 33k calls).
    # That's the "best case" — useful for chat.md narrative.
    if haiku_cache_read_total > 0 and n_judged > 1:
        # Use the actual per-read pricing observed on cache-hit calls.
        per_read_haiku_cost = (
            (haiku_input_total - haiku_cache_creation_total) * 0.80
            + haiku_cache_read_total * 0.08
            + haiku_output_total * 4.00
        ) / 1_000_000 / (n_judged - (1 if haiku_cache_creation_total > 0 else 0))
        per_read_gpt_cost = avg_gpt_cost  # OpenAI is per-call cached automatically
        best_case_pool = (per_read_haiku_cost + per_read_gpt_cost) * universe_size
    else:
        best_case_pool = projected_full_pool

    logger.info("")
    logger.info("=" * 60)
    logger.info("SANITY CHECK RESULTS (cached)")
    logger.info("=" * 60)
    logger.info(f"Pages judged successfully:           {n_judged} / {SANITY_CHECK_N}")
    logger.info(f"Haiku parse warnings:                {haiku_parse_warnings}")
    logger.info(f"gpt-4o-mini parse warnings:          {gpt_parse_warnings}")
    inter_agree = sum(1 for r in results if r["agreement"]) / n_judged * 100
    logger.info(f"Inter-model agreement (10-page):     {inter_agree:.1f}%")
    logger.info("")
    logger.info(f"Haiku avg tokens: in={avg_haiku_in:.0f} out={avg_haiku_out:.0f} "
                f"cache_write={avg_haiku_cw:.0f} cache_read={avg_haiku_cr:.0f}")
    logger.info(f"gpt-4o-mini avg tokens: in={avg_gpt_in:.0f} out={avg_gpt_out:.0f} "
                f"cached_in={avg_gpt_cached:.0f}")
    logger.info(f"Haiku per-page cost (amortized over {n_judged}-call run):     ${avg_haiku_cost:.6f}")
    logger.info(f"gpt-4o-mini per-page cost:                              ${avg_gpt_cost:.6f}")
    logger.info(f"Combined per-page cost:                                 ${combined_avg_cost:.6f}")
    logger.info(f"Projected full-pool cost ({universe_size:,} URLs, naive scale): ${projected_full_pool:.2f}")
    logger.info(f"Projected full-pool cost (best case, all cache reads):  ${best_case_pool:.2f}")
    logger.info("Budget cap: $30  |  Hard escalation: $36 (>20% over cap)")
    logger.info("")

    format_gate = "PASS" if gpt_parse_warnings <= 1 else "FAIL"
    cost_gate = "PASS" if projected_full_pool <= 36 else "FAIL"

    out_name = "sanity_check_v15_cached.json" if cached_variant else "sanity_check_v15.json"
    out_path = REPO_ROOT / "bench" / out_name
    out_path.write_text(json.dumps({
        "started_at": _dt.datetime.now(_dt.UTC).isoformat(),
        "site": SANITY_CHECK_SITE,
        "n_sampled": SANITY_CHECK_N,
        "n_judged": n_judged,
        "haiku_model_version": HAIKU_MODEL,
        "gpt4omini_model_version": gpt4omini_model,
        "judge_prompt_version": prompt_ver,
        "caching_enabled": True,
        "anthropic_cache_control": "ephemeral",
        "inter_model_agreement_pct": round(inter_agree, 2),
        "haiku_parse_warnings": haiku_parse_warnings,
        "gpt4omini_parse_warnings": gpt_parse_warnings,
        "haiku_avg_tokens": {
            "input_non_cached": round(avg_haiku_in),
            "output": round(avg_haiku_out),
            "cache_creation": round(avg_haiku_cw),
            "cache_read": round(avg_haiku_cr),
        },
        "gpt4omini_avg_tokens": {
            "input": round(avg_gpt_in),
            "output": round(avg_gpt_out),
            "cached_input": round(avg_gpt_cached),
        },
        "cost_per_page": {
            "haiku": round(avg_haiku_cost, 6),
            "gpt4omini": round(avg_gpt_cost, 6),
            "combined": round(combined_avg_cost, 6),
        },
        "projected_full_pool_usd": round(projected_full_pool, 2),
        "projected_full_pool_best_case_usd": round(best_case_pool, 2),
        "universe_size_assumed": universe_size,
        "haiku_pricing_assumed_per_million": {
            "input": 0.80,
            "output": 4.00,
            "cache_creation": 1.00,
            "cache_read": 0.08,
        },
        "gpt4omini_pricing_assumed_per_million": {
            "input": 0.15,
            "output": 0.60,
            "cached_input": 0.075,
        },
        "gates": {"format_compliance": format_gate, "cost_projection": cost_gate},
        "budget_cap_usd": 30,
        "escalation_threshold_usd": 36,
        "results": results,
    }, indent=2, default=str))
    logger.info(f"Sanity check results persisted: {out_path.relative_to(REPO_ROOT)}")

    if format_gate == "FAIL":
        logger.error(
            f"gpt-4o-mini parse warnings = {gpt_parse_warnings} / 10 — "
            "format-compliance gate FAILED (>10% threshold)."
        )
        logger.error("ESCALATE to chat.md before proceeding to calibration.")
        return 3
    if cost_gate == "FAIL":
        logger.error(
            f"Projected full-pool ${projected_full_pool:.2f} > $36 cap-plus-20% — "
            "cost-projection gate FAILED."
        )
        logger.error("ESCALATE to chat.md before proceeding to calibration.")
        return 4

    logger.info("Both gates PASS. Cleared to proceed to calibration scaffold + hand-judging.")
    return 0


def mode_build_calibration_scaffold(args) -> int:
    """Build the calibration ground-truth CSV scaffold — 100 URLs per
    calibration site = 400 URLs, with url/title/content_snippet columns +
    empty `ground_truth` column for paulsave's hand-judging input.

    For sites with full v1.4 cache overlap (newegg, rust-book): sample
    100 cached URLs. For sites with sparse cache overlap (HF, propublica):
    sample from the reference corpus + live-fetch.
    """
    logger.info("=" * 60)
    logger.info("DS-2 CALIBRATION SCAFFOLD — 4 sites × 100 URLs")
    logger.info("=" * 60)

    rng = random.Random(CALIBRATION_SAMPLE_SEED)
    rows = []

    for site in CALIBRATION_SITES:
        logger.info(f"\n--- {site} ---")
        ref_urls = (REF_CORPUS_DIR / site / "urls.txt").read_text().strip().split("\n")
        cache = load_v14_cached_pages(site)

        # Prefer cached URLs first (no live fetch needed).
        cached_in_ref = [
            u for u in ref_urls if _normalize_url_for_matching(u) in cache
        ]
        not_cached = [
            u for u in ref_urls if _normalize_url_for_matching(u) not in cache
        ]
        rng.shuffle(cached_in_ref)
        rng.shuffle(not_cached)

        take_cached = min(CALIBRATION_SAMPLE_PER_SITE, len(cached_in_ref))
        need_live = CALIBRATION_SAMPLE_PER_SITE - take_cached
        logger.info(
            f"  ref={len(ref_urls)} cached={len(cached_in_ref)} "
            f"→ {take_cached} from cache + {need_live} via live fetch"
        )

        site_rows: List[dict] = []

        # Cached sampling.
        for url in cached_in_ref[:take_cached]:
            title, text = cache[_normalize_url_for_matching(url)].get("title", ""), cache[_normalize_url_for_matching(url)].get("text", "")
            snippet = build_judge_snippet(text or "")
            site_rows.append({
                "site": site,
                "url": url,
                "title": title or "",
                "content_snippet": snippet,
                "source": "v14_cache",
                "ground_truth": "",  # to be filled by paulsave
            })

        # Live fetch for the gap.
        fetched = 0
        attempts = 0
        for url in not_cached:
            if fetched >= need_live:
                break
            attempts += 1
            if attempts > need_live * 3:
                logger.warning(
                    f"  too many failed fetches; stopping at {fetched}/{need_live} live"
                )
                break
            try:
                page = http_fetch_page(url)
            except Exception as e:
                logger.warning(f"  fetch error for {url}: {e}")
                continue
            if page is None:
                continue
            title, text = page
            snippet = build_judge_snippet(text or "")
            if len(snippet) < 100:
                continue  # too thin, try next
            site_rows.append({
                "site": site,
                "url": url,
                "title": title,
                "content_snippet": snippet,
                "source": "live_fetch",
                "ground_truth": "",
            })
            fetched += 1
            if fetched % 10 == 0:
                logger.info(f"    live-fetched {fetched}/{need_live}")

        logger.info(f"  TOTAL collected for {site}: {len(site_rows)} URLs")
        rows.extend(site_rows)

    # Write CSV.
    CALIB_GROUND_TRUTH.parent.mkdir(parents=True, exist_ok=True)
    fields = ["site", "url", "title", "content_snippet", "source", "ground_truth"]
    with open(CALIB_GROUND_TRUTH, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            # Clamp snippet for CSV readability.
            r["content_snippet"] = r["content_snippet"].replace("\n", " ").replace("\r", " ")
            w.writerow(r)

    by_site = {}
    for r in rows:
        by_site.setdefault(r["site"], []).append(r)
    logger.info("")
    logger.info("=" * 60)
    logger.info("CALIBRATION SCAFFOLD COMPLETE")
    logger.info("=" * 60)
    for site in CALIBRATION_SITES:
        n = len(by_site.get(site, []))
        cached = sum(1 for r in by_site.get(site, []) if r["source"] == "v14_cache")
        live = n - cached
        logger.info(f"  {site}: {n} URLs ({cached} cached + {live} live-fetched)")
    logger.info(f"\nTotal: {len(rows)} URLs in {CALIB_GROUND_TRUTH.relative_to(REPO_ROOT)}")
    logger.info(
        "\nNext step: paulsave hand-classifies each row's `ground_truth` "
        "column as HELPFUL or NON-HELPFUL based on the title + content_snippet."
    )
    logger.info("Then run with --calibration to evaluate both models against the ground truth.")
    return 0


# --- Calibration mode (--calibration) -------------------------------------


def _read_calibration_ground_truth() -> List[dict]:
    """Read bench/calibration_ground_truth_v15.csv. Returns list of dicts;
    callers should filter on `ground_truth in ('HELPFUL','NON-HELPFUL')`
    to drop unfilled rows."""
    if not CALIB_GROUND_TRUTH.exists():
        raise SystemExit(
            f"Calibration ground-truth CSV not found: {CALIB_GROUND_TRUTH}. "
            "Run --build-calibration-scaffold first, then hand-judge the "
            "ground_truth column before calling --calibration."
        )
    rows = []
    with open(CALIB_GROUND_TRUTH, newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def _kappa(haiku_labels: List[str], gt_labels: List[str]) -> float:
    """Cohen's kappa on binary labels HELPFUL / NON-HELPFUL."""
    n = len(haiku_labels)
    if n == 0:
        return float("nan")
    agree = sum(1 for a, b in zip(haiku_labels, gt_labels) if a == b)
    p_o = agree / n
    p_h_help = sum(1 for x in haiku_labels if x == "HELPFUL") / n
    p_g_help = sum(1 for x in gt_labels if x == "HELPFUL") / n
    p_e = p_h_help * p_g_help + (1 - p_h_help) * (1 - p_g_help)
    if 1 - p_e == 0:
        return 1.0 if p_o == 1.0 else 0.0
    return (p_o - p_e) / (1 - p_e)


def _per_class_agreement(
    model_labels: List[str], gt_labels: List[str]
) -> Dict[str, float]:
    """Agreement rate within each ground-truth class."""
    out = {}
    for cls in ("HELPFUL", "NON-HELPFUL"):
        idxs = [i for i, g in enumerate(gt_labels) if g == cls]
        if not idxs:
            out[cls] = float("nan")
            continue
        agree = sum(1 for i in idxs if model_labels[i] == cls)
        out[cls] = agree / len(idxs)
    return out


def _run_one_model_calibration_pass(
    rows: List[dict],
    *,
    is_haiku: bool,
    haiku_client=None,
    openai_client=None,
    openai_model_id: str = "",
    prefix_block: str = "",
    suffix_template: str = "",
    n_calls: int = 3,
) -> Tuple[List[List[str]], Dict]:
    """Run `n_calls` judge passes on `rows`, returning (labels, usage):
    labels is a list of len(rows) lists each of length n_calls; usage is
    exact spend metering accumulated from provider usage fields."""
    out: List[List[str]] = [[] for _ in rows]
    usage = {
        "calls": 0, "cost_usd": 0.0,
        "input_tokens": 0, "output_tokens": 0,
        "cache_creation_tokens": 0, "cache_read_tokens": 0,
        "cached_input_tokens": 0,
    }
    for call_i in range(n_calls):
        logger.info(f"    pass {call_i+1}/{n_calls} ...")
        for i, r in enumerate(rows):
            url = r["url"]
            title = r.get("title", "") or ""
            snippet = r.get("content_snippet", "") or ""
            variable = format_suffix(suffix_template, url, title, snippet)
            try:
                if is_haiku:
                    jr = call_haiku(haiku_client, prefix_block, variable)
                    usage["cost_usd"] += _haiku_cost_per_call(
                        jr.input_tokens or 0, jr.output_tokens or 0,
                        jr.cache_creation_input_tokens or 0,
                        jr.cache_read_input_tokens or 0)
                    usage["cache_creation_tokens"] += jr.cache_creation_input_tokens or 0
                    usage["cache_read_tokens"] += jr.cache_read_input_tokens or 0
                else:
                    full = prefix_block + "\n\n" + variable
                    jr, cached_in = call_gpt4omini_with_cache_meta(
                        openai_client, openai_model_id, full)
                    usage["cost_usd"] += _gpt4omini_cost_per_call(
                        jr.input_tokens or 0, jr.output_tokens or 0, cached_in)
                    usage["cached_input_tokens"] += cached_in
                usage["calls"] += 1
                usage["input_tokens"] += jr.input_tokens or 0
                usage["output_tokens"] += jr.output_tokens or 0
                out[i].append(jr.classification)
            except RuntimeError as e:
                logger.warning(f"      [{i+1}/{len(rows)}] call failed: {e}; recording PARSE_FAILURE")
                out[i].append("PARSE_FAILURE")
            if (i + 1) % 50 == 0:
                logger.info(f"      [{i+1}/{len(rows)}] running spend ${usage['cost_usd']:.4f}")
    return out, usage


def _summarize_calibration(
    labels_3x: List[List[str]],
    gt_labels: List[str],
    sites: List[str],
) -> Dict:
    """Compute the SC-3 acceptance metrics on a 3x-call run.

    Returns:
      - majority_labels (per-row majority vote across 3 calls)
      - multi_call_self_disagreement_pct (rows where all 3 calls don't agree)
      - per_site_ground_truth_agreement (dict site -> pct)
      - per_class_agreement (HELPFUL pct, NON-HELPFUL pct on majority vote)
      - cohen_kappa (overall)
      - SC-3 gate booleans
    """
    n = len(labels_3x)
    majority = []
    multi_disagree = 0
    for triple in labels_3x:
        # binary majority — if any 2 of 3 agree
        c = {"HELPFUL": 0, "NON-HELPFUL": 0}
        for lbl in triple:
            if lbl in c:
                c[lbl] += 1
        if c["HELPFUL"] == c["NON-HELPFUL"]:
            majority.append("HELPFUL")  # tie-break helpful (rare; only if labels include parse failures)
        else:
            majority.append("HELPFUL" if c["HELPFUL"] > c["NON-HELPFUL"] else "NON-HELPFUL")
        if c["HELPFUL"] > 0 and c["NON-HELPFUL"] > 0:
            multi_disagree += 1

    multi_pct = multi_disagree / n * 100 if n else 0.0
    per_site = {}
    for site in sorted(set(sites)):
        idxs = [i for i, s in enumerate(sites) if s == site]
        gt_here = [gt_labels[i] for i in idxs]
        mj_here = [majority[i] for i in idxs]
        if not idxs:
            per_site[site] = float("nan")
            continue
        agree = sum(1 for a, b in zip(mj_here, gt_here) if a == b)
        per_site[site] = agree / len(idxs) * 100

    per_class = _per_class_agreement(majority, gt_labels)
    kappa = _kappa(majority, gt_labels)

    # SC-3 gates
    gate_gt = all(v >= 90 for v in per_site.values() if not (v != v))  # NaN check
    gate_multi = multi_pct < 5
    gate_class = all(v >= 0.85 for v in per_class.values() if not (v != v))

    return {
        "n_rows": n,
        "majority_labels": majority,
        "multi_call_self_disagreement_pct": round(multi_pct, 2),
        "per_site_ground_truth_agreement_pct": {k: round(v, 2) for k, v in per_site.items()},
        "per_class_agreement_pct": {k: round(v * 100, 2) for k, v in per_class.items()},
        "cohen_kappa": round(kappa, 4),
        "gates": {
            "ground_truth_agreement_>=90pct_per_site": gate_gt,
            "multi_call_self_disagreement_<5pct": gate_multi,
            "per_class_agreement_>=85pct": gate_class,
            "all_pass": gate_gt and gate_multi and gate_class,
        },
    }


def mode_calibration(args) -> int:
    """Run dual-judge calibration against bench/calibration_ground_truth_v15.csv.

    For each model independently:
      1. 3 calls per URL (multi-call self-agreement)
      2. Majority vote vs ground truth → per-site agreement
      3. Per-class agreement (HELPFUL/NON-HELPFUL)
      4. Cohen's kappa
      5. SC-3 gate evaluation

    Picks canonical model per Option C: higher per-site ground-truth
    agreement; Haiku tiebreak default.

    Writes:
      bench/calibration_audit_v15.csv  — per-row labels (haiku × 3, gpt × 3,
                                          majority, gt, agree flags)
      bench/sanity_check_v15.md        — human-readable summary
    """
    logger.info("=" * 60)
    logger.info("DS-2 CALIBRATION — dual-judge on hand-judged ground truth")
    logger.info("=" * 60)

    rows_all = _read_calibration_ground_truth()
    rows = [r for r in rows_all if (r.get("ground_truth") or "").strip().upper() in ("HELPFUL", "NON-HELPFUL")]
    logger.info(
        f"Loaded {len(rows_all)} rows; {len(rows)} have ground_truth filled "
        f"(skipping {len(rows_all)-len(rows)} unfilled)."
    )
    if not rows:
        logger.error(
            "Zero rows have ground_truth filled. paulsave must hand-judge the "
            f"`ground_truth` column in {CALIB_GROUND_TRUTH} before --calibration "
            "can fire against real data. Aborting."
        )
        return 5

    for r in rows:
        r["ground_truth"] = r["ground_truth"].strip().upper()
    sites = [r["site"] for r in rows]
    gt_labels = [r["ground_truth"] for r in rows]

    # Stage 2a: deterministic pre-classification. SC-3 is computed on the
    # combined system (prefilter + LLM judge) — the same composition that
    # runs in --full-pool. Prefiltered rows cost zero API calls.
    site_lang: Dict[str, str] = {}
    for site in sorted({r["site"] for r in rows}):
        lang_counts: Dict[str, int] = {}
        for r in rows:
            if r["site"] != site:
                continue
            lg = _detect_lang((r.get("content_snippet", "") or "")[-1000:])
            if lg:
                lang_counts[lg] = lang_counts.get(lg, 0) + 1
        site_lang[site] = max(lang_counts, key=lang_counts.get) if lang_counts else "en"
    logger.info(f"Site primary languages: {site_lang}")

    site_caches: Dict[str, dict] = {}
    prefilter: List[Optional[Tuple[str, str, str]]] = []
    for r in rows:
        site = r["site"]
        if site not in site_caches:
            site_caches[site] = load_v14_cached_pages(site)
        rec = site_caches[site].get(_normalize_url_for_matching(r["url"])) or {}
        raw_text = rec.get("text") or None
        prefilter.append(deterministic_preclassify(
            r["url"], r.get("content_snippet", "") or "", raw_text, site_lang[site]))
    n_pre = sum(1 for p in prefilter if p)
    logger.info(f"Deterministic pre-classifier fired on {n_pre}/{len(rows)} rows "
                f"(LLM judges the remaining {len(rows) - n_pre}).")
    llm_rows = [r for r, p in zip(rows, prefilter) if p is None]

    prefix_block, suffix_template = load_prompt_blocks()

    haiku = _haiku_client()
    openai = _openai_client()
    gpt_model = resolve_gpt4omini_snapshot(openai)
    if not gpt_model:
        logger.error("gpt-4o-mini snapshot resolver returned None — cannot run dual calibration.")
        return 2

    logger.info(f"Haiku model: {HAIKU_MODEL}")
    logger.info(f"gpt-4o-mini snapshot: {gpt_model}")
    logger.info(f"Prompt: {PROMPT_PATH.relative_to(REPO_ROOT)}")
    logger.info("")

    # 3-call passes per model.
    logger.info(f"--- Haiku ({HAIKU_MODEL}) ---")
    haiku_labels_llm, haiku_usage = _run_one_model_calibration_pass(
        llm_rows, is_haiku=True, haiku_client=haiku,
        prefix_block=prefix_block, suffix_template=suffix_template,
        n_calls=3,
    )
    logger.info(f"    Sonnet spend: ${haiku_usage['cost_usd']:.4f} over {haiku_usage['calls']} calls")

    logger.info(f"--- gpt-4o-mini ({gpt_model}) ---")
    gpt_labels_llm, gpt_usage = _run_one_model_calibration_pass(
        llm_rows, is_haiku=False, openai_client=openai, openai_model_id=gpt_model,
        prefix_block=prefix_block, suffix_template=suffix_template,
        n_calls=3,
    )
    logger.info(f"    gpt-4o-mini spend: ${gpt_usage['cost_usd']:.4f} over {gpt_usage['calls']} calls")

    def _merge_with_prefilter(llm_labels: List[List[str]]) -> List[List[str]]:
        merged: List[List[str]] = []
        it = iter(llm_labels)
        for p in prefilter:
            merged.append([p[0]] * 3 if p else next(it))
        return merged

    haiku_labels_3x = _merge_with_prefilter(haiku_labels_llm)
    gpt_labels_3x = _merge_with_prefilter(gpt_labels_llm)

    haiku_summary = _summarize_calibration(haiku_labels_3x, gt_labels, sites)
    gpt_summary = _summarize_calibration(gpt_labels_3x, gt_labels, sites)

    # R-D iteration loop: if either model fails any SC-3 gate, the audit is
    # written and an exit code signals "iterate the prompt". The actual
    # prompt iteration is a manual step (write v3, re-run).
    iterations_used = 1  # this is iteration #1 of v2; spec allows up to 3
    needs_iteration = (
        not haiku_summary["gates"]["all_pass"]
        or not gpt_summary["gates"]["all_pass"]
    )

    # Canonical pick per Option C: higher overall ground-truth agreement
    # (averaged across sites). Tiebreak → Haiku.
    haiku_avg = sum(haiku_summary["per_site_ground_truth_agreement_pct"].values()) / max(len(haiku_summary["per_site_ground_truth_agreement_pct"]), 1)
    gpt_avg = sum(gpt_summary["per_site_ground_truth_agreement_pct"].values()) / max(len(gpt_summary["per_site_ground_truth_agreement_pct"]), 1)
    if haiku_avg >= gpt_avg:
        canonical = "haiku"
    else:
        canonical = "gpt4omini"

    # Write the per-row audit CSV.
    CALIB_AUDIT.parent.mkdir(parents=True, exist_ok=True)
    fields = (
        ["site", "url", "ground_truth", "prefilter"]
        + [f"haiku_call_{i+1}" for i in range(3)]
        + ["haiku_majority", "haiku_agrees"]
        + [f"gpt4omini_call_{i+1}" for i in range(3)]
        + ["gpt4omini_majority", "gpt4omini_agrees"]
    )
    with open(CALIB_AUDIT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, r in enumerate(rows):
            h_calls = haiku_labels_3x[i]
            g_calls = gpt_labels_3x[i]
            h_maj = haiku_summary["majority_labels"][i]
            g_maj = gpt_summary["majority_labels"][i]
            row = {
                "site": r["site"],
                "url": r["url"],
                "ground_truth": r["ground_truth"],
                "prefilter": prefilter[i][1] if prefilter[i] else "",
                "haiku_majority": h_maj,
                "haiku_agrees": h_maj == r["ground_truth"],
                "gpt4omini_majority": g_maj,
                "gpt4omini_agrees": g_maj == r["ground_truth"],
            }
            for j in range(3):
                row[f"haiku_call_{j+1}"] = h_calls[j] if j < len(h_calls) else ""
                row[f"gpt4omini_call_{j+1}"] = g_calls[j] if j < len(g_calls) else ""
            w.writerow(row)
    logger.info(f"Per-row audit written: {CALIB_AUDIT.relative_to(REPO_ROOT)}")

    # Persist the exact spend record (provider-reported usage fields).
    spend_path = REPO_ROOT / "bench" / "calibration_spend_v15.json"
    spend_path.write_text(json.dumps({
        "date_utc": _dt.datetime.now(_dt.UTC).isoformat(),
        "prompt": str(PROMPT_PATH.relative_to(REPO_ROOT)),
        "rows": len(rows),
        "sonnet": haiku_usage,
        "gpt4omini": gpt_usage,
        "total_usd": round(haiku_usage["cost_usd"] + gpt_usage["cost_usd"], 4),
    }, indent=2) + "\n")
    logger.info(f"Spend record written: {spend_path.relative_to(REPO_ROOT)}")

    # Write the human-readable summary markdown.
    md_path = REPO_ROOT / "bench" / "sanity_check_v15.md"
    md_lines = [
        "# v1.5 DS-2 Calibration Audit",
        "",
        f"- **Date**: {_dt.datetime.now(_dt.UTC).isoformat()}",
        f"- **Prompt**: `{PROMPT_PATH.relative_to(REPO_ROOT)}` (sha256: {prompt_sha256()[:16]}...)",
        f"- **Haiku model**: `{HAIKU_MODEL}`",
        f"- **gpt-4o-mini snapshot**: `{gpt_model}`",
        f"- **Ground-truth rows used**: {len(rows)} / {len(rows_all)} filled",
        f"- **Deterministic pre-classifier**: fired on {n_pre} rows "
        f"(facet/mirror/thin); SC-3 computed on the combined system "
        f"(prefilter + LLM judge), matching --full-pool composition",
        "",
        "## Haiku results",
        "",
        f"- Multi-call self-disagreement: **{haiku_summary['multi_call_self_disagreement_pct']:.2f}%** (gate: <5%)",
        f"- Cohen's kappa: **{haiku_summary['cohen_kappa']:.4f}**",
        f"- Per-class agreement (majority vote): HELPFUL=**{haiku_summary['per_class_agreement_pct'].get('HELPFUL', 'n/a')}%**, NON-HELPFUL=**{haiku_summary['per_class_agreement_pct'].get('NON-HELPFUL', 'n/a')}%** (gate: ≥85%)",
        "- Per-site ground-truth agreement (gate: ≥90% each):",
    ]
    for site, pct in haiku_summary["per_site_ground_truth_agreement_pct"].items():
        md_lines.append(f"  - {site}: **{pct:.2f}%**")
    md_lines += [
        f"- **All Haiku gates pass: {haiku_summary['gates']['all_pass']}**",
        "",
        "## gpt-4o-mini results",
        "",
        f"- Multi-call self-disagreement: **{gpt_summary['multi_call_self_disagreement_pct']:.2f}%** (gate: <5%)",
        f"- Cohen's kappa: **{gpt_summary['cohen_kappa']:.4f}**",
        f"- Per-class agreement: HELPFUL=**{gpt_summary['per_class_agreement_pct'].get('HELPFUL', 'n/a')}%**, NON-HELPFUL=**{gpt_summary['per_class_agreement_pct'].get('NON-HELPFUL', 'n/a')}%** (gate: ≥85%)",
        "- Per-site ground-truth agreement (gate: ≥90% each):",
    ]
    for site, pct in gpt_summary["per_site_ground_truth_agreement_pct"].items():
        md_lines.append(f"  - {site}: **{pct:.2f}%**")
    md_lines += [
        f"- **All gpt-4o-mini gates pass: {gpt_summary['gates']['all_pass']}**",
        "",
        "## Canonical model pick",
        "",
        "Pick rule: higher per-site ground-truth agreement (Haiku tiebreak default).",
        f"- Haiku avg per-site agreement: **{haiku_avg:.2f}%**",
        f"- gpt-4o-mini avg per-site agreement: **{gpt_avg:.2f}%**",
        f"- **Canonical**: `{canonical}`",
        "",
        "## API spend (exact, from provider usage fields)",
        "",
        f"- Sonnet: **${haiku_usage['cost_usd']:.4f}** over {haiku_usage['calls']} calls "
        f"(in {haiku_usage['input_tokens']:,} / out {haiku_usage['output_tokens']:,} / "
        f"cache-write {haiku_usage['cache_creation_tokens']:,} / cache-read {haiku_usage['cache_read_tokens']:,} tok)",
        f"- gpt-4o-mini: **${gpt_usage['cost_usd']:.4f}** over {gpt_usage['calls']} calls "
        f"(in {gpt_usage['input_tokens']:,} / out {gpt_usage['output_tokens']:,} / "
        f"cached-in {gpt_usage['cached_input_tokens']:,} tok)",
        f"- **Total: ${haiku_usage['cost_usd'] + gpt_usage['cost_usd']:.4f}**",
        "",
        "## Next step",
        "",
    ]
    if needs_iteration:
        md_lines += [
            "- One or more SC-3 gates failed. Iterate the prompt to v3 (sharpen failure-mode language, add an example for the offending class), then re-run `--calibration`.",
            "- Spec allows up to 3 prompt iterations (per `specs/v15-judge-prompt-v1.md`). After 3 failed iterations, escalate to chat.md.",
        ]
    else:
        md_lines += [
            "- Both models pass SC-3 gates. Cleared to fire `--full-pool` against the canonical model + sibling on all 33,316 URLs.",
        ]
    md_path.write_text("\n".join(md_lines) + "\n")
    logger.info(f"Markdown summary written: {md_path.relative_to(REPO_ROOT)}")

    # Update manifest with judge_prompt_version + canonical model meta.
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text())
    else:
        manifest = {}
    manifest["judge_prompt_version"] = (
        f"{PROMPT_PATH.relative_to(REPO_ROOT)}#sha256:{prompt_sha256()}"
    )
    manifest["haiku_model_version"] = HAIKU_MODEL
    manifest["gpt4omini_model_version"] = gpt_model
    manifest["canonical_judge_model"] = canonical
    manifest["calibration_iterations_used"] = iterations_used
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    logger.info("")
    logger.info("=" * 60)
    logger.info(f"Canonical model: {canonical}")
    logger.info(f"Haiku gates all_pass: {haiku_summary['gates']['all_pass']}")
    logger.info(f"gpt-4o-mini gates all_pass: {gpt_summary['gates']['all_pass']}")
    logger.info(
        f"TOTAL API SPEND: ${haiku_usage['cost_usd'] + gpt_usage['cost_usd']:.4f} "
        f"(Sonnet ${haiku_usage['cost_usd']:.4f} + gpt-4o-mini ${gpt_usage['cost_usd']:.4f})")
    logger.info("=" * 60)
    return 0 if not needs_iteration else 6


# --- Full-pool mode (--full-pool) -----------------------------------------


def _checkpoint_path(model: str, site: str) -> Path:
    base = HAIKU_OUT_DIR if model == "haiku" else GPT4OMINI_OUT_DIR
    return base / f"{site}.json"


def _load_checkpoint(model: str, site: str) -> Optional[Dict]:
    p = _checkpoint_path(model, site)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def _save_checkpoint(model: str, site: str, data: Dict) -> None:
    p = _checkpoint_path(model, site)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, default=str))
    tmp.replace(p)


def _ref_urls_for_site(site: str) -> List[str]:
    p = REF_CORPUS_DIR / site / "urls.txt"
    if not p.exists():
        return []
    return [u for u in p.read_text().splitlines() if u.strip()]


def mode_full_pool(args) -> int:
    """Run dual-judge on all URLs in bench/reference_corpora/<site>/urls.txt
    for the 11 has_queries sites, with per-site checkpointing.

    Writes:
      bench/helpful_pages_haiku/<site>.json
      bench/helpful_pages_gpt4omini/<site>.json

    Each file maps url -> {classification, rationale_prefix, rationale_text,
    judged_at, judge_call_id}. Resumable: if a file exists, only un-judged
    URLs are processed.

    Cost is the dominant DS-2 spend (~$15 expected after caching). Caller
    should monitor cumulative spend and abort if it crosses $30.
    """
    import yaml
    pool = yaml.safe_load(POOL_PATH.read_text())
    target_sites = [s["name"] for s in pool["sites"] if s.get("has_queries")]
    if args.sites:
        wanted = {s.strip() for s in args.sites.split(",") if s.strip()}
        target_sites = [s for s in target_sites if s in wanted]
    if not target_sites:
        logger.error("No sites match filter; check pool config or --sites flag.")
        return 1

    prefix_block, suffix_template = load_prompt_blocks()
    haiku = _haiku_client()
    openai = _openai_client()
    gpt_model = resolve_gpt4omini_snapshot(openai)
    if not gpt_model:
        logger.error("gpt-4o-mini snapshot resolver returned None.")
        return 2

    model_specs = [("haiku", "haiku"), ("gpt4omini", "openai")]
    if getattr(args, "models", None):
        wanted = {m.strip() for m in args.models.split(",") if m.strip()}
        unknown = wanted - {"haiku", "gpt4omini"}
        if unknown:
            logger.error(f"Unknown --models entries: {sorted(unknown)} (valid: haiku, gpt4omini)")
            return 1
        model_specs = [ms for ms in model_specs if ms[0] in wanted]
    logger.info(f"Judge models this run: {[m for m, _ in model_specs]}")

    total_judged = 0
    total_cost = 0.0
    model_costs = {"haiku": 0.0, "gpt4omini": 0.0}

    for site in target_sites:
        ref_urls = _ref_urls_for_site(site)
        logger.info(f"\n=== {site}: {len(ref_urls)} URLs ===")
        cache = load_v14_cached_pages(site)

        # Site primary language for the mirror rule, from a cache sample.
        lang_counts: Dict[str, int] = {}
        for rec in list(cache.values())[:40]:
            lg = _detect_lang((rec.get("text") or "")[-1000:])
            if lg:
                lang_counts[lg] = lang_counts.get(lg, 0) + 1
        site_primary_lang = max(lang_counts, key=lang_counts.get) if lang_counts else "en"

        for model_name, judge_fn_kind in model_specs:
            ckpt = _load_checkpoint(model_name, site) or {}
            already = set(ckpt.keys())
            remaining = [u for u in ref_urls if u not in already]
            logger.info(f"  [{model_name}] {len(already)} done, {len(remaining)} remaining")

            for i, url in enumerate(remaining, 1):
                page = get_page_text(url, cache, allow_live_fetch=args.allow_live_fetch)
                if page is None:
                    ckpt[url] = {
                        "classification": "SKIPPED_NO_CONTENT",
                        "judged_at": _dt.datetime.now(_dt.UTC).isoformat(),
                    }
                    continue
                title, raw_text = page
                pre = deterministic_preclassify(
                    url, strip_nav_chrome(raw_text), raw_text, site_primary_lang)
                if pre:
                    ckpt[url] = {
                        "classification": pre[0],
                        "rationale_prefix": pre[1],
                        "rationale_text": pre[2],
                        "judged_at": _dt.datetime.now(_dt.UTC).isoformat(),
                        "judge_call_id": "deterministic-prefilter",
                    }
                    total_judged += 1
                    continue
                snippet = build_judge_snippet(raw_text)
                if len(snippet) < 100:
                    ckpt[url] = {
                        "classification": "SKIPPED_THIN_CONTENT",
                        "judged_at": _dt.datetime.now(_dt.UTC).isoformat(),
                    }
                    continue
                variable = format_suffix(suffix_template, url, title, snippet)
                try:
                    if judge_fn_kind == "haiku":
                        jr = call_haiku(haiku, prefix_block, variable)
                        h_in = jr.input_tokens or 0
                        h_out = jr.output_tokens or 0
                        h_cw = jr.cache_creation_input_tokens or 0
                        h_cr = jr.cache_read_input_tokens or 0
                        call_cost = _haiku_cost_per_call(h_in, h_out, h_cw, h_cr)
                        total_cost += call_cost
                        model_costs["haiku"] += call_cost
                    else:
                        full = prefix_block + "\n\n" + variable
                        jr, cached_in = call_gpt4omini_with_cache_meta(openai, gpt_model, full)
                        call_cost = _gpt4omini_cost_per_call(
                            jr.input_tokens or 0, jr.output_tokens or 0, cached_in
                        )
                        total_cost += call_cost
                        model_costs["gpt4omini"] += call_cost
                except RuntimeError as e:
                    logger.warning(f"    [{i}/{len(remaining)}] {url}: judge failed: {e}")
                    continue
                ckpt[url] = {
                    "classification": jr.classification,
                    "rationale_prefix": jr.rationale_prefix,
                    "rationale_text": jr.rationale_text,
                    "judged_at": jr.judged_at,
                    "judge_call_id": jr.judge_call_id,
                    "parse_warning": jr.parse_warning,
                }
                total_judged += 1
                if i % 50 == 0:
                    _save_checkpoint(model_name, site, ckpt)
                    logger.info(
                        f"    [{i}/{len(remaining)}] checkpoint; running cost ≈ ${total_cost:.2f}"
                    )
                    if total_cost > 30:
                        logger.error(f"Running cost ${total_cost:.2f} crossed $30 hard cap. Saving + aborting.")
                        _save_checkpoint(model_name, site, ckpt)
                        return 7
            _save_checkpoint(model_name, site, ckpt)
            logger.info(f"  [{model_name}] DONE. saved {len(ckpt)} entries.")

    logger.info(
        f"\nFull-pool complete. total_judged={total_judged} "
        f"EXACT SPEND ${total_cost:.4f} "
        f"(sonnet ${model_costs['haiku']:.4f} + gpt-4o-mini ${model_costs['gpt4omini']:.4f})"
    )
    return 0


# --- Pilot mode (--pilot) -------------------------------------------------


def _pilot_checkpoint_path(model: str, site: str) -> Path:
    """Pilot-specific checkpoint path (separate dir from full-pool)."""
    base = PILOT_PRIMARY_OUT_DIR if model == "primary" else PILOT_GPT4OMINI_OUT_DIR
    return base / f"{site}.json"


def _pilot_load_ckpt(model: str, site: str) -> Dict:
    p = _pilot_checkpoint_path(model, site)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def _pilot_save_ckpt(model: str, site: str, data: Dict) -> None:
    p = _pilot_checkpoint_path(model, site)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, default=str))
    tmp.replace(p)


def mode_pilot(args) -> int:
    """2-site cost-validation pilot (Sonnet 4.5 + gpt-4o-mini on rust-book +
    huggingface-transformers = 5,357 URLs).

    Per the 2026-05-13 chat.md authorization: validate that:
      (a) Sonnet 4.5 prompt caching fires at scale (cache_creation on cold,
          cache_read on warm calls; cumulative cache read share is high).
      (b) Per-page cost under cached steady state lands at the projected
          ~$0.00126/page (Sonnet) + $0.00019/page (gpt-4o-mini).
      (c) Full-pool extrapolation (× 33,316 URLs) stays under $50 hard cap.

    Outputs go to bench/helpful_pages_sonnet_pilot/<site>.json and
    bench/helpful_pages_gpt4omini_pilot/<site>.json (separate from eventual
    full-pool output dirs). Aggregate metrics + per-call cache metering are
    persisted to bench/pilot_v15_results.json.

    Cost cap: $10 (escalation if exceeded mid-run).

    Concurrency: --pilot-concurrency N (default 6). Both models per URL are
    fired in parallel; the threadpool keeps Anthropic's 5-minute ephemeral
    cache warm.
    """
    import concurrent.futures as cf
    import threading

    concurrency = max(1, min(int(getattr(args, "pilot_concurrency", 6)), 8))
    cost_cap = float(getattr(args, "pilot_cost_cap", PILOT_COST_CAP_USD))
    allow_live = bool(getattr(args, "allow_live_fetch", True))

    # --pilot-sites override (default: PILOT_SITES). Comma-separated subset;
    # each token must be a member of PILOT_SITES so we don't accidentally fire
    # the pilot judge against a site without checkpoint scaffolding.
    pilot_sites_arg = getattr(args, "pilot_sites", None)
    if pilot_sites_arg:
        requested = [s.strip() for s in pilot_sites_arg.split(",") if s.strip()]
        unknown = [s for s in requested if s not in PILOT_SITES]
        if unknown:
            logger.error(
                f"--pilot-sites contains unknown site(s) {unknown}; "
                f"valid options are {list(PILOT_SITES)}."
            )
            return 2
        sites_to_run = tuple(requested)
    else:
        sites_to_run = PILOT_SITES

    logger.info("=" * 60)
    logger.info("DS-2 PILOT — 2-site cost validation")
    logger.info("=" * 60)
    logger.info(f"Sites: {list(sites_to_run)}")
    logger.info(f"Concurrency: {concurrency}; cost cap: ${cost_cap:.2f}; live-fetch: {allow_live}")

    prefix_block, suffix_template = load_prompt_blocks()
    prompt_ver = f"{PROMPT_PATH.relative_to(REPO_ROOT)} (sha256: {prompt_sha256()[:16]}...)"
    anthropic_client = _anthropic_client()
    openai_client = _openai_client()
    gpt_model = resolve_gpt4omini_snapshot(openai_client)
    if not gpt_model:
        logger.error("gpt-4o-mini snapshot resolver returned None — aborting pilot.")
        return 2
    logger.info(f"Primary judge: {PRIMARY_JUDGE_MODEL}")
    logger.info(f"Secondary judge: {gpt_model}")
    logger.info(f"Prompt: {prompt_ver}")

    # Thread-safe running totals.
    lock = threading.Lock()
    abort_event = threading.Event()
    state = {
        "primary_input_total": 0,
        "primary_output_total": 0,
        "primary_cache_creation_total": 0,
        "primary_cache_read_total": 0,
        "primary_cost_total": 0.0,
        "primary_calls": 0,
        "primary_cache_hits": 0,    # calls where cache_read > 0
        "primary_cache_writes": 0,  # calls where cache_creation > 0
        "gpt_input_total": 0,
        "gpt_output_total": 0,
        "gpt_cached_input_total": 0,
        "gpt_cost_total": 0.0,
        "gpt_calls": 0,
        "agreements": 0,
        "comparisons": 0,
        "per_call_records": [],  # capped sample of per-call diagnostics
        "per_call_keep_first_n": 50,
    }

    started = time.time()

    def judge_one_url(site: str, url: str, cache: Dict, primary_ckpt: Dict, gpt_ckpt: Dict) -> Optional[Tuple[str, str]]:
        """Judge a single URL with both models in sequence within one worker.
        Updates state under lock. Returns (primary_classification, gpt_classification)
        or None on skip."""
        if abort_event.is_set():
            return None
        page = get_page_text(url, cache, allow_live_fetch=allow_live)
        if page is None:
            with lock:
                primary_ckpt[url] = {
                    "classification": "SKIPPED_NO_CONTENT",
                    "judged_at": _dt.datetime.now(_dt.UTC).isoformat(),
                }
                gpt_ckpt[url] = {
                    "classification": "SKIPPED_NO_CONTENT",
                    "judged_at": _dt.datetime.now(_dt.UTC).isoformat(),
                }
            return None
        title, raw_text = page
        snippet = build_judge_snippet(raw_text)
        if len(snippet) < 100:
            with lock:
                primary_ckpt[url] = {
                    "classification": "SKIPPED_THIN_CONTENT",
                    "judged_at": _dt.datetime.now(_dt.UTC).isoformat(),
                }
                gpt_ckpt[url] = {
                    "classification": "SKIPPED_THIN_CONTENT",
                    "judged_at": _dt.datetime.now(_dt.UTC).isoformat(),
                }
            return None

        variable = format_suffix(suffix_template, url, title, snippet)
        full_prompt = prefix_block + "\n\n" + variable

        # Primary (Sonnet 4.5) — cached.
        try:
            pr = call_primary_judge(anthropic_client, prefix_block, variable)
        except RuntimeError as e:
            logger.warning(f"  [{site}] primary failed for {url[:60]}: {e}")
            return None
        p_in = pr.input_tokens or 0
        p_out = pr.output_tokens or 0
        p_cw = pr.cache_creation_input_tokens or 0
        p_cr = pr.cache_read_input_tokens or 0
        p_cost = _primary_judge_cost_per_call(p_in, p_out, p_cw, p_cr)

        # Secondary (gpt-4o-mini) — auto-cached.
        try:
            gr, g_cached_in = call_gpt4omini_with_cache_meta(openai_client, gpt_model, full_prompt)
        except RuntimeError as e:
            logger.warning(f"  [{site}] gpt failed for {url[:60]}: {e}")
            return None
        g_in = gr.input_tokens or 0
        g_out = gr.output_tokens or 0
        g_cost = _gpt4omini_cost_per_call(g_in, g_out, g_cached_in)

        with lock:
            primary_ckpt[url] = {
                "classification": pr.classification,
                "rationale_prefix": pr.rationale_prefix,
                "rationale_text": pr.rationale_text,
                "judged_at": pr.judged_at,
                "judge_call_id": pr.judge_call_id,
                "parse_warning": pr.parse_warning,
                "input_tokens": p_in,
                "output_tokens": p_out,
                "cache_creation_input_tokens": p_cw,
                "cache_read_input_tokens": p_cr,
                "per_call_cost_usd": p_cost,
            }
            gpt_ckpt[url] = {
                "classification": gr.classification,
                "rationale_prefix": gr.rationale_prefix,
                "rationale_text": gr.rationale_text,
                "judged_at": gr.judged_at,
                "judge_call_id": gr.judge_call_id,
                "parse_warning": gr.parse_warning,
                "input_tokens": g_in,
                "output_tokens": g_out,
                "cached_input_tokens": g_cached_in,
                "per_call_cost_usd": g_cost,
            }

            state["primary_input_total"] += p_in
            state["primary_output_total"] += p_out
            state["primary_cache_creation_total"] += p_cw
            state["primary_cache_read_total"] += p_cr
            state["primary_cost_total"] += p_cost
            state["primary_calls"] += 1
            if p_cw > 0:
                state["primary_cache_writes"] += 1
            if p_cr > 0:
                state["primary_cache_hits"] += 1

            state["gpt_input_total"] += g_in
            state["gpt_output_total"] += g_out
            state["gpt_cached_input_total"] += g_cached_in
            state["gpt_cost_total"] += g_cost
            state["gpt_calls"] += 1

            if pr.classification in ("HELPFUL", "NON-HELPFUL") and gr.classification in ("HELPFUL", "NON-HELPFUL"):
                state["comparisons"] += 1
                if pr.classification == gr.classification:
                    state["agreements"] += 1

            if len(state["per_call_records"]) < state["per_call_keep_first_n"]:
                state["per_call_records"].append({
                    "site": site,
                    "url": url,
                    "primary": {
                        "input_tokens": p_in,
                        "output_tokens": p_out,
                        "cache_creation_input_tokens": p_cw,
                        "cache_read_input_tokens": p_cr,
                        "per_call_cost_usd": p_cost,
                        "classification": pr.classification,
                    },
                    "gpt4omini": {
                        "input_tokens": g_in,
                        "output_tokens": g_out,
                        "cached_input_tokens": g_cached_in,
                        "per_call_cost_usd": g_cost,
                        "classification": gr.classification,
                    },
                })

            running = state["primary_cost_total"] + state["gpt_cost_total"]
            if running > cost_cap:
                logger.error(f"  Cost cap exceeded: ${running:.4f} > ${cost_cap:.2f}; signaling abort.")
                abort_event.set()
        return (pr.classification, gr.classification)

    # Per-site loop, but URLs within a site are dispatched to a threadpool.
    for site in sites_to_run:
        if abort_event.is_set():
            break
        ref_urls = _ref_urls_for_site(site)
        logger.info(f"\n=== {site}: {len(ref_urls)} URLs ===")
        cache = load_v14_cached_pages(site)
        logger.info(f"  v1.4 cache contains {len(cache)} URLs; live-fetch enabled: {allow_live}")

        primary_ckpt = _pilot_load_ckpt("primary", site)
        gpt_ckpt = _pilot_load_ckpt("gpt4omini", site)
        already_primary = set(primary_ckpt.keys())
        already_gpt = set(gpt_ckpt.keys())
        # URL is "done" only if BOTH per-model checkpoints have it.
        remaining = [u for u in ref_urls if not (u in already_primary and u in already_gpt)]
        logger.info(f"  Already complete: {len(ref_urls)-len(remaining)}; remaining: {len(remaining)}")

        progress_counter = {"n": 0}
        progress_lock = threading.Lock()
        site_start = time.time()

        def submit_url(url: str):
            res = judge_one_url(site, url, cache, primary_ckpt, gpt_ckpt)
            with progress_lock:
                progress_counter["n"] += 1
                n = progress_counter["n"]
            if n % 50 == 0:
                with lock:
                    running = state["primary_cost_total"] + state["gpt_cost_total"]
                    cr = state["primary_cache_read_total"]
                    cw = state["primary_cache_creation_total"]
                    hits = state["primary_cache_hits"]
                    calls = state["primary_calls"]
                _pilot_save_ckpt("primary", site, primary_ckpt)
                _pilot_save_ckpt("gpt4omini", site, gpt_ckpt)
                elapsed = time.time() - site_start
                rate = n / elapsed if elapsed > 0 else 0
                hit_rate = (hits / calls * 100) if calls > 0 else 0
                logger.info(
                    f"  [{n}/{len(remaining)}] cost≈${running:.4f} "
                    f"cache_hits={hits}/{calls} ({hit_rate:.1f}%) "
                    f"cw_tot={cw} cr_tot={cr} "
                    f"rate={rate:.1f}/s"
                )
            return res

        with cf.ThreadPoolExecutor(max_workers=concurrency) as ex:
            futures = [ex.submit(submit_url, u) for u in remaining]
            for f in cf.as_completed(futures):
                if abort_event.is_set():
                    # Drain remaining futures cleanly (don't kill mid-call).
                    for ff in futures:
                        ff.cancel()
                    break
                try:
                    f.result()
                except Exception as e:
                    logger.warning(f"  worker exception: {e}")

        _pilot_save_ckpt("primary", site, primary_ckpt)
        _pilot_save_ckpt("gpt4omini", site, gpt_ckpt)
        logger.info(f"  {site}: primary saved {len(primary_ckpt)} entries; gpt saved {len(gpt_ckpt)} entries.")

    elapsed_total = time.time() - started

    # Aggregate + write results.
    primary_calls = state["primary_calls"]
    gpt_calls = state["gpt_calls"]
    primary_cost = state["primary_cost_total"]
    gpt_cost = state["gpt_cost_total"]
    total_cost = primary_cost + gpt_cost
    cache_writes = state["primary_cache_writes"]
    cache_hits = state["primary_cache_hits"]
    hit_rate_pct = (cache_hits / primary_calls * 100) if primary_calls > 0 else 0.0
    agreement_pct = (state["agreements"] / state["comparisons"] * 100) if state["comparisons"] > 0 else 0.0

    avg_primary_cost = (primary_cost / primary_calls) if primary_calls > 0 else 0.0
    avg_gpt_cost = (gpt_cost / gpt_calls) if gpt_calls > 0 else 0.0
    avg_combined_cost = avg_primary_cost + avg_gpt_cost

    # Cached-steady-state per-page cost (excludes write calls; better extrapolation).
    if cache_hits > 0:
        # Re-derive per-read cost from totals minus the cache_creation share.
        # On read calls, input_tokens is small (just Block 2) and cache_creation=0.
        # We approximate steady-state as: avg primary cost across cache_hit calls only.
        # Without per-call cost stratified by hit/miss, use total minus the writes' premium.
        # Conservative: assume each cache write was ~25% premium over what a read would cost.
        steady_primary_per_call = (
            (primary_cost - cache_writes * (avg_primary_cost * 0.25))
            / max(primary_calls, 1)
        )
    else:
        steady_primary_per_call = avg_primary_cost

    # Full-pool projection — use AVG per-call cost (includes the amortized write cost,
    # since the full pool will likewise have periodic cache rewrites every ~5 min TTL).
    projected_full_pool = avg_combined_cost * PILOT_FULL_POOL_UNIVERSE_SIZE

    results = {
        "started_at": _dt.datetime.now(_dt.UTC).isoformat(),
        "pilot_sites": list(sites_to_run),
        "primary_judge_model": PRIMARY_JUDGE_MODEL,
        "gpt4omini_model_version": gpt_model,
        "judge_prompt_version": prompt_ver,
        "concurrency": concurrency,
        "cost_cap_usd": cost_cap,
        "aborted_mid_run": abort_event.is_set(),
        "wall_clock_seconds": round(elapsed_total, 1),
        "primary": {
            "calls": primary_calls,
            "cache_writes": cache_writes,
            "cache_hits": cache_hits,
            "cache_hit_rate_pct": round(hit_rate_pct, 2),
            "input_tokens_total_noncached": state["primary_input_total"],
            "output_tokens_total": state["primary_output_total"],
            "cache_creation_tokens_total": state["primary_cache_creation_total"],
            "cache_read_tokens_total": state["primary_cache_read_total"],
            "cost_total_usd": round(primary_cost, 4),
            "cost_per_page_avg_usd": round(avg_primary_cost, 6),
            "cost_per_page_steady_state_usd": round(steady_primary_per_call, 6),
        },
        "gpt4omini": {
            "calls": gpt_calls,
            "input_tokens_total": state["gpt_input_total"],
            "output_tokens_total": state["gpt_output_total"],
            "cached_input_tokens_total": state["gpt_cached_input_total"],
            "cost_total_usd": round(gpt_cost, 4),
            "cost_per_page_avg_usd": round(avg_gpt_cost, 6),
        },
        "combined": {
            "cost_total_usd": round(total_cost, 4),
            "cost_per_page_avg_usd": round(avg_combined_cost, 6),
        },
        "inter_model_agreement_pct": round(agreement_pct, 2),
        "comparisons_with_both_classified": state["comparisons"],
        "projection": {
            "full_pool_universe_size": PILOT_FULL_POOL_UNIVERSE_SIZE,
            "projected_full_pool_usd": round(projected_full_pool, 2),
            "escalation_threshold_usd": 50.0,
            "expected_option_e_usd": 42.0,
            "verdict": (
                "PASS_PROCEED_FULL_POOL" if projected_full_pool <= 45
                else "MARGINAL_PAULSAVE_DECIDE" if projected_full_pool <= 50
                else "FAIL_ESCALATE"
            ),
        },
        "sample_per_call_records": state["per_call_records"],
        "anthropic_sonnet45_pricing_per_million": {
            "input": 3.00,
            "output": 15.00,
            "cache_creation_5m": 3.75,
            "cache_read": 0.30,
        },
        "gpt4omini_pricing_per_million": {
            "input": 0.15,
            "output": 0.60,
            "cached_input": 0.075,
        },
    }
    PILOT_RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PILOT_RESULTS_PATH.write_text(json.dumps(results, indent=2, default=str))

    logger.info("")
    logger.info("=" * 60)
    logger.info("PILOT RESULTS")
    logger.info("=" * 60)
    logger.info(f"Wall clock: {elapsed_total:.1f} s")
    logger.info(f"Primary calls: {primary_calls} (cache writes={cache_writes}, hits={cache_hits}, hit-rate={hit_rate_pct:.1f}%)")
    logger.info(f"  total cost: ${primary_cost:.4f}  avg/call: ${avg_primary_cost:.6f}  steady-state: ${steady_primary_per_call:.6f}")
    logger.info(f"gpt-4o-mini calls: {gpt_calls}")
    logger.info(f"  total cost: ${gpt_cost:.4f}  avg/call: ${avg_gpt_cost:.6f}")
    logger.info(f"Combined per-page: ${avg_combined_cost:.6f}")
    logger.info(f"Inter-model agreement: {agreement_pct:.2f}% ({state['agreements']}/{state['comparisons']})")
    logger.info("")
    logger.info(f"Pilot spend total:                  ${total_cost:.4f}  (cap ${cost_cap:.2f})")
    logger.info(f"Full-pool projection (× {PILOT_FULL_POOL_UNIVERSE_SIZE:,}): ${projected_full_pool:.2f}")
    logger.info(f"Verdict: {results['projection']['verdict']}")
    logger.info(f"Results persisted: {PILOT_RESULTS_PATH.relative_to(REPO_ROOT)}")

    return 0 if not abort_event.is_set() else 8


# --- Merge mode (--merge) -------------------------------------------------


def mode_merge(args) -> int:
    """Merge per-model JSONs into canonical bench/helpful_pages/<site>.json
    + bench/helpful_pages_disagreement.csv. Updates universe_manifest with
    DS-2 populated fields.

    Canonical pick: read from universe_manifest.canonical_judge_model
    (written by --calibration). If absent, defaults to 'haiku'.
    """
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text())
    else:
        manifest = {}
    canonical = manifest.get("canonical_judge_model", "haiku")
    other = "gpt4omini" if canonical == "haiku" else "haiku"
    logger.info(f"Canonical model: {canonical}; sibling: {other}")

    CANONICAL_OUT_DIR.mkdir(parents=True, exist_ok=True)
    disagreement_rows: List[dict] = []
    helpful_counts = {}

    import yaml
    pool = yaml.safe_load(POOL_PATH.read_text())
    target_sites = [s["name"] for s in pool["sites"] if s.get("has_queries")]

    for site in target_sites:
        haiku_ck = _load_checkpoint("haiku", site) or {}
        gpt_ck = _load_checkpoint("gpt4omini", site) or {}
        if not haiku_ck and not gpt_ck:
            logger.warning(f"  {site}: no checkpoints — skipping")
            continue
        canonical_ck = haiku_ck if canonical == "haiku" else gpt_ck
        sibling_ck = gpt_ck if canonical == "haiku" else haiku_ck

        # Build canonical helpful-pages dict.
        helpful_for_site = {}
        helpful_n = 0
        nonhelpful_n = 0
        skipped_n = 0
        for url, payload in canonical_ck.items():
            cls = payload.get("classification", "")
            if cls == "HELPFUL":
                helpful_for_site[url] = payload
                helpful_n += 1
            elif cls == "NON-HELPFUL":
                nonhelpful_n += 1
            else:
                skipped_n += 1
        out_path = CANONICAL_OUT_DIR / f"{site}.json"
        out_path.write_text(json.dumps({
            "site": site,
            "canonical_judge_model": canonical,
            "total_urls": len(canonical_ck),
            "helpful_count": helpful_n,
            "non_helpful_count": nonhelpful_n,
            "skipped_count": skipped_n,
            "helpful_pages": helpful_for_site,
        }, indent=2, default=str))
        helpful_counts[site] = {"helpful": helpful_n, "non_helpful": nonhelpful_n, "skipped": skipped_n}
        logger.info(f"  {site}: helpful={helpful_n} non_helpful={nonhelpful_n} skipped={skipped_n}")

        # Disagreement rows.
        for url, c_payload in canonical_ck.items():
            s_payload = sibling_ck.get(url)
            if not s_payload:
                continue
            c_cls = c_payload.get("classification", "")
            s_cls = s_payload.get("classification", "")
            if c_cls != s_cls and c_cls in ("HELPFUL", "NON-HELPFUL") and s_cls in ("HELPFUL", "NON-HELPFUL"):
                disagreement_rows.append({
                    "site": site,
                    "url": url,
                    f"{canonical}_classification": c_cls,
                    f"{canonical}_rationale_prefix": c_payload.get("rationale_prefix", ""),
                    f"{other}_classification": s_cls,
                    f"{other}_rationale_prefix": s_payload.get("rationale_prefix", ""),
                })

    # Write disagreement CSV.
    if disagreement_rows:
        fields = list(disagreement_rows[0].keys())
        with open(DISAGREEMENT_CSV, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for r in disagreement_rows:
                w.writerow(r)
        logger.info(f"Disagreement rows: {len(disagreement_rows)} → {DISAGREEMENT_CSV.relative_to(REPO_ROOT)}")
    else:
        logger.info("No disagreement rows written (no overlap or perfect agreement).")

    # Manifest DS-2 fields.
    manifest.setdefault("sites", {})
    total_helpful = 0
    for site, counts in helpful_counts.items():
        manifest["sites"].setdefault(site, {})
        manifest["sites"][site]["helpful_count"] = counts["helpful"]
        manifest["sites"][site]["non_helpful_count"] = counts["non_helpful"]
        manifest["sites"][site]["skipped_count"] = counts["skipped"]
        total_helpful += counts["helpful"]
    manifest["total_helpful_pages"] = total_helpful
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    logger.info(f"Manifest updated with DS-2 fields. total_helpful_pages={total_helpful}")
    return 0


# --- Sanity-confidence mode (--sanity-confidence) -------------------------


def mode_sanity_confidence(args) -> int:
    """R-A confidence proxy: 20 URLs/site × 11 sites × 2 calls (canonical
    model only) = 440 calls. URLs where the two calls disagree are flagged
    as low-confidence.

    Writes bench/confidence_sample_v15.csv with one row per URL:
      site, url, call_1, call_2, disagreed (bool)
    """
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text())
    else:
        manifest = {}
    canonical = manifest.get("canonical_judge_model", "haiku")
    logger.info(f"Confidence proxy via canonical model: {canonical}")

    import yaml
    pool = yaml.safe_load(POOL_PATH.read_text())
    target_sites = [s["name"] for s in pool["sites"] if s.get("has_queries")]

    rng = random.Random(7919)  # distinct seed for confidence proxy
    prefix_block, suffix_template = load_prompt_blocks()
    haiku = _haiku_client()
    openai = _openai_client()
    gpt_model = resolve_gpt4omini_snapshot(openai) if canonical == "gpt4omini" else None

    out_rows = []
    for site in target_sites:
        # Sample 20 URLs from the canonical model's helpful_pages set.
        canon_ck = _load_checkpoint(canonical, site) or {}
        # Restrict to URLs with a real classification (not SKIPPED_*).
        scored = [u for u, p in canon_ck.items() if p.get("classification") in ("HELPFUL", "NON-HELPFUL")]
        if not scored:
            logger.warning(f"  {site}: no canonical scores — skipping")
            continue
        sample = rng.sample(scored, min(20, len(scored)))
        cache = load_v14_cached_pages(site)
        logger.info(f"  {site}: sampling {len(sample)} URLs for confidence proxy")

        for url in sample:
            page = get_page_text(url, cache, allow_live_fetch=False)
            if page is None:
                continue
            title, raw_text = page
            snippet = build_judge_snippet(raw_text)
            if len(snippet) < 100:
                continue
            variable = format_suffix(suffix_template, url, title, snippet)

            try:
                if canonical == "haiku":
                    call_1 = call_haiku(haiku, prefix_block, variable).classification
                    call_2 = call_haiku(haiku, prefix_block, variable).classification
                else:
                    full = prefix_block + "\n\n" + variable
                    call_1 = call_gpt4omini(openai, gpt_model, full).classification
                    call_2 = call_gpt4omini(openai, gpt_model, full).classification
            except RuntimeError as e:
                logger.warning(f"    {url}: failed: {e}")
                continue
            out_rows.append({
                "site": site,
                "url": url,
                "call_1": call_1,
                "call_2": call_2,
                "disagreed": call_1 != call_2,
            })

    out_path = REPO_ROOT / "bench" / "confidence_sample_v15.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["site", "url", "call_1", "call_2", "disagreed"])
        w.writeheader()
        for r in out_rows:
            w.writerow(r)
    n_dis = sum(1 for r in out_rows if r["disagreed"])
    logger.info(f"\nConfidence sample: {len(out_rows)} URLs; {n_dis} ({n_dis/max(len(out_rows),1)*100:.1f}%) disagreed.")
    logger.info(f"Written: {out_path.relative_to(REPO_ROOT)}")
    return 0


# --- methodology_validation.md scaffold ----------------------------------


def write_methodology_validation_scaffold() -> Path:
    """Create reports/methodology_validation.md with per-section templates.

    Populated by --calibration + --merge runs (some sections inline; others
    via manual narrative once SC-3 gates pass and full-pool is complete).
    """
    path = REPO_ROOT / "reports" / "methodology_validation.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return path  # never overwrite an existing report
    template = """# Methodology validation — v1.5

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
"""
    path.write_text(template)
    return path


# --- CLI ------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sanity-check",
        action="store_true",
        help="Run the dual 10-page sanity check (FIRST action of DS-2).",
    )
    parser.add_argument(
        "--build-calibration-scaffold",
        action="store_true",
        help="Build empty ground-truth CSV (4 sites × 100 URLs) for paulsave's hand-judging.",
    )
    parser.add_argument(
        "--calibration",
        action="store_true",
        help="Run 3x-call dual calibration vs hand-judged ground truth; "
             "compute SC-3 gates; pick canonical model.",
    )
    parser.add_argument(
        "--full-pool",
        action="store_true",
        help="Run dual-judge on all 33,316 reference URLs with per-site checkpoints.",
    )
    parser.add_argument(
        "--pilot",
        action="store_true",
        help="2-site cost-validation pilot (Sonnet 4.5 + gpt-4o-mini on rust-book "
             "+ huggingface-transformers, 5,357 URLs). Per chat.md 2026-05-13.",
    )
    parser.add_argument(
        "--pilot-concurrency",
        type=int,
        default=6,
        help="Concurrent worker count for --pilot (range 1-8, default 6).",
    )
    parser.add_argument(
        "--pilot-cost-cap",
        type=float,
        default=PILOT_COST_CAP_USD,
        help=f"Pilot cost cap in USD (default ${PILOT_COST_CAP_USD:.2f}).",
    )
    parser.add_argument(
        "--pilot-sites",
        default=None,
        help="Comma-separated subset of pilot sites to run "
             f"(default all of {list(PILOT_SITES)}). Each token must be a "
             "member of PILOT_SITES. Useful for re-running a single site "
             "(e.g. --pilot-sites rust-book) after a prompt iteration.",
    )
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Merge per-model JSONs into canonical bench/helpful_pages/ + disagreement CSV.",
    )
    parser.add_argument(
        "--sanity-confidence",
        action="store_true",
        help="R-A confidence proxy: 20 URLs/site × 11 sites × 2 calls (canonical model).",
    )
    parser.add_argument(
        "--write-methodology-scaffold",
        action="store_true",
        help="Create reports/methodology_validation.md template (idempotent; never overwrites).",
    )
    parser.add_argument(
        "--sites",
        default=None,
        help="Comma-separated subset of site names (for --full-pool).",
    )
    parser.add_argument(
        "--models",
        default=None,
        help="For --full-pool: comma-separated subset of judge models to run "
             "(valid: haiku, gpt4omini; default both). Single-model runs "
             "support the calibration-gated cheap-judge path (e.g. "
             "--models gpt4omini at ~$7 vs ~$100 dual).",
    )
    parser.add_argument(
        "--allow-live-fetch",
        action="store_true",
        help="For --full-pool: allow live HTTP fetch on cache miss "
             "(default off; sitemap-sourced sites need this).",
    )
    parser.add_argument(
        "--cached",
        dest="cached",
        action="store_true",
        default=True,
        help="(default) Use v3 prompt + Anthropic cache_control for --sanity-check.",
    )
    parser.add_argument(
        "--no-cached",
        dest="cached",
        action="store_false",
        help="Disable cache_control (writes to bench/sanity_check_v15.json, "
             "the pre-caching baseline path).",
    )
    args = parser.parse_args()

    if args.sanity_check:
        return mode_sanity_check(args)
    if args.build_calibration_scaffold:
        return mode_build_calibration_scaffold(args)
    if args.calibration:
        return mode_calibration(args)
    if args.full_pool:
        return mode_full_pool(args)
    if args.pilot:
        return mode_pilot(args)
    if args.merge:
        return mode_merge(args)
    if args.sanity_confidence:
        return mode_sanity_confidence(args)
    if args.write_methodology_scaffold:
        p = write_methodology_validation_scaffold()
        logger.info(f"Wrote {p.relative_to(REPO_ROOT)}")
        return 0
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
