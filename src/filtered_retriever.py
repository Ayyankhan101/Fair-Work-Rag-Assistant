"""Filtered retriever for unfair dismissal decisions with metadata filtering."""
import re
from typing import List, Optional
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document


def deduplicate_docs(docs: List[Document]) -> List[Document]:
    """Remove duplicate documents by content hash."""
    seen = set()
    unique = []
    for doc in docs:
        # Use first 500 chars for dedup to catch near-duplicates
        content_hash = hash(doc.page_content[:500])
        if content_hash not in seen:
            seen.add(content_hash)
            unique.append(doc)
    return unique


class UnfairDismissalRetriever(BaseRetriever):
    """Retriever for unfair dismissal decisions with metadata filtering.
    
    Per playbook Part 5.1: "Hybrid retrieval (top ~50) → Cross-encoder rerank (top ~8)"
    """
    base_retriever: BaseRetriever  # The underlying hybrid retriever
    reranker: Optional[object] = None  # Optional Cohere reranker
    
    # Filter defaults
    date_from: Optional[str] = None  # YYYY-MM-DD
    date_to: Optional[str] = None
    member: Optional[str] = None
    jurisdiction: Optional[str] = None
    claim_type: Optional[str] = None  # "unfair dismissal" | "general protections"
    outcome: Optional[str] = None  # "fair" | "unfair" | "reinstatement" | "compensation"
    
    class Config:
        arbitrary_types_allowed = True
    
    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager=None,
    ) -> List[Document]:
        """Retrieve with metadata filtering and optional reranking."""
        # Step 1: Base retrieval (hybrid BM25 + semantic)
        docs = self.base_retriever.get_relevant_documents(query)
        
        # Step 2: Metadata filtering
        docs = self._apply_filters(docs)
        
        # Step 3: Deduplicate
        docs = deduplicate_docs(docs)
        
        # Step 4: Optional reranking
        if self.reranker and len(docs) > 0:
            docs = self._rerank(query, docs)
        
        # Step 5: Limit to top N
        return docs[:20]
    
    def _apply_filters(self, docs: List[Document]) -> List[Document]:
        """Apply metadata filters to documents."""
        filtered = []
        for doc in docs:
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
            
            # Date filter
            if self.date_from:
                doc_date = metadata.get("decision_date", "")
                if doc_date and doc_date < self.date_from:
                    continue
            
            if self.date_to:
                doc_date = metadata.get("decision_date", "")
                if doc_date and doc_date > self.date_to:
                    continue
            
            # Member filter
            if self.member:
                doc_member = metadata.get("member", "").lower()
                if self.member.lower() not in doc_member:
                    continue
            
            # Jurisdiction filter
            if self.jurisdiction:
                doc_jurisdiction = metadata.get("jurisdiction", "").lower()
                if self.jurisdiction.lower() not in doc_jurisdiction:
                    continue
            
            # Claim type filter
            if self.claim_type:
                doc_claim = metadata.get("claim_type", "").lower()
                if self.claim_type.lower() not in doc_claim:
                    continue
            
            # Outcome filter
            if self.outcome:
                doc_outcome = metadata.get("outcome", "").lower()
                if self.outcome.lower() not in doc_outcome:
                    continue
            
            filtered.append(doc)
        
        return filtered
    
    def _rerank(self, query: str, docs: List[Document]) -> List[Document]:
        """Rerank documents using Cohere reranker."""
        try:
            # Prepare passages for reranking
            passages = [doc.page_content for doc in docs]
            
            # Rerank
            results = self.reranker.rerank(query, passages)
            
            # Sort by relevance score
            scored_docs = list(zip(docs, results))
            scored_docs.sort(key=lambda x: x[1].get("relevance_score", 0), reverse=True)
            
            return [doc for doc, _ in scored_docs]
        except Exception as e:
            # Fallback to original order if reranking fails
            print(f"Reranking failed: {e}")
            return docs
