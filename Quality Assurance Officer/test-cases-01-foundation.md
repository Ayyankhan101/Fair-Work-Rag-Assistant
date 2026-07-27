# Test cases 01: repository, dependencies, documents, and CI

## Execution rule

These are specifications. They are not pass results.

For every execution:

1. Record timestamp, commit SHA, branch, dirty flag, operating system, Python version, and tester.
2. Copy the exact command or manual procedure into the run record.
3. Keep raw output. Redact secret values but retain the finding and path.
4. Compare the output with the stated pass condition.
5. Record `passed`, `failed`, `blocked`, `not run`, or `invalid`.
6. Open a defect for every unexpected result.

Never run branch-changing, staging, commit, push, merge, delete, or deployment scripts as a test unless the target is an isolated disposable repository.

## Repository cases

| ID | Risk | Procedure | Pass condition |
|---|---|---|---|
| REP-001 | Wrong code tested | Record `git rev-parse HEAD`, branch, remotes, and status before and after the run | identity is complete and unchanged |
| REP-002 | Dirty evidence | Run `git status --porcelain`; compare against the approved candidate | no unapproved change |
| REP-003 | Missing files | Compare `git ls-tree -r HEAD` with the release manifest | every required file is tracked |
| REP-004 | Hidden untracked inputs | List untracked and ignored files used by commands | no test depends on an undeclared file |
| REP-005 | Case-sensitive breakage | Compare paths for names differing only by case; run on Linux | no collision or missing import |
| REP-006 | Line-ending breakage | Measure LF/CRLF by file type; syntax check scripts on Linux | configured endings match executable format |
| REP-007 | Large-file drift | Run Git LFS status and pointer checks | every LFS object is present and matches its pointer |
| REP-008 | Generated artifact drift | Hash cache, index, docstore, and result files twice | unchanged inputs produce declared outputs |
| REP-009 | Binary provenance gap | Map each binary to producer, version, source hash, and license | 100% of binaries have provenance |
| REP-010 | Accidental secret | Scan current files with pattern, entropy, and known-provider rules | zero unapproved secret |
| REP-011 | Secret in history | scan every reachable Git commit without printing values | zero live or unrevoked secret |
| REP-012 | Unsafe ignore rules | inspect `.gitignore`, LFS rules, and nested ignore files | secrets and local state ignored; evidence not hidden |
| REP-013 | Broken JSON | Parse every tracked and candidate JSON file as UTF-8 | zero parse failure |
| REP-014 | Broken YAML | Parse every workflow and configuration YAML file | zero parse failure |
| REP-015 | Broken Python syntax | compile every active Python source in an isolated tree | zero compile failure |
| REP-016 | Broken shell syntax | run `bash -n` for every shell file using Linux Bash | zero syntax failure |
| REP-017 | Unsafe shell behavior | run ShellCheck and manually inspect destructive commands | zero unapproved high-severity finding |
| REP-018 | User-specific path | search for home directories, drive letters, and named users | no active command depends on a developer path |
| REP-019 | Missing license | inventory source, data, models, plugins, fonts, and binaries | license and use basis recorded for each |
| REP-020 | Repository bloat | report file count and bytes by product, evidence, generated, personal, and vendor class | release repository contains only approved classes |

## Dependency cases

| ID | Risk | Procedure | Pass condition |
|---|---|---|---|
| DPN-001 | Resolver failure | resolve direct requirements on supported Python without using an existing environment | exit 0 |
| DPN-002 | Version drift | resolve twice from the same lock and compare | identical package names, versions, and hashes |
| DPN-003 | Unsupported Python | run clean install and imports on every supported Python minor version | all supported versions pass |
| DPN-004 | Unpinned direct dependency | inspect every direct requirement | exact version or approved bounded policy for each |
| DPN-005 | Unlocked transitive dependency | compare requirements with reviewed lock | complete transitive lock exists |
| DPN-006 | Package tampering | install with artifact hashes and index restrictions | every artifact hash verifies |
| DPN-007 | Known vulnerability | run `pip-audit` or equivalent against the exact lock | zero unaccepted vulnerability |
| DPN-008 | Malicious or abandoned package | review publisher, repository, release age, and ownership changes | every direct package approved |
| DPN-009 | License conflict | produce an SBOM and scan licenses | zero incompatible or unknown license |
| DPN-010 | Dependency confusion | inspect package sources and private/public name collision | all names resolve from approved indexes |
| DPN-011 | Offline rebuild failure | install from a captured wheelhouse with network disabled | clean environment installs and imports |
| DPN-012 | Excess dependency cost | measure download, installed bytes, files, and package count | within approved deployment budget |
| DPN-013 | Import-time side effect | trace imports for network, file writes, model downloads, and service start | no undeclared side effect |
| DPN-014 | Optional package required at runtime | run each route with only declared production dependencies | zero hidden dependency |
| DPN-015 | Audit database age | record audit-tool and vulnerability-database timestamps | data age within policy |

