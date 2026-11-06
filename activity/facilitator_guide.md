# Facilitator guide (for facilitators: contains answers)

> [!CAUTION]
> **Spoiler warning. Participants: stop here.** This page names the records the reference review included, the traps
> in each extraction paper and the expected AI errors. Reading it before you have saved your own screening and
> extraction makes the exercise meaningless. Go back to the [activity guide](README.md). If you are doing the exercise
> on your own, come back **after step 3**: the sections "What to expect in screening", "What to expect in
> extraction" and "Interpreting the scores" are then your debrief.

For the people running the hands-on part of the seminar, at EPH 2026 in Bilbao (Thursday 12 November 2026,
16:45-17:45) or in a later run of the same workshop. Participants use [`README.md`](README.md); this page adds timing,
preparation, the pitfalls you should expect, and how to run the debrief. Do not project it.

> **Status of the answers.** The reference review is **provisional** (see [`data/README.md`](data/README.md)) and may be
> replaced before the session. The extraction reference values were **prepared by the workshop team from the full
> texts**, each with a verbatim quote and, where available, the reference review's own table entry
> (`review_table_value`); they have not yet been validated against the review team's extraction sheet. Say so when
> groups compare with them.

## Before the session

| When | Check |
|---|---|
| The day before | Open the [records page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html) and the [scorer](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html) on the published site; copy batch 1 and confirm that the empty abstracts are filled from PubMed |
| The day before | On each facilitator laptop: `python3 activity/tools/fetch_abstracts.py` and `python3 activity/tools/fetch_fulltext.py` (local copies in `activity/data/local/`, git-ignored: do not publish them). This is the fallback if the venue network blocks NCBI |
| The day before | Run the scorers on the examples: `python3 activity/tools/score_screening.py activity/examples/decisions_example.csv` and `python3 activity/tools/score_extraction.py activity/examples/extraction_example.csv` |
| The day before | Print the [quick card](quick_card.md) (one per group) and a few copies of the [discrepancy log](worksheets/discrepancy_log.md) |
| Before the session | **Pre-assign groups, tracks and roles** (e.g. by table: tables marked "chat" and "agent", role cards on each table). Forming groups from scratch takes far more than one minute |
| On arrival | Write on a slide or board: the repository short link, "Chat track: batch 1 = R001-R020, paper Phan2020", "Do not open `answers/` before step 3" |

