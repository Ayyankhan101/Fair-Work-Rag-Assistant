"""Filtered retriever for award-specific queries."""
import re
import json
from typing import List, Optional
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from config import AWARD_PATTERNS, TOPIC_KEYWORDS


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
        
        # Filter by award name
        award_docs = [
            doc for doc in self.all_docs
            if award_name.lower() in doc.metadata.get('award_name', '').lower()
        ]
        
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
                if re.search(r'\$\d+\.\d{2}', content_lower):
                    score += 5  # Has specific dollar amounts
                if any(term in content_lower for term in ['table', 'schedule', 'minimum rates', 'hourly rates', 'summary of']):
                    score += 3  # Rate table section
                if score > 0:
                    scored_docs.append((score, doc))
            
            scored_docs.sort(key=lambda x: x[0], reverse=True)
            
            if scored_docs:
                return [doc for _, doc in scored_docs[:20]]
        
        return award_docs[:20]
    
    def _general_topic_retrieval(self, query: str, topic_keywords: List[str]) -> List[Document]:
        """Retrieve documents for general topics without specific award.
        
        Improved scoring:
        - Exact phrase match = 5 points
        - Single keyword match = 1 point
        - Clause number presence = 2 bonus points
        - Percentage/number in content = 1 bonus point
        """
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
            if len(diverse_docs) >= 15:
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
        """Extract topic keywords from query."""
        q = query.lower()
        keywords = []
        for topic, words in TOPIC_KEYWORDS.items():
            if topic in q:
                keywords.extend(words)
        return list(set(keywords))
