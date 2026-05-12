"""DS-13a defense-in-depth: model-invariant assertions + manifest writer.

Locks the canonical-model contract so future cycles can't silently
desync across embedder + judge dimensions even if an operator forgets
the runbook hygiene before firing a PUBLISH-BOTH secondary run."""

import json

import pytest

import models_manifest as mm

# --- assert_answer_model -----------------------------------------------------

def test_assert_answer_model_passes_canonical():
    mm.assert_answer_model("gpt-4o-mini")  # no raise


def test_assert_answer_model_fires_on_drift():
    with pytest.raises(SystemExit, match="ANSWER_MODEL drift"):
        mm.assert_answer_model("gpt-4o")
    with pytest.raises(SystemExit, match="ANSWER_MODEL drift"):
        mm.assert_answer_model("claude-3-haiku")


# --- assert_judge_model ------------------------------------------------------

def test_assert_judge_model_passes_canonical():
    mm.assert_judge_model("gpt-4o-mini")


def test_assert_judge_model_fires_on_drift():
    with pytest.raises(SystemExit, match="JUDGE_MODEL drift"):
        mm.assert_judge_model("gpt-4o")
    with pytest.raises(SystemExit, match="JUDGE_MODEL drift"):
        mm.assert_judge_model("gpt-4o-mini-2024-07-18")  # version drift counts


# --- assert_embedding_model --------------------------------------------------

def test_assert_embedding_model_accepts_openai_primary():
    mm.assert_embedding_model("text-embedding-3-small")


def test_assert_embedding_model_accepts_mxbai_secondary():
    """PUBLISH-BOTH: mxbai is the sanctioned secondary embedder. Must pass
    so the LOCAL run isn't blocked by the assertion."""
    mm.assert_embedding_model("mixedbread-ai/mxbai-embed-large-v1")


def test_assert_embedding_model_fires_on_unknown():
    """Anything outside the canonical PUBLISH-BOTH set is methodology drift."""
    with pytest.raises(SystemExit, match="EMBEDDING_MODEL drift"):
        mm.assert_embedding_model("BAAI/bge-large-en-v1.5")
    with pytest.raises(SystemExit, match="EMBEDDING_MODEL drift"):
        mm.assert_embedding_model("text-embedding-3-large")


# --- detect_env_overrides ----------------------------------------------------

def test_detect_env_overrides_empty_when_unset(monkeypatch):
    for k in ("ANSWER_MODEL", "JUDGE_MODEL", "EMBEDDING_MODEL"):
        monkeypatch.delenv(k, raising=False)
    assert mm.detect_env_overrides() == []


