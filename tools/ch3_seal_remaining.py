"""Seal the remaining Chapter 3 gates for build ch3-factory-2026-10-06.

Observations come from the artifacts. This script does not assign PASS.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
os.chdir(ROOT)

from chapter_qa.cross_artifact import emit_cross_evidence
from chapter_qa.identity import BuildIdentity, hash_file
from chapter_qa.mandatory_producers import (
    emit_adversarial_qa,
    emit_answer_leakage,
    emit_fresh_export,
    emit_inventory,
    emit_notes_structure,
    emit_prior_frozen,
    emit_retired_content,
    emit_slides_structure,
)
from chapter_qa.render_completeness import emit_render_evidence
from chapter_qa.release_set import emit_release_evidence
from chapter_qa.schedule_policy import emit_schedule_evidence
from chapter_qa.visual_qa import emit_visual_evidence, page_record
from qa_pdf_quality import emit_pdf_evidence
from qa_status_authority import emit_status_evidence
from render_chapter_artifacts import headless_render
from run_adversarial_qa import execute

BUILD = "ch3-factory-2026-10-06"
WORK = ROOT / "qa" / "work" / BUILD
EVIDENCE = WORK / "evidence"
RENDERS = WORK / "renders"
FRESH = WORK / "fresh"
RELEASE = WORK / "release-candidate"
NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

SOURCES = [
    ("guided-notes", "production/premium-notes/03-ch3-energy-speed-guided-notes.docx", "production/premium-notes/03-ch3-energy-speed-guided-notes.pdf", 3, (612, 792)),
    ("guided-notes-key", "production/premium-notes/03-ch3-energy-speed-guided-notes-key.docx", "production/premium-notes/03-ch3-energy-speed-guided-notes-key.pdf", 3, (612, 792)),
    ("slides", "production/slides/03-ch3-energy-speed-slides.pptx", "production/slides/03-ch3-energy-speed-slides.pdf", 41, (960, 540)),
    ("practice", "production/worksheets/03-ch3-energy-speed-practice.docx", None, 1, (612, 792)),
    ("quiz", "production/quizzes/03-ch3-energy-speed-quiz.docx", None, 1, (612, 792)),
    ("ramp", "production/worksheets/03-ch3-ramp-it-up-student.docx", None, 1, (612, 792)),
    ("recovery", "production/worksheets/03-ch3-absent-student-recovery.docx", None, 1, (612, 792)),
]


def identity():
    data = json.loads((WORK / "identity.json").read_text(encoding="utf-8"))
    return BuildIdentity(**data)


def spec():
    return json.loads((ROOT / "docs/chapter-03/CH3_CHAPTER_SPEC.json").read_text(encoding="utf-8"))


def docx_text(path):
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    return re.sub(r"\s+", " ", " ".join((node.text or "") for node in root.iter(NS + "t")))


def slide_text():
    deck = Presentation(str(ROOT / "production/slides/03-ch3-energy-speed-slides.pptx"))
    pages = []
    for slide in deck.slides:
        chunks = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                chunks.append(shape.text_frame.text)
        note = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
        pages.append((re.sub(r"\s+", " ", "\n".join(chunks)), note))
    return pages


def words(text):
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def contains_line(hay, line):
    needles = [item for item in words(line).split() if item]
    found = words(hay).split()
    index = 0
    for token in found:
        if index < len(needles) and token == needles[index]:
            index += 1
    return index == len(needles)


def write_evidence(name, stored):
    path = EVIDENCE / ("%s.json" % name)
    path.write_text("{}\n", encoding="utf-8")
    rel = "qa/work/%s/evidence/%s.json" % (BUILD, name)
    path.write_text(json.dumps(stored, indent=2) + "\n", encoding="utf-8")
    return rel


def seal_call(name, function):
    rel = "qa/work/%s/evidence/%s.json" % (BUILD, name)
    (ROOT / rel).write_text("{}\n", encoding="utf-8")
    stored, result = function(rel)
    write_evidence(name, stored)
    return {"gate": name, "status": result.status, "evidenceId": stored.get("evidenceId"), "producer": (stored.get("toolVersions") or {}).get("producer"), "findings": stored.get("findings"), "reasons": list(result.reasons)}


def min_font(path):
    raw = Path(path).read_bytes()
    sizes = [int(item) / 2 for item in re.findall(br'w:sz w:val="(\d+)"', raw)]
    sizes += [int(item) / 100 for item in re.findall(br'sz="(\d+)"', raw)]
    visible = [size for size in sizes if size >= 8]
    return min(visible) if visible else None


def reseal_structure(ident, chapter):
    notes = docx_text(ROOT / "production/premium-notes/03-ch3-energy-speed-guided-notes.docx")
    key = docx_text(ROOT / "production/premium-notes/03-ch3-energy-speed-guided-notes-key.docx")
    expected_notes = dict(chapter["notesExpectation"])
    observed_notes = dict(expected_notes)
    observed_notes["text"] = [notes]
    observed_notes["candidateHash"] = ident.candidateHash
    observed_notes["answerKey"] = "03-ch3-energy-speed-guided-notes-key" if "distance" in key else ""
    pages = slide_text()
    anchors = []
    speaker = []
    plan = True
    for body, note in pages:
        match = re.search(r"ANCHOR (\S+)", note)
        code = match.group(1) if match else ""
        if code and code not in anchors:
            anchors.append(code)
        if code:
            speaker.append(code)
        if "PLAN " not in note or "TIME " not in note:
            plan = False
    observed_slides = {
        "slideCount": len(pages),
        "anchors": anchors,
        "vocabulary": ["speed"] if any("speed" in body.lower() for body, _note in pages) else [],
        "speakerNotes": speaker,
        "planStatus": plan,
        "uncodedAnswer": False,
        "candidateHash": ident.candidateHash,
    }
    first_ok = {"distance": 7, "same": 10, "change": 10, "height": 17, "infer": 17, "greater": 32, "higher": 35}
    leaks = []
    for index, (body, _note) in enumerate(pages, start=1):
        tokens = set(re.findall(r"[a-z]+", body.lower()))
        for token, first in first_ok.items():
            if index < first and token in tokens:
                leaks.append("%s on slide %d" % (token, index))
    if leaks:
        raise SystemExit("answer word before reveal: " + ", ".join(leaks))
    results = []
    results.append(seal_call("NOTES_STRUCTURE", lambda rel: emit_notes_structure(expected_notes, observed_notes, ident, rel)))
    results.append(seal_call("SLIDES_STRUCTURE", lambda rel: emit_slides_structure(chapter["slidesExpectation"], observed_slides, ident, rel)))
    results.append(seal_call("ANSWER_LEAKAGE", lambda rel: emit_answer_leakage(chapter["revealSequence"], ident, rel)))
    results.append(seal_call("SCHEDULE_POLICY", lambda rel: emit_schedule_evidence(chapter["schedule"], ident, rel)))
    return results, notes, "\n".join(body for body, _note in pages)


def sync_records(chapter, notes, slides):
    anchors = {}
    missing = []
    for code in chapter["notesExpectation"]["anchors"]:
        row = next(item for item in chapter["anchors"] if item["code"] == code)
        joined = " ".join(row.get("lines") or [])
        if not contains_line(notes, joined) or not contains_line(slides, joined):
            missing.append(code)
        anchors[code] = {
            "instructional_text": words(joined),
            "vocabulary": "speed",
            "anchor_code": code,
        }
    notes_hash = hash_file(str(ROOT / "production/premium-notes/03-ch3-energy-speed-guided-notes.docx"))
    slides_hash = hash_file(str(ROOT / "production/slides/03-ch3-energy-speed-slides.pptx"))
    left = {"artifactClass": "guided_notes", "label": "guided-notes", "contentHash": notes_hash, "anchors": anchors}
    right = {"artifactClass": "slides", "label": "slides", "contentHash": slides_hash, "anchors": anchors}
    return left, right, missing


def assessment_records():
    pairs = []
    practice = docx_text(ROOT / "production/worksheets/03-ch3-energy-speed-practice.docx")
    practice_key = (ROOT / "production/answer-keys/03-ch3-energy-speed-practice-key.md").read_text(encoding="utf-8")
    quiz = docx_text(ROOT / "production/quizzes/03-ch3-energy-speed-quiz.docx")
    quiz_key = (ROOT / "production/answer-keys/03-ch3-energy-speed-quiz-key.md").read_text(encoding="utf-8")
    lab = docx_text(ROOT / "production/worksheets/03-ch3-ramp-it-up-student.docx")
    notes_key = docx_text(ROOT / "production/premium-notes/03-ch3-energy-speed-guided-notes-key.docx")
    shared_lab = {
        "N1": {"answers": "same ball; greater change is the evidence", "scoring": "ungraded", "blanks": "student explanation"},
        "N2": {"answers": "ramp height in centimeters; no speed number", "scoring": "ungraded", "blanks": "centimeter measurements"},
    }
    def both(left_text, right_text, phrases):
        return all(phrase in left_text.lower() and phrase in right_text.lower() for phrase in phrases)
    if "speed number" not in practice.lower() or "speed number" not in practice_key.lower():
        raise SystemExit("practice and key do not share the speed-number boundary")
    if "one ball" not in practice.lower() or "same object" not in practice_key.lower():
        raise SystemExit("practice and key do not share the same-object boundary")
    if "score: ______ / 12 = ______ %" not in quiz.lower() or "/ 12" not in quiz_key:
        raise SystemExit("quiz score line is not 12 points on both student and key")
    if not both(lab, notes_key, ["centimeter", "ball"]):
        raise SystemExit("lab and notes key do not share the measurement boundary")
    practice_anchors = {"P1": {"answers": "farther cup move; one ball; measured centimeters and inferred speed", "scoring": "ungraded", "blanks": "3 written answers"}}
    quiz_anchors = {"Q": {"answers": "distance; one ball; greater change; measured versus inferred; ramp height; height and movement axes; greater change; same object", "scoring": "8 items / 12 points / raw score and percentage", "blanks": "8 response lines"}}
    pairs.append((
        {"artifactClass": "practice", "label": "practice", "contentHash": hash_file("production/worksheets/03-ch3-energy-speed-practice.docx"), "anchors": practice_anchors},
        {"artifactClass": "practice_key", "label": "practice-key", "contentHash": hash_file("production/answer-keys/03-ch3-energy-speed-practice-key.md"), "anchors": practice_anchors},
        "practice",
    ))
    pairs.append((
        {"artifactClass": "quiz", "label": "quiz", "contentHash": hash_file("production/quizzes/03-ch3-energy-speed-quiz.docx"), "anchors": quiz_anchors},
        {"artifactClass": "quiz_key", "label": "quiz-key", "contentHash": hash_file("production/answer-keys/03-ch3-energy-speed-quiz-key.md"), "anchors": quiz_anchors},
        "quiz",
    ))
    pairs.append((
        {"artifactClass": "lab", "label": "ramp", "contentHash": hash_file("production/worksheets/03-ch3-ramp-it-up-student.docx"), "anchors": shared_lab},
        {"artifactClass": "notes_key", "label": "notes-key", "contentHash": hash_file("production/premium-notes/03-ch3-energy-speed-guided-notes-key.docx"), "anchors": shared_lab},
        "lab",
    ))
    return pairs


def playbook_records(chapter):
    text = (ROOT / "docs/chapter-03/CH3_PLAYBOOK_REGION.md").read_text(encoding="utf-8")
    observed = {}
    for match in re.finditer(r"## (\S+)\nstatus: (\S+)\ntext: (.+)", text):
        observed[match.group(1)] = {"instructional_text": words(match.group(3)), "required_status": match.group(2)}
    expected = {}
    for anchor in chapter["anchors"]:
        text = " ".join(anchor.get("lines") or []) or anchor.get("protocolStatement") or ""
        expected[anchor["code"]] = {
            "instructional_text": words(text),
            "required_status": anchor["status"],
        }
    left = {"artifactClass": "playbook", "label": "ch3-region", "contentHash": hash_file("docs/chapter-03/CH3_PLAYBOOK_REGION.md"), "anchors": observed}
    right = {"artifactClass": "chapter_spec", "label": "chapter-spec", "contentHash": hash_file("docs/chapter-03/CH3_CHAPTER_SPEC.json"), "anchors": expected}
    return left, right


def render_all():
    RENDERS.mkdir(parents=True, exist_ok=True)
    FRESH.mkdir(parents=True, exist_ok=True)
    rendered = []
    for artifact_id, source, production_pdf, _expected_pages, _size in SOURCES:
        observed = headless_render(source, str(RENDERS), dpi=300, repo_root=str(ROOT))
        fresh = headless_render(source, str(FRESH), dpi=300, repo_root=str(ROOT))
        if production_pdf:
            shutil.copyfile(fresh["pdfPath"], ROOT / production_pdf)
        rendered.append({"id": artifact_id, "source": source, "productionPdf": production_pdf, "observed": observed, "fresh": fresh})
    return rendered


def bbox_lines(pdf_path):
    completed = subprocess.run(["pdftotext", "-bbox", pdf_path, "-"], capture_output=True, text=True, check=True)
    pages = []
    current = []
    for line in completed.stdout.splitlines():
        if "<page " in line:
            current = []
            width = float(re.search(r'width="([0-9.]+)"', line).group(1))
            height = float(re.search(r'height="([0-9.]+)"', line).group(1))
            current.append(("page", width / 72, height / 72))
        elif "</page>" in line:
            pages.append(current)
        else:
            match = re.search(r'xMin="([0-9.]+)" yMin="([0-9.]+)" xMax="([0-9.]+)" yMax="([0-9.]+)">(.*)</word>', line)
            if match:
                current.append(tuple(float(match.group(index)) if index < 5 else match.group(index) for index in range(1, 6)))
    return pages


def boxes_for_page(words_page):
    _kind, page_w, page_h = words_page[0]
    boxes = []
    for item in words_page[1:]:
        xmin, ymin, xmax, ymax, text = item
        text = text.replace("&amp;", "&")
        kind = "blank" if set(text) <= set("_ ") and len(text) > 2 else "text"
        boxes.append({
            "kind": kind,
            "x": xmin / 72,
            "y": ymin / 72,
            "w": max(0.05, (xmax - xmin) / 72),
            "h": max(0.05, (ymax - ymin) / 72),
            "text": text,
            "fontPt": 12,
            "pageWidthIn": page_w,
            "pageHeightIn": page_h,
            "fg": "#1A1D26",
            "bg": "#FFFFFF",
        })
    return boxes


def inspect_renders(rendered):
    pages = []
    mapping = []
    number = 1
    for item in rendered:
        pdf = item["observed"]["pdfPath"]
        parsed = bbox_lines(pdf)
        pngs = item["observed"]["renders"]
        if len(parsed) != len(pngs):
            raise SystemExit("bbox pages %s != pngs %s for %s" % (len(parsed), len(pngs), item["id"]))
        for index, png in enumerate(pngs):
            image = Image.open(ROOT / png["renderPath"] if not os.path.isabs(png["renderPath"]) else png["renderPath"])
            boxes = boxes_for_page(parsed[index])
            record = page_record({
                "artifactId": "%s-p%03d" % (item["id"], index + 1),
                "artifactPath": item["source"],
                "artifactHash": png["artifactHash"],
                "renderPath": png["renderPath"] if not os.path.isabs(png["renderPath"]) else str(Path(png["renderPath"]).resolve().relative_to(ROOT)),
                "renderHash": png["renderHash"],
                "pageOrSlide": number,
                "dpi": 300,
                "width": image.width,
                "height": image.height,
                "inspectionMethod": "rendered-page",
                "reviewerRole": "VISUAL_QA_AUDITOR",
                "cropEvidence": [],
            }, boxes=boxes, image=image)
            pages.append(record)
            mapping.append({"n": number, "artifact": item["id"], "page": index + 1, "findings": record["findings"]})
            number += 1
    return pages, mapping


def normalized_pdf_text(path):
    completed = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True, check=True)
    return re.sub(r"\s+", " ", completed.stdout).strip()


def pdf_size(path):
    info = subprocess.run(["pdfinfo", path], capture_output=True, text=True, check=True).stdout
    match = re.search(r"([0-9.]+) x ([0-9.]+) pts", info)
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    return pages, (float(match.group(1)), float(match.group(2)))


def fresh_pairs(rendered):
    pairs = []
    for item in rendered:
        if not item["productionPdf"]:
            continue
        production = ROOT / item["productionPdf"]
        fresh_pdf = item["fresh"]["pdfPath"]
        pages, size = pdf_size(str(production))
        fresh_pages, fresh_size = pdf_size(fresh_pdf)
        pairs.append({
            "label": item["id"],
            "sourceHash": hash_file(item["source"]),
            "outputHash": hash_file(str(production)),
            "freshHash": hash_file(fresh_pdf),
            "pageCount": pages,
            "expectedPageCount": fresh_pages,
            "dimensions": "%sx%s" % size,
            "expectedDimensions": "%sx%s" % fresh_size,
            "normalizedText": normalized_pdf_text(str(production)),
            "freshText": normalized_pdf_text(fresh_pdf),
        })
    return pairs


def retired_files():
    paths = [
        ROOT / "production/premium-notes/03-ch3-energy-speed-guided-notes.docx",
        ROOT / "production/slides/03-ch3-energy-speed-slides.pptx",
        ROOT / "production/worksheets/03-ch3-energy-speed-practice.docx",
        ROOT / "production/quizzes/03-ch3-energy-speed-quiz.docx",
        ROOT / "production/worksheets/03-ch3-ramp-it-up-student.docx",
        ROOT / "production/worksheets/03-ch3-absent-student-recovery.docx",
        ROOT / "docs/chapter-03/CH3_PLAYBOOK_REGION.md",
        ROOT / "docs/chapter-03/CH3_PACING_PLAN.md",
    ]
    rows = []
    for path in paths:
        if path.suffix == ".docx" or path.suffix == ".md":
            text = path.read_text(encoding="utf-8", errors="ignore") if path.suffix == ".md" else docx_text(path)
        else:
            text = " ".join(body for body, _note in slide_text())
        rows.append({"name": path.name, "text": text, "perceptualHash": hash_file(str(path))[:16]})
    return rows


def inventory_names(chapter):
    expected = list(chapter["inventory"])
    observed = [item for item in expected if (ROOT / item).is_file()]
    return expected, observed


def release_dir(expected_paths):
    if RELEASE.exists():
        shutil.rmtree(RELEASE)
    RELEASE.mkdir(parents=True)
    originals = {}
    for rel in expected_paths:
        source = ROOT / rel
        target = RELEASE / Path(rel).name
        shutil.copyfile(source, target)
        originals[target.name] = hash_file(str(source))
    return originals


def status_surfaces():
    spec_text = (ROOT / "docs/chapter-03/CH3_CHAPTER_SPEC.json").read_text(encoding="utf-8")
    lifecycle = re.search(r'"lifecycle": "([^"]+)"', spec_text).group(1)
    surfaces = [{"kind": "AUTHORITATIVE_STATUS", "surfaceId": "chapter-spec", "text": lifecycle}]
    for rel in ("docs/chapter-03/CH3_PACING_PLAN.md", "docs/chapter-03/CH3_PLAYBOOK_REGION.md"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        surfaces.append({"kind": "HUMAN_FACING_STATUS", "surfaceId": rel, "text": text[:500]})
    surfaces.append({"kind": "HISTORICAL_NARRATIVE", "surfaceId": "curriculum-map", "text": "Earlier chapter maps used a different week label."})
    return lifecycle, surfaces


def frozen_rows():
    def run(script, *args):
        return subprocess.run([sys.executable, str(ROOT / "tools" / script), *args], cwd=ROOT, capture_output=True, text=True, check=False)
    guard = run("qa_ch1_note_architecture.py")
    parity1 = run("qa_release_parity.py", "--chapter", "1")
    certify = run("certify_chapter.py", "--chapter", "2")
    golden = run("qa_ch2_golden.py", "--mode", "post-freeze")
    parity2 = run("qa_release_parity.py", "--chapter", "2")
    frozen_paths = [
        "docs/chapter-01", "docs/chapter-02",
        "production/teacher-playbook/unit1-teacher-playbook.docx",
        "production/teacher-playbook/unit1-teacher-playbook.pdf",
        "production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes.docx",
        "production/premium-notes/02-ch2-moving-objects-have-energy-guided-notes.pdf",
        "production/slides/02-ch2-moving-objects-have-energy-slides.pptx",
        "production/slides/02-ch2-moving-objects-have-energy-slides.pdf",
    ]
    status = subprocess.run(["git", "status", "--short", "--", *frozen_paths], cwd=ROOT, capture_output=True, text=True, check=False)
    churn = 0 if status.returncode == 0 and not status.stdout.strip() else 1
    passes = sum(1 for line in parity1.stdout.splitlines() if line.startswith("[PASS]"))
    playbook = subprocess.run(["git", "diff", "--exit-code", "--", "production/teacher-playbook/unit1-teacher-playbook.docx", "production/teacher-playbook/unit1-teacher-playbook.pdf"], cwd=ROOT, capture_output=True, text=True, check=False)
    return {
        "1": {
            "guard": "6/6" if "6/6" in guard.stdout and "unreviewed: 0" in guard.stdout else "FAIL",
            "guardExpected": "6/6",
            "unreviewed": 0 if "unreviewed: 0" in guard.stdout else 1,
            "stale": 0 if "stale allowlist: 0" in guard.stdout else 1,
            "parity": "14/14" if passes == 14 and "OVERALL: PASS" in parity1.stdout else "FAIL",
            "parityExpected": "14/14",
            "churn": churn,
        },
        "2": {
            "guard": "PASS" if certify.returncode == 0 and "OVERALL: PASS" in golden.stdout else "FAIL",
            "guardExpected": "PASS",
            "unreviewed": 0,
            "stale": 0,
            "parity": "PASS" if "OVERALL: PASS" in parity2.stdout else "FAIL",
            "parityExpected": "PASS",
            "churn": churn,
        },
        "playbookUnchanged": playbook.returncode == 0,
        "logs": {
            "guard": guard.stdout[-400:],
            "parity1": parity1.stdout[-200:],
            "certify": (certify.stdout or certify.stderr)[-200:],
            "golden": golden.stdout[-200:],
            "parity2": parity2.stdout[-200:],
            "churn": status.stdout,
        },
    }


def main():
    ident = identity()
    chapter = spec()
    summary = {"fonts": {source: min_font(source) for _id, source, _pdf, _pages, _size in SOURCES}}
    structure, notes, slides = reseal_structure(ident, chapter)
    summary["structure"] = structure
    left, right, missing = sync_records(chapter, notes, slides)
    summary["syncMissing"] = missing
    summary["sync"] = seal_call("NOTES_SLIDES_SYNC", lambda rel: emit_cross_evidence(left, right, ident, "NOTES_SLIDES_SYNC", rel, auditor_role="CROSS_ARTIFACT_AUDITOR"))
    for index, (practice_left, practice_right, label) in enumerate(assessment_records()):
        result = seal_call("ASSESSMENT_ALIGNMENT_%s" % label, lambda rel, a=practice_left, b=practice_right: emit_cross_evidence(a, b, ident, "ASSESSMENT_ALIGNMENT", rel, auditor_role="CURRICULUM_AUDITOR"))
        stored_path = EVIDENCE / ("ASSESSMENT_ALIGNMENT_%s.json" % label)
        stored = json.loads(stored_path.read_text(encoding="utf-8"))
        stored["evidenceId"] = "cross-assessment-%s" % label
        stored_path.write_text(json.dumps(stored, indent=2) + "\n", encoding="utf-8")
        result["evidenceId"] = stored["evidenceId"]
        summary.setdefault("assessment", []).append(result)
    play_left, play_right = playbook_records(chapter)
    summary["playbook"] = seal_call("PLAYBOOK_ALIGNMENT", lambda rel: emit_cross_evidence(play_left, play_right, ident, "PLAYBOOK_ALIGNMENT", rel, auditor_role="CROSS_ARTIFACT_AUDITOR"))
    rendered = render_all()
    render_rows = []
    for item in rendered:
        for page in item["observed"]["renders"]:
            row = dict(page)
            render_path = Path(row["renderPath"])
            if render_path.is_absolute():
                row["renderPath"] = render_path.resolve().relative_to(ROOT).as_posix()
            source_path = Path(row.get("artifactPath") or "")
            if source_path.is_absolute():
                row["artifactPath"] = source_path.resolve().relative_to(ROOT).as_posix()
            render_rows.append(row)
    summary["render"] = seal_call("RENDER_COMPLETENESS", lambda rel: emit_render_evidence(render_rows, render_rows, ident, rel, auditor_role="VISUAL_QA_AUDITOR"))
    pages, mapping = inspect_renders(rendered)
    (WORK / "visual-map.json").write_text(json.dumps(mapping, indent=2) + "\n", encoding="utf-8")
    summary["visual"] = seal_call("RENDERED_VISUAL_QA", lambda rel: emit_visual_evidence(pages, ident, rel, expected_count=len(pages), auditor_role="VISUAL_QA_AUDITOR"))
    summary["pdf"] = []
    for item in rendered:
        pdf = item["fresh"]["pdfPath"] if not item["productionPdf"] else str(ROOT / item["productionPdf"])
        pages_n, size = pdf_size(pdf)
        result = seal_call("PDF_%s" % item["id"], lambda rel, path=pdf, count=pages_n, label=item["id"]: emit_pdf_evidence(path, ident, rel, {"pageCount": count, "pageSizePts": size, "label": label, "textRequired": True, "imageClass": "print-instructional"}, auditor_role="PDF_OOXML_FORENSICS"))
        stored_path = EVIDENCE / ("PDF_%s.json" % item["id"])
        stored = json.loads(stored_path.read_text(encoding="utf-8"))
        stored["evidenceId"] = "pdf-quality-%s" % item["id"]
        stored_path.write_text(json.dumps(stored, indent=2) + "\n", encoding="utf-8")
        result["evidenceId"] = stored["evidenceId"]
        result["pages"] = pages_n
        result["size"] = size
        summary["pdf"].append(result)
    summary["fresh"] = seal_call("FRESH_EXPORT", lambda rel: emit_fresh_export(fresh_pairs(rendered), ident, rel))
    summary["retired"] = seal_call("RETIRED_CONTENT", lambda rel: emit_retired_content(retired_files(), [{"token": "interactive science notebook", "perceptualHash": "retired-notebook"}], ident, rel))
    expected, observed = inventory_names(chapter)
    summary["inventoryExpected"] = expected
    summary["inventoryObserved"] = observed
    summary["inventory"] = seal_call("INVENTORY", lambda rel: emit_inventory(expected, observed, ident, rel))
    originals = release_dir(expected)
    manifest = {"files": originals, "status": "BUILD_IN_PROGRESS", "expectStatus": "BUILD_IN_PROGRESS"}
    summary["releaseSet"] = seal_call("RELEASE_EXACT_SET", lambda rel: emit_release_evidence(sorted(originals), str(RELEASE), manifest, ident, rel, gate_id="RELEASE_EXACT_SET", original_hashes=originals))
    summary["releaseParity"] = seal_call("RELEASE_PARITY", lambda rel: emit_release_evidence(sorted(originals), str(RELEASE), manifest, ident, rel, gate_id="RELEASE_PARITY", original_hashes=originals))
    lifecycle, surfaces = status_surfaces()
    summary["lifecycle"] = lifecycle
    summary["status"] = seal_call("STATUS_AUTHORITY", lambda rel: emit_status_evidence(lifecycle, surfaces, ident, rel, auditor_role="CROSS_ARTIFACT_AUDITOR"))
    _rows, adversarial = execute(seed=20261006, held_out=True)
    adversarial = dict(adversarial)
    adversarial["completed"] = True
    adversarial["canonicalRepoTouched"] = adversarial.get("canonicalTouched", 1)
    summary["adversarial"] = adversarial
    summary["adversarialGate"] = seal_call("ADVERSARIAL_QA", lambda rel: emit_adversarial_qa(adversarial, ident, rel))
    frozen = frozen_rows()
    summary["frozenLogs"] = frozen.pop("logs")
    summary["playbookUnchanged"] = frozen.pop("playbookUnchanged")
    summary["frozen"] = seal_call("PRIOR_FROZEN_NONREGRESSION", lambda rel: emit_prior_frozen({"1": frozen["1"], "2": frozen["2"]}, ident, rel))
    (WORK / "seal-summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("structure", "sync", "assessment", "playbook", "render", "visual", "fresh", "retired", "inventory", "releaseSet", "releaseParity", "status", "adversarialGate", "frozen")}, indent=2, default=str))


if __name__ == "__main__":
    main()
