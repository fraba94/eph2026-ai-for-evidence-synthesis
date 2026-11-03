"""Shared helpers for the workshop tools (standard library only).

Imported by the scripts in this folder; not meant to be run on its own.
"""
import csv
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

TOOLS = os.path.dirname(os.path.abspath(__file__))
ACTIVITY = os.path.dirname(TOOLS)
DATA = os.path.join(ACTIVITY, "data")
ANSWERS = os.path.join(ACTIVITY, "answers")
LOCAL = os.path.join(DATA, "local")  # git-ignored: files you fetch yourself (licences do not allow redistribution)
CONFIG = os.path.join(ACTIVITY, "review_config.yaml")

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TOOL_NAME = "eph2026_workshop"


# --------------------------------------------------------------------------- CSV
def read_csv(path, expect=None):
    """Read a CSV robustly and return a list of dicts with lower-case, stripped column names.

    Tolerates what comes back from chat assistants: a byte-order mark, ``` code fences, prose lines before the
    header or after the table, ';' or tab instead of ',', and unquoted commas in the last column (extra fields are
    joined back into the last column instead of being lost). `expect`: column names that identify the header line.
    """
    with open(path, encoding="utf-8-sig", errors="replace") as fh:
        text = fh.read().replace("\ufeff", "")
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("```")]
    expect = [e.lower() for e in (expect or [])]
    start = 0
    for i, ln in enumerate(lines):
        low = ln.lower()
        if expect and all(e in low for e in expect):
            start = i
            break
        if not expect and ln.strip():
            start = i
            break
    else:
        return []
    header_line = lines[start]
    delim = max([",", ";", "\t"], key=lambda d: header_line.count(d))
    rows = list(csv.reader(lines[start:], delimiter=delim))
    if not rows:
        return []
    header = [h.strip().strip('"').lower() for h in rows[0]]
    while header and not header[-1]:
        header.pop()
    out = []
    for r in rows[1:]:
        if not any(c.strip() for c in r):
            continue
        if len(r) == 1 and len(header) > 1 and delim not in r[0]:
            continue  # a prose line (e.g. "Let me know if you need more") or a stray note
        if len(r) > len(header):
            r = r[:len(header) - 1] + [delim.join(r[len(header) - 1:])]
        r = r + [""] * (len(header) - len(r))
        out.append({h: (v or "").strip() for h, v in zip(header, r) if h})
    return out


def write_csv(path, rows, columns):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in columns})


