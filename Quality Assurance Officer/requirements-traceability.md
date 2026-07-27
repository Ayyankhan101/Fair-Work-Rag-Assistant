# Requirements traceability

Status values are `pass`, `partial`, `fail`, and `not run`.

| ID | Requirement | Implementation evidence | QA evidence | Status |
|---|---|---|---|---|
| DATA-001 | Index all 122 mandatory Awards | `src/ingest.py`, `data/vectorstore/docstore.json` | `python qa/scripts/audit_repository.py` | fail |
| DATA-002 | Include current NES | `data/nes/nes_combined.txt`, `src/cag.py` | `tests/test_cag.py` | partial |
| DATA-003 | Identify every source by Award ID | chunk text and `source_file` | corpus audit | fail |
| DATA-004 | Record source version and checksum | no current field | corpus audit | fail |
| DATA-005 | Keep extra enterprise/public sources separate | no corpus-class field | corpus audit | fail |
| PROC-001 | Preserve clause and schedule boundaries | `parse_pdf_structure()` | no fixture suite | partial |
| PROC-002 | Keep page references | no page metadata in stored chunks | metadata audit | fail |
| PROC-003 | Reject unreadable input | `extract_award_name_from_pdf()` | unit fixture needed | partial |
| PROC-004 | Fail a build if any source fails | `ingest_all()` | code inspection | pass |
| META-001 | Store Award name | chunk metadata | corpus audit | partial |
| META-002 | Store clause and section | chunk metadata | corpus audit | pass |
| META-003 | Store source URL | chunk metadata | URL verification not run | partial |
| META-004 | Store document type | chunk metadata | corpus audit | pass |
| CAG-001 | Use CAG for NES-only questions | `src/router.py`, `src/rag.py` | `tests/test_config_router.py` | pass |
| CAG-002 | Preserve NES entitlement text | `src/cag.py` | `tests/test_cag.py` | pass |
| CAG-003 | Version the cache | no cache manifest | corpus audit | fail |
| RAG-001 | Retrieve the requested Award | filtered and hybrid retrievers | three-query smoke script only | partial |
| RAG-002 | Retrieve the requested clause | retrievers | no labelled clause-recall suite | not run |
| RAG-003 | Cover every mandatory Award | small alias list and no per-Award set | corpus audit | fail |
| ROUTE-001 | Route NES, Award, and combined queries | `route_question()` | router unit tests | pass |
| ROUTE-002 | Display the route actually used | shared decision in `src/rag.py` and UI | integration test needed | partial |
| ANSWER-001 | Answer only from accepted context | `RAG_PROMPT_TEMPLATE` | prompt safety tests | fail: prompt-only rule and no claim validator |
| ANSWER-002 | Cite Award/NES and clause | five-field output | format checks only | partial |
| ANSWER-003 | State when evidence is insufficient | dirty working-tree prompt rule and example | prompt safety tests | partial: unaccepted and not role-separated |
| ANSWER-004 | Avoid unsupported legal advice | prompt rule | adversarial answer set not run | partial |
| ANSWER-005 | Handle ambiguous Award coverage | prompt rule | ambiguity set not run | partial |
| NFR-001 | Respond within a few seconds | README claims 3-7 seconds | no dated benchmark | not run |
| NFR-002 | Support source updates | rebuild scripts | no version agreement or freshness gate | fail |
| NFR-003 | Reproduce the store from source | `data/awards/` absent | repository audit | fail |
| NFR-004 | Run on Windows and Linux | UTF-8 cache fix, Unix scripts remain | Windows full run not complete | partial |
| SEC-001 | Keep secrets out of source and logs | `.gitignore`, `.env.example` | secret-history scan not run | partial |
| SEC-002 | Resist prompt injection | prompt rule | 120-case prompt suite not run | fail: no system-role boundary |
| SEC-003 | Do not disclose server exceptions | generic UI response | unit test needed | partial |
| SEC-004 | Control unsafe serialization | committed pickle cache | security review | fail |
| QA-001 | Offline gates run on each pull request | `.github/workflows/ci.yml` | CI not observed after changes | partial |
| QA-002 | Evaluation evidence is attributable | result JSON lacks provenance | repository audit | fail |
| QA-003 | Release has no S0 or S1 defects | defect register | open S1 defects | fail |
