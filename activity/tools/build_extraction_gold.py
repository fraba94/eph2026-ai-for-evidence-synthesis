#!/usr/bin/env python3
"""Build and check the extraction gold standard.

Two sources of truth are combined in activity/answers/extraction_gold.csv:
  1. the reference review's OWN tables (characteristics and results of the included studies, made by
     its human reviewers): column `review_table_value`;
  2. verbatim quotes from the primary papers (columns `value`, `source_quote`, `location`), prepared by
     the workshop team from the full texts listed in activity/data/papers.csv.

Subcommands:
  tables   Download the reference review from PubMed Central (review.pmcid in review_config.yaml) and
           write every table, one cell per row, to activity/answers/reference_review_tables.csv
           (table,row_label,ref,pmid,column,value). Rows are linked to PMIDs through the review's
           reference list, so the file covers ALL included studies, not only the three papers.
  check    Check extraction_gold.csv: every source_quote must occur verbatim in the paper's full text
           (data/fulltext/ or data/local/fulltext/), the numbers in `value` should appear in the quote,
           and `review_table_value` should be the review's cell for that study and field
           (review_table_map in the config). With --write, empty review_table_value cells are filled.
  skeleton Write a gold skeleton for every included study of the review from its tables
           (field,value from the review only; quotes to be added by hand). Useful after swapping the
           reference review.

Usage:
    python3 activity/tools/build_extraction_gold.py tables
    python3 activity/tools/build_extraction_gold.py check [--write]
    python3 activity/tools/build_extraction_gold.py skeleton --out my_work/gold_skeleton.csv

Run `python3 activity/tools/fetch_fulltext.py` first so that the papers that are not redistributable are
available locally. Standard library only.
"""
import argparse
import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

ROOT = os.path.dirname(C.ACTIVITY)
GOLD_COLS = ["study_id", "field", "value", "source_quote", "location", "review_table_value", "notes"]
TABLE_COLS = ["table", "row_label", "ref", "pmid", "column", "value"]


