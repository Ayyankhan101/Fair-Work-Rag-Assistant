# Model and architecture decision record

## Status

Proposed evaluation decision. No production model or architecture change is approved.

## Decision

Do not select a model by reputation, parameter count, provider benchmark, or price.

First fix the corpus and evidence pipeline. Then compare a controlled set of model and retrieval candidates using the hidden, claim-level evaluation system.

An operational replacement for the current Groq models must be qualified before 16 August 2026.

## Reasons

- Both configured Groq model IDs have an announced developer-tier shutdown date.
- The current source store is incomplete and mislabelled.
- The historical 25-question score cannot distinguish retrieval from generation failure.
- No current result records model, prompt, corpus, or commit identity.
- A stronger model cannot recover a missing or truncated legal clause safely.
- Model changes alter accuracy, refusal, structure, injection behavior, latency, and cost.

## Evaluation criteria

| Criterion | Weight | Hard gate |
|---|---:|---|
| claim correctness | 25% | yes |
| claim support and citation | 20% | yes |
| high-impact numeric accuracy | 15% | yes |
| clarification, refusal, and safety | 15% | yes |
| retrieval quality | 10% | yes for architecture |
| cost per successful grounded answer | 5% | no |
| latency and throughput | 5% | approved limit |
| privacy, continuity, and operability | 5% | yes |

Weights rank candidates only after every hard gate passes.

## Candidate set

### Generators

- current committed Groq Llama 3.3 70B as a temporary comparison baseline;
- Groq GPT-OSS 20B;
- Groq GPT-OSS 120B;
- Groq Qwen 3.6 27B if production access and price are confirmed;
- OpenAI GPT-5.6 Luna;
- OpenAI GPT-5.6 Terra;
- OpenAI GPT-5.6 Sol as a quality-ceiling comparison, not an assumed default.

### Retrieval

- current BGE-base dense plus BM25 and reciprocal-rank fusion;
- current retrieval plus BGE reranker v2 M3;
- BGE-M3 dense;
- BGE-M3 dense plus sparse;
- BGE-M3 plus BGE reranker;
- best local retrieval plus Cohere Rerank 4 Fast;
- best local retrieval plus Cohere Rerank 4 Pro.

### Prompt

- committed prompt;
- dirty working-tree prompt;
- `FWRA-SYS-002-draft`;
- any shorter candidate derived after failure analysis.

The committed prompt is included only to measure the baseline. It is not a safe release candidate.

## Experiment design

### Stage A: retrieval only

Use the same accepted corpus and gold clauses. Compare retrieval candidates without an LLM answer.

Promote configurations that meet recall, contamination, latency, memory, and reproducibility gates.

### Stage B: fixed-context generation

Give every model the exact same reviewed evidence. This isolates generation, claim use, structure, and safety from retrieval.

### Stage C: full pipeline

Combine only the best retrieval and generator candidates. Measure end-to-end quality, latency, tokens, cost, and failure recovery.

### Stage D: cascade

Test a cheap default with escalation when:

- query ambiguity is high;
- evidence conflict exists;
- structured output fails;
- a claim verifier rejects output;
- the case is in a high-impact class.

The cascade passes only if it improves cost without lowering a hard gate.

## Required records

Each run records:

- candidate commit and dirty-state rejection;
- source manifest and index hashes;
- prompt ID and hash;
- provider, exact model ID, revision, parameters, and fingerprint;
- random seed where available;
- retrieved and reranked evidence;
- raw model response;
- schema and claim validation;
- reviewer decisions;
- input, cached, reasoning, and output tokens;
- latency, retries, and price snapshot;
- calculated cost per passed and grounded answer.

## Selection rule

Select the cheapest candidate whose lower confidence bound passes every approved threshold.

If several candidates are statistically indistinguishable, select the one with:

1. lower operational and privacy risk;
2. stable production support;
3. lower cost;
4. lower latency;
5. simpler recovery and observability.

## Rejected shortcuts

- switching directly to the provider-recommended replacement;
- using the largest model everywhere;
- using a small model because a 25-question suite passes;
- fine-tuning current legal facts into model weights;
- asking one LLM to grade itself;
- measuring format as accuracy;
- comparing models on different retrieved contexts;
- ignoring refusals, timeouts, or schema failures;
- choosing by average score while a high-impact case fails.

## Current disposition

No model is selected.

The immediate continuity candidates are Groq GPT-OSS 20B and 120B because they are production models named in Groq’s current migration guidance and support strict structured output. They still require the full prompt, claim, safety, cost, and latency evaluation.
