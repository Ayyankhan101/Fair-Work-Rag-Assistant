# QA runbook

Run commands from the repository root.

## Environment

```powershell
python --version
git rev-parse HEAD
git status --short
python -m pip install -r requirements.txt
```

Record Python 3.11, the commit SHA, and the dirty-worktree output in the test report.

## Offline source gates

```powershell
python -m compileall -q src scripts "Quality Assurance Officer/tests" "Quality Assurance Officer/tools" build_store.py
ruff check src scripts build_store.py "Quality Assurance Officer/tests" "Quality Assurance Officer/tools"
ruff format --check src scripts build_store.py "Quality Assurance Officer/tests" "Quality Assurance Officer/tools"
python -m unittest discover -s "Quality Assurance Officer/tests" -v
```

Pass: every command returns exit code 0.

## Repository and corpus audit

```powershell
python "Quality Assurance Officer/tools/audit_repository.py" `
  --json "Quality Assurance Officer/evidence/current-repository-audit.json"
```

The command currently returns exit code 1 because mandatory release blockers exist. Read the `failures` array; do not override it.

## Store rebuild

Do not overwrite the only evidence copy.

1. Materialize `data/awards/`.
2. Create a source manifest with Award ID, title, source URL, amendment date, byte size, and SHA-256.
3. Build into a new directory.
4. Audit the new directory.
5. Compare old and new retrieval results.
6. Promote the new store only after approval.

Do not rely on earlier QA working-tree behavior. Those product changes were reverted and preserved only as a patch. Test the exact engineering candidate.

## API evaluation

Required environment:

```powershell
$env:GROQ_API_KEY="<set outside shell history where possible>"
```

Do not run `scripts/eval_hard.py` as release evidence yet. Its scorer does not verify claim support and its output lacks provenance. Use it only for comparison until the replacement evaluator is implemented.

No live provider evaluation is valid without an approved key, spend cap, redaction rule, exact model ID, provider request metadata, and retained token, latency, and cost records.

## UI test

```powershell
$env:GRADIO_SERVER_NAME="127.0.0.1"
$env:GRADIO_SERVER_PORT="7860"
python src/app.py
```

Check:

1. empty input;
2. input over 2,000 characters;
3. NES-only route;
4. Award-only route;
5. combined route;
6. missing evidence;
7. provider timeout;
8. provider rate limit;
9. server log without secret values;
10. browser response without exception details.

## Evidence naming

Use:

```text
YYYY-MM-DD_<commit-short-sha>_<gate>.<ext>
```

Store machine-readable evidence under `Quality Assurance Officer/evidence/`. Store reviewed release reports at the QA folder root.
