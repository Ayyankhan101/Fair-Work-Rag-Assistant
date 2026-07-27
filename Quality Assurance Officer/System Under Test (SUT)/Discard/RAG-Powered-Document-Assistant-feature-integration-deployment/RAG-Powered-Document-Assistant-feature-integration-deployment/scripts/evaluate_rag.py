#!/usr/bin/env python3
"""Evaluate the retrieval + answer chain using the provided 10-pair QA set."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from rag_chain import answer_question, load_vector_store

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
EVAL_PATH = DATA_DIR / "eval_qa.json"
REPORT_PATH = DATA_DIR / "rag_eval_report.json"


def normalize_text(text: str) -> list[str]:
    return re.findall(r"\b\w+\b", text.lower())


def token_f1(prediction: str, reference: str) -> float:
    pred_tokens = normalize_text(prediction)
    ref_tokens = normalize_text(reference)
    if not pred_tokens or not ref_tokens:
        return 0.0
    common = Counter(pred_tokens) & Counter(ref_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0.0
    precision = num_same / len(pred_tokens)
    recall = num_same / len(ref_tokens)
    return 2 * precision * recall / (precision + recall)


def extract_sources_from_answer(answer: str) -> list[str]:
    match = re.search(r"Sources:\s*(.+)", answer, re.IGNORECASE | re.DOTALL)
    if not match:
        return []
    raw = match.group(1)
    items = [item.strip().strip("[]()") for item in raw.split(",")]
    return [item for item in items if item]


def evaluate(top_k: int = 5) -> dict:
    vector_store = load_vector_store()
    eval_rows = json.loads(EVAL_PATH.read_text())

    retrieval_hits = []
    answer_f1_scores = []
    citation_precisions = []
    hallucination_counts = []

    for row in eval_rows:
        result = answer_question(row["question"], vector_store, top_k=top_k)
        retrieved_sources = {chunk["metadata"].get("source") for chunk in result["retrieved_chunks"] if chunk["metadata"].get("source")}
        gold_sources = set(row.get("sources", []))

        retrieval_hit = 1.0 if gold_sources & retrieved_sources else 0.0
        retrieval_hits.append(retrieval_hit)

        answer = result["answer"]
        answer_sources = extract_sources_from_answer(answer)
        answer_source_set = set(answer_sources)
        citation_precision = len(answer_source_set & retrieved_sources) / max(1, len(answer_source_set))
        citation_precisions.append(citation_precision)

        hallucination_count = len(answer_source_set - retrieved_sources)
        hallucination_counts.append(hallucination_count)

        answer_f1_scores.append(token_f1(answer, row["answer"]))

    metrics = {
        "top_k": top_k,
        "num_questions": len(eval_rows),
        "retrieval_hit_rate": sum(retrieval_hits) / len(retrieval_hits),
        "answer_f1_mean": sum(answer_f1_scores) / len(answer_f1_scores),
        "citation_precision_mean": sum(citation_precisions) / len(citation_precisions),
        "hallucination_rate": sum(hallucination_counts) / len(hallucination_counts),
    }

    REPORT_PATH.write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    evaluate()
