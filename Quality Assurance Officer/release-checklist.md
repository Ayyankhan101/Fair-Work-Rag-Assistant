# Release checklist

## Source corpus

- [ ] Official A-Z Award list refreshed for the release date
- [ ] 122 mandatory Award IDs present
- [ ] 122 mandatory Award titles match
- [ ] NES entitlement list refreshed
- [ ] Amendment date recorded for every source
- [ ] SHA-256 recorded for every source
- [ ] Extra enterprise/public sources labelled separately
- [ ] No unreadable source
- [ ] No unexplained duplicate source

## Processing and stores

- [ ] Clause and schedule fixtures pass
- [ ] Page metadata exists
- [ ] Source URL check passes
- [ ] Empty chunk count is zero
- [ ] Exact duplicate chunk count is zero or each group is approved
- [ ] CAG manifest matches RAG manifest
- [ ] Cache, document store, and index counts agree
- [ ] Clean rebuild succeeds from source

## Retrieval and answers

- [ ] Router set passes 100%
- [ ] Award recall at 3 is at least 98%
- [ ] Award recall at 5 is 100%
- [ ] Clause recall at 5 is at least 95%
- [ ] Current-rate questions pass 100%
- [ ] Every answer claim is supported
- [ ] Every citation identifies supporting text
- [ ] Insufficient-evidence set passes 100%
- [ ] Ambiguity set passes 100%
- [ ] Prompt-injection set passes 100%

## Application and operations

- [ ] Windows run passes
- [ ] Linux CI passes
- [ ] Missing key behavior passes
- [ ] Rate-limit behavior passes
- [ ] Provider timeout behavior passes
- [ ] Corrupt-store behavior passes
- [ ] UI does not disclose exceptions or secrets
- [ ] Retrieval p95 is under 1 second
- [ ] Full response p95 is under 8 seconds
- [ ] Ten-user error rate is under 1%

## Evidence

- [ ] Commit SHA recorded
- [ ] Worktree state recorded
- [ ] Corpus and store hashes recorded
- [ ] Model and prompt recorded
- [ ] Raw retrieval and answers retained
- [ ] Manual reviewers named
- [ ] Open defects reviewed
- [ ] No S0 or S1 defect remains

Release decision: blocked until every unchecked S1-linked item passes.
