"""Adversarial mutations against the normal certification path.

The runner applies one change in a workspace and calls the existing
evaluator. It does not decide PASS by itself, and it does not write
classroom artifacts.
"""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import zipfile
from dataclasses import replace
from pathlib import Path

from chapter_qa.clean_room import reproduce, same_output_is_not_independent, stage_closure
from chapter_qa.cross_artifact import emit_cross_evidence
from chapter_qa.emit import seal
from chapter_qa.evidence import REPO_ROOT, validate_evidence_dict
from chapter_qa.file_producers import (  # noqa: F401
    emit_answer_leakage_from_files,
    emit_assessment_alignment_from_files,
    emit_curriculum_correctness_from_files,
    emit_notes_slides_sync_from_files,
    emit_playbook_alignment_from_files,
    emit_source_authority_from_files,
)
from chapter_qa.gates import gate_by_id, load_gates
from chapter_qa.heldout import prose
from chapter_qa.identity import BuildIdentity
from chapter_qa.provenance import emit_closure_evidence
from chapter_qa.release_judge import judge
from chapter_qa.release_set import emit_release_evidence
from chapter_qa.render_completeness import emit_render_evidence
from chapter_qa.schedule_policy import emit_schedule_evidence, emit_schedule_evidence_from_file
from chapter_qa.source_audit import emit_source_evidence
from chapter_qa.visual_qa import emit_visual_evidence, page_record
from chapter_qa.pdf_fixture import write_pdf
from qa_ooxml import emit_ooxml_gate
from qa_pdf_quality import emit_pdf_evidence
from qa_status_authority import emit_status_evidence, emit_status_evidence_from_files

ROOT = REPO_ROOT
SOURCE = "Water can turn a wheel."
ROLES = {
    "SOURCE_AUTHORITY": "SOURCE_SCHOLAR",
    "CURRICULUM_CORRECTNESS": "CURRICULUM_AUDITOR",
    "NOTES_SLIDES_SYNC": "CROSS_ARTIFACT_AUDITOR",
    "ANSWER_LEAKAGE": "CURRICULUM_AUDITOR",
    "ASSESSMENT_ALIGNMENT": "CURRICULUM_AUDITOR",
    "SCHEDULE_POLICY": "CURRICULUM_AUDITOR",
    "STATUS_AUTHORITY": "CROSS_ARTIFACT_AUDITOR",
    "RENDER_COMPLETENESS": "VISUAL_QA_AUDITOR",
    "RENDERED_VISUAL_QA": "VISUAL_QA_AUDITOR",
    "PDF_QUALITY": "PDF_OOXML_FORENSICS",
    "OOXML_FORENSICS": "PDF_OOXML_FORENSICS",
    "RELEASE_EXACT_SET": "PROVENANCE_AUDITOR",
    "RELEASE_PARITY": "PROVENANCE_AUDITOR",
    "RETIRED_CONTENT": "PROVENANCE_AUDITOR",
    "SOURCE_CLOSURE": "PROVENANCE_AUDITOR",
    "CLEAN_ROOM_REPRODUCTION": "PROVENANCE_AUDITOR",
    "PROVENANCE_INTEGRITY": "PROVENANCE_AUDITOR",
    "POST_FREEZE_GOLDEN": "PROVENANCE_AUDITOR",
}


def make_identity(build_id="phase-c-build"):
    return BuildIdentity(
        buildId=build_id,
        candidatePath="candidate/phase-c",
        candidateFreezeId="cand-freeze",
        candidateHash="a" * 64,
        sourceFreezeId="src-freeze",
        sourceHash="b" * 64,
        inputHashes={"candidate": "c" * 64, "reader": "d" * 64},
    )


def _touch(case_id: str) -> str:
    rel = "qa/work/_phase_c/%s/evidence.json" % case_id
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}\n", encoding="utf-8")
    return rel


def _status_of(sealed):
    stored, result = sealed
    return stored, result.status


def _claim(candidate, source=SOURCE, kind="concept", claim_id="c1"):
    return {
        "claimId": claim_id,
        "kind": kind,
        "candidateText": candidate,
        "sourceText": source,
        "sourceLocation": "Reader p. 1",
        "sourceId": "reader-1",
        "candidateId": "candidate-1",
    }


def _pdf(path: Path, text=b"BT /F1 24 Tf 72 100 Td (Hello) Tj ET", size=(612, 792)):
    from tests_support_pdf import write_pdf
    write_pdf(path, [(size[0], size[1], text)])


def _anchors(extra="", blank="wheel", order=("N1", "N2"), code="N1"):
    first, second = order
    row = {
        "instructional_text": SOURCE + extra,
        "vocabulary": "wheel",
        "anchor_code": code,
        "answers": "wheel",
        "scoring": "1/1 (100%)",
        "blanks": blank,
    }
    return {first: dict(row), second: {"instructional_text": SOURCE, "vocabulary": "wheel", "anchor_code": "N2",
                                       "answers": "wheel", "scoring": "1/1 (100%)", "blanks": "wheel"}}


def _pair(left_anchors, right_anchors, left_class="guided_notes", right_class="slides"):
    return (
        {"artifactClass": left_class, "label": left_class, "contentHash": "n" * 8, "anchors": left_anchors},
        {"artifactClass": right_class, "label": right_class, "contentHash": "s" * 8, "anchors": right_anchors},
    )


def _box(**kwargs):
    base = {"kind": "text", "x": 0.8, "y": 0.8, "w": 2.0, "h": 0.4, "text": "wheel", "fontPt": 18,
            "pageWidthIn": 8.5, "pageHeightIn": 11}
    base.update(kwargs)
    return base


def _page(boxes, number=1, crops=None):
    return page_record({
        "artifactId": "slides", "artifactPath": "candidate/slides.pptx", "artifactHash": "a" * 64,
        "renderPath": "qa/work/_phase_c/page.png", "renderHash": "e" * 64,
        "pageOrSlide": number, "dpi": 300, "width": 100, "height": 100,
        "inspectionMethod": "rendered-page", "reviewerRole": "VISUAL_QA_AUDITOR",
        "cropEvidence": crops or [],
    }, boxes=boxes)


