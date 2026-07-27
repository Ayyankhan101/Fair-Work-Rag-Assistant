# Accuracy improvement research

## Conclusion

Changing the language model alone will not make this system reliable.

The largest current accuracy risks are upstream:

1. incomplete and mislabelled sources;
2. no source-version handshake;
3. contaminated NES text;
4. insufficient Award aliases and ambiguity handling;
5. no reranker;
6. context truncation without claim coverage checks;
7. no claim-to-source verifier;
8. an invalid historical evaluation method.

A stronger model can make unsupported output sound more convincing. Corpus, retrieval, and grounding gates must pass before a model comparison is allowed to influence release status.

Research was checked against current first-party documentation and primary papers on 27 July 2026.

## Current architecture

The inspected implementation uses:

- `BAAI/bge-base-en-v1.5` local embeddings;
- a four-bit TurboVec index;
- BM25 and dense retrieval combined with reciprocal-rank fusion;
- deterministic Award and topic filters;
- a full NES cache for NES-labelled questions;
- Groq `llama-3.3-70b-versatile` for primary generation;
- Groq `llama-3.1-8b-instant` as a fallback;
- temperature zero and a 1,024-token answer limit.

This is a useful prototype structure. It is not a controlled legal-information architecture.

## Immediate model continuity risk

