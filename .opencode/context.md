# Project Context

## Code Quality Rules
- **Minimal code** — no unnecessary complexity
- **Smaller version preferred** — if 10 lines work, don't write 50
- **No boilerplate** — skip obvious comments, obvious functions
- **DRY** — never repeat logic
- **Readability > cleverness** — simple beats fancy

## CRITICAL: Vectorstore Resume Protocol
**ALWAYS resume from checkpoint — NEVER delete index and rebuild from scratch.**

When restarting build:
```bash
venv/bin/python3 build_store.py  # Auto-resumes from checkpoint
```

Checkpoint location: `data/vectorstore/build_checkpoint.json`

If you see "Resuming from doc X/16692" — it's working correctly.

If you see "Batch 1/522" — something went wrong. Check checkpoint file.

## Current Status
- **Build**: job_a00900e9 running (full rebuild, 1hr timeout)
- **Progress**: 544/16692 (3.3%) as of 23:44
- **ETA**: ~50-60 min from start
- **Eval**: 25/25 pass, 89.3% average, target 95%

## Completed This Session
1. ✅ Hard eval suite (25 questions, content scoring)
2. ✅ Prompt improvements (3 few-shot examples, extraction rules)
3. ✅ Eval question fixes (QH04, QH07, QH19 corrected)
4. ✅ Vault notes updated (14 files)
5. ✅ Checkpoint docs added to vault + todo

## Next Steps
1. Wait for build to complete (resume from 9920)
2. Run hard eval (25 questions)
3. Fix issues → hit 95%
4. Push to 98%
5. Code quality — minimize, clean up
6. Docs quality — improve vault + skill files

## Key Commands
- Run eval: `venv/bin/python3 scripts/eval_hard.py`
- Start build: `venv/bin/python3 build_store.py`
- Test vectorstore: `venv/bin/python3 -c "from src.vectorstore import load_vectorstore; vs = load_vectorstore('data/vectorstore'); print(len(vs._store))"`
