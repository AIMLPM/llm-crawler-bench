#!/usr/bin/env python3
"""Web UI for hand-judging the v1.5 calibration ground truth.

Single-click-per-page UX. Server pre-extracts content for all 373 URLs at
startup (using v1.4 crawler caches or live trafilatura fallback), then
serves a judging page with content inline alongside HELPFUL / NON-HELPFUL
buttons. CSV writes atomically after every click.

Run:
    .venv/bin/python tools/hand_judge_web.py

Then open: http://localhost:8765
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import threading
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from flask import Flask, jsonify, redirect, render_template_string, request

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "bench" / "calibration_ground_truth_v15.csv"
V14_RUN = ROOT / "runs" / "run_v13_merged_20260504_203748"
DRAFTS_PATH = ROOT / "bench" / "calibration_drafts_fable.json"
# Number of high-confidence drafted rows whose draft is HIDDEN in the UI, so
# the human vote on them is independent — used to estimate draft error rate.
BLIND_N = 30

VALID = {"HELPFUL", "NON-HELPFUL"}
CONTENT_LIMIT = 4000  # chars shown in UI
PORT = 8765
# Sites excluded from hand-judging in this calibration build.
# huggingface-transformers excluded because HF rate-limits free-tier fetches,
# preventing live content extraction; v1.4 cache has only 2 of 73 calibration
# URLs for HF, so judgable content is unavailable. Calibration proceeds on
# the 3 remaining sites (rust-book + newegg + propublica = 300 URLs).
EXCLUDED_SITES = {"huggingface-transformers"}

# ---------- URL normalization (same as benchmark_retrieval._normalize_url_for_matching) ----------
_LOCALE_PREFIXES = {"en", "fr", "es", "de", "ja", "zh", "ko", "pt", "it", "ru", "ar", "hi"}
_STRIP_KEYS = {"utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term",
               "lang", "ref", "fbclid", "gclid", "_ga", "msclkid"}
_STRIP_KEY_PREFIXES = ("utm_",)


def _normalize_url(url: str) -> str:
    if not isinstance(url, str):
        return ""
    try:
        scheme, netloc, path, query, _ = urlsplit(url.strip())
    except (ValueError, TypeError):
        return url.lower()
    netloc = netloc.lower()
    if "." in netloc:
        first, _, rest = netloc.partition(".")
        if first in _LOCALE_PREFIXES and rest:
            netloc = rest
    if query:
        kept = []
        for pair in query.split("&"):
            key = pair.partition("=")[0].lower()
            if key in _STRIP_KEYS:
                continue
            if any(key.startswith(p) for p in _STRIP_KEY_PREFIXES):
                continue
            kept.append(pair)
        query = "&".join(kept)
    return urlunsplit((scheme.lower(), netloc, path.lower(), query, ""))


# ---------- Content extraction ----------

TOOLS_PREFERRED = ["markcrawl", "crawl4ai", "crawl4ai-raw", "crawlee", "playwright", "colly+md", "scrapy+md"]


def _load_v14_index() -> dict[tuple[str, str], dict]:
    """Build {(site, normalized_url) -> first-tool-page-record} lookup."""
    idx: dict[tuple[str, str], dict] = {}
    if not V14_RUN.exists():
        return idx
    for tool in TOOLS_PREFERRED:
        tool_dir = V14_RUN / tool
        if not tool_dir.exists():
            continue
        for site_dir in tool_dir.iterdir():
            if not site_dir.is_dir():
                continue
            site = site_dir.name
            pjsonl = site_dir / "pages.jsonl"
            if not pjsonl.exists():
                continue
            with pjsonl.open() as f:
                for line in f:
                    try:
                        rec = json.loads(line)
                    except Exception:
                        continue
                    url = rec.get("url", "")
                    if not url:
                        continue
                    nu = _normalize_url(url)
                    key = (site, nu)
                    # First-wins by tool preference; we iterate in TOOLS_PREFERRED order
                    if key not in idx:
                        rec["_source_tool"] = tool
                        idx[key] = rec
    return idx


_V14_INDEX: dict[tuple[str, str], dict] | None = None


def _v14_lookup(site: str, url: str) -> tuple[str | None, str | None]:
    """Return (extracted_text, source_label) from v1.4 cache, or (None, None)."""
    global _V14_INDEX
    if _V14_INDEX is None:
        _V14_INDEX = _load_v14_index()
    rec = _V14_INDEX.get((site, _normalize_url(url)))
    if not rec:
        return None, None
    text = rec.get("text") or rec.get("content") or rec.get("markdown") or ""
    if not text:
        return None, None
    return text, f"v1.4 cache ({rec.get('_source_tool', '?')})"


_RATELIMITED_HOSTS: set[str] = set()
_RATELIMIT_LOCK = threading.Lock()


def _live_trafilatura(url: str) -> tuple[str | None, str | None]:
    try:
        import urllib.request

        import trafilatura

        # Skip if this host already rate-limited us in this run
        host = urlsplit(url).netloc.lower()
        with _RATELIMIT_LOCK:
            if host in _RATELIMITED_HOSTS:
                return None, f"skipped (host {host} rate-limited earlier)"

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            },
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        text = trafilatura.extract(html, include_comments=False, include_tables=False)
        if text:
            return text, "live trafilatura"
    except urllib.error.HTTPError as exc:
        if exc.code == 429:
            with _RATELIMIT_LOCK:
                _RATELIMITED_HOSTS.add(host)
            return None, "429 rate-limited (host blacklisted for this run)"
        return None, f"HTTP {exc.code}"
    except Exception as exc:
        return None, f"live error: {exc.__class__.__name__}"
    return None, None


_CHROME_PATTERNS = (
    "opens in a new window", "opens an external website", "close this dialog",
    "this website utilizes technologies such as cookies",
    "close cookie preferences", "cookie policy", "privacy policy",
    "terms of service", "gdpr", "ccpa",
    "skip to content", "skip to main", "menu menu", "menu search",
    "log in", "sign in", "sign up", "log out",
    "click here", "view all", "show all", "see all",
    "add to cart", "buy now", "add to wishlist", "compare items",
    "select store", "your location", "ship to",
    "all rights reserved", "© ", "©20", "powered by",
    "follow us on", "social media",
    "fetching metadata", "this space is sleeping", "restart this space",
)

_MD_LINK_RE = re.compile(r"\[[^\]]*\]\([^)]*\)")


def _is_chrome_line(line: str) -> bool:
    s = line.strip()
    low = s.lower()
    if not low:
        return True
    if len(low) < 4:
        return True
    # Lines where >50% of chars are inside markdown link syntax (nav menus)
    link_chars = sum(len(m.group(0)) for m in _MD_LINK_RE.finditer(line))
    if line and (link_chars / len(line)) > 0.5:
        return True
    for phrase in _CHROME_PATTERNS:
        if phrase in low:
            return True
    # Lines that are just a short list-item link
    if low.startswith(("* ", "- ")) and len(low) < 60:
        return True
    # Lines that are just a markdown header to a single product/nav entry
    if low.startswith("#") and len(low) < 60 and link_chars > len(low) * 0.3:
        return True
    return False


def _heuristic_skip_chrome(text: str) -> str:
    """Drop chrome lines from cached text; return cleaned content."""
    if not text:
        return text
    lines = text.split("\n")
    kept = [line for line in lines if not _is_chrome_line(line)]
    cleaned = "\n".join(kept).strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    if not cleaned or len(cleaned) < 50:
        # Heuristic gutted the content; fall back to raw skip
        return text[1500:1500 + CONTENT_LIMIT * 2] or text[:CONTENT_LIMIT * 2]
    return cleaned[:CONTENT_LIMIT * 2]


def extract_for_row(row: dict) -> dict:
    """Return {text, source} for the row's URL.

    Priority:
      1. markcrawl-cached (cleanest extraction, available mostly for rust-book)
      2. live trafilatura (works well for non-anti-bot sites; ~free in wall time
         because parallelized at startup)
      3. v1.4 cache from other tools (raw + chrome) with aggressive heuristic
    """
    site = row["site"]
    url = row["url"]

    # 1. Try markcrawl-cached first if available
    nu = _normalize_url(url)
    key = (site, nu)
    rec = (_V14_INDEX or {}).get(key)
    if rec and rec.get("_source_tool") == "markcrawl":
        text = rec.get("text") or rec.get("content") or rec.get("markdown") or ""
        if text:
            return {"text": text[:CONTENT_LIMIT * 2], "source": "v1.4 cache (markcrawl)"}

    # 2. Try live trafilatura
    text, source = _live_trafilatura(url)
    if text and not (source and "error" in source):
        return {"text": text[:CONTENT_LIMIT * 2], "source": source}

    # 3. Fall back to v1.4 cache (any other tool) with heuristic chrome strip
    text2, source2 = _v14_lookup(site, url)
    if text2:
        return {"text": _heuristic_skip_chrome(text2), "source": source2 + " + chrome-strip"}

    # 4. Both failed — empty text so the UI shows the "couldn't fetch" message
    return {"text": "", "source": source or "no content available"}


# ---------- CSV I/O ----------

_csv_lock = threading.Lock()


def load_rows() -> list[dict]:
    """Load all CSV rows (including excluded sites — they stay in memory so
    save_rows preserves them in the CSV)."""
    with CSV_PATH.open() as f:
        return list(csv.DictReader(f))


def is_active(row: dict) -> bool:
    """True if this row is presented to the UI (not in an excluded site)."""
    return row.get("site") not in EXCLUDED_SITES


def save_rows(rows: list[dict]) -> None:
    with _csv_lock:
        fieldnames = list(rows[0].keys())
        tmp = CSV_PATH.with_suffix(".csv.tmp")
        with tmp.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)
        tmp.replace(CSV_PATH)


# ---------- App state ----------

ROWS = load_rows()


def _load_drafts() -> dict[str, dict]:
    """{url -> draft verdict} from the Fable draft-labeling pass, if present."""
    if not DRAFTS_PATH.exists():
        return {}
    try:
        return json.loads(DRAFTS_PATH.read_text()).get("drafts", {})
    except Exception:
        return {}


DRAFTS = _load_drafts()


def _blind_sample() -> set[str]:
    """Deterministic sample of high-confidence drafted rows (md5-ordered, so it
    is stable across restarts). Drafts stay hidden on these rows."""
    urls = [r["url"] for r in ROWS
            if is_active(r) and DRAFTS.get(r["url"], {}).get("confidence") == "high"]
    urls.sort(key=lambda u: hashlib.md5(u.encode()).hexdigest())
    return set(urls[:BLIND_N])


BLIND_URLS = _blind_sample()


# ---- Targeted review queue ----
# Human eyes are needed only on: (1) rows where an existing human label
# conflicts with the draft, (2) blind rows (independent draft-error
# estimate), (3) low/medium-confidence drafts. Remaining high-confidence
# rows are bulk-accepted from drafts after the blind agreement gate
# (tools/bulk_accept_drafts.py).

def _build_queue() -> list[int]:
    conflicts, blind, shaky = [], [], []
    for i, r in enumerate(ROWS):
        if not is_active(r):
            continue
        d = DRAFTS.get(r["url"])
        gt = r.get("ground_truth", "").strip()
        if d and gt in VALID and gt != d["label"]:
            conflicts.append(i)
        elif r["url"] in BLIND_URLS:
            blind.append(i)
        elif d and d.get("confidence") in ("low", "medium"):
            shaky.append(i)
    return conflicts + blind + shaky


QUEUE = _build_queue()
ACTIONED: set[int] = set()


def queue_pending(i: int) -> bool:
    r = ROWS[i]
    if r.get("ground_truth", "").strip() not in VALID:
        return True
    # Filled rows stay pending only while they conflict with the draft and
    # haven't been revisited this run (SKIP counts as "keep my label").
    d = DRAFTS.get(r["url"])
    return bool(d and r["ground_truth"].strip() != d["label"] and i not in ACTIONED)


def find_next_queued(after: int | None = None) -> int | None:
    """Next pending queue item, in queue order, wrapping around."""
    if not QUEUE:
        return None
    start = QUEUE.index(after) + 1 if after in QUEUE else 0
    for i in QUEUE[start:] + QUEUE[:start]:
        if queue_pending(i):
            return i
    return None


CONTENT_CACHE: dict[int, dict] = {}
EXTRACT_LOCK = threading.Lock()
EXTRACT_PROGRESS = {"done": 0, "total": len(ROWS)}


def _preextract_worker(idx: int):
    row = ROWS[idx]
    try:
        result = extract_for_row(row)
    except Exception as exc:
        result = {"text": f"<extract crashed: {exc}>", "source": "error"}
    with EXTRACT_LOCK:
        CONTENT_CACHE[idx] = result
        EXTRACT_PROGRESS["done"] += 1


def start_preextraction(max_workers: int = 1):
    """Pre-extract sequentially in a single background thread.

    Disabled parallelism: lxml/trafilatura inside ThreadPoolExecutor on
    Python 3.14 segfaults. Single-thread is slow but stable.

    Skips rows in EXCLUDED_SITES (e.g., HF, which rate-limits free fetches).
    """
    def _runner():
        for i, row in enumerate(ROWS):
            if not is_active(row):
                continue
            try:
                _preextract_worker(i)
            except Exception:
                # Never let pre-extraction crash the server
                pass

    t = threading.Thread(target=_runner, daemon=True)
    t.start()


def get_content(idx: int) -> dict:
    """Synchronously get content for idx, extracting now if not pre-fetched."""
    with EXTRACT_LOCK:
        cached = CONTENT_CACHE.get(idx)
    if cached:
        return cached
    # Not yet pre-extracted — do it now (blocking)
    result = extract_for_row(ROWS[idx])
    with EXTRACT_LOCK:
        CONTENT_CACHE[idx] = result
        EXTRACT_PROGRESS["done"] = max(EXTRACT_PROGRESS["done"], len(CONTENT_CACHE))
    return result


def find_next_unjudged(start: int = 0) -> int | None:
    """Next row index that is (a) in an active site and (b) not yet judged."""
    i = start
    while i < len(ROWS):
        row = ROWS[i]
        if is_active(row) and row.get("ground_truth", "").strip() not in VALID:
            return i
        i += 1
    return None


def find_prev_active(start: int) -> int:
    """Previous row index that is in an active site (for the Back button)."""
    i = start - 1
    while i >= 0:
        if is_active(ROWS[i]):
            return i
        i -= 1
    return max(0, start)


# ---------- Flask app ----------

app = Flask(__name__)


PAGE_HTML = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Hand-judge {{ active_idx+1 }}/{{ total }}</title>
<style>
  * { box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 0; background: #f4f5f7; color: #222; }
  .topbar { background: #fff; padding: 0.8em 1.5em; border-bottom: 1px solid #ddd; position: sticky; top: 0; z-index: 100; }
  .progress { background: #eee; height: 6px; border-radius: 3px; margin-top: 0.5em; }
  .progress-fill { background: #4caf50; height: 100%; border-radius: 3px; transition: width 0.3s; }
  .stats { font-size: 0.85em; color: #666; margin-top: 0.3em; }
  .container { max-width: 1100px; margin: 1em auto; padding: 0 1.5em 9em; }
  .urlcard { background: #fff; border-radius: 8px; padding: 1em 1.2em; margin-bottom: 1em; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
  .urlcard .site { display: inline-block; background: #e3f2fd; color: #1565c0; font-size: 0.8em; font-weight: 600; padding: 0.15em 0.6em; border-radius: 4px; margin-bottom: 0.6em; }
  .urlcard .url { font-family: ui-monospace, SF Mono, Menlo, monospace; font-size: 0.9em; word-break: break-all; }
  .urlcard .url a { color: #1976d2; text-decoration: none; }
  .urlcard .url a:hover { text-decoration: underline; }
  .urlcard .title { font-size: 1.15em; font-weight: 600; margin-top: 0.4em; }
  .urlcard .source { font-size: 0.75em; color: #888; margin-top: 0.5em; }
  .content { background: #fff; border-radius: 8px; padding: 1.2em 1.5em; box-shadow: 0 1px 2px rgba(0,0,0,0.05); white-space: pre-wrap; line-height: 1.55; font-size: 0.96em; max-height: 60vh; overflow-y: auto; }
  .content .empty { color: #999; font-style: italic; }
  .actionbar { position: fixed; bottom: 0; left: 0; right: 0; background: rgba(255,255,255,0.96); backdrop-filter: blur(4px); border-top: 1px solid #ddd; padding: 1em 1.5em; display: flex; gap: 0.8em; justify-content: center; }
  .actionbar form { display: contents; }
  .btn { padding: 0.9em 1.6em; font-size: 1.08em; font-weight: 600; border: none; border-radius: 6px; cursor: pointer; color: #fff; min-width: 180px; }
  .btn.helpful { background: #4caf50; }
  .btn.helpful:hover { background: #43a047; }
  .btn.nonhelpful { background: #e53935; }
  .btn.nonhelpful:hover { background: #d32f2f; }
  .btn.skip { background: #757575; min-width: 110px; }
  .btn.back { background: #424242; min-width: 90px; }
  .kbd { background: rgba(255,255,255,0.3); padding: 0.05em 0.35em; border-radius: 3px; font-family: ui-monospace, monospace; font-size: 0.85em; margin-left: 0.5em; }
  .open-link { display: inline-block; margin-left: 0.8em; padding: 0.3em 0.7em; background: #2196f3; color: #fff; border-radius: 4px; font-size: 0.85em; text-decoration: none; }
  .current { background: #fff3e0; padding: 0.4em 0.7em; border-radius: 4px; font-size: 0.85em; color: #ef6c00; margin-top: 0.6em; }
  .draft { border-radius: 8px; padding: 0.8em 1.2em; margin-bottom: 1em; font-size: 0.95em; }
  .draft.helpful { background: #e8f5e9; border-left: 4px solid #4caf50; }
  .draft.nonhelpful { background: #ffebee; border-left: 4px solid #e53935; }
  .draft.blind { background: #eceff1; border-left: 4px solid #90a4ae; color: #555; }
  .draft .verdict { font-weight: 700; }
  .draft .rationale { margin-top: 0.3em; color: #444; }
  .draft .disagree { margin-top: 0.4em; color: #b71c1c; font-weight: 600; }
</style>
</head><body>

<div class="topbar">
  <div style="display: flex; justify-content: space-between; align-items: baseline;">
    <strong>Hand-judge calibration ground truth</strong>
    <span style="font-size: 0.85em; color: #555;">
      Row {{ active_idx + 1 }} of {{ total }} (HF excluded) &middot;
      <span style="color: #4caf50; font-weight: 600;">{{ h_count }} HELPFUL</span> &middot;
      <span style="color: #e53935; font-weight: 600;">{{ nh_count }} NON-HELPFUL</span> &middot;
      {{ remaining }} to go
    </span>
  </div>
  <div class="progress"><div class="progress-fill" style="width: {{ pct }}%"></div></div>
  <div class="stats">Extraction cache: {{ extract_done }}/{{ extract_total }} ready{% if drafts_loaded %} &middot; {{ drafts_loaded }} Fable drafts loaded &middot; <a href="/disagreements">disagreements</a>{% endif %}</div>
</div>

<div class="container">
  <div class="urlcard">
    <span class="site">{{ row.site }}</span>
    <div class="url">
      <a href="{{ row.url }}" target="judging_pane">{{ row.url }}</a>
      <a class="open-link" href="{{ row.url }}" target="judging_pane">Open in new tab</a>
    </div>
    <div class="title">{{ row.title }}</div>
    <div class="source">extracted from: {{ content.source or '?' }}</div>
    {% if row.ground_truth %}
      <div class="current">Already judged: {{ row.ground_truth }} (this click will overwrite)</div>
    {% endif %}
  </div>

  {% if blind %}
    <div class="draft blind">&#127922; Blind row — the Fable draft is hidden here so your vote independently estimates draft accuracy. Judge from the content below.</div>
  {% elif draft %}
    <div class="draft {{ 'helpful' if draft.label == 'HELPFUL' else 'nonhelpful' }}">
      <span class="verdict">Fable draft: {{ draft.label }}</span> &mdash; {{ draft.category }} ({{ draft.confidence }} confidence)
      <div class="rationale">{{ draft.rationale }}</div>
      {% if row.ground_truth and row.ground_truth != draft.label %}
        <div class="disagree">&#9888; Your existing label ({{ row.ground_truth }}) disagrees with this draft — please re-check.</div>
      {% endif %}
    </div>
  {% endif %}

  <div class="content">{% if content.text %}{{ content.text }}{% else %}<span class="empty">Couldn't fetch content for this URL{% if content.source %} ({{ content.source }}){% endif %} — click <strong>Open in new tab</strong> above to view the page, then come back and judge.</span>{% endif %}</div>
</div>

<div class="actionbar">
  <form method="POST" action="/row/{{ n }}" style="display: contents;">
    <input type="hidden" name="verdict" id="verdict" value="">
    <button type="button" class="btn back" onclick="window.location.href='/row/{{ prev_n }}'">← Back<span class="kbd">b</span></button>
    <button type="button" class="btn nonhelpful" onclick="submit('NON-HELPFUL')">↓ NON-HELPFUL<span class="kbd">n</span></button>
    <button type="button" class="btn helpful" onclick="submit('HELPFUL')">↑ HELPFUL<span class="kbd">h</span></button>
    <button type="button" class="btn skip" onclick="submit('SKIP')">Skip →<span class="kbd">s</span></button>
  </form>
</div>

<script>
function submit(verdict) {
  document.getElementById('verdict').value = verdict;
  document.querySelector('form').submit();
}
document.addEventListener('keydown', function(e) {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  // Arrow keys (primary)
  if (e.key === 'ArrowUp')         { e.preventDefault(); submit('HELPFUL'); return; }
  if (e.key === 'ArrowDown')       { e.preventDefault(); submit('NON-HELPFUL'); return; }
  if (e.key === 'ArrowLeft')       { e.preventDefault(); window.location.href = '/row/{{ prev_n }}'; return; }
  if (e.key === 'ArrowRight')      { e.preventDefault(); submit('SKIP'); return; }
  // Letter keys (backup)
  const k = e.key.toLowerCase();
  if (k === 'h') submit('HELPFUL');
  else if (k === 'n') submit('NON-HELPFUL');
  else if (k === 's') submit('SKIP');
  else if (k === 'b') window.location.href = '/row/{{ prev_n }}';
  else if (k === 'o') window.open('{{ row.url|safe }}', 'judging_pane');
});
</script>
</body></html>
"""

