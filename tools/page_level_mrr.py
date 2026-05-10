"""Page-level MRR + Hit@K helpers (v1.4 DS-1).

Collapses multiple chunks per URL into a single rank before computing
retrieval metrics. Removes the chunk-density gaming signal that made
chunk-level MRR penalize crawlers emitting fewer chunks per page.

Page-level MRR is computed by:
  1. Take the rank-ordered chunk URL list returned by retrieval.
  2. Collapse to unique URLs preserving the BEST rank each URL achieved
     (= the first time that URL appears in the chunk list).
  3. Find the rank of the first page-collapsed URL counted as a hit.
  4. Reciprocal rank = 1/rank, or 0 if no hit in the list.

The match function is supplied by the caller so this module stays
decoupled from how URLs are matched (DS-2 URL normalization, expected
URL patterns, etc. are the caller's concern).
"""

from __future__ import annotations

from collections.abc import Callable, Iterable


def collapse_chunks_to_pages(urls: Iterable[str]) -> list[str]:
    """Collapse a rank-ordered chunk URL list to unique URLs. First
    occurrence of each URL wins, preserving the best rank that URL
    achieved across all of its chunks."""
    seen: set[str] = set()
    pages: list[str] = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            pages.append(url)
    return pages


def reciprocal_rank(urls: Iterable[str], match_fn: Callable[[str], bool]) -> float:
    """Reciprocal rank of the first URL the predicate matches.
    Returns 0.0 if no URL in the list matches."""
    for i, url in enumerate(urls, start=1):
        if match_fn(url):
            return 1.0 / i
    return 0.0


def hit_at_k(urls: Iterable[str], k: int, match_fn: Callable[[str], bool]) -> bool:
    """Whether any URL in the first k positions matches the predicate."""
    if k <= 0:
        return False
    for i, url in enumerate(urls):
        if i >= k:
            return False
        if match_fn(url):
            return True
    return False


def page_level_metrics(
    chunk_urls: Iterable[str],
    match_fn: Callable[[str], bool],
    k_values: Iterable[int] = (1, 3, 5, 10),
) -> dict:
    """Single-query page-level MRR + Hit@K. Caller passes the rank-ordered
    chunk URLs and a predicate that returns True for URLs counted as a hit
    (e.g. one that wraps DS-2's URL normalization plus the expected pattern).

    Returns: {"reciprocal_rank": float, "hit_at_k": {k: bool, ...}}
    """
    pages = collapse_chunks_to_pages(chunk_urls)
    return {
        "reciprocal_rank": reciprocal_rank(pages, match_fn),
        "hit_at_k": {k: hit_at_k(pages, k, match_fn) for k in k_values},
    }


def aggregate_mrr(per_query_rrs: Iterable[float]) -> float:
    """Mean reciprocal rank across queries. Returns 0.0 for empty input."""
    rrs = list(per_query_rrs)
    if not rrs:
        return 0.0
    return sum(rrs) / len(rrs)
