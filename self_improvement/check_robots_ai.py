#!/usr/bin/env python3
"""Audit a site's robots.txt for AI-bot blocks before adding it to the pool.

The benchmark is for AI/RAG use cases. Even when User-agent: * allows our
crawl, sites that explicitly disallow AI-specific bots (GPTBot, ClaudeBot,
anthropic-ai, etc.) are signaling they don't want their content used by AI
systems. The pool should respect that signal.

Usage:
    python self_improvement/check_robots_ai.py URL [URL ...]
    python self_improvement/check_robots_ai.py --pool          # check entire current pool
    python self_improvement/check_robots_ai.py --strict        # exit 1 if any AI block found

Exit codes:
    0  All sites pass (no AI-bot disallow + seed allowed)
    1  At least one site blocks AI bots (in --strict mode)
    2  At least one site disallows our seed path under User-agent: *
"""
from __future__ import annotations

import argparse
import socket
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Tuple

# Major AI/LLM bots most sites explicitly Disallow when they want to opt out.
# Adding more is fine — false positives are unlikely (these are real UA strings).
AI_BOTS = [
    "GPTBot", "ChatGPT-User", "OAI-SearchBot",  # OpenAI
    "anthropic-ai", "ClaudeBot", "Claude-Web", "Claude-SearchBot",  # Anthropic
    "Google-Extended",  # Google AI training (separate from regular Googlebot)
    "Applebot-Extended",  # Apple AI training (separate from regular Applebot)
    "PerplexityBot",
    "CCBot",  # Common Crawl (used to train many LLMs)
    "Bytespider",  # ByteDance / TikTok
    "FacebookBot", "Meta-ExternalAgent",  # Meta
    "Cohere-AI",
    "AI2Bot",  # Allen Institute
    "Diffbot",
    "Omgili",  # Webz.io / training data aggregator
    "PetalBot",  # Huawei
    "ImagesiftBot",
]

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")

REPO_ROOT = Path(__file__).resolve().parent.parent
POOL_YAML = REPO_ROOT / "sites" / "pool_v1.yaml"


def fetch_robots(seed_url: str) -> Tuple[str, str]:
    parsed = urllib.parse.urlparse(seed_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    req = urllib.request.Request(robots_url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return robots_url, r.read().decode("utf-8", errors="replace")


def parse_robots(text: str) -> Dict[str, List[str]]:
    """Return {user_agent: [disallowed_paths]}. Only Disallow tracked here."""
    rules: Dict[str, List[str]] = {}
    current_uas: List[str] = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            current_uas = []
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip().lower()
        val = val.strip()
        if key == "user-agent":
            current_uas.append(val)
            rules.setdefault(val, [])
        elif key == "disallow" and current_uas:
            for ua in current_uas:
                rules[ua].append(val)
    return rules


def seed_allowed_for_star(seed_path: str, star_disallows: List[str]) -> bool:
    """True if User-agent: * allows the seed path. Empty Disallow rules are ignored."""
    return not any(d and seed_path.startswith(d) for d in star_disallows)


def ai_bots_blocking(rules: Dict[str, List[str]]) -> List[str]:
    """Return AI bot names that have Disallow: / (full block) in robots.txt."""
    blocked = []
    for bot in AI_BOTS:
        for ua, disallows in rules.items():
            if ua.lower() == bot.lower() and "/" in disallows:
                blocked.append(bot)
                break
    return blocked


def audit(seed_url: str, label: str = "") -> Tuple[bool, str, List[str]]:
    """Returns (overall_pass, robots_url, ai_bots_blocked)."""
    try:
        robots_url, txt = fetch_robots(seed_url)
    except Exception as exc:
        return False, "", [f"FETCH_ERROR:{exc}"]
    rules = parse_robots(txt)
    seed_path = urllib.parse.urlparse(seed_url).path or "/"
    star_disallows = rules.get("*", [])
    seed_ok = seed_allowed_for_star(seed_path, star_disallows)
    blocked = ai_bots_blocking(rules)
    return (seed_ok and not blocked), robots_url, blocked


def load_pool_seeds() -> List[Tuple[str, str]]:
    """Return [(name, url)] from pool_v1.yaml. Skips sites with has_queries: false."""
    import yaml
    raw = yaml.safe_load(POOL_YAML.read_text())
    return [(s["name"], s["url"]) for s in raw["sites"] if s.get("has_queries", False)]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("urls", nargs="*", help="Seed URLs to audit")
    p.add_argument("--pool", action="store_true", help="Audit all sites in current pool_v1.yaml")
    p.add_argument("--strict", action="store_true", help="Exit code 1 if any AI block found")
    args = p.parse_args()

    targets: List[Tuple[str, str]] = []
    if args.pool:
        targets.extend(load_pool_seeds())
    for u in args.urls:
        targets.append(("(custom)", u))
    if not targets:
        p.error("Provide at least one URL or --pool")

    socket.setdefaulttimeout(20)
    any_ai_block = False
    any_seed_block = False

    print(f"{'Site':<28} {'Seed':<8} {'AI bots blocked'}")
    print("-" * 100)
    for label, seed in targets:
        ok, robots_url, blocked = audit(seed, label)
        seed_marker = "✓" if not (blocked and "FETCH_ERROR" in (blocked[0] if blocked else "")) else "?"
        if blocked and "FETCH_ERROR" in blocked[0]:
            print(f"{label:<28} {seed_marker:<8} {blocked[0]}")
            continue
        # Recompute seed status separately for clarity
        try:
            _, txt = fetch_robots(seed)
            rules = parse_robots(txt)
            seed_path = urllib.parse.urlparse(seed).path or "/"
            seed_ok = seed_allowed_for_star(seed_path, rules.get("*", []))
        except Exception:
            seed_ok = False
        seed_marker = "✓" if seed_ok else "✗ BLOCKED"
        if not seed_ok:
            any_seed_block = True
        if blocked:
            any_ai_block = True
        ai_summary = ", ".join(blocked) if blocked else "none ✓"
        print(f"{label:<28} {seed_marker:<8} {ai_summary}")

    print()
    if any_seed_block:
        print("FAIL: at least one site disallows our seed path under User-agent: *")
        sys.exit(2)
    if any_ai_block:
        print("WARN: one or more sites disallow AI bots — consider removing from pool")
        if args.strict:
            sys.exit(1)
    else:
        print("All sites are AI-permissive ✓")
    sys.exit(0)


if __name__ == "__main__":
    main()
