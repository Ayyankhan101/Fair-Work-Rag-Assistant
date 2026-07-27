# Release report: 2026-07-27

## Decision

Release blocked.

The application is not ready to provide relied-upon Fair Work answers. The current dirty working tree passes local static and unit checks, but those checks include untracked tests and unaccepted pre-boundary code changes. Corpus identity, source reproducibility, evidence provenance, answer grounding, security, accessibility, performance, cost, and deployment readiness do not pass.

## Evidence summary

| Gate | Result | Reason |
|---|---|---|
| Compilation | pass | Python source compiles |
| Lint | pass on dirty working tree | Ruff 0.12.0 |
| Formatting | pass on dirty working tree | Ruff 0.12.0 |
| Unit tests | pass on dirty working tree | 16 tests; all test files untracked |
| Clean isolated imports | pass | Python 3.11; 95 packages; 80.202 seconds |
| Dependency resolution | pass with reproducibility gap | unpinned graph resolves; no lock |
| Known-vulnerability audit | pass with limitation | no known issue on 2026-07-27 resolved graph |
| Shell syntax | fail | three of four scripts fail `bash -n` |
| Candidate control | fail | 20 modified tracked files; 38 untracked files |
| Development alignment | fail | QA is four commits behind changes to conversion, ingestion, storage, and prompting |
| Mandatory Award coverage | fail | MA000095 and MA000121 missing |
| Award identity | fail | MA000002 labelled as Workplace Relations Act |
| Reproducibility | fail | source PDF directory absent |
| Metadata completeness | partial | required fields exist; page and source version do not |
| Duplicate content | fail | 1,251 extra exact-text chunks |
| Evaluation provenance | fail | commit, corpus, model, prompt, and time absent |
| Prompt hierarchy | fail | policy, evidence, and question are one human-role message |
| Model continuity | fail | both configured model IDs have a 16 August 2026 developer-tier shutdown date |
| Answer grounding | not proven | current scorer checks words, patterns, and length |
| Security | fail | executable pickle, 36 workflow findings, and untested injection/provider paths |
| Development ingestion | fail | isolated fixture loses preamble and `15.1` identity |
| Licensing | fail | README links to a nonexistent MIT license file |
| Engineering process | fail | self-certified completion, invalid acceptance math, and no independent sign-off |
| RAG+CAG request matrix | fail | 41 of 60 dirty-QA cases; 31 of 60 forced-UTF-8 development cases |
| Clarification and answerability | fail | zero of nine cases gated |
| Raw semantic Award retrieval | fail | 16 of 36 top-1; 24 of 36 top-10 |
| Historical claim support | fail | four of 25 pass a weak literal-support check |
| Local HTTP load | diagnostic fail | no errors, but provider-free 32-worker p95 7.902 seconds and 1.276 GB peak RSS |
| Accessibility | not run | no WCAG evidence |
| Performance and cost | not run | isolated setup timing only; no application or provider measurement |
| Deployment and recovery | not run | no candidate environment supplied |

## Changes made before the documentation-only boundary

The following are proposed working-tree changes, not accepted production fixes:

- corrected CI import targets;
- declared missing runtime dependencies;
- added offline config, router, CAG, and prompt-safety tests;
- fixed Windows NES decoding;
- stopped CAG cleaning from deleting entitlement headings;
- made route selection control context construction;
- removed prompt rules that forced unsupported answers;
- added prompt-injection and legal-advice constraints;
- fixed high-impact Award alias collisions;
- stopped UI exception disclosure;
- stopped silent append to a completed vector store;
- made ingestion fail when any source fails;
- added a deterministic repository audit.

After the user clarified the scope, no further product-code or root-configuration changes were made. Later work is QA documentation only.

The working-tree prompt remains unacceptable even with the added wording because it is still rendered as a human-role message, has no strict claim schema, does not version the prompt, and cannot enforce source support.

An operational model replacement must be qualified before 16 August 2026. Provider migration guidance is not qualification evidence.

## Required next run

1. Select the intended development lineage and exact candidate commit.
2. Decide whether to accept, reject, or separate the pre-boundary working-tree patch and reconcile QA to the candidate.
3. Materialize and checksum the 122-source corpus.
4. Replace MA000002 and add MA000095 and MA000121.
5. Revise the requirements against the current NES list.
6. Add page and source-version metadata.
7. Rebuild into a new store directory.
8. Run the corpus audit until no S1 failure remains.
9. Implement and qualify separate system and user messages, strict structured claims, and deterministic claim validation.
10. Qualify replacement model/prompt pairs before the configured model shutdown.
11. Execute the documented routing, retrieval, answer, security, UI, accessibility, performance, cost, and deployment cases in order.
12. Issue a new report tied to the tested commit and artifacts.
