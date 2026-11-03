#!/usr/bin/env python3
"""Compare two screening runs (record_id,decision,reason) against the record list.

Usage:
  python3 compare_runs.py RECORDS.csv RUN1.csv RUN2.csv [--merged OUT.csv]

Reports missing / extra / duplicated record_ids, invalid decisions, raw agreement,
Cohen's kappa, and every disagreement. With --merged, writes a conservative merged
file: agreements keep the shared decision, disagreements become "unsure".
Standard library only.
"""
import argparse
import csv
import sys
from collections import Counter

VALID = ("include", "exclude", "unsure")


def read_ids(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if "record_id" not in (reader.fieldnames or []):
            sys.exit(f"{path}: no 'record_id' column (found {reader.fieldnames})")
        return [row["record_id"].strip() for row in reader]


def read_run(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        needed = {"record_id", "decision", "reason"}
        missing = needed - set(reader.fieldnames or [])
        if missing:
            sys.exit(f"{path}: missing columns {sorted(missing)} (found {reader.fieldnames})")
        rows = [
            {k: (row.get(k) or "").strip() for k in ("record_id", "decision", "reason")}
            for row in reader
        ]
    for r in rows:
        r["decision"] = r["decision"].lower()
    return rows


def cohen_kappa(pairs):
    n = len(pairs)
    if n == 0:
        return float("nan")
    po = sum(a == b for a, b in pairs) / n
    c1 = Counter(a for a, _ in pairs)
    c2 = Counter(b for _, b in pairs)
    pe = sum(c1[k] * c2[k] for k in VALID) / (n * n)
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def check_run(name, rows, ids):
    problems = 0
    counts = Counter(r["record_id"] for r in rows)
    dups = sorted(k for k, v in counts.items() if v > 1)
    missing = [i for i in ids if i not in counts]
    extra = sorted(k for k in counts if k not in set(ids))
    invalid = [r["record_id"] for r in rows if r["decision"] not in VALID]
    no_reason = [r["record_id"] for r in rows if not r["reason"]]
    for label, items in (
        ("missing records (never silently drop!)", missing),
        ("duplicated record_ids", dups),
        ("record_ids not in the record list", extra),
        ("invalid decisions (must be include|exclude|unsure)", invalid),
        ("rows without a reason", no_reason),
    ):
        if items:
            problems += len(items)
            print(f"  [{name}] {label}: {len(items)} -> {', '.join(items[:20])}{' ...' if len(items) > 20 else ''}")
    dist = Counter(r["decision"] for r in rows)
    print(f"  [{name}] {len(rows)} rows: " + ", ".join(f"{k}={dist.get(k, 0)}" for k in VALID))
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("records")
    ap.add_argument("run1")
    ap.add_argument("run2")
    ap.add_argument("--merged", help="write conservative merged decisions to this CSV")
    a = ap.parse_args()

    ids = read_ids(a.records)
    print(f"Records in {a.records}: {len(ids)} ({len(set(ids))} unique)")
    r1, r2 = read_run(a.run1), read_run(a.run2)
    print("Completeness checks:")
    problems = check_run("run1", r1, ids) + check_run("run2", r2, ids)

    d1 = {r["record_id"]: r for r in r1}
    d2 = {r["record_id"]: r for r in r2}
    both = [i for i in ids if i in d1 and i in d2]
    pairs = [(d1[i]["decision"], d2[i]["decision"]) for i in both]
    agree = sum(x == y for x, y in pairs)
    print("\nAgreement between runs:")
    if both:
        print(f"  compared {len(both)} records, raw agreement {agree}/{len(both)} = {agree / len(both):.1%}")
        print(f"  Cohen's kappa = {cohen_kappa(pairs):.2f}")
    table = Counter(pairs)
    print("  run1 \\ run2  " + "  ".join(f"{k:>8}" for k in VALID))
    for k1 in VALID:
        print(f"  {k1:>11}  " + "  ".join(f"{table.get((k1, k2), 0):>8}" for k2 in VALID))

    dis = [i for i in both if d1[i]["decision"] != d2[i]["decision"]]
    if dis:
        print(f"\nDisagreements ({len(dis)}): resolve by a human, never by picking a run")
        for i in dis:
            print(f"  {i}: run1={d1[i]['decision']} ({d1[i]['reason']}) | run2={d2[i]['decision']} ({d2[i]['reason']})")
    else:
        print("\nNo disagreements.")

    if a.merged:
        with open(a.merged, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["record_id", "decision", "reason"])
            for i in ids:
                x, y = d1.get(i), d2.get(i)
                if x and y and x["decision"] == y["decision"]:
                    w.writerow([i, x["decision"], x["reason"]])
                else:
                    why = []
                    if x:
                        why.append(f"run1 {x['decision']}: {x['reason']}")
                    if y:
                        why.append(f"run2 {y['decision']}: {y['reason']}")
                    if not why:
                        why.append("missing in both runs")
                    w.writerow([i, "unsure", "runs disagree or missing -> human check | " + " | ".join(why)])
        print(f"\nMerged conservative decisions written to {a.merged} ({len(ids)} rows)")

    if problems:
        print(f"\nWARNING: {problems} completeness problem(s) found. Fix them before scoring.")
        sys.exit(1)


if __name__ == "__main__":
    main()
