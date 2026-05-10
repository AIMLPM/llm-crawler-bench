"""DS-7: TEST_QUERIES loader. The v1.4 LLM-generated set must take
priority over the v1.3 hand-written set; missing both must raise
FileNotFoundError so the benchmark fails fast instead of silently
running on an empty query set."""

from __future__ import annotations

import json

import pytest

import benchmark_retrieval as br


def test_load_test_queries_prefers_v14(tmp_path, monkeypatch):
    v14 = tmp_path / "v14.json"
    v13 = tmp_path / "v13.json"
    v14.write_text(json.dumps({"site_a": [{"query": "v14 query"}]}))
    v13.write_text(json.dumps({"site_a": [{"query": "v13 query"}]}))

    monkeypatch.setattr(br, "TEST_QUERY_SOURCES", [v14, v13])
    queries = br._load_test_queries()
    assert queries["site_a"][0]["query"] == "v14 query"


def test_load_test_queries_falls_back_to_v13(tmp_path, monkeypatch):
    v14 = tmp_path / "v14.json"  # not created
    v13 = tmp_path / "v13.json"
    v13.write_text(json.dumps({"site_a": [{"query": "v13 query"}]}))

    monkeypatch.setattr(br, "TEST_QUERY_SOURCES", [v14, v13])
    queries = br._load_test_queries()
    assert queries["site_a"][0]["query"] == "v13 query"


def test_load_test_queries_raises_when_neither_exists(tmp_path, monkeypatch):
    v14 = tmp_path / "v14.json"  # not created
    v13 = tmp_path / "v13.json"  # not created

    monkeypatch.setattr(br, "TEST_QUERY_SOURCES", [v14, v13])
    with pytest.raises(FileNotFoundError):
        br._load_test_queries()
