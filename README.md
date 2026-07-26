# Fair Work Awards & NES Knowledge Assistant

RAG-powered LLM assistant for Australian employment law — 130 Modern Awards + NES.

## Quick Start

```bash
# Setup
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your Groq API key

# Run eval
venv/bin/python3 scripts/eval_hard.py

# Run app
venv/bin/python3 src/app.py
```

## Architecture

- **LLM**: Groq `llama-3.3-70b-versatile` (fallback: `llama-3.1-8b-instant`)
- **Embeddings**: fastembed `BAAI/bge-base-en-v1.5` (768-dim, ONNX)
- **Vector DB**: TurboVec (4-bit quantized, 16,692 docs)
- **UI**: Gradio 6.x
- **Current accuracy**: 87.5% (23/25 pass)

## Project Structure

```
src/
  config.py          # Shared config (award patterns, keywords)
  rag.py             # RAG chain + prompt
  cag.py             # CAG context cache (NES)
  router.py          # Query router (CAG/RAG/Combined)
  filtered_retriever.py  # Award-specific retrieval
  hybrid_retriever.py    # BM25 + Semantic with RRF
  vectorstore.py     # TurboVec build/load
  ingest.py          # PDF ingestion
  app.py             # Gradio UI
scripts/
  eval_hard.py       # 25 hard eval questions
  eval_prd_questions.py  # 12 basic questions
build_store.py       # Vectorstore builder (resumable)
```

## Eval

```bash
venv/bin/python3 scripts/eval_hard.py
# Results: data/hard_eval_results.json
# Scoring: Keywords 40% + Pattern 30% + Quality 30%
```

## Data

- `data/awards/` — 130 award PDFs (not in zip, extract from Fair Work website)
- `data/nes/nes_combined.txt` — NES text
- `data/vectorstore/` — TurboVec index (16,692 docs)
- `data/docs_cache.pkl` — Cached ingested docs

## Notes

- Obsidian vault at `Cortex-insight-analytics/` (18 cross-linked notes)
- Project skill at `skills/fair-work-rag/`
- Code quality: 1,448 lines across 11 files
