# Rate Limit Status

## Groq Rate Limits
- **Model**: `llama-3.3-70b-versatile`
- **Limit**: ~30 requests/min
- **Impact**: Eval runs hit limits frequently

## Fallback Chain
1. Try `llama-3.3-70b-versatile`
2. On 429 → fallback to `llama-3.1-8b-instant`
3. Auto-retry with smaller context

## Mitigation
- `get_llm(fallback=True)` for auto-fallback
- `ask_question()` catches 429 and retries
- Eval scripts handle rate limits gracefully

## Related
- [[Project Overview]] — System design
- [[RAG Chain]] — LLM chain
