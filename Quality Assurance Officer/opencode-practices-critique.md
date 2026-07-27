# OpenCode practices critique

Date: 27 July 2026

## Scope and attribution rule

This document critiques the work products under `.opencode/` and the automation they prescribe. It does not claim that every repository defect was caused by OpenCode, identify which person or tool authored each line, or judge the OpenCode product generally.

The fair attribution is:

> The supplied OpenCode records contain specific planning, validation, safety, and documentation mistakes. Where authorship or execution cannot be proven, the mistake is attributed to the recorded practice, not to an unseen actor.

## What the OpenCode work did reasonably

- separated ingestion, retrieval, routing, model, and UI concerns;
- maintained a visible task list, status file, work log, and context file;
- recognized slug mapping, retrieval, chunking, and model-rate-limit problems;
- introduced hybrid retrieval and considered reranking;
- added checkpointing for a long-running store build;
- added CI, dependency audit, CODEOWNERS, and PR workflow concepts;
- recorded an imperfect 10-of-12 result instead of changing that number to 12-of-12.

These are useful prototype practices. They are not enough to substantiate the completion and accuracy claims.

## Major mistakes

### OC-001: declared completion despite a failed objective

Evidence:

- `.opencode/status.md:4-7` says 100% complete, zero issues, and complete execution.
- `.opencode/status.md:12` says only 10 of 12 answers are fully correct.
- `.opencode/todo.md:39` marks above-90% verification complete.
- `.opencode/todo.md:59` records approximately 83% content accuracy.

Why this is wrong: completion status must follow the acceptance result. The recorded objective failed.

Correct practice: reopen or fail the milestone, record the defect, and block downstream claims until a new immutable run passes.

### OC-002: used mathematically invalid acceptance language

Evidence: `.opencode/quality-plan.md:6` and `:133` say an above-97% target can be met by 11 of 12 correct.

Why this is wrong: 11 divided by 12 is 91.67%. A 12-case set also has an 8.33-point resolution and cannot measure 97% with useful precision.

Correct practice: define the population, sample size, confidence method, per-category minimums, and exact pass calculation before execution.

### OC-003: optimized against safe abstention

Evidence:

- `.opencode/quality-plan.md:25-27` treats “not specified” as the problem.
- `.opencode/quality-plan.md:98-101` directs the model not to say information is missing.
- `.opencode/quality-plan.md:134` requires all answers to be substantive.
- `HEAD:src/rag.py` consequently forces confident figures and forbids insufficient-evidence language.

Why this is wrong: for legal information, unsupported specificity is more dangerous than a controlled refusal.

Correct practice: measure answerability first, require source support for each atomic claim, and reward correct abstention.

### OC-004: counted skipped work as completed work

Evidence: `.opencode/todo.md:48-50` checks reranking implementation and optimization while saying both were skipped.

Why this is wrong: a skipped task is neither implemented nor tested.

Correct practice: mark it “not done” or “decision: rejected,” link the decision record, explain evidence, and adjust dependencies and risks.

### OC-005: used “unit test pass” as an unsupported file label

Evidence: `.opencode/work-log.md:7-16` labels source files, `.env`, and `requirements.txt` as unit-test passes without test IDs or results.

Why this is wrong: test evidence belongs to a run against behavior, not to an arbitrary file row. `.env` cannot meaningfully be called a unit-test pass.

Correct practice: record run ID, commit, test name, command, environment, fixture, oracle, output, duration, and result artifact.

### OC-006: treated format compliance as a large part of correctness

Evidence: status repeatedly leads with 12-of-12 format pass while only 10 answers are correct.

Why this is wrong: a five-heading response can be perfectly formatted and legally wrong. Format is a schema check, not an accuracy score.

Correct practice: make claim support, correct source identity, effective date, calculations, and citations hard gates. Report formatting separately.

### OC-007: made unmeasured improvement forecasts

Evidence: `.opencode/quality-plan.md:31`, `:47`, `:61`, `:74`, and `:87` assign percentage uplifts to proposed changes without controlled experiments.

Why this is wrong: multiple interacting retrieval and prompt changes make additive gains especially unreliable.

Correct practice: label expected impact as a hypothesis, change one controlled factor at a time, report uncertainty and regression slices.

### OC-008: confused a post-push workflow with branch protection

Evidence:

- `.opencode/context.md:47-52` says direct pushes are blocked.
- `.github/workflows/block-direct-push.yml` runs only after a push event.

Why this is wrong: a failing workflow cannot undo the accepted Git ref update.

Correct practice: configure GitHub rulesets or branch protection, restrict pushes, require status checks, and verify settings through repository administration evidence.

### OC-009: prescribed unsafe automatic change integration

