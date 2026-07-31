# Quality Improvement Plan — Current Status

## Current State
- **Accuracy**: 87.5% (22/25 hard questions pass content-based scoring)
- **Tests**: 67 passing (config, router, CAG, prompt safety, parser regression, adversarial)
- **Lint**: 0 errors (ruff)
- **Defects**: 70 tracked — 48 fixed, 14 partially fixed, 5 not fixed, 3 needs external

## Resolved Items

### Slug Mapping (DEF-003)
- MA000002 correctly mapped to Clerks—Private Sector Award 2010
- All 122+ Award aliases expanded in `src/config.py` AWARD_PATTERNS (233 entries)

### Retrieval (DEF-066)
- Hybrid search: BM25 + Semantic with RRF fusion
- Filtered retriever with fuzzy matching (threshold 0.85)
- Topic-aware scoring with clause/rate table detection

### Prompt Safety (DEF-033)
- System prompt enforces: no fabrication, insufficient evidence handling, clause references
- Structured 5-component output format

### Infrastructure
- Lazy app initialization (DEF-024)
- Content-hash deduplication (DEF-009)
- Cache hash verification (DEF-011)
- Pinned dependencies (DEF-012)
- UTF-8 encoding across all file reads (DEF-014)
- Structured claims parser (DEF-034)
- Circuit breaker for provider (DEF-043)
- Provider abstraction boundary (DEF-046)

## Remaining Work

### Needs External Verification
- **DEF-010**: Eval rerun required against current store (needs Groq API key)
- **DEF-021**: CRLF verification requires Linux environment
- **DEF-069**: Award case matching requires live rerun

### Deferred (Manual Review)
- **DEF-026/027**: PDF/DOCX visual inspection (requires LibreOffice)
- **DEF-034**: Full structured claims validation needs LLM output testing
- **DEF-046**: Provider abstraction tested structurally, needs integration test

## Success Criteria
- **Format**: 12/12 pass (5-component structure verified)
- **Accuracy**: 87.5% (22/25) — target >97% requires eval rerun after store rebuild
- **Tests**: 67 unit tests covering config, router, CAG, prompt safety, parser, adversarial
- **Lint**: Clean (0 errors)
