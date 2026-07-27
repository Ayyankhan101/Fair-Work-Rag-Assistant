from fastapi import FastAPI
from pydantic import BaseModel

from scripts.rag_chain import load_vector_store, answer_question

app = FastAPI(
    title="RAG Powered Document Assistant API",
    version="1.0"
)

# Load FAISS vector store once
vector_store = load_vector_store()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "RAG Powered Document Assistant API is running."
    }


@app.post("/ask")
def ask(request: QuestionRequest):

    result = answer_question(
        request.question,
        vector_store
    )

    return {
        "question": result["question"],
        "answer": result["answer"],
        "sources": result["sources"]
    }