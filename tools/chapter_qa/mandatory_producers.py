"""Producers for the nine gates that had no evidence source.

Each function checks a configured observation and calls seal(). None of them
assigns PASS. Empty configuration fails closed. Chapter 2 counts are not
the default for any other chapter.
"""

from __future__ import annotations

from chapter_qa.emit import seal

_SPEC_FIELDS = (
    "chapter",
    "title",
    "bigQuestion",
    "sourceRanges",
    "concepts",
    "exclusions",
    "vocabulary",
    "anchors",
    "schedule",
    "inventory",
)
_STATUSES = {"REQUIRED", "OPTIONAL", "FLEX"}


def _execution(present: bool, failed: bool) -> dict:
    return {
        "succeeded": present and not failed,
        "detectorException": False,
        "requiredInputsPresent": present,
        "missingRender": False,
        "missingEvidence": not present,
        "stale": False,
        "gateSpecificFailure": failed,
        "unavailableEvidence": False,
    }


def _finish(gate_id, role, identity, evidence_path, name, expected, observed, findings, inputs):
    present = bool(inputs) and expected is not None
    failed = bool(findings) or not present
    data = {
        "evidenceId": "%s-producer" % gate_id.lower(),
        "gateId": gate_id,
        "auditorRole": role,
        "performed": present,
        "expectedInputs": inputs if present else [],
        "observedInputs": inputs if present and not failed else [],
        "thingBeingCertified": "candidate-%s:%s" % (gate_id.lower(), identity.candidateHash),
        "independentEvidenceSource": "producer-observation:%s" % gate_id.lower(),
        "findings": findings,
        "evidencePaths": [evidence_path],
        "failureReason": None,
        "notVerifiedReason": None,
        "invalidationReasons": [],
        "execution": _execution(present, failed),
        "inventory": [{"name": name, "expected": expected if present else 0, "observed": observed if present else 0}],
    }
    return seal(data, identity, producer=True)


def _safe(func, *args):
    try:
        return func(*args)
    except Exception:
        return [_finding("bad_input", "producer input could not be read")]


def _finding(code: str, message: str) -> dict:
    return {"severity": "HIGH", "code": code, "message": message}


def _blank(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, list):
        return not value or all(_blank(item) for item in value)
    if isinstance(value, dict):
        return not value
    return False


def assess_chapter_spec(spec: dict | None) -> list[dict]:
    if not isinstance(spec, dict) or not spec:
        return [_finding("empty_spec", "chapter spec is empty")]
    findings = []
    for field in _SPEC_FIELDS:
        if _blank(spec.get(field)):
            findings.append(_finding("missing_field", "spec is missing %s" % field))
    anchors = spec.get("anchors")
    if not isinstance(anchors, list):
        anchors = []
    codes = []
    orders = []
    for row in anchors:
        if not isinstance(row, dict):
            findings.append(_finding("duplicate_anchor", "anchor is not a structured record"))
            continue
        codes.append(str(row.get("code") or "").strip())
        if not isinstance(row.get("order"), int):
            findings.append(_finding("anchor_order", "anchor order is missing"))
        else:
            orders.append(row.get("order"))
        if row.get("status") not in _STATUSES:
            findings.append(_finding("unknown_status", "anchor status is not REQUIRED, OPTIONAL, or FLEX"))
    if len(codes) != len(set(codes)) or any(not code for code in codes):
        findings.append(_finding("duplicate_anchor", "anchor code is missing or repeated"))
    if orders and orders != sorted(orders):
        findings.append(_finding("anchor_order", "anchors are out of order"))
    if _blank(spec.get("sourceRanges")):
        findings.append(_finding("missing_source", "spec has no Reader or Teacher Guide range"))
    if spec.get("chapter") is not None and spec.get("identityChapter") not in (None, spec.get("chapter")):
        findings.append(_finding("identity_conflict", "spec chapter does not match the candidate identity"))
    return findings


def emit_chapter_spec(spec, identity, evidence_path):
    findings = _safe(assess_chapter_spec, spec if isinstance(spec, dict) else None)
    count = len((spec or {}).get("anchors") or []) if isinstance(spec, dict) else 0
    return _finish(
        "CHAPTER_SPEC", "CURRICULUM_AUDITOR", identity, evidence_path,
        "specFields", len(_SPEC_FIELDS), len(_SPEC_FIELDS) - sum(1 for item in findings if item["code"] == "missing_field"),
        findings, ["chapter-spec"] if spec else [],
    )


