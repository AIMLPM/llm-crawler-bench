# Benchmark Methodology

<!-- style: v2, 2026-04-07 -->

## Author and conflict-of-interest disclosure

This benchmark suite is authored and maintained by the same team that develops one of the tools being compared (markcrawl). The v1.4 cycle removes humans from the query-acceptance loop to keep the benchmark resistant to motivated reasoning:

- **v1.3 query set** (current at this commit): hand-written by the maintainer (paulsave). This is the conflict-of-interest that v1.4 fixes.
- **v1.4 query set** (forthcoming, see spec [DS-6](../specs/v14-methodology-hardening.md)): drafted by gpt-4o-mini and verified by a separate gpt-4o-mini API invocation with no shared context window (no human reviewer in the acceptance loop). The structural separation is the API-call boundary — the verifier does not see the draft prompt or any prior turns. Rejected drafts are logged in `queries/v14_rejected.json` for transparency.
- **Runners and methodology**: written by the same maintainer. The fairness contract — every tool runs with equivalent settings, every tool chunked through the same pipeline — is enforced by code in `runners/` and `benchmark_*.py`, which are open for review.
- **markcrawl tool itself**: developed in a separate repository (https://github.com/AIMLPM/markcrawl). Versions used are pinned in `pyproject.toml` and announced in release notes.
- **Run execution**: deterministic given the pinned code + query set + crawl data — any third party running the same commit against the same `runs/` directory should reproduce the published numbers within network/API jitter. Reproducibility artifact (DS-13) makes this a single command. Closes the "but you ran it" attack: no party has to trust the maintainer's local execution.

Human inspection of LLM-generated queries before the full benchmark run (per the v1.4 spec's Implementation Roadmap, Gates 3a/3b) is permitted for setup-bug verification only — fixes happen at the prompt/code level, never at the individual-query level. See `specs/v14-methodology-hardening.md` "Inspection vs. curation" for the explicit allow/deny list.

## Anti-gaming

A retrieval benchmark authored by a tool's maintainer is structurally vulnerable to a handful of gaming attacks. The table below enumerates the attacks we considered and what the v1.4 cycle does about each. The "limitation noted" rows are honest disclosures — places where the defense is incomplete and a reviewer is right to be skeptical.

| Attack | What it looks like | Defense | Status |
|---|---|---|---|
| **Chunk-density inflation** | A crawler emits 5 chunks per page; another emits 1. The first ranks higher in MRR purely because it has more chunks competing for top-K slots — same content, more "shots on goal". | **Page MRR (DS-1 + DS-2)**: collapse all chunks per URL to a single rank, deduping by DS-2 normalized URL so locale mirrors and fragment variants of the same canonical page count once. Reported alongside chunk-level MRR in every report. **Empirical pattern (Gate 2)**: the v1.3 → Page-MRR transition produces TWO offsetting effects per tool — page-collapse uplift (chunks-per-canonical-page collapse to one slot, MRR up) AND v1.3 false-positive removal (chunks that were matching via stripped fragment-text or `?ref=` query-text no longer count, MRR down on those queries). Net per-tool delta is small (±0.005-0.012 in our v1.3 data) and the direction depends on which effect dominates for that tool. Both effects are correct behavior; a tool whose page-MRR drops is one whose v1.3 chunk-MRR was inflated by the false positives DS-2 now removes. | Implemented |
| **Locale duplication** | A crawler indexes locale mirrors (he.react.dev, de.react.dev, ...) and the duplicated content boosts MRR via repeated near-identical chunks. | **URL normalization (DS-2)** strips ISO-639-1 + BCP-47 locale subdomain prefixes before matching. Combined with page-level dedup (DS-1), the locale mirrors collapse into a single canonical page in the page-level metric. | Implemented |
| **URL-text injection** | A crawler appends or includes the `url_match` pattern in URL slugs to game substring matching. | Queries are derived from page **content**, not from URLs — `tools/generate_queries.py` (DS-6) prompts the LLM with the page body, never the URL. The `url_match` value is auto-derived from the URL's last path segment, identically across all tools. | Structural |
| **Hub-page inflation** | An index/sitemap page lists every product or article; substring matching finds the hub for almost any query. | The verifier (DS-6 second invocation) rejects queries that match content-poor pages with rationale "page is empty"; a non-zero count of these rejections indicates the sampler should be fixed (Gate 3a falsifiable check). | Implemented |
| **Embedder favoritism** | The author picks the embedding model that ranks their tool best. | **PUBLISH-BOTH (DS-13a)**: OpenAI text-embedding-3-small remains primary; mxbai-embed-large-v1 published as a never-mixed parallel secondary. Per-tool delta surfaced explicitly (markcrawl gains +0.043 MRR with mxbai; all 6 other tools lose -0.007 to -0.077). The asymmetric bias is the reason we kept OpenAI primary — we considered switching and chose not to, and we lead the disclosure with that delta rather than burying it. | Implemented |
| **Author conflict-of-interest in queries** | The benchmark maintainer (also the maintainer of one compared tool) writes queries that subtly favor their tool. | **DS-6 LLM generation + LLM verification** removes humans from the query-acceptance loop. The generator and verifier are both gpt-4o-mini but invoked as **separate API calls with no shared context window**. Human inspection (Gates 3a/3b) is permitted ONLY for setup-bug verification at the prompt/code level — never to drop or rewrite individual queries. | Implemented |
| **Verifier laxness** | The same model used for generation is also the verifier; it rationalizes its own drafts as "answerable". | The verifier sees only the URL + page content + query (no draft prompt, no prior turn context). Defaults to **rejection** on parse failure so malformed JSON cannot smuggle drafts through. The first-pass acceptance rate is logged per Gate 3a so anomalous laxness is visible. | Mitigated |
| **Single-trial cherry-picking** | One run produced unfavorable numbers for the author's tool; they re-ran and reported the better outcome. | **Run determinism + git-pinned commit + checkpoint cache** mean any third party can rerun the same commit and reproduce within network/API jitter. We do not iterate runs to chase a number — when methodology changes, we ship the diff and call it out (DS-14 release notes lead with markcrawl's deltas, including negative ones). | Mitigated |
| **Multi-trial variance hiding** | The published number happened to fall on a lucky run; a more honest framing would show the run-to-run variance. | **Single-trial caveat banner** on every report links to METHODOLOGY's `## Single-trial measurement` section. Multi-trial measurement deferred to v1.5 — explicitly limitation-noted, not papered over. | Limitation noted |
| **Cost-table assumption hiding** | Cost-of-scale claims bake in unstated assumptions (queries/day, embedding price, dedup ratio) that flatter one tool. | **DS-11 cost calculator** is a Python script with adjustable inputs and a sensitivity table showing how rankings shift when each input moves ±50%. Reviewers can re-run with their own pricing. | Pending DS-11 |
| **Substring-matcher fuzziness** | The `url_match` matcher is a case-insensitive substring check on the normalized URL — a short pattern like `state` matches 20+ react-dev URLs. Tools that happen to have the pattern text in many places get inflated hits. | This is **inherent to the substring approach** and v1.4 inherits it. Mitigated by (a) `url_match` patterns are derived from the page's content (DS-6), not chosen to favor any tool, and (b) the matcher operates on the DS-2-normalized URL so locale/fragment/UTM noise is gone before matching. Genuinely fixing this requires LLM-judged relevance — deferred to v1.5. | Limitation noted |

If a hostile reviewer finds a 11th attack we haven't named, the right response is to add a row, document the defense or limitation honestly, and update the spec — not to argue.

## Single-trial measurement

Each per-site number in the comparative reports comes from one benchmark run. Network jitter, WAF rate-limiting, and server load can shift per-site speed and coverage between runs by single-digit percent. Where confidence intervals are reported (currently a subset of retrieval Hit@K columns), they reflect query-set sampling only — derived from query count — and do NOT reflect run-to-run variance. Per-dimension CI coverage is widening: v1.4 Gate 4 (DS-9) adds Hit@1/3/5/10 with CIs to every retrieval table.

Multi-trial measurement (running each (tool, site) pair N times to compute both within-run and between-run variance) is deferred to v1.5. The current single-trial constraint is imposed by hardware budget on the development machine: a full v1.3 cycle takes ~24 hours wall-time across 7 tools × 11 sites, and N=3 trials would push that past a week.

For per-site numbers within ~5% of each other across tools, treat them as effectively tied. The 5% threshold is a **conservative rule of thumb based on observed jitter from prior re-runs, not a formally measured noise floor** — multi-trial work in v1.5 will replace it with a measured value. Aggregate metrics (overall MRR, content signal averaged across sites) are more stable than individual per-site numbers.

## Goal

Compare MarkCrawl against Crawl4AI, FireCrawl (self-hosted), Scrapy, Crawlee, Playwright, and Colly on the same sites with equivalent settings, measuring what matters for the "crawl a documentation site for RAG" use case.

Each tool starts from the same seed URL and discovers its own pages through link-following. This tests the full real-world workflow: URL discovery, content extraction, and Markdown conversion. Page counts may vary between tools depending on each tool's link-following strategy — this is itself a meaningful comparison dimension.

If one tool is faster than another, the reports say so. The comparison is factual, not promotional.

## Reporting approach

When one tool outperforms another, the reports state the result directly.
There is no default "winner" — each metric is reported factually.

## What is compared

**Measured:** Fetch HTML → extract clean Markdown → write to disk (the common denominator).

**NOT measured** (different scope, would need separate benchmarks):
- LLM extraction speed (only MarkCrawl and Crawl4AI have this)
- Supabase/vector upload (unique to MarkCrawl)
- FireCrawl SaaS API latency (depends on their servers, not the tool)
- Anti-bot bypass capability

## Tools and settings

**All tools run with equivalent settings:**

| Setting | Value | Why |
|---|---|---|
| Delay | 0 | Isolate processing speed, not politeness policy |
| Primary concurrency | 5 | How these tools are designed to be used in practice |
| Secondary concurrency | 1 | Single-threaded overhead comparison |
| JS rendering | OFF for static sites, ON for JS site | Fair comparison per site type |
| Timeout | 15s per request | Consistent across all |
| Output format | Markdown | Common denominator |
| Iterations | 2 per site, report median + std dev | Network variance is real |
| Warm-up | 1 throwaway run per site before timing | Exclude DNS/TLS cold start (see validation below) |
| Tool order | Randomized per site per run | Eliminate CDN/DNS cache bias from fixed ordering |
| Scheduling | Resource-aware parallel (see below) | Avoid browser-browser contention on one laptop |

### Why the warmup run is kept

Validation showed that the warmup run meaningfully improves benchmark stability.
The experiment (`warmup_validation/test_warmup_impact.py`) runs
each tool twice on the same site — once cold and once with a throwaway warmup
— and compares medians, standard deviations, and first-iteration outliers.

**Results (books-toscrape, 60 pages, concurrency=5, 4 iterations each):**

|                   | Median | Std dev | 1st iter | Range        |
|-------------------|--------|---------|----------|--------------|
| markcrawl (cold)  | 8.89s  | 0.59s   | 9.72s    | 8.32 – 9.72s |
| markcrawl (warm)  | 7.84s  | 0.32s   | 7.72s    | 7.64 – 8.36s |
| crawl4ai (cold)   | 5.67s  | 0.73s   | 6.95s    | 5.34 – 6.95s |
| crawl4ai (warm)   | 5.71s  | 0.40s   | 6.09s    | 5.28 – 6.09s |

**Key findings:**

1. **Variance drops ~47%** with warmup for both requests-based and
   browser-based tools. Lower variance means fewer iterations are needed
   to get a reliable median.

2. **The first cold iteration is 22–24% slower** than the warmed median
   for both tools, due to DNS resolution, TCP/TLS handshake, server-side
   CDN cache warming, and Python import/JIT effects.

3. **For markcrawl, warmup also shifts the median 13% faster**, likely
   because HTTP keep-alive and connection pooling benefit subsequent
   requests to the same host.

4. **With only 2 timed iterations** (the default), a cold first-run
   outlier has outsized impact on the median. Warmup eliminates this bias.

**Decision:** warmup is enabled by default. The cost is 1 extra run per
tool-site pair. The benefit is ~47% less measurement noise, which makes
the difference between "noisy numbers that could go either way" and
"stable numbers readers can trust."

To reproduce: `python warmup_validation/test_warmup_impact.py`

Full results: `warmup_validation/results_2026-04-07.txt`

### Resource-aware parallel scheduling

The benchmark classifies tools into two resource lanes:

- **Browser lane** (max 1 concurrent): crawl4ai, crawl4ai-raw, crawlee,
  playwright — these use Chromium and are CPU/memory heavy.
- **HTTP lane** (unlimited concurrency): markcrawl, scrapy+md, colly+md,
  firecrawl — lightweight, network-bound.

The scheduler enforces these pairing rules:

| Pairing | Allowed? | Why |
|---|---|---|
| browser + HTTP | Yes | HTTP tools are lightweight, no contention |
| HTTP + HTTP | Yes | Both are network-bound, not CPU-bound |
| browser + browser | No | Chromium contention degrades throughput |

This design was informed by measured throughput data showing browser tools
account for ~84% of total benchmark runtime. Running two browser tools
simultaneously on a single developer laptop causes resource thrash — more
memory pressure, more CPU contention, and less stable pages/sec — resulting
in worse throughput than running them sequentially.

The practical effect is ~2x wall-time speedup over fully sequential
execution: while a browser tool crawls one site, HTTP tools fill idle
time on other sites. Per-site semaphores still prevent multiple tools
(even HTTP tools) from hammering the same host simultaneously.

To force fully sequential execution: `--sequential`

### How each tool runs

> **Important:** No tool in this benchmark runs purely "out of the box." Every tool requires
> custom glue code for URL dispatch, output serialization, and integration with the benchmark
> harness. The table below documents exactly what custom code each tool uses so readers can
> judge how representative the results are.

| Tool | Custom code written | What crawl4ai/scrapy/etc. provides natively |
|---|---|---|
| markcrawl | Direct `CrawlEngine` API calls with per-URL fetch + process loop | CLI is out-of-box, but benchmark uses the Python API for URL-list mode |
| **crawl4ai** | `arun_many()` batch dispatch, custom file I/O (`.md` + `.jsonl`) | `AsyncWebCrawler`, `BrowserConfig`, `CrawlerRunConfig`, built-in markdown conversion. Also has `BFSDeepCrawlStrategy` for link discovery (unused) |
| **crawl4ai-raw** | Sequential `arun()` calls, same file I/O glue | Same as crawl4ai but without `arun_many()` batching — the simplest possible usage |
| **scrapy+md** | Full custom `Spider` class with `markdownify` in `parse()`, subprocess isolation | Scrapy provides the crawler framework; markdown conversion is custom |
| **crawlee** | Separate `crawlee_worker.py` subprocess with custom `PlaywrightCrawler` handler | Crawlee provides the crawler/queue; markdown conversion + file I/O is custom |
| **colly+md** | Go binary for HTML fetch + Python `markdownify` post-processing | Colly provides HTTP fetching; everything else is custom |
| **playwright** | Raw `page.goto()` + `page.content()` + `markdownify` | Playwright provides the browser; markdown conversion is entirely custom |
| **firecrawl** | API client with retry-with-backoff for rate limits, rate-limit wait subtracted from timing | FireCrawl API handles crawling + markdown conversion natively. Tested self-hosted (Docker); see note below |

#### Firecrawl limitations

Firecrawl is architecturally a SaaS product. Even the open-source self-hosted
version requires 4+ Docker services (API server, worker, Redis, Playwright) with
no library or single-process mode. The benchmarks use the self-hosted setup,
which crashed on 3 of 8 sites (react-dev, stripe-docs, blog-engineering) and
fetched fewer pages on others. Firecrawl's paid API likely performs better since
it scales these services independently. Firecrawl is included as the best
free-tier comparison available, but results may not reflect paid-tier
performance.

#### crawl4ai vs crawl4ai-raw

Crawl4AI is run in two configurations to show the impact of custom optimization:

- **crawl4ai** uses `arun_many()` which dispatches all URLs in a single batch call,
  letting crawl4ai manage browser tab concurrency internally. This is a performance
  optimization that requires knowing the URL list upfront.
- **crawl4ai-raw** uses sequential `arun()` calls with default `CrawlerRunConfig()` —
  the simplest possible crawl4ai usage. This represents what a developer gets with
  minimal effort.

Both use `result.markdown` directly (crawl4ai's built-in HTML-to-markdown conversion).
Neither uses crawl4ai's advanced features like `BFSDeepCrawlStrategy`, `FilterChain`,
content scoring, or LLM-based extraction.

#### Code samples

**MarkCrawl:**
```bash
markcrawl --base $URL --out ./results/markcrawl/$SITE --delay 0 --concurrency 5 --max-pages $N
```

**Crawl4AI (optimized):**
```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
    results = await crawler.arun_many(urls=url_list, config=CrawlerRunConfig())
    for result in results:
        # Write result.markdown to .md file + pages.jsonl
```

**Crawl4AI (raw baseline):**
```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
    for url in url_list:
        result = await crawler.arun(url=url, config=CrawlerRunConfig())
        # Write result.markdown to .md file + pages.jsonl
```

**Scrapy + markdownify:**
```python
# Custom Spider subclass with markdownify in parse()
# Markdown conversion cost is included in the timing
```

**FireCrawl:**
```python
from firecrawl import FirecrawlApp
app = FirecrawlApp(api_key=KEY)
result = app.crawl(url, limit=N, scrape_formats=["markdown"])
```

### Crawler tuning — equal effort across the board

Each crawler ships with default settings that are not necessarily what a user
would deploy in production. To keep the benchmark fair, we apply the same
*class* of tuning to every tool: realistic browser fingerprinting for HTTP
crawlers, common stealth flags for browser-based crawlers, and matched
timeouts. The intent is that any remaining performance gap reflects
**crawler design**, not missing config that a real user would have set.

Per-tool tuning applied (v1.3 cycle, 2026-05-04):

| Tool | Tuning applied | Rationale |
|---|---|---|
| **markcrawl** | upgraded to v0.10.5 (chunker defaults flip + sitemap-discovery deadline + idle-timeout exhaustion detection + partial-write recovery + 0-page diagnostic + adaptive scope broadening) + `MARKCRAWL_IDLE_TIMEOUT_S=300` env var | Five fixes between 0.5.0 → 0.10.5 affect benchmark numbers; the env var lets markcrawl wait longer for bursty URL discovery (HF surfaces URLs in 100-page bursts separated by 3-4 min idle windows). The 300s ceiling is universal — fast-discovery sites (postgres/mdn/k8s) exit in <30s and never hit it. Only sites with genuine bursty discovery (HF) benefit, exactly analogous to colly's WAF headers helping WAF sites and not helping static SPAs. |
| **scrapy+md** | browser-like UA (Chrome/130 macOS) + full Sec-Ch-Ua / Accept / Sec-Fetch-* headers via `USER_AGENT` and `DEFAULT_REQUEST_HEADERS`; subprocess timeout 300s → 600s with TimeoutExpired caught | Same WAF-bypass fix that landed for colly+md (commit `06501ac`); without it, scrapy is rejected by sites that gate on default-UA fingerprint (newegg, npr.org) |
| **crawl4ai** | default Patchright (stealth fork of Playwright). Two variants kept side-by-side: crawl4ai (Patchright) and crawl4ai-raw (raw Chromium) so we can measure when "stealth" helps and when it backfires (HF: raw wins 300/0; ikea: both work) | Patchright stealth tweaks paradoxically trigger MORE bot detection on some sites (Vercel/HF). Two-variant approach is the honest comparison |
| **crawl4ai-raw** | raw Chromium baseline, no stealth tweaks | Reference point for "what does an off-the-shelf browser see?" |
| **crawlee** | `--disable-blink-features=AutomationControlled` chromium flag (removes the most-detected automation signal: `navigator.webdriver=true`); browser-like UA + viewport 1920×1080 + en-US locale + `Sec-Ch-Ua` / `Accept-Language` extra HTTP headers via `browser_new_context_options` | Crawlee's defaults present a clearly-automated fingerprint; the flag + headers raise the floor without claiming full stealth (newegg may still block) |
| **playwright** (raw) | default Chromium, no stealth tweaks | Reference point similar to crawl4ai-raw — what does vanilla playwright see? |
| **colly+md** | browser-like UA (Chrome/130 macOS) + full Sec-Ch-Ua / Accept / Sec-Fetch-* headers (commit `06501ac`); 100ms delay, parallelism=5, retry-on-429 with backoff up to 3 retries; salvage logic in runner that markdownifies whatever HTML landed before subprocess timeout, so partial crawls produce partial output | Default colly UA (`colly - https://github.com/...`) is blocked by every modern WAF; without the headers colly returns 0 pages on 6+ sites |

**Cross-cutting wrapper changes** (apply equally to every tool):

| Change | Old | New | Why |
|---|---|---|---|
| `_RUN_TIMEOUT_PER_PAGE_S` (`benchmark_all_tools.py`) | 2 sec/page | 3 sec/page | Browser tools (crawl4ai, crawlee) regularly time out 5-10 pages short of completion on JS-heavy sites at 2 sec/page; 3 sec/page gives comfortable margin without inflating wall-clock for fast tools (which finish well under cap regardless) |
| `_Heartbeat` stall watchdog | 180s of no progress | 600s of no progress | colly writes HTML to a `_html/` subdir and only converts to `.md` after subprocess exits; previous 180s budget killed colly mid-crawl on big sites. 600s aligns with subprocess timeouts |
| `_Heartbeat` file-counting glob | `*.md` only | `*.md` + recursive `*.html` | colly's intermediate HTML files now register as progress, so the watchdog doesn't see "0 files" during colly's fetch phase |

**Where tuning hits its limit** (honest gaps remaining):

- **HTTP-only crawlers on JS-rendered SPAs** (scrapy+md/HF, colly+md/HF): no header tuning can render JavaScript. These zeros are *the benchmark working as intended* — they measure the cost of the HTTP-only design choice on sites that require a browser.
- **Aggressive anti-bot sites** (newegg, partly HF): even with full stealth + browser-like everything, sites that fingerprint TLS/JA3, browser audio context, GPU rendering, or canvas-fingerprint can detect automation. We don't pursue defeating these — that's a different benchmark (anti-bot bypass), not "RAG crawler quality."
- **markcrawl/HF specifically**: v0.10.3's idle-timeout fix lets the crawl exit cleanly with whatever it finds (~200 pages), so this gap closes in v1.3. Newegg still returns 0 (anti-bot) but now logs the HTTP status code so users can debug.

The intent is reproducibility: anyone can read the runner code (`runners/scrapy_runner.py`, `crawlee_worker.py`, `tools/colly_crawler/main.go`, `runners/markcrawl_runner.py`) and verify the tuning was actually applied — no hidden advantages.

### Site pool ethics — robots.txt and AI-bot policies

The benchmark is for AI/RAG use cases. Even when `User-agent: *` allows our
crawl, sites that explicitly disallow AI-specific bots (GPTBot, ClaudeBot,
anthropic-ai, PerplexityBot, etc.) are signaling they don't want their
content used by AI systems. The pool respects that signal — sites with broad
AI-bot blocks are removed even if technically crawlable.

**v1.3 cycle change:** `npr-news` removed, `propublica` added. NPR's
robots.txt explicitly disallows 15 AI bots. ProPublica is the only major
investigative-journalism outlet we audited that has no AI-bot blocks
(BBC News, Reuters, AP News, The Verge, Ars Technica, TechCrunch, Wired,
CNBC all block AI bots).

Future pool additions must pass `self_improvement/check_robots_ai.py`
before going into `sites/pool_v1.yaml`. The script audits any URL or the
entire current pool against the 19 known AI bots.

### Chunker dependency — markcrawl version delta

Every tool in this benchmark is chunked through markcrawl's
`chunk_markdown()` — see `benchmark_pipeline.py:45` and
`benchmark_retrieval.py:43`. MarkCrawl was upgraded from 0.5.0 (the PyPI
default at the time of the April v1.2 run) to 0.10.5 for this v1.3 cycle.
The version range spans 5+ minor releases; documented changes that affect
benchmark numbers include:

- **Chunker default flip** (multi-trial validated at +14% MRR on
  `all-MiniLM-L6-v2`, +15% on OpenAI 3-small per markcrawl's
  [v0.10 release report](https://github.com/AIMLPM/markcrawl/blob/main/bench/local_replica/v010_release_report.md))
- **DS-3.5 parallel sitemap discovery**, M6 dispatch cascade,
  scope-detection refinements, tenacity-backed retry layer
- **v0.10.2** sitemap-discovery deadline (60s wallclock cap on recursive
  sitemap-index parsing — fixes ikea's 2,113-shard index from exceeding
  the crawl-start budget)
- **v0.10.3** partial-write recovery (line-buffered `pages.jsonl`),
  discovery-exhaustion idle-timeout, 0-page diagnostic logging
- **v0.10.5** adaptive scope broadening (when narrow auto-scope exhausts
  with budget remaining and the leftmost path segment is a docs-hub marker
  like `docs`/`book`/`learn`, broaden once and replay filtered URLs —
  capped at 2 broadenings per crawl, never to whole-host).

Other tools were not upgraded between runs. Because `benchmark_pipeline.py`
chunks every tool's output through `markcrawl.chunker.chunk_markdown`, the
chunker change in particular affects all 7 tools' MRR and cost numbers,
not just markcrawl's row.

### Concurrency model comparison

Each tool handles concurrency differently. This affects how throughput scales and what limits apply.

| | MarkCrawl | Crawl4AI | Scrapy+md | Crawlee | FireCrawl |
|---|---|---|---|---|---|
| **Concurrency model** | Local threads (`--concurrency N`) | Async browser tabs (`arun_many`) | Async Twisted reactor (`CONCURRENT_REQUESTS`) | Async browser tabs (Playwright pool) | Remote browsers (server-side, tied to account tier) |
| **Default** | 1 (sequential) | 1 tab per `arun()`, batch via `arun_many()` | 16 | Automatic | 2 (free) to 100 (growth) |
| **Max practical** | Limited by target server's tolerance | Limited by local machine RAM/CPU | Limited by target server's tolerance | Limited by local machine RAM/CPU | Limited by your account tier |
| **Cost** | Free (your machine) | Free (your machine) | Free (your machine) | Free (your machine) | Pay for more browsers |
| **JS rendering** | Optional (`--render-js`, single Playwright) | Always (Playwright built-in) | No (HTTP only) | Always (Playwright built-in) | Always (remote Chromium) |
| **Scaling 1,000+ pages** | Increase `--concurrency`, add delay for politeness | Use `arun_many()` with dispatcher config | Increase `CONCURRENT_REQUESTS` | Configure crawler pool size | Upgrade account tier |

> **Note on FireCrawl tiers:** FireCrawl's crawl speed is directly tied to your account tier.
> Free accounts get 2 concurrent browsers, Hobby gets 5, Standard gets 50, and Growth gets 100.
> Per-page processing speed is the same across tiers — the difference is how many pages are
> processed simultaneously. A 100-page crawl that takes ~150s on free could finish in ~6s on Standard.

## Test sites

| Site | Pages | Type | Structural challenge |
|---|---|---|---|
| http://quotes.toscrape.com | 15 | Paginated content | Link-following, simple HTML |
| http://books.toscrape.com | 60 | E-commerce catalog | Pagination, product cards, categories |
| https://fastapi.tiangolo.com | 25 | API documentation | Code blocks, headings, tabs, admonitions |
| https://docs.python.org/3/library/ | 20 | Standard library docs | Tables, nested lists, cross-references |
| http://quotes.toscrape.com/js/ | 15 | JS-rendered version | Same content, requires browser rendering |

## Metrics

### Performance (automated)

| Metric | How measured | Tool |
|---|---|---|
| Pages/second (concurrent) | Total pages / wall-clock time at concurrency=5 | Script timer |
| Pages/second (sequential) | Same at concurrency=1 | Script timer |
| Time to first page | Time from process start to first .md file written | Script timer |
| Peak memory (RSS) | `psutil.Process().memory_info().rss` sampled every 0.5s during crawl | psutil |
| Output size | Total bytes of all .md files | `os.path.getsize` |

Note: Time to first page includes browser launch for Crawl4AI/FireCrawl. This is intentional — it's what the developer experiences.

### Markdown quality rubric (manual, reproducible)

For each test site, select 5 pages with known structural elements. Score each tool on a binary pass/fail per element:

| Element | Pass criteria | Pages to test |
|---|---|---|
| **Heading preservation** | All `<h1>`-`<h6>` converted to `#`-`######` with correct nesting | FastAPI tutorial page, Python docs module page |
| **Code block accuracy** | Fenced code blocks with language annotation preserved, no broken indentation | FastAPI endpoint examples, Python docs code samples |
| **Table rendering** | HTML tables converted to Markdown tables (or readable text if no table support) | Python docs comparison tables |
| **List structure** | Nested ordered/unordered lists maintain nesting and numbering | FastAPI query params docs |
| **Link preservation** | Internal and external links converted to Markdown `[text](url)` format | Any page with navigation links stripped, content links preserved |
| **Boilerplate removal** | No nav bar, footer, sidebar, cookie banner, or "Edit on GitHub" text in output | All pages — score as count of junk elements found |
| **Code inside paragraphs** | Inline code (`backticks`) preserved within paragraph text | FastAPI type hints documentation |

**Scoring per tool per site:** X/7 elements passing. Report as a percentage.

**Blind review:** Rename output directories to tool-A/tool-B/tool-C/tool-D before manual review to avoid bias.

### Junk detection (automated)

Same junk patterns as the existing benchmarks, applied to all tools equally:
- `<script>`, `<style>`, `<nav>`, `<footer>`, `<header>` tags in output
- Cookie banner/consent text
- "All rights reserved" boilerplate
- "Subscribe to newsletter" / "Follow us on" text

Count per tool across all pages. Lower is better.

### Quality scorer normalizations

The automated quality scorer (`quality_scorer.py`) applies several normalizations to
compare tool outputs fairly. These are **scoring-layer customizations**, not crawler
customizations — they don't change what any tool produces, only how it is measured.

| Normalization | What it does | Why it's needed |
|---|---|---|
| **URL trailing-slash stripping** | `url.rstrip("/")` when matching pages across tools | Scrapy records `/author/Jane-Austen/`, others record `/author/Jane-Austen`. Without this, the same page is treated as two different pages and consensus breaks. |
| **Paragraph unwrapping** | Joins soft line-wrapped lines into single sentences before splitting | The same sentence wrapped at column 80 (scrapy) vs column 200 (crawl4ai) would split into different fragments, making identical content look different. |
| **Markdown link stripping** | `[text](url)` → `text` before comparing sentences | URL text like `comlogin` or `comtagworldpage1` would contaminate sentence matching. |
| **Underscore normalization** | `_` → space | Markdown emphasis residue (`_keyword_`) kept underscores because `\w` matches `_`. |
| **Sparse page exclusion** | Pages with <2 extractable sentences excluded from precision/recall average | Short pages (e.g. a tag page with one quote) produce 0% for all tools, dragging every average down equally and hiding real differences. |

These normalizations are applied equally to all tools. Without them, the precision/recall
numbers are dominated by formatting artifacts rather than content quality differences.

### Retrieval quality (embedding comparison)

The quality metrics above measure extraction quality — how well each tool converts HTML to
Markdown. But for RAG pipelines, the downstream question is more important: **does the
extracted content produce useful embeddings?**

A tool that includes nav boilerplate in every page might still score well on precision
(the boilerplate is "shared" across tools) but produce poor embeddings because the same
navigation text dilutes the semantic signal in every chunk.

This is measured by running the same retrieval pipeline across all tools, using **four
retrieval modes** to test under realistic production conditions:

1. **Chunk** each tool's output using markdown-aware chunking (default: 400 word max, 50 word overlap)
2. **Embed** all chunks using OpenAI `text-embedding-3-small` (1536 dimensions)
3. **Index** chunks for both embedding (cosine similarity) and keyword (BM25 Okapi) search
4. **Query** — run 92 test queries across 8 sites against each tool's index
5. **Score** — measure Hit@K at K=1,3,5,10,20 plus MRR across four retrieval modes:
   - **Embedding**: Cosine similarity only
   - **BM25**: Keyword search only (Okapi BM25)
   - **Hybrid**: Embedding + BM25 fused via Reciprocal Rank Fusion (RRF, k=60)
   - **Reranked**: Top-50 hybrid candidates reranked by `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Chunk size sensitivity**: Optionally runs at three chunk configurations (~256tok, ~512tok,
~1024tok) to verify that quality differences hold regardless of chunking parameters.

The chunking, embedding, and retrieval pipeline is identical for all tools — the only
variable is extraction quality. This isolates the question: does cleaner extraction produce
better retrieval?

**Test sites** (8 sites, 109 queries):
| Site | Type | Queries | Why included |
|---|---|---|---|
| quotes-toscrape | Simple HTML | 8 | Paginated content, tag/author pages |
| books-toscrape | E-commerce | 10 | Category pages, product detail |
| fastapi-docs | API documentation | 20 | Code blocks, tutorials, reference |
| python-docs | Standard library docs | 19 | Glossary, release notes, how-tos |
| react-dev | SPA (JS-rendered) | 16 | Tests JS rendering, interactive docs |
| wikipedia-python | Wiki | 10 | Tables, infoboxes, citations |
| stripe-docs | API docs (tabbed) | 18 | Tabbed content, code samples |
| blog-engineering | Tech blog | 8 | Article extraction, images |

Results are published in [RETRIEVAL_COMPARISON.md](RETRIEVAL_COMPARISON.md).

To run the retrieval benchmark:

```bash
source .env  # needs OPENAI_API_KEY
python benchmark_retrieval.py                       # default config
python benchmark_retrieval.py --chunk-sensitivity   # + size analysis
python benchmark_retrieval.py --no-rerank           # skip cross-encoder (faster)
```

## Report format

### Summary table

```markdown
| Tool | Pages/sec (c=5) | Pages/sec (c=1) | Quality score | Junk count | Output KB | Peak RAM MB | Install time |
|---|---|---|---|---|---|---|---|
| MarkCrawl | X.X | X.X | X/7 | X | XX | XX | Xs |
| Crawl4AI | X.X | X.X | X/7 | X | XX | XX | Xs |
| FireCrawl | X.X | X.X | X/7 | X | XX | XX | Xs |
| Scrapy+md | X.X | X.X | X/7 | X | XX | XX | Xs |
```

### Per-site breakdown

One table per site with all metrics.

### Side-by-side output samples

For each site, show the same page's Markdown output from all 4 tools. Let the reader judge quality directly.

### Developer experience table (separate)

| Tool | Install command | Install time | Dependencies | First crawl command |
|---|---|---|---|---|
| MarkCrawl | `pip install markcrawl` | Xs | 4 (bs4, markdownify, requests, certifi) | `markcrawl --base URL --out ./output` |
| Crawl4AI | `pip install crawl4ai && playwright install` | Xs | Heavy (Playwright, Chromium) | Python script required |
| FireCrawl | `docker run ...` | Xs | Docker + Node.js | API call or SDK |
| Scrapy | `pip install scrapy markdownify` | Xs | Scrapy framework | Write spider class |

## Reproducibility

Every run writes a `manifest.json` capturing the exact sites, seed, pool
version, tool versions, and repo git SHA — so any run can be replayed
bit-for-bit. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the manifest
format and replay one-liners.

**Single-command reproduction (DS-13):**

```bash
make benchmark-quick   # ~5 min, single site, ~$0 spend (cached query embeddings) — verifies the pipeline runs
make benchmark         # ~24 hours, all 11 sites, ~$3 spend — produces the canonical reports
```

`benchmark-quick` is the smoke target — it runs `benchmark_retrieval.py` against the most recent merged run dir on a single site (`rust-book` by default; override with `SMOKE_SITE=...`) without the cross-encoder reranker. Useful for verifying the pipeline runs after methodology or code changes, before committing to a 24-hour cycle. Output goes to `reports/RETRIEVAL_QUICK_SMOKE.md` so it doesn't disrupt the canonical `RETRIEVAL_COMPARISON.md`.

`benchmark` is the full pipeline: `preflight` → retrieval (all 11 sites, all 4 modes including reranker) → answer-quality (LLM judge across 7 tools × ~104 queries × 2 calls each ≈ ~1,500 LLM calls) → pipeline timing → README regeneration. Wall-time is dominated by the cross-encoder reranker on large-chunk sites and the LLM-judge calls.

### Prerequisites

Before running the comparison, run the pre-flight script. It checks every dependency, installs anything missing, and tells you exactly what's ready:

```bash
python preflight.py --install
```

This handles everything automatically:
- Creates a `.venv` virtual environment if needed (avoids macOS system Python restrictions)
- Installs all Python packages (`markcrawl`, `crawl4ai`, `scrapy`, `crawlee`, `playwright`, `firecrawl-py`, `psutil`, etc.)
- Installs the Playwright Chromium browser
- Installs Go via Homebrew (if needed) and compiles the `colly+md` binary
- Checks all 4 test sites are reachable
- Prints a final ready status board showing green ✓ or red ✗ for every component

After it completes, activate the venv and run:

```bash
source .venv/bin/activate
python benchmark_all_tools.py
```

**FireCrawl (optional — skipped by default)**

FireCrawl requires one of:

- `FIRECRAWL_API_KEY` — use the FireCrawl SaaS API (free tier available at firecrawl.dev)
- `FIRECRAWL_API_URL` — point to a self-hosted instance

Add either to `.env` in the project root. The script auto-loads it — no need to `source .env` manually.

Self-hosting requires docker-compose (not a single container):

```bash
# See https://github.com/mendableai/firecrawl for the compose file
# Add to .env:
# FIRECRAWL_API_URL=http://localhost:3002
```

If neither env var is set, firecrawl is skipped and the other 6 tools run normally.

<details>
<summary>Manual setup reference (if you prefer not to use --install)</summary>

Python tools and their packages:

| Tool | Package(s) |
|---|---|
| markcrawl | `pip install -e .` (from repo root) |
| crawl4ai | `crawl4ai` 0.8.6+ |
| scrapy+md | `scrapy` + `markdownify` |
| crawlee | `crawlee[playwright]` 1.6.1+ |
| playwright | `playwright` 1.58.0+ |
| firecrawl | `firecrawl-py` 4.22.0+ (v2 API — `crawl()` not `crawl_url()`) |

`psutil` is also required for memory tracking.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[all]"
pip install crawl4ai scrapy markdownify crawlee playwright firecrawl-py psutil
playwright install chromium
```

For the Colly binary (Go 1.18+ required):

```bash
cd tools/colly_crawler
go build -o colly_crawler .
cd ../..
```

The script checks for the binary at `tools/colly_crawler/colly_crawler` and skips `colly+md` if it is not found.

</details>

### Running the benchmark

```bash
source .venv/bin/activate
python benchmark_all_tools.py
```

This script:
1. Checks that all tools are installed (exits with clear error if not)
2. Runs warm-up pass for each site
3. Runs 3 iterations per tool per site
4. Measures memory via psutil sampling
5. Generates `reports/SPEED_COMPARISON.md` with all tables and statistics
6. Saves raw Markdown output from each tool for manual quality review

Anyone can re-run it and verify the numbers. If the results are biased, the community can check.

## Benchmark 2: MarkCrawl full pipeline (end-to-end)

This is a **separate, MarkCrawl-only benchmark** that times the complete RAG pipeline that no other single tool offers. It answers: "If I crawl 50 pages, extract structured fields, and upload to Supabase, how long does the whole thing take?"

### What is timed (per stage)

```
Stage 1: Crawl           → pages.jsonl + .md files       (no API keys needed)
Stage 2: Extract fields  → extracted.jsonl                (needs OPENAI_API_KEY or similar)
Stage 3: Chunk + embed   → embedding vectors              (needs OPENAI_API_KEY)
Stage 4: Upload          → rows in Supabase               (needs SUPABASE_URL + KEY)
```

### Report format

```markdown
## Full Pipeline: FastAPI docs (25 pages)

| Stage | Time (s) | Cost | Output |
|---|---|---|---|
| Crawl (25 pages) | 4.8 | free | 25 .md files, 687 KB |
| Extract (5 fields) | 18.2 | ~$0.50 | extracted.jsonl |
| Chunk + embed | 3.1 | ~$0.003 | 89 chunks, 89 vectors |
| Upload to Supabase | 1.4 | free | 89 rows inserted |
| **Total** | **27.5** | **~$0.50** | **End-to-end RAG pipeline** |
```

### How it handles missing credentials

The script runs as much as possible without requiring setup:

| What's available | What runs |
|---|---|
| Nothing (just `pip install markcrawl`) | Stage 1 only — crawl timing |
| `OPENAI_API_KEY` set | Stages 1-3 — crawl + extract + embed |
| `OPENAI_API_KEY` + `SUPABASE_URL` + `SUPABASE_KEY` | All 4 stages — full pipeline |

Stages that can't run due to missing credentials are reported as "skipped (no API key)" rather than failing. This way anyone can run the benchmark and see at least the crawl timing.

### Mocked upload option

For users who want full pipeline timing without a real Supabase instance, the script offers a `--mock-upload` flag that:
- Runs the real chunking and embedding (measures actual OpenAI API time)
- Replaces the Supabase insert with a no-op (measures everything except network latency to Supabase)
- Reports the upload stage as "mocked — actual insert time depends on network to your Supabase instance"

### Script

```bash
# Crawl only (no API keys needed)
python run_pipeline.py

# With extraction (needs OPENAI_API_KEY)
python run_pipeline.py --extract

# Full pipeline with mock upload
python run_pipeline.py --extract --mock-upload

# Full pipeline with real Supabase
python run_pipeline.py --extract --upload
```

### Stage 5: Retrieval quality check (the real test)

The pipeline benchmark ends with a quality check that answers: "If I ask a question about the content I just crawled, do I get the right answer back?"

**How it works:**

1. After embedding, store all chunks + vectors in memory
2. Embed 5 test queries using the same embedding model
3. Compute cosine similarity between each query and all chunks
4. Check if the top-3 most similar chunks contain the correct source page
5. Report hit rate: "X/5 queries returned the correct page in top 3"

**Test queries for FastAPI docs (example):**

| Query | Expected source page | What it tests |
|---|---|---|
| "How do I add authentication to a FastAPI endpoint?" | Security/OAuth2 tutorial page | Can it find conceptual content? |
| "What is the default response status code?" | Response model docs | Can it find specific technical details? |
| "How do I define query parameters?" | Query parameters tutorial | Can it find tutorial content? |
| "What Python types does FastAPI support for request bodies?" | Request body docs | Can it find reference content? |
| "How do I handle file uploads?" | File upload tutorial | Can it find procedural content? |

**Why this is the most important metric:**

Pages/second measures how fast the pipe runs. Retrieval accuracy measures whether the pipe produces useful output. A crawler that's 10x faster but produces chunks that can't answer questions is worthless for RAG. This single metric — "does retrieval work?" — validates the entire pipeline: crawl quality, cleaning quality, chunk coherence, and embedding usefulness.

**No Supabase needed:** The similarity search runs in memory using numpy. The test is self-contained and reproducible.

```python
# Pseudocode for retrieval test
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

for query, expected_url in test_queries:
    query_vec = embed(query)
    scores = [(cosine_similarity(query_vec, chunk.vec), chunk) for chunk in all_chunks]
    top_3 = sorted(scores, reverse=True)[:3]
    hit = any(expected_url in chunk.url for _, chunk in top_3)
```

### A note on fairness

The retrieval quality check validates the entire pipeline end-to-end: if a crawl missed content, chunks split badly, or embeddings are poor, the test catches it. It is the metric that matters most for RAG.

This benchmark runs the retrieval check against all tools that support the full crawl-to-retrieval pipeline. Currently only markcrawl offers this as a built-in feature. If other tools add similar pipelines, the same retrieval queries will be run against their output for a direct comparison.

If retrieval accuracy for any tool falls to 3/5 or worse, that signals chunking or extraction needs improvement, and the reports will say so.

## Where results are published

- Full results: `reports/SPEED_COMPARISON.md` (separate doc, not in README)
- README: one-line link — "See [benchmark comparison](reports/SPEED_COMPARISON.md) for performance data against other crawlers."
- No benchmark tables in the README — keeps the README about the tool, not about competition.
