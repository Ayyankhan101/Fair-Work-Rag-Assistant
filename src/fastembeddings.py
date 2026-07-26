"""FastEmbed embeddings wrapper for LangChain."""
from typing import List
from langchain_core.embeddings import Embeddings
from fastembed import TextEmbedding


class FastEmbedEmbeddings(Embeddings):
    """LangChain-compatible wrapper around fastembed (ONNX, no torch)."""

    def __init__(self, model_name: str = "BAAI/bge-base-en-v1.5"):
        self.model = TextEmbedding(model_name=model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [vec.tolist() for vec in self.model.embed(texts)]

    def embed_query(self, text: str) -> List[float]:
        return next(iter(self.model.embed([text]))).tolist()
