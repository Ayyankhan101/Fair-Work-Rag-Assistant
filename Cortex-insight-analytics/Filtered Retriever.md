# Filtered Retriever

## Purpose
Award-specific retrieval with topic filtering for precise document retrieval.

## How It Works
1. Award detection (40+ patterns)
2. Topic detection (20+ keywords)
3. Document filtering and scoring
4. General topic retrieval for non-specific questions

## Scoring
- Award-specific: keyword match (1pt) + clause bonus (2pts)
- General topic: phrase (5pts) + keyword (1pts) + clause (2pts) + percentage (1pt)

## Configuration
- `k=20` for filtered retriever
- `k=10` for hybrid retriever

## Related
- [[Project Overview]] — System design
- [[Vector Store]] — Index details
- [[Query Router]] — Classification