If the reference review has been replaced, rebuild first (see [`data/README.md`](data/README.md#how-to-replace-the-reference-review)) and re-read the record IDs below.

## Timing (60 minutes)

Clock times are those of the Bilbao session (start 16:45); for another run, add the minutes to your start time.

| Min | Clock | Block | Facilitator cue |
|---:|---|---|---|
| 0-10 | 16:45-16:55 | Expert discussion: **Patrick Boudreau** on limitations (about 5 min), then **Francesco Baglivo** on benefits (about 5 min) | End on the key message: advantages only with AI literacy; humans stay responsible |
| 10-20 | 16:55-17:05 | Demo in four hands: **Francesco Baglivo** drives the AI, **Patrick Boudreau** checks the source | Follow the [demo script](#demo-script-four-hands): one screening batch, one extraction, then the errors the verifier caught |
| 18-20 | 17:03-17:05 | (end of demo) Groups and tracks already assigned by table; roles confirmed; the repository and records page open | "Driver, prompter, verifier, recorder: check your role card" |
| 20-30 | 17:05-17:15 | **Step 1 screening** | At minute 25: "Did you count the rows that came back?" At 29: "Save the file, even if incomplete" |
| 30-42 | 17:15-17:27 | **Step 2 extraction** (chat track: optional if screening ran late; then compare screening only) | At 30: "Read the form for one minute before uploading." At 37: "Verifier: search three quotes now" |
| 42-50 | 17:27-17:35 | **Step 3 compare** | "Open the scorer. Read the coverage line, missed includes and QUOTE NOT FOUND first. Log three discrepancies" |
| 50-60 | 17:35-17:45 | Structured discussion | Use the prompts below; collect one sentence per group |

## Demo script (four hands)

Ten minutes, 16:55-17:05, **Francesco Baglivo** and **Patrick Boudreau** together. The demo stages the message of the
workshop: **one drives the AI, one checks the source.**

- **Francesco = driver.** At the keyboard. Runs the AI with exactly the pages and prompts the participants will use,
  and says aloud what he clicks.
- **Patrick = verifier.** Never touches the AI. Asks "show me where it says that" and checks the answers against the
  abstract or the paper. He decides what is accepted.

Participants then do the same steps in the same roles (driver and verifier of the [group roles](README.md#group-roles)).
The point to land at the end: **the errors were caught by the verifier, not by the AI.**

**Pages used.** All on the published site, <https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/> (or on `http://localhost:8000/` if you serve `docs/` from a
laptop):

- [Start page, `start.html`](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/start.html): the screening prompt with C1-C6 already pasted in, with a Copy button.
- [Records page, `batch.html`](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html): the batches; missing abstracts are filled from PubMed in the browser.
- [Beginners walkthrough, step 5](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/beginners.html#step-5-extract-data-from-one-paper-with-quotes-12-min-optional-if-screening-ran-late):
  the extraction prompt and the verification prompt; the 11 core fields are the rows with `core = yes` of the
  [extraction form](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/data/extraction_form.csv). Same prompts in the [prompt library](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/prompts.html) (3.1, 4.2).
- [Scorer, `scorer.html`](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html): paste the CSV; nothing is uploaded.
- Mestre2012 full text (CC BY 4.0), the demo paper: [`data/fulltext/Mestre2012.txt`](data/fulltext/Mestre2012.txt), or
  [as plain text](https://raw.githubusercontent.com/fraba94/eph2026-ai-for-evidence-synthesis/main/activity/data/fulltext/Mestre2012.txt)
  to select all and copy.

> [!IMPORTANT]
> **Demo on batch 3 (R041-R060), not batch 1.** The chat-track groups screen batch 1 (R001-R020) right after the
> demo: projecting the scorer on batch 1 would show them its missed includes. Batch 3 keeps the same steps without
> the spoiler (agent-track groups, who screen all 60, see 20 of their answers: tell them so). Likewise, the demo
> extracts **Mestre2012**, not Phan2020: the chat-track groups extract Phan2020 right after.

### Minute by minute

| Time | Francesco (driver) | Patrick (verifier) | On screen |
|---|---|---|---|
| **A. Screening** | | | |
| 0:00-0:30 (16:55) | Opens the Start page: "This is the page you will use in five minutes." | Announces the roles: "Francesco drives the AI, I check the source. Nothing goes into our table until I have seen it in the abstract." | `start.html`, sections 1 and 3 |
| 0:30-1:15 | Records page: batch size **20**, **batch 3 (R041-R060)**; waits until the status says the abstracts are filled; **Copy batch** | "Why batch 3? You will screen batch 1, and we do not want to spoil it." | `batch.html` |
| 1:15-1:45 | Back on the Start page: **Copy the screening prompt** (C1-C6 already in it); new temporary chat; pastes the prompt, replaces `[PASTE THE RECORDS HERE]` with the batch; sends | Reads one rule aloud: "Exclude only if the abstract clearly shows that a criterion is not met. When in doubt, unsure." | Chat assistant |
| 1:45-2:30 | Scrolls the answer to the last line, "Records received: N. Rows returned: N." | "That line is the AI talking about itself. We count." Counts the IDs R041 to R060: any missing, repeated or renamed? | The CSV block in the chat |
| 2:30-3:45 | Switches to the records tab, Ctrl+F on the record Patrick names | Picks **two decisions**, preferably one exclude and one include or unsure: "Show me where it says that." Reads the sentence of the abstract and says aloud: supported, or not | `batch.html` (the abstract) next to the chat |
| 3:45-5:00 | Copies the CSV block; Scorer, screening tab; pastes it; leaves "I was meant to screen all records" **unticked**; compares | "Coverage line first: Screened 20 of 60 is expected, fewer means rows were dropped." Then: "Missed includes: the costly error at this stage." | `scorer.html` |
| **B. Extraction** | | | |
| 5:00-5:45 (17:00) | New chat; pastes the extraction prompt with the 11 core fields (prepared the day before), `study_id = Mestre2012`, then the full text of Mestre2012 (or attaches the file); sends | States the rule: "Every value has a verbatim quote and a location, or says not reported. A value without a quote is not a value." | Chat assistant |
| 5:45-6:30 | Opens `Mestre2012.txt` in the second tab while the answer arrives | Chooses **two quotes** from the answer: one with a number, and a `not reported` if there is one | Chat, then `Mestre2012.txt` |
| 6:30-7:30 | Ctrl+F on six to eight words of each quote, then on a synonym for the `not reported` field | "Is it there word for word, in the section it says?" Then **one number**: "Is the number in the value also in the quote?" | `Mestre2012.txt` with the match highlighted |
| 7:30-8:00 | "We do not score the extraction now: that is your job in step 2." | Sums up aloud what passed and what did not | Chat |
| **C. What we just saw** | | | |
| 8:00-9:15 (17:03) | Switches to the whiteboard slide and writes each error found: record ID or field, what was wrong | For each error: "Who caught it? Not the AI. The verifier, with the source open." If none: "No visible error today. That is also a result: here is what our rehearsal produced." | Whiteboard slide |
| 9:15-10:00 | Back to the Start page, section 2 (tracks) | Hands over: "Your turn. Same steps, same roles: driver at the keyboard, verifier with the source open. Chat track: batch 1 and Phan2020. Check your role card." | `start.html#choose-your-track` |

### What to watch for

| Part | Patrick looks for | What it shows |
|---|---|---|
| A. Screening | **Missing or renamed rows**: fewer than 20 rows, an ID skipped or repeated, `R41` instead of `R041`, rows out of order | Chat assistants drop rows silently; the self-reported count can be wrong |
| A. Screening | **A reason that cites no criterion** (no C1-C6 code), or a rule that is not in the criteria ("small sample", "low quality", "not in Europe") | The model adds its own criteria |
| A. Screening | **Exclude when the abstract is silent** (the reason says "not mentioned", "unclear", "no information") | At this stage that is `unsure`, not `exclude`: a possible missed include |
| B. Extraction | **A quote that is not in the paper** (Ctrl+F finds nothing, or finds a near-identical sentence) | Invented or paraphrased quote: the value is unverified |
| B. Extraction | **A number that is not in its quote** (the value says one figure, the quote another or none) | The value came from somewhere else, or was computed or rounded |
| B. Extraction | **A false "not reported"** (Ctrl+F on a synonym finds it, often in a table) | Missed information: "not reported" must be checked like any other value |

### The day before

- [ ] **Network.** Open `start.html`, `batch.html` (batch 3 fills its abstracts) and `scorer.html` on the venue Wi-Fi,
      or on the phone hotspot you will use as a fallback.
- [ ] **Chat assistant.** Logged in on the demo laptop; **memory off or a temporary chat**; no project knowledge or
      custom instructions that could leak earlier runs.
- [ ] **Readable from the back of the room.** Browser zoom 150%, large font in the chat; dark mode off if the
      projector washes it out.
- [ ] **Two tabs open:** `start.html` and the chat. Keep `batch.html`, `scorer.html` and `Mestre2012.txt` one click
      away (a local copy of `Mestre2012.txt` works without network).
- [ ] **Extraction prompt ready:** the prompt of the beginners walkthrough, step 5, with the 11 core fields of the
      extraction form pasted in and `study_id = Mestre2012`, saved in a text file on the laptop.
- [ ] **Rehearsal run saved locally as backup**, in case the live run shows no error or the network fails: the
      screening CSV, the extraction CSV and screenshots of the chat and of the scorer, with one error marked.
      Keep it on the laptop only (outside the repository or in the git-ignored `activity/data/local/`): **do not
      commit or post outputs that contain copyrighted abstracts**.
- [ ] **AI use record.** Note the model name, version and date of the rehearsal, and again on the day, in the
      [AI use record](worksheets/ai_use_record.md): the demo models what the recorder does.
- [ ] **Rehearse once in four hands** with a timer: who speaks when, and where the hand-over at 9:15 happens.

### If something fails

| Problem | What to do |
|---|---|
| No network (records page, chat or scorer do not load) | Show the saved rehearsal run: screenshots of the chat, the CSV and the scorer. Say it is a rehearsal and when it was run. Then point to the [fallbacks](#if-things-go-wrong) for the groups |
| The AI makes no visible error | Say so: it is also a result, and it does not prove the next run will be clean. Show the rehearsal's error and who caught it |
| Records page does not fill the abstracts | Use the records shipped with abstracts (see [If things go wrong](#if-things-go-wrong)) or the rehearsal run |
| Time overrun | Skip part B (extraction). **Always keep part C**: the errors on the whiteboard and the hand-over |

## What to expect in screening

Record IDs refer to the current build (seed 2026). Chat track groups see R001-R020 (4 includes).

| Record(s) | Reference | Typical AI behaviour and why it is instructive |
|---|---|---|
| R003 (multicentre programme, Chicago), R022 (national Cleanyourhands campaign), R017 (automated monitoring plus promotion), R040 (7-hospital system, CLABSI), R060 (Targeted Solutions Tool) | include | Often missed: the outcome is antimicrobial resistance or an association with HAI (C5 looks weak), the setting is national or a health system (C1/C2 look odd), or electronic monitoring triggers the "single measure" exclusion in C3 although it is embedded in a wider strategy |
| R039 (hospital-wide programme, Geneva) | exclude, flagged | Appears to meet all criteria but is not among the review's included or full-text-excluded studies: **possible gold-standard error**. Use it to ask "who checks the reference?" |
| R007, R009, R051 (single neonatal ICU), R045 (single urology ward) | exclude | Include-looking abstracts with HAI outcomes: the AI must apply C2 (single unit). Good test of whether the criteria were pasted verbatim |
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
| Mestre2012 | The country appears only in the author affiliations ("Delfos Medical Center, Barcelona, Catalonia, Spain"); Methods mention only a "Catalonian Regional Campaign" | `Spain` with the affiliation quote and "author affiliations" as location is correct. `Spain` with no quote, or with a quote that is not in the paper, is an inference to verify. The PDF and the text file both contain the affiliations |
| Mestre2012 | The HAI outcome (MRSA) is secondary; the primary outcome is compliance | Does not report compliance as the HAI outcome |
| Mestre2012 | MRSA rates shown only in a control chart: no numbers in the text | `not reported` for baseline and post rates; numbers "read" from the figure are not in the text |
| Mestre2012 | Baseline period given three ways (March 2007, October 2007, 2007-2008); phase 1 compliance 78% in Table 2 but 79.5% in the Abstract, with a CI that does not contain 78; denominator per 1,000 in Methods vs per 10,000 in Results | Flags internal inconsistencies |
| AlKuwaiti2017 | Post-intervention HAI rate 2.59 (Abstract, Results), 2.5483 (Table II, 2016) and 2.55 (Discussion); which year was the intervention year is not stated | Quotes one value and its location, notes the others |
| AlKuwaiti2017 | No surveillance definition; no effect estimate (only P < 0.05); a non-significant correlation (r = -0.278, p = 0.381) easily reported as an "effect" | `not reported` where the paper is silent |
| AlKuwaiti2017 | Licence CC BY-NC: not shipped in the repository | Agent track fetches it locally; chat track uses Phan2020 or Mestre2012 |

## Interpreting the scores

- **Coverage first.** The scorer starts with "Screened N of 60 records" and lists records not screened. Metrics are
  computed on the screened records; the line "Sensitivity counting not-screened includes as missed" shows the cost of
  dropped records (chat assistants often drop rows). Agent-track groups should score with `--expect-all`.
- **Sensitivity first.** At title/abstract stage, a missed include is the costly error. Precision against the final
  decision is naturally low because 21 records reached the review's full-text stage: point groups to the
  title/abstract-stage view and to `gold_basis`.
- **Kappa between two runs** shows sampling variability: the same prompt, the same records, different answers. Ask
  what a reviewer would report about it.
- **Extraction:** `QUOTE NOT FOUND` (invented or paraphrased quote), `unsupported` (value where the paper is silent)
  and `false absent` (missed information, often in tables) matter more than small numeric differences. `within tol.`
  values deserve a look (e.g. 2.55 vs 2.59 in AlKuwaiti2017 are two different numbers of the same paper).
- **The reference can be wrong.** R039; the review's Table 1 citing "Larson et al., 2010" for a 2000 paper; values that differ between the abstract, the text and the tables of the same paper (all three extraction papers). Treat a discrepancy as a question for
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
| Network blocks NCBI (records page cannot fill abstracts) | Use the 17 records shipped with abstracts: R008, R011, R018 (the only ones in batch 1), R021, R023, R029, R032, R034, R035, R038, R041, R046, R052, R053, R054, R056, R058; or share the local `screening_records_full.csv` on the facilitator laptop screen (do not post it online) |
| Chat assistant refuses uploads | Paste the text from [`data/fulltext/Phan2020.txt`](data/fulltext/Phan2020.txt) in two halves, in the same conversation |
| Group is fast | Second run in a new chat; or a second paper; or the agent track on all 60 records |
| Group is slow | Screen 10 records only; extract the core fields only (`--core-only` in the scorer) |
| Published website (GitHub Pages) not available | Serve it from a laptop: `cd docs && python3 -m http.server 8000`, then `http://localhost:8000/batch.html` and `scorer.html`; or Option B of the [beginners walkthrough](../beginners/README.md) and the Python scorers |
