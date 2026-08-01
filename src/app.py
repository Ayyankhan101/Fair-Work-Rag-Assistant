"""Gradio web interface for Fair Work RAG Assistant (Dual Mode)."""
import os
import sys
import logging
import gradio as gr
from dotenv import load_dotenv

# Ensure project root is on path (for `from src.X` imports)
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

logger = logging.getLogger(__name__)

STORE_DIR = "data/vectorstore"


def initialize_unfair_dismissal():
    """Initialize Unfair Dismissal RAG system."""
    from src.rag import UnfairDismissalRAG
    from src.cag import get_cag_cache

    logger.info("Initializing Unfair Dismissal mode...")
    load_dotenv()

    cag_cache = get_cag_cache()
    rag = UnfairDismissalRAG()

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

    return rag


def initialize_awards():
    """Initialize Awards RAG system (legacy)."""
    from src.rag import get_rag

    logger.info("Initializing Awards mode...")
    load_dotenv()

    rag = get_rag()

    # Try to load old vectorstore
    if os.path.exists(os.path.join(STORE_DIR, "index.tvim")):
        from src.vectorstore import load_vectorstore
        from src.hybrid_retriever import HybridRetriever

        vectorstore = load_vectorstore(STORE_DIR)
        retriever = HybridRetriever(vectorstore=vectorstore)
        rag.set_retriever(retriever)
        logger.info("Awards vectorstore loaded")
    else:
        logger.info("No Awards vectorstore found")

    return rag


# Lazy initialization
_systems = {}


def _get_system(mode):
    """Get or initialize the RAG system for the given mode."""
    if mode not in _systems:
        if mode == "Unfair Dismissal":
            _systems[mode] = initialize_unfair_dismissal()
        else:
            _systems[mode] = initialize_awards()
    return _systems[mode]


def format_response(result, mode):
    """Format the response with visual indicators."""
    answer = result.get("answer", "No answer generated.")
    query_type = result.get("query_type", "unknown")
    citations = result.get("citations", [])
    abstained = result.get("abstained", False)
    latency = result.get("latency", 0)

    # Build status line
    status_parts = [f"**Mode:** {mode}"]

    type_labels = {
        "jurisdictional": "JURISDICTIONAL",
        "navigator": "NAVIGATOR",
        "analogous": "ANALOGOUS",
    }
    status_parts.append(f"**Type:** {type_labels.get(query_type, query_type.upper())}")

    if abstained:
        status_parts.append("**Status:** ABSTAINED")

    if citations:
        verified = sum(1 for c in citations if c.get("verified", False))
        status_parts.append(f"**Citations:** {verified}/{len(citations)} verified")

    if latency:
        status_parts.append(f"**Latency:** {latency:.1f}s")

    status_line = " | ".join(status_parts)

    # Format answer
    response = f"{status_line}\n\n---\n\n{answer}"

    # Add citation details if available
    if citations:
        response += "\n\n---\n\n**Citations:**\n"
        for i, c in enumerate(citations[:5], 1):
            source = c.get("source", "Unknown")
            section = c.get("section", "")
            verified = "✓" if c.get("verified", False) else "○"
            response += f"{verified} [{i}] {source} — {section}\n"

    return response


def chat(message, history, mode):
    """Handle chat messages based on selected mode."""
    try:
        rag = _get_system(mode)
        result = rag.query(message)
        return format_response(result, mode)
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return f"**Error:** {str(e)}"


# Example questions by mode
EXAMPLES_UNFAIR_DISMISSAL = [
    "What is an unfair dismissal?",
    "How long do I have to apply for unfair dismissal?",
    "What is the minimum employment period?",
    "What criteria does the FWC consider?",
    "Can I get compensation instead of reinstatement?",
    "What is the high income threshold?",
    "How is compensation calculated?",
    "What is a summary dismissal?",
]

EXAMPLES_AWARDS = [
    "What are the casual loading rates?",
    "How many hours in a full-time week?",
    "What is the minimum break between shifts?",
    "What are the penalty rates for weekends?",
    "How much annual leave do I get?",
    "What is the notice period for resignation?",
]


# Build UI
with gr.Blocks(title="Fair Work RAG Assistant") as demo:
    # Header
    gr.Markdown(
        "# Fair Work Research Assistant\n"
        "AI-powered legal information retrieval for Australian employment law"
    )

    # Disclaimer
    gr.Markdown(
        "> **Note:** This is a legal information retrieval tool, not legal advice. "
        "Always consult a qualified legal professional for specific matters."
    )

    # Mode Selector
    with gr.Row():
        with gr.Column(scale=1):
            mode_selector = gr.Radio(
                choices=["Unfair Dismissal", "Awards"],
                value="Unfair Dismissal",
                label="Research Mode",
                info="Select which corpus to search",
            )

    # Chat Interface
    chatbot = gr.ChatInterface(
        fn=lambda msg, hist: chat(msg, hist, mode_selector.value),
        examples=EXAMPLES_UNFAIR_DISMISSAL,
        title="",
        description="",
    )

    # Footer
    gr.Markdown(
        "---\n"
        "*Fair Work RAG Assistant — Powered by Groq Llama 3.3 70B*\n\n"
        "*Data sources: Fair Work Act 2009, FWC Decisions, Modern Awards, National Employment Standards*"
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
