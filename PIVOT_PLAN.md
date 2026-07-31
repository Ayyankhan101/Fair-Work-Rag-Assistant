# PIVOT PLAN: Awards RAG → Unfair Dismissal RAG

**Date:** 31 July 2026
**Decision:** Follow playbook exactly — D5 = unfair dismissal (s 385–394 Fair Work Act 2009) only
**Rationale:** Playbook says Award interpretation is a different and harder problem. Do not mix in v1.

---

## 1. REUSABLE COMPONENTS (Keep As-Is)

| File | Lines | Why Reusable |
|------|-------|--------------|
| `src/fastembeddings.py` | 17 | FastEmbed ONNX wrapper — no changes needed |
| `src/vectorstore.py` | 118 | TurboVec build/load/search — adapt path only |
| `src/reranker.py` | 108 | Cohere reranker + keyword fallback — no changes |
| `src/bm25_retriever.py` | 58 | BM25 retriever — no changes |
| `src/hybrid_retriever.py` | 59 | RRF fusion — no changes |
| `src/app.py` | 99 | Gradio UI — rebrand only |
| `scripts/eval_hard.py` | ~200 | Eval harness — rewrite questions |

**Total reusable:** ~560 lines (46% of current codebase)

---

## 2. COMPONENTS TO REWRITE

### 2.1 `src/config.py` → `src/config.py`
**Current:** 119 award patterns + topic keywords + NES keywords
**New:** FWC decision metadata, Fair Work Act provision keywords, query classification categories

```python
# NEW STRUCTURE
FAIR_WORK_ACT_PROVISIONS = {
    "s385": {"title": "What is an Unfair Dismissal", "section": "Part 3-2 Division 4"},
    "s386": {"title": "Meaning of Dismissed", "section": "Part 3-2 Division 4"},
    "s387": {"title": "Criteria for Considering Unfairness", "section": "Part 3-2 Division 4"},
    "s388": {"title": "Summary Dismissal", "section": "Part 3-2 Division 4"},
    "s389": {"title": "Exceptions to Minimum Employment Period", "section": "Part 3-2 Division 4"},
    "s390": {"title": "Remedies for Unfair Dismissal", "section": "Part 3-2 Division 4"},
    "s391": {"title": "Compensation instead of Reinstatement", "section": "Part 3-2 Division 4"},
    "s392": {"title": "Remedy — How Compensation is Calculated", "section": "Part 3-2 Division 4"},
    "s393": {"title": "Notice of Termination", "section": "Part 3-2 Division 4"},
    "s394": {"title": "Application for Remedy", "section": "Part 3-2 Division 4"},
}

QUERY_CATEGORIES = {
    "jurisdictional": ["minimum employment period", "high income threshold", "small business", 
                       "21 days", "lodgment", "employee vs contractor", "casual"],
    "statutory_criteria": ["harsh", "unjust", "unreasonable", "s387", "valid reason", 
                           "notification", "response opportunity"],
    "analogous_facts": ["cases where", "similar to", "example of", "decided that",
                        "found unfair", "found not unfair"],
    "procedural": ["extension of time", "jurisdictional objection", "conciliation",
                   "arbitration", "Full Bench", "lodge", "application"],
}
```

### 2.2 `src/ingest.py` → `src/ingest.py`
**Current:** PDF → sections → chunks → Documents (512 lines)
**New:** FWC decisions + Fair Work Act → structure-aware chunks → Documents

Key changes:
- Download FWC decisions from FWC website (not PDFs)
- Parse decision structure: case name, citation, member, date, paragraphs
- Chunk on paragraph boundaries (not arbitrary windows)
- Metadata: case_name, medium_neutral_citation, member, date, jurisdiction, claim_type, outcome
- Point-in-time: `in_force_from` / `in_force_to` for legislation
- Contextual retrieval prefix: `[Case Name - Paragraph X]`

### 2.3 `src/rag.py` → `src/rag.py`
**Current:** Awards RAG with 5-component response (371 lines)
**New:** Citation-faithful RAG with post-hoc verifier

