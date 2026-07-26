# RAG Chain

## Purpose
LLM-powered Q&A using Groq with prompt engineering for employment law.

## Key Features
- 3 few-shot examples (specific Award, general topic, NES)
- Number extraction rules (never say "not specified")
- Auto-fallback on rate limits (70b → 8b)

## Files
- `src/rag.py` — Chain + prompt template
- `src/fastembeddings.py` — ONNX embeddings

## Prompt Structure
```
1. CRITICAL RULES (10 rules for extraction)
2. RESPONSE FORMAT (5 sections)
3. EXAMPLES (3 few-shot)
4. CONTEXT (retrieved docs)
```

## Related
- [[Project Overview]] — System design
- [[Filtered Retriever]] — Retrieval
- [[CAG Context Cache]] — NES handling
- [[Rate Limit Status]] — Rate limits
