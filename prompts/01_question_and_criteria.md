# 1. Question and eligibility criteria

> ⚠️ For learning only: see the disclaimer in the [prompt library index](README.md). You stay responsible for every decision.

Explicit criteria are the precondition for everything else. If you skip this step, the model will apply its own criteria, silently and differently on every run.

---

## 1.1 Question to PICO/PECO

**Purpose.** Turn a review question into a structured frame and draft criteria you can then edit.
**When to use.** At the start, before searching or screening.

```text
You are an experienced systematic reviewer in public health.

Task: turn the review question below into a structured frame and draft eligibility criteria.
Do not search the literature and do not cite any study.

Review question: [YOUR REVIEW QUESTION]
Type of review: [systematic review of effectiveness / prognostic / diagnostic / scoping / qualitative]

1. Choose the most suitable frame (PICO, PECO, PCC, SPIDER, or population/index/comparator/outcome/setting) and say why in one sentence.
2. Fill a table with columns: Element | Include if | Exclude if | Decidable from abstract? (yes/no)
   Cover: population, intervention/exposure/index, comparator, outcomes, study design, setting, dates, language, publication type.
3. Where my question is ambiguous, do NOT choose for me: list the possible readings as numbered questions.
4. End with: "Criteria are a draft until you approve them."
```

**Expected output.** A table and a list of open questions.
**Check afterwards.** Does each criterion have a matching exclude rule? Would two colleagues apply it the same way? Are dates, language and publication types stated?
**Failure modes.** Criteria stricter or looser than you meant; outcome criteria applied at the abstract stage; invented "standard" restrictions (English only, humans only) you never asked for.

---

## 1.2 Criteria stress test

**Purpose.** Find gaps and ambiguities in criteria you have already written.
**When to use.** Before piloting screening.

```text
Act as a critical methodologist reviewing a protocol. Do not rewrite my criteria.

Here are my eligibility criteria:
[PASTE CRITERIA]

1. For each criterion, give one realistic abstract-level situation where two reviewers could disagree.
2. List any element of the question not covered by an include AND an exclude rule.
3. List criteria that depend on information abstracts rarely report (these belong to full-text stage).
4. Rank the three changes that would most reduce disagreement. Explain each in one sentence.
```

**Check afterwards.** You decide which changes to make; record them with the date.
**Failure modes.** Suggestions that quietly change the scope of the review. Accept only what matches your question.

---

## 1.3 Borderline cases

**Purpose.** Create worked examples that make criteria concrete, for pilot screening and team calibration.

```text
Using only these criteria:
[PASTE CRITERIA]

Invent 6 short, clearly fictional abstract descriptions (2 lines each) that sit on the border of eligibility.
For each, give the decision a careful reviewer should take (include / exclude / unsure) and the criterion that decides it.
Label all examples as FICTIONAL.
```

**Check afterwards.** Discuss the examples with your team; disagreements show where the criteria need wording.
**Failure modes.** Fictional examples later mistaken for real studies: keep the FICTIONAL label.
