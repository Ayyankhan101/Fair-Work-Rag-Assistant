# Final QA report: 27 July 2026

## Post-cleanup state note

This report records the earlier dirty-QA and development-snapshot phases. QA later preserved its working product changes as patches, relocated QA tests and tools, and restored every non-QA path to fork point `3e91e9e`. The restored baseline passes 2 of 16 QA unit-test methods, fails its declared-dependency import, and blocks before request one on natural Windows encoding. The open-defect count is now 70. Use `developer-handoff-after-qa-2026-07-27.md` for the current handoff.

## Disposition

Release blocked.

The repository is a promising prototype with a sensible hybrid-retrieval direction. It is not ready to provide dependable Award or NES answers to the public.

## Scope completed

This QA pass:

- inventoried the entire tracked repository;
- read active code, scripts, workflow, data, configuration, and project documentation;
- inspected supplied PDF, DOCX, image, chat, vault, skill, and discarded prototype artifacts;
- compared the requested scope with current official Fair Work pages;
- audited the persisted store;
- checked current model and reranker options using current primary sources;
- reviewed the active and committed LLM prompts;
- audited GitHub Actions, Python security findings, narrowed secret exposure, dependency and license evidence;
- compared the QA branch with the current development tip and tested the development-only Markdown parser with isolated fixtures;
- assessed the supplied software engineering lifecycle and OpenCode work records;
- defined 485 unique test specifications;
- designed an unbiased, claim-level evaluation system;
- documented security, privacy, accessibility, performance, cost, deployment, and recovery gates;
- created detailed and quick-glance reports.

Product code was not changed after the documentation-only instruction. Earlier working-tree code and test changes remain unaccepted and are disclosed in `transparency-log.md`.

## Candidate identity

| Field | Value |
|---|---|
| branch | `QA` |
| HEAD | `fb9028a8978393968788038492c7d17af02ed42b` |
| tracked files at HEAD | 117 |
| tracked tests at HEAD | 0 |
| candidate state | dirty, not immutable |
| modified tracked files at baseline | 20 |
| relationship to `develop` | one commit ahead, four commits behind |
| current `develop` | `dd3bd45d58f430b6f88a927d7eee6ce1a815098d` |

The dirty working tree cannot be a release candidate. It also cannot qualify the current development branch because four development-only commits change conversion, ingestion, storage, and prompting.

## Source and data result

| Measure | Result |
|---|---:|
| official Award IDs | 122 |
| live pages reachable | 122 |
| persisted unique Award names | 129 |
| persisted Award chunks | 16,665 |
| persisted NES chunks | 27 |
| mandatory Award IDs missing | 2 |
| exact duplicate groups | 388 |
| extra duplicate chunks | 1,251 |

MA000095 and MA000121 are missing. MA000002 is labelled `Workplace Relations Act 1996`.

The live source check proves reachability, not corpus acceptance. Raw Award files and per-source hashes are absent. NES text is contaminated and unversioned.

## Prompt result

The application does not create a system message. It sends policy, evidence, and the user question as one human message.

The committed prompt explicitly requires confident answers and numbers even when evidence is incomplete. The working-tree prompt removes the worst instructions but remains unaccepted and retains architectural gaps.

Thirty prompt defects and 120 prompt-specific test specifications are recorded. The proposed role-separated, structured prompt remains a draft.

## Model result

The current primary and fallback Groq models have an announced 16 August 2026 developer-tier shutdown date.

No replacement is approved. Groq GPT-OSS 20B and 120B are immediate continuity candidates. OpenAI GPT-5.6 Luna, Terra, and Sol are controlled comparison candidates. Selection requires the same frozen corpus, context, prompt policy, hidden questions, claim review, and cost accounting.

## Evaluation result

The historical hard evaluation:

- contains 25 questions;
- records 24 format passes and 23 content passes;
- reports 87.5467%;
- lacks run time, commit, corpus, model, and prompt identity;
- uses keyword, regex, and length scoring;
- does not prove claim or citation support;
- includes stale output relative to the current store.

It is not release evidence.

## Test inventory

| File | Specifications |
|---|---:|
| `test-cases-01-foundation.md` | 65 |
| `test-cases-02-corpus-ingestion-store.md` | 80 |
| `test-cases-03-routing-retrieval-answer.md` | 105 |
| `test-cases-04-ui-security-performance-deployment.md` | 115 |
| `test-cases-05-prompt-assurance.md` | 120 |
| Total | 485 |

