# Phase 6 RAG+CAG request and load report

Date: 27 July 2026

Result: failed

This phase executed the maximum local request, retrieval, startup, failure, and loopback-server testing possible without a provider credential or product-code change.

## Honest scope

The phase proves behavior of local deterministic components. It does not prove generated-answer accuracy.

Real components exercised:

- router and Award/topic detectors;
- CAG loading and selection;
- persisted 16,692-document store;
- raw semantic retrieval;
- exact metadata-filtered semantic retrieval;
- filtered document retrieval;
- BM25 and hybrid fallback paths;
- prompt context assembly;
- prompt message rendering;
- string output parsing;
- Gradio UI handler, queue, and loopback HTTP API;
- application startup and missing-key behavior;
- provider-error selector and fallback construction.

Replaced component:

- the external LLM was replaced by a capture runnable during provider-free chain and server tests.

Consequently, output fluency, legal correctness, hallucination rate, provider latency, token usage, and provider cost remain untested.

## Test points

| Test point | Identity | Qualification |
|---|---|---|
| executable working tree | `QA` at `fb9028a`, dirty with 20 modified tracked files | diagnostic only |
| current development source | `develop` at `dd3bd45`, temporary archive | code exercised with the current QA data artifacts |
| persisted data | current `data/vectorstore` and NES file | unaccepted, incomplete, and unversioned |

QA is still four commits behind `develop`. Neither state is an immutable release candidate.

## Execution inventory

| Execution | Cases or operations | Result |
|---|---:|---|
| untracked unit suite | 16 | 16 passed |
| dirty-QA offline request matrix | 60 | 41 passed all applicable diagnostic checks |
| natural Windows development matrix | 0 requests | blocked by `UnicodeDecodeError` |
| forced-UTF-8 development matrix | 60 | 31 passed all applicable diagnostic checks |
| semantic Award-query accuracy | 36 | 16 top-1; 24 top-10 |
| metadata-filtered semantic accuracy | 36 | 33 returned only the expected Award |
| semantic deterministic repeats | 10 cases × 3 | 10 identical |
| semantic concurrency | 5 levels × 60 | 300 completed, zero errors |
| historical-answer support | 25 | 4 passed the weak literal-support diagnostic |
| provider-error simulations | 6 | three fallbacks; three propagated errors |
| corrected Gradio functional HTTP | 8 | 8 passed |
| corrected Gradio load HTTP | 6 levels × 48 | 288 completed, zero request errors |
| initial Gradio run | 296 HTTP requests | retained; capacity interpretation superseded |

Defined test specifications remain 485. This phase executed selected diagnostic instances, not all 485 specifications.

## Sixty-request RAG+CAG matrix

The questions included:

- 28 straightforward Award requests;
- 12 NES requests;
- five combined Award and NES requests;
- general overtime, penalty, and wage requests;
- ambiguous Award coverage;
- negated Award names;
- misspellings and punctuation variants;
- Unicode punctuation;
- a non-English question;
- nonsense input;
- two prompt-injection requests.

### Dirty QA working tree

| Measure | Result |
|---|---:|
| all applicable diagnostic checks | 41 of 60 |
| route expectation | 59 of 60 |
| Award detection expectation | 36 of 38 |
| topic detection expectation | 39 of 47 |
| expected Award present in context | 33 of 36 |
| expected CAG presence | 19 of 19 |
| clarification or answerability gate | 0 of 9 |
| chain execution | 60 of 60 |

These percentages are diagnostics for a hand-authored matrix. They are not statistical legal-accuracy estimates.

### Important failures

1. Clerks and Children’s Services requests returned zero Award documents because configured names do not equal persisted metadata.
2. All nine ambiguous, unknown, general-minimum-wage, typo, non-English, and nonsense cases lacked a clarification or answerability path.
3. “I do not work in retail” selected the Retail Award.
4. “This is about transport logistics, not sport” selected the Sporting Organisations Award.
5. Common phrases using generic `leave`, `weekend`, `hours`, and hyphenated `casual-loading` missed their expected topic.
6. Nonsense input retrieved Salt Industry Award documents.
7. “What rules apply to this job?” retrieved unrelated education, hospitality, modelling, and NES documents.
8. Every rendered prompt contained one `HumanMessage` and no system message.

