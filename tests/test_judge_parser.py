"""DS-2 (v1.5): tolerant two-line output parser for the helpful-pages judge.

The judge prompt instructs the model to emit exactly two lines:
  Line 1: HELPFUL | NON-HELPFUL
  Line 2: <prefix>: <rationale>

But models occasionally drift on whitespace, miss the second line entirely,
mis-prefix the rationale, or stick the verdict mid-line. _parse_response()
must extract what it can and surface a parse_warning instead of crashing,
so downstream calibration audits can quantify format-compliance separately
from semantic agreement (per SC-3).

These cases are derived from real outputs observed in the
2026-05-13 sanity-check + 4o-mini chat-completions echoes (3 of 10 of which
emit an extra leading space or trailing markdown bold)."""

from __future__ import annotations

from tools.judge_helpful_pages import _parse_response


def _call(raw: str):
    return _parse_response(
        raw_response=raw,
        judge_call_id="test",
        input_tokens=10,
        output_tokens=10,
    )


# --- Strict cases ---------------------------------------------------------


def test_strict_helpful_two_lines():
    r = _call("HELPFUL\nhelpful-docs: API reference page for the BERT model.")
    assert r.classification == "HELPFUL"
    assert r.rationale_prefix == "helpful-docs"
    assert "BERT" in r.rationale_text
    assert r.parse_warning is None


def test_strict_non_helpful_two_lines():
    r = _call("NON-HELPFUL\nnon-helpful-index: Category landing page with no own content.")
    assert r.classification == "NON-HELPFUL"
    assert r.rationale_prefix == "non-helpful-index"
    assert "Category" in r.rationale_text
    assert r.parse_warning is None


# --- Whitespace tolerance -------------------------------------------------


def test_extra_leading_whitespace_line1():
    """gpt-4o-mini occasionally prefixes lines with a single space."""
    r = _call(" HELPFUL\nhelpful-article: ProPublica investigative piece.")
    # Strict regex would require ^\s*(...)\s*$ — our pattern handles it.
    assert r.classification == "HELPFUL"
    assert r.rationale_prefix == "helpful-article"


def test_trailing_whitespace_both_lines():
    r = _call("HELPFUL   \nhelpful-docs: Documentation page.   ")
    assert r.classification == "HELPFUL"
    assert r.rationale_prefix == "helpful-docs"
    assert r.rationale_text.strip() == "Documentation page."


def test_blank_lines_between():
    """An empty separator line should not break parse."""
    r = _call("HELPFUL\n\nhelpful-docs: API reference.")
    assert r.classification == "HELPFUL"
    assert r.rationale_prefix == "helpful-docs"


def test_extra_trailing_blank_lines():
    r = _call("NON-HELPFUL\nnon-helpful-search: Search results page.\n\n\n")
    assert r.classification == "NON-HELPFUL"
    assert r.rationale_prefix == "non-helpful-search"


# --- Missing line 2 -------------------------------------------------------


def test_missing_line2_classification_only():
    """Sometimes the model forgets the rationale entirely."""
    r = _call("HELPFUL")
    assert r.classification == "HELPFUL"
    assert r.rationale_prefix == ""
    assert r.rationale_text == ""
    # No prefix found, but classification still extracted -- no warning needed
    # on rationale because we never advance into the line-2 branch.


def test_missing_line2_non_helpful():
    r = _call("NON-HELPFUL")
    assert r.classification == "NON-HELPFUL"
    assert r.rationale_prefix == ""


# --- Wrong / missing prefix on line 2 -------------------------------------


def test_rationale_missing_prefix_falls_back_to_whole_line():
    """If the rationale lacks a `prefix:` token, we still capture the text
    and mark parse_warning so the auditor can quantify how often models
    drift from format."""
    r = _call("HELPFUL\nThis is a documentation page about Rust ownership.")
    assert r.classification == "HELPFUL"
    assert r.rationale_prefix == ""
    assert "Rust ownership" in r.rationale_text
    assert r.parse_warning is not None
    assert "rationale_missing_prefix" in r.parse_warning


