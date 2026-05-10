"""DS-6: Unit tests for the deterministic helpers in tools/generate_queries.py.

LLM-calling code (generate_for_site, call_llm) is exercised live during
Gate 3a/3b smoke runs and is not unit-tested here — testing those would
require mocking OpenAI which adds maintenance burden without catching
real bugs (the LLM output is what we'd be mocking anyway). The pure
parsers and URL helpers DO have tests because they're the failure modes
that bite silently in production."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent
_tools_dir = _repo_root / "tools"
if str(_tools_dir) not in sys.path:
    sys.path.insert(0, str(_tools_dir))

import generate_queries as gq  # noqa: E402

# --- parse_json_list ---------------------------------------------------------

def test_parse_json_list_clean():
    assert gq.parse_json_list('["q1?", "q2?"]') == ["q1?", "q2?"]


def test_parse_json_list_markdown_wrapped():
    assert gq.parse_json_list('```json\n["q1?", "q2?"]\n```') == ["q1?", "q2?"]


def test_parse_json_list_bare_codefence():
    assert gq.parse_json_list('```\n["q1?"]\n```') == ["q1?"]


def test_parse_json_list_empty_array():
    assert gq.parse_json_list('[]') == []


def test_parse_json_list_invalid_json_returns_empty():
    assert gq.parse_json_list('not json at all') == []


def test_parse_json_list_object_returns_empty():
    """If the LLM returns an object instead of array, treat as zero-candidates rather than crash."""
    assert gq.parse_json_list('{"q1": "value"}') == []


def test_parse_json_list_strips_blank_strings():
    assert gq.parse_json_list('["q1?", "", "  ", "q2?"]') == ["q1?", "q2?"]


# --- parse_verdict ----------------------------------------------------------

def test_parse_verdict_true():
    v = gq.parse_verdict('{"answerable": true, "rationale": "answer is in para 2"}')
    assert v == {"answerable": True, "rationale": "answer is in para 2"}


def test_parse_verdict_false():
    v = gq.parse_verdict('{"answerable": false, "rationale": "page is empty"}')
    assert v == {"answerable": False, "rationale": "page is empty"}


def test_parse_verdict_markdown_wrapped():
    v = gq.parse_verdict('```json\n{"answerable": true, "rationale": "yes"}\n```')
    assert v["answerable"] is True


def test_parse_verdict_malformed_defaults_to_rejection():
    """Malformed verifier output must default to rejection — the safer
    direction (a borderline query gets dropped) is preferred over silently
    accepting JSON-broken output."""
    v = gq.parse_verdict("not json")
    assert v["answerable"] is False
    assert "malformed" in v["rationale"].lower()


def test_parse_verdict_missing_fields_safe_defaults():
    v = gq.parse_verdict('{"answerable": true}')
    assert v["answerable"] is True
    assert v["rationale"] == ""


# --- derive_url_match -------------------------------------------------------

def test_derive_url_match_basic_path():
    assert gq.derive_url_match("https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html") == \
        "ch04-01-what-is-ownership.html"


def test_derive_url_match_trailing_slash():
    assert gq.derive_url_match("https://react.dev/learn/managing-state/") == "managing-state"


def test_derive_url_match_skips_index():
    """`/foo/index.html` should derive `foo`, not `index.html`."""
    assert gq.derive_url_match("https://example.com/managing-state/index.html") == "managing-state"


def test_derive_url_match_root_returns_empty():
    assert gq.derive_url_match("https://react.dev/") == ""


def test_derive_url_match_malformed_returns_empty():
    assert gq.derive_url_match("not a url") == "not a url"  # urlsplit treats this as a single path segment
    # Empty input is the actual malformed test
    assert gq.derive_url_match("") == ""


# --- first_path_segment -----------------------------------------------------

def test_first_path_segment():
    assert gq.first_path_segment("https://react.dev/learn/managing-state") == "learn"
    assert gq.first_path_segment("https://doc.rust-lang.org/book/ch04") == "book"
    assert gq.first_path_segment("https://react.dev/") == ""


# --- load_pages_for_site ----------------------------------------------------

def test_load_pages_skips_malformed_lines(tmp_path):
    """A corrupt JSONL line in pages.jsonl must NOT crash the loader —
    the spec requires resilient JSONL parsing per CLAUDE.md."""
    site_dir = tmp_path / "tool" / "site"
    site_dir.mkdir(parents=True)
    pages_path = site_dir / "pages.jsonl"
    pages_path.write_text(
        json.dumps({"url": "https://x/a", "markdown": "alpha"}) + "\n"
        "not valid json\n"
        "\n"  # blank
        + json.dumps({"url": "https://x/b", "markdown": "beta"}) + "\n"
    )
    pages = gq.load_pages_for_site(tmp_path, "tool", "site")
    assert len(pages) == 2
    assert pages[0]["url"] == "https://x/a"
    assert pages[1]["url"] == "https://x/b"


def test_load_pages_missing_file_returns_empty(tmp_path):
    pages = gq.load_pages_for_site(tmp_path, "nope", "nope")
    assert pages == []
