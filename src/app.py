"""Gradio web interface for Unfair Dismissal RAG Assistant."""
import os
import sys
import logging
import gradio as gr
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)

STORE_DIR = "data/vectorstore"
FWC_DECISIONS_DIR = "data/fwc_decisions"
LEGISLATION_PATH = "data/legislation/fair_work_act_s385_394.txt"


def initialize_system():
    """Initialize all system components."""
    from src.rag import get_rag
    from src.cag import get_cag_cache

    logger.info("Initializing system...")
    load_dotenv()

    logger.info("Loading CAG cache...")
    cag_cache = get_cag_cache()

    logger.info("Initializing RAG pipeline...")
    rag = get_rag()

    # Try to load vectorstore if available
    if os.path.exists(os.path.join(STORE_DIR, "index.tvim")):
        from src.vectorstore import load_vectorstore
        from src.hybrid_retriever import HybridRetriever
        from src.filtered_retriever import UnfairDismissalRetriever

        vectorstore = load_vectorstore(STORE_DIR)
        base_retriever = HybridRetriever(vectorstore=vectorstore)
        filtered_retriever = UnfairDismissalRetriever(base_retriever=base_retriever)
        rag.set_retriever(filtered_retriever)
        logger.info("Vectorstore loaded — RAG enabled")
    else:
        logger.info("No vectorstore found — CAG only (legislation)")

    logger.info("System ready!")
    return rag, cag_cache


_system_initialized = False
_rag = None
_cag_cache = None


def _ensure_initialized():
    global _system_initialized, _rag, _cag_cache
    if not _system_initialized:
        _rag, _cag_cache = initialize_system()
        _system_initialized = True
    return _rag, _cag_cache


def chat(message, history):
    """Handle chat messages with the unfair dismissal pipeline."""
    try:
        rag, _ = _ensure_initialized()
        result = rag.query(message)

        # Format response
        answer = result["answer"]
        query_type = result["query_type"]
        citations = result["citations"]
        abstained = result["abstained"]
        latency = result["latency"]

        # Build header
        header = f"[Type: {query_type.upper()}]"
        if abstained:
            header += " [ABSTAINED]"
        if citations:
            verified = sum(1 for c in citations if c.get("verified", False))
            header += f" [Citations: {verified}/{len(citations)} verified]"

        return f"{header}\n\n{answer}"
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return f"Error: {str(e)}"


# Example questions
EXAMPLES = [
    "What is an unfair dismissal?",
    "How long do I have to apply for unfair dismissal?",
    "What is the minimum employment period?",
    "What criteria does the FWC consider?",
    "Can I get compensation instead of reinstatement?",
    "What is the high income threshold?",
    "How is compensation calculated?",
    "What is a summary dismissal?",
    "What happens if I'm a casual employee?",
    "Can I apply if I was employed for 3 months?",
]

# Build UI
with gr.Blocks(title="Unfair Dismissal RAG Assistant") as demo:
    gr.Markdown("# Unfair Dismissal Research Assistant")
    gr.Markdown("Ask questions about unfair dismissal under the Fair Work Act 2009 (Part 3-2 Division 4).")
    gr.Markdown("**Note:** This is a legal information retrieval tool, not legal advice.")

    chatbot = gr.ChatInterface(
        fn=chat,
        examples=EXAMPLES,
        title="",
        description="",
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft())
