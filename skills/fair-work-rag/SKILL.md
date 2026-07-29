---
name: fair-work-rag
description: Build, optimize, and troubleshoot RAG-powered LLM assistants for Australian employment law (Fair Work Awards + NES). Use when working with Claude/GPT-5.4 LLM, TurboVec vector store, fastembed embeddings, Cohere reranker, Gradio UI, or hybrid CAG+RAG architecture. Covers retrieval tuning, evaluation, and deployment.
---

# Fair Work RAG Assistant Skill

## Quick Start

```bash
# Run eval (from project root)
venv/bin/python3 scripts/eval_hard.py

# Build vectorstore (resumable)
venv/bin/python3 build_store.py

# Convert PDFs to markdown
venv/bin/python3 scripts/convert_pdfs_to_markdown.py

# Ingest markdown to vectorstore
venv/bin/python3 scripts/ingest_markdown.py

# Start Gradio UI
venv/bin/python3 src/app.py
```

## Architecture

Hybrid CAG+RAG system:
- **CAG**: Pre-loads NES (~28K chars) for NES-specific questions
- **RAG**: Vector search + BM25 + Reranker for Award-specific questions
- **Router**: Classifies questions as CAG/RAG/Combined (with negation handling)

### Key Files

| File | Purpose |
|------|---------|
| `src/config.py` | Shared config (119 award patterns, topic keywords, NES keywords) |
| `src/rag.py` | RAG chain with LLM + reranker integration, smart retrieval fallback |
| `src/cag.py` | CAG context cache for NES |
| `src/router.py` | Query router (with negation handling) |
| `src/filtered_retriever.py` | Award-specific retrieval (fuzzy matching, dedup, intent-aware scoring) |
| `src/hybrid_retriever.py` | BM25 + Semantic with RRF fusion |
| `src/reranker.py` | Cohere reranker + keyword fallback |
| `src/fastembeddings.py` | LangChain wrapper for fastembed ONNX |
| `src/vectorstore.py` | TurboVec build/load/search |
| `src/ingest.py` | PDF ingestion with contextual prefixes |
| `src/app.py` | Gradio chat interface |
| `build_store.py` | Auto-detects MD vs PDF, resumable |
| `scripts/ingest_markdown.py` | Markdown ingestion with full-clause header parsing |
| `scripts/convert_pdfs_to_markdown.py` | PDF → Markdown with table extraction |

## LLM Configuration

### Primary: Anthropic Claude Sonnet 4.6
```python
# src/rag.py
model="claude-sonnet-4-6-20250514"
```

### Alternative: OpenAI GPT-5.4
```python
model="gpt-5.4"
```

### Budget: Groq Llama 3.3 70B
```python
model="llama-3.3-70b-versatile"
```

### Auto-Fallback
```python
# get_llm(fallback=True) switches to cheaper model on rate limit
from src.rag import get_llm
llm = get_llm(fallback=True)
```

## Embedding Model

**BAAI/bge-base-en-v1.5** (768-dim, ONNX, CPU-only)
- Local inference, no API costs
- ~100ms per document
- Loaded via `src/fastembeddings.py`

## Vector Store

**TurboVec** (4-bit quantized, file-based)
- 31,134 chunks from 131 markdown files
- ~48MB index size
- Supports similarity search (NOT MMR)

## Reranker (Optional)

**Cohere rerank-english-v3.0** + keyword fallback
- +67% retrieval accuracy with Cohere
- Keyword-based fallback when Cohere unavailable
- Prioritizes dollar amounts, level patterns, rate terms

## Contextual Retrieval

Each chunk is prefixed with `[Award Name - Section]` for better retrieval:
```
[Clerks Award 2020 - Part 1: Application and Definitions]
This award covers all employees...
```

Implemented in:
- `scripts/convert_pdfs_to_markdown.py` — PDF → Markdown
- `scripts/ingest_markdown.py` — Fast ingestion with prefixes
- `src/ingest.py` — PDF ingestion with prefixes

## Evaluation

### Hard Eval (25 questions, content scoring)
```bash
venv/bin/python3 scripts/eval_hard.py
# Results: data/hard_eval_results.json
# Scoring: Keywords 40% + Pattern 30% + Quality 30%
```

### Basic Eval (12 questions)
```bash
venv/bin/python3 scripts/eval_prd_questions.py
# Results: data/prd_eval_results.json
```

### 5-Component Answer Format
```
**Answer:** [Direct answer with specific numbers]
**Award/NES Reference:** [Exact Award name]
**Clause/Section:** [Specific clause numbers]
**Explanation:** [How derived from context]
**Note:** [Required disclaimer]
```

## Accuracy Fixes (from QA)

| Fix | Description |
|-----|-------------|
| DEF-033 | System/user role separation, no forced answers |
| DEF-062 | 119 award aliases mapped (was 40) |
| DEF-063 | `needs_clarification()` for ambiguous queries |
| DEF-064 | Negation handling ("not retail" → excludes Retail) |
| DEF-066 | Fuzzy matching (0.9 threshold), k=30, deduplication |
| DEF-049/050 | Smart award name extraction from content |
| DEF-070 | BM25 retriever added |
| NEW | Query intent detection (rate vs clause vs rostering) |
| NEW | Dynamic scoring: clause queries penalize rate tables |
| NEW | Direct query term matching (bypasses topic keyword dependency) |
| NEW | Full-clause header parsing (resolves missing clause data) |
| NEW | Clause number extraction for sub-clauses (15.1, 13.5) |

## Retrieval Settings

| Parameter | Value | Notes |
|-----------|-------|-------|
| k (hybrid) | 10 | Balanced context |
| k (filtered) | 30 | Award-specific with dedup |
| max_tokens | 1024 | Full responses |
| doc truncation | 800 chars | More context per doc |
| max_chars | 4000 | More documents in context |
| reranker | Cohere v3.0 + keyword fallback | Optional, +67% accuracy |
| fuzzy threshold | 0.9 | High to avoid false positives |

## Award Mapping

119 award patterns in `src/config.py`:
- Clerks 2010, Children's 2010, Aged Care 2010
- Hospitality, Retail, Fast Food, Restaurant
- Cleaning, Health Professionals, Nurses
- Marine, Mining, Road Transport, Rail
- Professional Employees, Architects, Hair and Beauty
- And 100+ more...

## Topic Keywords

20+ topics for general questions:
- overtime, penalty, break, leave, casual, notice, allowance
- hours, public holiday, weekend, roster, junior, apprentice
- wages, redundancy, transfer, unfair dismissal, consultation

## Git Workflow

```bash
# Auto PR script
./scripts/auto-pr.sh "feat: add new feature"

# Manual PR
git checkout -b feature/my-change
git add . && git commit -m "feat: my change"
git push origin feature/my-change
gh pr create --base develop
```

**⚠️ NEVER touch `main` branch unless told.**

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Rate limit (429) | Use `get_llm(fallback=True)` for auto-switch |
| Empty retrieval | Check vectorstore exists: `ls data/vectorstore/` |
| Wrong award | Check `src/config.py` for 119 award patterns |
| Slow queries | Reduce k, use faster model |
| Reranker error | Set `COHERE_API_KEY` in `.env` or remove |

## Deployment

```bash
# Production VPS (4 vCPU, 8GB RAM)
# 1. Clone repo
# 2. Install deps: pip install -r requirements.txt
# 3. Set API keys in .env
# 4. Build vectorstore: python build_store.py
# 5. Start: python src/app.py
```
