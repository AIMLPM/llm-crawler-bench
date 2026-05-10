"""DS-2: URL normalization. Locale subdomain prefixes + UTM/lang/random
query params must be stripped before url_match substring evaluation, so
locale-mirror URLs no longer count as hits for English queries."""

from __future__ import annotations

import benchmark_retrieval as br

# --- _normalize_url_for_matching unit tests ----------------------------------

def test_strips_known_locale_prefixes():
    """The v1.3 false positive case: he.react.dev should normalize to react.dev."""
    assert br._normalize_url_for_matching("https://he.react.dev/learn/managing-state") == \
        "https://react.dev/learn/managing-state"


def test_strips_each_iso_locale_seen_in_v13():
    cases = [
        ("https://de.react.dev/learn", "https://react.dev/learn"),
        ("https://es.react.dev/learn", "https://react.dev/learn"),
        ("https://fr.react.dev/learn", "https://react.dev/learn"),
        ("https://ja.react.dev/learn", "https://react.dev/learn"),
        ("https://zh.react.dev/learn", "https://react.dev/learn"),
        ("https://ko.react.dev/learn", "https://react.dev/learn"),
        ("https://pt.react.dev/learn", "https://react.dev/learn"),
        ("https://ru.react.dev/learn", "https://react.dev/learn"),
        ("https://ar.react.dev/learn", "https://react.dev/learn"),
        ("https://it.react.dev/learn", "https://react.dev/learn"),
        ("https://hi.react.dev/learn", "https://react.dev/learn"),
    ]
    for raw, expected in cases:
        assert br._normalize_url_for_matching(raw) == expected, f"failed on {raw}"


def test_strips_bcp47_region_variants():
    assert br._normalize_url_for_matching("https://zh-cn.react.dev/learn") == \
        "https://react.dev/learn"
    assert br._normalize_url_for_matching("https://pt-br.react.dev/learn") == \
        "https://react.dev/learn"
    assert br._normalize_url_for_matching("https://en-us.react.dev/learn") == \
        "https://react.dev/learn"


def test_preserves_legitimate_non_locale_subdomains():
    """docs.stripe.com is a content subdomain, not a locale — must NOT collapse."""
    assert br._normalize_url_for_matching("https://docs.stripe.com/api/webhooks") == \
        "https://docs.stripe.com/api/webhooks"
    assert br._normalize_url_for_matching("https://support.smittenkitchen.com/help") == \
        "https://support.smittenkitchen.com/help"
    assert br._normalize_url_for_matching("https://api.openai.com/v1/embed") == \
        "https://api.openai.com/v1/embed"


def test_strips_utm_query_params():
    assert br._normalize_url_for_matching(
        "https://react.dev/learn?utm_source=twitter&utm_medium=social&utm_campaign=v19"
    ) == "https://react.dev/learn"


def test_strips_lang_locale_random_params():
    assert br._normalize_url_for_matching("https://react.dev/learn?lang=en") == \
        "https://react.dev/learn"
    assert br._normalize_url_for_matching("https://react.dev/learn?locale=en-US") == \
        "https://react.dev/learn"
    assert br._normalize_url_for_matching("https://react.dev/learn?random=12345") == \
        "https://react.dev/learn"


def test_preserves_meaningful_query_params():
    """Only known nuisance params are stripped — id/page/version stay."""
    assert br._normalize_url_for_matching("https://react.dev/learn?id=42") == \
        "https://react.dev/learn?id=42"
    assert br._normalize_url_for_matching("https://react.dev/learn?version=19&id=42") == \
        "https://react.dev/learn?version=19&id=42"


def test_strips_fragment():
    assert br._normalize_url_for_matching("https://react.dev/learn#useState") == \
        "https://react.dev/learn"


def test_lowercases_host_and_path():
    assert br._normalize_url_for_matching("https://React.Dev/Learn/UseState") == \
        "https://react.dev/learn/usestate"


def test_combined_normalization():
    """All transforms compose: locale strip + UTM drop + lowercase + fragment drop."""
    raw = "HTTPS://He.React.Dev/Learn/Managing-State?utm_source=foo&id=7#anchor"
    expected = "https://react.dev/learn/managing-state?id=7"
    assert br._normalize_url_for_matching(raw) == expected


def test_malformed_url_falls_back():
    """Unparseable input must NOT raise — return lowercased raw rather than
    drop the chunk."""
    assert br._normalize_url_for_matching("not a url at all") == "not a url at all"


def test_non_string_input_returns_empty():
    assert br._normalize_url_for_matching(None) == ""  # type: ignore[arg-type]
    assert br._normalize_url_for_matching(123) == ""  # type: ignore[arg-type]


# --- _check_hit integration tests --------------------------------------------

def test_check_hit_uses_normalization_for_host_anchored_patterns():
    """A url_match pattern that anchors to the canonical host (scheme +
    hostname) requires normalization to match a locale-mirror URL.
    Without DS-2 the substring 'https://react.dev/...' is not present
    in 'https://he.react.dev/...' (the 'he.' breaks the prefix). With
    DS-2 normalization stripping the locale subdomain, both the locale
    mirror and the canonical match the same host-anchored pattern —
    proving _check_hit is calling _normalize_url_for_matching."""
    ranked = ["https://he.react.dev/learn/managing-state"]
    hit, rank = br._check_hit("https://react.dev/learn/managing-state", "", ranked)
    assert hit is True
    assert rank == 1


def test_check_hit_still_matches_canonical():
    ranked = ["https://react.dev/learn/state"]
    hit, rank = br._check_hit("learn/state", "", ranked)
    assert hit is True
    assert rank == 1


def test_check_hit_strips_fragment_before_match():
    """url_match patterns that include the path's tail must still match
    when the URL has a #fragment — DS-2 drops the fragment first."""
    ranked = ["https://react.dev/learn/state#useState-hook"]
    hit, rank = br._check_hit("react.dev/learn/state", "", ranked)
    assert hit is True
    assert rank == 1


def test_check_hit_no_match_returns_none():
    ranked = ["https://react.dev/learn/effects"]
    hit, rank = br._check_hit("nonexistent-pattern", "", ranked)
    assert hit is False
    assert rank is None


def test_check_hit_chunk_level_locale_mirror_still_counts():
    """DS-2 alone does NOT prevent a locale-mirror chunk from being
    counted as a hit at the chunk level — that is page-level dedup's
    job (DS-1's collapse_chunks_to_pages applied to normalized URLs).
    For chunk-level _check_hit, normalization makes the locale mirror
    EQUIVALENT to the canonical (same normalized URL → same substring
    match), so it still counts. This documents the current contract;
    the v1.3 false-positive fix is delivered by DS-1+DS-2 together."""
    ranked = ["https://he.react.dev/learn/managing-state"]
    hit, rank = br._check_hit("learn/managing-state", "", ranked)
    assert hit is True
    assert rank == 1
