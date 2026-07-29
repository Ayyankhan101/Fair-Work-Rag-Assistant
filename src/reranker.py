"""Reranker for improving retrieval quality using Cohere."""
import os
from typing import List
from langchain_core.documents import Document


class CohereReranker:
    """Rerank documents using Cohere's rerank API."""
    
    def __init__(self, model: str = "rerank-english-v3.0"):
        self.model = model
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            try:
                import cohere
                from dotenv import load_dotenv
                load_dotenv()
                api_key = os.getenv("COHERE_API_KEY")
                if not api_key:
                    raise ValueError("COHERE_API_KEY not set")
                self._client = cohere.Client(api_key)
            except ImportError:
                raise ImportError("Install cohere: pip install cohere")
        return self._client
    
    def rerank(
        self,
        query: str,
        documents: List[Document],
        top_n: int = 10,
    ) -> List[Document]:
        """Rerank documents by relevance to query."""
        if not documents:
            return []
        
        docs_text = [doc.page_content for doc in documents]
        
        results = self.client.rerank(
            query=query,
            documents=docs_text,
            top_n=min(top_n, len(documents)),
            model=self.model,
            return_documents=True,
        )
        
        reranked = []
        for result in results.results:
            original_doc = documents[result.index]
            reranked.append(Document(
                page_content=original_doc.page_content,
                metadata={
                    **original_doc.metadata,
                    "relevance_score": result.relevance_score,
                },
            ))
        
        return reranked


def _simple_rerank(query: str, documents: List[Document], top_n: int) -> List[Document]:
    """Simple keyword-based reranker fallback when Cohere is unavailable."""
    import re
    q = query.lower()
    scored = []
    for doc in documents:
        text = doc.page_content.lower()
        score = 0
        # Exact phrase matches from query
        for word in q.split():
            if len(word) > 2 and word in text:
                score += 1
        # Bonus for dollar amounts + level patterns (rate tables)
        if re.search(r'\$\d+\.\d{2}', text):
            score += 3
        if re.search(r'level\s+\d', text):
            score += 2
        # Bonus for rate-related terms
        if any(t in text for t in ['minimum hourly rate', 'minimum rate', 'hourly rate']):
            score += 3
        if any(t in text for t in ['schedule b', 'schedule of rates', 'summary of hourly']):
            score += 2
        scored.append((score, doc))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_n]]


def rerank_documents(
    query: str,
    documents: List[Document],
    top_n: int = 10,
    use_cohere: bool = True,
) -> List[Document]:
    """Convenience function to rerank documents.
    
    Uses Cohere if available, falls back to keyword-based reranking.
    """
    if not use_cohere or not os.getenv("COHERE_API_KEY"):
        return _simple_rerank(query, documents, top_n)
    
    try:
        reranker = CohereReranker()
        return reranker.rerank(query, documents, top_n)
    except Exception as e:
        print(f"Cohere reranking failed, using keyword fallback: {e}")
        return _simple_rerank(query, documents, top_n)
