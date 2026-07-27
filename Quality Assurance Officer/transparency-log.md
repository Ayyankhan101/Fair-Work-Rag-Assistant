# Transparency log

## Purpose

This file records what was inspected, what changed, what was not tested, and where the evidence is weak. It is part of the release evidence.

## Test point

| Field | Value |
|---|---|
| Date and time | 2026-07-27 04:38:37 +05:00 |
| Repository | `fair-work-rag-assistant` |
| Branch | `QA` |
| HEAD | `fb9028a8978393968788038492c7d17af02ed42b` |
| Python | 3.11.15 |
| Ruff | 0.12.0 |
| Git | 2.54.0.windows.1 |
| uv | 0.11.28 |
| Operating system | Windows |
| Worktree | dirty |

The report covers the working tree, not an immutable release candidate.

## Documentation-only boundary

At approximately 04:20 local time on 27 July 2026, the user clarified:

> don't change any code or stuff ... do documentation for everything in my folder

After that clarification, the product code, workflows, root configuration, and root documentation were frozen. Later writes are limited to `Quality Assurance Officer`.

Read-only commands may still create tool caches outside the repository. Python imports may also use ignored `__pycache__` directories. These are not release artifacts.

## Changes made before the boundary

The QA session had already changed 20 tracked files and added untracked test and audit files before the instruction changed. These changes are not concealed and must be reviewed as a separate proposed patch.

Tracked files with working-tree changes:

```text
.github/workflows/ci.yml
README.md
build_store.py
requirements.txt
scripts/eval_hard.py
scripts/eval_prd_questions.py
scripts/rename_pdfs.py
scripts/smoke_test_rag.py
scripts/smoke_test_retrieval.py
src/app.py
src/bm25_retriever.py
src/cag.py
src/config.py
src/fastembeddings.py
src/filtered_retriever.py
src/hybrid_retriever.py
src/ingest.py
src/rag.py
src/router.py
src/vectorstore.py
```

Untracked implementation-support paths added by the QA session:

```text
qa/
tests/
```

The substantive changes attempted to address CI imports, dependency declarations, CAG decoding and filtering, routing consistency, prompt refusal rules, Award aliases, error disclosure, ingestion failures, and vector-store resume behavior. Ruff also made mechanical formatting changes.

These changes have local unit evidence but have not passed corpus, integration, provider, UI, performance, or release testing. They must not be described as production fixes.

The `Quality Assurance Officer` folder was already user-provided and untracked. This session added and updated QA Markdown and JSON evidence within it.

## Repository state

| Measure | Result |
|---|---:|
| Files tracked at HEAD | 117 |
| Test files tracked at HEAD | 0 |
| Modified tracked files at test point | 20 |
| Untracked files at test point | 38 |
| Untracked files under `Quality Assurance Officer` | 32 |
| Untracked files under `tests` | 4 |
| Untracked files under `qa` | 2 |

The 16 passing unit tests reported in this QA pass are untracked working-tree tests. HEAD itself contains no `tests/` files. This distinction is release-significant.

At the first documentation milestone, the untracked count increased from 38 to 48:

| Area | Untracked files at that milestone |
|---|---:|
| `Quality Assurance Officer` | 42 |
| `tests` | 4 |
| `qa` | 2 |

The ten-file increase at that milestone was QA documentation only. The QA root then contained 21 Markdown files and 2,293 lines.

## Source inspection

Observed:

- all 117 tracked paths were inventoried;
- all 34 tracked JSON files parsed;
- all four workflow YAML files parsed;
- all 21 tracked Python files were included in static inspection;
- all four tracked shell scripts were syntax checked;
- the seven-page requirements PDF was text-extracted, rendered, and visually inspected page by page;
- both DOCX files were structurally extracted;
- the architecture DOCX could not be rendered because LibreOffice is not installed;
- all 19 PDFs in the QA folder were opened and text-extracted;
- the 18 research PDFs in `Discard` contain extractable text;
- the source image and prior chat were read;
- the discarded prototype's code, manifests, evaluation data, Docker files, and documentation were inspected.

Limitations:

- the architecture DOCX and Week 1 DOCX did not receive page-by-page visual inspection;
- the 18 research PDFs were checked for readability and subject, not peer-reviewed for scientific correctness;
- Obsidian plugin bundles were inventoried and searched but third-party minified code was not manually reviewed line by line;
- no formal ISO certification audit occurred;
- no independent employment-law expert has reviewed the gold answers;
- no production environment, production logs, user analytics, cloud bill, or provider contract was supplied.

