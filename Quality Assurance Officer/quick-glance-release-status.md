# Quick glance: release status

## Decision

Release blocked.

Latest clean-baseline execution: every product path matches the QA/develop fork point. The restored code passes 2 of 16 QA unit-test methods, fails a declared-dependency import, and stops before request one on natural Windows encoding. With missing dependency and UTF-8 controls supplied only to diagnose deeper behavior, 31 of 60 request cases pass all applicable checks.

## Highest risks

| Risk | Current fact |
|---|---|
| corpus | MA000095 and MA000121 are missing |
| identity | MA000002 is mislabelled |
| reproducibility | raw Award sources are absent |
| prompt | no actual system-role message exists |
| model continuity | both configured Groq models shut down for developer tiers on 16 August 2026 |
| evaluation | the 87.55% historical score lacks provenance and claim checks |
| citations | no claim-to-source release test has passed |
| privacy | external data handling is not approved |
| deployment | UI, load, recovery, and security gates are unexecuted |
| API assurance | no replacement model has a live conformance, quality, failure, or cost result |
| candidate control | QA is four commits behind the changing development branch |
| development ingestion | preamble and `15.1` metadata loss reproduced |
| supply chain | unpinned dependencies and 12 unpinned GitHub Action uses |
| process | completion was self-declared despite 10 of 12 correctness and failed acceptance math |
| licensing | README claims MIT but the linked license file does not exist |
| clarification | zero of nine ambiguous, unknown, typo, or nonsense cases were gated |
| semantic retrieval | expected Award appears in only 16 of 36 raw top-1 results |
| historical answers | only four of 25 pass a weak current-context support check |
| local capacity | provider-free 32-worker p95 is 7.902 seconds at 1.276 GB peak RSS |
| declared dependencies | `rank_bm25` is imported but absent from `requirements.txt` |
| product static checks | Ruff reports 90 findings; 17 of 18 files need formatting |

## What passed

- 117 tracked paths inventoried.
- 34 tracked JSON and four YAML files parse.
- every product path outside the QA folder matches fork point `3e91e9e`.
- all 29 checked product and QA Python files parse as Python syntax.
- 2 of 16 QA unit-test methods pass against the restored baseline.
- an earlier dirty-QA run passed 16 tests but measured only 12% statement coverage; that code was reverted.
- official live Award pages respond for 122 of 122 IDs.
- 485 unique QA test specifications are defined.
- 33 development-archive Python files compile and pass Ruff.
- limited active-text and Git-blob scans found no candidate secret.
- 300 concurrent in-process semantic searches completed without error.
- 288 corrected loopback HTTP load requests completed without a request error.

These results do not make the release acceptable.

## Next valid action

Select and freeze the actual development candidate, reconcile QA to it, and materialize a checksummed 122-Award plus NES source corpus. Do not spend money on full model evaluation before those inputs pass.

Current handoff: `developer-handoff-after-qa-2026-07-27.md`.
