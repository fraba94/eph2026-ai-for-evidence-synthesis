---
name: quote-verifier
description: Verify AI-extracted data against the source text - check that every quote occurs verbatim in the paper, that every number in a value appears in its quote, that the quote actually supports the value, and that each "not reported" is truly absent. Marks unsupported values instead of fixing them silently. Use after any AI extraction, when asked to "check", "verify" or "fact-check" an extraction table or a summary that cites papers, or before extracted data enter a synthesis.
argument-hint: "[extraction.csv] [source text file or folder]"
---

# Quote verifier

Fluency tells you nothing about correctness. A value is accepted only when its support can be found, word for word, in the source, and a human agrees that the passage says what the value says.

## Human in the loop
- You verify and flag; you do not correct values on your own. Proposed corrections go in a separate column for the human to accept.
- If the quote is found but you are unsure it supports the value (different population, outcome, time point, model, or metric), mark `support: unclear` and ask.
- Never "verify" against your memory of the paper or of the literature. The source text is the only reference.

## Procedure

1. **Get the source as text**, the same text the extraction used if possible (`pdftotext -layout paper.pdf S01.txt`). Name files `<study_id>.txt`. Note if the text came from a different parser than the extraction (differences in tables are then expected).
2. **Mechanical check** with the bundled script:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/verify_quotes.py extraction_ai.csv sources/ --out verification.csv
   ```
   Status per row: `quote_found`, `value_not_in_quote`, `quote_not_found`, `no_quote`, `not_reported`, `no_source`.
3. **Semantic check** of every `quote_found` row (the script cannot do this): does the passage support the value for the right population, outcome, model, validation set, time point and unit? Is a confidence interval or denominator dropped? Is a rounded or converted value declared?
4. **Absence check** of every `not_reported` row: search the full text for the field's keywords and synonyms (e.g. AUROC, AUC, ROC, C-statistic, c-index), check tables, figure captions and mentions of supplementary material. If found, mark `missed: present at <location>`.
5. **Repair the unsupported rows only by locating the real quote.** For `quote_not_found`: search the source for the value; if a verbatim passage exists, propose it as `proposed_quote`; if not, mark the value **unsupported**. Do not reword the quote to make it match.
6. **Write** `verification.csv` (script output plus your columns `support` = supported / unclear / unsupported / missed, and `proposed_quote`, `proposed_value`) and report: counts per status, every unsupported or missed row, and rows from regions flagged `[PARSING RISK]`.

## Output
- `verification.csv` with columns `study_id,field,value,source_quote,location,verification,note,support,proposed_quote,proposed_value`.
- A short report with the rows the human must look at, most serious first: unsupported values, missed values, unclear support.

## When NOT to use
- To judge whether the value is *correct in the world* or whether a study is good: this checks fidelity to the source, not truth or quality.
- On text obtained by OCR of scanned pages without first checking the OCR quality: mismatches will be noise.
- As a substitute for a second human extractor on the critical outcome data of a real review; it reduces, not removes, the need for human checking.
