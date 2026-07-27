# API and model-provider assurance report

Date: 27 July 2026

Decision: no provider or model is approved

Immediate recommendation: use direct Groq `openai/gpt-oss-120b` as the lowest-change continuity candidate, then compare it against paid Gemini 3.6 Flash and direct OpenAI GPT-5.6 Luna or Terra on the same frozen evidence set. Use OpenRouter as a controlled QA transport only when the provider route is pinned.

This is a recommendation for testing. It is not permission to change the application.

## Why the current API path fails assurance

The application is tied directly to `ChatGroq`. Provider selection, model IDs, token limit, and failover behavior are embedded in `src/rag.py`.

| Control | Current state | Result |
|---|---|---|
| Provider abstraction | none | fail |
| Model configuration outside source | none | fail |
| Explicit request timeout | none | fail |
| Retry policy | client default of two | incomplete |
| Backoff and jitter evidence | not configured or tested | fail |
| Circuit breaker | none | fail |
| Structured JSON schema | none | fail |
| Semantic claim validator | none | fail |
| Token and cost record | none | fail |
| Provider request ID record | none | fail |
| Model and prompt version record | none | fail |
| Data-retention control | not configured | fail |
| Live provider tests | none in this phase | blocked |

The fallback path checks exception text for `429`, `rate_limit`, or `413`. A 413 means the request is too large. Retrying it with another model while keeping the same context builder does not correct the request size. The log says the retry uses a smaller context, but the code reuses the original context builder.

An offline 429 probe confirmed an additional defect. The fallback rendered one `HumanMessage`, placed the original `context` and `question` mapping inside a nested context dictionary, and repeated the user question twice. It did not create a smaller context. No provider request was used for this probe.

The fallback also changes from a 70B model to an 8B model without a quality gate, user-visible degradation state, or claim validation. Both configured IDs are scheduled to shut down on 16 August 2026 for Groq free and developer tiers.

## Provider comparison

Prices are published list prices observed on 27 July 2026. They can change. Quality rankings must come from this project's blind evaluation, not provider marketing or generic benchmarks.

| Lane | Candidate | Published input/output per 1M tokens | Useful properties | Main QA risk |
|---|---|---:|---|---|
| Groq direct | `openai/gpt-oss-120b` | $0.15 / $0.60 | production model, about 500 tokens/second, strict JSON schema | new prompt behavior still unqualified |
| Groq direct | `openai/gpt-oss-20b` | $0.075 / $0.30 | very low cost, about 1,000 tokens/second, strict JSON schema | likely quality loss on legal nuance |
| Gemini direct, paid | `gemini-3.6-flash` | $1.50 / $7.50 | stable model, structured output, batch at half price | semantic accuracy still needs validation |
| Gemini direct, paid | `gemini-3.5-flash-lite` | $0.30 / $2.50 | low-cost stable baseline, batch at half price | not a justified primary legal-answer model |
| OpenAI direct | `gpt-5.6-luna` | $1.00 / $6.00 | current cost-sensitive model, structured outputs | materially dearer than Groq |
| OpenAI direct | `gpt-5.6-terra` | $2.50 / $15.00 | quality/cost comparison lane, structured outputs | higher evaluation and production cost |
| OpenRouter | pinned model and provider | underlying price plus account fees | one API for cross-provider experiments, detailed usage records | default routing harms repeatability |

Groq's strict structured-output mode is currently documented for GPT-OSS 20B and 120B. Schema adherence does not prove that a rate, date, Award, clause, or legal explanation is correct. The deterministic claim validator remains mandatory.

Gemini structured output also guarantees format rather than semantic correctness. Google's documentation explicitly requires application validation.

## OpenRouter finding

OpenRouter is suitable for a QA model matrix, but its defaults are unsuitable for a reproducible acceptance test.

By default, OpenRouter can load-balance across providers and use fallbacks. Different providers for the same model may support different parameters, quantization, latency, retention rules, or schema enforcement. That creates an uncontrolled experimental variable.

Every acceptance request through OpenRouter should set or enforce:

```text
exact model ID
provider.only = [approved provider]
provider.allow_fallbacks = false
provider.require_parameters = true
provider.data_collection = deny
provider.zdr = true
response_format = strict JSON schema
stream = false
temperature = approved fixed value
maximum output tokens = approved fixed value
```

Record:

```text
run ID
test ID
model ID
canonical model slug when available
provider name
generation and request IDs
input and output token counts
reasoning and cached token counts
cost
latency and generation time
finish reason
schema-validation result
claim-validation result
retry and fallback count
```

If the privacy and provider constraints leave no matching route, the test must fail closed. Removing the constraints to obtain an answer would invalidate the run.

OpenRouter should not be the only production route until legal, privacy, retention, residency, procurement, incident-response, and provider-substitution controls are accepted.

## Gemini finding

Gemini is a valid comparison API, but the free tier is not appropriate for real user questions, confidential evaluation data, or personal employment records.

Google's current terms say unpaid-service prompts and responses may be used to improve products and may be reviewed by humans. Paid-service content is not used to improve Google's products, although limited logging and other processing still apply under the terms.

For this project:

