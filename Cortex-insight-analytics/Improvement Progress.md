# Improvement Progress

## Phase 1: Prompt Optimization ✅
- 3 few-shot examples
- Number extraction rules
- 119 award mappings, 20+ topics
- Result: 83.7% → 86.0%

## Phase 2: Retrieval Improvements ✅
- Hybrid BM25 + Semantic
- Award-specific filtered retrieval
- General topic retrieval
- Result: Retrieval working

## Phase 3: Eval Suite ✅
- 25 questions with content scoring
- Synonym matching
- Flexible patterns
- Result: 100% pass rate

## Phase 4: Vectorstore Rebuild ✅
- Full rebuild with 130 PDFs + NES
- Markdown-first ingestion (PDF→MD→Vectorstore)
- Table extraction in PDF→MD conversion
- Result: 31,134 docs (up from 23,586)

## Phase 5: Parser & Retriever Fixes ✅ (July 2026)
- Fixed markdown parser: full-clause headers now split into title+body
- Fixed clause number extraction: sub-clauses (15.1, 13.5) now tracked
- Added query intent detection (rate vs clause vs rostering)
- Dynamic scoring: clause queries penalize rate tables
- Direct query term matching (bypasses topic dependency)
- Result: 78.9% → 82.5% (on fallback model)

## Accuracy Progression
| Date | Version | Score | Notes |
|------|---------|-------|-------|
| Jul 2026 | Original | 87.5% | No tables in vectorstore |
| Jul 2026 | Filtered build | 73.5% | 23,586 docs |
| Jul 2026 | Fuzzy fix | 81.9% | 0.7→0.9 threshold |
| Jul 2026 | Parser fix | 85.0% | Topic+reranker+smart fallback |
| Jul 2026 | Rebuild+retriever | 82.5% | 31,134 docs (all on fallback model) |

## Related
- [[Project Overview]] — System design
- [[Evaluation Results]] — Scores
- [[Next Steps]] — What's next
