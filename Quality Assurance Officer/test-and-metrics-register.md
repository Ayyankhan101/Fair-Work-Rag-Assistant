# Test and metrics register

Owner: quality assurance

Status date: 27 July 2026

## Reading rule

A specification is a planned test. An execution is one recorded run against an identified test point. A diagnostic pass is not a release pass unless its data, environment, oracle, and threshold meet the release rule.

The allowed states are:

- `passed`: the stated procedure met its threshold on the named candidate;
- `failed`: it ran and missed the threshold;
- `blocked`: a prerequisite prevented valid execution;
- `not run`: no execution was attempted;
- `invalid`: it ran, but identity, evidence, oracle, or procedure was not acceptable;
- `historical`: it describes an older test point and cannot qualify the current candidate.

## Defined test inventory

| Specification file | Area | Unique specifications |
|---|---|---:|
| `test-cases-01-foundation.md` | repository, dependencies, documents, CI | 65 |
| `test-cases-02-corpus-ingestion-store.md` | source, ingestion, cache, vector store | 80 |
| `test-cases-03-routing-retrieval-answer.md` | routing, retrieval, grounding, answer | 105 |
| `test-cases-04-ui-security-performance-deployment.md` | UI, API failure, security, accessibility, load, recovery | 115 |
| `test-cases-05-prompt-assurance.md` | role hierarchy, evidence, dates, calculations, attacks, output | 120 |
| Total |  | 485 |

Parameterized execution across 122 Awards, multiple NES topics, providers, models, operating systems, repeated runs, browsers, and load levels produces more than 1,000 required executions. The package does not claim that 485 tests ran or passed.

## Executable QA assets

### Regression tests

| File | Methods | Main purpose |
|---|---:|---|
| `tests/test_cag.py` | 3 | UTF-8 preservation, CAG eligibility, missing-file behavior |
| `tests/test_config_router.py` | 9 | Award aliases, false positives, specificity, topics, route decisions |
| `tests/test_prompt_safety.py` | 4 | insufficient evidence, non-invention, untrusted context, no forced answer |
| Total | 16 |  |

These tests live under the QA folder so they do not pretend to be development-owned product tests. Engineering should implement reviewed tests in the product test structure and link each one to a requirement and defect.

Post-cleanup baseline result: 2 of 16 methods passed. The test runner reported 14 failure records and four errors due to subtest accounting.

### Diagnostic tools

| Tool | Purpose | External LLM required |
|---|---|---|
| `tools/audit_repository.py` | corpus identity, metadata, duplicates, evaluation provenance, reproducibility | no |
| `tools/check_documentation_style.py` | banned filler terms and title-case heading check | no |
| `tools/offline_request_matrix.py` | 60 request variants through router, retrieval, CAG, and captured prompt | no |
| `tools/semantic_retrieval_probe.py` | expected-Award rank, repeatability, concurrent search | no |
| `tools/historical_claim_support_probe.py` | weak literal support and citation-presence check for historical answers | no |
| `tools/failure_path_probe.py` | provider and application failure propagation | no |
| `tools/server_load_probe.py` | loopback Gradio behavior, concurrency, latency, throughput, memory | no |

The tools are evidence generators. They are not trusted merely because they exist. Their code, cases, and oracles need independent review.

## Executed evidence by layer

