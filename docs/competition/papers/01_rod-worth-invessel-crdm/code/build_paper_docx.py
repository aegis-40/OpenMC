# -*- coding: utf-8 -*-
"""Render PAPER-DRAFT.md as a clean submission-style manuscript DOCX.

Differences from the working markdown:
  * soft-wrapped source lines are joined into real paragraphs
  * body text is justified, Times New Roman throughout
  * editorial scaffolding is stripped - draft-status note, target-journal
    line, name-confirmation note, [TODO]/[verify] markers and the
    verification annotations on the reference list
The markdown keeps all of that; the DOCX is the clean reading copy.
"""
import io, os, re
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

BASE = (r"D:\projects\teknofest-2026-aegis-40-ipwr\docs\competition\papers"
        r"\01_rod-worth-invessel-crdm")
SRC = os.path.join(BASE, "PAPER-DRAFT.md")
OUT = os.path.join(BASE, "Aegis40-SBF-rod-worth-manuscript.docx")

FONT = "Times New Roman"
BODY_PT = 12
GREY = RGBColor(0x44, 0x44, 0x44)

doc = docx.Document()
sec = doc.sections[0]
sec.left_margin = sec.right_margin = Inches(1.0)
sec.top_margin = sec.bottom_margin = Inches(1.0)

st = doc.styles["Normal"]
st.font.name = FONT
st.font.size = Pt(BODY_PT)
st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
st.element.rPr.rFonts.set(qn("w:cs"), FONT)
st.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
st.paragraph_format.space_after = Pt(6)
st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

for h, sz in (("Heading 1", 14), ("Heading 2", 12.5)):
    s = doc.styles[h]
    s.font.name = FONT
    s.font.size = Pt(sz)
    s.font.bold = True
    s.font.color.rgb = RGBColor(0, 0, 0)
    s.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    s.paragraph_format.space_before = Pt(14)
    s.paragraph_format.space_after = Pt(6)
    s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

# ------------------------------------------------------------------ cleaning
DROP_LINE = re.compile(
    r"^\s*(\*\(Samira Achilova|\*\*Target journal:|>\s*\*\*Draft status)")
MARKER = re.compile(r"\*\*\[[^\]]*\]\*\*|\[TODO\]|\[verify[^\]]*\]")


