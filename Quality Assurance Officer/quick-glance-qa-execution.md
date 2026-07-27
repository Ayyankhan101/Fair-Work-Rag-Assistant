# Quick glance: QA execution

## Stop rule

If a lower-cost upstream gate fails, do not run dependent expensive tests.

## Order

1. Freeze candidate and record environment.
2. Approve requirements and official scope.
3. Accept 122 Award sources and NES with hashes.
4. Test parsing, metadata, duplication, and deterministic rebuild.
5. Test index integrity and rollback.
6. Test routing and ambiguity.
7. Test retrieval without an LLM.
8. Test prompt, claims, citations, and legal safety.
9. Test UI and WCAG 2.2.
10. Test security, privacy, and prompt injection.
11. Test load, provider failure, cost, deployment, and recovery.
12. Review defects and issue release decision.

## Evidence rule

Every result names:

- commit;
- corpus;
- index;
- prompt;
- model;
- environment;
- input;
- output;
- reviewer;
- time;
- tokens, latency, and cost.

## Current position

Candidate, requirements, dependency, and source gates fail. QA is four commits behind `develop`. Out-of-sequence diagnostics found development-ingestion loss, 36 workflow-security findings, weak semantic Award recall, no clarification gate, weak historical claim support, and multi-second provider-free HTTP latency. These diagnostics do not count as completed formal phases because their entry conditions failed.

Full procedure: `phase-by-phase-execution-plan.md`, `qa-runbook.md`, and `unbiased-evaluation-system.md`.
