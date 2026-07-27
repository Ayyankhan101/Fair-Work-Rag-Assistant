# Security review

## Summary

Release blocked.

High-severity integrity and code-execution risks remain in the document pipeline. The current development branch introduces a Markdown parser that loses preamble content and subclause identity, while the executable cache is not bound to an accepted corpus or parser version. The application also sends its policy, user question, and retrieved evidence as one human-role model message, sends employment data to an external model without a documented data-handling policy, has no verified dependency lock, and does not validate generated claims against retrieved sources.

The security skill contains no Python-general or Gradio-specific reference. This review therefore applies repository-specific Python and general secure-default checks to the Gradio application.

## High severity

### SEC-001: pickle cache can execute code

Location: `build_store.py:27`

`pickle.load()` executes Python object reconstruction instructions. A modified `data/docs_cache.pkl`, LFS object, downloaded artifact, or compromised branch can execute code under the account running the build.

Impact: repository or artifact compromise can become arbitrary code execution.

Required fix:

1. Replace the pickle cache with a non-executable format.
2. Until replacement, require a SHA-256 value from a reviewed manifest before loading.
3. Never load a cache supplied through a user upload or untrusted build artifact.

Status: open.

### SEC-002: answer claims are not verified after generation

Location: `src/rag.py:17-60`

The prompt tells the model to stay within context, but no code checks whether an Award name, clause, amount, percentage, or date in the answer occurs in the supplied chunks. Prompt instructions are not an enforcement boundary.

Impact: a fabricated pay rate or clause can be displayed as sourced legal information.

Required fix:

1. Return retrieved chunk IDs with the answer.
2. Parse the five response fields.
3. Reject numbers, Award names, and clauses that cannot be matched to a cited chunk.
4. Use an insufficient-evidence response when validation fails.

Status: open.

### SEC-003: external model data handling is undefined

Location: `src/rag.py:62-74`, `src/app.py:43-69`

User questions and retrieved text are sent to Groq. Employment questions can contain names, workplaces, pay details, health information, union activity, or dispute facts. The UI has no warning, redaction step, retention statement, or operator policy.

Impact: personal or workplace information may be disclosed to an external provider without an approved handling rule.

Required fix:

1. Define allowed and prohibited input data.
2. Display a short privacy warning before submission.
3. Redact obvious identifiers before provider calls where feasible.
4. Document provider retention and region settings.
5. Do not log raw questions by default.

Status: open.

### SEC-009: application policy has no system-role boundary

Location: `src/rag.py:142`

`ChatPromptTemplate.from_template()` renders the combined policy, evidence, and question as one human-role message. An isolated LangChain render reproduced this result. Direct user instructions and indirect instructions in retrieved text therefore compete inside the same message as the application rules.

Impact: prompt injection can redirect the task, request fabricated claims, or suppress limitations. A sentence telling the model to ignore such instructions is not a security boundary.

Required fix:

1. Put stable policy in a system-role message.
2. Put the question and delimited evidence in a separate user-role message.
3. Validate trusted metadata outside the model.
4. Use strict structured output and deterministic claim checks.
5. Pass all 120 prompt-assurance specifications.

Status: open.

### SEC-010: development ingestion loses legal source content

Location: `develop:scripts/ingest_markdown.py:14-40`, `develop:scripts/ingest_markdown.py:52-66`

The parser does not emit content before the first recognized `##` or `###` heading, and its clause expression does not recognize a subclause heading such as `15.1 Minimum rates`. An isolated fixture reproduced both failures.

Impact: retrieved evidence can omit controlling text or carry an incomplete citation while the system presents the derived store as a complete legal source.

Required fix:

1. Preserve preamble and every recognized source block.
2. Parse the full clause, subclause, paragraph, schedule, and table hierarchy.
3. Compare accepted source text, generated Markdown, and final chunks through a loss report.
4. Block publication on any unexplained loss.

Status: open on `develop`; not present in the older QA HEAD.

### SEC-011: derived artifacts are not bound to trusted inputs

Location: `develop:build_store.py:21-67`

An existing pickle cache is loaded before input-mode selection and contains no source manifest, parser version, configuration hash, or content checksum. More than 100 Markdown files is treated as sufficient input, and an existing store without a checkpoint can be appended from document zero.

Impact: stale, incomplete, duplicated, mixed-format, or malicious content can silently control the deployed retrieval index.

Required fix:

1. Replace executable serialization.
2. Require an exact accepted source manifest.
3. Bind cache, checkpoint, and store to source, parser, embedding, and configuration hashes.
4. Reject mismatches and publish only a new atomically completed store.

Status: open on `develop`.

## Medium severity

### SEC-004: dependencies are not locked

Location: `requirements.txt:1-12`

