# Developer handoff after QA

Date: 27 July 2026

From: quality assurance

To: development team

Decision: release blocked

## What QA is handing back

QA has removed its product implementation changes from the working tree. Every path outside `Quality Assurance Officer/` matches fork point:

```text
3e91e9e16c7417269242d7ef2f6f04bb6a49efff
```

The root README is the original development README from that point. The QA team README, tests, tools, reports, and evidence are under `Quality Assurance Officer/`.

No product fix is approved by this handoff. Earlier QA changes are retained only as reviewable patches in `evidence/`.

## Candidate status

There is no accepted candidate.

| Field | State |
|---|---|
| QA `HEAD` | `fb9028a8978393968788038492c7d17af02ed42b` |
| current development tip inspected | `dd3bd45d58f430b6f88a927d7eee6ce1a815098d` |
| common ancestor | `3e91e9e16c7417269242d7ef2f6f04bb6a49efff` |
| divergence | QA one commit ahead; develop four commits ahead |
| non-QA working tree versus common ancestor | identical |
| QA evidence | untracked pending review |
| root README versus QA `HEAD` | intentionally modified to restore the original |

Do not call QA `HEAD`, the cleaned working tree, or current `develop` a release candidate without an explicit owner decision.

## Current gate result

| Gate | Result |
|---|---|
| branch ownership cleanup | pass |
| declared dependency import | fail |
| QA regression suite | fail |
| static product checks | fail |
| Windows startup/request path | fail |
| corpus acceptance | fail |
| route and retrieval qualification | fail |
| prompt safety | fail |
| live provider comparison | blocked |
| legal review | blocked |
| production qualification | blocked |

The defect register contains 70 open findings. S1 findings block release.

## Immediate failures to reproduce

### Missing production dependency

Run:

```powershell
uv run --with-requirements requirements.txt `
  python "Quality Assurance Officer/tools/offline_request_matrix.py" --help
```

Expected current result:

```text
ModuleNotFoundError: No module named 'rank_bm25'
```

Do not close this by adding an unbounded package line only. Provide a reviewed lock, hashes or an approved locking policy, Python support matrix, clean install, import result, vulnerability report, license/SBOM result, and rollback note.

### Windows UTF-8 failure

After supplying the missing dependency only for diagnosis:

```powershell
uv run --with-requirements requirements.txt --with rank-bm25 `
  python "Quality Assurance Officer/tools/offline_request_matrix.py"
```

Expected current result:

```text
UnicodeDecodeError in src/cag.py before request one
```

The fix must apply to every accepted text input and output path, not only this file. Add Windows and Linux fixtures containing curly apostrophes, en dashes, non-Latin text, malformed bytes, BOM and no-BOM UTF-8, and declared rejection behavior.

### Regression suite

Run:

```powershell
python -m unittest discover -s "Quality Assurance Officer/tests" -v
```

Current baseline result:

```text
Ran 16 tests
FAILED (failures=14, errors=4)
```

Do not change test expectations merely to fit the implementation. Review the intended router API, then add development-owned tests that cover the public contract.

### Static checks

Run:

```powershell
uvx ruff check build_store.py src scripts
uvx ruff format --check build_store.py src scripts
```

Current result:

- 90 Ruff findings;
- 17 of 18 files require formatting.

Formatting is not the release risk, but a failing deterministic gate makes change review noisy and CI unreliable. Apply mechanical cleanup separately from behavior changes.

## Highest-risk product defects

### Source and legal identity

- MA000095 and MA000121 are missing.
- MA000002 is labelled as `Workplace Relations Act 1996`.
- Eight Award IDs outside the current 122-ID scope appear in the store.
- Raw Award inputs, checksums, effective dates, and a reproducible rebuild are absent.
- The store has 1,251 extra chunks in 388 exact-text duplicate groups.
- Current metadata cannot prove clause/page/version identity.

Development must create an accepted source manifest first. A vector-store rebuild from an unknown or partial source set is not acceptable.

### Routing and retrieval

The forced-UTF-8 baseline diagnostic produced:

- 31 of 60 cases passing every applicable check;
- Award detection 25 of 38;
- expected Award in context 22 of 36;
- clarification 0 of 9.

Independent semantic probing found the expected Award in 16 of 36 top-1 and 24 of 36 top-10 results. Clerks and Children’s Services identity mismatches can produce zero target-Award documents.

Do not attempt to solve canonical identity with a larger LLM. Use canonical Award IDs through source, chunk, filter, retrieval, citation, and output. Add reviewed aliases only at the input boundary. Detect negation and insufficient coverage facts before retrieval.

### Prompt and answer safety

The baseline prompt:

- is rendered as one human-role message;
- instructs the model to always answer;
- demands numbers even when the evidence is insufficient;
- contains numeric legal examples that can be copied;
- does not treat retrieved text as untrusted;
- has no atomic claim or citation schema;
- has no effective-date contract;
- has no deterministic post-generation validator.

The proposed prompt in `proposed-system-and-user-prompt.md` is a design draft, not an approved replacement. Implement role-separated messages, structured output, claim-to-source validation, clarification, insufficient evidence, date controls, and injection tests together.

