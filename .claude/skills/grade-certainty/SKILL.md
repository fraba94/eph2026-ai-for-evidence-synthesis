---
name: grade-certainty
description: Draft, for human reviewers, a GRADE certainty-of-evidence profile per outcome - starting level, the five reasons to rate down (risk of bias, inconsistency, indirectness, imprecision, publication bias) and the three reasons to rate up, each with the evidence it rests on (risk-of-bias table, extraction rows, verbatim quotes) and a footnote draft, including the narrative-synthesis case without a pooled estimate. Leaves every rating to the review team. Use whenever someone asks about certainty or quality of the body of evidence, GRADE, a Summary of Findings table or evidence profile, how confident they can be in a review's conclusion, or how to rate evidence from non-randomised studies, even if they only ask "how strong is this evidence?".
license: CC-BY-4.0 (text) and MIT (scripts); see LICENSE and LICENSE-CODE in the source repository
metadata:
  version: '1.0'
  last-reviewed: '2026-11-03'
  author: EUPHA Digital Health and AI Section, EPH 2026 skills building seminar
  source: https://github.com/fraba94/eph2026-ai-for-evidence-synthesis
---

# GRADE certainty of evidence (draft for the review team)

**Arguments:** `[outcome(s)] [extraction.csv] [risk-of-bias table]`

GRADE rates the certainty of a **body of evidence for one outcome**, not the quality of a study and not the review as a whole. Each decision to rate down or up needs a stated reason a reader can check. That makes it a good task for an assistant that collects and organises reasons, and a bad task for one that hands back "low certainty" without them. The ratings belong to the review team.

## Human in the loop
- **The team sets the frame**: which outcomes are rated (usually those in the Summary of Findings table, decided in the protocol), the comparison, how certainty is defined (for example, certainty that there is a non-null effect, or that the effect exceeds a threshold that matters), and the GRADE approach for non-randomised studies (see the table below). If any of this is missing, ask.
- **Draft, never decide.** For each domain write the evidence and a suggestion (`no concern / serious / very serious` for rating down; `none / rate up` for rating up) labelled draft. The team decides every rating and the final level.
- **No new numbers.** Use only effect estimates, confidence intervals, counts and risk-of-bias judgements that exist in the inputs (extraction table, approved risk-of-bias table, the review's own synthesis). Never compute a pooled estimate to make imprecision look assessable. Quote the source text (verbatim, with location) for every number you mention.
- **Do not rate down twice for the same problem** (for example, a co-intervention counted under risk of bias and again under indirectness): say where it is counted.
- Never upgrade automatically: a large effect, a dose-response gradient or opposing plausible confounding needs a written argument that the team accepts.

## Facts to rely on (checked on 3 November 2026)
- Four levels: high, moderate, low, very low; rated separately for each outcome. Five reasons to rate down: risk of bias, inconsistency, indirectness, imprecision, publication bias. Three considerations to rate up: large effect, dose-response, plausible confounding that would reduce the observed effect. Every assessment is justified and documented, usually as footnotes to the Summary of Findings table (Cochrane Handbook, chapter 14, version 6.5, last updated August 2023; GRADEpro GDT is the recommended software).
- Starting level: a body of evidence from randomised trials starts at high, one from non-randomised studies at low; when risk of bias of non-randomised studies is assessed with ROBINS-I, all studies may start at high and are then usually rated down for risk of bias (Handbook chapter 14; Schünemann HJ et al., GRADE guidelines 18, J Clin Epidemiol 2019;111:105-114, doi:10.1016/j.jclinepi.2018.01.012).
- Without a meta-analysis, GRADE can still be applied to a narrative summary of the effect across studies (Murad MH et al., Evid Based Med 2017;22:85-87, doi:10.1136/ebmed-2017-110668); report the synthesis method with SWiM (Campbell M et al., BMJ 2020;368:l6890, doi:10.1136/bmj.l6890).
- Original GRADE description: Guyatt GH et al., BMJ 2008;336:924-926, doi:10.1136/bmj.39489.470347.AD. For current guidance read the GRADE Book (https://book.gradepro.org) and the Handbook chapter 14, not your memory.

| Body of evidence | Risk-of-bias tool | Starting level the team should confirm |
|---|---|---|
| Randomised trials | RoB 2 | high |
| Non-randomised studies (ITS, controlled or uncontrolled before-after, cohort) | ROBINS-I | high, then rate down for risk of bias as ROBINS-I indicates (GRADE 18) |
| Non-randomised studies | another tool | low |

## Procedure
1. **List the outcomes and studies** that contribute to each (from the extraction and the approved inclusion list). Note studies that report the outcome but cannot be used, and why.
2. **Gather the inputs per outcome**: per-study effect estimates or directions as extracted (with their quotes), the team's risk-of-bias judgements, the population, intervention, comparator and outcome measure of each study versus the review question, and any information on unpublished or missing studies (registrations, protocols, small-study patterns the review reported).
3. **Draft each domain** in a table `grade_draft.md`, one block per outcome: `domain | evidence (study IDs, quotes with locations) | draft suggestion | footnote draft | team decision`.
   - *Risk of bias*: from the approved risk-of-bias table only; which domains drive it, in how many studies, and whether excluding the high-risk studies would change the picture.
   - *Inconsistency*: do directions and sizes of effect differ across studies more than chance would explain? Without a pooled estimate, describe the spread of directions.
   - *Indirectness*: differences in population, setting, intervention, comparator or outcome definition from the question (e.g. surveillance definitions, outcome families).
   - *Imprecision*: confidence intervals relative to the threshold the team chose; number of events; without a pooled estimate, say what can and cannot be judged.
   - *Publication bias*: what is known, not guessed; a funnel plot is not meaningful with few studies.
   - *Reasons to rate up*: only if the team asks, with the argument written out.
4. **Draft the plain-language statement** per outcome in the form the team uses (for example "may reduce" for low certainty), marked draft.
5. **Stop** and give the team the table, the open questions (thresholds, double counting, outcomes with too little information) and the list of inputs used.

## Output
- `grade_draft.md`: per outcome, the domain table with evidence and footnote drafts, a blank `team decision` column, and the draft statement.
- After the team decides, the ratings feed the Summary of Findings table and `ai-use-reporting` (AI that suggests certainty judgements must be declared under the 2025 position statement).

## Workshop note
The reference review rated certainty with GRADE by outcome category after a narrative synthesis of 12 quasi-experimental studies, all at serious or critical risk of bias by ROBINS-I (sections 2.4 and 3.3, doi:10.3390/jcm15103882, read in PubMed Central). Its GRADE summary is in its supplementary material, which is not shipped here: discuss the reasoning, not remembered ratings.

## When NOT to use
- To produce final ratings, a Summary of Findings table or a recommendation without the review team. GRADE recommendations (strength and direction) need a separate evidence-to-decision process.
- Before the risk-of-bias judgements exist and have been approved by humans.
- To rate a single study or "the review": GRADE rates the body of evidence for an outcome.
- To fill gaps with numbers not in the inputs (pooled estimates, event counts, thresholds the team did not choose).
