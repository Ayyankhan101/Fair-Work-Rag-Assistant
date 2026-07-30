# 🏛️ Fair Work Awards & NES Knowledge Assistant

> RAG-powered LLM assistant for Australian employment law — 130 Modern Awards + National Employment Standards

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LLM-Claude](https://img.shields.io/badge/LLM-Claude_4.6-7B5EA7.svg)](https://anthropic.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📊 Architecture Overview

```mermaid
graph TB
    subgraph User["👤 User Interface"]
        UI[Gradio Chat UI]
    end

    subgraph Router["🧠 Query Router"]
        R[Router]
        R -->|NES query| CAG
        R -->|Award query| RAG
        R -->|Mixed| BOTH
    end

    subgraph CAG["📦 CAG Context Cache"]
        NES[NES Text Cache<br/>~28K chars]
    end

    subgraph RAG["🔍 RAG Pipeline"]
        HYB[Hybrid Retriever]
        HYB --> BM25[BM25 Retriever]
        HYB --> SEM[Semantic Search]
        BM25 --> RRF[RRF Fusion<br/>k=60]
        SEM --> RRF
        RRF --> FIL[Filtered Retriever<br/>k=20]
    end

    subgraph VectorDB["💾 Vector Store"]
        TV[TurboVec<br/>4-bit Quantized]
        TV --> IDX[Index: 16,692 docs]
        TV --> DS[DocStore]
    end

    subgraph Embed["🧮 Embeddings"]
        FE[FastEmbed<br/>BAAI/bge-base-en-v1.5<br/>768-dim ONNX]
    end

    subgraph LLM["🤖 Language Model"]
        GROQ[Groq API]
        GROQ -->|Primary| 70B[llama-3.3-70b-versatile]
        GROQ -->|Fallback| 8B[llama-3.1-8b-instant]
    end

    subgraph Output["📄 5-Component Output"]
        O1[Answer]
        O2[Award/NES Reference]
        O3[Clause/Section]
        O4[Explanation]
        O5[Note]
    end

    UI --> R
    CAG --> FIL
    RAG --> FIL
    FIL --> FE
    FE --> TV
    FIL --> GROQ
    NES --> FIL
    GROQ --> O1
    GROQ --> O2
    GROQ --> O3
    GROQ --> O4
    GROQ --> O5

    style User fill:#0277bd,stroke:#01579b,stroke-width:2px,color:#fff
    style Router fill:#e65100,stroke:#bf360c,stroke-width:2px,color:#fff
    style CAG fill:#2e7d32,stroke:#1b5e20,stroke-width:2px,color:#fff
    style RAG fill:#b71c1c,stroke:#880e4f,stroke-width:2px,color:#fff
    style VectorDB fill:#6a1b9a,stroke:#4a148c,stroke-width:2px,color:#fff
    style Embed fill:#00695c,stroke:#004d40,stroke-width:2px,color:#fff
    style LLM fill:#f57f17,stroke:#e65100,stroke-width:2px,color:#000
    style Output fill:#283593,stroke:#1a237e,stroke-width:2px,color:#fff
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Groq API key ([Get one here](https://console.groq.com/))
- 2GB+ free disk space

### Installation

```bash
# Clone the repo
git clone https://github.com/Ayyankhan101/fair-work-rag-assistant.git
cd fair-work-rag-assistant

# Switch to develop branch (full codebase)
git checkout develop

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Run the App

```bash
venv/bin/python3 src/app.py
# Open http://localhost:7860 in your browser
```

### Run Evaluation

```bash
# Hard eval (25 questions with content scoring)
venv/bin/python3 scripts/eval_hard.py

# Basic eval (12 questions)
venv/bin/python3 scripts/eval_prd_questions.py
```

---

## 🏗️ Architecture Details

### Hybrid CAG+RAG System

| Component | Purpose | Technology |
|-----------|---------|------------|
| **CAG** | NES-specific questions (100% recall) | Pre-loaded text cache (~28K chars) |
| **RAG** | Award-specific questions | TurboVec + Hybrid retrieval |
| **Router** | Classifies incoming queries | Pattern matching + keyword detection |

### Query Flow

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant R as 🧠 Router
    participant C as 📦 CAG
    participant V as 💾 VectorStore
    participant L as 🤖 LLM

    U->>R: "What are casual loading rates?"
    R->>R: Detect topic + award
    
    alt NES Query
        R->>C: Fetch NES context
        C->>L: NES context + query
    else Award Query
        R->>V: Hybrid search (BM25 + Semantic)
        V->>L: Award docs + query
    else Combined Query
        R->>C: Fetch NES context
        R->>V: Hybrid search
        C->>L: NES + Award docs + query
    end
    
    L->>U: 5-component answer
```

### Retrieval Pipeline

```mermaid
graph LR
    Q[Query] --> BM25[BM25 Retriever<br/>k=10]
    Q --> SEM[Semantic Search<br/>k=10]
    BM25 --> RRF[RRF Fusion<br/>k=60]
    SEM --> RRF
    RRF --> FIL[Filtered Retriever<br/>Award-specific<br/>+ Topic keywords]
    FIL --> TOP[Top 10 Results]
    TOP --> CTX[Context Window<br/>max 4000 chars]
    
    style Q fill:#0277bd,stroke:#01579b,color:#fff
    style RRF fill:#e65100,stroke:#bf360c,color:#fff
    style FIL fill:#2e7d32,stroke:#1b5e20,color:#fff
    style CTX fill:#b71c1c,stroke:#880e4f,color:#fff
```

---

## 📁 Project Structure

```
fair-work-rag-assistant/
├── 📄 README.md                    # This file
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment template
├── 📄 build_store.py               # Vectorstore builder (resumable)
│
├── 📂 src/                         # Core application code
│   ├── 🐍 config.py                # Shared config (patterns, keywords)
│   ├── 🐍 rag.py                   # RAG chain + improved prompt
│   ├── 🐍 cag.py                   # CAG context cache (NES)
│   ├── 🐍 router.py                # Query router (CAG/RAG/Combined)
│   ├── 🐍 filtered_retriever.py    # Award-specific retrieval
│   ├── 🐍 hybrid_retriever.py      # BM25 + Semantic with RRF
│   ├── 🐍 bm25_retriever.py        # BM25 retriever
│   ├── 🐍 vectorstore.py           # TurboVec build/load/search
│   ├── 🐍 fastembeddings.py        # LangChain wrapper for fastembed
│   ├── 🐍 ingest.py                # PDF ingestion pipeline
│   └── 🐍 app.py                   # Gradio chat interface
│
├── 📂 scripts/                     # Evaluation & utilities
│   ├── 🐍 eval_hard.py             # 25 hard eval questions
│   ├── 🐍 eval_prd_questions.py    # 12 basic questions
│   └── 🐍 rename_pdfs.py           # PDF rename utility
│
├── 📂 data/                        # Data files
│   ├── 📂 awards/                  # 130 award PDFs (gitignored)
│   ├── 📂 nes/                     # NES text files
│   │   └── 📄 nes_combined.txt     # Full NES (~28K chars)
│   ├── 📂 vectorstore/             # TurboVec index (LFS)
│   │   ├── 📄 index.tvim           # Vector index
│   │   └── 📄 docstore.json        # Document store
│   ├── 📄 docs_cache.pkl           # Cached ingested docs (LFS)
│   ├── 📄 hard_eval_results.json   # Latest eval results
│   └── 📄 prd_eval_results.json    # Basic eval results
│
├── 📂 skills/fair-work-rag/        # Project skill
│   ├── 📄 SKILL.md                 # Skill documentation
│   ├── 📂 assets/
│   │   └── 📄 prompt_template.txt  # LLM prompt template
│   ├── 📂 references/
│   │   ├── 📄 architecture.md      # Architecture docs
│   │   ├── 📄 optimization.md      # Optimization guide
│   │   └── 📄 troubleshooting.md   # Common issues
│   └── 📂 scripts/
│       └── 🐍 run_eval.py          # Eval runner
│
├── 📂 Cortex-insight-analytics/    # Obsidian vault (18 notes)
│   ├── 📄 Project Overview.md
│   ├── 📄 Key Files.md
│   ├── 📄 Architecture Decision.md
│   └── 📄 ... (15 more notes)
│
└── 📂 .opencode/                   # Mission context
    ├── 📄 context.md               # Project context
    ├── 📄 todo.md                   # Task tracking
    └── 📄 work-log.md              # Work log
```

---

## 🎯 Evaluation

### Scoring System

| Component | Weight | Description |
|-----------|--------|-------------|
| **Keywords** | 40% | Must-include terms (synonyms accepted) |
| **Pattern** | 30% | Structural requirements (numbers, clauses) |
| **Quality** | 30% | Completeness and accuracy |

### Current Results

| Metric | Value |
|--------|-------|
| **Accuracy** | 87.5% (23/25 pass) |
| **Questions** | 25 hard questions |
| **Scoring** | Content-based (not exact match) |

### Running Eval

```bash
# Full eval with detailed output
venv/bin/python3 scripts/eval_hard.py

# Results saved to
data/hard_eval_results.json
```

---

## 🔧 Configuration

### Key Parameters (`src/config.py`)

| Parameter | Value | Description |
|-----------|-------|-------------|
| `K_HYBRID` | 10 | Hybrid retrieval results |
| `K_FILTERED` | 20 | Filtered retrieval results |
| `MAX_TOKENS` | 1024 | LLM max output tokens |
| `DOC_CHARS` | 800 | Doc truncation limit |
| `MAX_CHARS` | 4000 | Total context limit |

### Model Configuration

```python
# Primary model (production)
model = "llama-3.3-70b-versatile"

# Fallback model (rate limit)
model = "llama-3.1-8b-instant"
```

---

## 📚 Data Sources

| Source | Count | Size | Description |
|--------|-------|------|-------------|
| **Modern Awards** | 130 | ~133MB PDFs | All Australian awards |
| **NES** | 1 | ~28K chars | National Employment Standards |
| **Vector Store** | 16,692 docs | ~31MB | Indexed chunks |

---

## 🛠️ Development

### ⛔ Branch Rules (CRITICAL)

| Branch | Direct Push | PR Required | Notes |
|--------|-------------|-------------|-------|
| `main` | ❌ **NEVER TOUCH** | ❌ | Owner only - do not touch unless asked |
| `develop` | ❌ Blocked | ✅ Yes | All development happens here |
| `feature/*` | ✅ Allowed | No | Create PR to merge into develop |

### Quick PR (Recommended)

```bash
# Make changes, then run:
./scripts/auto-pr.sh "feat: add new award support"

# This will:
# 1. Create branch: feature/add-new-award-support-{timestamp}
# 2. Commit changes
# 3. Push branch
# 4. Create PR to develop
# 5. Auto-merge if no conflicts
```

### Manual PR Flow

1. Fork the repo
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request → **target: develop**

### Code Quality

- **DRY**: Minimal code, no unnecessary complexity
- **Readable**: Smaller version preferred over clever solutions
- **Config-driven**: All patterns in `src/config.py`

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Rate limit (429)** | Auto-fallback to 8b-instant, or wait for daily reset |
| **Vectorstore not found** | Run `venv/bin/python3 build_store.py` |
| **Import errors** | Ensure `pip install -r requirements.txt` |
| **Groq API error** | Check `.env` has valid `GROQ_API_KEY` |

---

## 📈 Performance

- **Retrieval**: ~200ms (hybrid search)
- **LLM Response**: ~2-5s (depending on model)
- **Total Latency**: ~3-7s per query

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for fast LLM inference
- [FastEmbed](https://qdrant.github.io/fastembed/) for local embeddings
- [TurboVec](https://github.com/turboprop) for quantized vector storage
- [Gradio](https://gradio.app/) for the chat interface

---


