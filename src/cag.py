"""Cache-Augmented Generation (CAG) for Fair Work Act s385-394 (Unfair Dismissal)."""
import os
from src.config import FAIR_WORK_ACT_PROVISIONS


# Fair Work Act is always cached - small, stable, universally relevant
FAIR_WORK_ACT_PATH = "data/legislation/fair_work_act_s385_394.txt"

# Key thresholds for quick lookup
KEY_THRESHOLDS = {
    "minimum_employment_period": "6 months (12 months for small business)",
    "small_business_definition": "fewer than 15 employees",
    "application_time_limit": "21 days after dismissal",
    "high_income_threshold": "$175,000 (2024-25)",
    "compensation_cap": "26 weeks pay or high income threshold (whichever less)",
}


class CAGCache:
    """Manages pre-loaded Fair Work Act context for CAG path."""
    
    def __init__(self, act_path: str = FAIR_WORK_ACT_PATH):
        self.act_text = ""
        self.provisions = {}
        self._load_act(act_path)
    
    def _load_act(self, act_path: str):
        """Load Fair Work Act text into cache."""
        if not os.path.exists(act_path):
            print(f"WARNING: Fair Work Act file not found: {act_path}")
            return
        
        with open(act_path, encoding='utf-8', errors='replace') as f:
            self.act_text = f.read()
        
        # Parse provisions into sections
        self._parse_provisions()
        
        print(f"CAG: Loaded Fair Work Act s385-394 ({len(self.act_text)} chars, {len(self.provisions)} sections)")
    
    def _parse_provisions(self):
        """Parse act text into individual sections."""
        current_section = None
        current_text = []
        
        for line in self.act_text.split('\n'):
            # Check for section header (e.g., "385  What is an unfair dismissal")
            stripped = line.strip()
            if stripped and stripped[0].isdigit() and '  ' in stripped:
                # Save previous section
                if current_section:
                    self.provisions[current_section] = '\n'.join(current_text)
                # Start new section
                parts = stripped.split('  ', 1)
                current_section = parts[0].strip()
                current_text = [parts[1] if len(parts) > 1 else ""]
            elif current_section:
                current_text.append(line)
        
        # Save last section
        if current_section:
            self.provisions[current_section] = '\n'.join(current_text)
    
    def get_act_context(self) -> str:
        """Get full Fair Work Act context."""
        return self.act_text
    
    def get_section(self, section_num: str) -> str:
        """Get a specific section."""
        return self.provisions.get(section_num, "")
    
    def is_cag_candidate(self, question: str) -> bool:
        """Check if question is a CAG candidate (unfair dismissal related)."""
        question_lower = question.lower()
        keywords = [
            "unfair dismissal", "unfairly dismissed", "dismissed",
            "harsh", "unjust", "unreasonable",
            "s385", "s386", "s387", "s388", "s389", "s390", "s391", "s392", "s393", "s394",
            "section 385", "section 386", "section 387", "section 388", "section 389",
            "section 390", "section 391", "section 392", "section 393", "section 394",
            "minimum employment period", "high income threshold",
            "small business", "21 days", "reinstatement", "compensation",
            "remedy", "application", "lodgment",
            "apply", "criteria", "criteria for", " unfair ", "dismissal",
            "employment", "terminated", "termination", "notice",
        ]
        return any(kw in question_lower for kw in keywords)
    
    def get_context(self, question: str) -> str:
        """Get CAG context for a question."""
        if not self.is_cag_candidate(question):
            return ""
        
        # Return full act text (it's small enough)
        return f"[Fair Work Act 2009 - Part 3-2 Division 4 - Unfair Dismissal]\n{self.act_text}"
    
    def get_threshold(self, key: str) -> str:
        """Get a key threshold value."""
        return KEY_THRESHOLDS.get(key, "")


def get_cag_cache() -> CAGCache:
    """Get or create CAG cache instance."""
    if not hasattr(get_cag_cache, '_instance'):
        get_cag_cache._instance = CAGCache()
    return get_cag_cache._instance
