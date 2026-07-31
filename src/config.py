"""Shared configuration: Fair Work Act provisions, query categories, FWC metadata."""

# Fair Work Act 2009, Part 3-2 Division 4 — Unfair Dismissal
# Source: https://www.legislation.gov.au/C2009A00142
FAIR_WORK_ACT_PROVISIONS = {
    "s385": {
        "title": "What is an Unfair Dismissal",
        "section": "Part 3-2 Division 4",
        "summary": "A person has been unfairly dismissed if dismissed in circumstances that are harsh, unjust or unreasonable",
        "keywords": ["unfair dismissal", "harsh", "unjust", "unreasonable", "dismissed"],
    },
    "s386": {
        "title": "Meaning of Dismissed",
        "section": "Part 3-2 Division 4",
        "summary": "Person dismissed if employer terminates at initiative, or fixed term contract not renewed",
        "keywords": ["dismissed", "termination", "initiative", "contract", "renewal"],
    },
    "s387": {
        "title": "Criteria for Considering Unfairness",
        "section": "Part 3-2 Division 4",
        "summary": "FWC must consider: valid reason, notification, response opportunity, size, HR, other matters",
        "keywords": ["s387", "valid reason", "notification", "response opportunity", "small business", "HR"],
    },
    "s388": {
        "title": "Summary Dismissal",
        "section": "Part 3-2 Division 4",
        "summary": "Summary dismissal is dismissal without notice; employer must show exceptional circumstances",
        "keywords": ["summary dismissal", "without notice", "exceptional circumstances"],
    },
    "s389": {
        "title": "Exceptions to Minimum Employment Period",
        "section": "Part 3-2 Division 4",
        "summary": "Exceptions for casual, fixed term, training arrangements, small business",
        "keywords": ["minimum employment period", "6 months", "12 months", "small business", "casual", "fixed term"],
    },
    "s390": {
        "title": "Remedies for Unfair Dismissal",
        "section": "Part 3-2 Division 4",
        "summary": "FWC may order reinstatement or compensation; reinstatement preferred",
        "keywords": ["remedy", "reinstatement", "compensation", "order"],
    },
    "s391": {
        "title": "Compensation instead of Reinstatement",
        "section": "Part 3-2 Division 4",
        "summary": "Compensation only if reinstatement inappropriate; maximum 26 weeks pay",
        "keywords": ["compensation", "26 weeks", "reinstatement inappropriate", "substantial"],
    },
    "s392": {
        "title": "How Compensation is Calculated",
        "section": "Part 3-2 Division 4",
        "summary": "Compensation based on income lost, lost benefits, shock/humiliation; capped at high income threshold",
        "keywords": ["compensation", "calculation", "income lost", "high income threshold", "cap"],
    },
    "s393": {
        "title": "Notice of Termination",
        "section": "Part 3-2 Division 4",
        "summary": "Employer must give written notice; NES notice periods apply",
        "keywords": ["notice of termination", "written notice", "NES", "notice period"],
    },
    "s394": {
        "title": "Application for Remedy",
        "section": "Part 3-2 Division 4",
        "summary": "Application within 21 days; FWC may extend in exceptional circumstances",
        "keywords": ["application", "21 days", "lodgment", "extension", "exceptional circumstances"],
    },
}

# Query classification categories per playbook Part 5.1
QUERY_CATEGORIES = {
    "jurisdictional": {
        "description": "Threshold questions about whether FWC can hear the matter",
        "keywords": [
            "minimum employment period", "6 months", "12 months",
            "high income threshold", "small business", "10 employees",
            "21 days", "lodgment", "extension of time",
            "employee vs contractor", "casual employee",
            "eligible", "jurisdiction", "can I apply",
        ],
    },
    "statutory_criteria": {
        "description": "Application of s387 factors (harsh/unjust/unreasonable)",
        "keywords": [
            "s387", "valid reason", "notification", "response opportunity",
            "harsh", "unjust", "unreasonable", "small business HR",
            "size of business", "absence of HR", "other matters",
        ],
    },
    "analogous_facts": {
        "description": "Finding cases with similar facts",
        "keywords": [
            "cases where", "similar to", "example of", "decided that",
            "found unfair", "found not unfair", "social media",
            "misconduct", "performance", "conduct", "illness",
        ],
    },
    "procedural": {
        "description": "Process and procedure questions",
        "keywords": [
            "extension of time", "jurisdictional objection", "conciliation",
            "arbitration", "Full Bench", "lodge", "application",
            "process", "procedure", "how to", "step by step",
        ],
    },
}

# Key thresholds and amounts (update annually)
KEY_THRESHOLDS = {
    "high_income_threshold_2024": 175000,  # AUD per annum
    "high_income_threshold_2025": 175000,  # Update when published
    "minimum_employment_period": "6 months",
    "minimum_employment_period_small_business": "12 months",
    "lodgment_time_limit": "21 days",
    "maximum_compensation_weeks": 26,
    "small_business_definition": "fewer than 15 employees (or 10 for some purposes)",
}

# FWC metadata
FWC_METADATA = {
    "decisions_url": "https://www.fwc.gov.au/documents/decisionssigned/html/",
    "benchbook_url": "https://www.fwc.gov.au/education/fwc-benchbooks",
    "guidance_note_url": "https://www.fwc.gov.au/genai-guidance",
    "corpus_scope": "unfair dismissal only (s385-394 Fair Work Act 2009)",
    "date_range": "2019-2026",
}


def detect_query_category(question: str) -> str:
    """Classify query into category per playbook Part 5.1.
    
    Returns: "jurisdictional" | "statutory_criteria" | "analogous_facts" | "procedural" | "general"
    """
    q = question.lower()
    
    scores = {}
    for category, info in QUERY_CATEGORIES.items():
        score = sum(1 for kw in info["keywords"] if kw in q)
        scores[category] = score
    
    if not scores or max(scores.values()) == 0:
        return "general"
    
    return max(scores, key=scores.get)


def detect_provision(question: str) -> str:
    """Detect which Fair Work Act provision the question relates to."""
    q = question.lower()
    
    for section, info in FAIR_WORK_ACT_PROVISIONS.items():
        if any(kw in q for kw in info["keywords"]):
            return section
    
    return ""


def get_provision_info(section: str) -> dict:
    """Get information about a specific provision."""
    return FAIR_WORK_ACT_PROVISIONS.get(section, {})