DONE_HTML = """<!DOCTYPE html><html><head><title>Done</title>
<style>body{font-family:-apple-system,sans-serif;max-width:600px;margin:4em auto;padding:0 1em;}</style>
</head><body>
<h1>All 373 rows judged!</h1>
<p>Helpful: <strong>{{ h }}</strong> &middot; Non-helpful: <strong>{{ nh }}</strong> &middot; Skipped/blank: <strong>{{ skipped }}</strong></p>
<p>Ground truth is saved at <code>bench/calibration_ground_truth_v15.csv</code>. You can shut down the server now (Ctrl-C in the terminal).</p>
<p><a href="/row/0">Review from the start</a></p>
</body></html>
"""


@app.route("/")
def index():
    n = find_next_queued()
    if n is None:
        return redirect("/queue-done")
    return redirect(f"/row/{n}")


@app.route("/row/<int:n>", methods=["GET", "POST"])
def row(n):
    if n < 0 or n >= len(ROWS):
        return redirect("/done")
    # If user navigates to an excluded-site row, jump to next active one
    if not is_active(ROWS[n]):
        nxt = find_next_unjudged(n)
        return redirect(f"/row/{nxt}" if nxt is not None else "/done")
    if request.method == "POST":
        v = request.form.get("verdict", "").strip()
        if v in VALID:
            ROWS[n]["ground_truth"] = v
            save_rows(ROWS)
        elif v == "SKIP":
            pass  # leave ground_truth as-is
        ACTIONED.add(n)
        nxt = find_next_queued(n)
        return redirect(f"/row/{nxt}" if nxt is not None else "/queue-done")

    row = ROWS[n]
    content = get_content(n)
    blind = row["url"] in BLIND_URLS
    draft = None if blind else DRAFTS.get(row["url"])
    # Stats: count over ACTIVE rows only (so progress reflects what the user is judging)
    active = [r for r in ROWS if is_active(r)]
    total_active = len(active)
    judged = sum(1 for r in active if r.get("ground_truth", "").strip() in VALID)
    h_count = sum(1 for r in active if r.get("ground_truth", "").strip() == "HELPFUL")
    nh_count = sum(1 for r in active if r.get("ground_truth", "").strip() == "NON-HELPFUL")
    # Active position (which active-row are we on?)
    active_idx = sum(1 for r in ROWS[:n] if is_active(r))
    prev_n = find_prev_active(n)
    return render_template_string(
        PAGE_HTML,
        n=n,
        active_idx=active_idx,
        total=total_active,
        row=row,
        content=content,
        judged=judged,
        h_count=h_count,
        nh_count=nh_count,
        remaining=total_active - judged,
        pct=int(judged * 100 / total_active) if total_active else 0,
        prev_n=prev_n,
        extract_done=EXTRACT_PROGRESS["done"],
        extract_total=EXTRACT_PROGRESS["total"],
        draft=draft,
        blind=blind,
        drafts_loaded=len(DRAFTS),
    )