def test_detect_env_overrides_lists_set_vars(monkeypatch):
    for k in ("ANSWER_MODEL", "JUDGE_MODEL", "EMBEDDING_MODEL"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("JUDGE_MODEL", "gpt-4o")
    monkeypatch.setenv("EMBEDDING_MODEL", "mixedbread-ai/mxbai-embed-large-v1")
    overrides = mm.detect_env_overrides()
    assert "JUDGE_MODEL=gpt-4o" in overrides
    assert "EMBEDDING_MODEL=mixedbread-ai/mxbai-embed-large-v1" in overrides
    assert not any(o.startswith("ANSWER_MODEL=") for o in overrides)


def test_detect_env_overrides_records_even_when_value_matches_canonical(monkeypatch):
    """If ANSWER_MODEL=gpt-4o-mini is exported (matches the default), it
    still gets recorded as an override — the manifest is the audit trail
    for "an env var was set", separate from the assertion's "value is
    canonical" check."""
    monkeypatch.setenv("ANSWER_MODEL", "gpt-4o-mini")
    overrides = mm.detect_env_overrides()
    assert "ANSWER_MODEL=gpt-4o-mini" in overrides


# --- write_models_manifest ---------------------------------------------------

def test_manifest_default_run_has_empty_overrides(tmp_path, monkeypatch):
    """Clean default run: env_overrides_detected = []."""
    for k in ("ANSWER_MODEL", "JUDGE_MODEL", "EMBEDDING_MODEL"):
        monkeypatch.delenv(k, raising=False)

    path = mm.write_models_manifest(
        tmp_path, "answer_quality",
        answer_model="gpt-4o-mini",
        judge_model="gpt-4o-mini",
        embedding_model="text-embedding-3-small",
        answer_temperature=0,
        judge_temperature=0,
    )
    data = json.loads(path.read_text())
    assert "answer_quality" in data
    section = data["answer_quality"]
    assert section["answer_model"] == "gpt-4o-mini"
    assert section["judge_model"] == "gpt-4o-mini"
    assert section["embedding_model"] == "text-embedding-3-small"
    assert section["answer_temperature"] == 0
    assert section["judge_temperature"] == 0
    assert section["env_overrides_detected"] == []
    assert "started_at" in section


def test_manifest_records_env_overrides_in_section(tmp_path, monkeypatch):
    for k in ("ANSWER_MODEL", "JUDGE_MODEL", "EMBEDDING_MODEL"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("JUDGE_MODEL", "gpt-4o-mini")  # canonical-but-overridden
    monkeypatch.setenv("EMBEDDING_MODEL", "mixedbread-ai/mxbai-embed-large-v1")

    path = mm.write_models_manifest(
        tmp_path, "answer_quality",
        answer_model="gpt-4o-mini",
        judge_model="gpt-4o-mini",
        embedding_model="mixedbread-ai/mxbai-embed-large-v1",
    )
    data = json.loads(path.read_text())
    overrides = data["answer_quality"]["env_overrides_detected"]
    assert "JUDGE_MODEL=gpt-4o-mini" in overrides
    assert "EMBEDDING_MODEL=mixedbread-ai/mxbai-embed-large-v1" in overrides


def test_manifest_multiple_phases_coexist(tmp_path, monkeypatch):
    """Retrieval phase + answer_quality phase both written; both keys
    persist (incremental update, not overwrite)."""
    for k in ("ANSWER_MODEL", "JUDGE_MODEL", "EMBEDDING_MODEL"):
        monkeypatch.delenv(k, raising=False)
    mm.write_models_manifest(tmp_path, "retrieval",
                             embedding_model="text-embedding-3-small")
    mm.write_models_manifest(tmp_path, "answer_quality",
                             answer_model="gpt-4o-mini",
                             judge_model="gpt-4o-mini",
                             embedding_model="text-embedding-3-small")
    data = json.loads((tmp_path / "models_manifest.json").read_text())
    assert "retrieval" in data
    assert "answer_quality" in data
    assert data["retrieval"]["embedding_model"] == "text-embedding-3-small"
    assert data["answer_quality"]["answer_model"] == "gpt-4o-mini"


def test_manifest_atomic_write(tmp_path, monkeypatch):
    """Pre-existing manifest gets updated atomically via .tmp + replace —
    a crashed write can't corrupt prior content."""
    for k in ("ANSWER_MODEL", "JUDGE_MODEL", "EMBEDDING_MODEL"):
        monkeypatch.delenv(k, raising=False)
    out = tmp_path / "models_manifest.json"
    out.write_text('{"stale": "data"}')
    mm.write_models_manifest(tmp_path, "retrieval",
                             embedding_model="text-embedding-3-small")
    # No leftover .tmp file
    assert not (tmp_path / "models_manifest.json.tmp").exists()
    data = json.loads(out.read_text())
    # Original key survives, new phase added (incremental merge)
    assert data.get("stale") == "data"
    assert "retrieval" in data


def test_manifest_includes_started_at_iso_format(tmp_path, monkeypatch):
    for k in ("ANSWER_MODEL", "JUDGE_MODEL", "EMBEDDING_MODEL"):
        monkeypatch.delenv(k, raising=False)
    path = mm.write_models_manifest(tmp_path, "test",
                                    answer_model="gpt-4o-mini")
    data = json.loads(path.read_text())
    started = data["test"]["started_at"]
    # ISO-8601 datetime sanity
    assert "T" in started
    assert started.endswith("+00:00") or started.endswith("Z")
