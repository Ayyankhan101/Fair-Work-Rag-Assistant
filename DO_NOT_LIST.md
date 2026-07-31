# DO NOT LIST — Team Sign-Off Required

**Date:** 31 July 2026
**Owner:** Tech Lead
**Status:** PENDING TEAM SIGN-OFF

Print this. Every team member reads and signs. This is our shared line.

---

## THE DO NOT LIST

1. **Do not ingest, embed, scrape, summarise or RAG over AustLII content.**
   - AustLII usage policy prohibits all AI-related use.
   - You may LINK users to AustLII for manual verification — different act from ingesting.

2. **Do not let the model produce a citation from parametric memory.**
   - Citations come ONLY from retrieved documents.
   - Every citation validated after generation against corpus index.

3. **Do not output a percentage or odds of winning to any end user.**
   - No "70% chance of success", no "strong case", no probability.
   - Output: what the sources say, not what you should do.

4. **Do not brand or describe the product as a lawyer, as providing legal advice, or as a substitute for a lawyer.**
   - No "AI lawyer", "legal advice", "your case will succeed", "we represent you".
   - Product copy: "verified research assistant", "legal information retrieval".

5. **Do not send identifiable client facts to any endpoint without a signed no-training, no-retention agreement and a documented cross-border assessment.**
   - Every model vendor must have written agreement.
   - Australian data residency preferred for legal buyers.
   - Document cross-border disclosure for APP 8 compliance.

6. **Do not fine-tune on customer matter data. Ever.**
   - Not without separate explicit consent and purpose-limited agreement.
   - Contractually and technically enforced.

7. **Do not let a document be exported for lodgment without human verification of every authority.**
   - Every citation in exportable document must be individually marked "verified by human".
   - Log who verified, when, against which URL.
   - Export locked until all verified.

8. **Do not measure success with BLEU, ROUGE, or "the demo felt good".**
   - Use domain-specific eval: citation validity, citation support, retrieval recall, abstention accuracy.
   - Golden set of 150+ questions written by employment law practitioner.

9. **Do not train on, or generate, content that reproduces commercial publishers' headnotes or editorial commentary.**
   - Westlaw AU, LexisNexis, CCH, Jade: licence or exclude.

10. **Do not autonomously lodge, file, or transact with the FWC.**
    - Human hand on every submission.
    - Tool makes compliance easy; tool does not replace human.

11. **Do not store sensitive personal information you have no defined need for.**
    - Collect minimum needed.
    - Do not build habit of hoovering entire HR files.

12. **Do not ship a "confidence score" that is really the model's self-assessment.**
    - Model confidence ≠ actual reliability.
    - Use retrieval scores, citation verification, not LLM self-assessment.

---

## TEAM SIGN-OFF

| Name | Role | Date Read | Signature |
|------|------|-----------|-----------|
| | Tech Lead | | |
| | Backend Eng 1 (Data & Retrieval) | | |
| | Backend Eng 2 (Application & Orchestration) | | |
| | QA (Quality & AI Evaluation) | | |
| | Data Analyst (Evaluation Data & Insights) | | |
| | Scrum Master (Delivery & Governance) | | |

---

## CONSEQUENCES

Violation of any item on this list is a **P0 incident**. The team lead must be notified immediately. Items 1, 2, 5, 7 are **Catastrophic** risk if violated.

## REVIEW CADENCE

- Monthly review of this list with the team.
- Any changes require written approval from Tech Lead and legal advisor.
- Track regulatory changes (FWC Guidance Note, Dec 2026 privacy ADM provisions).
