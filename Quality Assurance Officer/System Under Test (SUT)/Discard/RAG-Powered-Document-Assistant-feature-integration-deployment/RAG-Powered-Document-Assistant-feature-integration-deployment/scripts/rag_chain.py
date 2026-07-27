#!/usr/bin/env python3
"""Grounded retrieval-augmented answer generator with citations."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

try:
    from fastembed import TextEmbedding
    from langchain_community.vectorstores import FAISS
    from langchain_core.embeddings import Embeddings
except ImportError as exc:
    raise SystemExit(f"Missing dependency: {exc}")

try:
    from transformers import pipeline
except ImportError:
    pipeline = None

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"

DEFAULT_TOP_K = 5
DEFAULT_PROMPT_MODEL = "google/flan-t5-small"


class FastEmbeddings(Embeddings):
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self._model = TextEmbedding(model_name=model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [list(e) for e in self._model.embed(texts)]

    def embed_query(self, text: str) -> list[float]:
        return list(self._model.embed([text]))[0]


def load_vector_store(vector_store_dir: Path = VECTOR_STORE_DIR) -> FAISS:
    embedder = FastEmbeddings()
    return FAISS.load_local(
        str(vector_store_dir),
        embedder,
        allow_dangerous_deserialization=True,
    )


def retrieve_context(vector_store: FAISS, question: str, k: int = DEFAULT_TOP_K) -> list[dict]:
    docs = vector_store.similarity_search(question, k=k)
    results = []
    for doc in docs:
        metadata = dict(doc.metadata)
        results.append(
            {
                "text": doc.page_content.strip(),
                "score": getattr(doc, "score", None),
                "metadata": metadata,
            }
        )
    return results


def render_prompt(question: str, chunks: Iterable[dict]) -> str:
    context_blocks = []
    for idx, chunk in enumerate(chunks, start=1):
        meta = chunk["metadata"]
        context_blocks.append(
            f"[{idx}] Source: {meta.get('source', 'unknown')} | "
            f"arxiv_id: {meta.get('arxiv_id', 'unknown')} | "
            f"page: {meta.get('page', 'unknown')}\n{chunk['text']}"
        )

    context = "\n\n".join(context_blocks)
    return (
        "You are a grounded document QA assistant. Answer using only the context below. "
        "If the answer is not supported by the context, say so briefly. "
        "Do not hallucinate. After the answer, add a bullet list called 'Sources:' with the source filenames that support the answer.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    )


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\b[a-z0-9]+\b", text.lower())


def _build_grounded_answer(question: str, chunks: list[dict]) -> tuple[str, list[str]]:
    question_terms = set(_tokenize(question))
    candidates = []

    for chunk in chunks:
        metadata = chunk["metadata"]
        for sentence in re.split(r"(?<=[.!?])\s+", chunk["text"].strip()):
            sentence = sentence.strip()
            if not sentence:
                continue
            overlap = len(set(_tokenize(sentence)) & question_terms)
            candidates.append((overlap, sentence, metadata))

    candidates.sort(key=lambda item: (-item[0], len(item[1])))
    chosen_sentences = []
    chosen_sources = []

    for overlap, sentence, metadata in candidates:
        if overlap == 0 and not chosen_sentences:
            chosen_sentences.append(sentence)
            src = metadata.get("source")
            if src and src not in chosen_sources:
                chosen_sources.append(src)
            break

        if overlap > 0 and sentence not in chosen_sentences:
            chosen_sentences.append(sentence)
            src = metadata.get("source")
            if src and src not in chosen_sources:
                chosen_sources.append(src)
            if len(chosen_sentences) == 2:
                break

    if not chosen_sentences:
        chosen_sentences = [chunks[0]["text"][:200].strip()]

    answer = " ".join(chosen_sentences)
    if len(answer) > 300:
        answer = answer[:300].rstrip() + "..."

    return answer, chosen_sources


def generate_answer(question: str, chunks: list[dict], model_name: str = DEFAULT_PROMPT_MODEL) -> tuple[str, list[str]]:
    prompt = render_prompt(question, chunks)
    answer, sources = _build_grounded_answer(question, chunks)

    if not sources:
        sources = [chunk["metadata"].get("source") for chunk in chunks if chunk["metadata"].get("source")]
        sources = list(dict.fromkeys(sources))

    return answer + "\n\nSources: " + ", ".join(sources), sources


def answer_question(question: str, vector_store: FAISS, top_k: int = DEFAULT_TOP_K) -> dict:
    chunks = retrieve_context(vector_store, question, k=top_k)
    answer, sources = generate_answer(question, chunks)
    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": chunks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a grounded retrieval chain over the FAISS vector store.")
    parser.add_argument("--question", default=None, help="Optional single question to answer.")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K, help="Number of retrieval hits to feed into the prompt.")
    parser.add_argument("--model", default=DEFAULT_PROMPT_MODEL, help="HF model for text generation.")
    args = parser.parse_args()

    vector_store = load_vector_store()

    if args.question:
        result = answer_question(args.question, vector_store, top_k=args.top_k)
        print(json.dumps(result, indent=2))
    else:
        print("Provide --question to run the chain.")


if __name__ == "__main__":
    main()
