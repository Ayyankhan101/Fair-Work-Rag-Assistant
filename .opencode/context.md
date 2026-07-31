# Project Context

## Environment
- Language: Python 3.12
- Runtime: Groq API (llama-3.3-70b-versatile)
- Embeddings: fastembed (BAAI/bge-base-en-v1.5, 768-dim, ONNX)
- Vector DB: TurboVec (bit_width=4)
- UI: Gradio 6.x
- Repo: github.com/Ayyankhan101/fair-work-rag-assistant (private)
- Branch: develop

## Current Status
- **Phase 0: COMPLETE** (committed as 62599ee)
- **Phase 1: IN PROGRESS** — testing components before FWC decisions download

### What's Done (Phase 0)
- CORPUS_LICENCE_REGISTER.md (11 sources)
- DO_NOT_LIST.md (12 hard "do not" items)
- PIVOT_PLAN.md (comprehensive pivot plan)
- src/config.py — FWC provisions s385-394
- src/verifier.py — post-hoc citation verifier (needs Groq API)
- src/citation_resolver.py — regex extract + corpus validation ✅ tested
- src/abstention_gate.py — 4-rule abstention ✅ tested (needs method signature fix)
- src/audit_log.py — full audit trail
- src/corpus_manager.py — point-in-time, versioning
- src/cag.py — rewritten for Fair Work Act ✅ tested
- scripts/download_fwc_decisions.py — FWC scraper (blocked by bot protection)
- data/legislation/fair_work_act_s385_394.txt — legislation text

### What's Working
- Config loads 10 FWC provisions
- CAG detects unfair dismissal queries and returns legislation context
- Citation resolver extracts citations (e.g., "s385")
- Abstention gate loaded (needs method signature fix)

### Blockers
1. **FWC decisions** — website has bot protection, no public API
2. **Groq rate limits** — daily TPD exhausted, resets ~00:00 UTC
3. **No SME** — need employment law practitioner
4. **No sponsor decisions** — D1-D6 not made

### Can Be Done Now (No FWC needed)
- Fix abstention gate method signature
- Test full pipeline with Fair Work Act only
- Build UI
- Set up eval framework

## Pending Tasks (Phase 1)
- [ ] Fix abstention_gate.py method signature
- [ ] Test full RAG pipeline with legislation only
- [ ] Rewrite src/ingest.py for FWC decisions (when available)
- [ ] Rewrite src/rag.py with verifier + resolver + abstention
- [ ] Rewrite src/router.py for query classification
- [ ] Rewrite src/filtered_retriever.py for decision filtering
- [ ] Update src/app.py for unfair dismissal
- [ ] Download 100 FWC decisions (manual, user task)
