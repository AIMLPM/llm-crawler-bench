"""DS-1: Page-level MRR helper. Collapses chunks-per-URL to pages so
chunk-density does not game the MRR signal."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_repo_root = Path(__file__).resolve().parent.parent
_tools_dir = _repo_root / "tools"
if str(_tools_dir) not in sys.path:
    sys.path.insert(0, str(_tools_dir))

from page_level_mrr import (  # noqa: E402
    aggregate_mrr,
    collapse_chunks_to_pages,
    hit_at_k,
    page_level_metrics,
    reciprocal_rank,
)


def test_collapse_preserves_order_and_dedups():
    assert collapse_chunks_to_pages(["a", "a", "b", "c", "a"]) == ["a", "b", "c"]


def test_collapse_empty():
    assert collapse_chunks_to_pages([]) == []


def test_reciprocal_rank_first_position():
    assert reciprocal_rank(["match", "x", "y"], lambda u: u == "match") == 1.0


def test_reciprocal_rank_third_position():
    assert reciprocal_rank(["x", "y", "match"], lambda u: u == "match") == pytest.approx(1.0 / 3)


def test_reciprocal_rank_no_match():
    assert reciprocal_rank(["x", "y", "z"], lambda u: u == "match") == 0.0


def test_hit_at_k_true():
    assert hit_at_k(["x", "y", "match"], 5, lambda u: u == "match") is True


def test_hit_at_k_false_outside_window():
    assert hit_at_k(["x", "y", "match"], 2, lambda u: u == "match") is False


def test_hit_at_k_zero_k():
    assert hit_at_k(["match"], 0, lambda u: u == "match") is False


def test_chunk_density_neutralized():
    """Headline DS-1 case: a crawler emitting 5 chunks/page must not be
    advantaged over a crawler emitting 1 chunk/page when the relevant
    URL is the second page ranked. Page-level RR collapses both to 0.5."""
    crawler_a_chunks = ["page1", "page2"]
    crawler_b_chunks = ["page1"] * 5 + ["page2"] * 5

    a = page_level_metrics(crawler_a_chunks, lambda u: u == "page2")
    b = page_level_metrics(crawler_b_chunks, lambda u: u == "page2")

    assert a["reciprocal_rank"] == 0.5
    assert b["reciprocal_rank"] == 0.5


def test_page_level_hit_at_k_uses_collapsed_positions():
    """When chunks repeat, hit@1 must reflect the first unique PAGE,
    not the first chunk position before collapsing."""
    chunks = ["page_a", "page_a", "page_a", "page_b"]
    metrics = page_level_metrics(chunks, lambda u: u == "page_b", k_values=(1, 2, 3))
    # Collapsed: [page_a, page_b]. page_b at position 2.
    assert metrics["hit_at_k"][1] is False
    assert metrics["hit_at_k"][2] is True
    assert metrics["hit_at_k"][3] is True


def test_aggregate_mrr_average():
    assert aggregate_mrr([1.0, 0.5, 0.0]) == pytest.approx(0.5)


def test_aggregate_mrr_empty():
    assert aggregate_mrr([]) == 0.0
