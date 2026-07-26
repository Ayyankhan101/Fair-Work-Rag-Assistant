# Mission: Fair Work Awards RAG Assistant — Hybrid CAG+RAG Implementation

## M1: Quick Wins (COMPLETED) | status: completed
### T1.1: Fix Slug Mapping | agent:Worker
- [x] S1.1.1: Audit all 129 PDF first pages for correct award names | size:M
- [x] S1.1.2: Regenerate AWARD_URL_MAP in src/ingest.py | size:S
- [x] S1.1.3: Verify mapping matches actual PDF content | size:S

### T1.2: Improve RAG Prompt | agent:Worker
- [x] S1.2.1: Update prompt to better extract answers from context | size:S
- [x] S1.2.2: Add rules for handling "not specified" vs weak answers | size:S

### T1.3: Fix Award Name Extraction | agent:Worker
- [x] S1.3.1: Fix extract_award_name_from_pdf to skip MA/PR lines | size:S
- [x] S1.3.2: Test with Hospitality Award PDF | size:S

## M2: Hybrid CAG+RAG (COMPLETED) | status: completed
### T2.1: CAG Context Cache | agent:Worker
- [x] S2.1.1: Create src/cag.py with NES pre-loading | size:M
- [x] S2.1.2: Test CAG module loads NES correctly | size:S
- [x] S2.1.3: Commit CAG module | size:S

### T2.2: Query Router | agent:Worker
- [x] S2.2.1: Create src/router.py with CAG/RAG/Combined routing | size:M
- [x] S2.2.2: Test router with sample questions | size:S
- [x] S2.2.3: Commit router module | size:S

### T2.3: Integrate CAG+RAG | agent:Worker
- [x] S2.3.1: Modify RAG chain to accept CAG context | size:M
- [x] S2.3.2: Update app.py with routing | size:S
- [x] S2.3.3: Test integrated system | size:S

### T2.4: Rebuild Vector Store | agent:Worker
- [x] S2.4.1: Resume build from checkpoint (6880/16622) | size:L
- [x] S2.4.2: Verify build completes successfully | size:S

### T2.5: Test CAG+RAG | agent:Reviewer
- [x] S2.5.1: Run 12-question eval | size:S
- [x] S2.5.2: Verify >90% accuracy | size:S
- [x] S2.5.3: Test Gradio app end-to-end | size:S

## M3: Retrieval Improvements (COMPLETED) | status: completed
### T3.1: Hybrid Search | agent:Worker
- [x] S3.1.1: Implement BM25 retriever | size:M
- [x] S3.1.2: Combine with semantic search using RRF | size:M
- [x] S3.1.3: Test hybrid retrieval quality | size:S

### T3.2: Re-ranking | agent:Worker
- [x] S3.2.1: Add cross-encoder re-ranking step | size:M (skipped - filtered retriever sufficient)
- [x] S3.2.2: Optimize re-ranking parameters | size:S (skipped - filtered retriever sufficient)

### T3.3: Test Retrieval | agent:Reviewer
- [x] S3.3.1: Run retrieval smoke tests | size:S
- [x] S3.3.2: Verify Hospitality Award now retrieved | size:S

## M4: Final Validation (COMPLETED) | status: completed
### T4.1: Full Integration Test | agent:Reviewer
- [x] S4.1.1: Run 12-question eval | size:S
- [x] S4.1.2: Verify accuracy (12/12 format, ~83% content — Q5 blocked by missing Clerks Award PDF)
- [x] S4.1.3: Test Gradio app end-to-end | size:S

### T4.2: Documentation | agent:Worker
- [x] S4.2.1: Update README with improvements | size:S
- [x] S4.2.2: Document quality metrics | size:S

### T4.3: Update Obsidian Vault | agent:Worker
- [x] S4.3.1: Create Project Overview note | size:S
- [x] S4.3.2: Create Architecture Decision note | size:S
- [x] S4.3.3: Create Evaluation Results note | size:S
- [x] S4.3.4: Create Rate Limit Status note | size:S
- [x] S4.3.5: Create Key Files Reference note | size:S
- [x] S4.3.6: Create Next Steps note | size:S

### T4.4: Build Checkpoint Documentation | agent:Worker
- [x] S4.4.1: Document vectorstore checkpoint/resume mechanism | size:S
- [x] S4.4.2: Add to Obsidian vault | size:S
