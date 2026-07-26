# Key Files

## Source Code
| File | Purpose | Related |
|------|---------|---------|
| `src/config.py` | Shared config (patterns, keywords) | [[Project Overview]] |
| `src/rag.py` | LLM chain + prompt | [[RAG Chain]] |
| `src/cag.py` | NES pre-loading | [[CAG Context Cache]] |
| `src/router.py` | Query classification | [[Query Router]] |
| `src/filtered_retriever.py` | Award-specific search | [[Filtered Retriever]] |
| `src/vectorstore.py` | TurboVec load/save | [[Vector Store]] |
| `src/bm25_retriever.py` | BM25 search | [[Filtered Retriever]] |
| `src/hybrid_retriever.py` | BM25 + Semantic | [[Filtered Retriever]] |
| `src/fastembeddings.py` | ONNX embeddings | [[Vector Store]] |
| `src/ingest.py` | PDF ingestion | [[Vector Store]] |
| `src/app.py` | Gradio UI | [[Project Overview]] |

## Scripts
| File | Purpose | Related |
|------|---------|---------|
| `scripts/eval_hard.py` | 25 hard questions | [[Hard Eval Suite]] |
| `scripts/eval_prd_questions.py` | 12 basic questions | [[Evaluation Questions]] |
| `build_store.py` | Vectorstore build | [[Vectorstore Checkpoint]] |

## Data
| Path | Purpose | Related |
|------|---------|---------|
| `data/vectorstore/` | TurboVec index | [[Vector Store]] |
| `data/awards/` | 130 award PDFs | [[Vector Store]] |
| `data/nes/nes_combined.txt` | NES text | [[CAG Context Cache]] |
| `data/docs_cache.pkl` | Cached docs | [[Vectorstore Checkpoint]] |

## Config
| File | Purpose |
|------|---------|
| `.env` | Groq API key |
| `requirements.txt` | Dependencies |
| `README.md` | Project docs |

## Related
- [[Project Overview]] — System design
