#!/usr/bin/env python3
"""Build the README and website figures (SVG, light and dark) from the repository files.

Every number drawn in a figure is counted from the files of this repository, so the figures cannot drift
from the data. Run it after the records, the extraction form, the papers, the skills or the prompts change,
then copy the figures into the website:

    python3 assets/figures/build_figures.py
    python3 docs/sync_data.py

Style: white, thin outlines, pastel tints (light blue, green, yellow, pink), EUPHA blue #2E61A3 and navy
#0F2747, line icons drawn on a 24-pixel grid. Each figure is written twice: <name>-light.svg and
<name>-dark.svg; the README picks one with <picture> and prefers-color-scheme. Standard library only.
"""
import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Liberation Sans', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "light": dict(
        bg="#FFFFFF", card="#FFFFFF", soft="#F6F8FB", border="#D6E0EC", ink="#0F2747", muted="#4A5D78",
        faint="#8496AE", blue="#2E61A3", accent="#2E61A3",
        blue_bg="#EAF2FC", blue_ln="#A9C5E8", green_bg="#E8F5EC", green_ln="#9DCFB1", green_tx="#1D6A44",
        yellow_bg="#FFF7D6", yellow_ln="#E2CD78", yellow_tx="#5E4B0E", pink_bg="#FCEBEF", pink_ln="#E8B1BF",
        pink_tx="#A12F4B", bar="#BFD2EA"),
    "dark": dict(
        bg="#0D1117", card="#0D1117", soft="#161B22", border="#30363D", ink="#E6EDF3", muted="#9DA7B3",
        faint="#768390", blue="#7FB3E6", accent="#7FB3E6",
        blue_bg="#132840", blue_ln="#2F5A8C", green_bg="#10291C", green_ln="#2E6B4A", green_tx="#8FD6B2",
        yellow_bg="#29240F", yellow_ln="#776726", yellow_tx="#E9D589", pink_bg="#2D1720", pink_ln="#7D3A4E",
        pink_tx="#F2A7B8", bar="#2F4565"),
}

# ----------------------------------------------------------------------------- counts from the repository

def counts():
    rec = list(csv.DictReader(open(ROOT / "activity/data/screening_records.csv", encoding="utf-8")))
    form = list(csv.DictReader(open(ROOT / "activity/data/extraction_form.csv", encoding="utf-8")))
    papers = list(csv.DictReader(open(ROOT / "activity/data/papers.csv", encoding="utf-8")))
    cfg = (ROOT / "activity/review_config.yaml").read_text(encoding="utf-8")
    n_incl = int(re.search(r"^\s*n_included:\s*(\d+)", cfg, re.M).group(1))
    skills = sorted(p.parent.name for p in (ROOT / ".claude/skills").glob("*/SKILL.md"))
    stage_files = sorted((ROOT / "prompts").glob("0[0-9]_*.md"))
    n_prompts = sum(len(re.findall(r"^## \d+\.\d+ ", f.read_text(encoding="utf-8"), re.M)) for f in stage_files)
    return dict(records=len(rec), includes=n_incl, papers=len(papers), fields=len(form),
                core=sum(1 for r in form if (r.get("core") or "").strip() == "yes"),
                skills=len(skills), skill_names=skills, stages=len(stage_files), prompts=n_prompts)

# ----------------------------------------------------------------------------- drawing helpers

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=16, fill="#000", weight=400, anchor="start", family=None, spacing=None, italic=False):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    w = f' font-weight="{weight}"' if weight != 400 else ""
    f = f' font-family="{family}"' if family else ""
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    it = ' font-style="italic"' if italic else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}"{w}{a}{f}{ls}{it}>{esc(s)}</text>'


def lines(x, y, rows, size=16, fill="#000", weight=400, lh=1.35, anchor="start", family=None):
    return "".join(text(x, y + i * size * lh, r, size, fill, weight, anchor, family) for i, r in enumerate(rows))


