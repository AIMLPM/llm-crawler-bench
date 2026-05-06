#!/usr/bin/env python3
"""Compare two retrieval reports (OpenAI vs mxbai) and report leaderboard stability.

Reads RETRIEVAL_COMPARISON.md (primary) + RETRIEVAL_COMPARISON_LOCAL.md (secondary),
extracts per-tool / per-site MRR + Hit@1, computes Kendall's tau on rankings,
prints decision-criteria verdict per the v1.4 spec validation methodology.

Usage:
    python tools/compare_embedders.py
    python tools/compare_embedders.py \\
        --primary reports/RETRIEVAL_COMPARISON.md \\
        --secondary reports/RETRIEVAL_COMPARISON_LOCAL.md
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class ReportData:
    label: str
    overall: Dict[str, Dict[str, float]]  # tool -> {"mrr": float, "hit_at_10": float, "best_mode": str}
    per_site: Dict[str, Dict[str, Dict[str, float]]]  # site -> tool -> {"mrr": float, "hit_at_1": float, ...}


def _parse_overall_table(text: str) -> Dict[str, Dict[str, float]]:
    """Parse the 'Quick summary: best retrieval mode per tool' table."""
    out = {}
    # Find "## Quick summary: best retrieval mode per tool" then the next table
    m = re.search(r"## Quick summary: best retrieval mode per tool", text)
    if not m:
        return out
    sub = text[m.end():]
    end = re.search(r"\n## ", sub)
    sub = sub[: end.start() if end else len(sub)]
    # Rows: | tool | best mode | hit@10 | mrr |
    for row in re.finditer(r"\|\s*([\w+\-]+)\s*\|\s*(\w+)\s*\|\s*(\d+)%[^|]*\|\s*([\d.]+)\s*\|", sub):
        tool, mode, hit10, mrr = row.groups()
        out[tool] = {"best_mode": mode, "hit_at_10": float(hit10) / 100.0, "mrr": float(mrr)}
    return out


def _parse_per_site_tables(text: str) -> Dict[str, Dict[str, Dict[str, float]]]:
    """Parse per-site tables. Format:
    ## <site>
    | Tool | Hit@1 | Hit@3 | Hit@5 | Hit@10 | Hit@20 | MRR | Chunks | Pages |
    | <tool> | <H1> | <H3> | <H5> | <H10> | <H20> | <MRR> | <chunks> | <pages> |
    """
    out: Dict[str, Dict[str, Dict[str, float]]] = {}
    SITES = ["react-dev", "stripe-docs", "huggingface-transformers", "kubernetes-docs",
             "postgres-docs", "mdn-css", "rust-book", "newegg", "ikea",
             "smittenkitchen", "propublica", "npr-news"]
    TOOLS = ["markcrawl", "scrapy+md", "crawl4ai", "crawl4ai-raw", "crawlee", "playwright", "colly+md"]
    for site in SITES:
        m = re.search(rf"^## {re.escape(site)}\s*$", text, re.MULTILINE)
        if not m:
            continue
        section_start = m.end()
        next_sec = re.search(r"^##\s", text[section_start:], re.MULTILINE)
        section = text[section_start: section_start + (next_sec.start() if next_sec else len(text) - section_start)]
        site_data: Dict[str, Dict[str, float]] = {}
        for tool in TOOLS:
            # Pattern: | tool | H1 | H3 | H5 | H10 | H20 | MRR | chunks | pages
            row = re.search(
                rf"\|\s*{re.escape(tool)}\s*\|\s*(\d+)%[^|]*\|\s*\d+%[^|]*\|\s*\d+%[^|]*\|\s*(\d+)%[^|]*\|\s*\d+%[^|]*\|\s*([\d.]+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|",
                section,
            )
            if row:
                hit1, hit10, mrr, chunks, pages = row.groups()
                site_data[tool] = {
                    "hit_at_1": float(hit1) / 100.0,
                    "hit_at_10": float(hit10) / 100.0,
                    "mrr": float(mrr),
                    "chunks": float(chunks),
                    "pages": float(pages),
                }
        if site_data:
            out[site] = site_data
    return out


def _kendall_tau(x: List[float], y: List[float]) -> Tuple[float, int, int, int]:
    """Compute Kendall's tau (no ties handling — assumes distinct ranks).
    Returns (tau, concordant, discordant, total_pairs)."""
    if len(x) != len(y):
        raise ValueError("inputs differ in length")
    n = len(x)
    if n < 2:
        return (0.0, 0, 0, 0)
    concordant = 0
    discordant = 0
    total = n * (n - 1) // 2
    for i in range(n):
        for j in range(i + 1, n):
            sx = x[i] - x[j]
            sy = y[i] - y[j]
            prod = sx * sy
            if prod > 0:
                concordant += 1
            elif prod < 0:
                discordant += 1
    if total == 0:
        return (0.0, 0, 0, 0)
    return ((concordant - discordant) / total, concordant, discordant, total)


def _verdict(tau: float) -> Tuple[str, str]:
    """Decision criteria per v1.4 spec validation pass."""
    if tau >= 0.85:
        return ("SAFE-TO-SWITCH", "mxbai is safe as primary. Co-publish or switch.")
    elif tau >= 0.6:
        return ("PUBLISH-BOTH", "Publish both leaderboards; label embedder choice as a methodology variable.")
    else:
        return ("KEEP-OPENAI-PRIMARY", "Embedder is a real confound; mxbai stays secondary, OpenAI 3-small remains primary.")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--primary", default="reports/RETRIEVAL_COMPARISON.md",
                   help="Primary (OpenAI 3-small) report")
    p.add_argument("--secondary", default="reports/RETRIEVAL_COMPARISON_LOCAL.md",
                   help="Secondary (mxbai local) report")
    args = p.parse_args()

    primary_text = Path(args.primary).read_text()
    secondary_text = Path(args.secondary).read_text()

    primary = ReportData("openai-3-small",
                         _parse_overall_table(primary_text),
                         _parse_per_site_tables(primary_text))
    secondary = ReportData("mxbai-embed-large-v1",
                           _parse_overall_table(secondary_text),
                           _parse_per_site_tables(secondary_text))

    if not primary.overall or not secondary.overall:
        print("ERROR: failed to parse overall summary from one or both reports", file=sys.stderr)
        print(f"  primary tools parsed: {list(primary.overall.keys())}", file=sys.stderr)
        print(f"  secondary tools parsed: {list(secondary.overall.keys())}", file=sys.stderr)
        sys.exit(1)

    # ============================================================
    # Per-tool MRR delta (mxbai − openai) for overall summary
    # ============================================================
    print("=" * 90)
    print("v1.4 EMBEDDER VALIDATION — mxbai-embed-large-v1 vs openai/text-embedding-3-small")
    print("=" * 90)
    print()
    tools = sorted(set(primary.overall.keys()) & set(secondary.overall.keys()),
                   key=lambda t: -primary.overall[t]["mrr"])
    print("--- Overall leaderboard MRR (best mode per tool) ---")
    print(f"{'Tool':<14} {'OpenAI':>8} {'mxbai':>8} {'Δ':>8}  {'verdict'}")
    for tool in tools:
        o = primary.overall[tool]["mrr"]
        m = secondary.overall[tool]["mrr"]
        delta = m - o
        sign = "↑" if delta > 0 else ("↓" if delta < 0 else "=")
        print(f"  {tool:<12} {o:>7.3f}  {m:>7.3f}  {delta:>+7.3f} {sign}")

    # ============================================================
    # Kendall's tau on overall ranking
    # ============================================================
    print()
    print("--- Kendall's tau on overall leaderboard ---")
    primary_ranks = [primary.overall[t]["mrr"] for t in tools]
    secondary_ranks = [secondary.overall[t]["mrr"] for t in tools]
    tau, conc, disc, total = _kendall_tau(primary_ranks, secondary_ranks)
    print(f"  Tau = {tau:+.3f}  (concordant pairs: {conc}, discordant: {disc}, total: {total})")
    verdict_label, verdict_msg = _verdict(tau)
    print(f"  → {verdict_label}: {verdict_msg}")

    # ============================================================
    # Per-site rank stability
    # ============================================================
    print()
    print("--- Per-site ranking stability ---")
    print(f"{'Site':<26} {'tools':>5} {'tau':>7} {'verdict':<22}  per-tool MRR delta (m−o)")
    for site in sorted(set(primary.per_site.keys()) & set(secondary.per_site.keys())):
        site_tools = sorted(set(primary.per_site[site].keys()) & set(secondary.per_site[site].keys()),
                            key=lambda t: -primary.per_site[site][t]["mrr"])
        if len(site_tools) < 2:
            continue
        p_vals = [primary.per_site[site][t]["mrr"] for t in site_tools]
        s_vals = [secondary.per_site[site][t]["mrr"] for t in site_tools]
        site_tau, _, _, _ = _kendall_tau(p_vals, s_vals)
        v_label, _ = _verdict(site_tau)
        deltas = " ".join(f"{t[:5]}={(secondary.per_site[site][t]['mrr'] - primary.per_site[site][t]['mrr']):+.2f}"
                          for t in site_tools)
        print(f"  {site:<24} {len(site_tools):>5} {site_tau:>+6.3f}  {v_label:<22}  {deltas}")

    # ============================================================
    # Per-tool per-site detail
    # ============================================================
    print()
    print("--- Per-tool per-site MRR delta (mxbai − OpenAI) ---")
    sites = sorted(set(primary.per_site.keys()) & set(secondary.per_site.keys()))
    header = f"{'Tool':<14}" + "".join(f"{s[:8]:>9}" for s in sites)
    print(header)
    for tool in tools:
        row = f"  {tool:<12}"
        for site in sites:
            p_v = primary.per_site.get(site, {}).get(tool, {}).get("mrr")
            s_v = secondary.per_site.get(site, {}).get(tool, {}).get("mrr")
            if p_v is None or s_v is None:
                row += f"{'—':>9}"
            else:
                d = s_v - p_v
                row += f"{d:>+8.2f} "
        print(row)

    # ============================================================
    # Final summary
    # ============================================================
    print()
    print("=" * 90)
    print(f"FINAL VERDICT: {verdict_label}")
    print(f"  → {verdict_msg}")
    print("=" * 90)


if __name__ == "__main__":
    main()
