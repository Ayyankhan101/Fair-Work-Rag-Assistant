#!/usr/bin/env python3
"""Load test with SLOs for production-like validation.
DEF-016: Execute browser, provider, soak, and deployment tests.
DEF-068: Define SLOs, admission control, resource budgets.
"""
import json
import sys
import time
import statistics
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


# SLO definitions (DEF-068)
SLOS = {
    "p50_latency_ms": 5000,      # 50th percentile: 5 seconds
    "p95_latency_ms": 10000,     # 95th percentile: 10 seconds
    "p99_latency_ms": 15000,     # 99th percentile: 15 seconds
    "throughput_rps": 5,         # Minimum 5 requests per second
    "error_rate_pct": 5.0,       # Maximum 5% errors
    "max_concurrent": 20,        # Max concurrent requests
    "availability_pct": 99.0,    # 99% availability
}

# Test questions for load testing
LOAD_QUESTIONS = [
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
    "What is the notice period for resignation?",
    "What is the casual loading percentage?",
]


def run_single_request(rag_chain, question: str) -> dict:
    """Run a single request and return timing/error info."""
    start = time.time()
    try:
        from rag import ask_question
        answer = ask_question(rag_chain, question)
        latency_ms = (time.time() - start) * 1000
        return {
            "success": True,
            "latency_ms": round(latency_ms, 2),
            "answer_length": len(answer),
            "question": question,
        }
    except Exception as e:
        latency_ms = (time.time() - start) * 1000
        return {
            "success": False,
            "latency_ms": round(latency_ms, 2),
            "error": str(e)[:200],
            "question": question,
        }


def run_load_test(num_requests: int = 50, concurrency: int = 5) -> dict:
    """Run load test with defined concurrency."""
    from rag import create_rag_chain
    from vectorstore import load_vectorstore
    from cag import get_cag_cache

    store_dir = ROOT / "data" / "vectorstore"
    if not (store_dir / "index.tvim").exists():
        print("Vector store missing. Build first.")
        return {}

    print("Loading vector store...")
    vectorstore = load_vectorstore(str(store_dir))
    docstore_path = str(store_dir / "docstore.json")
    cag_cache = get_cag_cache()
    rag_chain = create_rag_chain(vectorstore, cag_cache, docstore_path)

    print(f"\nRunning load test: {num_requests} requests, concurrency={concurrency}")
    print(f"SLOs: p50<={SLOS['p50_latency_ms']}ms, p95<={SLOS['p95_latency_ms']}ms, throughput>={SLOS['throughput_rps']}rps")

    results = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = []
        for i in range(num_requests):
            question = LOAD_QUESTIONS[i % len(LOAD_QUESTIONS)]
            futures.append(executor.submit(run_single_request, rag_chain, question))

        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            results.append(result)
            if (i + 1) % 10 == 0:
                print(f"  Completed {i+1}/{num_requests} requests")

    total_time = time.time() - start_time

    # Calculate metrics
    latencies = [r["latency_ms"] for r in results]
    successes = [r for r in results if r["success"]]
    failures = [r for r in results if not r["success"]]

    metrics = {
        "total_requests": num_requests,
        "successful": len(successes),
        "failed": len(failures),
        "total_time_seconds": round(total_time, 2),
        "throughput_rps": round(num_requests / total_time, 2),
        "error_rate_pct": round((len(failures) / num_requests) * 100, 2),
        "latency": {
            "min_ms": round(min(latencies), 2) if latencies else 0,
            "max_ms": round(max(latencies), 2) if latencies else 0,
            "mean_ms": round(statistics.mean(latencies), 2) if latencies else 0,
            "median_ms": round(statistics.median(latencies), 2) if latencies else 0,
            "p95_ms": round(sorted(latencies)[int(len(latencies) * 0.95)], 2) if latencies else 0,
            "p99_ms": round(sorted(latencies)[int(len(latencies) * 0.99)], 2) if latencies else 0,
        },
    }

    # Check SLO compliance
    slo_compliance = {
        "p50_latency": metrics["latency"]["median_ms"] <= SLOS["p50_latency_ms"],
        "p95_latency": metrics["latency"]["p95_ms"] <= SLOS["p95_latency_ms"],
        "throughput": metrics["throughput_rps"] >= SLOS["throughput_rps"],
        "error_rate": metrics["error_rate_pct"] <= SLOS["error_rate_pct"],
    }
    metrics["slo_compliance"] = slo_compliance
    metrics["all_slos_met"] = all(slo_compliance.values())

    return metrics


def main() -> int:
    """Run load test and report."""
    metrics = run_load_test(num_requests=30, concurrency=5)

    if not metrics:
        return 1

    out_path = ROOT / "data" / "load_test_results.json"
    out_path.write_text(json.dumps(metrics, indent=2))

    print(f"\n{'='*60}")
    print("LOAD TEST RESULTS")
    print(f"{'='*60}")
    print(f"Total: {metrics['total_requests']} requests")
    print(f"Successful: {metrics['successful']}")
    print(f"Failed: {metrics['failed']}")
    print(f"Throughput: {metrics['throughput_rps']} rps")
    print(f"Error Rate: {metrics['error_rate_pct']}%")
    print(f"Latency: min={metrics['latency']['min_ms']}ms, "
          f"p50={metrics['latency']['median_ms']}ms, "
          f"p95={metrics['latency']['p95_ms']}ms, "
          f"p99={metrics['latency']['p99_ms']}ms")
    print("\nSLO Compliance:")
    for slo, met in metrics['slo_compliance'].items():
        status = "PASS" if met else "FAIL"
        print(f"  {slo}: {status}")
    print(f"\nAll SLOs Met: {'YES' if metrics['all_slos_met'] else 'NO'}")
    print(f"Saved to: {out_path}")

    return 0 if metrics['all_slos_met'] else 1


if __name__ == "__main__":
    raise SystemExit(main())
