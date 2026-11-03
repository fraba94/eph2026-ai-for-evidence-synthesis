# Quick card · AI for screening and extraction

**Question:** Are hand hygiene interventions effective in reducing healthcare-associated infections?
**Compare with:** the reference review (human, without AI). Full guide: `activity/README.md`

| Roles | |
|---|---|
| Driver | types and runs the tool |
| Prompter | writes prompts, pastes the criteria verbatim |
| Verifier | checks every quote and number in the source |
| Recorder | AI use record + discrepancy log |

**Include only if ALL are met**

| | |
|---|---|
| C1 | Acute care hospital (not long-term care, outpatient, rehabilitation, veterinary) |
| C2 | Hospital-wide or more than one ward (not a single ICU, NICU, ED or unit) |
| C3 | Multimodal hand hygiene intervention, clearly central (not one isolated measure; not a broad bundle) |
| C4 | Interrupted time series or before-after (not RCTs, cross-sectional, outbreak reports, reviews) |
| C5 | At least one clinical HAI outcome (not only compliance or hand rub use) |
| C6 | English |

**Step 1 · Screening · 10 min**
Chat: batch 1 (R001-R020) from the batch page. Agent: all 60.
Output `record_id,decision,reason` · decision `include | exclude | unsure` · reason = criterion.
Count the rows back. When in doubt: **unsure**. Save `run1.csv` (agent: `screening_run1.csv`).

**Step 2 · Extraction · 12 min**
Read the form first (`data/extraction_form.csv`, core fields). One paper per chat (chat: `Phan2020.txt`).
Output `study_id,field,value,source_quote,location`. Verbatim quote for every value; `not reported` is allowed.
Verifier: Ctrl+F three quotes. Save `extraction.csv`.

**Step 3 · Compare · 8 min** (now open `answers/`)
Browser scorer, or:
`python3 activity/tools/score_screening.py run1.csv` (agent: add `--expect-all`)
`python3 activity/tools/score_extraction.py extraction.csv`
Read first: missed includes · QUOTE NOT FOUND · unsupported · false absent. Log 3 discrepancies.

**Ask yourselves:** Would we accept this sensitivity? Can we trace every value? Did two runs agree? Is the reference
always right? Who signs the table?

> ⚠️ **For learning only.** These prompts are teaching material for this workshop. They are not a validated method.
> If you are not confident with how large language models work (context windows, parsing, sampling, retrieval,
> hallucination) and with advanced techniques (structured outputs, verification against the source, reproducibility
> checks, documentation of model and version), **do not use AI to conduct a real evidence review.** You stay
> responsible for every decision: the AI does not.
