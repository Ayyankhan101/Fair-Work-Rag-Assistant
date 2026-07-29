#!/usr/bin/env python3
"""Hard eval suite: 20+ questions with expected answers for content accuracy scoring."""
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rag import create_rag_chain, ask_question
from vectorstore import load_vectorstore


# Hard questions with expected answers for content scoring
HARD_QUESTIONS = [
    {
        "id": "H01",
        "question": "What is the minimum hourly rate for a Level 3 employee under the Cleaning Services Award 2020?",
        "expected_keywords": ["Cleaning Services Award", "Level 3", "hourly rate", "$"],
        "expected_pattern": r"\$\d+\.\d{2}",
        "difficulty": "specific",
    },
    {
        "id": "H02",
        "question": "How many consecutive days can an employee work without a day off under the Hospitality Award?",
        "expected_keywords": ["Hospitality Award", "consecutive days", "7 days", "day off"],
        "expected_pattern": r"(7|seven)\s*(consecutive\s*)?days",
        "difficulty": "specific",
    },
    {
        "id": "H03",
        "question": "What is the casual loading percentage for casual employees under the General Retail Industry Award?",
        "expected_keywords": ["General Retail", "casual loading", "25%", "25 percent"],
        "expected_pattern": r"(25\s*%|25\s*percent)",
        "difficulty": "specific",
    },
    {
        "id": "H04",
        "question": "Under the Restaurant Industry Award, what are the ordinary hours of work for a full-time employee?",
        "expected_keywords": ["Restaurant Award", "ordinary hours", "38 hours", "week"],
        "expected_pattern": r"(38\s+\w*\s*hours|ordinary\s+hours|average\s+38)",
        "difficulty": "specific",
    },
    {
        "id": "H05",
        "question": "What penalty rate applies to public holidays under the Fast Food Industry Award?",
        "expected_keywords": ["Fast Food", "public holiday", "penalty", "250%", "225%"],
        "expected_pattern": r"(2[25]0\s*%|public\s*holiday\s*penalty)",
        "difficulty": "specific",
    },
    {
        "id": "H06",
        "question": "What is the minimum annual leave entitlement under the NES?",
        "expected_keywords": ["NES", "annual leave", "4 weeks", "20 days", "4 weeks per year"],
        "expected_pattern": r"(4\s*weeks|20\s*days)",
        "difficulty": "nes",
    },
    {
        "id": "H07",
        "question": "How many weeks notice is required for termination after 5 years of continuous service under the NES?",
        "expected_keywords": ["NES", "notice", "termination", "5 years", "4 weeks", "notice period"],
        "expected_pattern": r"(4\s*weeks|notice\s*period\s*for\s*5\s*years)",
        "difficulty": "nes",
    },
    {
        "id": "H08",
        "question": "What is the maximum probationary period allowed under the Clerks—Private Sector Award?",
        "expected_keywords": ["Clerks Award", "probation", "6 months", "maximum"],
        "expected_pattern": r"(6\s*months|probationary\s*period)",
        "difficulty": "specific",
    },
    {
        "id": "H09",
        "question": "Under the Architects Award, what is the minimum annual salary for a graduate architect?",
        "expected_keywords": ["Architects Award", "graduate architect", "salary", "minimum"],
        "expected_pattern": r"(\$|salary|annual)",
        "difficulty": "specific",
    },
    {
        "id": "H10",
        "question": "What is the maximum daily hours an employee can work under the Black Coal Mining Industry Award?",
        "expected_keywords": ["Black Coal", "daily hours", "maximum", "12 hours"],
        "expected_pattern": r"(12\s*hours|daily\s*hours)",
        "difficulty": "specific",
    },
    {
        "id": "H11",
        "question": "What is the weekend penalty rate for Saturday work under the Cleaning Services Award?",
        "expected_keywords": ["Cleaning Award", "Saturday", "penalty", "150%", "125%"],
        "expected_pattern": r"(1[25]0\s*%|Saturday\s*penalty)",
        "difficulty": "specific",
    },
    {
        "id": "H12",
        "question": "How many breaks is a full-time employee entitled to during a 8-hour shift under the General Retail Industry Award?",
        "expected_keywords": ["General Retail", "break", "8-hour", "meal break", "rest break"],
        "expected_pattern": r"(meal\s*break|rest\s*break|1\s*break|2\s*breaks)",
        "difficulty": "specific",
    },
    {
        "id": "H13",
        "question": "What is the minimum engagement period for casual employees under the Hospitality Award?",
        "expected_keywords": ["Hospitality", "casual", "minimum engagement", "3 hours", "2 hours"],
        "expected_pattern": r"(3\s+\w*\s*hours|2\s+\w*\s*hours|minimum\s*engagement)",
        "difficulty": "specific",
    },
    {
        "id": "H14",
        "question": "Under the NES, what is the maximum unpaid parental leave an employee can take?",
        "expected_keywords": ["NES", "parental leave", "unpaid", "12 months", "maximum"],
        "expected_pattern": r"(12\s*months|maximum\s*unpaid\s*parental)",
        "difficulty": "nes",
    },
    {
        "id": "H15",
        "question": "What is the public holiday penalty rate for Sunday work under the Restaurant Industry Award?",
        "expected_keywords": ["Restaurant Award", "Sunday", "penalty", "175%", "150%"],
        "expected_pattern": r"(1[57]5\s*%|Sunday\s*penalty)",
        "difficulty": "specific",
    },
    {
        "id": "H16",
        "question": "How is overtime calculated for part-time employees under the Professional Employees Award?",
        "expected_keywords": ["Professional Employees", "overtime", "part-time", "150%", "rate"],
        "expected_pattern": r"(150\s*%|overtime\s*rate|part.time\s*overtime)",
        "difficulty": "specific",
    },
    {
        "id": "H17",
        "question": "What notice period is required for a casual employee to terminate employment under the Hair and Beauty Industry Award?",
        "expected_keywords": ["Hair and Beauty", "casual", "notice", "termination"],
        "expected_pattern": r"(notice|termination|no\s*notice)",
        "difficulty": "specific",
    },
    {
        "id": "H18",
        "question": "Under the NES, what are the 10 National Employment Standards?",
        "expected_keywords": ["NES", "10 standards", "National Employment Standards", "annual leave", "sick leave", "notice"],
        "expected_pattern": r"(10\s*standards|annual\s*leave|sick\s*leave|notice)",
        "difficulty": "nes",
    },
    {
        "id": "H19",
        "question": "What is the maximum number of ordinary hours a junior employee can work in a single day under the Fast Food Industry Award?",
        "expected_keywords": ["Fast Food", "junior", "hours", "maximum", "11 hours"],
        "expected_pattern": r"(11\s+\w*\s*hours|maximum\s+daily\s+hours|junior\s+hours)",
        "difficulty": "specific",
    },
    {
        "id": "H20",
        "question": "What is the minimum shift length for evening work under the Sporting Organisations Award?",
        "expected_keywords": ["Sporting Organisations", "evening", "shift", "minimum"],
        "expected_pattern": r"(shift|evening|minimum)",
        "difficulty": "specific",
    },
    {
        "id": "H21",
        "question": "Compare the casual loading between the Cleaning Services Award and the Hospitality Award. Which is higher?",
        "expected_keywords": ["casual loading", "Cleaning", "Hospitality", "25%", "comparison"],
        "expected_pattern": r"(25\s*%|casual\s*loading|higher|lower|same)",
        "difficulty": "comparison",
    },
    {
        "id": "H22",
        "question": "What is the maximum span of ordinary hours for a full-time employee across all Awards in the retail sector?",
        "expected_keywords": ["retail", "span", "ordinary hours", "12 hours", "General Retail"],
        "expected_pattern": r"(12\s*hours|span\s*of\s*hours|retail)",
        "difficulty": "cross-award",
    },
    {
        "id": "H23",
        "question": "What are the key differences between the NES and Modern Awards regarding annual leave?",
        "expected_keywords": ["NES", "Modern Award", "annual leave", "difference", "4 weeks", "20 days"],
        "expected_pattern": r"(4\s*weeks|20\s*days|difference|NES|Award)",
        "difficulty": "comparison",
    },
    {
        "id": "H24",
        "question": "Under which Awards can an employee be required to work on public holidays?",
        "expected_keywords": ["public holiday", "required to work", "Award", "Hospitality", "Retail", "essential"],
        "expected_pattern": r"(public\s*holiday|required|essential|Hospitality|Retail)",
        "difficulty": "cross-award",
    },
    {
        "id": "H25",
        "question": "What is the minimum hourly rate for a Level 5 employee under the General Retail Industry Award?",
        "expected_keywords": ["General Retail", "Level 5", "hourly rate", "$"],
        "expected_pattern": r"\$\d+\.\d{2}",
        "difficulty": "specific",
    },
]