def assess_notes(expected: dict | None, observed: dict | None) -> list[dict]:
    if not expected or not observed:
        return [_finding("missing_expectations", "notes structure has no configured expectation or observation")]
    findings = []
    if expected.get("pageCount") != observed.get("pageCount"):
        findings.append(_finding("page_count", "notes page count does not match the spec"))
    if list(expected.get("anchors") or []) != list(observed.get("anchors") or []):
        findings.append(_finding("anchor_order", "notes anchors are missing, duplicated, or out of order"))
    if list(expected.get("vocabulary") or []) != list(observed.get("vocabulary") or []):
        findings.append(_finding("vocabulary", "notes vocabulary groups do not match the spec"))
    if expected.get("blankCount") != observed.get("blankCount"):
        findings.append(_finding("blanks", "notes blank count does not match the spec"))
    if expected.get("answerKey") != observed.get("answerKey"):
        findings.append(_finding("answer_key", "notes are not paired with the configured answer key"))
    if observed.get("writingSpace") is False:
        findings.append(_finding("writing_space", "a required writing region is missing"))
    for term in expected.get("forbidden") or []:
        if term and term in " ".join(observed.get("text") or []):
            findings.append(_finding("forbidden_term", "notes contain a forbidden architecture term"))
            break
    if observed.get("secondSystem") is True:
        findings.append(_finding("second_system", "a second note system is present"))
    if not observed.get("candidateHash"):
        findings.append(_finding("identity", "notes observation has no candidate hash"))
    return findings


def emit_notes_structure(expected, observed, identity, evidence_path):
    findings = _safe(assess_notes, expected, observed)
    return _finish(
        "NOTES_STRUCTURE", "CROSS_ARTIFACT_AUDITOR", identity, evidence_path,
        "noteAnchors", len((expected or {}).get("anchors") or []), len((observed or {}).get("anchors") or []),
        findings, ["notes-structure"] if expected and observed else [],
    )


def assess_slides(expected: dict | None, observed: dict | None) -> list[dict]:
    if not expected or not observed:
        return [_finding("missing_expectations", "slides structure has no configured expectation or observation")]
    findings = []
    if expected.get("slideCount") != observed.get("slideCount"):
        findings.append(_finding("slide_count", "slide count does not match the spec"))
    if list(expected.get("anchors") or []) != list(observed.get("anchors") or []):
        findings.append(_finding("anchor_order", "slide anchors are missing or out of order"))
    if list(expected.get("vocabulary") or []) != list(observed.get("vocabulary") or []):
        findings.append(_finding("vocabulary", "slide vocabulary groups do not match the spec"))
    required_notes = set(expected.get("speakerNotes") or [])
    if not required_notes.issubset(set(observed.get("speakerNotes") or [])):
        findings.append(_finding("speaker_notes", "a required speaker note is missing"))
    if expected.get("planStatus") and observed.get("planStatus") is not True:
        findings.append(_finding("plan_status", "slide plan or status structure is missing"))
    if observed.get("uncodedAnswer") is True:
        findings.append(_finding("uncoded_answer", "an uncoded slide carries a required note answer"))
    if not observed.get("candidateHash"):
        findings.append(_finding("identity", "slides observation has no candidate hash"))
    return findings


def emit_slides_structure(expected, observed, identity, evidence_path):
    findings = _safe(assess_slides, expected, observed)
    return _finish(
        "SLIDES_STRUCTURE", "CROSS_ARTIFACT_AUDITOR", identity, evidence_path,
        "slideAnchors", len((expected or {}).get("anchors") or []), len((observed or {}).get("anchors") or []),
        findings, ["slides-structure"] if expected and observed else [],
    )


def assess_leakage(sequence: list[dict] | None) -> list[dict]:
    """Reveal order comes from the anchor sequence, not from a keyword list."""
    if not sequence:
        return [_finding("missing_sequence", "answer leakage has no anchor sequence")]
    findings = []
    written = set()
    allowed = {"slide", "speaker", "student", "uncoded"}
    for step in sequence:
        if not isinstance(step, dict):
            findings.append(_finding("bad_step", "a reveal step is not a structured record"))
            continue
        kind = str(step.get("kind") or "").strip().lower()
        anchor = step.get("anchor") or ""
        reveals = set(step.get("reveals") or [])
        writes = set(step.get("writes") or [])
        if kind not in allowed:
            findings.append(_finding("bad_step", "anchor %s has no known surface kind" % anchor))
        early = reveals - written
        if early:
            findings.append(_finding("early_reveal", "anchor %s reveals %s before the write step" % (anchor, ", ".join(sorted(map(str, early))))))
        if kind == "student" and step.get("prefilled"):
            findings.append(_finding("prefilled_blank", "student anchor %s is not blank" % anchor))
        if kind == "uncoded" and (reveals or step.get("prefilled")):
            findings.append(_finding("uncoded_answer", "uncoded surface carries a required answer"))
        written |= writes
    return findings


