# Architecture Decision

## Why Hybrid CAG+RAG?
- **CAG for NES**: Pre-load text, instant, 100% recall
- **RAG for Awards**: Vector search, flexible, handles 130+ Awards
- **Router**: Classifies questions, routes to optimal path

## Why TurboVec?
- Fast, quantized (4-bit), LangChain integration
- Resumable builds with checkpoint

## Why Groq?
- Fast, cheap, good quality
- Auto-fallback on rate limits

## Why fastembed?
- ONNX runtime (no torch dependency)
- Local inference (no API costs)
- 768-dim embeddings (BAAI/bge-base-en-v1.5)

## Related
- [[Project Overview]] — System design
- [[Vector Store]] — Index details
- [[CAG Context Cache]] — NES caching
