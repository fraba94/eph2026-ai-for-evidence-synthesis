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

Matching uses the same normalisation as activity/tools/score_extraction.py (imported from
activity/tools/common.py when available): case, all whitespace, table pipes "|",
typographic quotes and dashes are ignored. " ... " in a quote splits it into pieces that must each occur, in order.
A status of quote_found is necessary, not sufficient: a human still judges whether
the quote supports the value. Standard library only.
"""
import argparse
import csv
import importlib.util
import os
import re
import sys
import unicodedata
from collections import Counter


def _load_workshop_common():
    """Use activity/tools/common.py (the scorer's normalisation) when this skill runs inside the
    workshop repository, so that this check and score_extraction.py agree on what "found" means."""
    here = os.path.dirname(os.path.abspath(__file__))
    for base in (os.getcwd(), os.path.join(here, "..", "..", "..", "..")):
        path = os.path.normpath(os.path.join(base, "activity", "tools", "common.py"))
        if os.path.isfile(path):
            spec = importlib.util.spec_from_file_location("workshop_common", path)
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
                return mod
            except Exception:
                return None
    return None


_common = _load_workshop_common()

if _common is not None:
    norm_text, squash, is_not_reported, numbers_in = (
        _common.norm_text, _common.squash, _common.is_not_reported, _common.numbers_in)
else:
    # Fallback: a copy of the functions in activity/tools/common.py (keep them in sync).
    _TRANS = {
        "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "-", "\u2212": "-",
        "\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'", "\u2032": "'",
        "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u2033": '"',
        "\u00a0": " ", "\u2009": " ", "\u202f": " ", "\u2007": " ", "\u2002": " ",
        "\u00b7": ".", "\u2022": "", "\ufeff": "",
    }
    _NOT_REPORTED = {"not reported", "nr", "n/r", "not stated", "not available", "none reported", "missing",
                     "not applicable", "na", "n/a", "unclear", "not described"}

    def norm_text(s):
        s = unicodedata.normalize("NFKC", s or "")
        s = "".join(_TRANS.get(ch, ch) for ch in s)
        s = s.lower()
        return re.sub(r"\s+", " ", s).strip()

    def squash(s):
        return re.sub(r"[\s|]+", "", norm_text(s))

    def is_not_reported(value):
        v = norm_text(value).strip(" .;")
        return v in _NOT_REPORTED or v.startswith("not reported")

    def numbers_in(s):
        s = norm_text(s)
        out = []
        for m in re.finditer(r"(?<![\d.])-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![\d.])-?\d+(?:\.\d+)?", s):
            txt = m.group()
            if txt.startswith("-") and m.start() > 0 and s[m.start() - 1].isalnum():
                txt = txt[1:]
            out.append(float(txt.replace(",", "")))
        return out


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
            cache[key] = squash(f.read())
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
        if is_not_reported(value):
            status = "not_reported"
            note = "confirm absence by reading the paper (tables, figures, supplement)"
        elif src is None:
            status = "no_source"
        elif not quote:
            status = "no_quote"
        else:
            pieces = [squash(p) for p in re.split(r"\s*(?:\.\.\.|…)\s*", quote)]
            if not find_in_order(pieces, src):
                status = "quote_not_found"
            else:
                qn = set(numbers_in(quote))
                missing = [f"{n:g}" for n in numbers_in(value) if n not in qn]
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
