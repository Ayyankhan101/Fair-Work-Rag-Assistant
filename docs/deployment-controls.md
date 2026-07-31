# Deployment Controls

## Authentication
- API keys stored in `.env` (gitignored)
- No secrets in code or config files
- GROQ_API_KEY required for LLM calls

## Privacy
- No user data persisted beyond session
- Questions/answers logged for audit (provenance_log.jsonl)
- No PII in logs (questions truncated to 500 chars)

## Data Retention
- Eval results retained for comparison
- Provenance logs retained for audit
- No automatic deletion policy (manual review)

## Residency
- Data stored locally (no cloud sync)
- Groq API calls subject to Groq's data policy
- No cross-border data transfer configured

## Provider Training-Use
- Groq API: No training on API inputs by default
- No opt-out required for default configuration

## CORS
- Gradio serves on 0.0.0.0:7860
- No CORS restrictions configured (local use only)

## Rate Limiting
- Groq free tier: 30 RPM, 13K tokens/min
- Fallback to 8b-instant on 429 errors
- Circuit breaker after 3 consecutive failures
