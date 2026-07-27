# Previous documentation critique

## Decision

The previous project documentation is not a reliable source of release truth.

It contains useful implementation history, but counts, completion states, quality claims, source scope, model status, and operating instructions conflict with the repository and with one another.

## Root README

The current working-tree `README.md` is substantially more honest than the committed documentation. It states that release is blocked and identifies missing Awards, provenance gaps, privacy limits, and QA commands.

It still cannot be accepted as HEAD documentation because:

- it is a modified tracked file in a dirty working tree;
- it refers to untracked `tests/`, `qa/`, and QA reports;
- its setup cannot rebuild the store because `data/awards/` is absent;
- dependencies are not locked;
- its “builder now stops” statement describes an unaccepted code change;
- the documented test commands do not describe the committed branch state;
- it does not mention the 16 August 2026 model shutdown.

Required action: regenerate the final README only after an immutable candidate and accepted QA artifacts exist.

## `.opencode` records

### `context.md`

Problems:

- reports 87.5% accuracy as a current fact without evidence identity;
- declares a checkpoint resume rule that can preserve a corrupt or mismatched store;
- directs use of an automation script that stages all files, merges, deletes a branch, and switches branches;
- contains mojibake;
- treats a local workflow preference as a safety control.

### `integration-status.md`

Problems:

- says all tests pass and there are no sync issues;
- calls three retrieval queries, a five-field check, 12 questions, and seven integration checks a full pass;
- does not identify commit, corpus, model, prompt, environment, or raw output;
- provides no negative, injection, load, accessibility, or recovery result;
- contains mojibake.

### `quality-plan.md`

Useful points:

- recognizes bad slug mappings, retrieval weaknesses, chunking risk, reranking, and prompt risk.

Problems:

- treats 11/12 as potentially greater than 97%; 11/12 is 91.67%;
- predicts percentage gains without controlled evidence;
- proposes a generic web-search reranker trained outside this legal corpus;
- tells the prompt to use context aggressively, which can increase unsupported answers;
- does not separate source, retrieval, answer, and citation metrics;
- lacks cost, privacy, security, date, and legal-review gates;
- assumes all 129 mappings are the release scope without reconciling the official 122 list.

### `status.md`

Problems:

- declares 14/14 complete, zero issues, and execution complete;
- reports 16,622 documents while the current store contains 16,692;
- reports 129 PDFs plus NES while other documents say 130 Awards;
- says the full integration passes despite no tracked tests at HEAD;
- omits missing MA000095 and MA000121 and the MA000002 mislabelling;
- contains mojibake.

### `todo.md`

Problems:

- marks reranking “completed” even though it was skipped;
- marks 100% task completion while the content score remains approximately 83%;
- treats a missing Clerks source as a note rather than a release blocker;
- does not require immutable evidence or independent review;
- contains mojibake.

### `work-log.md`

Problems:

- records `.env` as modified with a Groq key, which is sensitive operational information even without the key value;
- reports no pending integration;
- repeats weak pass claims;
- conflicts with current chunk counts;
- does not contain checksums or immutable run IDs;
- contains mojibake.

Required action: archive `.opencode` as historical process notes or replace it with generated status tied to a candidate. Do not use it for release decisions.

The dedicated `opencode-practices-critique.md` now records 15 specific practice failures, their evidence, why each practice is unsound, and the required replacement. `software-engineering-process-audit.md` places those failures in the wider lifecycle without claiming that missing repository artifacts prove no external process occurred.

## `Cortex-insight-analytics` vault

### Project and architecture notes

Problems:

- describe 130 Awards, while the official in-scope list contains 122;
- state 87.5% quality without provenance;
- describe CAG as 100% recall even though loading all contaminated NES text is not a recall measurement;
- state Groq is fast, cheap, and good quality without a benchmark or price snapshot;
- omit privacy, prompt injection, source versioning, failure modes, accessibility, deployment, and recovery;
- do not compare architecture alternatives or record rejected options;
- contain mojibake.

### Evaluation notes

Problems:

- `Evaluation Results.md` says 25/25 content pass and 89.3% average;
- persisted hard results report 23 content passes of 25 and 87.5467%;
- `Hard Eval Suite.md` scores keywords, regex patterns, and general quality, not legal claims;
- a 70% per-question threshold permits a materially wrong answer;
- evaluation does not record commit, corpus, model, prompt, or run time;
- a partial vector-store explanation is asserted without a controlled rerun;
- old H01 content is stale relative to the current store.

