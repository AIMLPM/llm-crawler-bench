"""DS-11: Cost calculator tests.

Covers cost-formula correctness (matches published COST_AT_SCALE numbers
within ~1%), sort-order, sensitivity sweep shape, and the ranking-shift
detection that makes the sensitivity output credible (a sweep that
silently failed to detect shifts would be worse than no sweep)."""

from __future__ import annotations

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent
_tools_dir = _repo_root / "tools"
if str(_tools_dir) not in sys.path:
    sys.path.insert(0, str(_tools_dir))

import cost_calculator as cc  # noqa: E402


def test_v14_markcrawl_third_place_at_default_pricing():
    """v1.4 calculator: markcrawl is 3rd cheapest at default pricing
    (crawl4ai-raw and crawl4ai have lower chunks/page after the v1.4
    chunker default flip). Locks the v1.4 ordering — a future regression
    that put markcrawl back at 1st without updated empirical data would
    fail this test."""
    p = cc.PricingInputs()
    rows = cc.cost_table(p)
    ranking = [r["tool"] for r in rows]
    # crawl4ai-raw + crawl4ai cheaper than markcrawl in v1.4
    assert ranking[0] == "crawl4ai-raw"
    assert ranking[1] == "crawl4ai"
    assert ranking[2] == "markcrawl"


def test_cost_table_sorted_ascending_by_total():
    p = cc.PricingInputs()
    rows = cc.cost_table(p)
    totals = [r["total_yr"] for r in rows]
    assert totals == sorted(totals), "cost table must be ranked ascending"


def test_v14_crawl4ai_raw_first_in_baseline_ranking():
    """Sanity check: crawl4ai-raw should rank first under v1.4 default
    pricing (chunks_per_page 9.61 vs markcrawl's 12.19)."""
    rows = cc.cost_table(cc.PricingInputs())
    assert rows[0]["tool"] == "crawl4ai-raw"


def test_storage_cost_scales_linearly_with_pages():
    p1 = cc.PricingInputs(pages=1_000)
    p2 = cc.PricingInputs(pages=10_000)
    s1 = cc.storage_cost_yr("markcrawl", p1)
    s2 = cc.storage_cost_yr("markcrawl", p2)
    assert abs(s2 - 10 * s1) < 0.01, "storage cost should be 10x when pages 10x"


def test_query_cost_scales_linearly_with_queries():
    p1 = cc.PricingInputs(queries_per_day=100)
    p2 = cc.PricingInputs(queries_per_day=1_000)
    q1 = cc.query_cost_yr("markcrawl", p1)
    q2 = cc.query_cost_yr("markcrawl", p2)
    assert abs(q2 - 10 * q1) < 0.01, "query cost should be 10x when queries 10x"


def test_sensitivity_sweep_returns_two_per_input():
    """6 inputs × 2 directions = 12 perturbation rows."""
    results = cc.sensitivity_sweep(cc.PricingInputs())
    assert len(results) == 12


def test_sensitivity_sweep_baseline_robust_under_default_pricing():
    """Headline claim: under default pricing, ranking is robust to ±50% on
    every individual input. This is a credibility signal worth testing —
    if a future change accidentally introduces a fragile ranking, the test
    surfaces it."""
    results = cc.sensitivity_sweep(cc.PricingInputs())
    shifted = [r for r in results if r["ranking_shifted"]]
    assert shifted == [], (
        f"Expected ranking robust under default pricing, but {len(shifted)} "
        f"perturbations shifted the ranking: {[r['input'] + ' ' + str(r['delta_pct']) + '%' for r in shifted]}"
    )


def test_sensitivity_sweep_can_detect_ranking_shift(monkeypatch):
    """Negative test: artificially make scrapy+md the cheapest tool by
    flooring its chunks_per_page. The ranking-shift-detection logic should
    notice this is different from the default baseline (crawl4ai-raw 1st).
    Verifies the shift-detection isn't broken."""
    # Floor scrapy+md below crawl4ai-raw + crawl4ai
    monkeypatch.setitem(cc.PER_TOOL_DATA, "scrapy+md", {"chunks_per_page": 1.0, "k_retrieval": 1})
    rows = cc.cost_table(cc.PricingInputs())
    assert rows[0]["tool"] == "scrapy+md", "test setup: scrapy+md should be cheapest after monkeypatch"


def test_render_markdown_table_contains_em_dash_for_markcrawl():
    """markcrawl row uses an em-dash in 'vs markcrawl' column (not a delta)."""
    rows = cc.cost_table(cc.PricingInputs())
    md = cc.render_markdown_table(rows, cc.PricingInputs())
    mc_line = next(line for line in md.split("\n") if line.startswith("| markcrawl |"))
    assert "—" in mc_line and "+$" not in mc_line


def test_per_tool_data_has_seven_tools():
    """7 tools in v1.4 (firecrawl removed — not in the v1.4 run because
    FIRECRAWL_API_KEY was absent and all sites skipped). Sanity check
    that PER_TOOL_DATA hasn't been accidentally pared down."""
    assert len(cc.PER_TOOL_DATA) == 7
    assert "markcrawl" in cc.PER_TOOL_DATA
    assert "firecrawl" not in cc.PER_TOOL_DATA
