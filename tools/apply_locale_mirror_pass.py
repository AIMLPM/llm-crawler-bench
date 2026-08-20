#!/usr/bin/env python3
"""Apply the deterministic locale-mirror rule to an already-judged universe.

The rule (tools/judge_helpful_pages.detect_locale_scheme) landed after the
gpt-4o-mini full pool had already run. It is deterministic, so applying it
as a post-pass yields exactly what an inline run would have produced — no
re-judging, no API cost.

Only mini-HELPFUL rows are rewritten (the rule can only move a page TO
NON-HELPFUL); every rewrite records prior_classification so the change is
auditable and reversible.

Usage:
    .venv/bin/python tools/apply_locale_mirror_pass.py --dry-run
    .venv/bin/python tools/apply_locale_mirror_pass.py
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.judge_helpful_pages import (  # noqa: E402
    GPT4OMINI_OUT_DIR,
    detect_locale_scheme,
    url_locales,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    grand = 0
    for f in sorted(GPT4OMINI_OUT_DIR.glob("*.json")):
        recs = json.loads(f.read_text())
        _, mirrors = detect_locale_scheme(recs.keys())
        if not mirrors:
            print(f"{f.stem:18} no i18n scheme detected — unchanged")
            continue
        changed = 0
        for url, rec in recs.items():
            if rec.get("classification") != "HELPFUL":
                continue
            hit = next((c for c in url_locales(url) if c in mirrors), None)
            if not hit:
                continue
            changed += 1
            if not args.dry_run:
                rec.update(
                    classification="NON-HELPFUL",
                    rationale_prefix="non-helpful-mirror",
                    rationale_text=(f"URL locale segment '/{hit}/' is a translation of "
                                    f"the site's canonical locale (deterministic rule)"),
                    prior_classification="HELPFUL",
                    reclassified_at=_dt.datetime.now(_dt.UTC).isoformat(),
                    judge_call_id="deterministic-locale-mirror",
                )
        grand += changed
        print(f"{f.stem:18} {len(mirrors):2} mirror locales -> "
              f"{'would reclassify' if args.dry_run else 'reclassified'} {changed} pages")
        if changed and not args.dry_run:
            tmp = f.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(recs, indent=2))
            tmp.replace(f)

    verb = "would move" if args.dry_run else "moved"
    print(f"\nTOTAL: {verb} {grand} pages HELPFUL -> NON-HELPFUL (mirror), $0 API cost")
    return 0


if __name__ == "__main__":
    sys.exit(main())
