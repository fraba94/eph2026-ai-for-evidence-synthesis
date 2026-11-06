#!/usr/bin/env python3
"""Build the website pages of docs/ from the Markdown guides of the repository.

The Markdown files stay the single source (agents and GitHub read them). This script turns them into pages
with the same header, navigation, footer and style as the rest of the site, so that participants never leave
the website:

    activity/README.md        -> docs/activity.html
    beginners/README.md       -> docs/beginners.html
    prompts/README.md         -> docs/prompts.html, and prompts/0N_*.md -> docs/prompts/0N_*.html
    skills/README.md          -> docs/skills.html,  skills/EXTERNAL.md -> docs/skills-external.html
    and a few pages linked from the activity guide (data, worksheets, quick card, facilitator guide)

It also writes two pages from the workshop data (papers.html: the full texts, the extraction prompt and the form;
answers.html: the reference answers behind a button), keeps the navigation bar of the hand-written pages (index,
start, batch, scorer, references) identical, and writes the ready-to-paste screening and extraction prompts into
start.html.

    pip install -r docs/requirements.txt   # python-markdown, the only dependency
    python3 docs/build_pages.py            # write the pages
    python3 docs/build_pages.py --check    # exit 1 if a page is out of date (used by the GitHub Action)

Rendering follows GitHub: heading ids are GitHub's slugs (the slides' QR codes link to them), alerts
(> [!NOTE] ...) become callouts, <details> blocks, tables, task lists and fenced code (with a Copy button) are
supported, and relative links point to the site page when there is one, otherwise to the file on GitHub.
"""
import argparse
import csv
import datetime as dt
import html
import posixpath
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

try:
    import markdown
except ImportError:  # pragma: no cover
    sys.exit("python-markdown is missing: pip install -r docs/requirements.txt")

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parent
REPO = "fraba94/eph2026-ai-for-evidence-synthesis"
GH_BLOB = f"https://github.com/{REPO}/blob/main/"
GH_TREE = f"https://github.com/{REPO}/tree/main/"
GH_RAW = f"https://raw.githubusercontent.com/{REPO}/main/"
SITE = "https://fraba94.github.io/eph2026-ai-for-evidence-synthesis/"

# ---------------------------------------------------------------- pages
# source (repository path) -> output (docs path), navigation item, eyebrow, short description
PAGES = [
    ("activity/README.md", "activity.html", "Activity", "Hands-on activity · step by step",
     "The guide to the hands-on exercise: timing, working on your own, tracks, eligibility criteria, the three steps, going further and the self-paced path."),
    ("beginners/README.md", "beginners.html", "Beginners", "Chat track · learning only",
     "A copy-and-paste walkthrough of the exercise for anyone with a chat assistant. For learning only."),
    ("prompts/README.md", "prompts.html", "Prompts", "Prompt library",
     "18 prompts for chat assistants in 6 review stages, each with what to check afterwards and common failure modes."),
    ("prompts/01_question_and_criteria.md", "prompts/01_question_and_criteria.html", "Prompts", "Prompt library · stage 1 of 6",
     "Prompts for turning a review question into PICO and explicit eligibility criteria."),
    ("prompts/02_search.md", "prompts/02_search.html", "Prompts", "Prompt library · stage 2 of 6",
     "Prompts for drafting, breaking and translating a database search strategy."),
    ("prompts/03_screening.md", "prompts/03_screening.html", "Prompts", "Prompt library · stage 3 of 6",
     "Prompts for title and abstract screening with a chat assistant: one batch, a second run, disagreements."),
    ("prompts/04_extraction.md", "prompts/04_extraction.html", "Prompts", "Prompt library · stage 4 of 6",
     "Prompts for data extraction from full texts, with verbatim quotes and locations."),
    ("prompts/05_verification.md", "prompts/05_verification.html", "Prompts", "Prompt library · stage 5 of 6",
     "Prompts for checking extracted values against the source: quotes, 'not reported', two runs."),
    ("prompts/06_synthesis_and_reporting.md", "prompts/06_synthesis_and_reporting.html", "Prompts", "Prompt library · stage 6 of 6",
     "Prompts for narrative synthesis, the discrepancy summary of the exercise and the AI-use statement."),
    ("skills/README.md", "skills.html", "Skills", "Agent track · skills",
     "Ten Claude Code skills for evidence reviews, with the human in charge: catalogue, install and safety notes."),
    ("skills/EXTERNAL.md", "skills-external.html", "Skills", "Agent track · external skill collections",
     "A curated list of external agent-skill collections for evidence synthesis, with a security note."),
    ("activity/data/README.md", "activity-data.html", "Activity", "Hands-on activity · the data",
     "How the workshop data were built, the reference review and its limits."),
    ("activity/worksheets/discrepancy_log.md", "worksheet-discrepancy-log.html", "Activity", "Hands-on activity · worksheet",
     "The discrepancy log to fill in step 3 of the exercise."),
    ("activity/worksheets/ai_use_record.md", "worksheet-ai-use-record.html", "Activity", "Hands-on activity · worksheet",
     "The AI use record: tool, model, version, date, prompts and checks."),
    ("activity/quick_card.md", "quick-card.html", "Activity", "Hands-on activity · printable card",
     "The one-page quick card of the exercise."),
    ("activity/facilitator_guide.md", "facilitator-guide.html", "Activity", "For facilitators · contains answers",
     "The facilitator guide. Contains answers: participants read it only after step 3."),
]
SRC_TO_OUT = {src: out for src, out, *_ in PAGES}
# repository paths that have an equivalent hand-written page
EXTRA_MAP = {"README.md": "index.html", "REFERENCES.md": "references.html", "README.md#useful-references": "references.html",
             # the papers, the form and the answers have their own pages; the worksheet CSV is copied into docs/data/
             "activity/data/papers.csv": "papers.html", "activity/data/fulltext/README.md": "papers.html",
             "activity/data/fulltext": "papers.html", "activity/data/extraction_form.csv": "papers.html#extraction-form",
             "activity/answers/README.md": "answers.html", "activity/answers": "answers.html",
             "activity/worksheets/discrepancy_log.csv": "data/worksheets/discrepancy_log.csv"}


