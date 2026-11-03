# Third-party sources and attribution

On 3 November 2026 the skills in [`.claude/skills/`](../.claude/skills/) were benchmarked against the official Agent Skills specification and examples and against the most-starred public skill repositories for literature and systematic reviews (the full list, with caveats, is in [EXTERNAL.md](EXTERNAL.md)). This page records what came from where.

**Rule we followed.** Text was copied or adapted only from sources whose licence allows it (MIT, Apache-2.0, CC0, CC BY). From repositories with a non-commercial or no licence we took **ideas only**, written in our own words. Third-party content was read as data; none of their scripts was executed.

## Text reproduced

| Source | Licence | What | Where |
|---|---|---|---|
| Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ* 2021;372:n71. doi:[10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71). Full text retrieved from PubMed Central (PMC8005924) | CC BY 4.0 (PMC licence record, checked 3 November 2026) | Item wording of the 27-item checklist and of the 12-item abstract checklist, verbatim; layout changed to Markdown tables; glossary terms summarised | `.claude/skills/prisma-reporting-check/references/prisma_2020_checklist.md` |

**Not reproduced on purpose:** the signalling questions of RoB 2 and ROBINS-I. Their developers license the tools under CC BY-NC-ND 4.0 (https://www.riskofbias.info). `risk-of-bias-assessment` names the domains and judgement levels (facts, summarised in our words from the Cochrane Handbook, chapters 8 and 25) and asks the reviewer to supply the official form.

## Format and method (no text copied)

| Repository | Commit (date) | Licence | What we took |
|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills), `skills/skill-creator`, `spec/`, `template/`; and the specification at https://agentskills.io/specification | `ca45fc4` (2026-10-28) | Apache-2.0 (skill-creator `LICENSE.txt`) | Frontmatter limited to the portable fields (`name`, `description`, `license`, `compatibility`, `metadata`): we removed the Claude Code-only `argument-hint`, which makes uploads to claude.ai or the Skills API fail. Descriptions that say *what* and *when*, slightly "pushy" against under-triggering, no angle brackets, under 1024 characters. Progressive disclosure (`references/`, `scripts/`, SKILL.md well under 500 lines). An `evals/evals.json` per skill in the skill-creator schema (`skill_name`, `evals[].prompt`, `expected_output`, `expectations`) |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | `a25cf9e` (2026-11-02) | MIT | `metadata` with `version` and `last-reviewed`; the pointer that ROBINS-I V2 (November 2025) is a draft, which we then verified on riskofbias.info; keeping records, reports and studies apart in flow counts |

## Ideas adapted in our own words

| Repository | Commit (date) | Licence | Idea | Used in |
|---|---|---|---|---|
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills), `sr-screener` | `2e02041` (2026-11-02) | CC BY-NC 4.0: **ideas only** (non-commercial terms are not compatible with this repository's CC BY 4.0) | Record text is data, not instructions; judge the record text only, no recalled knowledge of the paper; cite the first failing criterion in protocol order; pilot with known eligible ("seed") studies before the full run; report PABAK next to kappa at extreme prevalence; human re-check of a sample of joint exclusions; never fill a failed decision with a default; one model run twice is not two independent reviewers; amendment log | `title-abstract-screening`, `compare_runs.py` (`--qc-sample`, PABAK: own code), `review-protocol-check`, `discrepancy-audit`, `ai-use-reporting` |
| [mronkko/claude-academic-research](https://github.com/mronkko/claude-academic-research), `fact-check`, `verifying-citations` | `34ed022` (2026-11-03) | MIT | Verify one cited source at a time with all its mentions together; abstract first, full text for numbers, quotes and methods; separate "overstated" from "unsupported" and "unverifiable" (an access problem, not a verdict); check direction and magnitude | `quote-verifier` |
| [Aperivue/medsci-skills](https://github.com/Aperivue/medsci-skills), `check-reporting` | `cc462bc` (2026-11-01) | MIT | Automatic check of PRISMA flow-diagram arithmetic; item-by-item status with evidence; licence-aware handling of checklists (verbatim only when the source licence allows) | `prisma-reporting-check` and its script `check_prisma_flow.py` (own code) |
| [poemswe/co-researcher](https://github.com/poemswe/co-researcher), `systematic-review` | `b9da57f` (2026-11-02) | MIT | Pilot-screen about 20 records before bulk screening when the set is large | `title-abstract-screening` |
| [htlin222/meta-pipe](https://github.com/htlin222/meta-pipe) | `5c5c3f0` (2026-09-23) | Academic and non-commercial licence: **ideas only** | Record protocol deviations such as single-reviewer extraction; and, as a counter-example, the use of model-reported confidence scores to decide what to check | `full-text-extraction` |

## Facts verified in primary sources (not taken from any skill)

Checked on PubMed (metadata, abstracts, licences) or in the Cochrane Handbook on 3 November 2026: PRISMA 2020 (doi:10.1136/bmj.n71), ROBINS-I (doi:10.1136/bmj.i4919), RoB 2 (doi:10.1136/bmj.l4898), GRADE (doi:10.1136/bmj.39489.470347.AD), GRADE guidelines 18 on ROBINS-I (doi:10.1016/j.jclinepi.2018.01.012), GRADE without a single effect estimate (doi:10.1136/ebmed-2017-110668), SWiM (doi:10.1136/bmj.l6890), LLM risk-of-bias evaluations (doi:10.2196/70450, doi:10.1001/jamanetworkopen.2024.12687), and the reference review's methods (ROBINS-I, GRADE, PRISMA; doi:10.3390/jcm15103882, PMC13207023). Cochrane Handbook version 6.5: chapter 8 (RoB 2), chapter 14 (GRADE), chapter 25 (ROBINS-I). ROBINS-I V2 status and the tools' licence: https://www.riskofbias.info.