The prompt capture used no model, so prompt-injection answer resistance was not passed.

## Current development source

The natural Windows run did not reach request one. `develop:src/cag.py` opens the NES file without an explicit encoding and raised:

```text
UnicodeDecodeError: 'charmap' codec can't decode byte 0x8d at position 1009
```

For diagnostic depth only, a second run forced `PYTHONUTF8=1`.

| Measure | Forced-UTF-8 `develop` result |
|---|---:|
| all applicable diagnostic checks | 31 of 60 |
| route expectation | 58 of 60 |
| Award detection expectation | 25 of 38 |
| topic detection expectation | 39 of 47 |
| expected Award present in context | 22 of 36 |
| clarification | 0 of 9 |
| chain execution | 60 of 60 |

Examples of development-source misrouting:

- marine towage mapped to Marine Tourism;
- generic mining mapped to Black Coal Mining;
- school general staff mapped to `General minimum wage`;
- pharmacist, pilot, nurse, and school-teacher aliases were missed;
- the Ambulance and social/community configured names did not join to stored names.

The forced runtime is not a fix and not a pass. It only exposed downstream defects.

## Semantic retrieval

The persisted TurboVec index and local `BAAI/bge-base-en-v1.5` embedding path loaded successfully.

| Metric | Result |
|---|---:|
| raw semantic expected Award at rank 1 | 16 of 36 |
| raw semantic expected Award within top 5 | 22 of 36 |
| raw semantic expected Award within top 10 | 24 of 36 |
| exact metadata filter returned only expected Award | 33 of 36 |
| three-run result order identical | 10 of 10 |
| store load time in measured process | 0.804 seconds |
| RSS before load | 129,269,760 bytes |
| RSS after load | 594,325,504 bytes |

Metadata filtering failed for two Clerks cases and one Children’s Services case because the expected canonical values were absent.

Raw semantic top-10 failures included Hospitality meal breaks, Retail casual loading, Clerks coverage, Hair and Beauty breaks, Local Government leave, Children’s Services breaks, disability support overtime, and several combined NES/Award questions.

### In-process semantic concurrency

Each level executed 60 local searches.

| Workers | Errors | Throughput/s | Median | p95 | Peak RSS |
|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 45.027 | 21.986 ms | 25.294 ms | 618,041,344 |
| 2 | 0 | 61.766 | 32.619 ms | 37.739 ms | 619,278,336 |
| 4 | 0 | 71.820 | 55.788 ms | 66.246 ms | 621,547,520 |
| 8 | 0 | 71.568 | 112.552 ms | 148.070 ms | 625,098,752 |
| 16 | 0 | 70.843 | 193.211 ms | 307.919 ms | 630,956,032 |

Retrieval throughput flattened near four workers while per-request latency continued to grow. This is not HTTP or provider capacity.

## Historical answer support

The 25 stored hard-evaluation answers were not regenerated. Each answer’s money, percentage, duration, citation, and source-reference strings were compared with the context retrieved now.

| Diagnostic | Found | Total |
|---|---:|---:|
| questions passing every applicable literal-support check | 4 | 25 |
| numeric claims found | 8 | 23 |
| citation strings found | 13 | 46 |
| source-reference fields supported | 22 | 25 |

The four passing IDs were H02, H04, H11, and H15.

This is intentionally a weak oracle:

- occurrence does not prove applicability or legal correctness;
- absence can result from retrieval truncation or formatting;
- the historical run identity is unknown;
- no legal reviewer approved the values.

Even this weak check contradicts using the historical 87.55% score as current evidence.

## Prompt and CAG size

Across 60 captured prompts:

| Measure | Result |
|---|---:|
| prompt message shape | 60 single `HumanMessage` |
| minimum prompt size | 3,063 characters |
| mean prompt size | 19,773.2 characters |
| maximum prompt size | 47,364 characters |
| CAG cache size | 38,482 characters |
| maximum captured context | 44,318 characters |

Every NES candidate receives the entire CAG cache. The system does not select only the NES sections needed for the question. This raises provider cost, latency, attention dilution, and conflicting-evidence risk.

