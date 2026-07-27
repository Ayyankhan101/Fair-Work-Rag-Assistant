# Software engineering process audit

Date: 27 July 2026

Disposition: inadequate for a legal-information release

## Conclusion

The repository does not contain sufficient evidence of a controlled software engineering lifecycle.

It does contain useful engineering fragments: source modules are separated by concern, Git is used, four CI or audit workflows exist, a task list and work log exist, retrieval alternatives were explored, and some smoke and evaluation scripts were run. Those facts prevent a fair conclusion that “no process happened.”

The stronger evidence-based conclusion is:

> The product appears to have been built through a rapid, implementation-first and self-certified workflow. The supplied repository lacks the controlled requirements, traceability, independent review, reproducible build, immutable test candidate, objective acceptance evidence, and release governance required for a system that answers employment-law questions.

Missing repository evidence does not prove that no external discussion or review occurred. No such external evidence was supplied, so it cannot support release acceptance.

## Lifecycle control assessment

| Control area | Repository evidence | Assessment |
|---|---|---|
| product scope | README, supplied requirements PDF, task notes | scope exists but current NES coverage and source count conflict |
| controlled requirements | one PDF with omissions and layout defects; no versioned acceptance record | failed |
| architecture | README diagrams and supplied DOCX | descriptive, not a controlled design baseline |
| decision records | no tracked ADRs or accepted trade-off records | failed |
| risk management | informal `.opencode/quality-plan.md`; no maintained risk register | failed |
| source control | Git branches and 19 commits | present, but branch lineage and candidate control are weak |
| code review | CODEOWNERS names one owner; auto-merge script exists | independence not demonstrated |
| unit testing | smoke scripts at HEAD; no tracked test suite | failed |
| integration testing | status claims 7 of 7; no reproducible result artifact | unverified |
| system testing | historical 12- and 25-question results | inadequate oracle and provenance |
| security testing | dependency workflow and this QA scan | incomplete; blocking findings open |
| configuration management | unpinned requirements, unversioned prompt and corpus | failed |
| data quality | persisted store but no accepted raw corpus or source manifest | failed |
| change control | PR instructions and automated PR script | unsafe and not evidence of required review |
| release management | no immutable candidate, release record, rollback proof, or named sign-off | failed |
| operations | no accepted deployment, observability, incident, privacy, recovery, or cost evidence | failed |

## Process contradictions

### Completion was declared before acceptance criteria were met

`.opencode/status.md:4-7` reports 14 of 14 complete, zero unresolved issues, and execution complete. The same file reports only 10 of 12 answers fully correct.

`.opencode/todo.md:37-40` marks verification above 90% complete. `.opencode/todo.md:56-60` records approximately 83% content accuracy and still marks final validation complete.

This is a gate failure, not merely a documentation typo. A lifecycle cannot close a quality objective while its own recorded result fails the objective.

### The acceptance arithmetic is wrong

`.opencode/quality-plan.md:1-6` sets a target above 97% and says 11 of 12 is a minimum. Eleven of twelve is 91.67%, not above 97%. Only 12 of 12 clears that threshold for a 12-item sample.

The sample is also too small to support a precise population claim. One result changes the score by 8.33 percentage points.

### Skipped work was counted as complete

`.opencode/todo.md:48-50` checks both reranking tasks as complete while describing them as skipped. A skipped task may be a valid decision, but it needs a documented decision, reason, impact assessment, and revised acceptance baseline. It is not evidence that reranking was implemented or tested.

### Test labels are not tied to test evidence

`.opencode/work-log.md:7-16` assigns “Unit Test: pass” to source files, `.env`, and `requirements.txt`. A configuration file or dependency list does not itself pass a unit test. The log supplies no command, test ID, commit, fixture, output hash, environment, or reviewer.

`.opencode/integration-status.md:5-12` says the app and all tests pass, but HEAD has no conventional tracked unit test suite and no machine-readable 7-test execution record.

### The process incentivized substantive-looking answers over supported answers

`.opencode/quality-plan.md:25-27`, `:87-107`, and `:131-135` treat “not specified” as a weakness and require every answer to be substantive. The resulting committed prompt orders the model to provide specific, confident numbers even when context is incomplete.

For legal information, abstaining on insufficient evidence is a safety behavior. Optimizing it away without claim validation is an assurance mistake.

### Status was manually asserted instead of generated

Status, context, work log, README, and evaluation artifacts disagree on:

