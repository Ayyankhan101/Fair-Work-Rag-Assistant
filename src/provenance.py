"""Per-request provenance logging for audit trail.

DEF-045: Persist provider request ID, actual model, tokens, latency, retries.
"""
import json
import datetime
from pathlib import Path

PROVENANCE_LOG = Path("data/provenance_log.jsonl")


def log_request(
    question: str,
    answer: str,
    model: str,
    prompt_version: str,
    prompt_hash: str,
    elapsed_s: float,
    tokens_used: int = 0,
    provider_request_id: str = "",
    retries: int = 0,
    truncated: bool = False,
    route: str = "",
    award_filter: str = "",
    error: str = "",
):
    """Append a provenance record to the JSONL log."""
    record = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "question": question[:500],
        "answer_preview": answer[:200],
        "model": model,
        "prompt_version": prompt_version,
        "prompt_hash": prompt_hash,
        "elapsed_s": round(elapsed_s, 3),
        "tokens_used": tokens_used,
        "provider_request_id": provider_request_id,
        "retries": retries,
        "truncated": truncated,
        "route": route,
        "award_filter": award_filter,
        "error": error,
    }
    PROVENANCE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(PROVENANCE_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def get_recent_provenance(n: int = 10) -> list:
    """Get the last N provenance records."""
    if not PROVENANCE_LOG.exists():
        return []
    records = []
    with open(PROVENANCE_LOG, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records[-n:]
