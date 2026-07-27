# Quality assurance team README

Owner: quality assurance team.

Scope: assess the `fair-work-rag-assistant` repository against the supplied requirements, current official Fair Work scope, and the quality standards recorded here.

The root `README.md` is the original development README inherited at Git fork point `3e91e9e16c7417269242d7ef2f6f04bb6a49efff`. QA did not rewrite it. This file is the second README requested by the project owner and is the entry point for QA evidence.

Product code is protected. On 27 July 2026, QA preserved its earlier working changes as patches, moved QA-created tests and tools into this folder, and restored every path outside this folder to the exact fork-point tree. QA records defects and recommended corrections but does not deliver product fixes.

The `System Under Test (SUT)/Discard` directory is historical reference material. It is not the active product and cannot provide pass evidence.

## Read this first

| File | Purpose |
|---|---|
| `developer-handoff-after-qa-2026-07-27.md` | current developer-facing findings, ownership boundary, and required response |
| `qa-branch-change-control-record-2026-07-27.md` | exact Git comparison, preserved patches, moves, and restoration proof |
| `quick-qa-iteration-after-cleanup-2026-07-27.md` | latest clean-baseline rerun and result |
| `test-and-metrics-register.md` | test inventory, metric definitions, thresholds, and execution state |
| `quick-glance-release-status.md` | one-page decision and highest risks |
| `quick-glance-architecture-and-risks.md` | current and target flow |
| `quick-glance-qa-execution.md` | phase order and evidence rule |
| `quick-glance-accuracy-roadmap.md` | prioritized accuracy and model work |
| `final-qa-report-2026-07-27.md` | consolidated final disposition |
| `step-1-report-2026-07-27.md` | current baseline verdict and exact evidence |
| `transparency-log.md` | worktree state, limitations, and pre-boundary changes |
| `phase-by-phase-execution-plan.md` | execution order, entry/exit gates, evidence, and cost bands |
| `standards-and-quality-model.md` | ISO, NIST, OWASP, WCAG, Fair Work, and release rules |
| `artifact-audit.md` | repository, PDF, DOCX, discard, script, and documentation findings |
| `evidence-record-templates.md` | run, test, defect, claim, result, cost, and phase records |

## Test specifications

| File | Defined cases |
|---|---:|
| `test-cases-01-foundation.md` | 65 |
| `test-cases-02-corpus-ingestion-store.md` | 80 |
| `test-cases-03-routing-retrieval-answer.md` | 105 |
| `test-cases-04-ui-security-performance-deployment.md` | 115 |
| `test-cases-05-prompt-assurance.md` | 120 |
| Total | 485 |

Parameterized Award, NES, prompt-injection, repetition, browser, platform, model, and load cases raise the minimum execution count above 1,000. A defined case is not a passed case.

## Control documents

