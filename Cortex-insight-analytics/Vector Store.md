# Vector Store

## Purpose
TurboVec quantized vector store for fast similarity search.

## Configuration
- Embeddings: `BAAI/bge-base-en-v1.5` (768-dim)
- Quantization: 4-bit (`bit_width=4`)
- Index: `data/vectorstore/index.tvim`

## Stats (July 2026)
- Documents: 31,134 (was 23,586)
- Index size: ~48MB
- Source: 131 markdown files (130 awards + NES)

## Files
| File | Purpose |
|------|---------|
| `index.tvim` | TurboVec index |
| `docstore.json` | Document store |
| `docs_cache.pkl` | Fastembed cache |

## Build
```bash
# Full rebuild (resumable)
PYTHONPATH=src venv/bin/python3 build_store.py --batch-size 16 --resume

# Ingest markdown only
PYTHONPATH=src venv/bin/python3 scripts/ingest_markdown.py
```

## Usage
```python
from vectorstore import load_vectorstore
vs = load_vectorstore("data/vectorstore")
results = vs.similarity_search("overtime penalty rate", k=10)
```

## Recent Changes (July 2026)
- Rebuilt with fixed parser (full-clause headers split into title+body)
- 31,134 docs (was 23,586) — recovered ~7,500 missing chunks
- Key recoveries: Fast Food clause 13.5 (11h max), Hospitality clause 15.1 (10 consecutive days)

## Related
- [[Project Overview]] — System design
- [[Vectorstore Checkpoint]] — Resume mechanism
- [[Filtered Retriever]] — Search logic
