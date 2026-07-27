# Test strategy

## Test order

Run cheap deterministic checks before embeddings or model calls.

1. Repository and dependency checks
2. Unit tests
3. Corpus identity and freshness
4. Ingestion fixtures
5. Store integrity
6. Router and retrieval
7. Answer grounding
8. UI and provider failures
9. Performance and concurrency
10. Release review

An answer evaluation is invalid when the corpus gate fails.

## Difficulty tiers

| Tier | Label | Example | Main metric |
|---|---|---|---|
| 0 | Static | imports, lint, metadata schema | pass/fail |
| 1 | Super easy | confirm MA000022 exists | 122/122 coverage |
| 2 | Easy | retrieve Cleaning Award coverage | Award recall |
| 3 | Medium | find a current Level 3 rate | clause recall and date |
| 4 | Hard | apply employment type and exception | factual correctness |
| 5 | Super hard | compare two Awards and the NES | claim grounding |
| 6 | Impossible | request legal judgment absent from sources | safe refusal |
| 7 | Server melter | concurrent long and adversarial queries | latency and error rate |

## Mandatory test sets

| Set | Minimum size | Composition |
|---|---:|---|
| Award presence | 122 | one test per official Award ID |
| Award retrieval | 244 | two labelled questions per Award |
| Clause retrieval | 122 | one clause or schedule per Award |
| NES | 24 | two questions per entitlement grouping |
| Router | 80 | CAG, RAG, combined, ambiguous, and unknown |
| Answer | 80 | rates, hours, breaks, leave, coverage, and comparisons |
| Insufficient evidence | 30 | absent fact, missing Award, and legal judgment |
| Injection | 25 | question and retrieved-text instruction attacks |
| UI/failure | 20 | input, store, key, provider, and encoding failures |

## Release thresholds

| Gate | Threshold |
|---|---:|
| Mandatory Award IDs | 122/122 |
| Mandatory Award title match | 122/122 |
| Required metadata | 100% |
| Empty chunks | 0 |
| Unexplained exact duplicates | 0 |
| Router labelled set | 100% |
| Target Award recall at 3 | at least 98% |
| Target Award recall at 5 | 100% |
| Clause recall at 5 | at least 95% |
| Current-rate questions | 100% |
| Claim grounding | 100% |
| Citation support | 100% |
| Overall reviewed answer correctness | at least 95% |
| Insufficient-evidence handling | 100% |
| S0 and S1 defects | 0 open |
| Retrieval latency p95 | under 1 second |
| Full response latency p95 | under 8 seconds |
| Ten-user error rate | under 1% |

## Evaluation record

Every evaluation output must contain:

- run timestamp in UTC;
- commit SHA;
- dirty-worktree flag;
- corpus manifest SHA-256;
- vector-store SHA-256;
- embedding model and version;
- LLM provider and model;
- prompt version or hash;
- retrieval parameters;
- raw retrieved chunk IDs;
- raw answer;
- scorer version;
- reviewer name for manual decisions.

Results without these fields are not release evidence.

## Stop conditions

Stop the run and mark it invalid when:

- an expected source is missing;
- the source version is unknown;
- CAG and RAG use different corpus revisions;
- the store count differs from its manifest;
- a provider changes the requested model;
- an evaluation question has no reviewed gold evidence;
- the worktree changes during the run.
