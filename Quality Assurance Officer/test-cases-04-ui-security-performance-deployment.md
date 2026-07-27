# Test cases 04: UI, accessibility, security, performance, cost, deployment, and operations

## Environment rule

UI and deployment tests run against a named candidate artifact in an isolated environment. Record:

- application and artifact version;
- corpus and vector-store manifest hashes;
- model, prompt, and embedding versions;
- instance type, CPU, memory, disk, region, and operating system;
- browser and viewport;
- provider region and account tier;
- network conditions;
- test start and end time;
- measured provider usage and currency.

Do not use production personal data.

## UI cases

| ID | Scenario | Procedure | Pass condition |
|---|---|---|---|
| UI-001 | Local startup | start from documented command with valid configuration | ready signal and usable page |
| UI-002 | Missing API key | start and submit a query without key | safe setup message; no secret prompt in public UI |
| UI-003 | Invalid API key | use a revoked test key | controlled provider error |
| UI-004 | Missing store | start without index and source corpus | explicit failure; no uncontrolled rebuild |
| UI-005 | Corrupt store | alter isolated index bytes | integrity failure before query |
| UI-006 | Stale store | use mismatched corpus/store manifests | startup blocked |
| UI-007 | Empty input | submit blank and whitespace input | validation; no provider call |
| UI-008 | Length boundary | submit 1,999, 2,000, and 2,001 characters | exact declared behavior |
| UI-009 | Unicode input | submit punctuation, emoji, and non-Latin text | no crash or mojibake |
| UI-010 | Double submit | click or press Enter twice quickly | one logical request or clear duplicate handling |
| UI-011 | Back-to-back query | submit a second question before first finishes | defined queue/cancel behavior |
| UI-012 | Browser refresh | refresh during and after a query | defined state; no corrupt session |
| UI-013 | Multi-session isolation | use two browsers with distinct questions | no history or answer leakage |
| UI-014 | Error recovery | force provider failure, then restore service | next request succeeds without restart |
| UI-015 | Citation link | open every displayed citation | correct approved HTTPS source |
| UI-016 | Route label | compare label with server evidence | exact route |
| UI-017 | Long answer | render maximum allowed answer and citations | no clipping or unusable overflow |
| UI-018 | Mobile viewport | run core flow at 320 CSS pixel width | usable without lost function |
| UI-019 | Supported browsers | run core flow on approved browser matrix | all pass |
| UI-020 | No JavaScript/error fallback | simulate blocked resource and server exception | clear error without stack trace |

## Accessibility cases

Target: WCAG 2.2 Level AA for the complete user flow. Automated tools assist but do not establish conformance.

| ID | Scenario | Procedure | Pass condition |
|---|---|---|---|
| A11Y-001 | Keyboard only | complete query, read answer, and open citations without mouse | all functions reachable |
| A11Y-002 | Focus order | tab through page before, during, and after response | logical order |
| A11Y-003 | Focus visibility | inspect every focused component | visible and not obscured |
| A11Y-004 | Accessible names | inspect input, submit, retry, links, and status controls | meaningful name, role, and value |
| A11Y-005 | Heading structure | inspect accessibility tree | one logical hierarchy |
| A11Y-006 | Status announcement | use screen reader while loading, succeeding, and failing | status announced without focus theft |
| A11Y-007 | Error association | trigger input and provider errors | error linked to affected control |
| A11Y-008 | Contrast | measure text, links, focus, controls, and status indicators | WCAG AA ratios |
| A11Y-009 | Zoom | test 200% browser zoom | no loss of content or function |
| A11Y-010 | Reflow | test 320 CSS pixel width and 400% equivalent | no two-dimensional scroll except allowed content |
| A11Y-011 | Target size | measure interactive targets | WCAG 2.2 minimum or documented exception |
| A11Y-012 | Color independence | inspect route, error, and source states without color | meaning retained |
| A11Y-013 | Motion | inspect spinners and transitions with reduced motion | preference respected |
| A11Y-014 | Plain language | test instructions and errors with representative users | tasks understood |
| A11Y-015 | Automated scan | run axe or equivalent on every state | zero serious or critical finding; manual review complete |

## Security and privacy cases

