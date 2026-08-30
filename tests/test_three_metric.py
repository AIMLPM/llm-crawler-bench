"""DS-4: three-metric decomposition (spec SC-6)."""

import json

import pytest

from tools import three_metric as tm


def test_coverage_counts_and_pct():
    covered, total, pct = tm.coverage_of_helpful(
        ["https://x.com/a", "https://x.com/b", "https://x.com/zzz"],
        ["https://x.com/a", "https://x.com/b", "https://x.com/c", "https://x.com/d"],
    )
    assert (covered, total) == (2, 4)
    assert pct == pytest.approx(50.0)


def test_coverage_normalizes_trailing_slash_and_case():
    covered, total, pct = tm.coverage_of_helpful(
        ["https://X.com/A/"], ["https://x.com/a"]
    )
    assert (covered, total, pct) == (1, 1, 100.0)


def test_coverage_empty_universe_is_not_measurable():
    assert tm.coverage_of_helpful(["https://x.com/a"], []) == (0, 0, None)


def test_uncovered_query_penalizes_end_to_end_but_not_on_covered():
    """The core of SC-6: a page the tool never crawled must not be scored as
    a ranking failure, but must still cost the headline metric."""
    records = [
        {"url_match": "a.html", "page_match": "", "rr": 1.0},
        {"url_match": "missing.html", "page_match": "", "rr": 0.0},
    ]
    out = tm.three_metrics(records, ["https://x.com/a.html"], ["https://x.com/a.html"])
    assert out["end_to_end_mrr"] == pytest.approx(0.5)
    assert out["retrieval_on_covered_mrr"] == pytest.approx(1.0)
    assert out["retrieval_on_covered_n"] == 1
    assert out["queries_uncovered"] == 1


def test_covered_but_badly_ranked_lowers_on_covered_mrr():
    records = [{"url_match": "a.html", "page_match": "", "rr": 0.2}]
    out = tm.three_metrics(records, ["https://x.com/a.html"], ["https://x.com/a.html"])
    assert out["retrieval_on_covered_mrr"] == pytest.approx(0.2)
    assert out["end_to_end_mrr"] == pytest.approx(0.2)


def test_no_coverage_yields_none_not_zero():
    """None distinguishes 'never crawled it' from 'ranked it last'."""
    records = [{"url_match": "a.html", "page_match": "", "rr": 0.0}]
    out = tm.three_metrics(records, ["https://x.com/other.html"], ["https://x.com/a.html"])
    assert out["retrieval_on_covered_mrr"] is None
    assert out["end_to_end_mrr"] == 0.0


def test_page_match_also_establishes_coverage():
    records = [{"url_match": "", "page_match": "guide", "rr": 1.0}]
    out = tm.three_metrics(records, ["https://x.com/guide"], ["https://x.com/guide"])
    assert out["retrieval_on_covered_n"] == 1


def test_load_helpful_urls_selects_only_helpful(tmp_path):
    (tmp_path / "s.json").write_text(json.dumps({
        "https://x.com/a": {"classification": "HELPFUL"},
        "https://x.com/b": {"classification": "NON-HELPFUL"},
        "https://x.com/c": {"classification": "SKIPPED_NO_CONTENT"},
    }))
    assert tm.load_helpful_urls("s", helpful_dir=tmp_path) == {"https://x.com/a"}


def test_load_helpful_urls_missing_site_is_empty(tmp_path):
    assert tm.load_helpful_urls("nope", helpful_dir=tmp_path) == set()


def test_format_coverage_shows_pct_and_counts():
    assert tm.format_coverage(1800, 4200, 42.857) == "42.9% (1800 / 4200)"
    assert tm.format_coverage(0, 0, None) == "n/a"
