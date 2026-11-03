#!/usr/bin/env python3
"""Download the full texts of the extraction papers from PubMed Central and convert them to plain text.

Reads activity/data/papers.csv. For every paper it downloads the PMC XML (NCBI E-utilities efetch)
and writes plain text with tools/pmc_to_text.py:
  - papers with shipped=yes (CC BY) are already in activity/data/fulltext/ and are skipped
    (use --refresh to rebuild them);
  - papers with shipped=no (licence does not allow redistribution) go to
    activity/data/local/fulltext/<study_id>.txt, which is git-ignored: keep them on your computer.

score_extraction.py looks for full texts in both folders to check that quotes really occur in the paper.

Usage:
    python3 activity/tools/fetch_fulltext.py              # fetch what is missing
    python3 activity/tools/fetch_fulltext.py --refresh    # rebuild every file
    python3 activity/tools/fetch_fulltext.py --study AlKuwaiti2017

Standard library only.
"""
import argparse
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402
import pmc_to_text  # noqa: E402

ROOT = os.path.dirname(C.ACTIVITY)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--papers", default=os.path.join(C.DATA, "papers.csv"))
    ap.add_argument("--study", action="append", help="only this study_id (repeatable)")
    ap.add_argument("--refresh", action="store_true", help="rebuild files that already exist")
    a = ap.parse_args()
    for p in C.read_csv(a.papers):
        if a.study and p["study_id"] not in a.study:
            continue
        dest = os.path.join(ROOT, p["fulltext_file"])
        if p["shipped"].strip().lower() == "yes" and not C.redistributable(p["licence"]):
            C.die(f"{p['study_id']}: shipped=yes but licence {p['licence']} does not allow redistribution")
        if os.path.exists(dest) and not a.refresh:
            print(f"{p['study_id']}: present ({p['fulltext_file']})")
            continue
        xml = C.efetch("pmc", [p["pmcid"].replace("PMC", "")])
        with tempfile.NamedTemporaryFile("wb", suffix=".xml", delete=False) as fh:
            fh.write(xml)
            tmp = fh.name
        try:
            text = pmc_to_text.convert(tmp)
        finally:
            os.unlink(tmp)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"{p['study_id']}: wrote {p['fulltext_file']} ({len(text.split())} words, licence {p['licence']})")


if __name__ == "__main__":
    main()
