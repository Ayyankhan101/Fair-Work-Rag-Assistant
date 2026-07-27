# Phase-by-phase QA execution plan

## Operating rule

QA observes, tests, records, and recommends. QA does not change product code under the current instruction.

When a test exposes a defect:

1. Preserve the raw evidence.
2. Record the candidate identity and environment.
3. Reproduce once with the same inputs.
4. Reduce to the smallest reliable case.
5. Assign severity and affected requirements.
6. Write expected and actual behavior.
7. Recommend a correction and verification test.
8. Return it to engineering.
9. Test the new candidate from the beginning of its affected gate.

QA does not mark a defect fixed from source inspection alone when dynamic evidence is required.

## Cost bands

| Band | Meaning | Examples |
|---|---|---|
| C0 | no provider or cloud cost | file checks, parsing, lint, unit tests |
| C1 | low local compute | corpus extraction, fixture ingestion, small retrieval suite |
| C2 | moderate local or provider cost | full retrieval set, controlled answer sample |
| C3 | high provider or infrastructure cost | repeated answer evaluation, browser matrix, concurrency |
| C4 | exceptional cost | soak, disaster recovery, large model comparison |

Run order follows cost. A failed lower-cost gate stops dependent higher-cost work.

## Phase 0: control the candidate

Entry:

- repository is available;
- intended branch and release target are stated.

Steps:

1. Record HEAD, branch, remotes, status, operating system, and tool versions.
2. List modified, untracked, ignored, and LFS files.
3. Identify which files are product, data, generated evidence, personal workspace, vendor, historical, or discard.
4. Obtain an immutable candidate commit.
5. Create the run ID and evidence directory.
6. Confirm no process will mutate the candidate during the run.

Exit:

- immutable candidate identified;
- scope approved;
- no undeclared input.

Evidence:

- candidate manifest;
- repository inventory;
- transparency log.

Cost: C0.

Current result: fail. The working tree is dirty and contains pre-boundary QA-session code changes.

## Phase 1: requirements and standards

Entry:

- controlled source documents are available.

Steps:

1. Extract every requirement and success statement.
2. Assign stable IDs.
3. Compare the PDF, architecture, README, vault notes, and official Fair Work pages.
4. Convert vague wording into measurable acceptance criteria.
5. Add missing security, privacy, accessibility, cost, recovery, and data-freshness requirements.
6. Record conflicts and obtain owner decisions.
7. Map requirements to the quality model and test cases.

Exit:

- 100% of requirements identified;
- every conflict resolved or blocking;
- every requirement has at least one test.

Evidence:

- requirements baseline;
- standards mapping;
- traceability matrix;
- approved conflict decisions.

Cost: C0.

Current result: fail. The supplied NES list is stale and non-functional criteria are not measurable.

## Phase 2: repository and dependency baseline

Entry:

- immutable candidate exists.

Steps:

1. Parse and syntax-check every active artifact.
2. Run compile, lint, format, import, and offline unit commands.
3. Test shell scripts with their target shell and operating system.
4. Resolve dependencies in a clean Python environment.
5. Produce a lock and SBOM for review.
6. Audit vulnerabilities, licenses, package sources, and hashes.
7. Test documented setup from a clean checkout.

Exit:

- all C0 build gates pass;
- supported environment matrix defined;
- dependency graph locked and reviewed.

Evidence:

- raw command logs;
- dependency lock and SBOM;
- vulnerability and license reports.

Cost: C0 to C1.

Current result: fail. The working tree gates pass, but HEAD has no tests, dependencies are unpinned, and three shell scripts fail syntax checking.

## Phase 3: source corpus acceptance

Entry:

- approved official scope exists;
- raw sources are supplied.

Steps:

1. Reacquire the official 122-item Award list.
2. Match one source to each official ID.
3. Check title, ID, URL, effective date, bytes, pages, checksum, readability, and authority.
4. Reject missing, extra, duplicate, corrupt, stale, generic-title, and unversioned sources.
5. Compare current NES entitlements with the local source.
6. Inspect tables, schedules, footnotes, first clause, and final clause.
7. Obtain human legal-source review.

Exit:

- 122 of 122 Awards accepted;
- current NES accepted;
- zero unknown or duplicate source;
- signed corpus manifest.

Evidence:

- source files;
- manifest;
- official-list snapshot;
- source review record.

Cost: C1.

