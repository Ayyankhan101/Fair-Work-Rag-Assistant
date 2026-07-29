# Next Steps

## Immediate
1. **Re-run eval after rate limit reset** — need 70b model for accurate scoring
2. **Rebuild vectorstore with clause_number fix** — sub-clauses (15.1, 13.5) now tracked
3. **Target 95% accuracy** — with 70b model + improved retrieval

## After 95%
1. **Deploy to production** — Gradio UI + API
2. **Real query testing** — user acceptance
3. **Streaming responses** — faster UX

## Future
1. **LLM-based intent classification** — replace rule-based intent detection
2. **Semantic cache** — cache common Q&A pairs
3. **Faithfulness check** — verify LLM answers match retrieved context
4. **Conversation memory** — multi-turn support
5. **Anthropic API key** — switch to Claude for better accuracy

## Related
- [[Project Overview]] — System design
- [[Improvement Progress]] — What's done
- [[Evaluation Results]] — Scores
