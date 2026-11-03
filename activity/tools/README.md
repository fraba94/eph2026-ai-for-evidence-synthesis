# Tools (Python 3, standard library only)

Every script prints its full help with `--help`. Run them from the repository root.

| Script | For | What it does |
|---|---|---|
| `score_screening.py` | participants (step 3) | Scores `record_id,decision,reason` against the reference: confusion matrix, sensitivity, specificity, precision, WSS, missed includes, unsure, title/abstract-stage view; `--compare run2.csv` for reproducibility (kappa) |
| `score_extraction.py` | participants (step 3) | Scores `study_id,field,value,source_quote,location` per field (exact, within tolerance, text match, partial, mismatch, missing, false absent, unsupported) and checks every quote against the full text |
| `fetch_abstracts.py` | participants, facilitators | Fills empty abstracts from PubMed into a local, git-ignored copy |
| `fetch_fulltext.py` | participants, facilitators | Downloads the extraction papers from PMC and converts them to text (non-redistributable ones go to `activity/data/local/`) |
| `build_screening_set.py` | workshop team | Rebuilds the 60-record set and its gold standard from PMIDs (`answers/reference_key.yaml`), or from a review team's own screening export (`--from-export`) |
| `build_extraction_gold.py` | workshop team | `tables`: extracts the reference review's tables from PMC; `check`: verifies every gold quote against the full texts; `skeleton`: gold template for a new review |
| `pmc_to_text.py` | used by the others | Converts a PMC (JATS) XML article to plain text |
| `common.py` | used by the others | Shared helpers (CSV, small YAML reader, text normalisation, NCBI E-utilities) |

Network access is needed only for `fetch_*` and `build_*` (NCBI E-utilities, at most about 3 requests per second).
