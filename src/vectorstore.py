"""TurboVec vector store management for Fair Work Awards."""
import json
import os
from pathlib import Path
from fastembeddings import FastEmbedEmbeddings
from turbovec.langchain import TurboQuantVectorStore
from ingest import ingest_all


def get_embeddings() -> FastEmbedEmbeddings:
    """Initialize local fastembed embeddings (BAAI/bge-base-en-v1.5, 768-dim, ONNX)."""
    return FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")


def build_vectorstore(
    awards_dir: str,
    nes_path: str,
    store_dir: str,
    batch_size: int = 32,
    checkpoint_every_batches: int = 5,
) -> TurboQuantVectorStore:
    """Build TurboVec vector store from documents in resumable batches."""
    embeddings = get_embeddings()
    store_path = Path(store_dir)
    checkpoint_path = store_path / "build_checkpoint.json"

    docs = ingest_all(awards_dir, nes_path)
    print(f"\nBuilding TurboVec index with {len(docs)} documents...")
    os.makedirs(store_dir, exist_ok=True)

    start_idx = 0
    if (store_path / "index.tvim").exists() and (store_path / "docstore.json").exists():
        store = TurboQuantVectorStore.load(store_dir, embedding=embeddings)
        if checkpoint_path.exists():
            checkpoint = json.loads(checkpoint_path.read_text())
            start_idx = int(checkpoint.get("next_doc_idx", 0))
        print(f"Resuming existing store from doc {start_idx}/{len(docs)}")
    else:
        store = TurboQuantVectorStore(embedding=embeddings, bit_width=4)

    total_batches = (len(docs) + batch_size - 1) // batch_size
    start_batch = start_idx // batch_size
    for batch_no, batch_start in enumerate(range(start_idx, len(docs), batch_size), start=start_batch + 1):
        batch = docs[batch_start:batch_start + batch_size]
        store.add_documents(batch)
        next_idx = batch_start + len(batch)
        print(
            f"  Batch {batch_no}/{total_batches}: added {len(batch)} docs "
            f"(total {next_idx}/{len(docs)})",
            flush=True,
        )
        if batch_no % checkpoint_every_batches == 0 or next_idx == len(docs):
            store.dump(store_dir)
            checkpoint_path.write_text(
                json.dumps(
                    {
                        "next_doc_idx": next_idx,
                        "total_docs": len(docs),
                        "batch_size": batch_size,
                    },
                    indent=2,
                )
            )

    store.dump(store_dir)
    if checkpoint_path.exists():
        checkpoint_path.unlink()
    print(f"Vector store saved to {store_dir}")

    return store


def load_vectorstore(store_dir: str) -> TurboQuantVectorStore:
    """Load existing TurboVec vector store."""
    embeddings = get_embeddings()
    store = TurboQuantVectorStore.load(store_dir, embedding=embeddings)
    print(f"Vector store loaded from {store_dir}")
    return store


def search_store(store: TurboQuantVectorStore, query: str, k: int = 5, 
                 award_filter: str = None) -> list:
    """Search the vector store."""
    if award_filter:
        return store.similarity_search(query, k=k, filter={"award_name": award_filter})
    return store.similarity_search(query, k=k)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    awards_dir = "data/awards"
    nes_path = "data/nes/nes_combined.txt"
    store_dir = "data/vectorstore"

    # Check if store already exists
    if os.path.exists(os.path.join(store_dir, "index.tvim")):
        print("Loading existing vector store...")
        store = load_vectorstore(store_dir)
    else:
        print("Building new vector store...")
        store = build_vectorstore(awards_dir, nes_path, store_dir)

    # Test search
    test_queries = [
        "What is the minimum break under the Hospitality Award?",
        "What are overtime rules for casual employees?",
        "Annual leave entitlements",
    ]

    for query in test_queries:
        print(f"\n--- Query: {query} ---")
        results = search_store(store, query, k=3)
        for i, doc in enumerate(results):
            print(f"  {i+1}. [{doc.metadata['document_type']}] {doc.metadata['award_name']}")
            print(f"     Clause: {doc.metadata.get('clause_number', 'N/A')}")
            print(f"     Text: {doc.page_content[:100]}...")
