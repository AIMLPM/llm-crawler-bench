#!/usr/bin/env python3
"""10-URL prototype for browser-assisted hand-judging.

Tests the UX flow proposed in chat.md before committing to building the full
373-URL version. Does NOT write to the calibration CSV — only prints results
at the end so we can decide which variant to commit to.

Picks a stratified sample (3 rust-book + 3 newegg + 2 propublica + 2 HF).

Single-key controls:
  h          → mark HELPFUL, advance
  n          → mark NON-HELPFUL, advance
  o          → open URL in default browser (then return to terminal and judge)
  s          → skip
  b          → back one row (revisit)
  q          → quit early

Run:
    .venv/bin/python tools/hand_judge_browser_prototype.py
"""

from __future__ import annotations

import csv
import random
import subprocess
import sys
import termios
import tty
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "bench" / "calibration_ground_truth_v15.csv"


_TTY_AVAILABLE: bool | None = None


def _has_tty() -> bool:
    global _TTY_AVAILABLE
    if _TTY_AVAILABLE is not None:
        return _TTY_AVAILABLE
    try:
        fd = sys.stdin.fileno()
        termios.tcgetattr(fd)
        _TTY_AVAILABLE = True
    except (termios.error, OSError, ValueError):
        _TTY_AVAILABLE = False
    return _TTY_AVAILABLE


def _getch() -> str:
    """Read one key. If no TTY available, fall back to line input."""
    if _has_tty():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch
    # Fallback: line-input mode (works in non-TTY contexts like Claude Code's
    # `!` subprocess). User must press Enter after each key.
    try:
        line = input()
    except EOFError:
        return "q"
    return (line[:1] if line else "").lower()


def _clear() -> None:
    sys.stdout.write("\x1b[H\x1b[2J\x1b[3J")
    sys.stdout.flush()


def _open_in_browser(url: str) -> None:
    try:
        subprocess.run(["open", url], check=False, timeout=5)
    except (subprocess.SubprocessError, OSError):
        pass


def _pick_sample(rows: list[dict], seed: int = 42) -> list[dict]:
    """3 rust-book + 3 newegg + 2 propublica + 2 HF, dedup'd by URL."""
    rng = random.Random(seed)
    by_site: dict[str, list[dict]] = {}
    for r in rows:
        by_site.setdefault(r["site"], []).append(r)

    sample: list[dict] = []
    targets = {
        "rust-book": 3,
        "newegg": 3,
        "propublica": 2,
        "huggingface-transformers": 2,
    }
    for site, n in targets.items():
        # Dedupe by URL first (CSV occasionally has duplicate URLs)
        seen: set[str] = set()
        pool: list[dict] = []
        for r in by_site.get(site, []):
            u = r.get("url", "")
            if u and u not in seen:
                seen.add(u)
                pool.append(r)
        if not pool:
            continue
        sample.extend(rng.sample(pool, min(n, len(pool))))
    return sample


def _render(rows: list[dict], idx: int, judgments: dict[int, str]) -> None:
    _clear()
    n = len(rows)
    done = sum(1 for v in judgments.values() if v in ("HELPFUL", "NON-HELPFUL"))
    bar_w = 30
    filled = int(bar_w * done / n) if n else 0
    bar = "█" * filled + "░" * (bar_w - filled)

    row = rows[idx]
    print()
    print(f"  Row {idx + 1} / {n}    Judged: {done}/{n}  [{bar}]")
    print(f"  Site: {row.get('site', '')}")
    print("─" * 78)
    print(f"  URL:   {row.get('url', '')}")
    print(f"  TITLE: {row.get('title', '')}")
    current = judgments.get(idx)
    if current:
        print(f"  CURRENT: {current}  (you can overwrite with h or n)")
    print("─" * 78)
    print("  [h] HELPFUL    [n] NON-HELPFUL    [o] open in browser")
    print("  [s] skip       [b] back           [q] quit")
    if not _has_tty():
        print("  (no TTY detected — type one letter then press Enter)")
    print()
    sys.stdout.write("  > ")
    sys.stdout.flush()


def main() -> int:
    # Hard precondition: this script needs interactive stdin.
    # Claude Code's `!` prefix runs subprocesses without an interactive
    # stdin, which silently EOFs on the first read and makes the script
    # auto-complete without any judgments. Detect and fail loudly.
    if not sys.stdin.isatty():
        print()
        print("  ERROR: This script needs an interactive terminal.")
        print()
        print("  You're running it in a non-interactive subprocess (e.g.,")
        print("  Claude Code's `!` prefix, a CI pipeline, or `echo ... | python`),")
        print("  which closes stdin and prevents single-key input.")
        print()
        print("  To run interactively, open Terminal.app / iTerm / your shell, then:")
        print()
        print("      cd /Users/paulsave/documents/coding/llm-crawler-benchmarks")
        print("      .venv/bin/python tools/hand_judge_browser_prototype.py")
        print()
        return 2

    if not CSV_PATH.exists():
        print(f"error: {CSV_PATH} not found", file=sys.stderr)
        return 1

    with CSV_PATH.open() as f:
        all_rows = list(csv.DictReader(f))

    sample = _pick_sample(all_rows, seed=42)
    if not sample:
        print("error: empty sample", file=sys.stderr)
        return 1

    judgments: dict[int, str] = {}
    idx = 0
    n = len(sample)

    while 0 <= idx < n:
        _render(sample, idx, judgments)
        try:
            key = _getch().lower()
        except KeyboardInterrupt:
            print("\n  interrupted.")
            break

        if key == "h":
            judgments[idx] = "HELPFUL"
            idx += 1
        elif key == "n":
            judgments[idx] = "NON-HELPFUL"
            idx += 1
        elif key == "o":
            _open_in_browser(sample[idx]["url"])
            # Stay on same row; let user judge after seeing browser
        elif key == "s":
            judgments[idx] = "SKIPPED"
            idx += 1
        elif key == "b":
            idx = max(0, idx - 1)
        elif key == "q":
            break
        # any other key: ignore, re-render

    _clear()
    print()
    print(f"  Prototype done. {len(judgments)} of {n} rows touched.")
    print("=" * 78)
    print(f"  {'#':>2}  {'site':<25}  {'verdict':<12}  url")
    print("─" * 78)
    for i, r in enumerate(sample):
        v = judgments.get(i, "(unjudged)")
        print(f"  {i+1:>2}  {r.get('site', ''):<25}  {v:<12}  {r.get('url', '')[:60]}")
    print()
    print("  NOTE: This was a prototype run; the calibration CSV was NOT modified.")
    print("        Tell markcrawl-agent what felt right or wrong about the UX and")
    print("        I'll build the full 373-URL version accordingly.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
