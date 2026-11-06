<a href="https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/"><picture>
  <source media="(max-width: 700px) and (prefers-color-scheme: dark)" srcset="assets/figures/hero-mobile-dark.svg">
  <source media="(max-width: 700px)" srcset="assets/figures/hero-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/figures/hero-dark.svg">
  <img src="assets/figures/hero-light.svg" width="100%" alt="AI for evidence synthesis. EPH 2026 Bilbao, skills building seminar M.8, EUPHA Digital Health and Artificial Intelligence Section. Screening and data extraction with AI, checked against a systematic review done by humans. An AI can screen all 60 records for you: would you notice the ones it got wrong? A schematic screening sheet shows one record that the AI excluded and the humans included.">
</picture></a>

> **Best viewed on the workshop website: <https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/>** (in the room? open [Start here](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/start.html)). The guides below are the same pages, as Markdown files.

**Hands-on materials for screening studies and extracting data with AI, and for checking the result against a systematic review done by humans.** Skills building seminar of the EUPHA Digital Health and Artificial Intelligence Section at the European Public Health Conference 2026, Bilbao (12 November 2026). Everything stays online: you can do the exercise on your own, without the session.

<p align="center">
  <a href="activity/README.md"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/buttons/activity-dark.svg"><img src="assets/buttons/activity-light.svg" width="49%" alt="Start the activity: 30 minutes, on your own"></picture></a>
  <a href="beginners/README.md"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/buttons/beginners-dark.svg"><img src="assets/buttons/beginners-light.svg" width="49%" alt="AI beginners track: learning only"></picture></a>
  <a href="https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/buttons/records-dark.svg"><img src="assets/buttons/records-light.svg" width="49%" alt="Records to screen: copy-ready batches"></picture></a>
  <a href="https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/buttons/scorer-dark.svg"><img src="assets/buttons/scorer-light.svg" width="49%" alt="Score your results: in your browser"></picture></a>
  <a href="prompts/README.md"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/buttons/prompts-dark.svg"><img src="assets/buttons/prompts-light.svg" width="49%" alt="Prompt library: 18 prompts, 6 stages"></picture></a>
  <a href="skills/README.md"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/buttons/skills-dark.svg"><img src="assets/buttons/skills-light.svg" width="49%" alt="Agent skills: 10 skills, Claude Code"></picture></a>
</p>

<p align="center">
  <a href="https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/"><b>Workshop website</b></a> &nbsp;·&nbsp;
  <a href="activity/README.md#doing-it-on-your-own-self-paced"><b>Do it on your own</b></a> &nbsp;·&nbsp;
  <a href="REFERENCES.md"><b>Useful references</b></a> &nbsp;·&nbsp;
  <a href="docs/slides/README.md"><b>Slides and abstract</b></a> &nbsp;·&nbsp;
  <a href="#quick-start-for-agents"><b>Quick start</b></a>
</p>

## The key message

<a href="REFERENCES.md" title="The evidence behind the key message"><picture>
  <source media="(max-width: 700px) and (prefers-color-scheme: dark)" srcset="assets/figures/key-message-mobile-dark.svg">
  <source media="(max-width: 700px)" srcset="assets/figures/key-message-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/figures/key-message-dark.svg">
  <img src="assets/figures/key-message-light.svg" width="100%" alt="Same tools, opposite outcomes. With three things together, AI literacy and advanced skills, review methods expertise and a verification workflow (necessary, not sufficient), AI tools bring real advantages (speed, scale, consistency, living updates) with the human in the loop. Without them, trusting fluent output leads to missed studies, invented values and unchecked runs: serious errors, loss of control, human out of the loop.">
</picture></a>

AI can bring real advantages to evidence synthesis (speed, scale, consistency, living updates), **but only to people with AI literacy and advanced skills.** Those skills are necessary, not sufficient: they work together with review methods expertise and a verification workflow. Without them come serious errors and loss of control, and the human drops out of the loop. Human reviewers stay responsible for every decision.

