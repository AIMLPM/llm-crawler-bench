#!/usr/bin/env python3
"""DS-1 (v1.5): Build per-site reference corpora for the helpful-pages universe.

Per-site preference order (per specs/v15-helpful-pages-universe.md DS-1):

  1. Fetch the site's `sitemap.xml` (with recursive `sitemap_index.xml`
     follow). Respect robots.txt; 3-attempt backoff; 15s timeout. Parse
     `<loc>` elements, normalize via `_normalize_url_for_matching`,
     dedup. If >10000 URLs, random-sample 10000 with fixed seed=42.
  2. Fallback (sitemap missing OR <50 URLs OR robots-blocked OR fetch-
     errored): UNION-OF-TOOLS over v1.4's per-tool `pages.jsonl` files at
     `runs/run_v13_merged_20260504_203748/<tool>/<site>/pages.jsonl`.
     Normalize, dedup, cap at 5000.
  3. NO fresh single-tool reference crawl — that just relocates the
     anchor bias.

Outputs per site:
  bench/reference_corpora/<site>/urls.txt     # alphabetical, one URL per line
  bench/reference_corpora/<site>/source.json  # path + counts + dates

Also writes (or extends) the per-site partial entries in:
  bench/universe_manifest.json

DS-1 only populates the per-site sub-fields that exist at universe-build
time (source, sitemap_fetch_date OR union_of_tools_run_id, sampling seed,
url_count, url_list_sha256). DS-2 / DS-5 extend the same manifest later.

Acceptance: SC-1 — all 11 sites end up with urls.txt and ≥50 URLs.

Usage:
    python3 tools/build_reference_corpus.py
    python3 tools/build_reference_corpus.py --sites rust-book,mdn-css
    python3 tools/build_reference_corpus.py --dry-run
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import random
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Re-use the canonical normalization helper from the retrieval pipeline so
# the reference universe matches the same canonicalization rules the rest
# of the benchmark uses (locale stripping, query-param scrubbing, etc.).
from benchmark_retrieval import _normalize_url_for_matching  # noqa: E402

# --- Constants -------------------------------------------------------------

POOL_PATH = REPO_ROOT / "sites" / "pool_v1.yaml"
V14_RUN = REPO_ROOT / "runs" / "run_v13_merged_20260504_203748"
V14_TOOLS = (
    "crawl4ai",
    "crawl4ai-raw",
    "crawlee",
    "playwright",
    "colly+md",
    "scrapy+md",
    "markcrawl",
)

OUTPUT_DIR = REPO_ROOT / "bench" / "reference_corpora"
MANIFEST_PATH = REPO_ROOT / "bench" / "universe_manifest.json"

SITEMAP_CAP = 10000
UNION_CAP = 5000
SITEMAP_SAMPLE_SEED = 42
MIN_URLS_FOR_SITEMAP_ACCEPT = 50

REQUEST_TIMEOUT_S = 15
RETRIES = 3
USER_AGENT = "bench-agent-v1.5/1.0 (+https://github.com/AIMLPM/llm-crawler-benchmarks)"

# XML namespaces commonly seen in sitemaps.
NS = {
    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "xhtml": "http://www.w3.org/1999/xhtml",
}


# --- Logging --------------------------------------------------------------


def log(msg: str) -> None:
    print(f"[build_reference_corpus] {msg}", flush=True)


# --- Site config loading ---------------------------------------------------


def load_pool_sites() -> List[Dict]:
    """Return the 11 v1.4 has_queries sites in pool_v1.yaml order."""
    with open(POOL_PATH, "r", encoding="utf-8") as f:
        pool = yaml.safe_load(f)
    sites = [s for s in pool["sites"] if s.get("has_queries")]
    return sites


# --- HTTP helpers ----------------------------------------------------------


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def fetch_with_retries(
    url: str, session: requests.Session
) -> Tuple[Optional[requests.Response], Optional[str]]:
    """Fetch `url` with up to RETRIES attempts and exponential backoff.

    Returns (response_or_None, error_msg_or_None). A non-2xx is treated
    as failure (response None, error message set).
    """
    last_err = None
    for attempt in range(1, RETRIES + 1):
        try:
            resp = session.get(
                url, timeout=REQUEST_TIMEOUT_S, allow_redirects=True
            )
            if 200 <= resp.status_code < 300:
                return resp, None
            last_err = f"HTTP {resp.status_code}"
        except requests.RequestException as e:
            last_err = f"{type(e).__name__}: {e}"
        if attempt < RETRIES:
            time.sleep(1.5 ** attempt)
    return None, last_err or "unknown error"


# --- Robots ---------------------------------------------------------------


def can_fetch_sitemap(site_root: str, sitemap_url: str) -> Tuple[bool, Optional[str]]:
    """Check robots.txt for the given sitemap URL.

    Returns (allowed, reason_if_blocked). Network/parse errors default to
    "allow" (consistent with conservative non-blocking behavior for
    measurement infra; the actual sitemap fetch will surface 4xx/5xx).
    """
    try:
        parsed = urlparse(site_root)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = RobotFileParser()
        rp.set_url(robots_url)
        # urlopen used inside read() — wrap with a request to add our UA
        # via a manual fetch + feed-from-string path so we don't violate
        # site policy.
        sess = _session()
        resp = sess.get(robots_url, timeout=REQUEST_TIMEOUT_S)
        if resp.status_code >= 400:
            # No robots.txt -> allow (RFC 9309 semantics).
            return True, None
        rp.parse(resp.text.splitlines())
        allowed = rp.can_fetch(USER_AGENT, sitemap_url)
        if not allowed:
            return False, "blocked_by_robots"
        return True, None
    except Exception as e:  # noqa: BLE001
        log(f"  robots.txt check failed ({e!r}); defaulting to allow")
        return True, None


# --- Sitemap parsing -------------------------------------------------------


_LOC_RX = re.compile(r"<loc>([^<]+)</loc>", re.IGNORECASE)


def _parse_sitemap_xml(content: bytes, base_url: str) -> Tuple[List[str], List[str]]:
    """Parse a sitemap (or sitemap index) XML body.

    Returns (urls_found, nested_sitemap_urls).

    Uses xml.etree first; falls back to a regex scan for malformed-but-
    readable sitemaps (some sites emit invalid XML).
    """
    urls: List[str] = []
    nested: List[str] = []
    try:
        root = ET.fromstring(content)
        tag = root.tag.lower()
        # sitemapindex vs urlset — both contain <sitemap>/<url> children.
        if tag.endswith("sitemapindex"):
            for sm in root.findall("sm:sitemap", NS) or root.findall("sitemap"):
                loc = sm.find("sm:loc", NS)
                if loc is None:
                    loc = sm.find("loc")
                if loc is not None and loc.text:
                    nested.append(loc.text.strip())
        elif tag.endswith("urlset"):
            for u in root.findall("sm:url", NS) or root.findall("url"):
                loc = u.find("sm:loc", NS)
                if loc is None:
                    loc = u.find("loc")
                if loc is not None and loc.text:
                    urls.append(loc.text.strip())
        else:
            # Unknown root element — try a generic walk for <loc>.
            for elem in root.iter():
                if elem.tag.lower().endswith("loc") and elem.text:
                    urls.append(elem.text.strip())
        return urls, nested
    except ET.ParseError:
        # Regex fallback for malformed XML.
        text = content.decode("utf-8", errors="replace")
        all_locs = [m.group(1).strip() for m in _LOC_RX.finditer(text)]
        # We can't distinguish nested from leaf without structure; treat any
        # .xml ending as a candidate nested sitemap.
        for loc in all_locs:
            if loc.lower().endswith(".xml") or "sitemap" in loc.lower():
                nested.append(loc)
            else:
                urls.append(loc)
        return urls, nested


def _maybe_decompress(resp: requests.Response, url: str) -> bytes:
    """Decompress .gz sitemap bodies if needed."""
    body = resp.content
    if url.endswith(".gz") or resp.headers.get("Content-Type", "").lower().startswith("application/x-gzip"):
        import gzip
        try:
            return gzip.decompress(body)
        except OSError:
            return body
    return body


def fetch_sitemap(
    site_url: str,
    session: requests.Session,
    max_nested: int = 5000,
) -> Tuple[List[str], Dict]:
    """Try to fetch sitemap.xml (then sitemap_index.xml) for the given site.

    Returns (urls, info) where info has keys:
      tried: list of URLs attempted
      successful: list of URLs that returned valid sitemap content
      errors: dict of url -> error
      blocked_by_robots: bool
      nested_count: int
    """
    parsed = urlparse(site_url)
    site_root = f"{parsed.scheme}://{parsed.netloc}"

    candidate_paths = ["/sitemap.xml", "/sitemap_index.xml"]
    info: Dict = {
        "tried": [],
        "successful": [],
        "errors": {},
        "blocked_by_robots": False,
        "nested_count": 0,
    }

    all_urls: List[str] = []
    seen_sitemap_urls: Set[str] = set()
    nested_queue: List[str] = []

    # Seed with both candidate top-level sitemap paths.
    for path in candidate_paths:
        candidate = urljoin(site_root, path)
        nested_queue.append(candidate)

    nested_processed = 0
    while nested_queue and nested_processed < max_nested:
        sm_url = nested_queue.pop(0)
        if sm_url in seen_sitemap_urls:
            continue
        seen_sitemap_urls.add(sm_url)
        nested_processed += 1

        # robots check
        allowed, reason = can_fetch_sitemap(site_root, sm_url)
        if not allowed:
            info["blocked_by_robots"] = True
            info["errors"][sm_url] = reason or "blocked"
            info["tried"].append(sm_url)
            continue

        info["tried"].append(sm_url)
        resp, err = fetch_with_retries(sm_url, session)
        if resp is None:
            info["errors"][sm_url] = err
            continue
        info["successful"].append(sm_url)

        body = _maybe_decompress(resp, sm_url)
        urls, nested = _parse_sitemap_xml(body, sm_url)
        all_urls.extend(urls)
        for n in nested:
            # Resolve relative URLs against the parent sitemap.
            absolute = urljoin(sm_url, n)
            if absolute not in seen_sitemap_urls:
                nested_queue.append(absolute)

        # Politeness pause between sitemap fetches when we have many to
        # fetch (e.g., ProPublica's 4000+ daily sitemap shards). Don't
        # pause for the top-level fetch.
        if nested_queue and nested_processed > 1:
            time.sleep(0.05)

    info["nested_count"] = nested_processed
    return all_urls, info


# --- Union of tools fallback ----------------------------------------------


def union_of_tools(site_name: str) -> Tuple[List[str], List[str]]:
    """Union the URLs across all v1.4 tools' pages.jsonl for `site_name`.

    Returns (urls, tools_with_data).
    """
    urls: List[str] = []
    tools_with_data: List[str] = []
    for tool in V14_TOOLS:
        path = V14_RUN / tool / site_name / "pages.jsonl"
        if not path.exists():
            continue
        count_before = len(urls)
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                u = obj.get("url")
                if isinstance(u, str) and u:
                    urls.append(u)
        if len(urls) > count_before:
            tools_with_data.append(tool)
    return urls, tools_with_data


# --- URL processing -------------------------------------------------------


def dedup_normalize(urls: Iterable[str]) -> List[str]:
    """Dedup by _normalize_url_for_matching but STORE the first-seen
    ORIGINAL URL, not the normalized form.

    Normalization lowercases paths, which breaks live fetching on
    case-sensitive servers (found 2026-08-17: docs.pytorch.org serves
    /generated/torch.nn.Conv2d.html but 404s the lowercased form —
    1,339/4,047 pytorch corpus URLs silently skipped; doc.rust-lang.org
    std/core struct pages likewise). The normalized form is for KEYS
    (dedup, cache lookup), never for the stored fetchable URL.

    Returns an alphabetically sorted list (stable for git diffs)."""
    seen: Set[str] = set()
    out: List[str] = []
    for u in urls:
        if not isinstance(u, str):
            continue
        n = _normalize_url_for_matching(u)
        if not n or n in seen:
            continue
        seen.add(n)
        out.append(u.strip())
    out.sort()
    return out


def sample_if_oversized(
    urls: List[str],
    cap: int,
    seed: int,
) -> Tuple[List[str], bool, int]:
    """If len(urls) > cap, random-sample with fixed seed.

    Returns (final_urls, sampled, pre_sample_total).
    Sampled output remains alphabetical for git stability."""
    pre = len(urls)
    if pre <= cap:
        return urls, False, pre
    rng = random.Random(seed)
    sampled = rng.sample(urls, cap)
    sampled.sort()
    return sampled, True, pre


# --- Manifest extension ---------------------------------------------------


def load_manifest() -> Dict:
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def write_manifest(manifest: Dict) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = MANIFEST_PATH.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    tmp.replace(MANIFEST_PATH)


def _git_commit() -> Optional[str]:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, stderr=subprocess.DEVNULL
        )
        return out.decode().strip()
    except Exception:  # noqa: BLE001
        return None


def init_manifest_top_level(manifest: Dict) -> Dict:
    """Populate (or refresh) the top-level fields appropriate to DS-1.

    DS-2 (judge_prompt_version + haiku_model_version) and DS-5
    (intersection_pool_total) extend this later."""
    manifest.setdefault("universe_built_at", _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    manifest.setdefault("judge_prompt_version", None)
    manifest.setdefault("haiku_model_version", None)
    manifest.setdefault("intersection_pool_total", None)
    commit = _git_commit()
    if commit:
        manifest["git_commit"] = commit
    manifest.setdefault("sites", {})
    return manifest


# --- Per-site write -------------------------------------------------------


def write_site_artifacts(
    site_name: str,
    urls: List[str],
    source_record: Dict,
) -> Tuple[Path, Path, str]:
    """Write urls.txt + source.json. Returns (urls_path, source_path, sha256).
    """
    site_dir = OUTPUT_DIR / site_name
    site_dir.mkdir(parents=True, exist_ok=True)

    urls_path = site_dir / "urls.txt"
    urls_blob = "\n".join(urls) + ("\n" if urls else "")
    tmp_u = urls_path.with_suffix(".txt.tmp")
    tmp_u.write_text(urls_blob, encoding="utf-8")
    tmp_u.replace(urls_path)

    sha = hashlib.sha256(urls_blob.encode("utf-8")).hexdigest()
    source_record["url_list_sha256"] = sha
    source_record["url_count"] = len(urls)

    source_path = site_dir / "source.json"
    tmp_s = source_path.with_suffix(".json.tmp")
    with open(tmp_s, "w", encoding="utf-8") as f:
        json.dump(source_record, f, indent=2, sort_keys=True)
        f.write("\n")
    tmp_s.replace(source_path)

    return urls_path, source_path, sha


# --- Per-site driver ------------------------------------------------------


def build_for_site(
    site: Dict,
    session: requests.Session,
    dry_run: bool = False,
) -> Dict:
    """Build the reference corpus for one site. Returns a summary dict for
    chat.md reporting + manifest updates."""
    name = site["name"]
    url = site["url"]
    log(f"--- {name} ({url})")

    today = _dt.date.today().isoformat()

    # Attempt sitemap.
    sitemap_urls, sitemap_info = fetch_sitemap(url, session)
    log(
        f"  sitemap: tried={len(sitemap_info['tried'])} successful="
        f"{len(sitemap_info['successful'])} raw_urls={len(sitemap_urls)} "
        f"errors={len(sitemap_info['errors'])} blocked={sitemap_info['blocked_by_robots']}"
    )

    use_sitemap = False
    sitemap_normalized: List[str] = []
    if sitemap_urls:
        sitemap_normalized = dedup_normalize(sitemap_urls)
        log(f"  sitemap: normalized+deduped = {len(sitemap_normalized)}")
        if len(sitemap_normalized) >= MIN_URLS_FOR_SITEMAP_ACCEPT:
            use_sitemap = True
        else:
            log(
                f"  sitemap below MIN_URLS_FOR_SITEMAP_ACCEPT ({MIN_URLS_FOR_SITEMAP_ACCEPT});"
                " falling back to union-of-tools"
            )

    summary: Dict = {
        "site": name,
        "outcome": None,
        "url_count_final": 0,
        "sitemap_raw_count": len(sitemap_urls),
        "sitemap_normalized_count": len(sitemap_normalized),
        "sitemap_blocked_by_robots": sitemap_info["blocked_by_robots"],
        "sitemap_errors": sitemap_info["errors"],
        "sampled": False,
        "pre_sample_total": None,
        "union_tools_with_data": [],
    }

    if use_sitemap:
        final_urls, sampled, pre = sample_if_oversized(
            sitemap_normalized, SITEMAP_CAP, SITEMAP_SAMPLE_SEED
        )
        source_record: Dict = {
            "path": "sitemap",
            "sitemap_fetch_date": today,
            "url_count": len(final_urls),
        }
        if sampled:
            source_record["sitemap_url_sample_seed"] = SITEMAP_SAMPLE_SEED
            source_record["sitemap_url_total_pre_sample"] = pre
        if sitemap_info["blocked_by_robots"]:
            # Some nested sitemaps were blocked but the corpus still landed.
            source_record["sitemap_fetch_status"] = "partial_robots_block"
        summary["outcome"] = "sitemap" + ("_sampled" if sampled else "")
        summary["url_count_final"] = len(final_urls)
        summary["sampled"] = sampled
        summary["pre_sample_total"] = pre if sampled else None

        if not dry_run:
            write_site_artifacts(name, final_urls, source_record)
        return {"summary": summary, "source_record": source_record, "final_urls_count": len(final_urls)}

    # Union of tools fallback.
    raw_union, tools_with_data = union_of_tools(name)
    log(f"  union-of-tools: raw_urls={len(raw_union)} tools_with_data={tools_with_data}")
    union_normalized = dedup_normalize(raw_union)
    log(f"  union-of-tools: normalized+deduped = {len(union_normalized)}")
    final_urls, sampled, pre = sample_if_oversized(
        union_normalized, UNION_CAP, SITEMAP_SAMPLE_SEED
    )

    source_record = {
        "path": "union_of_tools",
        "union_of_tools_run_id": V14_RUN.name,
        "url_count": len(final_urls),
        "union_of_tools_tools_with_data": tools_with_data,
    }
    if sitemap_info["blocked_by_robots"] and not sitemap_normalized:
        source_record["sitemap_fetch_status"] = "blocked_by_robots"
    elif sitemap_info["errors"] and not sitemap_normalized:
        # Record the sitemap fetch attempt outcome for auditability.
        source_record["sitemap_fetch_status"] = "errored_or_missing"
    if sitemap_normalized and len(sitemap_normalized) < MIN_URLS_FOR_SITEMAP_ACCEPT:
        source_record["sitemap_fetch_status"] = f"too_short_{len(sitemap_normalized)}_urls"
    if sampled:
        source_record["sitemap_url_sample_seed"] = SITEMAP_SAMPLE_SEED  # field reused per schema
        source_record["union_url_total_pre_sample"] = pre

    summary["outcome"] = (
        "union_after_sitemap_blocked" if sitemap_info["blocked_by_robots"]
        else ("union_after_sitemap_too_short" if sitemap_normalized
              else "union_no_sitemap")
    )
    summary["url_count_final"] = len(final_urls)
    summary["sampled"] = sampled
    summary["pre_sample_total"] = pre if sampled else None
    summary["union_tools_with_data"] = tools_with_data

    if not dry_run:
        write_site_artifacts(name, final_urls, source_record)
    return {"summary": summary, "source_record": source_record, "final_urls_count": len(final_urls)}


# --- Top-level driver -----------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--sites",
        default=None,
        help="Comma-separated subset of site names to build (default: all 11).",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch + parse + log, but do NOT write artifacts or manifest.",
    )
    ap.add_argument(
        "--sitemap-cap",
        type=int,
        default=None,
        help=(
            "Override SITEMAP_CAP for this run (default 10000). Used for the "
            "v1.5 cost-control re-cap to 5000 on the 4 biggest sampled sites "
            "(huggingface-transformers/mdn-css/postgres-docs/propublica) per "
            "chat.md option B+C. Same seed=42 sampling logic applies; the new "
            "5k sample is NOT a subset of the prior 10k — `rng.sample(raw, 5k)` "
            "with the same seed picks a different subset than `rng.sample(raw, 10k)`."
        ),
    )
    args = ap.parse_args()

    global SITEMAP_CAP
    if args.sitemap_cap is not None:
        log(f"Override: SITEMAP_CAP {SITEMAP_CAP} -> {args.sitemap_cap}")
        SITEMAP_CAP = args.sitemap_cap

    all_sites = load_pool_sites()
    if args.sites:
        wanted = {s.strip() for s in args.sites.split(",") if s.strip()}
        all_sites = [s for s in all_sites if s["name"] in wanted]
        if not all_sites:
            log(f"No sites matched filter {wanted}")
            return 1

    log(f"Building corpora for {len(all_sites)} sites: {[s['name'] for s in all_sites]}")

    session = _session()

    manifest = load_manifest()
    manifest = init_manifest_top_level(manifest)

    results: List[Dict] = []
    short_sites: List[str] = []
    for site in all_sites:
        try:
            res = build_for_site(site, session, dry_run=args.dry_run)
        except Exception as e:  # noqa: BLE001
            log(f"  FAILED for {site['name']}: {e!r}")
            results.append({
                "summary": {
                    "site": site["name"],
                    "outcome": "exception",
                    "exception": repr(e),
                    "url_count_final": 0,
                }
            })
            continue
        results.append(res)
        summary = res["summary"]
        if summary["url_count_final"] < MIN_URLS_FOR_SITEMAP_ACCEPT:
            short_sites.append(site["name"])

        # Manifest update.
        if not args.dry_run:
            src = res["source_record"]
            entry: Dict = {
                "source": src["path"],
                "url_count": src["url_count"],
                "url_list_sha256": src["url_list_sha256"],
            }
            if src["path"] == "sitemap":
                entry["sitemap_fetch_date"] = src["sitemap_fetch_date"]
                entry["sitemap_url_sample_seed"] = src.get("sitemap_url_sample_seed")
                if "sitemap_url_total_pre_sample" in src:
                    entry["sitemap_url_total_pre_sample"] = src["sitemap_url_total_pre_sample"]
                if "sitemap_fetch_status" in src:
                    entry["sitemap_fetch_status"] = src["sitemap_fetch_status"]
            else:
                entry["union_of_tools_run_id"] = src["union_of_tools_run_id"]
                entry["union_of_tools_tools_with_data"] = src.get("union_of_tools_tools_with_data", [])
                if "sitemap_fetch_status" in src:
                    entry["sitemap_fetch_status"] = src["sitemap_fetch_status"]
                if "union_url_total_pre_sample" in src:
                    entry["union_url_total_pre_sample"] = src["union_url_total_pre_sample"]
                if src.get("sitemap_url_sample_seed") is not None and "union_url_total_pre_sample" in src:
                    entry["sitemap_url_sample_seed"] = src["sitemap_url_sample_seed"]
            # DS-2 / DS-5 fields are left absent here — they get added by
            # judge_helpful_pages.py + intersection_set.py later.
            manifest["sites"][site["name"]] = entry

    if not args.dry_run:
        write_manifest(manifest)
        log(f"Wrote manifest to {MANIFEST_PATH}")

    # Summary print
    print("\n=== Summary ===")
    for r in results:
        s = r["summary"]
        sampled_note = f" (sampled from {s['pre_sample_total']})" if s.get("sampled") else ""
        print(f"  {s['site']:32s}  outcome={s['outcome']:36s}  urls={s['url_count_final']}{sampled_note}")

    if short_sites:
        print(f"\nSC-1 NOT MET for: {short_sites}")
        print("Escalate to chat.md for human review.")
        return 2
    print("\nSC-1 met: all sites have >=50 URLs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
