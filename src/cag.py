"""Cache-Augmented Generation (CAG) context cache for NES and high-frequency Award clauses."""
import os
from config import NES_KEYWORDS, TOPIC_KEYWORDS


# NES is always cached - it's small, stable, and universally relevant
NES_PATH = "data/nes/nes_combined.txt"

# High-frequency Award clauses to cache (from shared config)
CAG_KEYWORDS = NES_KEYWORDS + [
    "meal break", "rest break", "minimum break",
    "overtime", "penalty rates", "weekend",
    "allowance", "classification", "minimum rate",
    "notice period", "resignation",
]


class CAGCache:
    """Manages pre-loaded context for CAG path."""
    
    def __init__(self, nes_path: str = NES_PATH):
        self.nes_text = ""
        self._load_nes(nes_path)
    
    def _load_nes(self, nes_path: str):
        """Load NES text into cache."""
        if not os.path.exists(nes_path):
            print(f"WARNING: NES file not found: {nes_path}")
            return
        
        with open(nes_path) as f:
            raw_text = f.read()
        
        # Extract only the substantive content (skip navigation/boilerplate)
        lines = raw_text.split('\n')
        content_started = False
        content_lines = []
        
        # Navigation/boilerplate patterns to skip
        skip_patterns = [
            'skip to main', 'close', 'go to home', 'fair work ombuds',
            'translate', 'login', 'register', 'my account', 'resources',
            'log out', 'open search', 'popular searches', 'minimum wages',
            'annual leave', 'long service leave', 'on this page',
            'list of minimum', 'nes videos', 'who the nes', 'tools and',
            'related information', 'minimum entitlements for employees',
            'the national employment standards make up', 'other workplace',
            'award', 'enterprise agreement', 'a document between',
            'these also', 'employers have to give', 'fair work information',
            'casual employment information', 'the fwis', 'the ceis',
            'when they start', 'list of minimum nes entitlements',
            'automatic translation', 'our automatic translation',
            'select a language', 'professional translated',
            'default language is', 'english', 'arabic', 'bengali',
            'bosnian', 'bulgarian', 'chinese', 'croatian', 'czech',
            'danish', 'dutch', 'farsi', 'french', 'german', 'greek',
            'hebrew', 'hindi', 'hungarian', 'bahasa indonesia', 'italian',
            'japanese', 'korean', 'latvian', 'lithuanian', 'polish',
            'portuguese', 'romanian', 'russian', 'serbian', 'slovak',
            'slovene', 'spanish', 'swedish', 'thai', 'turkish',
            'ukrainian', 'vietnamese', 'language help',
        ]
        
        for line in lines:
            if "National Employment Standards" in line and not content_started:
                content_started = True
                continue
            if content_started:
                line_lower = line.strip().lower()
                # Skip navigation/boilerplate lines
                if any(skip in line_lower for skip in skip_patterns):
                    continue
                if line.strip():
                    content_lines.append(line.strip())
        
        self.nes_text = '\n'.join(content_lines)
        print(f"CAG: Loaded NES ({len(self.nes_text)} chars)")
    
    def get_nes_context(self) -> str:
        """Get pre-loaded NES context."""
        return self.nes_text
    
    def is_cag_candidate(self, question: str) -> bool:
        """Check if question is a CAG candidate (NES or high-frequency topic)."""
        question_lower = question.lower()
        return any(kw in question_lower for kw in CAG_KEYWORDS)
    
    def get_context(self, question: str) -> str:
        """Get CAG context for a question."""
        context_parts = []
        
        # Always include NES if question is NES-related
        if self.is_cag_candidate(question):
            nes_ctx = self.get_nes_context()
            if nes_ctx:
                context_parts.append(f"[National Employment Standards]\n{nes_ctx}")
        
        return "\n\n".join(context_parts)


def get_cag_cache() -> CAGCache:
    """Get or create CAG cache instance."""
    if not hasattr(get_cag_cache, '_instance'):
        get_cag_cache._instance = CAGCache()
    return get_cag_cache._instance