def emit_answer_leakage(sequence, identity, evidence_path):
    findings = _safe(assess_leakage, sequence if isinstance(sequence, list) else None)
    count = len(sequence) if isinstance(sequence, list) else 0
    return _finish(
        "ANSWER_LEAKAGE", "CURRICULUM_AUDITOR", identity, evidence_path,
        "revealSteps", count, count, findings, ["answer-sequence"] if sequence else [],
    )


def assess_fresh(pairs: list[dict] | None) -> list[dict]:
    if not pairs:
        return [_finding("no_pairs", "fresh export has no configured source and output pair")]
    findings = []
    for pair in pairs:
        if not isinstance(pair, dict):
            findings.append(_finding("bad_pair", "a fresh-export pair is not a structured record"))
            continue
        label = pair.get("label") or "pair"
        for key in ("pageCount", "expectedPageCount", "dimensions", "expectedDimensions", "normalizedText", "freshText"):
            if key not in pair or _blank(pair.get(key) if isinstance(pair.get(key), str) else None) and pair.get(key) in (None, ""):
                findings.append(_finding("missing_hash", "%s is missing %s" % (label, key)))
                break
        if pair.get("sourceHash") in (None, "") or pair.get("outputHash") in (None, "") or pair.get("freshHash") in (None, ""):
            findings.append(_finding("missing_hash", "%s is missing a source, output, or fresh hash" % label))
            continue
        if pair.get("outputHash") != pair.get("freshHash"):
            findings.append(_finding("stale_export", "%s output does not match a fresh export" % label))
        if pair.get("pageCount") != pair.get("expectedPageCount"):
            findings.append(_finding("page_count", "%s page count does not match the fresh export" % label))
        if pair.get("dimensions") != pair.get("expectedDimensions"):
            findings.append(_finding("dimensions", "%s page size does not match the fresh export" % label))
        if pair.get("normalizedText") != pair.get("freshText"):
            findings.append(_finding("text_mismatch", "%s text does not match the fresh export" % label))
    return findings


def emit_fresh_export(pairs, identity, evidence_path):
    findings = _safe(assess_fresh, pairs if isinstance(pairs, list) else None)
    count = len(pairs) if isinstance(pairs, list) else 0
    return _finish(
        "FRESH_EXPORT", "PDF_OOXML_FORENSICS", identity, evidence_path,
        "exportPairs", count, count, findings, ["fresh-export"] if pairs else [],
    )


def assess_retired(files: list[dict] | None, baselines: list[dict] | None) -> list[dict]:
    if not baselines:
        return [_finding("no_baseline", "retired content has no chapter baseline")]
    if files is None:
        return [_finding("no_files", "retired content has no observed files")]
    tokens = []
    hashes = set()
    for item in baselines:
        if not isinstance(item, dict) or not isinstance(item.get("token"), str) or not item.get("token").strip():
            return [_finding("bad_baseline", "a retired baseline is not usable")]
        tokens.append("".join(item["token"].lower().split()))
        if item.get("perceptualHash"):
            hashes.add(item["perceptualHash"])
    findings = []
    for item in files:
        name = item.get("name") or "file"
        text = "".join(str(item.get("text") or "").lower().replace("\u200b", "").split())
        folded_name = "".join(name.lower().split())
        for token in tokens:
            if token in text or token in folded_name:
                findings.append(_finding("retired_text", "%s contains retired baseline %s" % (name, token)))
                break
        if item.get("perceptualHash") and item.get("perceptualHash") in hashes:
            findings.append(_finding("retired_raster", "%s matches a retired page baseline" % name))
    return findings


def emit_retired_content(files, baselines, identity, evidence_path):
    findings = _safe(assess_retired, files if isinstance(files, list) else None, baselines if isinstance(baselines, list) else None)
    count = len(files) if isinstance(files, list) else 0
    return _finish(
        "RETIRED_CONTENT", "PROVENANCE_AUDITOR", identity, evidence_path,
        "retiredFiles", count, count, findings, ["retired-baseline"] if baselines else [],
    )