## Commands with side effects outside the repository

`uv pip compile` and `uvx pip-audit` used the local uv cache. The isolated import test downloaded packages to the uv cache. No deployment was created and no provider request was made.

The PDF renderer wrote seven PNG files to:

```text
C:\Users\HP\AppData\Local\Temp\fair-work-qa-27db1dcaeed64187a12f9534f9e6a015
```

They are temporary inspection files, not release evidence in the repository.

Cleanup was attempted after inspection. The environment policy rejected both recursive and explicit `Remove-Item` commands before execution. The seven PNG files may remain in that temporary directory. No repository file was affected.

## Claims not made

This QA pass does not claim:

- the application is release-ready;
- 122 Awards are present;
- the current answers are legally correct;
- the old 87.55% score is valid for the current store;
- the application meets WCAG 2.2;
- the application is secure;
- the system can support ten concurrent users;
- the deployment cost is known;
- a clean checkout passes;
- the prior code changes are accepted.

## Work after the expanded research request

The QA-only folder was extended with:

- a 122-page live source-corpus report and aggregate evidence record;
- current model, reranking, architecture, tuning, and cost research;
- an unbiased evaluation system;
- a standards-based QA method report;
- a strict critique of previous documentation;
- four quick-glance guides;
- a consolidated final QA report;
- a prompt-assurance report;
- a proposed role-separated system and user prompt;
- a prompt evaluation rubric;
- 120 prompt-specific test specifications.

No product code, workflow, dependency file, root documentation, `tests/`, or `qa/` path was changed during this expanded documentation work.

The model research used current official OpenAI, Groq, Cohere, BAAI, Fair Work, NIST, ISO, OWASP, W3C, ACL, NeurIPS, and arXiv sources. Model recommendations are candidates, not accepted changes.

The live source crawl reached 122 of 122 Award pages. The first parser incorrectly expected the Award ID inside the title heading and produced 122 invalid failure labels. Those labels were discarded. The corrected interpretation preserves the successful response, content-type, body-ID, title-presence, consolidation, and encoding checks. Raw pages and per-page hashes were not retained, so source acceptance still fails.

An isolated `uv run --with langchain-core` command downloaded or reused packages in the uv cache and proved that `ChatPromptTemplate.from_template` renders a `HumanMessage`. It did not change repository dependencies or files.

Internet research and the Award crawl produced network traffic. No provider inference request, deployment, external message, purchase, or account change was made.

A parallel `curl` check of 29 external documentation links was attempted. Curl’s per-transfer option handling caused response bodies to be printed and two requests timed out at 30 seconds. That attempt is not recorded as a passed link audit. Local Markdown targets were checked separately and passed. The primary research links used in the reports were opened during the research steps.

After the expanded research and prompt-assurance documentation:

| Measure | Current result |
|---|---:|
| Modified tracked files | 20 |
| Untracked files visible to Git | 64 |
| Untracked files under `Quality Assurance Officer` | 58 |
| Untracked files under `tests` | 4 |
| Untracked files under `qa` | 2 |
| QA-root Markdown files | 36 |
| QA-root Markdown lines | 4,193 |
| Files physically present under `Quality Assurance Officer` | 79 |

## Continuation after the request to continue QA

No product code, workflow, dependency declaration, root documentation, `tests/`, or `qa/` file was changed during this continuation. New evidence and reports were written only under `Quality Assurance Officer`.

Read-only or temporary operations performed:

- ran the 16 untracked unit tests in the host and isolated dependency environments;
- ran Ruff check and format verification without applying changes;
- ran the QA documentation style checker;
- ran `git diff --check`;
- resolved the unpinned requirements with `uv`;
- measured statement coverage with the coverage data file directed to the operating-system temporary directory;
- imported source modules in isolated subprocesses;
- inspected effective `ChatGroq` defaults with a dummy, non-working key;
- triggered the fallback with a fake local runnable and captured its rendered prompt without a provider request;
- checked only whether provider environment variables were present, without reading or printing any value;
- reviewed current official Groq, Gemini, OpenRouter, and OpenAI documentation.

The first isolated dependency/import command exceeded 60 seconds and was terminated. Its retry used the populated package cache and completed. The resolver installed or reused 96 packages and warned that `numpy==2.4.0` is yanked.

Application import was terminated after 20 seconds in the module matrix and after 50 seconds in a dedicated retry. Neither attempt produced a completed startup result. No server was exposed.

