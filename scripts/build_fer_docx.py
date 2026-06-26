"""Compile Samira's FER sections (§8.2 Core, §8.3 Fuel, §8.9 Energy Cycle, §8.11
Waste) into a single styled .docx, template-compliant (Arial 12 body / Arial Black
titles, 1.15 spacing, justified, 2.5 cm margins), with all tables, embedded figures,
references, and prominent placeholders where a 3D tech drawing must be inserted.

Sources (docs/competition/fer/*.md) authored this project; figures from
docs/competition/{cad,cycle,waste}/*.png. Output:
  docs/competition/fer/Aegis40_FER_NEU-sections.docx

Run:  py scripts/build_fer_docx.py     (requires python-docx)
"""

import os
import re
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "docs", "competition")
FER = os.path.join(BASE, "fer")
OUTDOC = os.path.join(FER, "Aegis40_FER_NEU-sections.docx")

SECTION_FILES = [
    os.path.join(FER, "section-8.1-general-parameters.md"),
    os.path.join(FER, "section-8.2-8.3-core-and-fuel.md"),
    os.path.join(FER, "section-8.4-cooling-circuit.md"),
    os.path.join(FER, "section-8.9-energy-cycle.md"),
    os.path.join(FER, "section-8.11-waste.md"),
    os.path.join(FER, "section-8.12-economics.md"),
    os.path.join(FER, "nonproliferation-assessment.md"),
]

BODY_FONT = "Arial"
TITLE_FONT = "Arial Black"
RED = RGBColor(0x9C, 0x27, 0x12)
GRAY = RGBColor(0x55, 0x55, 0x55)
BLUE = RGBColor(0x1F, 0x4E, 0x79)


