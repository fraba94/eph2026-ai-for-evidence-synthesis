# Quick card · AI for screening and extraction

**Question:** Are hand hygiene interventions effective in reducing healthcare-associated infections?
**Compare with:** the reference review, Pruna et al., *J Clin Med* 2026 (12 included studies; screening and extraction by two human reviewers without generative AI). Screening answers after step 1, extraction answers after step 3.
**Full guide:** `activity/README.md` (on your own: section "Doing it on your own (self-paced)", 60-90 min)

**Work on your own**, on your own laptop: you drive the AI, then you verify it. Site: Start page, then one tap per material.

**Turn off web search / browsing and use a temporary chat (memory off).** The reference review is published: an AI
with web access may simply look up the answers (at a previous workshop in Berlin, one recognised the review and offered to repeat it).

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
Copy batch 1 (R001-R020) from the Records page and the screening prompt from the Start page (criteria already in it).
Paste both into a new temporary chat, web search off. Then **paste the AI's answer into the Scorer** as it is: no file to save.
Coverage line first: "Screened 20 of 60" is expected; fewer means records were dropped. In doubt or no abstract: **unsure**.

**Step 2 · Look at the errors · 10 min** (screening answers: now)
The Scorer lists the missed includes and the false includes. Open 2 of them (title and abstract, PubMed link) and
decide yourself why the AI got them wrong: which criterion, and was it right? Keep one error for the discussion.

**Step 3 · Short extraction · 10 min** (extraction answers: after this step)
Paper `Phan2020` (Papers page: Copy full text), the extraction prompt with **5 fields** already filled in:
`country`, `study_design`, `intervention_components`, `primary_hai_outcome`, `direction_of_effect`.
Each value with a verbatim quote and its location, or `not reported`. Verify 2 quotes with Ctrl+F.
Compare with the reference values on the Answers page. Read the notes: some papers contradict themselves.

**Discussion · 10 min:** each person brings **one error they found**.

**Going further:** a second run in a new chat; the 11 core fields; the discrepancy log and the AI use record; the
agent track (all 60 records, 3 papers, skills, `python3 activity/tools/score_screening.py ... --expect-all`).

**Ask yourself:** Performance: would I accept this sensitivity? Transparency: can I trace every value? Bias: whose
errors, which studies? Oversight: would I sign the table? Reproducibility: would a second run agree, and would two human reviewers? And the
reference: is it always right?

> ⚠️ **For learning only.** These prompts are teaching material for this workshop. They are not a validated method.
> If you are not confident with how large language models work (context windows, parsing, sampling, retrieval,
> hallucination) and with advanced techniques (structured outputs, verification against the source, reproducibility
> checks, documentation of model and version), **do not use AI to conduct a real evidence review.** You stay
> responsible for every decision: the AI does not.
