# Optimization Guide

## Rate Limit Strategies

### Groq Limits
- `llama-3.3-70b-versatile`: 100k TPD (tokens per day)
- `llama-3.1-8b-instant`: 6k TPM (tokens per minute), higher TPD

### Workarounds (Implemented)
1. **Auto-fallback**: `ask_question()` auto-switches to 8b-instant on 429
2. **Context optimization**: k=10, 800 chars/doc, max_chars=4000
3. **Delays**: 1s between API calls for TPM limits
4. **Wait for reset**: Daily reset ~05:00 AM PKT

## Context Optimization

| Parameter | Default | Optimized | Token Impact |
|-----------|---------|-----------|--------------|
| k (retriever) | 20 | 10 | ~2k → ~1k tokens |
| max_tokens | 1024 | 1024 | Full responses |
| doc truncation | None | 800 chars | More context per doc |
| max_chars | 2000 | 4000 | More documents |

## Retrieval Optimization

### Award Mapping
- 40+ award patterns for precise filtering
- Synonyms: cleaner, hotel, payroll, software engineer, etc.
- Covers all major Awards

### Topic Keywords
- 20+ topics for general questions
- Weighted scoring: phrase match (5pts) > keyword (1pts)
- Bonus for clause numbers and specific values

### General Topic Retrieval
- Exact phrase match = 5 points
- Single keyword match = 1 point
- Clause number presence = 2 bonus points
- Percentage/number in content = 1 bonus points

## Model Selection
- **70b-versatile**: Higher quality, slower, 100k TPD
- **8b-instant**: Lower quality, faster, higher limits
- Use 70b for production, 8b for eval/testing during rate limits

## Evaluation Scoring
- **Keywords**: 40 points (exact + synonym matching)
- **Pattern**: 30 points (regex for specific values)
- **Quality**: 30 points (completeness, specificity)
- **Pass threshold**: 70% per question, 95% overall
