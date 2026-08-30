#!/usr/bin/env python3
"""DS-5 (v1.5): intersection-set computation + sibling report (spec SC-7).

The primary leaderboard measures crawl AND retrieval together, so a tool
can win by crawling more pages. The intersection set removes that: it is
the set of pages EVERY qualifying tool crawled, so each tool is ranked on
the same documents and only ranking quality separates them.

Two rules make the intersection meaningful rather than trivial:

  Qualifying tools — a tool must have crawled at least `min_pages` on a
  site to constrain that site's intersection. Without this, one tool that
  failed on a site (2 pages) would collapse the intersection to nearly
  nothing and the report would silently describe two pages instead of the
  corpus.

  Helpful-pages filter — the intersection is intersected AGAIN with the
  judged helpful set. Raw intersections are dominated by the boilerplate
  every crawler picks up (landing pages, /about, nav hubs), which would
  make the sibling report an easy target to game and uninformative to read.

This is a SIBLING reference, never the headline: restricting to pages all
tools found systematically favors whatever is easy to crawl.

Site-agnostic: everything derives from per-tool page lists and the
per-site universe, so a rotating pool needs no change here.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Set

REPO_ROOT = Path(__file__).resolve().parent.parent

MIN_PAGES_FOR_TOOL_INCLUSION = 10
# Below this many pool-level queries the intersection MRR is too noisy to
# read as a ranking; the report says so out loud (spec SC-7c).
POOL_N_WIDE_CI_THRESHOLD = 80


def _norm(u: str) -> str:
    return u.lower().rstrip("/")


def qualifying_tools(
    pages_by_tool: Dict[str, Iterable[str]],
    min_pages: int = MIN_PAGES_FOR_TOOL_INCLUSION,
) -> List[str]:
    """Tools with enough pages on this site to constrain its intersection."""
    return sorted(t for t, pages in pages_by_tool.items() if len(set(pages)) >= min_pages)


def site_intersection(
    pages_by_tool: Dict[str, Iterable[str]],
    helpful_urls: Iterable[str],
    min_pages: int = MIN_PAGES_FOR_TOOL_INCLUSION,
    normalize: Callable[[str], str] = _norm,
) -> Dict[str, object]:
    """Intersection ∩ helpful-pages for one site.

    Returns the page set plus the bookkeeping the report must disclose:
    which tools qualified, which were excluded for being too small, and how
    much the helpful filter removed.
    """
    qualified = qualifying_tools(pages_by_tool, min_pages)
    excluded = sorted(set(pages_by_tool) - set(qualified))
    if not qualified:
        return {"pages": set(), "qualified_tools": [], "excluded_tools": excluded,
                "raw_intersection_size": 0, "helpful_filtered_size": 0}

    sets = [{normalize(u) for u in pages_by_tool[t]} for t in qualified]
    raw = set.intersection(*sets) if sets else set()
    helpful_norm = {normalize(u) for u in helpful_urls}
    filtered = raw & helpful_norm if helpful_norm else set()
    return {
        "pages": filtered,
        "qualified_tools": qualified,
        "excluded_tools": excluded,
        "raw_intersection_size": len(raw),
        "helpful_filtered_size": len(filtered),
    }


def queries_in_intersection(
    query_records: Iterable[dict],
    intersection_pages: Set[str],
    normalize: Callable[[str], str] = _norm,
) -> List[dict]:
    """Queries whose answer page lies inside the intersection set."""
    out = []
    for rec in query_records:
        um = (rec.get("url_match") or "").lower()
        pm = (rec.get("page_match") or "").lower()
        if not um and not pm:
            continue
        for page in intersection_pages:
            norm = normalize(page)
            if (um and um in norm) or (pm and pm in norm):
                out.append(rec)
                break
    return out


def intersection_mrr(query_records: Iterable[dict]) -> Optional[float]:
    """MRR over intersection queries; None when there are none (not 0.0 —
    an empty set is 'not measured', not 'ranked badly')."""
    recs = list(query_records)
    if not recs:
        return None
    return sum(r.get("rr", 0.0) for r in recs) / len(recs)


def render_report(
    per_site: Dict[str, dict],
    per_tool_mrr: Dict[str, Optional[float]],
    pool_n: int,
    min_pages: int = MIN_PAGES_FOR_TOOL_INCLUSION,
) -> str:
    """RETRIEVAL_INTERSECTION.md (spec SC-7 a-e)."""
    lines = [
        "# Retrieval on the intersection set (sibling reference)",
        "",
        "> **This is a sibling reference, not the primary leaderboard.**",
        "> It ranks tools only on pages *every* qualifying tool crawled, which",
        "> removes coverage differences — and with them, credit for the harder",
        "> crawling that the primary leaderboard exists to measure. Restricting",
        "> to commonly-found pages systematically favours easy-to-crawl content.",
        "> Read it beside `RETRIEVAL_COMPARISON.md`, never instead of it.",
        "",
        "## Definition",
        "",
        f"- A tool constrains a site's intersection only if it crawled at least **{min_pages} pages** there;",
        "  tools below that threshold are listed as excluded per site rather than allowed to collapse the set.",
        "- The intersection is then filtered through the judged helpful-pages universe",
        "  (**intersection ∩ helpful-pages**, not the raw intersection). Raw intersections are dominated",
        "  by boilerplate every crawler picks up — landing pages, /about, nav hubs — which would make this",
        "  report both gameable and uninformative.",
        "",
        "## Per-site intersection sizes",
        "",
        "| Site | Qualifying tools | Excluded (<threshold) | Raw ∩ | ∩ helpful-pages |",
        "|---|---|---|---|---|",
    ]
    for site in sorted(per_site):
        d = per_site[site]
        lines.append(
            f"| {site} | {len(d['qualified_tools'])} | "
            f"{', '.join(d['excluded_tools']) or '—'} | "
            f"{d['raw_intersection_size']} | {d['helpful_filtered_size']} |"
        )
    lines += [
        "",
        f"**Pool-level intersection queries: {pool_n}**",
        "",
    ]
    if pool_n < POOL_N_WIDE_CI_THRESHOLD:
        lines += [
            "> ⚠️ **Intersection MRR has wide confidence intervals at this measurement**",
            f"> **resolution** — only {pool_n} pool-level queries fall inside the intersection",
            f"> (threshold for a readable signal: {POOL_N_WIDE_CI_THRESHOLD}). Differences between",
            "> tools below that N should not be read as ranking differences.",
            "",
        ]
    lines += ["## Per-tool intersection MRR", "", "| Tool | Intersection MRR |", "|---|---|"]
    for tool in sorted(per_tool_mrr, key=lambda t: (per_tool_mrr[t] is None, -(per_tool_mrr[t] or 0))):
        v = per_tool_mrr[tool]
        lines.append(f"| {tool} | {'n/a' if v is None else f'{v:.4f}'} |")
    lines.append("")
    return "\n".join(lines)


def load_tool_pages(run_dir: Path, tool: str, site: str) -> Set[str]:
    """URLs a tool crawled for a site, from its pages.jsonl."""
    path = run_dir / tool / site / "pages.jsonl"
    if not path.is_file():
        return set()
    urls = set()
    with path.open() as f:
        for line in f:
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec.get("url"):
                urls.add(rec["url"])
    return urls
