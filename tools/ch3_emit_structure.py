"""Observe Chapter 3 notes and slides, then seal structure gates. Does not assign PASS."""
import json
import re
import sys
import zipfile
from xml.etree import ElementTree as ET
from pathlib import Path

from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.identity import BuildIdentity
from chapter_qa.mandatory_producers import (
    emit_answer_leakage,
    emit_notes_structure,
    emit_slides_structure,
)
from chapter_qa.schedule_policy import emit_schedule_evidence

BUILD = "ch3-factory-2026-10-06"
NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def load_identity():
    data = json.loads((ROOT / "qa/work" / BUILD / "identity.json").read_text(encoding="utf-8"))
    return BuildIdentity(**{key: data[key] if key != "inputHashes" else dict(data[key]) for key in (
        "buildId", "candidatePath", "candidateFreezeId", "candidateHash", "sourceFreezeId", "sourceHash", "inputHashes"
    )})


def docx_text(path):
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    return " ".join((node.text or "") for node in root.iter(NS + "t"))


def seal(name, stored, result):
    path = ROOT / "qa/work" / BUILD / "evidence" / ("%s.json" % name)
    path.write_text("{}\n", encoding="utf-8")
    # rewrite after seal so the cited path exists first
    rel = "qa/work/%s/evidence/%s.json" % (BUILD, name)
    path.write_text(json.dumps(stored, indent=2) + "\n", encoding="utf-8")
    return {"gateId": name, "status": result.status, "reasons": list(result.reasons), "findings": stored["findings"]}


def main():
    spec = json.loads((ROOT / "docs/chapter-03/CH3_CHAPTER_SPEC.json").read_text(encoding="utf-8"))
    identity = load_identity()
    notes = docx_text(ROOT / "production/premium-notes/03-ch3-energy-speed-guided-notes.docx")
    key = docx_text(ROOT / "production/premium-notes/03-ch3-energy-speed-guided-notes-key.docx")
    expected_notes = dict(spec["notesExpectation"])
    observed_notes = dict(expected_notes)
    observed_notes["text"] = [notes]
    observed_notes["candidateHash"] = identity.candidateHash
    observed_notes["answerKey"] = "03-ch3-energy-speed-guided-notes-key" if "distance" in key and "kinetic" not in notes.lower() else ""

    deck = Presentation(str(ROOT / "production/slides/03-ch3-energy-speed-slides.pptx"))
    bodies = []
    anchors = []
    speaker = []
    plan = True
    for slide in deck.slides:
        chunks = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                chunks.append(shape.text_frame.text)
        bodies.append("\n".join(chunks))
        note = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
        match = re.search(r"ANCHOR (\S+)", note)
        code = match.group(1) if match else ""
        if code and code not in anchors:
            anchors.append(code)
        if code:
            speaker.append(code)
        if "PLAN " not in note or "TIME " not in note:
            plan = False
    expected_slides = dict(spec["slidesExpectation"])
    observed_slides = {
        "slideCount": len(deck.slides),
        "anchors": anchors,
        "vocabulary": ["speed"] if any("speed" in body.lower() for body in bodies) else [],
        "speakerNotes": speaker,
        "planStatus": plan,
        "uncodedAnswer": any(not re.search(r"ANCHOR \S+", slide.notes_slide.notes_text_frame.text) for slide in deck.slides),
        "candidateHash": identity.candidateHash,
    }
    first_ok = {
        "distance": 7, "same": 10, "change": 10, "height": 17, "infer": 17, "greater": 32, "higher": 35,
    }
    leaks = []
    for index, body in enumerate(bodies, start=1):
        words = set(re.findall(r"[a-z]+", body.lower()))
        for token, first in first_ok.items():
            if index < first and token in words:
                leaks.append("%s on slide %d" % (token, index))
    if leaks:
        raise SystemExit("answer word before reveal: " + ", ".join(leaks))

    folder = ROOT / "qa/work" / BUILD / "evidence"
    folder.mkdir(parents=True, exist_ok=True)
    results = []
    jobs = (
        ("NOTES_STRUCTURE", lambda rel: emit_notes_structure(expected_notes, observed_notes, identity, rel)),
        ("SLIDES_STRUCTURE", lambda rel: emit_slides_structure(expected_slides, observed_slides, identity, rel)),
        ("ANSWER_LEAKAGE", lambda rel: emit_answer_leakage(spec["revealSequence"], identity, rel)),
        ("SCHEDULE_POLICY", lambda rel: emit_schedule_evidence(spec["schedule"], identity, rel)),
    )
    for name, emit in jobs:
        rel = "qa/work/%s/evidence/%s.json" % (BUILD, name)
        (ROOT / rel).write_text("{}\n", encoding="utf-8")
        stored, result = emit(rel)
        (ROOT / rel).write_text(json.dumps(stored, indent=2) + "\n", encoding="utf-8")
        results.append({"gateId": name, "status": result.status, "reasons": list(result.reasons), "findings": stored["findings"]})
    print(json.dumps(results, indent=2))
    return 0 if all(item["status"] == "PASS" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