@app.route("/queue-done")
def queue_done():
    """Review queue exhausted — show blind-audit stats and next step."""
    blind = [r for r in ROWS if is_active(r) and r["url"] in BLIND_URLS]
    judged = [r for r in blind if r.get("ground_truth", "").strip() in VALID]
    agree = sum(1 for r in judged
                if r["ground_truth"].strip() == DRAFTS.get(r["url"], {}).get("label"))
    active = [r for r in ROWS if is_active(r)]
    filled = sum(1 for r in active if r.get("ground_truth", "").strip() in VALID)
    pct = f"{agree / len(judged):.0%}" if judged else "n/a"
    return (
        "<html><head><title>Queue done</title><style>"
        "body{font-family:-apple-system,sans-serif;max-width:640px;margin:4em auto;padding:0 1em;}"
        "</style></head><body><h1>Review queue complete</h1>"
        f"<p>Blind audit: <b>{agree}/{len(judged)}</b> of your independent votes "
        f"agree with the hidden Fable drafts (<b>{pct}</b>).</p>"
        f"<p>Labeled so far: <b>{filled}/{len(active)}</b>. The rest can be bulk-filled "
        "from drafts: tell Claude the queue is done, or run "
        "<code>tools/bulk_accept_drafts.py</code>.</p>"
        '<p><a href="/row/0">Browse all rows</a> &middot; '
        '<a href="/disagreements">disagreements</a></p></body></html>'
    )


