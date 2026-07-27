# QA method research

## Method selected for this project

This project needs risk-based software QA, data quality assurance, AI evaluation, legal-source control, security testing, accessibility review, and operational verification.

Ordinary unit testing is necessary but insufficient because the answer depends on changing external authorities, a generated index, nondeterministic models, and user-specific ambiguity.

## Governing references

| Reference | Use in this QA system |
|---|---|
| [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) | product quality characteristics and coverage |
| [ISO/IEC/IEEE 29119 series](https://committee.iso.org/sites/jtc1sc7/home/projects/flagship-standards/isoiecieee-29119-series.html) | test process, documentation, techniques, and evidence |
| [ISO/IEC TR 29119-11](https://www.iso.org/standard/79016.html) | AI-system testing considerations |
| [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | secure development and supply-chain practices |
| [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | govern, map, measure, and manage AI risk |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | application-security verification requirements |
| [OWASP Top 10:2025](https://owasp.org/Top10/) | current web-application risk coverage |
| [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/download/43299/?tmstv=1731900559) | prompt, output, model, and retrieval threats |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | user-interface accessibility |
| [Fair Work Award list](https://www.fairwork.gov.au/employment-conditions/awards/list-of-awards) | authoritative Award scope |
| [Fair Work NES](https://www.fairwork.gov.au/employment-conditions/national-employment-standards) | authoritative NES scope |

This is an internal conformance-oriented method. It is not an ISO certification audit and does not imply certification.

## Quality characteristics

The nine ISO/IEC 25010:2023 product-quality characteristics are applied as follows:

| Characteristic | Project interpretation |
|---|---|
| Functional suitability | correct Award, entitlement, calculation, citation, clarification, and refusal |
| Performance efficiency | build, retrieval, generation, memory, capacity, and cost |
| Compatibility | supported Python, operating system, browser, provider, and document formats |
| Interaction capability | understandable questions, answers, errors, focus, and accessibility |
| Reliability | deterministic artifacts, retries, recovery, availability, and repeatability |
| Security | secrets, input, output, dependencies, prompt injection, privacy, and tampering |
| Maintainability | modular tests, traceability, versioned configuration, and diagnosable failures |
| Flexibility | controlled provider, model, corpus, and deployment substitution |
| Safety | prevention of unsupported high-impact employment-law guidance |

## Risk model

Risk priority is:

```text
severity of harm × likelihood × detectability difficulty × exposure
```

Examples:

| Failure | Risk |
|---|---|
| wrong pay rate with confident citation | highest |
| wrong Award coverage | highest |
| stale NES entitlement | highest |
| fabricated clause | highest |
| source prompt injection | high |
| missing clarification | high |
| provider shutdown | high |
| slow non-critical response | medium |
| cosmetic spacing | low unless it blocks accessibility |

High-risk cases receive stricter thresholds, more repetitions, independent review, and no accepted failure allowance.

## Test design techniques

Use:

- equivalence partitioning for query types, employment types, and routes;
- boundary analysis for rates, dates, ages, hours, token sizes, and limits;
- decision tables for Award/NES interactions and clarification rules;
- state-transition testing for build, resume, publish, load, rollback, timeout, and retry;
- pairwise and combinatorial testing for browsers, platforms, models, and configurations;
- metamorphic testing for paraphrases, formatting, irrelevant text, and context order;
- property-based testing for IDs, schemas, Unicode, and deterministic transformations;
- mutation testing for test-suite sensitivity after a clean candidate exists;
- fault injection for missing files, corrupt indexes, provider errors, and partial writes;
- exploratory testing for unfamiliar legal-language and UI failure modes;
- adversarial testing for prompt injection and confident unsupported answers.

## Evidence hierarchy

From strongest to weakest:

1. retained raw input and output tied to an immutable candidate;
2. deterministic machine result with checksummed dependencies;
3. independent human review against an authoritative source;
4. reproducible integration or browser observation;
5. source inspection;
6. historical log without candidate identity;
7. documentation claim;
8. recollection or assertion.

Lower evidence cannot override a failed higher-level gate.

## Independence rules

The same person may create and run tests, but high-impact acceptance needs independent review.

The developer of a prompt or gold answer cannot be its only approver. A model that produced an answer cannot be its only judge. A provider benchmark cannot establish fitness for this corpus.

## Entry and exit gates

Each phase has:

- controlled inputs;
- named entry conditions;
- exact commands or procedure;
- expected results;
- retained evidence;
- defect and stop rules;
- exit criteria;
- owner and approval.

The phase plan is in `phase-by-phase-execution-plan.md`. Starting expensive generation tests before source and retrieval gates pass creates invalid evidence and unnecessary cost.

## Change-impact testing

| Change | Minimum rerun |
|---|---|
| source file or parser | source, parsing, store, retrieval, answer, regression |
| embedding or index | store, retrieval, answer, performance |
| router or aliases | routing, retrieval, answer, ambiguity |
| prompt | answer, citation, safety, repetition |
| model or provider | full answer, safety, cost, latency, privacy |
| dependency | static, unit, integration, vulnerability, deployment |
| UI | UI, accessibility, privacy, browser, session |
| deployment | security, performance, recovery, observability |

Changes to an upstream artifact invalidate downstream evidence unless equivalence is proved.

## Continuous QA

For each accepted change:

1. run deterministic offline gates;
2. verify corpus identity;
3. run affected retrieval regression;
4. run a cost-bounded answer sentinel set;
5. compare against the accepted baseline;
6. block on any S0/S1 regression;
7. archive results with the candidate.

In production:

- sample and review real queries under an approved privacy policy;
- detect new ambiguity and no-answer cases;
- monitor source changes and provider deprecations;
- measure unsupported-claim reports;
- track latency, errors, retries, and cost;
- add confirmed incidents to regression sets;
- never place raw personal employment details in evaluation data without lawful approval and de-identification.

## Current execution status

The method has produced 485 uniquely identified test specifications and more than 1,000 parameterized executions. They are specifications, not pass evidence.

Step 1 found a blocked release. Source reachability has been checked, but source acceptance still fails. Phases that require an accepted corpus remain invalid to complete.
