"""RAG chain with Groq LLM for Fair Work Awards & NES Q&A."""
import os
import re
import time
import json
import logging
from dataclasses import dataclass
from typing import Optional, List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from vectorstore import load_vectorstore
from bm25_retriever import build_bm25_retriever_from_docstore
from hybrid_retriever import HybridRetriever
from filtered_retriever import AwardFilteredRetriever
from reranker import rerank_documents
from config import detect_award, detect_topic

# DEF-031: Read model from env var
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

from model_config import (
    GROQ_PRIMARY_MODEL, GROQ_FALLBACK_MODEL, GROQ_TEMPERATURE,
    GROQ_MAX_TOKENS, GROQ_TIMEOUT, GROQ_MAX_RETRIES,
)

logger = logging.getLogger(__name__)

# DEF-037: Prompt versioning
PROMPT_VERSION = "2.1.0"
PROMPT_HASH = None  # Computed at module load time

# DEF-034: Structured claims dataclass
@dataclass
class AwardClaim:
    award_name: str
    clause_ref: str
    claim_text: str
    effective_date: Optional[str] = None
    confidence: float = 0.0

@dataclass
class StructuredAnswer:
    answer: str
    award_references: List[str]
    clause_references: List[str]
    explanation: str
    note: str
    claims: List[AwardClaim]
    truncated: bool = False
    prompt_version: str = PROMPT_VERSION


SYSTEM_PROMPT = """You are a Fair Work Award expert assistant for Australian employment law.

You answer questions about Modern Awards and the National Employment Standards (NES).

RULES:
1. ONLY use the provided context to answer — never fabricate information.
2. Extract specific numbers, percentages, time periods, and dollar amounts from the context.
3. If the context does not contain enough information, say "I don't have enough information to answer this question accurately."
4. If you're unsure, say "I'm not certain — please consult the full Award text or a Fair Work specialist."
5. Reference specific clause numbers and section titles from context.
6. For questions about a specific Award, PRIORITIZE that Award's provisions.
7. For general questions without a specific Award, request clarification rather than comparing across Awards.
8. If the context references a table or schedule, mention the table name.
9. NEVER make up numbers, dates, or clause references not in the context.
10. DEF-034: Structure every answer with AWARD, CLAUSE, and CLAIM components.
11. DEF-035: Do NOT compare across multiple Awards unless the user explicitly names specific Awards for comparison.
12. DEF-044: If context is too large (over 1200 chars), fail_closed — do not guess.

RESPONSE FORMAT:

AWARD: [Exact Award name(s) as they appear in context]

CLAUSE: [Specific clause numbers, e.g., Clause 16.1, Table 2]

CLAIM: [Direct answer with specific numbers/details from context]

EXPLANATION: [How the answer was derived from the specific context]

NOTE: [One of: "Multiple Awards may apply — please check specific Award for details" OR "Information is limited — please consult the full Award text for complete details" OR "This answer is based on the specific context provided"]

EXAMPLES:

Example 1 - Specific Award question:
Context: [Hospitality Industry (General) Award 2020 - Clause 16.1] An employee must be given an unpaid meal break of not less than 30 minutes...
Q: "What is the minimum break under the Hospitality Award?"
**Answer:** An unpaid meal break of no less than 30 minutes.
**Award/NES Reference:** Hospitality Industry (General) Award 2020
**Clause/Section:** Clause 16.1
**Explanation:** The context specifies a 30-minute unpaid meal break in Clause 16.
**Note:** This answer is based on the specific context provided.

Example 2 - Insufficient context:
Context: [General Retail Industry Award 2020 - Clause 15] Overtime is payable at 150%...
Q: "What is the minimum salary for a Level 5 retail employee in 2024?"
**Answer:** I don't have enough information to answer this question accurately. The context mentions overtime rates but does not include specific salary rates for Level 5 employees.
**Award/NES Reference:** General Retail Industry Award 2020
**Clause/Section:** Clause 15
**Explanation:** The retrieved context covers overtime provisions but does not contain salary rate tables.
**Note:** Information is limited — please consult the full Award text for complete details.

Context:
{context}

Question: {question}

Answer:"""

# Compute prompt hash for versioning
import hashlib as _hashlib
PROMPT_HASH = _hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest()[:16]


