# Quick glance: architecture and risks

## Current flow

```text
question
  -> deterministic route
  -> full NES cache, Award retrieval, or both
  -> BM25 plus BGE dense retrieval
  -> four-bit TurboVec results
  -> one human-role prompt
  -> Groq model
  -> free-form five-field answer
```

## Main failure points

| Stage | Risk |
|---|---|
| source | missing, stale, mislabelled, and unreproducible content |
| parsing | lost tables, footnotes, pages, dates, and qualifications |
| routing | incomplete aliases and forced Award selection |
| retrieval | no reranker, duplicates, truncated context |
| prompt | no system-role boundary or structured claim contract |
| generation | model can produce unsupported legal-looking text |
| validation | no deterministic citation or claim verification |
| operations | deprecated models, no privacy or recovery evidence |

## Target flow

```text
accepted versioned sources
  -> clause and table-aware parsing
  -> structured query and ambiguity gate
  -> Award/date filter
  -> hybrid retrieval
  -> reranking and parent-clause expansion
  -> system-role evidence-only prompt
  -> strict claim schema
  -> deterministic checks
  -> claim verifier
  -> user rendering and trace
```

Full design: `accuracy-improvement-research.md` and `proposed-system-and-user-prompt.md`.
