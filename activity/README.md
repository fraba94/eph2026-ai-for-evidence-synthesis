# Hands-on exercise: AI for screening and data extraction

**Question.** *Are hand hygiene interventions effective in reducing healthcare-associated infections?*

The topic is deliberately obvious and uncontroversial, so that your attention goes to the **method**: how an AI tool
screens abstracts and extracts data, where it fails, and how you would notice. You will compare what the AI does with
**the reference review**: Pruna et al., *J Clin Med* 2026, a systematic review of quasi-experimental studies in acute
care hospitals with **12 included studies**, in which two independent human reviewers did the screening, extraction,
risk of bias and synthesis without AI (the authors declare ChatGPT for English-language editing only). Its decisions
are the answers you compare with. The choice is **provisional**; citation, reasons and limits are in
[`data/README.md`](data/README.md). **Open the review after the exercise, not before:** it names the included studies.

This page is the guide for the live session (EPH 2026, Bilbao) **and** for anyone doing the exercise alone, months
later, without a facilitator or the slides: if that is you, start with
[Doing it on your own (self-paced)](#doing-it-on-your-own-self-paced).

> **The point of the exercise.** AI can bring real advantages to evidence synthesis (speed, scale, consistency,
> living updates), but only in the hands of people with AI literacy and advanced skills. Without understanding how
> these systems work you can make serious errors without seeing them, and lose control of the process. The human
> reviewer stays responsible for every decision. These skills are necessary, not sufficient: they work together
> with review methods expertise and a verification workflow. In this exercise you practise the checks that keep you
> in the loop.

| | |
|---|---|
| **Time** | Live session: 30 minutes in small groups, inside a 60-minute session. On your own: 60 to 90 minutes ([self-paced path](#doing-it-on-your-own-self-paced)) |
| **You need** | a laptop, any chat assistant (ChatGPT, Claude, Gemini, Copilot, Mistral...) or a coding agent |
| **Group** | 3 to 4 people, one screen is enough; alone works too: you take the four roles in turn |
| **Output** | screening decisions, one extraction table, a filled [discrepancy log](worksheets/discrepancy_log.md) |
| **Not finishing** | is expected. A careful comparison of 10 records beats a fast run of 60 |

---

## The 60-minute session

The live session: EPH 2026, Bilbao, skills building seminar M.8, Thursday 12 November 2026, 16:45-17:45.

| Min | Clock | Block | Who |
|---:|---|---|---|
| 0-10 | 16:45-16:55 | **Expert discussion.** Limitations of AI in evidence reviews (Patrick Boudreau, about 5 min), then benefits (Francesco Baglivo, about 5 min) | speakers |
| 10-20 | 16:55-17:05 | **Demo** of selected open-access AI tools on the same question ([what you will see](#the-demo)) | Francesco Baglivo and Patrick Boudreau |
| 20-50 | 17:05-17:35 | **Small-group exercise** (this page): step 1 screening (10 min, 17:05-17:15), step 2 extraction (12 min, 17:15-17:27), step 3 compare with the reference (8 min, 17:27-17:35) | you |
| 50-60 | 17:35-17:45 | **Structured discussion**: performance, transparency, bias, human oversight, reproducibility, and the reference itself | everyone |

### The demo

Before you start, Francesco Baglivo and Patrick Boudreau run the exercise in front of you, in four hands. **One drives
the AI, one checks the source.** Francesco is at the keyboard and uses the same pages and prompts you will use (the
[Start page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/start.html), the
[records page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html), the screening prompt, the
[scorer](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html)); Patrick asks "show me where it
says that" and checks the AI's answers against the abstract or the paper. Watch who catches the errors: the verifier,
not the AI. The demo uses batch 3 (R041-R060) and the paper Mestre2012, so that nothing you will work on is shown
in advance. Right after, your group does the same steps in the same roles (driver and verifier, see
[Group roles](#group-roles)).

Not at the session? The talks and the demo are not needed to do the exercise: the key message is above, and the
[self-paced path](#doing-it-on-your-own-self-paced) below replaces the facilitators and the slides.

---

## Group roles

Agree on the roles in the first minute. Rotate if you like. Alone, you take all four in turn: see the
[verifier checklist](#doing-it-on-your-own-self-paced).

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
| Screening | **20 records**: R001-R020 (batch 1 of the [records page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html), which fills missing abstracts from PubMed) | all **60 records** in [`data/screening_records.csv`](data/screening_records.csv) |
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

1. **Load the records.** Chat track: open the [records page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html), copy **batch 1** (R001-R020). Agent
   track: the full CSV. Some abstracts are empty in the repository because their licence does not allow
   redistribution: the records page fetches them from PubMed in your browser; agents can run
   `python3 activity/tools/fetch_abstracts.py` (writes a local copy in `activity/data/local/`). Records page not
   available? See [If the website is not available](#doing-it-on-your-own-self-paced).
2. **Prompt.** Give the AI the question, the criteria C1-C6 verbatim and the output format: one row per record,
   `record_id,decision,reason`, decision `include | exclude | unsure`, reason naming the criterion (e.g. `C2: single
   ICU`). Ask for **every** record back and for `unsure` when in doubt.
3. **Check the count.** Did you get back exactly as many rows as you sent? Any record missing, duplicated or renamed?
4. **Verifier:** pick 3 decisions and check them against the abstract yourself.
5. **Save** the output (header `record_id,decision,reason`) as `screening_run1.csv` (same name in both tracks and in the
   [beginners walkthrough](../beginners/README.md)).

<details>
<summary>Hints</summary>

- A prompt that starts from the criteria gets better results than "is this relevant to hand hygiene?".
- Ask the AI to quote the phrase of the abstract that decides each criterion: it makes the verifier's job faster.
- Records without an abstract: decide on the title and mark `unsure` with reason `no abstract`.
- Agent track: `.claude/skills/title-abstract-screening/` runs two independent passes and lists the disagreements.
- If you have one spare minute, **run the same prompt again in a new chat** and save `screening_run2.csv`: you will measure reproducibility in step 3.

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
   - Browser: [scorer page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html): load your CSV files (they stay in your browser).
   - Python (standard library only):
     ```bash
     # chat track
     python3 activity/tools/score_screening.py screening_run1.csv --compare screening_run2.csv
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

In the live session: one answer per group, in the last 10 minutes. On your own: answer each theme in writing, one or
two sentences, using your discrepancy log and AI use record as notes.

| Theme | Questions |
|---|---|
| **Performance** | How many includes did the AI miss? Would you accept that sensitivity in a real review? Was the time saved worth the time spent checking? |
| **Transparency** | Could you trace every decision and value to a sentence in the source? Which quotes were not in the paper? |
| **Bias** | Which kinds of records or fields did the AI get wrong systematically (single units, bundles, values only in tables or figures, countries it inferred)? |
| **Human oversight** | Where did a human catch an error the AI presented with confidence? Who in your group would sign this table? |
| **Reproducibility** | Did two runs of the same prompt agree? What would you report so that someone else can repeat what you did (see the AI use record)? |
| **The reference** | Is the reference standard always right? What did you find when the AI and the review disagreed? |

---

## Doing it on your own (self-paced)

Everything you need is in this repository; no facilitator, slides or group are required. Allow **60 to 90 minutes**.
Work through the same steps as the live session, with more time and one extra pause to verify before you look at
the answers.

| Block | Live session | On your own | What to do |
|---|---:|---:|---|
| Get ready | demo | 10 min | Read the key message and the criteria on this page; pick a track. New to AI? Follow the [beginners walkthrough](../beginners/README.md) (chat track, for learning only) |
| [Step 1 · Screening](#step-1--screening-10-min) | 10 min | 15-20 min | Batch 1 (R001-R020), then a second run in a new chat |
| [Step 2 · Data extraction](#step-2--data-extraction-12-min) | 12 min | 15-20 min | One paper (`Phan2020`), the 11 core fields, a quote for every value |
| Verify | (the verifier, during the steps) | 10 min | The verifier checklist below, **before** opening the answers |
| [Step 3 · Compare](#step-3--compare-with-the-reference-8-min) | 8 min | 10-15 min | Score, read the result (see below), log at least 3 discrepancies |
| [Discussion](#discussion-last-10-minutes-of-the-session) | 10 min | 10 min | Write one or two sentences per theme |

**One person, four roles.** Take the [group roles](#group-roles) in turn, not at once: as *prompter*, paste the
criteria and the form word for word; as *driver*, run the tool and save the files; then stop and become the
*verifier*, which is the part this exercise is about; as *recorder*, fill the
[AI use record](worksheets/ai_use_record.md) as you go. The verifier checklist:

- [ ] **Screening.** As many rows came back as you sent; no `record_id` missing, repeated or renamed.
- [ ] At least 3 decisions (one of them an *exclude*) checked against the abstract: does the abstract say what the reason claims?
- [ ] Every *exclude* names a criterion that the abstract clearly contradicts, not one it merely does not mention (that is *unsure*).
- [ ] No reason uses a rule that is not in C1-C6 (country, "low quality", date...).
- [ ] **Extraction.** At least 3 quotes found with Ctrl+F in the paper, character for character; every number in a value appears in its quote.
- [ ] Every `not reported` searched in the paper with synonyms (infection rate, nosocomial, hospital-acquired, per 1000 patient-days).
- [ ] **Record.** Tool, model and version as displayed, date, the exact prompts: in the [AI use record](worksheets/ai_use_record.md).

**When to open the answers.** Only after you have saved `screening_run1.csv` (and `screening_run2.csv`),
`extraction.csv` and done the checklist. The same applies to the reference review itself and to the
[facilitator guide](facilitator_guide.md): both name the included studies. If you use an agent, do not let it read
`answers/` before step 3 either.

**Reading the score without a facilitator.**

1. **Coverage line first.** In the chat track, "Screened 20 of 60 records (40 not screened)" is expected. Fewer than
   20 screened means the AI dropped or renamed records: that is already a finding.
2. **Missed includes.** The costly error at this stage. For each one, open the abstract: which criterion did the AI
   use, and was it right to?
3. **False includes.** Look at the "title/abstract-stage view" and the `gold_basis` column: a record excluded by the
   review only after reading the full text is not an error at title/abstract stage.
4. **Two runs.** Cohen's kappa between your runs: 1 means identical decisions; the lower it is, the more your result
   depends on chance. Every record that changed is a reproducibility problem.
5. **Extraction.** `QUOTE NOT FOUND`, `unsupported` and `false absent` matter more than small numeric differences;
   read the `notes` of the reference values, because some papers contradict themselves.
6. **The reference can be wrong.** One record is flagged as a possible error in the reference standard. Check the
   source before deciding who is right, and log at least 3 discrepancies in the
   [discrepancy log](worksheets/discrepancy_log.md).

After scoring, the sections "What to expect in screening", "What to expect in extraction" and "Interpreting the
scores" of the [facilitator guide](facilitator_guide.md) are your debrief.

**Discuss with yourself.** Answer the questions of the [discussion](#discussion-last-10-minutes-of-the-session) in
writing, one or two sentences per theme: performance, transparency, bias, human oversight, reproducibility, and the
reference itself. Then the one that matters most: *would you sign this screening and this table as they came out of
the AI, and what would you need to check first?*

**What next.**

- Do more: run the extraction twice and compare; try the second paper (`Mestre2012`); with a coding agent and the
  skills, screen all 60 records (agent track).
- Read the [five starting references](../README.md#useful-references), especially the position statement of
  Cochrane, the Campbell Collaboration, JBI and CEE and the RAISE recommendations, which say how AI use should be
  overseen and reported.
- Use the [prompt library](../prompts/README.md) for the other review stages, or the [agent skills](../skills/README.md)
  if you already work with coding agents.
- Before using AI in a real review, be honest about your AI literacy and skills (see the warning below), and pilot any
  tool on a sample with known answers, as you just did.
- Tell us what broke or what surprised you: [open an issue](https://github.com/fraba94/eph2026-ai-for-evidence-synthesis/issues/new/choose).

<details>
<summary><b>If the website (records page, scorer) is not available</b></summary>
<br>

The records page and the scorer are on GitHub Pages. If they do not open, everything still works:

- **Records**, with Python 3 and internet access to PubMed: Option B of the
  [beginners walkthrough](../beginners/README.md#step-2-screen-20-abstracts):
  `python3 activity/tools/fetch_abstracts.py`, then
  `python3 beginners/make_batches.py activity/data/local/screening_records_full.csv --size 20`, and paste
  `beginners/batches/screening_batch_01.md` (R001-R020). Both files are local and git-ignored: do not publish them.
- **Records, without Python:** open [`data/screening_records.csv`](data/screening_records.csv); for each record of
  R001-R020 with an empty abstract, open `https://pubmed.ncbi.nlm.nih.gov/<pmid>/` and copy the abstract word for
  word. Never ask the AI to find or write an abstract: it may invent one.
- **Both pages on your own computer:** `cd docs && python3 -m http.server 8000`, then open
  <http://localhost:8000/batch.html> and <http://localhost:8000/scorer.html> (the same pages, served locally).
- **Score** with the Python scorers in step 3 (standard library only); without Python, after step 3 compare your 20
  rows by hand with [`answers/screening_gold.csv`](answers/screening_gold.csv).

</details>

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
| [`facilitator_guide.md`](facilitator_guide.md) | For facilitators (timing, pitfalls, debrief). **Contains answers: participants read it only after step 3** |
