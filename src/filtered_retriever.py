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


def _is_rate_query(query: str) -> bool:
    """Check if query is about pay rates/salary."""
    q = query.lower()
    rate_terms = ['rate', 'salary', 'pay', 'wage', 'earnings', 'income', 'hourly', 'per hour', 'per week', 'per year', 'annum']
    return any(term in q for term in rate_terms)


def _is_clause_query(query: str) -> bool:
    """Check if query is about rules/entitlements/hours (not rates)."""
    q = query.lower()
    clause_terms = [
        'consecutive', 'maximum', 'minimum', 'hours', 'overtime', 'break', 'rest',
        'roster', 'penalty', 'loading', 'leave', 'notice', 'termination',
        'probation', 'casual', 'junior', 'engagement', 'entitled', 'entitlement',
        'can an employee', 'how many', 'what is the maximum', 'what is the minimum',
        'days off', 'day off', 'public holiday', 'annual leave', 'parental',
    ]
    return any(term in q for term in clause_terms)


def _is_rostering_query(query: str) -> bool:
    """Check if query is about rostering/scheduling."""
    q = query.lower()
    roster_terms = ['roster', 'rostering', 'consecutive', 'days off', 'shift', 'spread', 'span', 'daily hours']
    return any(term in q for term in roster_terms)


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
        
        # Extract key terms from query for direct content matching
        query_terms = self._extract_query_terms(query)
        
        # If no award specified but has topic, use general retrieval
        if not award_name and (topic_keywords or query_terms):
            return self._general_topic_retrieval(query, topic_keywords or query_terms)
        
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
        
        # Filter by topic keywords or query terms
        if topic_keywords or query_terms:
            # Detect query intent for scoring adjustments
            is_rate_q = _is_rate_query(query)
            is_clause_q = _is_clause_query(query)
            is_roster_q = _is_rostering_query(query)
            
            scored_docs = []
            for doc in award_docs:
                content_lower = doc.page_content.lower()
                
                # Score from topic keywords
                score = sum(2 for kw in topic_keywords if kw in content_lower)
                
                # Score from direct query term matches (high signal)
                for qt in query_terms:
                    if qt in content_lower:
                        score += 3
                
                # Bonus for clause numbers (more specific = better)
                clause_num = doc.metadata.get('clause_number', '')
                if clause_num:
                    score += 3
                
                # Rate table detection
                has_dollar = bool(re.search(r'\$\d+\.\d{2}', content_lower))
                has_level = bool(re.search(r'level\s+\d', content_lower))
                has_rate_table = any(term in content_lower for term in ['table', 'minimum rates', 'hourly rates', 'summary of'])
                
                # Penalty for rate table content in clause/rostering queries
                if is_clause_q or is_roster_q:
                    if has_rate_table:
                        score -= 3  # Penalize rate tables for clause queries
                    if has_dollar and has_level:
                        score -= 5  # Heavily penalize rate data for clause queries
                    # Boost clause-level operational content
                    if any(term in content_lower for term in ['must not', 'must roster', 'maximum number', 'minimum number', 'ordinary hours', 'consecutive']):
                        score += 5
                    # Boost rostering-specific content
                    if is_roster_q and any(term in content_lower for term in ['roster', 'consecutive', 'days off', 'daily hours', 'spread of hours']):
                        score += 5
                else:
                    # Rate query — boost rate tables
                    if has_dollar:
                        score += 5
                    if has_level:
                        score += 3
                    if has_rate_table:
                        score += 3
                    if has_dollar and has_level:
                        score += 10
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
    
    def _extract_query_terms(self, query: str) -> List[str]:
        """Extract key terms from query for direct content matching."""
        q = query.lower()
        # Stop words to ignore
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                      'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                      'should', 'may', 'might', 'can', 'shall', 'to', 'of', 'in', 'for',
                      'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during',
                      'before', 'after', 'above', 'below', 'between', 'under', 'again',
                      'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
                      'how', 'all', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
                      'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
                      'too', 'very', 'just', 'because', 'but', 'and', 'or', 'if', 'while',
                      'about', 'against', 'up', 'down', 'out', 'off', 'over', 'under'}
        
        # Extract meaningful terms (>=3 chars, not stop words)
        words = re.findall(r'\b[a-z]{3,}\b', q)
        terms = [w for w in words if w not in stop_words]
        
        # Also extract key phrases (2-word combinations)
        phrases = []
        word_list = re.findall(r'\b[a-z]+\b', q)
        for i in range(len(word_list) - 1):
            if word_list[i] not in stop_words and word_list[i+1] not in stop_words:
                phrases.append(f"{word_list[i]} {word_list[i+1]}")
        
        return list(set(terms + phrases))
