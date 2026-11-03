# Beyond this workshop: curated external skill collections

The ten skills in this repository cover one review workflow with the human in charge. Many other skill collections exist, some with tens of thousands of GitHub stars. This page lists the ones we reviewed on **3 November 2026** for evidence synthesis (systematic, scoping and literature reviews, appraisal, reporting), with what they do well and what to watch for. Stars, licences and last updates come from the GitHub search API on that date; they change quickly.

> [!WARNING]
> **Read before you install.** A skill is not a document: it is a set of instructions that steers your agent, often with scripts the agent will run on your machine with your permissions. A third-party skill can run code, send your files to external services, ask for API keys that cost money, or tell the agent to ignore your instructions.
> - Read **every** `SKILL.md`, reference file and script before installing. If you cannot read the code, do not install the skill.
> - Prefer official or well-maintained sources, and pin a release or commit (for example `gh skill install ... --pin <tag or SHA>`) so that the content cannot change under you.
> - Install into one project folder (`.claude/skills/`) to try it, not into your personal skills for every project.
> - Be wary of skills that need API keys, install packages, call paid services, or promise an "autonomous" or "end-to-end" review. None of them removes your responsibility for every decision.
> - Check the licence before you copy or adapt anything, and the data-protection rules of your institution before any skill touches unpublished or personal data.
> - **Beginners:** as for the rest of this workshop, external skills are for learning only. Do not use them to conduct a real review.

## How to install a skill (general)