@app.route("/disagreements")
def disagreements():
    """Rows where an existing human label conflicts with the Fable draft."""
    items = []
    for i, r in enumerate(ROWS):
        if not is_active(r):
            continue
        d = DRAFTS.get(r["url"])
        gt = r.get("ground_truth", "").strip()
        if d and gt in VALID and gt != d["label"]:
            items.append((i, r, d))
    html = ["<html><head><title>Disagreements</title><style>"
            "body{font-family:-apple-system,sans-serif;max-width:900px;margin:2em auto;padding:0 1em;}"
            "li{margin:0.5em 0;}</style></head><body>"]
    html.append(f"<h1>{len(items)} rows where your label disagrees with the Fable draft</h1><ol>")
    for i, r, d in items:
        html.append(
            f'<li><a href="/row/{i}">{r["title"][:70]}</a> — '
            f'you: <b>{gt_label(r)}</b>, draft: <b>{d["label"]}</b> ({d["category"]})</li>'
        )
    html.append('</ol><p><a href="/">Back to judging</a></p></body></html>')
    return "".join(html)


def gt_label(r: dict) -> str:
    return r.get("ground_truth", "").strip()


@app.route("/done")
def done():
    h = sum(1 for r in ROWS if r.get("ground_truth", "").strip() == "HELPFUL")
    nh = sum(1 for r in ROWS if r.get("ground_truth", "").strip() == "NON-HELPFUL")
    skipped = len(ROWS) - h - nh
    return render_template_string(DONE_HTML, h=h, nh=nh, skipped=skipped)