def read_csv(rel):
    with open(ROOT / rel, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


PAPERS = read_csv("activity/data/papers.csv")
for _p in PAPERS:  # links to a full text go to its card on the Papers page
    EXTRA_MAP[_p["fulltext_file"]] = f"papers.html#{_p['study_id']}"

# the prompt stages, for the previous / next links
PROMPT_STAGES = [p for p in PAGES if p[0].startswith("prompts/0")]

NAV = [("Home", "index.html"), ("Start", "start.html"), ("Activity", "activity.html"), ("Beginners", "beginners.html"),
       ("Records", "batch.html"), ("Papers", "papers.html"), ("Prompts", "prompts.html"), ("Skills", "skills.html"), ("Scorer", "scorer.html"),
       ("References", "references.html")]
HAND_WRITTEN = {"index.html": "Home", "start.html": "Start", "batch.html": "Records", "scorer.html": "Scorer",
                "references.html": "References"}

ICONS = {
    "note": '<path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z"/><path d="M12 11v5.5M12 7.5v.01"/>',
    "tip": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.6 10.8c.7.6 1.1 1.3 1.1 2.2h5c0-.9.4-1.6 1.1-2.2A6 6 0 0 0 12 3z"/>',
    "important": '<path d="M4 5.5h16a1.5 1.5 0 0 1 1.5 1.5v9a1.5 1.5 0 0 1-1.5 1.5H10l-4.5 3.5V17.5H4A1.5 1.5 0 0 1 2.5 16V7A1.5 1.5 0 0 1 4 5.5z"/><path d="M12 8.5v4M12 15v.01"/>',
    "warning": '<path d="M12 3 2.5 20h19z"/><path d="M12 10v4.5M12 17.5v.01"/>',
    "caution": '<path d="M8.2 2.5h7.6l5.7 5.7v7.6l-5.7 5.7H8.2l-5.7-5.7V8.2z"/><path d="M12 7.5v5.5M12 16.5v.01"/>',
}
COPY_ICON = ('<rect x="8" y="8" width="12" height="12" rx="2"/>'
             '<path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3"/>')
ALERT_TITLES = {"note": "Note", "tip": "Tip", "important": "Important", "warning": "Warning", "caution": "Caution"}


def svg(paths, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{paths}</svg>')


# ---------------------------------------------------------------- GitHub-compatible slugs
def github_slug(text):
    """GitHub's heading anchor: lowercase, drop punctuation (keep letters, digits, '-', '_', spaces), spaces -> '-'."""
    text = text.strip().lower()
    out = []
    for ch in text:
        cat = unicodedata.category(ch)
        if ch in " -_" or cat[0] in "LN" or cat in ("Mn", "Mc"):
            out.append(ch)
    return "".join(out).replace(" ", "-")


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


# ---------------------------------------------------------------- Markdown -> HTML (GitHub flavour)
TOKEN = "QQBLOCK{}QQ"
TOKEN_RE = re.compile(r"QQBLOCK(\d+)QQ")
FENCE_RE = re.compile(r"^( *)(`{3,}|~{3,})\s*([\w+-]*)[^\n]*$")
ITEM_RE = re.compile(r"^( *)([-*+]|\d{1,9}[.)])( {1,4})(\S.*)?$")
ALERT_RE = re.compile(r"^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$", re.I)


class Renderer:
    def __init__(self, src_rel, out_rel):
        self.src_rel = src_rel
        self.out_rel = out_rel
        self.blocks = []
        self.prompt_page = src_rel.startswith(("prompts/", "beginners/"))

    def stash(self, block_html):
        self.blocks.append(block_html)
        return TOKEN.format(len(self.blocks) - 1)

    # --- code blocks: rendered here, so that they also work inside lists
    def code_html(self, lang, code):
        lang = (lang or "").lower()
        if lang in ("bash", "sh", "shell", "console"):
            label, copy = "Terminal", "Copy"
        elif lang in ("text", "") and self.prompt_page:
            label, copy = "Prompt", "Copy prompt"
        else:
            label, copy = (lang or "text").capitalize(), "Copy"
        cls = f' class="language-{html.escape(lang)}"' if lang else ""
        return (f'<div class="codeblock"><div class="codebar"><span class="lang">{label}</span>'
                f'<button class="copy" type="button" data-label="{copy}">'
                f'{svg(COPY_ICON)}'
                f'<span>{copy}</span></button></div><pre><code{cls}>{html.escape(code)}</code></pre></div>')

    def extract_fences(self, lines):
        out, i = [], 0
        while i < len(lines):
            m = FENCE_RE.match(lines[i])
            if not m:
                out.append(lines[i])
                i += 1
                continue
            indent, marker, lang = len(m.group(1)), m.group(2), m.group(3)
            body, i = [], i + 1
            while i < len(lines) and not re.match(r"^ *" + re.escape(marker[0]) + "{" + str(len(marker)) + r",}\s*$", lines[i]):
                ln = lines[i]
                body.append(ln[indent:] if ln[:indent].strip() == "" else ln.lstrip())
                i += 1
            i += 1  # closing fence
            tok = self.stash(self.code_html(lang, "\n".join(body)))
            out += ["", " " * indent + tok, ""]
        return out

    # --- blockquotes: GitHub alerts and the "For learning only" warning become callouts
    def extract_quotes(self, lines):
        out, i = [], 0
        while i < len(lines):
            if not re.match(r"^ {0,3}>", lines[i]):
                out.append(lines[i])
                i += 1
                continue
            group = []
            while i < len(lines) and re.match(r"^ {0,3}>", lines[i]):
                group.append(re.sub(r"^ {0,3}> ?", "", lines[i]))
                i += 1
            first = group[0].strip()
            m = ALERT_RE.match(first)
            if m:
                kind = m.group(1).lower()
                inner = self.render_fragment("\n".join(group[1:]))
                title = f'<p class="md-alert-title">{svg(ICONS[kind])}{ALERT_TITLES[kind]}</p>'
                out += ["", self.stash(f'<div class="md-alert md-alert-{kind}">{title}{inner}</div>'), ""]
            elif first.startswith("⚠️") or first.startswith("⚠"):
                group[0] = re.sub(r"^\s*⚠️?\s*", "", group[0])
                inner = self.render_fragment("\n".join(group))
                out += ["", self.stash(f'<div class="md-alert md-alert-warning md-alert-plain">{svg(ICONS["warning"], "md-alert-icon")}<div>{inner}</div></div>'), ""]
            else:
                inner = self.render_fragment("\n".join(group))
                out += ["", self.stash(f"<blockquote>{inner}</blockquote>"), ""]
        return out

    # --- lists: GitHub allows lists right after a paragraph and 2-3 space nesting; python-markdown wants
    #     a blank line and 4 spaces. Re-indent every list line to multiples of 4.
    @staticmethod
    def normalise_lists(lines):
        out, stack, prev = [], [], ""
        for raw in lines:
            line = raw.expandtabs(4)
            if not line.strip():
                out.append("")
                prev = ""
                continue
            indent = len(line) - len(line.lstrip(" "))
            m = ITEM_RE.match(line)
            if m and not re.match(r"^ *([-*_])( *\1){2,} *$", line):
                while stack and indent < stack[-1]:
                    stack.pop()
                if indent >= 4 * (len(stack) + 1) and not stack:  # indented code, not a list
                    out.append(line)
                    prev = line
                    continue
                if not stack and prev.strip() and not ITEM_RE.match(prev):
                    out.append("")  # list right after a paragraph
                depth = len(stack)
                stack.append(indent + len(m.group(2)) + len(m.group(3)))
                out.append(" " * (4 * depth) + m.group(2) + " " + (m.group(4) or ""))
            elif stack:
                depth = sum(1 for c in stack if indent >= c)
                if depth == 0:
                    if prev == "":  # the list is over
                        stack = []
                        out.append(line)
                    else:          # lazy continuation of the item's paragraph
                        out.append(" " * (4 * (len(stack) - 1)) + line.lstrip())
                else:
                    del stack[depth:]
                    out.append(" " * (4 * depth) + line.lstrip())
            else:
                # a table right after a paragraph needs a blank line in python-markdown
                if line.lstrip().startswith("|") and prev.strip() and not prev.lstrip().startswith("|"):
                    out.append("")
                out.append(line)
            prev = line
        return out

    @staticmethod
    def mark_details(lines):
        out = []
        for ln in lines:
            m = re.match(r"^\s*<details(\s[^>]*)?>\s*$", ln)
            if m:
                out.append(f'<details{m.group(1) or ""} markdown="1">')
            else:
                out.append(ln)
        return out

    def render_fragment(self, text):
        lines = text.replace("\r\n", "\n").split("\n")
        lines = self.extract_fences(lines)
        lines = self.extract_quotes(lines)
        lines = self.mark_details(lines)
        lines = self.normalise_lists(lines)
        md = markdown.Markdown(extensions=["tables", "md_in_html", "sane_lists"], output_format="html")
        out = md.convert("\n".join(lines))
        return self.post_fragment(out)

    def post_fragment(self, h):
        # task lists: a real checkbox (pages.js remembers ticks in this browser)
        def task(m):
            checked = " checked" if m.group(3).lower() == "x" else ""
            return f'<li class="task-item">{m.group(2) or ""}<input type="checkbox" class="task-box"{checked}> '
        h = re.sub(r'<li>((\s*<p>)?)\[([ xX])\]\s+', task, h)
        # tables: 3+ columns become stacked cards on phones (each cell labelled with its column header),
        # worksheets and 2-column tables scroll sideways inside their frame
        stack = not self.src_rel.startswith("activity/worksheets/")
        return re.sub(r"<table>.*?</table>", lambda m: self.table(m.group(0), stack), h, flags=re.S)

    @staticmethod
    def table(t, stack):
        heads = [html.escape(strip_tags(x).strip(), quote=True) for x in re.findall(r"<th[^>]*>(.*?)</th>", t, re.S)]
        cls = "table-wrap md-table"
        if stack and len(heads) >= 3:
            cls += " stack"

            def row(m):
                i = iter(heads + [""] * 50)
                return re.sub(r"<td(\s[^>]*)?>", lambda c: f'<td{c.group(1) or ""} data-label="{next(i)}">', m.group(0))
            t = re.sub(r"<tr>.*?</tr>", row, t, flags=re.S)
        return f'<div class="{cls}">{t}</div>'

    def render(self, text):
        h = self.render_fragment(text)
        # put the stashed blocks back (they may contain tokens themselves)
        for _ in range(5):
            if not TOKEN_RE.search(h):
                break
            h = re.sub(r"<p>\s*QQBLOCK(\d+)QQ\s*</p>", lambda m: self.blocks[int(m.group(1))], h)
            h = TOKEN_RE.sub(lambda m: self.blocks[int(m.group(1))], h)
        h = self.headings(h)
        h = self.links(h)
        h = linkify(h)
        return h

    # --- headings: GitHub slugs, a hover anchor, and the table of contents
    def headings(self, h):
        seen, self.toc, self.title = {}, [], None

        def repl(m):
            level, inner = int(m.group(1)), m.group(2)
            text = strip_tags(inner).strip()
            base = github_slug(text)
            n = seen.get(base, 0)
            seen[base] = n + 1
            hid = base if n == 0 else f"{base}-{n}"
            if level == 1 and self.title is None:
                self.title = (hid, inner, text)
                return "<!--H1-->"
            if level == 2:
                self.toc.append((hid, text))
            return (f'<h{level} id="{hid}">{inner}<a class="anchor" href="#{hid}" '
                    f'aria-label="Link to this section">#</a></h{level}>')
        h = re.sub(r"<h([1-6])>(.*?)</h\1>", repl, h, flags=re.S)
        return h.replace("<!--H1-->", "", 1)

    # --- links and images
    def resolve(self, url, kind="a"):
        if not url or url.startswith(("#", "mailto:", "data:", "javascript:")):
            return url
        if url.startswith(SITE):
            rest = url[len(SITE):] or "index.html"
            return rel_link(self.out_rel, rest)
        if url.startswith(GH_BLOB) or url.startswith(GH_TREE):
            path, _, anchor = url.split("/main/", 1)[1].partition("#")
            target = self.site_target(path, anchor)
            return rel_link(self.out_rel, target) if target else url
        if re.match(r"^[a-z][a-z0-9+.-]*:", url, re.I) or url.startswith("//"):
            return url
        path, _, anchor = url.partition("#")
        repo_path = posixpath.normpath(posixpath.join(posixpath.dirname(self.src_rel), path)) if path else self.src_rel
        if repo_path.startswith(".."):
            return url
        if kind == "img":
            if repo_path.startswith("assets/") and (DOCS / repo_path).exists():
                return rel_link(self.out_rel, repo_path)
            return GH_RAW + repo_path
        target = self.site_target(repo_path, anchor)
        if target:
            return rel_link(self.out_rel, target)
        is_dir = (ROOT / repo_path).is_dir() or path.endswith("/")
        return (GH_TREE if is_dir else GH_BLOB) + repo_path.rstrip("/") + (f"#{anchor}" if anchor else "")

    @staticmethod
    def site_target(repo_path, anchor):
        repo_path = repo_path.rstrip("/")
        if (ROOT / repo_path).is_dir() and f"{repo_path}/README.md" in SRC_TO_OUT:
            repo_path = f"{repo_path}/README.md"
        key = f"{repo_path}#{anchor}" if anchor else repo_path
        if key in EXTRA_MAP:
            return EXTRA_MAP[key]
        if repo_path in SRC_TO_OUT:
            return SRC_TO_OUT[repo_path] + (f"#{anchor}" if anchor else "")
        if repo_path in EXTRA_MAP and not anchor:
            return EXTRA_MAP[repo_path]
        return None

    def links(self, h):
        def a(m):
            new = self.resolve(html.unescape(m.group(2)), "a")
            return f'{m.group(1)}"{html.escape(new, quote=True)}"'
        h = re.sub(r'(<a\s[^>]*?href=)"([^"]*)"', a, h)

        def img(m):
            new = self.resolve(html.unescape(m.group(2)), "img")
            return f'{m.group(1)}"{html.escape(new, quote=True)}"'
        h = re.sub(r'(<(?:img|source)\s[^>]*?(?:src|srcset)=)"([^"]*)"', img, h)
        return h


def linkify(h):
    """Bare URLs become links, as on GitHub (not inside <a>, <code>, <pre>)."""
    parts = re.split(r"(<[^>]+>)", h)
    depth = {"a": 0, "code": 0, "pre": 0}
    url_re = re.compile(r"(?<![\"'=/\w])(https?://[^\s<>\"']+)")
    for i, p in enumerate(parts):
        if p.startswith("<"):
            m = re.match(r"<(/?)(a|code|pre)\b", p)
            if m:
                depth[m.group(2)] += -1 if m.group(1) else 1
            continue
        if any(depth.values()) or "http" not in p:
            continue

        def repl(m):
            url = m.group(1)
            trail = ""
            while url and url[-1] in ".,;:)":
                if url[-1] == ")" and url.count("(") >= url.count(")"):
                    break
                trail = url[-1] + trail
                url = url[:-1]
            return f'<a href="{url}">{url}</a>{trail}'
        parts[i] = url_re.sub(repl, p)
    return "".join(parts)


def rel_link(from_out, to_target):
    """Relative link from one docs page to another docs path (keeps #anchor)."""
    path, _, anchor = to_target.partition("#")
    rel = posixpath.relpath(path, posixpath.dirname(from_out) or ".") if path else ""
    return rel + (f"#{anchor}" if anchor else "")


# ---------------------------------------------------------------- git dates
def last_updated(src_rel):
    try:
        dirty = subprocess.run(["git", "status", "--porcelain", "--", src_rel], cwd=ROOT, capture_output=True,
                               text=True, timeout=20).stdout.strip()
        if dirty:
            return dt.date.today()
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", src_rel], cwd=ROOT, capture_output=True,
                             text=True, timeout=20).stdout.strip()
        return dt.date.fromisoformat(out) if out else None
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def human_date(d):
    return f"{d.day} {d.strftime('%B')} {d.year}"


# ---------------------------------------------------------------- page shell
def nav_html(current, root):
    items = []
    for label, href in NAV:
        cur = ' aria-current="page"' if label == current else ""
        items.append(f'      <a href="{root}{href}"{cur}>{label}</a>')
    return '<nav class="nav" aria-label="Main">\n' + "\n".join(items) + "\n    </nav>"


def header_html(current, root):
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <div class="wrap">
    <a class="brand" href="{root}index.html"><img src="{root}assets/eupha-dhai-logo.png" alt="EUPHA Digital Health and Artificial Intelligence section logo"><span>AI for evidence synthesis<small>EPH 2026 · Bilbao · M.8</small></span></a>
    {nav_html(current, root)}
  </div>
</header>"""


def footer_html(root):
    return f"""<footer>
  <div class="wrap">
    <span>EUPHA Digital Health and Artificial Intelligence Section · <a href="mailto:euphadhai@gmail.com">euphadhai@gmail.com</a></span>
    <span><a href="https://github.com/{REPO}">Repository</a> · <a href="{root}references.html">References</a> · Content <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> · Code <a href="{GH_BLOB}LICENSE-CODE">MIT</a></span>
  </div>
</footer>"""


GITHUB_ICON = '<path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>'


def build_page(src_rel, out_rel, nav_item, eyebrow, description):
    text = (ROOT / src_rel).read_text(encoding="utf-8")
    r = Renderer(src_rel, out_rel)
    root = "../" * out_rel.count("/")
    body = inject_blocks(r.render(text), root)
    body = worksheet_tools(src_rel, root) + body
    hid, title_html, title_text = r.title or ("", html.escape(Path(src_rel).stem), Path(src_rel).stem)

    if src_rel.startswith("prompts/0"):
        eyebrow_html = f'<a href="{root}prompts.html">Prompt library</a> · {eyebrow.split(" · ", 1)[1]}'
    elif out_rel == "skills-external.html":
        eyebrow_html = f'<a href="skills.html">Agent skills</a> · external collections'
    elif nav_item == "Activity" and out_rel != "activity.html":
        eyebrow_html = f'<a href="{root}activity.html">Hands-on activity</a> · {eyebrow.split(" · ", 1)[1]}'
    else:
        eyebrow_html = html.escape(eyebrow)

    d = last_updated(src_rel)
    updated = (f'<span class="updated">Last updated <time datetime="{d.isoformat()}">{human_date(d)}</time></span>'
               if d else "")
    meta = (f'<p class="page-meta"><a href="{GH_BLOB}{src_rel}">{svg(GITHUB_ICON)}View source on GitHub</a>'
            f'{updated}</p>')

    toc = ""
    if len(r.toc) >= 3:
        links = "\n".join(f'        <li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in r.toc)
        toc = f"""<details class="toc" open>
      <summary>On this page</summary>
      <ol>
{links}
      </ol>
    </details>"""

    pager = ""
    if src_rel.startswith("prompts/0"):
        idx = [p[0] for p in PROMPT_STAGES].index(src_rel)
        prev = PROMPT_STAGES[idx - 1] if idx > 0 else None
        nxt = PROMPT_STAGES[idx + 1] if idx + 1 < len(PROMPT_STAGES) else None

        def stage_title(p):
            first = (ROOT / p[0]).read_text(encoding="utf-8").split("\n", 1)[0]
            return html.escape(first.lstrip("# ").strip())
        cells = []
        cells.append(f'<a class="prev" href="{posixpath.basename(prev[1])}"><small>Previous stage</small>{stage_title(prev)}</a>'
                     if prev else f'<a class="prev" href="{root}prompts.html"><small>Back to</small>All prompts</a>')
        cells.append(f'<a class="next" href="{posixpath.basename(nxt[1])}"><small>Next stage</small>{stage_title(nxt)}</a>'
                     if nxt else f'<a class="next" href="{root}prompts.html"><small>Back to</small>All prompts</a>')
        pager = '<nav class="pager" aria-label="Prompt stages">' + "".join(cells) + "</nav>"

    robots = '\n  <meta name="robots" content="noindex">' if "facilitator" in out_rel else ""
    page_title = html.escape(title_text)
    return f"""<!doctype html>
<!-- Generated by docs/build_pages.py from {src_rel}. Do not edit: change the Markdown and run the script. -->
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{page_title} · AI for evidence synthesis</title>
  <meta name="description" content="{html.escape(description, quote=True)}">{robots}
  <meta name="color-scheme" content="light dark">
  <link rel="icon" href="{root}assets/eupha-dhai-logo.png">
  <link rel="stylesheet" href="{root}assets/site.css">
</head>
<body class="doc-page">
{header_html(nav_item, root)}

<div class="page-head">
  <div class="wrap">
    <div class="eyebrow">{eyebrow_html}</div>
    <h1 id="{hid}">{title_html}</h1>
    {meta}
  </div>
</div>

<main id="main">
  <div class="wrap doc-layout{' has-toc' if toc else ''}">
    {toc}
    <article class="md">
{body}
{pager}
    </article>
  </div>
</main>

{footer_html(root)}
<script src="{root}assets/pages.js"></script>
</body>
</html>
"""


# ---------------------------------------------------------------- the extraction prompt, the Papers and Answers pages
# The short extraction of step 3: five of the core fields of activity/data/extraction_form.csv (the same list is in
# docs/scorer.js, SHORT_FIELDS, and in the Markdown guides). The 11 core fields are the "going further" version.
SHORT_FIELDS = ["country", "study_design", "intervention_components", "primary_hai_outcome", "direction_of_effect"]
COPY_BTN_ICON = svg(COPY_ICON)
LINK_ICON = '<path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>'
DOWN_ICON = '<path d="M12 4v12M7 11l5 5 5-5M4 20h16"/>'
EYE_ICON = '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>'
STOP_ICON = '<path d="M8.2 2.5h7.6l5.7 5.7v7.6l-5.7 5.7H8.2l-5.7-5.7V8.2z"/><path d="M8.5 8.5l7 7M15.5 8.5l-7 7"/>'
LICENCE_URL = {"CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/",
               "CC BY-NC 3.0": "https://creativecommons.org/licenses/by-nc/3.0/"}
# who works on which paper (not a column of papers.csv: the plan of the session)
AUDIENCE = {
    "Phan2020": ("Chat track · step 3", "The paper of the short extraction in the live session (step 3). Agent track: one of its three papers."),
    "Mestre2012": ("Live demo, then practice at home", "Used in the live demo. After the session it is free for practice on your own: same prompt, study_id Mestre2012."),
    "AlKuwaiti2017": ("Agent track · going further", "Not on this site: its licence (CC BY-NC) does not allow redistribution. The agent track downloads it to the computer with the command below, or reads it in PubMed Central."),
}


def form_rows():
    return read_csv("activity/data/extraction_form.csv")


def field_lines(fields):
    rows = {r["field"]: r for r in form_rows()}
    out = []
    for f in fields:
        if f not in rows:
            raise SystemExit(f"field {f} is not in activity/data/extraction_form.csv")
        r = rows[f]
        d = r["definition"].strip()
        d = d if d.endswith(".") else d + "."
        out.append(f"- {f}: {d} Allowed values: {r['allowed_values'].strip()}.")
    return "\n".join(out)


def core_fields():
    core = [r["field"] for r in form_rows() if r.get("core", "").strip().lower() == "yes"]
    if len(core) != 11:
        raise SystemExit(f"expected 11 core fields in extraction_form.csv, found {len(core)}: update the guides")
    return core


PAPER_PLACEHOLDER_RE = re.compile(r"\[PASTE THE TEXT OF THE PAPER[^\]]*\]")


def extraction_prompt(study_id="Phan2020", which="short"):
    """The extraction prompt of the beginners walkthrough with the form fields and the study_id filled in."""
    beg = (ROOT / "beginners/README.md").read_text(encoding="utf-8")
    m = re.search(r"```text\n((?:(?!```).)*?EXTRACTION FORM.*?)\n```", beg, re.S)
    if not m:
        raise SystemExit("could not find the extraction prompt (```text block with EXTRACTION FORM) in beginners/README.md")
    prompt = m.group(1)
    fields = SHORT_FIELDS if which == "short" else core_fields()
    ph = re.search(r"\[PASTE THE [^\]]*FIELDS[^\]]*\]", prompt)
    if not ph:
        raise SystemExit("the extraction prompt in beginners/README.md has no [PASTE THE ... FIELDS ...] placeholder")
    prompt = prompt.replace(ph.group(0), field_lines(fields))
    prompt = re.sub(r"\[[^\]\n]*Phan2020[^\]\n]*\]", study_id, prompt)
    if not PAPER_PLACEHOLDER_RE.search(prompt):
        raise SystemExit("the extraction prompt in beginners/README.md has no [PASTE THE TEXT OF THE PAPER ...] placeholder")
    return prompt


def paper_placeholder():
    return PAPER_PLACEHOLDER_RE.search(extraction_prompt()).group(0)


def copy_button(target, label, cls="btn-copy", extra=""):
    return (f'<button class="{cls}" type="button" data-copy="{target}"{extra}>{COPY_BTN_ICON}'
            f'<span>{html.escape(label)}</span></button>')


def pre_block(pid, text, hidden=False):
    h = " hidden" if hidden else ""
    return f'<pre id="{pid}"{h}><code>{html.escape(text)}</code></pre>'


def ready_prompt_html(root, pid="extraction-prompt-text", which="short", paper_button=True, intro=True):
    n = len(SHORT_FIELDS) if which == "short" else len(core_fields())
    names = ", ".join(f"<code>{f}</code>" for f in (SHORT_FIELDS if which == "short" else core_fields()))
    ph = html.escape(paper_placeholder())
    title = (f'<p class="ready-title"><b>Ready to paste: the extraction prompt</b> with the {n} fields '
             f'({names}) and <code>study_id = Phan2020</code> already filled in. In a new temporary chat with web search off, paste it, then paste '
             f'the paper where it says <code>{ph}</code>.</p>') if intro else ""
    paper = (f'<a class="btn btn-plain" href="{root}papers.html#Phan2020">Open the paper (Phan2020)</a>'
             if paper_button else "")
    return (f'<div class="ready-prompt">{title}<div class="row">{copy_button("#" + pid, "Copy the extraction prompt")}{paper}</div>'
            f'<details><summary>Show the prompt</summary>{pre_block(pid, extraction_prompt(which=which))}</details></div>')


def inject_blocks(body, root):
    """<!-- build_pages:extraction-prompt --> in a Markdown guide becomes the ready-to-paste prompt."""
    return re.sub(r"(?:<p>)?\s*<!-- build_pages:extraction-prompt -->\s*(?:</p>)?",
                  lambda m: ready_prompt_html(root), body)


WORKSHEETS = {  # worksheet page source -> the templates copied into docs/data/worksheets/ by sync_data.py
    "activity/worksheets/discrepancy_log.md": ["discrepancy_log.md", "discrepancy_log.csv"],
    "activity/worksheets/ai_use_record.md": ["ai_use_record.md"],
}


def worksheet_tools(src_rel, root):
    files = WORKSHEETS.get(src_rel)
    if not files:
        return ""
    md_name = files[0]
    text = (ROOT / "activity/worksheets" / md_name).read_text(encoding="utf-8")
    btns = []
    for f in files:
        ext = f.rsplit(".", 1)[1]
        btns.append(f'<a class="btn btn-plain" href="{root}data/worksheets/{f}" download="{f}">{svg(DOWN_ICON)}'
                    f'Download template (.{ext})</a>')
    btns.insert(0, copy_button("#worksheet-template", "Copy template"))
    return (f'<div class="worksheet-tools"><p><b>Optional, going further.</b> Fill it on paper, in a text editor or a '
            f'spreadsheet: copy the template or download it.</p><div class="row">{"".join(btns)}</div>'
            f'{pre_block("worksheet-template", text, hidden=True)}</div>\n')


def page_shell(out_rel, nav_item, title, description, eyebrow_html, lede_html, body, robots=False, scripts=()):
    root = "../" * out_rel.count("/")
    rob = '\n  <meta name="robots" content="noindex">' if robots else ""
    js = "\n".join(f'<script src="{root}{s}"></script>' for s in ("assets/pages.js",) + tuple(scripts))
    return f"""<!doctype html>
<!-- Generated by docs/build_pages.py. Do not edit: change the sources it names and run the script. -->
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} · AI for evidence synthesis</title>
  <meta name="description" content="{html.escape(description, quote=True)}">{rob}
  <meta name="color-scheme" content="light dark">
  <link rel="icon" href="{root}assets/eupha-dhai-logo.png">
  <link rel="stylesheet" href="{root}assets/site.css">
