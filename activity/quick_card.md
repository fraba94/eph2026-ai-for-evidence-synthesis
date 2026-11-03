# Quick card · AI for screening and extraction

**Question:** Are hand hygiene interventions effective in reducing healthcare-associated infections?
**Compare with:** the reference review, Pruna et al., *J Clin Med* 2026 (12 included studies; screening and extraction by two human reviewers without AI; provisional). Do not open it before step 3.
**Full guide:** `activity/README.md` (on your own: section "Doing it on your own (self-paced)", 60-90 min)

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
Chat: batch 1 (R001-R020) from the records page. Agent: all 60.
Output `record_id,decision,reason` · decision `include | exclude | unsure` · reason = criterion.
Count the rows back; verifier checks 3 decisions against the abstract. In doubt or no abstract: **unsure**.
Save `screening_run1.csv`. Spare minute: same prompt in a new chat, save `screening_run2.csv`.

**Step 2 · Extraction · 12 min**
Read the form first (`data/extraction_form.csv`, 11 core fields). One paper per chat (chat: `Phan2020.txt`, study_id `Phan2020`).
Output `study_id,field,value,source_quote,location`. Verbatim quote for every value; `not reported` is allowed.
Verifier: Ctrl+F three quotes. Save `extraction.csv`.

**Step 3 · Compare · 8 min** (now open `answers/`)
Browser scorer, or:
`python3 activity/tools/score_screening.py screening_run1.csv --compare screening_run2.csv` (agent: add `--expect-all`)
`python3 activity/tools/score_extraction.py extraction.csv`
Read the coverage line first ("Screened 20 of 60" is expected in the chat track), then: missed includes · QUOTE NOT FOUND · unsupported · false absent. Log 3 discrepancies in `worksheets/discrepancy_log.md`: who is right, after checking the source.

**Ask yourselves:** Performance: would we accept this sensitivity? Transparency: can we trace every value? Bias: whose
errors, which studies? Oversight: who signs the table? Reproducibility: did two runs agree? And the reference: is it
always right?

> ⚠️ **For learning only.** These prompts are teaching material for this workshop. They are not a validated method.
> If you are not confident with how large language models work (context windows, parsing, sampling, retrieval,
> hallucination) and with advanced techniques (structured outputs, verification against the source, reproducibility
> checks, documentation of model and version), **do not use AI to conduct a real evidence review.** You stay
> responsible for every decision: the AI does not.