All checked provider variables were absent:

```text
GROQ_API_KEY
GEMINI_API_KEY
GOOGLE_API_KEY
OPENROUTER_API_KEY
OPENAI_API_KEY
```

No model inference, purchase, credit use, account creation, deployment, external message, or provider configuration change occurred.

The OpenAI documentation skill's MCP connector was unavailable. Its prescribed `codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp` command was attempted and failed with an access-denied error. No connector installation was confirmed. Official OpenAI web documentation was used as the fallback.

New diagnostic conclusions:

- 16 of 16 untracked tests pass;
- total statement coverage is 12%;
- eight critical modules have 0% coverage;
- the unpinned requirements can select a yanked package;
- the current provider client has no explicit timeout;
- no replacement provider/model pair has live evidence;
- the release remains blocked.

After this continuation:

| Measure | Current result |
|---|---:|
| Modified tracked files | 20 |
| Untracked files visible to Git | 66 |
| Untracked files under `Quality Assurance Officer` | 61 |
| Untracked files under `tests` | 4 |
| Untracked files under `qa` | 1 |
| QA-root Markdown files | 38 |
| QA-root Markdown lines | 4,567 |
| Files physically present under `Quality Assurance Officer` | 82 |

## Continuation: security, supply chain, process, and OpenCode

No product code, workflow, dependency declaration, root document, `tests/`, or `qa/` file was changed during this continuation. Writes were limited to `Quality Assurance Officer`.

Read-only repository actions:

- compared `QA`, `develop`, and `main` histories;
- found that QA is one commit ahead of and four commits behind `develop`;
- inspected the seven paths changed between QA and the development tip;
- created and inspected a temporary `git archive` of `develop`;
- compiled 33 development Python files;
- ran Ruff check and format verification against that archive;
- executed a local fixture against the development-only Markdown parser and chunker;
- inspected `.opencode` status, context, task, plan, integration, and work-log records;
- inspected CODEOWNERS, workflows, the auto-PR script, repository licensing, and lifecycle artifacts.

Temporary or cache-affecting actions:

- `uvx bandit` wrote `C:\Users\HP\AppData\Local\Temp\fwra-qa-bandit-2026-07-27.json`;
- `uvx zizmor` wrote `C:\Users\HP\AppData\Local\Temp\fwra-qa-zizmor-2026-07-27.json`;
- the narrowed detect-secrets run wrote `C:\Users\HP\AppData\Local\Temp\fwra-qa-detect-secrets-active-text-2026-07-27.json`;
- the license inventory wrote `C:\Users\HP\AppData\Local\Temp\fwra-qa-python-licenses-2026-07-27.json`;
- the development archive remains at `C:\Users\HP\AppData\Local\Temp\fwra-develop-qa-51b17c0109cd402db02c7b675649b51f` and a sibling ZIP;
- uvx may have downloaded or reused scanner packages in the uv cache.

No external provider request, deployment, push, merge, message, purchase, or account-setting change occurred.

Completed security results:

- Bandit inspected 2,043 Python lines and reported the pickle import and unsafe load;
- zizmor reported 36 findings across four workflows;
- a 32-file active-text detect-secrets scan found no candidate;
- a selected-signature scan found no candidate in 122 reachable Git blobs;
- both full detect-secrets attempts exceeded 60 seconds;
- both fresh pip-audit attempts exceeded 60 seconds;
- a 198-row license inventory described the QA tool environment, not an exact application SBOM;
- no root `LICENSE`, `COPYING`, or `NOTICE` file exists even though the committed README claims MIT and links to `LICENSE`.

Development fixture results:

```text
SECTIONS=1
PREAMBLE_RETAINED=False
SUBCLAUSE_15_1=''
MAJOR_CLAUSE_15='15'
OVERSIZED_CHUNK_COUNT=1
OVERSIZED_MAX_LEN=1601
```

Interpretation boundaries:

- no match in the limited secret scans is not proof that the repository or its history is secret-free;
- a timed-out vulnerability refresh is not a pass or a new vulnerability finding;
- the development archive was inspected without switching the dirty working tree;
- missing lifecycle records do not prove no discussion or process occurred outside the repository;
- the OpenCode critique addresses supplied records and prescribed practices, not the OpenCode product or an unverified author;
- no legal expert reviewed the Markdown fidelity or defect severities.

New documentation:

- Phase 5 security and supply-chain report;
- software engineering process audit;
- OpenCode practices critique;
- machine-readable Phase 5 evidence;
- 13 additional defects, taking the register from 47 to 60.

