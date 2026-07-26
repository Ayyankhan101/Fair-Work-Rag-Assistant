#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PATTERN="${1:-build_store.py}"
SLEEP_SECS="${2:-60}"

while pgrep -f "$PATTERN" >/dev/null 2>&1; do
  sleep "$SLEEP_SECS"
done

if [[ -f data/vectorstore/index.tvim && -f data/vectorstore/docstore.json ]]; then
  ./scripts/run_verification.sh > verification.log 2>&1 || true
else
  printf 'Vector store missing after build stop. Skipping verification.\n' > verification.log
fi
