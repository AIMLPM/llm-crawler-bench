#!/usr/bin/env python3
"""Interactive CLI for hand-judging the v1.5 calibration ground truth.

Loops through `bench/calibration_ground_truth_v15.csv` row by row, shows the
site / URL / title / content snippet, and reads a single keystroke verdict.

Single-key controls:
  h          → mark HELPFUL, advance to next
  n          → mark NON-HELPFUL, advance to next
  s          → skip (leave ground_truth blank, advance)
  f          → toggle full-snippet view (default 600 chars)
  b          → step back one row (lets you re-judge the previous)
  q          → save and quit

Auto-skips rows that already have ground_truth filled. Use --redo to
re-judge already-completed rows. Saves the CSV after every keystroke so
you can quit anytime without losing progress.

Run:
    .venv/bin/python tools/hand_judge_cli.py
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import termios
import tty
from collections import Counter
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "bench" / "calibration_ground_truth_v15.csv"
SNIPPET_DEFAULT_CHARS = 600
VALID_GROUND_TRUTHS = {"HELPFUL", "NON-HELPFUL"}


def _getch() -> str:
    """Read a single keystroke from stdin (macOS / Linux only)."""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch


def _clear() -> None:
    sys.stdout.write("\x1b[H\x1b[2J\x1b[3J")
    sys.stdout.flush()


def _load_rows() -> list[dict]:
    with CSV_PATH.open() as f:
        return list(csv.DictReader(f))


def _save_rows(rows: list[dict]) -> None:
    fieldnames = list(rows[0].keys())
    tmp = CSV_PATH.with_suffix(".csv.tmp")
    with tmp.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    tmp.replace(CSV_PATH)


def _progress_summary(rows: list[dict]) -> tuple[int, int, Counter, Counter]:
    judged = [r for r in rows if r.get("ground_truth", "").strip() in VALID_GROUND_TRUTHS]
    pending = [r for r in rows if r.get("ground_truth", "").strip() not in VALID_GROUND_TRUTHS]
    by_class = Counter(r["ground_truth"].strip() for r in judged)
    by_site = Counter(r["site"] for r in pending)
    return len(judged), len(pending), by_class, by_site


def _render(rows: list[dict], idx: int, show_full: bool) -> None:
    _clear()
    n = len(rows)
    judged_n, pending_n, by_class, by_site_pending = _progress_summary(rows)
    row = rows[idx]
    snippet = row.get("content_snippet", "") or ""
    if not show_full:
        snippet = snippet[:SNIPPET_DEFAULT_CHARS]
        if len(row.get("content_snippet", "") or "") > SNIPPET_DEFAULT_CHARS:
            snippet += f"\n  ...[+{len(row.get('content_snippet', '') or '') - SNIPPET_DEFAULT_CHARS} chars; press f for full]"

    bar_width = 40
    filled = int(bar_width * judged_n / n) if n else 0
    bar = "█" * filled + "░" * (bar_width - filled)

    pending_str = ", ".join(f"{s} {c}" for s, c in by_site_pending.most_common())

    print()
    print(f"  Row {idx + 1} / {n}      Judged: {judged_n}/{n}  [{bar}]")
    print(f"  Already typed: HELPFUL={by_class.get('HELPFUL', 0)}  NON-HELPFUL={by_class.get('NON-HELPFUL', 0)}")
    if pending_str:
        print(f"  Pending per site: {pending_str}")
    print("─" * 78)
    print(f"  site:    {row.get('site', '')}")
    print(f"  url:     {row.get('url', '')}")
    print(f"  title:   {row.get('title', '')}")
    current = row.get("ground_truth", "").strip()
    if current:
        print(f"  CURRENT: {current}  (already filled; press h/n to overwrite, s to keep)")
    print("─" * 78)
    print("  Content snippet:")
    for line in snippet.splitlines():
        print(f"  {line}")
    print()
    print("─" * 78)
    print("  [h] HELPFUL    [n] NON-HELPFUL    [s] skip    [f] full snippet")
    print("  [b] back       [q] save and quit")
    print()
    sys.stdout.write("  > ")
    sys.stdout.flush()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--redo",
        action="store_true",
        help="Include already-judged rows in the loop (default: skip them).",
    )
    args = parser.parse_args()

    if not CSV_PATH.exists():
        print(f"error: {CSV_PATH} not found", file=sys.stderr)
        return 1

    rows = _load_rows()
    n = len(rows)
    if n == 0:
        print("CSV is empty.", file=sys.stderr)
        return 1

    # Find first unjudged row (or row 0 if --redo)
    if args.redo:
        idx = 0
    else:
        idx = 0
        while idx < n and rows[idx].get("ground_truth", "").strip() in VALID_GROUND_TRUTHS:
            idx += 1
        if idx >= n:
            _clear()
            judged, pending, by_class, _ = _progress_summary(rows)
            print()
            print("  All 373 rows already judged.")
            print(f"  HELPFUL: {by_class.get('HELPFUL', 0)}")
            print(f"  NON-HELPFUL: {by_class.get('NON-HELPFUL', 0)}")
            print(f"  Skipped/blank: {pending}")
            print()
            print("  Re-run with --redo to revisit any row.")
            print()
            return 0

    show_full = False
    while 0 <= idx < n:
        _render(rows, idx, show_full)
        try:
            key = _getch().lower()
        except KeyboardInterrupt:
            _save_rows(rows)
            print("\n  saved + interrupted.")
            return 0

        if key == "h":
            rows[idx]["ground_truth"] = "HELPFUL"
            _save_rows(rows)
            idx += 1
            show_full = False
            # auto-skip already-judged unless --redo
            if not args.redo:
                while idx < n and rows[idx].get("ground_truth", "").strip() in VALID_GROUND_TRUTHS:
                    idx += 1
        elif key == "n":
            rows[idx]["ground_truth"] = "NON-HELPFUL"
            _save_rows(rows)
            idx += 1
            show_full = False
            if not args.redo:
                while idx < n and rows[idx].get("ground_truth", "").strip() in VALID_GROUND_TRUTHS:
                    idx += 1
        elif key == "s":
            idx += 1
            show_full = False
            if not args.redo:
                while idx < n and rows[idx].get("ground_truth", "").strip() in VALID_GROUND_TRUTHS:
                    idx += 1
        elif key == "f":
            show_full = not show_full
        elif key == "b":
            idx = max(0, idx - 1)
            show_full = False
        elif key == "q":
            _save_rows(rows)
            _clear()
            judged, pending, by_class, _ = _progress_summary(rows)
            print()
            print(f"  Saved. Quit at row {idx + 1} / {n}.")
            print(f"  Judged so far: HELPFUL {by_class.get('HELPFUL', 0)}, NON-HELPFUL {by_class.get('NON-HELPFUL', 0)}")
            print(f"  Remaining unjudged: {pending}")
            print()
            print("  Resume any time with: .venv/bin/python tools/hand_judge_cli.py")
            print()
            return 0

    # Loop fell off the end
    _save_rows(rows)
    _clear()
    judged, pending, by_class, _ = _progress_summary(rows)
    print()
    print("  Done. All rows visited.")
    print(f"  HELPFUL: {by_class.get('HELPFUL', 0)}")
    print(f"  NON-HELPFUL: {by_class.get('NON-HELPFUL', 0)}")
    print(f"  Unjudged: {pending}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