After this continuation:

| Measure | Current result |
|---|---:|
| Modified tracked files | 20 |
| Untracked files visible to Git | 70 |
| Untracked files under `Quality Assurance Officer` | 65 |
| Untracked files under `tests` | 4 |
| Untracked files under `qa` | 1 |
| QA-root Markdown files | 41 |
| QA-root Markdown lines | 5,156 |
| QA JSON files | 8 |
| Files physically present under `Quality Assurance Officer` | 86 |

## Continuation: executable RAG+CAG requests and local load

The user requested the maximum QA and testing possible before supervisor submission.

Boundary retained:

- no product source, workflow, dependency declaration, root documentation, or product data was changed;
- QA-only harnesses and evidence were added under `Quality Assurance Officer`;
- no provider credential was present;
- no model-provider request, purchase, deployment, push, merge, or external message occurred.

QA-only harnesses added:

```text
tools/offline_request_matrix.py
tools/semantic_retrieval_probe.py
tools/server_load_probe.py
tools/historical_claim_support_probe.py
tools/failure_path_probe.py
```

Executed work:

- reran the 16 untracked working-tree unit tests;
- executed 60 varied offline RAG+CAG cases against the dirty QA state;
- attempted the same matrix against `develop`;
- recorded the natural Windows NES decoding failure before request one;
- forced Python UTF-8 for one explicitly non-qualifying development diagnostic;
- executed semantic accuracy, deterministic-repeat, and concurrency probes;
- compared 25 historical answers with current retrieved context;
- injected 429, 413, rate-limit, timeout, 500, and 401 failures;
- imported the actual application without a key and recorded the failure;
- launched the real local Gradio application twice with only the LLM replaced;
- ran eight HTTP functional cases and 288 timed HTTP load cases per server run;
- closed both loopback servers and verified their ports were no longer listening.

Provider-free component boundary:

- application import, CAG, store, retrieval, prompt, handler, Gradio queue, and HTTP were real;
- the external LLM was a capture runnable;
- captured responses cannot be scored as legal answers;
- provider latency, tokens, billing, rate limits, and output behavior were absent.

The first server load run constructed each worker client during the timed interval. QA identified that confound, retained the first JSON, changed only the QA harness, and executed a corrected run with clients created before timing. Only the corrected run is used for capacity interpretation.

Key diagnostic results:

- dirty QA request matrix: 41 of 60 passed all applicable checks;
- natural `develop` request matrix: blocked by Windows `UnicodeDecodeError`;
- forced-UTF-8 `develop` matrix: 31 of 60;
- raw semantic expected Award: 16 of 36 top-1 and 24 of 36 top-10;
- filtered semantic expected Award: 33 of 36;
- clarification: zero of nine;
- historical exact support: four of 25 questions;
- semantic concurrency: 300 of 300 completed;
- corrected HTTP load: 288 of 288 completed;
- corrected 32-worker HTTP: 5.936-second median, 7.902-second p95, 1,275,621,376-byte peak RSS;
- prompt message shape: 60 of 60 were a single human-role message;
- natural no-key import: failed after 15.349 seconds.

Temporary and host effects:

- uv reused or populated its dependency cache;
- the local embedding model and store were loaded into short-lived test processes;
- two earlier orphaned app-import processes were identified by exact command line; the child was stopped and the parent exited;
- loopback ports 59617 and 52578 were used and closed;
- generated QA bytecode cache was moved, not deleted, to `C:\Users\HP\AppData\Local\Temp\fwra-qa-tools-pycache-2026-07-27`;
- the temporary development archive remains outside the repository as previously disclosed.

Evidence limitations:

- the hand-authored 60-case expectations are not an employment-law gold set;
- literal occurrence is not legal claim validation;
- the development matrix combined development code with current QA data artifacts;
- the forced-UTF-8 run is a workaround diagnostic;
- HTTP load used a capture model and a single Windows host;
- the load sample was short and non-monotonic;
- no production proxy, authentication, provider, browser, network, autoscaling, soak, recovery, or multi-process topology was tested.

New documentation and status:

- Phase 6 RAG+CAG request and load report;
- supervisor handoff;
- five QA-only executable harnesses;
- eight new machine-readable evidence files, including the retained superseded server run;
- nine additional defects, taking the register from 60 to 69.

After this continuation:

| Measure | Current result |
|---|---:|
| Modified tracked files | 20 |
| Untracked files visible to Git | 85 |
| Untracked files under `Quality Assurance Officer` | 80 |
| Untracked files under `tests` | 4 |
| Untracked files under `qa` | 1 |
| QA-root Markdown files | 43 |
| QA-root Markdown lines | 5,611 |
| QA JSON files | 16 |
| QA-only executable harnesses | 5 |
| Files physically present under `Quality Assurance Officer` | 101 |

Some supplied files are ignored by repository rules, so the physical count is larger than Git’s untracked count.

## Continuation: QA branch ownership cleanup

The user asked QA to remove changes outside the QA role, keep a recovery record, restore the inherited product tree, create separate development and QA READMEs, and execute another quick QA iteration.

Baseline decision:

- QA `HEAD`: `fb9028a8978393968788038492c7d17af02ed42b`;
- inspected `develop`: `dd3bd45d58f430b6f88a927d7eee6ce1a815098d`;
- common ancestor and protected inherited tree: `3e91e9e16c7417269242d7ef2f6f04bb6a49efff`;
- current develop was not merged because it is four commits ahead of the inherited tree and remains unqualified.

Before restoration, QA retained:

- a 122,841-byte binary working-tree patch covering 20 tracked product paths;
- a 7,785-byte staged patch for the repository-audit script;
- a 384-byte patch for the committed QA README banner;
- commit IDs, README object IDs, branch divergence, change statistics, source hashes, and patch hashes in `evidence/pre-reversion-state-2026-07-27.json`.

QA-owned source was moved:

- four files from root `tests/` to `Quality Assurance Officer/tests/`;
- two files from `qa/scripts/` to `Quality Assurance Officer/tools/`.

Generated bytecode and Ruff cache directories were moved to named temporary directories. The now-empty root `qa/scripts` and `qa` directories were removed. No product source was deleted.

Twenty tracked product paths were restored from the common ancestor. Verification after restoration:

```text
non-QA paths different from common ancestor: 0
non-QA paths different from QA HEAD: README.md only
root README object: 2954b27f375aaa7ec884a4d13841236b12777d76
common-ancestor README object: 2954b27f375aaa7ec884a4d13841236b12777d76
```

The remaining root README difference from QA `HEAD` is intentional: the working copy removes the QA banner and restores the original development README. No commit, stage, push, merge, rebase, or deployment occurred.

Two procedural errors occurred:

1. the first restore guard checked silent Git output instead of the Git exit code and stopped before restoration;
2. the first unit-test transcript capture misquoted the spaced QA directory and produced a runner error.

Both are retained in the change-control record. The second output is retained under evidence filenames containing `invocation-error`.

Latest quick QA result against the restored baseline:

- 29 of 29 product and QA Python files parsed;
- 2 of 16 QA unit-test methods passed;
- the declared dependency environment could not import `rag.py` because `rank_bm25` is missing;
- natural Windows execution stopped before request one on UTF-8 decoding;
- the diagnostic forced-UTF-8 request matrix passed all applicable checks in 31 of 60 cases;
- corpus audit remained release-blocking;
- Ruff reported 90 product findings and 17 of 18 files requiring formatting;
- the QA-owned tests and tools passed Ruff check and format after QA-only corrections;
- all 47 QA Markdown files passed the QA documentation-style gate;
- no live provider test ran because no approved provider key or spend was available.

The diagnostic forced-UTF-8 run added only environment and ephemeral dependency overrides. It did not change product source and does not qualify the baseline.

New documentation:

- `developer-handoff-after-qa-2026-07-27.md`;
- `qa-branch-change-control-record-2026-07-27.md`;
- `quick-qa-iteration-after-cleanup-2026-07-27.md`;
- `test-and-metrics-register.md`;
- the QA README and runbook were updated for the new ownership boundary.

The defect register increased from 69 to 70 because the restored inherited requirements omit an unconditionally imported runtime dependency.

State after this continuation:

| Measure | Current result |
|---|---:|
| modified non-QA files versus common ancestor | 0 |
| modified non-QA files versus QA `HEAD` | 1, root README restoration |
| untracked top-level classes | QA folder only |
| QA-root Markdown files | 47 |
| QA-root Markdown lines | 6,466 |
| QA JSON files | 20 |
| QA evidence files | 32 |
| QA Python files, including supplied historical material | 17 |
| files physically present under QA folder | 130 |
| QA folder bytes | 64,294,561 |

The 64 MB package includes supplied historical and binary material. File count and size do not indicate test completeness.