Current result: failed. A 27 July 2026 live check reached all 122 official Award pages, but raw responses and per-source hashes were not retained. Raw Award sources remain absent from the repository; persisted content misses two mandatory IDs and mislabels MA000002.

## Phase 4: ingestion and data quality

Entry:

- Phase 3 passed.

Steps:

1. Build reviewed fixtures for headings, tables, schedules, page breaks, Unicode, malformed files, and navigation.
2. Run ingestion twice and compare manifests.
3. Verify clause-aware chunks and every metadata field.
4. Measure empty, small, oversized, duplicate, and boundary-damaged chunks.
5. Verify that cleaning removes chrome but preserves substantive text.
6. Interrupt and resume a build.
7. measure time, memory, and partial-output behavior.

Exit:

- 100% sources produce valid chunks;
- required metadata 100%;
- empty chunks 0;
- unexplained duplicates 0;
- deterministic manifest.

Evidence:

- fixture set;
- chunk manifest;
- data-quality report;
- resource report.

Cost: C1.

## Phase 5: cache and vector-store integrity

Entry:

- Phase 4 passed.

Steps:

1. Build CAG and RAG artifacts into a new versioned target.
2. Compare source, chunk, docstore, and vector counts.
3. verify embedding name, revision, dimension, and distance metric.
4. Sign or hash every artifact.
5. Test tampering, partial build, duplicate resume, atomic publish, load, and rollback.
6. Enforce one corpus version across CAG and RAG.
7. Record artifact size and load memory.

Exit:

- counts agree;
- artifacts reject tampering;
- CAG/RAG version handshake passes;
- rollback proven.

Evidence:

- artifact manifest;
- integrity report;
- load and rollback logs.

Cost: C1 to C2.

## Phase 6: routing

Entry:

- Phase 5 passed;
- reviewed route labels exist.

Steps:

1. Run NES-only, Award-only, combined, ambiguous, unknown, and out-of-scope sets.
2. Add misspellings, synonyms, inflections, abbreviations, negation, long narratives, and Unicode.
3. Test known substring and generic-industry collisions.
4. Test question and source prompt injection against routing.
5. Compare displayed route with actual context path.
6. Repeat deterministic cases.

Exit:

- 100% labelled route accuracy;
- zero display/context mismatch;
- ambiguous cases do not force unsupported Award choice.

Evidence:

- labelled set;
- route result file;
- confusion matrix;
- defect list.

Cost: C1.

## Phase 7: retrieval

Entry:

- Phase 6 passed;
- reviewed clause gold set exists.

Steps:

1. Run presence, coverage, and clause cases across all 122 Awards.
2. Run current rate, overtime, penalties, allowances, breaks, classifications, exclusions, and schedules.
3. Run every current NES grouping.
4. Measure top-k recall, rank, contamination, duplicates, and latency.
5. Compare dense, lexical, hybrid, filters, top-k, chunking, and embedding candidates.
6. Select the cheapest configuration that meets all recall gates.

Exit:

- Award recall at 3 at least 98%;
- Award recall at 5 100%;
- clause recall at 5 at least 95%;
- retrieval p95 under 1 second;
- zero unexplained cross-Award contamination in high-impact cases.

Evidence:

- raw ranked results;
- metric report;
- configuration comparison;
- selected configuration decision.

Cost: C1 to C2.

## Phase 8: answer grounding and legal safety

Entry:

- Phase 7 passed;
- gold claims have legal-source review;
- provider privacy and spending approval exists.

Steps:

1. Run a small calibration batch.
2. Inspect every claim and citation manually.
3. Run rates, hours, overtime, penalties, breaks, leave, coverage, classification, termination, redundancy, and combined cases.
4. Run missing-evidence, ambiguous, legal-judgment, and personal-advice cases.
5. Run direct and indirect prompt injections.
6. Repeat non-deterministic cases.
7. Compare model and prompt candidates only after hard safety gates pass.
8. Verify that application policy is sent in a system role and evidence remains untrusted data.
9. Validate strict answer status, atomic claims, effective dates, calculations, and citations.
10. Run all 120 cases in `test-cases-05-prompt-assurance.md` against primary and fallback models.

Exit:

- claim grounding 100%;
- citation support 100%;
- citation completeness 100%;
- current-rate answers 100%;
- insufficient-evidence handling 100%;
- reviewed correctness at least 95%;
- no unsupported high-impact claim.

