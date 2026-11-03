# Failure taxonomy for search strategies

For each category: what to look for, and a check you can run.

| Category | Look for | Check |
|---|---|---|
| **Missing terminology** | Synonyms, spelling variants (UK/US), abbreviations, older and newer terms, related concepts (e.g. for hand hygiene: "handwashing", "hand washing", "hand disinfection", "hand rub*", "alcohol-based", "hand sanitizer/sanitiser"; for the outcome: "nosocomial", "hospital-acquired", "cross infection", specific infections and organisms) | Read titles/abstracts of 5–10 known relevant records: are their key words covered? |
| **Fabricated or incorrect controlled vocabulary** | MeSH/Emtree headings that do not exist, are misspelled, or map to a different concept; subheadings used as headings | Run `"Term"[MeSH Terms]` in PubMed and read the query translation; MeSH Browser |
| **Controlled vocabulary only** | A concept searched only with MeSH: recent records not yet indexed are missed | Is there a free-text `[tiab]` equivalent for every MeSH term? |
| **Overly restrictive concepts** | Too many AND-ed blocks; outcome or study-design blocks at the search stage; narrow phrases in quotes | Remove one block at a time and compare counts; look at what the removed block excluded |
| **Boolean logic problems** | Missing parentheses (`A OR B AND C`), NOT excluding relevant records, OR/AND swapped between blocks | Rewrite the logic as nested blocks and read it aloud |
| **Syntax and field tags** | Wrong tags for the interface (`[tiab]` vs `.ti,ab.`), truncation that is too short (`infect*` vs `inf*`), truncation inside quoted phrases, proximity operators unsupported by the database | Check the interface's help page; run the string |
| **Unnecessary terms or filters** | Language, date or "humans" filters not in the protocol; study-design filters not validated | Compare with the protocol; every limit must be justified |
| **Translation errors** | Strategy copied between PubMed, Embase, Scopus, Web of Science without adapting vocabulary and syntax | Each database needs its own controlled vocabulary (MeSH ≠ Emtree) and syntax |
| **Inconsistent outputs** | The same prompt produced different strategies across runs | Generate twice; differences show which parts are unstable |

## Ranking rule
Rank by *expected loss of relevant studies*, not by number of issues. A fabricated MeSH term OR-ed with good free text costs little; a fabricated term AND-ed as the only representation of a concept can lose most of the evidence.
