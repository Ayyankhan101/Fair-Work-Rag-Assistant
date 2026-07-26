# Troubleshooting

## Rate Limit Errors (429)
```
groq.RateLimitError: Rate limit reached for model `llama-3.3-70b-versatile`... TPD: Limit 100000
```
**Fix**: Auto-fallback implemented — `ask_question()` auto-switches to 8b-instant on 429.

## Import Errors
```
ModuleNotFoundError: No module named 'fastembed'
```
**Fix**: Use venv python: `venv/bin/python3 script.py`

## Vector Store Missing
```
Vector store missing. Build first.
```
**Fix**: Run `venv/bin/python3 build_store.py`

## Missing Note Field
```
format_failures: ['missing **Note:**']
```
**Fix**: Prompt includes mandatory Note field instruction with 3 options.

## Retrieval Quality Issues
- Wrong Award returned → Check filtered retriever award detection (40+ patterns)
- Missing clauses → Increase k parameter (currently 10)
- Generic answers → Improved prompt with specific extraction instructions

## Build Issues
```
Build timeout / interrupted
```
**Fix**: Build is resumable — run `venv/bin/python3 build_store.py` again.

## Content Accuracy Issues
- Low keyword score → Check award mappings in `rag.py`
- Low pattern score → Check expected patterns in `eval_hard.py`
- Low quality score → Improve prompt specificity

## Common Fixes

### Restart Build
```bash
# Clear cache and rebuild
rm data/docs_cache.pkl
venv/bin/python3 build_store.py
```

### Run Eval
```bash
# Basic eval (12 questions)
venv/bin/python3 scripts/eval_prd_questions.py

# Hard eval (25 questions with scoring)
venv/bin/python3 scripts/eval_hard.py
```

### Check Vectorstore
```bash
# Check if index exists
ls -la data/vectorstore/

# Check checkpoint
cat data/vectorstore/build_checkpoint.json
```

## Related
- [[Architecture]] — System design
- [[Optimization]] — Performance tuning
