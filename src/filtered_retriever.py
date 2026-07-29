"""Filtered retriever for award-specific queries."""
import re
import json
from difflib import SequenceMatcher
from typing import List, Optional
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from config import AWARD_PATTERNS, TOPIC_KEYWORDS


def fuzzy_match(query: str, target: str, threshold: float = 0.6) -> float:
    """Fuzzy match ratio between query and target."""
    return SequenceMatcher(None, query.lower(), target.lower()).ratio()


def deduplicate_docs(docs: List[Document]) -> List[Document]:
    """Remove duplicate documents by content hash."""
    seen = set()
    unique = []
    for doc in docs:
        content_hash = hash(doc.page_content[:200])
        if content_hash not in seen:
            seen.add(content_hash)
            unique.append(doc)
    return unique


class AwardFilteredRetriever(BaseRetriever):
    """Retriever that filters by award name, then by topic keywords."""
    
    docstore_path: str = ""
    all_docs: List[Document] = []
    
    class Config:
        arbitrary_types_allowed = True
    
    def _load_docs(self):
        """Load all documents from docstore."""
        if self.all_docs:
            return
        
        with open(self.docstore_path) as f:
            docstore = json.load(f)
        
        for doc_id, doc in docstore['docs'].items():
            text = doc.get('text', '')
            metadata = doc.get('metadata', {})
            self.all_docs.append(Document(page_content=text, metadata=metadata))
    
    def _get_relevant_documents(self, query: str) -> List[Document]:
        """Retrieve documents filtered by award name or general topic."""
        self._load_docs()
        
        # Extract award name from query
        award_name = self._extract_award_name(query)
        
        # Extract topic keywords
        topic_keywords = self._extract_topic_keywords(query)
        
        # If no award specified but has topic, use general retrieval
        if not award_name and topic_keywords:
            return self._general_topic_retrieval(query, topic_keywords)
        
        if not award_name:
            return []
        
        # Filter by award name with fuzzy matching
        award_docs = []
        for doc in self.all_docs:
            doc_award = doc.metadata.get('award_name', '')
            # Exact match
            if award_name.lower() in doc_award.lower():
                award_docs.append(doc)
            # Fuzzy match — high threshold to avoid false positives (e.g. "Cleaning" matching "Telecommunications")
            elif fuzzy_match(award_name, doc_award) > 0.9:
                award_docs.append(doc)
        
        # Filter by topic keywords
        if topic_keywords:
            scored_docs = []
            for doc in award_docs:
                content_lower = doc.page_content.lower()
                score = sum(1 for kw in topic_keywords if kw in content_lower)
                # Bonus for clause numbers
                if doc.metadata.get('clause_number'):
                    score += 2
                # Bonus for rate tables (dollar amounts, schedules, tables)
                has_dollar = bool(re.search(r'\$\d+\.\d{2}', content_lower))
                has_level = bool(re.search(r'level\s+\d', content_lower))
                has_rate_table = any(term in content_lower for term in ['table', 'minimum rates', 'hourly rates', 'summary of'])
                
                if has_dollar:
                    score += 5
                if has_level:
                    score += 3
                if has_rate_table:
                    score += 3
                # Big bonus for rate table + dollar + level (actual rate data)
                if has_dollar and has_level:
                    score += 10
                # Bonus for "minimum hourly rate" or "minimum rate" phrases
                if 'minimum hourly rate' in content_lower or 'minimum rate' in content_lower:
                    score += 5
                if score > 0:
                    scored_docs.append((score, doc))
            
            scored_docs.sort(key=lambda x: x[0], reverse=True)
            
            if scored_docs:
                return deduplicate_docs([doc for _, doc in scored_docs[:30]])
        
        return deduplicate_docs(award_docs[:30])
    
    def _general_topic_retrieval(self, query: str, topic_keywords: List[str]) -> List[Document]:
        """Retrieve documents for general topics without specific award."""
        scored_docs = []
        for doc in self.all_docs:
            content_lower = doc.page_content.lower()
            award_name = doc.metadata.get('award_name', '').lower()
            
            score = 0
            # Exact phrase matching (higher weight)
            for kw in topic_keywords:
                if len(kw) > 3 and kw in content_lower:
                    score += 5  # Phrase match
                elif kw.split()[0] in content_lower:
                    score += 1  # Single word match
            
            # Bonus for clause numbers (more specific)
            if doc.metadata.get('clause_number'):
                score += 2
            
            # Bonus for specific numbers/percentages in content
            if re.search(r'\$\d+\.\d{2}', content_lower):
                score += 5  # Has specific dollar amounts
            elif re.search(r'\d+\s*%', content_lower):
                score += 2  # Has percentage rates
            if any(term in content_lower for term in ['table', 'schedule', 'minimum rates', 'hourly rates', 'summary of']):
                score += 3  # Rate table section
            
            # Boost for common awards (more likely to have general provisions)
            if any(common in award_name for common in ['hospitality', 'retail', 'cleaning', 'clerks']):
                score += 2
            
            if score > 0:
                scored_docs.append((score, doc))
        
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        
        # Return top docs from different awards for diversity
        seen_awards = set()
        diverse_docs = []
        for score, doc in scored_docs:
            award = doc.metadata.get('award_name', '')
            if award not in seen_awards or len(diverse_docs) < 5:
                diverse_docs.append(doc)
                seen_awards.add(award)
            if len(diverse_docs) >= 20:
                break
        
        return diverse_docs
    
    def _extract_award_name(self, query: str) -> Optional[str]:
        """Extract award name from query."""
        q = query.lower()
        for keyword, award_name in AWARD_PATTERNS.items():
            if keyword in q:
                return award_name
        return None
    
    def _extract_topic_keywords(self, query: str) -> List[str]:
        """Extract topic keywords from query — match topic name OR any keyword value."""
        q = query.lower()
        keywords = []
        for topic, words in TOPIC_KEYWORDS.items():
            if topic in q:
                keywords.extend(words)
            else:
                # Also check if any keyword phrase appears in the query
                for word in words:
                    if word in q:
                        keywords.extend(words)
                        break
        return list(set(keywords))
