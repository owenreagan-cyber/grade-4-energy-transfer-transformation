"""F-3 final closeout self-tests for the seven remaining producers.

Each producer must PASS a good fixture, FAIL a bad fixture, and be non-PASS on an
abort (missing/unreadable input). All through the normal file-observing entrypoint.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.file_producers import (  # noqa: E402
    emit_answer_leakage_from_files,
    emit_assessment_alignment_from_files,
    emit_curriculum_correctness_from_files,
    emit_fresh_export_from_files,
    emit_notes_slides_sync_from_files,
    emit_playbook_alignment_from_files,
    emit_source_authority_from_files,
)
from chapter_qa.identity import BuildIdentity  # noqa: E402

HASH = "a" * 64
WORK = ROOT / "qa" / "work" / "_f3final"


def identity():
    return BuildIdentity(
        buildId="f3final", candidatePath="c", candidateFreezeId="f", candidateHash=HASH,
        sourceFreezeId="s", sourceHash=HASH, inputHashes={"r": HASH},
    )


def _w(name: str, text: str) -> str:
    path = WORK / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path.relative_to(ROOT).as_posix()


def _e() -> str:
    p = WORK / "evidence.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("{}\n", encoding="utf-8")
    return p.relative_to(ROOT).as_posix()


SPEC = {
    "chapter": 3, "identityChapter": 3, "title": "Energy and Speed Are Related",
    "bigQuestion": "How are energy and speed related?", "sourceRanges": ["Reader pp. 13-16"],
    "concepts": ["same object"], "exclusions": ["kinetic"],
    "vocabulary": [{"term": "speed"}], "anchors": [],
}
READER = "How are energy and speed related? Speed is a measurement of the distance an object travels over an amount of time."
TG = "Teacher Guide Lesson 4. How are energy and speed related?"


class SourceAuthorityTests(unittest.TestCase):
    def _run(self, spec=SPEC, reader=READER, tg=TG):
        sp = _w("sp.json", json.dumps(spec))
        rp = _w("rd.md", reader)
        tp = _w("tg.md", tg)
        return emit_source_authority_from_files(sp, rp, tp, identity(), _e())[1].status

    def test_good(self):
        self.assertEqual(self._run(), "PASS")

    def test_wrong_reader(self):
        self.assertEqual(self._run(reader="unrelated text about frogs"), "FAIL")

    def test_abort_missing(self):
        st = emit_source_authority_from_files(None, None, None, identity(), _e())[1].status
        self.assertNotEqual(st, "PASS")


class CurriculumCorrectnessTests(unittest.TestCase):
    def test_good(self):
        f = _w("c-good.md", "Compare the same ball at two speeds.")
        self.assertEqual(emit_curriculum_correctness_from_files([f], identity(), _e())[1].status, "PASS")

    def test_ramp_is_speed(self):
        f = _w("c-bad.md", "Ramp height tells us the ball speed.")
        self.assertEqual(emit_curriculum_correctness_from_files([f], identity(), _e())[1].status, "FAIL")

    def test_kinetic(self):
        f = _w("c-kin.md", "students must know kinetic energy")
        self.assertEqual(emit_curriculum_correctness_from_files([f], identity(), _e())[1].status, "FAIL")

    def test_abort_missing(self):
        self.assertNotEqual(emit_curriculum_correctness_from_files([], identity(), _e())[1].status, "PASS")


class NotesSlidesSyncTests(unittest.TestCase):
    NOTES = "BQ How are energy and speed related?\nN1 Compare the same ____ ball.\nN2 We measure ramp ____ in centimeters. We do not measure a speed number.\n"
    SLIDES = "SLIDE 1\nBQ How are energy and speed related?\nSLIDE 2\nN1 Write both missing words.\nSLIDE 3\nN2 We do not measure a speed number.\nNOTES 1\n"
    ANCHORS = ["BQ", "N1", "N2"]

    def _run(self, notes=NOTES, slides=SLIDES):
        np = _w("n.md", notes)
        sp = _w("s.md", slides)
        return emit_notes_slides_sync_from_files(np, sp, self.ANCHORS, identity(), _e())[1].status

    def test_good(self):
        self.assertEqual(self._run(), "PASS")

    def test_remove_slides_support_line(self):
        slides = self.SLIDES.replace("We do not measure a speed number.", "")
        self.assertEqual(self._run(slides=slides), "FAIL")

    def test_remove_notes_anchor(self):
        notes = self.NOTES.replace("N1 Compare the same ____ ball.\n", "")
        self.assertEqual(self._run(notes=notes), "FAIL")

    def test_abort_missing(self):
        st = emit_notes_slides_sync_from_files(None, None, self.ANCHORS, identity(), _e())[1].status
        self.assertNotEqual(st, "PASS")


class AnswerLeakageTests(unittest.TestCase):
    NOTES = "BQ q\nN1 Compare the same ____ ball.\nN2 We measure ramp ____ in centimeters.\n"

    def test_good(self):
        np = _w("l-n.md", self.NOTES)
        sp = _w("l-s.md", "SLIDE 1\nBQ q\nSLIDE 2\nWRITE\nNOTES 1\n")
        kp = _w("l-k.md", "distance")
        self.assertEqual(emit_answer_leakage_from_files(np, sp, kp, identity(), _e())[1].status, "PASS")

    def test_early_reveal(self):
        np = _w("l-n2.md", self.NOTES)
        sp = _w("l-s2.md", "SLIDE 1\nREVEAL distance\nSLIDE 2\nWRITE\nNOTES 1\n")
        kp = _w("l-k2.md", "distance")
        self.assertEqual(emit_answer_leakage_from_files(np, sp, kp, identity(), _e())[1].status, "FAIL")

    def test_abort_missing(self):
        self.assertNotEqual(emit_answer_leakage_from_files(None, None, None, identity(), _e())[1].status, "PASS")


class AssessmentAlignmentTests(unittest.TestCase):
    QUIZ = "1. Speed is a measurement of the ____ an object travels over time.\n2. Which fits? A. one ball at two speeds B. a heavy and light ball\nScore: ____ / 12 = ____ %\n"
    QKEY = "1. distance\n2. A\n"

    def _run(self, quiz=QUIZ, qkey=QKEY):
        qp = _w("q.md", quiz)
        qkp = _w("qk.md", qkey)
        pp = _w("p.md", "1. The same ball rolls from a steeper ramp.\n")
        pkp = _w("pk.md", "1. a greater change\n")
        return emit_assessment_alignment_from_files(qp, qkp, pp, pkp, identity(), _e())[1].status

    def test_good(self):
        self.assertEqual(self._run(), "PASS")

    def test_key_changed(self):
        self.assertEqual(self._run(qkey="1. WRONG ANSWER\n2. B\n"), "FAIL")

    def test_abort_missing(self):
        self.assertNotEqual(emit_assessment_alignment_from_files(None, None, None, None, identity(), _e())[1].status, "PASS")


class PlaybookAlignmentTests(unittest.TestCase):
    PB = "Ramp It Up uses one ball. Ramp height in centimeters. We do not write a speed.\n"
    SPEC = "Ramp It Up uses one ball in centimeters."

    def _run(self, pb=PB, spec=SPEC):
        pp = _w("pb.md", pb)
        sp = _w("pbspec.md", spec)
        return emit_playbook_alignment_from_files(pp, sp, identity(), _e())[1].status

    def test_good(self):
        self.assertEqual(self._run(), "PASS")

    def test_missing_protocol(self):
        self.assertEqual(self._run(pb="We roll a marble."), "FAIL")

    def test_abort_missing(self):
        self.assertNotEqual(emit_playbook_alignment_from_files(None, None, identity(), _e())[1].status, "PASS")


class FreshExportTests(unittest.TestCase):
    def _docx(self, name, text):
        from docx import Document
        document = Document()
        document.add_paragraph(text)
        p = WORK / name
        p.parent.mkdir(parents=True, exist_ok=True)
        document.save(str(p))
        return p.relative_to(ROOT).as_posix()

    def _export(self, src_rel, out_name):
        import shutil
        import subprocess
        import tempfile
        src = ROOT / src_rel
        WORK.mkdir(parents=True, exist_ok=True)
        prof = tempfile.mkdtemp(prefix="lo_test_")
        try:
            subprocess.run(
                ["soffice", "--headless", "--norestore",
                 "-env:UserInstallation=file://" + prof,
                 "--convert-to", "pdf", "--outdir", str(WORK), str(src)],
                check=True, capture_output=True, text=True, timeout=300,
            )
        finally:
            shutil.rmtree(prof, ignore_errors=True)
        produced = WORK / (src.stem + ".pdf")
        target = WORK / out_name
        if produced.exists() and produced != target:
            shutil.move(str(produced), str(target))
        return target.relative_to(ROOT).as_posix()

    def test_good(self):
        src = self._docx("fe-good.docx", "source text for the export")
        prod = self._export(src, "fe-good-prod.pdf")
        st = emit_fresh_export_from_files(src, prod, "qa/work/_f3final/export", identity(), _e())[1].status
        self.assertEqual(st, "PASS")

    def test_stale(self):
        src = self._docx("fe-stale.docx", "first master text")
        prod = self._export(src, "fe-stale-prod.pdf")
        # Mutate the master; the tracked PDF is now stale and must FAIL.
        src2 = self._docx("fe-stale.docx", "changed master text")
        st = emit_fresh_export_from_files(src2, prod, "qa/work/_f3final/export", identity(), _e())[1].status
        self.assertEqual(st, "FAIL")

    def test_self_export(self):
        src = _w("fe-src2.txt", "identical")
        prod = _w("fe-prod2.pdf", "identical")
        self.assertEqual(emit_fresh_export_from_files(src, prod, "qa/work/_f3final/export", identity(), _e())[1].status, "FAIL")

    def test_abort_missing(self):
        self.assertNotEqual(emit_fresh_export_from_files(None, None, None, identity(), _e())[1].status, "PASS")


if __name__ == "__main__":
    unittest.main()
