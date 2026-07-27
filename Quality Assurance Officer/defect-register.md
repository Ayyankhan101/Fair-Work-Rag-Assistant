# Defect register

Severity:

- S0: secret exposure, data loss, or unsafe legal output likely to cause harm.
- S1: wrong Award or entitlement, fabricated citation, broken build, or mandatory corpus gap.
- S2: limited incorrect behavior, stale evidence, or degraded retrieval.
- S3: documentation, cosmetic, or low-impact maintenance issue.

## Open defects

| ID | Severity | Defect | Evidence | Required closure |
|---|---|---|---|---|
| DEF-001 | S1 | MA000095 Car Parking Award is missing from the store | repository audit | ingest current source and rebuild |
| DEF-002 | S1 | MA000121 State Government Agencies Award is missing | repository audit | ingest current source and rebuild |
| DEF-003 | S1 | MA000002 is labelled `Workplace Relations Act 1996` | `docstore.json` | replace source, verify title and clauses |
| DEF-004 | S1 | `data/awards/` is absent | repository tree | provide checksummed source corpus |
| DEF-005 | S1 | hard-eval results lack commit, corpus, model, prompt, and time | `hard_eval_results.json` | rerun with provenance schema |
| DEF-006 | S1 | no source version field exists on chunks | chunk metadata | add version and rebuild |
| DEF-007 | S1 | page references are absent | chunk metadata | preserve page number during parsing |
| DEF-008 | S1 | current answer suite has no claim-to-source scoring | `scripts/eval_hard.py` | add reviewed claims and citation checks |
| DEF-009 | S2 | 1,251 duplicate chunks exist | repository audit | classify boilerplate and remove duplicates |
| DEF-010 | S2 | stored answers predate the current July 2026 store; only 4 of 25 passed a weak literal-support check against current retrieved context | H01 result vs MA000022 chunk; Phase 6 historical-claim probe | rerun after gold values are reviewed and require atomic claim-to-context scoring |
| DEF-011 | S2 | pickle cache is loaded without a signed manifest | `build_store.py` | replace format or verify checksum before load |
| DEF-012 | S2 | dependencies are unpinned | `requirements.txt` | add reviewed lock file |
| DEF-013 | S2 | alias coverage is far below 122 Awards | `src/config.py` | generate reviewed aliases and ambiguity cases |
| DEF-014 | S2 | NES source text contains mojibake | `data/nes/nes_combined.txt` | reacquire and validate UTF-8 source text |
| DEF-015 | S2 | Unix verification scripts have no PowerShell equivalent | `scripts/*.sh` | add a cross-platform runner |
| DEF-016 | S2 | no production-like UI, browser, provider, soak, or deployment load result exists; the provider-free loopback probe is diagnostic only | repository search; Phase 6 server probe | execute accepted browser, provider, soak, and deployment tests against an immutable candidate |
| DEF-017 | S3 | README and vault notes contain conflicting counts and scores | project documentation | replace claims with generated evidence |
| DEF-018 | S1 | the supplied requirements omit current NES items including casual employment, family and domestic violence leave, superannuation, and CEIS | requirements PDF vs Fair Work NES page updated 2026-05-11 | issue a reviewed requirements revision |
| DEF-019 | S1 | there is still no immutable accepted candidate: the product tree now matches the fork point, root README reverses the QA banner relative to HEAD, and the QA evidence folder is untracked | post-cleanup Git verification; change-control record | engineering selects and commits an immutable candidate while QA evidence is reviewed separately |
| DEF-020 | S1 | HEAD contains no tracked test files | `git ls-tree -r HEAD` | engineering adds reviewed tests to a candidate commit |
| DEF-021 | S2 | three of four shell scripts fail `bash -n` because executable files use CRLF | Step 1 shell log | use target-shell line endings and add Linux syntax gate |
| DEF-022 | S2 | `wait_and_verify.sh` hides verification failures with `|| true` | source inspection | propagate failure and store structured evidence |
| DEF-023 | S2 | `auto-pr.sh` stages all files, pushes, merges, deletes a branch, and switches branches without confirmation | source inspection | remove from QA flow or add isolated safety controls |
| DEF-024 | S2 | application import loads CAG, embedding model, store, and RAG chain before readiness; actual import failed after 15.349 seconds when the provider key was absent | `src/app.py`; Phase 6 startup probe | separate construction from import and provide explicit bounded readiness and configuration errors |
| DEF-025 | S2 | direct dependencies resolve to 95 installed packages without a lock or hash policy | isolated import and resolver output | approve and track a reproducible lock and SBOM |
| DEF-026 | S3 | requirements PDF has heading/body collision on page 6 and a mostly blank page 7 | rendered page inspection | reflow and reissue controlled PDF |
| DEF-027 | S3 | architecture DOCX layout could not be visually verified because LibreOffice is unavailable | document inspection log | render and inspect every page in a capable environment |
| DEF-028 | S3 | unrelated Cortex vault, bundled plugins, and discarded prototype increase scope and reviewer confusion | artifact inventory | separate product, QA evidence, personal workspace, vendor, and discard material |
| DEF-029 | S2 | dependency audit normalized an invalid transitive version specifier `>=3.6.*` | `pip-audit` output | identify the package and confirm corrected metadata in the lock |
| DEF-030 | S1 | deployment authentication, privacy basis, data retention, residency, and provider training-use controls are undefined | requirements, architecture, and security review | approve deployment and data-handling requirements before external use |
| DEF-031 | S1 | both configured Groq model IDs are scheduled to shut down for free and developer tiers on 16 August 2026 | Groq deprecation schedule; `src/rag.py` | qualify, approve, and deploy replacement model/prompt pairs before shutdown |
| DEF-032 | S1 | the application creates the prompt with `ChatPromptTemplate.from_template`, producing one human-role message rather than a system policy plus user input | isolated LangChain render; `src/rag.py:142` | separate role messages and pass prompt-assurance tests |
| DEF-033 | S1 | the committed prompt orders the model to answer confidently even when evidence is missing | `HEAD:src/rag.py` | replace the unsafe policy and qualify insufficient-evidence behavior |
| DEF-034 | S1 | no atomic claim, effective-date, or claim-to-citation output contract exists | active prompt and parser | implement structured claims and deterministic validation |
| DEF-035 | S1 | general questions are instructed to compare arbitrary retrieved Awards | active and committed prompt | require clarification or an explicit limited comparison scope |
| DEF-036 | S2 | the prompt claims it can scan all context, but documents are truncated at 800 characters and total formatted retrieval at 4,000 characters | `src/rag.py` | expose truncation, retrieve complete parent clauses, and fail closed |
| DEF-037 | S2 | no prompt ID or hash is stored with answers | prompt and historical result schema | version the system, user template, schema, examples, and parameters |
| DEF-038 | S2 | Award-page acquisition has no retained raw response, per-page hash, resume, conditional request, or atomic publish evidence | Phase 3 live check | implement and qualify versioned source acquisition |
| DEF-039 | S2 | earlier status, vault, skill, and evaluation documentation contains contradictory counts, completion states, quality claims, and deprecated model guidance | documentation critique | archive historical notes and generate status from evidence |
| DEF-040 | S2 | the first QA crawl oracle incorrectly required the Award ID inside the title heading | Phase 3 report | correct the parser, preserve raw cases, and regression-test the oracle |
| DEF-041 | S1 | the working-tree suite covers only 12% of statements and leaves the RAG, retrieval, ingestion, vector-store, provider, and UI paths at 0% | Phase 4 coverage report | add tracked critical-path tests and meet approved coverage and mutation gates |
| DEF-042 | S2 | unpinned dependency resolution selected yanked `numpy==2.4.0` | isolated `uv` resolution | lock reviewed versions with hashes and reject yanked packages |
| DEF-043 | S2 | the provider client has no explicit request timeout, tested backoff, jitter, or circuit breaker; timeout, 500, and 401 probes propagate from `ask_question` | effective `ChatGroq` configuration; `src/rag.py`; Phase 6 failure probe | implement and qualify bounded provider-failure controls |
| DEF-044 | S1 | 429, 413, and rate-limit fallbacks change model and prompt shape, nest the original mapping, repeat the question, and do not reduce context | `src/rag.py:193-227`; Phase 6 six-error probe | define fail-closed behavior or qualify a fallback with correct role messages, real context reduction, and equal hard-gate performance |
| DEF-045 | S2 | answers do not retain provider request ID, actual model, tokens, latency, retries, or cost | API path inspection | persist redacted per-request operational and cost evidence |
| DEF-046 | S2 | provider and model selection are hard-coded to Groq in application source | `src/rag.py`; requirements | introduce a reviewed provider contract and configuration boundary |
| DEF-047 | S1 | no live API conformance, prompt, claim, failure, or cost run exists for any current replacement candidate | credential check; API assurance report | execute the controlled provider matrix with approved keys, budget, corpus, and legal oracle |
| DEF-048 | S1 | the QA branch is four commits behind `develop`, whose untested changes alter conversion, ingestion, storage, and prompting | `git rev-list --left-right --count QA...develop`; Phase 5 report | select one immutable candidate and rerun every applicable gate |
| DEF-049 | S1 | the development Markdown parser discards all content before the first recognized level-two or level-three heading | isolated development fixture; `develop:scripts/ingest_markdown.py:14-40` | preserve preamble content and pass PDF-to-chunk round-trip tests |
| DEF-050 | S1 | the development Markdown parser fails to retain subclause identity such as `15.1` | isolated development fixture; `develop:scripts/ingest_markdown.py:52-66` | parse and validate the complete legal heading hierarchy |
| DEF-051 | S2 | the development chunker can emit a 1,601-character chunk when configured for a 1,500-character maximum | isolated development fixture; `develop:scripts/ingest_markdown.py:69-89` | split oversized single paragraphs and property-test the maximum |
| DEF-052 | S1 | the development builder accepts any corpus above 100 Markdown files and emitted metadata uses a generic Awards landing page without Award ID, version, page, or hash | `develop:build_store.py:21-24`; `develop:scripts/ingest_markdown.py:115-123` | require the exact accepted manifest and complete source provenance |
| DEF-053 | S1 | development conversion and ingestion continue after per-source errors and can print completion for a partial corpus | `develop:scripts/convert_pdfs_to_markdown.py:66-81`; `develop:scripts/ingest_markdown.py:172-187` | fail atomically and report expected, accepted, rejected, and published source counts |
| DEF-054 | S1 | the development builder loads any existing pickle cache before selecting PDF or Markdown input and can append from zero to an existing store without a checkpoint | `develop:build_store.py:21-67` | bind versioned artifacts to source and tool hashes and reject any mismatch |
| DEF-055 | S2 | all 12 GitHub Action uses are referenced by movable tags rather than reviewed commit hashes | zizmor 1.28.0 offline audit | pin every action to a reviewed full commit SHA and automate controlled updates |
| DEF-056 | S2 | workflows use default broad permissions, three checkout workflows retain credentials, and no workflow defines concurrency control | zizmor 1.28.0 offline audit | set least privilege, disable persisted credentials, and add safe concurrency groups |
| DEF-057 | S2 | the evaluation workflow expands a dispatch input directly inside shell code and uses the provider secret outside a protected GitHub Environment | `.github/workflows/eval.yml:39-52`; zizmor audit | pass the input through an environment variable, validate it, and require protected environment approval |
| DEF-058 | S2 | the README claims MIT and links to `LICENSE`, but no root license, copying, or notice file exists | `HEAD:README.md`; `git ls-tree` | obtain owner approval, add the actual license and notices, and correct the README |
| DEF-059 | S2 | OpenCode records self-certify completion despite 10-of-12 correctness, a failed target, invalid above-97% arithmetic, and skipped tasks marked complete | `.opencode/status.md`; `.opencode/quality-plan.md`; `.opencode/todo.md` | generate status from immutable evidence and enforce objective gate transitions |
| DEF-060 | S2 | no independent review is evidenced: one CODEOWNER covers the repository and the prescribed script immediately attempts self-merge | `CODEOWNERS`; `.opencode/context.md`; `scripts/auto-pr.sh` | require protected reviews, named sign-offs, and documented independence exceptions |
| DEF-061 | S1 | current `develop` cannot load the NES file under the natural Windows encoding and blocks before the first RAG+CAG request | `develop:src/cag.py`; Windows matrix attempt | read accepted text with explicit UTF-8 and pass the cross-platform request matrix |
| DEF-062 | S1 | configured Award names do not join to persisted metadata: Clerks and Children’s Services requests return zero Award documents | Phase 6 offline and semantic probes; `docstore.json` | use an Award-ID canonical key and reject any alias-to-corpus join failure |
| DEF-063 | S1 | the application has no clarification or answerability path; zero of nine ambiguous, unknown, typo, general, or nonsense cases could be gated for clarification | Phase 6 60-request matrix | introduce explicit insufficient-identity and insufficient-evidence states before retrieval and generation |
| DEF-064 | S1 | negation is ignored, so “not retail” selects Retail and “not sport” selects Sporting Organisations | Phase 6 cases RQ-052 and RQ-053 | implement negation-aware intent handling and adversarial routing tests |
| DEF-065 | S2 | topic detection missed eight of 47 expected common phrasings, including generic `leave`, `weekend`, `hours`, `casual-loading`, and injected rate wording | Phase 6 60-request matrix | normalize punctuation and maintain reviewed topic intents with negative and paraphrase tests |
| DEF-066 | S1 | raw semantic retrieval found the expected Award in only 16 of 36 top-1 and 24 of 36 top-10 Award-labelled queries | Phase 6 semantic retrieval probe | require Award-ID filtering or qualified hybrid retrieval and meet approved recall by risk slice |
| DEF-067 | S2 | every NES candidate receives the entire 38,482-character CAG cache; captured prompts reached 47,364 characters | Phase 6 offline request matrix | retrieve only relevant versioned NES sections and impose measured token and cost budgets |
| DEF-068 | S2 | provider-free loopback HTTP throughput remained below five requests per second and at 32 workers median latency was 5.936 seconds, p95 7.902 seconds, with 1.276 GB peak RSS | corrected Phase 6 server load probe | define SLOs, admission control, resource budgets, and rerun with provider and deployment topology |
| DEF-069 | S1 | current `develop` detected only 25 of 38 expected Award cases and supplied the expected Award in only 22 of 36 contexts even after forced UTF-8 | develop forced-UTF-8 request matrix | reconcile aliases and canonical Award IDs, then rerun on the actual development candidate |
| DEF-070 | S1 | the inherited baseline imports `rank_bm25` unconditionally but omits it from `requirements.txt`, so the declared-dependency request harness cannot import `rag.py` | `post-cleanup-matrix-baseline-dependencies-2026-07-27.stderr.txt` | add the reviewed dependency to a locked candidate and prove a clean install and import |

