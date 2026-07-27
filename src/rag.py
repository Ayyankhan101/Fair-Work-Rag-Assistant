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
from reranker import rerank_documents
from config import AWARD_PATTERNS, TOPIC_KEYWORDS, detect_award, detect_topic


SYSTEM_PROMPT = """You are a Fair Work Award expert assistant for Australian employment law.

You answer questions about Modern Awards and the National Employment Standards (NES).

RULES:
1. ONLY use the provided context to answer — never fabricate information.
2. Extract specific numbers, percentages, time periods, and dollar amounts from the context.
3. If the context does not contain enough information, say "I don't have enough information to answer this question accurately."
4. If you're unsure, say "I'm not certain — please consult the full Award text or a Fair Work specialist."
5. Reference specific clause numbers and section titles from context.
6. For questions about a specific Award, PRIORITIZE that Award's provisions.
7. For general questions, COMPARE across multiple Awards when context allows.
8. If the context references a table or schedule, mention the table name.
9. NEVER make up numbers, dates, or clause references not in the context.

RESPONSE FORMAT:

**Answer:** [Direct answer with specific numbers/details from context]

**Award/NES Reference:** [Exact Award name(s) as they appear in context]

**Clause/Section:** [Specific clause numbers, e.g., "Clause 16.1, Table 2"]

**Explanation:** [How the answer was derived from the specific context]

**Note:** [One of: "Multiple Awards may apply — please check specific Award for details" OR "Information is limited — please consult the full Award text for complete details" OR "This answer is based on the specific context provided"]

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


def needs_clarification(question: str) -> bool:
    """Check if question needs clarification before answering."""
    import re
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
    
    return False


def format_docs(docs, max_chars=4000) -> str:
    """Format retrieved documents into context string with optional truncation.
    
    Strips contextual retrieval prefix before displaying to user.
    """
    import re
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

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template("{question}"),
    ])

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
        
        # Rerank documents for better relevance
        if docs and len(docs) > 10:
            docs = rerank_documents(question, docs, top_n=10, use_cohere=True)
        
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
    import re
    
    # Check if question needs clarification
    if needs_clarification(question):
        return """**Answer:** Could you please provide more details about your question?

**Award/NES Reference:** N/A

**Clause/Section:** N/A

**Explanation:** Your question appears to be too brief or unclear for me to provide an accurate answer.

**Note:** Please ask a specific question about a Modern Award or the National Employment Standards. For example:
- "What is the minimum break under the Hospitality Award?"
- "What are the casual loading rates in the Retail Award?"
- "How much annual leave am I entitled to under the NES?" """
    
    try:
        response = rag_chain.invoke(question)
        return response
    except Exception as e:
        if "429" in str(e) or "rate_limit" in str(e) or "413" in str(e):
            print(f"Rate limit hit, retrying with fallback model (smaller context)...")
            # Rebuild chain with fallback model and smaller k
            from langchain_groq import ChatGroq
            from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
            from langchain_core.output_parsers import StrOutputParser
            
            fallback_llm = get_llm(fallback=True)
            
            # Get context builder from original chain and rebuild with smaller k
            original_context_builder = rag_chain.first
            if hasattr(original_context_builder, 'func'):
                # Rebuild with smaller k
                fallback_chain = (
                    original_context_builder  # Same context builder
                    | ChatPromptTemplate.from_messages([
                        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
                        HumanMessagePromptTemplate.from_template("{question}"),
                    ])
                    | fallback_llm
                    | StrOutputParser()
                )
            else:
                # Fallback: rebuild entire chain
                fallback_chain = (
                    {"context": original_context_builder, "question": lambda x: x}
                    | ChatPromptTemplate.from_messages([
                        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
                        HumanMessagePromptTemplate.from_template("{question}"),
                    ])
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
