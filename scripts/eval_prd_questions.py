#!/usr/bin/env python3
"""Run 12 PRD sample questions and validate response format."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rag import create_rag_chain, ask_question
from vectorstore import load_vectorstore


QUESTIONS = [
    "What Award applies to a cleaner?",
    "What is the minimum break under the Hospitality Award?",
    "What are overtime rules for a casual employee?",
    "What penalties apply for weekend work?",
    "Does the Clerks Award cover payroll officers?",
    "How many hours can an employee work each week?",
    "What leave entitlements are covered by the NES?",
    "What Award covers architects?",
    "How are meal breaks handled?",
    "What allowances are payable under the Cleaning Award?",
    "Does the Professional Employees Award apply to software engineers?",
    "What is the notice period for resignation?",
]

REQUIRED_HEADERS = [
    "**Answer:**",
    "**Award/NES Reference:**",
    "**Clause/Section:**",
    "**Explanation:**",
    "**Note:**",
]


def validate_format(answer: str) -> list[str]:
    failures: list[str] = []
    for header in REQUIRED_HEADERS:
        if header not in answer:
            failures.append(f"missing {header}")
    if not re.search(r"\*\*Clause/Section:\*\*\s*.+", answer):
        failures.append("empty clause/section")
    if not re.search(r"\*\*Award/NES Reference:\*\*\s*.+", answer):
        failures.append("empty award reference")
    return failures


def main() -> int:
    store_dir = ROOT / "data" / "vectorstore"
    out_path = ROOT / "data" / "prd_eval_results.json"
    if not (store_dir / "index.tvim").exists():
        print("Vector store missing. Build first.")
        return 1

    vectorstore = load_vectorstore(str(store_dir))
    docstore_path = str(store_dir / "docstore.json")
    rag_chain = create_rag_chain(vectorstore, docstore_path=docstore_path)

    results = []
    failures = 0
    for question in QUESTIONS:
        answer = ask_question(rag_chain, question)
        format_failures = validate_format(answer)
        if format_failures:
            failures += 1
        results.append(
            {
                "question": question,
                "answer": answer,
                "format_failures": format_failures,
            }
        )
        print(f"DONE: {question}")

    out_path.write_text(json.dumps(results, indent=2))
    print(f"Saved results to {out_path}")
    print(f"Format failures: {failures}/{len(QUESTIONS)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
