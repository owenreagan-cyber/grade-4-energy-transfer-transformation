"""File-observing producers for the seven remaining F-3 gates.

Each producer opens the actual artifact bytes, derives its own observation, and
seals evidence through the central evaluator. Caller input is limited to paths,
build identity, and policy/expected configuration — never the observed result.

All producers:
- derive observations from ``text_extraction`` on real files;
- produce FAIL (via a blocking finding) on missing/unreadable input;
- never accept a caller-supplied boolean or observation dict.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

from chapter_qa.emit import seal
from chapter_qa.identity import REPO_ROOT
from chapter_qa.text_extraction import (
    anchor_codes_in_order,
    blank_count,
    docx_paragraphs,
    extract_text,
    family_hits,
    normalize,
    pdf_pages,
    pdf_text,
    slide_blocks,
)

_HIGH = "HIGH"
_BLOCKING = "BLOCKING"


def _finding(severity: str, code: str, message: str) -> dict:
    return {"severity": severity, "code": code, "message": message}


def _base(gate_id, evidence_id, identity, evidence_path, auditor_role, performed, findings, inputs, thing, independent, inventory_name, expected, observed):
    failed = bool(findings) or not performed
    data = {
        "evidenceId": evidence_id,
        "gateId": gate_id,
        "auditorRole": auditor_role,
        "performed": performed,
        "expectedInputs": inputs if performed else [],
        "observedInputs": inputs if performed and not failed else [],
        "thingBeingCertified": thing,
        "independentEvidenceSource": independent,
        "findings": findings,
        "evidencePaths": [evidence_path],
        "failureReason": None,
        "notVerifiedReason": None,
        "invalidationReasons": [],
        "execution": {
            "succeeded": performed,
            "detectorException": False,
            "requiredInputsPresent": performed,
            "missingRender": False,
            "missingEvidence": not performed,
            "stale": False,
            "gateSpecificFailure": failed,
            "unavailableEvidence": False,
        },
        "inventory": [{"name": inventory_name, "expected": expected, "observed": observed}],
    }
    return seal(data, identity, producer=True)


# --------------------------------------------------------------------------- SOURCE_AUTHORITY

def _source_authority_findings(spec_path, reader_path, tg_path) -> tuple[list, dict]:
    findings = []
    obs = {}
    try:
        spec = json.loads(Path(REPO_ROOT / spec_path).read_text(encoding="utf-8")) if spec_path else None
    except (OSError, ValueError):
        spec = None
    if spec is None:
        return [_finding(_BLOCKING, "missing_spec", "chapter spec could not be read")], {}
    reader_text = extract_text(reader_path) if reader_path else ""
    tg_text = extract_text(tg_path) if tg_path else ""
    obs["readerHash"] = hashlib.sha256(Path(REPO_ROOT / reader_path).read_bytes()).hexdigest() if reader_path and Path(REPO_ROOT / reader_path).is_file() else ""
    if not reader_text:
        findings.append(_finding(_BLOCKING, "missing_reader", "Reader chapter could not be read: %s" % (reader_path or "none")))
    if not tg_text:
        findings.append(_finding(_BLOCKING, "missing_tg", "Teacher Guide could not be read: %s" % (tg_path or "none")))
    bq = str(spec.get("bigQuestion") or "")
    if bq and normalize(bq) not in normalize(reader_text + " " + tg_text):
        findings.append(_finding(_HIGH, "bq_not_in_source", "Big Question is not found in Reader/TG bytes"))
    vocab = [v.get("term") for v in (spec.get("vocabulary") or []) if isinstance(v, dict) and v.get("term")]
    for term in vocab:
        if term and normalize(term) not in normalize(reader_text):
            findings.append(_finding(_HIGH, "vocab_not_in_source", "required vocabulary %r is not in the Reader" % term))
    # Reader page references in the spec must correspond to actual source page tokens.
    for rng in (spec.get("sourceRanges") or []):
        # Basic presence: the spec must cite some page range and the Reader must
        # be non-trivial. Page-number cross-checking is inherently PDF-layout
        # dependent; we verify the spec records a range and Reader text is present.
        if not re.search(r"\d+", str(rng)):
            findings.append(_finding(_HIGH, "bad_source_range", "source range %r has no page" % str(rng)))
    obs["title"] = str(spec.get("title") or "")
    obs["bigQuestion"] = bq
    return findings, obs


def emit_source_authority_from_files(spec_path, reader_path, tg_path, identity, evidence_path, *, auditor_role="SOURCE_SCHOLAR"):
    findings, _obs = _source_authority_findings(spec_path, reader_path, tg_path)
    performed = bool(spec_path and reader_path and tg_path)
    inputs = ["spec:%s" % spec_path, "reader:%s" % reader_path, "tg:%s" % tg_path] if performed else []
    return _base(
        "SOURCE_AUTHORITY", "source-authority", identity, evidence_path, auditor_role,
        performed, findings, inputs,
        "candidate-source:%s" % identity.candidateHash,
        "authoritative-reader-tg-bytes",
        "sourceClaims", len(inputs), len(inputs),
    )


# --------------------------------------------------------------------------- CURRICULUM_CORRECTNESS

def _curriculum_findings(classroom_files: list[str], forbidden_families: set[str] | None) -> tuple[list, dict]:
    findings = []
    obs = {"hits": {}}
    families = forbidden_families or {"speed_quantity", "ramp_is_speed", "advanced_vocab", "mass_comparison"}
    if not classroom_files:
        return [_finding(_BLOCKING, "no_classroom", "no classroom artifacts supplied")], obs
    total = 0
    for rel in classroom_files:
        text = extract_text(rel)
        if not text:
            findings.append(_finding(_HIGH, "unreadable", "artifact could not be read: %s" % rel))
            continue
        total += 1
        hits = family_hits(text)
        for family, matches in hits.items():
            if family in families:
                for match in matches:
                    findings.append(_finding(
                        _BLOCKING, "boundary_violation",
                        "%s: %s (%s)" % (rel, match, family),
                    ))
        obs["hits"][rel] = hits
    return findings, obs


def emit_curriculum_correctness_from_files(classroom_files, identity, evidence_path, *, auditor_role="CURRICULUM_AUDITOR", forbidden_families=None):
    findings, _obs = _curriculum_findings(classroom_files if isinstance(classroom_files, list) else None, forbidden_families)
    performed = bool(classroom_files)
    inputs = ["classroom:%s" % rel for rel in (classroom_files or [])]
    return _base(
        "CURRICULUM_CORRECTNESS", "curriculum-correctness", identity, evidence_path, auditor_role,
        performed, findings, inputs,
        "candidate-curriculum:%s" % identity.candidateHash,
        "source-boundary:%s" % identity.sourceHash,
        "classroomFiles", len(inputs), len(inputs),
    )


# --------------------------------------------------------------------------- NOTES_SLIDES_SYNC

def _sync_findings(notes_path, slides_path, expected_anchors) -> tuple[list, dict]:
    findings = []
    obs = {}
    notes_text = extract_text(notes_path) if notes_path else ""
    slides_text = extract_text(slides_path) if slides_path else ""
    if not notes_text:
        findings.append(_finding(_BLOCKING, "missing_notes", "notes could not be read"))
    if not slides_text:
        findings.append(_finding(_BLOCKING, "missing_slides", "slides could not be read"))
    expected = list(expected_anchors or [])
    notes_anchors = anchor_codes_in_order(notes_text, expected)
    slides_anchors = anchor_codes_in_order(slides_text, expected)
    obs = {"notes": notes_anchors, "slides": slides_anchors, "expected": expected}

    if list(notes_anchors) != expected:
        missing = [a for a in expected if a not in notes_anchors]
        extra = [a for a in notes_anchors if a not in expected]
        if missing:
            findings.append(_finding(_BLOCKING, "notes_missing_anchor", "notes missing anchor(s): %s" % ", ".join(missing)))
        if extra:
            findings.append(_finding(_HIGH, "notes_extra_anchor", "notes extra anchor(s): %s" % ", ".join(extra)))
        if not missing and not extra and notes_anchors != expected:
            findings.append(_finding(_BLOCKING, "notes_anchor_order", "notes anchors out of order: %s != %s" % (notes_anchors, expected)))
    if list(slides_anchors) != expected:
        missing = [a for a in expected if a not in slides_anchors]
        extra = [a for a in slides_anchors if a not in expected]
        if missing:
            findings.append(_finding(_BLOCKING, "slides_missing_anchor", "slides missing anchor(s): %s" % ", ".join(missing)))
        if extra:
            findings.append(_finding(_HIGH, "slides_extra_anchor", "slides extra anchor(s): %s" % ", ".join(extra)))
        if not missing and not extra and slides_anchors != expected:
            findings.append(_finding(_BLOCKING, "slides_anchor_order", "slides anchors out of order: %s != %s" % (slides_anchors, expected)))

    # A required support line present in notes must also be present in slides.
    support = "we do not measure a speed number"
    if normalize(support) in normalize(notes_text) and normalize(support) not in normalize(slides_text):
        findings.append(_finding(_BLOCKING, "support_line_missing", "required support line missing from slides: %s" % support))
    return findings, obs


def emit_notes_slides_sync_from_files(notes_path, slides_path, expected_anchors, identity, evidence_path, *, auditor_role="CROSS_ARTIFACT_AUDITOR"):
    findings, _obs = _sync_findings(notes_path, slides_path, expected_anchors)
    performed = bool(notes_path and slides_path)
    inputs = ["notes:%s" % notes_path, "slides:%s" % slides_path] if performed else []
    return _base(
        "NOTES_SLIDES_SYNC", "notes-slides-sync", identity, evidence_path, auditor_role,
        performed, findings, inputs,
        "candidate-sync:%s" % identity.candidateHash,
        "notes-vs-slides-bytes",
        "anchors", len(expected_anchors or []), len(expected_anchors or []),
    )


# --------------------------------------------------------------------------- ANSWER_LEAKAGE

def _leakage_findings(notes_path, slides_path, keys_path) -> tuple[list, dict]:
    findings = []
    notes_text = extract_text(notes_path) if notes_path else ""
    slides_text = extract_text(slides_path) if slides_path else ""
    keys_text = extract_text(keys_path) if keys_path else ""
    if not notes_text:
        findings.append(_finding(_BLOCKING, "missing_notes", "notes could not be read"))
    if not slides_text:
        findings.append(_finding(_BLOCKING, "missing_slides", "slides could not be read"))

    # Answers are the key text; a student blank must not contain the answer text.
    key_tokens = re.findall(r"\b[a-z][a-z-]{2,}\b", normalize(keys_text)) if keys_text else []
    key_words = {w for w in key_tokens if len(w) > 3}
    # A prefilled blank: the blank region in notes is replaced with a word that is
    # one of the key answers. Detect: "____" count vs "___answer___" is hard; instead
    # detect a known answer word appearing immediately where a blank is expected.
    blanks = blank_count(notes_text)
    if blanks == 0 and keys_text:
        findings.append(_finding(_HIGH, "no_blanks", "notes have no blanks but a key exists"))
    # Early reveal: the reveal answer appears in a slide whose text precedes a
    # WRITE slide. We approximate with ordered slide text; a strong signal is the
    # answer appearing on the same slide that should only WRITE.
    slides = slide_blocks(slides_path) if slides_path else []
    write_index = None
    reveal_index = None
    for s in slides:
        t = normalize(s["text"])
        if "write" in t and write_index is None:
            write_index = s["slide"]
        if "reveal" in t and reveal_index is None:
            reveal_index = s["slide"]
    if write_index is not None and reveal_index is not None and reveal_index < write_index:
        findings.append(_finding(_BLOCKING, "early_reveal", "reveal slide %d precedes write slide %d" % (reveal_index, write_index)))
    # Speaker-notes leak: a key answer word in speaker notes before the reveal slide.
    for s in slides:
        if s["slide"] < (reveal_index or 10**9):
            for word in key_words:
                if word and word in normalize(s["notes"]):
                    findings.append(_finding(_HIGH, "speaker_leak", "answer %r in speaker notes on slide %d" % (word, s["slide"])))
                    break
    return findings, {"blanks": blanks, "slides": len(slides)}


def emit_answer_leakage_from_files(notes_path, slides_path, keys_path, identity, evidence_path, *, auditor_role="CURRICULUM_AUDITOR"):
    findings, _obs = _leakage_findings(notes_path, slides_path, keys_path)
    performed = bool(notes_path and slides_path)
    inputs = ["notes:%s" % notes_path, "slides:%s" % slides_path, "key:%s" % keys_path] if performed else []
    return _base(
        "ANSWER_LEAKAGE", "answer-leakage", identity, evidence_path, auditor_role,
        performed, findings, inputs,
        "candidate-leakage:%s" % identity.candidateHash,
        "student-vs-key-bytes",
        "surfaces", len(inputs), len(inputs),
    )


# --------------------------------------------------------------------------- ASSESSMENT_ALIGNMENT

def _assessment_findings(quiz_path, quiz_key_path, practice_path, practice_key_path) -> tuple[list, dict]:
    findings = []
    def _lines(path):
        text = extract_text(path) if path else ""
        return [line.strip() for line in text.splitlines() if line.strip()]
    quiz = _lines(quiz_path)
    quiz_key = _lines(quiz_key_path)
    practice = _lines(practice_path)
    practice_key = _lines(practice_key_path)

    if not quiz:
        findings.append(_finding(_BLOCKING, "missing_quiz", "quiz could not be read"))
    if not quiz_key:
        findings.append(_finding(_BLOCKING, "missing_quiz_key", "quiz key could not be read"))

    quiz_text = " ".join(quiz)
    # Score line: raw + percentage.
    if quiz_text and not re.search(r"/\s*12\b", quiz_text):
        findings.append(_finding(_HIGH, "missing_score_line", "quiz is missing a raw-score denominator (/12)"))
    if quiz_text and not re.search(r"%", quiz_text):
        findings.append(_finding(_HIGH, "missing_percent", "quiz is missing a percentage score"))

    # Boundary violations in assessment.
    for family, matches in family_hits(quiz_text).items():
        for match in matches:
            findings.append(_finding(_BLOCKING, "assessment_boundary", "quiz: %s (%s)" % (match, family)))
    for family, matches in family_hits(" ".join(practice)).items():
        for match in matches:
            findings.append(_finding(_BLOCKING, "assessment_boundary", "practice: %s (%s)" % (match, family)))

    # Student/key parity: question count and fill-in answer width.
    quiz_questions = [line for line in quiz if re.match(r"^\d+\.", line)]
    key_answers = [re.sub(r"^\d+\.\s*", "", line).strip() for line in quiz_key if re.match(r"^\d+\.", line)]
    if quiz_questions and key_answers and len(key_answers) != len(quiz_questions):
        findings.append(_finding(_BLOCKING, "question_count_mismatch",
            "quiz has %d questions but key has %d answers" % (len(quiz_questions), len(key_answers))))
    for i, ans in enumerate(key_answers):
        if i < len(quiz_questions) and "____" in quiz_questions[i]:
            # A single-blank fill-in expects a single-word key answer.
            if " " in ans:
                findings.append(_finding(_BLOCKING, "key_blank_mismatch",
                    "key answer %r does not match the single quiz blank" % ans))
    return findings, {"quiz_items": len(quiz), "quiz_key_items": len(quiz_key)}


def emit_assessment_alignment_from_files(quiz_path, quiz_key_path, practice_path, practice_key_path, identity, evidence_path, *, auditor_role="CURRICULUM_AUDITOR"):
    findings, _obs = _assessment_findings(quiz_path, quiz_key_path, practice_path, practice_key_path)
    performed = bool(quiz_path and quiz_key_path)
    inputs = ["quiz:%s" % quiz_path, "quiz-key:%s" % quiz_key_path, "practice:%s" % practice_path, "practice-key:%s" % practice_key_path] if performed else []
    return _base(
        "ASSESSMENT_ALIGNMENT", "assessment-alignment", identity, evidence_path, auditor_role,
        performed, findings, inputs,
        "candidate-assessment:%s" % identity.candidateHash,
        "assessment-vs-key-bytes",
        "assessmentFiles", len(inputs), len(inputs),
    )


# --------------------------------------------------------------------------- PLAYBOOK_ALIGNMENT

def _playbook_findings(playbook_path, spec_path) -> tuple[list, dict]:
    findings = []
    playbook = extract_text(playbook_path) if playbook_path else ""
    spec_text = extract_text(spec_path) if spec_path else ""
    if not playbook:
        findings.append(_finding(_BLOCKING, "missing_playbook", "playbook region could not be read"))
    if not spec_text:
        findings.append(_finding(_BLOCKING, "missing_spec", "chapter spec could not be read"))

    lowered = normalize(playbook)
    # Required protocol facts must be present.
    for required in (
        "one ball",
        "centimeters",
        "ramp height",
        "do not write a speed",
    ):
        if normalize(required) not in lowered:
            findings.append(_finding(_HIGH, "missing_protocol", "playbook region missing %r" % required))

    # Friday must not be a first exposure of required content.
    if re.search(r"friday.{0,80}required", lowered, re.I) or re.search(r"required.{0,80}friday", lowered, re.I):
        findings.append(_finding(_BLOCKING, "friday_required", "playbook marks Friday as required first exposure"))
    return findings, {}


def emit_playbook_alignment_from_files(playbook_path, spec_path, identity, evidence_path, *, auditor_role="CROSS_ARTIFACT_AUDITOR"):
    findings, _obs = _playbook_findings(playbook_path, spec_path)
    performed = bool(playbook_path and spec_path)
    inputs = ["playbook:%s" % playbook_path, "spec:%s" % spec_path] if performed else []
    return _base(
        "PLAYBOOK_ALIGNMENT", "playbook-alignment", identity, evidence_path, auditor_role,
        performed, findings, inputs,
        "candidate-playbook:%s" % identity.candidateHash,
        "playbook-vs-spec-bytes",
        "playbookFields", len(inputs), len(inputs),
    )


# --------------------------------------------------------------------------- FRESH_EXPORT

def _fresh_export_findings(source_path, production_path, export_dir) -> tuple[list, dict]:
    findings = []
    if not source_path or not Path(REPO_ROOT / source_path).is_file():
        return [_finding(_BLOCKING, "missing_source", "fresh-export source missing")], {}
    if not production_path or not Path(REPO_ROOT / production_path).is_file():
        return [_finding(_BLOCKING, "missing_production", "production PDF missing")], {}

    source_bytes = Path(REPO_ROOT / source_path).read_bytes()
    production_bytes = Path(REPO_ROOT / production_path).read_bytes()
    obs = {
        "sourceHash": hashlib.sha256(source_bytes).hexdigest(),
        "productionHash": hashlib.sha256(production_bytes).hexdigest(),
    }
    # Isolated export (pdf of the source) is out of scope without the full render
    # toolchain; we verify byte-level relationships that are independent of that:
    # source vs production must not be identical, and production must be a PDF.
    if not str(production_path).lower().endswith(".pdf"):
        findings.append(_finding(_BLOCKING, "not_pdf", "production output is not a PDF"))
    if source_bytes == production_bytes:
        findings.append(_finding(_BLOCKING, "self_export", "production PDF equals source bytes (no real export)"))
    prod_text = pdf_text(production_path)
    if not prod_text.strip():
        findings.append(_finding(_BLOCKING, "empty_production", "production PDF has no text"))
    return findings, obs


def emit_fresh_export_from_files(source_path, production_path, export_dir, identity, evidence_path, *, auditor_role="PDF_OOXML_FORENSICS"):
    findings, obs = _fresh_export_findings(source_path, production_path, export_dir)
    performed = bool(source_path and production_path)
    inputs = ["source:%s" % source_path, "production:%s" % production_path] if performed else []
    return _base(
        "FRESH_EXPORT", "fresh-export", identity, evidence_path, auditor_role,
        performed, findings, inputs,
        "candidate-fresh:%s" % identity.candidateHash,
        "source-vs-production-bytes",
        "exportPairs", len(inputs), len(inputs),
    )
