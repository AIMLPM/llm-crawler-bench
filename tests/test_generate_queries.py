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


# --- strip_nav_chrome tests --------------------------------------------------
# Generic chrome stripper that runs before MAX_PAGE_CHARS. Crucial for
# kubernetes-docs-style pages where 6K+ chars of nav prepend the actual
# content. Tests lock the heuristic so a future regression is loud.

def test_link_dominated_detects_toc_entry():
    """Standard TOC entry: indented bullet + link."""
    assert gq._is_link_dominated("  * [Chapter 1: Introduction](https://x.com/ch01)")
    assert gq._is_link_dominated("[Spanish](https://x.com/es)")
    assert gq._is_link_dominated("[v1.36](url) | [v1.35](url) | [v1.34](url)")


def test_link_dominated_does_not_flag_prose_with_inline_links():
    """Prose with one inline link should NOT be flagged — most chars are non-link."""
    line = "The borrow checker, described in [Chapter 4](url), prevents dangling references."
    assert not gq._is_link_dominated(line)


def test_link_dominated_blank_line_neutral():
    assert not gq._is_link_dominated("")
    assert not gq._is_link_dominated("   ")


def test_strip_nav_chrome_removes_long_toc():
    """5+ consecutive link-dominated lines get dropped."""
    text = """\
Some real prose introducing the topic.

  * [Chapter 1](url1)
  * [Chapter 2](url2)
  * [Chapter 3](url3)
  * [Chapter 4](url4)
  * [Chapter 5](url5)
  * [Chapter 6](url6)

The borrow checker prevents dangling references."""
    out = gq.strip_nav_chrome(text)
    assert "Some real prose" in out
    assert "borrow checker" in out
    assert "Chapter 1" not in out
    assert "Chapter 6" not in out


def test_strip_nav_chrome_preserves_short_link_clusters():
    """A run of <5 link-dominated lines (likely inline link cluster in prose)
    is preserved — we don't want to strip 2-3 references."""
    text = """\
Header paragraph.

[Reference 1](url)
[Reference 2](url)
[Reference 3](url)

Footer paragraph."""
    out = gq.strip_nav_chrome(text)
    assert "Reference 1" in out
    assert "Reference 3" in out


def test_strip_nav_chrome_drops_locale_block():
    """Sequences of (LangName) link entries common at page footers."""
    text = """\
This page documents the foo feature.

[English](url)
[Chinese](url)
[Japanese](url)
[Korean](url)
[Spanish](url)
[French](url)
[German](url)
[Italian](url)

End of page."""
    out = gq.strip_nav_chrome(text)
    assert "documents the foo feature" in out
    assert "End of page" in out
    assert "Chinese" not in out
    assert "Korean" not in out


def test_strip_nav_chrome_pure_nav_page_collapses():
    """A page that is 100% nav should reduce to mostly empty — exactly
    what we want for sitemap pages so the LLM correctly returns []."""
    text = "\n".join(f"  * [Item {i}](url{i})" for i in range(20))
    out = gq.strip_nav_chrome(text)
    # All 20 nav lines stripped; result is just blank-ish
    assert "Item 1" not in out
    assert "Item 19" not in out


def test_strip_nav_chrome_handles_blank_lines_inside_run():
    """Blanks interleaved with nav lines shouldn't break the run — they
    get dropped along with the surrounding nav."""
    text = """\
Real content here.

  * [A](url)
  * [B](url)

  * [C](url)
  * [D](url)
  * [E](url)

More real content."""
    out = gq.strip_nav_chrome(text)
    assert "Real content" in out
    assert "More real content" in out
    assert "[A](url)" not in out
    assert "[E](url)" not in out


def test_strip_nav_chrome_does_not_touch_pure_prose():
    """Idempotency on prose-only text."""
    text = "This is a paragraph.\n\nThis is another paragraph with no links at all."
    assert gq.strip_nav_chrome(text) == text


# --- is_locale_mirror_url tests ---------------------------------------------
# v1.4 sampler is English-only-by-design. Locale-mirror URLs must be
# filtered from the pool before sampling — otherwise the LLM generates
# queries in the page's native language, creating a per-tool fairness
# confound (tools that crawl locale mirrors get asymmetric advantage on
# multilingual queries).

def test_is_locale_mirror_url_iso639():
    assert gq.is_locale_mirror_url("https://he.react.dev/learn/state")
    assert gq.is_locale_mirror_url("https://ar.react.dev/learn/state")
    assert gq.is_locale_mirror_url("https://ko.react.dev/learn/state")
    assert gq.is_locale_mirror_url("https://ja.react.dev/learn/state")


def test_is_locale_mirror_url_bcp47_region():
    assert gq.is_locale_mirror_url("https://zh-cn.react.dev/learn/state")
    assert gq.is_locale_mirror_url("https://pt-br.react.dev/learn/state")
    assert gq.is_locale_mirror_url("https://en-us.react.dev/learn/state")


def test_is_locale_mirror_url_canonical_is_kept():
    """Canonical (no locale prefix) and content-subdomain URLs must NOT
    be filtered."""
    assert not gq.is_locale_mirror_url("https://react.dev/learn/state")
    assert not gq.is_locale_mirror_url("https://docs.stripe.com/api/webhooks")
    assert not gq.is_locale_mirror_url("https://api.openai.com/v1/embed")
    assert not gq.is_locale_mirror_url("https://www.newegg.com/product")


