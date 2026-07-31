"""Cache-Augmented Generation (CAG) context cache for NES and high-frequency Award clauses."""
import os
from config import NES_KEYWORDS


# NES is always cached - it's small, stable, and universally relevant
NES_PATH = "data/nes/nes_combined.txt"

# NES topic segments for targeted retrieval (DEF-067: avoid sending full NES)
NES_TOPIC_SEGMENTS = {
    "annual leave": ["annual leave", "4 weeks", "20 days", "leave loading"],
    "personal leave": ["personal leave", "sick leave", "carer's leave", "2 days", "10 days"],
    "parental leave": ["parental leave", "unpaid parental", "12 months", "52 weeks", "parental"],
    "notice of termination": ["notice of termination", "notice period", "weeks notice"],
    "redundancy": ["redundancy", "redundancy pay", "severance", "genuine redundancy"],
    "public holiday": ["public holiday", "public holidays", "national public holiday"],
    "maximum weekly hours": ["maximum weekly hours", "38 hours", "average hours", "flexible working"],
    "casual employment": ["casual employment", "casual conversion", "casual entitlement"],
    "community service leave": ["community service leave", "jury duty", "jury service", "volunteer"],
    "long service leave": ["long service leave", "long service", "service leave"],
    "superannuation": ["superannuation", "super guarantee", "SG", "retirement"],
    "family domestic violence": ["family and domestic violence", "domestic violence", "family violence"],
    "fair work information": ["fair work information statement", "FWIS", "casual employment information", "CEIS"],
}

# High-frequency Award clauses to cache (from shared config)
CAG_KEYWORDS = NES_KEYWORDS + [
    "meal break", "rest break", "minimum break",
    "overtime", "penalty rates", "weekend",
    "allowance", "classification", "minimum rate",
    "notice period", "resignation",
]


class CAGCache:
    """Manages pre-loaded context for CAG path.
    
    DEF-067: Segment NES by topic to reduce context size.
    """
    
    def __init__(self, nes_path: str = NES_PATH):
        self.nes_text = ""
        self.nes_segments = {}
        self._load_nes(nes_path)
    
    def _load_nes(self, nes_path: str):
        """Load NES text into cache with explicit UTF-8 encoding."""
        if not os.path.exists(nes_path):
            print(f"WARNING: NES file not found: {nes_path}")
            return
        
        # DEF-061: Always read with explicit UTF-8
        with open(nes_path, encoding='utf-8', errors='replace') as f:
            raw_text = f.read()
        
        lines = raw_text.split('\n')
        content_started = False
        content_lines = []
        
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
                if any(skip in line_lower for skip in skip_patterns):
                    continue
                if line.strip():
                    content_lines.append(line.strip())
        
        self.nes_text = '\n'.join(content_lines)
        
        # DEF-067: Build topic segments from full NES text
        self._build_segments()
        
        print(f"CAG: Loaded NES ({len(self.nes_text)} chars, {len(self.nes_segments)} segments)")
    
    def _build_segments(self):
        """Build topic-specific NES segments for targeted retrieval."""
        self.nes_text.lower()
        for topic, keywords in NES_TOPIC_SEGMENTS.items():
            relevant_lines = []
            for line in self.nes_text.split('\n'):
                line_lower = line.lower()
                if any(kw in line_lower for kw in keywords):
                    relevant_lines.append(line)
            if relevant_lines:
                self.nes_segments[topic] = '\n'.join(relevant_lines)
    
    def get_nes_context(self) -> str:
        """Get pre-loaded NES context."""
        return self.nes_text
    
    def is_cag_candidate(self, question: str) -> bool:
        """Check if question is a CAG candidate (NES or high-frequency topic)."""
        question_lower = question.lower()
        return any(kw in question_lower for kw in CAG_KEYWORDS)
    
    def _find_relevant_segment(self, question: str) -> str:
        """Find the most relevant NES segment for a question."""
        question_lower = question.lower()
        best_topic = None
        best_score = 0
        
        for topic, keywords in NES_TOPIC_SEGMENTS.items():
            score = sum(1 for kw in keywords if kw in question_lower)
            if score > best_score:
                best_score = score
                best_topic = topic
        
        if best_topic and best_topic in self.nes_segments:
            return self.nes_segments[best_topic]
        return ""
    
    def get_context(self, question: str) -> str:
        """Get CAG context for a question.
        
        DEF-067: Use segmented retrieval to reduce context size.
        """
        context_parts = []
        
        if self.is_cag_candidate(question):
            # DEF-067: Try topic-specific segment first
            segment = self._find_relevant_segment(question)
            if segment and len(segment) < len(self.nes_text) * 0.5:
                context_parts.append(f"[National Employment Standards - Specific Topic]\n{segment}")
            else:
                # Fall back to full NES if no good segment match
                nes_ctx = self.get_nes_context()
                if nes_ctx:
                    context_parts.append(f"[National Employment Standards]\n{nes_ctx}")
        
        return "\n\n".join(context_parts)


def get_cag_cache() -> CAGCache:
    """Get or create CAG cache instance."""
    if not hasattr(get_cag_cache, '_instance'):
        get_cag_cache._instance = CAGCache()
    return get_cag_cache._instance