Every dependency is unpinned. A clean install can resolve different versions, change model behavior, or include a newly compromised release.

Required fix: generate and review a hash-locked dependency file for CI and release builds. Keep `pip-audit` as a separate gate.

Status: open.

### SEC-005: public binding can be enabled without an access-control gate

Location: `src/app.py:101-106`

The secure default now binds to `127.0.0.1`. An environment variable can still bind the application publicly without authentication, request quotas, or a reverse-proxy requirement.

Required fix: require an explicit production mode and documented authentication/rate-limiting layer before accepting a non-loopback bind.

Status: partially fixed.

### SEC-006: provider calls have no application-level timeout or request budget

Location: `src/rag.py:62-74`, `src/rag.py:194-223`

Model calls use provider defaults. The application has no total request deadline, concurrency limit, or per-user budget.

Required fix: define connection and response deadlines, cap concurrent requests, and return a controlled timeout message.

Status: open.

### SEC-007: source URLs can be constructed from an unverified filename

Location: `src/ingest.py:185-198`, `src/ingest.py:338`

When a filename is absent from the mapping, `get_award_slug()` returns a lower-case filename and the ingestion code presents the resulting URL as a Fair Work source.

Required fix: fail ingestion when an Award ID has no reviewed URL mapping. Verify each URL and Award ID before indexing.

Status: open.

### SEC-008: branch workflow is not branch protection

Location: `.github/workflows/block-direct-push.yml`

The workflow runs after a push event. It can mark a check as failed, but it cannot undo or prevent the direct push.

Required fix: configure repository branch protection or rulesets outside the workflow. Require CI, review, and restricted pushes.

Status: open.

### SEC-012: GitHub Actions trust is mutable and over-permissioned

Location: `.github/workflows/audit.yml`, `.github/workflows/block-direct-push.yml`, `.github/workflows/ci.yml`, `.github/workflows/eval.yml`

The offline zizmor audit reports 12 unpinned action uses, nine excessive-permission findings, four checkout credential-persistence findings, and four missing-concurrency findings.

Required fix:

1. Pin Actions to reviewed full commit hashes.
2. Set top-level and job-level least-privilege permissions.
3. Set `persist-credentials: false` where Git writes are not required.
4. Add cancellation-safe concurrency groups.

Status: open.

### SEC-013: evaluation input and secret controls are incomplete

Location: `.github/workflows/eval.yml:39-52`

The dispatch input is directly expanded inside a shell script, and `GROQ_API_KEY` is used without a dedicated protected GitHub Environment. The choice input narrows current values but does not justify code-template expansion.

Required fix:

1. Pass the dispatch value through an environment variable.
2. Validate it against an explicit allowlist inside the script.
3. Use a protected evaluation environment with required approval and restricted secrets.
4. Pin, log, and retain the evaluated model, prompt, corpus, and cost limits.

Status: open.

### SEC-014: secret assurance is incomplete

Location: repository and Git object history

A 32-file active-text detect-secrets scan and a selected-signature scan of 122 Git blobs found no candidate secret. Both the full-repository and tracked-file detect-secrets scans exceeded 60 seconds.

Required fix:

1. Run a complete entropy and provider detector scan in CI.
2. Include Git history, LFS, artifacts, releases, and logs.
3. Rotate any credential whose exposure cannot be excluded.
4. Never convert “no match in a limited scan” into “secret-free.”

Status: open assurance gap; no secret was found in the completed scans.

## Proposed controls in the dirty working tree

| Control | Evidence |
|---|---|
| Empty and oversized questions rejected | `src/app.py:43-50` |
| Server exceptions hidden from users | `src/app.py:66-68` |
| Default bind changed to loopback | `src/app.py:101-106` |
| Question and retrieved instructions treated as untrusted | `src/rag.py:33` |
| Unsupported numbers and citations forbidden in prompt | `src/rag.py:30` |
| `.env` excluded from Git | `.gitignore` |
| Weekly dependency audit exists | `.github/workflows/audit.yml` |

These controls are unaccepted changes. Even if accepted, they do not close SEC-001 through SEC-014.

## Phase 5 automated evidence

| Check | Result |
|---|---|
| Bandit | B403 at `build_store.py:5`; B301 at `build_store.py:27` |
| zizmor | 36 findings across four workflows |
| narrowed detect-secrets | zero candidates in 32 active text files |
| selected Git-blob signatures | zero candidates in 122 blobs |
| full detect-secrets | timed out twice |
| dependency vulnerability refresh | timed out twice |
| development fixture | preamble loss, missing `15.1`, and oversized chunk reproduced |

The detailed qualification and limitations are in `phase-5-security-supply-chain-report-2026-07-27.md`.
