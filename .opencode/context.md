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
- **Phase 0: COMPLETE** (62599ee)
- **Phase 1: IN PROGRESS** — pipeline tested, awaiting FWC decisions
- **All code pushed to develop** (233bfdc + eef7c02)
- **Merged branches deleted**: QA, qa (cleaned up)
- **Block Direct Push workflow fixed** (eef7c02)

## What's Working
- Router: classifies queries into 4 types (jurisdictional/statutory_criteria/analogous_facts/procedural)
- CAG: loads Fair Work Act s385-394 context (10978 chars, 10 sections)
- RAG: full pipeline (classify → generate → verify → resolve → abstain)
- Citation resolver: extracts and validates citations
- Ingest: legislation ingestion (13 chunks from s385-394)
- Eval: 8 golden-set questions — 100% section accuracy, 87.5% answer accuracy
- App: Gradio UI for unfair dismissal
- All docs updated: README, todo, quality-plan, work-log, context

## Commits (on develop, all pushed)
```
eef7c02 fix: Block Direct Push workflow
eb78e1d docs: update all documentation
e514d0a docs: update context
06d547d feat: rewrite ingest.py + eval framework
1fa1ece feat: add compensation keywords
58d39bd feat: fix rag pipeline
8390e24 feat: rewrite app.py
9c281e1 feat: rewrite rag.py
1e8553f feat: rewrite filtered_retriever
a04ada3 feat: rewrite router
baefd5e feat: rewrite cag.py
62599ee Phase 0: foundational files
```

## Blocked
1. **FWC decisions download** — bot protection, no API. User must manually download from https://www.fwc.gov.au/document-search?search-ui=decisions (search: "unfair dismissal", type: Decisions, date: 01/01/2023-31/07/2026, save .txt to data/fwc_decisions/)
2. **No vectorstore** — needs decisions first
3. **No SME** — need employment law practitioner
4. **No sponsor decisions D1-D6**

## Next Steps
1. User downloads 100 FWC decisions
2. Build vectorstore from decisions
3. Test full pipeline with decisions + legislation
4. Expand eval to 20+ questions
5. Get sponsor decisions D1-D6
6. Engage employment law SME
