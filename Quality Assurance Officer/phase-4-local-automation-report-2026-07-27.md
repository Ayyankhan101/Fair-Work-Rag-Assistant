# Phase 4 local automation report

Date: 27 July 2026

Result: failed

This report covers read-only test execution against the current working tree. It does not qualify the committed branch, a clean checkout, or a release build.

## Test point

| Field | Value |
|---|---|
| Branch | `QA` |
| HEAD | `fb9028a8978393968788038492c7d17af02ed42b` |
| Candidate state | dirty |
| Modified tracked files | 20 |
| Tests at HEAD | 0 |
| Executable working-tree tests | 16 untracked `unittest` methods |
| Provider credentials available | none |

The current results are diagnostic. They cannot be promoted to release evidence because the tested files are mutable and the tests are not part of HEAD.

## Results

| Check | Result | Qualification |
|---|---|---|
| `python -m unittest discover -s tests -v` | pass, 16 of 16 | host environment; critical RAG dependencies absent |
| isolated unit run | pass, 16 of 16 in 0.103 seconds | current requirements resolved through `uv` |
| statement coverage | 12% | 571 of 652 statements missed |
| Ruff check, CI scope | pass | `src/` and `scripts/` |
| Ruff format, CI scope | pass | 17 files |
| expanded Ruff check | pass | `src/`, `scripts/`, `tests/`, and `qa/scripts/` |
| expanded Ruff format | pass | 23 files |
| documentation style | pass | 37 Markdown files at the test point |
| Git whitespace check | pass | line-ending warnings remain |
| isolated requirements import | pass on cached retry | first cold attempt exceeded 60 seconds |
| application import | timeout twice | exceeded 20 seconds and then 50 seconds |
| live provider tests | not run | no provider key or approved spend |

Green lint and 16 passing unit tests do not offset the 12% coverage result.

## Coverage

Coverage was measured with `coverage` in an isolated requirements environment. The coverage data file was directed to the operating-system temporary directory.

| Module | Statements | Missed | Coverage |
|---|---:|---:|---:|
| `src/app.py` | 47 | 47 | 0% |
| `src/bm25_retriever.py` | 36 | 36 | 0% |
| `src/cag.py` | 46 | 10 | 78% |
| `src/config.py` | 22 | 1 | 95% |
| `src/fastembeddings.py` | 10 | 10 | 0% |
| `src/filtered_retriever.py` | 89 | 89 | 0% |
| `src/hybrid_retriever.py` | 36 | 36 | 0% |
| `src/ingest.py` | 166 | 166 | 0% |
| `src/rag.py` | 104 | 104 | 0% |
| `src/router.py` | 24 | 0 | 100% |
| `src/vectorstore.py` | 72 | 72 | 0% |
| Total | 652 | 571 | 12% |

The untested modules contain the source parser, chunker, embedding adapter, vector store, BM25 and hybrid retrieval, answer chain, provider call, failure handling, and user interface. Those are the product's main risk paths.

## Test-quality findings

The current 16 tests are useful regression examples, but they are not a system suite.

1. Four prompt tests search for literal strings inside `src/rag.py`. They do not render the role messages, call a model, parse an answer, or verify claim support.
2. Router tests cover a few aliases and routes. They do not cover the official 122-Award scope, ambiguity, negation, misspellings, collisions, or route-to-context agreement.
3. CAG tests cover file absence, one routing boundary, and text preservation. They do not prove that the accepted NES source is current or complete.
4. No test covers corpus acceptance, parser correctness, duplicate handling, vector-store persistence, retrieval recall, citation support, rate tables, calculations, provider failures, privacy, UI behavior, or deployment.
5. Test data contains visible mojibake sequences. A test can preserve corrupted text and still pass.
6. No mutation, branch, property, fuzz, concurrency, or cross-platform result exists.

The 485 documented test cases remain specifications. They have not been converted into executable, reviewed, traceable tests.

## Dependency result

The unpinned requirements resolved to the following direct package versions during this run:

```text
turbovec==0.8.0
langchain==1.3.14
langchain-groq==1.1.3
groq==0.37.1
fastembed==0.8.0
pdfplumber==0.11.10
gradio==6.20.0
python-dotenv==1.2.2
beautifulsoup4==4.15.0
lxml==6.1.1
numpy==2.4.0
rank-bm25==0.2.2
```

The resolver warned that `numpy==2.4.0` is yanked for a backward-compatibility bug. A dependency graph that selects a yanked package is not acceptable for a release, even though imports and the small unit suite happened to pass.

The first clean `uv` attempt exceeded 60 seconds. A retry succeeded from the populated cache. This is not a repeatable clean-install duration and must not be reported as a six-second installation.

The host Python executable had no `pip` module and lacked most runtime dependencies. The host-level `pip check` failure therefore describes the QA host, not an inconsistent project installation. Dependency consistency still needs to be tested from a locked clean environment.

## Import and startup result

After isolated dependency installation, these modules imported successfully:

```text
bm25_retriever
cag
config
fastembeddings
filtered_retriever
hybrid_retriever
ingest
rag
router
vectorstore
```

Importing `app` did not complete within 20 seconds. A second attempt did not complete within 50 seconds.

`src/app.py` performs CAG loading, embedding construction, vector-store loading or building, RAG-chain construction, and UI construction at module import time. The probe does not identify which operation consumed the time because startup tracing is absent. It does prove that import safety and cold-start performance are not controlled.

## Current API-client configuration

The effective `ChatGroq` configuration was inspected with a dummy, non-working key. No request was sent.

| Field | Effective value |
|---|---|
| Primary model | `llama-3.3-70b-versatile` |
| Fallback model | `llama-3.1-8b-instant` |
| Temperature | `1e-08` after client normalization of zero |
| Maximum output tokens | 1,024 |
| Request timeout | none |
| Client retry count | 2, inherited default |
| Streaming | false |
| Output count | 1 |

Construction without `GROQ_API_KEY` raises `GroqError`. The UI starts constructing the chain during import, so missing credentials are not handled through an explicit readiness gate.

## Offline fallback probe

A fake runnable raised `HTTP 429 rate_limit`. `get_llm()` was replaced in memory with a capture runnable. No provider request was made.

The fallback returned the fake response, but the rendered prompt was defective:

| Observation | Result |
|---|---|
| Rendered messages | one |
| Message type | `HumanMessage` |
| System message | absent |
| Context value | nested dictionary representation |
| User-question occurrences | two |
| Smaller context | not produced |

The fallback wraps the original parallel `context` and `question` mapping inside another `context` field. This changes the prompt shape, repeats the question, and still does not create the required system/user role boundary. A provider outage can therefore switch both model and prompt structure at the same time.

## Stop conditions

The following Phase 4 exits did not pass:

- critical-path coverage at or above the approved threshold;
- tracked tests in an immutable candidate;
- clean locked installation;
- yanked-package exclusion;
- bounded application cold start;
- provider contract tests;
- model-output schema validation;
- claim-to-citation validation;
- live failure, timeout, and retry tests.

## Required next work

Engineering must create the testable candidate. QA must not silently turn the current working-tree tests into release evidence.

1. Decide the existing 20-file product patch.
2. Create an immutable candidate with reviewed, tracked tests.
3. Lock dependencies with hashes and reject yanked releases.
4. Separate application construction from module import.
5. Add deterministic fixtures for ingestion, stores, retrieval, and provider responses.
6. Convert the highest-risk documented cases into executable tests.
7. Run coverage, mutation, integration, and failure tests on Linux and Windows.
8. Execute the provider matrix defined in the API assurance report.

Phase 4 remains failed until those results exist.
