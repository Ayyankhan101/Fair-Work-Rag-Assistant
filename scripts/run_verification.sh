#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

printf '== Retrieval smoke test ==\n'
./venv/bin/python3 scripts/smoke_test_retrieval.py

printf '\n== RAG smoke test ==\n'
./venv/bin/python3 scripts/smoke_test_rag.py

printf '\n== PRD 12-question eval ==\n'
./venv/bin/python3 scripts/eval_prd_questions.py

printf '\n== Gradio import check ==\n'
./venv/bin/python3 - <<'PY'
import sys
sys.path.insert(0, 'src')
import app
print('app import ok')
PY

printf '\nAll verification steps finished.\n'