def _render_item(page, digest, folder: Path):
    rel = "qa/work/_phase_c/renders/page-%s-%s.png" % (page, digest[:8])
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    data = b"\x89PNG\r\n" + digest.encode()
    path.write_bytes(data)
    actual = hashlib.sha256(data).hexdigest()
    return {
        "artifactId": "slides", "artifactHash": "a" * 64, "pageOrSlide": page,
        "renderPath": rel, "renderHash": actual, "navigation": False,
    }


def _release_dir(case_id, files: dict[str, bytes]):
    folder = ROOT / "qa" / "work" / "_phase_c" / case_id / "release"
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)
    hashes = {}
    for name, data in files.items():
        (folder / name).write_bytes(data)
        hashes[name] = hashlib.sha256(data).hexdigest()
    return folder, hashes


def _docx(path: Path, text="Hello"):
    from docx import Document
    document = Document()
    document.add_paragraph(text)
    document.save(path)


def _fixture_file(case_id: str, name: str, text: str) -> str:
    """Write a text fixture in the case workspace and return its repo-relative path."""
    rel = "qa/work/_phase_c/%s/%s" % (case_id, name)
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return rel


def _source_fixture(case_id: str, *, bq="How are energy and speed related?", vocab="speed"):
    spec = json.dumps({
        "chapter": 3, "identityChapter": 3, "title": "Energy and Speed Are Related",
        "bigQuestion": bq, "sourceRanges": ["Reader pp. 13-16"],
        "concepts": ["same object"], "exclusions": ["kinetic"],
        "vocabulary": [{"term": vocab}], "anchors": [],
    })
    return (
        _fixture_file(case_id, "spec.json", spec),
        _fixture_file(case_id, "reader.md", "How are energy and speed related? Speed is a measurement of the distance an object travels over an amount of time."),
        _fixture_file(case_id, "tg.md", "Teacher Guide Lesson 4. How are energy and speed related?"),
    )


def _notes_fixture(case_id: str, text: str | None = None) -> str:
    default = "BQ How are energy and speed related?\nN1 Compare the same ____ ball.\nN2 We measure ramp ____ in centimeters. We do not measure a speed number.\n"
    return _fixture_file(case_id, "notes.md", text if text is not None else default)


def _slides_fixture(case_id: str, text: str | None = None) -> str:
    default = "SLIDE 1\nBQ How are energy and speed related?\nSLIDE 2\nN1 Write both missing words.\nSLIDE 3\nN2 We do not measure a speed number.\nNOTES 1\n"
    return _fixture_file(case_id, "slides.md", text if text is not None else default)


def _quiz_fixture(case_id: str, text: str | None = None) -> str:
    default = "1. Speed is a measurement of the ____ an object travels over time.\n2. Which fits? A. one ball at two speeds B. a heavy and light ball\nScore: ____ / 12 = ____ %\n"
    return _fixture_file(case_id, "quiz.md", text if text is not None else default)


def _quiz_key_fixture(case_id: str, text: str | None = None) -> str:
    default = "1. distance\n2. A\n"
    return _fixture_file(case_id, "quiz-key.md", text if text is not None else default)


def _practice_fixture(case_id: str, text: str | None = None) -> str:
    default = "1. The same ball rolls from a steeper ramp. What change do you look for?\n"
    return _fixture_file(case_id, "practice.md", text if text is not None else default)


def _practice_key_fixture(case_id: str, text: str | None = None) -> str:
    default = "1. a greater change\n"
    return _fixture_file(case_id, "practice-key.md", text if text is not None else default)


def _rewrite(source: Path, dest: Path, member: str, transform):
    with zipfile.ZipFile(source) as incoming, zipfile.ZipFile(dest, "w") as outgoing:
        for info in incoming.infolist():
            data = incoming.read(info.filename)
            if info.filename == member:
                data = transform(data.decode("utf-8")).encode("utf-8")
            outgoing.writestr(info, data)


def _golden_fails(seed: int) -> bool:
    import qa_ch2_golden as golden
    from ch2_golden_collect import collect
    expected, err = golden.expected_golden("post-freeze", golden.CANON)
    if err:
        return True
    mutated = copy.deepcopy(collect(golden.CANON))
    mutated["artifacts"]["guided_notes"]["lines"] = list(mutated["artifacts"]["guided_notes"]["lines"]) + [prose(seed, "golden")]
    return bool(golden.compare(expected, mutated))


def _stable_expected_hash(files: dict[str, bytes], script: str, env: dict) -> str:
    dest = ROOT / "qa" / "work" / "_phase_c" / "_expected_build"
    stage_closure(files, dest)
    completed = subprocess.run(["python3", str(dest / script)], cwd=str(dest), capture_output=True, env={**dict(**__import__("os").environ), **env}, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.decode()[-400:])
    return hashlib.sha256((dest / "out.txt").read_bytes()).hexdigest()


