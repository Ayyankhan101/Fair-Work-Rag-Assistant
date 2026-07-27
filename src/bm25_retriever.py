"""BM25 retriever for hybrid search."""
import json
from rank_bm25 import BM25Okapi
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from typing import List


class BM25Retriever(BaseRetriever):
    """BM25 retriever using rank_bm25."""
    
    bm25: BM25Okapi = None
    docs: List[Document] = []
    tokenized_corpus: List[List[str]] = []
    
    class Config:
        arbitrary_types_allowed = True
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple whitespace + lowercase tokenization."""
        return text.lower().split()
    
    def _build_index(self, documents: List[Document]):
        """Build BM25 index from documents."""
        self.docs = documents
        self.tokenized_corpus = [self._tokenize(doc.page_content) for doc in documents]
        self.bm25 = BM25Okapi(self.tokenized_corpus)
    
    def _get_relevant_documents(self, query: str) -> List[Document]:
        """Retrieve top-k documents using BM25."""
        if self.bm25 is None:
            return []
        
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top-k indices
        k = min(15, len(self.docs))
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        
        return [self.docs[i] for i in top_indices]


def build_bm25_retriever_from_docstore(docstore_path: str) -> BM25Retriever:
    """Build BM25 retriever from docstore.json."""
    with open(docstore_path) as f:
        docstore = json.load(f)
    
    docs = []
    for doc_id, doc in docstore['docs'].items():
        text = doc.get('text', '')
        metadata = doc.get('metadata', {})
        docs.append(Document(page_content=text, metadata=metadata))
    
    retriever = BM25Retriever()
    retriever._build_index(docs)
    
    return retriever
