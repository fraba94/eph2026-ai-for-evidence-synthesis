# 5. Verification

> ⚠️ For learning only: see the disclaimer in the [prompt library index](README.md). You stay responsible for every decision.

The output is generated, not retrieved: a fluent answer is produced whether or not it is right. Verification is not optional, and the final check is yours, against the paper. Use these prompts in a **new conversation**, so the model is not checking its own reasoning in the same context.

---

## 5.1 Quote check

**Purpose.** Find values whose quotes are not in the paper, or do not support the value.

```text
You are verifying a data extraction. Use ONLY the attached paper.

For each row of the table below:
1. Search the paper for the quote. Answer FOUND (verbatim), NEAR (similar wording, give the real text), or NOT FOUND.
2. If FOUND or NEAR: does the passage support the value for the same population, outcome, model and time point? Answer yes / partly / no, with one sentence.
3. Do not correct values. Only report.

TABLE (study_id,field,value,source_quote,location):
[PASTE CSV ROWS]

Output a CSV with the header: study_id,field,quote_status,supports_value,comment
```

**Check afterwards.** Open the paper at every NOT FOUND, NEAR and "partly/no". If you have Python, a mechanical check is more reliable than the model for verbatim matching:
`python3 .claude/skills/quote-verifier/scripts/verify_quotes.py extraction.csv sources/ --out verification.csv`
**Failure modes.** The model says FOUND for a quote that is not there (it is checking its memory of the paper, not the text). Spot-check a few FOUND rows yourself.

---

## 5.2 "Not reported" check

**Purpose.** Catch retrieval and parsing failures reported as absence.

```text
In the attached paper, look for any information on each of these fields, which were marked "not reported":
[LIST FIELDS WITH THEIR DEFINITIONS]

For each field: search the main text, every table, figure captions and any mention of supplementary material, including synonyms (e.g. AUROC, AUC, ROC area, C-statistic).
Answer: PRESENT (quote + location) or ABSENT (list where you looked).
```

**Check afterwards.** For each PRESENT, verify the quote. For fields that matter, search the PDF yourself (Ctrl+F) with the synonyms.
**Failure modes.** Information only in figures or supplementary files that the model never received.

---

## 5.3 Compare two runs

**Purpose.** Check reproducibility of an extraction.

```text
Below are two extractions of the same paper made in separate conversations with the same prompt.
Compare them field by field. Output a table: field | run 1 value | run 2 value | same / different / one is more complete.
Do not decide which is right.

RUN 1: [PASTE CSV]
RUN 2: [PASTE CSV]
```

**Check afterwards.** Every "different" row goes back to the paper. Outcome numbers are usually less stable than study characteristics.
**Failure modes.** Treating the more detailed run as correct: completeness is not accuracy.
