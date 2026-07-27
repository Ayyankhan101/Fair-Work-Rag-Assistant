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


def rerank_documents(
    query: str,
    documents: List[Document],
    top_n: int = 10,
    use_cohere: bool = True,
) -> List[Document]:
    """Convenience function to rerank documents.
    
    Falls back to original order if Cohere unavailable.
    """
    if not use_cohere or not os.getenv("COHERE_API_KEY"):
        return documents[:top_n]
    
    try:
        reranker = CohereReranker()
        return reranker.rerank(query, documents, top_n)
    except Exception as e:
        print(f"Reranking failed, using original order: {e}")
        return documents[:top_n]