| ID | Risk | Procedure | Pass condition |
|---|---|---|---|
| SEC-001 | Public unauthenticated access | bind to non-loopback in isolated network and request page | access policy enforced |
| SEC-002 | Missing authorization | attempt any administrative, rebuild, log, or artifact action as ordinary user | denied |
| SEC-003 | Excess request rate | exceed user, IP, and global limits | controlled 429 or equivalent |
| SEC-004 | Oversized request | send body and question above limit at proxy and app | rejected before expensive work |
| SEC-005 | Slow request | send slow body and hold connections | timeouts protect workers |
| SEC-006 | Prompt injection | run direct, indirect, encoded, multilingual, and split injections | grounding rules remain effective |
| SEC-007 | Source injection | index an isolated malicious instruction fixture | instruction never controls model |
| SEC-008 | Output injection | cause Markdown, HTML, script, image, and link payloads in output | rendered safely |
| SEC-009 | Link spoofing | return punycode, user-info, redirect, and look-alike URLs | blocked or clearly untrusted |
| SEC-010 | Path traversal | supply path-like values through every input and metadata field | no file outside approved roots read |
| SEC-011 | Unsafe deserialization | replace pickle/cache with a canary exploit artifact in a sandbox | rejected without code execution |
| SEC-012 | Artifact tampering | alter cache, docstore, index, manifest, and prompt separately | integrity check blocks use |
| SEC-013 | Secret in source | scan current tree and history | zero live secret |
| SEC-014 | Secret in log | trigger auth and provider failures with canary key | key never logged |
| SEC-015 | Secret in UI | inspect client HTML, errors, and network traffic | no key or internal credential |
| SEC-016 | User data in log | submit canary name, email, address, health, union, and dispute details | retention matches approved policy |
| SEC-017 | Provider disclosure | capture outbound request in approved test proxy | only approved fields sent |
| SEC-018 | Provider retention | review contract and account controls | retention and training use approved |
| SEC-019 | Data residency | trace provider endpoint and storage regions | approved regions only |
| SEC-020 | Cross-user leakage | run simultaneous distinct canaries | zero leakage |
| SEC-021 | Exception disclosure | force parser, store, model, and provider exceptions | no stack, path, key, or internal object in UI |
| SEC-022 | Dependency compromise | verify lock, hashes, SBOM, signatures, and index policy | supply-chain policy met |
| SEC-023 | CI token privilege | inspect and test workflow permissions in disposable repo | least privilege |
| SEC-024 | Cache poisoning | attempt untrusted artifact insertion through CI cache | release job rejects it |
| SEC-025 | Denial by expensive query | send long, repeated, and adversarial questions | budget and timeout enforced |
| SEC-026 | Model cost abuse | request repeated retries and maximum output | per-request and account caps enforced |
| SEC-027 | Log injection | include newlines, control characters, and fake severity text | structured logs remain trustworthy |
| SEC-028 | Vulnerability response | simulate a critical dependency advisory | owner can identify, patch, test, and revoke within policy |
| SEC-029 | Backup exposure | inspect backup encryption, access, expiry, and restore logging | policy met |
| SEC-030 | Decommission | remove an isolated deployment and credentials | endpoint, data, cache, key, and logs handled per policy |

## Performance, capacity, and cost cases

Run each route separately: CAG, RAG, and combined. Warm and cold results are separate.

| ID | Scenario | Procedure | Pass condition |
|---|---|---|---|
| PFC-001 | Dependency cold setup | time clean environment creation and record bytes/packages | within deployment build budget |
| PFC-002 | Image/build size | measure source, dependencies, model, store, and final image | within hosting budget |
| PFC-003 | Application cold start | start fresh instance until readiness | within service level |
| PFC-004 | Warm restart | restart with local caches present | within service level |
| PFC-005 | Model download | clear approved model cache and measure download/time | declared and acceptable |
| PFC-006 | Store load | time and sample memory while loading store | within instance limit |
| PFC-007 | CAG latency | run at least 100 labelled CAG queries | p50, p95, max recorded; p95 within target |
| PFC-008 | RAG latency | run at least 100 labelled RAG queries | p50, p95, max recorded; p95 within target |
| PFC-009 | Combined latency | run at least 100 labelled combined queries | p50, p95, max recorded; p95 within target |
| PFC-010 | Retrieval-only latency | exclude model time and run labelled set | p95 under 1 second |
| PFC-011 | Generation-only latency | use fixed context sizes | curve recorded by input/output tokens |
| PFC-012 | Ten users | run realistic arrival rate and think time | error rate under 1%; latency target met |
| PFC-013 | Capacity ramp | increase users until service-level breach | safe capacity limit documented |
| PFC-014 | Spike | jump from idle to expected peak | no crash or uncontrolled queue |
| PFC-015 | Soak | run expected traffic for at least eight hours | no leak or latency drift |
| PFC-016 | Large input | test approved maximum input | budget and latency target met |
| PFC-017 | Large context | test maximum retrieved context | safe refusal or bounded response |
| PFC-018 | Provider timeout | delay provider beyond timeout | request ends within application deadline |
| PFC-019 | Provider rate limit | force 429 response | bounded backoff and retry budget |
| PFC-020 | Provider outage | fail 100% of calls | fast controlled failure; no retry storm |
| PFC-021 | Cache value | compare latency and cost with cache on/off using same gold set | benefit measured without accuracy loss |
| PFC-022 | Top-k trade-off | compare k=1, 3, 5, 10, and 20 | cheapest setting meeting recall and grounding gates |
| PFC-023 | Model trade-off | compare approved models on frozen set | Pareto table for quality, latency, and cost |
| PFC-024 | Prompt trade-off | compare prompt/context lengths on frozen set | minimum tokens meeting all hard gates |
| PFC-025 | Embedding trade-off | compare model size, build time, index size, and recall | minimum total cost meeting retrieval gates |
| PFC-026 | Rebuild cost | measure full and one-Award rebuild time, CPU, memory, disk, and operator time | incremental process justified |
| PFC-027 | Cost per request | calculate provider and infrastructure cost for every run row | complete measured cost |
| PFC-028 | Cost per success | divide total cost by fully grounded successful answers | reported for every candidate |
| PFC-029 | Retry cost | isolate cost caused by retries and failures | within approved percentage |
| PFC-030 | Monthly scenarios | model 100, 1k, 10k, and 100k questions with peak capacity | assumptions and totals reviewed |

