#!/usr/bin/env python3
"""Score a data extraction against the reference extraction and check every quote against the paper.

Input: long-format CSV, one row per study and field:
    study_id,field,value[,source_quote][,location]
study_id must match activity/data/papers.csv (e.g. Phan2020); field must match activity/data/extraction_form.csv.

For every gold value the scorer reports one of:
    exact           same value (after normalising case, dashes, spaces, %)
    within tol.     numeric value within the tolerance (default 2% relative, or 0.01 absolute)
    text match      free text / list that overlaps strongly with the gold value (check by eye)
    partial         some overlap: read both and decide
    mismatch        different value
    missing         no row for this study and field
    false absent    you wrote "not reported" but the paper reports it
    unsupported     you gave a value where the gold says "not reported": possible inference or hallucination
and, independently, a quote check against the full text of the paper:
    quote found / QUOTE NOT FOUND (hallucinated or paraphrased quote) / no quote / not checked (no full text)
    plus "number not in quote" when a number in your value does not appear in your own quote.

The CSV reader tolerates ';' or tab separators, a byte-order mark, ``` fences, prose around the table and
unquoted commas in the last column; study_id and field names are matched without regard to case
(phan2020 = Phan2020, "HAI rate baseline" = hai_rate_baseline).

Full texts are read from activity/data/fulltext/ and activity/data/local/fulltext/
(run `python3 activity/tools/fetch_fulltext.py` for the papers that are not shipped).

Examples:
    python3 activity/tools/score_extraction.py my_work/extraction_ai.csv
    python3 activity/tools/score_extraction.py my_work/extraction_ai.csv --study Phan2020 --out my_work/extraction_report.md
    python3 activity/tools/score_extraction.py extraction.csv --fields country,study_design,intervention_components,primary_hai_outcome,direction_of_effect
    python3 activity/tools/score_extraction.py activity/examples/extraction_example.csv

Do not run this before step 3 of the exercise: it reads the answers in activity/answers/.
Standard library only.
"""
import argparse
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

ROOT = os.path.dirname(C.ACTIVITY)
STOP = set("a an the and or of in on at to for with by from as is are was were be per vs versus its their this that "
           "other others e g eg i ie".split())
SYNONYMS = {
    "favorable": "favourable", "positive": "favourable", "beneficial": "favourable", "reduction": "favourable",
    "uncontrolled before after": "uncontrolled before-after", "before after": "uncontrolled before-after",
    "pre post": "uncontrolled before-after", "pre-post": "uncontrolled before-after", "before-after": "uncontrolled before-after",
    "its": "interrupted time series", "cba": "controlled before-after",
    "hospital wide": "hospital-wide", "multiward": "multi-ward", "multi ward": "multi-ward",
    "pre-intervention": "pre-intervention period", "baseline": "pre-intervention period",
    "y": "yes", "n": "no", "true": "yes", "false": "no",
}


def canon(v):
    v = C.norm_text(v).strip(" .;")
    v = v.replace("_", " ")
    return SYNONYMS.get(v, v)


def tokens(v):
    v = C.norm_text(v)
    v = re.sub(r"[^a-z0-9.%]+", " ", v)
    return {t for t in v.split() if t not in STOP and len(t) > 1}


def compare(value, gold, ftype, tol):
    """Return the agreement category for one value."""
    if not value.strip():
        return "missing"
    alts = [x.strip() for x in re.split(r"\s+OR\s+", gold) if x.strip()]
    g_nr = all(C.is_not_reported(x) for x in alts)
    v_nr = C.is_not_reported(value)
    if g_nr and v_nr:
        return "exact"
    if g_nr:
        return "unsupported"
    if v_nr:
        return "false absent"
    best = "mismatch"
    rank = {"exact": 4, "within tol.": 3, "text match": 2, "partial": 1, "mismatch": 0}
    for g in alts:
        if ftype in ("numeric", "proportion"):
            gv, vv = C.numbers_in(g), C.numbers_in(value)
            if not gv or not vv:
                cat = "exact" if canon(g) == canon(value) else "mismatch"
            else:
                a, b = gv[0], vv[0]
                if ftype == "proportion":
                    if a > 1 and b <= 1:
                        b *= 100
                    elif a <= 1 and b > 1:
                        a *= 100
                if abs(a - b) < 1e-9:
                    cat = "exact"
                elif abs(a - b) <= max(tol * abs(a), 0.01):
                    cat = "within tol."
                else:
                    cat = "mismatch"
        elif ftype == "categorical":
            cv, cg = canon(value), canon(g)
            if cv == cg:
                cat = "exact"
            elif cg in cv or cv in cg:
                cat = "partial"
            else:
                cat = "mismatch"
        else:  # text, list
            if canon(value) == canon(g):
                cat = "exact"
            else:
                tv, tg = tokens(value), tokens(g)
                j = len(tv & tg) / len(tv | tg) if tv | tg else 0
                cover = len(tv & tg) / len(tg) if tg else 0
                cat = "text match" if (j >= 0.5 or cover >= 0.7) else ("partial" if (j >= 0.15 or cover >= 0.3) else "mismatch")
        if rank[cat] > rank[best]:
            best = cat
    return best