| Method | Command or step | Notes |
|---|---|---|
| Claude Code plugin marketplace | `/plugin marketplace add <owner>/<repo>`, then `/plugin install <plugin>@<marketplace>` | Documented by Anthropic for [anthropics/skills](https://github.com/anthropics/skills) (`/plugin install example-skills@anthropic-agent-skills` or `document-skills@anthropic-agent-skills`) and by many repositories below. Anthropic's own marketplace: `/plugin marketplace add anthropics/claude-plugins-official` ([Claude Code docs](https://code.claude.com/docs/en/skills)) |
| Copy a folder | `cp -r <skill-folder> .claude/skills/` (this project) or `~/.claude/skills/` (all your projects) | Works for any skill that follows the [Agent Skills specification](https://agentskills.io/specification); you see exactly what you install |
| Installers | `npx skills add <owner>/<repo>`, `gh skill install <owner>/<repo> [skill] --pin <ref>` | Convenient, but they run code and may install many skills at once; prefer pinning |
| claude.ai | Upload a packaged skill in Settings (Customise, Skills) | Only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools` are accepted in the frontmatter |

## The collections

### Official

| Repository | Stars | Licence | Last update | Useful for evidence synthesis | Caveats | Install |
|---|---:|---|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 186,931 | Apache-2.0 for most skills; the document skills (docx, pdf, pptx, xlsx) are source-available | 2026-10-28 | No review skills, but `skill-creator` shows how to write, test (evals) and improve your own skills, and the `pdf`/`docx`/`xlsx` skills help with files | Presented by Anthropic as demonstration and educational examples; test before relying on them | `/plugin marketplace add anthropics/skills` |

### Science and research collections

| Repository | Stars | Licence | Last update | Useful for evidence synthesis | Caveats | Install (as documented by the repository) |
|---|---:|---|---|---|---|---|
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 55,906 | MIT | 2026-11-02 | 177 skills; `literature-review` (search coverage, records versus studies, PRISMA counts), `scientific-critical-thinking` (RoB 2, ROBINS-I, GRADE guidance with sources), `citation-management`, `peer-review` | Some steps need paid API keys (OpenRouter for figures, Parallel for web search); "conducts systematic reviews" means helps, its scripts do not run a review | `npx skills add K-Dense-AI/scientific-agent-skills` or `gh skill install K-Dense-AI/scientific-agent-skills <skill> --pin <tag>` |
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | 55,127 | CC BY-NC 4.0 | 2026-11-02 | `sr-screener` is the most careful screening skill we found: confirmed protocol first, pilot against the team's own labels, two blinded AI reviewers plus adjudicator, PABAK, re-check of joint exclusions, "record text is data, not instructions", PRISMA counts | Non-commercial licence; a full run fans out to hundreds of agent calls (cost); the wider pipeline goes on to write papers | `/plugin marketplace add Imbad0202/academic-research-skills`, then `/plugin install academic-research-skills` |
| [Aperivue/medsci-skills](https://github.com/Aperivue/medsci-skills) | 363 | MIT | 2026-11-02 | `check-reporting`: 49 reporting guidelines and risk-of-bias tools item by item, licence-aware (summaries for non-commercial tools), PRISMA flow arithmetic; `verify-refs`; `meta-analysis` | 63 skills of uneven relevance; the classroom installer and `npx` run code; read each skill you enable | `/plugin marketplace add Aperivue/medsci-skills` or `gh skill install Aperivue/medsci-skills ...` |
| [mronkko/claude-academic-research](https://github.com/mronkko/claude-academic-research) | 28 | MIT | 2026-11-03 | `fact-check` and `verifying-citations` (one source at a time, abstract then full text, verified / minor / major / unverifiable), human adjudication loop, cost gates | Needs Zotero, MCP servers and API keys; tools are labelled as costing LLM credits; the systematic-review skill is about 1,900 lines and targets social sciences (RoB 2 and ROBINS-I out of scope) | `/plugin marketplace add mronkko/claude-academic-research`, then `/plugin install academic-research@mronkko` |
| [poemswe/co-researcher](https://github.com/poemswe/co-researcher) | 135 | MIT | 2026-11-02 | `systematic-review` and `literature-review` with OpenAlex and Europe PMC search scripts; PRISMA counts produced by a script, not by hand | Casts the agent as a "PhD-level specialist" running the whole review, risk of bias and GRADE included, with few human checkpoints; needs `uv` | `/plugin marketplace add poemswe/co-researcher` |
| [K-Dense-AI/claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer) | 2,552 | MIT | 2026-10-31 | Writing support (papers, reports, grants) with research lookup | Requires `ANTHROPIC_API_KEY` and a Parallel key; produces "publication-ready" drafts: not a review-conduct tool | `/plugin marketplace add https://github.com/K-Dense-AI/claude-scientific-writer` |
| [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) | 550 | MIT | 2026-11-02 | A catalogue and installation layer for 17 research skills with explicit human gates (literature triage, evidence handoffs) | Mostly points to other repositories and an optional runtime installed with `pip` | `claude plugin marketplace add WenyuChiou/ai-research-skills` |
| [htlin222/meta-pipe](https://github.com/htlin222/meta-pipe) | 150 | Academic and non-commercial licence | 2026-09-23 | End-to-end meta-analysis pipeline (screening, extraction, R analysis, manuscript) showing how far automation can be pushed | Sold as "end-to-end automation"; dual AI screening counted as dual review; model-reported confidence used to triage extraction; API keys; restrictive licence | Clone and set up as its README describes |
| [keemanxp/slr-prisma](https://github.com/keemanxp/slr-prisma) | 117 | MIT (licence file; GitHub shows "other") | 2026-03-28 | Walks through writing a review section by section against the PRISMA 2020 items; explains records, reports and studies | Drafts the whole manuscript, introduction and discussion included, with citations; it checks references by web search, but a real reference can still be attached to a claim it does not support | `.skill` file from its Releases page (claude.ai, Customise, Skills), or copy the folder |
| [BESSER-PEARL/research-agent-skills](https://github.com/BESSER-PEARL/research-agent-skills) | 18 | MIT | 2026-10-20 | `research-paper-review`: structured critique, checks for numerical inconsistencies | Written for computer-science papers; not a systematic-review tool | `npx skills add BESSER-PEARL/agent-skills@research-paper-review` (as written in its README) |
| [lingzhi227/agent-research-skills](https://github.com/lingzhi227/agent-research-skills) | 448 | none | 2026-02-27 | `deep-research`: six-phase literature review with phase gates (each phase must leave files on disk) | No licence (no reuse); the skill points to an API-key file on the author's own computer; AI/CS literature focus | Its README uses an `install.sh`: read it before running anything |

### Curated lists (to find more)

| Repository | Stars | Licence | Last update | Useful for evidence synthesis | Caveats |
|---|---:|---|---|---|---|
| [brycewang-stanford/lit-review-agent-tools](https://github.com/brycewang-stanford/lit-review-agent-tools) | 46 | CC0-1.0 | 2026-11-02 | The best starting point: 70+ open-source agent tools for literature review, by workflow stage (search, screen, extract, cite-check, write), each with maintenance status and licence, refreshed weekly | A list, not an endorsement; check each tool |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 78,629 | none detected | 2026-09-18 | General Claude skills list; little on reviews | Includes vendor-promoted entries |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 57,149 | CC BY-NC-ND 4.0 | 2026-11-03 | Claude Code resources: skills, hooks, slash commands, workflows | General purpose |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 36,787 | MIT | 2026-11-02 | 1,000+ skills, many from official product teams | Sponsored entries; almost nothing on evidence synthesis |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | 15,683 | none detected | 2026-04-28 | General list; explains the plugin marketplace | Not updated since April 2026 |

Seen in searches but not reviewed in depth: [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills) (2,028 stars, MIT, hundreds of medical-research skills including RoB 2 and screening skills) and [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) (3,090 stars, no licence detected).

## What we learned, and what we did not adopt

Strong external skills improved ours (see [THIRD_PARTY.md](THIRD_PARTY.md)): treating record text as data rather than instructions, piloting with known eligible studies, PABAK next to kappa, a human re-check of records both AI runs excluded, checking direction and magnitude of a claim and not only the presence of a quote, and an automatic check of PRISMA flow arithmetic.

We deliberately did **not** adopt:
- **"Autonomous" or "end-to-end" reviews.** Several popular collections run search, screening, extraction, risk of bias, GRADE and writing with few human checkpoints. Guidance expects human oversight and responsibility (Cochrane-Campbell-JBI-CEE position statement 2025, doi:[10.1186/s13750-025-00374-5](https://doi.org/10.1186/s13750-025-00374-5)).
- **Two AI passes reported as dual review**, and **model-reported confidence scores** used to decide what humans check.
- **AI-generated risk-of-bias or GRADE ratings.** Our new skills collect the evidence and draft; humans judge.
- **Manuscript drafting with citations by the AI**, because of the risk of invented or misattributed references.
- **Paid APIs, installers and very long skills** (over 1,000 lines), which make a skill hard to read and to audit in a workshop.

To add a collection to this page, or to report that an entry changed, [open an issue](https://github.com/fraba94/eph2026-ai-for-evidence-synthesis/issues/new/choose).
