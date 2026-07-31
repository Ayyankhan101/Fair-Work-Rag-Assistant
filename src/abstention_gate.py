"""Abstention gate — determine if sufficient support exists to answer."""
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class AbstentionDecision:
    should_abstain: bool
    reason: str
    confidence: float
    found_citations: int
    verified_citations: int


class AbstentionGate:
    """Determine if sufficient support exists to answer.
    
    Per playbook Part 5.2: "'I could not find authority for this' is a correct 
    and valuable answer. Measure and reward it."
    """
    
    def __init__(
        self,
        min_verified_citations: int = 1,
        min_confidence: float = 0.5,
        min_coverage: float = 0.3,
    ):
        self.min_verified_citations = min_verified_citations
        self.min_confidence = min_confidence
        self.min_coverage = min_coverage
    
    def should_abstain(
        self,
        question: str,
        verified_citations: list,
        confidence: float = 0.0,
    ) -> AbstentionDecision:
        """Determine if system should abstain from answering.
        
        Args:
            question: Original user question
            verified_citations: List of verified citation objects
            confidence: Average confidence from verification
        """
        found_count = len(verified_citations)
        verified_count = sum(1 for c in verified_citations if c.verified)
        
        # Rule 1: No verified citations at all
        if verified_count == 0:
            return AbstentionDecision(
                should_abstain=True,
                reason="No verified citations found",
                confidence=0.0,
                found_citations=found_count,
                verified_citations=verified_count,
            )
        
        # Rule 2: Insufficient verified citations
        if verified_count < self.min_verified_citations:
            return AbstentionDecision(
                should_abstain=True,
                reason=f"Insufficient verified citations ({verified_count} < {self.min_verified_citations})",
                confidence=confidence,
                found_citations=found_count,
                verified_citations=verified_count,
            )
        
        # Rule 3: Low confidence
        if confidence < self.min_confidence:
            return AbstentionDecision(
                should_abstain=True,
                reason=f"Low confidence ({confidence:.2f} < {self.min_confidence})",
                confidence=confidence,
                found_citations=found_count,
                verified_citations=verified_count,
            )
        
        # Rule 4: Poor coverage (few citations relative to question complexity)
        question_words = len(question.split())
        coverage = verified_count / max(question_words / 5, 1)
        if coverage < self.min_coverage:
            return AbstentionDecision(
                should_abstain=True,
                reason=f"Poor coverage ({coverage:.2f} < {self.min_coverage})",
                confidence=confidence,
                found_citations=found_count,
                verified_citations=verified_count,
            )
        
        # All checks passed — answer is supported
        return AbstentionDecision(
            should_abstain=False,
            reason="Sufficient support found",
            confidence=confidence,
            found_citations=found_count,
            verified_citations=verified_count,
        )
    
    def get_abstention_response(self, question: str, found_citations: list) -> str:
        """Generate abstention response when support is insufficient."""
        if not found_citations:
            return (
                "**Answer:** I could not find sufficient authority to answer this question.\n\n"
                "**What was found:** No relevant sources were retrieved from the corpus.\n\n"
                "**Recommendation:** Please consult an employment law practitioner or "
                "search the Fair Work Commission decisions database directly."
            )
        
        citations_text = "\n".join([
            f"- {c.citation}" for c in found_citations[:5]
        ])
        
        return (
            "**Answer:** I could not find sufficient authority to answer this question "
            "with the required level of confidence.\n\n"
            f"**What was found:** {len(found_citations)} sources were retrieved, but they "
            "do not provide adequate support for a definitive answer.\n\n"
            f"**Retrieved sources:**\n{citations_text}\n\n"
            "**Recommendation:** Please verify these sources manually or consult "
            "an employment law practitioner."
        )