@app.route("/api/status")
def status():
    return jsonify({
        "rows": len(ROWS),
        "judged": sum(1 for r in ROWS if r.get("ground_truth", "").strip() in VALID),
        "extract_done": EXTRACT_PROGRESS["done"],
        "extract_total": EXTRACT_PROGRESS["total"],
    })


def main() -> int:
    if not CSV_PATH.exists():
        print(f"error: {CSV_PATH} not found", file=sys.stderr)
        return 1
    global _V14_INDEX
    print(f"Loaded {len(ROWS)} rows from {CSV_PATH.name}", file=sys.stderr)
    print("Building v1.4 cache index (one-time scan of all crawler pages.jsonl)…", file=sys.stderr)
    _V14_INDEX = _load_v14_index()
    print(f"  Indexed {len(_V14_INDEX)} (site, url) pairs from v1.4 cache.", file=sys.stderr)
    print("Starting parallel content pre-extraction (background)…", file=sys.stderr)
    start_preextraction(max_workers=16)
    if DRAFTS:
        print(f"  Loaded {len(DRAFTS)} Fable draft labels ({len(BLIND_URLS)} blind rows).", file=sys.stderr)
    print(f"\n  Open in browser: http://localhost:{PORT}\n", file=sys.stderr)
    # Disable Flask's noisy default logger
    import logging
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    app.run(host="127.0.0.1", port=PORT, debug=False, use_reloader=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