Parameterized execution across Awards, NES subjects, browsers, models, source states, and repetitions exceeds 1,000 runs.

Defined tests are not passed tests.

## Local checks

At the recorded dirty working-tree baseline:

- Ruff lint passed.
- Ruff format check passed.
- 16 untracked unit tests passed.
- 34 tracked JSON files parsed.
- four workflow YAML files parsed.
- dependency resolution succeeded.
- a clean isolated Python 3.11 import environment installed 95 packages.
- `pip-audit` found no known vulnerability in the resolved graph on the run date.
- three of four shell scripts failed `bash -n` due to CRLF.

These results qualify neither HEAD nor deployment.

## Blocking defect groups

### Source

- missing mandatory Awards;
- wrong Award identity;
- no raw source corpus;
- no source checksums or version handshake;
- contaminated NES source.

### Prompt and answer

- no system-role boundary;
- unsafe committed answer incentives;
- no explicit clarification or conflict status;
- no effective-date contract;
- no atomic claim citations;
- no claim verifier.

### Model and evaluation

- both models approaching shutdown;
- no qualified replacement;
- historical evaluation invalid for release;
- no blind held-out legal review.

### Engineering and operations

- dirty candidate;
- QA branch four commits behind current development;
- no tracked tests at HEAD;
- unpinned dependencies;
- unpinned GitHub Actions and excessive workflow permissions;
- Markdown conversion and ingestion can publish a partial or lossy corpus;
- README license claim has no repository license file;
- self-certified completion and no demonstrated independent review;
- unsafe or non-portable shell automation;
- no accepted privacy, security, accessibility, load, cost, rollback, or recovery evidence.

## Required release sequence

1. Select the intended development lineage and exact candidate commit.
2. Decide and remove or accept the pre-boundary working-tree patch, then reconcile QA to that candidate.
3. Issue corrected controlled requirements.
4. Materialize and accept the 122-Award plus NES corpus.
5. Rebuild versioned artifacts.
6. pass parser and store-integrity gates.
7. pass routing and retrieval gates.
8. implement and qualify role-separated prompt and claim validation.
9. qualify replacement models before shutdown.
10. run blind, held-out, claim-level evaluation.
11. pass security, privacy, accessibility, performance, cost, deployment, and recovery gates.
12. close all S0 and S1 defects and obtain named sign-off.

## Claims not made

This report does not claim:

- legal correctness;
- production readiness;
- 485 passing tests;
- ISO certification;
- WCAG conformance;
- security;
- privacy compliance;
- cost feasibility;
- provider continuity;
- a selected model;
- an accepted prompt;
- an accepted corpus.

## Final statement

The next correct step is not deployment and not a blind model upgrade. It is controlled source and candidate acceptance.

Until the blocking evidence exists, the application should remain clearly labelled as non-production and unsuitable for pay, entitlement, Award-coverage, or personal legal decisions.

## Continuation update: local automation and API assurance

After the first final disposition, QA continued with read-only execution against the same dirty working tree.

The 16 untracked tests passed in an isolated requirements environment. Measured statement coverage was 12%. `app.py`, `rag.py`, ingestion, vector-store management, embedding integration, and all three retrieval implementations had 0% coverage.

Unpinned dependency resolution selected yanked `numpy==2.4.0`. The first isolated install/import attempt exceeded 60 seconds; a cached retry passed. Application import exceeded both 20-second and 50-second limits.

The current `ChatGroq` configuration has no explicit request timeout. It inherits two retries, does not retain usage and request metadata, and does not request structured output. The fallback path changes to a materially smaller model without quality evidence and does not actually reduce the reused context builder.

An offline 429 probe showed that fallback also changes the prompt shape. It produced one human-role message, nested the original context/question mapping inside the context field, and repeated the question twice. No provider request was made for that probe.

Current official provider documentation was reviewed for Groq, Gemini, OpenRouter, and OpenAI. No live inference request was made because all relevant API keys were absent and no spend was approved.

The API decision remains open. Direct Groq `openai/gpt-oss-120b` is the lowest-change continuity candidate. Paid Gemini 3.6 Flash and OpenAI GPT-5.6 Luna or Terra are independent comparison lanes. OpenRouter is acceptable for a cross-provider QA matrix only when the exact provider, model, parameters, privacy policy, and fallback behavior are pinned.

