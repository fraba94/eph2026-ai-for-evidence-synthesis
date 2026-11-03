# 2. Search

> ⚠️ For learning only: see the disclaimer in the [prompt library index](README.md). You stay responsible for every decision.

Sensitivity comes first: missing eligible evidence can distort a synthesis, and a manageable number of hits is not evidence of quality. A strategy can run without errors and still be methodologically inadequate. Work with an information specialist for real reviews.

---

## 2.1 Draft concept blocks

**Purpose.** A first draft of terms per concept, to be reviewed, not executed as is.
**When to use.** After criteria are approved, as a starting point for the information specialist.

```text
You are an information specialist building a sensitive search for [DATABASE, e.g. PubMed].

Review question: [QUESTION]
Eligibility criteria: [PASTE CRITERIA]

1. Identify the 2-4 concepts that should be searched (not every criterion belongs in the search: outcomes and study design usually do not).
2. For each concept list: free-text terms with synonyms, spelling variants, abbreviations and truncation; and candidate controlled-vocabulary terms (MeSH).
3. Mark EVERY MeSH term as "to verify in the MeSH Browser". Do not claim a heading exists unless you are certain, and say if you are unsure.
4. Combine terms with OR within a concept and AND between concepts, using [tiab] and [MeSH] field tags.
5. List what this draft is likely to miss.
```

**Expected output.** Concept blocks, a draft Boolean string, a list of likely gaps.
**Check afterwards.** Verify each MeSH term at <https://meshb.nlm.nih.gov/>. Run the string in the database; check that a few known relevant studies are retrieved.
**Failure modes.** Fabricated or misspelled MeSH headings; outcome and design blocks that make the search too narrow; filters you did not ask for.

---

## 2.2 Break my search (critique mode)

**Purpose.** The most useful search prompt: *don't ask it to improve the search, ask it to break it.*
**When to use.** On any strategy, yours or AI-generated, before running it for real.

```text
Act as a skeptical information specialist.
Your task is NOT to rewrite this search strategy.
Identify how it could fail to retrieve relevant studies.

Review question: [QUESTION]
Database and interface: [e.g. PubMed]
Search strategy:
[PASTE THE EXACT STRING]

Check for:
- missing terminology (synonyms, variants, abbreviations, older/newer terms)
- incorrect or fabricated MeSH terms (say which ones you cannot confirm)
- overly restrictive concepts
- Boolean logic problems (parentheses, AND/OR/NOT)
- syntax and field-tag errors for this interface
- unnecessary terms or filters

Rank the three most important failure risks, each with: what could be missed, why, and a test I can run.
Do not modify the query yet.
```

**Expected output.** A ranked list of failure risks and tests.
**Check afterwards.** Run the tests yourself (remove one block, compare hit counts; check known studies). Verify any MeSH claim in the MeSH Browser.
**Failure modes.** The model "finds" errors that are not there, or misses real ones; it may suggest incorrect revisions. Treat each point as a hypothesis to test.

---

## 2.3 Translate between databases

**Purpose.** Adapt a validated PubMed strategy to another database's syntax.

```text
Translate this PubMed strategy into [Embase.com / Ovid MEDLINE / Scopus / Web of Science] syntax.

[PASTE STRATEGY]

Rules:
- Keep the logic identical; one line per concept block.
- Controlled vocabulary differs between databases (MeSH is not Emtree): for each heading give the candidate equivalent and mark it "to verify".
- List every element you could not translate exactly.
```

**Check afterwards.** Verify each heading in the target database's thesaurus; compare hit counts; consider translation tools such as the Polyglot Search Translator.
**Failure modes.** MeSH copied into Emtree; proximity operators and truncation that do not exist in the target interface.
