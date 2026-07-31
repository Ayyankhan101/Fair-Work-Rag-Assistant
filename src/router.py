"""Query router for hybrid CAG+RAG architecture."""
import re
from enum import Enum
from dataclasses import dataclass
from typing import Optional
from config import AWARD_PATTERNS, has_nes_keywords, detect_award


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
    negated_awards: list = None  # Awards explicitly excluded


def detect_negation(question: str) -> list:
    """Detect negated awards in question. Returns list of negated award names."""
    q = question.lower()
    negated = []
    
    # Patterns: "not X", "no X", "without X", "except X", "excluding X"
    negation_patterns = [
        r'not\s+([\w\s]+?)(?:\s+award|\s+rate|\s+rule|$)',
        r'no\s+([\w\s]+?)(?:\s+award|\s+rate|\s+rule|$)',
        r'without\s+([\w\s]+?)(?:\s+award|\s+rate|\s+rule|$)',
        r'except\s+([\w\s]+?)(?:\s+award|\s+rate|\s+rule|$)',
        r'excluding\s+([\w\s]+?)(?:\s+award|\s+rate|\s+rule|$)',
    ]
    
    for pattern in negation_patterns:
        for match in re.finditer(pattern, q):
            negated_word = match.group(1).strip()
            # Check if this matches any award
            for keyword, award_name in AWARD_PATTERNS.items():
                if keyword in negated_word or negated_word in keyword:
                    if award_name not in negated:
                        negated.append(award_name)
    
    return negated


def detect_award_with_negation(question: str):
    """Detect award with negation support. Returns (award_name, negated_awards)."""
    negated = detect_negation(question)
    award = detect_award(question)
    
    # If detected award is negated, return None
    if award and award in negated:
        return None, negated
    
    return award, negated


def route_question(question: str, cag_cache) -> RoutingDecision:
    """Route a question to CAG, RAG, or Combined path."""
    # Check for NES-related content
    nes_detected = has_nes_keywords(question)
    
    # Check for Award-specific content with negation
    award_name, negated_awards = detect_award_with_negation(question)
    
    # Decision logic
    if nes_detected and award_name:
        return RoutingDecision(
            route=RouteType.COMBINED,
            confidence=0.9,
            reasoning=f"NES keywords + specific Award ({award_name})",
            award_filter=award_name,
            negated_awards=negated_awards,
        )
    elif nes_detected:
        return RoutingDecision(
            route=RouteType.CAG,
            confidence=0.85,
            reasoning="NES keywords detected, no specific Award",
            negated_awards=negated_awards,
        )
    elif award_name:
        return RoutingDecision(
            route=RouteType.RAG,
            confidence=0.8,
            reasoning=f"Specific Award detected: {award_name}",
            award_filter=award_name,
            negated_awards=negated_awards,
        )
    else:
        return RoutingDecision(
            route=RouteType.RAG,
            confidence=0.7,
            reasoning="No NES or specific Award keywords",
            negated_awards=negated_awards,
        )
