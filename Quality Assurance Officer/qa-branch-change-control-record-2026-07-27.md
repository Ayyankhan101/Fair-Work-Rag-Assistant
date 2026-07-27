# QA branch change-control record

Date: 27 July 2026

Operator role: quality assurance

Repository: `fair-work-rag-assistant`

Branch: `QA`

## Decision

QA does not own product implementation. The inherited product tree is therefore protected at the common ancestor of `QA` and `develop`, not at the current tip of either branch.

The protected baseline is:

```text
3e91e9e16c7417269242d7ef2f6f04bb6a49efff
Add auto-pr script and update context
```

This choice avoids two invalid actions:

1. approving QA working changes as product code;
2. silently importing four later development commits that QA has not qualified.

## Git identity before cleanup

| Field | Value |
|---|---|
| QA `HEAD` | `fb9028a8978393968788038492c7d17af02ed42b` |
| `develop` at inspection | `dd3bd45d58f430b6f88a927d7eee6ce1a815098d` |
| merge base | `3e91e9e16c7417269242d7ef2f6f04bb6a49efff` |
| QA-only commits | 1 |
| develop-only commits | 4 |
| committed QA delta from merge base | root `README.md` only |

The QA-only commit added a quality-assurance banner to the product README. The restored working copy removes that banner and recovers the exact fork-point README.

The four development-only commits were not merged. At inspection, their product delta from the merge base was:

- modified `.gitignore`;
- modified `build_store.py`;
- added `scripts/convert_pdfs_to_markdown.py`;
- added `scripts/ingest_markdown.py`;
- modified `src/ingest.py`;
- modified `src/rag.py`.

## State preserved before restoration

There were 20 modified tracked product files, with 994 inserted and 918 deleted lines. One QA audit script was staged as a new file. QA tests and another QA script were untracked.

Three recovery patches were written before restoration:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `evidence/pre-reversion-unstaged-product-diff-2026-07-27.patch` | 122,841 | `8DB087EB9A20D5CEBFDDB057F0EB1AED9286F61940A38D90BF88C743B6C61A12` |
| `evidence/pre-reversion-staged-diff-2026-07-27.patch` | 7,785 | `3B49D5B8AF73133D823BF9D0DC275206DE49628FC2B53116A2F1E72CC669A489` |
| `evidence/qa-commit-versus-fork-point-2026-07-27.patch` | 384 | `B8B7529C8A65814549861876DBFF52129C5FBDDD1814D9955DDB741D444558C5` |

The machine-readable pre-state is `evidence/pre-reversion-state-2026-07-27.json`.

README recovery is also available from Git objects:

| Version | Git object |
|---|---|
| original merge-base README | `2954b27f375aaa7ec884a4d13841236b12777d76` |
| QA `HEAD` README | `d23c67ec09c5210d5ae474a02f74ad0c19908741` |
| dirty pre-restoration README | `9b14f2984b04e67fabdfddb434fd4074d7a62a74` |

The dirty README is recoverable from the unstaged patch. The other two are recoverable from Git.

## QA assets retained

QA-created source was retained, not discarded:

| Before | After |
|---|---|
| `tests/__init__.py` | `Quality Assurance Officer/tests/__init__.py` |
| `tests/test_cag.py` | `Quality Assurance Officer/tests/test_cag.py` |
| `tests/test_config_router.py` | `Quality Assurance Officer/tests/test_config_router.py` |
| `tests/test_prompt_safety.py` | `Quality Assurance Officer/tests/test_prompt_safety.py` |
| `qa/scripts/audit_repository.py` | `Quality Assurance Officer/tools/audit_repository.py` |
| `qa/scripts/check_documentation_style.py` | `Quality Assurance Officer/tools/check_documentation_style.py` |

The three test modules were updated only to resolve the repository root from their new location. No test expectation was weakened.

Pre-move source hashes are in the pre-state JSON. Generated Python bytecode was moved out of the repository to:

```text
C:\Users\HP\AppData\Local\Temp\fwra-root-tests-pycache-pre-reversion-2026-07-27
C:\Users\HP\AppData\Local\Temp\fwra-root-qa-scripts-pycache-pre-reversion-2026-07-27
C:\Users\HP\AppData\Local\Temp\fwra-qa-tests-pycache-post-cleanup-2026-07-27
C:\Users\HP\AppData\Local\Temp\fwra-root-pycache-post-cleanup-2026-07-27
C:\Users\HP\AppData\Local\Temp\fwra-scripts-pycache-post-cleanup-2026-07-27
C:\Users\HP\AppData\Local\Temp\fwra-src-pycache-post-cleanup-2026-07-27
C:\Users\HP\AppData\Local\Temp\fwra-root-ruff-cache-post-cleanup-2026-07-27
```

Those directories are temporary diagnostic residue, not source or release evidence.

The empty QA-created root directories `qa/scripts` and `qa` were removed after their source files were relocated. No file was present in either directory at removal.

## Product paths restored

The following paths were restored from the merge base:

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

No product path was restored from current `develop`, because current `develop` is not the inherited QA baseline.

## Verification after restoration

The controlling comparison is:

```powershell
git diff --name-status 3e91e9e16c7417269242d7ef2f6f04bb6a49efff -- . `
  ':(exclude)Quality Assurance Officer/**'
```

Result: no output.

This proves that every path outside the QA folder has the same Git content as the fork point.

The root README checks were:

```text
merge-base object: 2954b27f375aaa7ec884a4d13841236b12777d76
working-copy object: 2954b27f375aaa7ec884a4d13841236b12777d76
```

The comparison with QA `HEAD` shows only:

```text
M README.md
```

That difference is intentional. It reverses the QA banner committed after the branch split. A commit was not created, staged, pushed, merged, or rebased during this cleanup.

## Why Git status is not empty

An empty `git status` is not the correct proof for this task:

- `README.md` must differ from QA `HEAD` to recover the original inherited README;
- `Quality Assurance Officer/` contains the requested QA package and remains untracked until review;
- the branch still contains the historical QA README commit in its ancestry.

The correct proof is equality to the merge base outside the QA folder.

## Errors during the procedure

Two operator errors occurred and are retained in the record.

1. The first restore safety guard interpreted the silent output of `git cat-file -e` as a missing file. It stopped before `git restore` ran. The guard was corrected to check Git’s exit code.
2. The first attempt to capture the unit-test transcript passed the spaced QA path incorrectly to `Start-Process`. It produced an importable-directory error. Those files were renamed with `invocation-error` in their names. A correctly quoted run was then captured separately.

Neither error changed product source.

## Ownership outcome

There are now two README files with different owners:

1. root `README.md`: original development README from the fork point;
2. `Quality Assurance Officer/README.md`: QA navigation, results, and limitations.

Engineering owns any product correction. QA owns test design, independent execution, evidence, defect reporting, and release advice.

## Required reviewer checks

Before accepting this cleanup, a reviewer should:

1. recompute the three patch hashes;
2. rerun the merge-base comparison excluding the QA folder;
3. confirm the root README object hash;
4. inspect the post-cleanup Git status;
5. decide whether QA evidence will be committed on this branch or submitted separately;
6. select a new immutable engineering candidate before remediation testing.
