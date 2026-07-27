---
name: human-docs
description: Write and edit documentation (specs, runbooks, README, QA plans, reports) without common LLM writing tells. Based on Wikipedia:Signs of AI writing. Use when creating or revising any markdown documentation, design docs, test matrices, or project prose in this repo.
---

# Human documentation (no AI tells)

Source: [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Patterns below are adapted for **technical QA docs**, not encyclopedia articles.

## When to use

- Writing or editing files under `docs/`, `qa/`, README, spec, runbook, test matrix, or QA report
- Reviewing documentation before commit or handoff
- Rewriting agent-generated prose the user flagged as "AI-sounding"

## Core rule

Write like a senior engineer leaving notes for the next person on the team: short sentences, concrete nouns, numbers, file paths, pass/fail criteria. If a sentence adds no fact, cut it.

## Before writing

1. List what the reader must know when they finish (facts, commands, thresholds).
2. Gather evidence from the repo (paths, counts, test IDs) before drafting.
3. Pick one term per concept and keep it (e.g. "award PDF", not "document asset").

## Style (do)

| Do | Example |
|----|---------|
| Sentence-case headings | `## Phase 0 data checks` |
| Lead with the decision or fact | `129 PDFs must exist in data/awards/.` |
| Use tables for test matrices | columns: ID, check, pass criteria, script |
| Name files and functions | `scripts/eval_hard.py` returns exit 1 below 95% |
| State thresholds as numbers | `content pass ≥ 70% per question` |
| Use active voice, short paragraphs | 2–4 sentences max |
| Separate facts from open questions | `Open: Groq daily limit blocks full 129-run.` |

## Style (avoid)

Full banned-pattern list: [reference.md](reference.md).

**Content**
- Padding about "significance", "landscape", "broader impact", or why the work matters
- Opening with "In today's…", "This document serves to…", "It is worth noting…"
- Closing with "In conclusion", "To summarize", or calls to action ("Let me know if…")
- Vague authority: "experts say", "industry best practice" without a named source
- Hedging stacks: "may potentially", "could arguably", "it's important to note that"
- `-ing` tail phrases that add no data: "…highlighting the need for robust testing"
- Negative parallelisms: "Not just X, but Y", "It's not X—it's Y"
- Rule-of-three fluff: three adjectives or three parallel phrases where one fact suffices

**Vocabulary** (use plain alternatives)

| Avoid | Use instead |
|-------|-------------|
| delve / dive into | read, inspect, grep |
| robust | stable, passes under load |
| comprehensive | full, covers all 129 awards |
| crucial / pivotal / vital | required, blocks merge |
| leverage | use |
| utilize | use |
| facilitate | run, enable |
| underscore / highlight (metaphor) | show, record, fail if |
| landscape | stack, pipeline, list of awards |
| testament | (delete) |
| showcase | display, print |
| foster / cultivate | (delete or name the mechanism) |
| Additionally (sentence opener) | Also, or merge sentences |
| super / deeply / truly | (delete) |

**Formatting**
- Bold on every other phrase
- Emoji in formal specs (unless the user asked)
- Title Case On Every Heading Word
- Nested bullet forests where a table or numbered list is clearer
- Mermaid or ASCII diagrams unless they clarify control flow (OK for architecture, not decoration)
- Horizontal rules between every section

## Document templates

### Spec section

```markdown
## Ingest slug mapping

Problem: MA000006.pdf was mapped to Hospitality; correct name is Higher Education Academic Staff.

Check B-003 compares AWARD_URL_MAP in src/ingest.py to data/award_audit.json.
Pass: zero mismatches. Fail: list each PDF, expected name, actual name.

Owner: qa/scripts/audit_all_awards.py
```

### Test case row (prefer table, not prose)

| ID | Component | Command | Pass |
|----|-----------|---------|------|
| D-004 | vectorstore | `python qa/scripts/check_retrieval.py --award "Cleaning Services Award 2020"` | top-3 chunks same award |

### Runbook step

```markdown
1. Activate venv from repo root.
2. Run `python qa/scripts/run_all_qa.py --tier 0-2`.
3. If B-003 fails, open data/award_audit.json and fix src/ingest.py AWARD_URL_MAP; rebuild store.
```

## Self-review (run before finishing)

Read the draft once for **substance**, once for **tells**:

- [ ] Every heading is sentence case
- [ ] No word from the "Avoid" vocabulary table unless quoted from code
- [ ] No paragraph exists only to praise the project or the plan
- [ ] Each test ID links to a command or script path
- [ ] Numbers match the repo (re-run counts if unsure)
- [ ] No "Not only… but also…" or "It's not X, it's Y"
- [ ] Lists are not all exactly three items
- [ ] Bold used at most for UI labels or literal keywords in grep patterns
- [ ] First paragraph states scope in one or two sentences
- [ ] Last paragraph is facts or next action, not a sales pitch

## Good vs bad (QA context)

**Bad**

> This comprehensive QA framework leverages a robust, multi-tiered approach to delve deep into every facet of the RAG pipeline, ensuring unparalleled quality across the evolving Fair Work landscape. It's not just about testing—it's about building trust.

**Good**

> QA covers fair-work-rag-assistant only: 129 award PDFs, NES text, ingest, vectorstore, router, retrieval, and Groq answers. Tier 0–2 runs without an API key; tier 4+ needs GROQ_API_KEY and counts against the daily token limit.

**Bad**

> **Phase 0** establishes the **critical foundation** for **data integrity**, **highlighting** the **pivotal role** of accurate slug mapping.

**Good**

> Phase 0 checks data before any LLM call: PDF count, award_audit.json, chunk metadata, NES file size.

## Fixing existing AI-ish docs

1. Delete the intro and conclusion; keep middle facts.
2. Convert prose bullets to tables where there are repeated fields.
3. Replace buzzwords using the table above.
4. Split any sentence over 30 words.
5. Re-run self-review checklist.

## Further reading

- [reference.md](reference.md) — full pattern list from Wikipedia guide
- Wikipedia: [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
