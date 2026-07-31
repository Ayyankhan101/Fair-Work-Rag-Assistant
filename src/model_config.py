"""Provider and model configuration — single source of truth.

DEF-046: Provider config centralized here, not hardcoded in rag.py.
Models are read from environment variables with safe defaults.
"""
import os


# DEF-031/046: Groq model configuration from environment
GROQ_PRIMARY_MODEL = os.getenv("GROQ_MODEL_PRIMARY", "llama-3.3-70b-versatile")
GROQ_FALLBACK_MODEL = os.getenv("GROQ_MODEL_FALLBACK", "llama-3.1-8b-instant")
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0"))
GROQ_MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS", "1024"))
GROQ_TIMEOUT = int(os.getenv("GROQ_TIMEOUT", "30"))
GROQ_MAX_RETRIES = int(os.getenv("GROQ_MAX_RETRIES", "2"))

# Retrieval config
DOC_CHARS = int(os.getenv("DOC_CHARS", "1000"))
MAX_CHARS = int(os.getenv("MAX_CHARS", "4000"))
K_HYBRID = int(os.getenv("K_HYBRID", "10"))
K_FILTERED = int(os.getenv("K_FILTERED", "20"))
MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", "1500"))
