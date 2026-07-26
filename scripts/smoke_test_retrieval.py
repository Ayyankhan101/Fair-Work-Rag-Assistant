#!/usr/bin/env python3
"""Smoke test retrieval quality on built TurboVec store."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from vectorstore import load_vectorstore, search_store


TEST_QUERIES = [
    "What is the minimum break under the Hospitality Award?",
    "What leave entitlements are covered by the NES?",
    "Does the Professional Employees Award apply to software engineers?",
]


def main() -> int:
    store_dir = ROOT / "data" / "vectorstore"
    if not (store_dir / "index.tvim").exists():
        print("Vector store missing. Build first.")
        return 1

    store = load_vectorstore(str(store_dir))
    for query in TEST_QUERIES:
        print(f"\nQUERY: {query}")
        results = search_store(store, query, k=5)
        for idx, doc in enumerate(results, start=1):
            meta = doc.metadata
            print(
                f"  {idx}. {meta.get('award_name')} | "
                f"{meta.get('clause_number', '')} | {meta.get('document_type')}"
            )
            print(f"     {doc.page_content[:180].replace(chr(10), ' ')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
