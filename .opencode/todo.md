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
- [ ] S1.1.1: Run download script for 100 FWC decisions | size:L
- [ ] S1.1.2: Validate downloaded decisions (metadata, text quality) | size:M
- [ ] S1.1.3: Manually check 5 decisions for unfair dismissal relevance | size:S

### T1.2: Ingestion Pipeline | agent:Worker
- [ ] S1.2.1: Rewrite src/ingest.py for FWC decisions (paragraph-aware chunking) | size:M
- [ ] S1.2.2: Add metadata extraction (case name, citation, member, date, jurisdiction) | size:M
- [ ] S1.2.3: Test ingestion on 10 decisions | size:S

### T1.3: RAG Pipeline | agent:Worker
- [ ] S1.3.1: Rewrite src/rag.py with verifier + resolver + abstention | size:L
- [ ] S1.3.2: Rewrite src/router.py for query classification | size:M
- [ ] S1.3.3: Rewrite src/cag.py for Fair Work Act cache | size:S
- [ ] S1.3.4: Rewrite src/filtered_retriever.py for decision filtering | size:M

### T1.4: UI | agent:Worker
- [ ] S1.4.1: Update src/app.py for unfair dismissal (rebrand + passsages alongside claims) | size:S

### T1.5: Integration Test | agent:Reviewer
- [ ] S1.5.1: Run 10-question smoke test | size:S
- [ ] S1.5.2: Verify citation faithfulness (verifier working) | size:S
- [ ] S1.5.3: Test abstention on unsupported questions | size:S
