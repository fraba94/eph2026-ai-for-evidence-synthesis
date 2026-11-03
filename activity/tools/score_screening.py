#!/usr/bin/env python3
"""Score title/abstract screening decisions against the reference standard.

Input: a CSV with columns  record_id,decision,reason  (decision = include | exclude | unsure).
       Extra columns are ignored. Accepted spellings: include/included/yes/y/in,
       exclude/excluded/no/n/out, unsure/maybe/uncertain/?.

Output (printed, and as Markdown with --out):
  - confusion matrix (AI/your decisions vs the reference review)
  - sensitivity (recall), specificity, precision (PPV), NPV, accuracy, F1
  - work saved over sampling (WSS) at the recall achieved, and WSS@95 when recall >= 95%
  - missed includes (false negatives) with titles: the errors that matter most at this stage
  - false includes, "unsure" records, records with no decision, unknown record_ids
  - records flagged as POSSIBLE GOLD-STANDARD ERRORS in the reference (discussion items)
  - optional: agreement between two runs (--compare run2.csv): Cohen's kappa and the disagreements

"unsure" is counted as INCLUDE by default (at title/abstract stage an uncertain record goes on to
full text); use --unsure exclude to see the other scenario. Unsure records are always reported apart.

Examples:
    python3 activity/tools/score_screening.py my_work/screening_ai.csv
    python3 activity/tools/score_screening.py run1.csv --compare run2.csv --out my_work/screening_report.md
    python3 activity/tools/score_screening.py activity/examples/decisions_example.csv

Do not run this before step 3 of the exercise: it reads the answers in activity/answers/.
Standard library only.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

SYN = {
    "include": "include", "included": "include", "yes": "include", "y": "include", "in": "include", "i": "include",
    "exclude": "exclude", "excluded": "exclude", "no": "exclude", "n": "exclude", "out": "exclude", "e": "exclude",
    "unsure": "unsure", "maybe": "unsure", "uncertain": "unsure", "?": "unsure", "u": "unsure", "unclear": "unsure",
}


def norm_id(x):
    x = (x or "").strip().upper()
    if x.isdigit():
        x = "R" + x.zfill(3)
    return x


def load_decisions(path):
    rows = C.read_csv(path)
    if not rows:
        C.die(f"{path} has no rows")
    cols = {c.strip().lower(): c for c in rows[0].keys()}
    if "record_id" not in cols or "decision" not in cols:
        C.die(f"{path} needs the columns record_id,decision[,reason]; found: {', '.join(rows[0].keys())}")
    out, bad, dup = {}, [], []
    for i, r in enumerate(rows, 2):
        rid = norm_id(r[cols["record_id"]])
        if not rid:
            continue
        raw = (r[cols["decision"]] or "").strip().lower()
        d = SYN.get(raw)
        if d is None:
            bad.append((i, rid, raw))
            continue
        if rid in out:
            dup.append(rid)
        out[rid] = {"decision": d, "reason": (r.get(cols.get("reason", ""), "") or "").strip()}
    return out, bad, dup


def ratio(a, b):
    return a / b if b else float("nan")


def pct(x):
    return "n/a" if x != x else f"{100 * x:.1f}%"


def kappa(a, b, ids):
    labels = ("include", "exclude", "unsure")
    n = len(ids)
    if not n:
        return float("nan")
    po = sum(a[i] == b[i] for i in ids) / n
    pe = sum((sum(a[i] == l for i in ids) / n) * (sum(b[i] == l for i in ids) / n) for l in labels)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("decisions", help="CSV with record_id,decision,reason")
    ap.add_argument("--gold", default=os.path.join(C.ANSWERS, "screening_gold.csv"), help="reference standard")
    ap.add_argument("--records", default=os.path.join(C.DATA, "screening_records.csv"), help="records file (titles)")
    ap.add_argument("--unsure", choices=["include", "exclude"], default="include", help="how to count 'unsure' (default: include)")
    ap.add_argument("--compare", metavar="RUN2.csv", help="second run of the same screening: report agreement")
    ap.add_argument("--out", help="also write the report as Markdown to this file")
    a = ap.parse_args()

    gold_rows = C.read_csv(a.gold)
    gold = {norm_id(g["record_id"]): g for g in gold_rows}
    titles = {}
    if os.path.exists(a.records):
        titles = {norm_id(r["record_id"]): r.get("title", "") for r in C.read_csv(a.records)}
    dec, bad, dup = load_decisions(a.decisions)

    L = []
    p = L.append
    p(f"# Screening score: {os.path.basename(a.decisions)}")
    p("")
    p(f"Reference standard: `{os.path.relpath(a.gold)}` ({len(gold)} records, "
      f"{sum(g['gold_decision'] == 'include' for g in gold.values())} includes). 'unsure' counted as **{a.unsure}**.")
    p("")
    tp = fp = tn = fn = 0
    missed, false_inc, unsure, missing, flagged = [], [], [], [], []
    for rid, g in gold.items():
        gd = g["gold_decision"].strip().lower()
        if rid not in dec:
            missing.append(rid)
            continue
        d = dec[rid]["decision"]
        if d == "unsure":
            unsure.append(rid)
        eff = a.unsure if d == "unsure" else d
        if "POSSIBLE GOLD-STANDARD ERROR" in g.get("gold_basis", ""):
            flagged.append((rid, d))
        if gd == "include" and eff == "include":
            tp += 1
        elif gd == "include":
            fn += 1
            missed.append(rid)
        elif eff == "include":
            fp += 1
            false_inc.append(rid)
        else:
            tn += 1
    unknown = [r for r in dec if r not in gold]
    n = tp + fp + tn + fn
    sens, spec = ratio(tp, tp + fn), ratio(tn, tn + fp)
    prec, npv = ratio(tp, tp + fp), ratio(tn, tn + fn)
    acc = ratio(tp + tn, n)
    f1 = ratio(2 * tp, 2 * tp + fp + fn)
    wss = ratio(tn + fn, n) - (1 - sens) if n else float("nan")

    p("## Confusion matrix")
    p("")
    p("| | Reference: include | Reference: exclude |")
    p("|---|---:|---:|")
    p(f"| **Decision: include** | {tp} (true include) | {fp} (false include) |")
    p(f"| **Decision: exclude** | {fn} (MISSED include) | {tn} (true exclude) |")
    p("")
    p("## Metrics")
    p("")
    p("| Metric | Value | Meaning |")
    p("|---|---:|---|")
    p(f"| Records scored | {n} of {len(gold)} | records with a valid decision |")
    p(f"| Sensitivity (recall) | {pct(sens)} | share of the review's includes that you kept: the key metric at this stage |")
    p(f"| Specificity | {pct(spec)} | share of the excludes that you excluded |")
    p(f"| Precision (PPV) | {pct(prec)} | share of your includes that the review included |")
    p(f"| NPV | {pct(npv)} | share of your excludes that the review excluded |")
    p(f"| Accuracy | {pct(acc)} | (misleading when includes are few) |")
    p(f"| F1 | {pct(f1)} | harmonic mean of recall and precision |")
    p(f"| WSS at achieved recall | {pct(wss)} | work saved over sampling = (TN+FN)/N - (1 - recall) |")
    if sens == sens and sens >= 0.95:
        p(f"| WSS@95 | {pct(ratio(tn + fn, n) - 0.05)} | recall >= 95%, so WSS@95 = (TN+FN)/N - 0.05 |")
    else:
        p("| WSS@95 | not applicable | recall is below 95%: the screening missed too many includes |")
    p(f"| Unsure | {len(unsure)} | counted as {a.unsure}; listed below |")
    p("")

    # Title/abstract-stage view: records the review assessed in full text passed ITS title/abstract stage.
    ft = [rid for rid, g in gold.items() if "full-text assessment" in g.get("gold_basis", "")]
    if ft:
        t2 = f2 = n2 = m2 = 0
        for rid, g in gold.items():
            if rid not in dec:
                continue
            eff = a.unsure if dec[rid]["decision"] == "unsure" else dec[rid]["decision"]
            ta = "include" if (g["gold_decision"].strip().lower() == "include" or rid in ft) else "exclude"
            if ta == "include" and eff == "include":
                t2 += 1
            elif ta == "include":
                m2 += 1
            elif eff == "include":
                f2 += 1
            else:
                n2 += 1
        p("### Title/abstract-stage view")
        p("")
        p(f"{len(ft)} records were excluded by the review only after reading the full text, so they passed its "
          "title/abstract stage. Counting them as 'include' gives a fairer picture of title/abstract screening:")
        p("")
        p(f"| | value |\n|---|---:|\n| Sensitivity (stage view) | {pct(ratio(t2, t2 + m2))} ({t2}/{t2 + m2}) |\n"
          f"| Specificity (stage view) | {pct(ratio(n2, n2 + f2))} ({n2}/{n2 + f2}) |\n"
          f"| Precision (stage view) | {pct(ratio(t2, t2 + f2))} |")
        p("")

    def line(rid):
        g = gold[rid]
        r = dec.get(rid, {})
        return (f"| {rid} | {titles.get(rid, '')[:110]} | {r.get('decision', '-')} | {g['gold_decision']} | "
                f"{(r.get('reason') or '')[:90]} | {g.get('gold_basis', '')[:120]} |")

    head = "| record | title | decision | reference | your reason | reference basis |\n|---|---|---|---|---|---|"
    if missed:
        p(f"## Missed includes ({len(missed)}) - check these first")
        p("")
        p(head)
        for rid in missed:
            p(line(rid))
        p("")
    if false_inc:
        p(f"## False includes ({len(false_inc)})")
        p("")
        p(head)
        for rid in false_inc:
            p(line(rid))
        p("")
    if unsure:
        p(f"## Unsure ({len(unsure)}) - counted as {a.unsure}")
        p("")
        p(head)
        for rid in unsure:
            p(line(rid))
        p("")
    if flagged:
        p("## Possible errors in the reference standard")
        p("")
        p("These records were not included by the reference review although they appear to meet its criteria. "
          "A 'false include' here may be a correct decision: discuss before blaming the AI.")
        p("")
        p(head)
        for rid, _ in flagged:
            p(line(rid))
        p("")
    probs = []
    if missing:
        probs.append(f"**{len(missing)} record(s) without a decision**: {', '.join(missing)}. A record that is silently dropped is a record that can be missed.")
    if unknown:
        probs.append(f"{len(unknown)} record_id(s) not in the reference: {', '.join(unknown)}")
    if bad:
        probs.append("invalid decisions: " + "; ".join(f"line {i} {rid} '{raw}'" for i, rid, raw in bad))
    if dup:
        probs.append("duplicated record_id (last one kept): " + ", ".join(dup))
    if probs:
        p("## Problems in the decisions file")
        p("")
        for x in probs:
            p("- " + x)
        p("")

    if a.compare:
        dec2, bad2, _ = load_decisions(a.compare)
        ids = [r for r in gold if r in dec and r in dec2]
        d1 = {r: dec[r]["decision"] for r in ids}
        d2 = {r: dec2[r]["decision"] for r in ids}
        diff = [r for r in ids if d1[r] != d2[r]]
        p(f"## Reproducibility: run 1 vs run 2 (`{os.path.basename(a.compare)}`)")
        p("")
        p(f"Records in both runs: {len(ids)}. Agreement: {len(ids) - len(diff)}/{len(ids)} "
          f"({pct(ratio(len(ids) - len(diff), len(ids)))}). Cohen's kappa: {kappa(d1, d2, ids):.2f}.")
        p("")
        if diff:
            p("| record | title | run 1 | run 2 | reference |")
            p("|---|---|---|---|---|")
            for r in diff:
                p(f"| {r} | {titles.get(r, '')[:100]} | {d1[r]} | {d2[r]} | {gold[r]['gold_decision']} |")
            p("")

    p("Interpretation: at title/abstract stage a missed include is far more costly than a false include. "
      "The reference is the review's FINAL inclusion (after full text), so records it excluded at full text "
      "are legitimate includes at this stage: read the 'reference basis' before calling a false include an error.")
    report = "\n".join(L) + "\n"
    print(report)
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"(report written to {a.out})")


if __name__ == "__main__":
    main()
