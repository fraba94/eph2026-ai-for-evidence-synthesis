# Extraction score: extraction_answer_Mestre2012.csv

Reference: `activity/answers/extraction_gold.csv` (values prepared by the workshop team from the full texts, cross-checked with the reference review's own tables: column 'review table'). Studies scored: Mestre2012

## Summary

| Agreement with the reference | n |
|---|---:|
| exact | 3 |
| text match | 1 |
| partial | 1 |
| **agreement (exact + within tol. + text match)** | **4/5** |
| agreement among the fields you extracted | 4/5 |

| Quote check against the full text | n |
|---|---:|
| quote found | 4 |
| quote found, number not in quote | 1 |

## Per field

| field | type | exact | within tol. | text match | partial | mismatch | missing | false absent | unsupported |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| country | text | 1 |  |  |  |  |  |  |  |
| study_design | categorical | 1 |  |  |  |  |  |  |  |
| intervention_components | list |  |  |  | 1 |  |  |  |  |
| primary_hai_outcome | text |  |  | 1 |  |  |  |  |  |
| direction_of_effect | categorical | 1 |  |  |  |  |  |  |  |

## Details (everything that is not an exact match, plus every quote problem)

| study | field | your value | reference value | agreement | quote check | review table | note |
|---|---|---|---|---|---|---|---|
| Mestre2012 | intervention_components | Phase 2 (January–December 2011, added to phase 1): alcohol-based hand rub at point of car… | education/training; alcohol-based hand rub at point of care; reminders/posters; audit and… | partial | quote found, number not in quote | WHO multimodal hand hygiene strategy followed by a continuous quality… |  |
| Mestre2012 | primary_hai_outcome | healthcare-acquired colonisation/infection due to methicillin-resistant Staphylococcus au… | healthcare-acquired MRSA colonisation/infection rate | text match | quote found | Healthcare-acquired MRSA colonization/infection rate | A SECONDARY outcome of the study: its primary outcome is hand hygiene compliance. |

## Problems

- duplicated study/field rows (last kept): Mestre2012/intervention_components

How to read this: 'QUOTE NOT FOUND' means the quote is not in the paper as written (paraphrased, merged from two places, or invented): treat the value as unverified. 'unsupported' means a value where the paper reports nothing: the typical sign of inference or hallucination. 'false absent' means the information was there but was reported as missing (often a retrieval or parsing failure, e.g. a table). Check the notes column: several reference values are themselves ambiguous because the papers contradict themselves, and the review table sometimes differs from the paper.
