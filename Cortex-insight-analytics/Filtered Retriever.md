# Filtered Retriever

## Purpose
Award-specific retrieval with intent-aware scoring for precise document retrieval.

## How It Works
1. Award detection (119 patterns + fuzzy 0.9 threshold)
2. Topic detection (20+ topics with keyword values)
3. Query term extraction (direct content matching)
4. Intent detection (rate vs clause vs rostering)
5. Dynamic scoring based on query intent
6. General topic retrieval for non-specific questions

## Detection Pipeline
- **Award**: `AWARD_PATTERNS` dict in `src/config.py` (119 entries)
- **Topic**: `TOPIC_KEYWORDS` dict (20 topics, each with keyword values)
- **Query terms**: Stop-word filtered nouns/phrases from query
- **Intent**: `_is_rate_query()`, `_is_clause_query()`, `_is_rostering_query()`

## Dynamic Scoring

### Rate Queries (pay/salary/rate)
- Rate table bonus: +5 (dollar), +3 (level), +3 (table), +10 (dollar+level)
- "minimum hourly rate" phrase: +5

### Clause Queries (hours/rostering/rules)
- Rate table penalty: -3 (table), -5 (dollar+level)
- Operational content bonus: +5 (must not, must roster, maximum number, etc.)
- Rostering content bonus: +5 (roster, consecutive, days off, etc.)

### Direct Term Matching
- Each query term in content: +3
- Bypasses topic keyword dependency for queries like "consecutive days"

## Configuration
- `k=30` for filtered retriever
- `k=10` for hybrid retriever
- Fuzzy threshold: 0.9 (high to avoid false positives)

## Recent Fixes (July 2026)
- Query intent detection (rate vs clause vs rostering)
- Dynamic scoring to prevent rate tables overpowering clause docs
- Direct query term matching for queries without topic keywords
- Full-clause header parsing in `ingest_markdown.py`
- Clause number extraction for sub-clauses (15.1, 13.5)

## Related
- [[Project Overview]] — System design
- [[Vector Store]] — Index details
- [[Query Router]] — Classification
