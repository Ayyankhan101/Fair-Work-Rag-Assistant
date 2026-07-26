# Project Context

## Code Quality Rules
- **Minimal code** — no unnecessary complexity
- **Smaller version preferred** — if 10 lines work, don't write 50
- **No boilerplate** — skip obvious comments, obvious functions
- **DRY** — never repeat logic
- **Readability > cleverness** — simple beats fancy

## Git Workflow (CRITICAL)
**⛔ NEVER touch `main` branch unless user explicitly says so.**
**All development happens via PRs to `develop` branch ONLY.**

### Auto PR Script
```bash
# Make changes, then run:
./scripts/auto-pr.sh "fix: resolve rate limit issue"
```

This will:
1. Create new branch: `feature/fix-rate-limit-issue-{timestamp}`
2. Commit changes
3. Push branch to origin
4. Create PR to `develop`
5. Auto-merge if no conflicts
6. Switch back to `develop`

### Manual PR Flow
```bash
# 1. Create feature branch
git checkout -b feature/add-new-award

# 2. Make changes, commit
git add .
git commit -m "feat: add new award support"

# 3. Push branch
git push origin feature/add-new-award

# 4. Create PR on GitHub
gh pr create --base develop --head feature/add-new-award --title "feat: add new award"

# 5. Merge after review
gh pr merge --merge --delete-branch
```

### Branch Rules
| Branch | Direct Push | PR Required |
|--------|-------------|-------------|
| `main` | ❌ Blocked | ✅ Yes |
| `develop` | ❌ Blocked | ✅ Yes |
| `feature/*` | ✅ Allowed | No |

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
- **Accuracy**: 87.5% (23/25 pass)
- **Vectorstore**: 16,692 docs indexed
- **Repo**: https://github.com/Ayyankhan101/fair-work-rag-assistant

## Key Commands
- Run eval: `venv/bin/python3 scripts/eval_hard.py`
- Start build: `venv/bin/python3 build_store.py`
- Auto PR: `./scripts/auto-pr.sh "commit message"`
- Test vectorstore: `venv/bin/python3 -c "from src.vectorstore import load_vectorstore; vs = load_vectorstore('data/vectorstore'); print(len(vs._store))"`
