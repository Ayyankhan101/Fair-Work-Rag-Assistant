# QA plan

## Exit criteria

QA is complete when every blocking gate below passes from a clean checkout, evidence is stored with the run date and commit SHA, and no severity 0 or severity 1 defect remains open.

| Gate | Area | Pass criteria |
|---|---|---|
| G0 | Reproducibility | setup commands work on Python 3.11; CI commands match real symbols |
| G1 | Static quality | `compileall`, `ruff check`, and `ruff format --check` pass |
| G2 | Source corpus | expected award count is defined; every file is readable, unique, and mapped to a valid award |
| G3 | Ingestion | every source produces chunks; required metadata is present and clause/page values are plausible |
| G4 | Stores | vector count matches the manifest; cache/index versions identify their source corpus |
| G5 | Router | labelled CAG, RAG, combined, ambiguous, and unrelated queries route as expected |
| G6 | Retrieval | each award has at least one labelled query; target award appears in top-k; clause tests meet the agreed recall threshold |
| G7 | Answers | grounded content, citation, refusal, ambiguity, and legal-advice safeguards pass |
| G8 | UI/API | startup, normal query, missing key, corrupt store, empty input, and error messages pass |
| G9 | Performance | latency and concurrency thresholds are measured and documented |
| G10 | Security/privacy | unsafe deserialization, secrets, uploads, logs, prompt injection, and dependency findings are resolved or accepted |
| G11 | Regression | offline gates run on pull requests; API-dependent evaluation is scheduled and stores comparable results |
| G12 | Release | requirements traceability, defect list, residual risks, and release recommendation are signed off |

## Phase 0: establish the baseline

1. Record commit SHA, branch, Python version, dependency state, and data file counts.
2. Run the same commands used by `.github/workflows/ci.yml`.
3. Compare CI imports with functions defined in `src/`.
4. Validate stored evaluation result schemas and timestamps.
5. Record failures in a dated baseline report.

Pass: another developer can reproduce every reported result.

## Phase 1: make offline quality gates reliable

1. Fix CI symbol names or add intentional compatibility aliases.
2. Fix lint and formatting failures.
3. Add `pytest` and unit tests for `src/config.py`, `src/router.py`, `src/cag.py`, chunking, metadata, and answer-format validation.
4. Separate offline tests from tests that require `GROQ_API_KEY`.
5. Make Windows and Linux commands available; current shell scripts only target Unix paths.

Pass: G0 and G1 pass without an API key.

## Phase 2: audit the corpus before retrieval

1. Define the authoritative expected award list and count. Project documents say 122; repository notes say 129 or 130.
2. Check PDF readability, page count, checksum, duplicate content, filename, award title, Award ID, and source URL.
3. Fail generic extracted titles such as `Award 2020`, malformed titles, and raw IDs used as names.
4. Verify NES completeness against the entitlement list in the requirements.
5. Create a corpus manifest with source version and ingestion timestamp.

Pass: G2 passes with zero unknown, duplicate, unreadable, or unmapped sources.

## Phase 3: verify ingestion and storage

1. Test clause extraction on headings, schedules, tables, page breaks, and Awards with non-standard titles.
2. Assert required metadata on every chunk.
3. Test chunk size, overlap, duplicate chunks, empty chunks, and boundary preservation.
4. Rebuild the document cache and vector store from the audited corpus.
5. Compare source counts, chunk counts, metadata distributions, and store counts.
6. Add a version contract so CAG and RAG cannot load different corpus revisions.

Pass: G3 and G4 pass with a rebuild from source.

## Phase 4: test routing and retrieval

Build labelled test sets for:

- every Award;
- all NES entitlement areas;
- CAG-only questions;
- Award-only RAG questions;
- combined NES and Award questions;
- ambiguous occupations and employers;
- paraphrases, misspellings, abbreviations, and adversarial wording;
- questions with no answer in the corpus.

Measure route accuracy, award recall at k, clause recall at k, reciprocal rank, and cross-award contamination.

Pass: G5 and G6 meet thresholds set from a reviewed labelled set. A stored model answer is not ground truth for retrieval.

## Phase 5: test answers

Score each answer separately for:

| Dimension | Check |
|---|---|
| Grounding | every factual claim is supported by returned context |
| Correctness | values, qualifiers, employee type, dates, and exceptions match source text |
| Citation | Award/NES name and clause/section identify the supporting source |
| Completeness | the answer includes required conditions and exceptions |
| Refusal | missing evidence produces an insufficient-information response |
| Ambiguity | multiple possible Awards are named or clarification is requested |
| Safety | output does not present unsupported legal advice |
| Format | required five-part response is present without hiding content failures |

Use deterministic source assertions where possible. Use human review for legal qualifiers and ambiguous scenarios.

Pass: G7 meets the agreed per-difficulty thresholds and has zero unsupported high-impact answer.

## Phase 6: UI, failure, performance, and security tests

Test startup and query flows with:

- valid and missing API keys;
- missing, stale, and corrupt stores;
- empty, long, Unicode, and injection-style questions;
- provider timeouts, rate limits, and malformed responses;
- concurrent users and repeated cache hits;
- dependency and secret scans;
- upload validation if uploads are enabled.

Record p50, p95, and maximum latency separately for CAG, RAG, and combined routes. Record error rate and provider usage.

Pass: G8 through G10 pass against written thresholds.

## Phase 7: automation and release evidence

1. Run offline gates on every pull request.
2. Run the labelled retrieval suite after corpus, chunking, embedding, or retriever changes.
3. Run API-dependent answer evaluation on a schedule and before release.
4. Store the commit SHA, corpus version, model, prompt version, configuration, and raw results.
5. Publish a release report with open defects and residual risks.

Pass: G11 and G12 pass.

## Defect severity

| Severity | Meaning | Release rule |
|---|---|---|
| S0 | data loss, secret exposure, or unsafe legal answer likely to cause harm | stop work and release |
| S1 | wrong award/entitlement, fabricated citation, broken build, or major corpus gap | blocks release |
| S2 | limited incorrect result, degraded retrieval, or failure-path defect | fix or document acceptance |
| S3 | cosmetic, documentation, or low-impact maintainability issue | may defer with owner |

## Immediate queue

| Order | Work item | Evidence |
|---|---|---|
| 1 | Repair CI imports and static checks | clean CI-equivalent local run |
| 2 | Resolve authoritative award count and bad mappings | corpus audit with zero unknown names |
| 3 | Add offline unit-test foundation | pytest report |
| 4 | Add per-award retrieval coverage | labelled test matrix and metrics |
| 5 | Strengthen answer and citation scoring | raw results plus reviewed failures |
| 6 | Add performance, failure, and security suites | dated reports |
| 7 | Produce release traceability report | gate table and sign-off |
