# The demo video

A silent video, about 5 minutes (4:52), 1280×720, with captions burned in: the three steps of the exercise done
once on demo material, with **real AI answers** and a human who checks every answer against the source. It is the
demo of the EPH 2026 seminar M.8 (Bilbao, 12 November 2026, 16:55-17:05), commented live in the room: Francesco
Baglivo narrates, Patrick Boudreau speaks for the verifier. The live demo in four hands is the fallback (see the
[facilitator guide](../activity/facilitator_guide.md#demo-script)).

- Watch it on the [Start page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/start.html#demo) or in the
  [activity guide](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/activity.html#the-demo).
- Files: [`docs/assets/demo/demo.mp4`](../docs/assets/demo/demo.mp4) (H.264), the poster
  [`demo_poster.png`](../docs/assets/demo/demo_poster.png) and the captions as text,
  [`demo.vtt`](../docs/assets/demo/demo.vtt) (WebVTT, the same captions as in the video, with the step of each one).

**Demo material, not yours.** The video uses records **batch 3 (R041-R060)** and the paper **Mestre2012**. In the
exercise you do the same steps on **batch 1 (R001-R020)** and **Phan2020**: nothing of your material, and none of its
answers, is shown. The scorer's list of records not screened marks the batch 1 reference answers, so that line is
covered in the video.

## How the AI answers were produced

- **Tool:** an AI chat assistant (Claude), a general-purpose assistant, as a participant would use it.
- **Date:** 6 November 2026. **Settings:** a new temporary chat, **web search off**, no files or project knowledge.
- **Prompts:** copied from the live site, unchanged: the screening prompt of the
  [Start page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/start.html#step-1-screening) (criteria C1-C6
  pasted in) followed by batch 3 as copied from the
  [Records page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/batch.html) (abstracts fetched from PubMed);
  for the extraction, **Copy prompt + this paper** on the Mestre2012 card of the
  [Papers page](https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/papers.html#Mestre2012) (the 5 fields of the
  short extraction and the full text, CC BY 4.0).
- **No answer key** was consulted to produce the answers. One run each; no second run.
- **Shown unedited.** The video shows each answer exactly as returned. The CSV files here are the CSV blocks of the two
  answers, copied verbatim; only the code fences (```` ```csv ````) were removed, and in the screening answer the
  line written after the CSV, `Records received: 20. Rows returned: 20.`
- The batch text and the extraction prompt with the paper are not stored here: the abstracts are copyrighted, and the
  prompt and the paper are on the site.

## Files in this folder

| File | What it is |
|---|---|
| [`screening_answer_batch3.csv`](screening_answer_batch3.csv) | The AI's screening decisions for R041-R060 (`record_id,decision,reason`), as returned |
| [`screening_score_batch3.md`](screening_score_batch3.md) | `activity/tools/score_screening.py` on that answer, against the reference decisions for R041-R060 only (so that the report does not name batch 1 answers; the metrics are those the web scorer shows) |
| [`extraction_answer_Mestre2012.csv`](extraction_answer_Mestre2012.csv) | The AI's short extraction of Mestre2012 (`study_id,field,value,source_quote,location`), as returned: 6 rows, intervention components in two rows, one per phase |
| [`extraction_score_Mestre2012.md`](extraction_score_Mestre2012.md) | `activity/tools/score_extraction.py` on that answer, the 5 fields of the short extraction (the scorer keeps the last of the two intervention-components rows) |
| [`quote_verification_Mestre2012.csv`](quote_verification_Mestre2012.csv) | `.claude/skills/quote-verifier/scripts/verify_quotes.py` against the full text: every quote found verbatim; the two intervention-components rows hold numbers that are not in their quote |

## What the video shows

The step names and numbers are those of the Start page. Each caption names the button to press.

| Time | Scene | What it shows |
|---|---|---|
| 0:00 | Title and the three steps | Batch 3 and Mestre2012, not your material; real AI answers. You will do the same on batch 1 and Phan2020 |
| 0:18 | Step 1 · Screening · 1/4 | Start page, **Open the records**, batch **41-60**, wait for "20 records ready" (abstracts from PubMed), **Copy batch** |
| 0:43 | Step 1 · 2/4 | **Copy the screening prompt**, **Show the screening prompt**: criteria C1-C6 already in it |
| 0:58 | Step 1 · 3/4 | Paste the prompt, then the records where it says `[PASTE THE RECORDS HERE]`, in a new temporary chat, web search off. The AI's answer, unedited: check the count first, 20 records in, 20 rows out |
| 1:26 | Step 1 · 4/4 | Scorer: paste the whole answer, **Score my screening**. Coverage 20 of 60 (one batch); sensitivity 100%, 0 missed includes; 4 false includes. Recap card |
| 1:50 | Step 2 · Look at the errors · 1/3 | The 4 false includes (R044, R050, R058, R059) were all excluded by the review only after reading the full text: not errors at this stage. **Going further**, title/abstract-stage view: 70% (7/10); the AI excluded R043, R046 and R054, which the human screeners had sent to full text (all three excluded in the end) |
| 2:25 | Step 2 · 2/3 and 3/3 | Open 2 of them on the Records page, the sentences highlighted. **R050** (AI: unsure, C2): a hospital-wide campaign, but infections measured only in the ICU; "unsure" was fair. **R058** (AI: include, "check C3"): a hospital-wide campaign whose components are not described, then contact precautions and chlorhexidine bathing; C3 is in doubt, so "unsure" fits the prompt better. Either way both go to full text, where the review excluded them. Recap card |
| 3:28 | Step 3 · Short extraction · 1/3 | Papers page, Mestre2012, **Copy prompt + this paper**; paste into a new temporary chat, web search off |
| 3:44 | Step 3 · 2/3 | The AI's answer, unedited: every value with a quote and its location; intervention components in two rows, one per phase, as the prompt allows |
| 4:01 | Step 3 · 3/3 | **Show text**, find 2 quotes. **Quote 1**, country = Spain: found word for word, in the authors' affiliations, labelled "author affiliations" as the form allows. **Quote 2**, intervention components of phase 2: found word for word, but "3 days every 3 weeks" in the value is not in the quote; it is in Methods, a few lines up. The quote-check script agrees: 6 of 6 quotes verbatim. Recap card |
| 4:43 | Your turn | The three steps on batch 1 and Phan2020, 30 minutes; scan the QR on the slide or open the Start page. AI drafts. You check. You decide |

## How it was made

Recorded on the live site with Playwright (`recordVideo`, Chromium, 1280×720): the captions, the step counter, the
cursor dot, the yellow highlights and a 1.2× zoom of the site pages (for a projector) were injected into the page;
the AI answers were shown as plain text on a neutral page that imitates no chat product. Encoded with ffmpeg (H.264,
CRF 28, yuv420p, faststart). The highlights mark sentences of the real abstract or paper on the site; nothing else
on the pages was changed.

*For learning only.* One run of one assistant on 20 records and one paper says nothing about how good a tool is.
