# Answers: do not open before step 3

> **Stop.** This folder holds the reference answers of the exercise. Opening it (or letting an AI agent read it)
> before you have saved your own screening and extraction makes the comparison meaningless. Go back to
> [`../README.md`](../README.md) until step 3.

| File | Content |
|---|---|
| `screening_gold.csv` | `record_id,gold_decision,gold_basis`: the reference review's final decision for each of the 60 records and the basis for it |
| `reference_key.yaml` | PubMed IDs behind the gold standard: included studies, the review's full-text exclusions, near misses with the workshop team's reason, one possible gold-standard error. Used by `tools/build_screening_set.py` |
| `extraction_gold.csv` | `study_id,field,value,source_quote,location,review_table_value,notes`: provisional reference values for the 3 extraction papers, each with a verbatim quote, plus the reference review's own table entry and notes on ambiguities |
| `reference_review_tables.csv` | Every cell of the reference review's Table 1 (characteristics) and Table 2 (outcomes), for all 12 included studies, linked to PMIDs. From the review's PMC full text (CC BY 4.0) |

How to score: `python3 activity/tools/score_screening.py --help`, `python3 activity/tools/score_extraction.py --help`,
or the [browser scorer](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html). How these answers were made and their limits:
[`../data/README.md`](../data/README.md).

**Reading the answers critically.** The reference is a human product and can be wrong. `gold_basis` says where each
decision comes from; one record is flagged as a *possible gold-standard error*; several extraction values carry notes
because the papers contradict themselves (text versus tables, abstract versus methods) or because the review's table
differs from the paper. The extraction values are provisional until validated against the review team's own
extraction sheet.
