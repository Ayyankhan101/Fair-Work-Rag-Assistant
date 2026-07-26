# Vector Store

## Purpose
TurboVec quantized vector store for fast similarity search.

## Configuration
- Embeddings: `BAAI/bge-base-en-v1.5` (768-dim)
- Quantization: 4-bit (`bit_width=4`)
- Index: `data/vectorstore/index.tvim`

## Files
| File | Purpose |
|------|---------|
| `index.tvim` | TurboVec index |
| `docstore.json` | Document store |
| `build_checkpoint.json` | Resume position |

## Build
```bash
venv/bin/python3 build_store.py
```

## Usage
```python
from vectorstore import load_vectorstore
vs = load_vectorstore("data/vectorstore")
results = vs.similarity_search("overtime penalty rate", k=10)
```

## Related
- [[Project Overview]] — System design
- [[Vectorstore Checkpoint]] — Resume mechanism
- [[Filtered Retriever]] — Search logic
