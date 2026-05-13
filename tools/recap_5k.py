#!/usr/bin/env python3
"""DS-2 (v1.5) recap helper: re-sample existing sitemap sites with cap=5000.

Re-fetches sitemap.xml for the four biggest sampled sites and re-runs the
exact same normalize/dedup/sample pipeline as build_reference_corpus.py,
but with a 5000-URL cap instead of 10000.

Only intended for one-shot use during the DS-2 cost-control re-cap on
2026-05-13 per chat.md Option B+C. Idempotent: re-running produces the
same urls.txt + sha256 because seed=42 is fixed.

Usage:
    python3 tools/recap_5k.py
    python3 tools/recap_5k.py --sites mdn-css,postgres-docs,propublica
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.build_reference_corpus import (  # noqa: E402
    OUTPUT_DIR,
    MANIFEST_PATH,
    _session,
    dedup_normalize,
    fetch_sitemap,
    load_manifest,
    load_pool_sites,
    sample_if_oversized,
    write_manifest,
    init_manifest_top_level,
    SITEMAP_SAMPLE_SEED,
)

RECAP_CAP = 5000

# The four biggest sampled sites per chat.md 2026-05-13T16:30:00Z directive.
DEFAULT_SITES = {
    "huggingface-transformers",
    "mdn-css",
    "postgres-docs",
    "propublica",
}


def write_site(site_name: str, urls, source_record):
    site_dir = OUTPUT_DIR / site_name
    site_dir.mkdir(parents=True, exist_ok=True)

    urls_path = site_dir / "urls.txt"
    blob = "\n".join(urls) + ("\n" if urls else "")
    urls_path.write_text(blob, encoding="utf-8")

    sha = hashlib.sha256(blob.encode("utf-8")).hexdigest()
    source_record["url_list_sha256"] = sha
    source_record["url_count"] = len(urls)

    source_path = site_dir / "source.json"
    with open(source_path, "w", encoding="utf-8") as f:
        json.dump(source_record, f, indent=2, sort_keys=True)
        f.write("\n")
    return sha


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--sites",
        default=None,
        help="Comma-separated subset (default: all 4 big sampled sites).",
    )
    args = ap.parse_args()

    wanted = (
        {s.strip() for s in args.sites.split(",") if s.strip()}
        if args.sites
        else DEFAULT_SITES
    )

    pool = load_pool_sites()
    target = [s for s in pool if s["name"] in wanted]
    if not target:
        print(f"No matching sites: {wanted}")
        return 1

    session = _session()
    today = _dt.date.today().isoformat()

    manifest = load_manifest()
    manifest = init_manifest_top_level(manifest)

    results = []
    for site in target:
        name = site["name"]
        url = site["url"]
        print(f"\n=== {name} ({url}) ===")
        sitemap_urls, info = fetch_sitemap(url, session)
        print(
            f"  tried={len(info['tried'])} successful={len(info['successful'])} "
            f"raw_urls={len(sitemap_urls)} errors={len(info['errors'])}"
        )
        normalized = dedup_normalize(sitemap_urls)
        print(f"  normalized+deduped = {len(normalized)}")

        final, sampled, pre = sample_if_oversized(
            normalized, RECAP_CAP, SITEMAP_SAMPLE_SEED
        )
        print(f"  cap={RECAP_CAP} sampled={sampled} pre_sample={pre} final={len(final)}")

        source_record = {
            "path": "sitemap",
            "sitemap_fetch_date": today,
            "url_count": len(final),
        }
        if sampled:
            source_record["sitemap_url_sample_seed"] = SITEMAP_SAMPLE_SEED
            source_record["sitemap_url_total_pre_sample"] = pre

        sha = write_site(name, final, source_record)
        print(f"  wrote urls.txt sha256={sha}")

        manifest.setdefault("sites", {})
        entry = manifest["sites"].get(name, {})
        entry["source"] = "sitemap"
        entry["url_count"] = len(final)
        entry["url_list_sha256"] = sha
        entry["sitemap_fetch_date"] = today
        entry["sitemap_url_sample_seed"] = SITEMAP_SAMPLE_SEED if sampled else None
        if sampled:
            entry["sitemap_url_total_pre_sample"] = pre
        manifest["sites"][name] = entry

        results.append((name, len(final), sha, pre))

    write_manifest(manifest)

    print("\n=== Summary ===")
    for name, n, sha, pre in results:
        print(f"  {name:32s} urls={n} pre_sample={pre} sha256={sha[:12]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
