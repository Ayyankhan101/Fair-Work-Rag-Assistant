# QA supervisor handoff

Date: 27 July 2026

Prepared status: assessment package ready for review; product release blocked

Latest state: QA product changes were preserved as patches and removed from the product tree. Every non-QA path now matches fork point `3e91e9e`. Read `developer-handoff-after-qa-2026-07-27.md` and `quick-qa-iteration-after-cleanup-2026-07-27.md` before the earlier phase reports.

## Supervisor decision requested

Do not approve public or relied-upon use.

Approve the QA package as a documented prototype assessment only. Require engineering remediation and a new immutable candidate before release qualification.

## One-minute summary

| Area | Result |
|---|---|
| repository and documentation audit | completed |
| test specifications | 485 unique cases defined |
| open defects | 70 |
| current candidate | none; product tree restored to fork point and current `develop` remains unqualified |
| latest local unit tests | 2 of 16 methods passed against restored baseline |
| earlier dirty-QA unit tests | 16 of 16 passed; historical and reverted |
| natural Windows baseline matrix | fails before request one |
| forced-UTF-8 baseline matrix | 31 of 60 diagnostic passes |
| earlier dirty-QA matrix | 41 of 60; historical and reverted |
| semantic expected Award | 16 of 36 top-1; 24 of 36 top-10 |
| clarification cases | 0 of 9 |
| historical-answer literal support | 4 of 25 questions |
| provider-free HTTP | 288 of 288 corrected load requests completed |
| 32-worker provider-free HTTP | 5.936 s median, 7.902 s p95, 1.276 GB peak RSS |
| live LLM answer testing | blocked; no credential or approved spend |
| legal review | not supplied |
| release decision | blocked |

## Highest-risk observations

1. Mandatory source identity is not controlled. Awards are missing or mislabelled.
2. Current `develop` loses Markdown content and cannot naturally load NES text on Windows.
3. Clerks and Children’s Services routing can return zero target-Award context.
4. Negated, ambiguous, typo, nonsense, and under-specified questions are not safely clarified.
5. Raw semantic retrieval misses the expected Award in 12 of 36 top-10 cases.
6. All captured prompts use one human-role message rather than a system/user boundary.
7. The full 38,482-character NES cache is inserted for every NES candidate.
8. Historical accuracy claims do not survive even a weak current-context support check.
9. Provider fallback changes prompt structure and repeats the question.
10. The engineering process self-declared completion despite failed objectives and contradictory evidence.

## Evidence that passed

- repository and supplied-artifact inventory;
- Python and documentation static checks at the recorded diagnostic points;
- exact product-tree equality to the fork point outside the QA folder;
- Python syntax parsing for 29 of 29 checked product and QA files;
- 16 local tests on the earlier dirty QA state, now historical;
- 60 of 60 dirty-QA chains executed with a capture model;
- 10 of 10 repeated semantic searches produced identical ordering;
- 300 of 300 in-process concurrent semantic searches completed;
- eight of eight loopback HTTP functional checks behaved as implemented;
- 288 of 288 corrected loopback load requests completed without request errors;
- all QA evidence JSON parses;
- no candidate secret was found in the completed limited scans.

These passes do not offset the blocking failures.

## Evidence unavailable

- an exact accepted development/release commit;
- checksummed raw 122-Award plus NES corpus;
- approved legal gold answers;
- live Groq, Gemini, OpenRouter, or OpenAI results;
- provider cost and failure behavior;
- production authentication and privacy acceptance;
- full accessibility, soak, recovery, and deployment evidence;
- independent sign-off.

## Documents to review first

1. `developer-handoff-after-qa-2026-07-27.md`
2. `qa-branch-change-control-record-2026-07-27.md`
3. `quick-qa-iteration-after-cleanup-2026-07-27.md`
4. `test-and-metrics-register.md`
5. `quick-glance-release-status.md`
6. `final-qa-report-2026-07-27.md`
7. `defect-register.md`
8. `transparency-log.md`

Machine-readable run evidence is under `evidence/`. Reusable QA-only harnesses are under `tools/`.

## Required engineering response

Engineering should return:

1. one immutable candidate commit based on the intended development lineage;
2. the exact accepted source manifest and hashes;
3. corrected canonical Award-ID joins;
4. cross-platform UTF-8 ingestion;
5. a clarification and insufficient-evidence path;
6. role-separated prompts and deterministic claim validation;
7. qualified retrieval thresholds;
8. a locked dependency graph and pinned Actions;
9. approved provider, privacy, timeout, cost, and observability configuration;
10. tracked executable tests linked to the defect closures.

## Required review response

The supervisor should record:

- whether the product remains a prototype;
- which branch and patch are authorized for remediation;
- named engineering, QA, legal, security/privacy, and release owners;
- approved provider test credentials and maximum spend, if live testing is authorized;
- accepted performance and cost thresholds;
- whether any residual defect exception is allowed.

## Sign-off statement

This package may be submitted as evidence of extensive QA work.

It must not be submitted as evidence that:

- all 485 tests passed;
- answer accuracy is 87.55% or above;
- the current development branch passed;
- the system is legally correct, secure, accessible, private, scalable, or production-ready;
- release QA is complete.

The accurate statement is:

> QA executed all currently feasible local diagnostics under the documentation-only boundary. Blocking candidate, corpus, legal, provider, and deployment evidence remains unavailable. Release is not approved.
