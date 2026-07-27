# RAG Document Assistant — Data Contract

> **From:** Ayyan (Data Engineer)
> **To:** Model Engineer (Tooba & Hania Mugheez)
> **Week:** 1

## Input Format

**Source:** arXiv AI/LLM papers in PDF format

```
week1-rag/papers/
├── 2305.10403.pdf    (LLaMA 2)
├── 1706.03762.pdf    (Attention Is All You Need)
├── 2005.11401.pdf    (RAG original paper)
└── ...
```

## Chunking Strategy

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Chunk size | 1000 characters | Fits LLM context, preserves paragraph meaning |
| Chunk overlap | 200 characters | Prevents cutting mid-sentence, maintains context |
| Splitter | RecursiveCharacterTextSplitter | Handles markdown/text hierarchy |
| Separators | `["\n\n", "\n", ". ", " "]` | Paragraphs → sentences → words |

## Embedding Model

- **Model:** `BAAI/bge-small-en-v1.5` via fastembed (ONNX runtime, CPU-friendly)
- **Dimensions:** 384
- **Library:** fastembed (not sentence-transformers — no PyTorch dependency)

## Vector Store Output

```python
# Each chunk stored as:
{
    "id": "chunk_001",           # Unique chunk ID
    "text": "chunk content...",   # The actual text
    "metadata": {
        "source": "2305.10403.pdf",  # Filename
        "title": "LLaMA 2",          # Paper title (from manifest)
        "page": 5,                   # Page number (if extractable)
        "chunk_index": 3,            # Position in document
        "arxiv_id": "2305.10403"     # arXiv identifier
    },
    "embedding": [0.12, -0.03, ...]  # 384-d or 1536-d vector
}
```

## Retrieval Contract

Model Engineer receives:
- **Query:** User question string
- **Returns:** Top-k chunks (default k=5) with scores
- **Format:** List of `(chunk_text, score, metadata)` tuples

```python
# Retrieval example
results = vector_store.similarity_search(query, k=5)
# returns: [{"text": ..., "score": 0.87, "metadata": {...}}, ...]
```

## Quality Requirements

- [x] Chunks preserve sentence boundaries (no mid-sentence cuts)
- [x] Each chunk has source metadata (which paper, page, position)
- [x] Embeddings are normalized (L2 norm = 1)
- [x] Vector store supports cosine similarity search
- [x] Pipeline is repeatable (script, not manual)

## Files

- `papers/` — raw PDFs
- `papers/manifest.txt` — list of downloaded papers
- `scripts/chunk_and_embed.py` — chunking + embedding pipeline
- `data/vector_store/` — FAISS index (2744 vectors, 7 MB)
- `data/eval_qa.json` — 10-pair Q&A evaluation set
- `data/chunk_manifest.json` — chunk metadata manifest
- `docs/data_contract.md` — this file
