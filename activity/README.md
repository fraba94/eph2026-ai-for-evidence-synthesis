# Hands-on exercise: AI for screening and data extraction

**Question.** *Are hand hygiene interventions effective in reducing healthcare-associated infections?*

The topic is deliberately obvious and uncontroversial, so that your attention goes to the **method**: how an AI tool
screens abstracts and extracts data, where it fails, and how you would notice. You will compare what the AI does with
**the reference review**, a published systematic review on this question conducted by human reviewers without AI
for screening, extraction or synthesis. Its decisions are the answers you compare with (details:
[`data/README.md`](data/README.md)).

> **The point of the exercise.** AI can bring real advantages to evidence synthesis (speed, scale, consistency,
> living updates), but only in the hands of people with AI literacy and advanced skills. Without understanding how
> these systems work you can make serious errors without seeing them, and lose control of the process. The human
> reviewer stays responsible for every decision. Today you practise the checks that keep you in the loop.

| | |
|---|---|
| **Time** | 30 minutes in small groups, inside a 60-minute session |
| **You need** | a laptop, any chat assistant (ChatGPT, Claude, Gemini, Copilot, Mistral...) or a coding agent |
| **Group** | 3 to 4 people, one screen is enough |
| **Output** | screening decisions, one extraction table, a filled [discrepancy log](worksheets/discrepancy_log.md) |
| **Not finishing** | is expected. A careful comparison of 10 records beats a fast run of 60 |

---

## The 60-minute session

| Time | Block | Who |
|---:|---|---|
| 0-10 | **Expert discussion.** Limitations of AI in evidence reviews (Patrick Boudreau, about 5 min), then benefits (Francesco Baglivo, about 5 min) | speakers |
| 10-20 | **Demo** of selected open-access AI tools on the same question | speakers |
| 20-50 | **Small-group exercise** (this page): step 1 screening (10 min), step 2 extraction (12 min), step 3 compare with the reference (8 min) | you |
| 50-60 | **Structured discussion**: performance, transparency, bias, human oversight, reproducibility | everyone |

---

## Group roles

Agree on the roles in the first minute. Rotate if you like.

| Role | Does |
|---|---|
| **Driver** | types, uploads, runs the tool; one screen for the whole group |
| **Prompter** | writes and refines the prompts; reads the criteria to the AI, not from memory |
| **Verifier** | checks the AI against the source: opens the abstract or the paper and looks for every quote and number |
| **Recorder** | fills the [AI use record](worksheets/ai_use_record.md) (model, version, date, prompts) and the [discrepancy log](worksheets/discrepancy_log.md) |

---

## Choose your track

| | **Chat track** | **Agent track** |
|---|---|---|
| For | anyone with a chat assistant | people already using Claude Code, Codex CLI, Gemini CLI or similar |
| Screening | **20 records**: R001-R020 (batch 1 of the [batch page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html), which fills missing abstracts from PubMed) | all **60 records** in [`data/screening_records.csv`](data/screening_records.csv) |
| Extraction | **1 paper**: [`data/fulltext/Phan2020.txt`](data/fulltext/Phan2020.txt) (or [`Mestre2012.txt`](data/fulltext/Mestre2012.txt)) | the **3 papers** in [`data/papers.csv`](data/papers.csv) |
| Help | step-by-step walkthrough and ready prompts: [`../beginners/README.md`](../beginners/README.md), prompt library [`../prompts/README.md`](../prompts/README.md) | skills for screening, extraction, quote checking and discrepancy audit: [`../skills/README.md`](../skills/README.md) |
| Scoring | [browser scorer](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html) | `python3 activity/tools/score_screening.py` and `score_extraction.py` |

> ⚠️ **For learning only.** These prompts are teaching material for this workshop. They are not a validated method.
> If you are not confident with how large language models work (context windows, parsing, sampling, retrieval,
> hallucination) and with advanced techniques (structured outputs, verification against the source, reproducibility
> checks, documentation of model and version), **do not use AI to conduct a real evidence review.** You stay
> responsible for every decision: the AI does not.

**Two rules for both tracks.** Do not open [`answers/`](answers/README.md) before step 3. Upload or paste only texts
whose licence allows it (the `license` column of the records, the `licence` column of
[`data/papers.csv`](data/papers.csv)), and never personal or confidential data.

---

## The eligibility criteria (from the reference review)

PICO: **P** patients and healthcare workers in acute care hospitals · **I** hospital-wide or multi-ward multimodal
hand hygiene intervention · **C** pre-intervention period, standard practice or a contemporaneous comparator ·
**O** clinical healthcare-associated infection outcomes · **Design** quasi-experimental studies.

