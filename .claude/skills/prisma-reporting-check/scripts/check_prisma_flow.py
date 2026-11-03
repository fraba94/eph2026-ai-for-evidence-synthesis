#!/usr/bin/env python3
"""Check the arithmetic of a PRISMA 2020 flow diagram.

Usage:
  python3 check_prisma_flow.py COUNTS.csv

COUNTS.csv has two columns, box,n (one row per box of the flow diagram, numbers copied
from the review's figure or text by a human). Recognised boxes (leave n empty when the
review does not report a box):

  identified_databases, identified_registers, identified_other
  duplicates_removed, removed_automation, removed_other
  records_screened, records_excluded
  reports_sought, reports_not_retrieved
  reports_assessed, reports_excluded
  excluded_reason:<short reason>     (one row per full-text exclusion reason)
  studies_included, reports_included

The script checks each subtraction of the flow, that the full-text exclusion reasons add
up to reports_excluded, and that studies_included is not larger than reports_included.
It reports each check as OK, MISMATCH or NOT CHECKED (a box is missing). A mismatch is a
question for the authors or the human reviewer, not proof of an error: some reviews
legitimately count records and reports differently. Standard library only.
"""
import argparse
import csv
import sys

KNOWN = {
    "identified_databases", "identified_registers", "identified_other",
    "duplicates_removed", "removed_automation", "removed_other",
    "records_screened", "records_excluded",
    "reports_sought", "reports_not_retrieved",
    "reports_assessed", "reports_excluded",
    "studies_included", "reports_included",
}


def read_counts(path):
    counts, reasons, problems = {}, {}, []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not {"box", "n"} <= set(reader.fieldnames or []):
            sys.exit(f"{path}: needs the columns box,n (found {reader.fieldnames})")
        for row in reader:
            box = (row.get("box") or "").strip()
            raw = (row.get("n") or "").strip().replace(",", "")
            if not box or raw == "":
                continue
            try:
                n = int(raw)
            except ValueError:
                problems.append(f"{box}: '{raw}' is not a whole number")
                continue
            if box.startswith("excluded_reason:"):
                reasons[box.split(":", 1)[1].strip()] = n
            elif box in KNOWN:
                counts[box] = n
            else:
                problems.append(f"unknown box '{box}' (ignored)")
    return counts, reasons, problems


def check(label, needed, counts, compute, expected_box):
    missing = [b for b in needed + [expected_box] if b not in counts]
    if missing:
        return "NOT CHECKED", f"{label}: missing {', '.join(missing)}"
    got, expr = compute(counts)
    exp = counts[expected_box]
    status = "OK" if got == exp else "MISMATCH"
    return status, f"{label}: {expr} = {got}; {expected_box} = {exp}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("counts", help="CSV with columns box,n")
    a = ap.parse_args()
    c, reasons, problems = read_counts(a.counts)

    ident = [b for b in ("identified_databases", "identified_registers", "identified_other") if b in c]
    removed = [b for b in ("duplicates_removed", "removed_automation", "removed_other") if b in c]
    results = []

    if ident and "duplicates_removed" in c:
        def f1(k):
            total = sum(k[b] for b in ident) - sum(k[b] for b in removed)
            return total, " + ".join(ident) + " - " + " - ".join(removed)
        results.append(check("identification to screening", [], c, f1, "records_screened"))
    else:
        results.append(("NOT CHECKED", "identification to screening: needs identified_* and duplicates_removed"))

    results.append(check(
        "screening to retrieval", ["records_screened", "records_excluded"], c,
        lambda k: (k["records_screened"] - k["records_excluded"], "records_screened - records_excluded"),
        "reports_sought"))
    results.append(check(
        "retrieval to assessment", ["reports_sought", "reports_not_retrieved"], c,
        lambda k: (k["reports_sought"] - k["reports_not_retrieved"], "reports_sought - reports_not_retrieved"),
        "reports_assessed"))
    results.append(check(
        "assessment to inclusion (reports)", ["reports_assessed", "reports_excluded"], c,
        lambda k: (k["reports_assessed"] - k["reports_excluded"], "reports_assessed - reports_excluded"),
        "reports_included"))

    if reasons and "reports_excluded" in c:
        s = sum(reasons.values())
        status = "OK" if s == c["reports_excluded"] else "MISMATCH"
        results.append((status, f"full-text exclusion reasons: {len(reasons)} reasons add up to {s}; reports_excluded = {c['reports_excluded']}"))
    else:
        results.append(("NOT CHECKED", "full-text exclusion reasons: needs excluded_reason:* rows and reports_excluded"))

    if "studies_included" in c and "reports_included" in c:
        ok = c["studies_included"] <= c["reports_included"]
        results.append(("OK" if ok else "MISMATCH",
                        f"studies vs reports: studies_included = {c['studies_included']}, reports_included = {c['reports_included']}"
                        + ("" if ok else " (more studies than reports?)")))
    else:
        results.append(("NOT CHECKED", "studies vs reports: needs studies_included and reports_included"))

    print(f"PRISMA flow arithmetic for {a.counts}")
    for status, msg in results:
        print(f"  [{status}] {msg}")
    for p in problems:
        print(f"  [INPUT] {p}")
    n_mis = sum(1 for s, _ in results if s == "MISMATCH")
    n_nc = sum(1 for s, _ in results if s == "NOT CHECKED")
    print(f"\n{n_mis} mismatch(es), {n_nc} check(s) not possible with the boxes given.")
    if n_mis:
        print("A mismatch is a question for the human reviewer: check the figure, the text and the supplement before calling it an error.")
        sys.exit(1)


if __name__ == "__main__":
    main()