Pipeline per playbook Part 5.1:
1. Query understanding (classify: jurisdictional / principle / analogous-facts / procedural)
2. Hybrid retrieval (top ~50) → Cross-encoder rerank (top ~8) → Currency & treatment filter
3. Constrained generation: answer ONLY from provided passages, cite paragraph-level
4. **POST-HOC VERIFIER** (separate call): does each cited passage actually support the claim?
5. **Citation resolver**: every citation must resolve to a real corpus doc + live URL
6. **Abstention gate**: insufficient support → say so, show what was found
7. Render with inline quoted passages + links + corpus version + audit log

### 2.4 `src/router.py` → `src/router.py`
**Current:** NES vs Award routing (100 lines)
**New:** Query classification (jurisdictional / principle / analogous-facts / procedural)

### 2.5 `src/cag.py` → `src/cag.py`
**Current:** NES cache (164 lines)
**New:** Fair Work Act s 385–394 cache (always loaded, small, stable)

### 2.6 `src/filtered_retriever.py` → `src/filtered_retriever.py`
**Current:** Award-specific filtering (273 lines)
**New:** Decision filtering by jurisdiction, claim type, member, date range, outcome

---

## 3. NEW COMPONENTS (Must Build)

### 3.1 `src/verifier.py` — Post-Hoc Citation Verifier
**Playbook requirement:** "A second model call, with no access to the original question's framing, asked only: 'Does passage X support claim Y? Answer supported / partially / unsupported, and quote the supporting text.' Unsupported claims are stripped or flagged, not shipped."

```python
class CitationVerifier:
    """Verify each cited passage actually supports the generated claim."""
    
    def verify(self, claim: str, passage: str, citation: str) -> VerificationResult:
        """Returns: supported / partially / unsupported + supporting text."""
        # Separate LLM call — no access to original question
        prompt = f"""Does the following passage support the claim?

CLAIM: {claim}
PASSAGE: {passage}
CITATION: {citation}

Answer ONLY one of: supported, partially, unsupported
Then quote the supporting text if any."""

        result = self.llm.invoke(prompt)
        return self._parse_result(result)
```

### 3.2 `src/citation_resolver.py` — Citation Validation + URL Resolution
**Playbook requirement:** "Regex-extract every citation from output, resolve against the corpus index. Anything that does not resolve to a real document with a working URL is deleted from the response and logged as a hallucination event."

```python
class CitationResolver:
    """Validate every citation resolves to a real corpus document."""
    
    def resolve(self, citations: List[str], corpus_index: Dict) -> List[ResolvedCitation]:
        """Returns only citations that resolve to real documents."""
        resolved = []
        for citation in citations:
            doc = corpus_index.get(citation)
            if doc and self._url_works(doc.source_url):
                resolved.append(ResolvedCitation(citation, doc, verified=True))
            else:
                self._log_hallucination(citation)  # Monitor SLO
        return resolved
```

### 3.3 `src/abstention_gate.py` — Insufficient Support Detection
**Playbook requirement:** "'I could not find authority for this' is a correct and valuable answer. Measure and reward it."

```python
class AbstentionGate:
    """Determine if sufficient support exists to answer."""
    
    def should_abstain(self, verified_citations: List, confidence: float) -> bool:
        """Abstain if: no verified citations, low confidence, or insufficient support."""
        if not verified_citations:
            return True
        if confidence < 0.6:
            return True
        # Check if citations actually cover the question
        return self._coverage_check(verified_citations)
```

### 3.4 `src/audit_log.py` — Full Audit Trail
**Playbook requirement:** "Query, retrieved doc IDs and scores, prompt version, model version, corpus version, generated output, verifier verdicts, user verification actions, export events."

```python
@dataclass
class AuditEntry:
    query: str
    retrieved_doc_ids: List[str]
    retrieved_scores: List[float]
    prompt_version: str
    prompt_hash: str
    model_version: str
    corpus_version: str
    generated_output: str
    verifier_verdicts: List[VerificationResult]
    resolved_citations: List[ResolvedCitation]
    abstained: bool
    timestamp: str
    session_id: str
    user_verification_actions: List[dict]  # For export verification gate
```

### 3.5 `src/corpus_manager.py` — Point-in-Time + Versioning
**Playbook requirement:** "Law changes; the Fair Work Act has been amended repeatedly. Every provision needs in_force_from / in_force_to."

```python
class CorpusManager:
    """Manage corpus versioning and point-in-time correctness."""
    
    def get_current_version(self) -> str:
        """Return corpus version string."""
    
    def is_in_force(self, provision: str, date: datetime) -> bool:
        """Check if a provision was in force on a given date."""
    
    def get_treatment(self, decision_citation: str) -> TreatmentSignal:
        """Was this decision appealed, overturned, distinguished, followed?"""
```

