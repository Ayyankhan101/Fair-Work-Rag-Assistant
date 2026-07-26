# Architecture — Hybrid CAG+RAG

## Overview
Combines Cache-Augmented Generation (NES) with Retrieval-Augmented Generation (Awards) for optimal accuracy.

## Components
```
Question → Router → CAG (NES) or RAG (Awards) or Both
                         ↓
                    LLM (Groq 70b/8b)
                         ↓
                    5-Component Answer
```

## CAG Path (NES)
- Pre-loads NES text (~28K chars) into context
- Triggers on NES keywords: "leave", "notice", "redundancy", "public holiday"
- No retrieval needed — instant, 100% recall

## RAG Path (Awards)
- TurboVec vector store (16K+ docs, 130 awards)
- BM25 + Semantic hybrid search with RRF (k=60)
- Filtered retriever for award-specific queries
- Award detection via 40+ keyword patterns
- Topic detection via 20+ topic keywords

## Router Logic
1. Check NES keywords → CAG or Combined
2. Check Award keywords → RAG or Combined
3. Check topic keywords → RAG with filtered retrieval
4. Default → Hybrid RAG

## Filtered Retriever
Fixes embedding similarity mismatch (e.g., Hospitality Award query returning Wine Industry docs).
- Detects award name from query (40+ patterns)
- Detects topic from query (20+ topics)
- Filters documents by award
- Scores by topic keywords with weighted scoring:
  - Exact phrase match = 5 points
  - Single keyword match = 1 point
  - Clause number presence = 2 bonus points
  - Percentage/number in content = 1 bonus points

## General Topic Retrieval
For questions without specific Award (e.g., "overtime rules"):
- Retrieves documents from multiple Awards
- Scores by relevance and diversity
- Boosts common Awards (Hospitality, Retail, Cleaning, Clerks)
- Returns top 15 diverse documents

## Auto Rate Limit Handling
- `ask_question()` catches 429 errors
- Auto-switches to `llama-3.1-8b-instant`
- Rebuilds chain with fallback model
- Retries automatically

## Evaluation
- Basic eval: 12 questions (format only)
- Hard eval: 25 questions (format + content scoring)
- Scoring: Keywords 40% + Pattern 30% + Quality 30%
- Current: 87.5% accuracy (23/25 pass)
- Target: 95%+

## Key Files
- `src/config.py` — Shared config (award patterns, topic keywords, NES keywords)
- `src/rag.py` — Main RAG chain
- `src/cag.py` — CAG context cache
- `src/router.py` — Query router
- `src/filtered_retriever.py` — Award-specific retrieval
- `src/hybrid_retriever.py` — BM25+Semantic with RRF
- `src/vectorstore.py` — TurboVec index
- `src/fastembeddings.py` — fastembed wrapper
- `src/ingest.py` — PDF ingestion