| File | Purpose |
|---|---|
| `qa-plan.md` | original gate and phase outline |
| `baseline-2026-07-27.md` | first inspection before the current expanded baseline |
| `system-under-test.md` | components, data flow, state, and trust boundaries |
| `requirements-traceability.md` | requirement mapping and gaps |
| `test-strategy.md` | test order, tiers, thresholds, and stop rules |
| `defect-register.md` | severity-ranked findings |
| `security-review.md` | security findings and required closure |
| `prompt-assurance-report.md` | active and committed prompt defects |
| `proposed-system-and-user-prompt.md` | role-separated prompt and output-schema draft |
| `prompt-evaluation-rubric.md` | hard prompt gates and review fields |
| `unbiased-evaluation-system.md` | blind, held-out, claim-level evaluation controls |
| `accuracy-improvement-research.md` | model, retrieval, reranking, tuning, and cost research |
| `model-and-architecture-decision-record.md` | controlled candidate comparison and selection rule |
| `qa-method-research.md` | standards-based method selected for this project |
| `previous-documentation-critique.md` | strict review of earlier project and QA claims |
| `phase-3-source-corpus-report-2026-07-27.md` | 122-page live check and source-acceptance result |
| `phase-4-local-automation-report-2026-07-27.md` | executed tests, coverage, dependency, import, and startup evidence |
| `phase-5-security-supply-chain-report-2026-07-27.md` | security scans, workflow audit, licensing, branch drift, and development-parser evidence |
| `phase-6-rag-cag-request-and-load-report-2026-07-27.md` | 60-request matrices, semantic accuracy, claim support, startup, failure, and loopback load results |
| `api-provider-assurance-report-2026-07-27.md` | Groq, Gemini, OpenRouter, and OpenAI comparison and test protocol |
| `software-engineering-process-audit.md` | lifecycle, candidate, review, traceability, and release-process assessment |
| `opencode-practices-critique.md` | evidence-based critique of the supplied OpenCode records and automation |
| `supervisor-handoff-2026-07-27.md` | review-ready decision summary, evidence boundaries, and requested actions |
| `qa-runbook.md` | commands and evidence handling |
| `release-checklist.md` | release sign-off gates |
| `release-report-2026-07-27.md` | current release decision |
| `tests/` | QA-owned executable regression tests; these are not product tests |
| `tools/` | QA-owned audit and diagnostic harnesses |
| `evidence/` | machine-readable scope and audit output |

## Current status

Latest iteration: complete with a failed result.

Release: blocked. There is no accepted release candidate.

Every product path outside this folder matches the fork point. Relative to QA `HEAD`, root `README.md` is intentionally modified only to remove the QA banner and recover the inherited development README. QA files remain untracked until the owner decides how they will be reviewed and committed.

The restored baseline passed 2 of 16 QA unit-test methods. The runner reported 14 failure records and four errors because failed subtests are counted separately. The baseline also fails a clean declared-dependency import because `rank_bm25` is absent from `requirements.txt`.

The natural Windows 60-request matrix stops before request one because `src/cag.py` reads UTF-8 data with the platform default encoding. With `PYTHONUTF8=1` and an ephemeral `rank-bm25` install used only for diagnosis, 31 of 60 cases passed all applicable checks. Award detection passed 25 of 38, expected-Award context passed 22 of 36, and clarification passed 0 of 9.

Ruff 0.16.0 reports 90 product-source findings. Seventeen of 18 checked product files would be reformatted. All 29 product and QA Python sources parse as Python syntax, which is a weaker result than passing lint or tests.

The QA branch is four commits behind `develop`. Those commits change source conversion, Markdown ingestion, vector-store construction, and prompting. An isolated development fixture reproduced preamble loss, missing subclause identity, and failure to enforce the configured chunk maximum. Earlier QA execution does not qualify the current development candidate.

The process audit found an implementation-first, self-certified workflow rather than a controlled release lifecycle. OpenCode records mark execution complete while recording only 10 of 12 correct answers, use invalid above-97% arithmetic, and count skipped reranking work as complete. This is a critique of the supplied records, not proof that no external process occurred.

The earlier provider-free request phase executed 60 varied RAG+CAG cases against the now-reverted dirty QA state and 60 against a forced-UTF-8 development snapshot. Those results remain useful diagnostics but are not candidate evidence. Raw semantic retrieval found the expected Award in 16 of 36 top-1 results. Zero of nine requests that required clarification were gated for it.

A corrected local Gradio run completed 288 of 288 load requests without a request error, but at 32 workers median latency was 5.936 seconds, p95 was 7.902 seconds, and peak process RSS was 1.276 GB even though the external model was replaced. This is local diagnostic evidence, not production capacity.

The current Groq API path has no explicit timeout, structured claim output, usage record, or qualified fallback. No Groq, Gemini, OpenRouter, or OpenAI inference run occurred because no provider key or approved spend was available. The provider decision remains open.

All 122 official Award pages were reachable on 27 July 2026, but that is not source acceptance. The next valid action is candidate control: engineering must select an exact commit, respond to the handoff, and produce a checksummed 122-Award plus NES corpus before accuracy qualification resumes.
