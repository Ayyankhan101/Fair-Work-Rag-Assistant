"""Gradio web interface for Fair Work Awards & NES Q&A."""
import os
import sys
import logging
import gradio as gr
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)

STORE_DIR = "data/vectorstore"
AWARDS_DIR = "data/awards"
NES_PATH = "data/nes/nes_combined.txt"


def initialize_system():
    """Initialize all system components. DEF-024: Separate construction from import."""
    from vectorstore import load_vectorstore, build_vectorstore
    from rag import create_rag_chain
    from cag import get_cag_cache

    logger.info("Initializing system...")
    load_dotenv()

    logger.info("Loading CAG cache...")
    cag_cache = get_cag_cache()

    if os.path.exists(os.path.join(STORE_DIR, "index.tvim")):
        vectorstore = load_vectorstore(STORE_DIR)
    else:
        vectorstore = build_vectorstore(AWARDS_DIR, NES_PATH, STORE_DIR)

    docstore_path = os.path.join(STORE_DIR, "docstore.json")
    rag_chain = create_rag_chain(vectorstore, cag_cache, docstore_path)
    logger.info("System ready!")
    return rag_chain, cag_cache


_system_initialized = False
_rag_chain = None
_cag_cache = None


def _ensure_initialized():
    global _system_initialized, _rag_chain, _cag_cache
    if not _system_initialized:
        _rag_chain, _cag_cache = initialize_system()
        _system_initialized = True
    return _rag_chain, _cag_cache


def chat(message, history):
    """Handle chat messages with CAG+RAG routing."""
    from rag import ask_question
    from router import route_question

    try:
        rag_chain, cag_cache = _ensure_initialized()
        decision = route_question(message, cag_cache)
        logger.info(f"Route: {decision.route.value} | Confidence: {decision.confidence} | Reason: {decision.reasoning}")
        response = ask_question(rag_chain, message)
        route_info = f"[Route: {decision.route.value.upper()}]"
        return f"{route_info}\n\n{response}"
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return f"Error: {str(e)}"


# Example questions from PRD
EXAMPLES = [
    "What Award applies to a cleaner?",
    "What is the minimum break under the Hospitality Award?",
    "What are overtime rules for a casual employee?",
    "What penalties apply for weekend work?",
    "Does the Clerks Award cover payroll officers?",
    "How many hours can an employee work each week?",
    "What leave entitlements are covered by the NES?",
    "What Award covers architects?",
    "How are meal breaks handled?",
    "What allowances are payable under the Cleaning Award?",
    "Does the Professional Employees Award apply to software engineers?",
    "What is the notice period for resignation?",
]

# Build UI
with gr.Blocks(title="Fair Work Awards & NES Q&A") as demo:
    gr.Markdown("# Fair Work Awards & NES Q&A Assistant")
    gr.Markdown("Ask questions about Australia's Modern Awards and National Employment Standards.")

    chatbot = gr.ChatInterface(
        fn=chat,
        examples=EXAMPLES,
        title="",
        description="",
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft())
