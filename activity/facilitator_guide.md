# Facilitator guide

For the people running the hands-on part of the seminar. Participants use [`README.md`](README.md); this page adds
timing, preparation, the pitfalls you should expect, and how to run the debrief. It contains answers: do not project it.

## Before the session

| When | Check |
|---|---|
| The day before | Open the [batch page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html) and the [scorer](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html) on the published site; copy batch 1 and confirm that the empty abstracts are filled from PubMed |
| The day before | On each facilitator laptop: `python3 activity/tools/fetch_abstracts.py` and `python3 activity/tools/fetch_fulltext.py` (local copies in `activity/data/local/`, git-ignored: do not publish them). This is the fallback if the venue network blocks NCBI |
| The day before | Run the scorers on the examples: `python3 activity/tools/score_screening.py activity/examples/decisions_example.csv` and `python3 activity/tools/score_extraction.py activity/examples/extraction_example.csv` |
| The day before | Print the [quick card](quick_card.md) (one per group) and a few copies of the [discrepancy log](worksheets/discrepancy_log.md) |
| On arrival | Write on a slide or board: the repository short link, "Chat track: batch 1 = R001-R020, paper Phan2020", "Do not open `answers/` before step 3" |

If the reference review has been replaced, rebuild first (see [`data/README.md`](data/README.md#how-to-replace-the-reference-review)) and re-read the record IDs below.

## Timing (60 minutes)

| Min | Block | Facilitator cue |
|---:|---|---|
| 0-10 | Expert discussion: **Patrick Boudreau** on limitations (about 5 min), then **Francesco Baglivo** on benefits (about 5 min) | End on the key message: advantages only with AI literacy; humans stay responsible |
| 10-20 | Demo of open-access tools | Show one screening prompt and one extraction prompt on the same question, including one visible error |
| 20-21 | Groups form, roles assigned | "Driver, prompter, verifier, recorder. Choose chat or agent track." |
| 21-31 | **Step 1 screening** | At minute 26: "Did you count the rows that came back?" At 30: "Save the file, even if incomplete" |
| 31-43 | **Step 2 extraction** | At 31: "Read the form for one minute before uploading." At 38: "Verifier: search three quotes now" |
| 43-51 | **Step 3 compare** | "Open the scorer. Read missed includes and QUOTE NOT FOUND first. Log three discrepancies" |
| 51-60 | Structured discussion | Use the prompts below; collect one sentence per group |

## What to expect in screening

Record IDs refer to the current build (seed 2026). Chat track groups see R001-R020 (4 includes).

| Record(s) | Reference | Typical AI behaviour and why it is instructive |
|---|---|---|
| R003 (multicentre programme, Chicago), R022 (national Cleanyourhands campaign), R017 (automated monitoring plus promotion), R040 (7-hospital system, CLABSI), R060 (Targeted Solutions Tool) | include | Often missed: the outcome is antimicrobial resistance or an association with HAI (C5 looks weak), the setting is national or a health system (C1/C2 look odd), or electronic monitoring triggers the "single measure" exclusion in C3 although it is embedded in a wider strategy |
| R039 (hospital-wide programme, Geneva) | exclude, flagged | Appears to meet all criteria but is not among the review's included or full-text-excluded studies: **possible gold-standard error**. Use it to ask "who checks the reference?" |
| R007, R009, R051 (single neonatal ICU), R045 (single urology ward), R013 (mixed ICU) | exclude | Include-looking abstracts with HAI outcomes: the AI must apply C2 (single unit). Good test of whether the criteria were pasted verbatim |
| R005, R015 and other bundles | exclude | Hand hygiene appears in the abstract, but as one component of MRSA/CRE/HAI bundles: C3 requires judgement; `unsure` is acceptable at this stage |
| R034, R047 (randomised trials) | exclude | Strong designs excluded by C4: participants are often surprised, which is a good moment to say that criteria are the review's choice, not the AI's |
| R023 (equine hospitals) | exclude | Tests whether anyone (human or AI) reads past the title |
| The 21 records the review excluded after full text (e.g. R013, R020, R031, R046, R050, R054) | exclude (final) | Including them at title/abstract stage is **correct behaviour**; the scorer's "title/abstract-stage view" counts them as include |
| Any batch | - | Rows dropped, renamed IDs, decisions without a criterion, `exclude` used instead of `unsure`, long batches where middle records get shorter reasons |

## What to expect in extraction

All three papers contain traps that come from the papers, not from the AI. The `notes` column of
[`answers/extraction_gold.csv`](answers/extraction_gold.csv) explains each one.

| Paper | Pitfall | What a careful extraction does |
|---|---|---|
| Phan2020 | Post-intervention compliance 75.1% in the text, 75.0% in Table 1; Table 1 title says 2010-2016 but runs to 2018 | Quotes the text value and notices the table difference |
| Phan2020 | HAI outcome called "overall HAI" in Results, "HAI other than SSI" in the Discussion and in the reference review | Names the outcome as the authors define it in Methods |
| Phan2020 | IRR 0.85 is a per-year trend, not a before-after ratio | Says what the estimate measures |
| Phan2020 | Concurrent CAUTI programme and SSI measures | Reports co-interventions instead of "none" |
| Mestre2012 | The country is never stated (only "Catalonian Regional Campaign"); the reference review says Spain | `not reported`, or a value flagged as inferred. "Barcelona, Spain" with a quote is a fabricated quote |
| Mestre2012 | The HAI outcome (MRSA) is secondary; the primary outcome is compliance | Does not report compliance as the HAI outcome |
| Mestre2012 | MRSA rates shown only in a control chart: no numbers in the text | `not reported` for baseline and post rates; numbers "read" from the figure are not in the text |
| Mestre2012 | Baseline period given three ways (March 2007, October 2007, 2007-2008); phase 1 compliance 78% in Table 2 but 79.5% in the Abstract, with a CI that does not contain 78; denominator per 1,000 in Methods vs per 10,000 in Results | Flags internal inconsistencies |
| AlKuwaiti2017 | Post-intervention HAI rate 2.59 (Abstract, Results), 2.5483 (Table II, 2016) and 2.55 (Discussion); which year was the intervention year is not stated | Quotes one value and its location, notes the others |
| AlKuwaiti2017 | No surveillance definition; no effect estimate (only P < 0.05); a non-significant correlation (r = -0.278, p = 0.381) easily reported as an "effect" | `not reported` where the paper is silent |
| AlKuwaiti2017 | Licence CC BY-NC: not shipped in the repository | Agent track fetches it locally; chat track uses Phan2020 or Mestre2012 |

## Interpreting the scores

- **Sensitivity first.** At title/abstract stage, a missed include is the costly error. Precision against the final
  decision is naturally low because 21 records reached the review's full-text stage: point groups to the
  title/abstract-stage view and to `gold_basis`.
- **Kappa between two runs** shows sampling variability: the same prompt, the same records, different answers. Ask
  what a reviewer would report about it.
- **Extraction:** `QUOTE NOT FOUND` (invented or paraphrased quote), `unsupported` (value where the paper is silent)
  and `false absent` (missed information, often in tables) matter more than small numeric differences. `within tol.`
  values deserve a look (e.g. 2.55 vs 2.59 in AlKuwaiti2017 are two different numbers of the same paper).
- **The reference can be wrong.** R039; the review's Table 1 citing "Larson et al., 2010" for a 2000 paper; the
  review reporting "Spain" for Mestre2012 although the paper does not say so. Treat a discrepancy as a question for
  the source, not a verdict on the AI.

## Debrief prompts (last 10 minutes)

1. **Performance.** Hands up: who missed at least one include? Which one, and why?
2. **Transparency.** Who found a quote that was not in the paper? How long did it take to find out?
3. **Bias.** Were the errors random, or always the same kind (single units, bundles, numbers in tables, inferred
   countries)?
4. **Oversight.** Who would sign the extraction table as it came out of the AI? What would you need to check first?
5. **Reproducibility.** Did your two runs agree? What should go in a methods section so that someone can repeat it?
6. **The reference.** Did anyone disagree with the reference after checking the source?

Close with the repository's position: these tools can help people who understand how they work and verify them
systematically; for everyone else the beginners track is **for learning only**, not for real reviews.

## If things go wrong

| Problem | Fallback |
|---|---|
| Network blocks NCBI (batch page cannot fill abstracts) | Use the 17 records shipped with abstracts, or share the local `screening_records_full.csv` on the facilitator laptop screen (do not post it online) |
| Chat assistant refuses uploads | Paste the text from [`data/fulltext/Phan2020.txt`](data/fulltext/Phan2020.txt) in two halves, in the same conversation |
| Group is fast | Second run in a new chat; or a second paper; or the agent track on all 60 records |
| Group is slow | Screen 10 records only; extract the core fields only (`--core-only` in the scorer) |
