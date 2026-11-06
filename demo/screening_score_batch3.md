# Screening score: screening_answer_batch3.csv

Reference standard: `activity/answers/screening_gold.csv`, rows R041-R060 only (batch 3) (20 records, 3 includes). 'unsure' counted as **include**.

## Coverage

Screened 20 of 20 records (0 not screened).

## Confusion matrix

| | Reference: include | Reference: exclude |
|---|---:|---:|
| **Decision: include** | 3 (true include) | 4 (false include) |
| **Decision: exclude** | 0 (MISSED include) | 13 (true exclude) |

## Metrics

| Metric | Value | Meaning |
|---|---:|---|
| Records scored | 20 of 20 | records with a valid decision |
| Sensitivity (recall) | 100.0% | share of the review's includes that you kept: the key metric at this stage |
| Specificity | 76.5% | share of the excludes that you excluded |
| Precision (PPV) | 42.9% | share of your includes that the review included |
| NPV | 100.0% | share of your excludes that the review excluded |
| Accuracy | 80.0% | (misleading when includes are few) |
| F1 | 60.0% | harmonic mean of recall and precision |
| WSS at achieved recall | 65.0% | work saved over sampling = (TN+FN)/N - (1 - recall) |
| WSS@95 | 60.0% | recall >= 95%, so WSS@95 = (TN+FN)/N - 0.05 |
| Unsure | 3 | counted as include; listed below |

### Title/abstract-stage view

7 records were excluded by the review only after reading the full text, so they passed its title/abstract stage. Counting them as 'include' gives a fairer picture of title/abstract screening:

| | value |
|---|---:|
| Sensitivity (stage view) | 70.0% (7/10) |
| Specificity (stage view) | 100.0% (10/10) |
| Precision (stage view) | 100.0% |

## False includes (4)

| record | title | decision | reference | your reason | reference basis |
|---|---|---|---|---|---|
| R044 | Hand Hygiene and Hospital-Acquired Infections During COVID-19 Increased Vigilance: One Hospital's Experience. | unsure | exclude | C3 unclear: hospital-wide COVID-19 infection control measures, not a defined multimodal ha | excluded by the reference review after full-text assessment (cited among its full-text exclusions; it passed the review' |
| R050 | The effect of hand hygiene compliance on hospital-acquired infections in an ICU setting in a Kuwaiti teaching  | unsure | exclude | C2 unclear: campaign described as hospital-wide, but implementation focus and HAI outcomes | excluded by the reference review after full-text assessment (cited among its full-text exclusions; it passed the review' |
| R058 | Minimal intervention for controlling nosocomial transmission of methicillin-resistant staphylococcus aureus in | include | exclude | C1-C6 not contradicted: hospital-wide hand hygiene campaign phase evaluated by interrupted | excluded by the reference review after full-text assessment (cited among its full-text exclusions; it passed the review' |
| R059 | Improving hand hygiene adherence among nursing staff. | unsure | exclude | C1/C2 unclear: setting and scope not reported; quasi-experimental education plus reinforce | excluded by the reference review after full-text assessment (cited among its full-text exclusions; it passed the review' |

## Unsure (3) - counted as include

| record | title | decision | reference | your reason | reference basis |
|---|---|---|---|---|---|
| R044 | Hand Hygiene and Hospital-Acquired Infections During COVID-19 Increased Vigilance: One Hospital's Experience. | unsure | exclude | C3 unclear: hospital-wide COVID-19 infection control measures, not a defined multimodal ha | excluded by the reference review after full-text assessment (cited among its full-text exclusions; it passed the review' |
| R050 | The effect of hand hygiene compliance on hospital-acquired infections in an ICU setting in a Kuwaiti teaching  | unsure | exclude | C2 unclear: campaign described as hospital-wide, but implementation focus and HAI outcomes | excluded by the reference review after full-text assessment (cited among its full-text exclusions; it passed the review' |
| R059 | Improving hand hygiene adherence among nursing staff. | unsure | exclude | C1/C2 unclear: setting and scope not reported; quasi-experimental education plus reinforce | excluded by the reference review after full-text assessment (cited among its full-text exclusions; it passed the review' |

Interpretation: at title/abstract stage a missed include is far more costly than a false include. The reference is the review's FINAL inclusion (after full text), so records it excluded at full text are legitimate includes at this stage: read the 'reference basis' before calling a false include an error.
