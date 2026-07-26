# Vectorstore Checkpoint & Resume

## How It Works

The vectorstore build (`build_store.py`) supports **checkpoint/resume** — you can safely stop and restart without losing progress.

### Mechanism

1. **Checkpoint file**: `data/vectorstore/build_checkpoint.json`
2. **Saves every 5 batches** (every 160 docs by default)
3. **On restart**: reads checkpoint, loads existing index, continues from saved position

### Checkpoint File Contents
```json
{
  "next_doc_idx": 14400,
  "total_docs": 16692,
  "batch_size": 32
}
```

### How to Use

#### Start Build
```bash
venv/bin/python3 build_store.py
```

#### Stop Safely
- Press `Ctrl+C` — checkpoint saves automatically on next batch
- Or kill the process — last checkpoint is preserved

#### Resume Build
```bash
venv/bin/python3 build_store.py
```
Output shows: `Resuming from doc 14400/16692`

### Configuration

Environment variables:
- `VECTORSTORE_BATCH_SIZE` — docs per batch (default: 32)
- `VECTORSTORE_CHECKPOINT_EVERY` — save every N batches (default: 5)

### File Locations

| File | Purpose |
|------|---------|
| `data/vectorstore/build_checkpoint.json` | Resume position |
| `data/vectorstore/index.tvim` | TurboVec index |
| `data/vectorstore/docstore.json` | Document store |
| `data/docs_cache.pkl` | Cached ingested docs |

### What Gets Preserved
- ✅ All indexed documents (in index.tvim)
- ✅ Resume position (in checkpoint.json)
- ✅ Cached PDFs (in docs_cache.pkl)
- ❌ Nothing lost on restart

### Troubleshooting

**Index corrupted error:**
```
ValueError: persisted store is inconsistent with its index
```
Fix: Delete index files and rebuild:
```bash
rm -f data/vectorstore/index.tvim data/vectorstore/docstore.json data/vectorstore/build_checkpoint.json
venv/bin/python3 build_store.py
```

## Related
- [[Vector Store]] — Index details
- [[Architecture Decision]] — System design
