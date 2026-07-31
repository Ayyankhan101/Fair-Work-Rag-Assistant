#!/usr/bin/env python3
"""Live API conformance test for Groq provider.

DEF-047: Execute controlled provider matrix with approved keys.
Requires GROQ_API_KEY in environment.
"""
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dotenv import load_dotenv
load_dotenv()

RESULTS = []


def test(name: str, func):
    """Run a test and record result."""
    start = time.time()
    try:
        result = func()
        elapsed = time.time() - start
        RESULTS.append({"test": name, "status": "PASS", "elapsed_s": round(elapsed, 2), "detail": str(result)[:200]})
        print(f"  PASS  {name} ({elapsed:.2f}s)")
    except Exception as e:
        elapsed = time.time() - start
        RESULTS.append({"test": name, "status": "FAIL", "elapsed_s": round(elapsed, 2), "error": str(e)[:200]})
        print(f"  FAIL  {name}: {e}")


def test_basic_connection():
    from langchain_groq import ChatGroq
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, max_tokens=50, timeout=10)
    resp = llm.invoke("Say hello in one word.")
    return resp.content


def test_primary_model():
    from langchain_groq import ChatGroq
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, max_tokens=50, timeout=15)
    resp = llm.invoke("What is 2+2?")
    return resp.content


def test_system_message():
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, max_tokens=100, timeout=10)
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("You are a helpful assistant. Answer briefly."),
        HumanMessagePromptTemplate.from_template("{question}"),
    ])
    chain = prompt | llm
    resp = chain.invoke({"question": "What is the capital of France?"})
    return resp.content


def test_clarification_path():
    from rag import needs_clarification
    assert needs_clarification("hello")
    assert not needs_clarification("What is the minimum break under the Hospitality Award?")
    return "Clarification logic works"


def test_negation_detection():
    from router import detect_negation, detect_award_with_negation
    negated = detect_negation("Not the retail award")
    assert isinstance(negated, list)
    award, neg = detect_award_with_negation("Not the sporting organisations award")
    return f"Negation detection works: negated={len(neg)} awards"


if __name__ == "__main__":
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY not set. Cannot run live tests.")
        print("Set it in .env or environment: export GROQ_API_KEY=gsk_...")
        sys.exit(1)

    print("Running provider conformance tests...\n")
    test("basic_connection", test_basic_connection)
    test("primary_model", test_primary_model)
    test("system_message", test_system_message)
    test("clarification_path", test_clarification_path)
    test("negation_detection", test_negation_detection)

    passed = sum(1 for r in RESULTS if r["status"] == "PASS")
    total = len(RESULTS)
    print(f"\nResults: {passed}/{total} passed")
    
    import json
    out = ROOT / "data" / "provider_conformance_results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump({"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"), "passed": passed, "total": total, "results": RESULTS}, f, indent=2)
    print(f"Results saved to {out}")