### Progress and next-step notes

Problems:

- say retrieval is working without clause-level recall evidence;
- treat deployment as the next step after a score target;
- omit corpus acceptance, legal review, security, privacy, accessibility, cost, rollback, and operational approval;
- promise 95%+ after a rebuild without experimental evidence.

Required action: label the entire vault historical. Replace quality dashboards with generated evidence, not manually copied percentages.

## Repository skill documentation

Files:

- `skills/fair-work-rag/SKILL.md`;
- `skills/fair-work-rag/references/architecture.md`;
- `skills/fair-work-rag/references/optimization.md`;
- `skills/fair-work-rag/references/troubleshooting.md`.

Problems:

- hard-code both Groq models that are scheduled for shutdown;
- repeat unproved “100% recall” and 87.5% accuracy claims;
- call the 70B model production without a current qualification result;
- give rate-limit values and reset behavior without a dated provider source;
- describe 40+ aliases as broad Award coverage even though 122 Awards are required;
- recommend increasing `k` as a generic retrieval fix;
- tell operators to delete `data/docs_cache.pkl`, contrary to the stated never-rebuild rule and without source reproducibility;
- contain destructive or platform-specific commands without recovery checks;
- contain mojibake.

Required action: do not distribute or install this skill until the model, commands, evidence, and safety rules are revised and tested.

## Requirements PDF

Problems:

- NES scope is stale compared with the current Fair Work page;
- quality targets do not define claim, citation, date, and safety measures;
- non-functional requirements are not measurable enough for release;
- source acquisition, manifest, privacy, retention, residency, authentication, accessibility, recovery, and cost requirements are missing or incomplete;
- page 6 has a heading/body collision;
- page 7 is mostly blank.

Required action: issue a controlled requirements revision with requirement IDs, rationale, owner, measurable criteria, and legal review.

## Architecture DOCX

Problems:

- architecture claims were not backed by benchmark, cost, or failure evidence;
- generated artifacts and source-version handshakes are not specified;
- trust boundaries and provider data flows are incomplete;
- no prompt-role design, output schema, claim verifier, or trace schema is defined;
- no migration plan exists for model deprecation;
- visual layout could not be verified in this environment.

Required action: revise after architecture decisions are tested, then render and inspect every page.

## Discarded prototype

The discarded prototype is useful historical material, not product evidence.

Problems:

- its source and evaluation data represent a different implementation;
- Docker and dependency files are not evidence that the active product deploys;
- its evaluation result cannot be transferred to the active corpus;
- keeping it under the QA SUT directory increases the chance that reviewers confuse historical and active artifacts.

Required action: move it to a clearly labelled archive outside the active SUT evidence tree.

## User and operational documentation gaps

No accepted document explains:

- what the assistant can and cannot decide;
- how to verify a citation;
- what user facts are sent to the model provider;
- data retention and deletion;
- how to report a harmful answer;
- how source dates affect an answer;
- how to interpret a clarification or insufficient-evidence response;
- supported browsers, languages, and accessibility;
- incident, rollback, restore, and outage procedures;
- model-deprecation response;
- cost limits and billing alerts.

## Critique of the current QA documentation

The QA set is more controlled than the previous notes, but it also has limitations:

- 485 cases are specifications, not 485 passed tests;
- 16 passing unit tests are untracked and cannot qualify HEAD;
- no employment-law expert has approved gold claims;
- the live Award crawl did not retain raw responses or per-page hashes;
- the first live-crawl oracle incorrectly required the Award ID in the title heading;
- the architecture DOCX was not visually rendered;
- production, browser, provider, load, accessibility, privacy, and recovery tests remain unexecuted;
- some evidence JSON is an aggregate reconstruction, not raw capture;
- several reports overlap and require the README index for navigation;
- the proposed prompt is deliberately unimplemented and unqualified.

These limitations are release-significant and must remain visible.

## Documentation acceptance rules

Future documentation must:

1. identify the candidate, corpus, model, prompt, environment, author, and date;
2. distinguish observation, inference, proposal, and accepted decision;
3. link every metric to raw evidence;
4. use one generated source of truth for counts and status;
5. retain failed and blocked results;
6. state scope and limitations beside each conclusion;
7. avoid words such as complete, accurate, secure, production, or verified without named gates;
8. archive superseded documents;
9. pass encoding, link, structure, and render checks;
10. receive independent review for legal and high-impact claims.
