"""Citation resolver — validate every citation resolves to real corpus doc + URL."""
import re
import json
import logging
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ResolvedCitation:
    citation: str
    doc_id: Optional[str]
    source_url: Optional[str]
    verified: bool
    reason: str  # "resolved" | "hallucinated" | "url_broken"


class CitationResolver:
    """Validate every citation resolves to a real corpus document.
    
    Per playbook Part 5.2: "Regex-extract every citation from output, resolve 
    against the corpus index. Anything that does not resolve to a real document 
    with a working URL is deleted from the response and logged as a hallucination 
    event."
    """
    
    def __init__(self, corpus_index_path: str = "data/corpus_index.json"):
        self.corpus_index = self._load_index(corpus_index_path)
        self.hallucination_log = []
    
    def _load_index(self, path: str) -> dict:
        """Load corpus index for citation resolution."""
        if Path(path).exists():
            with open(path) as f:
                return json.load(f)
        logger.warning(f"Corpus index not found: {path}")
        return {}
    
    def extract_citations(self, text: str) -> list[str]:
        """Extract all citations from text using regex patterns."""
        citations = []
        
        # Pattern 1: [Case Name] citations
        case_patterns = [
            r'\[([A-Z][^.]*?\s+v\s+[A-Z][^.]*?)\]',  # [Smith v employer]
            r'(?:decision|case|authority)\s+(?:of\s+)?([A-Z][^.]*?\s+v\s+[A-Z][^.]*?)',  # decision of Smith v employer
        ]
        
        # Pattern 2: Section references
        section_patterns = [
            r's(?:ection)?\s*(\d+[A-Z]*(?:\(\d+\))?(?:\([a-z]+\))?)',  # s387, section 387(1)(a)
            r'Part\s+(\d+-\d+)',  # Part 3-2
            r'Division\s+(\d+)',  # Division 4
        ]
        
        # Pattern 3: Paragraph references
        paragraph_patterns = [
            r'paragraph?\s+([a-z]+(?:\(\d+\))?)',  # paragraph (a), paragraph (a)(i)
            r'clause\s+(\d+(?:\.\d+)?)',  # clause 15.1
        ]
        
        for pattern in case_patterns:
            citations.extend(re.findall(pattern, text))
        
        for pattern in section_patterns:
            for match in re.finditer(pattern, text):
                citations.append(match.group(0))
        
        for pattern in paragraph_patterns:
            for match in re.finditer(pattern, text):
                citations.append(match.group(0))
        
        return list(set(citations))
    
    def resolve(self, citations: list[str]) -> list[ResolvedCitation]:
        """Validate every citation against corpus index."""
        resolved = []
        
        for citation in citations:
            # Check corpus index
            doc = self.corpus_index.get(citation)
            
            if doc:
                # Check URL
                url = doc.get("source_url", "")
                if self._url_valid(url):
                    resolved.append(ResolvedCitation(
                        citation=citation,
                        doc_id=doc.get("doc_id"),
                        source_url=url,
                        verified=True,
                        reason="resolved",
                    ))
                else:
                    resolved.append(ResolvedCitation(
                        citation=citation,
                        doc_id=doc.get("doc_id"),
                        source_url=url,
                        verified=False,
                        reason="url_broken",
                    ))
                    self._log_hallucination(citation, "url_broken")
            else:
                resolved.append(ResolvedCitation(
                    citation=citation,
                    doc_id=None,
                    source_url=None,
                    verified=False,
                    reason="hallucinated",
                ))
                self._log_hallucination(citation, "not_in_corpus")
        
        return resolved
    
    def _url_valid(self, url: str) -> bool:
        """Check if URL is valid and accessible."""
        if not url:
            return False
        # For now, just check format - full validation would require HTTP request
        return url.startswith("http")
    
    def _log_hallucination(self, citation: str, reason: str):
        """Log hallucination event for monitoring SLO."""
        import datetime
        entry = {
            "citation": citation,
            "reason": reason,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        self.hallucination_log.append(entry)
        logger.warning(f"HALLUCINATION: {citation} ({reason})")
    
    def get_hallucination_rate(self) -> float:
        """Calculate hallucination rate for monitoring."""
        if not self.hallucination_log:
            return 0.0
        # This would need total citations checked - placeholder
        return len(self.hallucination_log)
    
    def save_hallucination_log(self, path: str = "data/hallucination_log.json"):
        """Save hallucination log for monitoring."""
        with open(path, "w") as f:
            json.dump(self.hallucination_log, f, indent=2)
