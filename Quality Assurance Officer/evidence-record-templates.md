# Evidence record templates

Copy these templates for each run. Do not overwrite an earlier run.

## Run header

```text
Run ID:
Run type:
Start time UTC:
End time UTC:
Tester:
Reviewer:

Repository:
Branch:
Commit SHA:
Dirty worktree: yes/no
Operating system:
Python:
Dependency lock SHA-256:

Corpus manifest ID:
Corpus manifest SHA-256:
Vector-store manifest ID:
Vector-store SHA-256:
CAG bundle ID and SHA-256:

Embedding model and revision:
LLM provider:
LLM model:
Prompt version or SHA-256:
Retriever configuration:
Application configuration:

Environment:
CPU:
Memory:
Disk:
Region:
Browser and viewport:

Purpose:
Included cases:
Excluded cases and reason:
Known limitations:
```

## Test execution record

```text
Test ID:
Run ID:
Requirement IDs:
Risk:
Severity if failed:

Preconditions:
1.
2.

Test data:
- ID:
- source:
- checksum:

Steps:
1.
2.
3.

Expected result:

Actual result:

Status: passed/failed/blocked/not run/invalid

Raw evidence:
- command:
- exit code:
- log:
- screenshot:
- result row:

Observed facts:

Inference, if any:

Limitations:

Defect ID:
Executed by:
Reviewed by:
Review date:
```

## Defect record

```text
Defect ID:
Title:
Severity: S0/S1/S2/S3
Status:
Owner:
Found in commit:
Found in artifact:
Found by test:

Requirement affected:
User or business impact:
Safety, legal, privacy, cost, or operational impact:

Preconditions:

Reproduction:
1.
2.
3.

Expected:

Actual:

Reproduction rate:
First observed:
Last reproduced:
Environments:

Raw evidence:

Suspected component:
Root cause: unknown until confirmed

Recommended correction:

Required verification:

Regression scope:

Risk acceptance, if proposed:
- approver:
- reason:
- scope:
- expiry:
- monitoring:
```

## Claim review record

Use one row per factual answer claim.

| Field | Value |
|---|---|
| Run ID |  |
| Question ID |  |
| Answer ID |  |
| Claim number |  |
| Claim text |  |
| Claim type | Award/NES/rate/hours/break/leave/coverage/classification/termination/other |
| High impact | yes/no |
| Source ID |  |
| Award ID or NES section |  |
| Clause/section/page |  |
| Effective date |  |
| Supporting text |  |
| Supporting text SHA-256 |  |
| Support result | full/partial/none/conflict |
| Required qualifier present | yes/no/not applicable |
| Citation present | yes/no |
| Citation resolves | yes/no |
| Reviewer |  |
| Review date |  |
| Notes |  |

An answer fails grounding if any factual claim has partial, absent, or conflicting support.

## Retrieval result row

```json
{
  "run_id": "",
  "question_id": "",
  "query": "",
  "expected_route": "",
  "actual_route": "",
  "target_source_ids": [],
  "target_clause_ids": [],
  "k": 5,
  "filters": {},
  "results": [
    {
      "rank": 1,
      "chunk_id": "",
      "source_id": "",
      "award_id": "",
      "clause": "",
      "score": null,
      "text_sha256": ""
    }
  ],
  "latency_ms": 0,
  "passed": false,
  "reviewer": "",
  "reviewed_at_utc": ""
}
```

## Answer result row

```json
{
  "run_id": "",
  "question_id": "",
  "question": "",
  "route": "",
  "retrieved_chunk_ids": [],
  "answer": "",
  "citations": [],
  "input_tokens": 0,
  "cached_input_tokens": 0,
  "output_tokens": 0,
  "provider_request_id": "",
  "provider_latency_ms": 0,
  "total_latency_ms": 0,
  "retry_count": 0,
  "estimated_provider_cost": 0,
  "currency": "",
  "grounding_passed": false,
  "citation_passed": false,
  "correctness_passed": false,
  "safety_passed": false,
  "reviewer": "",
  "reviewed_at_utc": ""
}
```

## Performance and cost record

```text
Run ID:
Candidate:
Route:
Load pattern:
Users:
Requests:
Duration:
Warm or cold:

Successes:
Grounded successes:
Failures by type:
Retries:

Latency p50:
Latency p95:
Latency p99:
Latency maximum:
Retrieval p95:
Provider p95:

CPU mean/maximum:
Memory mean/maximum:
Disk read/write:
Network ingress/egress:
Store bytes:
Image bytes:
Cold-start seconds:

Input tokens:
Cached input tokens:
Output tokens:
Embedding calls:
Provider charge:
Infrastructure charge:
Storage charge:
Monitoring charge:
Operator time and rate:
Total cost:
Cost per request:
Cost per successful grounded answer:

Accuracy and safety gates met: yes/no
Eligible for cost comparison: yes/no
```

## Phase exit record

```text
Phase:
Candidate:
Entry criteria met: yes/no
Cases planned:
Cases passed:
Cases failed:
Cases blocked:
Cases not run:
Invalid runs:

Open S0:
Open S1:
Open S2:
Open S3:

Exit criteria:
1.
2.

Evidence:

Limitations:

Decision: pass/fail/blocked
QA officer:
Engineering owner:
Product owner:
Security/privacy reviewer:
Legal-source reviewer:
Decision date:
```

