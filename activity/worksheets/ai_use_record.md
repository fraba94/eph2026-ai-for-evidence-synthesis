# AI use record

A record of how AI was used in your run of the exercise, so that someone else could repeat it and judge it. The items
follow the reporting expected by the RAISE recommendations (Responsible use of AI in evidence SynthEsis,
https://osf.io/fwaud/) and the position statement on AI use in evidence synthesis by Cochrane, the Campbell
Collaboration, JBI and the Collaboration for Environmental Evidence (2025, doi:10.1186/s13750-025-00374-5): what was
used, for what, how, how it was checked, and its limits. In a real review this information belongs in the protocol and
in the methods section. The skill `.claude/skills/ai-use-reporting/` helps draft it.

**Group:** ............ **Recorder:** ............

## 1. Tool

| Item | Screening | Extraction |
|---|---|---|
| Tool / product (e.g. ChatGPT, Claude, Gemini, Copilot, Claude Code) | | |
| Model and version as shown by the tool | | |
| Date and time of use | | |
| Access (free, paid, institutional; web, app, API, agent) | | |
| Settings you could see or change (temperature, "thinking", web search on/off, memory on/off, project knowledge) | | |
| Files given to the tool (which records, which paper, format: CSV, text, PDF) | | |
| Data protection: was anything confidential or personal uploaded? Licence of the texts checked? | | |

## 2. Prompts

Paste the exact prompts, in order, including follow-ups and corrections. Note which ones were run in a new
conversation.

```text
Prompt 1:

Prompt 2:
```

## 3. Outputs

| Item | Screening | Extraction |
|---|---|---|
| File name of the raw output saved | | |
| Number of records/values requested vs returned | | |
| Was the output edited by hand before scoring? What? | | |
| Second run done? File name | | |

## 4. Human checks

| Check | Done? | What it found |
|---|---|---|
| Count of rows returned vs sent | | |
| Decisions checked against the abstract (how many?) | | |
| Quotes searched in the paper (how many? found?) | | |
| Numbers checked against tables | | |
| "Not reported" values checked by searching the paper | | |
| Two runs compared | | |

## 5. Performance against the reference

| Measure | Value |
|---|---|
| Screening sensitivity (recall) / specificity / precision | |
| Missed includes (record IDs) | |
| Extraction agreement (from `score_extraction.py` or the browser scorer) | |
| Quotes not found in the source | |
| Agreement between run 1 and run 2 (kappa or % agreement) | |

## 6. Limitations and judgement

- What would you **not** trust this tool to do without a human check?
- Would you use it in a real review? For which step, as first or second reviewer, and with which checks?
- What would you write in the methods section? (One paragraph.)
