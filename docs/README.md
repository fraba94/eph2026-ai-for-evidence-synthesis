# The workshop website (GitHub Pages)

This folder is a static website: plain HTML, CSS and JavaScript, no build step and no external scripts.
Published address once enabled: <https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/>

| Page | What it does |
|---|---|
| [`index.html`](index.html) | Landing page: the key message, the session, the two tracks, the review map, a prompt, references, organisers. Figures come from `assets/figures/` (built by `assets/figures/build_figures.py`) |
| [`batch.html`](batch.html) | **Records to screen**: the workshop records in batches of 10 or 20, copy-ready for a chat assistant. Empty abstracts are fetched from PubMed (NCBI E-utilities `efetch`) by the visitor's browser, by PMID, at most 20 per request, one request at a time, without an API key or an email address. Nothing is stored. |
| [`scorer.html`](scorer.html) | **Score your results**. Same rules and numbers as `activity/tools/score_screening.py` and `score_extraction.py`. Screening: metrics on the records in the uploaded file, coverage always shown ("Screened N of 60"), not-screened reference includes highlighted, sensitivity counting them as missed, a toggle "I was meant to screen all records" (= `--expect-all`), title/abstract-stage view, run-2 reproducibility with Cohen's kappa. Extraction: only the studies present in the file, optional core fields only, " OR " alternatives in reference values, false absent / unsupported values, human review of partial matches. The quote check against the full text is done only by the Python scorer. Runs in the browser; files are never uploaded. |
| [`references.html`](references.html) | **Useful references**: the list of [`REFERENCES.md`](../REFERENCES.md) with filters by type (guidance, evidence, context, human factors, tool, exercise) |
| [`slides/`](slides/README.md) | Abstract link; slides after the session |

## Enable GitHub Pages (once)

1. On GitHub: **Settings → Pages**.
2. **Build and deployment → Source: Deploy from a branch**.
3. **Branch: `main`**, folder **`/docs`**, then **Save**.
4. After a minute the site is live at the address above. The file `.nojekyll` tells GitHub to serve the
   files as they are (without it, folders starting with `_`, such as `data/_sample/`, would be dropped).

## Keep the data and images in sync

Pages publishes only `docs/`, so the site cannot read `../activity/` or `../assets/`. Copies live in
`docs/data/` and `docs/assets/`. After the workshop data or the images change, run:

```bash
python3 docs/sync_data.py          # copies activity/data (records, form, papers), activity/answers and assets into docs/
python3 docs/sync_data.py --check  # exits 1 if a copy is out of date
```

The GitHub Action `.github/workflows/pages-data.yml` runs the check on every push and pull request.
If a copy is missing anyway, the scorer and the batch page fall back to the raw files of the `main`
branch on `raw.githubusercontent.com`, so the site keeps working.

Note: `docs/data/screening_gold.csv` and `docs/data/extraction_gold.csv` are the reference answers.
They are public by design (the repository is open), so ask participants to score only after they
have finished.

## Try it locally

```bash
cd docs && python3 -m http.server 8000
# http://localhost:8000/scorer.html?sample=1   synthetic data, to see how scoring works
# http://localhost:8000/batch.html?sample=1    real PubMed records with empty abstracts, to test fetching
```

Opening the files directly (`file://`) does not work, because browsers block `fetch` there.
The sample files are described in [`data/_sample/README.md`](data/_sample/README.md).

## Formats the pages read

| File | Columns |
|---|---|
| `data/screening_records.csv` | `record_id,pmid,doi,title,abstract,year,journal,license` |
| `data/screening_gold.csv` | `record_id,gold_decision,gold_basis` (`include` or `exclude`) |
| participant decisions | `record_id,decision,reason` (`include`, `exclude` or `unsure`; commas, semicolons or tabs) |
| `data/extraction_form.csv` | `field,definition,allowed_values,type` |
| `data/extraction_gold.csv` and participant extraction | `study_id,field,value,source_quote,location` |
