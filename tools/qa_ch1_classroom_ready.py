#!/usr/bin/env python3
"""Fast deterministic QA for the Chapter 1 classroom-ready wrapper."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "production/classroom-ready/week-2026-10-12/chapter-01"
SRC = ROOT / "production/releases/chapter-01"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def text(path: Path) -> str:
    return "\n".join((page.extract_text() or "") for page in PdfReader(str(path)).pages)


def pages(path: Path) -> int:
    return len(PdfReader(str(path)).pages)


def page_size(path: Path):
    page = PdfReader(str(path)).pages[0]
    return round(float(page.mediabox.width)), round(float(page.mediabox.height))


def pptx_slide_count(path: Path) -> int:
    with zipfile.ZipFile(path) as archive:
        return sum(1 for name in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", name))


def main() -> int:
    results = []

    def check(name, ok, detail):
        results.append((name, "PASS" if ok else "FAIL", detail))

    required = [
        "README_PRINT_FIRST.md",
        "01_TEACHER/Chapter_1_Teacher_Packet_Classroom_Ready.pdf",
        "01_TEACHER/Materials_and_Prep.pdf",
        "02_STUDENT_PRINT/Chapter_1_Guided_Notes.pdf",
        "02_STUDENT_PRINT/Chapter_1_Practice.pdf",
        "02_STUDENT_PRINT/Chapter_1_Check.pdf",
        "02_STUDENT_PRINT/Chapter_1_Student_Print_Packet.pdf",
        "03_SLIDES/Chapter_1_Slides.pptx",
        "03_SLIDES/Chapter_1_Slides.pdf",
        "04_EXTENSIONS/Energy_Detectives_Optional.pdf",
        "05_OPTIONAL_MEDIA/MEDIA_GUIDE.md",
        "06_KEYS/Guided_Notes_Key.pdf",
        "06_KEYS/Practice_Key.pdf",
        "06_KEYS/Check_Key.pdf",
        "06_KEYS/Energy_Detectives_Optional_Key.pdf",
    ]
    for rel in required:
        check(f"inventory: {rel}", (OUT / rel).is_file(), "present")

    copies = {
        "02_STUDENT_PRINT/Chapter_1_Guided_Notes.pdf": "01-ch1-energy-causes-change-guided-notes.pdf",
        "02_STUDENT_PRINT/Chapter_1_Practice.pdf": "01-ch1-energy-causes-change-practice.pdf",
        "02_STUDENT_PRINT/Chapter_1_Check.pdf": "01-ch1-energy-causes-change-quiz.pdf",
        "03_SLIDES/Chapter_1_Slides.pptx": "01-ch1-energy-causes-change-slides.pptx",
        "03_SLIDES/Chapter_1_Slides.pdf": "01-ch1-energy-causes-change-slides.pdf",
        "04_EXTENSIONS/Energy_Detectives_Optional.pdf": "01-ch1-energy-detectives-student.pdf",
        "06_KEYS/Guided_Notes_Key.pdf": "01-ch1-energy-causes-change-guided-notes-key.pdf",
    }
    for dst, src in copies.items():
        ok = sha256(OUT / dst) == sha256(SRC / src)
        check(f"frozen copy parity: {dst}", ok, "byte-identical" if ok else "hash mismatch")

    expected_pages = {
        "01_TEACHER/Chapter_1_Teacher_Packet_Classroom_Ready.pdf": 12,
        "01_TEACHER/Materials_and_Prep.pdf": 1,
        "02_STUDENT_PRINT/Chapter_1_Guided_Notes.pdf": 3,
        "02_STUDENT_PRINT/Chapter_1_Practice.pdf": 2,
        "02_STUDENT_PRINT/Chapter_1_Check.pdf": 2,
        "02_STUDENT_PRINT/Chapter_1_Student_Print_Packet.pdf": 7,
        "03_SLIDES/Chapter_1_Slides.pdf": 45,
        "04_EXTENSIONS/Energy_Detectives_Optional.pdf": 2,
        "06_KEYS/Guided_Notes_Key.pdf": 3,
        "06_KEYS/Practice_Key.pdf": 2,
        "06_KEYS/Check_Key.pdf": 2,
        "06_KEYS/Energy_Detectives_Optional_Key.pdf": 1,
    }
    for rel, expected in expected_pages.items():
        actual = pages(OUT / rel)
        check(f"page count: {rel}", actual == expected, f"{actual} pages")

    for rel in [
        "01_TEACHER/Chapter_1_Teacher_Packet_Classroom_Ready.pdf",
        "01_TEACHER/Materials_and_Prep.pdf",
        "02_STUDENT_PRINT/Chapter_1_Guided_Notes.pdf",
        "02_STUDENT_PRINT/Chapter_1_Practice.pdf",
        "02_STUDENT_PRINT/Chapter_1_Check.pdf",
        "02_STUDENT_PRINT/Chapter_1_Student_Print_Packet.pdf",
        "04_EXTENSIONS/Energy_Detectives_Optional.pdf",
        "06_KEYS/Guided_Notes_Key.pdf",
        "06_KEYS/Practice_Key.pdf",
        "06_KEYS/Check_Key.pdf",
        "06_KEYS/Energy_Detectives_Optional_Key.pdf",
    ]:
        size = page_size(OUT / rel)
        check(f"US Letter: {rel}", size == (612, 792), f"{size[0]}x{size[1]} pt")

    slide_pdf_size = page_size(OUT / "03_SLIDES/Chapter_1_Slides.pdf")
    check("slides: 16:9 PDF", slide_pdf_size == (960, 540), f"{slide_pdf_size[0]}x{slide_pdf_size[1]} pt")
    count = pptx_slide_count(OUT / "03_SLIDES/Chapter_1_Slides.pptx")
    check("slides: PPTX count", count == 45, f"{count} slides")

    packet = PdfReader(str(OUT / "02_STUDENT_PRINT/Chapter_1_Student_Print_Packet.pdf"))
    expected_texts = []
    for rel in (
        "02_STUDENT_PRINT/Chapter_1_Guided_Notes.pdf",
        "02_STUDENT_PRINT/Chapter_1_Practice.pdf",
        "02_STUDENT_PRINT/Chapter_1_Check.pdf",
    ):
        expected_texts.extend((page.extract_text() or "") for page in PdfReader(str(OUT / rel)).pages)
    actual_texts = [(page.extract_text() or "") for page in packet.pages]
    check("student packet: exact page order", actual_texts == expected_texts, "notes 1-3, practice 1-2, check 1-2")

    teacher_text = text(OUT / "01_TEACHER/Chapter_1_Teacher_Packet_Classroom_Ready.pdf")
    required_teacher_phrases = [
        "Chapter Overview", "Where can we observe evidence of energy causing change?",
        "Session 1 Observe and Name", "Session 2 Forms and Stored Energy",
        "Session 3 Recognize Reflect and Check", "Electric Pencil Sharpener Demonstration",
        "Guided Notes and Slide Anchor Map", "What to Collect and How to Grade",
        "Absent Student", "Optional Energy Detectives", "Optional Media Decision",
        "Gold-standard version 1.1 remains authoritative",
    ]
    missing = [phrase for phrase in required_teacher_phrases if phrase not in teacher_text]
    check("teacher packet: required sections", not missing, f"missing {missing or 'none'}")

    notes_text = text(OUT / "02_STUDENT_PRINT/Chapter_1_Guided_Notes.pdf")
    notes_key_text = text(OUT / "06_KEYS/Guided_Notes_Key.pdf")
    for anchor in ("BQ", "V1", "N1", "N2", "V2", "N3", "N4"):
        check(f"notes/key anchor: {anchor}", anchor in notes_text and anchor in notes_key_text, "present in both")
    for answer in ("change", "different", "evidence", "later", "position"):
        check(f"guided key answer: {answer}", answer in notes_key_text.lower(), "present")

    check_text = text(OUT / "02_STUDENT_PRINT/Chapter_1_Check.pdf")
    key_text = text(OUT / "06_KEYS/Check_Key.pdf")
    check("check: 16-point raw and percent line", "SCORE:" in check_text and "/ 16" in check_text and "%" in check_text, "raw + percentage")
    check(
        "check key: answer sequence",
        all(x in key_text for x in ("c) cause change", "b) evidence", "a) has stored energy", "a YES; b NO; c YES")),
        "items 1, 2, 7, 9",
    )

    readme = (OUT / "README_PRINT_FIRST.md").read_text(encoding="utf-8")
    check("README: 20-student count", "140 printed page sides" in readme and "80 sheets" in readme, "20 x 7 pages")
    media = (OUT / "05_OPTIONAL_MEDIA/MEDIA_GUIDE.md").read_text(encoding="utf-8")
    check("media: missing upload disclosed", "was not present" in media and "DO NOT USE" in media, "lesson independent of video")

    manifest = OUT / "CLASSROOM_READY_MANIFEST.json"
    if manifest.is_file():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        check("manifest: frozen version", data.get("goldStandardVersion") == "1.1" and data.get("goldStandardStatus") == "UNCHANGED", "version 1.1 unchanged")

    failures = [row for row in results if row[1] == "FAIL"]
    for name, status, detail in results:
        print(f"{status:4} {name}: {detail}")
    print(f"OVERALL: {'FAIL' if failures else 'PASS'} ({len(results) - len(failures)}/{len(results)} gates)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
