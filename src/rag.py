"""RAG chain with Groq LLM for Fair Work Awards & NES Q&A."""
import os
from typing import Optional
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from vectorstore import load_vectorstore
from bm25_retriever import build_bm25_retriever_from_docstore
from hybrid_retriever import HybridRetriever
from filtered_retriever import AwardFilteredRetriever
from config import AWARD_PATTERNS, TOPIC_KEYWORDS, detect_award, detect_topic


RAG_PROMPT_TEMPLATE = """You are an expert on Australian employment law. Your task is to answer questions using ONLY the provided context from Modern Awards and the National Employment Standards (NES).

CRITICAL RULES:
1. EXTRACT specific numbers, percentages, time periods, and dollar amounts from the context.
2. NEVER say "not specified", "not explicitly stated", or "the context does not contain" — ALWAYS provide the best answer from the context.
3. If context contains multiple relevant clauses, SYNTHESIZE them into a complete answer.
4. For questions about a specific Award, PRIORITIZE that Award's provisions.
5. For general questions (e.g., "overtime rules", "penalty rates"), COMPARE across multiple Awards.
6. Use EXACT figures from context (e.g., "30 minutes", "150%", "$23.23").
7. Reference specific clause numbers and section titles from context.
8. If you find a number in the context, STATE IT CONFIDENTLY — do not hedge with "approximately" or "up to".
9. If the context references a table or schedule, mention the table name even if the exact figure isn't visible.
10. When the question asks "what is X", you MUST provide a specific answer with a number — never give a vague response.
11. RATE TABLE RULE: If the question asks for a specific dollar amount or hourly rate, scan ALL context documents for tables, schedules, or rate summaries. Look for patterns like "$XX.XX", "Table X", "Schedule B", "Minimum rates", "Hourly Rates". If you find a rate table, extract the exact dollar figure for the requested level/classification.
12. OVERTIME RATE RULE: For overtime questions, always look for percentage rates (150%, 200%, etc.) and specify the tiers (e.g., "150% for first 2 hours, 200% thereafter").

RESPONSE FORMAT (use exactly this structure):

**Answer:** [Direct answer with specific numbers/details from context]

**Award/NES Reference:** [Exact Award name(s) as they appear in context]

**Clause/Section:** [Specific clause numbers, e.g., "Clause 16.1, Table 2"]

**Explanation:** [How the answer was derived from the specific context]

**Note:** [One of: "Multiple Awards may apply — please check specific Award for details" OR "Information is limited — please consult the full Award text for complete details" OR "This answer is based on the specific context provided"]

EXAMPLES OF GOOD ANSWERS:

Example 1 - Specific Award question:
Q: "What is the minimum break under the Hospitality Award?"
**Answer:** An unpaid meal break of no less than 30 minutes.
**Award/NES Reference:** Hospitality Industry (General) Award 2020
**Clause/Section:** Clause 16.1, 16.2, Table 2
**Explanation:** The context specifies a 30-minute unpaid meal break in Clause 16 and Table 2.
**Note:** This answer is based on the specific context provided.

Example 2 - General topic question:
Q: "What are overtime rules for a casual employee?"
**Answer:** Casual employees receive overtime at 150% for the first 2-3 hours, then 200% thereafter, varying by Award. For example, under the General Retail Industry Award, casual overtime is 150% for first 2 hours, 200% thereafter. Under the Cleaning Services Award, it is 150% for first 3 hours, 200% thereafter.
**Award/NES Reference:** Multiple Awards (General Retail Industry Award 2020, Cleaning Services Award 2020, Vehicle Repair, Services and Retail Award 2020)
**Clause/Section:** Various clauses across Awards
**Explanation:** Multiple Awards in the context specify different overtime rates for casual employees. The answer synthesizes rates from multiple Awards.
**Note:** Multiple Awards may apply — please check specific Award for details.

Example 3 - NES question:
Q: "What is the notice period for resignation under the NES?"
**Answer:** Under section 117 of the Fair Work Act, an employee must give notice based on their period of continuous service: less than 1 year = 1 week, 1-3 years = 2 weeks, 3-5 years = 3 weeks, 5+ years = 4 weeks.
**Award/NES Reference:** National Employment Standards
**Clause/Section:** Section 117(3), NES Part 2-2
**Explanation:** The NES specifies notice periods based on continuous service length.
**Note:** This answer is based on the specific context provided.

Context:
{context}

Question: {question}

Answer:"""


