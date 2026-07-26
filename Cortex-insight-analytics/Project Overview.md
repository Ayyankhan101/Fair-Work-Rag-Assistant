# Project Overview

## What Is This?
A RAG-powered LLM assistant for Australian employment law — answers questions about 130 Modern Awards + National Employment Standards (NES).

## Architecture
- **LLM**: Groq `llama-3.3-70b-versatile` (fallback: `llama-3.1-8b-instant`)
- **Embeddings**: fastembed `BAAI/bge-base-en-v1.5` (768-dim, ONNX)
- **Vector DB**: TurboVec (4-bit quantized, 16,692 docs)
- **UI**: Gradio 6.x
- **Quality**: 87.5% on hard eval (23/25 pass)

## Components
| Component | File | Purpose |
|-----------|------|---------|
| [[Config]] | `src/config.py` | Shared patterns + keywords |
| [[RAG Chain]] | `src/rag.py` | LLM + prompt |
| [[CAG Context Cache]] | `src/cag.py` | NES pre-loading |
| [[Query Router]] | `src/router.py` | CAG/RAG routing |
| [[Filtered Retriever]] | `src/filtered_retriever.py` | Award-specific search |
| [[Vector Store]] | `src/vectorstore.py` | TurboVec index |
| [[Vectorstore Checkpoint]] | `build_store.py` | Resume mechanism |

## Evaluation
- [[Evaluation Questions]] — 12 basic questions
- [[Evaluation Results]] — Scores and analysis
- [[Hard Eval Suite]] — 25 advanced questions

## Operations
- [[Rate Limit Status]] — Groq rate limits
- [[Code Quality Rules]] — Minimal code standards
- [[Architecture Decision]] — Why these choices

## Progress
- [[Improvement Progress]] — What's done
- [[Next Steps]] — What's next

## Key Files
- `src/config.py` — Shared award patterns, topic keywords, NES keywords
- `src/rag.py` — Prompt with rate-table rules
- `src/filtered_retriever.py` — Award-specific retrieval with rate-table scoring
- `scripts/eval_hard.py` — 25 questions with content scoring
- `data/vectorstore/` — TurboVec index (16,692 docs)
