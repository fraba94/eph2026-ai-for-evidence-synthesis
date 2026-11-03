# AI-use record and reporting template

## 1. AI-use record (one row per task)

| Field | Entry |
|---|---|
| Review stage | e.g. title/abstract screening |
| Task delegated to AI | e.g. second reviewer: include/exclude/unsure with reasons |
| Tool, product and model version | exactly as displayed by the tool, e.g. product name + model identifier; `[TO CONFIRM]` if unknown |
| Access route | web chat / API / desktop agent / other; account type (institutional, personal) |
| Settings | temperature, file upload vs. retrieval, tools enabled, system prompt; "default" if not changed |
| Date(s) of use | YYYY-MM-DD |
| Input | which records/files, how many, licence of full texts uploaded |
| Prompt(s) | file name or appendix reference; prompts archived verbatim |
| Runs | number of runs; how run-to-run differences were handled |
| Human role | who checked, what proportion, blinded or not, how disagreements were resolved, who made final decisions |
| Performance observed | only figures actually computed (e.g. agreement with human decisions, recall of includes) with denominator; otherwise "not assessed" |
| Data protection | personal or confidential data? institutional approval? |
| Limitations | observed problems and known limitations |

## 2. Generic reporting template (protocol / methods)

The 2025 position statement says that decisions to use AI should be considered and reported as part of protocol development, and offers a generic reporting template. The text below is reproduced from the version quoted in the EUPHA DHAI Berlin workshop slides (10 September 2026), which cite the Cochrane editorial doi:10.1002/14651858.ED000178. Check it against the published statement before reusing it verbatim.

> We will use [AI system/tool/approach name, version, date] developed by [organization/developer] for [specific purpose(s)] in [the evidence synthesis process]. The [AI system/tool/approach] will [state it will be used according to the user guide, and include reference, and/or briefly describe any customization, training, or parameters to be applied]. Outputs from the [AI system/tool/approach] are justified for use in our synthesis because [describe how you have determined it is methodologically sound and will not undermine the trustworthiness or reliability of the synthesis or its conclusions and how it has been validated or calibrated to ensure that it is appropriate for use in the context of the specific evidence synthesis, if not covered in the user guide, evaluations or elsewhere]. Limitations [of the AI system/tool/approach] include [describe known limitations, potential biases, and ethical concerns]/[are included as a supplementary material]. [If applicable] A detailed description of the methodology, including parameters and validation procedures, is available in [supplementary materials].

## 3. Example for the workshop exercise (past tense, for a training report)

> During a training exercise we used [product, model identifier as displayed] ([access route]) on [date] to screen [N] titles and abstracts against pre-specified eligibility criteria, with the prompt reported in [appendix]. The AI output was compared with the decisions of a systematic review conducted without AI (Barbati et al., Artif Intell Med 2025;172:103321, doi:10.1016/j.artmed.2025.103321). [Observed agreement / missed includes, with denominators, from the scoring script.] All final decisions were made by the reviewers. Limitations include non-deterministic outputs (the second run differed on [n] records), [parsing / context issues observed], and the small, non-representative sample.

## 4. Archive checklist
- [ ] Prompts, verbatim, with dates
- [ ] Model / product / version as displayed
- [ ] Raw AI outputs (all runs)
- [ ] Final human decisions and who made them
- [ ] Comparison results (agreement, discrepancy log)
- [ ] Licence status of each uploaded full text
