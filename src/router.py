"""Query router for hybrid CAG+RAG architecture."""
from enum import Enum
from dataclasses import dataclass
from typing import Optional
from config import AWARD_PATTERNS, NES_KEYWORDS, has_nes_keywords, detect_award


class RouteType(Enum):
    CAG = "cag"           # Cache hit - use pre-loaded context only
    RAG = "rag"           # Retrieval - use vector search only
    COMBINED = "combined" # Both cache and retrieval needed


@dataclass
class RoutingDecision:
    route: RouteType
    confidence: float
    reasoning: str
    award_filter: Optional[str] = None  # For RAG: filter to specific Award


def route_question(question: str, cag_cache) -> RoutingDecision:
    """Route a question to CAG, RAG, or Combined path."""
    # Check for NES-related content
    nes_detected = has_nes_keywords(question)
    
    # Check for Award-specific content
    award_name = detect_award(question)
    
    # Decision logic
    if nes_detected and award_name:
        return RoutingDecision(
            route=RouteType.COMBINED,
            confidence=0.9,
            reasoning=f"NES keywords + specific Award ({award_name})",
            award_filter=award_name,
        )
    elif nes_detected:
        return RoutingDecision(
            route=RouteType.CAG,
            confidence=0.85,
            reasoning="NES keywords detected, no specific Award",
        )
    elif award_name:
        return RoutingDecision(
            route=RouteType.RAG,
            confidence=0.8,
            reasoning=f"Specific Award detected: {award_name}",
            award_filter=award_name,
        )
    else:
        return RoutingDecision(
            route=RouteType.RAG,
            confidence=0.7,
            reasoning="No NES or specific Award keywords",
        )