# DEF-043: Circuit breaker for provider failures
class CircuitBreaker:
    """Simple circuit breaker to prevent cascading failures."""
    def __init__(self, failure_threshold=3, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "closed"  # closed = normal, open = blocking, half-open = testing
    
    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
            logger.warning(f"Circuit breaker OPEN after {self.failure_count} failures")
    
    def record_success(self):
        self.failure_count = 0
        self.state = "closed"
    
    def allow_request(self) -> bool:
        if self.state == "closed":
            return True
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
                logger.info("Circuit breaker half-open, allowing test request")
                return True
            return False
        return True  # half-open allows one request

_circuit_breaker = CircuitBreaker()


# DEF-046: Provider abstraction boundary
class LLMProvider:
    """Abstract provider boundary for LLM calls.
    
    DEF-031: Model IDs read from environment via model_config.
    """
    def __init__(self):
        self.primary_model = GROQ_PRIMARY_MODEL
        self.fallback_model = GROQ_FALLBACK_MODEL
    
    def get_client(self, fallback: bool = False) -> ChatGroq:
        load_dotenv()
        model = self.fallback_model if fallback else self.primary_model
        return ChatGroq(
            model=model,
            temperature=GROQ_TEMPERATURE,
            max_tokens=GROQ_MAX_TOKENS,
            timeout=30,  # DEF-043: explicit timeout
            max_retries=GROQ_MAX_RETRIES,
        )
    
    @property
    def models(self) -> dict:
        return {"primary": self.primary_model, "fallback": self.fallback_model}

_provider = LLMProvider()


def get_llm(fallback=False) -> ChatGroq:
    """Initialize Groq LLM with optional fallback.
    
    DEF-031: Model IDs updated to avoid deprecated models.
    DEF-046: Uses provider abstraction boundary.
    """
    return _provider.get_client(fallback=fallback)


def needs_clarification(question: str) -> bool:
    """Check if question needs clarification before answering.
    
    DEF-035: Also gate overly general comparison questions.
    """
    q = question.lower().strip()
    
    # Too short to be meaningful
    if len(q) < 5:
        return True
    
    # Greetings only
    greeting_patterns = [
        r'^(hi|hello|hey|greetings|good morning|good afternoon|good evening)[\s!]*$',
        r'^(yo|sup|howdy|hiya)[\s!]*$',
    ]
    if any(re.match(p, q) for p in greeting_patterns):
        return True
    
    # Just a question word
    just_question = r'^(what|how|when|where|who|why|can|could|would|should|is|are|do|does|did|tell|explain|show)[\s?]*$'
    if re.match(just_question, q):
        return True
    
    # Just punctuation
    if all(c in '?!. ' for c in q):
        return True
    
    # DEF-035: Overly general comparison questions with no specific topic
    general_comparison_patterns = [
        r'^(compare|difference between|vs|versus)\s+',
        r'^(what are the (differences|similarities) between)',
        r'^(how do .+ compare)',
    ]
    award = detect_award(q)
    topic = detect_topic(q)
    if any(re.match(p, q) for p in general_comparison_patterns) and not award and not topic:
        return True
    
    return False


def format_docs(docs, max_chars=4000) -> tuple[str, bool]:
    """Format retrieved documents into context string with truncation tracking.
    
    DEF-036: Returns (formatted_text, was_truncated) so caller can expose truncation.
    Strips contextual retrieval prefix before displaying to user.
    """
    formatted = []
    total_chars = 0
    truncated = False
    for i, doc in enumerate(docs):
        if total_chars >= max_chars:
            truncated = True
            break
        metadata = doc.metadata
        header = f"[Document {i+1}: {metadata['award_name']}"
        if metadata.get('clause_number'):
            header += f" — {metadata['clause_number']}"
        header += f" ({metadata['document_type']})]"
        source_url = metadata.get('source_url', '')
        section = metadata.get('section_title', '')
        
        # Strip contextual retrieval prefix: "[Award Name - Section] "
        content = doc.page_content
        content = re.sub(r'^\[.+?\]\s*', '', content)
        
        # Show more content for better answer quality
        content = content[:800] + "..." if len(content) > 800 else content
        formatted.append(
            f"{header}\n"
            f"Section: {section}\n"
            f"Source: {source_url}\n"
            f"{content}"
        )
        total_chars += len(content)
    return "\n\n".join(formatted), truncated


def format_cag_context(cag_text: str) -> str:
    """Format CAG context for inclusion in prompt."""
    if not cag_text:
        return ""
    return f"[CAG Cache - Pre-loaded Content]\n{cag_text}"


def create_rag_chain(vectorstore, cag_cache=None, docstore_path=None):
    """Create RAG chain with optional CAG context.
    
    Args:
        vectorstore: TurboVec vector store for RAG path
        cag_cache: Optional CAGCache instance for CAG path
        docstore_path: Path to docstore.json for BM25 index
    """
    llm = get_llm()
    
    # Create semantic retriever
    semantic_retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10},
    )
    
    # Create filtered retriever for award-specific queries
    if docstore_path and os.path.exists(docstore_path):
        filtered_retriever = AwardFilteredRetriever(docstore_path=docstore_path)
        bm25_retriever = build_bm25_retriever_from_docstore(docstore_path)
        hybrid_retriever = HybridRetriever(
            bm25_retriever=bm25_retriever,
            semantic_retriever=semantic_retriever,
            k=10,
        )
    else:
        filtered_retriever = None
        hybrid_retriever = semantic_retriever

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_messages([("system", SYSTEM_PROMPT)]),
        HumanMessagePromptTemplate.from_messages([("human", "{question}")]),
    ])

    # Award name mapping for filtering (from shared config)
    
    def detect_award_filter(question: str) -> Optional[str]:
        """Detect if question mentions a specific Award."""
        return detect_award(question)
    
    # Topic keywords for general questions (from shared config)
    
    def detect_topic_filter(question: str) -> Optional[str]:
        """Detect if question is about a general topic."""
        return detect_topic(question)
    
    def build_context(question: str) -> tuple[str, bool]:
        """Build context from CAG cache, RAG retrieval, or both.
        
        Returns (context_text, was_truncated) tuple.
        """
        context_parts = []
        was_truncated = False
        
        # Check if CAG cache is available and question is CAG candidate
        if cag_cache and cag_cache.is_cag_candidate(question):
            cag_ctx = cag_cache.get_context(question)
            if cag_ctx:
                context_parts.append(format_cag_context(cag_ctx))
        
        # Detect award filter or topic filter
        award_filter = detect_award_filter(question)
        topic_filter = detect_topic_filter(question)
        
        # Use filtered retriever for award-specific queries with strong topic match
        # Fall back to hybrid for weak topic matches or no award
        use_filtered = False
        if (award_filter or topic_filter) and filtered_retriever:
            try:
                test_docs = filtered_retriever.invoke(question)
                # Check if filtered retriever found answer-relevant docs
                if test_docs and any(
                    any(kw in d.page_content.lower() for kw in question.lower().split() if len(kw) > 3)
                    for d in test_docs[:5]
                ):
                    docs = test_docs
                    use_filtered = True
            except Exception:
                pass
        
        if not use_filtered:
            docs = hybrid_retriever.invoke(question)
        
        # Rerank documents for better relevance
        if docs and len(docs) > 10:
            docs = rerank_documents(question, docs, top_n=10, use_cohere=True)
        
        if docs:
            ctx_text, was_truncated = format_docs(docs)
            context_parts.append(ctx_text)
        
        full_context = "\n\n".join(context_parts) if context_parts else "No relevant context found."
        return full_context, was_truncated

    # DEF-036: Chain returns (context, truncated) tuple
    rag_chain = (
        {"context": build_context, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def parse_claims(response_text: str) -> List[AwardClaim]:
    """DEF-034: Parse structured claims from LLM response."""
    claims = []
    award_refs = re.findall(r'\*\*Award/NES Reference:\*\*\s*(.+?)(?:\n|$)', response_text)
    clause_refs = re.findall(r'\*\*Clause/Section:\*\*\s*(.+?)(?:\n|$)', response_text)
    
    for i, award in enumerate(award_refs):
        clause = clause_refs[i] if i < len(clause_refs) else "Unknown"
        claims.append(AwardClaim(
            award_name=award.strip(),
            clause_ref=clause.strip(),
            claim_text=response_text[:200],
            confidence=0.8,
        ))
    return claims


def ask_question(rag_chain, question: str) -> str:
    """Ask a question and get a formatted answer with auto-fallback on rate limit.
    
    DEF-043: Added circuit breaker and timeout handling.
    DEF-044: Rate limit fallback reuses original prompt template.
    DEF-045: Added request logging with timing and token info.
    DEF-046: Uses provider abstraction boundary.
    """
    if needs_clarification(question):
        return """**Answer:** Could you please provide more details about your question?

**Award/NES Reference:** N/A

**Clause/Section:** N/A

**Explanation:** Your question appears to be too brief or unclear for me to provide an accurate answer.

**Note:** Please ask a specific question about a Modern Award or the National Employment Standards. For example:
- "What is the minimum break under the Hospitality Award?"
- "What are the casual loading rates in the Retail Award?"
- "How much annual leave am I entitled to under the NES?" """
    
    if not _circuit_breaker.allow_request():
        return "**Answer:** Service temporarily unavailable due to repeated errors. Please try again later.\n\n**Note:** Circuit breaker active."
    
    start_time = time.time()
    try:
        # DEF-044: build_context now returns (context, truncated) tuple
        context_result = rag_chain.first["context"](question)
        context_text, was_truncated = context_result if isinstance(context_result, tuple) else (context_result, False)
        
        response = rag_chain.invoke(question)
        elapsed = time.time() - start_time
        
        # DEF-045: Log structured metadata
        log_data = {
            "prompt_version": PROMPT_VERSION,
            "prompt_hash": PROMPT_HASH,
            "elapsed_s": round(elapsed, 2),
            "truncated": was_truncated,
            "model": _provider.models["primary"],
        }
        logger.info(f"RAG request completed | {json.dumps(log_data)}")
        _circuit_breaker.record_success()
        
        # DEF-034: Append truncation notice if applicable
        if was_truncated:
            response += "\n\n*Note: Some retrieved context was truncated due to size limits.*"
        
        return response
    except Exception as e:
        elapsed = time.time() - start_time
        error_str = str(e)
        _circuit_breaker.record_failure()
        logger.error(f"RAG request failed in {elapsed:.2f}s | error={error_str[:200]}")
        
        if "429" in error_str or "rate_limit" in error_str:
            logger.warning("Rate limit hit, retrying with fallback model and reduced context...")
            fallback_llm = get_llm(fallback=True)
            
            # DEF-044: Reuse original prompt template instead of creating inline
            fallback_chain = (
                {"context": lambda q: context_text[:2000] + "\n\n[Context truncated for rate limit fallback]", "question": lambda x: x}
                | ChatPromptTemplate.from_messages([
                    SystemMessagePromptTemplate.from_messages([("system", SYSTEM_PROMPT)]),
                    HumanMessagePromptTemplate.from_messages([("human", "{question}")]),
                ])
                | fallback_llm
                | StrOutputParser()
            )
            
            try:
                response = fallback_chain.invoke(question)
                elapsed = time.time() - start_time
                logger.info(f"Fallback request completed in {elapsed:.2f}s | model={_provider.models['fallback']}")
                _circuit_breaker.record_success()
                return response
            except Exception as fallback_err:
                logger.error(f"Fallback also failed: {fallback_err}")
                return "**Answer:** I'm experiencing technical difficulties. Please try again shortly.\n\n**Note:** Service temporarily unavailable."
        
        if "413" in error_str:
            return "**Answer:** Your question is too complex for the current context window. Please try a more specific question.\n\n**Note:** Question too large."
        
        return f"**Answer:** An error occurred while processing your question.\n\n**Note:** {error_str[:200]}"


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    store_dir = "data/vectorstore"

    # Load vector store
    vectorstore = load_vectorstore(store_dir)

    # Create RAG chain
    rag_chain = create_rag_chain(vectorstore)

    # Test with sample questions
    test_questions = [
        "What is the minimum break under the Hospitality Award?",
        "What are overtime rules for a casual employee?",
        "What leave entitlements are covered by the NES?",
    ]

    for q in test_questions:
        print(f"\n{'='*60}")
        print(f"Q: {q}")
        print(f"{'='*60}")
        answer = ask_question(rag_chain, q)
        print(answer)
