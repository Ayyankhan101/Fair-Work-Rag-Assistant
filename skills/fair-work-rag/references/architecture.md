# Architecture — Hybrid CAG+RAG

## Overview
Combines Cache-Augmented Generation (NES) with Retrieval-Augmented Generation (Awards) for optimal accuracy.

## Components
```
Question → Router → CAG (NES) or RAG (Awards) or Both
                         ↓
                    Smart Retriever (filtered vs hybrid based on answer relevance)
                         ↓
                    Reranker (Cohere + keyword fallback)
                         ↓
                    LLM (Groq llama-3.3-70b-versatile)
                         ↓
                    5-Component Answer
```

## CAG Path (NES)
- Pre-loads NES text (~28K chars) into context
- Triggers on NES keywords: "leave", "notice", "redundancy", "public holiday"
- No retrieval needed — instant, 100% recall

## RAG Path (Awards)
- TurboVec vector store (31,134 docs, 130 awards)
- BM25 + Semantic hybrid search with RRF (k=60)
- Filtered retriever for award-specific queries
- Award detection via 119 keyword patterns
- Topic detection via 20+ topic keywords

## Router Logic
1. Check NES keywords → CAG or Combined
2. Check Award keywords → RAG or Combined
3. Check topic keywords → RAG with filtered retrieval
4. Default → Hybrid RAG

## Filtered Retriever (Intent-Aware)
Fixes embedding similarity mismatch (e.g., Hospitality Award query returning Wine Industry docs).

### Detection Pipeline
1. **Award detection**: 119 keyword patterns + fuzzy matching (0.9 threshold)
2. **Topic detection**: 20+ topics with keyword values
3. **Query term extraction**: Direct content matching (bypasses topic dependency)
4. **Intent detection**: Rate vs clause vs rostering query classification

### Dynamic Scoring
- **Rate queries** (pay/salary/rate): Boost rate tables (+10 for dollar+level)
- **Clause queries** (hours/rostering/rules): Penalize rate tables (-5), boost operational content (+5)
- **Rostering queries**: Additional boost for roster/consecutive/days off content
- **Direct term matches**: +3 per matching query term in content

## General Topic Retrieval
For questions without specific Award (e.g., "overtime rules"):
- Retrieves documents from multiple Awards
- Scores by relevance and diversity
- Boosts common Awards (Hospitality, Retail, Cleaning, Clerks)
- Returns top 20 diverse documents

## Smart Retrieval Fallback
In `src/rag.py`: Filtered retriever used only when top-5 docs contain query keywords. Falls back to hybrid otherwise.

## Auto Rate Limit Handling
- `ask_question()` catches 429 errors
- Auto-switches to `llama-3.1-8b-instant`
- Rebuilds chain with fallback model
- Retries automatically

## Evaluation
- Hard eval: 25 questions (format + content scoring)
- Scoring: Keywords 40% + Pattern 30% + Quality 30%
- Best: 85.0% (with 70b model, before vectorstore rebuild)
- Latest: 82.5% (all questions on fallback model due to rate limits)
- Target: 95%+

## Key Files
- `src/config.py` — Shared config (119 award patterns, topic keywords, NES keywords)
- `src/rag.py` — Main RAG chain with smart retrieval fallback
- `src/cag.py` — CAG context cache
- `src/router.py` — Query router with negation handling
- `src/filtered_retriever.py` — Intent-aware award-specific retrieval
- `src/hybrid_retriever.py` — BM25+Semantic with RRF
- `src/reranker.py` — Cohere reranker + keyword fallback
- `src/vectorstore.py` — TurboVec index
- `src/fastembeddings.py` — fastembed wrapper
- `src/ingest.py` — PDF ingestion
- `scripts/ingest_markdown.py` — Markdown ingestion with full-clause parsing
- `scripts/convert_pdfs_to_markdown.py` — PDF→MD with table extraction
