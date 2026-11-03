#!/usr/bin/env python3
"""Convert a PMC (JATS) XML article into a plain-text file for the extraction exercise.

Usage:
    python3 activity/tools/pmc_to_text.py article.xml output.txt

What it keeps: title, citation line, licence statement, abstract, body sections
(as "## Heading" lines) and tables (caption, then one line per row with cells
separated by " | "). Figures are reduced to their captions. References are dropped.

Standard library only. The text produced is the reference used by
score_extraction.py to check that a quote really occurs in the paper.
"""
import re
import sys
import xml.etree.ElementTree as ET

XLINK = "{http://www.w3.org/1999/xlink}href"


def text_of(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()


def table_lines(tw):
    out = []
    label = tw.findtext("label") or ""
    cap = tw.find("caption")
    out.append(f"[{label}] {text_of(cap) if cap is not None else ''}".strip())
    for tr in tw.iter("tr"):
        cells = [text_of(c) for c in tr if c.tag in ("td", "th")]
        out.append(" | ".join(cells))
    for fn in tw.iter("table-wrap-foot"):
        out.append("Table note: " + text_of(fn))
    return out


def walk_sec(sec, depth, out):
    title = sec.find("title")
    if title is not None:
        out.append("")
        out.append("#" * min(depth + 1, 4) + " " + text_of(title))
    for child in sec:
        tag = child.tag
        if tag == "p":
            # tables/figures nested in a paragraph are handled separately
            nested = [c for c in child if c.tag in ("table-wrap", "fig")]
            for c in nested:
                child.remove(c)
            t = text_of(child)
            if t:
                out.append(t)
            for c in nested:
                handle_float(c, out)
        elif tag == "sec":
            walk_sec(child, depth + 1, out)
        elif tag in ("table-wrap", "fig"):
            handle_float(child, out)
        elif tag in ("list",):
            for li in child.iter("list-item"):
                out.append("- " + text_of(li))


def handle_float(el, out):
    out.append("")
    if el.tag == "table-wrap":
        out.extend(table_lines(el))
    else:
        label = el.findtext("label") or "Figure"
        cap = el.find("caption")
        out.append(f"[{label}] {text_of(cap) if cap is not None else ''}")
    out.append("")


def convert(xml_path):
    root = ET.parse(xml_path).getroot()
    art = root if root.tag == "article" else root.find(".//article")
    front = art.find("front")
    meta = front.find("article-meta")
    out = []
    out.append("# " + text_of(meta.find(".//article-title")))
    journal = text_of(front.find(".//journal-title")) if front.find(".//journal-title") is not None else ""
    ids = {a.get("pub-id-type"): a.text for a in meta.findall("article-id")}
    year = meta.findtext(".//pub-date/year") or ""
    out.append(f"Journal: {journal} ({year}). DOI: {ids.get('doi', '')}. PMID: {ids.get('pmid', '')}. PMCID: PMC{str(ids.get('pmc', ids.get('pmcid', ''))).replace('PMC', '')}")
    affs = [re.sub(r"^\d+\s*", "", text_of(a)) for a in meta.iter("aff")]
    if affs:
        out.append("Affiliations: " + "; ".join(x for x in affs if x))
    lic = meta.find(".//permissions/license")
    if lic is not None:
        out.append("Licence: " + (lic.get(XLINK) or "") + " | " + text_of(lic))
    out.append("Changes: converted from the PubMed Central XML to plain text by activity/tools/pmc_to_text.py; "
               "author names, references, figure images and supplementary files omitted; tables flattened (cells separated by ' | ').")
    out.append("")
    for ab in meta.findall("abstract"):
        if ab.get("abstract-type") in ("graphical", "teaser", "plain-language-summary", "author-highlights"):
            continue
        out.append("## Abstract")
        secs = ab.findall("sec")
        if secs:
            for s in secs:
                t = s.find("title")
                body = " ".join(text_of(p) for p in s.findall("p"))
                out.append((text_of(t) + ": " if t is not None else "") + body)
        else:
            for p in ab.findall("p"):
                out.append(text_of(p))
    body = art.find("body")
    if body is not None:
        for child in body:
            if child.tag == "sec":
                walk_sec(child, 1, out)
            elif child.tag == "p":
                out.append(text_of(child))
            elif child.tag in ("table-wrap", "fig"):
                handle_float(child, out)
    # floats placed in <floats-group> (some publishers)
    fg = art.find("floats-group")
    if fg is not None:
        out.append("")
        out.append("## Tables and figures")
        for child in fg:
            if child.tag in ("table-wrap", "fig"):
                handle_float(child, out)
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        fh.write(convert(sys.argv[1]))
