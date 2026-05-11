"""DS-3: QUERY_AUDIT.csv emitter. One row per (query × tool × rank-1-to-K)
so reviewers can spot-check any specific number without re-running."""

from __future__ import annotations

import csv

import benchmark_retrieval as br


def _make_qr(query, url_match, top_k_urls, top_k_scores):
    return br.QueryResult(
        query=query,
        description="",
        expected_url_match=url_match,
        expected_page_match="",
        top_k_urls=top_k_urls,
        top_k_scores=top_k_scores,
        hit=True,
        hit_rank=1,
        category="",
    )


def _make_result(tool, site, query_results):
    return br.ToolSiteRetrievalResult(
        tool=tool,
        site=site,
        total_queries=len(query_results),
        hits=0,
        hit_rate=0.0,
        total_chunks=0,
        total_pages=0,
        avg_chunk_words=0.0,
        query_results=query_results,
        embed_time=0.0,
        search_time=0.0,
    )


def test_audit_csv_has_expected_header(tmp_path):
    out = tmp_path / "QUERY_AUDIT.csv"
    br._write_query_audit_csv({}, out)
    with open(out, encoding="utf-8") as f:
        header = next(csv.reader(f))
    assert header == [
        "query_id", "query_text", "site", "tool", "rank",
        "url", "cosine_score", "is_hit",
        "url_match_pattern", "normalized_url",
        "page_rank_after_collapse",
    ]


def test_audit_csv_row_count_matches_queries_x_tools_x_topk(tmp_path):
    """3 queries × 2 tools × top_k=5 → 30 rows (excluding header)."""
    qrs = [
        _make_qr("q1", "state", [f"https://x.com/p{i}" for i in range(5)], [0.9, 0.8, 0.7, 0.6, 0.5]),
        _make_qr("q2", "effect", [f"https://x.com/p{i}" for i in range(5)], [0.9, 0.8, 0.7, 0.6, 0.5]),
        _make_qr("q3", "memo", [f"https://x.com/p{i}" for i in range(5)], [0.9, 0.8, 0.7, 0.6, 0.5]),
    ]
    all_results = {
        "react-dev": {
            "markcrawl": _make_result("markcrawl", "react-dev", qrs),
            "crawl4ai": _make_result("crawl4ai", "react-dev", qrs),
        },
    }
    out = tmp_path / "QUERY_AUDIT.csv"
    rows_written = br._write_query_audit_csv(all_results, out, top_k=5)
    assert rows_written == 30

    with open(out, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 30


def test_audit_csv_truncates_when_top_k_exceeds_available(tmp_path):
    """If a query only returned 3 URLs but top_k=5, write only 3 rows for
    that query — never pad with empty/None."""
    qrs = [_make_qr("q1", "state", ["https://x.com/p0", "https://x.com/p1", "https://x.com/p2"], [0.9, 0.8, 0.7])]
    all_results = {"site-a": {"tool-a": _make_result("tool-a", "site-a", qrs)}}
    out = tmp_path / "QUERY_AUDIT.csv"
    rows_written = br._write_query_audit_csv(all_results, out, top_k=5)
    assert rows_written == 3


def test_audit_csv_is_hit_uses_normalized_url(tmp_path):
    """is_hit must reflect the DS-2 normalized form, not the raw URL.
    A locale mirror URL with the right path normalizes to the canonical
    and counts as a hit."""
    qrs = [_make_qr(
        "q1",
        "react.dev/learn/state",  # host-anchored pattern
        ["https://he.react.dev/learn/state"],
        [0.9],
    )]
    all_results = {"react-dev": {"markcrawl": _make_result("markcrawl", "react-dev", qrs)}}
    out = tmp_path / "QUERY_AUDIT.csv"
    br._write_query_audit_csv(all_results, out)

    with open(out, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["is_hit"] == "true"
    assert rows[0]["normalized_url"] == "https://react.dev/learn/state"
    assert rows[0]["url"] == "https://he.react.dev/learn/state"


def test_audit_csv_query_id_stable_across_tools(tmp_path):
    """Same site+query_index produces the same query_id regardless of tool —
    so reviewers can join rows for the same query across tools."""
    qrs = [_make_qr("q1", "x", ["https://x.com/p0"], [0.9])]
    all_results = {
        "site-a": {
            "tool-a": _make_result("tool-a", "site-a", qrs),
            "tool-b": _make_result("tool-b", "site-a", qrs),
        },
    }
    out = tmp_path / "QUERY_AUDIT.csv"
    br._write_query_audit_csv(all_results, out)

    with open(out, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert rows[0]["query_id"] == rows[1]["query_id"] == "site-a:0"
    assert {rows[0]["tool"], rows[1]["tool"]} == {"tool-a", "tool-b"}


def test_audit_csv_includes_page_rank_after_collapse(tmp_path):
    """Reviewer Q1: audit CSV must expose the chunk → page collapse so a
    reviewer reading it cold can see that locale-mirror and fragment-
    variant chunks share a page_rank slot. Without this column the CSV
    looks like the bench is matching different canonicals when actually
    it's collapsing per DS-1+DS-2."""
    qrs = [_make_qr(
        "q1",
        "react.dev/learn/state",
        [
            "https://he.react.dev/learn/state",      # rank 1
            "https://react.dev/learn/state#hooks",   # rank 2 (same canonical as 1+3)
            "https://react.dev/learn/state",         # rank 3 (canonical)
            "https://react.dev/learn/effects",       # rank 4 (different canonical)
            "https://react.dev/learn/refs",          # rank 5 (different canonical)
        ],
        [0.95, 0.93, 0.91, 0.85, 0.80],
    )]
    all_results = {"react-dev": {"markcrawl": _make_result("markcrawl", "react-dev", qrs)}}
    out = tmp_path / "QUERY_AUDIT.csv"
    br._write_query_audit_csv(all_results, out)

    with open(out, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 5
    # Three chunks share the same canonical → all get page_rank 1
    assert rows[0]["page_rank_after_collapse"] == "1"
    assert rows[1]["page_rank_after_collapse"] == "1"
    assert rows[2]["page_rank_after_collapse"] == "1"
    # Different canonicals get monotonically-increasing page ranks
    assert rows[3]["page_rank_after_collapse"] == "2"
    assert rows[4]["page_rank_after_collapse"] == "3"


def test_audit_csv_atomic_write(tmp_path):
    """Write goes through a .tmp file then rename, so a crashed write
    doesn't corrupt a prior CSV."""
    out = tmp_path / "QUERY_AUDIT.csv"
    out.write_text("stale,old,header\n1,2,3\n", encoding="utf-8")  # pre-existing file
    qrs = [_make_qr("q1", "x", ["https://x.com/p0"], [0.9])]
    all_results = {"site-a": {"tool-a": _make_result("tool-a", "site-a", qrs)}}
    br._write_query_audit_csv(all_results, out)

    assert not (tmp_path / "QUERY_AUDIT.csv.tmp").exists()
    with open(out, encoding="utf-8") as f:
        first_line = f.readline().strip()
    assert first_line.startswith("query_id,query_text,site,tool,rank")  # not the stale header