See `phase-4-local-automation-report-2026-07-27.md` and `api-provider-assurance-report-2026-07-27.md`.

## Continuation update: security, supply chain, and engineering process

QA continued without changing product files.

The QA branch is four commits behind `develop`. The development-only changes add PDF-to-Markdown conversion, Markdown ingestion, contextual retrieval, and a revised builder. An isolated archive of `develop` compiled 33 Python files and passed Ruff, but functional fixtures failed:

- content before the first recognized Markdown section was discarded;
- `15.1` did not produce subclause metadata;
- a 1,601-character paragraph passed through a 1,500-character chunk limit;
- per-source conversion and ingestion exceptions can be printed and ignored;
- any corpus above 100 Markdown files can be selected;
- an existing cache wins without a source-format or corpus handshake.

Bandit confirmed the executable pickle risk. An offline zizmor audit reported 36 workflow findings, including 12 unpinned Action uses, excessive permissions, persisted checkout credentials, a direct shell-template expansion, and a provider secret outside a protected environment. Limited active-text and Git-blob scans found no candidate secret, but the complete detect-secrets runs timed out and secret-free status is not claimed. A fresh dependency vulnerability audit also timed out twice.

The README claims an MIT license and links to `LICENSE`; no root license, copying, or notice file exists.

The software-process audit found useful prototype practices but no controlled release lifecycle. The supplied OpenCode records declare 100% completion while recording 10 of 12 fully correct answers, treat 11 of 12 as above 97%, mark skipped reranking tasks complete, and provide narrative test status without candidate-bound execution evidence. This supports an “implementation-first and self-certified” assessment. It does not prove that no external process occurred.

The defect register now contains 60 open defects. Phase 5 failed, and release remains blocked.

See `phase-5-security-supply-chain-report-2026-07-27.md`, `software-engineering-process-audit.md`, and `opencode-practices-critique.md`.

## Continuation update: executable RAG+CAG and local load

QA continued under the documentation-only boundary. Five reusable QA-only harnesses were added under `Quality Assurance Officer/tools`; product code and configuration were not changed.

The dirty QA working tree executed a 60-request provider-free matrix through its real router, CAG, persisted docstore, filtered retrieval, BM25 path, context builder, and prompt renderer. A capture runnable replaced the LLM.

Results:

- 41 of 60 cases passed every applicable diagnostic check;
- route expectation passed 59 of 60;
- expected Award detection passed 36 of 38;
- expected Award appeared in context for 33 of 36 applicable cases;
- zero of nine clarification cases were gated;
- all 60 prompts contained one human-role message and no system role;
- prompts ranged from 3,063 to 47,364 characters.

Current `develop` failed before the first request on Windows because the NES loader used the platform default encoding. With `PYTHONUTF8=1` forced only for diagnosis, it passed all applicable checks in 31 of 60 cases, detected 25 of 38 expected Awards, and included the expected Award in 22 of 36 contexts.

Raw semantic retrieval placed the expected Award first for 16 of 36 Award-labelled queries and within the top ten for 24. Exact metadata filtering improved to 33 of 36 but returned no target documents for Clerks and Children’s Services cases.

Only four of the 25 historical hard-evaluation answers passed a weak literal-support comparison with the context retrieved now. Eight of 23 numeric claims and 13 of 46 citation strings were present. This check is weaker than legal review and invalidates treating the historical 87.55% as current release evidence.

A corrected provider-free loopback Gradio run passed eight structural functional checks and completed all 288 timed load requests. At 32 workers:

- throughput was 4.592 requests per second;
- median latency was 5.936 seconds;
- p95 was 7.902 seconds;
- peak RSS was 1,275,621,376 bytes.

No provider latency was present. The run is diagnostic, not a production capacity result.

Natural application import without a provider key failed after loading the CAG and store, exiting after 15.349 seconds. Six injected provider errors confirmed that 429, 413, and rate-limit strings enter the defective fallback, while timeout, 500, and 401 errors propagate from `ask_question`.

The defect register now contains 69 open defects. The supervisor handoff is in `supervisor-handoff-2026-07-27.md`.

See `phase-6-rag-cag-request-and-load-report-2026-07-27.md` and its machine-readable evidence files.
