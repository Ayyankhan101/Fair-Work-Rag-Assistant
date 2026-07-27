# Week 1 — RAG Document Assistant

> Chatbot that answers questions from uploaded PDFs with citations.
> **Role:** Data Engineer (Ayyan)

## Project Structure

```
week1-rag/
├── papers/                  # Raw PDFs (arXiv AI/LLM papers)
│   ├── manifest.txt         # List of downloaded papers
│   ├── 2305.10403.pdf       # LLaMA 2
│   ├── 1706.03762.pdf       # Attention Is All You Need
│   ├── 2005.11401.pdf       # RAG original paper
│   └── ...
├── scripts/
│   ├── download_papers.py   # Download from arXiv
│   └── chunk_and_embed.py   # Chunk + embed + build vector store
├── data/
│   ├── vector_store/        # FAISS index (2744 vectors, 7 MB)
│   ├── eval_qa.json         # 10-pair Q&A evaluation set
│   └── chunk_manifest.json  # Chunk stats for Model Engineer
└── docs/
    └── data_contract.md     # Handoff contract for Model Engineer
```

## Setup

```bash
pip install langchain langchain-community faiss-cpu fastembed pypdf
python scripts/download_papers.py
python scripts/chunk_and_embed.py
```

## Data Source

**arXiv AI/LLM papers** — 18 curated papers covering:
- Foundational LLMs (GPT-3, LLaMA, BERT, Attention)
- RAG (original paper, survey, Active RAG)
- Alignment (InstructGPT, DPO)
- Multimodal (GPT-4, Visual ChatGPT)
- Agents (Toolformer, HuggingGPT)
- Evaluation (HELM, Sparks of AGI)
- Efficiency (Mistral 7B, Gorilla)

## Chunking Strategy

- **Size:** 1000 characters
- **Overlap:** 200 characters
- **Splitter:** RecursiveCharacterTextSplitter
- **Separators:** `["\n\n", "\n", ". ", " "]`

## Definition of Done

- [x] Handles 50+ page documents (tested: GPT-4 100pp, LLaMA 2 93pp, GPT-3 75pp)
- [x] Shows its sources (citations via metadata: source, arxiv_id, chunk_index)
- [x] Scored against 10-pair Q&A evaluation set (`data/eval_qa.json`)

## Quick Start for Model Engineer

```python
# 1. Install deps
pip install langchain langchain-community faiss-cpu fastembed pypdf

# 2. Load vector store
from langchain_community.vectorstores import FAISS
from fastembed import TextEmbedding

class FastEmbed:
    def __init__(self):
        self._m = TextEmbedding("BAAI/bge-small-en-v1.5")
    def embed_documents(self, texts):
        return [list(e) for e in self._m.embed(texts)]
    def embed_query(self, text):
        return list(self._m.embed([text]))[0]

vs = FAISS.load_local(
    "data/vector_store",
    FastEmbed(),
    allow_dangerous_deserialization=True
)

# 3. Query
results = vs.similarity_search("What is RAG?", k=5)
for r in results:
    print(f"[{r.metadata['source']}] {r.page_content[:100]}...")

# 4. Eval set
import json
eval_set = json.load(open("data/eval_qa.json"))
# Each: {"question": "...", "answer": "...", "sources": [...]}
```

## Handoff Notes

**From:** Ayyan (Data Engineer)
**To:** Hania (Model Engineer)

### What You Get
- 18 arXiv papers chunked into 2744 vectors
- Pre-built FAISS index (load, don't rebuild)
- 10-pair Q&A eval set for scoring
- Full data contract in `docs/data_contract.md`

### Known Limitations
| Issue | Impact | What to Do |
|-------|--------|------------|
| CPU-only embedding | Rebuild takes ~8 min | Use pre-built index |
| 384-d vectors | Lower recall than 1536-d | Fine for 2744 chunks |
| FAISS flat index | Exact search | Scale OK at this size |

### Getting Help
- Data contract: `docs/data_contract.md`
- Pipeline script: `scripts/chunk_and_embed.py`
- Ask Ayyan if anything unclear

# Week 1 — RAG Document Assistant (Model Engineering & Evaluation)

> Optimizing RAG chain, reducing hallucinations, and improving citation precision.  
> **Role:** Model Engineer (Hania Mugheez)

---

## Project Overview

Took over the RAG pipeline handoff from Data Engineer (Ayyan), which included a pre-built FAISS vector store (2,744 vectors) and a 10-pair evaluation dataset (`eval_qa.json`). As Model Engineer, the goal is to implement the end-to-end RAG chain, evaluate generation quality, and refine response grounding to minimize hallucinations.

---

## Technical Stack & Dependencies

### Environment Setup

Configured the local virtual environment (`.venv`) and installed all required dependencies:

```bash
# Activate Virtual Environment (PowerShell)
.venv\Scripts\Activate.ps1

# Install Project Dependencies
pip install -r requirements.txt

[ FAISS Vector Store ]
            │
            ▼  (Top-k Retrieval: k=5)
   [ Context Documents ]
            │
            ▼
   [ Prompt Constraint ] ──► (Strict Grounding & Citation Rules)
            │
            ▼
  [ rag_chain.py Pipeline ]
            │
            ▼
 [ scripts/evaluate_rag.py ]
            │
            ▼
 [ data/rag_eval_report.json ]