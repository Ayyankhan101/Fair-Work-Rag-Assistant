#!/usr/bin/env python3
"""Build vector store from markdown files (fast) or PDFs (slow)."""
import os
import pickle
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from fastembeddings import FastEmbedEmbeddings
from turbovec.langchain import TurboQuantVectorStore

start = time.time()
CACHE_PATH = Path("data/docs_cache.pkl")
STORE_DIR = Path("data/vectorstore")
CHECKPOINT_PATH = STORE_DIR / "build_checkpoint.json"
BATCH_SIZE = int(os.getenv("VECTORSTORE_BATCH_SIZE", "16"))
CHECKPOINT_EVERY_BATCHES = int(os.getenv("VECTORSTORE_CHECKPOINT_EVERY", "5"))

# Use markdown if available, otherwise PDFs
MD_DIR = Path("data/md_awards")
USE_MD = MD_DIR.exists() and len(list(MD_DIR.glob("*.md"))) > 100

if CACHE_PATH.exists():
    print("Step 1: Loading cached docs...", flush=True)
    with CACHE_PATH.open("rb") as f:
        docs = pickle.load(f)
    print(f"  Loaded {len(docs)} cached chunks in {time.time()-start:.0f}s", flush=True)
elif USE_MD:
    print("Step 1: Ingesting from markdown (fast)...", flush=True)
    from scripts.ingest_markdown import ingest_from_md
    docs = ingest_from_md(str(MD_DIR))
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CACHE_PATH.open("wb") as f:
        pickle.dump(docs, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"  Ingested {len(docs)} chunks in {time.time()-start:.0f}s", flush=True)
    print(f"  Cached docs to {CACHE_PATH}", flush=True)
else:
    print("Step 1: Ingesting from PDFs (slow)...", flush=True)
    from ingest import ingest_all
    docs = ingest_all("data/awards", "data/nes/nes_combined.txt")
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CACHE_PATH.open("wb") as f:
        pickle.dump(docs, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"  Ingested {len(docs)} chunks in {time.time()-start:.0f}s", flush=True)
    print(f"  Cached docs to {CACHE_PATH}", flush=True)

print("Step 2: Loading embeddings model...", flush=True)
emb = FastEmbedEmbeddings()
print("  Model loaded", flush=True)

print("Step 3: Building TurboVec index...", flush=True)
STORE_DIR.mkdir(parents=True, exist_ok=True)

if (STORE_DIR / "index.tvim").exists() and (STORE_DIR / "docstore.json").exists():
    store = TurboQuantVectorStore.load(str(STORE_DIR), embedding=emb)
    if CHECKPOINT_PATH.exists():
        import json
        checkpoint = json.loads(CHECKPOINT_PATH.read_text())
        start_idx = int(checkpoint.get("next_doc_idx", 0))
    else:
        start_idx = 0
    print(f"  Resuming from doc {start_idx}/{len(docs)}", flush=True)
else:
    store = TurboQuantVectorStore(embedding=emb, bit_width=4)
    start_idx = 0

total_batches = (len(docs) + BATCH_SIZE - 1) // BATCH_SIZE
start_batch = start_idx // BATCH_SIZE
for batch_no, batch_start in enumerate(range(start_idx, len(docs), BATCH_SIZE), start=start_batch + 1):
    batch = docs[batch_start:batch_start + BATCH_SIZE]
    store.add_documents(batch)
    next_idx = batch_start + len(batch)
    print(
        f"  Batch {batch_no}/{total_batches}: added {len(batch)} docs "
        f"(total {next_idx}/{len(docs)})",
        flush=True,
    )
    if batch_no % CHECKPOINT_EVERY_BATCHES == 0 or next_idx == len(docs):
        import json
        store.dump(str(STORE_DIR))
        CHECKPOINT_PATH.write_text(
            json.dumps(
                {
                    "next_doc_idx": next_idx,
                    "total_docs": len(docs),
                    "batch_size": BATCH_SIZE,
                },
                indent=2,
            )
        )

store.dump(str(STORE_DIR))
if CHECKPOINT_PATH.exists():
    CHECKPOINT_PATH.unlink()
print(f"Done. Vector store saved. Total: {time.time()-start:.0f}s", flush=True)
