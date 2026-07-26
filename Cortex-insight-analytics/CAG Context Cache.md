# CAG Context Cache

## Purpose
Pre-loads NES text for instant, 100% recall on NES-specific questions.

## How It Works
1. NES text: `data/nes/nes_combined.txt` (~28,924 chars)
2. CAG candidate detection (NES keywords)
3. Context pre-loading (no retrieval needed)

## Usage
```python
from cag import CAGCache
cache = CAGCache("data/nes/nes_combined.txt")
if cache.is_cag_candidate("What leave entitlements?"):
    context = cache.get_context("What leave entitlements?")
```

## Benefits
- Speed: No retrieval
- Accuracy: 100% recall for NES
- Reliability: No vector search failures

## Related
- [[Project Overview]] — System design
- [[Query Router]] — Classification
- [[RAG Chain]] — LLM chain