def validate_format(answer: str) -> list[str]:
    """Validate response format."""
    failures = []
    required_headers = [
        "**Answer:**",
        "**Award/NES Reference:**",
        "**Clause/Section:**",
        "**Explanation:**",
        "**Note:**",
    ]
    for header in required_headers:
        if header not in answer:
            failures.append(f"missing {header}")
    if not re.search(r"\*\*Clause/Section:\*\*\s*.+", answer):
        failures.append("empty clause/section")
    if not re.search(r"\*\*Award/NES Reference:\*\*\s*.+", answer):
        failures.append("empty award reference")
    return failures


def score_content(answer: str, expected: dict) -> dict:
    """Score content accuracy against expected answer.
    
    Scoring:
    - Keywords: 40 points (exact match + synonym matching)
    - Pattern: 30 points (regex match for specific values)
    - Quality: 30 points (answer completeness and specificity)
    """
    score = 0
    max_score = 0
    details = []
    
    answer_lower = answer.lower()
    
    # Check keyword presence with synonym matching
    keywords = expected.get("expected_keywords", [])
    keywords_found = 0
    for kw in keywords:
        kw_lower = kw.lower()
        # Direct match
        if kw_lower in answer_lower:
            keywords_found += 1
        # Synonym matching for common variations
        elif kw_lower == "casual loading" and ("casual" in answer_lower and "loading" in answer_lower):
            keywords_found += 1
        elif kw_lower == "hourly rate" and ("hourly" in answer_lower or "rate" in answer_lower):
            keywords_found += 1
        elif kw_lower == "notice period" and ("notice" in answer_lower or "termination" in answer_lower):
            keywords_found += 1
        elif kw_lower == "meal break" and ("meal" in answer_lower or "break" in answer_lower):
            keywords_found += 1
        elif kw_lower == "rest break" and ("rest" in answer_lower or "break" in answer_lower):
            keywords_found += 1
        elif kw_lower == "penalty" and ("penalty" in answer_lower or "penalties" in answer_lower):
            keywords_found += 1
        elif kw_lower == "overtime" and ("overtime" in answer_lower):
            keywords_found += 1
        elif kw_lower == "leave" and ("leave" in answer_lower):
            keywords_found += 1
        elif kw_lower == "hours" and ("hour" in answer_lower):
            keywords_found += 1
        elif kw_lower == "junior" and ("junior" in answer_lower or "under 18" in answer_lower):
            keywords_found += 1
        elif kw_lower == "apprentice" and ("apprentice" in answer_lower or "trainee" in answer_lower):
            keywords_found += 1
        elif kw_lower == "12 months" and ("12 months" in answer_lower or "52 weeks" in answer_lower):
            keywords_found += 1
        elif kw_lower == "maximum" and ("maximum" in answer_lower or "up to" in answer_lower or "max" in answer_lower):
            keywords_found += 1
        elif kw_lower == "20 days" and ("20 days" in answer_lower or "4 weeks" in answer_lower):
            keywords_found += 1
        elif kw_lower == "minimum engagement" and ("minimum" in answer_lower and ("engagement" in answer_lower or "engaged" in answer_lower)):
            keywords_found += 1
        elif kw_lower == "rate" and ("rate" in answer_lower or "%" in answer_lower):
            keywords_found += 1
        elif kw_lower == "3 hours" and ("3 hours" in answer_lower or "3 consecutive hours" in answer_lower):
            keywords_found += 1
        elif kw_lower == "consecutive days" and ("consecutive" in answer_lower and "day" in answer_lower):
            keywords_found += 1
        elif kw_lower == "7 days" and ("7 days" in answer_lower or "seven days" in answer_lower):
            keywords_found += 1
        elif kw_lower == "day off" and ("day off" in answer_lower or "days off" in answer_lower):
            keywords_found += 1
    
    keyword_score = (keywords_found / len(keywords)) * 40 if keywords else 40
    score += keyword_score
    max_score += 40
    details.append(f"Keywords: {keywords_found}/{len(keywords)} ({keyword_score:.0f}/40)")
    
    # Check pattern match (more flexible)
    pattern = expected.get("expected_pattern", "")
    if pattern:
        pattern_match = bool(re.search(pattern, answer, re.IGNORECASE))
        # Also check for percentage patterns as fallback
        if not pattern_match and "%" in pattern:
            pattern_match = bool(re.search(r'\d+\s*%', answer_lower))
        if not pattern_match and "$" in pattern:
            pattern_match = bool(re.search(r'\$\d+', answer_lower))
        pattern_score = 30 if pattern_match else 0
        score += pattern_score
        max_score += 30
        details.append(f"Pattern: {'match' if pattern_match else 'no match'} ({pattern_score}/30)")
    else:
        max_score += 30
        details.append("Pattern: N/A (30/30)")
    
    # Check answer quality (length, specificity, completeness)
    quality_score = 0
    if len(answer) > 100:
        quality_score += 10
    if len(answer) > 300:
        quality_score += 10
    if "not specified" not in answer_lower and "not found" not in answer_lower:
        quality_score += 10
    # Bonus for specific numbers/percentages
    if re.search(r'\d+\s*%', answer_lower) or re.search(r'\$\d+', answer_lower):
        quality_score = min(quality_score + 5, 30)
    # Bonus for clause references
    if re.search(r'clause\s*\d+', answer_lower) or re.search(r'section\s*\d+', answer_lower):
        quality_score = min(quality_score + 5, 30)
    score += quality_score
    max_score += 30
    details.append(f"Quality: {quality_score}/30")
    
    return {
        "score": score,
        "max_score": max_score,
        "percentage": (score / max_score) * 100 if max_score > 0 else 0,
        "details": details,
    }


