#!/usr/bin/env python3
"""Check every extracted value against the source text.

Usage:
  python3 verify_quotes.py EXTRACTION.csv SOURCES [--out verification.csv]

EXTRACTION.csv  long format: study_id,field,value,source_quote,location
SOURCES         a directory with one text file per study named <study_id>.txt or
                <study_id>.md (e.g. from `pdftotext -layout`), or a single text file
                used for every row.

For each row the script assigns a status:
  quote_found       the quote occurs in the source and every number in the value is in the quote
  value_not_in_quote  the quote occurs, but a number in the value does not appear in it
  quote_not_found   the quote does not occur in the source (paraphrased, reconstructed or invented)
  no_quote          a value is given without any quote
  not_reported      value is "not reported" (check by hand: was it really absent?)
  no_source         no source text found for this study_id

Matching ignores case, whitespace, line-break hyphenation, typographic quotes and
dashes. " ... " in a quote splits it into pieces that must each occur, in order.
A status of quote_found is necessary, not sufficient: a human still judges whether
the quote supports the value. Standard library only.
"""
import argparse
import csv
import os
import re
import sys
import unicodedata
from collections import Counter

NOT_REPORTED = {"not reported", "nr", "n/r", "not stated", "not available"}
NUM = re.compile(r"\d+(?:[.,]\d+)?")


def norm(text):
    text = unicodedata.normalize("NFKC", text or "")
    text = re.sub(r"-\s*\n\s*", "", text)  # hyphenation at line end
    for a, b in (("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"'),
                 ("–", "-"), ("—", "-"), ("−", "-"), (" ", " ")):
        text = text.replace(a, b)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r" ?- ?", "-", text)  # "0.861 - 0.975" == "0.861-0.975"
    return text.strip().lower()


def nums(text):
    return [n.replace(",", ".") for n in NUM.findall(norm(text))]


def find_in_order(pieces, source):
    pos = 0
    for p in pieces:
        if not p:
            continue
        i = source.find(p, pos)
        if i < 0:
            return False
        pos = i + len(p)
    return True


def load_source(sources, study_id, cache):
    if os.path.isfile(sources):
        key = sources
    else:
        key = None
        for ext in (".txt", ".md", ".text"):
            cand = os.path.join(sources, study_id + ext)
            if os.path.isfile(cand):
                key = cand
                break
        if key is None:
            return None
    if key not in cache:
        with open(key, encoding="utf-8", errors="replace") as f:
            cache[key] = norm(f.read())
    return cache[key]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("extraction")
    ap.add_argument("sources")
    ap.add_argument("--out", default="verification.csv")
    a = ap.parse_args()

    with open(a.extraction, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        need = {"study_id", "field", "value", "source_quote", "location"}
        miss = need - set(reader.fieldnames or [])
        if miss:
            sys.exit(f"missing columns {sorted(miss)} in {a.extraction} (found {reader.fieldnames})")
        rows = list(reader)

    cache, out, stats = {}, [], Counter()
    for r in rows:
        value, quote = (r.get("value") or "").strip(), (r.get("source_quote") or "").strip()
        src = load_source(a.sources, (r.get("study_id") or "").strip(), cache)
        note = ""
        if norm(value) in NOT_REPORTED:
            status = "not_reported"
            note = "confirm absence by reading the paper (tables, figures, supplement)"
        elif src is None:
            status = "no_source"
        elif not quote:
            status = "no_quote"
        else:
            pieces = [norm(p) for p in re.split(r"\s*(?:\.\.\.|…)\s*", quote)]
            if not find_in_order(pieces, src):
                status = "quote_not_found"
            else:
                qn = set(nums(quote))
                missing = [n for n in nums(value) if n not in qn]
                if missing:
                    status = "value_not_in_quote"
                    note = "numbers not in quote: " + ", ".join(missing)
                else:
                    status = "quote_found"
        stats[status] += 1
        out.append({**{k: r.get(k, "") for k in ("study_id", "field", "value", "source_quote", "location")},
                    "verification": status, "note": note})

    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["study_id", "field", "value", "source_quote", "location", "verification", "note"])
        w.writeheader()
        w.writerows(out)

    print(f"Checked {len(rows)} rows -> {a.out}")
    for k in ("quote_found", "value_not_in_quote", "quote_not_found", "no_quote", "not_reported", "no_source"):
        print(f"  {k:<19} {stats.get(k, 0)}")
    bad = [o for o in out if o["verification"] in ("value_not_in_quote", "quote_not_found", "no_quote")]
    if bad:
        print("\nRows needing correction:")
        for o in bad:
            print(f"  {o['study_id']} | {o['field']} | {o['value']} | {o['verification']} {o['note']}")


if __name__ == "__main__":
    main()
