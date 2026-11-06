# Hands-on exercise: AI for screening and data extraction

**Question.** *Are hand hygiene interventions effective in reducing healthcare-associated infections?*

The topic is deliberately obvious and uncontroversial, so that your attention goes to the **method**: how an AI tool
screens abstracts and extracts data, where it fails, and how you would notice. You will compare what the AI does with
**the reference review**: Pruna et al., *J Clin Med* 2026, a systematic review of quasi-experimental studies in acute
care hospitals with **12 included studies**, in which two independent human reviewers did the screening, extraction,
risk of bias and synthesis without AI (the authors declare ChatGPT for English-language editing only). Its decisions
are the answers you compare with. The choice was confirmed by the workshop team on 6 November 2026; citation, reasons and limits are in
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
| **Time** | Live session: 30 minutes on your own, inside a 60-minute session. On your own, later: 60 to 90 minutes ([self-paced path](#doing-it-on-your-own-self-paced)) |
| **You need** | a laptop (a phone works for reading the pages), any chat assistant (ChatGPT, Claude, Gemini, Copilot, Mistral...) or a coding agent |
| **How** | individually: each person on their own laptop. You drive the AI, then you verify it |
| **Three moves** | 1 screen 20 records and paste the AI's answer into the scorer · 2 look at two of its errors · 3 extract 5 fields from one paper, with quotes |
| **Not finishing** | is expected. Two errors you understand are worth more than twenty decisions you did not check |

## All materials at a glance

Everything for the hands-on part is on the workshop website, one tap away on a phone or a laptop.

| Material | Where |
|---|---|
| Start page: the three steps in order, with every button | [Start](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/start.html) |
| Eligibility criteria C1-C6 | [On this page](#the-eligibility-criteria-from-the-reference-review) |
| Step 1: records to screen, copy-ready (batch 1, R001-R020) | [Records](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html) |
| Step 1: screening prompt, criteria already pasted in | [Start, step 1](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/start.html#step-1-screening) |
| Steps 1 and 2: scorer, paste the AI's answer (nothing is uploaded) | [Scorer](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html) |
| Reference answers: **screening answers after step 1, extraction answers after step 3** | [Answers](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/answers.html) |
| Step 3: full text of Phan2020, copy or download | [Papers](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/papers.html#Phan2020) |
| Step 3: extraction prompt, 5 fields and `study_id` already filled in | [Papers, extraction prompt](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/papers.html#extraction-prompt) |
| Extraction form (19 fields, 11 core, 5 for step 3) | [Papers, extraction form](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/papers.html#extraction-form) |
| Step-by-step walkthrough for chat assistants (learning only) | [Beginners](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/beginners.html) |
| One-page card to print | [Quick card](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/quick-card.html) |
| Going further: discrepancy log and AI use record (templates to download) | [Discrepancy log](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/worksheet-discrepancy-log.html) · [AI use record](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/worksheet-ai-use-record.html) |
| Going further: more prompts, agent skills | [Prompts](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/prompts.html) · [Skills](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/skills.html) |

---

## The 60-minute session

The live session: EPH 2026, Bilbao, skills building seminar M.8, Thursday 12 November 2026, 16:45-17:45.

| Min | Clock | Block | Who |
|---:|---|---|---|
| 0-10 | 16:45-16:55 | **Expert discussion.** Limitations of AI in evidence reviews (Patrick Boudreau, about 5 min), then benefits (Francesco Baglivo, about 5 min) | speakers |
| 10-20 | 16:55-17:05 | **Demo video** (about 5 min, commented live) and your task ([watch it](#the-demo)) | Francesco Baglivo and Patrick Boudreau |
| 20-50 | 17:05-17:35 | **Exercise, on your own** (this page): step 1 screening (10 min, 17:05-17:15), step 2 look at the errors (10 min, 17:15-17:25), step 3 short extraction (10 min, 17:25-17:35) | you |
| 50-60 | 17:35-17:45 | **Structured discussion**: each person brings one error they found; performance, transparency, bias, human oversight, reproducibility, and the reference itself | everyone |

### The demo

Before you start, watch the demo video: the three steps of this exercise, done once with an AI chat assistant and
checked by a human, with captions that name every button you will click. In the room, Francesco Baglivo comments it
live and Patrick Boudreau speaks for the verifier, the person who checks every answer against the abstract or the
paper. The AI answers in the video are real: an AI chat assistant was run on 6 November 2026 with the prompts of this
site, web search off, and its answers are shown unedited. The video uses batch 3 (R041-R060) and the paper Mestre2012,
so that nothing you will work on is shown in advance: **you do the same steps on batch 1 and Phan2020.** Watch who
catches the errors: the verifier, not the AI. **Today, on your own, you do both:** you drive the AI, then you verify
it (see [Working on your own](#working-on-your-own)).

<!-- build_pages:demo-video -->

On GitHub: [the video (MP4)](../docs/assets/demo/demo.mp4), its [captions (WebVTT)](../docs/assets/demo/demo.vtt), and
[what it shows, with the raw AI answers](../demo/README.md).

Not at the session? Watch the video above: it shows the three steps without a facilitator. The talks are not needed
to do the exercise: the key message is above, and the [self-paced path](#doing-it-on-your-own-self-paced) below
replaces the facilitators and the slides.

---

## Working on your own

Everyone works individually, on their own laptop: **you drive the AI, then you verify it.** First you paste the
prompt and the records and let the AI answer; then you stop and check what it said against the source, the abstract
or the paper, before you believe it. A laptop is recommended (copying, pasting and reading two windows side by side);
a phone works for reading the pages and the answers. If you like, compare your errors with your neighbour's
after step 2 (optional). In the discussion each person brings one error they found.

---

## Choose your track

| | **Chat track** (most participants) | **Agent track** (going further) |
|---|---|---|
| For | anyone with a chat assistant | people already using Claude Code, Codex CLI, Gemini CLI or similar |
| Step 1 · Screening | **20 records**: R001-R020 (batch 1 of the [records page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html), which fills missing abstracts from PubMed); paste the AI's answer into the [scorer](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html) | all **60 records** in [`data/screening_records.csv`](data/screening_records.csv) |
| Step 2 · Errors | open 2 missed or false includes in the scorer | the same, on all 60 records |
| Step 3 · Extraction | **1 paper**: [`Phan2020`](data/fulltext/Phan2020.txt), **5 fields** (`Mestre2012`, the paper of the demo, is for practice at home) | the **3 papers** in [`data/papers.csv`](data/papers.csv), all fields |
| Help | step-by-step walkthrough and ready prompts: [`../beginners/README.md`](../beginners/README.md), prompt library [`../prompts/README.md`](../prompts/README.md) | skills for screening, extraction, quote checking and discrepancy audit: [`../skills/README.md`](../skills/README.md) |
| Scoring | [browser scorer](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html): paste the answer | `python3 activity/tools/score_screening.py` and `score_extraction.py` |

> ⚠️ **For learning only.** These prompts are teaching material for this workshop. They are not a validated method.
> If you are not confident with how large language models work (context windows, parsing, sampling, retrieval,
> hallucination) and with advanced techniques (structured outputs, verification against the source, reproducibility
> checks, documentation of model and version), **do not use AI to conduct a real evidence review.** You stay
> responsible for every decision: the AI does not.

**Three rules for both tracks.**

1. **Turn off web search / browsing and use a temporary chat (memory off).** In the previous run of this workshop
   (Berlin, September 2026) a chat assistant with internet access recognised the published reference review and
   offered to repeat it. The reference review here (Pruna et al. 2026) is published too: an AI with web access may
   simply look up the answers. Agent track: do not allow web search or web fetch tools.
2. **Screening answers after step 1, extraction answers after step 3**: do not open the
   [reference answers](answers/README.md) earlier.
3. **Upload or paste only texts whose licence allows it** (the `license` column of the records, the `licence` column
   of [`data/papers.csv`](data/papers.csv)), and never personal or confidential data.

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

1. **Copy the records.** Open the [records page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html) and copy **batch 1** (R001-R020)
   with one tap. Some abstracts are empty in the repository because their licence does not allow redistribution: the
   records page fetches them from PubMed in your browser.
2. **Copy the screening prompt** from the [Start page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/start.html#step-1-screening): the criteria
   C1-C6 are already pasted in, with the output format (one row per record, `record_id,decision,reason`, decision
   `include | exclude | unsure`, a reason naming the criterion).
3. **Paste both** into a new temporary chat with your AI assistant, web search off: the prompt first, the records where it says
   `[PASTE THE RECORDS HERE]`.
4. **Paste the AI's answer into the [scorer](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html)**, as it is: no file to save. The scorer
   finds the table even with code fences, a sentence before or after it, or semicolons. Read the coverage line first:
   "Screened 20 of 60 records" is expected; fewer than 20 means the AI dropped or renamed records.

<details>
<summary>Hints</summary>

- A prompt that starts from the criteria gets better results than "is this relevant to hand hygiene?".
- Records without an abstract: the AI should decide on the title and mark `unsure` with reason `no abstract`. Never let it write the abstract.
- If the answer is cut off, type `continue from record [last record_id], same format`.

</details>

## Step 2 · Look at the errors (10 min)

The scorer lists the **missed includes** (records the reference review included and the AI excluded: the costly
error) and the **false includes**. Now you are the verifier.

1. **Open 2 of them**: read the title and the abstract (the scorer links each record to PubMed).
2. **Decide yourself why the AI got them wrong.** Which criterion did it use? Does the abstract say what its reason
   claims? Was the criterion contradicted, or just not mentioned (that is *unsure*, not *exclude*)?
3. **Check the reference too.** The [screening answers](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/answers.html#screening) give the basis of
   every reference decision. A record that the review excluded only after reading the full text is not an error at
   title/abstract stage, and one record is flagged as a possible error in the reference standard.
4. **Keep one error** to bring to the discussion: what the AI said, what the source says, and why.

## Step 3 · Short extraction (10 min)

One paper, **Phan2020**, and **5 fields** of the [extraction form](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/papers.html#extraction-form):
`country`, `study_design`, `intervention_components`, `primary_hai_outcome`, `direction_of_effect`.

1. **Copy the extraction prompt** ([Papers page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/papers.html#extraction-prompt) or Start page):
   the 5 fields, their definitions and `study_id = Phan2020` are already filled in.
2. **Copy the full text** of [`Phan2020.txt`](data/fulltext/Phan2020.txt) (Copy and Download buttons on the
   [Papers page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/papers.html#Phan2020)) and paste it into a **new temporary chat** (web search off) after the prompt.
3. Every value must come with a **verbatim quote** and its location (section or table), or `not reported`.
4. **Verify 2 quotes** yourself: Ctrl+F in the paper. Is the quote there, word for word? Does it support the value?
5. **Compare** with the [reference values](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/answers.html#extraction) (extraction answers, after this
   step), or paste the answer into the scorer (tab "Short extraction"). Read the notes: some papers contradict
   themselves.

<!-- build_pages:extraction-prompt -->

<details>
<summary>Hints</summary>

- Numbers live in tables, and tables are the hardest part to parse: check table values first.
- "Not reported" is a valid answer. A value with no quote is not a value.
- Retrieval tools (project knowledge, notebooks) answer from fragments: if a fragment is not retrieved, the AI says
  "not reported" instead of "I did not see it". For one paper, give the whole text.

</details>

---

## Discussion (last 10 minutes of the session)

In the live session: **each person brings one error they found** (in step 2 or step 3) and how they caught it; the
room collects them. On your own: answer each theme in writing, one or two sentences.

| Theme | Questions |
|---|---|
| **Performance** | How many includes did the AI miss? Would you accept that sensitivity in a real review? Was the time saved worth the time spent checking? |
| **Transparency** | Could you trace every decision and value to a sentence in the source? Which quotes were not in the paper? |
| **Bias** | Which kinds of records or fields did the AI get wrong systematically (single units, bundles, values only in tables or figures, countries it inferred)? |
| **Human oversight** | Where did you catch an error the AI presented with confidence? Would you sign this table? |
| **Reproducibility** | Would the same prompt give the same answer twice? And how reproducible are human reviewers: would two of them, or the same one a month later, agree? What would you report so that someone else can repeat what you did? |
| **The reference** | Is the reference standard always right? What did you find when the AI and the review disagreed? |

---

## Going further

Not needed for the 30 minutes. Do these at home, or if you finish early.

- **A second run.** Paste the same prompt and the same batch in a **new** chat and paste both answers into the scorer
  (Going further box): it reports how many decisions changed and Cohen's kappa. A result you cannot reproduce is not
  a method.
- **Research idea from Berlin:** compare the reproducibility of human reviewers and AI on the same extraction task.
- **The 11 core fields.** The longer extraction, with the 11 core fields of the form: the prompt is on the
  [Papers page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/papers.html#going-further). Try the second paper, `Mestre2012` (the paper of the
  demo), with the same prompt.
- **Log the discrepancies** in the [discrepancy log](worksheets/discrepancy_log.md) (what the AI said, what the
  reference says, who is right after checking the source, the error type) and fill the
  [AI use record](worksheets/ai_use_record.md) (tool, model, version, date, prompts): both have templates to copy or
  download.
- **The agent track with skills.** With Claude Code or another coding agent: screen all 60 records and extract the 3
  papers, with the skills of [`../skills/README.md`](../skills/README.md) (`title-abstract-screening` runs two
  independent passes and lists the disagreements). The third paper, Al Kuwaiti 2017, is CC BY-NC: download it to
  your computer with `python3 activity/tools/fetch_fulltext.py`. Score with Python (standard library only):
  ```bash
  python3 activity/tools/score_screening.py screening_run1.csv --compare screening_run2.csv --expect-all
  python3 activity/tools/score_extraction.py extraction.csv
  ```
  Chat track with Python: the same commands without `--expect-all`, and
  `--fields country,study_design,intervention_components,primary_hai_outcome,direction_of_effect` for the short
  extraction.
- **The title/abstract-stage view** and the other indicators of the scorer (specificity, precision, WSS): see below.

<details>
<summary>How to read the screening score</summary>

**Coverage rule** (the same in the Python and the browser scorer): the metrics are computed on the records present
in your answer, and the report always says how many were screened ("Screened N of 60 records"), lists the records
not screened, highlights any reference include among them, and gives the sensitivity *counting not-screened
includes as missed*. In the chat track you screen 20 records, so 40 "not screened" is expected. With `--expect-all`
(agent track) records not screened count as exclude in every metric. `unsure` counts as include.

The reference is the review's **final** decision. Some records were excluded by the review only after reading the
full text: including them at title/abstract stage is not an error. The scorer shows a "title/abstract-stage view"
for this, and the `gold_basis` column explains each reference decision. Sensitivity (missed includes) matters most.
One record is marked as a **possible error in the reference standard**: discuss it.

</details>

---

## Doing it on your own (self-paced)

Everything you need is on the website and in this repository; no facilitator, slides or group are required. Allow
**60 to 90 minutes**: the same three steps as the live session, with more time to verify before you look at the
answers.

| Block | Live session | On your own | What to do |
|---|---:|---:|---|
| Get ready | demo video | 10 min | Watch the [demo video](#the-demo) (5 min); read the key message and the criteria on this page; pick a track; turn off web search and use a temporary chat ([three rules](#choose-your-track)). New to AI? Follow the [beginners walkthrough](../beginners/README.md) (chat track, for learning only) |
| [Step 1 · Screening](#step-1--screening-10-min) | 10 min | 15-20 min | Batch 1 (R001-R020); paste the AI's answer into the scorer |
| [Step 2 · Look at the errors](#step-2--look-at-the-errors-10-min) | 10 min | 15-20 min | Open the missed and false includes; decide why the AI got them wrong |
| [Step 3 · Short extraction](#step-3--short-extraction-10-min) | 10 min | 15-20 min | Phan2020, 5 fields, a quote for every value; verify the quotes before opening the extraction answers |
| [Discussion](#discussion-last-10-minutes-of-the-session) | 10 min | 10 min | Write one or two sentences per theme |
| [Going further](#going-further) | | as you like | Second run, 11 fields, discrepancy log, AI use record, agent track |

**You drive, then you verify.** Do not let the two jobs blur: first run the AI and keep its answer as it is; then
stop and become the verifier, which is the part this exercise is about. The verifier checklist:

- [ ] **Screening.** As many rows came back as you sent (the scorer's coverage line); no `record_id` missing, repeated or renamed.
- [ ] At least 2 decisions (one of them an *exclude*) checked against the abstract: does the abstract say what the reason claims?
- [ ] Every *exclude* names a criterion that the abstract clearly contradicts, not one it merely does not mention (that is *unsure*).
- [ ] No reason uses a rule that is not in C1-C6 (country, "low quality", date...).
- [ ] **Extraction.** At least 2 quotes found with Ctrl+F in the paper, character for character; every number in a value appears in its quote.
- [ ] Every `not reported` searched in the paper with synonyms (infection rate, nosocomial, hospital-acquired, per 1000 patient-days).

**When to open the answers.** Screening answers after step 1, extraction answers after step 3. The scorer shows the
screening reference as soon as you score, so screen first. The reference review itself and the
[facilitator guide](facilitator_guide.md) name the included studies: open them only after the exercise. If you use an
agent, do not let it read `answers/` before then either.

**Reading the score without a facilitator.**

1. **Coverage line first.** "Screened 20 of 60 records (40 not screened)" is expected for batch 1. Fewer than 20
   screened means the AI dropped or renamed records: that is already a finding.
2. **Missed includes.** The costly error at this stage. For each one, open the abstract: which criterion did the AI
   use, and was it right to?
3. **False includes.** Look at the `gold_basis`: a record excluded by the review only after reading the full text is
   not an error at title/abstract stage.
4. **Extraction.** A quote that is not in the paper, a value where the paper reports nothing (`unsupported`) and a
   `not reported` for something the paper does report (`false absent`) matter more than small wording differences;
   read the `notes` of the reference values, because some papers contradict themselves.
5. **The reference can be wrong.** One record is flagged as a possible error in the reference standard. Check the
   source before deciding who is right.

After scoring, the sections "What to expect in screening", "What to expect in extraction" and "Interpreting the
scores" of the [facilitator guide](facilitator_guide.md) are your debrief.

**Discuss with yourself.** Answer the questions of the [discussion](#discussion-last-10-minutes-of-the-session) in
writing. Then the one that matters most: *would you sign this screening and this table as they came out of the AI,
and what would you need to check first?*

**What next.**

- Do more: everything under [Going further](#going-further).
- Read the [five starting references](../README.md#useful-references), especially the position statement of
  Cochrane, the Campbell Collaboration, JBI and CEE and the RAISE recommendations, which say how AI use should be
  overseen and reported.
- Use the [prompt library](../prompts/README.md) for the other review stages, or the [agent skills](../skills/README.md)
  if you already work with coding agents.
- Before using AI in a real review, be honest about your AI literacy and skills (see the warning above), and pilot any
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
- **Score** with the Python scorers (standard library only): save the AI's answer as a text file and run the commands
  under [Going further](#going-further); without Python, after step 1 compare your 20 rows by hand with
  [`answers/screening_gold.csv`](answers/screening_gold.csv).

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
| [`answers/`](answers/README.md) | Reference answers: **screening answers after step 1, extraction answers after step 3** |
| [`tools/`](tools/) | Scorers and builders (Python 3, standard library only); every script has `--help` |
| [`examples/`](examples/README.md) | Fake decisions and extraction files to try the scorers |
| [`worksheets/`](worksheets/) | Optional (going further): [discrepancy log](worksheets/discrepancy_log.md) ([CSV](worksheets/discrepancy_log.csv)), [AI use record](worksheets/ai_use_record.md) |
| [`quick_card.md`](quick_card.md) | One-page printable card |
| [`facilitator_guide.md`](facilitator_guide.md) | For facilitators (timing, pitfalls, debrief). **Contains answers: participants read it only after the exercise** |
