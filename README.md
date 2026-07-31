# Fair Work Unfair Dismissal RAG Assistant

> RAG-powered LLM assistant for Australian unfair dismissal law — FWC decisions + Fair Work Act 2009 (s385-394)

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LLM-Groq](https://img.shields.io/badge/LLM-Groq_Llama_3.3-70B-blue.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Architecture

```
User Query
    ↓
┌─────────────────┐
│   Query Router   │  Classifies: jurisdictional / statutory_criteria / analogous_facts / procedural
└────────┬────────┘
         ↓
┌─────────────────┐
│  CAG / RAG Path  │
├─────────────────┤
│ CAG: Fair Work   │  Legislation context (s385-394) for definition/jurisdiction questions
│ RAG: FWC Decisions│  Hybrid search (BM25 + Semantic) for case law
└────────┬────────┘
         ↓
┌─────────────────┐
│   LLM Generate   │  Groq llama-3.3-70b-versatile
└────────┬────────┘
         ↓
┌─────────────────┐
│  Post-Hoc Verify  │  Citations validated against source
├─────────────────┤
│  Citation Resolve │  Regex extract + corpus validation
├─────────────────┤
│  Abstention Gate  │  4-rule check: if uncertain, abstain
└────────┬────────┘
         ↓
┌─────────────────┐
│   5-Part Output   │  Answer + Legislation Reference + Section + Explanation + Note
└─────────────────┘
```

---

## Quick Start

### Prerequisites

- Python 3.12+
- Groq API key ([Get one here](https://console.groq.com/))

### Installation

```bash
git clone https://github.com/Ayyankhan101/fair-work-rag-assistant.git
cd fair-work-rag-assistant
git checkout develop

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Run the App

```bash
python src/app.py
# Open http://localhost:7860
```

### Run Evaluation

```bash
python scripts/eval_unfair_dismissal.py
```

---

## Project Structure

```
fair-work-rag-assistant/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment template
│
├── src/                               # Core application code
│   ├── config.py                      # FWC provisions, query categories, thresholds
│   ├── rag.py                         # Full pipeline: classify → generate → verify → abstain
│   ├── cag.py                         # CAG context cache (Fair Work Act s385-394)
│   ├── router.py                      # Query classifier (4 types)
│   ├── filtered_retriever.py          # UnfairDismissalRetriever (metadata filtering)
│   ├── hybrid_retriever.py            # BM25 + Semantic with RRF
│   ├── bm25_retriever.py              # BM25 retriever
│   ├── vectorstore.py                 # TurboVec build/load/search
│   ├── fastembeddings.py              # LangChain wrapper for fastembed
│   ├── ingest.py                      # FWC decisions + legislation ingestion
│   ├── verifier.py                    # Post-hoc citation verifier
│   ├── citation_resolver.py           # Regex extract + corpus validation
│   ├── abstention_gate.py             # 4-rule abstention check
│   ├── audit_log.py                   # Full audit trail
│   ├── corpus_manager.py              # Point-in-time corpus management
│   ├── reranker.py                    # Cohere reranker + keyword fallback
│   └── app.py                         # Gradio chat interface
│
├── scripts/
│   ├── eval_unfair_dismissal.py       # 8 golden-set evaluation questions
│   └── download_fwc_decisions.py      # FWC scraper (blocked by bot protection)
│
├── data/
│   ├── legislation/
│   │   └── fair_work_act_s385_394.txt # Fair Work Act provisions
│   ├── fwc_decisions/                 # FWC decisions (user downloads manually)
│   └── vectorstore/                   # TurboVec index (built from decisions)
│
├── skills/fair-work-rag/              # Project skill
│   ├── SKILL.md
│   └── references/
│       ├── architecture.md
│       ├── optimization.md
│       └── troubleshooting.md
│
└── .opencode/                         # Mission context
    ├── context.md
    ├── todo.md
    └── work-log.md
```

---

## Key Components

### Query Router

Classifies queries into 4 types:

| Type | Description | Example |
|------|-------------|---------|
| **jurisdictional** | Threshold questions (can FWC hear?) | "What is an unfair dismissal?" |
| **statutory_criteria** | Application of s387 factors | "What criteria does FWC consider?" |
| **analogous_facts** | Similar case outcomes | "What happened in cases like mine?" |
| **procedural** | Application process | "How do I apply?" |

### CAG (Cache-Augmented Generation)

Pre-loaded Fair Work Act s385-394 context for:
- Definition of unfair dismissal (s385)
- Meaning of dismissed (s386)
- Criteria for unfairness (s387)
- Summary dismissal (s388)
- Minimum employment period (s389)
- Remedies (s390-394)

### Post-Hoc Verification

1. **Citation Extractor** — Regex finds section references (e.g., "s385")
2. **Corpus Validator** — Checks citations exist in source documents
3. **Abstention Gate** — 4-rule check:
   - Too few citations → abstain
   - Low confidence → abstain
   - Conflicting citations → abstain
   - Unverified citations → abstain

---

## Evaluation

### Golden Set (8 Questions)

| Question | Expected Section | Category |
|----------|-----------------|----------|
| What is an unfair dismissal? | s385 | jurisdictional |
| How long to apply? | s394 | jurisdictional |
| Minimum employment period? | s389 | jurisdictional |
| High income threshold? | s391/s392 | jurisdictional |
| FWC criteria? | s387 | statutory_criteria |
| Compensation instead of reinstatement? | s391 | statutory_criteria |
| How is compensation calculated? | s392 | statutory_criteria |
| What is summary dismissal? | s388 | procedural |

### Current Results

| Metric | Value |
|--------|-------|
| Section Accuracy | 100% |
| Answer Accuracy | 87.5% |
| Abstention Rate | 0% |
| Avg Latency | ~7.6s |

---

## Configuration

### Key Parameters (`src/config.py`)

| Parameter | Value | Description |
|-----------|-------|-------------|
| `K_HYBRID` | 10 | Hybrid retrieval results |
| `K_FILTERED` | 20 | Filtered retrieval results |
| `MAX_TOKENS` | 1024 | LLM max output tokens |
| `CONFIDENCE_THRESHOLD` | 0.6 | Minimum confidence to answer |

### Model Configuration

```python
# Primary model (production)
model = "llama-3.3-70b-versatile"

# Fallback model (rate limit)
model = "llama-3.1-8b-instant"
```

---

## Data Sources

| Source | Status | Description |
|--------|--------|-------------|
| **Fair Work Act s385-394** | ✅ Ingested | Legislation text (13 chunks) |
| **FWC Decisions** | ⏳ Pending | User must download manually |
| **AustLII** | ⛔ Blocked | Do Not List - never use |

### FWC Decisions Download

FWC website blocks automated access. User must manually download:

1. Go to https://www.fwc.gov.au/document-search?search-ui=decisions
2. Search: "unfair dismissal"
3. Type: Decisions
4. Date: 01/01/2023 - 31/07/2026
5. Save .txt files to `data/fwc_decisions/`

---

## Branch Rules

| Branch | Direct Push | PR Required | Notes |
|--------|-------------|-------------|-------|
| `main` | ❌ **NEVER** | ❌ | Owner only |
| `develop` | ❌ Blocked | ✅ Yes | All development |
| `feature/*` | ✅ Allowed | No | PR to develop |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Rate limit (429) | Auto-fallback to 8b-instant, or wait for daily reset |
| Vectorstore not found | Run `python build_store.py` |
| Import errors | Ensure `pip install -r requirements.txt` |
| Groq API error | Check `.env` has valid `GROQ_API_KEY` |

---

## Performance

- **Retrieval**: ~200ms (hybrid search)
- **LLM Response**: ~2-5s (depending on model)
- **Total Latency**: ~3-7s per query

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- [Groq](https://groq.com/) for fast LLM inference
- [FastEmbed](https://qdrant.github.io/fastembed/) for local embeddings
- [TurboVec](https://github.com/turboprop) for quantized vector storage
- [Gradio](https://gradio.app/) for the chat interface
