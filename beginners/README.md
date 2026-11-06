# AI beginners track

A step-by-step, copy-paste walkthrough of the workshop exercise for people who only have a chat assistant (ChatGPT, Claude, Gemini, Copilot, Mistral Le Chat, ...). No installation, no code.

> ⚠️ **For learning only.** These prompts are teaching material for this workshop. They are not a validated method.
> If you are not confident with how large language models work (context windows, parsing, sampling, retrieval,
> hallucination) and with advanced techniques (structured outputs, verification against the source, reproducibility
> checks, documentation of model and version), **do not use AI to conduct a real evidence review.** You stay
> responsible for every decision: the AI does not.

> [!WARNING]
> This track exists so you can **see** how AI behaves on a review task, safely, on data where the right answers are known. It is not a shortcut to doing reviews with AI. AI can bring real advantages to evidence synthesis, but only for people with AI literacy and advanced skills; without them you risk serious errors and losing control of the process. **If you lack these skills, do not use AI to run real reviews.**

## What you will do (about 30 minutes live, 60 to 90 minutes on your own)

The steps are those of the live session at EPH 2026 in Bilbao: **screening (10 min) → extraction (12 min) → score and compare (8 min) → discussion (10 min)**. On your own, without a facilitator or the slides, take more time and follow [Doing it on your own (self-paced)](../activity/README.md#doing-it-on-your-own-self-paced): it says how to be your own verifier, when to open the answers and how to read the score.

| Step | What | Live session | On your own |
|:-:|---|:-:|:-:|
| 0–4 | Get ready, read the criteria, screen 20 abstracts, check what came back (and, with a spare minute, run it again in a new chat) | 10 min | 25–30 min |
| 5 | Extract data from one paper, with quotes (optional if screening ran late) | 12 min | 15–20 min |
| 6 | Score and compare with the reference review | 8 min | 10–15 min |
| 7 | Talk about it | 10 min, all together | 10 min, in writing |

**The question** is deliberately simple, so you can focus on the AI and not on the topic: *are hand hygiene interventions effective in preventing healthcare-associated infections (HAI)?*

| P | I | C | O |
|---|---|---|---|
| Patients and healthcare workers in acute care hospitals | Multimodal hand hygiene intervention, hospital-wide or across more than one ward | Pre-intervention period, standard practice, or a contemporaneous comparator group | Clinical healthcare-associated infection outcomes |

Study design: quasi-experimental (interrupted time series, controlled or uncontrolled before-after). The full criteria C1–C6 are in [`activity/README.md`](../activity/README.md).

The **reference review** is Pruna et al., *J Clin Med* 2026: a systematic review of quasi-experimental studies in acute care hospitals, with 12 included studies, in which two independent human reviewers did the screening and extraction **without AI**. Its decisions are the answers you compare with. The choice is provisional; the full reference, and why it was chosen, are in [`activity/data/README.md`](../activity/data/README.md). **Open it after the exercise, not before**: it names the included studies.

---

## Step 0. Get ready

- [ ] A laptop with a chat assistant open in the browser. Any one works; if your tool has a "temporary chat" or lets you switch memory off, use that.
- [ ] A text editor or spreadsheet (Notepad, TextEdit, Excel, Google Sheets, LibreOffice) to save the answers.
- [ ] A note with: **tool name, model name as displayed, date and time**. You will need it at the end.

> [!CAUTION]
> Never paste personal, patient or confidential data into a chat assistant. The workshop records are published abstracts, so they are fine for this exercise.

## Step 1. Read the question and the criteria

Open the hands-on guide: **[`activity/README.md`](../activity/README.md)**. It contains the review question and the **eligibility criteria** (labelled C1, C2, ...). Keep that page open: you will paste the criteria into the prompt. (The same criteria are stored in [`activity/review_config.yaml`](../activity/review_config.yaml).)

Why this matters: if you do not give the AI explicit criteria, it uses its own, and they change every time you ask.

## Step 2. Screen 20 abstracts

**Get the records.** Choose one of the two options.

<details open>
<summary><b>Option A (easiest): the records page</b></summary>

1. Open the **[records page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html)**.
2. Choose **batch 1 (R001-R020)**. The page downloads the abstracts that the repository cannot ship (licence) directly from PubMed, in your browser.
3. Click **Copy batch** and paste it after the prompt below.

If the records page does not open (the website is not available), use Option B or Option C.
</details>

<details>
<summary><b>Option B: build the batch on your computer</b> (needs Python)</summary>

```bash
python3 activity/tools/fetch_abstracts.py
python3 beginners/make_batches.py activity/data/local/screening_records_full.csv --size 20
```

Run them from the repository folder (download it with **Code → Download ZIP** on GitHub, or `git clone`). The first command fills the missing abstracts from PubMed into a local, git-ignored file (do not publish it: many abstracts are copyrighted). The second writes paste-ready batches in `beginners/batches/`; use `screening_batch_01.md` (R001-R020): open it, copy everything inside the box and paste it after the prompt below.
</details>

<details>
<summary><b>Option C: by hand</b> (no website, no Python)</summary>

1. Open [`activity/data/screening_records.csv`](../activity/data/screening_records.csv) on GitHub and take records R001 to R020.
2. For each record with an empty abstract, open `https://pubmed.ncbi.nlm.nih.gov/<pmid>/` (the `pmid` column) and copy the abstract **word for word**.
3. Paste the records after the prompt below, one per block: `record_id`, `title`, `abstract`.

Slower, but it works anywhere. Never ask the assistant to find or write a missing abstract.
</details>

> [!NOTE]
> **Why some abstracts are missing from the repository.** The repository ships an abstract only when its licence allows redistribution; the others are fetched from PubMed by the records page (Option A) or by `fetch_abstracts.py` (Option B). If you still see an empty abstract, leave it: the prompt tells the assistant to mark it *unsure*. **Do not** ask the assistant to "find" or write the abstract: it may invent one.

**Open a new chat**, paste this prompt, replace the two parts in `[BRACKETS]`, and send.

```text
You are a second reviewer screening titles and abstracts for a systematic review.

ELIGIBILITY CRITERIA (apply exactly these, nothing else):
[PASTE THE CRITERIA C1, C2, ... FROM activity/README.md]

RULES
- Decide for each record: include, exclude, or unsure.
- exclude ONLY if the title/abstract clearly shows that at least one criterion is NOT met. Name the criterion.
- include if all criteria are met or not contradicted by the abstract.
- unsure if information is missing or ambiguous. When in doubt, do not exclude.
- Use only the text given. Do not use anything you may know about these studies.
- Return one row for EVERY record, in the same order. If the abstract is empty, decide on the title only and use unsure with reason "no abstract".

OUTPUT: only a CSV block with the header
record_id,decision,reason
where reason is max 25 words and starts with the criterion code (e.g. "C2 not met: ...").
After the CSV, write: "Records received: N. Rows returned: N."

RECORDS
[PASTE THE RECORDS HERE]

Reminder: apply only the criteria above; one row per record; when in doubt, unsure.
```

**Save the answer.** Copy the CSV block into your text editor and save it as `screening_run1.csv` (plain text, not .docx). In a spreadsheet: paste, then *File → Download / Save as → CSV*.

> [!TIP]
> If the reply is cut off, type `continue from record [last record_id], same format`. If it gives you a table instead of CSV, ask: `Give me the same as a CSV code block, nothing else.`

## Step 3. Check what came back

Before trusting anything, check it. This is the most important step.

| Check | How | Why |
|---|---|---|
| **Every record is there** | Count the rows. Same number as the records you pasted? Any `record_id` missing or repeated? | Models silently drop rows in long lists |
| **Reasons are real** | Pick 3 records. Does the abstract really say what the reason claims? | The reason can be invented even when the decision is right |
| **Excludes are justified** | Read every *exclude*. Is the criterion clearly contradicted, or just not mentioned? | "Not mentioned" should be *unsure*, not *exclude* |
| **Only your criteria were used** | Any reason citing something not in the criteria (language, country, "low quality")? | The model may add its own rules |

## Step 4. Run it again, in a new chat

1. Open a **new** chat (not the same one: it would just repeat itself).
2. Paste the same prompt and the same batch again. A fresh chat does not remember the first run, so this is an independent second run.
3. Save the answer as `screening_run2.csv`.
4. Compare `screening_run1.csv` and `screening_run2.csv` side by side in a spreadsheet. Mark every record where the decision changed.

> [!NOTE]
> The answer is **sampled**: the model picks each word with some randomness. The same prompt on the same text can give a different decision. A result you cannot reproduce is not a method.

For records where the two runs disagree, **you** decide: write your own decision in a third file, `my_decisions.csv` (same columns). Keep the AI files as they are.

## Step 5. Extract data from one paper, with quotes (12 min; optional if screening ran late)

This is the 12-minute extraction step of [`activity/README.md`](../activity/README.md). If you are short of time, skip it; if you can, do it: extraction is where AI errors are hardest to see.

1. **Look at the form first**, before giving the paper to the assistant: [`activity/data/extraction_form.csv`](../activity/data/extraction_form.csv). For this track use only the **11 core fields** (column `core = yes`): `country`, `intervention_scope`, `study_design`, `intervention_components`, `comparator`, `primary_hai_outcome`, `hh_compliance_baseline`, `hh_compliance_post`, `hai_rate_baseline`, `hai_rate_post`, `direction_of_effect`.
2. Open a **new chat** and paste (or upload) the plain text of the paper: [`activity/data/fulltext/Phan2020.txt`](../activity/data/fulltext/Phan2020.txt) (the [Papers page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/papers.html) has **Copy full text** and **Download .txt** buttons). Use `study_id = Phan2020`. At home, for more practice: [`Mestre2012.txt`](../activity/data/fulltext/Mestre2012.txt), the paper of the live demo (`study_id = Mestre2012`).
3. Paste the prompt below, then save the CSV block as **`extraction.csv`**. Ready to paste: the [Papers page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/papers.html#extraction-prompt) has this prompt with the 11 core fields and `study_id = Phan2020` already filled in, with a Copy button. Otherwise fill the parts in `[BRACKETS]` yourself.

<!-- build_pages:extraction-prompt -->

```text
You are extracting data for a systematic review. Use ONLY the paper I give you. Do not use outside knowledge.

EXTRACTION FORM (fill every field, do not add or change fields):
[PASTE THE 11 CORE FIELDS: field, definition, allowed values]

RULES
- For every field give: value, a verbatim quote copied exactly from the paper, and the location (section, table, page).
- If the paper does not report the field, write: not reported. Do not guess.
- Do not round or convert. If there are several values (several wards, arms or time periods), list each on its own row and say which is which.

OUTPUT: only a CSV block with the header
study_id,field,value,source_quote,location
Use study_id = [Phan2020 or Mestre2012].

PAPER:
[PASTE THE TEXT OF THE PAPER, OR SAY "attached"]
```

Then verify, in **another new chat** with the same paper pasted or attached:

```text
For each row below, find the quote in the paper I give you. Answer FOUND (verbatim), NEAR (similar wording: give the real text) or NOT FOUND, and say whether the passage supports the value (yes / partly / no). Do not correct anything.

[PASTE THE CSV ROWS]
```

**What to look for**

- [ ] Open the paper at every location given (Ctrl+F on the quote). Is the number really there, in the right row and column of the table?
- [ ] Every *not reported*: search the paper yourself (Ctrl+F) with synonyms (infection rate, nosocomial, hospital-acquired, per 1000 patient-days). Is it really absent?
- [ ] Quotes that are "almost" the same as the paper: the model rewrote them. Treat the value as unverified.
- [ ] If you ran it twice: which fields changed? Numbers usually change more than descriptions.
- [ ] Score it (scorer page or `python3 activity/tools/score_extraction.py extraction.csv`): read `QUOTE NOT FOUND`, `unsupported` and `false absent` first.

## Step 6. Score and compare with the reference review (8 min)

Only now look at the answers.

- **Online scorer** (nothing leaves your browser): open the workshop website's scorer, <https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html>, and load `screening_run1.csv`, `screening_run2.csv` or `my_decisions.csv`.
- **With Python** (if you have it, or if the website is not available): `python3 activity/tools/score_screening.py screening_run1.csv --compare screening_run2.csv` and `python3 activity/tools/score_extraction.py extraction.csv` (use `--help` to see the options).
- **Reference answers** (decisions with their basis, extraction values with quotes and notes), behind a button: <https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/answers.html>. The **discrepancy log** to fill: <https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/worksheet-discrepancy-log.html>.
- **Without website and without Python:** compare your 20 rows by hand with [`activity/answers/screening_gold.csv`](../activity/answers/screening_gold.csv) (open it only now).

**Read the coverage line first**: "Screened 20 of 60 records" is expected, because you screened batch 1 only (the 40 others count as *not screened*, not as errors). Fewer than 20 means the assistant dropped or renamed records.

Then look at each disagreement with the reference and ask: was it a **missed include** (the most serious error), a **false include**, an *unsure* that was reasonable, or a criterion that two humans could also read differently? The prompt to help you classify them is [6.2 in the prompt library](../prompts/06_synthesis_and_reporting.md#62-discrepancy-summary-after-the-workshop-exercise).

## Step 7. Talk about it (10 min, all together)

In the live session, bring your answers to the group discussion. On your own, answer each question in writing, in one or two sentences:

1. How many records did the AI get wrong, and of which kind? Would any error have changed the review's conclusions?
2. What changed between run 1 and run 2?
3. Which check caught the most problems?
4. What would you need to write in a paper to report what you did? (Tool, model and version, date, prompt, what you checked: see [prompt 6.3](../prompts/06_synthesis_and_reporting.md#63-ai-use-statement).)
5. Would you trust this for a real review? What would you need to learn first?

These questions cover the five themes of the session's discussion (performance, transparency, bias, human oversight, reproducibility) and the reference itself: is the human review always right? The full list is in the [activity guide](../activity/README.md#discussion-last-10-minutes-of-the-session).

---

## Glossary

| Term | Plain meaning | Why it matters here |
|---|---|---|
| **Large language model (LLM)** | Software trained on huge amounts of text to continue text plausibly | It produces fluent answers whether or not they are correct |
| **Token** | A small piece of text (part of a word) that the model reads and writes | Limits on length and cost are counted in tokens |
| **Context window** | Everything the model can "see" at once: your instructions, the documents, the whole conversation so far | It is finite, and information in the middle of a long input is used less reliably than at the start or end. One task per chat |
| **Parsing** | Turning a PDF into plain text before the model reads it | The model never sees your PDF. Tables often come out scrambled, and numbers end up in the wrong place |
| **Sampling** | The model chooses each next word with some randomness | The same prompt can give different answers: run twice and compare |
| **Hallucination** | A confident statement, quote, number or reference that is not supported by the source or does not exist | Always ask for quotes and check them in the source |
| **RAG (retrieval-augmented generation)** | The tool splits your documents into chunks, finds a few that look relevant to your question, and answers only from those | If the right chunk is not found, it says the information is "not reported" instead of saying it failed to find it |
| **Agent** | A model wrapped in software that can take actions for you (open and save files, run programs) step by step | Powerful, and it acts with whatever access you give it. Give it one project folder, never your whole disk |
| **Prompt** | The instructions you give the model | Explicit criteria and a fixed output format make answers checkable |
| **Reference standard / gold standard** | The decisions of the original review done by humans without AI | What you compare the AI against |

## Where next

- [Prompt library](../prompts/README.md): more prompts for every stage of a review, with the checks to do afterwards.
- [Skills library](../skills/README.md): the same method for agent tools like Claude Code, for advanced users.
- Guidance: the 2025 position statement of Cochrane, the Campbell Collaboration, JBI and CEE says that evidence synthesists remain responsible for their synthesis, that AI should be used with human oversight, and that AI use that makes or suggests judgements must be fully reported (doi:[10.1186/s13750-025-00374-5](https://doi.org/10.1186/s13750-025-00374-5)). It supports the RAISE recommendations: <https://osf.io/fwaud/>.

---

> ⚠️ **For learning only.** These prompts are teaching material for this workshop. They are not a validated method.
> If you are not confident with how large language models work (context windows, parsing, sampling, retrieval,
> hallucination) and with advanced techniques (structured outputs, verification against the source, reproducibility
> checks, documentation of model and version), **do not use AI to conduct a real evidence review.** You stay
> responsible for every decision: the AI does not.

> [!WARNING]
> **If you lack AI literacy and advanced skills, do not use AI to run real reviews.** Learn first; practise on data where the answers are known, like the data of this exercise.
