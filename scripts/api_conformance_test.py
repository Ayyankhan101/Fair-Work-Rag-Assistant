#!/usr/bin/env python3
"""API conformance test framework for provider evaluation.
DEF-047: Execute controlled provider matrix with approved keys, budget, corpus, and legal oracle.
"""
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


# Test matrix for provider conformance
PROVIDER_MATRIX = [
    {
        "id": "PC-001",
        "name": "Basic Award Query",
        "question": "What Award applies to a cleaner?",
        "expected_keywords": ["Cleaning", "Award"],
        "expected_route": "rag",
        "timeout_seconds": 30,
    },
    {
        "id": "PC-002",
        "name": "NES Query",
        "question": "What is the minimum annual leave under the NES?",
        "expected_keywords": ["annual leave", "4 weeks", "20 days"],
        "expected_route": "cag",
        "timeout_seconds": 30,
    },
    {
        "id": "PC-003",
        "name": "Specific Award Detail",
        "question": "What is the casual loading under the Hospitality Award?",
        "expected_keywords": ["casual", "loading", "25%"],
        "expected_route": "rag",
        "timeout_seconds": 30,
    },
    {
        "id": "PC-004",
        "name": "Rate Limit Recovery",
        "question": "What are overtime rules for casual employees under the Retail Award?",
        "expected_keywords": ["overtime", "casual"],
        "expected_route": "rag",
        "timeout_seconds": 30,
        "rate_limit_test": True,
    },
    {
        "id": "PC-005",
        "name": "Combined NES+Award",
        "question": "What are the NES annual leave and Hospitality Award leave provisions?",
        "expected_keywords": ["annual leave", "leave"],
        "expected_route": "combined",
        "timeout_seconds": 30,
    },
    {
        "id": "PC-006",
        "name": "Clarification Needed",
        "question": "hello",
        "expected_keywords": ["clarification", "more details"],
        "expected_route": "clarification",
        "timeout_seconds": 10,
    },
    {
        "id": "PC-007",
        "name": "Unknown Award",
        "question": "What is the minimum wage for a rocket scientist?",
        "expected_keywords": ["not enough information", "don't have"],
        "expected_route": "rag",
        "timeout_seconds": 30,
    },
    {
        "id": "PC-008",
        "name": "Response Format Validation",
        "question": "What is the notice period for resignation under the Clerks Award?",
        "expected_format": ["**Answer:**", "**Award/NES Reference:**", "**Clause/Section:**", "**Explanation:**", "**Note:**"],
        "expected_route": "rag",
        "timeout_seconds": 30,
    },
]


def validate_conformance(answer: str, test: dict) -> dict:
    """Validate answer against conformance requirements."""
    result = {
        "test_id": test["id"],
        "passed": True,
        "failures": [],
        "latency_ms": 0,
    }

    # Format validation
    if "expected_format" in test:
        for header in test["expected_format"]:
            if header not in answer:
                result["passed"] = False
                result["failures"].append(f"Missing format: {header}")

    # Keyword validation
    if "expected_keywords" in test:
        answer_lower = answer.lower()
        for kw in test["expected_keywords"]:
            if kw.lower() not in answer_lower:
                result["passed"] = False
                result["failures"].append(f"Missing keyword: {kw}")

    # Length validation (should not be empty or error)
    if len(answer) < 50:
        result["passed"] = False
        result["failures"].append(f"Answer too short: {len(answer)} chars")

    return result


def run_conformance_tests() -> int:
    """Run all conformance tests."""
    from rag import create_rag_chain, ask_question
    from vectorstore import load_vectorstore
    from cag import get_cag_cache
    from router import route_question

    store_dir = ROOT / "data" / "vectorstore"
    if not (store_dir / "index.tvim").exists():
        print("Vector store missing. Build first.")
        return 1

    print("Loading vector store...")
    vectorstore = load_vectorstore(str(store_dir))
    docstore_path = str(store_dir / "docstore.json")
    cag_cache = get_cag_cache()
    rag_chain = create_rag_chain(vectorstore, cag_cache, docstore_path)

    results = []
    passed = 0
    total = len(PROVIDER_MATRIX)

    for test in PROVIDER_MATRIX:
        print(f"\n[{test['id']}] {test['name']}: {test['question'][:60]}...")

        start = time.time()
        try:
            # Test routing
            decision = route_question(test["question"], cag_cache)
            actual_route = decision.route.value

            # Get answer
            answer = ask_question(rag_chain, test["question"])
            latency = (time.time() - start) * 1000

            # Validate
            result = validate_conformance(answer, test)
            result["latency_ms"] = round(latency, 2)
            result["actual_route"] = actual_route
            result["answer_preview"] = answer[:200]

            if result["passed"]:
                passed += 1
                print(f"  PASS ({latency:.0f}ms)")
            else:
                print(f"  FAIL: {', '.join(result['failures'])}")

        except Exception as e:
            latency = (time.time() - start) * 1000
            result = {
                "test_id": test["id"],
                "passed": False,
                "failures": [f"Exception: {str(e)[:100]}"],
                "latency_ms": round(latency, 2),
            }
            print(f"  ERROR: {e}")

        results.append(result)
        time.sleep(1)

    # Save results
    output = {
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": f"{(passed/total)*100:.1f}%",
        },
        "results": results,
    }

    out_path = ROOT / "data" / "conformance_results.json"
    out_path.write_text(json.dumps(output, indent=2))

    print(f"\n{'='*60}")
    print("CONFORMANCE TEST RESULTS")
    print(f"{'='*60}")
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Pass Rate: {(passed/total)*100:.1f}%")
    print(f"Saved to: {out_path}")

    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(run_conformance_tests())
