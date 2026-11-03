# Full texts for the extraction exercise

Plain-text versions of the open-access papers used in step 2 of the exercise, so that they can be pasted into a chat
assistant or read by an agent, and so that `activity/tools/score_extraction.py` can check that every quote really
occurs in the paper.

| File | Paper | Licence |
|---|---|---|
| `Phan2020.txt` | Phan HT, Zingg W, Tran HTT, Dinh APP, Pittet D. *Antimicrob Resist Infect Control* 2020;9:51. doi:[10.1186/s13756-020-00712-x](https://doi.org/10.1186/s13756-020-00712-x), PMID 32276646, PMCID PMC7146877 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| `Mestre2012.txt` | Mestre G, Berbel C, Tortajada P, et al. *PLoS One* 2012;7(10):e47200. doi:[10.1371/journal.pone.0047200](https://doi.org/10.1371/journal.pone.0047200), PMID 23110061, PMCID PMC3478274 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

The third paper of the exercise (Al Kuwaiti 2017, CC BY-NC 3.0) is **not** stored here: its licence does not allow
redistribution in this repository. Run `python3 activity/tools/fetch_fulltext.py` to download it to
`activity/data/local/fulltext/` (git-ignored), or open it at https://pmc.ncbi.nlm.nih.gov/articles/PMC5700699/.

**Attribution and changes.** Text © the original authors, from PubMed Central. Each file was produced from the PMC
XML by `activity/tools/pmc_to_text.py`: the author names, references, figure images and supplementary files were
omitted, and tables were flattened to one line per row with cells separated by ` | `. Author affiliations are kept (one line at the top). No other change was made.
Figures exist in these papers but appear here only as captions: values that are shown only in a figure cannot be
quoted from the text (this is one of the lessons of the exercise).
