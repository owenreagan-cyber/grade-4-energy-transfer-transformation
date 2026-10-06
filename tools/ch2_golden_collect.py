"""Collect the Chapter 2 instructional text the golden baseline protects."""
import os, re
from docx.oxml.ns import qn
from chapter_text import docx_lines, norm_line, pptx_slides

ROOT_FILES = {
    "guided_notes": "production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes.docx",
    "guided_notes_key": "production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes-key.docx",
    "slides": "production/slides/02-ch2-moving-objects-have-energy-slides.pptx",
    "quiz": "production/quizzes/02-ch2-moving-objects-have-energy-quiz.docx",
    "practice": "production/worksheets/02-ch2-moving-objects-have-energy-practice.docx",
    "moving_marbles": "production/worksheets/02-ch2-moving-marbles-student.docx",
    "friday_flex": "production/worksheets/02-ch2-friday-flex.docx",
    "recovery": "production/worksheets/02-ch2-absent-student-recovery.docx",
    "playbook": "production/teacher-playbook/unit1-teacher-playbook.docx",
}
KEY_FILES = [
    "production/answer-keys/02-ch2-moving-objects-have-energy-quiz-key.md",
    "production/answer-keys/02-ch2-moving-objects-have-energy-practice-key.md",
    "production/answer-keys/02-ch2-moving-marbles-key.md",
    "production/answer-keys/02-ch2-friday-flex-key.md",
]
# Structural Playbook boundaries. These are section headings (bottom border), not body filters.
CH2_START = "CHAPTER 2 - TEACHER SPREAD"


def _md_lines(path):
    lines = []
    for raw in open(path, encoding="utf-8"):
        text = norm_line(raw)
        if text:
            lines.append(text)
    return lines


def _bottom_border(p_elm):
    pPr = p_elm.find(qn("w:pPr"))
    if pPr is None:
        return False
    pBdr = pPr.find(qn("w:pBdr"))
    return pBdr is not None and pBdr.find(qn("w:bottom")) is not None


def _other_chapter_heading(text):
    """A section heading that opens a chapter other than Chapter 2."""
    if text.startswith("CHAPTERS "):
        return True
    return text.startswith("CHAPTER ") and not text.startswith("CHAPTER 2")


def _row_line(row):
    cells = []
    prev = None
    for cell in row.cells:
        text = norm_line(cell.text)
        if text and text != prev:
            cells.append(text)
            prev = text
    return " | ".join(cells)


def playbook_chapter_region(path):
    """Every paragraph and table row from the Chapter 2 heading until the next chapter heading.

    Inclusion does not depend on wording. Chapter 1 material before the Chapter 2 heading
    stays out. Chapter 3 and later stay out. Unit sections that sit between those two
    headings are inside the region because they are inside the structural span.
    """
    from docx import Document
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    d = Document(path)
    capturing = False
    lines, paragraphs, rows = [], [], []
    for child in d.element.body.iterchildren():
        if child.tag == qn("w:p"):
            text = norm_line(Paragraph(child, d).text)
            if _bottom_border(child) and text:
                if not capturing:
                    if text == CH2_START:
                        capturing = True
                    else:
                        continue
                elif _other_chapter_heading(text):
                    break
            if not capturing or not text:
                continue
            lines.append(text)
            paragraphs.append(text)
        elif child.tag == qn("w:tbl") and capturing:
            table = Table(child, d)
            for row in table.rows:
                line = _row_line(row)
                if line:
                    lines.append(line)
                    rows.append(line)
    return {"lines": lines, "paragraphs": paragraphs, "rows": rows}


def _playbook_ch2(path):
    return playbook_chapter_region(path)["lines"]


def collect(root):
    data = {"artifacts": {}}
    for key, rel in ROOT_FILES.items():
        path = os.path.join(root, rel)
        if key == "slides":
            data["artifacts"][key] = {"path": rel, "slides": pptx_slides(path)}
        elif key == "playbook":
            data["artifacts"][key] = {"path": rel, "lines": _playbook_ch2(path)}
        else:
            data["artifacts"][key] = {"path": rel, "lines": docx_lines(path)}
    keys = []
    for rel in KEY_FILES:
        keys.append({"path": rel, "lines": _md_lines(os.path.join(root, rel))})
    data["artifacts"]["teacher_keys"] = keys
    return data


def exact_chrome(collected):
    """Full lines only. A longer sentence is never chrome just because it shares a prefix."""
    badge = {
        "write", "check", "observe", "before", "after", "draw", "sample", "n", "r", "c",
        "bq", "v1", "v2", "n1", "n2", "n3", "big question",
    }
    found = set()
    for slide in collected["artifacts"]["slides"]["slides"]:
        for line in slide["lines"]:
            n = line.lower()
            if n in badge or re.fullmatch(r"\d+", n):
                found.add(line)
            elif n == "chapter 2 · moving objects have energy" or n == "chapter 2 - moving objects have energy":
                found.add(line)
            elif re.fullmatch(r"guided notes( · reader pp?\. [\d–-]+)?", n) or re.fullmatch(r"guided notes p\. \d+", n):
                found.add(line)
            elif re.fullmatch(r"reader pp?\. [\d–-]+", n):
                found.add(line)
            elif n in ("big question - my first thinking", "bq - now i think"):
                found.add(line)
            elif _label_only(n):
                found.add(line)
    for key in ("guided_notes", "guided_notes_key"):
        for line in collected["artifacts"][key]["lines"]:
            n = line.lower()
            if re.fullmatch(r"reader pp?\. [\d–-]+", n):
                found.add(line)
            elif re.match(r"^(bq|v1|v2|n1|n2|n3|check)\b", n) and "how are energy" not in n and "____" not in line and "___" not in line:
                found.add(line)
            elif _label_only(n):
                found.add(line)
    return sorted(found)


def _label_only(n):
    """Period-free diagram labels. Semantic QA only. Golden compare does not use this."""
    if "." in n or "?" in n:
        return False
    words = re.findall(r"[a-z0-9]+", n)
    allowed = {"moving", "object", "change", "evidence", "before", "after", "what", "does", "it", "cause"}
    return bool(words) and set(words) <= allowed