def get_llm(fallback=False) -> ChatGroq:
    """Initialize Groq LLM with optional fallback.
    
    Args:
        fallback: If True, use smaller model (8b-instant) for rate limit avoidance
    """
    load_dotenv()
    model = "llama-3.1-8b-instant" if fallback else "llama-3.3-70b-versatile"
    return ChatGroq(
        model=model,
        temperature=0,
        max_tokens=1024,
    )


def format_docs(docs, max_chars=4000) -> str:
    """Format retrieved documents into context string with optional truncation."""
    formatted = []
    total_chars = 0
    for i, doc in enumerate(docs):
        if total_chars >= max_chars:
            break
        metadata = doc.metadata
        header = f"[Document {i+1}: {metadata['award_name']}"
        if metadata.get('clause_number'):
            header += f" — {metadata['clause_number']}"
        header += f" ({metadata['document_type']})]"
        source_url = metadata.get('source_url', '')
        section = metadata.get('section_title', '')
        # Show more content for better answer quality
        content = doc.page_content[:800] + "..." if len(doc.page_content) > 800 else doc.page_content
        formatted.append(
            f"{header}\n"
            f"Section: {section}\n"
            f"Source: {source_url}\n"
            f"{content}"
        )
        total_chars += len(content)
    return "\n\n".join(formatted)


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

    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

    # Award name mapping for filtering (from shared config)
    AWARD_KEYWORDS = AWARD_PATTERNS
    
    def detect_award_filter(question: str) -> Optional[str]:
        """Detect if question mentions a specific Award."""
        return detect_award(question)
    
    # Topic keywords for general questions (from shared config)
    TOPIC_KEYWORDS_MAP = TOPIC_KEYWORDS
    
    def detect_topic_filter(question: str) -> Optional[str]:
        """Detect if question is about a general topic."""
        return detect_topic(question)
    
    def build_context(question: str):
        """Build context from CAG cache, RAG retrieval, or both."""
        context_parts = []
        
        # Check if CAG cache is available and question is CAG candidate
        if cag_cache and cag_cache.is_cag_candidate(question):
            cag_ctx = cag_cache.get_context(question)
            if cag_ctx:
                context_parts.append(format_cag_context(cag_ctx))
        
        # Detect award filter or topic filter
        award_filter = detect_award_filter(question)
        topic_filter = detect_topic_filter(question)
        
        # Use filtered retriever for award-specific or general topic queries
        if (award_filter or topic_filter) and filtered_retriever:
            docs = filtered_retriever.invoke(question)
        else:
            docs = hybrid_retriever.invoke(question)
        
        if docs:
            context_parts.append(format_docs(docs))
        
        return "\n\n".join(context_parts) if context_parts else "No relevant context found."

    rag_chain = (
        {"context": build_context, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def ask_question(rag_chain, question: str) -> str:
    """Ask a question and get a formatted answer with auto-fallback on rate limit."""
    try:
        response = rag_chain.invoke(question)
        return response
    except Exception as e:
        if "429" in str(e) or "rate_limit" in str(e) or "413" in str(e):
            print(f"Rate limit hit, retrying with fallback model (smaller context)...")
            # Rebuild chain with fallback model and smaller k
            from langchain_groq import ChatGroq
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_core.output_parsers import StrOutputParser
            
            fallback_llm = get_llm(fallback=True)
            
            # Get context builder from original chain and rebuild with smaller k
            original_context_builder = rag_chain.first
            if hasattr(original_context_builder, 'func'):
                # Rebuild with smaller k
                fallback_chain = (
                    original_context_builder  # Same context builder
                    | ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
                    | fallback_llm
                    | StrOutputParser()
                )
            else:
                # Fallback: rebuild entire chain
                fallback_chain = (
                    {"context": original_context_builder, "question": lambda x: x}
                    | ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
                    | fallback_llm
                    | StrOutputParser()
                )
            
            response = fallback_chain.invoke(question)
            return response
        raise


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