Evidence:

- `.opencode/context.md:14-26` promotes the auto-PR script.
- `scripts/auto-pr.sh:23` stages the entire working tree.
- `scripts/auto-pr.sh:43` immediately attempts merge and branch deletion.
- the script performs no test, clean-tree, secret, candidate, reviewer, or release-gate check.

Why this is wrong: unrelated files and secrets can be staged, and the author can effectively self-merge an unverified change.

Correct practice: stage explicit paths, show the diff, run required gates, require review, preserve failed branches, and never treat successful command execution as approval.

### OC-010: forced checkpoint resume without artifact validation

Evidence: `.opencode/context.md:54-66` says always resume and never rebuild.

Why this is wrong: resuming is only safe when the checkpoint is cryptographically bound to the same accepted corpus, parser, embedding model, configuration, store version, and document order. The current checkpoint and cache do not provide that handshake.

Correct practice: reject a mismatched checkpoint. Permit a clean versioned rebuild while preserving the old artifact as evidence.

### OC-011: accepted source counts without a source contract

Evidence:

- `.opencode/status.md:10` claims 129 PDFs plus NES.
- official scope in this QA baseline is 122 Awards.
- the persisted store is missing mandatory Awards and contains a wrong document identity.

Why this is wrong: “more files” is not completeness. The accepted set must be exact, current, uniquely identified, and checksummed.

Correct practice: compare the corpus manifest against the approved official ID list and fail on missing, extra, duplicate, stale, or misidentified sources.

### OC-012: self-certified integration without reproducible evidence

Evidence: `.opencode/integration-status.md:8-20` says all tests pass, no breaking changes exist, and the app launches. No commit-bound machine-readable execution artifact, provider transcript, UI trace, or clean-environment record is supplied.

Why this is wrong: a narrative status file is an assertion, not evidence.

Correct practice: generate status from immutable CI artifacts and link every claim to its run.

### OC-013: did not control secrets and external data

Evidence:

- `.opencode/work-log.md:15` records that a Groq key was set in `.env`.
- the application sends questions and retrieved content to Groq.
- no approved data classification, redaction, retention, residency, or provider-use policy is recorded.

Why this is wrong: a local environment file is not a secret-management process, and employment questions can contain sensitive personal or workplace facts.

Correct practice: define prohibited input, protected secret storage, logging rules, provider contract settings, retention, incident response, and credential rotation.

### OC-014: left dependency and action resolution mutable

Evidence:

- `requirements.txt` is unpinned;
- current resolution selected a yanked NumPy release;
- zizmor reports 12 unpinned GitHub Action uses;
- no exact application SBOM is present.

Why this is wrong: the same commit can install or execute different third-party code on another day.

Correct practice: lock Python dependencies with hashes, pin Actions to reviewed commit SHAs, generate an SBOM, and schedule controlled updates.

### OC-015: ignored release and license completeness

Evidence:

- the README claims MIT and links to `LICENSE`;
- no `LICENSE`, `COPYING`, or `NOTICE` exists at QA or development HEAD;
- no named release sign-off or residual-risk acceptance exists.

Why this is wrong: the repository makes a distribution claim that its files do not support, while product release status is self-declared.

Correct practice: owner-approved licensing, exact notices, and a controlled release record must precede public distribution.

## How the OpenCode records should be rewritten

Use distinct record types:

| Record | Must contain |
|---|---|
| requirement | ID, version, owner, rationale, acceptance test |
| risk | hazard, cause, impact, likelihood, control, owner, status |
| decision | options, evidence, trade-off, approvers, revisit trigger |
| task | deliverable, dependencies, done definition, result link |
| test run | candidate tuple, environment, command, oracle, result, artifact hash |
| defect | severity, reproduction, affected candidate, owner, closure evidence |
| status | generated gate result; no manually invented percentage |
| release | exact artifacts, sign-offs, exceptions, rollback and monitoring |

Rules:

1. never mark “skipped” as implemented;
2. never mark a quality objective complete when the recorded measure fails;
3. never combine format and legal correctness into one success narrative;
4. never treat a prompt instruction as claim validation;
5. never report an accuracy percentage without candidate and oracle provenance;
6. never let the same automation author, test, approve, and merge a risky change invisibly;
7. retain failed and superseded results instead of overwriting history.

## Final assessment

OpenCode helped produce a coherent prototype quickly, but the recorded practices favored visible progress and confident status over verifiable assurance. The central mistake was not “using AI.” It was allowing plans, implementation, evaluation, and approval to collapse into the same self-reporting loop.

The remedy is independent, traceable evidence and hard stop conditions. A better prompt or model alone cannot repair that process failure.
