"""DS-13b: retrieval checkpoint filenames must include the embedder slug,
so swapping EMBEDDING_MODEL between runs cannot silently load the prior
embedder's cached vectors."""

import benchmark_retrieval as br


def test_embedder_slug_passes_through_openai_default():
    assert br._embedder_slug("text-embedding-3-small") == "text-embedding-3-small"


def test_embedder_slug_normalizes_huggingface_style_names():
    assert br._embedder_slug("mixedbread-ai/mxbai-embed-large-v1") == "mixedbread-ai_mxbai-embed-large-v1"
    assert br._embedder_slug("BAAI/bge-large-en-v1.5") == "BAAI_bge-large-en-v1.5"


def test_checkpoint_key_changes_with_embedder(monkeypatch):
    monkeypatch.setattr(br, "EMBEDDING_MODEL", "text-embedding-3-small")
    openai_key = br._checkpoint_key("run_x", "markcrawl", "rust-book", "~512tok")

    monkeypatch.setattr(br, "EMBEDDING_MODEL", "mixedbread-ai/mxbai-embed-large-v1")
    mxbai_key = br._checkpoint_key("run_x", "markcrawl", "rust-book", "~512tok")

    assert openai_key != mxbai_key
    assert "text-embedding-3-small" in openai_key
    assert "mxbai-embed-large-v1" in mxbai_key


def test_load_returns_none_when_embedder_differs(tmp_path, monkeypatch):
    """The DS-13b smoke: a checkpoint written under OpenAI must NOT be
    returned by a load call running under mxbai."""
    monkeypatch.setattr(br, "CHECKPOINT_DIR", tmp_path)

    monkeypatch.setattr(br, "EMBEDDING_MODEL", "text-embedding-3-small")
    openai_key = br._checkpoint_key("run_x", "markcrawl", "rust-book", "~512tok")
    openai_path = tmp_path / f"{openai_key}.json"
    openai_path.write_text("{}")
    assert openai_path.is_file()

    monkeypatch.setattr(br, "EMBEDDING_MODEL", "mixedbread-ai/mxbai-embed-large-v1")
    mxbai_key = br._checkpoint_key("run_x", "markcrawl", "rust-book", "~512tok")
    assert mxbai_key != openai_key
    assert br._load_checkpoint("run_x", "markcrawl", "rust-book", "~512tok") is None


def test_legacy_pre_fix_checkpoint_is_bypassed(tmp_path, monkeypatch):
    """Pre-DS-13b checkpoints (no embedder slug in name) must not be
    returned even when current EMBEDDING_MODEL is the OpenAI default —
    we cannot prove what embedder wrote them, so they're invalidated."""
    monkeypatch.setattr(br, "CHECKPOINT_DIR", tmp_path)
    monkeypatch.setattr(br, "EMBEDDING_MODEL", "text-embedding-3-small")

    legacy_key = "run_x__markcrawl__rust-book__~512tok"
    (tmp_path / f"{legacy_key}.json").write_text("{}")

    assert br._load_checkpoint("run_x", "markcrawl", "rust-book", "~512tok") is None
