"""Gradio web interface for Fair Work Awards & NES Q&A."""
import os
import sys
import gradio as gr
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vectorstore import load_vectorstore, build_vectorstore
from rag import create_rag_chain, ask_question
from cag import get_cag_cache
from router import route_question, RouteType


# Load or build vector store
STORE_DIR = "data/vectorstore"
AWARDS_DIR = "data/awards"
NES_PATH = "data/nes/nes_combined.txt"

print("Initializing system...")
load_dotenv()

# Load CAG cache (NES pre-loaded)
print("Loading CAG cache...")
cag_cache = get_cag_cache()

# Load or build vector store
if os.path.exists(os.path.join(STORE_DIR, "index.tvim")):
    vectorstore = load_vectorstore(STORE_DIR)
else:
    vectorstore = build_vectorstore(AWARDS_DIR, NES_PATH, STORE_DIR)

# Create RAG chain with CAG support
docstore_path = os.path.join(STORE_DIR, "docstore.json")
rag_chain = create_rag_chain(vectorstore, cag_cache, docstore_path)
print("System ready!")


def chat(message, history):
    """Handle chat messages with CAG+RAG routing."""
    try:
        # Route the question
        decision = route_question(message, cag_cache)
        
        # Log routing decision
        print(f"Route: {decision.route.value} | Confidence: {decision.confidence} | Reason: {decision.reasoning}")
        
        # Get answer (chain handles CAG/RAG internally)
        response = ask_question(rag_chain, message)
        
        # Add routing info for debugging
        route_info = f"[Route: {decision.route.value.upper()}]"
        return f"{route_info}\n\n{response}"
    except Exception as e:
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
