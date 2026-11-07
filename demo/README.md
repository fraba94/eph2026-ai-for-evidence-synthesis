# The demo video: one repository, your AI, your way

A silent video of 1:40, 1280×720, with captions burned in. Its message: **the repository holds the materials. Bring
your own AI. Work your way. Then check it against the human review.** It shows two routes to bring the same materials
to an AI (Route 1 on a phone, Route 2 on a laptop), then the checks that follow whatever the route. It is the demo of the EPH 2026 seminar M.8 (Bilbao,
12 November 2026, 16:55-17:05), commented live in the room; the live demo in four hands is the fallback (see the
[facilitator guide](../activity/facilitator_guide.md#demo-script)).

- Watch it on the [Start page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/start.html#demo) or in the
  [activity guide](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/activity.html#the-demo).
- Files: [`docs/assets/demo/demo.mp4`](../docs/assets/demo/demo.mp4) (H.264), the poster
  [`demo_poster.png`](../docs/assets/demo/demo_poster.png) and the captions as text,
  [`demo.vtt`](../docs/assets/demo/demo.vtt) (WebVTT, the same captions as in the video).

**Demo material, not yours.** The video uses records **batch 3 (R041-R060)** and the paper **Mestre2012**. In the
exercise you do the same on **batch 1 (R001-R020)** and **Phan2020**: none of their answers is shown. The scorer's
list of records not screened marks the batch 1 reference answers, so that line is covered in the video.

## What the video shows, and what is real in it

| Time | Scene | Caption(s) | What is real |
|---|---|---|---|
| 0:00 | Title card | The repository holds the materials. Bring your own AI. | |
| 0:11 | The repository | Everything you need is here. Use it with any AI. / Data, prompts, agent instructions, website: the same materials. | The repository page on github.com, as it is |
| 0:21 | Pick one of two routes | Pick one of two routes. Any generative AI. | |
| 0:26 | **Route 1 · Phone · copy and paste** (any AI chat app; for demonstration and learning only) | Tap once: the prompt and the 20 records are copied. / Paste it into your AI app: temporary chat, web search off. / The AI answers: check 20 records in, 20 rows out. | The live Start page in a 390 px wide phone window, with its one-tap button **Copy prompt + 20 records** (shown with `?batch=3`, the demo batch; the video reads the clipboard to check that it holds the prompt and 20 records). The AI's answer is the real answer of an AI chat assistant (below), on a neutral panel that imitates no chat product |
| 0:49 | **Route 2 · Laptop · connect an agent** (Claude Code, Codex CLI, Gemini CLI, Cursor…) | Clone it: the agent reads AGENTS.md and the skills. / A real agent run: two screenings, then compared. / Runs agree on 19 of 20; a human resolves R044. | The commands and their output come from the log of a real run (below), abridged with "…", never edited. The first lines (the `git clone` and the request in plain words) are labelled as an example of what you type |
| 1:07 | **Whatever the route: check it** | Paste the AI's decisions into the scorer: coverage first. / 0 missed includes; open the flagged records yourself. / Then find the AI's quote in the paper, word for word. / Found. But the value's "3 days every 3 weeks" is in Table 1. | The live scorer, with the Route 1 answer pasted; the Mestre2012 full text on the site, with a quote of the chat assistant's extraction and the sentence of Table 1 highlighted |
| 1:32 | Your turn | Your turn: batch 1 and Phan2020. Your AI, your way. | The closing card shows the two routes and "Start page: QR on the slide" |

## The real AI runs

**Route 1, AI chat assistant** (also used in the final check):

- **Tool:** an AI chat assistant (Claude), as a participant would use it. **Date:** 6 November 2026. **Settings:** a
  new temporary chat, **web search off**.
- **Prompts:** copied from the site, unchanged: the screening prompt of the Start page (criteria C1-C6 pasted in)
  followed by batch 3 from the Records page (the answer was recorded before the one-tap button existed; the button gives the same text in one copy); for the extraction, **Copy prompt + this paper** on the Mestre2012 card of
  the Papers page (the 5 fields of the short extraction and the full text, CC BY 4.0). No answer key was consulted.
- Files: [`screening_answer_batch3.csv`](screening_answer_batch3.csv) and
  [`extraction_answer_Mestre2012.csv`](extraction_answer_Mestre2012.csv), the CSV blocks of the two answers copied
  verbatim (only the code fences and, in the screening answer, the line `Records received: 20. Rows returned: 20.` were
  removed). Scores: [`screening_score_batch3.md`](screening_score_batch3.md) (`score_screening.py` against the
  reference decisions for R041-R060 only, so that the report names no batch 1 answer),
  [`extraction_score_Mestre2012.md`](extraction_score_Mestre2012.md) (`score_extraction.py`, the 5 short fields) and
  [`quote_verification_Mestre2012.csv`](quote_verification_Mestre2012.csv) (`verify_quotes.py`: 6 of 6 quotes verbatim;
  the two intervention-components rows hold numbers that are not in their quote).

**Route 2, AI coding agent** (folder [`agent_route/`](agent_route/)):

- **Tool:** an AI coding agent (Claude Code) on a fresh clone of this repository (commit 5d3430a), 6 November 2026,
  **no web search and no web fetch**; it followed `AGENTS.md` and the skills `title-abstract-screening`,
  `full-text-extraction` and `quote-verifier`, and did not open `activity/answers/` or run the scorers.
- [`agent_route/log.md`](agent_route/log.md): every command it ran and its full output. One change in this copy: the
  model identifier in the header line was removed, because this repository names no model versions. Nothing else was
  changed.
- [`screening_run1.csv`](agent_route/screening_run1.csv), [`screening_run2.csv`](agent_route/screening_run2.csv),
  [`screening_merged.csv`](agent_route/screening_merged.csv): two screening passes and their conservative merge
  (`compare_runs.py`: raw agreement 19/20, Cohen's kappa 0.90, PABAK 0.92; merged 4 include, 13 exclude, 3 unsure; the
  one disagreement, R044, became unsure). **Run 2 is a second pass by the same model in the same session** (records in
  reverse order, run 1 not reopened), **not an independent reviewer**: two runs of one model share blind spots, as the
  log says.
- [`extraction.csv`](agent_route/extraction.csv) and [`verification.csv`](agent_route/verification.csv): the short
  extraction of Mestre2012 (5 fields) and the quote check (5 of 5 quotes found, with the agent's semantic-check columns).
  One AI pass, no second extractor.
- Not copied: the records files with the abstracts the agent fetched from PubMed (publisher copyright) and its helper
  script. The copied files were checked for abstract text: none.

## How it was made

Recorded with Playwright (`recordVideo`, Chromium, 1280×720) on a local copy of the website (the version with the one-tap buttons) and on github.com: the captions,
the route label, the cursor dot, the yellow outlines and highlights and a 1.2× zoom of the website pages were
injected into the page; Route 1 is shown in a phone frame (an iframe 390 px wide); the AI answer and the agent's terminal output were shown on neutral local pages that imitate
no product. Encoded with ffmpeg (H.264, CRF 28, yuv420p, faststart).

*For learning only.* One run of each tool on 20 records and one paper says nothing about how good a tool is.
