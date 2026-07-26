"""Shared configuration: award patterns, topic keywords, NES keywords."""

# Award name patterns — single source of truth
AWARD_PATTERNS = {
    "cleaning": "Cleaning Services Award 2020",
    "cleaner": "Cleaning Services Award 2020",
    "hospitality": "Hospitality Industry (General) Award 2020",
    "hotel": "Hospitality Industry (General) Award 2020",
    "clerk": "Clerks—Private Sector Award 2020",
    "clerks": "Clerks—Private Sector Award 2020",
    "payroll officer": "Clerks—Private Sector Award 2020",
    "payroll": "Clerks—Private Sector Award 2020",
    "retail": "General Retail Industry Award 2020",
    "fast food": "Fast Food Industry Award 2020",
    "restaurant": "Restaurant Industry Award 2020",
    "professional employee": "Professional Employees Award 2020",
    "software engineer": "Professional Employees Award 2020",
    "architect": "Architects Award 2020",
    "architects": "Architects Award 2020",
    "hair and beauty": "Hair and Beauty Industry Award 2020",
    "hairdresser": "Hair and Beauty Industry Award 2020",
    "marine": "Marine Tourism and Charter Vessels Award 2020",
    "charter vessel": "Marine Tourism and Charter Vessels Award 2020",
    "sporting": "Sporting Organisations Award 2020",
    "sport": "Sporting Organisations Award 2020",
    "animal care": "Animal Care and Veterinary Services Award 2020",
    "veterinary": "Animal Care and Veterinary Services Award 2020",
    "aquaculture": "Aquaculture Industry Award 2020",
    "cotton": "Cotton Ginning Award 2020",
    "black coal": "Black Coal Mining Industry Award 2020",
    "mining": "Black Coal Mining Industry Award 2020",
    "aluminium": "Aluminium Industry Award 2020",
    "steel": "Steel Industry Award 2020",
    "waste": "Waste Management Award 2020",
    "local government": "Local Government Industry Award 2020",
    "nursing": "Nursing Award 2020",
    "health": "Health Professionals and Support Services Award 2020",
    "ambulance": "Ambulance Industry Award 2020",
    "education": "Educational Services (Schools) General Staff Award 2020",
    "child care": "Children's Services Award 2020",
    "social and community": "Social, Community, Home Care and Disability Services Award 2020",
    "disability": "Social, Community, Home Care and Disability Services Award 2020",
    "wages": "General minimum wage",
    "minimum wage": "General minimum wage",
}

# Topic keywords for general questions
TOPIC_KEYWORDS = {
    "overtime": ["overtime", "overtime rate", "overtime pay", "overtime hours"],
    "penalty": ["penalty rate", "penalties", "weekend penalty", "penalty rates"],
    "break": ["meal break", "rest break", "break entitlement", "breaks"],
    "leave": ["leave entitlement", "annual leave", "personal leave", "sick leave", "carer's leave", "long service leave", "parental leave"],
    "casual": ["casual employee", "casual loading", "casual rate", "casual conversion"],
    "notice": ["notice of termination", "notice period", "resignation", "termination"],
    "allowance": ["allowance", "allowances", "payment", "travel allowance", "uniform allowance"],
    "hours": ["hours of work", "maximum hours", "weekly hours", "ordinary hours", "span of hours"],
    "public holiday": ["public holiday", "public holidays", "holiday penalty"],
    "weekend": ["saturday", "sunday", "weekend work", "weekend penalty"],
    "roster": ["roster", "rostering", "roster cycle", "roster pattern"],
    "junior": ["junior employee", "junior rate", "under 18", "apprentice"],
    "apprentice": ["apprentice", "apprenticeship", "trainee"],
    "wages": ["hourly rate", "minimum wage", "pay rate", "salary", "wage"],
    "redundancy": ["redundancy", "redundant", "redundancy pay"],
    "transfer": ["transfer", "transfer of business", "transfer of employment"],
    "unfair dismissal": ["unfair dismissal", "dismissal", "termination of employment"],
    "consultation": ["consultation", "consultation requirement", "redundancy consultation"],
    "record keeping": ["record", "time and wages", "pay slip", "record keeping"],
}

# NES keywords — questions about these always use CAG or Combined
NES_KEYWORDS = [
    "nes", "national employment standards",
    "leave entitlement", "annual leave", "personal leave",
    "parental leave", "notice of termination", "redundancy",
    "public holiday", "maximum weekly hours", "flexible working",
    "casual employment", "community service leave", "long service leave",
    "superannuation",
]


def detect_award(question: str):
    """Detect award name from question text. Returns award name or None."""
    q = question.lower()
    for keyword, award_name in AWARD_PATTERNS.items():
        if keyword in q:
            return award_name
    return None


def detect_topic(question: str):
    """Detect topic from question text. Returns topic name or None."""
    q = question.lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw in q for kw in keywords):
            return topic
    return None


def has_nes_keywords(question: str) -> bool:
    """Check if question mentions NES-related content."""
    q = question.lower()
    return any(kw in q for kw in NES_KEYWORDS)