### API and provider behavior

The current Groq path has:

- hard-coded provider and model choices;
- no explicit request timeout;
- no qualified retry/backoff/circuit-breaker policy;
- a fallback that changes model and prompt shape without reducing context correctly;
- no recorded request ID, actual model, tokens, latency, retry count, or cost;
- no approved privacy, retention, residency, or provider-training-use decision.

No live Groq, Gemini, OpenRouter, or OpenAI run was executed because no approved key or spend was available. Do not infer provider quality from model reputation or benchmark marketing.

Implement a provider adapter with a common request/response evidence contract. Qualify each provider/model/prompt pair on the same hidden set. Compare cost only among candidates that pass legal safety and grounding gates.

### Performance and deployment

The earlier provider-free loopback probe completed 288 of 288 requests, but the 32-worker run had:

- 5.936-second median latency;
- 7.902-second p95;
- 1.276 GB peak process RSS;
- fewer than five requests per second.

That is not production evidence. The external provider was replaced, authentication was absent, and the topology was local. Define SLOs and budgets before optimization, then test the accepted deployment with provider latency, rate limits, queues, admission control, soak, recovery, and cost.

## Required engineering phases

### Phase 1: control the candidate

Deliver:

- exact commit SHA;
- clean status;
- branch lineage decision;
- reviewed change list;
- dependency lock;
- supported Python and operating-system matrix;
- assigned engineering owner.

Do not combine branch reconciliation, formatting, dependency, corpus, retrieval, and prompt behavior in one review.

### Phase 2: control sources and ingestion

Deliver:

- 122 official Award sources plus accepted NES sources;
- source ID, title, URL, retrieval time, effective date, bytes, and SHA-256;
- parser fixtures for preamble, clauses, subclauses, tables, schedules, footnotes, and Unicode;
- atomic failure behavior;
- new output directory for each build;
- signed or checksummed artifact manifest;
- cross-platform rebuild evidence.

### Phase 3: make identity deterministic

Deliver:

- canonical Award ID on every source and chunk;
- one reviewed mapping from user aliases to Award ID;
- negative and ambiguous aliases;
- a coverage/clarification state;
- exact-ID filtering and citation;
- 122/122 source and title pass.

### Phase 4: qualify retrieval

Compare:

- lexical baseline;
- current vector baseline;
- hybrid fusion;
- exact-ID filter;
- reranker candidate;
- parent-clause or table-aware context.

Report recall@3, recall@5, clause recall@5, MRR, nDCG, latency, memory, prompt tokens, and cost by risk slice. Do not tune on the final held-out set.

### Phase 5: implement safe generation

Deliver:

- system/user role separation;
- untrusted-evidence boundary;
- accepted structured schema;
- atomic claims and citations;
- effective dates and units;
- explicit `needs_clarification`, `insufficient_evidence`, and `cannot_determine` outcomes;
- deterministic validator;
- prompt ID/hash and provider metadata;
- passing prompt-assurance set.

### Phase 6: qualify API, UI, and deployment

Deliver:

- explicit timeouts and bounded retry policy;
- qualified fallback or fail-closed behavior;
- redacted observability and cost records;
- provider privacy approval;
- UI validation and generic error handling;
- keyboard and accessibility results;
- ramp, spike, soak, saturation, recovery, and rollback evidence;
- actual deployment cost.

## Evidence required with every closure

For each defect, return:

1. defect ID;
2. requirement ID;
3. changed files;
4. design decision;
5. unit and integration test IDs;
6. exact commands;
7. raw output paths;
8. commit, corpus, prompt, model, and dependency identities;
9. before/after measured result;
10. reviewer and date;
11. residual risk;
12. rollback procedure.

A screenshot, console excerpt, or “works for me” statement is not enough.

## What development must not do

- Do not apply the recovery patch blindly.
- Do not merge current `develop` into QA and reuse old results.
- Do not report the historical 87.55% score as current accuracy.
- Do not count the 485 specifications as passing tests.
- Do not use forced UTF-8 or an ephemeral dependency as release configuration without changing and testing the candidate.
- Do not use a larger model to compensate for missing source identity.
- Do not run a costly provider comparison before corpus, routing, and prompt hard gates pass.
- Do not expose a legal-answering prototype publicly without named legal, security/privacy, and release acceptance.

## Requested development response

Return one short control packet:

```text
candidate commit:
branch:
changes included:
changes deliberately excluded:
source manifest hash:
store manifest hash:
dependency lock hash:
prompt hash:
primary provider/model:
fallback behavior:
supported platforms:
defects claimed closed:
raw evidence location:
engineering reviewer:
```

QA will then perform change-impact analysis and rerun the ordered gates in `test-and-metrics-register.md`.

## QA recommendation

Treat the product as a prototype. Fix candidate control and source identity before model tuning. Then fix deterministic routing, clarification, and evidence validation before comparing larger or more expensive models.

This order provides the largest accuracy gain per engineering and provider dollar because it removes failures a model cannot reliably correct.
