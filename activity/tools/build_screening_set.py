#!/usr/bin/env python3
"""Build (or rebuild) the screening set of the exercise from PubMed IDs.

Reads the reference review in activity/review_config.yaml and the answer key in
activity/answers/reference_key.yaml (included studies, records excluded by the review at full text,
near misses, possible gold-standard errors), fetches titles, abstracts and licences from NCBI
E-utilities, shuffles the records with a fixed seed and writes:

    activity/data/screening_records.csv   record_id,pmid,doi,title,abstract,year,journal,license
    activity/answers/screening_gold.csv   record_id,gold_decision,gold_basis

Abstracts are written ONLY for records whose PubMed Central licence is CC BY or CC0; for the others the
abstract is left empty and `license` says so (fill them locally with fetch_abstracts.py).

Usage:
    python3 activity/tools/build_screening_set.py                 # rebuild from the answer key
    python3 activity/tools/build_screening_set.py --dry-run       # show counts, write nothing
    python3 activity/tools/build_screening_set.py --from-export screening_export.csv \\
            --id-col pmid --decision-col decision                # use the review team's own screening export

With --from-export the gold standard becomes the review team's ORIGINAL title/abstract decisions
(include/exclude per record), which is the authoritative standard for this exercise. The export must
be a CSV with one row per record, a PubMed ID column and a decision column; values counted as
"include" are set with --include-values (default: include,included,yes,y,1,maybe,unsure).

Standard library only. Network: NCBI E-utilities (cached in activity/data/local/metadata_cache.json).
"""
import argparse
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

RECORD_COLS = ["record_id", "pmid", "doi", "title", "abstract", "year", "journal", "license"]
GOLD_COLS = ["record_id", "gold_decision", "gold_basis"]

BASIS = {
    "included": "included in the reference review (listed in its table of included studies)",
    "fulltext_excluded": "excluded by the reference review after full-text assessment (cited among its full-text exclusions; it passed the review's title/abstract stage)",
    "near_misses": "not included in the reference review (retrieved by approximate search); workshop note: {reason}",
    "possible_gold_errors": "not included in the reference review, although it appears to meet its criteria: POSSIBLE GOLD-STANDARD ERROR (discussion item). {reason}",
}


def load_key(path):
    key = C.load_yaml(path)
    items = []
    for role in ("included", "fulltext_excluded", "near_misses", "possible_gold_errors"):
        for e in key.get(role) or []:
            items.append({"pmid": str(e["pmid"]), "role": role, "reason": e.get("reason", ""), "label": e.get("label", "")})
    return items


def load_export(path, id_col, dec_col, include_values):
    rows = C.read_csv(path)
    if not rows:
        C.die(f"{path} is empty")
    for col in (id_col, dec_col):
        if col not in rows[0]:
            C.die(f"column '{col}' not found in {path}; columns are: {', '.join(rows[0])}")
    inc = {v.strip().lower() for v in include_values.split(",")}
    items = []
    for r in rows:
        pmid = (r[id_col] or "").strip()
        if not pmid:
            continue
        d = (r[dec_col] or "").strip().lower()
        role = "export_include" if d in inc else "export_exclude"
        items.append({"pmid": pmid, "role": role, "reason": r[dec_col], "label": ""})
    return items