def quote_check(row, texts):
    q = (row.get("source_quote") or "").strip()
    sid = row["study_id"]
    if not q:
        return "no quote" if not C.is_not_reported(row.get("value", "")) else "n/a (not reported)"
    if sid not in texts:
        return "not checked (no full text)"
    if C.squash(q) not in C.squash(texts[sid]):
        return "QUOTE NOT FOUND"
    nv = C.numbers_in(row.get("value", ""))
    nq = C.numbers_in(q)
    if any(not any(abs(x - y) < 1e-9 or abs(x - y * 100) < 1e-6 or abs(x * 100 - y) < 1e-6 for y in nq) for x in nv):
        return "quote found, number not in quote"
    return "quote found"


def load_texts(papers):
    out = {}
    for p in papers:
        for c in (os.path.join(ROOT, p.get("fulltext_file", "")), os.path.join(C.DATA, "fulltext", p["study_id"] + ".txt"),
                  os.path.join(C.LOCAL, "fulltext", p["study_id"] + ".txt")):
            if c and os.path.isfile(c):
                with open(c, encoding="utf-8") as fh:
                    out[p["study_id"]] = fh.read()
                break
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("extraction", help="CSV: study_id,field,value[,source_quote][,location]")
    ap.add_argument("--gold", default=os.path.join(C.ANSWERS, "extraction_gold.csv"))
    ap.add_argument("--form", default=os.path.join(C.DATA, "extraction_form.csv"))
    ap.add_argument("--papers", default=os.path.join(C.DATA, "papers.csv"))
    ap.add_argument("--study", action="append", help="score only this study_id (repeatable); default: studies present in your file")
    ap.add_argument("--core-only", action="store_true", help="score only the core fields of the form")
    ap.add_argument("--fields", help="score only these fields, comma-separated (the short extraction of step 3: "
                    "country,study_design,intervention_components,primary_hai_outcome,direction_of_effect)")
    ap.add_argument("--tol", type=float, default=0.02, help="relative tolerance for numbers (default 0.02 = 2%%)")
    ap.add_argument("--out", help="also write the report as Markdown to this file")
    a = ap.parse_args()

    form = {f["field"]: f for f in C.read_csv(a.form)}
    gold = C.read_csv(a.gold)
    papers = C.read_csv(a.papers)
    texts = load_texts(papers)
    rows = C.read_csv(a.extraction, expect=["study_id", "field"])
    if not rows or not {"study_id", "field", "value"} <= set(rows[0].keys()):
        C.die("the extraction file needs the columns study_id,field,value[,source_quote][,location]")
    canon_sid = {g["study_id"].lower(): g["study_id"] for g in gold}
    canon_sid.update({p_["study_id"].lower(): p_["study_id"] for p_ in papers})

    def fkey(x):
        return re.sub(r"[\s-]+", "_", (x or "").strip().strip("`*").lower())
    mine = {}
    unknown_fields, dups = set(), []
    for r in rows:
        sid = (r.get("study_id") or "").strip().strip("`*")
        sid = canon_sid.get(sid.lower(), sid)
        f = fkey(r.get("field"))
        if not sid or not f:
            continue
        if f not in form:
            unknown_fields.add(f)
        if (sid, f) in mine:
            dups.append(f"{sid}/{f}")
        r["study_id"], r["field"] = sid, f
        mine[(sid, f)] = r
    studies = [canon_sid.get(x.lower(), x) for x in a.study] if a.study else sorted({k[0] for k in mine})
    known = {g["study_id"] for g in gold}
    missing_studies = [s for s in studies if s not in known]

    L = []
    p = L.append
    p(f"# Extraction score: {os.path.basename(a.extraction)}")
    p("")
    p(f"Reference: `{os.path.relpath(a.gold)}` (values prepared by the workshop team from the full texts, cross-checked "
      "with the reference review's own tables: column 'review table'). Studies scored: " + (", ".join(s for s in studies if s in known) or "none"))
    p("")
    only_fields = {x.strip().lower() for x in (a.fields or "").split(",") if x.strip()}
    results = []
    for g in gold:
        if g["study_id"] not in studies:
            continue
        f = form.get(g["field"], {})
        if a.core_only and f.get("core", "yes") != "yes":
            continue
        if only_fields and g["field"] not in only_fields:
            continue
        r = mine.get((g["study_id"], g["field"]))
        val = (r or {}).get("value", "") or ""
        cat = compare(val, g["value"], f.get("type", "text"), a.tol) if r else "missing"
        qc = quote_check(r, texts) if r else "-"
        results.append((g, r, cat, qc))

    cats = Counter(c for _, _, c, _ in results)
    qcs = Counter(q for _, _, _, q in results if q != "-")
    p("## Summary")
    p("")
    order = ["exact", "within tol.", "text match", "partial", "mismatch", "missing", "false absent", "unsupported"]
    p("| Agreement with the reference | n |")
    p("|---|---:|")
    for c in order:
        if cats.get(c):
            p(f"| {c} | {cats[c]} |")
    agree = cats["exact"] + cats["within tol."] + cats["text match"]
    p(f"| **agreement (exact + within tol. + text match)** | **{agree}/{len(results)}** |")
    attempted = len(results) - cats["missing"]
    p(f"| agreement among the fields you extracted | {agree}/{attempted} |")
    p("")
    p("| Quote check against the full text | n |")
    p("|---|---:|")
    for q, n in qcs.most_common():
        p(f"| {q} | {n} |")
    p("")

    per_field = defaultdict(Counter)
    for g, _, c, _ in results:
        per_field[g["field"]][c] += 1
    p("## Per field")
    p("")
    p("| field | type | " + " | ".join(order) + " |")
    p("|---|---|" + "---:|" * len(order))
    for fld in form:
        if fld in per_field:
            p(f"| {fld} | {form[fld].get('type', '')} | " + " | ".join(str(per_field[fld].get(c, 0) or "") for c in order) + " |")
    p("")

    p("## Details (everything that is not an exact match, plus every quote problem)")
    p("")
    p("| study | field | your value | reference value | agreement | quote check | review table | note |")
    p("|---|---|---|---|---|---|---|---|")

    def cut(s, n=90):
        s = re.sub(r"\s+", " ", (s or "")).replace("|", "/")
        return s if len(s) <= n else s[:n - 1] + "…"
    for g, r, c, q in results:
        if c == "missing" or (c == "exact" and q in ("quote found", "n/a (not reported)")):
            continue
        p(f"| {g['study_id']} | {g['field']} | {cut((r or {}).get('value', ''))} | {cut(g['value'])} | {c} | {q} | "
          f"{cut(g.get('review_table_value', ''), 70)} | {cut(g.get('notes', ''), 140)} |")
    p("")
    miss = defaultdict(list)
    for g, _, c, _ in results:
        if c == "missing":
            miss[g["study_id"]].append(g["field"])
    if miss:
        p("Fields not extracted (no row in your file): " + "; ".join(f"**{k}**: {', '.join(v)}" for k, v in miss.items()))
        p("")
    extra = [k for k in mine if k[0] in studies and not any(g["study_id"] == k[0] and g["field"] == k[1] for g in gold)]
    issues = []
    if missing_studies:
        issues.append("study_id not in the reference: " + ", ".join(missing_studies) + " (see activity/data/papers.csv)")
    if unknown_fields:
        issues.append("fields not in the form: " + ", ".join(sorted(unknown_fields)))
    if extra:
        issues.append(f"{len(extra)} row(s) without a reference value (not scored)")
    if dups:
        issues.append("duplicated study/field rows (last kept): " + ", ".join(dups))
    no_text = sorted({g["study_id"] for g, _, _, q in results if q == "not checked (no full text)"})
    if no_text:
        issues.append("quotes not checked for " + ", ".join(no_text) + ": run `python3 activity/tools/fetch_fulltext.py`")
    if issues:
        p("## Problems")
        p("")
        for x in issues:
            p("- " + x)
        p("")
    p("How to read this: 'QUOTE NOT FOUND' means the quote is not in the paper as written (paraphrased, merged from two "
      "places, or invented): treat the value as unverified. 'unsupported' means a value where the paper reports nothing: "
      "the typical sign of inference or hallucination. 'false absent' means the information was there but was reported as "
      "missing (often a retrieval or parsing failure, e.g. a table). Check the notes column: several reference values are "
      "themselves ambiguous because the papers contradict themselves, and the review table sometimes differs from the paper.")
    report = "\n".join(L) + "\n"
    print(report)
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"(report written to {a.out})")


if __name__ == "__main__":
    main()