def rect(x, y, w, h, fill, stroke=None, r=12, sw=1.2, dash=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{s}{d}/>'


ICONS = {  # line icons on a 24 x 24 grid (Phosphor-like), stroke only
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 19c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><circle cx="16.5" cy="9" r="2.6"/><path d="M16.2 13.6c2.7 0 4.8 1.9 4.8 4.9"/>',
    "chat": '<path d="M4 5.5h16a1.5 1.5 0 0 1 1.5 1.5v9a1.5 1.5 0 0 1-1.5 1.5H10l-4.5 3.5V17.5H4A1.5 1.5 0 0 1 2.5 16V7A1.5 1.5 0 0 1 4 5.5z"/><path d="M7 10h10M7 13.5h6"/>',
    "stack": '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3"/>',
    "file": '<path d="M6 2.5h8l4.5 4.5v14.5H6z"/><path d="M14 2.5V7h4.5"/><path d="M9 12h6.5M9 15.5h6.5M9 8.5h2.5"/>',
    "terminal": '<rect x="2.5" y="4" width="19" height="16" rx="2"/><path d="M6.5 9.5l3 2.5-3 2.5M12 15h5"/>',
    "chart": '<path d="M3.5 20.5h17"/><path d="M6.5 20.5v-7M11.5 20.5V5M16.5 20.5v-10"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/>',
    "funnel": '<path d="M3.5 4.5h17l-6.5 7.5v6.5l-4 2v-8.5z"/>',
    "question": '<circle cx="12" cy="12" r="9"/><path d="M9.6 9.4a2.5 2.5 0 1 1 3.4 2.4c-.6.3-1 .8-1 1.5v.6"/><path d="M12 16.8v.01"/>',
    "quote": '<path d="M6 2.5h8l4.5 4.5v14.5H6z"/><path d="M14 2.5V7h4.5"/><path d="M9.5 12.5h2v2.5a2 2 0 0 1-2 2M13.5 12.5h2v2.5a2 2 0 0 1-2 2"/>',
    "scale": '<path d="M12 4v16M8 20h8M5 7.5h14"/><path d="M5 7.5 2.5 13.5a2.5 2.5 0 0 0 5 0zM19 7.5l-2.5 6a2.5 2.5 0 0 0 5 0z"/>',
    "clipboard": '<rect x="5" y="4.5" width="14" height="17" rx="2"/><path d="M9 4.5V3h6v1.5"/><path d="M8.5 11l2 2 4-4M8.5 17h7"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7"/>',
    "x": '<path d="M7 7l10 10M17 7 7 17"/>',
    "person": '<circle cx="12" cy="7.5" r="3.5"/><path d="M5 21c0-4 3-6.5 7-6.5s7 2.5 7 6.5"/>',
    "sparkle": '<path d="M12 3.5l1.9 5.1 5.1 1.9-5.1 1.9-1.9 5.1-1.9-5.1-5.1-1.9 5.1-1.9z"/><path d="M18.5 16v4M16.5 18h4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
    "warning": '<path d="M12 3.5 2.5 20h19z"/><path d="M12 10v4.5M12 17.4v.01"/>',
    "book": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
    "talk": '<path d="M3 6.5A1.5 1.5 0 0 1 4.5 5h9A1.5 1.5 0 0 1 15 6.5v5a1.5 1.5 0 0 1-1.5 1.5H8l-3 2.5V13h-.5A1.5 1.5 0 0 1 3 11.5z"/><path d="M15 9h4.5a1.5 1.5 0 0 1 1.5 1.5v5a1.5 1.5 0 0 1-1.5 1.5H19v2.5L16 17h-4.5a1.5 1.5 0 0 1-1.5-1.5V13"/>',
    "play": '<rect x="2.5" y="4.5" width="19" height="15" rx="2"/><path d="M10 9v6l5-3z"/>',
    "arrow": '<path d="M4 12h16M14 6l6 6-6 6"/>',
    "loop": '<path d="M17 2.5l3 3-3 3"/><path d="M4 11.5v-1a5 5 0 0 1 5-5h11"/><path d="M7 21.5l-3-3 3-3"/><path d="M20 12.5v1a5 5 0 0 1-5 5H4"/>',
}


def icon(name, x, y, size=24, color="#000", sw=1.7):
    k = size / 24
    return (f'<g transform="translate({x} {y}) scale({k:.4f})" fill="none" stroke="{color}" stroke-width="{sw / k * k:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def badge_icon(name, cx, cy, r, bg, ln, color, size=None):
    size = size or r * 1.15
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}" stroke="{ln}" stroke-width="1.2"/>'
            + icon(name, cx - size / 2, cy - size / 2, size, color))


def svg(w, h, title, body, t, extra_style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{esc(title)}" font-family="{FONT}">\n<title>{esc(title)}</title>\n'
            + (f"<style>{extra_style}</style>\n" if extra_style else "")
            + f'<rect width="{w}" height="{h}" rx="16" fill="{t["bg"]}"/>\n' + body + "\n</svg>\n")

# ----------------------------------------------------------------------------- figures