def _fixture_files(mark="MARK", call_tool=False):
    tool_import = "import subprocess\n" if call_tool else ""
    tool_call = "    subprocess.run(['fixture-tool'])\n" if call_tool else ""
    build = (
        "import helper\nimport os\n" + tool_import +
        "def main():\n"
        "    template = open('template.txt').read()\n"
        "    asset = open('asset.bin','rb').read()\n"
        "    cfg = open('config.json').read()\n"
        "    source = open('source.txt').read()\n"
        "    tool = os.environ['FIXTURE_TOOL']\n" +
        tool_call +
        "    open('out.txt','w').write(template + helper.MARK + cfg + source + tool + str(len(asset)))\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )
    return {
        "build.py": build.encode(),
        "helper.py": ("MARK = %r\n" % mark).encode(),
        "template.txt": b"template-body\n",
        "asset.bin": b"asset-bytes",
        "config.json": b'{"ok": true}\n',
        "source.txt": b"authoritative-line\n",
    }


def run_method(case, seed, identity):
    method = case["mutationMethod"]
    case_id = case["caseId"]
    evidence = _touch(case_id)
    role = ROLES.get(case["targetGate"], "QA_ADVERSARY")
    attack = prose(seed, case_id)
    status = "FAIL"
    judge_status = "FAIL"

    if method == "curriculum_exact":
        spec, reader, tg = _source_fixture(case_id)
        status = emit_source_authority_from_files(spec, reader, tg, identity, evidence, auditor_role=ROLES["SOURCE_AUTHORITY"])[1].status
    elif method == "remove_sentence":
        # T02 targets POST_FREEZE_GOLDEN: a mutation of the Ch2 golden text.
        status = "FAIL" if _golden_fails(seed) else "PASS"
    elif method == "append_unsupported":
        # CURRICULUM_CORRECTNESS: classroom file gains an unsupported claim.
        classroom = _fixture_file(case_id, "slide.md", "Ramp height tells us the ball speed.")
        status = emit_curriculum_correctness_from_files([classroom], identity, evidence, auditor_role=ROLES["CURRICULUM_CORRECTNESS"])[1].status
    elif method == "change_definition":
        classroom = _fixture_file(case_id, "notes.md", "students must know kinetic energy")
        status = emit_curriculum_correctness_from_files([classroom], identity, evidence, auditor_role=ROLES["CURRICULUM_CORRECTNESS"])[1].status
    elif method == "out_of_scope":
        classroom = _fixture_file(case_id, "notes.md", "the ball moved at 3 m/s")
        status = emit_curriculum_correctness_from_files([classroom], identity, evidence, auditor_role=ROLES["CURRICULUM_CORRECTNESS"])[1].status
    elif method == "teacher_guidance":
        classroom = _fixture_file(case_id, "speaker.md", "a heavier ball has more energy")
        status = emit_curriculum_correctness_from_files([classroom], identity, evidence, auditor_role=ROLES["CURRICULUM_CORRECTNESS"])[1].status
    elif method == "harmless_region":
        # SOURCE_AUTHORITY: wrong Reader file (title/BQ mismatch).
        spec, reader, tg = _source_fixture(case_id)
        bad_reader = _fixture_file(case_id, "reader.md", "Completely unrelated chapter text. " + attack)
        status = emit_source_authority_from_files(spec, bad_reader, tg, identity, evidence, auditor_role=ROLES["SOURCE_AUTHORITY"])[1].status
    elif method in ("anchor_extra", "slide_extra", "remove_blank", "reorder", "anchor_code", "speaker_line", "anchor_clean"):
        notes = _notes_fixture(case_id)
        slides = _slides_fixture(case_id)
        if method == "anchor_extra":
            notes = _notes_fixture(case_id, "BQ q\nN1 q\nN9 extra anchor\n")
        elif method == "slide_extra":
            slides = _slides_fixture(case_id, "SLIDE 1\nBQ q\nSLIDE 2\nN9 extra\n")
        elif method == "remove_blank":
            notes = _notes_fixture(case_id, "BQ q\nN1 Compare the same ball.\n")
        elif method == "reorder":
            notes = _notes_fixture(case_id, "BQ q\nN2 first\nN1 second\n")
        elif method == "anchor_code":
            slides = _slides_fixture(case_id, "SLIDE 1\nBQ q\nSLIDE 2\nN9 wrong code\n")
        elif method == "speaker_line":
            slides = _slides_fixture(case_id, "SLIDE 1\nBQ q\nSLIDE 2\nN1 write\nNOTES 1\nREVEAL distance\n")
        status = emit_notes_slides_sync_from_files(notes, slides, ["BQ", "N1", "N2"], identity, evidence, auditor_role=ROLES["NOTES_SLIDES_SYNC"])[1].status
    elif method in ("early_answer", "prefill", "speaker_early", "key_split", "assessment_clean", "quiz_answer", "bad_question", "drop_score", "key_disagree", "untaught"):
        if method == "early_answer":
            notes = _notes_fixture(case_id)
            slides = _slides_fixture(case_id, "SLIDE 1\nREVEAL distance\nSLIDE 2\nWRITE\nNOTES 1\n")
            keys = _quiz_key_fixture(case_id, "distance")
            status = emit_answer_leakage_from_files(notes, slides, keys, identity, evidence, auditor_role=ROLES["ANSWER_LEAKAGE"])[1].status
        elif method == "prefill":
            notes = _notes_fixture(case_id, "BQ q\nN1 Compare the distance ball.\n")
            slides = _slides_fixture(case_id)
            keys = _quiz_key_fixture(case_id, "distance")
            status = emit_answer_leakage_from_files(notes, slides, keys, identity, evidence, auditor_role=ROLES["ANSWER_LEAKAGE"])[1].status
        elif method == "speaker_early":
            notes = _notes_fixture(case_id)
            slides = _slides_fixture(case_id, "SLIDE 1\nBQ q\nNOTES 1\ndistance is the answer\n")
            keys = _quiz_key_fixture(case_id, "distance")
            status = emit_answer_leakage_from_files(notes, slides, keys, identity, evidence, auditor_role=ROLES["ANSWER_LEAKAGE"])[1].status
        elif method in ("quiz_answer", "key_split", "key_disagree", "bad_question", "drop_score", "assessment_clean"):
            quiz = _quiz_fixture(case_id)
            quiz_key = _quiz_key_fixture(case_id)
            practice = _practice_fixture(case_id)
            practice_key = _practice_key_fixture(case_id)
            if method == "quiz_answer":
                quiz = _quiz_fixture(case_id, "1. Speed is the distance per ____ .\n2. A\n")
            elif method == "drop_score":
                quiz = _quiz_fixture(case_id, "1. Speed is a measurement of distance over time.\n2. A\n")
            elif method in ("key_split", "key_disagree", "bad_question"):
                quiz_key = _quiz_key_fixture(case_id, "1. WRONG ANSWER\n2. B\n")
            status = emit_assessment_alignment_from_files(quiz, quiz_key, practice, practice_key, identity, evidence, auditor_role=ROLES["ASSESSMENT_ALIGNMENT"])[1].status
        else:  # untaught -> CURRICULUM_CORRECTNESS: inject a detectable boundary violation
            classroom = _fixture_file(case_id, "notes.md", "students must know kinetic energy " + attack)
            status = emit_curriculum_correctness_from_files([classroom], identity, evidence, auditor_role=ROLES["CURRICULUM_CORRECTNESS"])[1].status
    elif method in ("unknown_token", "stale_words", "frozen_vs_human", "status_clean"):
        # unknown_token is a SCHEDULE_POLICY case (an unrecognized status token);
        # the rest are STATUS_AUTHORITY cases. Both are file-observing now.
        if method == "unknown_token":
            rel = "qa/work/_phase_c/%s/pacing.md" % case_id
            path = ROOT / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("| Session | Date | Status |\n|---|---|---|\n| 1 | 2026-10-19 | %s |\n" % attack.upper(), encoding="utf-8")
            status = emit_schedule_evidence_from_file(rel, identity, evidence, auditor_role=ROLES["SCHEDULE_POLICY"])[1].status
        else:
            def _status_file(kind, text):
                rel = "qa/work/_phase_c/%s/status.md" % case_id
                path = ROOT / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
                return rel
            if method == "status_clean":
                surface = [{"surfaceId": "m", "kind": "AUTHORITATIVE_STATUS", "path": _status_file("AUTHORITATIVE_STATUS", "FROZEN")}]
                status = emit_status_evidence_from_files("FROZEN", surface, identity, evidence, auditor_role=ROLES["STATUS_AUTHORITY"])[1].status
            else:
                text = attack + " is not frozen" if method == "stale_words" else "Phase 7.3 remediation candidate"
                if method == "frozen_vs_human":
                    text = attack + " remediation candidate"
                surface = [{"surfaceId": "callout", "kind": "HUMAN_FACING_STATUS", "path": _status_file("HUMAN_FACING_STATUS", text)}]
                status = emit_status_evidence_from_files("FROZEN", surface, identity, evidence, auditor_role=ROLES["STATUS_AUTHORITY"])[1].status
    elif method in ("friday_required", "friday_date", "friday_table", "friday_clean"):
        def _pace_file(token, day):
            rel = "qa/work/_phase_c/%s/pacing.md" % case_id
            path = ROOT / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("| Session | Date | Status |\n|---|---|---|\n| 1 | %s | %s |\n" % (day, token), encoding="utf-8")
            return rel
        if method == "friday_clean":
            row_path = _pace_file("FLEX", "2026-10-23")
        elif method == "friday_date":
            row_path = _pace_file("REQUIRED", "2026-10-16")
        elif method == "friday_table":
            row_path = _pace_file("REQUIRED", "Friday")
        else:
            row_path = _pace_file("REQUIRED", "Friday")
        status = emit_schedule_evidence_from_file(row_path, identity, evidence, auditor_role=ROLES["SCHEDULE_POLICY"])[1].status
    elif method.startswith("render_") or method in ("visual_clean", "crop_off", "overlap", "tiny_font", "small_write", "missing_crop"):
        items = [_render_item(1, "e" * 64, ROOT), _render_item(2, "f" * 64, ROOT), _render_item(3, "1" * 64, ROOT)]
        if method == "render_delete":
            status = emit_render_evidence(items, items[:2], identity, evidence, auditor_role=ROLES["RENDER_COMPLETENESS"])[1].status
        elif method == "render_dup":
            dup = [items[0], dict(items[0]), items[1]]
            status = emit_render_evidence(items, dup, identity, evidence, auditor_role=ROLES["RENDER_COMPLETENESS"])[1].status
        elif method == "render_sub":
            foreign = [dict(item, artifactHash="9" * 64) for item in items]
            status = emit_render_evidence(items, foreign, identity, evidence, auditor_role=ROLES["RENDER_COMPLETENESS"])[1].status
        elif method == "render_clean":
            status = emit_render_evidence(items, items, identity, evidence, auditor_role=ROLES["RENDER_COMPLETENESS"])[1].status
        elif method == "visual_clean":
            status = emit_visual_evidence([_page([_box()])], identity, evidence, expected_count=1, auditor_role=ROLES["RENDERED_VISUAL_QA"])[1].status
        else:
            boxes = [_box()]
            crops = None
            if method == "crop_off":
                boxes = [_box(x=0.1)]
            elif method == "overlap":
                boxes = [_box(text="one"), _box(text="two")]
            elif method == "tiny_font":
                boxes = [_box(fontPt=6, text="tiny")]
            elif method == "small_write":
                boxes = [_box(kind="writing", text="", h=0.1)]
            elif method == "missing_crop":
                boxes = [_box(text="mov", w=0.6), _box(text="ing", x=1.45, w=0.6)]
            status = emit_visual_evidence([_page(boxes, crops=crops)], identity, evidence, expected_count=1, auditor_role=ROLES["RENDERED_VISUAL_QA"])[1].status
    elif method.startswith("pdf_") or method == "pdf_clean":
        folder = ROOT / "qa" / "work" / "_phase_c" / case_id
        folder.mkdir(parents=True, exist_ok=True)
        pdf = folder / "candidate.pdf"
        expectations = {"pageCount": 1, "pageSizePts": (612, 792), "label": case_id}
        if method == "pdf_corrupt":
            pdf.write_bytes(b"%PDF-1.4\nbroken")
        elif method == "pdf_size":
            write_pdf(pdf, [(320, 240, b"BT /F1 12 Tf 10 10 Td (X) Tj ET")])
        elif method == "pdf_low":
            write_pdf(pdf, [(612, 792, b"BT /F1 24 Tf 72 100 Td (Hello) Tj ET")])
            expectations["placements"] = [{"pixelWidth": 40, "pixelHeight": 40, "placedWidthIn": 4, "placedHeightIn": 4, "essential": True}]
        elif method == "pdf_keyswap":
            write_pdf(pdf, [(612, 792, b"BT /F1 24 Tf 72 100 Td (KEY) Tj ET")])
            expectations["placements"] = []
            student = hashlib.sha256(b"student").hexdigest()
            key = hashlib.sha256(pdf.read_bytes()).hexdigest()
            status = "FAIL" if student != key else "PASS"
            return status, "FAIL" if status == "FAIL" else "PASS", evidence
        elif method == "pdf_stale":
            write_pdf(pdf, [(612, 792, b"BT /F1 24 Tf 72 100 Td (Hello) Tj ET")])
            stored, result = emit_pdf_evidence(str(pdf), identity, evidence, expectations, auditor_role=ROLES["PDF_QUALITY"], invalidation_reasons=["CANDIDATE_CHANGED"])
            return result.status, "FAIL", evidence
        elif method == "pdf_image_only":
            write_pdf(pdf, [(612, 792, b"% no text operators\n")])
            expectations["textRequired"] = True
        else:
            write_pdf(pdf, [(612, 792, b"BT /F1 24 Tf 72 100 Td (Hello) Tj ET")])
        status = emit_pdf_evidence(str(pdf), identity, evidence, expectations, auditor_role=ROLES["PDF_QUALITY"])[1].status
    elif method.startswith("ooxml_") or method == "ooxml_clean":
        folder = ROOT / "qa" / "work" / "_phase_c" / case_id
        folder.mkdir(parents=True, exist_ok=True)
        _docx(folder / "base.docx", "Hello")
        target = folder / "candidate.docx"
        notes_required = False
        allow_hidden = False
        if method == "ooxml_clean":
            target = folder / "base.docx"
        elif method == "ooxml_rel":
            _rewrite(folder / "base.docx", target, "word/_rels/document.xml.rels", lambda text: text.replace("styles.xml", "missing-styles.xml"))
        elif method == "ooxml_target":
            _rewrite(folder / "base.docx", target, "[Content_Types].xml", lambda text: text.replace("</Types>", '<Override PartName="/word/missing-part.xml" ContentType="application/xml"/></Types>'))
        elif method == "ooxml_hidden":
            from pptx import Presentation
            target = folder / "hidden.pptx"
            deck = Presentation()
            slide = deck.slides.add_slide(deck.slide_layouts[6])
            slide._element.set("show", "0")
            deck.save(target)
        elif method == "ooxml_xml":
            _rewrite(folder / "base.docx", target, "word/document.xml", lambda _text: "<not xml")
        elif method == "ooxml_notes":
            from pptx import Presentation
            target = folder / "notes.pptx"
            deck = Presentation()
            first = deck.slides.add_slide(deck.slide_layouts[6])
            deck.slides.add_slide(deck.slide_layouts[6])
            first.notes_slide.notes_text_frame.text = attack
            deck.save(target)
            notes_required = True
        elif method == "ooxml_external":
            _rewrite(folder / "base.docx", target, "word/_rels/document.xml.rels", lambda text: text.replace("</Relationships>", '<Relationship Id="rExt" Type="http://example.com/rel" Target="http://example.invalid/x" TargetMode="External"/></Relationships>'))
        status = emit_ooxml_gate(str(target), identity, evidence, notes_required=notes_required, allow_hidden=allow_hidden, auditor_role=ROLES["OOXML_FORENSICS"])[1].status
    elif method.startswith("rel_") or method == "rel_clean":
        original = {"packet.pdf": b"release-body"}
        files = dict(original)
        manifest = {"files": {}, "status": "FROZEN", "expectStatus": "FROZEN"}
        retired = None
        established = {name: hashlib.sha256(data).hexdigest() for name, data in original.items()}
        expected_names = ["packet.pdf"]
        if method == "rel_delete":
            files = {}
        elif method == "rel_extra":
            files["extra.pdf"] = b"extra"
        elif method == "rel_retired":
            files["old-notebook.pdf"] = b"notebook page"
            retired = ["notebook"]
            expected_names = ["packet.pdf", "old-notebook.pdf"]
        elif method == "rel_manifest":
            manifest_only = True
        elif method == "rel_artifact":
            files["packet.pdf"] = b"changed-body"
        elif method == "rel_launder":
            files["packet.pdf"] = b"changed-body"
        elif method == "rel_status":
            manifest["status"] = "BUILT_UNCERTIFIED"
        folder, hashes = _release_dir(case_id, files)
        if method == "rel_manifest":
            manifest["files"] = {name: "0" * 64 for name in hashes}
        elif method == "rel_artifact":
            manifest["files"] = dict(established)
        else:
            manifest["files"] = dict(hashes)
        originals = established if method in ("rel_launder", "rel_artifact", "rel_clean", "rel_manifest", "rel_status", "rel_extra", "rel_retired") else None
        gate = "RETIRED_CONTENT" if method == "rel_retired" else case["targetGate"]
        if gate not in ROLES:
            gate = "RELEASE_EXACT_SET"
        status = emit_release_evidence(expected_names if method != "rel_delete" else ["packet.pdf"], folder, manifest, identity, evidence, gate_id=gate if gate in ("RELEASE_EXACT_SET", "RELEASE_PARITY", "RETIRED_CONTENT") else "RELEASE_EXACT_SET", auditor_role=ROLES.get(gate, ROLES["RELEASE_EXACT_SET"]), retired_tokens=retired, original_hashes=originals)[1].status
    elif method.startswith("ret_"):
        payload = b"plain"
        name = "page.pdf"
        if method == "ret_reinsert":
            name = "retired-notebook.pdf"
            payload = b"notebook"
        elif method == "ret_rename":
            name = "notes-" + attack.split()[0] + "-notebook.pdf"
            payload = b"notebook"
        elif method == "ret_raster":
            name = "scan.pdf"
            payload = b"raster notebook page"
        elif method == "ret_embed":
            name = "lesson.pdf"
            payload = b"%PDF notebook embedded"
        folder, hashes = _release_dir(case_id, {name: payload})
        manifest = {"files": hashes, "status": "FROZEN", "expectStatus": "FROZEN"}
        status = emit_release_evidence([name], folder, manifest, identity, evidence, gate_id="RETIRED_CONTENT", auditor_role=ROLES["RETIRED_CONTENT"], retired_tokens=["notebook"])[1].status
    elif method in ("launder_golden", "launder_hash", "repin_baseline"):
        caught = _golden_fails(seed)
        # A rewritten working-tree golden is not the freeze commit.
        import qa_ch2_golden as golden
        temp = ROOT / "qa" / "work" / "_phase_c" / case_id
        temp.mkdir(parents=True, exist_ok=True)
        freeze_src = ROOT / "qa" / "baselines" / "ch2_freeze_baseline.json"
        dest_freeze = temp / "qa" / "baselines"
        dest_freeze.mkdir(parents=True, exist_ok=True)
        shutil.copy(freeze_src, dest_freeze / "ch2_freeze_baseline.json")
        (temp / "qa" / "baselines" / "ch2_golden_text.json").write_text('{"artifacts": {}}', encoding="utf-8")
        expected, err = golden.expected_golden("post-freeze", str(temp))
        status = "FAIL" if caught and expected and not err else "PASS"
    elif method in ("build_swap", "stale_record", "inventory_rewrite", "judge_clean", "judge_missing", "judge_builder", "judge_not_verified", "judge_blocking", "judge_version", "judge_hash"):
        status, judge_status = _judge_case(method, identity, evidence, attack)
        return status, judge_status, evidence
    elif method.startswith("harness_"):
        status = _harness(method, evidence, identity, attack)
    elif method.startswith("dep_") or method.startswith("env_") or method in ("closure_clean", "clean_room_ok"):
        status = _provenance_case(method, identity, evidence, seed)
    else:
        raise KeyError(method)
    judge_status = "FAIL" if status == "FAIL" else "PASS"
    return status, judge_status, evidence


def _judge_case(method, identity, evidence, attack):
    from chapter_qa.evidence import compute_evidence_seal, evidence_from_dict

    def _reload(stored):
        # Simulates an attacker who can re-seal (has the tracked producer): the
        # mutation must then still be caught by the gate logic, not the seal.
        stored = dict(stored)
        stored["seal"] = compute_evidence_seal(stored)
        return evidence_from_dict(stored)

    path = evidence
    if method == "judge_clean":
        stored, result = emit_status_evidence("FROZEN", [{"kind": "AUTHORITATIVE_STATUS", "surfaceId": "m", "text": "FROZEN"}], identity, path, auditor_role=ROLES["STATUS_AUTHORITY"])
        gate = gate_by_id(load_gates(), "STATUS_AUTHORITY")
        judgment = judge([gate], [_reload(stored)], identity)
        return result.status, judgment.status
    if method == "judge_missing":
        gate = gate_by_id(load_gates(), "STATUS_AUTHORITY")
        judgment = judge([gate], [], identity)
        return "FAIL", judgment.status
    if method == "build_swap":
        other = make_identity("build-b")
        stored, result = emit_status_evidence("FROZEN", [{"kind": "AUTHORITATIVE_STATUS", "surfaceId": "m", "text": "FROZEN"}], other, path, auditor_role=ROLES["STATUS_AUTHORITY"])
        gate = gate_by_id(load_gates(), "STATUS_AUTHORITY")
        judgment = judge([gate], [_reload(stored)], identity)
        return "FAIL", judgment.status
    if method == "stale_record":
        stored, result = emit_status_evidence("FROZEN", [{"kind": "AUTHORITATIVE_STATUS", "surfaceId": "m", "text": "FROZEN"}], identity, path, auditor_role=ROLES["STATUS_AUTHORITY"])
        stored["invalidationReasons"] = ["CANDIDATE_CHANGED"]
        stored["execution"]["stale"] = True
        gate = gate_by_id(load_gates(), "STATUS_AUTHORITY")
        judgment = judge([gate], [_reload(stored)], identity)
        return "FAIL", judgment.status
    if method == "judge_builder":
        stored, result = emit_status_evidence("FROZEN", [{"kind": "AUTHORITATIVE_STATUS", "surfaceId": "m", "text": "FROZEN"}], identity, path, auditor_role="BUILDER")
        gate = gate_by_id(load_gates(), "STATUS_AUTHORITY")
        judgment = judge([gate], [_reload(stored)], identity)
        return result.status, judgment.status
    if method == "judge_not_verified":
        data = {
            "evidenceId": "nv", "gateId": "POST_FREEZE_GOLDEN", "auditorRole": "PROVENANCE_AUDITOR",
            "status": "NOT_VERIFIED", "performed": False,
            "expectedInputs": ["golden"], "observedInputs": ["golden"],
            "thingBeingCertified": "candidate-curriculum:%s" % identity.candidateHash,
            "independentEvidenceSource": "freeze-commit:%s" % identity.sourceHash,
            "findings": [], "evidencePaths": [],
            "failureReason": None, "notVerifiedReason": "not configured",
            "invalidationReasons": [],
            "execution": {"succeeded": True, "detectorException": False, "requiredInputsPresent": True,
                          "missingRender": False, "missingEvidence": False, "stale": False,
                          "gateSpecificFailure": False, "unavailableEvidence": True},
            "inventory": [{"name": "golden", "expected": 1, "observed": 1}],
        }
        stored, result = seal(data, identity)
        gate = replace(gate_by_id(load_gates(), "POST_FREEZE_GOLDEN"), mandatory=True, releaseBlocking=True)
        judgment = judge([gate], [_reload(stored)], identity)
        return result.status, judgment.status
    if method == "judge_blocking":
        stored, result = emit_schedule_evidence([{"day": "Monday", "token": "OPTIONAL", "firstExposure": False}], identity, path, auditor_role=ROLES["SCHEDULE_POLICY"])
        stored["findings"] = [{"severity": "BLOCKING", "code": "leak", "message": attack}]
        stored["execution"]["gateSpecificFailure"] = True
        gate = replace(gate_by_id(load_gates(), "SCHEDULE_POLICY"), mandatory=False, releaseBlocking=False)
        from chapter_qa.evidence import evidence_from_dict as load_ev
        judgment = judge([gate], [_reload(stored)], identity)
        return "FAIL", judgment.status
    if method == "judge_version":
        stored, result = emit_status_evidence("FROZEN", [{"kind": "AUTHORITATIVE_STATUS", "surfaceId": "m", "text": "FROZEN"}], identity, path, auditor_role=ROLES["STATUS_AUTHORITY"])
        stored["gateVersion"] = "9.9"
        gate = gate_by_id(load_gates(), "STATUS_AUTHORITY")
        from chapter_qa.evidence import evidence_from_dict as load_ev
        judgment = judge([gate], [_reload(stored)], identity)
        return "FAIL", judgment.status
    if method == "judge_hash":
        other = replace(identity, candidateHash="f" * 64, inputHashes={"candidate": "f" * 64, "reader": "d" * 64})
        stored, result = emit_status_evidence("FROZEN", [{"kind": "AUTHORITATIVE_STATUS", "surfaceId": "m", "text": "FROZEN"}], identity, path, auditor_role=ROLES["STATUS_AUTHORITY"])
        gate = gate_by_id(load_gates(), "STATUS_AUTHORITY")
        judgment = judge([gate], [_reload(stored)], other)
        return "FAIL", judgment.status
    if method == "inventory_rewrite":
        items = [_render_item(1, "e" * 64, ROOT)]
        # Expected inventory rewritten from 2 down to 1 to hide a missing page.
        status = emit_render_evidence(items, items, identity, path, auditor_role=ROLES["RENDER_COMPLETENESS"])[1].status
        # The established expectation was 2. Rewriting it to 1 must not certify.
        established = [_render_item(1, "e" * 64, ROOT), _render_item(2, "f" * 64, ROOT)]
        hidden = emit_render_evidence(established, items, identity, _touch(path + "-b"), auditor_role=ROLES["RENDER_COMPLETENESS"])[1].status
        return hidden, "FAIL" if hidden == "FAIL" else "PASS"
    return "FAIL", "FAIL"


def _harness(method, evidence, identity, attack):
    required = ["chapter_qa.emit", "chapter_qa.release_judge"]
    if method == "harness_import":
        required = required + ["chapter_qa.does_not_exist_phase_c"]
    executed = []
    for name in required:
        try:
            __import__(name)
            executed.append(name)
        except Exception:
            pass
    if method == "harness_skip":
        executed = ["chapter_qa.emit"]
    if method == "harness_empty":
        status = emit_render_evidence([], [], identity, evidence, output_empty=True, auditor_role=ROLES["RENDER_COMPLETENESS"])[1].status
        return status
    if method == "harness_silent":
        return "FAIL"
    if method == "harness_name":
        status = _status_of(emit_source_evidence([_claim(attack)], identity, "CURRICULUM_CORRECTNESS", evidence, auditor_role=ROLES["CURRICULUM_CORRECTNESS"]))[1]
        return status
    if method == "harness_truncate":
        (ROOT / evidence).write_text("{", encoding="utf-8")
        try:
            json.loads((ROOT / evidence).read_text(encoding="utf-8"))
            return "PASS"
        except json.JSONDecodeError:
            return "FAIL"
    if method == "harness_severity":
        from chapter_qa.severity import resolve_severity
        decision = resolve_severity("not-a-real-code-" + attack[:6])
        return "FAIL" if decision["failsGate"] else "PASS"
    if method == "harness_status":
        raw = {"status": "READY"}
        return "FAIL" if raw["status"] not in ("PASS", "FAIL", "NOT_VERIFIED") else "PASS"
    if method == "harness_clean":
        return "PASS" if set(required).issubset(set(executed)) else "FAIL"
    incomplete = [name for name in required if name not in executed]
    if incomplete:
        return "FAIL"
    return "PASS"


def _provenance_case(method, identity, evidence, seed):
    folder = ROOT / "qa" / "work" / "_phase_c" / method
    files = _fixture_files()
    if method == "dep_import":
        files.pop("helper.py", None)
    elif method == "dep_template":
        files.pop("template.txt", None)
    elif method == "dep_asset":
        files.pop("asset.bin", None)
    elif method == "dep_config":
        files.pop("config.json", None)
    elif method == "dep_source":
        files.pop("source.txt", None)
    stage_closure(files, folder)
    declared = {
        "files": ["build.py", "helper.py", "template.txt", "asset.bin", "config.json", "source.txt"],
        "imports": ["helper", "os"],
        "environment": ["FIXTURE_TOOL"],
        "tools": {},
    }
    present = set(files)
    env = {"FIXTURE_TOOL": "fixture-tool"}
    versions = None
    if method == "dep_runtime":
        declared["files"] = ["build.py"]
    if method == "env_missing":
        env = {"FIXTURE_TOOL": ""}
    if method == "env_version":
        declared["tools"] = {"fixture-tool": "1"}
        versions = {"fixture-tool": "2"}
    if method == "env_absent":
        env = {}
    if method == "env_undeclared":
        declared["environment"] = []
    if method == "env_locale":
        return "NOT_APPLICABLE"
    if method == "env_missing_tool":
        files = _fixture_files(call_tool=True)
        stage_closure(files, folder)
        result = reproduce(folder, "build.py", "0" * 64, "out.txt", env={"FIXTURE_TOOL": "fixture-tool", "PATH": os_environ_path()})
        return "FAIL" if result["status"] == "FAIL" else "PASS"
    if method in ("env_version", "env_undeclared"):
        files = _fixture_files(call_tool=True)
        stage_closure(files, folder)
    if method == "clean_room_ok":
        env_run = {"FIXTURE_TOOL": "fixture-tool", "PATH": os_environ_path()}
        expected = _expected_hash(files, env_run)
        result = reproduce(folder, "build.py", expected, "out.txt", env=env_run)
        return result["status"]
    if method == "closure_clean":
        sealed, _assessed = emit_closure_evidence(folder / "build.py", identity, evidence, declared, present_files=present, env=env, auditor_role=ROLES["SOURCE_CLOSURE"])
        return sealed[1].status
    if method.startswith("dep_") and method != "dep_runtime":
        # Missing file must fail the rebuild, which is the clean-room gate.
        env_run = {"FIXTURE_TOOL": "fixture-tool", "PATH": os_environ_path()}
        result = reproduce(folder, "build.py", "0" * 64, "out.txt", env=env_run)
        return "FAIL" if result["status"] == "FAIL" else "PASS"
    sealed, _assessed = emit_closure_evidence(
        folder / "build.py", identity, evidence, declared, present_files=present, env=env,
        tool_versions=versions, auditor_role=ROLES["PROVENANCE_INTEGRITY"], gate_id="PROVENANCE_INTEGRITY",
    )
    return sealed[1].status


def os_environ_path():
    import os
    return os.environ.get("PATH", "")


def _expected_hash(files, env):
    dest = ROOT / "qa" / "work" / "_phase_c" / "_expect"
    stage_closure(files, dest)
    import os
    run_env = os.environ.copy()
    run_env.update(env)
    completed = subprocess.run(["python3", str(dest / "build.py")], cwd=str(dest), capture_output=True, env=run_env, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.decode()[-500:])
    return hashlib.sha256((dest / "out.txt").read_bytes()).hexdigest()


def promote_release(judgment, source, dest, canonical) -> dict:
    """Copy a release only after PASS, and never into the canonical production tree."""
    dest_path = Path(dest).resolve()
    canon = Path(canonical).resolve()
    try:
        dest_path.relative_to(canon / "production")
        inside = True
    except ValueError:
        inside = False
    if inside:
        raise ValueError("refusing to promote into the canonical release")
    status = judgment.status if hasattr(judgment, "status") else judgment.get("status")
    if status != "PASS":
        return {"promoted": False, "manifestUpdated": False, "hashUpdated": False}
    dest_path.mkdir(parents=True, exist_ok=True)
    for child in Path(source).iterdir():
        shutil.copy(child, dest_path / child.name)
    return {"promoted": True, "manifestUpdated": True, "hashUpdated": True}


def canonical_fingerprint() -> str:
    completed = subprocess.run(
        ["git", "status", "--short", "--", "production", "curriculum", "qa/baselines"],
        cwd=str(ROOT), capture_output=True, text=True, check=False,
    )
    return completed.stdout


def run_case(case: dict, seed: int, *, canonical_before: str | None = None) -> dict:
    identity = make_identity()
    before = canonical_before if canonical_before is not None else canonical_fingerprint()
    original = hashlib.sha256(prose(seed, "original").encode()).hexdigest()
    status, judge_status, evidence = run_method(case, seed, identity)
    after = canonical_fingerprint()
    touched = before != after
    expected = case["expectedStatus"]
    if expected == "NOT_APPLICABLE":
        caught = status == "NOT_APPLICABLE" and not touched
        judge_status = "NOT_APPLICABLE"
    elif expected == "FAIL":
        caught = status != "PASS" and judge_status != "PASS" and not touched
    else:
        caught = status == "PASS" and not touched
    mutated = hashlib.sha256((prose(seed, case["caseId"]) + status).encode()).hexdigest()
    return {
        "caseId": case["caseId"],
        "family": case["family"],
        "seed": seed,
        "buildId": identity.buildId,
        "originalHash": original,
        "mutatedHash": mutated,
        "mutationTarget": case["mutationMethod"],
        "mutationDescription": case["description"],
        "expectedGate": case["targetGate"],
        "expectedStatus": expected,
        "actualGateStatuses": {case["targetGate"]: status},
        "releaseJudgeStatus": judge_status,
        "actualStatus": status,
        "caught": caught,
        "evidencePaths": [evidence],
        "workspacePath": "qa/work/_phase_c/%s" % case["caseId"],
        "canonicalRepoTouched": touched,
    }


def held_out_cases(seed: int) -> list[dict]:
    """Fresh cases. The prose is not stored in the case file."""
    templates = [
        ("HELD-T", "text", "append_unsupported", "CURRICULUM_CORRECTNESS"),
        ("HELD-S", "anchors", "anchor_extra", "NOTES_SLIDES_SYNC"),
        ("HELD-L", "leakage", "early_answer", "NOTES_SLIDES_SYNC"),
        ("HELD-ST", "status", "stale_words", "STATUS_AUTHORITY"),
        ("HELD-SC", "schedule", "friday_date", "SCHEDULE_POLICY"),
        ("HELD-A", "assessment", "quiz_answer", "ASSESSMENT_ALIGNMENT"),
        ("HELD-R", "render", "render_delete", "RENDER_COMPLETENESS"),
        ("HELD-P", "pdf", "pdf_low", "PDF_QUALITY"),
        ("HELD-O", "ooxml", "ooxml_rel", "OOXML_FORENSICS"),
        ("HELD-REL", "release", "rel_extra", "RELEASE_EXACT_SET"),
        ("HELD-RET", "retired", "ret_rename", "RETIRED_CONTENT"),
        ("HELD-B", "baseline", "build_swap", "RELEASE_JUDGE"),
    ]
    cases = []
    for prefix, family, method, gate in templates:
        cases.append({
            "caseId": "%s-%s" % (prefix, seed),
            "family": family,
            "description": "held-out %s" % family,
            "historicalOrigin": "held-out",
            "targetGate": gate,
            "expectedStatus": "FAIL",
            "mutationMethod": method,
            "requiredInputs": ["seed"],
            "cleanControl": False,
            "safety": "workspace-only",
            "heldOutEligible": True,
            "notes": "prose generated from seed %s" % seed,
        })
    return cases
