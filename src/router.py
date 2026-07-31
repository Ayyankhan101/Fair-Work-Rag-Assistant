"""Query router for unfair dismissal RAG — classifies queries by type."""
import re
from enum import Enum
from dataclasses import dataclass
from typing import Optional
from src.config import QUERY_CATEGORIES


class QueryType(Enum):
    JURISDICTIONAL = "jurisdictional"      # Threshold questions (time limits, eligibility)
    STATUTORY_CRITERIA = "statutory_criteria"  # s387 factors, harsh/unjust/unreasonable
    ANALOGOUS_FACTS = "analogous_facts"    # "cases where...", similar situations
    PROCEDURAL = "procedural"              # Extensions, objections, process
    GENERAL = "general"                    # Does not fit above categories


@dataclass
class RoutingDecision:
    query_type: QueryType
    confidence: float
    reasoning: str
    relevant_sections: list = None  # e.g., ["s385", "s387"]
    is_cag_candidate: bool = False


def classify_query(question: str) -> RoutingDecision:
    """Classify an unfair dismissal question by type.
    
    Per playbook Part 5.1: "Classify: jurisdictional / principle / analogous-facts / procedural"
    """
    q = question.lower()
    scores = {}
    matched_sections = set()
    
    # Check each category
    for category, data in QUERY_CATEGORIES.items():
        keywords = data.get("keywords", [])
        score = sum(1 for kw in keywords if kw.lower() in q)
        if score > 0:
            scores[category] = score
    
    # Check for specific section references
    section_pattern = r's(?:ection)?\s*(\d{3})'
    for match in re.finditer(section_pattern, q):
        section_num = match.group(1)
        if section_num in ["385", "386", "387", "388", "389", "390", "391", "392", "393", "394"]:
            matched_sections.add(f"s{section_num}")
    
    # Determine category
    if scores:
        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]
        
        # Map config category to QueryType
        category_map = {
            "jurisdictional": QueryType.JURISDICTIONAL,
            "statutory_criteria": QueryType.STATUTORY_CRITERIA,
            "analogous_facts": QueryType.ANALOGOUS_FACTS,
            "procedural": QueryType.PROCEDURAL,
        }
        
        query_type = category_map.get(best_category, QueryType.GENERAL)
        confidence = min(0.9, 0.5 + best_score * 0.1)
        
        # Check if this is a CAG candidate (legislation question)
        is_cag = bool(matched_sections) or best_category in ["jurisdictional", "statutory_criteria"]
        
        return RoutingDecision(
            query_type=query_type,
            confidence=confidence,
            reasoning=f"Matched {best_category} ({best_score} keywords)",
            relevant_sections=list(matched_sections),
            is_cag_candidate=is_cag,
        )
    
    # No category match — check if it references any section
    if matched_sections:
        return RoutingDecision(
            query_type=QueryType.STATUTORY_CRITERIA,
            confidence=0.6,
            reasoning=f"Section reference found: {matched_sections}",
            relevant_sections=list(matched_sections),
            is_cag_candidate=True,
        )
    
    # Default to general
    return RoutingDecision(
        query_type=QueryType.GENERAL,
        confidence=0.4,
        reasoning="No category keywords matched",
        is_cag_candidate=False,
    )