def txt(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip() if el is not None else ""


def cmd_tables(a, cfg):
    pmcid = cfg["review"]["pmcid"]
    root = ET.fromstring(C.efetch("pmc", [pmcid.replace("PMC", "")]))
    refs = {}
    for ref in root.iter("ref"):
        lab = (ref.findtext("label") or "").strip().rstrip(".")
        for pid in ref.iter("pub-id"):
            if pid.get("pub-id-type") == "pmid":
                refs[lab] = pid.text.strip()
    rows = []
    for tw in root.iter("table-wrap"):
        label = (tw.findtext("label") or "").strip()
        header = []
        thead = tw.find(".//thead")
        if thead is not None:
            trs = thead.findall(".//tr")
            if trs:
                header = [txt(c) for c in trs[-1] if c.tag in ("th", "td")]
        body = tw.find(".//tbody")
        trs = body.findall(".//tr") if body is not None else tw.findall(".//tr")
        if not header and trs:
            header = [txt(c) for c in trs[0]]
            trs = trs[1:]
        for tr in trs:
            cells = [txt(c) for c in tr if c.tag in ("td", "th")]
            if not cells:
                continue
            row_label = cells[0]
            m = re.search(r"\[(\d+)\]", row_label)
            ref = m.group(1) if m else ""
            for col, val in zip(header[1:], cells[1:]):
                rows.append({"table": label, "row_label": row_label, "ref": ref, "pmid": refs.get(ref, ""),
                             "column": col, "value": val})
    out = os.path.join(ROOT, cfg["extraction"]["review_tables_file"])
    C.write_csv(out, rows, TABLE_COLS)
    studies = {r["pmid"] for r in rows if r["pmid"]}
    print(f"wrote {os.path.relpath(out, ROOT)}: {len(rows)} cells, {len(studies)} studies linked to PMIDs")


def load_fulltexts(papers):
    out = {}
    for p in papers:
        cands = [os.path.join(ROOT, p["fulltext_file"]),
                 os.path.join(C.DATA, "fulltext", p["study_id"] + ".txt"),
                 os.path.join(C.LOCAL, "fulltext", p["study_id"] + ".txt")]
        for c in cands:
            if os.path.exists(c):
                with open(c, encoding="utf-8") as fh:
                    out[p["study_id"]] = fh.read()
                break
    return out


def review_cells(cfg):
    path = os.path.join(ROOT, cfg["extraction"]["review_tables_file"])
    cells = {}
    if os.path.exists(path):
        for r in C.read_csv(path):
            cells[(r["pmid"], r["column"])] = r["value"]
    return cells


def cmd_check(a, cfg):
    gold_path = os.path.join(ROOT, cfg["extraction"]["gold_file"])
    gold = C.read_csv(gold_path)
    papers = C.read_csv(os.path.join(ROOT, cfg["extraction"]["papers_file"]))
    pmid_of = {p["study_id"]: p["pmid"] for p in papers}
    texts = load_fulltexts(papers)
    cells = review_cells(cfg)
    fmap = cfg["extraction"].get("review_table_map") or {}
    problems = warnings = filled = 0
    for i, g in enumerate(gold, 2):
        sid, field = g["study_id"], g["field"]
        where = f"line {i} ({sid}/{field})"
        q = (g.get("source_quote") or "").strip()
        if q:
            if sid not in texts:
                print(f"SKIP   {where}: full text not available (run tools/fetch_fulltext.py)")
            elif C.squash(q) not in C.squash(texts[sid]):
                print(f"ERROR  {where}: quote NOT found verbatim in the full text")
                problems += 1
            else:
                nums_v = [n for n in C.numbers_in(g["value"]) if " or " not in C.norm_text(g["value"])]
                nums_q = C.numbers_in(q)
                miss = [n for n in nums_v if not any(abs(n - m) < 1e-9 for m in nums_q)]
                if miss:
                    print(f"warn   {where}: number(s) {miss} of the value are not in the quote")
                    warnings += 1
        elif not C.is_not_reported(g["value"]):
            print(f"warn   {where}: value without a quote")
            warnings += 1
        col = fmap.get(field)
        cell = cells.get((pmid_of.get(sid, ""), col)) if col else None
        if col and cell is not None:
            if not g.get("review_table_value"):
                g["review_table_value"] = cell
                filled += 1
            elif C.squash(g["review_table_value"]) not in C.squash(cell):
                print(f"warn   {where}: review_table_value differs from the review's cell '{col}'")
                warnings += 1
    print(f"{len(gold)} gold values checked: {problems} error(s), {warnings} warning(s); "
          f"{filled} review_table_value cell(s) {'filled' if a.write else 'could be filled (--write)'}")
    if a.write and filled:
        C.write_csv(gold_path, gold, GOLD_COLS)
    sys.exit(1 if problems else 0)


def cmd_skeleton(a, cfg):
    cells = C.read_csv(os.path.join(ROOT, cfg["extraction"]["review_tables_file"]))
    fmap = cfg["extraction"].get("review_table_map") or {}
    rows = []
    for (field, col) in fmap.items():
        for c in cells:
            if c["column"] == col and c["pmid"]:
                rows.append({"study_id": "PMID" + c["pmid"], "field": field, "value": "", "source_quote": "",
                             "location": "", "review_table_value": c["value"], "notes": c["row_label"]})
    rows.sort(key=lambda r: (r["study_id"], r["field"]))
    C.write_csv(a.out, rows, GOLD_COLS)
    print(f"wrote {a.out}: {len(rows)} rows (fill value, source_quote and location from the full texts)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=C.CONFIG)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("tables", help="extract the reference review's tables from PMC")
    ch = sub.add_parser("check", help="verify the gold standard")
    ch.add_argument("--write", action="store_true", help="fill empty review_table_value cells")
    sk = sub.add_parser("skeleton", help="gold skeleton for all included studies from the review tables")
    sk.add_argument("--out", required=True)
    a = ap.parse_args()
    cfg = C.load_yaml(a.config)
    {"tables": cmd_tables, "check": cmd_check, "skeleton": cmd_skeleton}[a.cmd](a, cfg)


if __name__ == "__main__":
    main()