def test_is_locale_mirror_url_malformed():
    """Non-URL inputs return False rather than raising."""
    assert not gq.is_locale_mirror_url("")
    assert not gq.is_locale_mirror_url(None)  # type: ignore[arg-type]
    assert not gq.is_locale_mirror_url(123)  # type: ignore[arg-type]


# --- is_in_site_scope tests ------------------------------------------------
# v1.4 truth-in-labeling: queries must come from the canonical scope the
# site name PROMISES. Caught 2026-05-11 when 91% of huggingface-transformers
# queries were off-topic (endpoints.* product UI, discuss.* forum) because
# the source-tool had crawled the broader eTLD+1.

def test_is_in_site_scope_accepts_in_scope_url():
    assert gq.is_in_site_scope("https://huggingface.co/docs/transformers/model_doc/bert",
                                "huggingface-transformers")
    assert gq.is_in_site_scope("https://kubernetes.io/docs/tasks/run-application/",
                                "kubernetes-docs")
    assert gq.is_in_site_scope("https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html",
                                "rust-book")


def test_is_in_site_scope_rejects_off_host_for_hf():
    """The headline case: endpoints.huggingface.co + discuss.huggingface.co
    are SAME eTLD+1 but OUT of the docs/transformers scope. Filter them."""
    assert not gq.is_in_site_scope("https://endpoints.huggingface.co/something",
                                    "huggingface-transformers")
    assert not gq.is_in_site_scope("https://discuss.huggingface.co/t/12345",
                                    "huggingface-transformers")


def test_is_in_site_scope_rejects_off_path_within_same_host():
    """huggingface.co/blog is the same host as huggingface.co/docs/transformers
    but a different scope. Filter it."""
    assert not gq.is_in_site_scope("https://huggingface.co/blog/announcement",
                                    "huggingface-transformers")
    assert not gq.is_in_site_scope("https://huggingface.co/spaces/foo/bar",
                                    "huggingface-transformers")


def test_is_in_site_scope_rust_book_multi_prefix():
    """rust-book scope accepts both /book and /stable/book (same content
    version-pinned at two URLs). /reference and /std are not the book."""
    assert gq.is_in_site_scope("https://doc.rust-lang.org/book/ch04-01.html",
                                "rust-book")
    assert gq.is_in_site_scope("https://doc.rust-lang.org/stable/book/ch04-01.html",
                                "rust-book")
    assert not gq.is_in_site_scope("https://doc.rust-lang.org/reference/items.html",
                                    "rust-book")
    assert not gq.is_in_site_scope("https://doc.rust-lang.org/std/result/enum.Result.html",
                                    "rust-book")


def test_is_in_site_scope_unknown_site_is_permissive():
    """Sites without an explicit scope_prefix entry don't block — so a
    new site added before its scope is set still works."""
    assert gq.is_in_site_scope("https://anywhere.example.com/foo",
                                "newly-added-site")


def test_is_in_site_scope_malformed_input():
    assert not gq.is_in_site_scope(None, "rust-book")  # type: ignore[arg-type]
    assert not gq.is_in_site_scope(123, "rust-book")  # type: ignore[arg-type]


def test_load_pages_filters_out_of_scope_urls(tmp_path):
    """The headline integration test: HF endpoints + discuss URLs are dropped."""
    site_dir = tmp_path / "tool" / "huggingface-transformers"
    site_dir.mkdir(parents=True)
    pages_path = site_dir / "pages.jsonl"
    pages_path.write_text(
        json.dumps({"url": "https://huggingface.co/docs/transformers/model_doc/bert", "markdown": "x"}) + "\n"
        + json.dumps({"url": "https://endpoints.huggingface.co/product", "markdown": "x"}) + "\n"
        + json.dumps({"url": "https://discuss.huggingface.co/t/12345", "markdown": "x"}) + "\n"
        + json.dumps({"url": "https://huggingface.co/blog/announcement", "markdown": "x"}) + "\n"
        + json.dumps({"url": "https://huggingface.co/docs/transformers/installation", "markdown": "x"}) + "\n"
    )
    pages = gq.load_pages_for_site(tmp_path, "tool", "huggingface-transformers")
    urls = {p["url"] for p in pages}
    assert urls == {
        "https://huggingface.co/docs/transformers/model_doc/bert",
        "https://huggingface.co/docs/transformers/installation",
    }, f"Out-of-scope HF URLs should be filtered. Got: {urls}"


def test_load_pages_filters_locale_mirrors(tmp_path):
    """Integration: load_pages_for_site must drop locale-mirror URLs."""
    site_dir = tmp_path / "tool" / "site"
    site_dir.mkdir(parents=True)
    pages_path = site_dir / "pages.jsonl"
    pages_path.write_text(
        json.dumps({"url": "https://react.dev/learn/state", "markdown": "x"}) + "\n"
        + json.dumps({"url": "https://he.react.dev/learn/state", "markdown": "x"}) + "\n"
        + json.dumps({"url": "https://react.dev/learn/effects", "markdown": "x"}) + "\n"
        + json.dumps({"url": "https://ar.react.dev/learn/effects", "markdown": "x"}) + "\n"
        + json.dumps({"url": "https://zh-cn.react.dev/learn/state", "markdown": "x"}) + "\n"
    )
    pages = gq.load_pages_for_site(tmp_path, "tool", "site")
    urls = {p["url"] for p in pages}
    assert urls == {
        "https://react.dev/learn/state",
        "https://react.dev/learn/effects",
    }, f"Locale mirrors should be filtered. Got: {urls}"
