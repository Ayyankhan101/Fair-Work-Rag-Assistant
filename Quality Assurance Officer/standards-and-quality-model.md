# Standards and quality model

Verified: 27 July 2026.

This project is assessed against several standards because no single standard covers software quality, testing process, web security, accessibility, AI behavior, and legal-information risk.

This is a project test framework, not a claim of ISO certification. Formal certification requires an accredited assessment and access to the full licensed standards where applicable.

## Standards used

| Source | Use in this QA program | Project evidence |
|---|---|---|
| [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) | product quality model | quality gates, measures, and release decision |
| [ISO/IEC/IEEE 29119 series](https://committee.iso.org/sites/jtc1sc7/home/projects/flagship-standards/isoiecieee-29119-series.html) | test process, design, documentation, and reporting | plan, cases, run records, incident records, completion report |
| [ISO/IEC TR 29119-11:2020](https://www.iso.org/standard/79016.html) | AI test-oracle and non-determinism guidance | reviewed gold evidence, repeated runs, model and prompt identity |
| [NIST SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) | secure software development | dependency, secret, build, integrity, and vulnerability controls |
| [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | generative-AI risk management | grounding, harmful output, privacy, monitoring, and incident tests |
| [OWASP ASVS 5.0.0](https://owasp.org/www-project-application-security-verification-standard/) | web security verification | input, error, logging, configuration, dependency, and deployment tests |
| [OWASP Top 10:2025](https://owasp.org/Top10/) | common web risks | security abuse cases |
| [OWASP Top 10 for LLM applications 2025](https://genai.owasp.org/download/43299/?tmstv=1731900559) | LLM-specific abuse cases | prompt injection, data leakage, excessive agency, and output handling |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | user-interface accessibility | Level A and AA checks plus selected AAA checks |
| [Fair Work award list](https://www.fairwork.gov.au/employment-conditions/awards/list-of-awards) | authoritative Award scope | dated list of 122 Award IDs |
| [Fair Work NES page](https://www.fairwork.gov.au/employment-conditions/national-employment-standards) | authoritative NES scope | entitlement and source-freshness checks |

NIST SP 800-218 version 1.1 is the current final SSDF used here. Version 1.2 was still a draft on the verification date.

## Quality dimensions

The ISO/IEC 25010 model is applied to the whole product, including data and external services.

| Dimension | Meaning for this system | Main measure |
|---|---|---|
| Functional suitability | the system covers the required Awards and NES and returns the requested information | requirement coverage and answer correctness |
| Performance efficiency | response time, throughput, memory, storage, and provider use stay within limits | p50, p95, maximum, resource use, and cost |
| Compatibility | supported Python, operating systems, browsers, and provider versions work together | environment matrix pass rate |
| Interaction capability | users can understand, operate, and recover from the interface | task completion, error recovery, WCAG result |
| Reliability | repeated requests, failures, restarts, and stale state do not corrupt results | error rate, recovery time, repeatability |
| Security | secrets, data, build artifacts, prompts, and output are protected | ASVS, SSDF, and LLM abuse-case pass rate |
| Maintainability | changes are testable, traceable, and isolated | change impact, test coverage, rebuild evidence |
| Flexibility | deployment, provider, corpus, and model can change without hidden breakage | configuration and portability tests |
| Safety | wrong or unsupported legal-information output is prevented or clearly stopped | zero unsupported high-impact claims |

The following project-specific dimensions are mandatory:

- corpus identity and freshness;
- source and clause traceability;
- retrieval accuracy;
- claim-level grounding;
- ambiguity handling;
- legal-information boundaries;
- privacy of user questions;
- cost per successful grounded answer;
- environmental and operational cost of rebuilds;
- transparent evidence provenance.

## Evidence states

Every requirement and test uses one of these states.

| State | Meaning |
|---|---|
| Observed | directly confirmed from a file, command, rendered page, or official source |
| Inferred | conclusion based on observed evidence; the reasoning is recorded |
| Passed | the defined procedure ran and every pass condition was met |
| Failed | the procedure ran and at least one pass condition was not met |
| Blocked | a required input, environment, authority, or source was unavailable |
| Not run | no valid execution occurred |
| Invalid | a run occurred but a stop condition made its result unusable |
| Accepted risk | an owner approved a known failure with scope and expiry |

“Not found” is not automatically “does not exist.” Search scope and limitations must be recorded.

## Release rule

Release is blocked when any of the following is true:

1. An S0 or S1 defect is open.
2. An official Award is absent or misidentified.
3. The source version or corpus checksum is unknown.
4. CAG and RAG are not proven to use the same corpus revision.
5. A pay, hours, leave, break, coverage, termination, or penalty claim lacks direct support.
6. A citation does not resolve to the text supporting the claim.
7. Insufficient evidence produces a guessed answer.
8. Prompt injection can change source-grounding rules.
9. User data can be sent to an external provider without an approved privacy basis.
10. Deployment has no defined authentication, limits, logging, rollback, or incident process.

## Accuracy and cost rule

Cost is optimized only after safety and correctness gates pass.

The comparison unit is one successful grounded answer, not one request. Failed, unsupported, retried, or uncited answers still count toward cost.

For each candidate configuration, record:

- retrieval recall at 3 and 5;
- claim grounding and citation support;
- reviewed answer correctness;
- input, cached-input, and output tokens;
- embedding calls;
- provider retries and failures;
- p50 and p95 latency;
- peak memory;
- vector-store and cache size;
- cold-start time;
- rebuild duration;
- estimated monthly cost at 100, 1,000, 10,000, and 100,000 questions.

A configuration is eligible for cost comparison only when mandatory coverage is 100%, claim grounding is 100%, citation support is 100%, and current-rate questions are 100% correct.

## Test independence

The answer produced by the system is never used as its own expected result.

Gold evidence must contain:

- the official source URL;
- Award ID or NES section;
- source publication or update date;
- clause or section;
- exact supporting text or a stable text hash;
- expected qualifiers and exceptions;
- reviewer and review date.

Model-based grading may assist triage. It cannot be the sole release oracle for legal-information answers.

