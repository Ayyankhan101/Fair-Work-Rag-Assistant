---
name: fair-work-rag
description: Build, optimize, and troubleshoot RAG-powered LLM assistants for Australian employment law (Fair Work Awards + NES). Use when working with Groq LLM, TurboVec vector store, fastembed embeddings, Gradio UI, or hybrid CAG+RAG architecture. Covers rate limit handling, context optimization, retrieval tuning, and evaluation.
---

# Fair Work RAG Assistant Skill

## Quick Start

```bash
# Run eval (from project root)
venv/bin/python3 scripts/eval_prd_questions.py

# Run hard eval (25 questions with content scoring)
venv/bin/python3 scripts/eval_hard.py

# Build vector store (resumable)
venv/bin/python3 build_store.py

# Check rate limit
venv/bin/python3 -c "from groq import Groq; import os; from dotenv import load_dotenv; load_dotenv(); c=Groq(api_key=os.getenv('GROQ_API_KEY')); print('OK')"
```

## Architecture

Hybrid CAG+RAG system:
- **CAG**: Pre-loads NES (~28K chars) for NES-specific questions
- **RAG**: Vector search for Award-specific questions
- **Router**: Classifies questions as CAG/RAG/Combined

Key files:
- `src/config.py` — Shared config (award patterns, topic keywords, NES keywords)
- `src/rag.py` — RAG chain with Groq LLM (improved prompt, rate-table rules)
- `src/cag.py` — CAG context cache
- `src/router.py` — Query router
- `src/filtered_retriever.py` — Award-specific retrieval with rate-table scoring
- `src/hybrid_retriever.py` — BM25+Semantic with RRF
- `src/ingest.py` — PDF ingestion pipeline (130 PDFs + NES)
- `src/vectorstore.py` — TurboVec build/load/search

## Rate Limit Handling

Groq TPD limit (100k tokens/day) blocks eval. Strategies:

1. **Auto-fallback**: `ask_question()` auto-switches to 8b-instant on 429
2. **Reduce context**: k=10, truncated docs, max_tokens=1024
3. **Add delays**: 1s between questions for TPM limits
4. **Wait for reset**: Daily reset ~05:00 AM PKT

Model switching in `src/rag.py`:
```python
model="llama-3.3-70b-versatile"  # Production
model="llama-3.1-8b-instant"     # Rate limit fallback
```

## Context Optimization

| Parameter | Default | Optimized | Impact |
|-----------|---------|-----------|--------|
| k (retriever) | 20 | 10 | Balanced context |
| max_tokens | 1024 | 1024 | Full responses |
| doc truncation | None | 800 chars | More context per doc |
| max_chars | 2000 | 4000 | More documents in context |

## Evaluation

### Basic Eval (12 questions)
```bash
venv/bin/python3 scripts/eval_prd_questions.py
# Results saved to data/prd_eval_results.json
```

### Hard Eval (25 questions with content scoring)
```bash
venv/bin/python3 scripts/eval_hard.py
# Results saved to data/hard_eval_results.json
# Scoring: Keywords 40% + Pattern 30% + Quality 30%
```

### 5-Component Format
```
**Answer:** [Direct answer with specific numbers]
**Award/NES Reference:** [Exact Award name]
**Clause/Section:** [Specific clause numbers]
**Explanation:** [How derived from context]
**Note:** [Required disclaimer]
```

## Award Mapping

40+ award patterns in `src/config.py` (single source of truth):
- Cleaning, Hospitality, Clerks, Retail, Fast Food, Restaurant
- Professional Employees, Architects, Hair and Beauty
- Marine, Sporting, Animal Care, Aquaculture, Cotton
- Black Coal, Aluminium, Steel, Waste, Nursing, Health
- And many more...

Used by: rag.py, filtered_retriever.py, router.py, cag.py

## Topic Keywords

20+ topics for general questions:
- overtime, penalty, break, leave, casual, notice, allowance
- hours, public holiday, weekend, roster, junior, apprentice
- wages, redundancy, transfer, unfair dismissal, consultation

## Troubleshooting

See `references/troubleshooting.md` for common errors and fixes.
