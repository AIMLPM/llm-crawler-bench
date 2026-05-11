"""Defense-in-depth for the JUDGE_MODEL / ANSWER_MODEL / EMBEDDING_MODEL
drift surface (v1.4 DS-13a prep).

Two functions:

  - assert_*_model() raises SystemExit BEFORE any API spend if a model
    env var has been overridden to a non-canonical value. The PUBLISH-BOTH
    secondary (DS-13a) allows EMBEDDING_MODEL to be the mxbai model in
    addition to the OpenAI default; ANSWER_MODEL and JUDGE_MODEL are
    locked to gpt-4o-mini so the leaderboard delta between primary and
    secondary cleanly attributes to embedder choice alone.

  - write_models_manifest() appends a per-phase section to
    runs/<run_id>/models_manifest.json with resolved model names, temps,
    detected env overrides, and the git commit. Reviewers can audit
    after-the-fact whether two runs were made under the same conditions.

Why this exists: gpt-4o-mini at temp=0 is mostly-but-not-100% deterministic;
that noise is symmetric across runs (both draw the same model with the
same params) so it's absorbed by the single-trial caveat. But if an
operator accidentally exports JUDGE_MODEL=gpt-4o for the secondary run,
the leaderboard delta confounds embedder choice with judge-model choice.
The assertion closes that drift surface so future cycles can't silently
desync across two dimensions even if the runbook hygiene is forgotten."""

from __future__ import annotations

import datetime
import json
import os
import subprocess
from pathlib import Path
from typing import Optional

CANONICAL_ANSWER_MODEL = "gpt-4o-mini"
CANONICAL_JUDGE_MODEL = "gpt-4o-mini"

# EMBEDDING_MODEL is the only model the spec ALLOWS to be overridden — but
# only to the PUBLISH-BOTH secondary. Anything else (bge-large, openai-3-large,
# etc.) is methodology drift and the assertion fires.
CANONICAL_EMBEDDING_MODELS = frozenset({
    "text-embedding-3-small",                   # OpenAI primary
    "mixedbread-ai/mxbai-embed-large-v1",       # PUBLISH-BOTH local secondary (DS-13a)
})


def assert_answer_model(answer_model: str) -> None:
    if answer_model != CANONICAL_ANSWER_MODEL:
        raise SystemExit(
            f"ANSWER_MODEL drift: got {answer_model!r}, expected "
            f"{CANONICAL_ANSWER_MODEL!r}. Unset the ANSWER_MODEL env var, "
            f"or update CANONICAL_ANSWER_MODEL + methodology."
        )


def assert_judge_model(judge_model: str) -> None:
    if judge_model != CANONICAL_JUDGE_MODEL:
        raise SystemExit(
            f"JUDGE_MODEL drift: got {judge_model!r}, expected "
            f"{CANONICAL_JUDGE_MODEL!r}. Unset the JUDGE_MODEL env var, "
            f"or update CANONICAL_JUDGE_MODEL + methodology."
        )


def assert_embedding_model(embedding_model: str) -> None:
    if embedding_model not in CANONICAL_EMBEDDING_MODELS:
        raise SystemExit(
            f"EMBEDDING_MODEL drift: got {embedding_model!r}, expected one of "
            f"{sorted(CANONICAL_EMBEDDING_MODELS)!r}. PUBLISH-BOTH allows only "
            f"the listed values; introducing a new embedder is a methodology "
            f"change that needs its own spec entry."
        )


def detect_env_overrides() -> list[str]:
    """List of model env vars resolved from an env var rather than the
    code default. Records the override regardless of whether the value
    matches canonical — assertion handles the canonical check; manifest
    documents the override happened for the audit trail."""
    overrides = []
    for key in ("ANSWER_MODEL", "JUDGE_MODEL", "EMBEDDING_MODEL"):
        val = os.environ.get(key)
        if val is not None:
            overrides.append(f"{key}={val}")
    return overrides


def get_git_commit() -> Optional[str]:
    """Current git HEAD sha, or None if not in a git checkout."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5, check=True,
        )
        return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        return None


def write_models_manifest(
    run_dir: Path,
    phase: str,
    *,
    answer_model: Optional[str] = None,
    judge_model: Optional[str] = None,
    embedding_model: Optional[str] = None,
    answer_temperature: Optional[float] = None,
    judge_temperature: Optional[float] = None,
) -> Path:
    """Append a per-phase section to runs/<run_id>/models_manifest.json.

    Reads existing manifest if present, merges this phase's section in,
    writes back atomically. Multiple phases (retrieval / answer_quality /
    pipeline) coexist as sibling keys in the manifest dict."""
    manifest_path = run_dir / "models_manifest.json"

    section: dict[str, object] = {
        "started_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "env_overrides_detected": detect_env_overrides(),
        "git_commit": get_git_commit(),
    }
    if answer_model is not None:
        section["answer_model"] = answer_model
    if judge_model is not None:
        section["judge_model"] = judge_model
    if embedding_model is not None:
        section["embedding_model"] = embedding_model
    if answer_temperature is not None:
        section["answer_temperature"] = answer_temperature
    if judge_temperature is not None:
        section["judge_temperature"] = judge_temperature

    if manifest_path.is_file():
        try:
            existing = json.loads(manifest_path.read_text())
            if not isinstance(existing, dict):
                existing = {}
        except json.JSONDecodeError:
            existing = {}
    else:
        existing = {}

    existing[phase] = section

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = manifest_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(existing, indent=2, sort_keys=True))
    tmp.replace(manifest_path)
    return manifest_path
