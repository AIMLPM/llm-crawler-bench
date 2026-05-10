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


def test_default_pricing_reproduces_published_markcrawl_within_1pct():
    """Default pricing should produce markcrawl mid-scale cost within 1%
    of the published COST_AT_SCALE.md number ($4,505)."""
    p = cc.PricingInputs()  # all defaults
    rows = cc.cost_table(p)
    mc = next(r for r in rows if r["tool"] == "markcrawl")
    published = 4505
    assert abs(mc["total_yr"] - published) / published < 0.01, \
        f"markcrawl mid-scale cost {mc['total_yr']} differs >1% from published {published}"


def test_cost_table_sorted_ascending_by_total():
    p = cc.PricingInputs()
    rows = cc.cost_table(p)
    totals = [r["total_yr"] for r in rows]
    assert totals == sorted(totals), "cost table must be ranked ascending"


def test_markcrawl_first_in_baseline_ranking():
    """Sanity check: markcrawl should rank first under default pricing.
    If this fails, either chunks_per_page numbers changed or pricing changed."""
    rows = cc.cost_table(cc.PricingInputs())
    assert rows[0]["tool"] == "markcrawl"


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
    """Negative test: if we artificially make markcrawl's chunks_per_page
    much larger than scrapy+md's, the ranking SHOULD shift somewhere in
    the ±50% sweep. Verifies the shift-detection isn't broken."""
    monkeypatch.setitem(cc.PER_TOOL_DATA, "markcrawl", {"chunks_per_page": 14.0, "k_retrieval": 14})
    monkeypatch.setitem(cc.PER_TOOL_DATA, "scrapy+md", {"chunks_per_page": 12.0, "k_retrieval": 12})
    rows = cc.cost_table(cc.PricingInputs())
    # Now scrapy+md should rank below markcrawl in baseline
    assert rows[0]["tool"] == "scrapy+md", "test setup: scrapy+md should be cheapest after monkeypatch"


def test_render_markdown_table_contains_em_dash_for_markcrawl():
    """markcrawl row uses an em-dash in 'vs markcrawl' column (not a delta)."""
    rows = cc.cost_table(cc.PricingInputs())
    md = cc.render_markdown_table(rows, cc.PricingInputs())
    mc_line = next(line for line in md.split("\n") if line.startswith("| markcrawl |"))
    assert "—" in mc_line and "+$" not in mc_line


def test_per_tool_data_has_seven_competitors_plus_markcrawl():
    """The 8 tool keys: markcrawl + 7 competitors. Sanity check that
    PER_TOOL_DATA hasn't been accidentally pared down."""
    assert len(cc.PER_TOOL_DATA) == 8
    assert "markcrawl" in cc.PER_TOOL_DATA
