---
name: quote-verifier
description: Verify AI-extracted data or AI-written claims against the source text - check that every quote occurs verbatim in the paper, that every number in a value appears in its quote, that the quote supports the value (population, outcome, period, direction, magnitude), and that each "not reported" is truly absent. Marks unsupported or overstated values instead of fixing them silently. Use after any AI extraction or AI summary of studies, whenever asked to check, verify, audit or fact-check an extraction table or a text that cites papers, and before extracted data enter a synthesis.
license: CC-BY-4.0 (text) and MIT (scripts); see LICENSE and LICENSE-CODE in the source repository
compatibility: Bundled script needs Python 3 (standard library only). Written for Claude Code; any agent that reads SKILL.md can follow it.
metadata:
  version: '1.1'
  last-reviewed: '2026-11-03'
  author: EUPHA Digital Health and AI Section, EPH 2026 skills building seminar
  source: https://github.com/fraba94/eph2026-ai-for-evidence-synthesis
---

# Quote verifier

**Arguments:** `[extraction.csv] [source text file or folder]`

Fluency tells you nothing about correctness. A value is accepted only when its support can be found, word for word, in the source, and a human agrees that the passage says what the value says.

## Human in the loop
- You verify and flag; you do not correct values on your own. Proposed corrections go in a separate column for the human to accept.
- If the quote is found but you are unsure it supports the value (different population, outcome, period, arm, or metric), mark `support: unclear` and ask.
- Never "verify" against your memory of the paper or of the literature. The source text is the only reference.

## Procedure

1. **Get the source as text**, the same text the extraction used if possible (`pdftotext -layout paper.pdf S01.txt`). Name files `<study_id>.txt` (in the workshop the texts are already in `activity/data/fulltext/`, e.g. `Phan2020.txt`). Inside the workshop repository the script uses the scorer's own text normalisation (`activity/tools/common.py`), so its "found" agrees with `score_extraction.py`. Note if the text came from a different parser than the extraction (differences in tables are then expected).
2. **Mechanical check** with the bundled script:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/verify_quotes.py extraction.csv activity/data/fulltext/ --out verification.csv
   ```
   Status per row: `quote_found`, `value_not_in_quote`, `quote_not_found`, `no_quote`, `not_reported`, `no_source`.
3. **Semantic check** of every `quote_found` row (the script cannot do this): does the passage support the value for the right population, outcome, ward or period, time point and unit? Do the **direction** (reduction vs increase, favourable vs unfavourable) and the **magnitude** match? Is a confidence interval or denominator dropped? Is a rounded or converted value declared? A value that goes beyond its passage (a trend called significant, an association called an effect, a caveat dropped) is `overstated`, not `supported`.
4. **Absence check** of every `not_reported` row: search the full text for the field's keywords and synonyms (e.g. healthcare-associated, nosocomial, hospital-acquired, infection rate, incidence density, per 1000 patient-days), check tables, figure captions and mentions of supplementary material. If found, mark `missed: present at <location>`.
5. **Repair the unsupported rows only by locating the real quote.** For `quote_not_found`: search the source for the value; if a verbatim passage exists, propose it as `proposed_quote`; if not, mark the value **unsupported**. Do not reword the quote to make it match.
6. **Write** `verification.csv` (script output plus your columns `support` = supported / overstated / unclear / unsupported / missed, and `proposed_quote`, `proposed_value`) and report: counts per status, every unsupported, overstated or missed row, and rows from regions flagged `[PARSING RISK]`.

## Checking a text that cites papers (summary, discussion, slide)
Work **one cited source at a time**, with all the sentences that cite it together, so that contradictions between two mentions of the same paper become visible. For each sentence: find the supporting passage in the source (abstract first; full text whenever the sentence gives a number, a quote or a method detail, or the abstract is silent), then classify it `supported`, `overstated`, `unsupported` (the source says something else, or the passage cannot be found) or `unverifiable` (the source text is not available here: an access problem, not a verdict). A citation that cannot be resolved to a real record is `unsupported`; say so instead of searching for a "close" paper.

## Output
- `verification.csv` with columns `study_id,field,value,source_quote,location,verification,note,support,proposed_quote,proposed_value`.
- A short report with the rows the human must look at, most serious first: unsupported values, missed values, overstated values, unclear support.

## When NOT to use
- To judge whether the value is *correct in the world* or whether a study is good: this checks fidelity to the source, not truth or quality.
- On text obtained by OCR of scanned pages without first checking the OCR quality: mismatches will be noise.
- As a substitute for a second human extractor on the critical outcome data of a real review; it reduces, not removes, the need for human checking.
