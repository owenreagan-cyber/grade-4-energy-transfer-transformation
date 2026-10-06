"""Reusable visible-text extraction for chapter golden baselines.

DOCX and PPTX are the canonical sources. PDF text is for export checks only.
Normalization keeps display case. It does not drop or reorder blocks.
"""
import re


def norm_line(s):
    s = s.replace("\u2014", "-").replace("\u2013", "-").replace("—", "-")
    s = s.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2026", "...")
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r"\n{2,}", "\n", s).strip()
    return s


def docx_lines(path):
    from docx import Document
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    d = Document(path)
    out = []
    for child in d.element.body.iterchildren():
        if child.tag.endswith("}p"):
            text = norm_line(Paragraph(child, d).text)
            if text:
                out.append(text)
        elif child.tag.endswith("}tbl"):
            table = Table(child, d)
            for row in table.rows:
                cells = []
                prev = None
                for cell in row.cells:
                    text = norm_line(cell.text)
                    if text and text != prev:
                        cells.append(text)
                        prev = text
                if cells:
                    out.append(" | ".join(cells))
    return out


def pptx_slides(path):
    from pptx import Presentation
    prs = Presentation(path)
    slides = []
    for i, slide in enumerate(prs.slides, 1):
        shapes = sorted(slide.shapes, key=lambda s: ((s.top or 0), (s.left or 0)))
        lines = []
        for sh in shapes:
            if not sh.has_text_frame:
                continue
            for p in sh.text_frame.paragraphs:
                text = norm_line(p.text)
                if text:
                    lines.append(text)
        note = ""
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
            note = norm_line(slide.notes_slide.notes_text_frame.text)
        slides.append({"slide": i, "lines": lines, "speaker": note})
    return slides


def diff_lines(expected, actual):
    """Return added, removed, and a short change list. Order-sensitive."""
    import difflib
    sm = difflib.SequenceMatcher(a=expected, b=actual)
    added, removed, changed = [], [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "delete":
            removed.extend(expected[i1:i2])
        elif tag == "insert":
            added.extend(actual[j1:j2])
        else:
            changed.append({
                "expected": expected[i1:i2],
                "actual": actual[j1:j2],
            })
    return added, removed, changed
