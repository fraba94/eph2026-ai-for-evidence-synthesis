---
name: ai-use-reporting
description: Build the AI-use record of an evidence review (tool, version, date, purpose, stage, prompts, settings, human checks, performance against human decisions, limitations) and draft the protocol or methods paragraph declaring AI use, aligned with the Cochrane-Campbell-JBI-CEE 2025 position statement and the RAISE recommendations. Use when someone used or plans to use AI in a review, writes a protocol or methods section, asks "how do I report/declare/disclose AI use?", or at the end of the workshop exercise to document what was done.
argument-hint: "[folder with prompts/outputs or short description of AI use]"
---

# AI-use reporting

If AI made or suggested a judgement (eligibility, extraction, risk of bias, synthesis, certainty, summaries), it must be reported fully and transparently. A use you cannot describe precisely (which model, which version, which prompt, which checks) is a use you cannot defend.

## Human in the loop
- You draft from what the record shows; the authors confirm every statement. Never fill a gap with a plausible guess: write `[TO CONFIRM: ...]`.
- Never invent a version number, a date, a performance figure or a validation that was not done. If no comparison with human decisions exists, say so in the limitations.
- The authors decide where the paragraph goes (protocol, methods, supplement) following the journal's policy.

## Procedure

1. **Collect the evidence**: prompts used (verbatim), model and product names, version or model identifier as shown by the tool, access route (web chat, API, agent), settings if known (temperature, tools, retrieval/upload), dates of use, input files, output files, and any comparison with human decisions (e.g. output of `compare_runs.py`, `score_screening.py`, `score_extraction.py`, `discrepancy_log.csv`).
2. **Fill the AI-use record**, one row per task, with [references/ai_use_record_template.md](references/ai_use_record_template.md). Fields: stage, task, tool and version, date(s), what the AI did, what the humans did (who checked what, how much, how disagreements were resolved), performance observed, prompt location, data protection and licence notes, limitations.
3. **Check the declaration triggers** from the position statement (Table 1, "Report AI use..."): AI that makes or suggests judgements on eligibility, appraisal/risk of bias, extraction of bibliographic, numerical or qualitative data, synthesis, certainty of evidence, text on strength of evidence or implications, or plain-language summaries must be declared. Spelling/grammar help generally need not be listed, but check the journal policy.
4. **Draft the paragraph** from the template in the reference file, filling each bracket from the record. Keep it factual; no adjectives such as "robust" or "validated" unless a validation is documented.
5. **Draft the limitations sentence(s)**: model non-determinism (outputs may differ between runs), version drift, parsing of PDFs and tables, context-window limits, possible biases of the training data, and anything observed in your own comparison.
6. **List what must be archived** with the review: prompts, model/version, raw AI outputs, final human decisions, comparison results, dates.
7. **Stop** and give the human the record, the paragraph and the list of `[TO CONFIRM]` items.

## Output
- `ai_use_record.md` (table) and a paragraph ready for the protocol/methods, plus the limitations text and the archive checklist.

## Verified sources (checked on PubMed, November 2026)
- Flemyng E, Noel-Storr A, Macura B, et al. Position statement on artificial intelligence (AI) use in evidence synthesis across Cochrane, the Campbell Collaboration, JBI and the Collaboration for Environmental Evidence 2025. Published simultaneously in several journals, e.g. Environ Evid 2025;14(1):20, doi:10.1186/s13750-025-00374-5; Campbell Syst Rev 2025;21(4):e70074, doi:10.1002/cl2.70074; JBI Evid Synth 2025;23(11):2162-2166, doi:10.11124/JBIES-25-00480; Cochrane Database Syst Rev editorial, doi:10.1002/14651858.ED000178.
- Thomas J, et al. Responsible use of AI in evidence SynthEsis (RAISE): recommendations and guidance. OSF, https://osf.io/fwaud/ (three documents: RAISE 1 recommendations by role; RAISE 2 building and evaluating tools; RAISE 3 selecting and using tools). Always use the latest version.
- PRISMA 2020 includes items on reporting automation tools; follow the reporting guideline your journal uses.

## When NOT to use
- To make an AI use look more validated than it was. The record reports what happened, including failures.
- For journal-specific disclosure wording: check the journal's own policy, which overrides a generic template.
- As legal advice on data protection or copyright: ask your institution's data protection officer or library.
