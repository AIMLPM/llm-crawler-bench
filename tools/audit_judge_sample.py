#!/usr/bin/env python3
"""v1.5 DS-2 audit: re-judge a sample of the gpt-4o-mini universe with Sonnet.

Why this exists. SC-3 calibration (2026-08-17, round 3) cleared Sonnet on
every gate but left gpt-4o-mini failing the per-class NON-HELPFUL gate
(13/20) while posting the best per-site agreement (97/99/95). The owner
chose the affordable path: mini judges the full pool, and Sonnet audits a
sample to BOUND mini's over-inclusion rather than leave it assumed.

Two strata, never pooled:

  A. UNBIASED — proportional random sample across sites x mini-class.
     This is the only stratum the headline over-inclusion estimate is
     computed from, so the number generalizes to the universe.

  B. TARGETED — URL patterns the rubric calls NON-HELPFUL that mini is
     known to over-include (source viewers, _sources dumps, generated
     API index pages). Reported SEPARATELY as a worst-case probe; folding
     it into A would inflate the estimate by construction.

Sonnet sees the identical pipeline mini saw (Stage-2a prefilter, then the
same prompt + snippet builder), so a disagreement is a judge disagreement
and not a plumbing artifact.

Usage:
    .venv/bin/python tools/audit_judge_sample.py --dry-run
    .venv/bin/python tools/audit_judge_sample.py --n 1000
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.judge_helpful_pages import (  # noqa: E402
    GPT4OMINI_OUT_DIR,
    _detect_lang,
    _haiku_client,
    _haiku_cost_per_call,
    build_judge_snippet,
    call_haiku,
    deterministic_preclassify,
    format_suffix,
    get_page_text,
    load_prompt_blocks,
    load_v14_cached_pages,
    strip_nav_chrome,
)

AUDIT_SEED = 42
OUT_JSON = ROOT / "bench" / "audit_sonnet_sample_v15.json"
OUT_MD = ROOT / "bench" / "audit_sonnet_sample_v15.md"

# Stratum-B patterns: rubric-NON-HELPFUL shapes mini demonstrably passes.
TARGETED_PATTERNS = ("/_modules/", "/_sources/", "/src/", "/genindex",
                     "/py-modindex", "/modindex", "/search")
TARGETED_FRACTION = 0.2  # cap; stratum B is usually smaller (few such pages
                         # survive fetching), and the unused budget goes to A

JUDGED = {"HELPFUL", "NON-HELPFUL"}


def load_universe() -> dict[str, dict]:
    """{site: {url: record}} for every completed mini checkpoint."""
    out = {}
    for f in sorted(GPT4OMINI_OUT_DIR.glob("*.json")):
        out[f.stem] = json.loads(f.read_text())
    return out


def pick_sample(universe: dict[str, dict], n: int) -> tuple[list, list]:
    rng = random.Random(AUDIT_SEED)

    # --- Stratum B first: it is supply-limited, so A absorbs the remainder ---
    pool_b = [
        (site, url, rec["classification"])
        for site, recs in universe.items()
        for url, rec in recs.items()
        if rec.get("classification") == "HELPFUL"
        and any(p in url for p in TARGETED_PATTERNS)
    ]
    stratum_b = rng.sample(pool_b, min(int(n * TARGETED_FRACTION), len(pool_b)))
    b_urls = {u for _, u, _ in stratum_b}
    n_unbiased = n - len(stratum_b)

    # --- Stratum A: proportional across site x class ---
    pool_a = [
        (site, url, rec["classification"])
        for site, recs in universe.items()
        for url, rec in recs.items()
        if rec.get("classification") in JUDGED and url not in b_urls
    ]
    # Proportional allocation by (site, class) preserves universe shape;
    # every cell keeps >=1 row so tiny sites/classes stay representable.
    cells = defaultdict(list)
    for site, url, cls in pool_a:
        cells[(site, cls)].append((site, url, cls))
    total = len(pool_a)
    stratum_a = []
    for cell, rows in sorted(cells.items()):
        take = max(1, round(n_unbiased * len(rows) / total))
        stratum_a.extend(rng.sample(rows, min(take, len(rows))))
    rng.shuffle(stratum_a)
    stratum_a = stratum_a[:n_unbiased]

    return stratum_a, stratum_b


def rejudge(rows: list, label: str, client, prefix_block, suffix_template) -> tuple[list, float]:
    """Re-judge rows with Sonnet through the same pipeline mini used."""
    results, cost = [], 0.0
    caches: dict[str, dict] = {}
    langs: dict[str, str] = {}
    for i, (site, url, mini_cls) in enumerate(rows, 1):
        if site not in caches:
            caches[site] = load_v14_cached_pages(site)
            counts: Counter = Counter()
            for rec in list(caches[site].values())[:40]:
                lg = _detect_lang((rec.get("text") or "")[-1000:])
                if lg:
                    counts[lg] += 1
            langs[site] = counts.most_common(1)[0][0] if counts else "en"
        page = get_page_text(url, caches[site], allow_live_fetch=True)
        if page is None:
            results.append({"site": site, "url": url, "mini": mini_cls,
                            "sonnet": "SKIPPED_NO_CONTENT", "via": "fetch-failed"})
            continue
        title, raw_text = page
        pre = deterministic_preclassify(url, strip_nav_chrome(raw_text), raw_text, langs[site])
        if pre:
            results.append({"site": site, "url": url, "mini": mini_cls,
                            "sonnet": pre[0], "via": "prefilter:" + pre[1]})
            continue
        snippet = build_judge_snippet(raw_text)
        if len(snippet) < 100:
            results.append({"site": site, "url": url, "mini": mini_cls,
                            "sonnet": "SKIPPED_THIN_CONTENT", "via": "thin"})
            continue
        try:
            jr = call_haiku(client, prefix_block,
                            format_suffix(suffix_template, url, title, snippet))
        except RuntimeError as exc:
            results.append({"site": site, "url": url, "mini": mini_cls,
                            "sonnet": "CALL_FAILED", "via": str(exc)[:80]})
            continue
        cost += _haiku_cost_per_call(
            jr.input_tokens or 0, jr.output_tokens or 0,
            jr.cache_creation_input_tokens or 0, jr.cache_read_input_tokens or 0)
        results.append({"site": site, "url": url, "mini": mini_cls,
                        "sonnet": jr.classification, "via": "sonnet",
                        "rationale": f"{jr.rationale_prefix}: {jr.rationale_text}"[:300]})
        if i % 50 == 0:
            print(f"    [{label} {i}/{len(rows)}] running spend ${cost:.4f}", flush=True)
    return results, cost


def summarize(results: list) -> dict:
    comparable = [r for r in results if r["sonnet"] in JUDGED]
    agree = sum(1 for r in comparable if r["sonnet"] == r["mini"])
    mini_h = [r for r in comparable if r["mini"] == "HELPFUL"]
    over = sum(1 for r in mini_h if r["sonnet"] == "NON-HELPFUL")
    mini_nh = [r for r in comparable if r["mini"] == "NON-HELPFUL"]
    under = sum(1 for r in mini_nh if r["sonnet"] == "HELPFUL")
    per_site = {}
    for site in sorted({r["site"] for r in comparable}):
        rows = [r for r in comparable if r["site"] == site]
        hrows = [r for r in rows if r["mini"] == "HELPFUL"]
        per_site[site] = {
            "n": len(rows),
            "agreement_pct": round(100 * sum(1 for r in rows if r["sonnet"] == r["mini"]) / len(rows), 2),
            "over_inclusion_pct": round(100 * sum(1 for r in hrows if r["sonnet"] == "NON-HELPFUL") / len(hrows), 2) if hrows else None,
        }
    return {
        "n_sampled": len(results),
        "n_comparable": len(comparable),
        "n_uncomparable": len(results) - len(comparable),
        "agreement_pct": round(100 * agree / len(comparable), 2) if comparable else None,
        "over_inclusion_pct": round(100 * over / len(mini_h), 2) if mini_h else None,
        "over_inclusion_n": f"{over}/{len(mini_h)}",
        "under_inclusion_pct": round(100 * under / len(mini_nh), 2) if mini_nh else None,
        "under_inclusion_n": f"{under}/{len(mini_nh)}",
        "per_site": per_site,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1000, help="total rows to audit")
    ap.add_argument("--dry-run", action="store_true", help="show sample plan, no API calls")
    args = ap.parse_args()

    universe = load_universe()
    judged = sum(1 for recs in universe.values() for r in recs.values()
                 if r.get("classification") in JUDGED)
    print(f"Universe: {len(universe)} sites, {judged} judged rows")
    a, b = pick_sample(universe, args.n)
    print(f"Stratum A (unbiased): {len(a)} rows — {dict(Counter(s for s, _, _ in a))}")
    print(f"Stratum B (targeted): {len(b)} rows — {dict(Counter(s for s, _, _ in b))}")
    if args.dry_run:
        print("\n--dry-run: no API calls made.")
        return 0

    prefix_block, suffix_template = load_prompt_blocks()
    client = _haiku_client()
    print("\n--- Stratum A ---", flush=True)
    res_a, cost_a = rejudge(a, "A", client, prefix_block, suffix_template)
    print("\n--- Stratum B ---", flush=True)
    res_b, cost_b = rejudge(b, "B", client, prefix_block, suffix_template)

    sum_a, sum_b = summarize(res_a), summarize(res_b)
    payload = {
        "date_utc": _dt.datetime.now(_dt.UTC).isoformat(),
        "seed": AUDIT_SEED,
        "auditor_model": "claude-sonnet-4-5-20250929",
        "audited_model": "gpt-4o-mini-2024-07-18",
        "spend_usd": {"stratum_a": round(cost_a, 4), "stratum_b": round(cost_b, 4),
                      "total": round(cost_a + cost_b, 4)},
        "stratum_a_unbiased": sum_a,
        "stratum_b_targeted": sum_b,
        "targeted_patterns": list(TARGETED_PATTERNS),
        "rows": {"stratum_a": res_a, "stratum_b": res_b},
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n")

    md = [
        "# v1.5 DS-2 — Sonnet audit of the gpt-4o-mini universe", "",
        f"- **Date**: {payload['date_utc']}",
        f"- **Auditor**: `{payload['auditor_model']}` re-judging `{payload['audited_model']}`",
        f"- **Sample**: {len(res_a)} unbiased + {len(res_b)} targeted (seed {AUDIT_SEED})",
        f"- **Spend**: **${payload['spend_usd']['total']:.4f}**", "",
        "## Stratum A — unbiased estimate (headline)", "",
        f"- Agreement with mini: **{sum_a['agreement_pct']}%** ({sum_a['n_comparable']} comparable rows)",
        f"- **Over-inclusion** (mini HELPFUL, Sonnet NON-HELPFUL): **{sum_a['over_inclusion_pct']}%** ({sum_a['over_inclusion_n']})",
        f"- Under-inclusion (mini NON-HELPFUL, Sonnet HELPFUL): {sum_a['under_inclusion_pct']}% ({sum_a['under_inclusion_n']})", "",
        "| Site | n | Agreement | Over-inclusion |", "|---|---|---|---|",
    ]
    for site, s in sum_a["per_site"].items():
        md.append(f"| {site} | {s['n']} | {s['agreement_pct']}% | {s['over_inclusion_pct']}% |")
    md += [
        "", "## Stratum B — targeted worst case (NOT part of the estimate)", "",
        f"Patterns: `{'`, `'.join(TARGETED_PATTERNS)}` — rubric-NON-HELPFUL shapes mini is known to pass.", "",
        f"- Over-inclusion on these patterns: **{sum_b['over_inclusion_pct']}%** ({sum_b['over_inclusion_n']})",
        f"- Agreement: {sum_b['agreement_pct']}% of {sum_b['n_comparable']} comparable rows", "",
        "## How to read this", "",
        "Stratum A bounds how much the published helpful-pages universe is inflated by",
        "the cheap judge. Inflation applies to every crawler equally (the universe is the",
        "denominator for Coverage-of-Helpful), so leaderboard ORDERING is unaffected;",
        "absolute coverage percentages carry this as a known bias. Stratum B is the",
        "worst case on the specific shapes mini mishandles, reported separately so it",
        "cannot inflate the headline number.", "",
    ]
    OUT_MD.write_text("\n".join(md) + "\n")
    print(f"\nWrote {OUT_JSON.relative_to(ROOT)} + {OUT_MD.relative_to(ROOT)}")
    print(f"TOTAL AUDIT SPEND: ${cost_a + cost_b:.4f}")
    print(f"Headline over-inclusion (stratum A): {sum_a['over_inclusion_pct']}% ({sum_a['over_inclusion_n']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
