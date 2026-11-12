#!/usr/bin/env python3
"""Build the Pollack Periodica manuscript (Word) from paper.md, in the journal's own template.

    ~/.venvs/paper/bin/python build_docx.py      # needs python-docx (pip install python-docx)

Writes pollack_paper.docx and pollack_paper_anonymous.docx (author block, acknowledgements and the
repository link removed, for the double-blind review), and checks the journal's rules
(pollack_template.docx, "Instruction for preparation of papers", updated 6 Nov 2023): a title of at
most 80 characters, an abstract of at most 800 characters with no abbreviations, 5–6 keywords, no
personal pronouns, US English, IEEE references numbered in order of citation, editable tables that
are repeated on separate pages at the end.

paper.md: a `---` block of `key: value` lines (title, authors, affiliation, email, abstract,
keywords, data), then `# Section` / `## Subsection` (numbered; `{-}` for an unnumbered one),
paragraphs, `- ` list items, and tables: a `Table: caption {#tab:id}` line followed by pipe rows
(the first is the header). In the text: [@key; @key] cites references.bib, `Table @tab:id` refers to
a table, `code`, *italic*, **bold**; {{data}} stands for the data-availability sentence;
<!-- ... --> comments (also over several lines) are left out.
"""

import copy
import re
import sys
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

HERE = Path(__file__).resolve().parent
SOURCE, BIB, TEMPLATE = HERE / "paper.md", HERE / "references.bib", HERE / "pollack_template.docx"
CODE_FONT = "Courier New"
TABLE_PT = 8

# ── paper.md ──────────────────────────────────────────────────────────────────


def parse_source(text: str):
    _, front, body = text.split("---\n", 2)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)  # commented-out text is left out of the paper
    meta = dict(line.split(": ", 1) for line in front.strip().splitlines())
    blocks, para, lines = [], [], body.splitlines()

    def flush():
        if para:
            blocks.append(("p", " ".join(para)))
            para.clear()

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            flush()
        elif line.startswith("#"):
            flush()
            level = len(line) - len(line.lstrip("#"))
            title = line[level:].strip()
            numbered = not title.endswith("{-}")
            blocks.append(("h", level, title.removesuffix("{-}").strip(), numbered))
        elif line.startswith("- "):
            flush()
            blocks.append(("li", line[2:]))
        elif line.startswith("Table: "):
            flush()
            m = re.fullmatch(r"Table: (.*) \{#(tab:[\w-]+)\}", line)
            if not m:
                sys.exit(f"table caption without an id: {line}")
            rows = []
            i += 1
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            blocks.append(("table", m.group(2), m.group(1), rows))
            continue
        else:
            para.append(line.strip())
        i += 1
    flush()
    return meta, blocks


# ── references.bib → IEEE ─────────────────────────────────────────────────────

LATEX = {r'{\"o}': "ö", r'{\"a}': "ä", r'{\"u}': "ü", r"{\l}": "ł", r"\&": "&", "``": "“", "''": "”", "--": "–"}
VENUES = {  # booktitle as written in the .bib → the conference's full name
    "Proceedings of ICLR": "International Conference on Learning Representations (ICLR)",
    "Proceedings of ICML": "International Conference on Machine Learning (ICML)",
    "Proceedings of EMNLP": "Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    "Proceedings of EMNLP, Industry Track": "Conference on Empirical Methods in Natural Language Processing (EMNLP), Industry Track",
    "Proceedings of EMNLP: System Demonstrations": "Conference on Empirical Methods in Natural Language Processing (EMNLP), System Demonstrations",
    "Findings of ACL": "Findings of the Association for Computational Linguistics (ACL)",
    "NeurIPS Datasets and Benchmarks Track": "Conference on Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track",
    "Proceedings of the REALM Workshop at EMNLP": "REALM Workshop at the Conference on Empirical Methods in Natural Language Processing (EMNLP)",
}


def parse_bib(text: str) -> dict:
    entries = {}
    for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", text, re.S):
        kind, key, body = m.group(1).lower(), m.group(2).strip(), m.group(3)
        fields = {}
        for f in re.finditer(r"(\w+)\s*=\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}", body):
            fields[f.group(1).lower()] = re.sub(r"\s+", " ", f.group(2)).strip()
        entries[key] = {"kind": kind, **fields}
    return entries


