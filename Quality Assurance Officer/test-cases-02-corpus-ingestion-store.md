# Test cases 02: corpus, ingestion, cache, and vector store

## Data rule

Corpus tests run before retrieval or answer tests.

Each source record must contain:

```text
source_id
document_type
official_title
Award ID or NES section
official URL
effective date
retrieved_at_utc
content_type
byte_count
page_count when applicable
SHA-256
parser version
license or use basis
```

The expected Award list is the dated 122-ID file in `evidence/official-award-scope-2026-07-27.json`. A later run must reacquire and approve a new list rather than silently editing the old evidence.

## Corpus cases

| ID | Risk | Procedure | Pass condition |
|---|---|---|---|
| COR-001 | Missing Award | for each of 122 official IDs, locate exactly one approved source | 122 of 122 present |
| COR-002 | Extra Award | list IDs outside the approved 122 and review each | zero unapproved extra |
| COR-003 | Wrong title | compare extracted and metadata titles with official title by ID | 122 of 122 exact approved match |
| COR-004 | Wrong ID | search source text for the controlling Award ID | metadata and text agree |
| COR-005 | Duplicate file | group source files by SHA-256 | zero unexplained duplicate |
| COR-006 | Near duplicate | compare normalized text and source dates | every superseded or alternate copy classified |
| COR-007 | Empty source | measure bytes and extracted substantive characters | zero empty source |
| COR-008 | Corrupt source | open every source with strict parser settings | zero parser error |
| COR-009 | Encrypted source | inspect PDF encryption and permissions | zero undeclared encryption |
| COR-010 | Scanned source | measure text coverage per page and inspect low-text pages | every page readable or OCR-approved |
| COR-011 | Missing page | compare page count with official artifact | counts agree |
| COR-012 | Truncated source | compare first and last clauses, schedules, and file trailer | complete document |
| COR-013 | Wrong content type | verify signature, extension, MIME type, and parser choice | all four agree |
| COR-014 | Redirected URL | request source URL and record redirect chain | ends at approved Fair Work source |
| COR-015 | Broken source URL | request each URL with a dated user agent | 100% successful or accepted archive |
| COR-016 | Unknown effective date | extract and review publication/effective date | 100% dated |
| COR-017 | Stale source | compare with official current version and update feed | zero unapproved stale source |
| COR-018 | Checksum drift | reacquire source and compare normalized and raw hashes | expected drift explained and versioned |
| COR-019 | Title-only parsing | test generic titles such as `Award 2020` | generic title rejected |
| COR-020 | Clause loss | sample coverage, pay, hours, overtime, breaks, leave, termination, dispute, and schedules | every sample present |
| COR-021 | Table loss | compare wage and allowance tables with rendered source | values, headers, units, and footnotes preserved |
| COR-022 | Schedule loss | compare final schedules and appendices | all schedules present and ordered |
| COR-023 | Footnote loss | sample footnotes affecting rates or eligibility | linked to the correct value |
| COR-024 | Encoding damage | scan for replacement characters and mojibake patterns; visually verify hits | zero unresolved damage |
| COR-025 | Navigation contamination | quantify menus, cookies, translations, feedback, and footer text | non-source chrome excluded |
| COR-026 | Over-cleaning | diff cleaned text against substantive source blocks | zero substantive deletion |
| COR-027 | NES scope drift | compare local NES headings with current official entitlement list | all current items represented |
| COR-028 | NES source mixture | identify every page combined into the NES text | only approved NES material included |
| COR-029 | Legal source tier | label Ombudsman guidance, Commission Award, legislation, and secondary material | authority level retained |
| COR-030 | Human source review | employment-law reviewer checks manifest and high-impact extracts | approval recorded with date |

`COR-001`, `COR-003`, `COR-004`, and `COR-020` are parameterized. Their minimum combined execution count is 488, not four.

## Ingestion cases

