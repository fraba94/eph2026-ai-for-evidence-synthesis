# Data of the exercise: how they were built, and their limits

Everything here was built on 3 November 2026 from PubMed and PubMed Central (NCBI E-utilities) by the scripts in
[`../tools/`](../tools/), so it can be rebuilt or replaced. This page gives the full reference of the reference review
and its limits; the other pages introduce it briefly as Pruna et al., *J Clin Med* 2026.

> **Doing the exercise?** This page describes the reference review but does not list its decisions. The review itself
> (and [`../answers/`](../answers/README.md)) names the included studies: open them only after step 3.

## The reference review

> Pruna ED, Davidescu L, Sorop-Florea M, Demeter I, Iurciuc S, Varga NI, David VL, Buleu F, Horhat FG.
> Multimodal Hand Hygiene Interventions and Clinical Healthcare-Associated Infection Outcomes in Acute Care Hospitals:
> A Systematic Review of Quasi-Experimental Studies. *J Clin Med* 2026;15(10):3882.
> doi:[10.3390/jcm15103882](https://doi.org/10.3390/jcm15103882) · PMID 42194842 · PMCID PMC13207023 · CC BY 4.0 ·
> PROSPERO CRD420261339769. Metadata and full text from PubMed / PubMed Central.

**In short.** A systematic review of quasi-experimental studies (interrupted time series, controlled and uncontrolled
before-after) in acute care hospitals; **12 included studies**; screening, extraction, risk of bias (ROBINS-I) and
synthesis by two independent human reviewers without generative AI. **Confirmed** by the workshop team on 6 November 2026 (to adapt the exercise to another review, see
[How to replace](#how-to-replace-the-reference-review)).

**Why this one (for now).** Its question is exactly the exercise question; it is open access under CC BY, so its
criteria, tables and included-study list can be reused here; its full text in PMC lists the **12 included studies**
(Table 1: characteristics; Table 2: outcomes) and the **21 studies excluded after full-text assessment**; its
criteria are explicit and demanding (hospital-wide or multi-ward scope, multimodal intervention, quasi-experimental
designs only, clinical HAI outcome), which makes screening non-trivial. Two human reviewers screened, extracted and
assessed risk of bias independently. **Caveat:** it is recent (2026), not a pre-generative-AI review. Its section 2.5
declares Rayyan (duplicate detection and screening workflow) and ChatGPT for English-language editing only, and states
that no generative AI was used for selection, extraction, risk of bias or synthesis. This declaration is itself a
useful example for the discussion on reporting AI use.

**Alternatives considered** (all verified in PubMed; DOIs from PubMed):

| Review | For | Against |
|---|---|---|
| Gould DJ, Moralejo D, Drey N, Chudleigh JH, Taljaard M. Interventions to improve hand hygiene compliance in patient care. *Cochrane Database Syst Rev* 2017;9:CD005186. doi:[10.1002/14651858.CD005186.pub4](https://doi.org/10.1002/14651858.CD005186.pub4), PMID 28862335 | Cochrane methods, clearly conducted before generative AI (searches to October 2016), 26 studies, GRADE | Primary outcome is compliance; only 8 studies report infection or colonisation. PMC holds the abstract only; the full text is not under CC BY, so tables cannot be shipped |
| Mouajou V, Adams K, DeLisle G, Quach C. Hand hygiene compliance in the prevention of hospital-acquired infections: a systematic review. *J Hosp Infect* 2022;119:33-48. doi:[10.1016/j.jhin.2021.09.016](https://doi.org/10.1016/j.jhin.2021.09.016), PMID 34582962 | Pre-generative-AI, directly about compliance and HAI incidence, 35 studies | Closed access: the included-study list and tables cannot be checked or redistributed here |
| Zhang Y, Chen X, Lao Y, et al. Effects of the implementation of intelligent technology for hand hygiene in hospitals: systematic review and meta-analysis. *J Med Internet Res* 2023;25:e37249. doi:[10.2196/37249](https://doi.org/10.2196/37249), PMID 37247215 | CC BY, searched to December 2022, 36 studies, meta-analysis of HAI rates | Restricted to "intelligent technology" interventions (confusing in an AI workshop); study characteristics only in a supplement |

Clancy C, Delungahawatta T, Dunne CP (*J Hosp Infect* 2021;111:6-26, doi:[10.1016/j.jhin.2021.03.007](https://doi.org/10.1016/j.jhin.2021.03.007))
was also checked: CC BY and pre-AI, but it covers compliance trials without synthesising HAI outcomes.

**What would make the reference authoritative.** A review team's own records: (1) the export of the original
title/abstract screening (one row per record with PMID and include/exclude), which turns the gold standard into
real title/abstract decisions (see "How to replace" below); (2) the review's own extraction sheet, to replace the
provisional extraction values; (3) the authors' confirmation of the included-study list. If the workshop team adopts another
review (for example one of its own reviews conducted without generative AI), the same three files are needed.

## Screening set: `screening_records.csv` (60 records)

Columns: `record_id,pmid,doi,title,abstract,year,journal,license`. Order shuffled with a fixed seed (2026);
`record_id` R001-R060. The answers are in [`../answers/screening_gold.csv`](../answers/screening_gold.csv)
(`record_id,gold_decision,gold_basis`), built from [`../answers/reference_key.yaml`](../answers/reference_key.yaml).

| Part | n | Reference decision | Source |
|---|---:|---|---|
| Studies included by the reference review | 12 | include | its Table 1 and reference list (refs 35-46) |
| Studies excluded by the review after full-text assessment | 21 | exclude | its Results section (refs 14-34; reasons in its Supplementary File S2). They **passed** the review's title/abstract stage |
| Near misses from an approximate PubMed search | 26 | exclude | not included in the review; chosen by the workshop team because they fail a criterion clearly: single ICU/NICU or single ward (5), process outcomes only (7), randomised trials (3), long-term care (1), broad infection-control bundles (5), reviews (2), veterinary (1), outbreak report (1), ecological study (1) |
| Possible gold-standard error | 1 | exclude | a well-known hospital-wide programme that appears to meet the criteria but is neither included nor listed among the review's full-text exclusions; kept as a discussion item |

**Approximate search** (PubMed, 3 November 2026; full strings in [`../review_config.yaml`](../review_config.yaml)):
the review's four domains (hand hygiene AND healthcare-associated infection AND quasi-experimental design AND
hospital, English, NOT long-term care) returned 367 records and retrieves 8 of the 12 included studies; a second query
(randomised trials, ICU-only, long-term care, reviews) supplied the remaining near-miss types.

**Abstracts and licences.** An abstract is shipped only when the article's PubMed Central licence is CC BY or CC0
(17 records; text © the authors, copied verbatim from PubMed, source identified by the `pmid` and `doi` columns). For the other 43 the `abstract` column is empty and `license` says why. They can be filled on your own
computer, not redistributed:

```bash
python3 activity/tools/fetch_abstracts.py        # -> activity/data/local/screening_records_full.csv (git-ignored)
```

The [records page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html) does the same in the browser for chat users.

**Limits (say them in the debrief).**
- The reference decision is the review's **final inclusion**, not its title/abstract decision. At title/abstract stage
  the 21 full-text exclusions were includes; `score_screening.py` therefore also shows a "title/abstract-stage view".
- The review screened a fairly small set (353 records at title/abstract stage) from a narrower search than the one
  used here. Eligible-looking studies exist that it did not include (one is flagged in the set). Near misses were
  chosen so that their exclusion does not depend on this: each fails a criterion on its own. The workshop team's
  reasons are notes, not the review's.
- The review's Table 1 lists "Larson et al., 2010" while the cited paper (PMID 10971880) was published in 2000.
- Records are not a random sample of a real search: includes are over-represented (20%) to make 30 minutes useful.

## Extraction set: `papers.csv`, `extraction_form.csv`, `fulltext/`

Three of the 12 included studies, chosen because they are open access in PMC and differ in length and difficulty:

| study_id | Paper | Licence | Full text here |
|---|---|---|---|
| Phan2020 | *Antimicrob Resist Infect Control* 2020;9:51, doi:[10.1186/s13756-020-00712-x](https://doi.org/10.1186/s13756-020-00712-x), PMID 32276646 | CC BY 4.0 | [`fulltext/Phan2020.txt`](fulltext/Phan2020.txt) |
| Mestre2012 | *PLoS One* 2012;7(10):e47200, doi:[10.1371/journal.pone.0047200](https://doi.org/10.1371/journal.pone.0047200), PMID 23110061 | CC BY 4.0 | [`fulltext/Mestre2012.txt`](fulltext/Mestre2012.txt) |
| AlKuwaiti2017 | *Interv Med Appl Sci* 2017;9(3):137-143, doi:[10.1556/1646.9.2017.24](https://doi.org/10.1556/1646.9.2017.24), PMID 29201437 | CC BY-NC 3.0 | not shipped: `python3 activity/tools/fetch_fulltext.py` |

The form ([`extraction_form.csv`](extraction_form.csv): `field,definition,allowed_values,type,core`) follows the data
items the reference review says it extracted (country, setting, design, wards, intervention, periods, comparator,
outcome definitions, denominators, findings, compliance, co-interventions), plus effect estimate and direction.

The reference values ([`../answers/extraction_gold.csv`](../answers/extraction_gold.csv):
`study_id,field,value,source_quote,location,review_table_value,notes`) are **provisional**: prepared by the workshop
team from the full texts, every value with a verbatim quote that `build_extraction_gold.py check` finds in the text,
and cross-checked with the reference review's own tables (`review_table_value`, copied verbatim; all tables of the
review for all 12 studies are in [`../answers/reference_review_tables.csv`](../answers/reference_review_tables.csv)).
They must be validated against the review team's extraction sheet before being called a gold standard. Where the
paper contradicts itself, or the review's table differs from the paper, the `notes` column says so.

## How to replace the reference review

1. Edit [`../review_config.yaml`](../review_config.yaml) (citation, PICO, criteria C1-Cn, PMC ID) and
   [`../answers/reference_key.yaml`](../answers/reference_key.yaml) (PMIDs of included studies, full-text exclusions,
   near misses with reasons).
2. Rebuild the screening set: `python3 activity/tools/build_screening_set.py` (`--dry-run` to preview).
   With the review team's own screening export (CSV with a PMID column and a decision column):
   `python3 activity/tools/build_screening_set.py --from-export export.csv --id-col pmid --decision-col decision`.
3. Extraction: update [`papers.csv`](papers.csv), run `python3 activity/tools/fetch_fulltext.py`,
   `python3 activity/tools/build_extraction_gold.py tables` (review tables) and
   `python3 activity/tools/build_extraction_gold.py skeleton --out my_work/gold_skeleton.csv`, fill values and quotes,
   then `python3 activity/tools/build_extraction_gold.py check --write`.
4. Update the criteria table in [`../README.md`](../README.md) and the short mentions of the review ("Pruna et al.")
   in the repository's `README.md`, `activity/README.md`, `activity/quick_card.md`, `beginners/README.md` and
   `docs/index.html`, then run `python3 docs/sync_data.py` for the website.