</head>
<body class="doc-page tool-page">
{header_html(nav_item, root)}

<div class="page-head">
  <div class="wrap">
    <div class="eyebrow">{eyebrow_html}</div>
    <h1>{html.escape(title)}</h1>
    {lede_html}
  </div>
</div>

<main id="main">
  <div class="wrap tool-wrap">
{body}
  </div>
</main>

{footer_html(root)}
{js}
</body>
</html>
"""


def md_snippet(src_rel, out_rel, text):
    return Renderer(src_rel, out_rel).render(text)


def split_citation(cit):
    parts = [x.strip() for x in cit.split(". ")]
    authors, journal, vol = parts[0], parts[-2], parts[-1].rstrip(".")
    title = ". ".join(parts[1:-2])
    names = [a.strip() for a in authors.split(",") if a.strip()]
    first = names[0] + (" et al." if len(names) > 1 else "")
    return first, title, journal, vol


def build_papers():
    out = "papers.html"
    form = form_rows()
    cards, who = [], []
    for p in PAPERS:
        sid = p["study_id"]
        first, title, journal, vol = split_citation(p["citation"])
        badge, why = AUDIENCE.get(sid, ("", ""))
        lic = p["licence"].strip()
        lic_html = f'<a href="{LICENCE_URL[lic]}">{html.escape(lic)}</a>' if lic in LICENCE_URL else html.escape(lic)
        shipped = p.get("shipped", "").strip().lower() == "yes"
        who.append(f'<li><a href="#{sid}"><b>{sid}</b></a> <span>{html.escape(badge)}</span></li>')
        cite = (f'<p class="cite">{html.escape(first)} <i>{html.escape(journal)}</i> {html.escape(vol)}. '
                f'doi:<a href="{html.escape(p["doi_url"])}">{html.escape(p["doi"])}</a> · '
                f'PMID <a href="{html.escape(p["pubmed_url"])}">{html.escape(p["pmid"])}</a> · {html.escape(p["pmcid"])}</p>')
        meta = (f'<p class="paper-meta"><span class="pill">{html.escape(badge)}</span> <span>Licence {lic_html}</span> '
                f'<span><code>study_id = {sid}</code></span></p>')
        open_btn = (f'<a class="btn btn-plain" href="{html.escape(p["pmc_url"])}" target="_blank" rel="noopener">'
                    f'{svg(LINK_ICON)}Open original (PMC)</a>')
        if shipped:
            text = (ROOT / p["fulltext_file"]).read_text(encoding="utf-8")
            words = len(text.split())
            combo_id = f"prompt-{sid}"
            fill = f' data-fill="#text-{sid}" data-placeholder="{html.escape(paper_placeholder(), quote=True)}"'
            body = (f'<div class="row">{copy_button("#text-" + sid, "Copy full text")}'
                    f'<a class="btn btn-plain" href="data/fulltext/{sid}.txt" download="{sid}.txt">{svg(DOWN_ICON)}Download .txt</a>'
                    f'{open_btn}</div>'
                    f'<p class="hint">{words:,} words, plain text from PubMed Central (tables flattened, figures as captions only). '
                    f'One tap for the whole step: '
                    f'{copy_button("#" + combo_id, "Copy prompt + this paper", "btn-link", fill)}'
                    f' (the short extraction prompt with the paper already pasted in).</p>'
                    f'{pre_block(combo_id, extraction_prompt(study_id=sid), hidden=True)}'
                    f'<details class="box fulltext"><summary>{svg(EYE_ICON)}Show text</summary>'
                    f'<pre id="text-{sid}"><code>{html.escape(text)}</code></pre></details>')
        else:
            body = (f'<div class="row">{open_btn}</div>'
                    f'<div class="codeblock"><div class="codebar"><span class="lang">Terminal</span>'
                    f'<button class="copy" type="button" data-label="Copy">{COPY_BTN_ICON}<span>Copy</span></button></div>'
                    f'<pre><code>python3 activity/tools/fetch_fulltext.py</code></pre></div>')
        cards.append(f'<article class="card paper" id="{sid}">{meta}<h2>{html.escape(title)}</h2>{cite}'
                     f'<p class="why">{html.escape(why)}</p>{body}</article>')

    rows = "".join(
        f'<tr><td data-label="Field"><code>{html.escape(r["field"])}</code></td>'
        f'<td data-label="Definition">{html.escape(r["definition"])}</td>'
        f'<td data-label="Allowed values">{html.escape(r["allowed_values"])}</td>'
        f'<td data-label="Used in">{"step 3 (short extraction)" if r["field"] in SHORT_FIELDS else ("core (going further)" if r.get("core") == "yes" else "all 19 (agent track)")}</td></tr>'
        for r in form)
    fulltext_readme = (ROOT / "activity/data/fulltext/README.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Attribution and changes\.\*\*.*?(?=\n\n|\Z)", fulltext_readme, re.S)
    attribution = md_snippet("activity/data/fulltext/README.md", out, m.group(0)) if m else ""

    body = f"""    <ul class="who-list" aria-label="Who uses which paper">
      {''.join(who)}
    </ul>

    <section class="tool-sec" id="extraction-prompt" aria-labelledby="h-prompt">
      <h2 id="h-prompt">Step 3 · The extraction prompt</h2>
      <p>The prompt of the <a href="beginners.html">walkthrough</a> with the {len(SHORT_FIELDS)} fields of the short extraction and their definitions already filled in.</p>
      <ol class="mini-steps">
        <li>Open a <b>new temporary chat</b> (web search off), copy the prompt and paste it.</li>
        <li>Copy the full text of <a href="#Phan2020">Phan2020</a> and paste it where it says <code>{html.escape(paper_placeholder())}</code>. Or use <b>Copy prompt + this paper</b> in the paper's card: one paste.</li>
        <li>Check 2 quotes yourself with Ctrl+F in the paper (<b>Show text</b>, or the .txt file).</li>
        <li>Compare with the reference values on the <a href="answers.html#extraction">answers page</a>, or paste the answer into the <a href="scorer.html#extraction">scorer</a>.</li>
      </ol>
      {ready_prompt_html("", paper_button=False, intro=False)}
    </section>

    <section class="tool-sec" id="papers" aria-labelledby="h-papers">
      <h2 id="h-papers">The papers</h2>
      {''.join(cards)}
      <div class="attribution hint">{attribution}</div>
    </section>

    <section class="tool-sec" id="going-further" aria-labelledby="h-further">
      <h2 id="h-further">Going further: the 11 core fields</h2>
      <p>The longer version of the same prompt, with the 11 core fields of the form. Use it at home, or after the session.</p>
      {ready_prompt_html("", pid="extraction-prompt-core", which="core", paper_button=False, intro=False)}
    </section>

    <section class="tool-sec" id="extraction-form" aria-labelledby="h-form">
      <h2 id="h-form">The extraction form</h2>
      <p>{len(form)} fields; the {len(SHORT_FIELDS)} of the short extraction are part of the {len(core_fields())} core fields. Read the definitions before you give the paper to the AI. <a href="data/extraction_form.csv" download="extraction_form.csv">Download the form (.csv)</a></p>
      <div class="md"><div class="table-wrap md-table stack"><table><thead><tr><th>Field</th><th>Definition</th><th>Allowed values</th><th>Used in</th></tr></thead><tbody>{rows}</tbody></table></div></div>
    </section>"""
    lede = ('<p>The full texts for the extraction, ready to copy into your chat assistant or to download, and the '
            'extraction prompt with the fields already filled in. Chat track: <a href="#Phan2020">Phan2020</a>.</p>')
    return page_shell(out, "Papers", "Papers for data extraction",
                      "The open-access full texts of the extraction exercise (copy, download, show), the ready-to-paste extraction prompt and the extraction form.",
                      'Hands-on activity · <a href="activity.html#step-3--short-extraction-10-min">step 3</a>', lede, body)


def build_answers():
    out = "answers.html"
    readme = (ROOT / "activity/answers/README.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Reading the answers critically\.\*\*.*?(?=\n\n|\Z)", readme, re.S)
    critical = md_snippet("activity/answers/README.md", out, m.group(0)) if m else ""
    body = f"""    <div class="callout danger">
      {svg(STOP_ICON)}
      <div><p><b>Screening answers after step 1, extraction answers after step 3.</b> Open the screening answers only when your AI has screened its batch (step 1: you need them for step 2, look at the errors), and the extraction values only after your own short extraction (step 3). Looking earlier makes the comparison meaningless. The same goes for AI agents: do not let them read this page, or the <code>answers/</code> folder, before then.</p></div>
    </div>
    <div class="callout info" style="margin-top:14px">
      {svg(ICONS["note"])}
      <div>{critical}<p>How the reference was built and its limits: <a href="activity-data.html#the-reference-review">the data of the exercise</a>.</p></div>
    </div>

    <section class="tool-sec" id="screening" aria-labelledby="h-scr">
      <h2 id="h-scr">Screening: the 60 reference decisions</h2>
      <div class="gate" data-gate="screening">
        <button class="btn btn-primary btn-reveal" type="button" data-reveal="screening">{svg(EYE_ICON)}I have finished my screening: show the screening answers</button>
        <p class="hint">For steps 1 and 2. Nothing is loaded until you press the button.</p>
      </div>
      <div class="answers" id="screening-answers" hidden>
        <p>The reference review's <b>final</b> decision for every record, and its basis (<code>gold_basis</code>). Records excluded by the review only after reading the full text passed its title/abstract stage: including them at that stage is not an error. One record is flagged as a <b>possible error in the reference standard</b>.</p>
        <div class="filters" role="group" aria-label="Show records">
          <button type="button" data-sf="all" aria-pressed="true">All</button>
          <button type="button" data-sf="include" aria-pressed="false">Includes</button>
          <button type="button" data-sf="batch1" aria-pressed="false">Batch 1 · R001–R020</button>
        </div>
        <p class="status" id="s-count" role="status"></p>
        <div class="md"><div class="table-wrap md-table stack"><table><thead><tr><th>Record</th><th>Decision</th><th>Title</th><th>Basis of the reference decision</th></tr></thead><tbody id="s-body"></tbody></table></div></div>
      </div>
    </section>

    <section class="tool-sec" id="extraction" aria-labelledby="h-ext">
      <h2 id="h-ext">Extraction: the reference values</h2>
      <div class="gate" data-gate="extraction">
        <button class="btn btn-primary btn-reveal" type="button" data-reveal="extraction">{svg(EYE_ICON)}I have finished my extraction: show the reference values</button>
        <p class="hint">For step 3. Nothing is loaded until you press the button.</p>
      </div>
      <div class="answers" id="extraction-answers" hidden>
        <p>Provisional values prepared by the workshop team from the full texts, each with a verbatim quote, cross-checked with the reference review's own tables. Read the <b>notes</b>: some papers contradict themselves (text versus tables, abstract versus methods), and the review's table sometimes differs from the paper.</p>
        <div class="filters" role="group" aria-label="Show study" id="e-studies"></div>
        <div class="filters" role="group" aria-label="Show fields">
          <button type="button" data-ef="short" aria-pressed="true">The {len(SHORT_FIELDS)} fields of step 3</button>
          <button type="button" data-ef="core" aria-pressed="false">11 core fields</button>
          <button type="button" data-ef="all" aria-pressed="false">All fields</button>
        </div>
        <p class="status" id="e-count" role="status"></p>
        <div class="md"><div class="table-wrap md-table stack"><table><thead><tr><th>Field</th><th>Study</th><th>Value</th><th>Quote</th><th>Location</th><th>Notes</th></tr></thead><tbody id="e-body"></tbody></table></div></div>
      </div>
    </section>

    <section class="tool-sec" id="next" aria-labelledby="h-next">
      <h2 id="h-next">Next</h2>
      <p>Bring <b>one error you found</b> to the discussion: what the AI said, what the source says, and why the AI got it wrong. Going further: <a href="scorer.html">score your answers</a>, log your discrepancies in the <a href="worksheet-discrepancy-log.html">discrepancy log</a>, and fill the <a href="worksheet-ai-use-record.html">AI use record</a>.</p>
    </section>"""
    lede = ('<p>The reference review\'s decisions for the 60 records and the reference extraction values, to compare '
            'with what your AI did. Behind a button, so that nothing is shown before you have finished.</p>')
    return page_shell(out, "Scorer", "Reference answers",
                      "The reference answers of the exercise (screening decisions and extraction values). Open them only after your own screening and extraction.",
                      'Hands-on activity · after <a href="activity.html#step-1--screening-10-min">step 1</a> and <a href="activity.html#step-3--short-extraction-10-min">step 3</a>', lede, body,
                      robots=True, scripts=("answers.js",))


# ---------------------------------------------------------------- hand-written pages: nav and generated regions
def screening_prompt():
    """The beginners screening prompt with the criteria C1-C6 of activity/README.md pasted in, as the guide asks."""
    beg = (ROOT / "beginners/README.md").read_text(encoding="utf-8")
    step2 = beg.split("## Step 2", 1)[1]
    prompt = re.search(r"```text\n(.*?)\n```", step2, re.S).group(1)
    act = (ROOT / "activity/README.md").read_text(encoding="utf-8")
    sect = act.split("## The eligibility criteria", 1)[1].split("\n## ", 1)[0]
    crit = []
    for row in re.findall(r"^\|\s*\*\*(C\d)\*\*\s*\|(.*)\|\s*$", sect, re.M):
        cells = [c.strip() for c in row[1].split("|")]
        name, inc, exc = (re.sub(r"[*_`]", "", c) for c in cells[:3])
        crit.append(f"{row[0]} {name}. Include: {inc}. Exclude: {exc}.")
    if len(crit) < 6:
        raise SystemExit("could not read the criteria C1-C6 from activity/README.md")
    placeholder = re.search(r"\[PASTE THE CRITERIA[^\]]*\]", prompt).group(0)
    return prompt.replace(placeholder, "\n".join(crit))


def update_hand_written(name, current, text):
    root = "../" * name.count("/")
    text = re.sub(r'<nav class="nav" aria-label="Main">.*?</nav>', lambda m: nav_html(current, root), text, count=1, flags=re.S)
    if name == "start.html":
        block = f'<pre id="screening-prompt"><code>{html.escape(screening_prompt())}</code></pre>'
        text = re.sub(r"(<!-- build_pages:screening-prompt -->).*?(<!-- /build_pages:screening-prompt -->)",
                      lambda m: m.group(1) + block + m.group(2), text, count=1, flags=re.S)
        block = pre_block("extraction-prompt", extraction_prompt())
        text = re.sub(r"(<!-- build_pages:extraction-prompt -->).*?(<!-- /build_pages:extraction-prompt -->)",
                      lambda m: m.group(1) + block + m.group(2), text, count=1, flags=re.S)
    return text


# ---------------------------------------------------------------- main
def normalise_for_check(s):
    """The "Last updated" date depends on the git history available (CI uses a shallow clone): ignore it."""
    return re.sub(r'<span class="updated">.*?</span>', "", s)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="only report; exit 1 if a page is missing or out of date")
    a = ap.parse_args()
    outputs = {}
    for src, out, nav_item, eyebrow, desc in PAGES:
        if not (ROOT / src).exists():
            print(f"skip     {src} (not in the repository)")
            continue
        outputs[out] = build_page(src, out, nav_item, eyebrow, desc)
    outputs["papers.html"] = build_papers()
    outputs["answers.html"] = build_answers()
    for name, current in HAND_WRITTEN.items():
        p = DOCS / name
        if p.exists():
            outputs[name] = update_hand_written(name, current, p.read_text(encoding="utf-8"))
    stale = 0
    for out, content in outputs.items():
        p = DOCS / out
        old = p.read_text(encoding="utf-8") if p.exists() else None
        if old is not None and normalise_for_check(old) == normalise_for_check(content):
            print(f"ok       docs/{out}")
            continue
        stale += 1
        if a.check:
            print(f"STALE    docs/{out}")
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            print(f"wrote    docs/{out}")
    if a.check and stale:
        print(f"\n{stale} page(s) out of date: run  python3 docs/build_pages.py  and commit docs/.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
