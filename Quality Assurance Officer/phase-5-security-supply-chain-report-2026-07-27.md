# Phase 5 security and supply-chain report

Date: 27 July 2026

Result: failed

This phase used read-only inspection and temporary tool output. No product code, workflow, dependency declaration, or root documentation was changed.

## Scope and qualification

Two different source states were inspected:

| State | Identity | Qualification |
|---|---|---|
| QA working tree | branch `QA`, HEAD `fb9028a8978393968788038492c7d17af02ed42b` | dirty diagnostic state |
| current development tip | branch `develop`, `dd3bd45d58f430b6f88a927d7eee6ce1a815098d` | read through a temporary `git archive` |

The QA branch is one commit ahead of and four commits behind `develop`. The four untested development commits alter ingestion, vector-store construction, prompt handling, and source conversion. Earlier QA execution therefore does not qualify the current development tip.

The security skill had no Python-general or Gradio-specific reference. The review used Python secure-default principles, repository trust boundaries, and the automated results below. It is not a penetration test or certification.

## Automated check summary

| Check | Scope | Result | Decision |
|---|---|---|---|
| Bandit | active Python working tree, exclusions applied to supplied archives and QA material | 2 findings in 2,043 lines | failed |
| zizmor | four GitHub Actions workflows | 36 audit findings | failed |
| detect-secrets | 32 active text source and workflow files | no candidate secret | limited pass |
| Git object signature scan | 122 blobs from 197 repository objects | no match for selected provider and private-key signatures | limited pass |
| full detect-secrets scan | repository, then tracked-file set | both exceeded 60 seconds | not completed |
| pip-audit refresh | current unpinned requirements | two attempts exceeded 60 seconds | not completed |
| license metadata | direct dependencies plus a tool-environment inventory | direct metadata inspected; exact release SBOM absent | failed |
| development archive syntax | 33 Python files | 33 compiled | passed |
| development archive Ruff | active Python scope | lint and format passed | passed |
| development Markdown fixture | parser and chunker functions | three invariant failures reproduced | failed |

Static success does not establish safe runtime behavior. The release remains blocked.

## High-priority findings

### P5-SEC-001: the current development candidate has not been tested

`QA...develop` reports `1 4`. The development-only changes are:

```text
.gitignore
README.md
build_store.py
scripts/convert_pdfs_to_markdown.py
scripts/ingest_markdown.py
src/ingest.py
src/rag.py
```

The new path changes the source representation from PDF to Markdown, adds contextual prefixes, changes vector-store selection, and still contains the unsafe answer-forcing prompt. A QA result from the older branch cannot be transferred to this code.

Required closure:

1. identify one immutable candidate commit;
2. merge or rebase the intended QA branch onto that exact candidate;
3. rerun every applicable source, ingestion, retrieval, prompt, security, and release gate;
4. record the tested commit and artifact hashes in every result.

### P5-SEC-002: Markdown ingestion silently loses source content

`develop:scripts/ingest_markdown.py:14-40` buffers lines before the first `##` or `###` header but never emits them once a header is encountered. A local fixture returned one section while `PREAMBLE_RETAINED=False`.

Impact: definitions, coverage text, commencement provisions, or other legally relevant material before the first recognized header can disappear from the retrieval corpus.

Required closure: preserve and identify preamble content, add exact round-trip fixtures, and compare accepted PDF text against generated Markdown and final chunks.

### P5-SEC-003: subclause identity is lost

`develop:scripts/ingest_markdown.py:52-66` only recognizes a major clause followed by a period and space. The fixture produced:

```text
extract_clause_number("15. Minimum rates") == "15"
extract_clause_number("15.1 Minimum rates") == ""
```

Impact: an answer can cite the wrong level of the legal hierarchy or omit the subclause that actually supports a claim.

Required closure: parse nested clause forms, schedules, tables, paragraphs, and subparagraphs; retain the original heading; validate citations against source structure.

### P5-SEC-004: conversion and ingestion can report success after source failures

`develop:scripts/convert_pdfs_to_markdown.py:66-81` and `develop:scripts/ingest_markdown.py:172-187` catch per-file exceptions, print an error, and continue. The converter then reports the number discovered, not the number successfully written. The builder accepts Markdown when more than 100 files exist.

Impact: a partial corpus can be described as complete and indexed without a failing process exit.

Required closure: maintain expected and successful source manifests, fail atomically on any missing or rejected mandatory source, write to a staging directory, and publish only after corpus acceptance.

### P5-SEC-005: cached artifacts have no source handshake

`develop:build_store.py:21-47` loads `data/docs_cache.pkl` whenever it exists, before considering whether Markdown or PDF is the intended source. The cache contains no accepted corpus hash, parser version, source format, or configuration identity. If an index exists without a checkpoint, `develop:build_store.py:56-67` starts from document zero and appends again.

Impact: stale, mixed-format, duplicated, or malicious cached content can silently control the deployed store.

Required closure: replace executable serialization, bind every derived artifact to source and tool hashes, reject mismatches, and build into a new versioned directory.

## GitHub Actions findings

The zizmor 1.28.0 offline audit produced 36 top-level findings:

| Audit | Count | Maximum reported determination |
|---|---:|---|
| unpinned action use | 12 | high severity, high confidence |
| excessive permissions | 9 | medium severity, medium confidence |
| anonymous job or step definition | 5 | informational |
| missing concurrency limits | 4 | low severity, high confidence |
| persisted checkout credentials | 4 | medium severity, low confidence |
| template injection | 1 | low severity, high confidence |
| secret outside a dedicated environment | 1 | medium severity, high confidence |

Specific release concerns:

- all action references use movable version tags rather than reviewed commit hashes;
- none of the four workflows defines least-privilege workflow permissions;
- checkout credentials persist in the audit, CI, and evaluation jobs;
- no workflow defines concurrency control;
- `.github/workflows/eval.yml:43` embeds the dispatch input directly into a shell script;
- `.github/workflows/eval.yml:41` uses `GROQ_API_KEY` without a dedicated protected GitHub Environment;
- `.github/workflows/block-direct-push.yml` still runs after a push and cannot prevent that push.

The dispatch input is currently a two-value choice, which narrows practical exploitation. It does not make direct expression expansion inside shell code an acceptable pattern.

## Python code scan

Bandit reported:

| Location | Test | Severity | Confidence | Finding |
|---|---|---|---|---|
| `build_store.py:5` | B403 | low | high | import of `pickle` |
| `build_store.py:27` | B301 | medium | high | deserialization with `pickle.load` |

These findings confirm SEC-001. They are not two independent vulnerabilities.

Bandit reported no other finding in the inspected 2,043 Python lines. That is not proof of security. Bandit does not test prompt injection, legal claim validity, privacy handling, authentication, business logic, provider failure, or artifact provenance.

## Secret scan

No candidate secret was found in the narrowed active-text scan. A second limited scanner found no selected AWS, GitHub, OpenAI, Groq, Google, Slack, or private-key signature in reachable Git blobs.

Limitations:

- the full entropy and plugin scan timed out;
- the Git-object scan used signatures, not every detect-secrets detector;
- no remote fork, pull request, release artifact, CI log, LFS history, deleted reflog, host history, or provider console was inspected;
- absence of a match does not prove that the `.env` value mentioned in `.opencode/work-log.md` was never exposed elsewhere.

The correct result is “no secret found in the completed limited scans,” not “the repository is secret-free.”

## Dependencies, vulnerabilities, and licensing

The current requirements are unpinned and previously resolved to a yanked NumPy release. Two fresh `pip-audit` attempts exceeded 60 seconds, so the previous dated audit result was not promoted as a current pass.

Direct dependency metadata identifies common permissive licenses, including MIT, Apache-2.0, BSD-3-Clause, and NumPy's compound license set. A 198-row license inventory came from the QA tool environment and includes packages not proven to be application dependencies. It is not an application SBOM.

The repository contains no root `LICENSE`, `COPYING`, or `NOTICE` file. The committed README nevertheless displays an MIT badge linking to `LICENSE` and says to see that file. Distribution terms are therefore incomplete and internally inconsistent.

Required closure:

1. create a locked, hash-verified release environment;
2. generate its exact SBOM and license inventory;
3. review transitive notices and policy compatibility;
4. add the intended repository license only after the owner confirms the terms;
5. make the README match the actual license files.

## Development Markdown fixture

The isolated fixture imported the development-only ingestion module without building a store or contacting a provider.

| Invariant | Observed |
|---|---|
| section count | 1 |
| preamble retained | false |
| `15.1` subclause extracted | empty string |
| major clause `15` extracted | `15` |
| oversized chunk count | 1 |
| largest chunk with maximum 1,500 | 1,601 characters |

The chunker only splits between blank-line paragraphs. A single oversized paragraph remains oversized. This can invalidate context budgets, split behavior assumptions, and evaluation comparability.

## Traceability to existing test specifications

No new case IDs were invented for already-covered risks.

| Finding | Applicable specifications |
|---|---|
| stale candidate and dirty evidence | REP-001, REP-002, REP-004 |
| preamble and substantive-text loss | COR-020, COR-026 |
| missing subclause identity | ING-020, ING-023 |
| maximum chunk not enforced | ING-015 |
| swallowed source error and partial publish | ING-002, ING-003, ING-004 |
| cache and store identity mismatch | CIC-010, CIC-011, STO-007, STO-008, STO-009, STO-010 |
| Action pins and permissions | CIC-007, CIC-008 |
| direct-push false control | CIC-009 |
| secrets and logging | CIC-012, ING-029 |
| dependency and license completeness | DPN-004, DPN-009, REP-019 |

These are documented specifications. Only the narrow development fixture and static scans described in this report were executed in this phase.

## What was not done

- no product, workflow, dependency, or root-document fix;
- no provider inference or credential use;
- no deployment or live penetration test;
- no GitHub settings or branch-ruleset inspection;
- no container or infrastructure scan because no accepted deployment artifact exists;
- no complete dependency vulnerability refresh;
- no complete entropy scan;
- no legal review of generated Markdown fidelity.

## Exit decision

Phase 5 failed.

At minimum, the candidate mismatch, content-loss parser, silent partial-corpus success, executable cache, unpinned Actions, permission model, missing release lock, and missing repository license must be resolved and retested before security or supply-chain acceptance.
