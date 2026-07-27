# Phase 3 source-corpus report

## Decision

Phase 3 does not pass.

The current Fair Work Ombudsman Award pages are reachable and internally identifiable. The repository still lacks the raw 122-Award source set, per-source checksums, a controlled NES source, and a signed manifest. A live web response cannot substitute for a reproducible release corpus.

## Scope

The authoritative Award scope is the 122 links on the Fair Work Ombudsman [A–Z Award list](https://www.fairwork.gov.au/employment-conditions/awards/list-of-awards).

The authoritative NES scope is the Fair Work Ombudsman [National Employment Standards page](https://www.fairwork.gov.au/employment-conditions/national-employment-standards).

The Award ID list used by this run is preserved in `evidence/official-award-scope-2026-07-27.json`.

## Live Award-page check

Run date: 27 July 2026.

Request pattern:

```text
https://awards.fairwork.gov.au/{AWARD_ID}.html
```

The 122 requests used six concurrent workers.

| Measure | Result |
|---|---:|
| Official IDs requested | 122 |
| Unique IDs requested | 122 |
| HTTP 200 responses | 122 |
| `text/html` responses | 122 |
| Expected Award ID present in body | 122 |
| Non-empty Award title heading | 122 |
| Consolidation statement present | 122 |
| Unicode replacement characters detected | 0 |
| Total response bytes | 179,885,839 |
| Smallest response | 849,065 bytes |
| Largest response | 3,250,100 bytes |
| Elapsed time | 236.300 seconds |
| Retries | 0 |

The total transfer was approximately 171.55 MiB. This is material for refresh time, CI use, egress, and rate-control design.

## Consolidation dates

The text extractor observed:

| Extracted statement | Pages |
|---|---:|
| 1 July 2026 | 105 |
| `1 July 202 6` | 15 |
| 14 July 2026 | 1 |
| 29 June 2026 | 1 |

The spaced `202 6` form is treated as an extraction artifact pending raw-DOM inspection. It must not be normalized silently in a release manifest.

Different consolidation dates are not automatically defects. The manifest must preserve the date displayed by each Award page, and a reviewer must decide whether every page is current for the intended release date.

## Critical identity samples

Independent page inspection confirmed:

| ID | Current page title |
|---|---|
| MA000002 | Clerks—Private Sector Award 2020 |
| MA000018 | Aged Care Award 2010 |
| MA000095 | Car Parking Award 2020 |
| MA000121 | State Government Agencies Administration Award 2020 |

The title printed on an Award page may differ from a shortened A–Z display label. The source policy must keep the Award ID, A–Z label, canonical page title, URL, and consolidation date as separate fields.

The current persisted store fails this identity check:

- MA000095 is absent.
- MA000121 is absent.
- MA000002 is labelled `Workplace Relations Act 1996`.

## Test-oracle correction

The first live-check parser expected the Award ID inside the Award title heading. That assumption was wrong. The official page presents the ID separately from the title.

Consequences:

- the first parser labelled all 122 pages as failures;
- those labels are invalid and are not product defects;
- body-ID, title-presence, response, content-type, consolidation, and encoding results remain valid;
- title-to-ID acceptance needs a corrected parser plus retained raw evidence.

This is a QA-process defect. It is disclosed to prevent a false claim that the authoritative website failed 122 checks.

## NES check

The current NES page was shown as last updated on 11 May 2026 during this review. It includes subjects absent from the supplied requirements, including casual employment, family and domestic violence leave, superannuation contributions, and the Casual Employment Information Statement.

The local `data/nes/nes_combined.txt` is not acceptable release source evidence because it contains navigation text, translation and footer material, and mojibake. It also lacks a source URL, acquisition time, effective date, and checksum beside the content.

## Acquisition and reproducibility findings

The source acquisition design has no demonstrated:

- conditional request support using `ETag` or `Last-Modified`;
- bounded retry and backoff policy;
- rate-limit response;
- resumable download manifest;
- temporary-file and atomic-publish procedure;
- response size limit;
- content-type rejection;
- redirect policy;
- TLS and hostname evidence;
- per-source SHA-256;
- HTML snapshot or PDF retention;
- page parser revision;
- change report between corpus versions;
- rollback to the previously accepted corpus.

Fetching every page on every run is slow and wasteful. Reusing unverified responses is unsafe. The required design is a versioned acquisition cache keyed by URL and response validator, with checksums, immutable manifests, and a human-reviewed change report.

## Required acceptance evidence

Phase 3 can pass only when one immutable directory contains:

1. Exactly one accepted raw source for each of the 122 official Award IDs.
2. The accepted current NES source.
3. A manifest with ID, labels, canonical title, URL, retrieval time, consolidation or update date, content type, byte count, SHA-256, parser revision, and review status.
4. A comparison against the official A–Z list showing no missing or unapproved extra IDs.
5. A legal-source review of titles, dates, tables, schedules, first clauses, and final clauses.
6. A reproducible downloader log and a second-run no-change result.
7. Named approval of any source whose date differs from the release date.

## Evidence limitation

The live run retained aggregate results but did not retain the 122 raw responses or a per-page hash table. Its aggregate reconstruction is in `evidence/official-award-live-check-2026-07-27.json`.

The run proves reachability on the run date. It does not prove that the repository corpus is complete, current, untampered, or reproducible.
