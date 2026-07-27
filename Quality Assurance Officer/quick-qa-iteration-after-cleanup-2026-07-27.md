# Quick QA iteration after branch cleanup

Date: 27 July 2026

Test point:

| Field | Value |
|---|---|
| branch | `QA` |
| `HEAD` | `fb9028a8978393968788038492c7d17af02ed42b` |
| protected product baseline | `3e91e9e16c7417269242d7ef2f6f04bb6a49efff` |
| operating system | Windows |
| direct Python | 3.11.15 |
| Ruff | 0.16.0 |
| live provider keys | none detected |

## Result

Release blocked.

The cleanup passed its ownership gate: every non-QA path equals the fork-point tree. The restored application did not pass the executable gates.

## Execution summary

| Check | Result | Meaning |
|---|---|---|
| product tree versus fork point | pass, zero changed paths | QA product edits are no longer present |
| root README object | pass, exact merge-base object | original development README restored |
| Python syntax | pass, 29 of 29 files parsed | no syntax error in checked product or QA sources |
| QA unit suite | fail, 2 of 16 methods passed | encoding, CAG, routing, Award detection, and prompt rules fail |
| clean declared-dependency import | fail | `rank_bm25` absent from `requirements.txt` |
| natural Windows request matrix | blocked before request 1 | NES read raises `UnicodeDecodeError` |
| diagnostic forced-UTF-8 matrix | fail, 31 of 60 cases | deeper routing and retrieval defects remain |
| repository and corpus audit | fail, release blocked | missing/mislabelled Awards, duplicates, provenance, and reproducibility failures |
| Ruff check | fail, 90 findings | product static-quality gate fails |
| Ruff format check | fail, 17 of 18 files | product formatting gate fails |
| live LLM/API evaluation | blocked | no approved credentials or spend |

## Unit-test detail

Command:

```powershell
python -m unittest discover -s "Quality Assurance Officer/tests" -v
```

The runner reported:

```text
Ran 16 tests
FAILED (failures=14, errors=4)
```

The counts include failed subtests, so failure records plus errors exceed the number of methods.

The two passing methods were:

- missing CAG file returns an empty cache;
- the two tested topic aliases for salary and annual leave resolve as expected.

Observed failure classes:

- CAG deletes valid entitlement lines;
- platform-default decoding corrupts or blocks UTF-8 text;
- CAG treats Award meal-break and overtime questions as NES candidates;
- generic mining maps to Black Coal;
- marine towage maps to marine tourism;
- several common occupation aliases do not resolve;
- substring matching maps `transport logistics` to Sporting Organisations;
- router tests expose an API that requires a cache object and does not match the intended test contract;
- the prompt forces specific answers and numbers;
- the prompt lacks an insufficient-evidence state;
- the prompt does not mark retrieved instructions as untrusted.

Raw output:

- `evidence/post-cleanup-unit-tests-2026-07-27.stdout.txt`;
- `evidence/post-cleanup-unit-tests-2026-07-27.stderr.txt`.

The earlier misquoted runner attempt is retained under filenames containing `invocation-error`.

## Dependency detail

The exact baseline requirements command was:

```powershell
uv run --with-requirements requirements.txt `
  python "Quality Assurance Officer/tools/offline_request_matrix.py" --help
```

It failed while importing `rag.py`:

```text
ModuleNotFoundError: No module named 'rank_bm25'
```

This is DEF-070. `rank-bm25` was then supplied with `uv --with` only to diagnose behavior below the import layer. That does not fix the baseline or make the dependency gate pass.

The resolver also selected yanked `numpy==2.4.0`, confirming the existing dependency-control defect.

## Request-matrix detail

Natural Windows command, after only the missing dependency was supplied:

```powershell
uv run --with-requirements requirements.txt --with rank-bm25 `
  python "Quality Assurance Officer/tools/offline_request_matrix.py"
```

It stopped in `src/cag.py` before request one:

```text
UnicodeDecodeError: 'charmap' codec can't decode byte 0x8d in position 1009
```

The diagnostic rerun added `PYTHONUTF8=1`. It did not edit code.

| Metric | Result |
|---|---:|
| cases | 60 |
| all applicable checks passed | 31 |
| failed | 29 |
| route | 58/60 |
| Award detection | 25/38 |
| topic detection | 39/47 |
| expected Award present in context | 22/36 |
| CAG presence | 19/19 |
| clarification | 0/9 |
| chain execution with capture model | 60/60 |
| prompt role shape | 60 human-role messages |
| prompt length | 4,221 to 39,361 characters |
| mean prompt length | 25,208 characters |
| elapsed | 22.332 seconds on the final evidence rerun |

These are provider-free diagnostic checks. They do not measure legal correctness or live model answer quality.

Machine-readable result:

```text
evidence/offline-request-matrix-post-cleanup-baseline-forced-utf8-2026-07-27.json
SHA-256 E2CFFE2ED68D079362BB4E30DE56B7B24878197E19F6C242A6328D3EB705810C
runner SHA-256 89FB85D8F9879DB4C9A9C11EB91B17E54979F3A81BCBD63EA7A49F55D9B97C2C
```

## Corpus-audit detail

The post-cleanup audit found:

| Measure | Result |
|---|---:|
| documents | 16,692 |
| Award chunks | 16,665 |
| NES chunks | 27 |
| expected official Award IDs | 122 |
| missing official IDs | 2 |
| outside-scope IDs in store | 8 |
| duplicate text groups | 388 |
| extra duplicate chunks | 1,251 |
| empty text chunks | 0 |
| required metadata omissions | 0 |

Release blockers include missing MA000095 and MA000121, incorrect MA000002 identity, absent hard-evaluation provenance, and absent raw `data/awards`.

Machine-readable result:

```text
evidence/post-cleanup-repository-audit-2026-07-27.json
SHA-256 C72203AA21EECEE310DFA4207C704C3137DB6B5FE8FE8E804C9BABEAB722C296
```

## Static-check detail

Ruff checked `build_store.py`, `src`, and `scripts`.

| Check | Result |
|---|---|
| `ruff check` | 90 findings; 74 marked automatically fixable |
| `ruff format --check` | 17 files would change; one already formatted |

QA did not apply fixes because product files are outside QA ownership.

## Exit decision

The iteration exits with:

- branch-ownership cleanup: passed;
- application qualification: failed;
- release: blocked;
- live provider testing: blocked;
- next owner: engineering.

Engineering must return an immutable candidate with declared and locked dependencies, explicit UTF-8 handling, corrected Award identity and routing, a safe prompt contract, tracked tests, and a reproducible corpus. QA must then rerun the same gates without diagnostic environment overrides.