A record is **included** only if it meets **all** of C1 to C6. Paste these criteria into your prompt word for word
(they are also in [`review_config.yaml`](review_config.yaml), which contains no answers).

| | Criterion | Include | Exclude |
|---|---|---|---|
| **C1** | Setting | Acute care hospital (general, tertiary referral or teaching hospital providing short-term inpatient care) | Only long-term care, nursing homes, outpatient or ambulatory care, rehabilitation; veterinary settings |
| **C2** | Scope | Implemented hospital-wide or across more than one inpatient ward or department | Only a single ICU, neonatal ICU, emergency department or any other isolated single unit |
| **C3** | Intervention | Multimodal hand hygiene intervention (at least two components, e.g. education, reminders, audit and feedback, hand rub availability, leadership, champions) that is the clearly central focus | A single isolated measure (posters alone, glove policy, product comparison, electronic monitoring alone); broad infection-prevention bundles (screening, isolation, cohorting, cleaning, stewardship) where hand hygiene is one component whose contribution cannot be interpreted |
| **C4** | Design | Interrupted time series, controlled before-after, or uncontrolled before-after with clearly defined pre- and post-intervention periods | Randomised trials (including cluster), cross-sectional or descriptive studies, outbreak reports, case reports, editorials, letters, conference abstracts, reviews |
| **C5** | Outcome | At least one clinical HAI outcome (overall HAI rate, CLABSI, CAUTI, VAP, *C. difficile* infection, MRSA or VRE acquisition or infection, other defined hospital-acquired infection) | Only process measures (compliance, hand rub consumption, knowledge, microbial counts on hands) |
| **C6** | Language | English (no date limits) | Other languages |

At title/abstract stage, if the abstract does not let you decide, the answer is **unsure**, not exclude.

---

## Step 1 · Screening (10 min)

1. **Load the records.** Chat track: open the [batch page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html), copy **batch 1** (R001-R020). Agent
   track: the full CSV. Some abstracts are empty in the repository because their licence does not allow
   redistribution: the batch page fetches them from PubMed in your browser; agents can run
   `python3 activity/tools/fetch_abstracts.py` (writes a local copy in `activity/data/local/`).
2. **Prompt.** Give the AI the question, the criteria C1-C6 verbatim and the output format: one row per record,
   `record_id,decision,reason`, decision `include | exclude | unsure`, reason naming the criterion (e.g. `C2: single
   ICU`). Ask for **every** record back and for `unsure` when in doubt.
3. **Check the count.** Did you get back exactly as many rows as you sent? Any record missing, duplicated or renamed?
4. **Verifier:** pick 3 decisions and check them against the abstract yourself.
5. **Save** the output (header `record_id,decision,reason`) as `run1.csv` in the chat track (same names as the
   [beginners walkthrough](../beginners/README.md)) or `screening_run1.csv` in the agent track.

<details>
<summary>Hints</summary>

- A prompt that starts from the criteria gets better results than "is this relevant to hand hygiene?".
- Ask the AI to quote the phrase of the abstract that decides each criterion: it makes the verifier's job faster.
- Records without an abstract: decide on the title and mark `unsure` with reason `no abstract`.
- Agent track: `.claude/skills/title-abstract-screening/` runs two independent passes and lists the disagreements.
- If you have one spare minute, **run the same prompt again in a new chat** and save `run2.csv` (agents:
  `screening_run2.csv`): you will measure reproducibility in step 3.

</details>

## Step 2 · Data extraction (12 min)

*Chat track: optional if screening took longer. A careful screening comparison is worth more than a rushed
extraction; you can do extraction at home with the same files.*

1. **Look at the form first**, before uploading anything: [`data/extraction_form.csv`](data/extraction_form.csv)
   (19 fields; the 11 marked `core = yes` are enough for the chat track). Discuss in 1 minute what each core field
   means for this paper type.
2. **One paper per conversation.** Chat track: paste or upload [`Phan2020.txt`](data/fulltext/Phan2020.txt) (or
   [`Mestre2012.txt`](data/fulltext/Mestre2012.txt)). Agent track: the three papers of
   [`data/papers.csv`](data/papers.csv) (the third, Al Kuwaiti 2017, is CC BY-NC: download it to your computer with
   `python3 activity/tools/fetch_fulltext.py`).
3. **Prompt.** Ask for a long table `study_id,field,value,source_quote,location`, a **verbatim quote** and a
   location (section or table) for every value, and `not reported` when the paper does not say it. Use the
   `study_id` from `papers.csv` (e.g. `Phan2020`).
