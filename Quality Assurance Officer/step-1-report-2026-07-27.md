# Step 1 report: repository baseline

## Verdict

Step 1 execution is complete.

Phase result: fail.

Release result: blocked.

The working tree passes its current Python lint, formatting, compilation, and 16 untracked unit tests. That does not make the repository release-ready. The test point is dirty, HEAD contains no test files, the source corpus cannot be rebuilt, mandatory Award coverage fails, metadata provenance is incomplete, and historical evaluation results cannot be tied to the tested system.

## Scope

Step 1 covered:

- repository identity and worktree state;
- tracked and untracked inventory;
- Python, JSON, YAML, and shell syntax;
- dependency resolution and known-vulnerability audit;
- current offline unit tests;
- source requirements and architecture documents;
- current persisted corpus and evaluation metadata;
- secret-pattern history signals;
- QA documentation style;
- evidence and release-stop conditions.

It did not run provider calls, answer evaluation, browser interaction, load tests, deployment, failover, or legal review. Those results remain `not run` or `blocked`.

## Environment

| Field | Value |
|---|---|
| Timestamp | 2026-07-27 04:38:37 +05:00 |
| Branch | `QA` |
| HEAD | `fb9028a8978393968788038492c7d17af02ed42b` |
| Dirty worktree | yes |
| Python | 3.11.15 |
| Ruff | 0.12.0 |
| uv | 0.11.28 |
| Operating system | Windows |

## Inventory

| Measure | Result |
|---|---:|
| Tracked files | 117 |
| Tracked bytes present | 58,739,487 |
| Tracked Python files | 21 |
| Tracked Python lines | 2,314 |
| Tracked JSON files | 34 |
| Workflow YAML files | 4 |
| Shell files | 4 |
| Files modified from HEAD | 20 |
| Untracked files after documentation | 48 |
| Untracked files under `Quality Assurance Officer` | 42 |
| Test files at HEAD | 0 |
| Current untracked test files | 4 |

## Executed checks

| Check | Result | Evidence |
|---|---|---|
| `ruff check src scripts tests build_store.py qa` | pass | no lint findings |
| `ruff format --check src scripts tests build_store.py qa` | pass | working-tree format clean |
| `python -m compileall -q src scripts tests build_store.py qa` | pass | exit 0 |
| `python -m unittest discover -s tests -v` | pass | 16 tests, 0 failures, 0.032 seconds |
| tracked JSON parse | pass | 34 of 34 parsed |
| workflow YAML parse | pass | 4 of 4 parsed |
| dependency resolution | pass | `uv pip compile`, exit 0, 310 output lines |
| isolated Python 3.11 imports | pass | 95 packages installed; 80.202 seconds |
| known-vulnerability audit | pass with limitation | `pip-audit`: no known vulnerabilities on the resolved 27 July graph |
| shell syntax | fail | 3 of 4 scripts fail `bash -n` |
| corpus audit | fail | S1 and S2 findings |
| QA documentation style | pass | 22 Markdown files including root README |
| QA test-case identity | pass | 365 unique IDs; no duplicate |
| QA local links | pass | 10 checked; 0 missing |
| clean-checkout test | not run | worktree contains proposed changes |
| application startup | not run | corpus gate failed; heavy model load deferred |
| provider query | not run | no valid answer evaluation while corpus gate fails |

The vulnerability result is a point-in-time database lookup, not proof of secure dependencies. Direct requirements are unpinned, no lock file is tracked, and a later install may resolve different versions.

## Isolated dependency result

The current 12 direct requirements resolved successfully for Python 3.11. The clean import environment installed 95 packages and took 80.202 seconds on this machine, including downloads.

Large downloaded packages included:

- Gradio: 29.5 MiB;
- ONNX Runtime: 13.1 MiB;
- NumPy: 12.0 MiB;
- pandas: 9.5 MiB;
- Pillow: 6.9 MiB;
- pdfminer-six: 6.3 MiB.

This is installation evidence, not application cold-start evidence. The embedding model and full Gradio startup were not included.

`pip-audit` reported no known vulnerabilities. It also warned that a transitive package contained an invalid version specifier that had to be normalized from `>=3.6.*` to `>=3.6`.

## Corpus result

Observed persisted state:

| Measure | Result |
|---|---:|
| Total stored documents | 16,692 |
| Award documents | 16,665 |
| NES documents | 27 |
| Unique stored Award names | 129 |
| Unique source files | 131 |
| Exact duplicate groups | 388 |
| Extra duplicate chunks | 1,251 |

Blocking failures:

| ID | Severity | Finding |
|---|---|---|
| CORPUS-001 | S1 | MA000095 and MA000121 are absent |
| CORPUS-NAME-MA000002 | S1 | MA000002 is labelled `Workplace Relations Act 1996` |
| REPRO-001 | S1 | `data/awards/` is absent |
| EVAL-001 | S1 | evaluation provenance fields are absent |
| CORPUS-004 | S2 | 1,251 extra exact duplicate chunks |

The store also contains eight Award IDs outside the current 122-item A-Z evidence list: MA000123, MA000132, MA000134, MA000135, MA000136, MA000150, MA000152, and MA000155. These may be enterprise or public-sector sources, but their inclusion in the product scope is not approved in the supplied requirements.

## NES result

The local combined NES text contains current entitlement terms, but it also contains navigation, translation-language lists, footer material, and mojibake such as malformed Arabic, Chinese, Greek, and accented text.

The source requirements PDF does not list all items on the current Fair Work NES page. This creates a requirements-baseline defect before application testing begins.

## Secret result

Observed:

- only `.env.example` is tracked;
- two commits touched `.env.example`;
- history search found the placeholder-shaped `gsk_` pattern in `.env.example`;
- no actual secret value was printed during the audit.

Limitation:

This was a targeted pattern and path search, not a full entropy-based history scan. A dedicated secret scanner is still required.

## Stop conditions applied

The test strategy says answer evaluation is invalid when the corpus gate fails. Therefore:

- no API spend was incurred;
- no historical answer score was accepted;
- no latency claim was made;
- no cost-per-answer claim was made;
- no deployment was attempted.

This is both a quality control and a cost control. Paying for model calls over an unidentified corpus would produce unusable evidence.

## Required phase 2 inputs

Before corpus and retrieval testing can pass, the project needs:

1. the exact 122 approved source documents;
2. source URL, Award ID, title, effective date, retrieval time, and SHA-256 for each source;
3. a reviewed decision on the eight out-of-scope IDs;
4. corrected sources for MA000002, MA000095, and MA000121;
5. a current NES baseline;
6. a clean candidate branch or commit;
7. a decision on whether the pre-boundary code changes are accepted, rejected, or separated.

## Step 1 conclusion

The repository is inspectable and the current proposed test foundation runs. Reproducibility and corpus identity fail. The next valid activity is source-corpus verification and test-data preparation, not answer scoring.
