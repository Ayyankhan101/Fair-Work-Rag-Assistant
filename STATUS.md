# STATUS.md — Evidence-Based Project Status

## Build Health
- **Branch**: develop
- **Last Commit**: e045062 (revert)
- **Tests**: 67 passing (pytest)
- **Coverage**: 37% (threshold: 35%)
- **Accuracy**: 92% (23/25 hard questions)
- **Vector Store**: 16,622 docs from 122 PDFs + NES

## Defect Summary (DEF-001 to DEF-070)
| Metric | Count |
|--------|-------|
| Total Checked | 78 |
| Passed | 77 (98.7%) |
| Failed | 1 |

### Failed Defects
- **DEF-029**: pip-audit has 9 fixable vulnerabilities in transitive dependencies (pypdf, gitpython, pytest, click, etc.)

## Key Metrics
| Item | Value |
|------|-------|
| Award Mappings | 100+ MA codes in config.py |
| Alias Patterns | 233 keyword-to-Award mappings |
| NES Keywords | 60+ national employment standards terms |
| Topic Categories | 41 topic detection categories |
| Test Files | 5 test files in tests/ |
| CI Workflows | 2 GitHub Actions workflows |

## Evidence Files
- `data/hard_eval_results.json` — Eval results with provenance
- `data/awards_manifest.json` — Corpus manifest (122 Awards)
- `data/awards_receipts.json` — Award download receipts
- `data/provenance_log.jsonl` — Per-request audit trail
- `data/provider_conformance_results.json` — Live API tests
- `STATUS.md` — This file
- `.coveragerc` — Coverage configuration (threshold: 35%)
- `requirements.txt` — Pinned dependency versions
- `src/model_config.py` — Provider config from env vars
- `src/provenance.py` — Per-request provenance logging
- `scripts/test_provider.py` — Live API conformance tests
- `scripts/wait_and_verify.sh` — Service verification
- `docs/deployment-controls.md` — Deployment controls
- `archive/` — Pre-QA notes archive

## Resolved Defects (77/78)
All defects from DEF-001 to DEF-070 have been addressed except DEF-029 (transitive dependency vulnerabilities).

### Key Resolutions
- **Data Integrity**: Award PDFs added, metadata fields verified, deduplication implemented
- **Security**: Cache hash verification, GitHub Actions pinned to SHA, credentials disabled
- **Quality**: Prompt uses from_messages, refusal rules, structured output enforced
- **DevOps**: PowerShell scripts, deployment controls, immutable candidate tags
- **Observability**: Provenance logging, prompt hash tracking, eval results with timestamps

## Blocked Items
- **DEF-029**: 9 fixable vulnerabilities in transitive dependencies (requires dependency updates with conflict resolution)