## Deployment and operations cases

| ID | Scenario | Procedure | Pass condition |
|---|---|---|---|
| DOP-001 | Build from clean checkout | build candidate using only documented inputs | identical identified artifact |
| DOP-002 | Configuration validation | omit, corrupt, and add unknown settings | startup fails clearly where required |
| DOP-003 | Non-root runtime | inspect and run process identity | least-privileged user |
| DOP-004 | Read-only filesystem | run with read-only application filesystem and explicit writable paths | normal service works |
| DOP-005 | Resource limits | enforce CPU, memory, disk, process, and connection limits | controlled degradation |
| DOP-006 | Health checks | test startup, liveness, readiness, and dependency failure | truthful distinct signals |
| DOP-007 | Graceful shutdown | stop during idle and active queries | no corruption; requests handled by policy |
| DOP-008 | Rolling deployment | replace instances during traffic | no invalid mixed corpus/model state |
| DOP-009 | Blue/green switch | validate candidate then shift and reverse traffic | rollback within target |
| DOP-010 | Migration | deploy changed store/manifest schema | compatibility or safe blocked startup |
| DOP-011 | Environment parity | compare development, CI, staging, and production manifests | approved differences only |
| DOP-012 | TLS and headers | scan public endpoint | approved TLS, transport, and security headers |
| DOP-013 | Network egress | attempt unapproved destinations | denied and logged |
| DOP-014 | Secret rotation | rotate provider key while service runs | no prolonged outage or old-key use |
| DOP-015 | Monitoring | trigger success, latency, error, rate-limit, cost, and integrity events | correct metrics and alerts |
| DOP-016 | Alert routing | trigger critical alert in test channel | acknowledged within policy |
| DOP-017 | Log correlation | trace one request across UI, route, retrieval, and provider | correlation without personal data leakage |
| DOP-018 | Backup restore | restore configuration and artifacts into clean environment | integrity and smoke tests pass |
| DOP-019 | Disaster recovery | simulate loss of serving environment | recovery time and recovery point targets met |
| DOP-020 | Incident rollback | simulate unsupported high-impact answer after release | traffic stopped, evidence retained, prior version restored |

## Cost approval table

Complete this table with measured values. Estimates must be labelled.

| Candidate | Grounding | Correctness | p95 | Cost/success | Peak RAM | Store size | Eligible |
|---|---:|---:|---:|---:|---:|---:|---|
| Current | not proven | not proven | not run | unknown | not run | 32.1 MiB index plus docstore | no |
| Candidate A |  |  |  |  |  |  |  |
| Candidate B |  |  |  |  |  |  |  |

## Current status

| Group | Defined cases | Status |
|---|---:|---|
| UI | 20 | not run |
| Accessibility | 15 | not run |
| Security and privacy | 30 | source review only |
| Performance, capacity, and cost | 30 | isolated import timing only |
| Deployment and operations | 20 | not run |
| Total | 115 | incomplete |

The first four test-case documents define 365 cases. The prompt-assurance document adds 120, for 485 total. Parameterized Award, NES, repetition, browser, platform, model, injection, and load cases raise the minimum execution count well above 1,000.
