# Quick glance: accuracy roadmap

## Priority order

1. Repair and version the source corpus.
2. Preserve clauses, tables, footnotes, and effective dates.
3. Add query fields and a clarification state.
4. Filter by Award and date before semantic ranking.
5. compare hybrid retrieval candidates.
6. Add and benchmark a reranker.
7. reduce duplicate and irrelevant context.
8. separate system rules from user and source data.
9. generate atomic claims with strict citations.
10. reject unsupported claims.
11. compare models blindly.
12. optimize cost only after hard accuracy gates pass.

## Model continuity

Qualify a replacement for both configured Groq models before 16 August 2026.

Immediate candidates:

- Groq GPT-OSS 20B;
- Groq GPT-OSS 120B;
- Groq Qwen 3.6 27B after availability and price confirmation.

Quality-ceiling comparisons:

- OpenAI GPT-5.6 Luna;
- OpenAI GPT-5.6 Terra;
- OpenAI GPT-5.6 Sol.

No candidate is approved yet.

Full research: `accuracy-improvement-research.md` and `model-and-architecture-decision-record.md`.