# ---------- low-level helpers ------------------------------------------------
def set_cell_shading(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def add_runs(p, text, base_size=12):
    """Render inline **bold**, `code`, and <inline editorial notes> into runs."""
    text = text.replace("‹", "<").replace("›", ">")
    parts = re.split(r"(\*\*.+?\*\*|`.+?`|<[^>]+>)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            r = p.add_run(part[2:-2]); r.bold = True
        elif part.startswith("`") and part.endswith("`"):
            r = p.add_run(part[1:-1]); r.font.name = "Consolas"; r.font.size = Pt(base_size - 1.5)
        elif part.startswith("<") and part.endswith(">"):
            r = p.add_run("[TODO: " + part[1:-1] + "]")
            r.italic = True; r.font.color.rgb = GRAY
        else:
            p.add_run(part)
        for run in p.runs:
            if run.font.name in (None, BODY_FONT):
                run.font.name = BODY_FONT


def style_normal(doc):
    st = doc.styles["Normal"]
    st.font.name = BODY_FONT
    st.font.size = Pt(12)
    st.paragraph_format.line_spacing = 1.15
    st.paragraph_format.space_after = Pt(6)
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Cm(2.5)
        s.left_margin = s.right_margin = Cm(2.5)


def heading(doc, text, size):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.font.name = TITLE_FONT
    r.font.size = Pt(size)
    r.font.color.rgb = BLUE
    r.bold = True
    return p


def body_para(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    add_runs(p, text)
    return p


def bullet(doc, text, numbered=False):
    p = doc.add_paragraph(style="List Number" if numbered else "List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    add_runs(p, text)


def note_block(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.space_before = Pt(2)
    r = p.add_run("▸ ")
    r.font.color.rgb = GRAY
    add_runs(p, text)
    for run in p.runs:
        run.italic = True
        run.font.size = Pt(10.5)
        run.font.color.rgb = GRAY


def render_table(doc, rows):
    header, body = rows[0], rows[1:]
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(header):
        c = t.rows[0].cells[j]
        c.paragraphs[0].text = ""
        add_runs(c.paragraphs[0], h, base_size=10)
        for r in c.paragraphs[0].runs:
            r.bold = True; r.font.size = Pt(10)
        set_cell_shading(c, "DDE3EA")
    for row in body:
        cells = t.add_row().cells
        for j, val in enumerate(row):
            if j >= len(cells):
                break
            cells[j].paragraphs[0].text = ""
            add_runs(cells[j].paragraphs[0], val, base_size=10)
            for r in cells[j].paragraphs[0].runs:
                r.font.size = Pt(10)
    doc.add_paragraph()


def resolve_png(png_rel):
    """Resolve a PNG reference against the figure roots (docs/competition and .../fer)."""
    rel = png_rel.replace("\\", "/")
    for root in (BASE, FER):
        full = os.path.join(root, rel)
        if os.path.exists(full):
            return full
    return None


def embed_figure(doc, png_rel, caption):
    full = resolve_png(png_rel)
    if not full:
        return False
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(full, width=Inches(6.0))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cr = cap.add_run(caption)
    cr.italic = True; cr.font.size = Pt(9.5); cr.font.color.rgb = GRAY
    return True


def techdraw_box(doc, label, desc):
    low = desc.lower()
    # classify the missing asset: 3D drawing vs notebook plot vs results table
    if any(k in low for k in ("results table", "§8.4", "8.4 result", "temperature distribution")):
        kind, src = "TABLE TO INSERT", "from the §8.4 thermal-hydraulic analysis (TH lead)"
    elif any(k in low for k in ("k_eff", "burnup", "depletion", "power map", "power profile",
                                "flux", "tally", "notebook", "reactivity")):
        kind, src = "FIGURE TO INSERT (plot)", \
            "export PNG from the OpenMC depletion notebook (aegis40_3d_core_outputs/)"
    elif any(k in low for k in ("isometric", "rpv", "cutaway")) and "rod" not in low and "pin" not in low:
        kind, src = "3D TECH DRAWING TO INSERT", \
            "render aegis_rpv.step (or aegis_core_context.step) — quarter-cut isometric — in Creo"
    elif any(k in low for k in ("fuel-rod", "fuel rod", "sectioned pin", "pin cutaway", "sectioned-pin", "pin")):
        kind, src = "3D TECH DRAWING TO INSERT", \
            "render aegis_fuel_pin.step — sectioned rod (pellet / gap / clad / plugs) — in Creo"
    elif "assembly" in low:
        kind, src = "3D TECH DRAWING TO INSERT", "render aegis_fuel_assembly.step (17x17 bundle) in Creo"
    else:
        kind, src = "FIGURE TO INSERT", "from the relevant model/analysis"
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = t.rows[0].cells[0]
    set_cell_shading(c, "FFF3CD")
    p = c.paragraphs[0]
    r = p.add_run("■ " + kind)
    r.bold = True; r.font.color.rgb = RED; r.font.size = Pt(11)
    if label:
        rr = p.add_run("   (" + label + ")")
        rr.bold = True; rr.font.size = Pt(10)
    p2 = c.add_paragraph()
    add_runs(p2, desc)
    for run in p2.runs:
        run.font.size = Pt(10)
    p3 = c.add_paragraph()
    r3 = p3.add_run("Suggested source: " + src + ".")
    r3.italic = True; r3.font.size = Pt(9.5); r3.font.color.rgb = GRAY
    doc.add_paragraph()


# ---------- markdown parsing -------------------------------------------------
PNG_RE = re.compile(r"([\w./\\-]+\.png)")
FIGLABEL_RE = re.compile(r"(?:FIGURE|Figure)\s+([\d.\-]+)")


def heading_level(text):
    m = re.match(r"^(?:FER\s+)?[§]?\s*(\d+\.\d+(?:\.\d+)?)", text)
    if m:
        return 2 if m.group(1).count(".") >= 2 else 1
    return 1


def clean_heading(text):
    return text.replace("FER ", "").strip()


def figure_caption(text, label):
    t = re.sub(r"\([^)]*\.png[^)]*\)", "", text)       # drop (…png…) parentheticals
    t = t.replace("**", "").replace("`", "").replace("‹", "").replace("›", "")
    if "—" in t:
        t = t.split("—", 1)[1]
    t = re.sub(r"^\s*(?:INSERT\s+)?FIGURE\s+[\d.\-]+", "", t, flags=re.I).strip()
    t = t.lstrip("—:- ").strip()
    if t.lower().startswith("is "):
        t = t[3:]
    t = re.split(r"[:.]\s|\bShows\b|\bSource\b|\bGenerated\b|\bUse\b", t)[0].strip().rstrip(".")
    lbl = "Figure " + label if label else "Figure"
    return lbl + (" — " + t[:130] if t else "")


def process_file(doc, path, embedded):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    i, n = 0, len(lines)
    skip_file = False
    while i < n:
        line = lines[i]
        s = line.strip()

        if not s:
            i += 1
            continue

        # headings
        if s.startswith("#"):
            txt = s.lstrip("#").strip()
            low = txt.lower()
            if any(k in low for k in ("checklist", "to-resolve", "figure / table")):
                skip_file = True
            if skip_file:
                i += 1
                continue
            if "Aegis-40" in txt and "—" in txt:        # banner file-title, skip
                i += 1
                continue
            lvl = heading_level(txt)
            heading(doc, clean_heading(txt), 14 if lvl == 1 else 12.5)
            i += 1
            continue
        if skip_file:
            i += 1
            continue

        # standalone INSERT callout (figure or tech-drawing placeholder)
        callout = s.lstrip(">").strip().lstrip("*").strip()
        if callout.startswith("‹INSERT") or callout.startswith("<INSERT"):
            block = s
            while not block.rstrip().endswith(("›", ">")) and i + 1 < n and lines[i + 1].strip():
                i += 1
                block += " " + lines[i].strip()
            txt = block.replace("‹", "").replace("›", "").lstrip(">").strip().lstrip("*").strip()
            label = FIGLABEL_RE.search(txt)
            label = label.group(1) if label else ""
            png = PNG_RE.search(txt)
            png_ok = png and resolve_png(png.group(1))
            if png_ok and os.path.normpath(png.group(1)) not in embedded:
                embed_figure(doc, png.group(1), figure_caption(txt, label))
                embedded.add(os.path.normpath(png.group(1)))
            else:
                desc = txt.split("—", 1)[1].strip() if "—" in txt else txt
                techdraw_box(doc, "Figure " + label if label else "", desc)
            i += 1
            continue

        # markdown image  ![alt](path.png)  — embed; use a following **Figure …** line as caption
        m_img = re.match(r"^!\[(.*?)\]\(([^)]+\.png)\)", s)
        if m_img:
            alt, png = m_img.group(1), m_img.group(2)
            caption = alt
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            if j < n and lines[j].strip().startswith("**Figure"):
                caption = lines[j].strip().replace("**", "")
                i = j  # consume the bold caption line too
            if resolve_png(png):
                if os.path.normpath(png) not in embedded:
                    embed_figure(doc, png, caption)
                    embedded.add(os.path.normpath(png))
            else:
                techdraw_box(doc, alt, caption)
            i += 1
            continue

        # tables
        if s.startswith("|"):
            tbl = []
            while i < n and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not re.match(r"^[\s\-:]+$", "".join(cells)):   # skip --- separator
                    tbl.append(cells)
                i += 1
            if tbl:
                render_table(doc, tbl)
            continue

        # blockquote
        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            text = " ".join(x for x in buf if x)
            low = text.lower()
            if any(k in low for k in ("drafting status", "status:", "citation discipline",
                                      "owner interface")):
                continue
            note_block(doc, text)
            for pth in PNG_RE.findall(text):
                if resolve_png(pth) and os.path.normpath(pth) not in embedded:
                    lbl = FIGLABEL_RE.search(text)
                    embed_figure(doc, pth, figure_caption(text, lbl.group(1) if lbl else ""))
                    embedded.add(os.path.normpath(pth))
            continue

        # bullets / numbered
        m_b = re.match(r"^[-*]\s+(.*)", s)
        m_n = re.match(r"^\d+\.\s+(.*)", s)
        if m_b or m_n:
            txt = (m_b or m_n).group(1)
            j = i + 1
            while j < n and not lines[j].strip().startswith(("-", "*")) and \
                    not re.match(r"^\d+\.\s", lines[j].strip()) and lines[j].strip() and \
                    not lines[j].strip().startswith(("#", "|", ">", "‹")):
                txt += " " + lines[j].strip()
                j += 1
            bullet(doc, txt, numbered=bool(m_n))
            i = j
            continue

        # paragraph (join wrapped lines)
        para = [s]
        i += 1
        while i < n and lines[i].strip() and not lines[i].strip().startswith(
                ("#", "|", ">", "-", "*", "‹", "<INSERT")) and not re.match(r"^\d+\.\s", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        text = " ".join(para)
        body_para(doc, text)
        for pth in PNG_RE.findall(text):
            if resolve_png(pth) and os.path.normpath(pth) not in embedded:
                lbl = FIGLABEL_RE.search(text)
                embed_figure(doc, pth, figure_caption(text, lbl.group(1) if lbl else ""))
                embedded.add(os.path.normpath(pth))


def main():
    doc = Document()
    style_normal(doc)

    # cover banner
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("Aegis-40 iPWR — Final Evaluation Report")
    r.font.name = TITLE_FONT; r.font.size = Pt(18); r.font.color.rgb = BLUE; r.bold = True
    sub = doc.add_paragraph(); sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rs = sub.add_run("§8.1 General · §8.2 Core · §8.3 Fuel · §8.4 Cooling Circuit · "
                     "§8.9 Energy Cycle · §8.11 Waste · §8.12 Economics · Non-proliferation (3S)")
    rs.font.size = Pt(12); rs.italic = True
    note = doc.add_paragraph(); note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rn = note.add_run("Compiled draft. Styling per FER template (Arial 12 / Arial Black titles, "
                      "1.15 spacing, justified, 2.5 cm margins). Yellow boxes mark 3D tech drawings to insert.")
    rn.font.size = Pt(9.5); rn.font.color.rgb = GRAY
    doc.add_paragraph()

    embedded = set()
    for path in SECTION_FILES:
        process_file(doc, path, embedded)
        doc.add_page_break()

    doc.save(OUTDOC)
    # validation
    d2 = Document(OUTDOC)
    n_imgs = len(d2.inline_shapes)
    print("wrote", OUTDOC)
    print("  paragraphs=%d  tables=%d  images=%d  (%.2f MB)" %
          (len(d2.paragraphs), len(d2.tables), n_imgs, os.path.getsize(OUTDOC) / 1024 / 1024))


if __name__ == "__main__":
    main()
