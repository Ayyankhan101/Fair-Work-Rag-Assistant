"""Basic evaluation framework for unfair dismissal RAG."""
import json
import time
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass, asdict


@dataclass
class EvalItem:
    """Single evaluation item."""
    question: str
    expected_sections: List[str]  # e.g., ["s385", "s387"]
    expected_answer_contains: List[str]  # Key phrases that should appear
    category: str  # "jurisdictional" | "statutory_criteria" | "analogous_facts" | "procedural"
    difficulty: str  # "easy" | "medium" | "hard"


@dataclass
class EvalResult:
    """Result of evaluating a single item."""
    question: str
    predicted_answer: str
    expected_sections: List[str]
    found_sections: List[str]
    section_match: bool
    answer_contains_check: bool
    latency: float
    abstained: bool
    query_type: str


# Golden set for unfair dismissal
GOLDEN_SET: List[EvalItem] = [
    # Jurisdictional threshold questions
    EvalItem(
        question="What is an unfair dismissal?",
        expected_sections=["s385"],
        expected_answer_contains=["harsh", "unjust", "unreasonable"],
        category="jurisdictional",
        difficulty="easy",
    ),
    EvalItem(
        question="How long do I have to apply for unfair dismissal?",
        expected_sections=["s394"],
        expected_answer_contains=["21 days"],
        category="jurisdictional",
        difficulty="easy",
    ),
    EvalItem(
        question="What is the minimum employment period?",
        expected_sections=["s389"],
        expected_answer_contains=["6 months", "12 months"],
        category="jurisdictional",
        difficulty="easy",
    ),
    EvalItem(
        question="What is the high income threshold?",
        expected_sections=["s391", "s392"],
        expected_answer_contains=["high income threshold"],
        category="jurisdictional",
        difficulty="easy",
    ),
    # Statutory criteria
    EvalItem(
        question="What criteria does the FWC consider when assessing unfairness?",
        expected_sections=["s387"],
        expected_answer_contains=["valid reason", "notification", "opportunity to respond"],
        category="statutory_criteria",
        difficulty="medium",
    ),
    EvalItem(
        question="Can I get compensation instead of reinstatement?",
        expected_sections=["s391"],
        expected_answer_contains=["compensation", "reinstatement inappropriate"],
        category="statutory_criteria",
        difficulty="medium",
    ),
    EvalItem(
        question="How is compensation calculated?",
        expected_sections=["s392"],
        expected_answer_contains=["remuneration lost", "alternative employment"],
        category="statutory_criteria",
        difficulty="medium",
    ),
    # Procedural
    EvalItem(
        question="What is a summary dismissal?",
        expected_sections=["s388"],
        expected_answer_contains=["without notice", "conduct", "capacity"],
        category="procedural",
        difficulty="easy",
    ),
]


class EvalRunner:
    """Run evaluation on the RAG pipeline."""
    
    def __init__(self, rag):
        self.rag = rag
        self.results: List[EvalResult] = []
    
    def run(self, golden_set: List[EvalItem] = None) -> List[EvalResult]:
        """Run evaluation on all items."""
        if golden_set is None:
            golden_set = GOLDEN_SET
        
        self.results = []
        
        for item in golden_set:
            print(f"Evaluating: {item.question[:50]}...")
            
            start_time = time.time()
            result = self.rag.query(item.question)
            latency = time.time() - start_time
            
            # Check sections
            answer_lower = result["answer"].lower()
            found_sections = []
            for section in item.expected_sections:
                if section.lower() in answer_lower:
                    found_sections.append(section)
            
            section_match = len(found_sections) > 0
            
            # Check answer contains
            answer_contains_check = all(
                phrase.lower() in answer_lower
                for phrase in item.expected_answer_contains
            )
            
            eval_result = EvalResult(
                question=item.question,
                predicted_answer=result["answer"],
                expected_sections=item.expected_sections,
                found_sections=found_sections,
                section_match=section_match,
                answer_contains_check=answer_contains_check,
                latency=latency,
                abstained=result["abstained"],
                query_type=result["query_type"],
            )
            
            self.results.append(eval_result)
        
        return self.results
    
    def summary(self) -> Dict:
        """Generate summary statistics."""
        if not self.results:
            return {"error": "No results"}
        
        total = len(self.results)
        section_matches = sum(1 for r in self.results if r.section_match)
        answer_checks = sum(1 for r in self.results if r.answer_contains_check)
        abstentions = sum(1 for r in self.results if r.abstained)
        avg_latency = sum(r.latency for r in self.results) / total
        
        return {
            "total": total,
            "section_accuracy": section_matches / total,
            "answer_accuracy": answer_checks / total,
            "abstention_rate": abstentions / total,
            "avg_latency": avg_latency,
        }
    
    def save_results(self, path: str = "data/eval_results.json"):
        """Save results to file."""
        with open(path, "w") as f:
            json.dump([asdict(r) for r in self.results], f, indent=2)
        
        # Save summary
        summary = self.summary()
        summary_path = path.replace(".json", "_summary.json")
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"Results saved to {path}")
        print(f"Summary saved to {summary_path}")
        
        return summary


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    
    from src.rag import get_rag
    
    rag = get_rag()
    runner = EvalRunner(rag)
    
    print("Running evaluation...")
    results = runner.run()
    
    print("\nSummary:")
    summary = runner.summary()
    for k, v in summary.items():
        if isinstance(v, float):
            print(f"  {k}: {v:.2%}")
        else:
            print(f"  {k}: {v}")
    
    runner.save_results()
