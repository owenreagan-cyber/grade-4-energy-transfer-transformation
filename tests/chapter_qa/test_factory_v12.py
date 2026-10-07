"""Regression tests for render, visual, and PDF gate version 1.2."""

from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.adversary import make_identity  # noqa: E402
from chapter_qa.evidence import evaluate, evidence_from_dict  # noqa: E402
from chapter_qa.gates import gate_by_id, load_gates  # noqa: E402
from chapter_qa.pdf_fixture import write_pdf  # noqa: E402
from chapter_qa.render_completeness import assess_renders, emit_render_evidence  # noqa: E402
from chapter_qa.visual_qa import page_record  # noqa: E402
from qa_pdf_quality import assess_pdf  # noqa: E402


def _png(page, salt):
    relative = "qa/work/_v12/p%s-%s.png" % (page, salt[:6])
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    data = b"\x89PNG\r\n" + salt.encode()
    path.write_bytes(data)
    return {
        "artifactId": "notes",
        "artifactHash": "b" * 64,
        "pageOrSlide": page,
        "renderPath": relative,
        "renderHash": hashlib.sha256(data).hexdigest(),
        "navigation": False,
        "buildId": "chapter-build",
    }


class RenderIdentityTests(unittest.TestCase):
    def test_spec_hash_may_differ_from_render_hash(self):
        row = _png(1, "source-b")
        assessed = assess_renders([row], [row], candidate_hash="a" * 64, build_id="chapter-build")
        self.assertFalse(assessed["failsGate"])
        self.assertNotEqual(row["renderHash"], "a" * 64)
        self.assertNotEqual(row["artifactHash"], "a" * 64)

    def test_wrong_source_hash_fails(self):
        expected = _png(1, "source-b")
        observed = dict(expected, artifactHash="c" * 64)
        self.assertTrue(assess_renders([expected], [observed], build_id="chapter-build")["failsGate"])

    def test_wrong_build_fails(self):
        row = dict(_png(1, "build"), buildId="other-build")
        self.assertTrue(assess_renders([row], [row], build_id="chapter-build")["failsGate"])

    def test_missing_page_fails(self):
        rows = [_png(1, "one"), _png(2, "two")]
        self.assertTrue(assess_renders(rows, rows[:1])["failsGate"])

    def test_duplicate_index_fails(self):
        first = _png(1, "one")
        second = dict(_png(1, "other"), pageOrSlide=1)
        self.assertTrue(assess_renders([first], [first, second])["failsGate"])

    def test_foreign_artifact_fails(self):
        expected = _png(1, "ours")
        foreign = dict(expected, artifactId="other-chapter")
        self.assertTrue(assess_renders([expected], [foreign])["failsGate"])

    def test_tampered_render_hash_fails(self):
        row = _png(1, "clean")
        path = ROOT / row["renderPath"]
        path.write_bytes(path.read_bytes() + b"tamper")
        self.assertTrue(assess_renders([row], [row])["failsGate"])

    def test_old_gate_version_cannot_certify(self):
        gate = gate_by_id(load_gates(), "RENDER_COMPLETENESS")
        identity = make_identity()
        row = dict(_png(1, "version"), buildId=identity.buildId)
        stored, result = emit_render_evidence([row], [row], identity, row["renderPath"], auditor_role="VISUAL_QA_AUDITOR")
        self.assertEqual(result.status, "PASS")
        self.assertEqual(stored["gateVersion"], "1.2")
        stale = evidence_from_dict(dict(stored, gateVersion="1.1", status="PASS"))
        rejected = evaluate(stale, gate, identity)
        self.assertEqual(rejected.status, "FAIL")
        self.assertIn("GATE_VERSION_MISMATCH", rejected.codes)


