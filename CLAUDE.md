# Claude Code instructions

@AGENTS.md

## Specific to Claude Code

- The skills in `.claude/skills/` load automatically. Prefer them over improvising: `review-protocol-check`, `search-strategy-critic`, `title-abstract-screening`, `full-text-extraction`, `quote-verifier`, `discrepancy-audit`, `risk-of-bias-assessment`, `grade-certainty`, `prisma-reporting-check`, `ai-use-reporting`. Catalogue: `skills/README.md`.
- For the second screening run or for one-paper-per-context extraction, use a subagent with a fresh context, so the second pass is independent of the first.
- If PubMed tools are available in the session (e.g. a PubMed MCP server), use them to verify MeSH terms, PMIDs, DOIs and abstracts instead of relying on memory. Attribute information to PubMed and give DOIs.
- The exercise question is hand hygiene → healthcare-associated infections; the reference review and its criteria are in `activity/review_config.yaml`. If abstracts in `activity/data/screening_records.csv` are empty, offer to run `activity/tools/fetch_abstracts.py` (or use PubMed tools to fetch them by PMID, copying the abstract verbatim); otherwise mark those records `unsure`.
- Write outputs in `my_work/` (create it if needed). Never edit `activity/data/` or `activity/answers/`.
- If the user is a workshop participant with little AI experience, point them to `beginners/README.md` and remind them that the beginners track is for learning only.
- Before saying a task is complete, run the relevant check (`compare_runs.py`, `verify_quotes.py`, or the scorer when the user has asked to score) and report its output.
