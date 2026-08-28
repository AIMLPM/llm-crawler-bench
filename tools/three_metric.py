#!/usr/bin/env python3
"""DS-4 (v1.5): three-metric decomposition against the helpful-pages universe.

v1.4 published a single MRR, which conflates two different failures: a tool
can score badly because it never crawled the answer page, or because it
crawled it and ranked it poorly. Those call for opposite fixes, so v1.5
reports them separately (spec SC-6):

  Coverage-of-Helpful    |tool pages ∩ helpful| / |helpful|, pct AND counts
  Retrieval-on-covered   MRR over only the queries whose answer page the
                         tool actually indexed — pure ranking quality
  End-to-end (headline)  MRR over every query; an uncovered answer scores 0,
                         so this carries the coverage penalty implicitly

The universe is anchor-independent, so all tools are scored against the
same target set rather than against one competitor's crawl.

Site-agnostic by construction: everything is derived from the per-site
universe file and the tool's own page list, so a rotating pool needs no
code change here.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
HELPFUL_PAGES_DIR = REPO_ROOT / "bench" / "helpful_pages_gpt4omini"


def load_helpful_urls(site: str, helpful_dir: Optional[Path] = None) -> Set[str]:
    """URLs judged HELPFUL for `site`. Empty set when the site has no
    universe file, which callers treat as "coverage not measurable"."""
    path = (helpful_dir or HELPFUL_PAGES_DIR) / f"{site}.json"
    if not path.is_file():
        return set()
    recs = json.loads(path.read_text())
    return {u for u, v in recs.items() if v.get("classification") == "HELPFUL"}


def coverage_of_helpful(
    indexed_urls: Iterable[str],
    helpful_urls: Iterable[str],
    normalize: Callable[[str], str] = lambda u: u.lower().rstrip("/"),
) -> Tuple[int, int, Optional[float]]:
    """(covered, total_helpful, pct) — pct is None when the universe is empty.

    Both sides are normalized before comparison so trailing slashes, case,
    and tracking parameters do not read as misses.
    """
    helpful_norm = {normalize(u) for u in helpful_urls}
    if not helpful_norm:
        return 0, 0, None
    indexed_norm = {normalize(u) for u in indexed_urls}
    covered = len(helpful_norm & indexed_norm)
    return covered, len(helpful_norm), 100.0 * covered / len(helpful_norm)


def query_is_covered(
    url_match: str,
    page_match: str,
    indexed_urls: Sequence[str],
    normalize: Callable[[str], str] = lambda u: u.lower(),
) -> bool:
    """True when the query's answer page is present in the tool's index.

    Uses the same substring-on-normalized-URL rule the hit checker uses, so
    "covered" and "hit" agree about what counts as the answer page.
    """
    um = (url_match or "").lower()
    pm = (page_match or "").lower()
    if not um and not pm:
        return False
    for url in indexed_urls:
        norm = normalize(url)
        if um and um in norm:
            return True
        if pm and pm in norm:
            return True
    return False


def split_by_coverage(
    query_records: Sequence[dict],
    indexed_urls: Sequence[str],
    normalize: Callable[[str], str] = lambda u: u.lower(),
) -> Tuple[List[dict], List[dict]]:
    """Partition query records into (covered, uncovered).

    Each record needs `url_match`, `page_match`, and `rr` (the reciprocal
    rank this query earned, 0.0 for a miss).
    """
    covered, uncovered = [], []
    for rec in query_records:
        target = covered if query_is_covered(
            rec.get("url_match", ""), rec.get("page_match", ""),
            indexed_urls, normalize) else uncovered
        target.append(rec)
    return covered, uncovered


def three_metrics(
    query_records: Sequence[dict],
    indexed_urls: Sequence[str],
    helpful_urls: Iterable[str],
    normalize: Callable[[str], str] = lambda u: u.lower(),
) -> Dict[str, object]:
    """Compute the SC-6 triple for one (tool, site).

    `query_records` carry `rr` — reciprocal rank, 0.0 when the tool missed.
    End-to-end averages every query; retrieval-on-covered averages only the
    queries whose answer page was indexed. When nothing is covered,
    retrieval-on-covered is None rather than 0.0: no ranking was attempted,
    and reporting 0.0 would read as "ranked badly" instead of "never saw it".
    """
    covered, uncovered = split_by_coverage(query_records, indexed_urls, normalize)
    n = len(query_records)
    end_to_end = sum(r.get("rr", 0.0) for r in query_records) / n if n else 0.0
    on_covered = (sum(r.get("rr", 0.0) for r in covered) / len(covered)
                  if covered else None)
    cov_n, cov_total, cov_pct = coverage_of_helpful(
        indexed_urls, helpful_urls,
        normalize=lambda u: normalize(u).rstrip("/"))
    return {
        "coverage_covered": cov_n,
        "coverage_total": cov_total,
        "coverage_pct": cov_pct,
        "retrieval_on_covered_mrr": on_covered,
        "retrieval_on_covered_n": len(covered),
        "end_to_end_mrr": end_to_end,
        "queries_total": n,
        "queries_uncovered": len(uncovered),
    }


def format_coverage(covered: int, total: int, pct: Optional[float]) -> str:
    """"43.0% (1800 / 4200)" — spec SC-6 requires percentage AND counts, so
    a scope-strategy difference reads as a design choice, not a failure."""
    if pct is None:
        return "n/a"
    return f"{pct:.1f}% ({covered} / {total})"
