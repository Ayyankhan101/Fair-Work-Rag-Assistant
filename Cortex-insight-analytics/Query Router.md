# Query Router

## Purpose
Classifies questions as CAG, RAG, or Combined for optimal retrieval.

## Classification Logic
1. NES keywords → CAG or Combined
2. Award keywords → RAG or Combined
3. Topic keywords → RAG with filtered retrieval
4. Default → Hybrid RAG

## Decision Tree
```
Question
  ↓
NES keywords? → CAG or Combined
  ↓
Award keywords? → RAG or Combined
  ↓
Topic keywords? → RAG with filtered retrieval
  ↓
Default → Hybrid RAG
```

## Usage
```python
from router import classify_query
result = classify_query("What leave entitlements under Hospitality Award?")
# → Combined (NES + Award)
```

## Related
- [[Project Overview]] — System design
- [[CAG Context Cache]] — NES caching
- [[Filtered Retriever]] — Award search
