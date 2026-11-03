---
name: title-abstract-screening
description: Dual-pass title/abstract screening of a CSV of records against explicit, human-approved eligibility criteria - include/exclude/unsure with a criterion-level reason per record, conservative bias toward inclusion, two independent runs with disagreement report, never silently dropping a record, then scoring against a gold standard when one exists. Use when asked to screen abstracts, "triage these records", run the workshop screening exercise on activity/data/screening_records.csv, or act as a second reviewer at title/abstract stage.
argument-hint: "[records.csv] [criteria file]"
---

# Title/abstract screening (dual pass)

The AI is a second pair of eyes, not the reviewer. Its job is to sort records with reasons a human can check quickly, and to be wrong in the safe direction: a false include costs a minute at full text, a missed include can change the conclusions.

## Human in the loop
- **No criteria, no screening.** Take the criteria from the user, from an approved criteria file, or for the workshop from `activity/review_config.yaml` (also in `activity/README.md`). If none exists, stop and run `review-protocol-check`.
- If a criterion is ambiguous for a specific record, mark it `unsure` and write the ambiguity in the reason. Do not resolve ambiguity by inventing a rule; collect these cases and ask the human at the end.
- Final decisions are the human's. Your file is a draft labelled as AI output.
- Do **not** open `activity/answers/` (or any gold file) before both runs are saved and the human asks to score.

## Input
- Records CSV with at least `record_id,title,abstract` (workshop format: `record_id,pmid,doi,title,abstract,year,journal,license`).
- Criteria: the approved criteria file, quoted verbatim into your working notes.

## Procedure

1. **Count first.** Read the CSV with a CSV parser (not by eye). Report the number of records, duplicates of `record_id`, and records with empty abstracts. In the workshop data, empty abstracts can be filled with `python3 activity/tools/fetch_abstracts.py` (check `--help`; needs network) or, if PubMed tools are available, by fetching the abstract by PMID and copying it verbatim. Never write an abstract from memory. Still empty → screen on the title, decision `unsure`, reason `no abstract`.
2. **Number the criteria** (C1, C2, ...) exactly as approved. Every reason cites at least one criterion ID.
3. **Run 1.** For each record, in order, decide:
   - `exclude` only if the title/abstract shows that at least one criterion is clearly **not** met. Reason: `C3 not met: <short quote or paraphrase from the abstract>`.
   - `include` if all title/abstract-stage criteria are met or not contradicted.
   - `unsure` if information is missing or ambiguous. Reason names what is missing.
   - Tie-break rule: **when in doubt, not exclude.**
   Work in batches of about 10–20 records and re-read the criteria at the start of each batch (long contexts degrade attention to instructions in the middle). Write `screening_run1.csv` with exactly the columns `record_id,decision,reason` and one row per input record.
4. **Run 2, independent.** Re-screen from the original CSV in **reverse or shuffled order**, without looking at run 1 (a fresh subagent or a fresh context is best). Write `screening_run2.csv`.
5. **Check completeness and agreement** with the bundled script:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/compare_runs.py RECORDS.csv screening_run1.csv screening_run2.csv --merged screening_merged.csv
   ```
   It reports missing, extra and duplicated records, invalid decisions, raw agreement and Cohen's kappa, lists every disagreement, and writes a merged file where any disagreement becomes `unsure` (conservative). If any record is missing, fix that before going on: **never silently drop a record.**
6. **Report to the human**: counts per decision, agreement statistics, the list of disagreements and of `unsure` records with their reasons, and the criteria that produced the most ambiguity (these are the questions for the human).
7. **Score only when asked.** If a gold file exists (workshop: `activity/answers/screening_gold.csv`) and the human asks to score, run:
   ```
   python3 activity/tools/score_screening.py --help     # check the exact arguments first
   python3 activity/tools/score_screening.py screening_run1.csv --compare screening_run2.csv
   python3 activity/tools/score_screening.py screening_merged.csv    # optional: the conservative merge
   ```
   Then hand over to `discrepancy-audit` to classify each disagreement with the gold standard.

## Output files
| File | Content |
|---|---|
| `screening_run1.csv`, `screening_run2.csv` | `record_id,decision,reason`, one row per record |
| `screening_merged.csv` | merged, disagreements → `unsure` |
| chat report | counts, kappa, disagreements, questions for the human |

## Common failure modes to watch
- Rewarding topical similarity instead of applying criteria ("about AI and infections" ≠ eligible).
- Excluding for information the abstract does not report (e.g. no comparator mentioned): that is `unsure` or `include`, not `exclude`, unless the criterion is title/abstract-stage and clearly contradicted.
- Drifting criteria over a long batch; reasons getting shorter and vaguer towards the end.
- Hallucinated reasons that quote text not in the abstract: spot-check five reasons against the abstract.

## When NOT to use
- Without approved criteria, or to decide the criteria by looking at the records.
- As the only screener of a real review: published guidance expects human oversight (Cochrane–Campbell–JBI–CEE position statement 2025, doi:10.1186/s13750-025-00374-5). Use it as a second reviewer or to prioritise records, with the human deciding.
- Full-text eligibility decisions: those need the full text and the full-text criteria.
- Confidential or unpublished records in a cloud tool not approved by your institution.
