#!/usr/bin/env python3
"""Fill unjudged calibration rows from the Fable draft labels.

Two accepted provenance paths (recorded in the summary this prints):
  --audited    requires the blind-sample gate: >=25 blind rows hand-judged
               and >=95% agreement with the hidden drafts.
  --ratified   pattern-ratification path: the benchmark owner explicitly
               ruled on each pattern class in conversation instead of
               clicking rows; no blind gate. Use only with that sign-off.

Existing human labels are never overwritten.

Usage:
    .venv/bin/python tools/bulk_accept_drafts.py --dry-run
    .venv/bin/python tools/bulk_accept_drafts.py --audited | --ratified
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "bench" / "calibration_ground_truth_v15.csv"
DRAFTS_PATH = ROOT / "bench" / "calibration_drafts_fable.json"
BLIND_N = 30  # must match tools/hand_judge_web.py
EXCLUDED_SITES = {"huggingface-transformers"}
VALID = {"HELPFUL", "NON-HELPFUL"}


def main() -> int:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--audited", action="store_true",
                      help="require the blind-sample agreement gate")
    mode.add_argument("--ratified", action="store_true",
                      help="pattern-ratification path (owner signed off per class)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rows = list(csv.DictReader(CSV_PATH.open()))
    drafts = json.loads(DRAFTS_PATH.read_text())["drafts"]
    active = [r for r in rows if r["site"] not in EXCLUDED_SITES]

    # Blind set must be computed identically to hand_judge_web.py.
    blind_urls = set(sorted(
        (r["url"] for r in active
         if drafts.get(r["url"], {}).get("confidence") == "high"),
        key=lambda u: hashlib.md5(u.encode()).hexdigest())[:BLIND_N])
    judged_blind = [r for r in active
                    if r["url"] in blind_urls and r["ground_truth"].strip() in VALID]
    agree = sum(1 for r in judged_blind
                if r["ground_truth"].strip() == drafts[r["url"]]["label"])
    rate = agree / len(judged_blind) if judged_blind else 0.0
    print(f"Blind sample: {agree}/{len(judged_blind)} agree "
          f"({rate:.1%} of {len(blind_urls)} blind rows judged)")

    if args.audited:
        if len(judged_blind) < 25 or rate < 0.95:
            print("GATE NOT MET: --audited needs >=25 judged blind rows at >=95% "
                  "agreement. Judge more blind rows or use --ratified with owner sign-off.")
            return 1
        provenance = f"audited (blind {agree}/{len(judged_blind)}, {rate:.1%})"
    elif args.ratified:
        provenance = "pattern-ratified by owner (no blind gate)"
    elif args.dry_run:
        provenance = "dry-run"
    else:
        print("Pick a provenance path: --audited or --ratified (or --dry-run).")
        return 1

    filled = Counter()
    kept = 0
    for r in active:
        if r["ground_truth"].strip() in VALID:
            kept += 1
            continue
        d = drafts.get(r["url"])
        if d:
            if not args.dry_run:
                r["ground_truth"] = d["label"]
            filled[(r["site"], d["label"])] += 1

    verb = "Would fill" if args.dry_run else "Filled"
    print(f"{verb} {sum(filled.values())} rows from drafts "
          f"(kept {kept} existing human labels):")
    for (site, label), n in sorted(filled.items()):
        print(f"  {site}: {n} {label}")
    print(f"Provenance: {provenance}")

    if not args.dry_run:
        tmp = CSV_PATH.with_suffix(".csv.tmp")
        with tmp.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        tmp.replace(CSV_PATH)
        print(f"Wrote {CSV_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