def hero(t, c, mobile=False):
    """Title, hook question and a schematic screening sheet with a slow scanning lens (the only animation)."""
    rows = [  # schematic only: (AI decision, reference decision)
        ("include", "include"), ("exclude", "exclude"), ("exclude", "include"),
        ("exclude", "exclude"), ("include", "include")]
    W, H = (760, 940) if mobile else (1280, 470)
    sx, sy = (40, 486) if mobile else (744, 40)  # sheet origin
    sw_, rh = (680, 56) if mobile else (496, 54)
    style = ("@keyframes scan{0%,12%{transform:translateY(0)}30%,46%{transform:translateY(" + str(2 * rh) + "px)}"
             "64%,80%{transform:translateY(" + str(4 * rh) + "px)}100%{transform:translateY(0)}}"
             ".lens{animation:scan 14s ease-in-out infinite}"
             "@media (prefers-reduced-motion:reduce){.lens{animation:none}}")
    b = []
    if mobile:
        tx, ty = 40, 76
        b.append(text(tx, ty, "EPH 2026 · BILBAO · SKILLS BUILDING SEMINAR M.8", 17, t["accent"], 700, spacing=1.6))
        b.append(lines(tx, ty + 70, ["AI for evidence", "synthesis"], 58, t["ink"], 800, 1.08))
        b.append(lines(tx, ty + 210, ["Screening and data extraction with AI,", "checked against a review done by humans."], 25, t["muted"], 400, 1.4))
        b.append(rect(tx, ty + 290, 680, 92, t["blue_bg"], t["blue_ln"], 14))
        b.append(icon("search", tx + 22, ty + 314, 34, t["accent"], 2))
        b.append(lines(tx + 78, ty + 326, [f"An AI can screen all {c['records']} records for you.", "Would you notice the ones it got wrong?"], 23, t["ink"], 650, 1.35))
    else:
        tx, ty = 56, 88
        b.append(text(tx, ty, "EPH 2026 · BILBAO · SKILLS BUILDING SEMINAR M.8", 14.5, t["accent"], 700, spacing=1.8))
        b.append(text(tx, ty + 62, "AI for evidence synthesis", 50, t["ink"], 800))
        b.append(lines(tx, ty + 112, ["Screening and data extraction with AI, checked", "against a systematic review done by humans."], 22, t["muted"], 400, 1.45))
        b.append(rect(tx, ty + 186, 600, 92, t["blue_bg"], t["blue_ln"], 14))
        b.append(icon("search", tx + 22, ty + 213, 36, t["accent"], 2))
        b.append(lines(tx + 80, ty + 223, [f"An AI can screen all {c['records']} records for you.", "Would you notice the ones it got wrong?"], 21, t["ink"], 650, 1.4))
        b.append(text(tx, ty + 330, "EUPHA Digital Health and Artificial Intelligence Section", 15.5, t["muted"], 600))
    # the sheet
    sh = 92 + rh * len(rows) + 56
    b.append(rect(sx, sy, sw_, sh, t["card"], t["border"], 16))
    b.append(text(sx + 24, sy + 38, "Screening sheet", 19 if mobile else 17, t["ink"], 700))
    b.append(text(sx + sw_ - 24, sy + 38, "schematic", 15 if mobile else 13, t["faint"], 400, "end", italic=True))
    hx = sx + 24
    colA, colR = sx + sw_ - 224, sx + sw_ - 112
    yh = sy + 74
    b.append(text(hx, yh, "RECORD", 13 if mobile else 11.5, t["faint"], 700, spacing=1.2))
    for x_, lab in ((colA, "AI"), (colR, "HUMANS")):
        b.append(text(x_ + 46, yh, lab, 13 if mobile else 11.5, t["faint"], 700, "middle", spacing=1.2))
    for i, (ai, ref) in enumerate(rows):
        y = sy + 92 + i * rh
        miss = ai != ref
        if ai == "exclude" and ref == "include":
            b.append(rect(sx + 10, y - 2, sw_ - 20, rh - 4, t["pink_bg"], t["pink_ln"], 10))
        b.append(f'<line x1="{sx + 16}" y1="{y + rh - 3}" x2="{sx + sw_ - 16}" y2="{y + rh - 3}" stroke="{t["border"]}" stroke-width="1"/>')
        # letters, not record IDs: a schematic must not hint at the real reference decisions
        b.append(text(hx, y + 31, f"Record {'ABCDE'[i]}", 16 if mobile else 14.5, t["muted"], 600))
        bx = hx + (100 if mobile else 92)
        bw = colA - bx - 26
        b.append(rect(bx, y + 14, bw, 7, t["bar"], None, 3.5))
        b.append(rect(bx, y + 28, bw * (0.55 + 0.07 * (i % 4)), 7, t["bar"], None, 3.5))
        for xx, d in ((colA, ai), (colR, ref)):
            inc = d == "include"
            bg, ln, tc = (t["green_bg"], t["green_ln"], t["green_tx"]) if inc else (t["soft"], t["border"], t["muted"])
            b.append(rect(xx, y + 11, 92, 28, bg, ln, 14))
            b.append(text(xx + 46, y + 30, d, 14 if mobile else 13, tc, 600, "middle"))
    ylast = sy + 92 + len(rows) * rh
    b.append(icon("warning", hx, ylast + 12, 20, t["pink_tx"], 1.8))
    b.append(text(hx + 30, ylast + 28, "Record C: the AI excluded a study the humans included", 15.5 if mobile else 14, t["pink_tx"], 600))
    # the lens
    b.append(f'<g class="lens"><rect x="{sx + 8}" y="{sy + 90 + rh * 0}" width="{sw_ - 16}" height="{rh * 2 - 4}" rx="12" '
             f'fill="none" stroke="{t["accent"]}" stroke-width="2" stroke-dasharray="6 5" opacity="0.85"/></g>')
    title = (f"AI for evidence synthesis. EPH 2026 Bilbao, skills building seminar M.8, EUPHA Digital Health and Artificial "
             f"Intelligence Section. An AI can screen all {c['records']} records for you: would you notice the ones it got wrong? "
             "A schematic screening sheet compares AI decisions with the human review and highlights a missed include.")
    return svg(W, H, title, "\n".join(b), t, style)


def sheet(t, c):
    """The screening sheet of the hero alone, for the website hero (the page gives the title in HTML)."""
    s = hero(t, c)
    s = re.sub(r'<text[^>]*>[^<]*</text>', lambda m: m.group(0) if 'x="' in m.group(0) and float(re.search(r' x="([\d.]+)"', m.group(0)).group(1)) >= 744 else '', s)
    s = re.sub(r'<g transform="translate\(78 301\)[^>]*>.*?</g>', '', s)
    s = s.replace('width="1280" height="470" viewBox="0 0 1280 470"', 'width="520" height="434" viewBox="732 30 520 434"', 1)
    s = s.replace('aria-label="AI for evidence synthesis. EPH 2026 Bilbao, skills building seminar M.8, EUPHA Digital Health and Artificial Intelligence Section. ', 'aria-label="', 1)
    return s