| ID | Risk | Procedure | Pass condition |
|---|---|---|---|
| ING-001 | Non-deterministic ingestion | run twice from identical files and configuration | ordered chunk manifest hashes match |
| ING-002 | Source silently skipped | ingest all approved sources and compare source IDs | every source produces chunks |
| ING-003 | Error swallowed | add one corrupt fixture among valid fixtures | run fails and identifies the corrupt source |
| ING-004 | Partial output accepted | interrupt after a controlled batch | output marked incomplete and cannot load as complete |
| ING-005 | Resume duplication | interrupt, resume, and compare with clean rebuild | identical chunks and count |
| ING-006 | Rebuild appends | run complete build twice against same target | second run is no-op or safe replacement |
| ING-007 | Wrong parser | provide HTML, text, and PDF fixtures | correct parser selected by verified type |
| ING-008 | Blank PDF | ingest a PDF with blank pages | controlled rejection with source ID |
| ING-009 | Encrypted PDF | ingest password-protected fixture | controlled rejection; no hang |
| ING-010 | Malformed PDF | ingest truncated and object-bomb fixtures under limits | controlled failure within time and memory limit |
| ING-011 | Unicode loss | ingest names, apostrophes, symbols, and multilingual navigation | substantive Unicode preserved |
| ING-012 | Clause split | place a clause heading at a page and chunk boundary | heading remains linked to clause text |
| ING-013 | Table split | place row, unit, and footnote near boundaries | relationship preserved |
| ING-014 | Schedule split | ingest long classification schedule | schedule identity on every chunk |
| ING-015 | Oversized chunk | measure characters and tokens for every chunk | within declared maximum |
| ING-016 | Tiny fragment | inspect chunks below minimum useful size | zero unexplained fragment |
| ING-017 | Bad overlap | recompute adjacent overlap | declared overlap without repeated full sections |
| ING-018 | Empty chunk | trim and test every stored text | zero empty chunk |
| ING-019 | Duplicate chunk | hash normalized chunk text within and across sources | zero unexplained duplicate |
| ING-020 | Metadata omission | validate required schema on every chunk | 100% complete |
| ING-021 | Metadata type drift | validate strings, integers, dates, URLs, and enums | zero type error |
| ING-022 | Page off by one | compare first, middle, and last sampled chunks with source page | exact human page reference |
| ING-023 | Clause hallucinated | compare parsed clause with source heading | exact or explicitly unknown |
| ING-024 | Wrong source URL | resolve chunk URL against its manifest record | 100% match |
| ING-025 | Cross-source contamination | tag sentinel fixtures and inspect chunks | no chunk contains two source identities |
| ING-026 | Cleaning order defect | run cleaning before and after structural extraction on fixture | approved order preserves more required structure |
| ING-027 | Excess memory | ingest largest source while sampling peak RSS | below approved worker limit |
| ING-028 | Excess time | time each source and total ingestion | within rebuild service level |
| ING-029 | Log leakage | insert canary personal and secret-like strings in fixture | logs contain IDs, not raw sensitive content |
| ING-030 | Ingestion provenance | inspect generated manifest | code, parser, source, config, and time recorded |

## Cache and vector-store cases

| ID | Risk | Procedure | Pass condition |
|---|---|---|---|
| STO-001 | Store count mismatch | compare manifest chunk count, docstore count, and index count | all equal |
| STO-002 | Missing vector | verify an index entry for every chunk ID | 100% present |
| STO-003 | Orphan vector | enumerate vectors without manifest chunk | zero orphan |
| STO-004 | Dimension mismatch | compare model output dimension with index metadata | exact match |
| STO-005 | Wrong embedding model | record model name, revision, files, and hash | matches approved configuration |
| STO-006 | Unnormalized assumption | sample vector norms and distance behavior | matches retriever metric requirements |
| STO-007 | Unsafe cache load | tamper with cache in an isolated environment | loader rejects before deserialization |
| STO-008 | Unsigned artifact | alter one byte of each artifact | checksum verification blocks load |
| STO-009 | CAG/RAG version split | load intentionally mismatched manifest IDs | startup fails safely |
| STO-010 | Stale store | change one source without rebuild | startup or query identifies stale store |
| STO-011 | Atomic publish | interrupt store publication | previous complete store remains loadable |
| STO-012 | Rollback | activate prior signed store and run smoke set | documented rollback succeeds |
| STO-013 | Concurrent load | start multiple read-only workers | no corruption or uncontrolled duplicate memory |
| STO-014 | Concurrent rebuild | attempt two builders on same target | lock or isolated target prevents collision |
| STO-015 | Filter correctness | query each Award filter by exact metadata value | only target source class returned |
| STO-016 | Filter missing value | query nonexistent and null filters | empty controlled result |
| STO-017 | Persistence round trip | build, dump, reload, and repeat labelled searches | chunk IDs and ranking unchanged within tolerance |
| STO-018 | Cross-platform load | load approved artifact on Windows and Linux | both pass or platform scope is explicit |
| STO-019 | Storage budget | record raw corpus, cache, docstore, index, and total bytes | within approved deployment budget |
| STO-020 | Backup restore | restore artifacts and manifest into clean environment | integrity checks and smoke set pass |

## Current status

| Group | Defined cases | Minimum executions | Status |
|---|---:|---:|---|
| Corpus | 30 | at least 514 | failed at baseline |
| Ingestion | 30 | at least 30 plus fixtures | not run |
| Cache and vector store | 20 | at least 20 | partial inspection |
| Total | 80 | at least 564 | incomplete |

The corpus group cannot pass until raw Award sources are supplied. Store inspection cannot substitute for source verification.

