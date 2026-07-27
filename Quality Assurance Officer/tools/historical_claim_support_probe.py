#!/usr/bin/env python3
"""Check whether historical answer claims occur in current retrieved context.

Exact-string support is a weak diagnostic, not legal validation. The historical
answers were not generated in this run, and occurrence in context does not
prove that a claim is applicable, current, calculated correctly, or cited well.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(SRC))

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from offline_request_matrix import extract_context, extract_source_awards

import rag
from cag import CAGCache
from vectorstore import load_vectorstore

MONEY_RE = re.compile(r"(?<!\w)\$\d[\d,]*(?:\.\d+)?")
PERCENT_RE = re.compile(r"\b\d+(?:\.\d+)?%")
DURATION_RE = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:minutes?|hours?|days?|weeks?|months?|years?)\b",
    re.IGNORECASE,
)
CITATION_RE = re.compile(
    r"\b(?:clause|section|table|part)\s+[A-Z]?\d+(?:\.\d+)*(?:\([a-z0-9]+\))*"
    r"|\bschedule\s+[A-Z0-9]+",
    re.IGNORECASE,
)


def field(answer: str, name: str) -> str:
    """Extract one bold-labelled response field."""
    match = re.search(
        rf"\*\*{re.escape(name)}:\*\*\s*(.*?)(?=\n\s*\n?\*\*|\Z)",
        answer,
        re.DOTALL | re.IGNORECASE,
    )
    return match.group(1).strip() if match else ""


def unique_matches(pattern: re.Pattern[str], text: str) -> list[str]:
    """Return distinct matches in first-seen order."""
    values = []
    for match in pattern.finditer(text):
        value = match.group(0)
        if value not in values:
            values.append(value)
    return values


def normalize(text: str) -> str:
    """Normalize for conservative exact-claim occurrence checks."""
    return re.sub(r"\s+", " ", text.casefold().replace(",", "")).strip()


def claim_results(claims: list[str], context: str) -> list[dict[str, Any]]:
    """Check normalized literal occurrence of each claim."""
    normalized_context = normalize(context)
    return [
        {
            "claim": claim,
            "found": normalize(claim) in normalized_context,
        }
        for claim in claims
    ]


def run_probe() -> dict[str, Any]:
    """Retrieve current context and compare it with historical answer claims."""
    historical_path = ROOT / "data" / "hard_eval_results.json"
    historical = json.loads(historical_path.read_text(encoding="utf-8"))
    entries = historical.get("results", [])

    capture: list[str] = []

    def fake_llm(prompt_value: Any) -> AIMessage:
        messages = prompt_value.to_messages()
        capture.append(messages[0].content if messages else "")
        return AIMessage(content="QA_CAPTURE_ONLY_NO_MODEL_ANSWER")

    original_get_llm = rag.get_llm
    rag.get_llm = lambda fallback=False: RunnableLambda(fake_llm)
    started = time.perf_counter()
    try:
        store = load_vectorstore(str(ROOT / "data" / "vectorstore"))
        cag = CAGCache(str(ROOT / "data" / "nes" / "nes_combined.txt"))
        chain = rag.create_rag_chain(
            store,
            cag_cache=cag,
            docstore_path=str(ROOT / "data" / "vectorstore" / "docstore.json"),
        )

        results = []
        for entry in entries:
            question = entry.get("question", "")
            answer = entry.get("answer", "")
            before = len(capture)
            error = None
            try:
                chain.invoke(question)
            except Exception as exc:  # noqa: BLE001 - evidence records all failures
                error = f"{type(exc).__name__}: {exc}"
            prompt_text = capture[-1] if len(capture) > before else ""
            context = extract_context(prompt_text)
            context_awards = extract_source_awards(context)

            answer_field = field(answer, "Answer")
            reference_field = field(answer, "Award/NES Reference")
            citation_field = field(answer, "Clause/Section")
            numeric_claims = []
            for pattern in (MONEY_RE, PERCENT_RE, DURATION_RE):
                for value in unique_matches(pattern, answer_field):
                    if value not in numeric_claims:
                        numeric_claims.append(value)
            citation_claims = unique_matches(CITATION_RE, citation_field)

            numeric_checks = claim_results(numeric_claims, context)
            citation_checks = claim_results(citation_claims, context)
            normalized_reference = normalize(reference_field)
            matching_sources = [
                source
                for source in sorted(set(context_awards))
                if normalize(source) in normalized_reference
                or normalized_reference in normalize(source)
            ]
            if "national employment standards" in normalized_reference:
                reference_supported = "national employment standards" in normalize(
                    context
                )
            elif "multiple awards" in normalized_reference:
                reference_supported = len(set(context_awards)) >= 2
            elif reference_field:
                reference_supported = bool(matching_sources)
            else:
                reference_supported = None

            all_numeric = all(item["found"] for item in numeric_checks)
            all_citations = all(item["found"] for item in citation_checks)
            applicable = [
                value
                for value in (
                    all_numeric if numeric_checks else None,
                    all_citations if citation_checks else None,
                    reference_supported,
                    error is None,
                )
                if value is not None
            ]
            results.append(
                {
                    "id": entry.get("id"),
                    "question": question,
                    "historical_answer": answer,
                    "historical_content_score": entry.get("content_score"),
                    "current_context": {
                        "characters": len(context),
                        "document_blocks": context.count("[Document "),
                        "source_awards": context_awards,
                        "unique_source_awards": sorted(set(context_awards)),
                        "cag_present": "[CAG Cache - Pre-loaded Content]" in context,
                    },
                    "claims": {
                        "answer_field": answer_field,
                        "reference_field": reference_field,
                        "citation_field": citation_field,
                        "numeric": numeric_checks,
                        "citations": citation_checks,
                        "matching_reference_sources": matching_sources,
                        "reference_supported": reference_supported,
                    },
                    "checks": {
                        "all_numeric_found": all_numeric if numeric_checks else None,
                        "all_citations_found": all_citations
                        if citation_checks
                        else None,
                        "reference_supported": reference_supported,
                        "retrieval_error": error,
                    },
                    "exact_support_diagnostic_pass": all(applicable),
                }
            )
    finally:
        rag.get_llm = original_get_llm

    numeric_items = [item for result in results for item in result["claims"]["numeric"]]
    citation_items = [
        item for result in results for item in result["claims"]["citations"]
    ]
    reference_items = [
        result["claims"]["reference_supported"]
        for result in results
        if result["claims"]["reference_supported"] is not None
    ]
    return {
        "schema_version": "1.0",
        "scope": {
            "candidate": "current dirty QA working tree and current store",
            "answers": "historical data/hard_eval_results.json; not regenerated",
            "provider_request": False,
            "method": "normalized literal occurrence in currently retrieved context",
            "legal_validation": False,
        },
        "summary": {
            "questions": len(results),
            "exact_support_diagnostic_passes": sum(
                item["exact_support_diagnostic_pass"] for item in results
            ),
            "numeric_claims": {
                "found": sum(item["found"] for item in numeric_items),
                "total": len(numeric_items),
            },
            "citation_claims": {
                "found": sum(item["found"] for item in citation_items),
                "total": len(citation_items),
            },
            "reference_fields": {
                "supported": sum(bool(item) for item in reference_items),
                "total": len(reference_items),
            },
            "retrieval_errors": sum(
                result["checks"]["retrieval_error"] is not None for result in results
            ),
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        },
        "limitations": [
            "Occurrence does not prove legal applicability or correctness.",
            "Absence can result from retrieval truncation or formatting differences.",
            "The historical answers were produced with unidentified run inputs.",
            "The current working-tree prompt differs from the committed prompt.",
            "No employment-law reviewer approved the claims.",
        ],
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    evidence = run_probe()
    rendered = json.dumps(evidence, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(json.dumps(evidence["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