# --------------------------------------------------------------------------- YAML (small subset)
def load_yaml(path):
    """Load a YAML file. Uses PyYAML when installed, otherwise a small parser that understands
    the subset used in this repository: nested mappings, lists of scalars, lists of mappings,
    single- or double-quoted strings, plain scalars and # comments. No anchors, no block scalars."""
    try:
        import yaml  # type: ignore
        with open(path, encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except ImportError:
        pass
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    return _MiniYaml(lines).parse()


class _MiniYaml:
    def __init__(self, lines):
        self.items = []
        for raw in lines:
            line = _strip_comment(raw).rstrip()
            if not line.strip():
                continue
            indent = len(line) - len(line.lstrip(" "))
            self.items.append((indent, line.strip()))
        self.i = 0

    def parse(self):
        if not self.items:
            return {}
        return self._block(self.items[0][0])

    def _block(self, indent):
        if self.items[self.i][1].startswith("- ") or self.items[self.i][1] == "-":
            return self._list(indent)
        return self._map(indent)

    def _map(self, indent):
        out = {}
        while self.i < len(self.items):
            ind, text = self.items[self.i]
            if ind < indent:
                break
            if ind > indent:
                raise ValueError(f"unexpected indentation near: {text}")
            key, _, rest = text.partition(":")
            key = _scalar(key.strip())
            rest = rest.strip()
            self.i += 1
            if rest:
                out[key] = _scalar(rest)
            elif self.i < len(self.items) and self.items[self.i][0] > ind:
                out[key] = self._block(self.items[self.i][0])
            elif self.i < len(self.items) and self.items[self.i][0] == ind and self.items[self.i][1].startswith("- "):
                out[key] = self._list(ind)
            else:
                out[key] = None
        return out

    def _list(self, indent):
        out = []
        while self.i < len(self.items):
            ind, text = self.items[self.i]
            if ind < indent or not (text.startswith("- ") or text == "-"):
                break
            body = text[2:].strip() if text != "-" else ""
            if body and re.match(r"^[A-Za-z_][\w ]*:(\s|$)", body):
                # list item that is a mapping: re-insert the first pair at a deeper indent
                child_indent = ind + 2
                self.items[self.i] = (child_indent, body)
                out.append(self._map(child_indent))
            else:
                self.i += 1
                out.append(_scalar(body) if body else None)
        return out


def _strip_comment(line):
    out, q = [], None
    for ch in line:
        if q:
            out.append(ch)
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
            out.append(ch)
        elif ch == "#" and (not out or out[-1] in " \t"):
            break
        else:
            out.append(ch)
    return "".join(out)


def _scalar(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] == '"':
        return json.loads(s)
    if len(s) >= 2 and s[0] == s[-1] == "'":
        return s[1:-1].replace("''", "'")
    if s in ("null", "~", ""):
        return None
    if s in ("true", "True"):
        return True
    if s in ("false", "False"):
        return False
    if s.startswith("{") and s.endswith("}"):
        out = {}
        for part in _split_flow(s[1:-1].strip()):
            if part:
                k, _, v = part.partition(":")
                out[_scalar(k)] = _scalar(v)
        return out
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [_scalar(x) for x in _split_flow(inner)] if inner else []
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    return s


def _split_flow(s):
    parts, cur, q, depth = [], [], None, 0
    for ch in s:
        if q:
            cur.append(ch)
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
            cur.append(ch)
        elif ch in "[{":
            depth += 1
            cur.append(ch)
        elif ch in "]}":
            depth -= 1
            cur.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return [p.strip() for p in parts]


# --------------------------------------------------------------------------- text normalisation
_TRANS = {
    "‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-", "−": "-",
    "‘": "'", "’": "'", "‚": "'", "‛": "'", "′": "'",
    "“": '"', "”": '"', "„": '"', "″": '"',
    " ": " ", " ": " ", " ": " ", " ": " ", " ": " ",
    "·": ".", "•": "", "﻿": "",
}


def norm_text(s):
    """Lower-case, unify dashes/quotes/minus signs, unicode NFKC, collapse whitespace."""
    s = unicodedata.normalize("NFKC", s or "")
    s = "".join(_TRANS.get(ch, ch) for ch in s)
    s = s.lower()
    return re.sub(r"\s+", " ", s).strip()


def squash(s):
    """Form used to test whether a quote occurs in a paper: norm_text without any whitespace or
    table separators, so line breaks, hyphenation spaces and table layout do not matter."""
    s = norm_text(s)
    return re.sub(r"[\s|]+", "", s)


NOT_REPORTED_EXACT = {"nr", "n/r", "n.r", "na", "n/a", "n.a", "missing", "unclear", "none", "-", "--", "?", "unknown"}
NOT_REPORTED_PREFIX = ("not reported", "not stated", "not mentioned", "none reported", "not available", "not described",
                       "not specified", "not given", "not provided", "not applicable", "no data", "not found",
                       "no information", "information not", "not clearly reported", "not explicitly", "nr ", "nr:",
                       "nr(", "n/r ", "na ", "n/a ")


def is_not_reported(value):
    v = norm_text(value).strip(" .;:")
    v = re.sub(r"[_*]", "", v).strip()
    return v in NOT_REPORTED_EXACT or v.startswith(NOT_REPORTED_PREFIX)


def numbers_in(s):
    """All numbers in a string (handles 1,234 and 1.5 and -2)."""
    s = norm_text(s)
    out = []
    for m in re.finditer(r"(?<![\d.])-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![\d.])-?\d+(?:\.\d+)?", s):
        txt = m.group()
        if txt.startswith("-") and m.start() > 0 and s[m.start() - 1].isalnum():
            txt = txt[1:]  # a range such as 2010-2018 or 0.79-0.90, not a negative number
        out.append(float(txt.replace(",", "")))
    return out


# --------------------------------------------------------------------------- NCBI E-utilities
def http_get(url, tries=6, timeout=60):
    last = None
    for a in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": TOOL_NAME})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # network errors, 429 rate limits
            last = e
            time.sleep(2 + 3 * a)
    raise RuntimeError(f"could not fetch {url}: {last}")


def efetch(db, ids, **params):
    q = {"db": db, "id": ",".join(ids), "tool": TOOL_NAME}
    q.update(params)
    data = http_get(EUTILS + "efetch.fcgi?" + urllib.parse.urlencode(q))
    time.sleep(0.4)  # stay below 3 requests per second without an API key
    return data


def pubmed_records(pmids):
    """Fetch title, abstract, year, journal, doi, pmcid for a list of PMIDs."""
    out = {}
    pmids = [str(p) for p in pmids if str(p).strip()]
    for i in range(0, len(pmids), 100):
        root = ET.fromstring(efetch("pubmed", pmids[i:i + 100], retmode="xml"))
        for a in root.findall("PubmedArticle"):
            pmid = a.findtext(".//MedlineCitation/PMID")
            art = a.find(".//Article")
            title = re.sub(r"\s+", " ", "".join(art.find("ArticleTitle").itertext())).strip()
            parts = []
            for t in art.findall(".//Abstract/AbstractText"):
                lab = t.get("Label")
                txt = re.sub(r"\s+", " ", "".join(t.itertext())).strip()
                parts.append((lab + ": " if lab else "") + txt)
            ids = {x.get("IdType"): (x.text or "") for x in a.findall(".//PubmedData/ArticleIdList/ArticleId")}
            year = art.findtext(".//Journal/JournalIssue/PubDate/Year") or \
                (art.findtext(".//Journal/JournalIssue/PubDate/MedlineDate") or "")[:4]
            out[pmid] = {
                "pmid": pmid, "title": title, "abstract": " ".join(parts), "year": year,
                "journal": art.findtext(".//Journal/Title") or "", "doi": ids.get("doi", ""),
                "pmcid": ids.get("pmc", ""),
                "ptypes": [t.text for t in art.findall(".//PublicationTypeList/PublicationType")],
            }
    return out


_XLINK = "{http://www.w3.org/1999/xlink}href"


def classify_licence(href, text):
    t = (href + " " + text).lower()
    m = re.search(r"creativecommons\.org/licenses/(by[a-z-]*)/([\d.]+)", t)
    if m:
        return "CC " + m.group(1).upper() + " " + m.group(2)
    if "publicdomain/zero" in t:
        return "CC0"
    return "not open licence"


def pmc_licences(pmcids):
    """Licence of each PMC article, read from <permissions><license> in its PMC XML."""
    out = {}
    pmcids = [p for p in pmcids if p]
    for i in range(0, len(pmcids), 20):
        chunk = pmcids[i:i + 20]
        root = ET.fromstring(efetch("pmc", [p.replace("PMC", "") for p in chunk]))
        for art in root.iter("article"):
            pid = None
            for aid in art.iter("article-id"):
                if aid.get("pub-id-type") in ("pmc", "pmcid", "pmcaid") and aid.text:
                    v = aid.text.strip()
                    pid = v if v.startswith("PMC") else "PMC" + v
            lic = art.find(".//front//permissions/license")
            out[pid] = "not open licence" if lic is None else classify_licence(lic.get(_XLINK) or "", " ".join(lic.itertext()))
    return out


def redistributable(licence):
    """Abstract/full text may be shipped in the public repository: CC BY (any version) or CC0 only."""
    l = (licence or "").upper()
    return l == "CC0" or re.fullmatch(r"CC BY [\d.]+", l) is not None


def die(msg, code=2):
    print("error: " + msg, file=sys.stderr)
    sys.exit(code)