> [!WARNING]
> **For learning only.** These prompts are teaching material for this workshop. They are not a validated method.
> If you are not confident with how large language models work (context windows, parsing, sampling, retrieval,
> hallucination) and with advanced techniques (structured outputs, verification against the source, reproducibility
> checks, documentation of model and version), **do not use AI to conduct a real evidence review.** You stay
> responsible for every decision: the AI does not.

## How the session works

<a href="activity/README.md#the-60-minute-session" title="The 60-minute session in the activity guide"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/figures/session-dark.svg">
  <img src="assets/figures/session-light.svg" width="100%" alt="How the session works: 60 minutes. Expert talks 10 min (limitations, with Patrick Boudreau, then benefits, with Francesco Baglivo), demo of open-access tools 10 min (Francesco Baglivo drives the AI, Patrick Boudreau checks the source), exercise on your own 30 min, discussion 10 min. The exercise: 1 screen (10 min, 20 records with your AI, then paste its answer into the scorer), 2 look at the errors (10 min, open 2 missed or false includes and decide why the AI got them wrong), 3 short extraction (10 min, one paper, 5 fields, a verbatim quote for each, check 2 with Ctrl+F), then 4 discuss (10 min, each person brings one error they found).">
</picture></a>

**Watch the demo video first** (about 2 minutes, silent, with captions): **one repository, your AI, your way.** The repository holds the materials; bring the AI you use (copy and paste, attach the files, or connect an agent), then check it against the human review. Real AI answers on demo material (batch 3 and Mestre2012). [On the Start page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/start.html#demo) · [MP4](docs/assets/demo/demo.mp4) · [what it shows and the raw AI answers](demo/README.md).

The live session is on Thursday 12 November 2026, 16:45-17:45, at EPH 2026 in Bilbao (seminar M.8). **Not there?** You do not need the talks or a facilitator: watch the demo video, then allow 60 to 90 minutes and follow [Doing it on your own (self-paced)](activity/README.md#doing-it-on-your-own-self-paced), which says how to be your own verifier, when to open the answers and how to read the score.

**The exercise.** The question is deliberately uncontroversial, so the focus stays on the AI method: *how effective are hand hygiene interventions in preventing healthcare-associated infections?* The reference standard is the review by **Pruna et al.** (*J Clin Med*, 2026), a systematic review of quasi-experimental studies in acute care hospitals with 12 included studies, screened and extracted by two independent human reviewers without generative AI ([doi:10.3390/jcm15103882](https://doi.org/10.3390/jcm15103882)). The choice was confirmed by the workshop team on 6 November 2026; details and limits are in [`activity/data/README.md`](activity/data/README.md). Open the review after the exercise, not before: it names the included studies. Each person works on their own laptop, in three moves: screen 20 records with an AI and paste its answer into the [scorer](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html); look at two of its errors and decide why it got them wrong; extract 5 fields from one paper, each with a verbatim quote. Then everyone discusses where, and why, the AI and the humans differ: missed studies, invented values, "not reported" when the information is there. You drive the AI, then you verify it. The criteria, the steps and what to do next ("Going further") are in the [activity guide](activity/README.md); every material is one tap away on the [website](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/start.html).

<details>
<summary><b>Learning objectives</b></summary>

1. Apply AI tools to screening and data extraction within a structured review workflow.
2. Compare AI-assisted outputs with manual results and identify discrepancies.
3. Critically assess risks, limitations and appropriate use of AI in evidence synthesis.
</details>

<a href="activity/README.md#files-of-the-exercise" title="The files of the exercise"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/figures/at-a-glance-dark.svg">
  <img src="assets/figures/at-a-glance-light.svg" width="100%" alt="At a glance: 60 records to screen, titles and abstracts; 12 human includes in the reference review; 3 full-text papers for data extraction; 19 extraction fields, 11 of them core; 10 agent skills for Claude Code; 18 chat prompts in 6 review stages.">
</picture></a>

## See it before you start

The website gives the chat track everything without installing anything: the records in copy-ready batches (abstracts that the repository cannot ship are fetched from PubMed in your browser) the full texts and a ready extraction prompt on the [Papers page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/papers.html), a scorer that compares the AI's pasted answer with the reference review, and the [reference answers](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/answers.html) behind a button (screening answers after step 1, extraction answers after step 3). Shown here with the fake decisions of [`activity/examples/`](activity/examples/README.md).

<a href="https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html"><img src="assets/screenshots/scorer.png" width="100%" alt="Screenshot of the scorer with the example decisions: sensitivity 81.8%, specificity 56.2%, precision 30.0%, 2 missed includes, and the confusion matrix with 9 true includes, 21 false includes, 2 missed includes and 27 true excludes."></a>
<p align="center"><sub>The scorer with the example file: the same numbers as <code>python3 activity/tools/score_screening.py activity/examples/decisions_example.csv</code></sub></p>

> [!NOTE]
> **Website not available?** The records page and the scorer are on GitHub Pages. Without them, everything still works: build the batches on your computer ([Option B of the beginners track](beginners/README.md#step-2-screen-20-abstracts): `fetch_abstracts.py` and `make_batches.py`), score with the Python scorers in [`activity/tools/`](activity/tools/README.md) (standard library only), or serve the same pages locally with `cd docs && python3 -m http.server 8000`. Details: [activity guide](activity/README.md#doing-it-on-your-own-self-paced).

<details>
<summary><b>The records page</b> (screenshot)</summary>
<br>
<a href="https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html"><img src="assets/screenshots/batch.png" width="100%" alt="Screenshot of the records page: 60 records loaded, batches 1-20, 21-40 and 41-60, 20 records ready with 3 abstracts from the file and 17 fetched from PubMed, and the learning-only notice."></a>
</details>

## Choose your path

<a href="activity/README.md#choose-your-track" title="Choose your track"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/figures/tracks-dark.svg">
  <img src="assets/figures/tracks-light.svg" width="100%" alt="Agent track, for Claude Code or another coding agent, needs AI literacy and advanced skills: clone the repository, skills load automatically, screen all 60 records and extract 3 papers, score against the reference. Chat track, any chat assistant, learning only: open the beginners guide, copy a batch and a prompt, paste the answer in the scorer, look at the errors. Both end the same way: compare with the human reference review, then discuss.">
</picture></a>

<details>
<summary><b>The two tracks side by side</b></summary>
<br>

| | **Agent track** | **Chat track** |
|---|---|---|
| **For** | People who already use Claude Code or another coding agent, and know how to check its work | Everyone else: any chat assistant (ChatGPT, Claude, Gemini, Copilot, Mistral...), no installation |
| **Start** | [Quick start for agents](#quick-start-for-agents) | [AI beginners track](beginners/README.md) |
| **Records** | [`activity/data/`](activity/README.md), all 60 | [Copy-ready batches](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html), R001-R020 |
| **Score** | `activity/tools/score_*.py` or the [web scorer](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html) | The [web scorer](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html): nothing is uploaded |
| **Status** | Needs AI literacy and advanced skills | **For learning only** |
</details>

### Quick start for agents

```bash
git clone https://github.com/fraba94/eph2026-ai-for-evidence-synthesis
cd eph2026-ai-for-evidence-synthesis
claude          # open the folder with Claude Code
```

When Claude Code opens the folder it reads [`CLAUDE.md`](CLAUDE.md) and [`AGENTS.md`](AGENTS.md), and the ten skills in [`.claude/skills/`](.claude/skills/) load automatically: Claude uses one when your request matches its description, or you can call it by name (for example `/title-abstract-screening`). Other agents (Codex CLI, Gemini CLI, Cursor, Copilot...) read [`AGENTS.md`](AGENTS.md). Looking for more skills? [`skills/EXTERNAL.md`](skills/EXTERNAL.md) is a curated list of external collections, with a security note: read it before installing anything.

<details>
<summary><b>The ten skills, one line each</b></summary>
<br>

| Skill | Use it to |
|---|---|
| `review-protocol-check` | turn the question into PICO and explicit eligibility criteria before anything else |
| `search-strategy-critic` | break a search strategy, not improve it |
| `title-abstract-screening` | screen twice, with a reason per record, and merge conservatively |
| `full-text-extraction` | fill a form designed first, with a verbatim quote and location for every value |
| `quote-verifier` | check every quote and number against the source |
| `discrepancy-audit` | compare with the reference review and classify each error |
| `risk-of-bias-assessment` | collect the evidence for each ROBINS-I or RoB 2 domain, with quotes; humans judge |
| `grade-certainty` | draft the GRADE reasons per outcome; the team rates |
| `prisma-reporting-check` | check a review against PRISMA 2020, item by item, with quotes |
| `ai-use-reporting` | document model, version, prompts and checks for the methods section |

Catalogue and installation notes: [`skills/README.md`](skills/README.md).
</details>

### Quick start for AI beginners

1. Read the warning above, then open the [AI beginners track](beginners/README.md).
2. Copy a batch of records from the [records page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html) and paste it into your chat after the screening prompt.
3. Save the answer as `record_id,decision,reason` and load it into the [scorer](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/scorer.html).
4. Bring your missed includes and your surprises to the discussion; on your own, answer the [discussion questions](activity/README.md#discussion-last-10-minutes-of-the-session) in writing.

## Inside the repository

<a href="skills/README.md"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/figures/review-map-dark.svg">
  <img src="assets/figures/review-map-light.svg" width="100%" alt="Where AI can help and where a human must check, stage by stage, with the agent skills and chat prompts of this repository. Question: AI drafts PICO terms; a human owns the question and sets criteria first; review-protocol-check; prompts 1.1 to 1.3. Search: AI drafts Boolean strings; a human runs the search and tests known studies; search-strategy-critic; 2.1 to 2.3. Screen: AI pre-screens; a human makes final calls and audits exclusions; title-abstract-screening; 3.1 to 3.3. Extract: AI drafts values with verbatim quotes; a human designs the form and checks every value; full-text-extraction and quote-verifier; 4.1 to 5.3. Appraise: AI collects passages and drafts GRADE reasons; a human judges bias and certainty; risk-of-bias-assessment and grade-certainty; 6.1. Report: checklist support and AI-use record; a human is accountable and discloses AI use; prisma-reporting-check and ai-use-reporting; 6.2 to 6.3. Across stages: discrepancy-audit. Red flags at every stage: invented studies or values, not reported when the text is there, a different answer on a second run, undocumented model.">
</picture></a>

<a href="prompts/02_search.md"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/figures/prompt-card-dark.svg">
  <img src="assets/figures/prompt-card-light.svg" width="100%" alt="A prompt from the library, prompt 2.2 Break my search (critique mode), verbatim excerpt: Act as a skeptical information specialist. Your task is NOT to rewrite this search strategy. Identify how it could fail to retrieve relevant studies. [...] Rank the three most important failure risks, each with: what could be missed, why, and a test I can run. Do not modify the query yet. Why it works: asking to improve yields confident rewrites; asking to break yields checkable problems.">
</picture></a>

<details>
<summary><b>Repository map</b></summary>

```text
eph2026-ai-for-evidence-synthesis/
├── README.md             ← you are here
├── REFERENCES.md         ← useful references, verified
├── activity/             ← the hands-on guide, records, extraction form, scoring scripts
│   ├── README.md
│   ├── data/             ← screening_records.csv, extraction_form.csv
│   ├── answers/          ← reference answers: open only when you score
│   ├── facilitator_guide.md ← for facilitators: contains answers, read after step 3
│   └── tools/            ← score_screening.py, score_extraction.py
├── beginners/            ← AI beginners track (for learning only)
├── prompts/              ← prompt library for chat assistants, by review stage
├── skills/               ← catalogue of the agent skills, external collections (EXTERNAL.md), attribution
├── .claude/skills/       ← the Claude Code skills (auto-loaded)
├── AGENTS.md, CLAUDE.md  ← rules for any coding agent opened here
├── docs/                 ← website: landing page, records page, scorer, references (GitHub Pages)
├── assets/               ← figures (and the script that builds them), buttons, logos, screenshots
└── LICENSE, LICENSE-CODE, CITATION.cff
```

The figures are built from the repository files by `python3 assets/figures/build_figures.py`, so the numbers they show are counted, not typed; `python3 docs/sync_data.py` then copies them into the website.
</details>

## Useful references

Five starting points; the [full list](REFERENCES.md) has 25 references checked on PubMed and Crossref, each introduced by its design and sample before what it found.

- **Flemyng et al., *Campbell Syst Rev* 2025.** Joint position statement of Cochrane, the Campbell Collaboration, JBI and the Collaboration for Environmental Evidence: reviewers stay responsible, AI is used with human oversight and reported. [doi:10.1002/cl2.70074](https://doi.org/10.1002/cl2.70074)
- **Fleurence et al., *Value Health* 2026.** ISPOR task-force good-practices report built on 115 empirical studies and expert consensus: AI inside human-in-the-loop workflows, not autonomous reviews. [doi:10.1016/j.jval.2026.08.007](https://doi.org/10.1016/j.jval.2026.08.007)
- **Adam et al., *Res Synth Methods* 2026.** Living rapid review of 134 studies of AI tools for evidence synthesis; the authors conclude that no existing tool can replace human expertise. [doi:10.1017/rsm.2026.10118](https://doi.org/10.1017/rsm.2026.10118)
- **Gartlehner et al., *Ann Intern Med* 2025.** Study within 6 ongoing systematic reviews comparing extraction by Claude, verified by a human, with human-only extraction. [doi:10.7326/ANNALS-25-00739](https://doi.org/10.7326/ANNALS-25-00739)
- **Qazi et al., *NEJM AI* 2026.** Randomised trial with 44 physicians trained in AI literacy: erroneous ChatGPT-4o suggestions lowered their diagnostic accuracy. Literacy is necessary, not sufficient. [doi:10.1056/AIoa2501001](https://doi.org/10.1056/AIoa2501001)

<p><a href="REFERENCES.md"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/buttons/references-dark.svg"><img src="assets/buttons/references-light.svg" width="49%" alt="Useful references: guidance and evidence"></picture></a></p>

## About this repository

| | |
|---|---|
| **What** | Teaching materials (activity guide, data, prompts, agent skills, scorers, website) for the skills building seminar M.8 *"Building skills in using AI tools to support evidence reviews for effective public health strategies"* |
| **Event** | European Public Health Conference 2026 (EPH 2026), Bilbao, Thursday 12 November 2026, 16:45-17:45 |
| **Made by** | The EUPHA Digital Health and Artificial Intelligence Section and Francesco Baglivo (University of Pisa), with the organisers and speakers below |
| **Builds on** | A previous EUPHA DHAI workshop (annual meeting, Berlin, 10 September 2026) and its participants' feedback, which shaped the ready-made prompts, the time to verify and the rule to turn off web search |
| **Status** | Kept online for self-paced practice. Teaching material, not a validated method; the reference review was confirmed on 6 November 2026 ([why and limits](activity/data/README.md)) |
| **Last updated** | 3 November 2026 (version 2026.11) |
| **Cite** | [How to cite](#how-to-cite), or the [`CITATION.cff`](CITATION.cff) file |
| **Licence** | Content CC BY 4.0, code MIT, logos excluded: [Licences](#licences) |
| **Contact** | [euphadhai@gmail.com](mailto:euphadhai@gmail.com), or [open an issue](https://github.com/fraba94/eph2026-ai-for-evidence-synthesis/issues/new/choose) |

## Organisers and speakers

Organised by the **EUPHA Digital Health and Artificial Intelligence (DHAI) Section** with **Concordia University** (Canada), the **Leibniz ScienceCampus Digital Public Health Bremen** (Germany) and the **Italian Society for AI in Medicine (SIIAM)**.

| Role | Person |
|---|---|
| Chair and contact | **Laura Maaß**, SOCIUM, University of Bremen; EUPHA |
| Co-chair | **Simon Bacon**, Concordia University |
| Speaker, limitations | **Patrick Boudreau**, Montreal Behavioural Medicine Centre, Concordia University |
| Speaker, benefits | **Francesco Baglivo**, University of Pisa |
| Demo video (16:55-17:05), commented live | **Francesco Baglivo** (narrates) and **Patrick Boudreau** (speaks for the verifier); the live demo in four hands is the fallback |

<p align="center"><a href="https://eupha.org/digital-health" title="EUPHA Digital Health and AI section"><img src="assets/logos/eupha-dhai.png" height="56" alt="EUPHA Digital Health and AI section"></a>&nbsp;&nbsp; <a href="https://www.concordia.ca" title="Concordia University"><img src="assets/logos/concordia.png" height="44" alt="Concordia University"></a>&nbsp;&nbsp; <a href="https://www.lsc-digital-public-health.de" title="Leibniz ScienceCampus Digital Public Health Bremen"><img src="assets/logos/lsc-diph.png" height="44" alt="Leibniz ScienceCampus Digital Public Health Bremen"></a>&nbsp;&nbsp; <a href="https://www.siiam.it" title="SIIAM"><img src="assets/logos/siiam.png" height="44" alt="SIIAM"></a>&nbsp;&nbsp; <a href="https://www.unipi.it" title="University of Pisa"><img src="assets/logos/unipi.png" height="44" alt="University of Pisa"></a>&nbsp;&nbsp;</p>

Abstract: *Eur J Public Health* 2026;36(Suppl 5):ckag169.470, [on the journal website](https://academic.oup.com/eurpub/article/36/Supplement_5/ckag169.470/8995443).

## How to cite

Use the **Cite this repository** button on GitHub, which reads [`CITATION.cff`](CITATION.cff), or:

> EUPHA Digital Health and Artificial Intelligence Section, Baglivo F. *AI for evidence synthesis: materials for the EPH 2026 skills building seminar M.8.* 2026. https://github.com/fraba94/eph2026-ai-for-evidence-synthesis

## Licences

<details>
<summary>Content CC BY 4.0, code MIT, with exceptions</summary>

- **Content** (texts, prompts, skills, guides, diagrams): [Creative Commons Attribution 4.0 International](LICENSE) (CC BY 4.0).
- **Code** (`.py`, `.js`, `.html`, `.css` files, including the scripts in `.claude/skills/` and `assets/figures/build_figures.py`): [MIT](LICENSE-CODE).
- **Not covered:** the logos of the EUPHA Digital Health and Artificial Intelligence Section, Concordia University, the Leibniz ScienceCampus Digital Public Health Bremen, SIIAM and the University of Pisa (`assets/eupha-dhai-logo.png`, `assets/logos/`, their copies in `docs/assets/`, and `assets/social-preview.png`), used only to identify the organisers and the speakers' institutions, which may not be reused without their owners' permission; bibliographic records, abstracts and articles of third parties, which keep their own licences and copyright (see the `license` column of the data files).
</details>

## Contact

EUPHA Digital Health and Artificial Intelligence Section: [euphadhai@gmail.com](mailto:euphadhai@gmail.com). Problems with the materials or a prompt to share: [open an issue](https://github.com/fraba94/eph2026-ai-for-evidence-synthesis/issues/new/choose).
