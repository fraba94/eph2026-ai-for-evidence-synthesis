#!/usr/bin/env python3
"""Draft a discrepancy log comparing AI output with a human/gold reference.

Screening:
  python3 draft_discrepancy_log.py screening AI.csv GOLD.csv [--out discrepancy_log.csv]
    AI.csv   record_id,decision,reason              (include|exclude|unsure)
    GOLD.csv record_id,gold_decision,gold_basis      (include|exclude)

Extraction:
  python3 draft_discrepancy_log.py extraction AI.csv GOLD.csv [--out discrepancy_log.csv]
    both in long format: study_id,field,value,source_quote,location

The script assigns a *provisional* category where it can be decided mechanically and
leaves `final_category` and `human_note` empty for the reviewer. Categories:
  screening : missed_include, false_include, unsure_on_include, unsure_on_exclude,
              missing_record
  extraction: omission (gold has a value, AI missing or "not reported"),
              possible_hallucination (AI value where gold says not reported / has no row),
              value_mismatch (both have values that differ: a human sub-classifies as
              wrong_value, parsing_error, wrong_unit_or_rounding, different_model_or_subgroup,
              or gold_error)
Matching of values ignores case, spaces and trailing zeros of numbers; it is deliberately
strict, so some "mismatches" will be equivalent wordings a human should accept.
Standard library only.
"""
import argparse
import csv
import re
import sys
from collections import Counter

NOT_REPORTED = {"", "not reported", "nr", "n/r", "not stated", "not available"}


def read(path, need):
    with open(path, newline="", encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        miss = set(need) - set(r.fieldnames or [])
        if miss:
            sys.exit(f"{path}: missing columns {sorted(miss)} (found {r.fieldnames})")
        return [{k: (v or "").strip() for k, v in row.items() if k} for row in r]


def norm_value(v):
    v = (v or "").strip().lower()
    v = re.sub(r"\s+", " ", v)
    v = re.sub(r"(?<=\d),(?=\d{3}\b)", "", v)  # 1,250 -> 1250
    v = re.sub(r"(\d+\.\d*?)0+\b", r"\1", v)
    v = re.sub(r"(\d+)\.(?!\d)", r"\1", v)
    return v


def screening(ai_path, gold_path):
    ai = {r["record_id"]: r for r in read(ai_path, ["record_id", "decision", "reason"])}
    gold = read(gold_path, ["record_id", "gold_decision"])
    rows = []
    for g in gold:
        rid, gd = g["record_id"], g["gold_decision"].lower()
        a = ai.get(rid)
        ad = a["decision"].lower() if a else ""
        if not a:
            cat = "missing_record"
        elif ad == gd:
            continue
        elif gd == "include" and ad == "exclude":
            cat = "missed_include"
        elif gd == "exclude" and ad == "include":
            cat = "false_include"
        elif gd == "include" and ad == "unsure":
            cat = "unsure_on_include"
        elif gd == "exclude" and ad == "unsure":
            cat = "unsure_on_exclude"
        else:
            cat = "other"
        rows.append({"item": rid, "field": "", "ai": ad, "ai_reason_or_quote": a["reason"] if a else "",
                     "gold": gd, "gold_basis_or_quote": g.get("gold_basis", ""),
                     "provisional_category": cat, "severity": "high" if cat in ("missed_include", "missing_record") else "low",
                     "final_category": "", "human_note": ""})
    return rows


def extraction(ai_path, gold_path):
    need = ["study_id", "field", "value"]
    ai = {(r["study_id"], r["field"]): r for r in read(ai_path, need)}
    gold = {(r["study_id"], r["field"]): r for r in read(gold_path, need)}
    rows = []
    for key in sorted(set(ai) | set(gold)):
        a, g = ai.get(key), gold.get(key)
        av = a["value"] if a else ""
        gv = g["value"] if g else ""
        a_nr, g_nr = norm_value(av) in NOT_REPORTED, norm_value(gv) in NOT_REPORTED
        if a_nr and g_nr:
            continue
        if not a_nr and not g_nr and norm_value(av) == norm_value(gv):
            continue
        if g is None:
            cat, sev = "field_not_in_gold", "low"
        elif a_nr:
            cat, sev = "omission", "medium"
        elif g_nr:
            cat, sev = "possible_hallucination", "high"
        else:
            cat, sev = "value_mismatch", "high"
        rows.append({"item": key[0], "field": key[1], "ai": av,
                     "ai_reason_or_quote": (a or {}).get("source_quote", ""),
                     "gold": gv, "gold_basis_or_quote": (g or {}).get("source_quote", ""),
                     "provisional_category": cat, "severity": sev, "final_category": "", "human_note": ""})
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["screening", "extraction"])
    ap.add_argument("ai")
    ap.add_argument("gold")
    ap.add_argument("--out", default="discrepancy_log.csv")
    a = ap.parse_args()
    rows = screening(a.ai, a.gold) if a.mode == "screening" else extraction(a.ai, a.gold)
    cols = ["item", "field", "ai", "ai_reason_or_quote", "gold", "gold_basis_or_quote",
            "provisional_category", "severity", "final_category", "human_note"]
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} discrepancies -> {a.out}")
    for k, v in Counter(r["provisional_category"] for r in rows).most_common():
        print(f"  {k:<24} {v}")
    print("Fill final_category and human_note for every row: the categories above are provisional.")


if __name__ == "__main__":
    main()
