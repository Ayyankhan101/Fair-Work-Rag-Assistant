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
- **All code pushed to develop** (latest: a04f1f1)
- **Merged branches deleted**: QA, qa
- **Block Direct Push workflow fixed** (eef7c02)
- **README upgraded** with professional Mermaid diagrams (a04f1f1)

## What's Working
- Router: 4 query types (jurisdictional/statutory_criteria/analogous_facts/procedural)
- CAG: Fair Work Act s385-394 (10978 chars, 10 sections)
- RAG: full pipeline (classify → generate → verify → resolve → abstain)
- Citation resolver: extracts and validates citations
- Ingest: legislation ingestion (13 chunks from s385-394)
- Eval: 8 golden-set questions — 100% section accuracy, 87.5% answer accuracy
- App: Gradio UI for unfair dismissal
- Docs: README, todo, quality-plan, work-log, context all updated

## Known Issues
- **README Mermaid diagrams** — some may not render on GitHub due to syntax (working on fix)

## Commits (on develop, all pushed)
```
a04f1f1 docs: professional README with Mermaid diagrams
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
1. **FWC decisions download** — bot protection. User must manually download from https://www.fwc.gov.au/document-search?search-ui=decisions (search: "unfair dismissal", type: Decisions, date: 01/01/2023-31/07/2026, save .txt to data/fwc_decisions/)
2. **No vectorstore** — needs decisions first
3. **No SME** — need employment law practitioner
4. **No sponsor decisions D1-D6**

## Next Steps
1. Fix remaining Mermaid syntax errors in README
2. User downloads 100 FWC decisions
3. Build vectorstore from decisions
4. Test full pipeline with decisions + legislation
5. Expand eval to 20+ questions
