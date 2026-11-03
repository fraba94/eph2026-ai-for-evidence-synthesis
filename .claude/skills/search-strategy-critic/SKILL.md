---
name: search-strategy-critic
description: 'Critique a Boolean database search strategy (PubMed/MEDLINE, Embase, Scopus, Web of Science) as a skeptical information specialist - find how it could fail to retrieve relevant studies, verify every MeSH/Emtree term instead of trusting it, detect Boolean and syntax errors, test retrieval of known relevant records, and rank the top failure risks without rewriting the query. Use whenever someone shares a search string, asks "is my search good?", "check my search strategy", "peer review my search", or has just had an AI generate a query, even if they ask to improve it: the job is to break the search, not to improve it.'
license: CC-BY-4.0 (text) and MIT (scripts); see LICENSE and LICENSE-CODE in the source repository
metadata:
  version: '1.1'
  last-reviewed: '2026-11-03'
  author: EUPHA Digital Health and AI Section, EPH 2026 skills building seminar
  source: https://github.com/fraba94/eph2026-ai-for-evidence-synthesis
---

# Search strategy critic

**Arguments:** `[search string or path to file] [database]`

Principle from the workshop: **don't ask the AI to improve the search, ask it to break it.** A strategy can run without errors and still be methodologically inadequate. Sensitivity comes first: a manageable number of hits is not evidence of quality.

## Human in the loop
- You critique; the information specialist or review team decides what to change. **Do not rewrite the query** unless the human explicitly asks after reading the critique.
- If the review question or eligibility criteria are missing, ask for them (or run `review-protocol-check`). A search cannot be judged without the question it serves.
- Say clearly which findings you verified (with a tool) and which are judgement.
- PubMed tools verify MeSH only. Emtree (Embase), CINAHL headings and the syntax of other interfaces cannot be checked that way: mark them `unverified` and name the place where the human can check them.

## Procedure

1. **Collect inputs**: the exact search string as executed, the database and interface (PubMed, Ovid MEDLINE, Embase.com...), date of search, limits/filters, and the review question with criteria. Do not reformat the string; quote it.
2. **Parse it into concept blocks.** Show a table: block, free-text terms, controlled vocabulary terms, field tags, how the block is combined. This makes the logic visible to the human.
3. **Verify controlled vocabulary.** For every MeSH term:
   - If PubMed tools are available (e.g. a PubMed MCP `search_articles` tool), run `"Term"[MeSH Terms]` and check it returns results and that PubMed's query translation maps it to the intended heading. A term that maps to nothing, or to something else, is **fabricated or wrong**.
   - Otherwise tell the human to check each term in the MeSH Browser (https://meshb.nlm.nih.gov/) and mark the term "unverified". Never assert that a heading exists from memory.
   - Note entry dates where relevant (a recent heading will not index older records) and whether explosion is intended.
4. **Check each failure category** in [references/failure_taxonomy.md](references/failure_taxonomy.md): missing terminology, fabricated or incorrect vocabulary, overly restrictive concepts, Boolean logic problems, syntax and field-tag errors, unnecessary terms or filters, translation errors between databases.
5. **Test, don't guess, where you can.** With a PubMed tool: compare hit counts for the full string vs. the string without one block or filter; check whether known relevant records (e.g. a set of PMIDs of included studies the human provides) are retrieved. Report the counts and the date you ran them.
6. **Rank the three most important failure risks**, each with: what could be missed, why, evidence (verified / judgement), and a test the human can run. Then list minor issues.
7. **Stop.** Ask whether the human wants proposed edits. If yes, propose them as a diff against the original, one change per line, each linked to a risk.

## Output format
```
## Concept blocks
| Block | Free text | Controlled vocabulary | Combined with |
## Vocabulary check
| Term | Status (verified / not found / maps elsewhere / unverified) | Evidence |
## Top 3 failure risks
1. ...
## Minor issues
## Tests run (date, tool, counts)
## Not changed: the original query is unchanged.
```

## Reference points
- Cochrane Handbook, Chapter 4 (Searching for and selecting studies): https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04
- PRISMA-S reporting of literature searches: Rethlefsen et al., Syst Rev 2021, doi:10.1186/s13643-020-01542-z
- Report the final executed strategies, databases, platforms and dates; keep AI drafts and prompts with the review records. PRISMA 2020 item 7 asks for the full search strategies for all databases, registers and websites, including any filters and limits used (Page et al., BMJ 2021, doi:10.1136/bmj.n71).

## When NOT to use
- To *generate* a strategy from scratch for a real review without an information specialist: use the critique on a human-drafted strategy instead.
- As proof that a search is comprehensive: a critique reduces risk, it does not validate recall. Validate against a set of known relevant studies.
- For grey-literature or web searches, where Boolean structure and controlled vocabulary do not apply in the same way.
