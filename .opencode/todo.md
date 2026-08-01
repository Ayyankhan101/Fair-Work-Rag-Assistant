# Mission: Fair Work Unfair Dismissal RAG Assistant

**Pivot:** Awards → Unfair Dismissal (s385-394 Fair Work Act 2009) only
**Playbook:** fwc-legal-rag-tech-lead-playbook.md

---

## Phase 0 — Foundations (Weeks 1-2) | status: completed

### T0.1: Corpus Licence & Governance
- [x] S0.1.1: Create CORPUS_LICENCE_REGISTER.md (11 sources) | size:S
- [x] S0.1.2: Create DO_NOT_LIST.md (12 hard 'do not' items) | size:S
- [x] S0.1.3: Create PIVOT_PLAN.md (comprehensive pivot plan) | size:S

### T0.2: Fair Work Act Provisions
- [x] S0.2.1: Download Fair Work Act s385-394 extract | size:S
- [x] S0.2.2: Create src/config.py for FWC provisions | size:S

### T0.3: New Components
- [x] S0.3.1: Create src/verifier.py (post-hoc citation verifier) | size:S
- [x] S0.3.2: Create src/citation_resolver.py (regex + corpus validation) | size:S
- [x] S0.3.3: Create src/abstention_gate.py (4-rule abstention) | size:S
- [x] S0.3.4: Create src/audit_log.py (full audit trail) | size:S
- [x] S0.3.5: Create src/corpus_manager.py (point-in-time, versioning) | size:S

### T0.4: Scraper
- [x] S0.4.1: Create scripts/download_fwc_decisions.py | size:S

---

## Phase 1 — Vertical Slice (Weeks 3-6) | status: in_progress

### T1.1: Download FWC Decisions | agent:Worker
- [x] S1.1.1: Run download script for 100 FWC decisions | size:L (POSTPONED: user decision — FWC website blocks automation)
- [x] S1.1.2: Validate downloaded decisions (metadata, text quality) | size:M (POSTPONED: awaiting S1.1.1)
- [x] S1.1.3: Manually check 5 decisions for unfair dismissal relevance | size:S (POSTPONED: awaiting S1.1.1)

### T1.2: Ingestion Pipeline | agent:Worker
- [x] S1.2.1: Rewrite src/ingest.py for FWC decisions (paragraph-aware chunking) | size:M
- [x] S1.2.2: Add metadata extraction (case name, citation, member, date, jurisdiction) | size:M
- [x] S1.2.3: Test ingestion on 10 decisions | size:S (POSTPONED: awaiting S1.1.1 — user decision)

### T1.3: RAG Pipeline | agent:Worker
- [x] S1.3.1: Rewrite src/rag.py with verifier + resolver + abstention | size:L
- [x] S1.3.2: Rewrite src/router.py for query classification | size:M
- [x] S1.3.3: Rewrite src/cag.py for Fair Work Act cache | size:S
- [x] S1.3.4: Rewrite src/filtered_retriever.py for decision filtering | size:M

### T1.4: UI | agent:Worker
- [x] S1.4.1: Update src/app.py for unfair dismissal (rebrand) | size:S

### T1.5: Integration Test | agent:Reviewer
- [x] S1.5.1: Run 8-question smoke test | size:S (100% section accuracy, 87.5% answer accuracy)
- [x] S1.5.2: Verify citation faithfulness with decisions | size:S (POSTPONED: awaiting S1.1.1 — user decision)
- [x] S1.5.3: Test abstention on unsupported questions | size:S (out-of-scope questions correctly abstain)

### T1.6: Documentation & Cleanup | agent:Worker
- [x] S1.6.1: Update all .opencode/ docs with current status | size:S
- [x] S1.6.2: Fix ingest_all backward compatibility | size:S
- [x] S1.6.3: Commit and push all changes | size:S
- [x] S1.6.4: Restart Gradio app with correct venv | size:S
- [x] S1.6.5: Verify app running on localhost:7860 | size:S
- [x] S1.6.6: Update all documentation files | size:S
- [x] S1.6.7: Final verification and commit | size:S
- [x] S1.6.8: Fix localStorage error documentation | size:S
- [x] S1.6.9: Verify all Python files compile | size:S
- [x] S1.6.10: Push all changes to develop | size:S
- [x] S1.6.11: Verify app responds on port 7860 | size:S

---

## Phase 1 Summary

### Completed
- Config rewritten for FWC provisions (10 sections)
- Router rewritten with 4 query types + CAG candidate detection
- RAG pipeline rewritten with full verification pipeline
- CAG rewritten for Fair Work Act s385-394
- Filtered retriever rewritten as UnfairDismissalRetriever
- App rewritten for unfair dismissal Gradio UI
- Ingest rewritten for FWC decisions (structure-aware chunking)
- Eval framework created with 8 golden-set questions
- Pipeline tested: 100% section accuracy, 87.5% answer accuracy

### Blocked
- FWC decisions download (bot protection) — user must manually download
- No vectorstore until decisions are downloaded
- No SME (employment law practitioner)
- No sponsor decisions D1-D6

### Next Steps
1. User downloads 100 FWC decisions from FWC search portal
2. Build vectorstore from decisions
3. Test full pipeline with decisions + legislation
4. Set up eval with more questions
5. Get sponsor decisions D1-D6
6. Engage employment law SME
