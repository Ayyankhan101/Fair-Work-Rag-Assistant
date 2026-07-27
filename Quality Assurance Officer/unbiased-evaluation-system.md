# Unbiased evaluation system

## Purpose

This system measures the application, not the persuasiveness of its answers and not the reputation of a model provider.

It separates source quality, retrieval, generation, citation, safety, latency, and cost. A single percentage cannot replace these measures.

## Non-negotiable controls

- Freeze the commit, corpus, index, prompts, configuration, model revision, and evaluation data before a run.
- Pre-register the primary metrics, thresholds, exclusions, and statistical tests.
- Keep a hidden test set unavailable to prompt, retrieval, and model tuning.
- Do not let a model score its own answers for release.
- Blind human reviewers to provider, model, prompt, and system labels.
- Preserve every prompt, retrieved passage, output, score, override, and cost.
- Report failures and excluded cases, not only averages.
- Do not change gold answers after seeing a candidate output without an independent change record.
- Treat synthetic questions as test leads until a human verifies them.
- Use model graders for triage only until their agreement with human reviewers is demonstrated.

## Evaluation layers

| Layer | Unit | Primary measures |
|---|---|---|
| Source | official document | completeness, identity, date, checksum |
| Parsing | clause, table, footnote | structural preservation, metadata completeness |
| Routing | labelled question | accuracy, ambiguity handling, display-path agreement |
| Retrieval | question and gold clauses | recall at k, precision at k, reciprocal rank, contamination |
| Context | final evidence set | gold coverage, noise, duplicates, position |
| Answer | atomic claim | correctness, support, completeness |
| Citation | claim-source pair | source validity, clause validity, entailment |
| Safety | scenario | refusal, clarification, escalation, injection resistance |
| Operation | request and run | latency, errors, tokens, cost, recovery |
| Fairness | matched scenario pairs | performance gaps and inconsistent treatment |

## Test-set design

### Corpus coverage set

For every one of the 122 Awards, include at least:

1. identity and coverage retrieval;
2. one high-impact entitlement or rate clause;
3. one exclusion, qualification, schedule, or no-answer case.

This gives at least 366 Award cases before paraphrases and dates.

### NES set

Cover every current NES subject, interaction with Awards, exceptions, eligibility conditions, and information statements. Include questions that should retrieve only a narrow NES section.

### Risk set

Stratify by:

- minimum and Award rates;
- classifications;
- ordinary hours;
- overtime;
- penalties;
- allowances;
- breaks;
- leave;
- notice;
- redundancy;
- casual employment;
- juniors and apprentices;
- public holidays;
- Award coverage and exclusions;
- effective date;
- conflicts between Award and NES;
- calculations;
- missing facts;
- out-of-scope legal judgment.

### Language and accessibility set

Use plain English, misspellings, abbreviations, long narratives, short fragments, Unicode, screen-reader input, and reviewed non-English or translated cases where the product claims support.

Do not assume an English embedding benchmark proves equal service to multilingual users.

### Adversarial set

Include:

- instructions in the question to ignore the system;
- instructions embedded in source text;
- fabricated Award IDs and clauses;
- plausible but nonexistent rates;
- stale dates;
- cross-Award contamination;
- conflicting retrieved passages;
- irrelevant long context;
- duplicate passages;
- Unicode controls and delimiter attacks;
- attempts to obtain personal legal advice;
- questions for which the corpus has no answer.

### Matched-pair fairness set

Create semantically identical questions that vary only a non-material personal attribute or writing style. Any answer, confidence, refusal, or escalation difference must be explained by a legitimate legal distinction.

Employment type, age, location, and duties may be legally material in some cases. Reviewers must mark which fields are material before the answer is generated.

## Dataset partitions

Use four partitions:

| Partition | Purpose | Visibility |
|---|---|---|
| Development | prompt and pipeline diagnosis | engineering |
| Validation | candidate selection and threshold tuning | limited team |
| Hidden release | final comparison | QA custodian only |
| Post-release sentinel | production drift and new defects | operations and QA |

Group paraphrases, source clauses, and near-duplicates into the same partition. Otherwise the model or prompt can effectively see the test answer during development.

Do not publish the hidden release questions or gold support spans.

## Gold-record schema

Each test record must include:

```text
case_id
partition
risk_class
question
material_facts
missing_facts
expected_route
expected_clarification
accepted_answer_status
gold_claims[]
accepted_source_ids[]
accepted_clauses[]
support_spans[]
effective_date
forbidden_claims[]
severity_if_wrong
reviewer_ids
review_status
revision
```

For calculation cases, store the formula, inputs, units, rounding rule, effective date, and expected value separately.

## Human review

### Reviewer qualifications

Gold legal claims require a reviewer competent in Australian workplace law and current Fair Work sources. General software QA can verify structure, evidence, repeatability, security, and statistics but cannot certify legal correctness alone.

### Review process

1. Reviewer A drafts or verifies the gold claim from the official source.
2. Reviewer B independently reviews every S0/S1 case and a stratified sample of lower-risk cases.
3. Neither reviewer sees candidate identity while scoring output.
4. Disagreements go to a named adjudicator.
5. Record the original ratings, disagreement, decision, rationale, and date.
6. Reopen affected gold records when an Award or NES source changes.

