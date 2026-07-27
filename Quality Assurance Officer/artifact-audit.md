# Artifact audit

## Scope

The repository contains three different bodies of material:

1. the active Fair Work assistant;
2. a Cortex/Obsidian workspace;
3. a discarded general-purpose RAG prototype inside the QA folder.

Only the active Fair Work assistant is the release target. The other material still matters because it affects repository size, reviewer clarity, supply-chain exposure, and accidental deployment risk.

## Tracked repository

| Area | Files | Finding |
|---|---:|---|
| `Cortex-insight-analytics` | 57 | unrelated vault and bundled Obsidian plugins dominate the tracked file count |
| `data` | 15 | contains generated stores, NES captures, mappings, and historical evaluations; raw Award sources are absent |
| `src` | 12 | active application code |
| `skills` | 8 | local operating scripts and notes |
| `scripts` | 8 | smoke, evaluation, rename, PR, and verification scripts |
| `.opencode` | 6 | project instructions and agent material |
| repository root | 6 | setup, build, requirements, and Git files |
| `.github` | 5 | four workflows plus related configuration |

Tracked size is 58,739,487 bytes. The largest files are:

| Bytes | File | Risk |
|---:|---|---|
| 25,509,513 | `data/vectorstore/docstore.json` | generated evidence without a source manifest |
| 21,229,553 | `data/docs_cache.pkl` | unsafe deserialization if tampered with |
| 6,616,194 | `data/vectorstore/index.tvim` | generated binary tied to unknown source revision |
| 1,329,444 | Obsidian Dataview `main.js` | third-party bundled code outside the product |
| 779,367 | Obsidian OpenCode `main.js` | third-party bundled code outside the product |

Room for improvement:

- separate the active application from personal vault material;
- keep generated release artifacts in a versioned artifact store with manifests;
- document which third-party bundles are intentionally vendored;
- add license and provenance records for vendored plugins;
- make the raw source corpus reproducible without relying on local files.

## Requirements PDF

File:

```text
System Under Test (SUT)/Fair_Work_Awards__NES_LLM_Knowledge_Assistant.pdf
```

Observed:

- seven pages;
- 7,064 extractable text characters;
- no blank text pages;
- all pages rendered;
- readable headings, body text, lists, and links.

Content findings:

- it requires 122 Modern Awards and the NES;
- it requires source metadata, clause preservation, insufficient-information handling, and avoidance of unsupported legal advice;
- “within a few seconds,” “accurate,” “reliable,” and “minimal hallucinations” have no numeric acceptance criteria;
- no privacy, security, accessibility, authentication, retention, audit-log, recovery, or cost requirement is defined;
- no supported browser, operating system, Python version, deployment topology, or concurrency target is defined;
- no source-freshness service level is defined;
- no owner or process is defined for legal review;
- no answer schema defines how claim-to-citation support is represented.

Freshness finding:

The PDF's NES list is older than the Fair Work page last updated 11 May 2026. The current official page includes casual employment, family and domestic violence leave, superannuation contributions, and the Casual Employment Information Statement. These are not all stated in the PDF's list.

Layout findings:

- pages 1 through 5 are clear;
- page 6 places body text on the same line as the `Deliverables` and `Success Criteria` headings;
- page 7 contains only the final five bullets and a large unused area;
- the document has no version date, approver, change history, stable requirement IDs, or page footer.

## Architecture DOCX

File:

```text
System Under Test (SUT)/FairWork_Architecture_Design_Document_HYBRID_CAG_RAG.docx
```

Observed:

- 117 non-empty paragraphs;
- two tables;
- two inline images;
- one section;
- version 1.0;
- structured headings through section 9.

Strengths:

- separates CAG, RAG, and combined routing;
- requires shared citation metadata;
- states that insufficient evidence must not be guessed;
- identifies cache staleness, router misses, cache growth, and citation consistency risks.

Gaps:

- no date, author, approver, status, or change history;
- no component versions or deployment diagram;
- no authentication, authorization, privacy, threat model, logging, rate limit, timeout, retry, or recovery design;
- no cache size or token budget;
- no objective rule for promoting clauses into CAG;
- no proof that “frequently asked Award clauses” fit within provider context limits;
- no version handshake between CAG and RAG;
- no source manifest, checksum, effective date, or rollback process;
- no claim verifier between LLM output and presentation;
- no answer-level audit record;
- no cost model;
- no accessibility design;
- “respond within a few seconds” is not converted into a measurable service level.