def key_message(t, c):
    W, H = 1240, 560
    b = []
    b.append(text(40, 56, "Same tools, opposite outcomes", 28, t["ink"], 800))
    b.append(text(40, 88, "The advantages of AI in evidence synthesis come only with the skills to control it.", 17, t["muted"]))
    # origin
    ox, oy = 40, 252
    b.append(rect(ox, oy, 200, 92, t["card"], t["border"], 14))
    b.append(icon("sparkle", ox + 18, oy + 22, 26, t["accent"], 1.8))
    b.append(lines(ox + 54, oy + 40, ["AI tools in an", "evidence review"], 17, t["ink"], 700, 1.3))
    # upper path
    b.append(f'<path d="M240 286 C 300 286, 300 170, 352 170" fill="none" stroke="{t["green_ln"]}" stroke-width="2.4"/>')
    b.append(f'<path d="M240 312 C 300 312, 300 430, 352 430" fill="none" stroke="{t["pink_ln"]}" stroke-width="2.4" stroke-dasharray="7 6"/>')
    b.append(text(356, 128, "NECESSARY, NOT SUFFICIENT: ALL THREE TOGETHER", 12.5, t["green_tx"], 800, spacing=1.2))
    reqs = [("person", "AI literacy and advanced skills", "how models fail: context, parsing, sampling"),
            ("book", "Review methods expertise", "criteria, bias, what a valid answer looks like"),
            ("check", "A verification workflow", "quotes checked, two runs, model and version logged")]
    for i, (ic, a, s) in enumerate(reqs):
        x = 356 + i * 0
    bx, by, bw, bh = 352, 140, 520, 62
    b.append(rect(bx, by, bw, bh * 3 + 16, t["green_bg"], t["green_ln"], 16))
    for i, (ic, a, s) in enumerate(reqs):
        y = by + 10 + i * (bh + 0)
        b.append(icon(ic, bx + 20, y + 14, 26, t["green_tx"], 1.8))
        b.append(text(bx + 60, y + 27, a, 17.5, t["ink"], 700))
        b.append(text(bx + 60, y + 48, s, 15, t["muted"]))
        if i < 2:
            b.append(f'<line x1="{bx + 60}" y1="{y + bh + 3}" x2="{bx + bw - 20}" y2="{y + bh + 3}" stroke="{t["green_ln"]}" stroke-width="0.8" stroke-dasharray="3 4"/>')
    # lower path
    lx, ly = 352, 376
    b.append(rect(lx, ly, 520, 112, t["pink_bg"], t["pink_ln"], 16, dash="6 5"))
    b.append(text(lx + 20, ly + 34, "WITHOUT THEM", 12.5, t["pink_tx"], 800, spacing=1.2))
    b.append(lines(lx + 20, ly + 62, ["Trusts fluent output: missed studies, invented values,", "“not reported” when the text is there, unchecked runs"], 16, t["ink"], 500, 1.4))
    # results
    for (y, bg, ln, tc, ic, head, sub, tag, dash) in (
            (164, t["green_bg"], t["green_ln"], t["green_tx"], "check", "Real advantages", ["speed, scale, consistency,", "living updates"], "HUMAN IN THE LOOP", None),
            (372, t["pink_bg"], t["pink_ln"], t["pink_tx"], "warning", "Serious errors", ["loss of control over", "the review process"], "HUMAN OUT OF THE LOOP", "6 5")):
        b.append(f'<path d="M872 {y + 60} L 926 {y + 60}" stroke="{ln}" stroke-width="2.4" fill="none"' + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")
        b.append(f'<path d="M918 {y + 53} L 928 {y + 60} L 918 {y + 67}" stroke="{ln}" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        b.append(rect(936, y, 264, 124, bg, ln, 16, dash=dash))
        b.append(icon(ic, 954, y + 18, 24, tc, 2))
        b.append(text(988, y + 37, head, 20, t["ink"], 800))
        b.append(lines(956, y + 64, sub, 15, t["muted"], 400, 1.35))
        b.append(text(956, y + 108, tag, 12, tc, 800, spacing=1.2))
    b.append(f'<line x1="40" y1="512" x2="1200" y2="512" stroke="{t["border"]}" stroke-width="1"/>')
    b.append(text(40, 540, "The human reviewer stays responsible for every decision. The AI does not.", 16, t["ink"], 700))
    b.append(text(1200, 540, "Beginners track: for learning only", 15, t["muted"], 400, "end"))
    title = ("Same tools, opposite outcomes. With three things together, AI literacy and advanced skills, review methods "
             "expertise and a verification workflow (necessary, not sufficient), AI tools bring real advantages (speed, "
             "scale, consistency, living updates) with the human in the loop. Without them, trusting fluent output leads "
             "to missed studies, invented values and unchecked runs: serious errors, loss of control, human out of the loop.")
    return svg(W, H, title, "\n".join(b), t)


def session(t, c):
    W, H = 1240, 470
    b = []
    b.append(text(40, 56, "60 minutes, four parts", 28, t["ink"], 800))
    b.append(text(40, 88, "The hands-on part is the middle half hour; then everyone discusses what went wrong, and why.", 17, t["muted"]))
    x0, x1, y = 40, 1200, 118
    unit = (x1 - x0) / 60
    segs = [(10, "Expert talks", "limits, benefits", "talk", False),
            (10, "Demo", "open-access tools", "play", False),
            (30, "Small-group exercise", "screen, extract, score", "users", True),
            (10, "Discussion", "the whole room", "chat", False)]
    x = x0
    pos = []
    for m, name, sub, ic, hi in segs:
        w = m * unit
        bg, ln = (t["blue_bg"], t["blue_ln"]) if hi else (t["soft"], t["border"])
        b.append(rect(x + 3, y, w - 6, 74, bg, ln, 12))
        b.append(icon(ic, x + 18, y + 14, 22, t["accent"], 1.7))
        b.append(text(x + 48, y + 31, name, 16, t["ink"], 700))
        b.append(text(x + 18, y + 58, f"{m} min · {sub}", 13.5, t["muted"]))  # short labels: segments are 193 px
        pos.append((x, w))
        x += w
    # bracket from the exercise segment to its three steps, and from the discussion segment to step 4
    steps = [("funnel", "Screen", 10, [f"{c['records']} records (20 in the chat", "track): include, exclude", "or unsure, with a reason"], "blue"),
             ("quote", "Extract", 12, ["one paper (3 for agents):", "a verbatim quote and its", "location for every value"], "blue"),
             ("chart", "Score", 8, ["compare with the human", "reference review: read", "the missed includes first"], "green"),
             ("talk", "Discuss", 10, ["missed studies, invented", "values, a different answer", "on a second run"], "yellow")]
    cw, gap, cy = 274, 21.3, 262
    ex, ew = pos[2]
    dx, dw = pos[3]
    cxs = [x0 + i * (cw + gap) for i in range(4)]
    # connectors
    yb = y + 106  # orthogonal bracket
    ln_ = f'fill="none" stroke="{t["blue_ln"]}" stroke-width="1.6" stroke-linejoin="round"'
    b.append(f'<path d="M{ex + ew / 2} {y + 74} V {yb}" {ln_}/>')
    b.append(f'<path d="M{cxs[0] + cw / 2} {cy - 4} V {yb} H {cxs[2] + cw / 2} V {cy - 4}" {ln_}/>')
    b.append(f'<path d="M{cxs[1] + cw / 2} {yb} V {cy - 4}" {ln_}/>')
    b.append(f'<path d="M{dx + dw / 2} {y + 74} V {yb} H {cxs[3] + cw / 2} V {cy - 4}" fill="none" stroke="{t["yellow_ln"]}" stroke-width="1.6" stroke-linejoin="round"/>')
    for i, (ic, name, m, desc, tone) in enumerate(steps):
        cx = cxs[i]
        bg, ln = t[f"{tone}_bg"], t[f"{tone}_ln"]
        b.append(rect(cx, cy, cw, 176, t["card"], t["border"], 16))
        b.append(badge_icon(ic, cx + 40, cy + 40, 22, bg, ln, t["ink"], 24))
        b.append(text(cx + 74, cy + 36, f"{i + 1} · {name}", 20, t["ink"], 800))
        b.append(text(cx + 74, cy + 58, f"{m} min", 14.5, t["muted"], 600))
        b.append(lines(cx + 20, cy + 98, desc, 15, t["muted"], 400, 1.42))
        if i < 3:
            ax = cx + cw + 3
            b.append(icon("arrow", ax, cy + 30, 16, t["faint"], 2))
    b.append(text(40, 458, "Not finishing is expected: a careful comparison of 10 records beats a fast run of 60.", 15, t["muted"], 400, italic=True))
    title = (f"60 minutes, four parts. Expert discussion 10 min, demo 10 min, small-group exercise 30 min, "
             f"structured discussion 10 min. The exercise: 1 screen (10 min, {c['records']} records, 20 in the chat track), "
             "2 extract (12 min, a verbatim quote for every value), 3 score (8 min, compare with the human reference review), "
             "then 4 discuss (10 min).")
    return svg(W, H, title, "\n".join(b), t)


def glance(t, c):
    W, H = 1240, 360
    b = [text(40, 56, "At a glance", 28, t["ink"], 800),
         text(40, 88, "Counted from the files in this repository.", 17, t["muted"])]
    cards = [(c["records"], "records to screen", "titles and abstracts", "stack", "blue"),
             (c["includes"], "human includes", "in the reference review", "person", "green"),
             (c["papers"], "full-text papers", "for data extraction", "quote", "blue"),
             (c["fields"], "extraction fields", f"{c['core']} of them core", "file", "yellow"),
             (c["skills"], "agent skills", "for Claude Code", "terminal", "blue"),
             (c["prompts"], "chat prompts", f"in {c['stages']} review stages", "chat", "pink")]
    cw, gap = 182, 13.6
    for i, (n, lab, sub, ic, tone) in enumerate(cards):
        x = 40 + i * (cw + gap)
        y = 118
        b.append(rect(x, y, cw, 210, t["card"], t["border"], 16))
        b.append(badge_icon(ic, x + 38, y + 40, 20, t[f"{tone}_bg"], t[f"{tone}_ln"], t["ink"], 22))
        b.append(text(x + 20, y + 124, str(n), 62, t["ink"], 800))
        b.append(text(x + 20, y + 160, lab, 17, t["ink"], 700))
        b.append(text(x + 20, y + 184, sub, 14.5, t["muted"]))
    title = (f"At a glance: {c['records']} records to screen; {c['includes']} included by the human reference review; "
             f"{c['papers']} full-text papers; {c['fields']} extraction fields, {c['core']} core; {c['skills']} agent skills; "
             f"{c['prompts']} chat prompts in {c['stages']} review stages.")
    return svg(W, H, title, "\n".join(b), t)


def review_map(t, c):
    W, H = 1308, 690
    stages = [
        ("question", "Question", ["PICO terms,", "synonyms, scope gaps"], ["owns the question,", "sets criteria first"], ["review-protocol-check"], "1.1–1.3", False),
        ("search", "Search", ["draft Boolean strings,", "translate syntax"], ["runs the search,", "tests known studies"], ["search-strategy-critic"], "2.1–2.3", False),
        ("funnel", "Screen", ["pre-screen titles and", "abstracts, 2nd screener"], ["makes final calls,", "audits exclusions"], ["title-abstract-screening"], "3.1–3.3", True),
        ("quote", "Extract", ["draft values with", "verbatim quotes"], ["designs the form,", "checks every value"], ["full-text-extraction", "quote-verifier"], "4.1–4.3 · 5.1–5.3", True),
        ("scale", "Appraise", ["collect passages,", "draft GRADE reasons"], ["judges bias and", "certainty"], ["risk-of-bias-assessment", "grade-certainty"], "6.1", False),
        ("clipboard", "Report", ["checklist support,", "AI-use record"], ["is accountable,", "discloses AI use"], ["prisma-reporting-check", "ai-use-reporting"], "6.2–6.3", False),
    ]
    b = [text(40, 56, "Where AI can help, where a human must check", 28, t["ink"], 800),
         text(40, 88, f"The review stages, with the {c['skills']} agent skills and the {c['prompts']} chat prompts of this repository placed under the stage they serve.", 17, t["muted"])]
    lx, x0, cw, gap = 40, 196, 172, 8
    rows = [("AI can draft", "sparkle", "blue", 236, 74), ("A human checks", "person", "green", 318, 74),
            ("Agent skills", "terminal", None, 400, 96), ("Chat prompts", "file", None, 504, 40)]
    for lab, ic, tone, y, h in rows:
        b.append(icon(ic, lx, y + h / 2 - 11, 22, t["accent"], 1.7))
        b.append(text(lx + 30, y + h / 2 + 6, lab, 14.5, t["ink"], 700))
    for i, (ic, name, ai, hu, sk, pr, ex) in enumerate(stages):
        x = x0 + i * (cw + gap)
        if ex and not stages[i - 1][6]:
            span = sum(1 for st in stages[i:] if st[6]) if all(st[6] for st in stages[i:i + 2]) else 1
            ww = span * cw + (span - 1) * gap
            b.append(rect(x - 6, 116, ww + 12, 438, "none", t["accent"], 16, 1.4, "5 5"))
            b.append(rect(x + ww / 2 - 92, 107, 184, 20, t["bg"], None, 10))
            b.append(text(x + ww / 2, 122, "IN TODAY'S EXERCISE", 11.5, t["accent"], 800, "middle", spacing=1))
        b.append(badge_icon(ic, x + 30, 174, 20, t["soft"], t["border"], t["ink"], 22))
        b.append(text(x + 58, 181, name, 19, t["ink"], 800))
        b.append(f'<line x1="{x + 10}" y1="{208}" x2="{x + cw - 10}" y2="{208}" stroke="{t["border"]}"/>')
        b.append(rect(x, 236, cw, 74, t["blue_bg"], t["blue_ln"], 12))
        b.append(lines(x + 12, 266, ai, 13.5, t["ink"], 500, 1.35))
        b.append(rect(x, 318, cw, 74, t["green_bg"], t["green_ln"], 12))
        b.append(lines(x + 12, 348, hu, 13.5, t["ink"], 500, 1.35))
        for j, s in enumerate(sk):
            yy = 404 + j * 44
            b.append(rect(x, yy, cw, 36, t["card"], t["accent"], 18, 1.1))
            b.append(text(x + cw / 2, yy + 23, s, round(min(12.5, (cw - 22) / (len(s) * 0.61)), 1), t["accent"], 600, "middle", MONO))
        b.append(rect(x, 504, cw, 40, t["soft"], t["border"], 12))
        b.append(text(x + cw / 2, 529, pr, 14, t["muted"], 600, "middle"))
    # across stages: discrepancy-audit
    b.append(rect(x0, 570, 6 * cw + 5 * gap, 44, t["card"], t["border"], 12))
    b.append(icon("loop", x0 + 14, 581, 22, t["accent"], 1.7))
    b.append(text(x0 + 46, 598, "Across stages:", 14.5, t["ink"], 700))
    b.append(rect(x0 + 160, 578, 176, 28, t["card"], t["accent"], 14, 1.1))
    b.append(text(x0 + 248, 597, "discrepancy-audit", 12.5, t["accent"], 600, "middle", MONO))
    b.append(text(x0 + 350, 597, "compares AI output with the human reference and classifies every error", 14.5, t["muted"]))
    b.append(rect(x0, 626, 6 * cw + 5 * gap, 44, t["pink_bg"], t["pink_ln"], 12))
    b.append(icon("warning", x0 + 14, 637, 22, t["pink_tx"], 1.8))
    b.append(text(x0 + 46, 654, "Red flags at every stage:", 14.5, t["pink_tx"], 700))
    b.append(text(x0 + 238, 654, "invented studies or values · “not reported” when the text is there · a different answer on a second run · undocumented model", 14, t["ink"]))
    title = ("Where AI can help and where a human must check, stage by stage, with the agent skills and chat prompts of this "
             "repository. Question: review-protocol-check, prompts 1.1 to 1.3. Search: search-strategy-critic, 2.1 to 2.3. "
             "Screen: title-abstract-screening, 3.1 to 3.3. Extract: full-text-extraction and quote-verifier, 4.1 to 5.3. "
             "Appraise: risk-of-bias-assessment and grade-certainty, 6.1. Report: prisma-reporting-check and ai-use-reporting, "
             "6.2 to 6.3. Across stages: discrepancy-audit. Red flags: invented studies or values, not reported when the text "
             "is there, a different answer on a second run, undocumented model.")
    return svg(W, H, title, "\n".join(b), t)


def tracks(t, c):
    W, H = 1240, 550
    b = [text(40, 56, "Two ways to take part", 28, t["ink"], 800),
         text(40, 88, "Same records, same human reference review, two ways to work.", 17, t["muted"])]
    cols = [("terminal", "Agent track", "Claude Code or another coding agent", "blue", None,
             [("Clone the repository", "open the folder with Claude Code"),
              ("Skills load automatically", "from .claude/skills/"),
              ("Screen and extract", f"all {c['records']} records, {c['papers']} papers"),
              ("Score against the reference", "Python scorer or web scorer")],
             "Needs AI literacy and advanced skills"),
            ("chat", "Chat track", "any chat assistant, no installation", "yellow", "LEARNING ONLY",
             [("Open the beginners guide", "beginners/README.md"),
              ("Copy a batch and a prompt", "records R001–R020"),
              ("Save your decisions", "record_id, decision, reason"),
              ("Score in the browser", "nothing is uploaded")],
             "Teaching material, not a validated method")]
    for k, (ic, name, sub, tone, tag, steps, foot) in enumerate(cols):
        x, y, w = 40 + k * 590, 116, 570
        b.append(rect(x, y, w, 330, t["card"], t["border"], 16))
        b.append(f'<path d="M{x} {y + 16} a16 16 0 0 1 16 -16 h{w - 32} a16 16 0 0 1 16 16 v62 h-{w} z" fill="{t[tone + "_bg"]}" stroke="{t[tone + "_ln"]}" stroke-width="1.2"/>')
        b.append(icon(ic, x + 22, y + 22, 30, t["ink"], 1.7))
        b.append(text(x + 66, y + 37, name, 21, t["ink"], 800))
        b.append(text(x + 66, y + 61, sub, 14.5, t["muted"]))
        if tag:
            b.append(rect(x + w - 150, y + 25, 128, 28, t["card"], t["yellow_ln"], 14))
            b.append(text(x + w - 86, y + 44, tag, 12, t["ink"], 800, "middle", spacing=1))
        for i, (a, s) in enumerate(steps):
            yy = y + 104 + i * 44
            b.append(f'<circle cx="{x + 36}" cy="{yy + 6}" r="13" fill="{t[tone + "_bg"]}" stroke="{t[tone + "_ln"]}" stroke-width="1.2"/>')
            b.append(text(x + 36, yy + 11, str(i + 1), 14, t["ink"], 800, "middle"))
            b.append(text(x + 62, yy + 6, a, 16, t["ink"], 700))
            b.append(text(x + 62, yy + 26, s, 13.5, t["muted"], 400, family=MONO if "/" in s or "_" in s else None))
            if i < 3:
                b.append(f'<line x1="{x + 36}" y1="{yy + 20}" x2="{x + 36}" y2="{yy + 36}" stroke="{t[tone + "_ln"]}" stroke-width="1.2"/>')
        b.append(f'<line x1="{x + 22}" y1="{y + 284}" x2="{x + w - 22}" y2="{y + 284}" stroke="{t["border"]}" stroke-dasharray="3 4"/>')
        b.append(text(x + 22, y + 311, foot, 14, t["muted"], 700))
        b.append(f'<path d="M{x + w / 2} {y + 330} V {476}" stroke="{t["green_ln"]}" stroke-width="1.6"/>')
    b.append(rect(140, 476, 960, 50, t["green_bg"], t["green_ln"], 25))
    b.append(icon("check", 168, 489, 24, t["green_tx"], 2))
    b.append(text(640, 507, "Both end the same way: compare with the human reference review, then discuss", 17, t["ink"], 700, "middle"))
    title = (f"Two ways to take part. Agent track (Claude Code or another coding agent; needs AI literacy and advanced skills): "
             f"clone, skills load automatically, screen all {c['records']} records and extract {c['papers']} papers, score. "
             "Chat track (any chat assistant, learning only): open the beginners guide, copy a batch and a prompt, save your "
             "decisions, score in the browser. Both end by comparing with the human reference review and discussing.")
    return svg(W, H, title, "\n".join(b), t)


def prompt_card(t, c):
    W, H = 1240, 470
    b = [text(40, 56, "A prompt from the library", 28, t["ink"], 800),
         text(40, 88, "Prompt 2.2, “Break my search (critique mode)”, from prompts/02_search.md (excerpt, verbatim).", 17, t["muted"])]
    # chat window
    x, y, w, h = 40, 116, 760, 330
    b.append(rect(x, y, w, h, t["soft"], t["border"], 16))
    b.append(icon("chat", x + 20, y + 16, 22, t["muted"], 1.6))
    b.append(text(x + 52, y + 33, "New chat", 14.5, t["muted"], 600))
    bx, by, bw, bh = x + 90, y + 56, w - 112, 250
    b.append(f'<path d="M{bx + 18} {by} h{bw - 18} a14 14 0 0 1 14 14 v{bh - 28} a14 14 0 0 1 -14 14 h-{bw - 32} a14 14 0 0 1 -14 -14 v-{bh - 46} l-14 -4 l14 -10 z" '
             f'fill="{t["blue_bg"]}" stroke="{t["blue_ln"]}" stroke-width="1.2"/>')
    rows = [("Act as a skeptical information specialist.", 600),
            ("Your task is NOT to rewrite this search strategy.", 600),
            ("Identify how it could fail to retrieve relevant studies.", 600),
            ("[...]", 400),
            ("Rank the three most important failure risks, each with:", 400),
            ("what could be missed, why, and a test I can run.", 400),
            ("Do not modify the query yet.", 600)]
    for i, (r, wt) in enumerate(rows):
        b.append(text(bx + 24, by + 38 + i * 30, r, 16.5, t["muted"] if r == "[...]" else t["ink"], wt, family=MONO if False else None))
    b.append(badge_icon("person", x + 48, by + 24, 18, t["card"], t["border"], t["muted"], 20))
    # why it works
    rx = 830
    b.append(rect(rx, y, 370, h, t["card"], t["border"], 16))
    b.append(badge_icon("search", rx + 40, y + 44, 20, t["yellow_bg"], t["yellow_ln"], t["ink"], 22))
    b.append(text(rx + 72, y + 51, "Why it works", 20, t["ink"], 800))
    b.append(lines(rx + 24, y + 98, ["Asking to improve yields", "confident rewrites;", "asking to break yields", "checkable problems."], 18, t["ink"], 600, 1.45))
    b.append(lines(rx + 24, y + 232, ["The same pattern runs through", "the library: criteria first, quotes", "for every value, two runs."], 15, t["muted"], 400, 1.45))
    title = ("A prompt from the library, prompt 2.2 Break my search (critique mode), verbatim excerpt: Act as a skeptical "
             "information specialist. Your task is NOT to rewrite this search strategy. Identify how it could fail to retrieve "
             "relevant studies. [...] Rank the three most important failure risks, each with: what could be missed, why, and a "
             "test I can run. Do not modify the query yet. Why it works: asking to improve yields confident rewrites; asking "
             "to break yields checkable problems.")
    return svg(W, H, title, "\n".join(b), t)


BUTTONS = {  # short labels: on a phone each button is about 175 pixels wide
    "activity": ("users", "Start the activity", "30-minute group exercise", "blue", None),
    "beginners": ("chat", "Beginners track", "", "yellow", "LEARNING ONLY"),
    "records": ("stack", "Records to screen", "copy-ready batches", "blue", None),
    "scorer": ("chart", "Score your results", "in your browser", "green", None),
    "prompts": ("file", "Prompt library", "{prompts} prompts, {stages} stages", "blue", None),
    "skills": ("terminal", "Agent skills", "{skills} skills, Claude Code", "blue", None),
    "references": ("book", "Useful references", "guidance and evidence", "pink", None),
}


def button(t, c, key):
    ic, head, sub, tone, tag = BUTTONS[key]
    sub = sub.format(**c)
    W, H = 480, 124
    b = [rect(1, 1, W - 2, H - 2, t["card"], t["border"], 20, 1.6),
         badge_icon(ic, 58, 62, 32, t[tone + "_bg"], t[tone + "_ln"], t["ink"], 32),
         text(110, 56, head, 30, t["ink"], 800),
         icon("arrow", W - 50, 50, 26, t["accent"], 2.4)]
    if sub:
        b.append(text(110, 92, sub, 22, t["muted"]))
    if tag:
        b.append(rect(110, 72, 178, 32, t[tone + "_bg"], t[tone + "_ln"], 16))
        b.append(text(199, 94, tag, 15, t["ink"], 800, "middle", spacing=1))
    label = f"{head}: {sub or tag.lower()}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="{esc(label)}" font-family="{FONT}"><title>{esc(label)}</title>'
            + "".join(b) + "</svg>\n")


def key_message_mobile(t, c):
    """The key message stacked vertically, for screens narrower than 700 pixels."""
    W, H = 760, 1330
    b = [text(40, 64, "Same tools,", 40, t["ink"], 800), text(40, 112, "opposite outcomes", 40, t["ink"], 800),
         lines(40, 156, ["The advantages of AI in evidence synthesis", "come only with the skills to control it."], 22, t["muted"], 400, 1.4)]
    b.append(rect(40, 228, 680, 76, t["card"], t["border"], 16))
    b.append(icon("sparkle", 64, 248, 34, t["accent"], 1.8))
    b.append(text(116, 276, "AI tools in an evidence review", 25, t["ink"], 700))
    # with the skills
    b.append(f'<path d="M380 304 V 352" stroke="{t["green_ln"]}" stroke-width="2.6"/>')
    b.append(text(40, 384, "NECESSARY, NOT SUFFICIENT: ALL THREE TOGETHER", 16, t["green_tx"], 800, spacing=1.2))
    b.append(rect(40, 402, 680, 300, t["green_bg"], t["green_ln"], 18))
    reqs = [("person", "AI literacy and advanced skills", "how models fail: context, parsing, sampling"),
            ("book", "Review methods expertise", "criteria, bias, what a valid answer looks like"),
            ("check", "A verification workflow", "quotes checked, two runs, version logged")]
    for i, (ic, a_, s_) in enumerate(reqs):
        y = 420 + i * 94
        b.append(icon(ic, 64, y + 14, 34, t["green_tx"], 1.8))
        b.append(text(116, y + 38, a_, 24, t["ink"], 700))
        b.append(text(116, y + 70, s_, 20, t["muted"]))
    b.append(f'<path d="M380 702 V 742" stroke="{t["green_ln"]}" stroke-width="2.6"/><path d="M370 732 L380 744 L390 732" fill="none" stroke="{t["green_ln"]}" stroke-width="2.6" stroke-linecap="round"/>')
    b.append(rect(40, 752, 680, 116, t["green_bg"], t["green_ln"], 18))
    b.append(icon("check", 64, 772, 30, t["green_tx"], 2.2))
    b.append(text(110, 798, "Real advantages", 28, t["ink"], 800))
    b.append(text(64, 834, "speed, scale, consistency, living updates", 21, t["muted"]))
    b.append(text(64, 860 - 2, "HUMAN IN THE LOOP", 15, t["green_tx"], 800, spacing=1.2))
    # without them
    b.append(rect(40, 908, 680, 150, t["pink_bg"], t["pink_ln"], 18, dash="7 6"))
    b.append(text(64, 946, "WITHOUT THEM", 16, t["pink_tx"], 800, spacing=1.2))
    b.append(lines(64, 984, ["Trusts fluent output: missed studies, invented", "values, \u201cnot reported\u201d when the text is there"], 22, t["ink"], 500, 1.4))
    b.append(f'<path d="M380 1058 V 1098" stroke="{t["pink_ln"]}" stroke-width="2.6" stroke-dasharray="6 5"/><path d="M370 1088 L380 1100 L390 1088" fill="none" stroke="{t["pink_ln"]}" stroke-width="2.6" stroke-linecap="round"/>')
    b.append(rect(40, 1108, 680, 116, t["pink_bg"], t["pink_ln"], 18, dash="7 6"))
    b.append(icon("warning", 64, 1128, 30, t["pink_tx"], 2.2))
    b.append(text(110, 1154, "Serious errors", 28, t["ink"], 800))
    b.append(text(64, 1190, "loss of control over the review process", 21, t["muted"]))
    b.append(text(64, 1214, "HUMAN OUT OF THE LOOP", 15, t["pink_tx"], 800, spacing=1.2))
    b.append(f'<line x1="40" y1="1256" x2="720" y2="1256" stroke="{t["border"]}"/>')
    b.append(lines(40, 1292, ["The human reviewer stays responsible for every", "decision. The AI does not."], 21, t["ink"], 700, 1.4))
    title = ("Same tools, opposite outcomes. With AI literacy and advanced skills, review methods expertise and a "
             "verification workflow, all three together (necessary, not sufficient), AI tools bring real advantages with "
             "the human in the loop. Without them, trusting fluent output leads to serious errors and the human out of the loop.")
    return svg(W, H, title, "\n".join(b), t)


def main():
    c = counts()
    print("counts:", {k: v for k, v in c.items() if k != "skill_names"})
    out = HERE
    figs = {"hero": hero, "key-message": key_message, "session": session, "at-a-glance": glance,
            "review-map": review_map, "tracks": tracks, "prompt-card": prompt_card}
    for theme, t in THEMES.items():
        for name, fn in figs.items():
            (out / f"{name}-{theme}.svg").write_text(fn(t, c), encoding="utf-8")
        (out / f"hero-mobile-{theme}.svg").write_text(hero(t, c, mobile=True), encoding="utf-8")
        (out / f"sheet-{theme}.svg").write_text(sheet(t, c), encoding="utf-8")
        (out / f"key-message-mobile-{theme}.svg").write_text(key_message_mobile(t, c), encoding="utf-8")
        bdir = ROOT / "assets/buttons"
        bdir.mkdir(exist_ok=True)
        for key in BUTTONS:
            (bdir / f"{key}-{theme}.svg").write_text(button(t, c, key), encoding="utf-8")
    print("written:", len(list(out.glob("*.svg"))), "figures,", len(list((ROOT / "assets/buttons").glob("*-*.svg"))), "buttons")


if __name__ == "__main__":
    main()