4. **Verifier:** search 3 quotes in the paper (Ctrl+F). Then check every number against its quote.
5. **Save** as `extraction.csv`.

<details>
<summary>Hints</summary>

- Ask the model to break its own table, not to improve it: *"For each value, find the reason why it could be wrong."*
- Numbers live in tables, and tables are the hardest part to parse: check table values first.
- "Not reported" is a valid answer. A value with no quote is not a value.
- Retrieval tools (project knowledge, notebooks) answer from fragments: if a fragment is not retrieved, the AI says
  "not reported" instead of "I did not see it". For one paper, give the whole text.
- Sampling: run one paper twice and compare the two tables.

</details>

## Step 3 · Compare with the reference (8 min)

Now you may open [`answers/`](answers/README.md).

1. **Score.**
   - Browser: [scorer page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html): upload your CSV files.
   - Python (standard library only):
     ```bash
     # chat track
     python3 activity/tools/score_screening.py run1.csv --compare run2.csv
     # agent track: every record should have been screened
     python3 activity/tools/score_screening.py screening_run1.csv --compare screening_run2.csv --expect-all
     python3 activity/tools/score_extraction.py extraction.csv
     ```
2. **Read the coverage line first** ("Screened N of 60 records", records not screened), **then the misses**: missed includes (screening), `QUOTE NOT FOUND`, `unsupported` and `false absent`
   (extraction). Then the notes of the reference values: some papers contradict themselves.
3. **Fill the [discrepancy log](worksheets/discrepancy_log.md)** for at least 3 discrepancies: what the AI said,
   what the reference says, who is right after checking the source, and the error type.
4. **Finish the [AI use record](worksheets/ai_use_record.md)**.

<details>
<summary>How to read the screening score</summary>

**Coverage rule** (the same in the Python and the browser scorer): the metrics are computed on the records present
in your file, and the report always says how many were screened ("Screened N of 60 records"), lists the records
not screened, highlights any reference include among them, and gives the sensitivity *counting not-screened
includes as missed*. In the chat track you screen 20 records, so 40 "not screened" is expected. With `--expect-all`
(agent track) records not screened count as exclude in every metric. `unsure` counts as include.

The reference is the review's **final** decision. Some records were excluded by the review only after reading the
full text: including them at title/abstract stage is not an error. The scorer shows a "title/abstract-stage view"
for this, and the `gold_basis` column explains each reference decision. Sensitivity (missed includes) matters most.
One record is marked as a **possible error in the reference standard**: discuss it.

</details>

---

## Discussion (last 10 minutes of the session)

| Theme | Questions |
|---|---|
| **Performance** | How many includes did the AI miss? Would you accept that sensitivity in a real review? Was the time saved worth the time spent checking? |
| **Transparency** | Could you trace every decision and value to a sentence in the source? Which quotes were not in the paper? |
| **Bias** | Which kinds of records or fields did the AI get wrong systematically (single units, bundles, values only in tables or figures, countries it inferred)? |
| **Human oversight** | Where did a human catch an error the AI presented with confidence? Who in your group would sign this table? |
| **Reproducibility** | Did two runs of the same prompt agree? What would you report so that someone else can repeat what you did (see the AI use record)? |
| **The reference** | Is the reference standard always right? What did you find when the AI and the review disagreed? |

---

## Files of the exercise

| Path | What |
|---|---|
| [`review_config.yaml`](review_config.yaml) | Question, PICO, criteria C1-C6, reference review citation (no answers) |
| [`data/screening_records.csv`](data/screening_records.csv) | 60 records to screen (`record_id,pmid,doi,title,abstract,year,journal,license`) |
| [`data/extraction_form.csv`](data/extraction_form.csv) | Extraction form (`field,definition,allowed_values,type,core`) |
| [`data/papers.csv`](data/papers.csv), [`data/fulltext/`](data/fulltext/README.md) | The 3 extraction papers, links, licences, plain-text full texts |
| [`data/README.md`](data/README.md) | How the data were built, the reference review, limits, how to replace it |
| [`answers/`](answers/README.md) | Reference answers: **do not open before step 3** |
| [`tools/`](tools/) | Scorers and builders (Python 3, standard library only); every script has `--help` |
| [`examples/`](examples/README.md) | Fake decisions and extraction files to try the scorers |
| [`worksheets/`](worksheets/) | [Discrepancy log](worksheets/discrepancy_log.md) ([CSV](worksheets/discrepancy_log.csv)), [AI use record](worksheets/ai_use_record.md) |
| [`quick_card.md`](quick_card.md) | One-page printable card |
| [`facilitator_guide.md`](facilitator_guide.md) | For facilitators: timing, pitfalls, debrief |