def _latex(s: str) -> str:
    for a, b in LATEX.items():
        s = s.replace(a, b)
    return s


def _initials(first: str) -> str:
    parts = []
    for word in first.split():
        if re.fullmatch(r"([A-Z]\.)+", word):  # already initials, e.g. "M.A.K."
            parts.append(" ".join(c + "." for c in word.replace(".", "")))
        else:
            parts.append("-".join(p[0].upper() + "." for p in word.split("-") if p))
    return " ".join(parts)


def ieee_authors(field: str) -> str:
    names = []
    for raw in re.split(r"\s+and\s+", _latex(field)):
        raw = raw.strip()
        if raw == "others":
            names.append("et al.")
        elif raw.startswith("{") and raw.endswith("}"):  # a team or institution
            names.append(raw[1:-1])
        elif "," in raw:
            last, first = (s.strip() for s in raw.split(",", 1))
            names.append(f"{_initials(first)} {last.strip('{}')}")
        else:
            names.append(raw)
    if names[-1] == "et al.":
        return ", ".join(names[:-1]) + " et al."
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return ", ".join(names[:-1]) + ", and " + names[-1]


def sentence_case(title: str) -> str:
    """Lower-case letters (Pollack), keeping {protected} words and capitalizing after : ? ."""
    out, start = [], True
    for token in re.findall(r"\{[^{}]*\}|[^\s{}]+|\s+", _latex(title)):
        if token.isspace():
            out.append(token)
            continue
        if token.startswith("{"):
            word = token[1:-1]
        else:  # each part of a hyphenated word on its own: "Tool-Calling" → "tool-calling", "GPT-4" stays
            parts = [p if re.search(r"\w[A-Z]|\d", p) else p.lower() for p in token.split("-")]
            word = "-".join(parts)
            if start:
                word = word[0].upper() + word[1:]
        out.append(word)
        start = bool(re.search(r"[:?]$", token))
    return "".join(out).replace("{", "").replace("}", "")


def ieee_reference(e: dict) -> str:
    authors, title, year = ieee_authors(e["author"]), sentence_case(e["title"]), e.get("year", "")
    if e["kind"] == "misc":
        url = re.sub(r"\\url\{(.*)\}", r"\1", e.get("howpublished", ""))
        return (f"{authors}, “{title},” {year}. [Online]. Available: {url} "
                f"(accessed {date.today():%d %B %Y}).")
    if e["kind"] == "inproceedings":  # Pollack: Conference, City, Country, day–day Month year, pages
        parts = [f"in {VENUES.get(e.get('booktitle', ''), e.get('booktitle', ''))}"]
        if e.get("address"):
            parts.append(e["address"])
        parts.append(event_dates(e["eventdate"]) if e.get("eventdate") else year)
        if e.get("pages"):
            parts.append(f"pp. {_latex(e['pages'])}")
        if e.get("note"):
            parts.append(e["note"])
        return f"{authors}, “{title},” {', '.join(parts)}."
    journal = e.get("journal", "")
    arxiv = re.fullmatch(r"arXiv preprint (arXiv:\S+)", journal)
    if arxiv:
        return f"{authors}, “{title},” arXiv preprint {arxiv.group(1)}, {year}."
    vol = f", vol. {e['volume']}" if e.get("volume") else ""
    pages = f", pp. {_latex(e['pages'])}" if e.get("pages") else ""
    return f"{authors}, “{title},” {journal}{vol}{pages}, {year}."


def event_dates(field: str) -> str:
    """biblatex eventdate → Pollack's day–day Month year: 2024-11-12/2024-11-16 → 12–16 November 2024."""
    start, _, end = field.partition("/")
    a = date.fromisoformat(start)
    b = date.fromisoformat(end) if end else a
    if a == b:
        return f"{a.day} {a:%B %Y}"
    if (a.year, a.month) == (b.year, b.month):
        return f"{a.day}–{b.day} {b:%B %Y}"
    if a.year == b.year:
        return f"{a.day} {a:%B} – {b.day} {b:%B %Y}"
    return f"{a.day} {a:%B %Y} – {b.day} {b:%B %Y}"


