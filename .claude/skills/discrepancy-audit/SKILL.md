---
name: discrepancy-audit
description: Compare AI-assisted screening or extraction output with human or gold-standard decisions, classify every discrepancy (missed include, false include, wrong value, hallucinated value, omission, parsing error, ambiguous criterion, gold error), look for errors both AI runs shared, write a discrepancy log and summarise what the errors mean for the review. Use after scoring the workshop exercise, whenever asked "where did the AI go wrong?", to compare AI with manual results, or when piloting or calibrating an AI tool against a human-reviewed sample.
license: CC-BY-4.0 (text) and MIT (scripts); see LICENSE and LICENSE-CODE in the source repository
compatibility: Bundled script needs Python 3 (standard library only). Written for Claude Code; any agent that reads SKILL.md can follow it.
metadata:
  version: '1.1'
  last-reviewed: '2026-11-03'
  author: EUPHA Digital Health and AI Section, EPH 2026 skills building seminar
  source: https://github.com/fraba94/eph2026-ai-for-evidence-synthesis
---

# Discrepancy audit

**Arguments:** `[screening|extraction] [ai.csv] [gold.csv]`

A single accuracy figure hides what matters. One missed eligible study can change a pooled estimate; ten false includes cost ten minutes. The audit looks at each disagreement, asks *why* it happened, and turns that into a decision about whether and how AI can be used for this task.

## Human in the loop
- Run only when the human asks to compare with the reference. In the workshop, `activity/answers/` is opened **only at this point**.
- Categories proposed by you or the script are provisional; the human sets `final_category`. The gold standard can also be wrong: say so when the source text supports the AI, and let the human decide.
- Do not tune prompts on the gold set and then report performance on the same set without saying so (that is overfitting to the test).

## Procedure

1. **Score** with the workshop scorers if they exist (check arguments with `--help` first):
   `python3 activity/tools/score_screening.py ...` or `python3 activity/tools/score_extraction.py ...`. Report their output as is.
2. **Draft the log**:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/draft_discrepancy_log.py screening  screening_merged.csv  activity/answers/screening_gold.csv
   python3 ${CLAUDE_SKILL_DIR}/scripts/draft_discrepancy_log.py extraction extraction.csv activity/answers/extraction_gold.csv
   ```
   It writes `discrepancy_log.csv` with provisional categories and empty `final_category`, `human_note`.
3. **Classify each row** by reading the abstract/full text, the AI reason or quote, and the gold basis. Use the taxonomy:

   | Category | Stage | Meaning | Typical cause |
   |---|---|---|---|
   | `missed_include` | screening | gold include, AI exclude | over-strict reading, criterion applied to info the abstract lacks |
   | `false_include` | screening | gold exclude, AI include | topical similarity mistaken for eligibility |
   | `unsure` (on include / exclude) | screening | AI deferred | ambiguous abstract or criterion; acceptable cost |
   | `ambiguous_criterion` | both | both readings defensible | protocol wording; fix the criteria, not the model |
   | `wrong_value` | extraction | value differs from source | misreading, wrong row/model/subgroup |
   | `parsing_error` | extraction | value wrong because the text extraction was wrong | scrambled tables, two columns, figures |
   | `hallucinated_value` | extraction | value with no support in the source | generated, not read; quote not found |
   | `omission` | extraction | AI "not reported"/missing, source has it | retrieval failure, value in table/figure/supplement |
   | `unit_or_rounding` | extraction | same quantity, different format | form did not define format |
   | `gold_error` | both | the source supports the AI | reference standard mistake; flag to the review team |

   For extraction rows, run `quote-verifier` first: a `quote_not_found` row is a candidate `hallucinated_value`; a quote found in a scrambled table is a candidate `parsing_error`.
   Mark in `human_note` the errors that **both AI runs made** (e.g. a gold include excluded by run 1 and run 2 with the same reason). They are invisible in the run-to-run disagreement report and tell you what a second AI pass will never catch.
4. **Summarise** for the human: counts by category with denominators (e.g. "2 of 9 gold includes missed"), the most serious errors first (missed includes, hallucinated values), patterns (which criterion, which field, which kind of paper), shared errors of the two runs, and what would change the result (clearer criterion, better form definition, different parser, human check of a specific field). When you give agreement with the gold standard, give raw agreement and counts next to kappa: with very few includes, kappa can look poor while agreement is high (PABAK, printed by `compare_runs.py`, shows the size of that effect).
5. **Conclude with a use decision table**: for each task, *AI acceptable as second reviewer / acceptable with full human check / not acceptable*, with the reason. The human makes the final call.

## Output
- `discrepancy_log.csv`: `item,field,ai,ai_reason_or_quote,gold,gold_basis_or_quote,provisional_category,severity,final_category,human_note`
- A summary (counts, patterns, implications, use decision table) suitable for the group discussion or for the `ai-use-reporting` record.

## When NOT to use
- To produce a headline accuracy figure for a tool from a handful of records: small samples give unstable estimates; report counts with denominators and call it a pilot.
- When the reference set was itself produced with the same AI tool (circular).
- To decide that a criterion was "wrong" after seeing results, without the review team: that is a protocol change.
