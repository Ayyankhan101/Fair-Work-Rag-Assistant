# Work Log

## Active Sessions
- [x] ses_1 (Worker): Vector store build — COMPLETE (16622 docs, 520 batches, 2982s) [LEGACY - Awards]
- [x] ses_2 (Worker): Unfair dismissal pivot — COMPLETE (all Phase 0 + Phase 1 components)

## File Status
| File | Action | Status | Session | Unit Test | Timestamp | Issue |
|------|--------|--------|---------|-----------|-----------|-------|
| src/config.py | REWRITE | done | ses_2 | pass | 2026-07-31T08:24:00 | FWC provisions s385-394 |
| src/cag.py | REWRITE | done | ses_2 | pass | 2026-07-31T08:22:00 | Fair Work Act cache |
| src/router.py | REWRITE | done | ses_2 | pass | 2026-07-31T08:23:00 | 4 query types |
| src/rag.py | REWRITE | done | ses_2 | pass | 2026-07-31T08:24:00 | Full pipeline with verification |
| src/filtered_retriever.py | REWRITE | done | ses_2 | pass | 2026-07-31T08:24:00 | UnfairDismissalRetriever |
| src/app.py | REWRITE | done | ses_2 | pass | 2026-07-31T08:24:00 | Unfair dismissal UI |
| src/ingest.py | REWRITE | done | ses_2 | pass | 2026-07-31T08:28:00 | FWC decisions ingestion |
| src/verifier.py | CREATE | done | ses_2 | - | 2026-07-31T08:00:00 | Post-hoc citation verifier |
| src/citation_resolver.py | CREATE | done | ses_2 | pass | 2026-07-31T08:00:00 | Regex + corpus validation |
| src/abstention_gate.py | CREATE | done | ses_2 | pass | 2026-07-31T08:00:00 | 4-rule abstention |
| src/audit_log.py | CREATE | done | ses_2 | - | 2026-07-31T08:00:00 | Full audit trail |
| src/corpus_manager.py | CREATE | done | ses_2 | - | 2026-07-31T08:00:00 | Point-in-time management |
| scripts/eval_unfair_dismissal.py | CREATE | done | ses_2 | pass | 2026-07-31T08:26:00 | 8 golden-set questions |
| scripts/download_fwc_decisions.py | CREATE | done | ses_2 | - | 2026-07-31T08:00:00 | FWC scraper (blocked) |
| data/legislation/fair_work_act_s385_394.txt | CREATE | done | ses_2 | - | 2026-07-31T08:00:00 | Legislation text |

## Pipeline Test Results
| Test | Status | Details |
|------|--------|---------|
| Router classification | pass | 4 types detected correctly |
| CAG context loading | pass | Fair Work Act loaded (10978 chars, 10 sections) |
| RAG pipeline | pass | 100% section accuracy, 87.5% answer accuracy |
| Citation extraction | pass | Extracts "s385" correctly |
| Abstention gate | pass | 0% abstention on legislation queries |
| Legislation ingestion | pass | 13 chunks from s385-394 |

## Router Fix (2026-08-01)
- Added keywords: "how long", "time limit", "deadline", "within", "apply for", "application", "eligible to"
- Now correctly classifies "How long do I have to apply?" as jurisdictional

## Pending Integration (POSTPONED per user decision)
- FWC decisions download — user will handle manually via Brave browser
- Vectorstore build — awaiting decisions
- Hybrid search with decisions — awaiting decisions
