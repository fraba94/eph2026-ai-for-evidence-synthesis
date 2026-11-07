# 6. Synthesis and reporting

> ⚠️ For learning only: see the disclaimer in the [prompt library index](README.md). You stay responsible for every decision.

Synthesis and certainty judgements are where AI errors are hardest to see and most consequential. Use AI here to draft from tables you have verified, never from papers it has not been given, and report what it did.

---

## 6.1 Evidence table to narrative (with limits)

**Purpose.** Draft a descriptive summary of a verified evidence table.
**When to use.** Only on data you have already verified against the papers.

```text
Below is a verified evidence table from a systematic review. Write a descriptive summary of max 200 words.

Rules:
- Use only the numbers in the table. Do not add studies, numbers or citations.
- Report counts with denominators (e.g. "12 of 30 studies").
- Do not use causal language or judge the certainty of the evidence; describe only.
- After the summary, list every number you used with the table row it came from.
- Then list what the table cannot tell us.

TABLE:
[PASTE VERIFIED TABLE]
```

**Check afterwards.** Every number in the text against the table. Remove any claim not traceable to a row.
**Failure modes.** Invented totals or percentages; over-generalisation ("AI outperforms"); added references.

---

## 6.2 Discrepancy summary (after the workshop exercise)

**Purpose.** Turn the comparison between AI output and the reference review into lessons.
**When to use.** After scoring, with the discrepancy list (see [`activity/README.md`](../activity/README.md) and the scorer at [`docs/scorer.html`](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html)).

```text
Below are the records where the AI screening (or extraction) disagreed with a reference review conducted without generative AI.
For each row, classify the discrepancy as one of:
missed include | false include | unsure | ambiguous criterion | wrong value | parsing error | hallucinated value | omission | unit or rounding | possible error in the reference.
Give a one-line reason based only on the text provided.
Then summarise: counts per category, the most serious errors first, and what would reduce them (clearer criterion, better form definition, human check of a specific field).

DISCREPANCIES:
[PASTE: id, AI decision/value, AI reason/quote, reference decision/value, abstract or quote]
```

**Check afterwards.** You set the final category for each row. Missed includes and hallucinated values matter most.
**Failure modes.** Blaming the reference for every disagreement, or never considering that the reference could be wrong.

---

## 6.3 AI-use statement

**Purpose.** Draft a transparent declaration of AI use for a protocol, methods section or training report.
**When to use.** Whenever AI made or suggested judgements (eligibility, extraction, risk of bias, synthesis, certainty, summaries). The 2025 position statement of Cochrane, the Campbell Collaboration, JBI and CEE asks that such use be fully and transparently reported (doi:[10.1186/s13750-025-00374-5](https://doi.org/10.1186/s13750-025-00374-5)).

```text
Draft an AI-use statement for the methods section of an evidence review, using ONLY the facts I give you.
Where a fact is missing, write [TO CONFIRM] instead of guessing.

Facts:
- Tool / product and model version as displayed: [ ]
- Access route (web chat, API, agent) and settings: [ ]
- Date(s) of use: [ ]
- Review stage(s) and task(s): [ ]
- Prompts: [where they are archived]
- Human role: [who checked what, how disagreements were resolved, who made final decisions]
- Comparison with human decisions, if done: [numbers with denominators, or "not assessed"]
- Problems observed: [ ]

Structure: what was used, for what, how humans oversaw it, how it was evaluated, limitations (including non-reproducible outputs and possible errors). No adjectives like "robust" or "validated" unless a validation is described in the facts.
```

**Check afterwards.** Every sentence against your notes; journal-specific policy; the reporting guideline you follow (PRISMA 2020 includes items on automation tools).
**Failure modes.** Invented version numbers or performance figures; overstating validation.

See also the agent skill [`ai-use-reporting`](../.claude/skills/ai-use-reporting/SKILL.md) and its [record template](../.claude/skills/ai-use-reporting/references/ai_use_record_template.md).