Rendering limitation:

LibreOffice is unavailable in the test environment. The text, table, section, and image structure was inspected, but page layout was not rendered. Layout status is blocked, not passed.

## Source image and prior chat

The PNG states the required QA posture: verify every document before, during, and after processing, from easy cases through server-load cases. It also records the official Award list URL.

`cursor chat.txt` is planning context. It is not a signed requirement, test record, or release approval.

## Discarded prototype

Path:

```text
System Under Test (SUT)/Discard/RAG-Powered-Document-Assistant-feature-integration-deployment/
```

This is an unrelated assistant over 18 AI research PDFs. It must not be mixed with Fair Work release evidence.

Observed:

- 18 readable PDFs;
- 658 total PDF pages;
- 2,744 reported chunks;
- 10 evaluation questions;
- reported retrieval hit rate 0.8;
- reported answer F1 0.0487;
- reported citation precision 0;
- reported `hallucination_rate` 49.5.

The last value is labelled as a rate but is not bounded from 0 to 1 or 0% to 100%. Its calculation averages a count, so the metric name is wrong.

Serious findings:

- `rag_chain.py` constructs an LLM prompt but never sends it to a model;
- the `model` argument is unused;
- the answer is a two-sentence lexical overlap heuristic, not the documented generation chain;
- FAISS is loaded with `allow_dangerous_deserialization=True`;
- uploaded PDFs overwrite the vector store instead of merging into a controlled corpus;
- upload size, PDF structure, timeout, and resource limits are absent;
- temporary files are removed only after successful processing;
- chat history is stored in one shared JSON file;
- user questions are inserted into an `unsafe_allow_html=True` history block;
- no authentication, authorization, session isolation, or privacy notice exists;
- Docker runs as root and uses unpinned dependencies;
- Docker has no health check or resource limits;
- the source/data contract claims sentence-boundary preservation, normalized embeddings, and page metadata without stored verification evidence;
- `2305.10403.pdf` is PaLM 2, but the README and evaluation treat it as LLaMA 2;
- the stored evaluation is therefore not a trustworthy release oracle;
- several files contain mojibake;
- the Week 1 document says all tools run locally without paid keys, while the implementation and later active project use a hosted provider.

Because the directory is named `Discard`, these findings do not block the active product by themselves. Keeping the directory inside the QA source tree creates reviewer confusion and adds about 62 MB of unrelated material.

## Research PDFs

All 18 PDFs opened and contained extractable text. They cover Transformers, BERT, original RAG, GPT-3, instruction following, BLIP-2, Toolformer, LLaMA, GPT-4, climate-research mapping, PaLM 2, quantization, preference optimization, RAG evaluation, and a RAG survey.

They are background reading. They do not provide:

- Fair Work gold answers;
- current Award text;
- legal review;
- a corpus manifest;
- product performance evidence;
- permission to release.

## Repository scripts

All four tracked shell scripts use CRLF line endings.

`bash -n` result:

| Script | Result |
|---|---|
| `Cortex-insight-analytics/create-vault.sh` | fail: unexpected end of file |
| `scripts/auto-pr.sh` | fail: unexpected end of file |
| `scripts/run_verification.sh` | pass |
| `scripts/wait_and_verify.sh` | fail: unexpected end of file |

Other script risks:

- `auto-pr.sh` stages all files, commits, pushes, attempts a merge, deletes the branch, and switches branches; it is too destructive for a QA command;
- `auto-pr.sh` has no confirmation, target verification, secret scan, or clean-tree rule;
- `wait_and_verify.sh` hides verification failure with `|| true`;
- `wait_and_verify.sh` writes `verification.log` without run metadata;
- `run_verification.sh` assumes `venv/bin/python3`, which is not the Windows environment used for this audit;
- `create-vault.sh` contains a user-specific absolute path.

## Documentation conflicts

The repository contains claims of 122, 129, and 130 Awards. Historical evaluation scores are presented without a complete link to the current source corpus and code revision.

Required improvement:

1. Establish one generated source of truth for scope.
2. Generate counts and versions from the corpus manifest.
3. Remove hand-maintained accuracy and performance claims from release-facing documents.
4. Label discarded and historical artifacts so they cannot be mistaken for current evidence.

