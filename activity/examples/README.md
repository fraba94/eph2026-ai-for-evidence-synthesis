# Example files (fake, for trying the scorers)

These files are **invented** outputs that imitate typical AI mistakes. Use them to see what the scorers report
before you score your own work. They are not answers.

| File | Imitates |
|---|---|
| `decisions_example.csv` | a screening run (`record_id,decision,reason`) with two missed includes, some false includes, "unsure" records and one record silently dropped |
| `decisions_example_run2.csv` | a second run of the same prompt, with some decisions changed (reproducibility) |
| `extraction_example.csv` | an extraction (`study_id,field,value,source_quote,location`) with an invented quote, an inferred country, a value read from a table that differs from the text, a "not reported" that is reported, and a correlation given as effect estimate |

```bash
python3 activity/tools/score_screening.py activity/examples/decisions_example.csv --compare activity/examples/decisions_example_run2.csv
python3 activity/tools/score_extraction.py activity/examples/extraction_example.csv
```

(For the quote check of `AlKuwaiti2017`, first run `python3 activity/tools/fetch_fulltext.py`.)