- 16,622 versus 16,692 chunks;
- 129 PDFs versus the current 122-Award official scope;
- 83%, 87.5%, and 87.5467% accuracy;
- complete versus known missing sources;
- 12-question versus 25-question results;
- successful tests versus the absence of reproducible test evidence.

A release status should be derived from an immutable run manifest, not copied across narrative files.

## Branch and candidate control

The branch graph shows:

- `QA` at `fb9028a` is four commits behind `develop`;
- the untested commits change ingestion, conversion, storage, and prompting;
- `main` and `develop` have separate root histories with parallel, similar commits;
- the current QA working tree also has 20 modified tracked files;
- the test specifications and local unit tests are not part of the tested HEAD.

This prevents a reviewer from answering a basic question: “Which exact code, data, prompt, dependencies, and tests produced this result?”

The minimum candidate identifier is a tuple:

```text
commit
locked dependency hash
raw corpus manifest hash
derived store hash
prompt ID and hash
model/provider/version
configuration hash
test-suite commit
run ID and time
```

None of the historical accuracy artifacts records that tuple.

## Review independence

`CODEOWNERS` assigns the repository to one account. The documented auto-PR flow creates, pushes, and immediately attempts to merge a change. No required approval count, segregation of duties, legal reviewer, data reviewer, QA sign-off, or protected-environment approver is evidenced.

For this product, at least these roles must be explicit even if one person holds more than one role:

| Role | Cannot self-certify |
|---|---|
| product owner | scope and risk acceptance without recorded rationale |
| engineer | correctness of own code change |
| QA reviewer | release status of a mutable candidate |
| employment-law reviewer | legal gold answer and citation correctness |
| security/privacy reviewer | data-handling and external-provider acceptance |
| release owner | deployment and rollback readiness |

Where staffing prevents independence, the exception and compensating controls must be documented. Silence is not an exception record.

## Documentation quality

The existing notes are useful as a development diary but unsuitable as controlled evidence because they mix:

- plans, claims, and results;
- implementation and validation;
- skipped and completed work;
- current and stale measurements;
- test names and unrecorded assertions;
- confidence language and unsupported projections.

The earlier documentation also uses speculative uplift estimates such as “+5–10%” without experiment design or confidence intervals. Those estimates should be treated as hypotheses, not forecasts.

## Process maturity statement

No formal maturity certification is claimed. Based only on repository evidence, the workflow has ad hoc controls and some repeatable habits, but it is not a defined, measured, or release-controlled process.

The main failure is not lack of paperwork. It is the absence of reliable feedback gates:

```text
requirement -> risk -> design decision -> code/data change -> traceable test
-> immutable result -> independent review -> release decision -> monitoring
```

Several arrows are missing, and some recorded failures were converted into “complete.”

## Required process reset

### Phase A: establish control

1. name the product owner, engineering owner, QA owner, legal reviewer, and release owner;
2. select one branch lineage and one immutable candidate;
3. decide or discard the existing dirty working-tree patch;
4. approve a severity model, stop conditions, and exception process;
5. make branch protection and required reviews real repository settings.

### Phase B: baseline requirements and risks

1. issue versioned functional, legal-scope, privacy, security, performance, accessibility, cost, and operational requirements;
2. define non-goals and prohibited uses;
3. create requirements-to-risk-to-test traceability;
4. approve the 122-Award plus NES source contract;
5. record architecture and provider decisions with alternatives and reversal criteria.

### Phase C: make the build reproducible

1. lock dependencies with hashes;
2. retain a checksummed raw corpus;
3. version parsers, chunking, prompts, models, and store artifacts;
4. build atomically and reject incomplete inputs;
5. generate an SBOM and license record.

### Phase D: implement objective verification

1. track executable unit, property, parser, store, retrieval, prompt, provider, UI, and deployment tests;
2. require claim-level legal oracles and citation verification;
3. separate visible development tests from hidden acceptance tests;
4. store run manifests and immutable results;
5. prohibit status claims not generated from those results.

### Phase E: independent release decision

1. close every S0 and S1 defect;
2. review residual S2 defects and documented exceptions;
3. obtain named engineering, QA, legal, privacy/security, and release sign-off;
4. prove rollback, recovery, monitoring, incident response, and budget limits;
5. publish only the exact accepted candidate.

## Current decision

The process evidence fails release acceptance.

The repository should be treated as a prototype under reconstruction, not as a completed system with a quality percentage. Adding more model capability before controlling source identity, candidate identity, and claim validation would make the output more fluent without making it more trustworthy.