## Proposed changes made before the documentation-only boundary

These were working-tree changes, not accepted fixes. QA reverted all product-file changes to fork point `3e91e9e` on 27 July 2026. Recovery patches remain under `evidence/`; engineering may review them but must not treat them as accepted code.

| ID | Previous defect | Proposed change | Current evidence |
|---|---|---|---|
| FIX-001 | CI imported nonexistent function names | corrected `.github/workflows/ci.yml` | local clean imports pass; CI not run |
| FIX-002 | lint and format checks failed | mechanical cleanup | local Ruff passes |
| FIX-003 | `rank_bm25` was missing from dependencies | updated `requirements.txt` | clean isolated imports pass |
| FIX-004 | CAG failed to decode NES on Windows | explicit UTF-8 read | untracked `tests/test_cag.py` |
| FIX-005 | CAG cleaning deleted entitlement and Award lines | exact UI-line filtering | untracked `tests/test_cag.py` |
| FIX-006 | Award-only topics could receive NES cache content | CAG limited to NES keywords | untracked CAG unit test |
| FIX-007 | displayed route could differ from context path | context builder uses `route_question()` | untracked router unit tests; integration not run |
| FIX-008 | prompt forced an answer without evidence | insufficient-evidence and non-invention rules | untracked prompt-safety tests |
| FIX-009 | substring detection mapped `transport` to Sporting | word-boundary matching | untracked config unit test |
| FIX-010 | generic mining mapped to Black Coal | longest specific match plus generic mapping | untracked config unit test |
| FIX-011 | UI returned exception text to users | generic response plus server log | source inspection only |
| FIX-012 | completed store could be appended again | completed-count guard | builder unit test not run |
| FIX-013 | ingestion continued after source errors | aggregate failure after ingestion | ingestion fixture not run |

All rows in this section now have status `reverted from product tree; patch retained`.

## Release status

Blocked. All S1 defects must close before answer accuracy is reported as release-ready.