No tokenizer-specific count is reported because the configured model/tokenizer was not available for an accepted run.

## Startup

### Capture-model startup

With the provider replaced, actual app initialization and store loading completed in:

- 9.288 seconds in the first server run;
- 7.825 seconds in the corrected run.

The corrected server then launched in 0.617 seconds.

### Natural startup without a key

With no provider replacement and no `GROQ_API_KEY`, import:

- loaded CAG and the vector store;
- failed during `ChatGroq` construction;
- exited after 15.349 seconds;
- did not expose a controlled readiness or configuration response.

Startup does expensive work before detecting missing mandatory provider configuration.

## Provider-error paths

Six local exceptions were injected.

| Error | Fallback | Result |
|---|---|---|
| 429 rate limit | yes | capture response |
| 413 too large | yes | capture response |
| text containing `rate_limit` | yes | capture response |
| timeout | no | exception propagated from `ask_question` |
| 500 | no | exception propagated |
| 401 | no | exception propagated |

All three fallback prompts:

- were one human-role message;
- contained a nested mapping representation;
- included the question twice;
- were 8,236 characters;
- did not implement the claimed smaller context.

The UI catches propagated exceptions and returns a generic message, but no bounded timeout, retry schedule, jitter, circuit breaker, or recovery telemetry was demonstrated.

## Gradio functional and load testing

The corrected loopback server used the actual application, CAG, store, retrieval, prompt, handler, Gradio queue, and HTTP serialization. The provider was replaced.

### Functional HTTP

Eight of eight checks returned the expected structural behavior:

- empty and whitespace input were rejected;
- Award, NES, and combined questions showed the expected route label;
- nonsense and injection input reached the RAG route;
- a 2,001-character question was rejected.

“Passed” here means the endpoint behaved as implemented. Routing nonsense or an injection attempt to generation is not a safety pass.

### Corrected load run

Gradio clients were constructed before each timed interval. Each level sent 48 mixed easy, NES, combined, unknown, and nonsense requests.

| Workers | Complete | Errors | Throughput/s | Median | p95 | Maximum | Peak RSS |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 48 | 0 | 0.870 | 0.701 s | 3.681 s | 6.432 s | 1,102,180,352 |
| 2 | 48 | 0 | 1.220 | 0.750 s | 5.058 s | 6.758 s | 1,113,739,264 |
| 4 | 48 | 0 | 1.730 | 1.539 s | 7.284 s | 7.665 s | 1,129,938,944 |
| 8 | 48 | 0 | 4.492 | 1.827 s | 1.956 s | 2.011 s | 1,157,558,272 |
| 16 | 48 | 0 | 2.608 | 6.751 s | 9.947 s | 10.158 s | 1,199,542,272 |
| 32 | 48 | 0 | 4.592 | 5.936 s | 7.902 s | 7.961 s | 1,275,621,376 |

The non-monotonic small-sample results show queue and runtime variability. They do not establish a maximum sustainable capacity.

What can be stated:

- all 288 timed requests completed;
- no response was structurally invalid;
- latency became multi-second without provider latency;
- process memory was near 1 GB after initialization and peaked near 1.28 GB;
- no application admission limit, per-user quota, or request deadline was exercised.

The initial 296-request run is retained as raw evidence, but its capacity values are superseded because client construction occurred inside the timed interval.

## What still cannot be executed

- current-model answers without an approved credential and spend;
- legal correctness without reviewed gold claims;
- provider token, latency, retry, rate-limit, and cost behavior;
- full browser interaction and screen-reader testing;
- long soak, leak, restart, and multi-process testing;
- production proxy, authentication, autoscaling, region, and network behavior;
- malicious-payload penetration testing;
- rollback and disaster recovery;
- current-development end-to-end testing on an immutable artifact and accepted corpus.

## Decision

Phase 6 failed.

The server did not crash under the bounded provider-free HTTP probe, but “did not crash” is not a release criterion. Retrieval accuracy, clarification, canonical Award identity, prompt hierarchy, historical claim support, startup readiness, context size, and deployment cost remain unacceptable or unqualified.

Release remains blocked.
