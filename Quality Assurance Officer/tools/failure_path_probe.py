#!/usr/bin/env python3
"""Exercise provider-error and fallback behavior without network requests."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from langchain_core.messages import AIMessage
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnableLambda

import rag
from cag import CAGCache

QUESTION = "What meal break applies under the Hospitality Award?"
ERRORS = [
    ("429", "HTTP 429 rate_limit"),
    ("413", "HTTP 413 request too large"),
    ("rate_limit", "provider rate_limit exceeded"),
    ("timeout", "request timed out"),
    ("500", "HTTP 500 internal server error"),
    ("401", "HTTP 401 unauthorized"),
]


class EmptyRetriever(BaseRetriever):
    """Semantic stand-in; Award-specific retrieval uses the real docstore."""

    def _get_relevant_documents(self, query: str) -> list:
        return []


class FakeVectorStore:
    """Provide the create_rag_chain vector-store interface."""

    def as_retriever(self, **kwargs: Any) -> BaseRetriever:
        return EmptyRetriever()


def run_probe() -> dict[str, Any]:
    """Build real chains around injected failures and inspect disposition."""
    results = []
    original_get_llm = rag.get_llm
    try:
        for error_id, error_text in ERRORS:
            captures: list[dict[str, Any]] = []

            def fail(_: Any, message: str = error_text) -> AIMessage:
                raise RuntimeError(message)

            def capture(
                prompt_value: Any,
                capture_log: list[dict[str, Any]] = captures,
            ) -> AIMessage:
                messages = prompt_value.to_messages()
                capture_log.append(
                    {
                        "message_types": [
                            type(message).__name__ for message in messages
                        ],
                        "contents": [message.content for message in messages],
                    }
                )
                return AIMessage(content="QA_FALLBACK_CAPTURE")

            rag.get_llm = lambda fallback=False: (
                RunnableLambda(capture) if fallback else RunnableLambda(fail)
            )
            cag = CAGCache(str(ROOT / "data" / "nes" / "nes_combined.txt"))
            chain = rag.create_rag_chain(
                FakeVectorStore(),
                cag_cache=cag,
                docstore_path=str(ROOT / "data" / "vectorstore" / "docstore.json"),
            )

            output = None
            raised = None
            try:
                output = rag.ask_question(chain, QUESTION)
            except Exception as exc:  # noqa: BLE001 - retain every injected failure
                raised = f"{type(exc).__name__}: {exc}"

            rendered = captures[-1] if captures else None
            content = (
                rendered["contents"][0] if rendered and rendered["contents"] else ""
            )
            results.append(
                {
                    "id": error_id,
                    "injected_error": error_text,
                    "fallback_attempted": bool(captures),
                    "output": output,
                    "raised": raised,
                    "fallback_prompt": {
                        "message_types": rendered["message_types"] if rendered else [],
                        "characters": len(content),
                        "question_occurrences": content.count(QUESTION),
                        "contains_nested_mapping": "{'context':" in content
                        or '"context":' in content,
                    },
                }
            )
    finally:
        rag.get_llm = original_get_llm

    return {
        "schema_version": "1.0",
        "scope": {
            "candidate": "current dirty QA working tree",
            "provider_request": False,
            "real_components": [
                "create_rag_chain",
                "docstore retrieval",
                "prompt renderer",
                "ask_question fallback selector",
            ],
            "fake_components": [
                "primary provider exception",
                "fallback capture model",
            ],
        },
        "summary": {
            "cases": len(results),
            "fallback_attempts": sum(item["fallback_attempted"] for item in results),
            "exceptions_propagated": sum(
                item["raised"] is not None for item in results
            ),
            "single_human_fallback_prompts": sum(
                item["fallback_prompt"]["message_types"] == ["HumanMessage"]
                for item in results
            ),
            "repeated_question_prompts": sum(
                item["fallback_prompt"]["question_occurrences"] > 1 for item in results
            ),
            "nested_mapping_prompts": sum(
                item["fallback_prompt"]["contains_nested_mapping"] for item in results
            ),
        },
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
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
