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
- **All code pushed to develop** (latest: 573f39d)
- **Merged branches deleted**: QA, qa
- **Block Direct Push workflow fixed** (eef7c02)
- **README upgraded** with Mermaid diagrams, syntax errors fixed (573f39d)

## What's Working
- Router: 4 query types
- CAG: Fair Work Act s385-394 (10978 chars, 10 sections)
- RAG: full pipeline (classify → generate → verify → resolve → abstain)
- Citation resolver, abstention gate, audit log
- Ingest: legislation ingestion (13 chunks)
- Eval: 100% section accuracy, 87.5% answer accuracy
- App: Gradio UI

## Blocked
1. **FWC decisions download** — bot protection. User must manually download from https://www.fwc.gov.au/document-search?search-ui=decisions (search: "unfair dismissal", type: Decisions, date: 01/01/2023-31/07/2026, save .txt to data/fwc_decisions/)
2. **No vectorstore** — needs decisions first
3. **No SME** — need employment law practitioner
4. **No sponsor decisions D1-D6**

## Next Steps
1. User downloads 100 FWC decisions
2. Build vectorstore from decisions
3. Test full pipeline with decisions + legislation
4. Expand eval to 20+ questions
