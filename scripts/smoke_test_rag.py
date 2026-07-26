#!/usr/bin/env python3
"""Smoke test RAG answers and output format."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rag import create_rag_chain, ask_question
from vectorstore import load_vectorstore


TEST_QUESTIONS = [
    "What is the minimum break under the Hospitality Award?",
    "What are overtime rules for a casual employee?",
    "What leave entitlements are covered by the NES?",
]

REQUIRED_HEADERS = [
    "**Answer:**",
    "**Award/NES Reference:**",
    "**Clause/Section:**",
    "**Explanation:**",
    "**Note:**",
]


def main() -> int:
    store_dir = ROOT / "data" / "vectorstore"
    if not (store_dir / "index.tvim").exists():
        print("Vector store missing. Build first.")
        return 1

    vectorstore = load_vectorstore(str(store_dir))
    rag_chain = create_rag_chain(vectorstore)

    failures = 0
    for question in TEST_QUESTIONS:
        print(f"\nQUESTION: {question}")
        answer = ask_question(rag_chain, question)
        print(answer)
        missing = [header for header in REQUIRED_HEADERS if header not in answer]
        if missing:
            failures += 1
            print(f"FORMAT FAILURE: missing {missing}")
        if not re.search(r"\*\*Clause/Section:\*\*\s*.+", answer):
            failures += 1
            print("FORMAT FAILURE: empty clause/section")

    if failures:
        print(f"\nFAILURES: {failures}")
        return 1

    print("\nRAG smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