Groq’s [deprecation schedule](https://console.groq.com/docs/deprecations) states that both configured model IDs are scheduled to shut down for free and developer tiers on 16 August 2026:

| Current model | Groq replacement guidance |
|---|---|
| `llama-3.1-8b-instant` | `openai/gpt-oss-20b` |
| `llama-3.3-70b-versatile` | `openai/gpt-oss-120b` or `qwen/qwen3.6-27b` |

This is a release blocker, not a future enhancement. The fallback does not provide continuity because it has the same shutdown date.

Groq currently lists `openai/gpt-oss-20b` and `openai/gpt-oss-120b` as production models. Its [structured-output documentation](https://console.groq.com/docs/structured-outputs) lists both as supporting strict JSON-schema output.

## Model candidates

The candidates below are an experiment set, not a recommendation to switch without evidence.

| Candidate | Intended role | Current public token price | Why test it | Main risk |
|---|---|---:|---|---|
| Groq GPT-OSS 20B | routing, query extraction, cheap generation | $0.075 input / $0.30 output per million | low cost, strict structured output, high throughput | may miss difficult legal distinctions |
| Groq GPT-OSS 120B | primary answer or verifier | $0.15 input / $0.60 output per million | Groq replacement for the present 70B model | quality on this corpus is unproved |
| Groq Qwen 3.6 27B | primary answer comparison | obtain quote during experiment | named by Groq as a replacement candidate | availability and price need confirmation |
| OpenAI GPT-5.6 Luna | cost-sensitive answer path | $1 input / $6 output per million | current high-volume OpenAI model | materially higher cost than Groq OSS |
| OpenAI GPT-5.6 Terra | balanced quality candidate | $2.50 input / $15 output per million | current balance of intelligence and cost | cost and latency |
| OpenAI GPT-5.6 Sol | quality ceiling and adjudication candidate | $5 input / $30 output per million | current flagship for complex work | too expensive as an unmeasured default |

OpenAI’s current [model catalogue](https://developers.openai.com/api/docs/models) describes Sol as the flagship, Terra as the balanced option, and Luna as the cost-sensitive option. The same page supplies the prices in the table. OpenAI’s [model guidance](https://developers.openai.com/api/docs/guides/latest-model) says to compare reasoning settings on representative workloads instead of assuming more reasoning is better.

## Illustrative generation cost

The table below assumes one request with 4,000 uncached input tokens and 500 output tokens. It excludes retries, routing, reranking, embeddings, storage, taxes, network, and human review.

| Candidate | Illustrative request cost |
|---|---:|
| Groq GPT-OSS 20B | $0.00045 |
| Groq GPT-OSS 120B | $0.00090 |
| OpenAI GPT-5.6 Luna | $0.00700 |
| OpenAI GPT-5.6 Terra | $0.01750 |
| OpenAI GPT-5.6 Sol | $0.03500 |

The release metric must be cost per successful grounded answer, not cost per API call. A cheap answer that fails citation or legal-review gates is wasted spend.

## Required architecture

### 1. Version the authorities

Every raw source needs a stable ID, authoritative URL, canonical title, consolidation or update date, response checksum, parser version, and review state.

The CAG cache, docstore, vector index, BM25 index, prompt, evaluation result, and deployed process must all name the same corpus version. Refuse startup when they do not.

### 2. Parse the legal structure

Chunk by Award structure rather than a target character count:

- Award;
- part;
- clause and subclause;
- schedule;
- classification;
- table;
- row and column headings;
- footnote;
- operative date.

Keep a parent record for the complete clause and child records for retrieval. Return children for ranking and the parent clause for context. Do not separate a pay value from its classification, unit, date, or footnote.

### 3. Extract a structured query

Before retrieval, identify:

- possible Award or industry;
- occupation and duties;
- employee type;
- classification;
- age or junior status when relevant;
- date of the event;
- location or jurisdiction when relevant;
- entitlement topic;
- requested calculation;
- missing facts;
- ambiguity level.

Use schema-constrained output and validate every field. A small model may perform this task only after deterministic and labelled evaluation.

### 4. Ask before guessing

When multiple Awards, classifications, employment types, or dates are plausible, ask a targeted question. Do not silently choose the most common Award.

The evaluation set must reward a correct clarification and penalize confident guessing.

### 5. Use staged retrieval

Recommended candidate pipeline:

```text
question
  -> structured query and ambiguity gate
  -> Award and effective-date filter
  -> BM25 plus dense candidate retrieval
  -> deduplication
  -> cross-encoder reranking
  -> parent-clause and table expansion
  -> context budget and coverage check
```

The current BGE model remains a valid baseline. Test it against:

- BGE-M3 dense retrieval;
- BGE-M3 dense plus sparse retrieval;
- the current BM25 plus BGE-base approach;
- an API embedding candidate only if privacy and cost permit.

The official [FlagEmbedding project](https://github.com/FlagOpen/FlagEmbedding) describes BGE-M3 as multilingual, able to process inputs up to 8,192 tokens, and able to support dense, sparse, and multi-vector retrieval. These are candidate capabilities, not proof on Australian Award text.

### 6. Add a reranker

Rerank only the best 20 to 100 first-stage candidates. Evaluate at least:

- local `BAAI/bge-reranker-v2-m3`;
- Cohere `rerank-v4.0-fast`;
- Cohere `rerank-v4.0-pro`;
- no reranker.

The [BGE reranker model card](https://huggingface.co/BAAI/bge-reranker-v2-m3) identifies it as a multilingual, local cross-encoder-style relevance scorer. Cohere’s current [Rerank documentation](https://docs.cohere.com/v2/docs/rerank) positions v4.0 Pro for quality and v4.0 Fast for latency and throughput.

Do not buy a reranking service until local and hosted candidates are compared on the same hidden clause-retrieval set.

### 7. Reduce and order context

Do not place the entire NES cache into every broad NES question. Retrieve the relevant NES section, adjacent qualifications, definitions, and interaction rules.

Remove repeated navigation and duplicate chunks. Place the strongest support near the beginning and preserve a second copy of critical qualifications near the end only if testing proves it helps.

The primary paper [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9.pdf) found that long-context performance can degrade when relevant information appears in the middle. A larger context window does not remove the need for focused retrieval.

### 8. Generate structured claims

Require a schema such as:

```text
answer_status
clarification_question
claims[]
  claim_text
  source_id
  clause
  quoted_support_span
  effective_date
uncertainties[]
disclaimer
```

Render the human answer from validated fields. Reject unknown source IDs, clauses not present in context, dates outside the selected corpus, and numeric claims without exact source support.

Structured output improves parse reliability. It does not prove factual correctness.

### 9. Verify after generation

Split the answer into atomic claims. For each claim:

1. locate the cited chunk and parent clause;
2. verify that the support span exists;
3. compare Award ID, clause, date, units, and numbers deterministically;
4. run an entailment or independent-model check for non-numeric prose;
5. remove or refuse unsupported claims;
6. escalate high-impact ambiguity to a human or an explicit limitation.

The verifier must not be the sole release oracle. Human-reviewed claim sheets remain required.

### 10. Trace every answer

Record:

- run and request ID;
- candidate commit;
- corpus and index versions;
- raw normalized query;
- route and extracted fields;
- candidate documents and scores;
- reranked documents;
- final context order;
- model, provider, parameters, prompt version, and token use;
- structured claims and verifier results;
- latency and cost by stage.

Without this trace, an incorrect answer cannot be diagnosed or reproduced.

## Tuning policy

Fine-tuning is not the first fix for missing or changing legal facts.

OpenAI’s [accuracy guidance](https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy) separates context problems from behavior problems. It recommends retrieval for missing, proprietary, or out-of-date information and fine-tuning for consistent task behavior.

Permitted fine-tuning experiments, after the baseline gates pass:

- query-field extraction;
- Award-alias normalization;
- clarification decisions;
- stable output format;
- refusal and uncertainty behavior;
- use of supplied RAG evidence.

Do not fine-tune current rates, Award clauses, or NES entitlements into model weights as the source of truth. They change and cannot be cited or invalidated reliably from weights.

Use representative RAG examples, a held-out set, and a no-regression suite. Stop if the gain does not exceed its confidence interval, operational complexity, and retraining cost.

## Cost-control design

Use this order:

1. deterministic rules for exact Award IDs and known aliases;
2. local embedding and BM25 retrieval;
3. local reranking if it meets latency and memory limits;
4. a small structured model for ambiguous query analysis;
5. the cheapest generator that passes every hard gate;
6. a larger model only for failed verification or approved difficult classes.

Further controls:

- retrieve narrow clauses instead of full documents;
- cap adaptive top-k by evidence coverage;
- cache only outputs keyed by normalized question, corpus, prompt, model, and policy version;
- never cache personalized or ambiguous legal answers across users;
- use asynchronous batch or flex processing for offline evaluations;
- set per-request and daily token budgets;
- stop retries after a bounded policy;
- count all failed and retried requests in cost;
- expire caches on a corpus or policy change.

OpenAI’s [cost guidance](https://developers.openai.com/api/docs/guides/cost-optimization) recommends reducing requests and tokens, selecting a smaller model when quality is maintained, and using batch or slower processing for suitable offline work. Groq advertises a 50% batch discount on its [pricing page](https://groq.com/pricing); contract terms and actual billed usage still need verification.

## Experiment order

Run only after corpus and retrieval gold sets are approved:

1. current embeddings and BM25, no reranker;
2. current retrieval plus local BGE reranker;
3. BGE-M3 dense plus sparse, with and without local reranker;
4. best local retrieval plus hosted reranker candidates;
5. best retrieval with Groq GPT-OSS 20B and 120B;
6. the same context with OpenAI Luna, Terra, and Sol;
7. cascades using a cheap default and quality escalation;
8. optional behavior fine-tuning after remaining failures are classified.

Each comparison must use the same frozen context, prompt policy, hidden test cases, randomization, and cost accounting. Change one factor at a time unless the experiment is explicitly factorial.

## Promotion rule

No candidate is promoted because it is newer, larger, faster, cheaper, or recommended by a provider.

Promote only when:

- every high-impact safety case passes;
- claim support and citation completeness are 100%;
- the lower confidence bound meets the approved correctness threshold;
- no protected or language stratum regresses beyond its margin;
- latency and memory meet deployment limits;
- cost per successful grounded answer improves or has an approved trade-off;
- privacy and provider terms are approved;
- the result repeats on an immutable candidate.
