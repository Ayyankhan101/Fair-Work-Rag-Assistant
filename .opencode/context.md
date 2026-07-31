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
- **Phase 1: IN PROGRESS** — pipeline tested, awaiting FWC decisions

### Completed
- All Phase 0 foundational files committed
- Router rewritten with query classification (jurisdictional/statutory_criteria/analogous_facts/procedural)
- RAG pipeline rewritten with full verification pipeline
- CAG rewritten for Fair Work Act s385-394
- App rewritten for unfair dismissal Gradio UI
- Config updated with expanded keywords
- filtered_retriever rewritten as UnfairDismissalRetriever
- Ingest rewritten for FWC decisions (structure-aware chunking)
- Eval framework created with 8 golden-set questions
- Pipeline tested: 100% section accuracy, 87.5% answer accuracy, 0% abstention rate

### Working Components
- Router: classifies queries into 4 types, detects CAG candidates
- CAG: loads Fair Work Act legislation context for unfair dismissal queries
- RAG: full pipeline (classify → CAG → generate → verify → resolve → abstain)
- Citation resolver: extracts and validates citations
- Ingest: legislation ingestion working (13 chunks from s385-394)
- Eval: runs 8 questions, measures section accuracy + answer accuracy

### Blockers
1. **FWC decisions** — website has bot protection, no public API. User must manually download.
2. **No vectorstore** — needs FWC decisions to build
3. **No SME** — need employment law practitioner
4. **No sponsor decisions** — D1-D6 not made

### FWC Download Instructions
User must manually download from: https://www.fwc.gov.au/document-search?search-ui=decisions
- Search: "unfair dismissal"
- Type: Decisions
- Date: 01/01/2023 - 31/07/2026
- Save .txt files to data/fwc_decisions/

## Next Steps
1. User downloads 100 FWC decisions
2. Build vectorstore from decisions
3. Test pipeline with decisions + legislation
4. Set up eval with more questions
5. Get sponsor decisions D1-D6
6. Engage employment law SME