def assess_inventory(expected: list[str] | None, observed: list[str] | None) -> list[dict]:
    if not expected:
        return [_finding("empty_expected", "inventory expectation is missing or empty")]
    if observed is None:
        return [_finding("missing_observed", "inventory observation is missing")]
    findings = []
    expected_set = set(expected)
    observed_set = set(observed)
    for name in sorted(expected_set - observed_set):
        findings.append(_finding("missing_file", "required inventory file %s is missing" % name))
    if len(expected) != len(observed):
        findings.append(_finding("count_mismatch", "expected inventory count does not match the observation"))
    return findings


def emit_inventory(expected, observed, identity, evidence_path):
    findings = _safe(assess_inventory, expected if isinstance(expected, list) else None, observed if isinstance(observed, list) else None)
    return _finish(
        "INVENTORY", "CROSS_ARTIFACT_AUDITOR", identity, evidence_path,
        "inventoryFiles", len(expected) if isinstance(expected, list) else 0,
        len(observed) if isinstance(observed, list) else 0,
        findings, ["inventory"] if expected else [],
    )


def assess_adversarial(summary: dict | None) -> list[dict]:
    if not summary:
        return [_finding("not_run", "adversarial suite did not run")]
    if "cleanControls" not in summary and "clean" in summary:
        summary = dict(summary)
        summary["cleanControls"] = summary["clean"]
    required = (
        "projectBad", "projectBadGreen", "heldOutBad", "heldOutGreen",
        "cleanControls", "cleanRed", "canonicalRepoTouched", "completed",
    )
    findings = []
    for key in required:
        if key not in summary:
            findings.append(_finding("incomplete", "adversarial summary is missing %s" % key))
    if findings:
        return findings
    if summary.get("completed") is not True:
        findings.append(_finding("incomplete", "adversarial execution did not finish"))
    if summary.get("projectBadGreen") not in (0,):
        findings.append(_finding("escaped", "a project mutation was not caught"))
    if summary.get("heldOutGreen") not in (0,):
        findings.append(_finding("held_out_escaped", "a held-out mutation was not caught"))
    if summary.get("cleanRed") not in (0,):
        findings.append(_finding("clean_red", "a clean control was failed"))
    if summary.get("canonicalRepoTouched") not in (False, 0):
        findings.append(_finding("canonical_touched", "the adversarial run touched the canonical tree"))
    if not summary.get("projectBad") or not summary.get("heldOutBad") or not summary.get("cleanControls"):
        findings.append(_finding("incomplete", "project, held-out, or clean controls were not executed"))
    return findings


def emit_adversarial_qa(summary, identity, evidence_path):
    findings = _safe(assess_adversarial, summary if isinstance(summary, dict) else None)
    count = int((summary or {}).get("projectBad") or 0) if isinstance(summary, dict) else 0
    return _finish(
        "ADVERSARIAL_QA", "QA_ADVERSARY", identity, evidence_path,
        "mutations", count, count, findings, ["adversarial-suite"] if summary else [],
    )


_FROZEN_KEYS = ("guard", "unreviewed", "stale", "parity", "churn")


def assess_prior_frozen(chapters: dict | None) -> list[dict]:
    if not chapters:
        return [_finding("no_chapters", "no previously frozen chapter was checked")]
    findings = []
    for chapter, observed in chapters.items():
        if not isinstance(observed, dict) or any(key not in observed for key in _FROZEN_KEYS):
            findings.append(_finding("incomplete", "frozen chapter %s is missing a required check" % chapter))
            continue
        if observed.get("unreviewed") != 0 or observed.get("stale") != 0 or observed.get("churn") != 0:
            findings.append(_finding("frozen_change", "frozen chapter %s changed or has unreviewed clauses" % chapter))
        expected_guard = observed.get("guardExpected")
        expected_parity = observed.get("parityExpected")
        if not isinstance(expected_guard, str) or not expected_guard.strip() or observed.get("guard") != expected_guard:
            findings.append(_finding("guard", "frozen chapter %s guard did not match" % chapter))
        if not isinstance(expected_parity, str) or not expected_parity.strip() or observed.get("parity") != expected_parity:
            findings.append(_finding("parity", "frozen chapter %s parity did not match" % chapter))
    return findings


def emit_prior_frozen(chapters, identity, evidence_path):
    findings = _safe(assess_prior_frozen, chapters if isinstance(chapters, dict) else None)
    count = len(chapters) if isinstance(chapters, dict) else 0
    return _finish(
        "PRIOR_FROZEN_NONREGRESSION", "PROVENANCE_AUDITOR", identity, evidence_path,
        "frozenChapters", count, count, findings, ["frozen-chapters"] if chapters else [],
    )
