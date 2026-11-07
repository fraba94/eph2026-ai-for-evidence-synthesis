# Instructions for AI agents working in this repository

This file is for any coding agent (Claude Code, Codex CLI, Gemini CLI, Cursor, Copilot and others) opened in this repository. Read it before doing anything.

## What this repository is

Teaching material for the skills-building seminar **"Building skills in using AI tools to support evidence reviews for effective public health strategies"** (EPH Conference 2026, Bilbao), organised by the EUPHA Digital Health and Artificial Intelligence (DHAI) section with Concordia University, Leibniz ScienceCampus Digital Public Health Bremen and the Italian Society for AI in Medicine (SIIAM).

Participants use AI to screen abstracts and extract data on a deliberately uncontroversial question, so that the focus stays on the AI method: **the effectiveness of hand hygiene interventions in preventing healthcare-associated infections (HAI)**. PICO of the reference review: *Population* patients and healthcare workers in acute care hospitals; *Intervention* multimodal hand hygiene intervention, hospital-wide or across more than one ward; *Comparator* pre-intervention period, standard practice or a contemporaneous comparator group; *Outcome* clinical HAI outcomes; quasi-experimental designs (criteria C1–C6 in `activity/review_config.yaml`).

The AI output is compared with **the reference review**, a systematic review conducted **without generative AI**. Its citation, question and eligibility criteria are defined in `activity/review_config.yaml` (confirmed by the workshop team on 6 November 2026). Always read the criteria from there, from `activity/README.md`, or from the user; never reconstruct them from memory.

**Position of the repository:** AI can bring real advantages to evidence synthesis (speed, scale, consistency, living updates), but only for people with AI literacy and advanced skills. Users who do not understand how these systems work risk serious errors and losing control of the process. Human reviewers stay responsible for every decision.

## Where things are

| Path | Content |
|---|---|
| `activity/README.md` | The hands-on guide: task, eligibility criteria, steps |
| `activity/review_config.yaml` | The reference review: citation, question, eligibility criteria |
| `activity/data/screening_records.csv` | Records to screen: `record_id,pmid,doi,title,abstract,year,journal,license` (no labels). Some abstracts may be empty until filled by `activity/tools/fetch_abstracts.py` |
| `activity/data/extraction_form.csv` | Extraction form: `field,definition,allowed_values,type` |
| `activity/answers/` | **Reference answers. Do not open until the user asks to score.** |
| `activity/tools/score_screening.py`, `activity/tools/score_extraction.py` | Scorers (Python 3, standard library) |
| `.claude/skills/` | Agent skills, one folder per review task (`SKILL.md`) |
| `skills/README.md` | Catalogue of the skills and how to install them; `skills/EXTERNAL.md` lists external skill collections (read its security note), `skills/THIRD_PARTY.md` records attribution |
| `prompts/` | Prompt library for chat assistants, by review stage |
| `beginners/` | AI beginners track (for learning only) |
| `docs/` | Website, including a browser-based scorer |

## Rules

1. **The human decides.** You draft, sort, quote and flag. Never present AI output as a final decision. When eligibility criteria, form fields or a source passage are ambiguous, stop and ask; do not choose silently.
2. **Never invent citations, DOIs, PMIDs, numbers or quotes.** If you cannot verify something in a source available in this session, say it is unverified. Your memory is not a source.
3. **Verbatim quotes.** Every extracted value carries a quote copied character for character from the source text, plus its location (section, table, page). If the information is absent, write `not reported` and say where you looked.
4. **Traceability.** Every screening decision has a reason that names the criterion. Every input record appears in the output exactly once: never drop a record silently. Keep prompts, model/version, dates and raw outputs.
5. **Conservative at title/abstract stage.** When in doubt, `unsure`, not `exclude`.
6. **Run twice** when the task allows, and report differences between runs.
7. **Do not read `activity/answers/`** (or any gold file) before the user explicitly asks to score or compare. Reading it earlier invalidates the exercise.
8. **Data protection and licences.** Do not send personal or confidential data to external services. Process full texts only if their licence allows it (see the `license` column).
9. **Stay in this folder.** Do not read or write outside the repository. Do not modify the files in `activity/data/` or `activity/answers/`; write your outputs to new files (suggested: `my_work/`).