| Layer | Execution | Test point | Result | Status |
|---|---|---|---|---|
| repository inventory | tracked and untracked tree classification | QA worktree | paths and artifact classes recorded | passed for inventory |
| Git ownership | diff outside QA versus merge base | post-cleanup | zero paths differ | passed |
| Python syntax | AST parse of 29 product and QA files | post-cleanup baseline | 29/29 | passed |
| unit regression | 16 QA methods | post-cleanup baseline | 2 passed; suite failed | failed |
| declared dependency | matrix import using only requirements | post-cleanup baseline | missing `rank_bm25` | failed |
| static lint | Ruff 0.16.0 product check | post-cleanup baseline | 90 findings | failed |
| format | Ruff 0.16.0 format check | post-cleanup baseline | 17 of 18 files need change | failed |
| corpus audit | persisted docstore | post-cleanup baseline | release blockers present | failed |
| official page reachability | 122 official Award IDs | 27 July 2026 | 122/122 pages reachable | passed only for reachability |
| source acceptance | raw accepted Award sources with hashes | repository | raw source set absent | blocked |
| request matrix | 60 cases, natural Windows | post-cleanup baseline | stopped before case 1 | blocked by encoding |
| request matrix | 60 cases, forced UTF-8 and ephemeral missing dependency | post-cleanup baseline | 31/60 all-check pass | failed diagnostic |
| request matrix | 60 cases | earlier dirty QA state | 41/60 all-check pass | historical |
| semantic retrieval | 36 labelled expected-Award cases | persisted store | top-1 16/36; top-10 24/36 | failed |
| filtered retrieval | 36 expected-Award cases | persisted store | 33/36 contained expected Award | failed |
| repeatability | 10 repeated searches | persisted store | same order in 10/10 | passed diagnostic |
| concurrency | 300 in-process searches | persisted store | 300/300 completed | passed diagnostic |
| clarification | nine cases requiring more facts | offline matrix | 0/9 | failed |
| historical answer support | 25 saved answers | current retrieved context | 4/25 weak literal support | failed diagnostic |
| historical numeric support | 23 numeric checks | current retrieved context | 8/23 | failed diagnostic |
| historical citation presence | 46 cited references | current retrieved context | 13/46 | failed diagnostic |
| provider failure | six injected failure types | capture/failure harness | behavior recorded; controls inadequate | failed |
| loopback HTTP functional | eight requests | local provider-free server | 8/8 behavior checks | passed diagnostic |
| loopback load | 288 requests | local provider-free server | 288/288 transport completions | passed transport only |
| 32-worker load | local provider-free server | earlier dirty QA state | median 5.936 s; p95 7.902 s; peak RSS 1.276 GB | failed pending SLO |
| live model quality | Groq, Gemini, OpenRouter, OpenAI candidates | none | no approved key or spend | blocked |
| legal answer review | claim-level gold set | none | no approved legal oracle | blocked |
| browser accessibility | accepted UI candidate | none | candidate absent | not run |
| production security/load | accepted deployment | none | deployment absent | not run |

## Metric catalogue

### Candidate and evidence metrics

| Metric | Definition | Release rule |
|---|---|---|
| candidate identity completeness | commit, branch, dirty flag, build ID, corpus hash, prompt hash, model ID, dependency lock hash present | 100% |
| product-tree ownership | changed non-QA paths versus approved base | zero unapproved paths |
| evidence provenance | required run fields present in every result | 100% |
| evidence immutability | retained artifact hash matches reviewed manifest | 100% |
| repeatability | repeated deterministic runs returning the accepted result | 10/10 minimum for selected probes |

### Source and corpus metrics

| Metric | Formula or method | Release rule |
|---|---|---|
| official Award coverage | accepted official Award IDs / 122 | 122/122 |
| title identity | accepted ID-title pairs / 122 | 122/122 |
| source provenance | sources with URL, retrieval time, effective date, bytes, and SHA-256 / accepted sources | 100% |
| source freshness | sources within approved amendment/update rule / accepted sources | 100% |
| parse retention | required headings, clauses, tables, footnotes, and preamble retained / labelled fixtures | 100% for legal identity fields |
| metadata completeness | chunks with all required metadata / all chunks | 100% |
| empty chunks | count of blank chunks | zero |
| unexplained exact duplicates | duplicate chunks not classified as intentional | zero |
| CAG/RAG version consistency | route artifacts sharing the same corpus manifest | 100% |
| reproducible rebuild | clean rebuild matching declared inputs and expected acceptance checks | pass |

### Routing and retrieval metrics

| Metric | Formula | Release rule |
|---|---|---:|
| route accuracy | correct labelled routes / labelled route cases | 100% |
| Award detection accuracy | correct canonical Award ID / applicable cases | threshold set by risk slice; current plan requires 100% labelled routing |
| topic detection accuracy | correct normalized topic / applicable cases | approved per-slice threshold |
| expected Award in context | applicable contexts containing target Award ID / cases | 100% for exact-Award questions |
| Award recall@3 | cases with target Award in top three / cases | at least 98% |
| Award recall@5 | cases with target Award in top five / cases | 100% |
| clause recall@5 | cases with reviewed target clause in top five / cases | at least 95% |
| mean reciprocal rank | mean reciprocal rank of first accepted target | report with recall; no substitute for hard gates |
| normalized discounted cumulative gain | ranked relevance against multi-grade labels | compare retriever candidates |
| clarification recall | correctly blocked under-specified cases / cases requiring clarification | 100% |
| over-clarification rate | answerable cases incorrectly blocked / answerable cases | approved low threshold after legal/product review |
| negation failure rate | adversarial negated cases incorrectly selecting excluded Award/topic / negation cases | zero |

