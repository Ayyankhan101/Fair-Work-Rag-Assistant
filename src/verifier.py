"""Post-hoc citation verifier — separate LLM call to validate claims."""
import os
import logging
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)


@dataclass
class VerificationResult:
    citation: str
    verdict: str  # "supported" | "partially" | "unsupported"
    supporting_text: Optional[str]
    confidence: float


class CitationVerifier:
    """Verify each cited passage actually supports the generated claim.
    
    Per playbook Part 5.2: "A second model call, with no access to the 
    original question's framing, asked only: 'Does passage X support claim Y?'"
    """
    
    def __init__(self):
        load_dotenv()
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_tokens=512,
            timeout=30,
            max_retries=2,
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a legal citation verifier. Your ONLY job is to determine if a passage supports a claim.

RULES:
1. Answer ONLY: supported, partially, or unsupported
2. Quote the exact supporting text if any
3. Be strict — the passage must DIRECTLY support the claim
4. If the passage is about a different topic, answer unsupported
5. Do NOT add any interpretation or analysis

RESPONSE FORMAT:
VERDICT: [supported/partially/unsupported]
SUPPORTING TEXT: [exact quote if supported, or "None"]
CONFIDENCE: [0.0-1.0]"""),
            ("human", """CLAIM: {claim}

PASSAGE: {passage}

CITATION: {citation}

Does the passage support the claim?"""),
        ])
    
    def verify(self, claim: str, passage: str, citation: str) -> VerificationResult:
        """Verify a single citation claim pair."""
        try:
            chain = self.prompt | self.llm
            response = chain.invoke({
                "claim": claim,
                "passage": passage,
                "citation": citation,
            })
            return self._parse_result(response.content, citation)
        except Exception as e:
            logger.error(f"Verification failed for {citation}: {e}")
            return VerificationResult(
                citation=citation,
                verdict="unsupported",
                supporting_text=None,
                confidence=0.0,
            )
    
    def verify_batch(self, claims: list[dict]) -> list[VerificationResult]:
        """Verify multiple citation-claim pairs.
        
        Args:
            claims: List of {"claim": str, "passage": str, "citation": str}
        """
        results = []
        for item in claims:
            result = self.verify(item["claim"], item["passage"], item["citation"])
            results.append(result)
            if result.verdict == "unsupported":
                logger.warning(f"HALLUCINATION DETECTED: {item['citation']}")
        return results
    
    def _parse_result(self, response: str, citation: str) -> VerificationResult:
        """Parse LLM response into VerificationResult."""
        verdict = "unsupported"
        supporting_text = None
        confidence = 0.0
        
        for line in response.split("\n"):
            line = line.strip()
            if line.upper().startswith("VERDICT:"):
                v = line.split(":", 1)[1].strip().lower()
                if v in ("supported", "partially", "unsupported"):
                    verdict = v
            elif line.upper().startswith("SUPPORTING TEXT:"):
                text = line.split(":", 1)[1].strip()
                if text and text.lower() != "none":
                    supporting_text = text
            elif line.upper().startswith("CONFIDENCE:"):
                try:
                    confidence = float(line.split(":", 1)[1].strip())
                except ValueError:
                    confidence = 0.5
        
        return VerificationResult(
            citation=citation,
            verdict=verdict,
            supporting_text=supporting_text,
            confidence=confidence,
        )