## Empty abstracts

Some records in `activity/data/screening_records.csv` may have an empty `abstract`. Where the network allows, they can be filled with `python3 activity/tools/fetch_abstracts.py` (check `--help`). If an abstract is still empty, screen on the title only, mark the record `unsure` with reason `no abstract`, and tell the user. Never write an abstract from memory.

## File formats for outputs

File names are the same as in `activity/README.md`, for both the chat and the agent track.

- Screening decisions: `screening_run1.csv`, `screening_run2.csv` (and, for agents, the conservative merge `screening_merged.csv`), columns `record_id,decision,reason` with `decision` in `include|exclude|unsure`.
- Extraction: `extraction.csv`, long format `study_id,field,value,source_quote,location`, one row per study and field. When a paper does not report a field, write exactly `not reported`.
- Full texts for extraction: `activity/data/fulltext/<study_id>.txt` (e.g. `Phan2020.txt`); the study list is `activity/data/papers.csv`.

## How to run the scorers

Check the arguments first, then score (only when the user asks):

```bash
python3 activity/tools/score_screening.py --help
python3 activity/tools/score_screening.py my_work/screening_run1.csv --compare my_work/screening_run2.csv
python3 activity/tools/score_extraction.py --help
python3 activity/tools/score_extraction.py my_work/extraction.csv
```

Helper scripts (standard library only):

```bash
python3 .claude/skills/title-abstract-screening/scripts/compare_runs.py activity/data/screening_records.csv my_work/screening_run1.csv my_work/screening_run2.csv --merged my_work/screening_merged.csv --qc-sample 10
python3 .claude/skills/quote-verifier/scripts/verify_quotes.py my_work/extraction.csv activity/data/fulltext/ --out verification.csv
python3 .claude/skills/discrepancy-audit/scripts/draft_discrepancy_log.py screening my_work/screening_merged.csv activity/answers/screening_gold.csv
python3 .claude/skills/prisma-reporting-check/scripts/check_prisma_flow.py my_work/flow_counts.csv
```

Screening one batch only (e.g. R041-R060)? Filter the records file to that batch first and give the filtered file to `compare_runs.py`: with the full 60-record file it reports the other 40 records as missing.

## Skills (task procedures)

Follow the matching `SKILL.md` when the user asks for one of these tasks. Agents that do not load skills automatically should read the file directly.

| Task | File |
|---|---|
| Question → PICO/PECO and eligibility criteria | `.claude/skills/review-protocol-check/SKILL.md` |
| Critique a search strategy | `.claude/skills/search-strategy-critic/SKILL.md` |
| Title/abstract screening | `.claude/skills/title-abstract-screening/SKILL.md` |
| Full-text data extraction | `.claude/skills/full-text-extraction/SKILL.md` |
| Verify extracted values against the source | `.claude/skills/quote-verifier/SKILL.md` |
| Compare AI with the reference, classify errors | `.claude/skills/discrepancy-audit/SKILL.md` |
| Risk-of-bias evidence table (ROBINS-I, RoB 2), humans judge | `.claude/skills/risk-of-bias-assessment/SKILL.md` |
| GRADE certainty draft per outcome, team decides | `.claude/skills/grade-certainty/SKILL.md` |
| Check a review against PRISMA 2020, flow arithmetic | `.claude/skills/prisma-reporting-check/SKILL.md` |
| Document and report AI use | `.claude/skills/ai-use-reporting/SKILL.md` |

## Guidance to rely on

- Position statement on AI use in evidence synthesis across Cochrane, the Campbell Collaboration, JBI and the Collaboration for Environmental Evidence (2025): doi:10.1186/s13750-025-00374-5 (also doi:10.1002/cl2.70074).
- RAISE, Responsible use of AI in evidence SynthEsis: https://osf.io/fwaud/
- Cochrane Handbook, Chapter 4 (searching and selecting studies) and Chapter 5 (collecting data): https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04 and .../chapter-05

Writing language for this repository: English.
