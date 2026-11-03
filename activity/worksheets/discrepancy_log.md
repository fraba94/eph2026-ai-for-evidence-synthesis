# Discrepancy log

Fill this in step 3, for at least three discrepancies between the AI output and the reference. Check the **source**
(abstract or paper) before deciding who is right: the reference can be wrong too. A CSV version with the same columns
is in [`discrepancy_log.csv`](discrepancy_log.csv).

**Group:** ............ **Track:** chat / agent **Tool and model:** ............ **Date:** ............

| # | Task | Record or study / field | AI said | Reference says | Source says (quote, location) | Who is right? | Error type | Would a human reviewer have caught it? How? |
|---|---|---|---|---|---|---|---|---|
| 1 | screening / extraction | | | | | AI / reference / both / unclear | | |
| 2 | | | | | | | | |
| 3 | | | | | | | | |
| 4 | | | | | | | | |
| 5 | | | | | | | | |

## Error types

| Code | Error type | Example in this exercise |
|---|---|---|
| **MI** | Missed include (screening false negative) | a hospital-wide programme excluded because the abstract also mentions an ICU |
| **FI** | False include (screening false positive) | a single-NICU study, a randomised trial, a compliance-only study included |
| **CR** | Criterion misapplied | C3 applied to any multi-component infection-control bundle |
| **DR** | Dropped or renamed record | 19 rows returned for 20 records |
| **WV** | Wrong value | a number from the wrong period, subgroup or outcome |
| **HV** | Hallucinated or inferred value | a country, definition or confidence interval that the paper does not report |
| **QF** | Quote not in the source | paraphrased, merged from two places, or invented quote |
| **FA** | False absence ("not reported" but it is reported) | value only in a table or in another section |
| **PE** | Parsing error | table columns shifted, numbers from a figure axis, two-column layout mixed |
| **AM** | Ambiguous field or criterion | "post-intervention compliance": last period or whole intervention period? |
| **GE** | Error in the reference standard | the review's table differs from the paper, or an eligible study was not included |
| **RP** | Not reproducible | two runs of the same prompt disagree |

## Summary (2 lines)

- The most frequent error type in our run was: ............
- The check that caught most errors was: ............
