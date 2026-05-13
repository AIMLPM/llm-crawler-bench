#!/usr/bin/env python3
"""DS-2 (v1.5): Dual-model helpful-pages judge.

Classifies each URL in the v1.5 reference corpora as `helpful` or
`non-helpful` for RAG query generation, using TWO independent judge
models (primary Haiku + secondary gpt-4o-mini) with the same model-
agnostic prompt at `specs/v15-judge-prompt-v1.md`.

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
import os
import random
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field, asdict
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

PROMPT_PATH = REPO_ROOT / "specs" / "v15-judge-prompt-v1.md"
MANIFEST_PATH = REPO_ROOT / "bench" / "universe_manifest.json"

# Output directories per spec DS-2 (per-model files + merged canonical).
HAIKU_OUT_DIR = REPO_ROOT / "bench" / "helpful_pages_haiku"
GPT4OMINI_OUT_DIR = REPO_ROOT / "bench" / "helpful_pages_gpt4omini"
CANONICAL_OUT_DIR = REPO_ROOT / "bench" / "helpful_pages"
DISAGREEMENT_CSV = REPO_ROOT / "bench" / "helpful_pages_disagreement.csv"

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

# Model versions (per spec resolved decisions Q2 + R-E snapshot resolver).
HAIKU_MODEL = "claude-haiku-4-5-20251001"  # pinned, drift assertion fires on mismatch
GPT4OMINI_FAMILY_PREFIX = "gpt-4o-mini-"   # resolver picks latest GA snapshot

# HTTP fetch (for sitemap-source calibration sites lacking v1.4 cache).
USER_AGENT = "bench-agent-v1.5/1.0 (+https://github.com/AIMLPM/llm-crawler-benchmarks)"
REQUEST_TIMEOUT_S = 15
FETCH_POLITENESS_S = 0.5

# Two-line judge output regex (tolerant to whitespace + case).
HELPFUL_PATTERN = re.compile(r"^\s*(HELPFUL|NON[\-\s]?HELPFUL)\s*$", re.I)
RATIONALE_PATTERN = re.compile(
    r"^\s*(helpful-(?:docs|article|reference|howto|other)|"
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


# --- Prompt loader --------------------------------------------------------


def load_prompt_template() -> str:
    """Extract the model-agnostic prompt body from the spec artifact.

    The artifact contains the prompt inside a fenced code block following
    the 'Prompt body' heading. Returns the prompt with `{url}`, `{title}`,
    `{content}` placeholders intact."""
    text = PROMPT_PATH.read_text()
    # Find the first ``` ... ``` block after the prompt-body heading.
    m = re.search(r"## Prompt body.*?```\s*\n(.*?)\n```", text, re.DOTALL)
    if not m:
        raise SystemExit(
            f"Could not extract prompt body from {PROMPT_PATH}. "
            "Update load_prompt_template() if the spec format changed."
        )
    return m.group(1)


def prompt_sha256() -> str:
    return hashlib.sha256(PROMPT_PATH.read_bytes()).hexdigest()


def format_prompt(template: str, url: str, title: str, content: str) -> str:
    """Substitute placeholders. The prompt expects raw {url}/{title}/{content}
    tokens — DO NOT use str.format because the prompt body contains literal
    JSON / regex braces that would break .format()."""
    out = template.replace("{url}", url)
    out = out.replace("{title}", title)
    out = out.replace("{content}", content)
    return out


# --- API clients ----------------------------------------------------------


def _haiku_client():
    import anthropic
    return anthropic.Anthropic()


def _openai_client():
    from openai import OpenAI
    return OpenAI()


def resolve_gpt4omini_snapshot(client) -> Optional[str]:
    """R-E: pick the most-recent `gpt-4o-mini-*` GA snapshot via
    client.models.list(). Returns None if no snapshot available
    (escape-hatch path → SC-14 records `blocked — gpt-4o-mini snapshot
    unavailable`)."""
    try:
        models = client.models.list()
    except Exception as e:
        logger.warning(f"OpenAI models.list() failed: {e}")
        return None
    candidates = [
        m.id for m in models.data
        if m.id.startswith(GPT4OMINI_FAMILY_PREFIX)
    ]
    if not candidates:
        return None
    # Snapshot IDs include date suffix (e.g., gpt-4o-mini-2024-07-18);
    # sort lexically descending picks the most recent.
    return sorted(candidates, reverse=True)[0]


def call_haiku(client, prompt: str) -> JudgeResult:
    """Haiku single-call with retries. Returns JudgeResult."""
    last_err = None
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=HAIKU_MODEL,
                max_tokens=200,
                temperature=0,
                messages=[{"role": "user", "content": prompt}],
            )
            text = resp.content[0].text if resp.content else ""
            return _parse_response(
                raw_response=text,
                judge_call_id=resp.id,
                input_tokens=getattr(resp.usage, "input_tokens", None),
                output_tokens=getattr(resp.usage, "output_tokens", None),
            )
        except Exception as e:
            last_err = e
            if attempt < 2:
                time.sleep(2 ** attempt * 2)
    raise RuntimeError(f"Haiku call failed after 3 attempts: {last_err}")


def call_gpt4omini(client, model_id: str, prompt: str) -> JudgeResult:
    """gpt-4o-mini single-call with retries. Model ID is the resolved
    snapshot (R-E)."""
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
            return _parse_response(
                raw_response=text,
                judge_call_id=resp.id,
                input_tokens=resp.usage.prompt_tokens if resp.usage else None,
                output_tokens=resp.usage.completion_tokens if resp.usage else None,
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
                r"(helpful-(?:docs|article|reference|howto|other)|"
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


def mode_sanity_check(args) -> int:
    """Dual 10-page sanity check (FIRST action of DS-2 per spec)."""
    logger.info("=" * 60)
    logger.info("DS-2 SANITY CHECK — dual 10-page validation")
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

    template = load_prompt_template()
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
    haiku_tokens_in = haiku_tokens_out = 0
    gpt_tokens_in = gpt_tokens_out = 0
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
        prompt = format_prompt(template, url, title, text_capped)

        try:
            haiku_r = call_haiku(haiku, prompt)
        except RuntimeError as e:
            logger.error(f"  [{i}/{len(sample)}] Haiku failed: {e}")
            continue
        try:
            gpt_r = call_gpt4omini(openai, gpt4omini_model, prompt)
        except RuntimeError as e:
            logger.error(f"  [{i}/{len(sample)}] gpt-4o-mini failed: {e}")
            continue

        if haiku_r.input_tokens:
            haiku_tokens_in += haiku_r.input_tokens
            haiku_tokens_out += haiku_r.output_tokens or 0
        if gpt_r.input_tokens:
            gpt_tokens_in += gpt_r.input_tokens
            gpt_tokens_out += gpt_r.output_tokens or 0
        if haiku_r.parse_warning:
            haiku_parse_warnings += 1
        if gpt_r.parse_warning:
            gpt_parse_warnings += 1

        agree = haiku_r.classification == gpt_r.classification
        agreement_marker = "==" if agree else "!="
        logger.info(
            f"  [{i}/{len(sample)}] {url[:60]:<60s} "
            f"haiku={haiku_r.classification:<12s} "
            f"{agreement_marker} gpt={gpt_r.classification:<12s}"
            f"{' [WARN]' if (haiku_r.parse_warning or gpt_r.parse_warning) else ''}"
        )
        results.append({
            "url": url,
            "title": title,
            "haiku": asdict(haiku_r),
            "gpt4omini": asdict(gpt_r),
            "agreement": agree,
        })

    # Cost projection per spec — Haiku $0.80/1M input, $4.00/1M output; gpt-4o-mini $0.15/1M in, $0.60/1M out.
    n_judged = len(results)
    if n_judged == 0:
        logger.error("Zero pages judged — sanity check failed.")
        return 2
    avg_haiku_in = haiku_tokens_in / n_judged
    avg_haiku_out = haiku_tokens_out / n_judged
    avg_gpt_in = gpt_tokens_in / n_judged
    avg_gpt_out = gpt_tokens_out / n_judged
    haiku_cost_per_page = (avg_haiku_in * 0.80 + avg_haiku_out * 4.00) / 1_000_000
    gpt_cost_per_page = (avg_gpt_in * 0.15 + avg_gpt_out * 0.60) / 1_000_000
    total_cost_per_page = haiku_cost_per_page + gpt_cost_per_page
    universe_size = 53_316  # from D1 outcome
    projected_full_pool = total_cost_per_page * universe_size

    logger.info("")
    logger.info("=" * 60)
    logger.info("SANITY CHECK RESULTS")
    logger.info("=" * 60)
    logger.info(f"Pages judged successfully:           {n_judged} / {SANITY_CHECK_N}")
    logger.info(f"Haiku parse warnings (non-strict):   {haiku_parse_warnings}")
    logger.info(f"gpt-4o-mini parse warnings:          {gpt_parse_warnings}")
    inter_agree = sum(1 for r in results if r["agreement"]) / n_judged * 100
    logger.info(f"Inter-model agreement (10-page):     {inter_agree:.1f}%")
    logger.info("")
    logger.info(f"Haiku avg tokens:        {avg_haiku_in:.0f} in / {avg_haiku_out:.0f} out")
    logger.info(f"gpt-4o-mini avg tokens:  {avg_gpt_in:.0f} in / {avg_gpt_out:.0f} out")
    logger.info(f"Haiku per-page cost:        ${haiku_cost_per_page:.6f}")
    logger.info(f"gpt-4o-mini per-page cost:  ${gpt_cost_per_page:.6f}")
    logger.info(f"Combined per-page cost:     ${total_cost_per_page:.6f}")
    logger.info(f"Projected full-pool cost (~53k URLs): ${projected_full_pool:.2f}")
    logger.info(f"Budget cap: $30  |  Hard escalation: $36 (>20% over cap)")
    logger.info("")

    # Format-compliance gate per spec DS-2.
    if gpt_parse_warnings > 1:  # >10% of 10 fails
        logger.error(
            f"gpt-4o-mini parse warnings = {gpt_parse_warnings} / 10 — "
            "format-compliance gate FAILED (>10% threshold)."
        )
        logger.error("ESCALATE to chat.md before proceeding to calibration.")
        return 3
    # Cost-projection gate per spec DS-2.
    if projected_full_pool > 36:
        logger.error(
            f"Projected full-pool ${projected_full_pool:.2f} > $36 cap-plus-20% — "
            "cost-projection gate FAILED."
        )
        logger.error("ESCALATE to chat.md before proceeding to calibration.")
        return 4

    # Persist results for the chat.md confirmation.
    out_path = REPO_ROOT / "bench" / "sanity_check_v15_dual.json"
    out_path.write_text(json.dumps({
        "started_at": _dt.datetime.now(_dt.UTC).isoformat(),
        "site": SANITY_CHECK_SITE,
        "n_sampled": SANITY_CHECK_N,
        "n_judged": n_judged,
        "haiku_model_version": HAIKU_MODEL,
        "gpt4omini_model_version": gpt4omini_model,
        "judge_prompt_version": prompt_ver,
        "inter_model_agreement_pct": round(inter_agree, 2),
        "haiku_parse_warnings": haiku_parse_warnings,
        "gpt4omini_parse_warnings": gpt_parse_warnings,
        "haiku_avg_tokens": {"input": round(avg_haiku_in), "output": round(avg_haiku_out)},
        "gpt4omini_avg_tokens": {"input": round(avg_gpt_in), "output": round(avg_gpt_out)},
        "cost_per_page": {
            "haiku": round(haiku_cost_per_page, 6),
            "gpt4omini": round(gpt_cost_per_page, 6),
            "combined": round(total_cost_per_page, 6),
        },
        "projected_full_pool_usd": round(projected_full_pool, 2),
        "gates": {"format_compliance": "PASS", "cost_projection": "PASS"},
        "results": results,
    }, indent=2, default=str))
    logger.info(f"Sanity check results: {out_path.relative_to(REPO_ROOT)}")
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
            snippet = strip_nav_chrome(text or "")[:MAX_CONTENT_CHARS]
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
            snippet = strip_nav_chrome(text or "")[:MAX_CONTENT_CHARS]
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
    args = parser.parse_args()

    if args.sanity_check:
        return mode_sanity_check(args)
    if args.build_calibration_scaffold:
        return mode_build_calibration_scaffold(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