NO_PAGES = {"Proceedings of ICLR", "NeurIPS Datasets and Benchmarks Track"}  # proceedings without page numbers


def incomplete(e: dict) -> list[str]:
    """What Pollack's reference rules ask for that the entry lacks."""
    gaps = []
    if "others" in e["author"]:
        gaps.append("all author names")
    if e["kind"] == "inproceedings":
        if not e.get("address"):
            gaps.append("city and country")
        if not e.get("eventdate"):
            gaps.append("dates")
        if not e.get("pages") and e.get("booktitle") not in NO_PAGES:
            gaps.append("pages")
    return gaps


# ── citations and cross-references ────────────────────────────────────────────

CITE = re.compile(r"\[(@[\w-]+(?:;\s*@[\w-]+)*)\]")


def number_citations(blocks) -> list[str]:
    order = []
    for b in blocks:
        texts = [b[1]] if b[0] in ("p", "li") else ([b[2]] + [c for row in b[3] for c in row] if b[0] == "table" else [])
        for t in texts:
            for m in CITE.finditer(t):
                for key in re.findall(r"@([\w-]+)", m.group(1)):
                    if key not in order:
                        order.append(key)
    return order


def cite_text(keys: list[str], order: list[str]) -> str:
    nums = sorted(order.index(k) + 1 for k in keys)
    groups, run = [], [nums[0]]
    for n in nums[1:]:
        if n == run[-1] + 1:
            run.append(n)
        else:
            groups.append(run)
            run = [n]
    groups.append(run)
    return ", ".join(f"[{g[0]}]–[{g[-1]}]" if len(g) > 2 else ", ".join(f"[{n}]" for n in g) for g in groups)


def resolve(text: str, order: list[str], tables: dict, meta: dict, anonymous: bool) -> str:
    text = CITE.sub(lambda m: cite_text(re.findall(r"@([\w-]+)", m.group(1)), order), text)
    text = re.sub(r"@(tab:[\w-]+)", lambda m: str(tables[m.group(1)]), text)
    if "{{data}}" not in text:
        return text
    data = ("Code, prompts, answer schemas, the decoding grammar, seeds, run logs and the scripts behind every "
            "number are available in a public repository (link withheld for review).") if anonymous else meta["data"]
    return text.replace("{{data}}", data)


# ── checks against the journal's rules ────────────────────────────────────────

UK = re.compile(r"\b\w*(?:i[sz]ation|ise[ds]?|ising|isable|our(?:s|ed|ing)?|yse[ds]?|ysing|ogue|tre|ence\b)\b", re.I)
UK_OK = {"our", "ours", "four", "hour", "hours", "your", "pour", "otherwise", "precise", "concise", "exercise",
         "rise", "raise", "raised", "raises", "noise", "promise", "premise", "advise", "wise", "arise", "arises",
         "surprise", "enterprise", "devise", "revise", "revised", "supervise", "supervised", "advised", "devised", "dialogue", "catalogue", "centre", "dialogues",
         "evidence", "difference", "sequence", "confidence", "consequence", "influence", "reference", "inference",
         "sentence", "sentences", "absence", "presence", "occurrence", "experience", "science", "conference",
         "independence", "dependence", "preference", "preferences", "references", "differences", "sequences",
         "competence", "existence", "sense", "license", "silence", "audience", "since", "once", "hence", "fence",
         "whence", "pence", "incidence", "coherence", "variance", "sentence", "intelligence", "persistence",
         "correspondence", "insistence", "convergence", "divergence", "emergence", "violence", "prudence",
         "valence", "patience", "residence", "excellence", "precedence", "prominence", "adherence", "inferences"}
UK_WORDS = {"behaviour", "behaviours", "behavioural", "favour", "favourable", "colour", "modelling", "modelled",
            "judgement", "labelled", "labelling", "travelled", "centre", "programme", "artefact", "artefacts",
            "analyse", "analysed", "optimise", "maximise", "minimise", "realise", "specialise", "generalise",
            "internalised", "quantisation", "characterisation", "organisation", "recognise", "summarise", "whilst"}


