"""DS-7 follow-up: answer_quality checkpoint key must include the active
TEST_QUERIES + ANSWER_MODEL + JUDGE_MODEL + EMBEDDING_MODEL so that
swapping any of them invalidates the per-(tool, site) cache.

Empirically observed 2026-05-11: first Gate 4 fire after the v1.4 query
set landed silently loaded v1.3 cached results via the "RESUMED" code
path — same class of stale-cache bug as DS-13b. This test locks the fix
so a future cycle can't accidentally re-introduce the same hole."""

from __future__ import annotations

import benchmark_answer_quality as baq


def test_models_slug_changes_with_test_queries(monkeypatch):
    monkeypatch.setattr(baq, "ANSWER_MODEL", "gpt-4o-mini")
    monkeypatch.setattr(baq, "JUDGE_MODEL", "gpt-4o-mini")
    monkeypatch.setattr(baq, "EMBEDDING_MODEL", "text-embedding-3-small")

    monkeypatch.setattr(baq, "TEST_QUERIES", {"site_a": [{"query": "v13"}]})
    slug_v13 = baq._models_slug()
    monkeypatch.setattr(baq, "TEST_QUERIES", {"site_a": [{"query": "v14"}]})
    slug_v14 = baq._models_slug()
    assert slug_v13 != slug_v14


def test_models_slug_changes_with_judge_model(monkeypatch):
    monkeypatch.setattr(baq, "TEST_QUERIES", {"site_a": [{"query": "x"}]})
    monkeypatch.setattr(baq, "ANSWER_MODEL", "gpt-4o-mini")
    monkeypatch.setattr(baq, "EMBEDDING_MODEL", "text-embedding-3-small")

    monkeypatch.setattr(baq, "JUDGE_MODEL", "gpt-4o-mini")
    a = baq._models_slug()
    monkeypatch.setattr(baq, "JUDGE_MODEL", "gpt-4o")
    b = baq._models_slug()
    assert a != b


def test_models_slug_changes_with_answer_model(monkeypatch):
    monkeypatch.setattr(baq, "TEST_QUERIES", {"site_a": [{"query": "x"}]})
    monkeypatch.setattr(baq, "JUDGE_MODEL", "gpt-4o-mini")
    monkeypatch.setattr(baq, "EMBEDDING_MODEL", "text-embedding-3-small")

    monkeypatch.setattr(baq, "ANSWER_MODEL", "gpt-4o-mini")
    a = baq._models_slug()
    monkeypatch.setattr(baq, "ANSWER_MODEL", "gpt-4o")
    b = baq._models_slug()
    assert a != b


def test_models_slug_changes_with_embedding_model(monkeypatch):
    """Embedding model affects which chunks make it into the top-K-for-answer
    step, so it has to invalidate too (PUBLISH-BOTH primary vs secondary)."""
    monkeypatch.setattr(baq, "TEST_QUERIES", {"site_a": [{"query": "x"}]})
    monkeypatch.setattr(baq, "ANSWER_MODEL", "gpt-4o-mini")
    monkeypatch.setattr(baq, "JUDGE_MODEL", "gpt-4o-mini")

    monkeypatch.setattr(baq, "EMBEDDING_MODEL", "text-embedding-3-small")
    a = baq._models_slug()
    monkeypatch.setattr(baq, "EMBEDDING_MODEL", "mixedbread-ai/mxbai-embed-large-v1")
    b = baq._models_slug()
    assert a != b


def test_checkpoint_key_changes_with_models_slug(monkeypatch):
    """End-to-end: checkpoint filename includes the models slug, so
    swapping TEST_QUERIES produces a different file."""
    monkeypatch.setattr(baq, "ANSWER_MODEL", "gpt-4o-mini")
    monkeypatch.setattr(baq, "JUDGE_MODEL", "gpt-4o-mini")
    monkeypatch.setattr(baq, "EMBEDDING_MODEL", "text-embedding-3-small")

    monkeypatch.setattr(baq, "TEST_QUERIES", {"site_a": [{"query": "v13"}]})
    key_v13 = baq._checkpoint_key("run_x", "markcrawl", "site_a")

    monkeypatch.setattr(baq, "TEST_QUERIES", {"site_a": [{"query": "v14"}]})
    key_v14 = baq._checkpoint_key("run_x", "markcrawl", "site_a")

    assert key_v13 != key_v14, (
        "answer_quality checkpoint must invalidate on TEST_QUERIES change — "
        "same class of stale-cache bug as DS-13b, fix same way."
    )
