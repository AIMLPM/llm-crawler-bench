"""DS-5: intersection-set computation + sibling report (spec SC-7)."""

import pytest

from tools import intersection_set as isect


def _pages(*urls):
    return list(urls)


def test_small_tool_is_excluded_not_allowed_to_collapse_set():
    """A tool that failed on a site must not shrink the intersection to nothing."""
    big_a = [f"https://x.com/p{i}" for i in range(20)]
    big_b = [f"https://x.com/p{i}" for i in range(20)]
    tiny = ["https://x.com/p0", "https://x.com/p1"]  # 2 pages, below threshold
    out = isect.site_intersection(
        {"a": big_a, "b": big_b, "broken": tiny},
        helpful_urls=big_a,
    )
    assert out["excluded_tools"] == ["broken"]
    assert out["qualified_tools"] == ["a", "b"]
    assert out["raw_intersection_size"] == 20


def test_helpful_filter_removes_boilerplate():
    common = [f"https://x.com/p{i}" for i in range(12)]
    out = isect.site_intersection(
        {"a": common, "b": common},
        helpful_urls=[f"https://x.com/p{i}" for i in range(5)],  # only 5 are helpful
    )
    assert out["raw_intersection_size"] == 12
    assert out["helpful_filtered_size"] == 5


def test_intersection_is_pages_common_to_all_qualifying_tools():
    a = [f"https://x.com/p{i}" for i in range(15)]
    b = [f"https://x.com/p{i}" for i in range(5, 20)]
    out = isect.site_intersection({"a": a, "b": b}, helpful_urls=a + b)
    assert out["helpful_filtered_size"] == 10  # p5..p14


def test_no_qualifying_tools_yields_empty_not_crash():
    out = isect.site_intersection({"a": ["https://x.com/p1"]}, helpful_urls=["https://x.com/p1"])
    assert out["pages"] == set()
    assert out["qualified_tools"] == []


def test_queries_filtered_to_intersection():
    pages = {"https://x.com/guide", "https://x.com/api"}
    recs = [
        {"url_match": "guide", "rr": 1.0},
        {"url_match": "elsewhere", "rr": 0.5},
    ]
    kept = isect.queries_in_intersection(recs, pages)
    assert len(kept) == 1 and kept[0]["url_match"] == "guide"


def test_intersection_mrr_none_when_empty():
    assert isect.intersection_mrr([]) is None
    assert isect.intersection_mrr([{"rr": 0.5}, {"rr": 1.0}]) == pytest.approx(0.75)


def test_report_warns_below_ci_threshold():
    md = isect.render_report(
        {"s": {"qualified_tools": ["a", "b"], "excluded_tools": [],
               "raw_intersection_size": 10, "helpful_filtered_size": 4}},
        {"a": 0.5, "b": 0.4},
        pool_n=12,
    )
    assert "wide confidence intervals" in md
    assert "sibling reference, not the primary leaderboard" in md
    assert "intersection ∩ helpful-pages" in md


def test_report_omits_warning_when_n_is_adequate():
    md = isect.render_report(
        {"s": {"qualified_tools": ["a"], "excluded_tools": ["c"],
               "raw_intersection_size": 100, "helpful_filtered_size": 90}},
        {"a": 0.5},
        pool_n=200,
    )
    assert "wide confidence intervals" not in md
    # The excluded tool belongs in the per-site row, never in the ranking table.
    ranking = md[md.index("Per-tool intersection MRR"):]
    assert "| c |" not in ranking
    assert "| c |" in md[: md.index("Per-tool intersection MRR")]


def test_report_ranks_tools_by_mrr_descending():
    md = isect.render_report(
        {}, {"low": 0.1, "high": 0.9, "missing": None}, pool_n=100,
    )
    body = md[md.index("Per-tool intersection MRR"):]
    assert body.index("high") < body.index("low") < body.index("missing")
