"""Corpus manager — point-in-time correctness, versioning, treatment signals."""
import json
import datetime
import logging
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ProvisionVersion:
    section: str
    in_force_from: str  # ISO date
    in_force_to: Optional[str]  # None = currently in force
    text: str
    amendment_history: list[dict]


@dataclass
class TreatmentSignal:
    decision_citation: str
    was_appealed: bool
    appeal_result: Optional[str]  # "upheld" | "overturned" | "distinguished"
    appeal_citation: Optional[str]
    date_checked: str


class CorpusManager:
    """Manage corpus versioning and point-in-time correctness.
    
    Per playbook Part 4.2: "Law changes; the Fair Work Act has been amended 
    repeatedly. Every provision needs in_force_from / in_force_to."
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.corpus_version = self._load_corpus_version()
        self.provisions = self._load_provisions()
        self.treatments = self._load_treatments()
    
    def _load_corpus_version(self) -> str:
        """Load or create corpus version string."""
        version_file = self.data_dir / "corpus_version.json"
        if version_file.exists():
            with open(version_file) as f:
                data = json.load(f)
                return data.get("version", "unknown")
        
        # Create new version
        version = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        version_file.parent.mkdir(parents=True, exist_ok=True)
        with open(version_file, "w") as f:
            json.dump({"version": version, "created": version}, f, indent=2)
        return version
    
    def _load_provisions(self) -> dict:
        """Load provision versioning data."""
        provisions_file = self.data_dir / "provisions.json"
        if provisions_file.exists():
            with open(provisions_file) as f:
                return json.load(f)
        return {}
    
    def _load_treatments(self) -> dict:
        """Load treatment/appeal signals."""
        treatments_file = self.data_dir / "treatments.json"
        if treatments_file.exists():
            with open(treatments_file) as f:
                return json.load(f)
        return {}
    
    def get_current_version(self) -> str:
        """Return current corpus version string."""
        return self.corpus_version
    
    def is_in_force(self, section: str, date: Optional[str] = None) -> bool:
        """Check if a provision was in force on a given date.
        
        Args:
            section: e.g., "s387", "s390(1)"
            date: ISO date string, defaults to today
        """
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        provision = self.provisions.get(section)
        if not provision:
            logger.warning(f"No versioning data for {section}")
            return True  # Assume in force if unknown
        
        in_force_from = provision.get("in_force_from", "1900-01-01")
        in_force_to = provision.get("in_force_to", "9999-12-31")
        
        return in_force_from <= date <= in_force_to
    
    def get_treatment(self, decision_citation: str) -> Optional[TreatmentSignal]:
        """Was this decision appealed, overturned, distinguished, followed?"""
        treatment_data = self.treatments.get(decision_citation)
        if not treatment_data:
            return None
        
        return TreatmentSignal(
            decision_citation=decision_citation,
            was_appealed=treatment_data.get("was_appealed", False),
            appeal_result=treatment_data.get("appeal_result"),
            appeal_citation=treatment_data.get("appeal_citation"),
            date_checked=treatment_data.get("date_checked", "unknown"),
        )
    
    def add_provision(self, section: str, in_force_from: str, text: str, 
                      in_force_to: Optional[str] = None):
        """Add or update a provision version."""
        self.provisions[section] = {
            "section": section,
            "in_force_from": in_force_from,
            "in_force_to": in_force_to,
            "text": text,
            "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        self._save_provisions()
    
    def add_treatment(self, citation: str, was_appealed: bool, 
                      appeal_result: Optional[str] = None,
                      appeal_citation: Optional[str] = None):
        """Add or update a treatment signal."""
        self.treatments[citation] = {
            "was_appealed": was_appealed,
            "appeal_result": appeal_result,
            "appeal_citation": appeal_citation,
            "date_checked": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
        }
        self._save_treatments()
    
    def _save_provisions(self):
        """Save provisions to disk."""
        provisions_file = self.data_dir / "provisions.json"
        with open(provisions_file, "w") as f:
            json.dump(self.provisions, f, indent=2)
    
    def _save_treatments(self):
        """Save treatments to disk."""
        treatments_file = self.data_dir / "treatments.json"
        with open(treatments_file, "w") as f:
            json.dump(self.treatments, f, indent=2)
    
    def get_corpus_metadata(self) -> dict:
        """Get complete corpus metadata for audit trail."""
        return {
            "version": self.corpus_version,
            "provisions_count": len(self.provisions),
            "treatments_count": len(self.treatments),
            "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