def check(meta: dict, blocks, order: list[str], bib: dict) -> list[str]:
    problems = []
    if len(meta["title"]) > 80:
        problems.append(f"title has {len(meta['title'])} characters (at most 70–80)")
    if len(meta["abstract"]) > 800:
        problems.append(f"abstract has {len(meta['abstract'])} characters including spaces (at most 800)")
    keywords = [k.strip() for k in meta["keywords"].split(",")]
    if not 5 <= len(keywords) <= 6:
        problems.append(f"{len(keywords)} keywords (5–6)")
    for name, text in (("title", meta["title"]), ("abstract", meta["abstract"]), ("keywords", meta["keywords"])):
        abbr = re.findall(r"\b(?:[A-Z][a-z]*[A-Z]\w*|[A-Z]{2,})\b", text)
        if abbr:
            problems.append(f"abbreviations in the {name}: {sorted(set(abbr))}")
    prose = " ".join(b[1] for b in blocks if b[0] in ("p", "li")) + " " + meta["abstract"]
    prose = re.sub(r"`[^`]*`", "", prose)
    pronouns = re.findall(r"\b(?:[Ww]e|[Oo]ur|[Uu]s|I|[Mm]y)\b", prose)
    if pronouns:
        problems.append(f"personal pronouns: {sorted(set(pronouns))}")
    uk = sorted({w for w in re.findall(r"[A-Za-z]+", prose) if w.lower() in UK_WORDS}
                | {w for w in UK.findall(prose) if w.lower() not in UK_OK and w.lower().endswith(("ise", "ised", "ises", "ising", "isation", "our", "ours", "yse", "ysed"))})
    if uk:
        problems.append(f"possible UK spellings: {uk}")
    missing = [k for k in order if k not in bib]
    if missing:
        problems.append(f"citations missing from references.bib: {missing}")
    return problems


# ── Word output ───────────────────────────────────────────────────────────────


def set_text(paragraph, text: str):
    """Replace a template paragraph's text, keeping the first run's formatting."""
    runs = paragraph.runs
    if not runs:
        paragraph.add_run(text)
        return
    runs[0].text = text
    for r in runs[1:]:
        r._r.getparent().remove(r._r)


def add_inline(paragraph, text: str, size=None, bold=False):
    for token in re.split(r"(`[^`]+`|\*\*[^*]+\*\*|\*[^*\s][^*]*\*)", text):
        if not token:
            continue
        if token.startswith("`"):
            run = paragraph.add_run(token[1:-1])
            run.font.name = CODE_FONT
            run._r.get_or_add_rPr().get_or_add_rFonts().set(qn("w:hAnsi"), CODE_FONT)
            run.font.size = Pt((size or 10) - 1)
        elif token.startswith("**"):
            run = paragraph.add_run(token[2:-2])
            run.bold = True
        elif token.startswith("*"):
            run = paragraph.add_run(token[1:-1])
            run.italic = True
        else:
            run = paragraph.add_run(token)
        if bold:
            run.bold = True
        if size and not token.startswith("`"):
            run.font.size = Pt(size)


def _border(cell, edges: dict):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.find(qn("w:tcBorders"))
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge, size in edges.items():
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(size))
        el.set(qn("w:color"), "000000")
        borders.append(el)


def add_table(doc, number: int, caption: str, rows: list[list[str]], resolve_text):
    cap = doc.add_paragraph(style="Table cuption")
    cap.paragraph_format.keep_with_next = True
    add_inline(cap, f"Table {number}. ", bold=True)
    add_inline(cap, resolve_text(caption))
    table = doc.add_table(rows=len(rows), cols=len(rows[0]))
    table.alignment = 1  # centered
    for r, row in enumerate(rows):
        for c, value in enumerate(row):
            cell = table.cell(r, c)
            p = cell.paragraphs[0]
            p.style = doc.styles["Normal"]
            p.paragraph_format.alignment = 0 if c == 0 else 1
            p.paragraph_format.keep_with_next = r < len(rows) - 1
            add_inline(p, resolve_text(value), size=TABLE_PT, bold=(r == 0))
            edges = {}
            if r == 0:
                edges.update(top=8, bottom=4)
            if r == len(rows) - 1:
                edges["bottom"] = 8
            if edges:
                _border(cell, edges)
    doc.add_paragraph()  # space after the table
    return table


