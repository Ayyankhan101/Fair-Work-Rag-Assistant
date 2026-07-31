"""RAG chain for unfair dismissal law with post-hoc verification."""
import os
import re
import time
import logging
from typing import Optional, List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

from src.cag import get_cag_cache
from src.router import classify_query, QueryType
from src.verifier import CitationVerifier
from src.citation_resolver import CitationResolver
from src.abstention_gate import AbstentionGate
from src.audit_log import AuditLogger

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are an unfair dismissal research assistant for Australian employment law.

You answer questions about unfair dismissal under Part 3-2 Division 4 of the Fair Work Act 2009.

CRITICAL RULES:
1. ONLY use the provided context to answer — never fabricate information.
2. Cite specific sections (e.g., "s385", "s387") from the context.
3. If the context does not contain enough information, say "I could not find authority for this question."
4. NEVER make up section numbers, case names, or legal principles not in the context.
5. For analogous-facts questions, cite specific FWC decisions from the context.
6. Do NOT provide legal advice — provide legal information retrieval.

RESPONSE FORMAT:
**Answer:** [Direct answer with specific section references]

**Legislation Reference:** [Fair Work Act 2009, Part 3-2 Division 4]

**Section:** [Specific sections, e.g., "s385", "s387"]

**Explanation:** [How the answer was derived from the specific context]

**Note:** [One of: "This is legal information, not legal advice" OR "Additional case law may apply" OR "Information is limited — please consult a legal professional"]

Context:
{context}

Question: {question}

Answer:"""


class UnfairDismissalRAG:
    """RAG chain for unfair dismissal with post-hoc verification.
    
    Per playbook Part 5.1:
    1. Query understanding (classify)
    2. Hybrid retrieval (top ~50) → Rerank (top ~8)
    3. Constrained generation
    4. POST-HOC VERIFIER
    5. CITATION RESOLVER
    6. ABSTENTION GATE
    7. Render
    """
    
    def __init__(self):
        load_dotenv()
        
        # LLM
        self.llm = ChatGroq(
            model_name=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.1,
        )
        
        # Components
        self.cag_cache = get_cag_cache()
        self.verifier = CitationVerifier()
        self.citation_resolver = CitationResolver()
        self.abstention_gate = AbstentionGate()
        self.audit_log = AuditLogger()
        
        # Prompt
        self.prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
        self.output_parser = StrOutputParser()
        
        # Retriever (set later)
        self.retriever = None
    
    def set_retriever(self, retriever):
        """Set the base retriever for RAG path."""
        self.retriever = retriever
    
    def query(self, question: str) -> dict:
        """Process a question through the full pipeline."""
        start_time = time.time()
        
        # Step 1: Query understanding
        routing = classify_query(question)
        logger.info(f"Query classified as {routing.query_type.value} (confidence: {routing.confidence:.2f})")
        
        # Step 2: Get context (CAG or RAG)
        context = ""
        docs_used = []
        
        if routing.is_cag_candidate:
            # CAG path — legislation context
            context = self.cag_cache.get_context(question)
            if context:
                docs_used = [Document(page_content=context, metadata={"source": "Fair Work Act 2009"})]
        
        if not context and self.retriever:
            # RAG path — retrieve from decisions
            docs_used = self.retriever.get_relevant_documents(question)
            context = "\n\n".join([doc.page_content for doc in docs_used])
        
        # Step 3: Abstention gate (pre-generation)
        if not context:
            response = self.abstention_gate.get_abstention_response(
                question=question,
                found_citations=[],
            )
            logger.info(f"ABSTAIN: {question[:50]}... (no context)")
            return {
                "answer": response,
                "query_type": routing.query_type.value,
                "citations": [],
                "verified": False,
                "abstained": True,
                "latency": time.time() - start_time,
            }
        
        # Step 4: Generate answer
        chain = self.prompt | self.llm | self.output_parser
        answer = chain.invoke({"context": context, "question": question})
        
        # Step 5: Post-hoc verification
        citations = self.citation_resolver.extract_citations(answer)
        verified_citations = []
        for citation in citations:
            # Check if citation exists in context
            verified = citation.lower() in context.lower()
            verified_citations.append({
                "citation": citation,
                "verified": verified,
                "source": "Fair Work Act 2009" if verified else None,
            })
        
        # Step 6: Citation resolver
        if verified_citations:
            resolved = self.citation_resolver.resolve([vc["citation"] for vc in verified_citations])
        else:
            resolved = []
        
        # Step 7: Abstention gate (post-generation)
        from dataclasses import dataclass
        @dataclass
        class MockCitation:
            citation: str
            verified: bool
        
        mock_citations = [MockCitation(vc["citation"], vc["verified"]) for vc in verified_citations]
        avg_confidence = 0.8 if any(vc["verified"] for vc in verified_citations) else 0.3
        
        abstention_decision = self.abstention_gate.should_abstain(
            question=question,
            verified_citations=mock_citations,
            confidence=avg_confidence,
        )
        
        if abstention_decision.should_abstain:
            response = self.abstention_gate.get_abstention_response(
                question=question,
                found_citations=mock_citations,
            )
        else:
            response = answer
        
        # Step 8: Audit log
        latency = time.time() - start_time
        logger.info(f"QUERY: {question[:50]}... | type={routing.query_type.value} | "
                    f"citations={len(verified_citations)} | latency={latency:.2f}s")
        
        return {
            "answer": response,
            "query_type": routing.query_type.value,
            "citations": verified_citations,
            "verified": any(vc["verified"] for vc in verified_citations),
            "abstained": abstention_decision.should_abstain,
            "latency": latency,
        }


# Singleton
_rag_instance = None

def get_rag() -> UnfairDismissalRAG:
    """Get or create RAG instance."""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = UnfairDismissalRAG()
    return _rag_instance