class VisualRegionTests(unittest.TestCase):
    def test_edge_fringe_is_not_content(self):
        image = Image.new("RGB", (200, 200), "white")
        image.putpixel((199, 0), (249, 249, 249))
        page = page_record({
            "artifactId": "slide", "pageOrSlide": 1, "dpi": 72, "inspectionMethod": "rendered-page",
            "reviewerRole": "VISUAL_QA_AUDITOR", "renderPath": "qa/work/_v12/p1-source.png",
            "renderHash": "e" * 64,
        }, boxes=[{"kind": "text", "x": 0.8, "y": 0.8, "w": 1.2, "h": 0.4, "text": "speed", "fontPt": 18,
                   "pageWidthIn": 2.7, "pageHeightIn": 2.7}], image=image)
        self.assertFalse(any(item["code"] == "TEXT_OUTSIDE_SAFE_AREA" for item in page["findings"]))

    def test_full_bleed_background_is_allowed(self):
        image = Image.new("RGB", (200, 200), (27, 79, 194))
        page = page_record({
            "artifactId": "title", "pageOrSlide": 1, "dpi": 72, "inspectionMethod": "rendered-page",
            "reviewerRole": "VISUAL_QA_AUDITOR",
            "regions": [{"role": "BACKGROUND_BLEED", "x": 0, "y": 0, "w": 3, "h": 3}],
        }, boxes=[{"kind": "text", "x": 0.8, "y": 0.8, "w": 1.2, "h": 0.4, "text": "title", "fontPt": 18,
                   "pageWidthIn": 2.7, "pageHeightIn": 2.7}], image=image)
        self.assertFalse(any(item["code"] == "TEXT_OUTSIDE_SAFE_AREA" for item in page["findings"]))

    def test_content_in_the_margin_still_fails(self):
        image = Image.new("RGB", (200, 200), "white")
        image.putpixel((0, 0), (0, 0, 0))
        page = page_record({
            "artifactId": "slide", "pageOrSlide": 1, "dpi": 72, "inspectionMethod": "rendered-page",
            "reviewerRole": "VISUAL_QA_AUDITOR",
        }, boxes=[{"kind": "text", "x": 0.1, "y": 0.1, "w": 1.0, "h": 0.4, "text": "cut", "fontPt": 18,
                   "pageWidthIn": 2.7, "pageHeightIn": 2.7}], image=image)
        self.assertTrue(any(item["code"] == "TEXT_OUTSIDE_SAFE_AREA" for item in page["findings"]))

    def test_white_gap_is_not_a_visible_overlap(self):
        image = Image.new("RGB", (300, 300), "white")
        boxes = [
            {"kind": "text", "x": 0.6, "y": 0.6, "w": 1.0, "h": 0.5, "text": "one", "fontPt": 18, "pageWidthIn": 4, "pageHeightIn": 4},
            {"kind": "text", "x": 0.6, "y": 0.9, "w": 1.0, "h": 0.5, "text": "two", "fontPt": 18, "pageWidthIn": 4, "pageHeightIn": 4},
        ]
        page = page_record({
            "artifactId": "notes", "pageOrSlide": 1, "dpi": 72, "inspectionMethod": "rendered-page",
            "reviewerRole": "VISUAL_QA_AUDITOR",
        }, boxes=boxes, image=image)
        self.assertFalse(any(item["code"] == "TEXT_OVERLAP" for item in page["findings"]))


class PdfTextTests(unittest.TestCase):
    def test_compressed_text_is_present_without_literal_tj(self):
        path = ROOT / "qa/work/_v12/encoded.pdf"
        path.parent.mkdir(parents=True, exist_ok=True)
        write_pdf(path, [(612, 792, b"BT /F1 24 Tf 72 100 Td (Encoded) Tj ET")], compress=True)
        raw = path.read_bytes()
        self.assertNotIn(b"Encoded", raw)
        assessed = assess_pdf(str(path), {"pageCount": 1, "pageSizePts": (612, 792), "textRequired": True, "label": "encoded"})
        self.assertTrue(assessed["output"]["hasText"])
        self.assertGreater(assessed["output"]["textChars"], 0)
        self.assertFalse(any(item["code"] == "image_only_page" for item in assessed["findings"]))

    def test_image_only_page_has_no_text(self):
        path = ROOT / "qa/work/_v12/image-only.pdf"
        path.parent.mkdir(parents=True, exist_ok=True)
        write_pdf(path, [(612, 792, b"q Q")])
        assessed = assess_pdf(str(path), {"pageCount": 1, "textRequired": True, "label": "image"})
        self.assertFalse(assessed["output"]["hasText"])
        self.assertTrue(assessed["failsGate"])

    def test_malformed_pdf_fails(self):
        path = ROOT / "qa/work/_v12/bad.pdf"
        path.write_bytes(b"%PDF-1.4\nnot a pdf")
        assessed = assess_pdf(str(path), {"pageCount": 1, "textRequired": True, "label": "bad"})
        self.assertTrue(assessed["failsGate"])
        self.assertTrue(any(item["code"] == "corrupt_pdf" for item in assessed["findings"]))
