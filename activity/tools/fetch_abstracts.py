#!/usr/bin/env python3
"""Fill the empty abstracts of the screening set from PubMed, on YOUR computer.

Why: the repository ships an abstract only when its licence allows redistribution (CC BY or CC0).
For the other records the `abstract` column is empty. This script downloads those abstracts from
NCBI E-utilities (efetch, by PMID) and writes a complete copy for your own use.

Usage:
    python3 activity/tools/fetch_abstracts.py
        -> writes activity/data/local/screening_records_full.csv (git-ignored; do not publish it)
    python3 activity/tools/fetch_abstracts.py --out my_work/records_full.csv

Then use the full file for screening, e.g.:
    python3 beginners/make_batches.py activity/data/local/screening_records_full.csv

Standard library only. Needs internet access to eutils.ncbi.nlm.nih.gov (about 1 request per 100 records).
Abstracts are copied verbatim from PubMed; their copyright stays with the publishers.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

COLS = ["record_id", "pmid", "doi", "title", "abstract", "year", "journal", "license"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="inp", default=os.path.join(C.DATA, "screening_records.csv"), help="records CSV to complete")
    ap.add_argument("--out", default=os.path.join(C.LOCAL, "screening_records_full.csv"),
                    help="output CSV (default: activity/data/local/screening_records_full.csv, git-ignored)")
    a = ap.parse_args()

    rows = C.read_csv(a.inp)
    cols = list(rows[0].keys()) if rows else COLS
    todo = [r["pmid"].strip() for r in rows if not (r.get("abstract") or "").strip() and (r.get("pmid") or "").strip()]
    print(f"{len(rows)} records, {len(todo)} with an empty abstract", file=sys.stderr)
    got = C.pubmed_records(todo) if todo else {}
    filled, still = 0, []
    for r in rows:
        if (r.get("abstract") or "").strip():
            continue
        m = got.get((r.get("pmid") or "").strip())
        if m and m["abstract"]:
            r["abstract"] = m["abstract"]
            r["license"] = "abstract fetched locally from PubMed (not for redistribution)"
            filled += 1
        else:
            still.append(r["record_id"])
    out = a.out
    if os.path.abspath(out) == os.path.abspath(a.inp) or os.path.abspath(out) == os.path.abspath(os.path.join(C.DATA, "screening_records.csv")):
        C.die("refusing to overwrite the shipped records file: abstracts fetched from PubMed must not go into a tracked file")
    C.write_csv(out, rows, cols)
    print(f"filled {filled} abstracts -> {out}")
    if still:
        print("no abstract in PubMed for: " + ", ".join(still) + " (screen on the title, mark 'unsure')")


if __name__ == "__main__":
    main()