def fetch_metadata(pmids, cache_path, refresh=False):
    cache = {}
    if os.path.exists(cache_path) and not refresh:
        with open(cache_path, encoding="utf-8") as fh:
            cache = json.load(fh)
    todo = [p for p in pmids if p not in cache]
    if todo:
        print(f"fetching {len(todo)} PubMed records from NCBI E-utilities ...", file=sys.stderr)
        recs = C.pubmed_records(todo)
        lic = C.pmc_licences([r["pmcid"] for r in recs.values() if r["pmcid"]])
        for p, r in recs.items():
            r["licence"] = lic.get(r["pmcid"], "not open licence") if r["pmcid"] else "no PMC licence"
            cache[p] = r
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        with open(cache_path, "w", encoding="utf-8") as fh:
            json.dump(cache, fh, indent=0)
    missing = [p for p in pmids if p not in cache]
    if missing:
        C.die("PubMed returned nothing for: " + ", ".join(missing))
    return cache


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=C.CONFIG, help="reference review configuration (default: activity/review_config.yaml)")
    ap.add_argument("--key", default=None, help="answer key (default: screening.answers_file in the config)")
    ap.add_argument("--from-export", help="CSV export of the review team's own title/abstract decisions")
    ap.add_argument("--id-col", default="pmid", help="PubMed ID column in the export (default: pmid)")
    ap.add_argument("--decision-col", default="decision", help="decision column in the export (default: decision)")
    ap.add_argument("--include-values", default="include,included,yes,y,1,maybe,unsure",
                    help="export values counted as include (comma separated)")
    ap.add_argument("--records-out", default=os.path.join(C.DATA, "screening_records.csv"))
    ap.add_argument("--gold-out", default=os.path.join(C.ANSWERS, "screening_gold.csv"))
    ap.add_argument("--cache", default=os.path.join(C.LOCAL, "metadata_cache.json"))
    ap.add_argument("--refresh", action="store_true", help="ignore the local metadata cache")
    ap.add_argument("--seed", type=int, default=None, help="shuffle seed (default: screening.seed in the config)")
    ap.add_argument("--dry-run", action="store_true", help="print the counts and write nothing")
    a = ap.parse_args()

    cfg = C.load_yaml(a.config)
    root = os.path.dirname(C.ACTIVITY)
    key_path = a.key or os.path.join(root, cfg["screening"]["answers_file"])
    seed = a.seed if a.seed is not None else int(cfg["screening"].get("seed", 2026))

    if a.from_export:
        items = load_export(a.from_export, a.id_col, a.decision_col, a.include_values)
    else:
        items = load_key(key_path)
    seen = set()
    for it in items:
        if it["pmid"] in seen:
            C.die(f"PMID {it['pmid']} appears twice")
        seen.add(it["pmid"])

    meta = fetch_metadata([it["pmid"] for it in items], a.cache, a.refresh)
    random.Random(seed).shuffle(items)

    records, gold = [], []
    shipped = 0
    for n, it in enumerate(items, 1):
        m = meta[it["pmid"]]
        rid = f"R{n:03d}"
        ok = C.redistributable(m["licence"])
        shipped += ok
        records.append({
            "record_id": rid, "pmid": it["pmid"], "doi": m["doi"], "title": m["title"],
            "abstract": m["abstract"] if ok else "", "year": m["year"], "journal": m["journal"],
            "license": m["licence"] if ok else f"{m['licence']}: abstract not redistributed, run tools/fetch_abstracts.py",
        })
        if it["role"].startswith("export_"):
            dec = "include" if it["role"] == "export_include" else "exclude"
            basis = f"title/abstract decision of the reference review team (original screening export: {it['reason']})"
        else:
            dec = "include" if it["role"] == "included" else "exclude"
            basis = BASIS[it["role"]].format(reason=it["reason"]).strip()
        gold.append({"record_id": rid, "gold_decision": dec, "gold_basis": basis})

    n_inc = sum(g["gold_decision"] == "include" for g in gold)
    print(f"{len(records)} records: {n_inc} include, {len(records) - n_inc} exclude; "
          f"{shipped} abstracts redistributable (CC BY/CC0), {len(records) - shipped} left empty.")
    if a.dry_run:
        return
    C.write_csv(a.records_out, records, RECORD_COLS)
    C.write_csv(a.gold_out, gold, GOLD_COLS)
    print(f"wrote {os.path.relpath(a.records_out, root)} and {os.path.relpath(a.gold_out, root)}")


if __name__ == "__main__":
    main()
