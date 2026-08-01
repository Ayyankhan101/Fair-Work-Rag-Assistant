# Project Context

## Environment
- Language: Python 3.12
- Runtime: Groq API (llama-3.3-70b-versatile)
- Embeddings: fastembed (BAAI/bge-base-en-v1.5, 768-dim, ONNX)
- Vector DB: TurboVec (bit_width=4)
- UI: Gradio 6.x
- Repo: github.com/Ayyankhan101/Fair-Work-Rag-Assistant (private)
- Branch: develop

## Current Status
- **Phase 0: COMPLETE** (62599ee)
- **Phase 1: COMPLETE** (fa9bffd) — all code done, FWC decisions postponed
- **App running** at http://localhost:7860
- **Eval**: 100% section accuracy, 87.5% answer accuracy

## What's Working
- Router: 4 query types (jurisdictional, statutory_criteria, analogous_facts, procedural)
- CAG: Fair Work Act s385-394 (10978 chars, 10 sections)
- RAG: full pipeline (classify → generate → verify → resolve → abstain)
- Citation resolver: regex + corpus validation
- Abstention gate: 4-rule check
- Audit log: full trail
- Ingest: legislation ingestion (13 chunks)
- App: dual-mode Gradio UI (Unfair Dismissal / Awards)
- Router fix: time-limit queries now route correctly

## All Source Files
```
src/config.py       - FWC provisions, query categories, thresholds
src/router.py       - Query classification (4 types)
src/cag.py          - Cache-Augmented Generation for legislation
src/rag.py          - Full RAG pipeline with verification
src/filtered_retriever.py - UnfairDismissalRetriever
src/verifier.py     - Post-hoc citation verifier
src/citation_resolver.py - Regex + corpus validation
src/abstention_gate.py - 4-rule abstention
src/audit_log.py    - Full audit trail
src/corpus_manager.py - Point-in-time management
src/ingest.py       - FWC decisions ingestion
src/hybrid_retriever.py - BM25 + semantic hybrid search
src/bm25_retriever.py - BM25 retrieval
src/reranker.py     - Cohere reranker
src/fastembeddings.py - Fastembed ONNX embeddings
src/vectorstore.py  - TurboVec vector store
src/app.py          - Gradio UI
```

## Blocked
1. **FWC decisions download** — user will manually download via Brave browser (postponed)
2. **No vectorstore** — needs decisions first
3. **No SME** — need employment law practitioner
4. **No sponsor decisions D1-D6**

## Next Steps
1. User downloads 100 FWC decisions
2. Build vectorstore from decisions
3. Test full pipeline with decisions + legislation
4. Expand eval to 20+ questions