### Answer and prompt metrics

| Metric | Formula or method | Release rule |
|---|---|---|
| atomic claim support | supported atomic factual claims / all factual claims | 100% |
| citation entailment | citations that support the complete linked claim / cited claims | 100% |
| citation identity | citations tied to correct Award ID, clause, version, and effective date / citations | 100% |
| current-rate correctness | reviewed current rate answers correct in value, unit, classification, date, and condition / cases | 100% |
| calculation correctness | exact formula, inputs, units, and output all correct / calculation cases | 100% |
| insufficient-evidence recall | correctly declined cases / insufficient-evidence cases | 100% |
| unsupported-answer rate | answered cases with one or more unsupported claims / answered cases | zero |
| prompt role separation | rendered requests with stable system policy and separate user content / requests | 100% |
| prompt-injection resistance | attacks causing no policy override or source-instruction execution / attacks | 100% |
| structured-output validity | responses valid against the accepted schema / responses | 100% before claim validation |
| prompt size | system, user, and evidence tokens and characters per request | report p50, p95, max and cost |
| context use | cited accepted chunks / supplied chunks | diagnostic; use to detect waste |

An aggregate “accuracy” number cannot override a failed legal hard gate. Scores must also be sliced by Award, question type, difficulty, date sensitivity, ambiguity, language, and retrieval condition.

### API and provider metrics

| Metric | Definition | Required record |
|---|---|---|
| requested-model compliance | responses served by exact requested model / requests | requested and actual model IDs |
| transport success | valid provider response / attempts | status, exception class, request ID |
| timeout rate | timed-out requests / requests | timeout setting and elapsed time |
| retry count | total and per-request retries | reason, delay, jitter |
| fallback rate | requests changing model/provider/prompt / requests | original and fallback identities |
| rate-limit rate | 429 or provider throttle responses / requests | retry-after and recovery |
| input tokens | provider-reported prompt tokens | per request and distribution |
| output tokens | provider-reported completion tokens | per request and distribution |
| estimated cost | provider price applied to recorded token use | price date, currency, formula |
| observed billed cost | provider billing record for run | invoice/export reference |
| quality per cost | hard-gate pass plus reviewed score divided by cost | compare only candidates passing safety gates |
| latency | wall time from request dispatch to accepted response | p50, p95, p99, max |

Provider comparison must use the same frozen corpus, request set, prompt policy, temperature, maximum output, retry policy, and scorer. Gemini, OpenRouter, Groq, and OpenAI are candidates, not automatically interchangeable APIs.

### Performance and deployment metrics

| Metric | Definition | Current planned rule |
|---|---|---|
| retrieval latency | route start to accepted context | p95 under 1 second |
| full response latency | accepted request to validated answer | p95 under 8 seconds |
| error rate at ten users | failed or invalid responses / requests | under 1% |
| throughput | accepted validated responses / wall second | report at each load level |
| peak RSS | maximum process resident memory | threshold requires deployment budget |
| startup readiness | process start to healthy and usable | bounded, no provider call at import |
| saturation point | first load level missing latency/error SLO | report workers and topology |
| soak stability | resource, latency, and error trend over approved duration | no unexplained growth or threshold breach |
| recovery time | fault injection to restored service | approved RTO |
| recovery point | accepted data loss after failure | approved RPO |
| deployment cost | compute, storage, bandwidth, provider, and observability cost | approved monthly and per-answer limits |

### Security, privacy, accessibility, and operations metrics

| Metric | Release rule |
|---|---|
| open S0/S1 defects | zero |
| live or unrevoked secrets in candidate/history | zero |
| vulnerable locked dependencies | zero unaccepted findings |
| action pinning | 100% of third-party workflow actions pinned to reviewed commit |
| least-privilege workflow jobs | 100% |
| provider data classification | approved for every transmitted field |
| retention, residency, training-use, and deletion policy | approved and tested |
| prompt and log redaction | no secret or prohibited personal data in retained artifacts |
| keyboard operation | all supported UI functions |
| accessible name and error announcement | 100% of interactive/error states |
| contrast and focus visibility | accepted WCAG target |
| audit event completeness | request, model, prompt, corpus, validator, outcome, latency, tokens, and cost IDs present |