Evidence:

- raw prompts, contexts, outputs, and usage;
- claim review sheets;
- model/prompt comparison;
- reviewer sign-off.

Cost: C2 to C3.

## Phase 9: UI and accessibility

Entry:

- Phase 8 passed;
- deployment candidate available in staging.

Steps:

1. Test startup, query, citation, validation, failure, recovery, refresh, double-submit, and concurrent sessions.
2. Run supported browser and viewport matrix.
3. Complete keyboard and screen-reader flows.
4. Check focus, labels, status, error association, contrast, reflow, zoom, target size, and color independence.
5. Run automated accessibility scan and manual review.

Exit:

- core user flow passes every supported browser;
- zero session leakage;
- WCAG 2.2 Level A and AA checks pass or release is blocked.

Evidence:

- screenshots;
- browser logs;
- accessibility report;
- manual assistive-technology notes.

Cost: C2 to C3.

## Phase 10: security and privacy

Entry:

- threat boundaries and deployment design approved.

Steps:

1. Execute ASVS-based input, output, configuration, error, session, logging, and deployment tests.
2. Execute LLM prompt and source injection cases.
3. Test artifact tampering and unsafe deserialization in a sandbox.
4. Verify secrets, outbound provider payload, retention, training use, and region.
5. Test abuse limits, timeouts, retries, and cost caps.
6. Review CI, dependencies, backups, incident response, and decommissioning.

Exit:

- zero open S0 or S1 security/privacy defect;
- all external data handling approved;
- abuse controls proven.

Evidence:

- security report;
- outbound-data capture;
- provider review;
- accepted-risk records.

Cost: C2 to C3.

## Phase 11: performance, capacity, cost, and deployment

Entry:

- functional, safety, and security gates passed.

Steps:

1. Measure clean build, image size, model download, cold start, warm start, store load, and memory.
2. Measure CAG, RAG, and combined p50, p95, and maximum latency.
3. Ramp concurrency, run spike and soak tests, and find safe capacity.
4. Test provider timeout, rate limit, and outage.
5. Measure tokens, retries, provider charges, infrastructure, rebuild, storage, and operator time.
6. Calculate cost per request and cost per successful grounded answer.
7. Model 100, 1,000, 10,000, and 100,000 monthly questions.
8. Test build, health, shutdown, rolling update, rollback, restore, and disaster recovery.

Exit:

- full response p95 under 8 seconds on approved load;
- ten-user error rate under 1%;
- capacity and cost limits approved;
- rollback and recovery targets met.

Evidence:

- raw load results;
- resource graphs;
- provider usage;
- cost workbook;
- deployment and recovery logs.

Cost: C3 to C4.

## Phase 12: release review

Entry:

- every prior phase has a result.

Steps:

1. Freeze the candidate and rerun all applicable offline gates.
2. Verify every requirement and test has evidence.
3. Review all S0 through S3 defects and accepted risks.
4. Confirm corpus, store, model, prompt, configuration, and deployment identities.
5. Review legal, security, privacy, accessibility, operations, and product sign-offs.
6. Publish the release report.

Exit:

- every blocking gate passes;
- zero open S0 or S1;
- named owners approve residual risks;
- evidence is immutable and reproducible.

Cost: C1 after prior evidence exists.

## Current phase position

| Phase | Status |
|---|---|
| 0 Candidate control | fail |
| 1 Requirements and standards | fail |
| 2 Repository and dependencies | fail |
| 3 Source corpus | live reachability checked; acceptance fail |
| 4 Ingestion and data quality | diagnostic development fixture failed; formal phase blocked |
| 5 Cache and vector store | integrity fail; semantic concurrency diagnostic completed |
| 6 Routing | 60-request diagnostic failed |
| 7 Retrieval | semantic Award-recall diagnostic failed |
| 8 Answer grounding | historical literal-support diagnostic failed; live answers blocked |
| 9 UI and accessibility | loopback HTTP diagnostic completed; browser/accessibility blocked |
| 10 Security and privacy | static diagnostic failed; full phase blocked |
| 11 Performance and deployment | provider-free local load diagnostic failed; formal phase blocked |
| 12 Release | blocked |

The next cost-effective action is to select the actual development candidate, reconcile QA to it, and then provide and approve the raw 122-Award corpus. Provider evaluation before those controls pass would spend money on invalid evidence.
