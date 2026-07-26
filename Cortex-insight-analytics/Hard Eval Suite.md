# Hard Eval Suite

## Overview
25 advanced questions with content scoring for rigorous accuracy testing.

## Questions
| ID | Topic | Difficulty |
|----|-------|------------|
| H01 | Cleaning Award Level 3 rate | Specific |
| H02 | Hospitality consecutive days | Specific |
| H03 | General Retail casual loading | Specific |
| H04 | Restaurant ordinary hours | Specific |
| H05 | Fast Food public holiday penalty | Specific |
| H06 | NES annual leave | NES |
| H07 | NES termination notice | NES |
| H08 | Clerks probation period | Specific |
| H09 | Architects graduate salary | Specific |
| H10 | Professional Employee max hours | Specific |
| H11 | Clerks Saturday penalty | Specific |
| H12 | Hospitality meal break | Specific |
| H13 | Hospitality casual engagement | Specific |
| H14 | NES parental leave | NES |
| H15 | Restaurant Sunday penalty | Specific |
| H16 | General Retail overtime PT | Specific |
| H17 | Fast Food casual notice | Specific |
| H18 | NES 10 standards | NES |
| H19 | Fast Food junior hours | Specific |
| H20 | Sporting evening shift | Specific |
| H21 | Casual loading comparison | Comparison |
| H22 | Clerks span of hours | Specific |
| H23 | NES vs Awards differences | NES |
| H24 | Public holiday refusals | Specific |
| H25 | Hospitality Level 5 rate | Specific |

## Scoring
- **Keywords**: 40pts (exact match + synonyms)
- **Pattern**: 30pts (regex for specific values)
- **Quality**: 30pts (completeness, specificity)
- **Pass threshold**: 70% per question

## Run
```bash
venv/bin/python3 scripts/eval_hard.py
```

## Related
- [[Project Overview]] — System design
- [[Evaluation Results]] — Scores
- [[Evaluation Questions]] — Basic eval