### 3.6 `scripts/download_fwc_decisions.py` — FWC Decision Scraper
Download FWC unfair dismissal decisions from the FWC website.
- Source: https://www.fwc.gov.au/documents/decisionssigned/html/
- Filter: unfair dismissal matters (s 385-394)
- Parse: case name, citation, member, date, full text
- Store: `data/fwc_decisions/` as structured JSON

### 3.7 `scripts/download_fair_work_act.py` — Fair Work Act Provisions
Download Fair Work Act s 385-394 from Federal Register of Legislation.
- Source: https://www.legislation.gov.au/C2004A00612/latest/text
- Parse: sections, subsections, paragraphs
- Add point-in-time metadata
- Store: `data/legislation/` as structured JSON

### 3.8 `CORPUS_LICENCE_REGISTER.md` — Corpus Licence Register
**Playbook requirement:** "Produce a CORPUS_LICENCE_REGISTER.md with one row per source."

```markdown
| Source | Content | Licence | AI Use Permitted | Attribution | Date Checked | Evidence |
|--------|---------|---------|------------------|-------------|--------------|----------|
| FWC Decisions | Unfair dismissal decisions | Court/tribunal copyright — reproduction with acknowledgement | Y (check each) | "Source: Fair Work Commission" | 2026-07-31 | evidence/ |
| Federal Register | Fair Work Act 2009 | CC BY 4.0 | Y | "© Commonwealth of Australia" | 2026-07-31 | evidence/ |
| FWC Benchbooks | Unfair dismissal summaries | Check reuse terms | TBD | TBD | 2026-07-31 | evidence/ |
| AustLII | N/A | PROHIBITED — Do not ingest | N | N/A | 2026-07-31 | austlii_policy.pdf |
```

---

## 4. ARCHITECTURE (Per Playbook Part 5)