## Document cases

| ID | Risk | Procedure | Pass condition |
|---|---|---|---|
| DOC-001 | Unstable requirements | assign a stable ID to every “shall,” “should,” success criterion, and deliverable | 100% identified |
| DOC-002 | Unmeasurable wording | review “accurate,” “fast,” “reliable,” “minimal,” and similar terms | each has a numeric acceptance rule |
| DOC-003 | Missing ownership | record author, approver, status, version, and effective date | all controlled documents complete |
| DOC-004 | Requirements conflict | compare PDF, architecture, README, vault, tests, and official sources | every conflict resolved or open as a defect |
| DOC-005 | Stale official link | request each source URL and verify final destination and update date | all links valid and current |
| DOC-006 | PDF text loss | compare extracted text with every rendered page | no missing or reordered requirement |
| DOC-007 | PDF layout defect | inspect headings, lists, links, page breaks, footer, and whitespace | zero unreadable or collided content |
| DOC-008 | DOCX structure defect | inspect headings, tables, images, sections, and document properties | structure complete and intentional |
| DOC-009 | DOCX layout defect | render every page at 100% and inspect visually | zero clipped, overlapping, or broken item |
| DOC-010 | Missing traceability | map each requirement to design, code, test, and evidence | 100% traceability or explicit gap |
| DOC-011 | Unsupported claim | identify every count, percentage, latency, and cost statement | every claim links to dated raw evidence |
| DOC-012 | Historical confusion | label each old score, store, screenshot, and prototype | no historical item appears current |
| DOC-013 | Discard contamination | compare discard paths with build, test, package, and deploy inputs | discard content cannot enter the product |
| DOC-014 | Setup mismatch | perform each documented command from a clean checkout | every supported command works |
| DOC-015 | Human readability | review with a new operator and time each procedure | operator completes it without undocumented help |

## CI and configuration cases

| ID | Risk | Procedure | Pass condition |
|---|---|---|---|
| CIC-001 | CI misses main branch | compare trigger branches with real branch policy | all protected branches covered |
| CIC-002 | CI misses paths | change one file in each product area in a disposable branch | required jobs run for every affected area |
| CIC-003 | CI command drift | compare local runbook commands with workflow commands | commands and versions match |
| CIC-004 | CI imports wrong symbol | run every workflow import line in a clean environment | all imports pass |
| CIC-005 | Tests absent from CI | inspect jobs and intentionally fail one test in a disposable branch | CI blocks the candidate |
| CIC-006 | Failure ignored | search `|| true`, continue-on-error, swallowed exits, and allowed failures | no release gate can be hidden |
| CIC-007 | Action supply-chain risk | inspect action versions and commit pinning | actions pinned to approved immutable versions |
| CIC-008 | Excess workflow permission | inspect job and token permissions | least privilege for every job |
| CIC-009 | Direct-push false control | test repository branch protection, not post-push workflow output | prohibited push is rejected before update |
| CIC-010 | Cache poisoning | inspect cache keys, restore scope, and write permissions | untrusted changes cannot seed release caches |
| CIC-011 | Stale cache | change corpus, model, prompt, and dependency lock independently | each relevant change invalidates its cache |
| CIC-012 | Secret exposure in logs | run failing provider setup with a canary value | canary never appears in log or artifact |
| CIC-013 | Matrix gap | execute supported OS and Python matrix | all required cells pass |
| CIC-014 | Non-reproducible tool | pin Ruff, audit, test, and packaging tools | tool versions recorded and repeatable |
| CIC-015 | Artifact overwrite | run two evaluations with different identities | separate immutable artifacts retained |

## Current status

| Group | Defined cases | Executed in Step 1 |
|---|---:|---:|
| Repository | 20 | partial |
| Dependencies | 15 | partial |
| Documents | 15 | partial |
| CI and configuration | 15 | partial |
| Total | 65 | partial |

No group is complete. Step 1 evidence must be mapped case by case before any group is marked passed.

