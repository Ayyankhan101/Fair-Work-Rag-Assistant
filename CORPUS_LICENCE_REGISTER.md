# Corpus Licence Register

**Owner:** Tech Lead | **Last verified:** 31 July 2026 | **Review cadence:** Monthly

No source enters the pipeline without a row. This is a procurement asset.

| # | Source | Content | Publisher | Licence | AI Use Permitted | Attribution String | Date Checked | Evidence File |
|---|--------|---------|-----------|---------|------------------|-------------------|--------------|---------------|
| 1 | FWC Decisions Database | Unfair dismissal decisions (2019–2026) | Fair Work Commission | Court/tribunal copyright — reproduction of decisions in unaltered form with acknowledgement permitted; altered/commercial reuse restricted | **Y (check each decision's copyright statement)** | "Source: Fair Work Commission, [Case Name], [Citation], [Date]" | 2026-07-31 | evidence/fwc_decision_copyright.md |
| 2 | FWC Benchbooks | Unfair dismissal, general protections summaries of principle | Fair Work Commission | Check reuse terms | **TBD — verify before ingestion** | TBD | 2026-07-31 | evidence/fwc_benchbook_terms.md |
| 3 | Federal Register of Legislation | Fair Work Act 2009, Fair Work Regulations | Commonwealth of Australia | CC BY 4.0 (confirm per item) | **Y** | "© Commonwealth of Australia, Fair Work Act 2009, sourced from legislation.gov.au" | 2026-07-31 | evidence/federal_register_tou.md |
| 4 | Fair Work Ombudsman | Plain-language guidance | Fair Work Ombudsman | Check reuse terms | **Y (good for user explanation, not legal propositions)** | "Source: Fair Work Ombudsman" | 2026-07-31 | evidence/fwo_terms.md |
| 5 | AustLII | N/A | Australasian Legal Information Institute | **PROHIBITED** — usage policy prohibits AI-related use including semantic retrieval, summarisation, paraphrasing, integration into decision-support systems | **N — DO NOT INGEST** | N/A | 2026-07-31 | evidence/austlii_usage_policy.pdf |
| 6 | Westlaw AU | Headnotes, commentary, citator | Thomson Reuters | Restrictive terms; headnotes and editorial value-add separately protected | **N (unless negotiated licence)** | N/A | 2026-07-31 | evidence/westlaw_au_terms.md |
| 7 | LexisNexis | Headnotes, commentary, citator | RELX Group | Restrictive terms; headnotes and editorial value-add separately protected | **N (unless negotiated licence)** | N/A | 2026-07-31 | evidence/lexis_terms.md |
| 8 | Jade | Case law, legislation | LexisNexis | Restrictive terms | **N (unless negotiated licence)** | N/A | 2026-07-31 | evidence/jade_terms.md |
| 9 | CCH | Commentary, case digests | Wolters Kluwer | Restrictive terms; editorial content separately protected | **N (unless negotiated licence)** | N/A | 2026-07-31 | evidence/cch_terms.md |
| 10 | Federal Court | Court decisions | Federal Court of Australia | Copyright statement permits reproduction in unaltered form with acknowledgement | **Y (under copyright statement terms)** | "Source: Federal Court of Australia, [Case Name], [Citation]" | 2026-07-31 | evidence/federal_court_copyright.md |
| 11 | FCFCOA | Court decisions | Federal Circuit and Family Court of Australia | Check copyright statement per publication | **TBD** | TBD | 2026-07-31 | evidence/fcfoa_terms.md |

## Notes

- **Australia has no text-and-data-mining (TDM) exception.** Government is consulting via Copyright and AI Reference Group. Do not assume TDM carve-out arrives.
- **AustLII prohibition is absolute.** Their policy explicitly bans: "use of AustLII's data for any AI-related purpose, including training, semantic retrieval, summarisation, paraphrasing, or integration into decision-support systems."
- You may **link** users to AustLII for manual verification (FWC guidance contemplates this) — different act from ingesting.
- Commercial publishers (Westlaw, Lexis, Jade, CCH): licence or exclude. Do not assume fair use.
- Court/tribunal copyright statements typically permit reproduction in unaltered form with acknowledgement. Read each source's statement individually.
- Every source entry should have an evidence file in `evidence/` directory.
- **Review monthly.** Regulatory positions changing on scale of weeks.
