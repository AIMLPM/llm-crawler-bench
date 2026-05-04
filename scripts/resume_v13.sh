#!/usr/bin/env bash
# Resume the v1.3 benchmark from checkpoint.
# Handles two cases:
#   1. Original temp dir still exists -> resume in place.
#   2. Temp dir cleaned (post-reboot, post-jetsam) -> rehydrate from safe copy
#      and rewrite checkpoint base_dir to point at the safe location.
#
# Usage:  scripts/resume_v13.sh
#
# Safe to run multiple times. Does not start the benchmark — just prepares
# state. Final line prints the command to actually relaunch.

set -euo pipefail

REPO=/Users/paulsave/Documents/Coding/llm-crawler-benchmarks
ORIG=/var/folders/k4/f24sfzw17cq9hrl7qmf6vyzh0000gn/T/benchmark_comparison_pvvlm_hg
SAFE="$REPO/runs/.in_progress_v13_temp"
CKPT="$REPO/.benchmark_checkpoint.json"

cd "$REPO"

if [[ ! -f "$CKPT" ]]; then
    echo "ERROR: no checkpoint at $CKPT — nothing to resume."
    exit 1
fi

if [[ -d "$ORIG" ]]; then
    echo "[resume] original temp dir exists, no rehydration needed."
    TARGET="$ORIG"
    # Top up safe copy with anything new in source.
    if [[ -d "$SAFE" ]]; then
        rsync -a "$ORIG/" "$SAFE/"
        echo "[resume] safe copy refreshed."
    fi
else
    echo "[resume] original temp dir is gone (likely post-reboot or post-jetsam)."
    if [[ ! -d "$SAFE" ]]; then
        echo "ERROR: no safe copy at $SAFE — cannot rehydrate. Aborting."
        exit 1
    fi
    TARGET="$SAFE"
    .venv/bin/python - <<PY
import json
cp = json.load(open("$CKPT"))
cp["base_dir"] = "$TARGET"
json.dump(cp, open("$CKPT", "w"), indent=2)
print(f"[resume] checkpoint base_dir rewritten to: $TARGET")
PY
fi

echo
echo "[resume] checkpoint state:"
.venv/bin/python -c "
import json
cp = json.load(open('$CKPT'))
results = cp.get('results') or {}
print(f'  base_dir: {cp.get(\"base_dir\")}')
print(f'  tools: {len(results)}, total tool-site pairs: {sum(len(s) for s in results.values())}')
"
echo
echo "[resume] all good. Relaunch with:"
echo "    nohup ./run_benchmarks.sh --standalone > /tmp/v13_run.log 2>&1 &"
echo "    caffeinate -i -s -w \$! &"
