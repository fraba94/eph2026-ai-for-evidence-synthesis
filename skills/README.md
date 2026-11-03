# Skills library: AI agents for evidence reviews, with the human in charge

Seven [Claude Code skills](https://code.claude.com/docs/en/skills) that turn the method of this workshop into reusable instructions for a coding agent. Each one covers a single review task, keeps the human as the decision-maker, writes traceable files (CSV with reasons, quotes and locations), and says when it should **not** be used.

> [!IMPORTANT]
> These skills are for people who already understand how large language models work and can check their output against the source. They make careful work faster. They do not make an inexperienced user safe. If you are new to AI, start with the [AI beginners track](../beginners/README.md), which is for learning only.

The skills live in [`.claude/skills/`](../.claude/skills/). This page is the catalogue.

## Catalogue

| Skill | What it does | Review stage | Input | Output |
|---|---|---|---|---|
| [`review-protocol-check`](../.claude/skills/review-protocol-check/SKILL.md) | Turns a question into PICO/PECO and operational eligibility criteria, runs a completeness check, **refuses to go on without approved criteria** | Question & protocol | Review question or protocol | Criteria table, open questions, `criteria.md` after approval |
| [`search-strategy-critic`](../.claude/skills/search-strategy-critic/SKILL.md) | Acts as a skeptical information specialist: verifies MeSH terms, finds Boolean and syntax errors, ranks the top 3 failure risks. **Breaks the search instead of rewriting it** | Search | Search string, database, question | Concept-block table, vocabulary check, ranked risks |
| [`title-abstract-screening`](../.claude/skills/title-abstract-screening/SKILL.md) | Two independent screening runs with a reason per record citing the criterion, conservative merge (disagreement = unsure), completeness check, kappa | Title/abstract screening | Records CSV + criteria | `screening_run1.csv`, `screening_run2.csv`, `screening_ai.csv` |
| [`full-text-extraction`](../.claude/skills/full-text-extraction/SKILL.md) | Form-first extraction, one paper per context, verbatim quote + location for every value, "not reported" allowed, parsing risks flagged | Data extraction | Extraction form + full texts | `extraction_ai.csv` (long format) |
| [`quote-verifier`](../.claude/skills/quote-verifier/SKILL.md) | Checks every quote against the source text and every number against its quote, then the human-level check of support and of each "not reported" | Verification | Extraction CSV + source text | `verification.csv` |
| [`discrepancy-audit`](../.claude/skills/discrepancy-audit/SKILL.md) | Compares AI with human/gold decisions and classifies each discrepancy (missed include, false include, wrong value, hallucinated value, omission, parsing error, gold error) | Evaluation / piloting | AI CSV + reference CSV | `discrepancy_log.csv`, summary, use-decision table |
| [`ai-use-reporting`](../.claude/skills/ai-use-reporting/SKILL.md) | Builds the AI-use record and drafts the protocol/methods paragraph aligned with the 2025 position statement and RAISE | Reporting | Prompts, outputs, comparison results | `ai_use_record.md`, reporting paragraph |

How they chain in a review:

```
review-protocol-check ──► search-strategy-critic ──► title-abstract-screening ──► full-text-extraction
                                                            │                           │
                                                            ▼                           ▼
                                                     discrepancy-audit ◄──────── quote-verifier
                                                            │
                                                            ▼
                                                     ai-use-reporting
```

Three helper scripts ship with the skills (Python 3, standard library only, no installation):

| Script | Purpose |
|---|---|
| `.claude/skills/title-abstract-screening/scripts/compare_runs.py` | completeness, agreement and kappa between two screening runs; conservative merge |
| `.claude/skills/quote-verifier/scripts/verify_quotes.py` | quote found in source? numbers of the value in the quote? |
| `.claude/skills/discrepancy-audit/scripts/draft_discrepancy_log.py` | draft discrepancy log against a gold file, with provisional categories |

## Principles built into every skill

1. **The human decides, the AI drafts.** No skill marks anything as final.
2. **Stop and ask** when criteria, form fields or a source are ambiguous, instead of choosing silently.
3. **Traceability**: every decision has a reason; every extracted value has a verbatim quote and a location; every record is accounted for.
4. **Conservative errors**: when in doubt, *unsure* rather than *exclude*; *not reported* rather than a guess.
5. **Reproducibility**: run twice, compare, report the differences; record model, version, date and prompt.
6. **No invented citations or numbers.** The source text is the only reference.

## Install and use

### (a) Clone and open with Claude Code (simplest)

```bash
git clone https://github.com/fraba94/eph2026-ai-for-evidence-synthesis.git
cd eph2026-ai-for-evidence-synthesis
claude
```

Project skills in `.claude/skills/` load automatically. Claude uses a skill when your request matches its description, or you can call it directly by name, e.g. `/title-abstract-screening`. Type `/` to see the list. The repository's [`CLAUDE.md`](../CLAUDE.md) gives the agent the workshop rules.

### (b) Copy into your personal skills (available in all your projects)

```bash
mkdir -p ~/.claude/skills
cp -r .claude/skills/* ~/.claude/skills/
```

Personal skills (`~/.claude/skills/<name>/SKILL.md`) are available in every project on your machine. Edit the copies to fit your team's protocol, for example the default screening rule or the columns of your extraction form.

### (c) Other agents (Codex CLI, Gemini CLI, Cursor, Copilot, ...)

Each `SKILL.md` is plain Markdown with a short YAML header, so any agent can follow it:

- The repository's [`AGENTS.md`](../AGENTS.md) contains the shared rules and points to the skills; many agents read `AGENTS.md` automatically.
- If your agent does not discover skills, tell it explicitly: *"Read `.claude/skills/title-abstract-screening/SKILL.md` and follow it to screen `activity/data/screening_records.csv`."*
- Replace `${CLAUDE_SKILL_DIR}` in the commands with the skill's folder path (e.g. `.claude/skills/quote-verifier`).
- For chat assistants without file access, use the [prompt library](../prompts/README.md) instead: same method, copy-paste form.

## Example invocations

```text
/review-protocol-check Are hand hygiene interventions effective in preventing healthcare-associated infections?

/search-strategy-critic ("Hand Hygiene"[MeSH] OR "hand hygiene"[tiab]) AND ("Cross Infection"[MeSH] OR "healthcare-associated infection*"[tiab])  -- database: PubMed

Screen activity/data/screening_records.csv against the criteria in activity/review_config.yaml, two independent runs, then show me the disagreements. Do not score yet.

Extract the fields in activity/data/extraction_form.csv from papers/S01.pdf. One paper only. Quote and location for every value.

Verify extraction_ai.csv against the texts in sources/.

Now score my screening against the gold standard and run the discrepancy audit.

Write the AI-use record and the methods paragraph for what we did today.
```

## Safety notes

> [!WARNING]
> **Data protection.** Do not put personal, patient-level or confidential data (unpublished manuscripts, internal reports, peer-review material) into a cloud model unless your institution has approved that tool for that data. Agents can read every file in the folder you open: open only the project folder.

- **Licences of the PDFs you upload.** A paper you may read is not always a paper you may upload to a third-party AI service. Check the licence (CC BY is the clearest case) and your institution's agreements; the workshop data list a licence for each record.
- **Version drift.** Models and products change without notice. Record the model identifier and date of every run; re-validate on a sample when the model changes.
- **Permission prompts.** Claude Code asks before running commands or editing files. Read what it proposes; do not approve blindly.
- **Responsibility.** Under the Cochrane–Campbell–JBI–CEE position statement (2025), evidence synthesists remain ultimately responsible for their synthesis, AI should be used with human oversight, and AI that makes or suggests judgements should be fully and transparently reported (Flemyng et al., doi:[10.1186/s13750-025-00374-5](https://doi.org/10.1186/s13750-025-00374-5)). See also the RAISE recommendations: <https://osf.io/fwaud/>.

## Adapting a skill

Keep the frontmatter (`name`, `description`), keep the *Human in the loop* and *When NOT to use* sections, and change the procedure to match your protocol. Test a changed skill on a small set with known answers (for example the workshop data) before using it on a real review, and record the version of the skill you used.
