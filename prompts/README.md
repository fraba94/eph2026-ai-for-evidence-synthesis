# Prompt library for evidence reviews

Copy-paste prompts for any chat assistant (ChatGPT, Claude, Gemini, Copilot, Mistral, Le Chat, ...), organised by review stage. They are the chat version of the [agent skills](../skills/README.md): same method, no installation.

> ⚠️ **For learning only.** These prompts are teaching material for this workshop. They are not a validated method.
> If you are not confident with how large language models work (context windows, parsing, sampling, retrieval,
> hallucination) and with advanced techniques (structured outputs, verification against the source, reproducibility
> checks, documentation of model and version), **do not use AI to conduct a real evidence review.** You stay
> responsible for every decision: the AI does not.

## Index

| Stage | File | Prompts |
|---|---|---|
| 1. Question and criteria | [01_question_and_criteria.md](01_question_and_criteria.md) | 1.1 Question to PICO/PECO · 1.2 Criteria stress test · 1.3 Borderline cases |
| 2. Search | [02_search.md](02_search.md) | 2.1 Draft concept blocks · 2.2 Break my search (critique mode) · 2.3 Translate between databases |
| 3. Screening | [03_screening.md](03_screening.md) | 3.1 Screen a batch (CSV output) · 3.2 Second independent run · 3.3 Explain disagreements |
| 4. Extraction | [04_extraction.md](04_extraction.md) | 4.1 Design the form first · 4.2 Extract with quotes · 4.3 Table check |
| 5. Verification | [05_verification.md](05_verification.md) | 5.1 Quote check · 5.2 "Not reported" check · 5.3 Compare two runs |
| 6. Synthesis and reporting | [06_synthesis_and_reporting.md](06_synthesis_and_reporting.md) | 6.1 Evidence table to narrative (with limits) · 6.2 Discrepancy summary · 6.3 AI-use statement |

Every prompt has: purpose, when to use it, the copyable prompt with `[PLACEHOLDERS]`, the expected output, what to check afterwards, and common failure modes.

## Prompting patterns

These patterns appear in every prompt. Knowing *why* they work matters more than the exact wording.

| Pattern | What to do | Why |
|---|---|---|
| **Role + task + criteria + output format** | State who the model should act as, the single task, the explicit criteria, and the exact output | Missing criteria get filled with the model's own, differently every run |
| **Structured output** | Ask for a table, CSV or JSON with fixed columns; one row per record | You can paste it into a spreadsheet, count rows, and compare runs mechanically |
| **Ask for quotes** | Every decision or value with a verbatim quote and its location | Turns "trust me" into "check me"; unsupported values become visible |
| **Allow "not reported" / "unsure"** | Say explicitly that these answers are allowed and preferred to guessing | The model always produces *some* answer; give it a safe one |
| **Critique mode** | "Do not rewrite it. Find how it could fail. Rank the three biggest risks." | Asking to *improve* yields confident rewrites; asking to *break* yields checkable problems |
| **Run twice** | Same prompt, new conversation; compare | Outputs are sampled: a result you cannot reproduce is not a method |
| **Temperature and consistency** | In chat apps you usually cannot set temperature: compensate with fixed formats, explicit rules and two runs. Via API, use a low temperature for screening and extraction, and record it | Lower randomness reduces, but does not remove, run-to-run variation |
| **Chunking** | 10–20 abstracts per message; one full-text paper per conversation | Long inputs degrade attention; batches keep counts checkable |
| **Context window position** | Put instructions first and repeat the key rules at the end; do not bury the paper in the middle of a long chat | Models use information at the start and end of a long input better than in the middle (Liu et al., TACL 2024, doi:[10.1162/tacl_a_00638](https://doi.org/10.1162/tacl_a_00638)) |
| **Fresh conversation per task** | New chat for each task or paper | Earlier text keeps influencing later answers; memory features add hidden context |
| **No retrieval for form filling** | Paste or upload the whole paper; avoid "chat with your folder" tools for extraction | When a retrieved chunk misses the answer, the model reports the information as absent |
| **Document as you go** | Note tool, model/version as displayed, date, prompt, and what you checked | You will need it for the AI-use statement (prompt 6.3) |

## Four ideas behind all of this

What happens between your document and the answer: **parsing → tokens → context window → sampling.**

1. **Parsing**: the model never sees your PDF, only the text a parser extracted. Scrambled tables give scrambled numbers.
2. **Tokens**: text is cut into sub-word pieces; this is what the model reads and what limits how much fits.
3. **Context window**: one working memory of finite size and uneven attention, shared by your instructions, the documents and the whole conversation.
4. **Sampling**: the answer is generated one token at a time. There is no lookup that visibly fails, so a fluent answer is produced either way. Fluency tells you nothing about correctness.

## Guidance

- Position statement on AI use in evidence synthesis (Cochrane, Campbell, JBI, CEE; 2025): evidence synthesists remain responsible; AI with human oversight; AI that makes or suggests judgements must be reported. doi:[10.1186/s13750-025-00374-5](https://doi.org/10.1186/s13750-025-00374-5)
- RAISE recommendations: <https://osf.io/fwaud/>
- Cochrane Handbook, [Chapter 4](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04) (searching and selecting) and [Chapter 5](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-05) (collecting data).

> [!CAUTION]
> Never paste personal, patient-level or confidential data into a chat assistant your institution has not approved. Check the licence of a PDF before uploading it.