def build(meta: dict, blocks, bib: dict, order: list[str], anonymous: bool, out: Path):
    doc = Document(TEMPLATE)
    body = doc.element.body
    head_table = body.find(qn("w:tbl"))
    for el in list(body):  # keep the title block and the section properties
        if el is not head_table and el.tag != qn("w:sectPr"):
            body.remove(el)
    cell = doc.tables[0].cell(0, 0)
    paras = cell.paragraphs
    set_text(paras[0], meta["title"])
    set_text(paras[2], "Anonymous author(s)" if anonymous else meta["authors"])
    set_text(paras[4], "Affiliation withheld for review" if anonymous else meta["affiliation"])
    set_text(paras[14], "* Corresponding author" if anonymous else f"* Corresponding author, e-mail: {meta['email']}")

    tables = {b[1]: n for n, b in enumerate((b for b in blocks if b[0] == "table"), 1)}
    res = lambda text: resolve(text, order, tables, meta, anonymous)

    p = doc.add_paragraph(style="Abstract")
    add_inline(p, "Abstract: ", bold=True)
    add_inline(p, meta["abstract"])
    p = doc.add_paragraph(style="Abstract")
    add_inline(p, "Keywords: ", bold=True)
    add_inline(p, meta["keywords"])

    section = sub = 0
    for b in blocks:
        if b[0] == "h":
            _, level, title, numbered = b
            if anonymous and title == "Acknowledgements":
                break
            if level == 1:
                section, sub = (section + 1, 0) if numbered else (section, sub)
                doc.add_paragraph(f"{section}. {title}" if numbered else title, style="Section Title")
            else:
                sub += 1
                doc.add_paragraph(f"{section}.{sub}. {title}", style="Subheading")
        elif b[0] == "p":
            add_inline(doc.add_paragraph(style="Normal"), res(b[1]))
        elif b[0] == "li":
            p = doc.add_paragraph(style="Normal")
            p.paragraph_format.left_indent = Cm(0.6)
            p.paragraph_format.first_line_indent = Cm(-0.3)
            add_inline(p, "– " + res(b[1]))
        elif b[0] == "table":
            add_table(doc, tables[b[1]], b[2], b[3], res)

    doc.add_paragraph("References", style="Section Title")
    for key in order:
        doc.add_paragraph(ieee_reference(bib[key]), style="References")

    for b in (b for b in blocks if b[0] == "table"):  # every table again, on a page of its own
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        add_table(doc, tables[b[1]], b[2], b[3], res)

    props = doc.core_properties
    props.author = "" if anonymous else meta["authors"].rstrip("*")
    props.title, props.comments, props.last_modified_by = meta["title"], "", ""
    doc.save(out)


def main():
    meta, blocks = parse_source(SOURCE.read_text())
    bib = parse_bib(BIB.read_text())
    order = number_citations(blocks)
    problems = check(meta, blocks, order, bib)
    for anonymous, name in ((False, "pollack_paper.docx"), (True, "pollack_paper_anonymous.docx")):
        build(meta, blocks, bib, order, anonymous, HERE / name)
        print(f"written {name}")

    prose = " ".join(b[1] for b in blocks if b[0] in ("p", "li"))
    n_tables = sum(b[0] == "table" for b in blocks)
    chars = len(prose) + len(meta["abstract"])
    print(f"title {len(meta['title'])} characters, abstract {len(meta['abstract'])} characters, "
          f"{len(meta['keywords'].split(','))} keywords")
    print(f"text {len(prose.split())} words / {chars:,} characters with spaces, {n_tables} tables, "
          f"{len(order)} references")
    # The template's 12.5 x 18.7 cm text area takes about 3,300 characters of 10-pt Times per page.
    pages = chars / 3300 + 0.6 * n_tables + len(order) / 16 + 1
    print(f"estimate: about {pages:.0f} template pages (the limit is 10-14); check the page count in Word")
    gaps = {k: incomplete(bib[k]) for k in order if incomplete(bib[k])}
    if gaps:
        print("references to complete (Pollack asks for all authors, and city, country, dates and pages):")
        for k, g in gaps.items():
            print(f"  [{order.index(k) + 1}] {k}: {', '.join(g)}")
    for prob in problems:
        print("CHECK:", prob)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