## Bias controls

The evaluation system uses these controls:

1. Freeze candidate, corpus, prompts, parameters, and provider versions before opening results.
2. Keep development examples separate from hidden evaluation cases.
3. Include every official Award ID rather than selecting easy or familiar Awards.
4. Stratify by question difficulty and risk.
5. Use reviewed atomic claims and source spans, not keyword-only scoring.
6. Blind reviewers to provider/model identity where manual scoring is required.
7. Require two reviewers or adjudication for disputed legal labels.
8. Record failures and invalid runs; do not delete inconvenient cases.
9. Report per-slice results and confidence intervals where sample size permits.
10. Run contamination checks for prompt examples, saved answers, and public benchmark overlap.
11. Compare cost only after safety and correctness gates pass.
12. Keep a held-out final set unused for prompt, retriever, or model selection.

## Test planning order

### Stage 0: freeze and identify

Entry:

- engineering supplies one immutable commit;
- QA records a clean status and dependency lock;
- corpus, prompt, and model identities are fixed.

Exit:

- no unapproved product change during execution.

### Stage 1: cheap deterministic gates

Run:

- repository manifest;
- JSON/YAML/Python/shell validation;
- clean dependency install;
- dependency vulnerability and license scan;
- unit and property tests;
- documentation and workflow checks.

Stop on missing dependency, syntax error, source absence, or identity mismatch.

### Stage 2: source, ingestion, and store

Run:

- 122-ID source acceptance;
- checksums and effective dates;
- parser round-trip fixtures;
- table, footnote, subclause, Unicode, and maximum-chunk tests;
- isolated rebuild;
- store identity and duplicate checks;
- cross-platform load.

Stop before answer evaluation if this stage fails.

### Stage 3: routing and retrieval

Run:

- labelled route, Award, topic, negation, ambiguity, typo, and unknown cases;
- two retrieval questions per Award;
- clause and schedule cases;
- lexical, vector, hybrid, filter, reranker, and parent-context candidates;
- repeated and concurrent searches.

Select architecture only from hidden held-out results, latency, memory, and cost.

### Stage 4: prompt and answer

Run every accepted model/prompt pair against:

- 120 prompt specifications;
- reviewed atomic legal claims;
- missing-evidence and clarification cases;
- date/version conflicts;
- rates and calculations;
- injection in both user input and retrieved text;
- structured-output and claim-validator failures.

Any unsupported claim, invented citation, wrong current rate, or unsafe forced answer blocks the pair.

### Stage 5: API and failure handling

Run approved Groq, Gemini, OpenRouter, and OpenAI candidates only where access and spend are authorized.

Capture:

- request and actual model IDs;
- timeout, retries, fallback, and request ID;
- input/output tokens;
- latency;
- billed or estimated cost;
- raw redacted response;
- validation outcome.

Test 401, 403, 404/model missing, 413, 429, timeout, 500, malformed output, provider model substitution, and network loss.

### Stage 6: UI, security, accessibility, and deployment

Run against the accepted deployed topology:

- browser behavior and error states;
- input limits and concurrency;
- keyboard and assistive-technology checks;
- secret, dependency, workflow, and application security checks;
- privacy and retention verification;
- ramp, spike, soak, saturation, recovery, rollback, and cost tests.

### Stage 7: independent release review

QA issues a release report only after:

- every mandatory result maps to raw evidence;
- legal, security/privacy, engineering, QA, and release owners sign their gates;
- no S0/S1 defect remains;
- exceptions identify owner, reason, expiry, monitoring, and rollback.

## Current stop point

Execution is stopped at deterministic and corpus gates. Missing declared dependency, Windows decoding failure, source reproducibility gaps, corpus identity defects, prompt safety defects, and lack of an immutable engineering candidate make full model comparison wasteful and invalid.

This stop protects accuracy and cost: do not spend provider tokens to score answers produced from an unaccepted corpus and a failing route/prompt stack.
