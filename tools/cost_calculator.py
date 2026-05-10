#!/usr/bin/env python3
"""DS-11: Cost calculator with sensitivity analysis (v1.4).

Computes per-tool annual RAG infrastructure cost from current pricing
inputs + per-tool chunk-density data measured in the v1.3 cycle.
Supports a sensitivity sweep: for each input, vary by ±50% and report
how the per-tool ranking shifts.

The reason this exists: the published cost-of-scale numbers in
reports/COST_AT_SCALE.md bake in many assumptions (queries/day,
embedding price, dedup ratio). A reviewer should be able to plug in
their own pricing and see whether markcrawl's cost lead survives —
this script makes that one command line.

Cost model:
  Storage cost = (chunks_per_page * pages) * tokens_per_chunk * embedding_price/1M
                 + (chunks_per_page * pages / 1000) * vector_db_price/month * 12
  Query cost   = K * tokens_per_chunk * queries_per_day * 365 * llm_input_price/1M

Usage:
    # Default: mid-scale (100K pages, 1K queries/day) markdown table
    python tools/cost_calculator.py

    # Custom scale
    python tools/cost_calculator.py --pages 500000 --queries-per-day 5000

    # Sensitivity sweep ±50% on each input
    python tools/cost_calculator.py --sensitivity

    # JSON output for machine consumption
    python tools/cost_calculator.py --json --sensitivity
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, replace

# Per-tool empirical data from the v1.3 cycle (chunk counts from
# reports/RETRIEVAL_COMPARISON.md, retrieval depths derived from chunk
# density per the COST_AT_SCALE methodology). Update these when v1.4
# numbers land — DS-14 release notes consume the calculator output.
PER_TOOL_DATA: dict[str, dict[str, float]] = {
    "markcrawl":    {"chunks_per_page": 10.1,  "k_retrieval": 10},
    "scrapy+md":    {"chunks_per_page": 12.0,  "k_retrieval": 12},
    "firecrawl":    {"chunks_per_page": 12.97, "k_retrieval": 13},
    "crawl4ai":     {"chunks_per_page": 15.0,  "k_retrieval": 15},
    "crawl4ai-raw": {"chunks_per_page": 15.0,  "k_retrieval": 15},
    "colly+md":     {"chunks_per_page": 15.0,  "k_retrieval": 15},
    "playwright":   {"chunks_per_page": 15.0,  "k_retrieval": 15},
    "crawlee":      {"chunks_per_page": 16.0,  "k_retrieval": 16},
}


@dataclass
class PricingInputs:
    """All adjustable cost-model parameters in one place. Defaults match
    reports/COST_AT_SCALE.md so calculator output reproduces the published
    numbers when no flags are passed."""
    embedding_price_per_1m_tokens: float = 0.02      # OpenAI text-embedding-3-small
    vector_db_price_per_1k_vectors_month: float = 0.10
    llm_input_price_per_1m_tokens: float = 3.00      # Claude Sonnet
    tokens_per_chunk: int = 300
    pages: int = 100_000
    queries_per_day: int = 1_000


def storage_cost_yr(tool: str, p: PricingInputs) -> float:
    """Annual storage cost: embedding (one-time, amortized) + vector DB hosting × 12."""
    chunks = PER_TOOL_DATA[tool]["chunks_per_page"] * p.pages
    embed_tokens = chunks * p.tokens_per_chunk
    embed_cost = embed_tokens / 1_000_000 * p.embedding_price_per_1m_tokens
    db_cost_yr = chunks / 1000 * p.vector_db_price_per_1k_vectors_month * 12
    return embed_cost + db_cost_yr


def query_cost_yr(tool: str, p: PricingInputs) -> float:
    """Annual LLM query cost: K × tokens/chunk × queries/day × 365 × price/M."""
    k = PER_TOOL_DATA[tool]["k_retrieval"]
    tokens_per_query = k * p.tokens_per_chunk
    annual_queries = p.queries_per_day * 365
    annual_input_tokens = tokens_per_query * annual_queries
    return annual_input_tokens / 1_000_000 * p.llm_input_price_per_1m_tokens


def total_cost_yr(tool: str, p: PricingInputs) -> dict:
    """Return per-tool cost breakdown as a dict (JSON-friendly)."""
    s = storage_cost_yr(tool, p)
    q = query_cost_yr(tool, p)
    return {"tool": tool, "storage_yr": s, "query_yr": q, "total_yr": s + q}


def cost_table(p: PricingInputs) -> list[dict]:
    """Per-tool cost table sorted by total annual cost ascending."""
    rows = [total_cost_yr(t, p) for t in PER_TOOL_DATA]
    rows.sort(key=lambda r: r["total_yr"])
    return rows


def render_markdown_table(rows: list[dict], p: PricingInputs) -> str:
    lines = [
        f"_Inputs: {p.pages:,} pages, {p.queries_per_day:,} queries/day, "
        f"embedding ${p.embedding_price_per_1m_tokens:.4f}/1M tokens, "
        f"LLM input ${p.llm_input_price_per_1m_tokens:.2f}/1M tokens, "
        f"vector DB ${p.vector_db_price_per_1k_vectors_month:.2f}/1K vectors/month, "
        f"{p.tokens_per_chunk} tokens/chunk._",
        "",
        "| Tool | Storage/yr | Queries/yr | Total/yr | vs markcrawl |",
        "|---|---|---|---|---|",
    ]
    mc_total = next(r["total_yr"] for r in rows if r["tool"] == "markcrawl")
    for r in rows:
        if r["tool"] == "markcrawl":
            delta_str = "—"
        else:
            delta = r["total_yr"] - mc_total
            pct = delta / mc_total * 100 if mc_total else 0
            delta_str = f"+${delta:,.0f} ({pct:+.1f}%)"
        lines.append(
            f"| {r['tool']} | ${r['storage_yr']:,.0f} | ${r['query_yr']:,.0f} "
            f"| ${r['total_yr']:,.0f} | {delta_str} |"
        )
    return "\n".join(lines)


def sensitivity_sweep(p: PricingInputs) -> list[dict]:
    """Vary each input by ±50% in turn; report whether the per-tool
    ranking shifts. Inputs that don't shift the ranking are the
    "robust" knobs; those that do are credibility risks worth disclosing."""
    inputs_to_vary = [
        ("queries_per_day", "queries/day"),
        ("pages", "pages"),
        ("embedding_price_per_1m_tokens", "embedding price"),
        ("vector_db_price_per_1k_vectors_month", "vector DB price"),
        ("llm_input_price_per_1m_tokens", "LLM input price"),
        ("tokens_per_chunk", "tokens/chunk"),
    ]
    baseline_ranking = [r["tool"] for r in cost_table(p)]
    results = []
    for attr, label in inputs_to_vary:
        baseline_val = getattr(p, attr)
        for delta_pct in (-0.5, 0.5):
            new_val = baseline_val * (1 + delta_pct)
            if isinstance(baseline_val, int):
                new_val = int(round(new_val))
            modified = replace(p, **{attr: new_val})
            new_ranking = [r["tool"] for r in cost_table(modified)]
            shifted = new_ranking != baseline_ranking
            results.append({
                "input": label,
                "delta_pct": int(delta_pct * 100),
                "baseline_value": baseline_val,
                "new_value": new_val,
                "ranking_shifted": shifted,
                "new_ranking": new_ranking,
            })
    return results


def render_sensitivity_table(results: list[dict], baseline_ranking: list[str]) -> str:
    lines = [
        "**Baseline ranking** (by total annual cost ascending): " + " < ".join(baseline_ranking),
        "",
        "| Input varied | Δ | New value | Ranking shifted? | New ranking |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        shifted = "**yes**" if r["ranking_shifted"] else "no"
        new_rank = " < ".join(r["new_ranking"]) if r["ranking_shifted"] else "(unchanged)"
        v = r["new_value"]
        if isinstance(v, float):
            new_value_str = f"{v:.4g}"
        else:
            new_value_str = f"{v:,}"
        lines.append(
            f"| {r['input']} | {r['delta_pct']:+d}% | {new_value_str} | {shifted} | {new_rank} |"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--pages", type=int, default=100_000,
                        help="Pages crawled (storage scale, default 100,000)")
    parser.add_argument("--queries-per-day", type=int, default=1_000,
                        help="Daily query volume (default 1,000)")
    parser.add_argument("--embedding-price", type=float, default=0.02,
                        help="$/1M tokens for embedding (default 0.02 = OpenAI text-embedding-3-small)")
    parser.add_argument("--vector-db-price", type=float, default=0.10,
                        help="$/1K vectors/month for vector DB (default 0.10)")
    parser.add_argument("--llm-input-price", type=float, default=3.00,
                        help="$/1M input tokens for LLM judge (default 3.00 = Claude Sonnet)")
    parser.add_argument("--tokens-per-chunk", type=int, default=300,
                        help="Tokens per chunk (default 300)")
    parser.add_argument("--sensitivity", action="store_true",
                        help="Run ±50% sweep on each input and report ranking shifts")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON instead of markdown")
    args = parser.parse_args()

    p = PricingInputs(
        embedding_price_per_1m_tokens=args.embedding_price,
        vector_db_price_per_1k_vectors_month=args.vector_db_price,
        llm_input_price_per_1m_tokens=args.llm_input_price,
        tokens_per_chunk=args.tokens_per_chunk,
        pages=args.pages,
        queries_per_day=args.queries_per_day,
    )
    rows = cost_table(p)

    if args.json:
        out = {
            "pricing": asdict(p),
            "rows": rows,
        }
        if args.sensitivity:
            out["sensitivity"] = sensitivity_sweep(p)
        print(json.dumps(out, indent=2))
        return

    print("# Cost calculator output")
    print()
    print(render_markdown_table(rows, p))
    print()
    if args.sensitivity:
        baseline = [r["tool"] for r in rows]
        print("## Sensitivity sweep (±50% per input)")
        print()
        print(render_sensitivity_table(sensitivity_sweep(p), baseline))


if __name__ == "__main__":
    main()
