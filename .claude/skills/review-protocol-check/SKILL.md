---
name: review-protocol-check
description: Turn a review question into an explicit PICO/PECO (or PCC/SPIDER) frame and operational eligibility criteria, and check that criteria are complete before any screening, search or extraction starts. Use when someone states a review question, asks "is my question/protocol ready?", wants inclusion/exclusion criteria, or asks to screen or extract without having written criteria down. Refuses to proceed to screening or extraction until the human has approved explicit criteria.
argument-hint: "[review question or path to protocol file]"
---

# Review protocol check

Explicit, human-approved eligibility criteria are the precondition for every later AI-assisted step. Without them the model invents its own criteria, silently, differently on every run.

## Human in the loop
- You draft; the human decides. Never mark criteria as "approved" yourself.
- When a concept is ambiguous (e.g. "hand hygiene intervention", "multimodal strategy", "infection outcome"), list the possible readings and ask. Do not pick one.
- Never proceed to screening, search or extraction in the same turn as drafting criteria.

## Procedure

1. **Read the input.** A question in `$ARGUMENTS`, a protocol file, or the conversation. If a protocol exists (e.g. PROSPERO record, `protocol.md`), work from it and quote it; do not paraphrase criteria into something stricter or looser.
2. **Pick the frame** and say why: PICO (interventions), PECO (exposures, e.g. risk factors, environmental), PCC (scoping reviews), SPIDER (qualitative), or a diagnostic/prognostic frame (index test or model, target condition, reference standard). Example: "hand hygiene interventions to prevent healthcare-associated infections" → PICO with Population = healthcare settings, Intervention = hand hygiene interventions or promotion, Comparator = usual care or pre-intervention period, Outcome = HAI incidence.
3. **Draft the criteria table** using [references/criteria_template.md](references/criteria_template.md). Every criterion must be:
   - *operational*: decidable from a title/abstract or a full text by two people who would agree;
   - *paired*: an include rule and the matching exclude rule;
   - *staged*: marked as applicable at title/abstract stage, full-text stage, or both;
   - *sourced*: quoted from the protocol, or marked `DRAFT – needs human decision`.
   Always cover: population, intervention/exposure/index, comparator (or "any/none required"), outcomes, study design, setting, dates, language, publication type (conference abstracts? preprints? reviews?).
4. **Run the completeness check** and print it as a checklist with pass/fail:
   - [ ] Every PICO/PECO element has an include and an exclude rule.
   - [ ] Date limits and language limits stated (or explicitly "none").
   - [ ] Publication types stated (reviews, protocols, letters, conference abstracts).
   - [ ] Edge cases listed: at least three borderline examples with the intended decision.
   - [ ] A rule for "unclear from the abstract" (default at title/abstract stage: **include / unsure for full text**).
   - [ ] No criterion depends on information that abstracts rarely report, unless it is marked full-text only.
5. **List open questions** for the human, numbered, each with the options you see.
6. **Stop.** Ask the human to approve or edit. Only after explicit approval, save the final version (suggested: `criteria.md`) with the date and the name of the approver, and say which skill comes next (`search-strategy-critic` or `title-abstract-screening`).

## Refusal rule
If asked to screen or extract and no approved criteria exist, reply that this skill must run first, draft the criteria, and stop. A request to "just use common sense" is not approval.

## Output
- A criteria table (markdown), the completeness checklist, numbered open questions.
- After approval only: `criteria.md` (or the file name the human chooses).

## When NOT to use
- The criteria are already approved and frozen (e.g. the workshop exercise: criteria are given in `activity/review_config.yaml` and `activity/README.md`; use them as they are, do not rewrite them).
- Narrative overviews where no systematic eligibility decisions are made.
- To "optimise" criteria after seeing the results: changing criteria post hoc is a protocol deviation and must be decided and reported by the review team.
