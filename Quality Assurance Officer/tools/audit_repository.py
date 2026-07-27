#!/usr/bin/env python3
"""Run deterministic repository and persisted-corpus QA checks."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCSTORE_PATH = ROOT / "data" / "vectorstore" / "docstore.json"
SCOPE_PATH = (
    ROOT
    / "Quality Assurance Officer"
    / "evidence"
    / "official-award-scope-2026-07-27.json"
)
REQUIRED_METADATA = {
    "award_name",
    "clause_number",
    "section_title",
    "source_url",
    "document_type",
    "source_file",
    "chunk_index",
}
CRITICAL_ID_NAMES = {
    "MA000002": "Clerks",
    "MA000022": "Cleaning Services",
    "MA000095": "Car Parking",
    "MA000121": "State Government Agencies",
}


def git_value(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def load_json(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if text.startswith("version https://git-lfs.github.com/spec"):
        raise RuntimeError(f"Git LFS object is not materialized: {path}")
    return json.loads(text)


def inspect_docstore() -> tuple[dict, list[dict]]:
    store = load_json(DOCSTORE_PATH)
    docs = list(store.get("docs", {}).values())
    failures = []

    missing_metadata = Counter()
    empty_metadata = Counter()
    document_types = Counter()
    award_names = Counter()
    source_files = Counter()
    text_hashes = Counter()
    ids_to_names: dict[str, set[str]] = defaultdict(set)
    empty_text = 0

    for doc in docs:
        text = doc.get("text", "")
        metadata = doc.get("metadata") or {}
        if not text.strip():
            empty_text += 1
        text_hashes[hashlib.sha256(text.encode("utf-8")).hexdigest()] += 1
        document_types[metadata.get("document_type", "<missing>")] += 1
        award_names[metadata.get("award_name", "<missing>")] += 1
        source_files[metadata.get("source_file", "<missing>")] += 1

        for key in REQUIRED_METADATA:
            if key not in metadata:
                missing_metadata[key] += 1
            elif metadata[key] in ("", None, []):
                empty_metadata[key] += 1

        for award_id in re.findall(r"\bMA\d{6}\b", text, re.IGNORECASE):
            ids_to_names[award_id.upper()].add(metadata.get("award_name", ""))

    scope = load_json(SCOPE_PATH)
    expected_ids = set(scope["award_ids"])
    indexed_ids = set(ids_to_names)
    missing_ids = sorted(expected_ids - indexed_ids)
    outside_scope_ids = sorted(indexed_ids - expected_ids)
    duplicate_groups = sum(1 for count in text_hashes.values() if count > 1)
    duplicate_extra_docs = sum(count - 1 for count in text_hashes.values() if count > 1)

    if missing_ids:
        failures.append(
            {
                "id": "CORPUS-001",
                "severity": "S1",
                "message": f"Missing official Award IDs: {', '.join(missing_ids)}",
            }
        )
    if empty_text:
        failures.append(
            {
                "id": "CORPUS-002",
                "severity": "S1",
                "message": f"{empty_text} chunks have empty text",
            }
        )
    if missing_metadata or empty_metadata:
        failures.append(
            {
                "id": "CORPUS-003",
                "severity": "S1",
                "message": "Required chunk metadata is missing or empty",
            }
        )
    if duplicate_extra_docs:
        failures.append(
            {
                "id": "CORPUS-004",
                "severity": "S2",
                "message": (
                    f"{duplicate_extra_docs} extra chunks occur in "
                    f"{duplicate_groups} exact-text duplicate groups"
                ),
            }
        )

    for award_id, expected_name_fragment in CRITICAL_ID_NAMES.items():
        actual_names = ids_to_names.get(award_id, set())
        if not any(
            expected_name_fragment.lower() in name.lower() for name in actual_names
        ):
            failures.append(
                {
                    "id": f"CORPUS-NAME-{award_id}",
                    "severity": "S1",
                    "message": (
                        f"{award_id} is not indexed with an Award name containing "
                        f"'{expected_name_fragment}'. Actual: {sorted(actual_names)}"
                    ),
                }
            )

    report = {
        "doc_count": len(docs),
        "document_types": dict(document_types),
        "unique_award_names": len(award_names),
        "unique_source_files": len(source_files),
        "expected_official_award_ids": len(expected_ids),
        "indexed_award_ids": len(indexed_ids),
        "missing_official_award_ids": missing_ids,
        "outside_scope_award_ids": outside_scope_ids,
        "missing_metadata": dict(missing_metadata),
        "empty_metadata": dict(empty_metadata),
        "empty_text_chunks": empty_text,
        "duplicate_text_groups": duplicate_groups,
        "duplicate_extra_chunks": duplicate_extra_docs,
    }
    return report, failures


def inspect_results() -> tuple[dict, list[dict]]:
    path = ROOT / "data" / "hard_eval_results.json"
    data = load_json(path)
    summary = data.get("summary", {})
    failures = []
    required_provenance = {
        "run_at",
        "commit_sha",
        "corpus_version",
        "model",
        "prompt_version",
    }
    missing = sorted(required_provenance - set(summary))
    if missing:
        failures.append(
            {
                "id": "EVAL-001",
                "severity": "S1",
                "message": f"Hard-eval provenance is missing: {', '.join(missing)}",
            }
        )
    return {
        "summary": summary,
        "missing_provenance": missing,
    }, failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path, help="Write the full report to this path")
    args = parser.parse_args()

    failures = []
    corpus, corpus_failures = inspect_docstore()
    evaluation, evaluation_failures = inspect_results()
    failures.extend(corpus_failures)
    failures.extend(evaluation_failures)

    if not (ROOT / "data" / "awards").exists():
        failures.append(
            {
                "id": "REPRO-001",
                "severity": "S1",
                "message": "data/awards is absent; the persisted store is not reproducible",
            }
        )

    report = {
        "commit_sha": git_value("rev-parse", "HEAD"),
        "branch": git_value("branch", "--show-current"),
        "corpus": corpus,
        "evaluation": evaluation,
        "failures": failures,
        "release_blocked": any(item["severity"] in {"S0", "S1"} for item in failures),
    }

    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    print(rendered)
    if args.json:
        output = args.json if args.json.is_absolute() else ROOT / args.json
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")

    return 1 if report["release_blocked"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
