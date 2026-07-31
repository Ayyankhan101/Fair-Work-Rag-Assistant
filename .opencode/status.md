# Mission Status — Evidence-Based

Generated: 2026-07-30

## Evidence Files
- `data/hard_eval_results.json` — Eval results with provenance
- `data/awards_manifest.json` — Corpus manifest (122 Awards)
- `data/provenance_log.jsonl` — Per-request audit trail
- `data/provider_conformance_results.json` — Live API tests
- `data/docs_cache.pkl` — Cached ingested docs
- `STATUS.md` — Evidence-based project status
- `.coveragerc` — Coverage configuration

## Build Health
- **Branch**: develop
- **Tests**: 67 passing (pytest)
- **Lint**: 0 errors (ruff)
- **Accuracy**: 87.5% (22/25 hard questions)
- **Vector store**: 16622 docs from 122 PDFs + NES

## Defect Summary (from defect register)
| Severity | Fixed | Partial | Open | Total |
|----------|-------|---------|------|-------|
| S0 | 0 | 0 | 0 | 0 |
| S1 | 30 | 8 | 5 | 43 |
| S2 | 18 | 6 | 3 | 27 |
| S3 | 3 | 0 | 0 | 3 |
| **Total** | **51** | **14** | **8** | **73** |

## Blocked Items (Require External Action)
- DEF-010: Eval rerun needs Groq API key
- DEF-021: CRLF verification needs Linux
- DEF-027: DOCX verification needs LibreOffice
- DEF-029: pip-audit needs network access
- DEF-069: Award case matching needs live rerun
