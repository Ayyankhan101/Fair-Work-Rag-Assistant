#!/usr/bin/env python3
"""Measure semantic retrieval accuracy, determinism, and local concurrency.

This QA-only harness loads the persisted TurboVec store and local embedding
model. It does not start Gradio and never contacts an LLM provider.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import psutil

ROOT = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(SRC))

from offline_request_matrix import CASES

from vectorstore import load_vectorstore


def percentile(values: list[float], fraction: float) -> float:
    """Return a nearest-rank percentile for a non-empty list."""
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(len(ordered) * fraction) - 1))
    return ordered[index]


def document_identity(doc: Any) -> str:
    """Create a stable diagnostic identity for a retrieved document."""
    payload = json.dumps(
        {
            "text": doc.page_content,
            "metadata": doc.metadata,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def summarize_docs(docs: list[Any]) -> list[dict[str, Any]]:
    """Retain compact retrieval evidence without copying full source text."""
    return [
        {
            "identity": document_identity(doc),
            "award_name": doc.metadata.get("award_name"),
            "clause_number": doc.metadata.get("clause_number"),
            "section_title": doc.metadata.get("section_title"),
            "document_type": doc.metadata.get("document_type"),
            "text_prefix": doc.page_content[:160],
        }
        for doc in docs
    ]


def run_probe() -> dict[str, Any]:
    """Execute accuracy, deterministic-repeat, and concurrency diagnostics."""
    process = psutil.Process()
    initial_rss = process.memory_info().rss
    overall_started = time.perf_counter()
    load_started = time.perf_counter()
    store = load_vectorstore(str(ROOT / "data" / "vectorstore"))
    load_seconds = time.perf_counter() - load_started
    after_load_rss = process.memory_info().rss

    accuracy_results = []
    award_cases = [case for case in CASES if case.get("award")]
    for case in award_cases:
        query = case["question"]
        expected = case["award"]

        raw_started = time.perf_counter()
        raw_docs = store.similarity_search(query, k=10)
        raw_ms = (time.perf_counter() - raw_started) * 1000

        filter_started = time.perf_counter()
        filtered_docs = store.similarity_search(
            query,
            k=5,
            filter={"award_name": expected},
        )
        filter_ms = (time.perf_counter() - filter_started) * 1000

        raw_awards = [doc.metadata.get("award_name") for doc in raw_docs]
        filtered_awards = [doc.metadata.get("award_name") for doc in filtered_docs]
        accuracy_results.append(
            {
                "id": case["id"],
                "category": case["category"],
                "question": query,
                "expected_award": expected,
                "raw": {
                    "latency_ms": round(raw_ms, 3),
                    "top_1_match": bool(raw_awards and raw_awards[0] == expected),
                    "top_5_match": expected in raw_awards[:5],
                    "top_10_match": expected in raw_awards[:10],
                    "documents": summarize_docs(raw_docs),
                },
                "metadata_filtered": {
                    "latency_ms": round(filter_ms, 3),
                    "returned": len(filtered_docs),
                    "all_match": bool(filtered_docs)
                    and all(name == expected for name in filtered_awards),
                    "documents": summarize_docs(filtered_docs),
                },
            }
        )

    repeat_cases = award_cases[:10]
    repeat_results = []
    for case in repeat_cases:
        runs = []
        for _ in range(3):
            docs = store.similarity_search(case["question"], k=10)
            runs.append([document_identity(doc) for doc in docs])
        repeat_results.append(
            {
                "id": case["id"],
                "identical_across_three_runs": runs[0] == runs[1] == runs[2],
                "runs": runs,
            }
        )

    concurrency_results = []
    questions = [case["question"] for case in CASES]
    for workers in (1, 2, 4, 8, 16):
        total_requests = 60
        latencies = []
        errors = []
        peak_rss = process.memory_info().rss
        stop_sampling = threading.Event()

        def sample_memory(stop_event: threading.Event = stop_sampling) -> None:
            nonlocal peak_rss
            while not stop_event.wait(0.02):
                peak_rss = max(peak_rss, process.memory_info().rss)

        def retrieve(index: int) -> float:
            started = time.perf_counter()
            docs = store.similarity_search(questions[index % len(questions)], k=5)
            if len(docs) != 5:
                raise RuntimeError(f"expected 5 documents, received {len(docs)}")
            return (time.perf_counter() - started) * 1000

        sampler = threading.Thread(target=sample_memory, daemon=True)
        sampler.start()
        level_started = time.perf_counter()
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(retrieve, index) for index in range(total_requests)
            ]
            for future in as_completed(futures):
                try:
                    latencies.append(future.result())
                except Exception as exc:  # noqa: BLE001 - retain worker failures
                    errors.append(f"{type(exc).__name__}: {exc}")
        duration = time.perf_counter() - level_started
        stop_sampling.set()
        sampler.join(timeout=1)
        peak_rss = max(peak_rss, process.memory_info().rss)

        concurrency_results.append(
            {
                "workers": workers,
                "requests": total_requests,
                "completed": len(latencies),
                "errors": errors,
                "duration_seconds": round(duration, 3),
                "throughput_requests_per_second": round(len(latencies) / duration, 3),
                "latency_ms": {
                    "minimum": round(min(latencies), 3) if latencies else None,
                    "median": round(statistics.median(latencies), 3)
                    if latencies
                    else None,
                    "p95": round(percentile(latencies, 0.95), 3) if latencies else None,
                    "maximum": round(max(latencies), 3) if latencies else None,
                },
                "peak_rss_bytes": peak_rss,
            }
        )

    raw_top_1 = sum(item["raw"]["top_1_match"] for item in accuracy_results)
    raw_top_5 = sum(item["raw"]["top_5_match"] for item in accuracy_results)
    raw_top_10 = sum(item["raw"]["top_10_match"] for item in accuracy_results)
    filtered_all = sum(
        item["metadata_filtered"]["all_match"] for item in accuracy_results
    )

    return {
        "schema_version": "1.0",
        "scope": {
            "candidate": "current dirty QA working tree",
            "store": "data/vectorstore",
            "embedding": "BAAI/bge-base-en-v1.5 through FastEmbed",
            "provider_request": False,
            "server_request": False,
            "load_type": "in-process retrieval concurrency, not HTTP load",
        },
        "summary": {
            "award_queries": len(accuracy_results),
            "raw_semantic": {
                "top_1": raw_top_1,
                "top_5": raw_top_5,
                "top_10": raw_top_10,
                "total": len(accuracy_results),
            },
            "metadata_filtered": {
                "all_results_match_expected": filtered_all,
                "total": len(accuracy_results),
            },
            "deterministic_three_run": {
                "identical": sum(
                    item["identical_across_three_runs"] for item in repeat_results
                ),
                "total": len(repeat_results),
            },
            "load_seconds": round(load_seconds, 3),
            "initial_rss_bytes": initial_rss,
            "after_load_rss_bytes": after_load_rss,
            "final_rss_bytes": process.memory_info().rss,
            "elapsed_seconds": round(time.perf_counter() - overall_started, 3),
        },
        "accuracy_results": accuracy_results,
        "repeat_results": repeat_results,
        "concurrency_results": concurrency_results,
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
    print(
        json.dumps(
            {"concurrency_results": evidence["concurrency_results"]},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
