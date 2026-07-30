"""Hybrid retriever combining BM25 + Semantic search with RRF."""
from typing import List
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from bm25_retriever import BM25Retriever


class HybridRetriever(BaseRetriever):
    """Hybrid retriever using BM25 + Semantic with RRF fusion."""
    
    bm25_retriever: BM25Retriever = None
    semantic_retriever: BaseRetriever = None
    k: int = 20  # Number of results to retrieve from each
    rrf_k: int = 60  # RRF constant
    
    class Config:
        arbitrary_types_allowed = True
    
    def _reciprocal_rank_fusion(self, ranked_lists: List[List[Document]]) -> List[Document]:
        """Fuse multiple ranked lists using Reciprocal Rank Fusion."""
        doc_scores = {}
        doc_map = {}
        
        for ranked_list in ranked_lists:
            for rank, doc in enumerate(ranked_list):
                # Create a unique key based on content hash
                doc_key = hash(doc.page_content)
                
                if doc_key not in doc_scores:
                    doc_scores[doc_key] = 0.0
                    doc_map[doc_key] = doc
                
                # RRF score: 1 / (k + rank)
                doc_scores[doc_key] += 1.0 / (self.rrf_k + rank + 1)
        
        # Sort by fusion score
        sorted_keys = sorted(doc_scores.keys(), key=lambda k: doc_scores[k], reverse=True)
        
        return [doc_map[key] for key in sorted_keys[:self.k]]
    
    def _get_relevant_documents(self, query: str) -> List[Document]:
        """Retrieve documents using hybrid search."""
        results = []
        
        # BM25 search
        if self.bm25_retriever:
            bm25_results = self.bm25_retriever.invoke(query)
            results.append(bm25_results[:self.k])
        
        # Semantic search
        if self.semantic_retriever:
            semantic_results = self.semantic_retriever.invoke(query)
            results.append(semantic_results[:self.k])
        
        if not results:
            return []
        
        if len(results) == 1:
            return results[0][:self.k]
        
        # Fuse using RRF
        return self._reciprocal_rank_fusion(results)
