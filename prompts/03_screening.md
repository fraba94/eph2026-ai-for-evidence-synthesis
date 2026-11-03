# 3. Title/abstract screening

> ⚠️ For learning only: see the disclaimer in the [prompt library index](README.md). You stay responsible for every decision.

The AI can be a second pair of eyes, not the reviewer. Ask it to be wrong in the safe direction: a false include costs a minute at full text, a missed include can change the conclusions. Workshop data: [`activity/data/screening_records.csv`](../activity/data/screening_records.csv); criteria in [`activity/README.md`](../activity/README.md) (also stored in [`activity/review_config.yaml`](../activity/review_config.yaml)). Worked example: hand hygiene interventions to prevent healthcare-associated infections.

---

## 3.1 Screen a batch (CSV output)

**Purpose.** Include/exclude/unsure for each record, with the criterion behind each decision.
**When to use.** With approved criteria, on batches of 10–20 records.

```text
You are a second reviewer screening titles and abstracts for a systematic review.

ELIGIBILITY CRITERIA (apply exactly these, nothing else):
[C1 ...]
[C2 ...]
[C3 ...]

RULES
- Decide for each record: include, exclude, or unsure.
- exclude ONLY if the title/abstract clearly shows that at least one criterion is NOT met. Name the criterion.
- include if all criteria are met or not contradicted by the abstract.
- unsure if information is missing or ambiguous. When in doubt, do not exclude.
- Do not use any knowledge about these studies beyond the text given.
- Return one row for EVERY record, in the same order. If the abstract is empty, decide on the title only and use unsure with reason "no abstract".

OUTPUT: only a CSV block with the header
record_id,decision,reason
where reason is max 25 words and starts with the criterion code (e.g. "C2 not met: ...").
After the CSV, write one line: "Records received: N. Rows returned: N."

RECORDS
[PASTE RECORDS: record_id, title, abstract]

Reminder: apply only criteria C1-C[n]; one row per record; when in doubt, unsure.
```

**Expected output.** A CSV block with one row per record and a count line.
**Check afterwards.**
- Count: rows returned = records sent? Any record missing or duplicated?
- Spot-check five reasons against the abstracts: is the quoted or paraphrased text really there?
- Read every *exclude*: is the named criterion clearly contradicted, or just not mentioned?
**Failure modes.** Abstracts "filled in" from the model's memory when the abstract field is empty (never ask it to find or write an abstract: fetch it from PubMed yourself); rows silently dropped in long batches; topical similarity treated as eligibility; excluding for missing information; reasons getting vaguer towards the end of the batch.

---

## 3.2 Second independent run

**Purpose.** Measure reproducibility. Outputs are sampled: the same prompt can give different decisions.
**When to use.** Always, for at least part of the batch.

Open a **new conversation** (no memory of the first run; turn off memory or use a temporary chat if your tool has it). Paste prompt 3.1 again with the records **in a different order** (for example reversed). Save them as `screening_run1.csv` and `screening_run2.csv` (the names used in `activity/README.md` and by the scorer).

Then compare in a spreadsheet, or with the helper script if you have Python:

```bash
python3 .claude/skills/title-abstract-screening/scripts/compare_runs.py activity/data/screening_records.csv screening_run1.csv screening_run2.csv --merged screening_merged.csv
```

**Check afterwards.** How many records changed decision? Any record that is *include* in one run and *exclude* in the other must be decided by you. A conservative merge treats every disagreement as *unsure*.
**Failure modes.** Running the second time in the same chat (it just repeats itself); comparing by eye on long lists.

---

## 3.3 Explain disagreements

**Purpose.** Understand *why* two runs (or the AI and you) disagree, so you can fix criteria or wording.

```text
Two screening passes disagreed on the records below. For each record:
1. Quote the exact words of the abstract that bear on the disputed criterion.
2. Say which reading of the criterion leads to include and which to exclude.
3. Say whether the disagreement comes from (a) missing information in the abstract, (b) ambiguous wording of the criterion, or (c) a plain error in one pass.
Do not make the final decision: I will.

CRITERIA: [PASTE]
RECORDS WITH BOTH DECISIONS AND REASONS: [PASTE]
```

**Check afterwards.** Read the quotes against the abstracts. Ambiguous criteria are a team decision; note any change and its date.
**Failure modes.** The model defends whichever answer it gave last; quotes that are paraphrases. Check each quote.
