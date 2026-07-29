# Evaluation Results

## Hard Eval (Current)

### Run 8 (Latest — July 2026)
- Format: 23/25 (92%)
- Content: 22/25 (88% pass)
- Average: 82.5%
- Note: ALL questions used fallback model (llama-3.1-8b-instant) due to Groq rate limits

### Run 7 (Previous — before vectorstore rebuild)
- Format: 25/25 (100%)
- Content: 21/25 (84% pass)
- Average: 85.0%
- Note: Questions 17-25 used fallback model

### Best Score
- 85.0% (Run 7) — with 70b model for Q1-16

### Lowest Scoring Questions
| ID | Score | Issue |
|----|-------|-------|
| H02 | 30% | Hospitality consecutive days — data exists, 8b model can't extract |
| H19 | 52% | Fast Food junior hours — data exists, 8b model can't extract |
| H16 | 54% | Overtime part-time — partial retrieval |

### Root Cause
Rate limits from Groq daily TPD. All questions fell back to weak 8b model.
Need to re-run after rate limit reset (~00:00 UTC) for 70b model.

## Accuracy Progression
| Run | Score | Model | Notes |
|-----|-------|-------|-------|
| 1 | 87.5% | 70b | Original baseline |
| 2 | 73.5% | 70b | Filtered build (23,586 docs) |
| 3 | 81.9% | 70b | Fuzzy threshold fix |
| 4 | 85.0% | 70b | Parser + retriever fixes |
| 5 | 78.9% | mixed | Rebuilt vectorstore (31,134 docs) |
| 6 | 82.5% | fallback | Intent-aware retriever |

## Basic Eval
- Format: 12/12 (100%)
- Content: ~89%

## Related
- [[Project Overview]] — System design
- [[Hard Eval Suite]] — 25 questions
- [[Evaluation Questions]] — Basic eval
