"""Full audit trail — query, docs, prompt, model, corpus version, verdicts."""
import json
import datetime
import hashlib
import logging
from dataclasses import dataclass, asdict
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class AuditEntry:
    """Complete audit record for a single query."""
    # Query
    query: str
    query_id: str
    session_id: str
    
    # Retrieval
    retrieved_doc_ids: list[str]
    retrieved_scores: list[float]
    retrieval_method: str  # "hybrid" | "semantic" | "bm25"
    
    # Generation
    prompt_version: str
    prompt_hash: str
    model_version: str
    generated_output: str
    
    # Verification
    verifier_verdicts: list[dict]  # [{"citation": str, "verdict": str, "confidence": float}]
    resolved_citations: list[dict]  # [{"citation": str, "verified": bool, "reason": str}]
    abstained: bool
    abstention_reason: Optional[str]
    
    # Corpus
    corpus_version: str
    
    # Timing
    timestamp: str
    retrieval_latency_ms: float
    generation_latency_ms: float
    verification_latency_ms: float
    total_latency_ms: float
    
    # User verification (for export gate)
    user_verification_actions: list[dict] = None
    
    def __post_init__(self):
        if self.user_verification_actions is None:
            self.user_verification_actions = []


class AuditLogger:
    """Full audit log for every query.
    
    Per playbook Part 5.2: "Query, retrieved doc IDs and scores, prompt version, 
    model version, corpus version, generated output, verifier verdicts, user 
    verification actions, export events."
    """
    
    def __init__(self, log_dir: str = "data/audit_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.session_entries = []
    
    def log_query(self, entry: AuditEntry):
        """Log a complete query audit entry."""
        # Append to session log
        self.session_entries.append(entry)
        
        # Write individual entry
        entry_file = self.log_dir / f"{entry.query_id}.json"
        with open(entry_file, "w") as f:
            json.dump(asdict(entry), f, indent=2, default=str)
        
        logger.info(f"AUDIT: {entry.query_id} | abstained={entry.abstained} | "
                    f"verified_citations={len([c for c in entry.resolved_citations if c.get('verified')])}")
    
    def log_user_verification(self, query_id: str, citation: str, verified: bool, url: str):
        """Log user verification action (for export gate)."""
        for entry in self.session_entries:
            if entry.query_id == query_id:
                entry.user_verification_actions.append({
                    "citation": citation,
                    "verified": verified,
                    "url": url,
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                })
                # Update entry file
                entry_file = self.log_dir / f"{query_id}.json"
                with open(entry_file, "w") as f:
                    json.dump(asdict(entry), f, indent=2, default=str)
                break
    
    def get_session_summary(self) -> dict:
        """Get summary of current session."""
        total = len(self.session_entries)
        abstained = sum(1 for e in self.session_entries if e.abstained)
        hallucinations = sum(
            len([c for c in e.resolved_citations if not c.get("verified")])
            for e in self.session_entries
        )
        
        return {
            "total_queries": total,
            "abstained": abstained,
            "abstention_rate": abstained / total if total > 0 else 0,
            "hallucination_events": hallucinations,
        }
    
    def generate_provenance(self, entry: AuditEntry) -> str:
        """Generate provenance string for answer."""
        return (
            f"corpus_version={entry.corpus_version} | "
            f"model={entry.model_version} | "
            f"prompt={entry.prompt_version} | "
            f"query_id={entry.query_id}"
        )