```
┌─────────────────────────────────────────────────────────────┐
│                    CORPUS                                    │
│  FWC Decisions (5yr) + Fair Work Act s385-394 + Benchbooks │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                INGEST PIPELINE                               │
│  Download → Normalise → Structure-aware chunk → Index       │
│  (BM25 + dense + metadata)                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              QUERY UNDERSTANDING                             │
│  Classify: jurisdictional / principle / analogous / procedural │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              HYBRID RETRIEVAL                                │
│  BM25 + Semantic (top ~50) → Rerank (top ~8)               │
│  → Currency & treatment filter                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              CONSTRAINED GENERATION                          │
│  Answer ONLY from provided passages, cite paragraph-level   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              POST-HOC VERIFIER (separate call)               │
│  "Does passage X support claim Y?"                          │
│  unsupported → strip/flag                                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              CITATION RESOLVER                               │
│  Every citation → validate against corpus → resolve URL      │
│  Hallucination events logged                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              ABSTENTION GATE                                 │
│  Insufficient support → "I could not find authority"        │
│  Show what was found                                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              RENDER                                          │
│  Inline quoted passages + links + corpus version + audit log│
│  GenAI disclosure block + verification checklist            │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. EVALUATION (Per Playbook Part 6)

### 5.1 Golden Set
- **Target:** 150–200 questions for v1
- **Written by:** Employment law practitioner
- **Each item:** question, expected authorities, expected propositions, common wrong answers, difficulty, category

### 5.2 Categories
1. Jurisdictional threshold questions (minimum employment period, high income threshold, small business definition, 21-day limit)
2. Statutory criteria application (s 387 factors)
3. Analogous-facts retrieval ("cases where summary dismissal for social media was unfair")
4. Procedural questions (extensions of time, jurisdictional objections)
5. **Superseded-law traps** (repealed provision questions)
6. **Overturned-decision traps** (authority was overturned on appeal)
7. **Adversarial/no-answer questions** (correct behavior is abstention)
8. Out-of-scope questions (state IR, workers comp, discrimination under other statutes)

### 5.3 Metrics + Launch Thresholds

| Metric | Definition | v1 Gate |
|--------|-----------|---------|
| Citation validity | cited authority exists and URL resolves | **100%** |
| Citation support | passage genuinely supports claim (expert-scored) | ≥ 95% |
| Currency correctness | no superseded provisions or overturned decisions | ≥ 98% |
| Retrieval recall@10 | expected authority present in retrieved set | ≥ 90% |
| Correct abstention | abstains when no support exists | ≥ 85% |
| Harmful over-claim | states conclusion on user's matter as advice | **0** |
| Answer usefulness | expert 1–5 rating | ≥ 4.0 mean |
| p95 latency | end to end | < 15s |

### 5.4 Eval Harness
- Run in CI on every prompt, retrieval, corpus or model change
- Store results with commit SHAs
- Each item run n≥3 (non-determinism)
- Report variance

---

## 6. DELIVERY PLAN (Per Playbook Part 9)

### Phase 0 — Foundations (Weeks 1–2)
- [ ] Answer D1–D6 (sponsor decisions)
- [ ] Engage employment law SME (1-2 days/week)
- [ ] Engage independent legal/privacy advisor
- [ ] Create CORPUS_LICENCE_REGISTER.md
- [ ] Download FWC exposure draft Guidance Note
- [ ] Write "do not" list, get team sign-off
- [ ] Set up repo, CI, IaC, environments
- **Exit gate:** Written scope decision, SME engaged, licence register complete

### Phase 1 — Vertical Slice Prototype (Weeks 3–6)
- [ ] Download 100 FWC unfair dismissal decisions
- [ ] Download Fair Work Act s 385-394
- [ ] Structure-aware chunking with paragraph numbers
- [ ] Hybrid retrieval (BM25 + semantic)
- [ ] Cross-encoder reranking
- [ ] Generate with citations (paragraph-level)
- [ ] Post-hoc verifier
- [ ] Citation resolver
- [ ] Basic UI showing passages alongside claims
- [ ] First 50 golden-set questions
- [ ] Eval harness in CI from week 1
- **Exit gate:** 100% citation validity, recall@10 ≥ 75%, SME rates ≥ 3.5/5

### Phase 2 — Depth and Hardening (Weeks 7–12)
- [ ] Full corpus (5yr decisions)
- [ ] Point-in-time legislation
- [ ] Treatment/appeal flagging
- [ ] Golden set to 150+
- [ ] Abstention tuning
- [ ] Red team round one
- [ ] Tenancy, authn, audit logging, retention policy
- [ ] Verification UX and export gating with FWC disclosure block
- [ ] Model card and limitations documentation
- [ ] Security review readiness pack
- **Exit gate:** All Part 6.2 thresholds met, PIA complete, ToU drafted

### Phase 3 — Design Partner Pilot (Weeks 13–20)
- [ ] 3–5 friendly practitioners or single small firm
- [ ] Free/nominal in exchange for structured feedback
- [ ] Instrument everything
- [ ] Weekly feedback sessions
- **Exit gate:** Partners would pay, no P0 accuracy incidents, verification behavior observed

### Phase 4 — Production Readiness (Weeks 21–26)
- [ ] Observability and alerting on hallucination events, abstention rate, latency, cost
- [ ] Incident runbooks
- [ ] Breach response plan
- [ ] On-call
- [ ] Load and cost modelling
- [ ] Model upgrade procedure with mandatory eval re-run
- [ ] Backup and restore tested
- [ ] Procurement documentation
- **Exit gate:** Production readiness review passed

---

## 7. CODE MIGRATION MAP

| Current File | Lines | Action | New File | Lines |
|-------------|-------|--------|----------|-------|
| `src/fastembeddings.py` | 17 | KEEP | `src/fastembeddings.py` | 17 |
| `src/vectorstore.py` | 118 | ADAPT | `src/vectorstore.py` | ~120 |
| `src/reranker.py` | 108 | KEEP | `src/reranker.py` | 108 |
| `src/bm25_retriever.py` | 58 | KEEP | `src/bm25_retriever.py` | 58 |
| `src/hybrid_retriever.py` | 59 | KEEP | `src/hybrid_retriever.py` | 59 |
| `src/app.py` | 99 | REBRAND | `src/app.py` | ~100 |
| `src/config.py` | 361 | REWRITE | `src/config.py` | ~150 |
| `src/ingest.py` | 512 | REWRITE | `src/ingest.py` | ~400 |
| `src/rag.py` | 371 | REWRITE | `src/rag.py` | ~500 |
| `src/router.py` | 100 | REWRITE | `src/router.py` | ~80 |
| `src/cag.py` | 164 | REWRITE | `src/cag.py` | ~80 |
| `src/filtered_retriever.py` | 273 | REWRITE | `src/filtered_retriever.py` | ~200 |
| NEW | - | CREATE | `src/verifier.py` | ~150 |
| NEW | - | CREATE | `src/citation_resolver.py` | ~120 |
| NEW | - | CREATE | `src/abstention_gate.py` | ~80 |
| NEW | - | CREATE | `src/audit_log.py` | ~100 |
| NEW | - | CREATE | `src/corpus_manager.py` | ~150 |
| NEW | - | CREATE | `scripts/download_fwc_decisions.py` | ~300 |
| NEW | - | CREATE | `scripts/download_fair_work_act.py` | ~150 |
| NEW | - | CREATE | `CORPUS_LICENCE_REGISTER.md` | ~50 |
| NEW | - | CREATE | `DO_NOT_LIST.md` | ~30 |

**Current total:** ~2,456 lines
**New total:** ~2,865 lines (reuse ~560, rewrite ~1,200, new ~1,105)

---

## 8. RISK REGISTER (Per Playbook Part 2)

| ID | Risk | Rating | Mitigation |
|----|------|--------|------------|
| R1 | Unqualified legal practice | C | Information only, no advice, disclaimers |
| R2 | Hallucinated authorities | C | Extractive grounding, post-gen verification, abstention |
| R3 | Misleading conduct | H | Evidence-backed claims, no "99% accurate" |
| R4 | Privacy Act | H | Collect minimum, APP 5, no offshore facts |
| R5 | Privilege/confidentiality | H | No training on tenant data, zero retention |
| R6 | Corpus licensing | H | LICENCE_REGISTER, no AustLII, no commercial publishers |
| R7 | FWC GenAI Guidance | H | Disclosure block, verification gate, hyperlink enforcement |
| R8 | Commonwealth AI policy | M | AI impact assessment, transparency statement |
| R9 | Bias/fairness | M | No probability of success, slice evals |
| R10 | Non-determinism | M | Run n≥3, report variance |
| R11 | Insurance/contracts | M | PI + cyber cover, ToU drafted |
| R12 | Model/vendor dependency | M | Pin versions, abstraction layer |

---

## 9. HARD "DO NOT" LIST (Per Playbook Part 3)

1. ~~Do not ingest AustLII content~~ ✅ (we don't)
2. **Do not let the model produce a citation from parametric memory.** Citations come only from retrieved documents, and are validated after generation.
3. ~~Do not output percentage or odds of winning~~ ✅ (we don't)
4. ~~Do not brand as lawyer/advice~~ ✅ (we don't)
5. **Do not send identifiable client facts to any endpoint without signed no-training, no-retention agreement.**
6. ~~Do not fine-tune on customer data~~ ✅ (we don't)
7. **Do not let a document be exported for lodgment without human verification of every authority.**
8. ~~Do not measure with BLEU/ROUGE~~ ✅ (we use domain eval)
9. ~~Do not reproduce commercial publishers' headnotes~~ ✅ (we don't)
10. ~~Do not autonomously lodge with FWC~~ ✅ (we don't)
11. ~~Do not store unnecessary sensitive info~~ ✅ (we don't)
12. ~~Do not ship confidence score as self-assessment~~ ✅ (we don't)

**Violations to fix:**
- #2: Currently LLM generates citations from memory → must validate against corpus
- #5: Groq is US endpoint → need Australian region or signed agreement
- #7: No export verification gate → must build

---

## 10. IMMEDIATE NEXT STEPS (This Week)

1. **Get sponsor decisions D1-D6 in writing** (Day 1)
2. **Engage employment law SME** — contract, part-time (Day 1-2)
3. **Engage independent legal/privacy advisor** (Day 1-2)
4. **Create CORPUS_LICENCE_REGISTER.md** (Day 2)
5. **Download FWC Guidance Note** — read as team (Day 2)
6. **Write "do not" list** — get team sign-off (Day 3)
7. **Spike: Download 100 FWC decisions** — structure-aware chunk — stand up hybrid retrieval (Day 3-7)
8. **Draft first 20 golden-set questions** — have SME correct (Day 4-7)
9. **Book fortnightly eval review** for next 6 months (Day 1)