def test_unknown_prefix_falls_through():
    """A prefix not in the controlled vocabulary should also flag warning."""
    r = _call("HELPFUL\nhelpful-magic: An unknown prefix the model invented.")
    # Tolerant scan won't match an undefined prefix → falls through to
    # 'rationale_missing_prefix'.
    assert r.classification == "HELPFUL"
    assert r.rationale_prefix == ""
    assert "unknown prefix" in r.rationale_text.lower()
    assert r.parse_warning is not None


def test_known_prefix_anywhere_in_line2_is_recovered():
    """Tolerant fallback: prefix appears mid-sentence, not at start."""
    r = _call("HELPFUL\nThe right tag here is helpful-howto: step-by-step tutorial.")
    assert r.classification == "HELPFUL"
    assert r.rationale_prefix == "helpful-howto"
    assert "tutorial" in r.rationale_text


# --- Variant verdict spellings -------------------------------------------


def test_non_helpful_with_space_instead_of_hyphen():
    """Some models emit 'NON HELPFUL' with a space."""
    r = _call("NON HELPFUL\nnon-helpful-nav: Navigation menu.")
    assert r.classification == "NON-HELPFUL"


def test_lowercase_verdict_recovered():
    r = _call("helpful\nhelpful-docs: API ref.")
    assert r.classification == "HELPFUL"


def test_verdict_buried_in_line1_flags_warning():
    """If line 1 contains other text around the verdict, strict regex fails
    but tolerant fallback recovers + marks parse_warning."""
    r = _call("Answer: HELPFUL.\nhelpful-docs: API doc.")
    assert r.classification == "HELPFUL"
    assert r.parse_warning is not None
    assert "line1_not_strict" in r.parse_warning


# --- Total failure --------------------------------------------------------


def test_empty_response():
    r = _call("")
    assert r.classification == "PARSE_FAILURE"
    assert r.parse_warning == "could_not_extract_classification"


def test_whitespace_only_response():
    r = _call("   \n  \n  ")
    assert r.classification == "PARSE_FAILURE"


def test_completely_off_topic_response():
    r = _call("I'm sorry, I can't classify this URL.")
    assert r.classification == "PARSE_FAILURE"
    assert r.parse_warning == "could_not_extract_classification"


# --- Cache-token plumbing -------------------------------------------------


def test_cache_tokens_round_trip():
    """The new cache_creation/read fields propagate from API response into
    the JudgeResult dataclass without affecting classification parsing."""
    r = _parse_response(
        raw_response="HELPFUL\nhelpful-docs: API.",
        judge_call_id="x",
        input_tokens=100,
        output_tokens=20,
        cache_creation_input_tokens=1131,
        cache_read_input_tokens=0,
    )
    assert r.cache_creation_input_tokens == 1131
    assert r.cache_read_input_tokens == 0
    assert r.classification == "HELPFUL"


def test_cache_tokens_default_none():
    r = _call("HELPFUL\nhelpful-docs: ok.")
    assert r.cache_creation_input_tokens is None
    assert r.cache_read_input_tokens is None


# --- Prompt loader smoke ---------------------------------------------------


def test_load_prompt_blocks_returns_two_strings():
    """v2 prompt loader should extract Block 1 (cacheable) + Block 2
    (variable template). Block 1 must be substantially longer (1024+ tokens
    needed for Anthropic cache); Block 2 should contain placeholder tokens."""
    from tools.judge_helpful_pages import load_prompt_blocks
    prefix, suffix = load_prompt_blocks()
    assert len(prefix) > len(suffix), \
        "Block 1 (cacheable prefix) should be the bulk of the prompt"
    assert "{url}" in suffix
    assert "{title}" in suffix
    assert "{content}" in suffix
    # Block 1 must include the controlled prefix vocabulary so the model
    # knows which tags to use.
    assert "helpful-docs" in prefix
    assert "non-helpful-index" in prefix


def test_format_suffix_substitutes_all_placeholders():
    from tools.judge_helpful_pages import format_suffix
    template = "URL: {url}\nTitle: {title}\nContent: {content}\nClassify."
    out = format_suffix(template, "https://x.com/a", "Page A", "Body text.")
    assert "{url}" not in out
    assert "{title}" not in out
    assert "{content}" not in out
    assert "https://x.com/a" in out
    assert "Page A" in out
    assert "Body text." in out