def main() -> int:
    """Run hard eval suite."""
    store_dir = ROOT / "data" / "vectorstore"
    out_path = ROOT / "data" / "hard_eval_results.json"
    
    if not (store_dir / "index.tvim").exists():
        print("Vector store missing. Build first.")
        return 1
    
    print("Loading vector store...")
    vectorstore = load_vectorstore(str(store_dir))
    docstore_path = str(store_dir / "docstore.json")
    rag_chain = create_rag_chain(vectorstore, docstore_path=docstore_path)
    
    results = []
    total_score = 0
    max_total = 0
    format_failures = 0
    content_pass = 0
    
    for i, q in enumerate(HARD_QUESTIONS):
        print(f"\n[{i+1}/{len(HARD_QUESTIONS)}] {q['id']}: {q['question'][:60]}...")
        
        try:
            answer = ask_question(rag_chain, q["question"])
        except Exception as e:
            answer = f"Error: {e}"
        
        # Format validation
        fmt = validate_format(answer)
        if fmt:
            format_failures += 1
        
        # Content scoring
        content = score_content(answer, q)
        total_score += content["score"]
        max_total += content["max_score"]
        
        passed = content["percentage"] >= 70
        if passed:
            content_pass += 1
        
        status = "✓" if passed else "✗"
        print(f"  {status} Content: {content['percentage']:.0f}% ({content['score']:.0f}/{content['max_score']:.0f})")
        
        results.append({
            "id": q["id"],
            "question": q["question"],
            "expected_keywords": q["expected_keywords"],
            "difficulty": q["difficulty"],
            "answer": answer,
            "format_failures": fmt,
            "content_score": content,
            "passed": passed,
        })
        
        # Rate limit avoidance
        if i < len(HARD_QUESTIONS) - 1:
            time.sleep(1)
    
    # Summary
    overall = (total_score / max_total) * 100 if max_total > 0 else 0
    
    summary = {
        "total_questions": len(HARD_QUESTIONS),
        "format_pass": len(HARD_QUESTIONS) - format_failures,
        "content_pass": content_pass,
        "overall_accuracy": overall,
        "total_score": total_score,
        "max_score": max_total,
    }
    
    output = {"summary": summary, "results": results}
    out_path.write_text(json.dumps(output, indent=2))
    
    print(f"\n{'='*60}")
    print(f"EVAL SUMMARY")
    print(f"{'='*60}")
    print(f"Total Questions: {summary['total_questions']}")
    print(f"Format Pass: {summary['format_pass']}/{summary['total_questions']}")
    print(f"Content Pass: {summary['content_pass']}/{summary['total_questions']}")
    print(f"Overall Accuracy: {summary['overall_accuracy']:.1f}%")
    print(f"Saved to: {out_path}")
    
    return 0 if summary["overall_accuracy"] >= 95 else 1


if __name__ == "__main__":
    raise SystemExit(main())
