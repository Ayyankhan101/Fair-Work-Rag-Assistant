# Prompt assurance report

## Decision

The current prompt system does not pass release assurance.

The highest-risk problem is architectural: the application has no actual system message. It sends the application rules, retrieved source text, and end-user question together as one human-role message.

The prompt wording has also been tuned historically to maximize answer and format completion. That incentive conflicts with legal-source safety.

## Prompt inventory

| Item | Location | Status |
|---|---|---|
| committed answer prompt | `HEAD:src/rag.py` | active in HEAD |
| modified working-tree prompt | `src/rag.py:18` | unaccepted pre-boundary change |
| prompt construction | `src/rag.py:142` | one `from_template` call |
| fallback prompt | `src/rag.py:213` and `src/rag.py:221` | same template, smaller model |
| retrieved-document formatter | `src/rag.py:81` | metadata and text merged into prompt |
| NES formatter | `src/rag.py:105` | cache text merged into prompt |
| prompt version identifier | none | absent |
| structured output schema | none | absent |
| post-generation claim validator | none | absent |

No other production LLM prompt was found under `src/`.

## Verified message role

The following isolated check was run with `langchain-core`:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("Hello {x}")
message = prompt.format_messages(x="world")[0]
print(type(message).__name__)
print(message.type)
```

Observed:

```text
HumanMessage
human
```

The current `ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)` therefore does not create a system message.

This conflicts with both current OpenAI [prompt-engineering guidance](https://developers.openai.com/api/docs/guides/prompt-engineering), which places application rules ahead of user input through higher-priority messages, and Groq’s [prompting guidance](https://console.groq.com/docs/prompting), which recommends separate system, user, and assistant roles.

## Committed prompt risk

The committed prompt contains these instructions:

```text
NEVER say "not specified" ... ALWAYS provide the best answer from the context.
```

```text
If you find a number in the context, STATE IT CONFIDENTLY.
```

```text
When the question asks "what is X", you MUST provide a specific answer with a number.
```

Those instructions can convert incomplete or irrelevant retrieval into confident misinformation. The historical examples also contain exact legal-looking values, which can be copied even when they do not apply.

The dirty working-tree prompt removed the three most dangerous instructions and added insufficient-evidence and injection wording. Those are sensible proposals, but they are not accepted code and do not fix the missing system-role boundary.

## Findings

| ID | Severity | Finding | Consequence | Required correction |
|---|---|---|---|---|
| PRF-001 | S1 | no system-role message exists | user and source text compete at the same instruction level | create separate system and user messages |
| PRF-002 | S1 | committed prompt requires an answer when support is absent | confident hallucination is rewarded | allow and test insufficient-evidence status |
| PRF-003 | S1 | committed prompt requires confident numbers | unrelated values can become legal-looking facts | require complete rate identity and support |
| PRF-004 | S1 | prompt asks general questions to compare multiple Awards | arbitrary retrieved Awards may be presented as general law | clarify scope or explain variation without arbitrary examples |
| PRF-005 | S1 | no effective-date contract exists | stale and current provisions can be mixed | require question date and source effective date |
| PRF-006 | S1 | no atomic claim-to-source output exists | one citation can appear to support several unsupported claims | cite every claim separately |
| PRF-007 | S1 | question and evidence are only labelled by plain text | boundaries are weak and injection is easier | use role separation and structured delimiters |
| PRF-008 | S1 | retrieved instructions are rejected only by a sentence inside the same human message | indirect prompt injection control is weak | system-level data-only rule plus adversarial tests and validation |
| PRF-009 | S1 | “scan ALL context documents” is false in operation | the formatter stops at 4,000 characters and truncates each document at 800 | report context incompleteness and never claim exhaustive review |
| PRF-010 | S1 | truncated text is passed without a completeness flag | qualifications after truncation may be omitted | mark truncation and retrieve parent clauses |
| PRF-011 | S1 | no source-conflict status exists | contradictory evidence may be synthesized into a false rule | detect conflict and stop |
| PRF-012 | S1 | ambiguity cannot produce a machine-readable clarification state | the model may answer while merely noting missing facts | add explicit `needs_clarification` status |
| PRF-013 | S1 | Award coverage is not constrained | naming or retrieving an Award may be treated as proof it applies | forbid definitive coverage decisions from incomplete facts |
| PRF-014 | S1 | calculation rules are absent | units, loadings, tiers, and rounding can be silently assumed | require inputs, formula, unit, date, and assumptions |
| PRF-015 | S2 | “expert on Australian employment law” overstates the product | users may infer professional legal judgment | identify it as a source-grounded information assistant |
| PRF-016 | S2 | fixed Note choices are not tied to answer status | disclaimers can be irrelevant or contradictory | derive limitations from structured status |
| PRF-017 | S2 | response is free-form Markdown | format checks do not prove field validity | use strict schema where supported |
| PRF-018 | S2 | output has one shared Award and clause field | mixed claims lose traceability | use a citation array on each claim |
| PRF-019 | S2 | no distinction exists between trusted manifest metadata and source body | a poisoned title or URL can be repeated | validate metadata outside the model |
| PRF-020 | S2 | no policy exists for Award/NES interaction | the model may imply one source overrides another | present supported provisions and flag interpretation |
| PRF-021 | S2 | exact numeric examples appear in instructions | examples can anchor unrelated responses and become stale | use schema-only examples or verified fixtures |
| PRF-022 | S2 | prompt and examples are not versioned | evaluation cannot identify behavior | add immutable prompt ID and hash |
| PRF-023 | S2 | primary and fallback models receive the same untested wording | fallback behavior may differ silently | qualify every model/prompt pair |
| PRF-024 | S2 | 1,024 output tokens can cut the mandatory format | partial output may pass weak checks or omit limitations | validate completion and schema |
| PRF-025 | S2 | no instruction covers empty, missing, duplicate, or mismatched source IDs | malformed context may be treated as valid | fail closed on evidence-integrity flags |
| PRF-026 | S2 | no rule prevents unsupported external knowledge | “ONLY context” is present but not operationally checked | verify every factual claim after generation |
| PRF-027 | S2 | no privacy reminder or personal-data boundary exists in the model exchange | users may disclose sensitive employment facts | control input before provider transmission |
| PRF-028 | S3 | mojibake appears in separators and Note text | output quality and exact-format tests are unstable | use controlled UTF-8 text |
| PRF-029 | S3 | uppercase imperatives and repeated rules add length without a formal priority order | collisions are harder to reason about | use concise ordered rules with explicit precedence |
| PRF-030 | S3 | “good answer” examples were treated as general truth | examples can outlive their source date | keep examples in versioned tests, not permanent legal facts |

## Instruction conflicts

### Answer completeness versus evidence

The committed prompt prioritizes producing a number over admitting missing evidence. That is unacceptable for pay and entitlement questions.

The correct priority is:

1. evidence integrity;
2. correct scope and date;
3. clarification;
4. claim support;
5. answer completeness;
6. style and format.

### Specific Award versus coverage

“Prioritize that Award” is unsafe when the user merely guesses an Award. The assistant must distinguish:

- the user asks what an identified Award says;
- the user asks whether that Award covers them;
- the user assumes coverage without enough facts.

Only the first can normally be answered from an Award clause alone.

### General comparison versus useful answer

Comparing a few retrieved Awards does not answer a general legal question. It can mislead users into thinking the examples are exhaustive or representative.

For a broad question, ask for the Award or relevant employment facts. If a comparison is explicitly requested, name the limited comparison set and avoid a general conclusion.

### Exact value versus missing table context

A rate is not identified by a dollar sign alone. The prompt must require Award ID, classification, employment type, rate type, unit, operative date, table, and qualifications.

If any required field is missing, the result is insufficient evidence or a clarification request.

## What prompt engineering cannot fix

A strong prompt cannot:

- supply the two missing Award IDs;
- repair the MA000002 label;
- reconstruct text after the 800-character truncation;
- know a missing table heading or footnote;
- validate a source URL;
- determine Award coverage without material facts;
- make stale NES text current;
- guarantee resistance to prompt injection;
- prove a claim is supported;
- preserve continuity after the configured models shut down.

These require source, retrieval, application, validation, and operational controls.

## Required implementation pattern

The future implementation should use:

1. a system message containing stable policy;
2. a user message containing structured task inputs;
3. evidence enclosed in explicit document boundaries;
4. trusted manifest metadata supplied separately from source body;
5. a strict output schema;
6. deterministic validation;
7. a claim-level verifier;
8. a human-readable renderer;
9. a prompt version and hash in every trace.

The proposed wording is in `proposed-system-and-user-prompt.md`.

## Assurance rule

No prompt is “super specific” merely because it is long.

It passes only if the 120 prompt-assurance specifications in `test-cases-05-prompt-assurance.md` pass across the primary and fallback candidates, with the claim and citation gates in `unbiased-evaluation-system.md`.
