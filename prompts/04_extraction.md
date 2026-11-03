# 4. Data extraction from full texts

> ⚠️ For learning only: see the disclaimer in the [prompt library index](README.md). You stay responsible for every decision.

Design the form **before** you upload anything. One paper per conversation. A quote and a location for every value. "Not reported" is a valid answer. Workshop form: [`activity/data/extraction_form.csv`](../activity/data/extraction_form.csv).

Before extracting, remember: the model never sees your PDF, only the text a parser extracted from it. Tables are the hardest thing to parse, and many apparent "reasoning errors" on numbers are really parsing errors.

---

## 4.1 Design the form first

**Purpose.** Turn your objective into fields with names, definitions and permitted values, without the paper in view.
**When to use.** Before uploading any full text.

```text
I am preparing a data extraction form for a systematic review. Do not extract anything yet; I have not given you any paper.

Review question: [QUESTION]
Objective of this extraction: [e.g. describe the studies / the AI models and data sources / performance and comparators]

Propose a form as a table with columns: field | definition (one sentence) | allowed values or format | type (categorical / numeric / text).
Rules:
- Include at least one descriptive field and one numerical field.
- For numeric fields, define the format exactly (e.g. "AUROC as reported, with 95% CI if given; best model on external validation if available, else internal").
- Every field must allow the value "not reported".
- Flag fields where studies often report several values (several models, cohorts, time points) and ask me how to handle them.
```

**Check afterwards.** Edit the form yourself; pilot it on one paper; freeze it before extracting the rest.
**Failure modes.** Vague definitions ("performance") that produce inconsistent values; no rule for multiple models or cohorts.

---

## 4.2 Extract with quotes

**Purpose.** Fill the form for one paper with traceable values.
**When to use.** One paper per new conversation, with the whole paper attached or pasted (not a "chat with your folder" tool).

```text
You are extracting data for a systematic review. Use ONLY the attached paper. Do not use any outside knowledge.

EXTRACTION FORM (fill every field, do not add or change fields):
[PASTE FORM: field | definition | allowed values]

RULES
- For every field give: value, a verbatim quote copied exactly from the paper, and the location (section, table or figure, page).
- If the paper does not report the field, write value = not reported, leave the quote empty, and write in location where you looked.
- Do not round, convert units, or pick among several values without saying so. If several values exist (models, cohorts), list each on its own row and say which is which.
- If a value comes from a table, say so and give the row and column labels.

OUTPUT: only a CSV block with the header
study_id,field,value,source_quote,location
Use study_id = [STUDY ID]. One row per field (or per field and model if needed).

Reminder: verbatim quotes only; "not reported" is better than a guess.
```

**Expected output.** A CSV block, one row per field.
**Check afterwards.** Rows first (is any field missing?), then numbers (open the paper at each location), then every "not reported" (search the paper for the keyword and its synonyms).
**Failure modes.** Quotes that look verbatim but are reconstructed; values from the wrong row of a scrambled table; best model chosen silently; confidence intervals dropped; "not reported" for values that are in a table, a figure or the supplement.

---

## 4.3 Table check

**Purpose.** Expose parsing problems before trusting numbers that come from tables.

```text
Look at Table [N] of the attached paper.
1. Reproduce it as a markdown table exactly as you read it, without correcting anything.
2. Mark any cell where you are unsure which row or column a number belongs to.
3. Say whether the table appears complete (number of rows and columns you expected from its title and footnotes).
```

**Check afterwards.** Compare the reproduction with the PDF on screen. If it is scrambled, extract those values by hand.
**Failure modes.** Merged cells and multi-line headers shifting numbers to the wrong column; tables split across pages.
