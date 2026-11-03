# Synthetic sample data (for testing the scorer only)

These files are **invented**, are not taken from any study, and exist only so that `docs/scorer.html` can be tried
before the real workshop data are copied into `docs/data/` (see `docs/README.md`). Open the scorer with
`?sample=1` (for example `scorer.html?sample=1`) to load them. They follow the exact formats of the workshop files:

| File | Format |
|---|---|
| `screening_records.csv` | `record_id,pmid,doi,title,abstract,year,journal,license` |
| `screening_gold.csv` | `record_id,gold_decision,gold_basis` |
| `decisions_example.csv`, `decisions_example_run2.csv` | `record_id,decision,reason` |
| `extraction_form.csv` | `field,definition,allowed_values,type` |
| `extraction_gold.csv` | `study_id,field,value,source_quote,location` |
| `extraction_example.csv` | `study_id,field,value,source_quote,location` |