def clean(text, is_ref=False):
    """Strip editorial scaffolding from a line of manuscript text."""
    if is_ref:
        for tok in ("✅", "⚠"):
            i = text.find(tok)
            if i != -1:
                text = text[:i]
    text = MARKER.sub("", text)
    text = re.sub(r"[–—-]\s*\.", ".", text)      # dangling dash before a stop
    text = re.sub(r"\s+([.,;])", r"\1", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text


INLINE = re.compile(r"(\*\*.+?\*\*|(?<!\*)\*[^*]+?\*(?!\*)|`[^`]+?`)")


def emit(par, text, base_size=None, color=None, base_italic=False):
    text = text.replace("\\*", "\u2217").replace("\\_", "_")
    for piece in INLINE.split(text):
        if not piece:
            continue
        bold = italic = mono = False
        if piece.startswith("**") and piece.endswith("**"):
            piece, bold = piece[2:-2], True
        elif piece.startswith("*") and piece.endswith("*"):
            piece, italic = piece[1:-1], True
        elif piece.startswith("`") and piece.endswith("`"):
            piece, mono = piece[1:-1], True
        r = par.add_run(piece.replace("\u2217", "*"))
        r.font.name = FONT
        if mono:
            r.italic = True
        r.font.size = Pt(base_size or BODY_PT)
        r.bold, r.italic = bold, italic or base_italic
        if color is not None:
            r.font.color.rgb = color
    return par


lines = io.open(SRC, encoding="utf-8").read().split("\n")

# ------------------------------------------------------------------ title
title = lines[0].lstrip("# ").strip()
p = doc.add_paragraph()
p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(14)
r = p.add_run(title)
r.bold, r.font.size, r.font.name = True, Pt(15), FONT

i, n = 1, len(lines)
in_refs = False
buf = []


def flush():
    """Emit any accumulated soft-wrapped lines as one justified paragraph."""
    global buf
    if not buf:
        return
    txt = clean(" ".join(buf))
    buf = []
    if txt:
        par = doc.add_paragraph()
        par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        emit(par, txt)


while i < n:
    raw = lines[i]
    s = raw.strip()

    if DROP_LINE.match(raw):
        flush(); i += 1; continue

    # ---- tables
    if s.startswith("|"):
        flush()
        rows = []
        while i < n and lines[i].strip().startswith("|"):
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                rows.append(cells)
            i += 1
        if rows:
            ncol = max(len(r_) for r_ in rows)
            t = doc.add_table(rows=0, cols=ncol)
            t.style = "Table Grid"
            t.alignment = WD_TABLE_ALIGNMENT.CENTER
            for ri, row in enumerate(rows):
                cells = t.add_row().cells
                for ci in range(ncol):
                    cp = cells[ci].paragraphs[0]
                    cp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                    cp.paragraph_format.space_after = Pt(2)
                    cp.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    emit(cp, clean(row[ci] if ci < len(row) else ""), base_size=9.5)
                    if ri == 0:
                        for rr in cp.runs:
                            rr.bold = True
            doc.add_paragraph().paragraph_format.space_after = Pt(4)
        continue

    # ---- figure blocks
    if s.startswith(">"):
        flush()
        block = []
        while i < n and lines[i].strip().startswith(">"):
            block.append(lines[i].strip().lstrip(">").strip())
            i += 1
        img, keep = None, []
        for b in block:
            m = re.fullmatch(r"`(figures/[^`]+)`", b)
            if m:
                img = os.path.join(BASE, m.group(1).replace("/", os.sep))
            elif b:
                keep.append(b)
        if img and os.path.exists(img):
            ip = doc.add_paragraph()
            ip.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            ip.add_run().add_picture(img, width=Inches(6.2))
            ip.paragraph_format.space_before = Pt(8)
            ip.paragraph_format.space_after = Pt(4)
        cap = doc.add_paragraph()
        cap.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        cap.paragraph_format.space_after = Pt(10)
        cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        emit(cap, clean(" ".join(keep)), base_size=10)
        continue

    # ---- headings
    if s.startswith("### ") or s.startswith("## "):
        flush()
        lvl = 2 if s.startswith("### ") else 1
        h = s[4:].strip() if lvl == 2 else s[3:].strip()
        in_refs = h.lower().startswith("references")
        doc.add_heading(h, level=lvl)
        i += 1
        continue

    if s == "---":
        flush(); i += 1; continue

    # ---- numbered items (references / conclusions)
    m = re.match(r"^(\d+)\.\s+(.*)", s)
    if m:
        flush()
        body = clean(m.group(2), is_ref=in_refs)
        if not body:
            i += 1; continue
        par = doc.add_paragraph()
        par.paragraph_format.left_indent = Inches(0.35)
        par.paragraph_format.first_line_indent = Inches(-0.35)
        par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if in_refs:
            par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            par.paragraph_format.space_after = Pt(6)
        emit(par, "[%s]  %s" % (m.group(1), body) if in_refs
             else "%s.  %s" % (m.group(1), body),
             base_size=10.5 if in_refs else None)
        i += 1
        continue

    if not s:
        flush(); i += 1; continue

    # ---- centred display equation (two-space indent in source)
    if raw.startswith("  ") and not raw.startswith("   -"):
        flush()
        par = doc.add_paragraph()
        par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.space_before = Pt(4)
        par.paragraph_format.space_after = Pt(4)
        emit(par, clean(s))
        i += 1
        continue

    buf.append(s)
    i += 1

flush()
doc.save(OUT)
print("saved:", OUT)
print("size: %.1f KB" % (os.path.getsize(OUT) / 1024))
