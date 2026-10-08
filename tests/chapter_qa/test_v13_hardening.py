"""Chapter 3 v1.3 factory-hardening canaries.

OOXML canonical identity, prompt-gate clean controls, and the sensor-collision
regression. Each is a machine-checkable same-run canary, not a certification.
"""

from __future__ import annotations

import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from qa_ooxml import canonical_oo_xml_hash  # noqa: E402

WORK = ROOT / "qa" / "work" / "_v13"


def _docx(name: str, text: str) -> Path:
    from docx import Document
    document = Document()
    document.add_paragraph(text)
    p = WORK / name
    p.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(p))
    return p


def _rezip(src: Path, dest: Path, year: int) -> None:
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dest, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            new_info = zipfile.ZipInfo(info.filename, date_time=(year, 1, 1, 0, 0, 0))
            new_info.compress_type = info.compress_type
            new_info.external_attr = info.external_attr
            zout.writestr(new_info, data)


def _rewrite_member(src: Path, dest: Path, member: str, transform) -> None:
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dest, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == member:
                data = transform(data)
            zout.writestr(info, data)


class CanonicalOOXMLTests(unittest.TestCase):
    def test_zip_timestamp_does_not_change_canonical_hash(self):
        a = _docx("canon-a.docx", "hello world")
        b = WORK / "canon-b.docx"
        _rezip(a, b, 2001)
        self.assertEqual(canonical_oo_xml_hash(str(a)), canonical_oo_xml_hash(str(b)))

    def test_xml_text_change_changes_canonical_hash(self):
        a = _docx("canon-c.docx", "hello world")
        b = WORK / "canon-d.docx"
        _rewrite_member(a, b, "word/document.xml", lambda data: data.replace(b"hello", b"world"))
        self.assertNotEqual(canonical_oo_xml_hash(str(a)), canonical_oo_xml_hash(str(b)))

    def test_embedded_image_change_changes_canonical_hash(self):
        a = _docx("canon-e.docx", "hello world")
        with_img = WORK / "canon-f.docx"
        with zipfile.ZipFile(a) as zin, zipfile.ZipFile(with_img, "w") as zout:
            for info in zin.infolist():
                zout.writestr(info, zin.read(info.filename))
            zout.writestr("word/media/image1.png", b"image-bytes-v1")
        changed = WORK / "canon-g.docx"
        _rewrite_member(with_img, changed, "word/media/image1.png", lambda _data: b"image-bytes-v2")
        self.assertNotEqual(canonical_oo_xml_hash(str(with_img)), canonical_oo_xml_hash(str(changed)))


class PromptGateCleanControlTests(unittest.TestCase):
    def test_ramp_height_is_not_speed_is_not_a_boundary_violation(self):
        from chapter_qa.text_extraction import family_hits
        self.assertNotIn("ramp_is_speed", family_hits("Ramp height is not a speed."))
        self.assertNotIn("ramp_is_speed", family_hits("Ramp height is not speed."))
        self.assertIn("ramp_is_speed", family_hits("Ramp height tells us the ball speed."))

    def test_what_happened_with_explicit_referent_is_not_vague(self):
        from chapter_qa.student_prompt import assess_prompts
        prompts = [{"artifact": "quiz", "anchor": "", "text": "What happened to the average cup movement?", "classification": "READ_DATA"}]
        findings = assess_prompts(prompts)
        self.assertFalse(any(f["code"] == "vague_referent" for f in findings))

    def test_what_happened_without_referent_is_vague(self):
        from chapter_qa.student_prompt import assess_prompts
        prompts = [{"artifact": "quiz", "anchor": "", "text": "What happened?", "classification": "READ_DATA"}]
        findings = assess_prompts(prompts)
        self.assertTrue(any(f["code"] == "vague_referent" for f in findings))


class LabStructureTests(unittest.TestCase):
    def test_actual_ramp_it_up_passes(self):
        from chapter_qa.file_producers import _lab_structure_findings
        findings, _obs = _lab_structure_findings(
            str(ROOT / "production" / "worksheets" / "03-ch3-ramp-it-up-student.docx"))
        self.assertEqual(findings, [])

    def test_missing_average_and_graph_fail(self):
        from docx import Document
        from chapter_qa.file_producers import _lab_structure_findings
        document = Document()
        document.add_paragraph("One ball. Same ramp. Same release. Same cup. Let go.")
        document.add_paragraph("Three trials at each height. Nine measured trials.")
        document.add_paragraph("CONNECT TO SPEED")
        document.add_paragraph("CONNECT TO ENERGY")
        table = document.add_table(rows=2, cols=5)
        for i, header in enumerate(("Condition", "Ramp height", "Trial 1", "Trial 2", "Trial 3")):
            table.rows[0].cells[i].text = header
        p = WORK / "mutated-lab.docx"
        p.parent.mkdir(parents=True, exist_ok=True)
        document.save(str(p))
        findings, _obs = _lab_structure_findings(str(p))
        codes = {f["code"] for f in findings}
        self.assertIn("missing_average", codes)
        self.assertIn("missing_graph", codes)


if __name__ == "__main__":
    unittest.main()
