"""Shared configuration: award patterns, topic keywords, NES keywords."""

# Award name patterns — single source of truth
AWARD_PATTERNS = {
    "cleaning": "Cleaning Services Award 2020",
    "cleaner": "Cleaning Services Award 2020",
    "hospitality": "Hospitality Industry (General) Award 2020",
    "hotel": "Hospitality Industry (General) Award 2020",
    "clerk": "Clerks—Private Sector Award 2010",
    "clerks": "Clerks—Private Sector Award 2010",
    "private sector clerks": "Clerks—Private Sector Award 2010",
    "payroll officer": "Clerks—Private Sector Award 2010",
    "payroll": "Clerks—Private Sector Award 2010",
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
    "nurse": "Nursing Award 2020",
    "health": "Health Professionals and Support Services Award 2020",
    "hospital": "Health Professionals and Support Services Award 2020",
    "ambulance": "Ambulance Industry Award 2020",
    "education": "Educational Services (Schools) General Staff Award 2020",
    "school": "Educational Services (Schools) General Staff Award 2020",
    "child care": "Children's Services Award 2010",
    "childcare": "Children's Services Award 2010",
    "children's services": "Children's Services Award 2010",
    "aged care": "Aged Care Award 2010",
    "agedcare": "Aged Care Award 2010",
    "social and community": "Social, Community, Home Care and Disability Services Award 2020",
    "disability": "Social, Community, Home Care and Disability Services Award 2020",
    "community": "Social, Community, Home Care and Disability Services Award 2020",
    "home care": "Social, Community, Home Care and Disability Services Award 2020",
    "wages": "General minimum wage",
    "minimum wage": "General minimum wage",
    "airline": "Airline Operations—Ground Staff Award 2020",
    "airport": "Airport Employees Award 2020",
    "banking": "Banking, Finance and Insurance Award 2020",
    "finance": "Banking, Finance and Insurance Award 2020",
    "insurance": "Banking, Finance and Insurance Award 2020",
    "building": "Building and Construction General On-site Award 2020",
    "construction": "Building and Construction General On-site Award 2020",
    "electrical": "Electrical, Electronic and Communications Contracting Award 2020",
    "plumbing": "Plumbing and Fire Sprinklers Award 2020",
    "gardening": "Gardening and Landscaping Services Award 2020",
    "landscaping": "Gardening and Landscaping Services Award 2020",
    "graphic arts": "Graphic Arts, Printing and Publishing Award 2020",
    "printing": "Graphic Arts, Printing and Publishing Award 2020",
    "publishing": "Graphic Arts, Printing and Publishing Award 2020",
    "higher education": "Higher Education Industry-Academic Staff-Award 2020",
    "university": "Higher Education Industry-Academic Staff-Award 2020",
    "pharmacy": "Pharmacy Industry Award 2020",
    "telecommunications": "Telecommunications Services Award 2020",
    "truck": "Road Transport and Distribution Award 2020",
    "transport": "Road Transport and Distribution Award 2020",
    "distribution": "Road Transport and Distribution Award 2020",
    "security": "Security Services Industry Award 2020",
    "textile": "Textile, Clothing, Footwear and Associated Industries Award 2020",
    "clothing": "Textile, Clothing, Footwear and Associated Industries Award 2020",
    "footwear": "Textile, Clothing, Footwear and Associated Industries Award 2020",
    "manufacturing": "Manufacturing and Associated Industries and Occupations Award 2020",
    "warehousing": "Warehousing, Storage and Distribution Award 2020",
    "wine": "Wine Industry Award 2020",
    "sugar": "Sugar Industry Award 2020",
    "port": "Port Authorities Award 2020",
    "pilot": "Air Pilots Award 2020",
    "flight attendant": "Aircraft Cabin Crew Award 2020",
    "cabin crew": "Aircraft Cabin Crew Award 2020",
    "fitness": "Fitness Industry Award 2020",
    "gym": "Fitness Industry Award 2020",
    "funeral": "Funeral Industry Award 2020",
    "cemetery": "Cemetery Industry Award 2020",
    "broadcasting": "Broadcasting, Recorded Entertainment and Cinemas Award 2020",
    "cinema": "Broadcasting, Recorded Entertainment and Cinemas Award 2020",
    "events": "Amusement, Events and Recreation Award 2020",
    "recreation": "Amusement, Events and Recreation Award 2020",
    "amusement": "Amusement, Events and Recreation Award 2020",
    "asphalt": "Asphalt Industry Award 2020",
    "cement": "Cement, Lime and Quarrying Award 2020",
    "quarrying": "Cement, Lime and Quarrying Award 2020",
    "concrete": "Concrete Products Award 2020",
    "dredging": "Dredging Industry Award 2020",
    "dry cleaning": "Dry Cleaning and Laundry Industry Award 2020",
    "laundry": "Dry Cleaning and Laundry Industry Award 2020",
    "fire fighting": "Fire Fighting Industry Award 2020",
    "firefighter": "Fire Fighting Industry Award 2020",
    "gas": "Gas Industry Award 2020",
    "corrections": "Corrections and Detention (Private Sector) Award 2020",
    "detention": "Corrections and Detention (Private Sector) Award 2020",
    "call centre": "Contract Call Centres Award 2020",
    "call center": "Contract Call Centres Award 2020",
    "business equipment": "Business Equipment Award 2020",
    "commercial sales": "Commercial Sales Award 2020",
    "coal export": "Coal Export Terminals Award 2020",
    "book": "Book Industry Award 2020",
    "alpine": "Alpine Resorts Award 2020",
    "aboriginal": "Aboriginal and Torres Strait Islander Health Workers and Practitioners Award 2020",
    "government": "Australian Government Industry Award 2016",
    "federal government": "Australian Government Industry Award 2016",
    "power": "Electrical Power Industry Award 2020",
    "electricity": "Electrical Power Industry Award 2020",
    "post-secondary": "Educational Services (Post-Secondary Education) Award 2020",
    "tertiary": "Educational Services (Post-Secondary Education) Award 2020",
    "teachers": "Educational Services (Teachers) Award 2020",
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