- paid Gemini may be used for approved synthetic and public-source evaluation;
- free Gemini may be used only for non-confidential smoke cases after the owner accepts the terms;
- no real user logs, names, pay records, health information, dispute records, or confidential gold answers may be submitted;
- Google Search grounding should remain off during corpus-only QA because it changes the evidence boundary and has separate retention behavior;
- the exact stable model ID must be recorded; `latest`, preview, and experimental aliases are not acceptance-test baselines.

Gemini 3.6 Flash is the quality comparison candidate. Gemini 3.5 Flash-Lite is a cost baseline, not a presumed production answer model.

## OpenAI finding

OpenAI's current model guide positions GPT-5.6 Luna for cost-sensitive workloads and Terra for a balance of quality and cost. Both support structured outputs.

For this application:

- Luna is the appropriate lower-cost direct comparison;
- Terra is the quality/cost comparison;
- Sol is an optional ceiling test, not the first production choice;
- reasoning effort must be fixed and recorded;
- the same prompt, context, schema, cases, repetitions, and validators must be used for every candidate.

No direct OpenAI run occurred because no API key or budget was supplied.

## Cost scenario

The table below is a planning calculation, not a bill.

Assumption:

- 1,000 model calls;
- 2,000 input tokens per call;
- 500 output tokens per call;
- no cache discount, batch discount, retries, reasoning-token surcharge, tool charge, tax, or account fee.

This equals 2.0 million input tokens and 0.5 million output tokens.

| Candidate | Estimated cost |
|---|---:|
| Groq `openai/gpt-oss-20b` | $0.30 |
| Groq `openai/gpt-oss-120b` | $0.60 |
| current Groq Llama 3.3 70B | $1.58 |
| Gemini 3.5 Flash-Lite standard | $1.85 |
| Gemini 3.5 Flash-Lite batch | $0.93 |
| OpenAI GPT-5.6 Luna | $5.00 |
| Gemini 3.6 Flash standard | $6.75 |
| Gemini 3.6 Flash batch | $3.38 |
| OpenAI GPT-5.6 Terra | $12.50 |
| OpenAI GPT-5.6 Sol | $25.00 |

Actual cost must be calculated from provider-returned usage fields. Current application code does not retain those fields.

## Controlled provider test plan

### Stage A: transport conformance

Run 20 synthetic cases against each adapter.

Check authentication failure, schema enforcement, timeout, cancellation, rate limit, oversized input, malformed response, refusal, token accounting, request IDs, and logging redaction.

Exit: all required metadata is captured and every failure is bounded.

### Stage B: prompt assurance

Run all 120 prompt cases against:

- Groq GPT-OSS 120B;
- paid Gemini 3.6 Flash;
- OpenAI GPT-5.6 Luna or Terra;
- one cheap fallback candidate.

Use at least three repetitions for non-deterministic provider/model combinations. Do not use a model's own answer as the gold label.

Exit: zero unsupported numeric or citation claims, 100% valid schema, and approved clarification and insufficient-evidence behavior.

### Stage C: hidden legal set

Use a frozen held-out set reviewed by an Australian employment-law specialist. Each expected claim must point to an accepted source cell, clause, date, and qualifier.

Exit: the thresholds in `test-strategy.md` pass and no S0 or S1 model defect remains.

### Stage D: cost and reliability

Run fixed concurrency and long-duration tests with the same prompt distribution.

Measure:

- p50, p95, and p99 latency;
- timeout, retry, refusal, and invalid-output rates;
- tokens and cost per accepted answer;
- cost per fully supported claim;
- provider and model substitutions;
- cache effects;
- daily and monthly spend projections.

Exit: the selected pair passes the quality floor and the approved latency and cost ceiling.

## Selection rule

Do not select the model with the highest generic benchmark or the lowest token price.

Select the cheapest provider/model/prompt pair that:

1. passes every hard legal and citation gate;
2. passes the hidden claim-level evaluation;
3. has an accepted privacy and retention path;
4. has stable model identity and deprecation monitoring;
5. has bounded timeout, retry, and fallback behavior;
6. produces complete usage and cost evidence;
7. passes load, recovery, and incident tests.

Until that comparison is executed, the provider decision remains open.

## Sources

- [Groq model deprecations](https://console.groq.com/docs/deprecations)
- [Groq supported models and pricing](https://console.groq.com/docs/models)
- [Groq structured outputs](https://console.groq.com/docs/structured-outputs)
- [Groq error responses](https://console.groq.com/docs/errors)
- [Gemini models](https://ai.google.dev/gemini-api/docs/models)
- [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Gemini structured outputs](https://ai.google.dev/gemini-api/docs/structured-output)
- [Gemini API terms](https://ai.google.dev/gemini-api/terms)
- [Gemini zero-data-retention guidance](https://ai.google.dev/gemini-api/docs/zdr)
- [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection)
- [OpenRouter structured outputs](https://openrouter.ai/docs/guides/features/structured-outputs)
- [OpenRouter provider logging](https://openrouter.ai/docs/guides/privacy/provider-logging/)
- [OpenRouter usage accounting](https://openrouter.ai/docs/cookbook/administration/usage-accounting)
- [OpenRouter pricing and fees](https://openrouter.ai/docs/faq)
- [OpenAI current model catalog](https://developers.openai.com/api/docs/models)
- [OpenAI GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model)
