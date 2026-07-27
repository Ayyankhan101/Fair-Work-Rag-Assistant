#!/usr/bin/env python3
"""Chunk PDFs and build vector store for RAG Document Assistant."""

import argparse
import json
import hashlib
from pathlib import Path

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_community.vectorstores import FAISS
    from langchain_core.embeddings import Embeddings
    from fastembed import TextEmbedding
except ImportError:
    print("Install dependencies: pip install langchain langchain-community faiss-cpu fastembed pypdf")
    exit(1)

PAPERS_DIR = Path(__file__).parent.parent / "papers"
DATA_DIR = Path(__file__).parent.parent / "data"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"

# Chunking config (from data contract)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
SEPARATORS = ["\n\n", "\n", ". ", " "]

# Embedding model
EMBED_MODEL = "BAAI/bge-small-en-v1.5"  # fastembed default, similar to all-MiniLM-L6-v2


class FastEmbeddings(Embeddings):
    """LangChain-compatible wrapper for fastembed."""

    def __init__(self, model_name: str = EMBED_MODEL):
        self._model = TextEmbedding(model_name=model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [list(e) for e in self._model.embed(texts)]

    def embed_query(self, text: str) -> list[float]:
        return list(self._model.embed([text]))[0]


def load_papers(papers_dir: Path, limit: int | None = None, papers: list[str] | None = None) -> list:
    """Load PDFs from papers directory."""
    documents = []
    if papers:
        pdf_files = [papers_dir / p for p in papers]
    else:
        pdf_files = sorted(papers_dir.glob("*.pdf"))
        if limit:
            pdf_files = pdf_files[:limit]

    print(f"Found {len(pdf_files)} PDFs")

    for pdf_path in pdf_files:
        print(f"  Loading {pdf_path.name}...")
        try:
            loader = PyPDFLoader(str(pdf_path))
            docs = loader.load()
            # Add arxiv_id metadata
            arxiv_id = pdf_path.stem.replace("_", "/")
            for doc in docs:
                doc.metadata["arxiv_id"] = arxiv_id
                doc.metadata["source"] = pdf_path.name
            documents.extend(docs)
            print(f"    -> {len(docs)} pages")
        except Exception as e:
            print(f"    -> ERROR: {e}")

    return documents


def chunk_documents(documents: list) -> list:
    """Split documents into chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=SEPARATORS,
        length_function=len,
    )

    chunks = splitter.split_documents(documents)
    print(f"Chunked {len(documents)} pages into {len(chunks)} chunks")

    # Add chunk IDs
    for i, chunk in enumerate(chunks):
        content = chunk.page_content
        chunk_id = hashlib.md5(content.encode()).hexdigest()[:12]
        chunk.metadata["chunk_id"] = f"chunk_{chunk_id}"
        chunk.metadata["chunk_index"] = i

    return chunks


def build_vector_store(chunks: list, batch_size: int = 64):
    """Build FAISS vector store from chunks, embedding in batches."""
    from langchain_core.documents import Document

    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Loading embedding model: {EMBED_MODEL}...")
    embeddings = FastEmbeddings(model_name=EMBED_MODEL)

    total = len(chunks)
    vector_store = None
    for i in range(0, total, batch_size):
        batch = chunks[i : i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (total + batch_size - 1) // batch_size
        print(f"  Batch {batch_num}/{total_batches} ({len(batch)} chunks)...")

        docs = [
            Document(page_content=c.page_content, metadata=c.metadata)
            for c in batch
        ]

        if vector_store is None:
            vector_store = FAISS.from_documents(docs, embeddings)
        else:
            vector_store.add_documents(docs)

        print(f"    Done. Total vectors: {vector_store.index.ntotal}")

    # Save
    vector_store.save_local(str(VECTOR_STORE_DIR))
    print(f"Vector store saved to {VECTOR_STORE_DIR}")

    # Stats
    index_size = sum(f.stat().st_size for f in VECTOR_STORE_DIR.iterdir()) / (1024 * 1024)
    print(f"Index size: {index_size:.1f} MB")

    return vector_store


def generate_manifest(chunks: list):
    """Generate chunk manifest for Model Engineer."""
    manifest_path = DATA_DIR / "chunk_manifest.json"

    manifest = {
        "total_chunks": len(chunks),
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "embedding_model": EMBED_MODEL,
        "sources": {},
        "chunks": [],
    }

    # Count by source
    for chunk in chunks:
        src = chunk.metadata.get("source", "unknown")
        manifest["sources"][src] = manifest["sources"].get(src, 0) + 1

    # Sample chunks (first 5 for verification)
    for chunk in chunks[:5]:
        manifest["chunks"].append({
            "chunk_id": chunk.metadata.get("chunk_id"),
            "source": chunk.metadata.get("source"),
            "arxiv_id": chunk.metadata.get("arxiv_id"),
            "preview": chunk.page_content[:200] + "...",
        })

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Manifest saved to {manifest_path}")
    print(f"Sources: {json.dumps(manifest['sources'], indent=2)}")


def main():
    parser = argparse.ArgumentParser(description="Chunk PDFs and build FAISS vector store")
    parser.add_argument("--limit", type=int, default=None, help="Process only first N papers")
    parser.add_argument("--papers", nargs="+", default=None, help="Specific paper filenames to process")
    parser.add_argument("--batch-size", type=int, default=64, help="Chunks per embedding batch (default: 64)")
    args = parser.parse_args()

    print("=" * 60)
    print("RAG Pipeline — Chunk & Embed")
    print("=" * 60)

    # Step 1: Load
    print("\n[1] Loading PDFs...")
    documents = load_papers(PAPERS_DIR, limit=args.limit, papers=args.papers)
    print(f"Total pages: {len(documents)}")

    # Step 2: Chunk
    print("\n[2] Chunking documents...")
    chunks = chunk_documents(documents)

    # Step 3: Embed + Index
    print("\n[3] Building vector store...")
    vector_store = build_vector_store(chunks, batch_size=args.batch_size)

    # Step 4: Manifest
    print("\n[4] Generating manifest...")
    generate_manifest(chunks)

    print("\n" + "=" * 60)
    print("Pipeline complete.")
    print(f"Vector store: {VECTOR_STORE_DIR}")
    print(f"Ready for Model Engineer.")
    print("=" * 60)


if __name__ == "__main__":
    main()
