#!/usr/bin/env python3
"""Copy the files the GitHub Pages site needs into docs/.

GitHub Pages publishes only the docs/ folder, so the website cannot read ../activity/ or ../assets/.
This script copies them in. Run it from anywhere after the workshop data or the images change:

    python3 docs/sync_data.py          # copy what changed
    python3 docs/sync_data.py --check  # exit 1 if docs/ is out of date (used by the GitHub Action)

The scorer and the batch page also fall back to the raw files on GitHub (main branch) when a copy is
missing, so the site keeps working even if this script was not run. Standard library only.
"""
import argparse
import filecmp
import shutil
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parent

COPIES = [
    # (source relative to the repository root, destination relative to docs/)
    ("activity/data/screening_records.csv", "data/screening_records.csv"),
    ("activity/answers/screening_gold.csv", "data/screening_gold.csv"),
    ("activity/data/extraction_form.csv", "data/extraction_form.csv"),
    ("activity/data/papers.csv", "data/papers.csv"),
    ("activity/answers/extraction_gold.csv", "data/extraction_gold.csv"),
    ("assets/eupha-dhai-logo.png", "assets/eupha-dhai-logo.png"),
    ("assets/banner.svg", "assets/banner.svg"),
    ("assets/workflow.svg", "assets/workflow.svg"),
    ("assets/in-the-loop.svg", "assets/in-the-loop.svg"),
    ("assets/two-tracks.svg", "assets/two-tracks.svg"),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="only report; exit 1 if a copy is missing or different")
    a = ap.parse_args()
    stale = 0
    for src_rel, dst_rel in COPIES:
        src, dst = ROOT / src_rel, DOCS / dst_rel
        if not src.exists():
            print(f"skip     {src_rel} (not in the repository yet)")
            continue
        if dst.exists() and filecmp.cmp(src, dst, shallow=False):
            print(f"ok       docs/{dst_rel}")
            continue
        stale += 1
        if a.check:
            print(f"STALE    docs/{dst_rel}  <- {src_rel}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            print(f"copied   {src_rel} -> docs/{dst_rel}")
    if a.check and stale:
        print(f"\n{stale} file(s) out of date: run  python3 docs/sync_data.py  and commit docs/.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