Measure percent agreement and Cohen’s kappa for categorical decisions. A high percentage with low kappa can occur when one label dominates, so report both.

## Automated scoring

Use deterministic scoring wherever possible:

- exact Award ID;
- source URL and checksum;
- clause existence;
- number, currency, unit, date, percentage, and formula;
- required and forbidden fields;
- retrieved gold-chunk presence;
- context duplication;
- response schema;
- latency, tokens, and cost.

Use claim-level entailment or model grading only for semantic judgments that deterministic checks cannot resolve.

The primary [RAGChecker paper](https://arxiv.org/abs/2408.08067) argues for separate diagnostic metrics for retrieval and generation and uses claim-level checking. [RAGAS](https://aclanthology.org/2024.eacl-demo.16/) similarly separates retrieval relevance, faithfulness, and answer quality. These tools may assist diagnosis; neither replaces reviewed legal gold.

## Model-grader controls

Model graders are subject to position, verbosity, and self-preference bias. The [MT-Bench judge paper](https://proceedings.neurips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf) reports these limitations.

When a model grader is used:

1. do not use the answer model as the only grader;
2. remove provider and model names;
3. use an explicit claim-level rubric and gold support;
4. randomize answer order in pairwise comparison;
5. score both A/B and B/A order;
6. hide response length where the task permits;
7. include known pass, fail, and adversarial calibration cases;
8. measure agreement against human decisions by stratum;
9. send disagreement and high-impact cases to humans;
10. never convert grader confidence into legal certainty.

OpenAI’s current [evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices) recommends task-specific evaluations, production-like distributions, logging, continuous evaluation, and human calibration. It also warns against biased datasets, generic metrics, and subjective “vibe” evaluation.

## Repetition and randomness

Temperature zero does not guarantee identical hosted-model output.

For deterministic layers, require exact repeatability. For generation:

- run at least five repetitions for the release-critical subset;
- use a fixed seed when the provider supports it, but still repeat;
- report best, median, worst, and failure rate;
- treat any unsupported high-impact claim in any required repeat as a failure unless the risk policy explicitly says otherwise;
- record provider model revision and system fingerprint when available.

## Metrics

### Retrieval

- Award recall at 3 and 5;
- clause recall at 5 and 10;
- mean reciprocal rank;
- precision at k;
- cross-Award contamination;
- duplicate-context rate;
- no-answer retrieval precision;
- effective-date filter accuracy.

### Answers

- claim correctness;
- claim support;
- citation completeness;
- citation correctness;
- numeric and calculation accuracy;
- correct clarification;
- correct refusal or escalation;
- answer completeness;
- unsupported-claim rate.

### Operations

- p50, p95, p99, and maximum latency;
- request and retry failure rate;
- input, cached input, reasoning, and output tokens;
- provider and infrastructure cost;
- cost per passed answer;
- cost per successful grounded answer;
- memory and cold-start time.

### Fairness

Report every primary metric by Award, topic, difficulty, language form, employment type, and other approved strata. Do not hide a failed group behind an overall average.

## Statistical comparison

Compare candidates on identical cases.

- Use paired results.
- Use 10,000 paired bootstrap samples for confidence intervals on continuous or rate metrics.
- Use McNemar’s test for paired binary pass/fail changes.
- Correct multiple comparisons with Holm’s method when selecting among several candidates.
- Report effect size and confidence interval, not only a p-value.
- Predefine a non-inferiority margin for cost-saving candidates.
- Require the lower confidence bound to meet the release threshold.

A one- or two-question improvement on a 25-question set is not reliable proof of a better system.

## Bias and leakage audit

Before release, verify:

- no hidden case appears in prompts, few-shot examples, training data, or public project documents;
- no gold answer was written by copying a candidate answer;
- synthetic cases were independently sourced and reviewed;
- model names are removed from human review;
- candidate order is randomized;
- rejected runs remain in the result set;
- timeouts and refusals are not silently excluded;
- missing data is reported;
- manual overrides have named rationale;
- metrics and thresholds were fixed before the final run.

## Release thresholds

Minimum hard gates:

| Gate | Threshold |
|---|---:|
| Official Award source coverage | 122/122 |
| Required metadata | 100% |
| Award recall at 5 | 100% |
| Clause recall at 5 | at least 95% |
| High-impact numeric accuracy | 100% |
| Claim support | 100% |
| Citation correctness | 100% |
| Citation completeness | 100% |
| Missing-evidence handling | 100% |
| Prompt-injection high-impact failures | 0 |
| Reviewed overall correctness | at least 95% |
| Open S0 or S1 defects | 0 |

These are release floors, not optimization targets. Product ownership may require stricter thresholds after legal and risk review.

## Evaluation run order

1. Validate dataset schema and partition integrity.
2. Run source and parser tests.
3. Run routing tests.
4. Run retrieval without generation.
5. Stop if retrieval gates fail.
6. Run a small generation calibration set.
7. Validate human and automated grader agreement.
8. Run the full hidden set.
9. Repeat the release-critical subset.
10. Calculate paired statistics and cost.
11. Review every S0/S1 failure.
12. Publish raw results, limitations, and the disposition.

No later stage can compensate for a failed earlier evidence gate.
