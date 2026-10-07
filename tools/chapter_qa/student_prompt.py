"""STUDENT_PROMPT_CLARITY producer.

Student difficulty must come from the science, not from guessing what the prompt
means. This producer inspects student-facing prompt text (extracted from the
actual notes, practice, quiz, lab, and recovery files) and flags vague or
unscoped prompts. It derives observations from the supplied text; it never
compares a caller-supplied "expected" to itself.
"""

from __future__ import annotations

import re

from chapter_qa.emit import seal

PROMPT_CLASSES = (
    "RECALL",
    "IDENTIFY",
    "OBSERVE",
    "READ_DATA",
    "COMPARE",
    "CALCULATE",
    "CONNECT",
    "EXPLAIN",
    "CLAIM_EVIDENCE",
    "EXTEND",
)

# Vague referents: these make a prompt fail unless the referent is explicit.
_VAGUE_REFERENT = (
    re.compile(r"\bthat change\b", re.I),
    re.compile(r"\bthese results\b", re.I),
    re.compile(r"\bwhat happened\b", re.I),
    re.compile(r"\bthe relationship\b", re.I),
    re.compile(r"\binfer the\b", re.I),
    re.compile(r"\bwhat does this show\b", re.I),
    re.compile(r"\buse evidence\b", re.I),
    re.compile(r"\bexplain why\b\s*\.?\s*$", re.I),
    re.compile(r"\bexplain your thinking\b\s*\.?\s*$", re.I),
)

# Tokens that scope a READ_DATA prompt to an actual data source.
_DATA_TOKENS = re.compile(
    r"\b(table|graph|chart|data|average|column|row|axis|cell|value|values|"
    r"centimeter|cm|books?|trial|results of)\b",
    re.I,
)


def _finding(code: str, message: str) -> dict:
    return {"severity": "HIGH", "code": code, "message": message}


def assess_prompts(prompts: list[dict] | None) -> list[dict]:
    if not isinstance(prompts, list) or not prompts:
        return [_finding("no_prompts", "no student-facing prompts were supplied")]
    findings = []
    extend_count = 0
    for row in prompts:
        if not isinstance(row, dict):
            findings.append(_finding("bad_prompt", "a prompt is not a structured record"))
            continue
        text = str(row.get("text") or "").strip()
        classification = str(row.get("classification") or "").strip().upper()
        artifact = str(row.get("artifact") or "artifact")
        anchor = str(row.get("anchor") or "")
        where = "%s:%s" % (artifact, anchor or "?")

        if not text:
            findings.append(_finding("empty_prompt", "%s has empty prompt text" % where))
            continue
        if classification not in PROMPT_CLASSES:
            findings.append(_finding("unclassified", "%s has no valid classification (%r)" % (where, classification or "missing")))
            continue

        if classification == "EXTEND":
            extend_count += 1

        for pattern in _VAGUE_REFERENT:
            if pattern.search(text):
                findings.append(_finding(
                    "vague_referent",
                    "%s uses a vague referent: %r" % (where, text),
                ))
                break

        if classification == "READ_DATA" and not _DATA_TOKENS.search(text):
            findings.append(_finding("read_data_unscoped", "%s asks for data without naming the table/graph/values" % where))
        if classification == "COMPARE" and not re.search(r"\b(and|vs\.?|versus|to)\b", text, re.I):
            findings.append(_finding("compare_unscoped", "%s asks for a comparison without naming both things" % where))
        if classification == "EXPLAIN" and not re.search(r"\b(why|how|result|change|pattern|difference)\b", text, re.I):
            findings.append(_finding("explain_unscoped", "%s asks to explain without naming the result" % where))
        if classification == "CLAIM_EVIDENCE" and not re.search(r"\b(evidence|data|table|graph|value|values|average|observation)\b", text, re.I):
            findings.append(_finding("claim_unscoped", "%s asks for a claim with no evidence pointer" % where))

    if extend_count > 1:
        findings.append(_finding("too_many_extensions", "more than one final extension item (%d)" % extend_count))
    return findings


def emit_student_prompt_evidence(prompts, identity, evidence_path: str, *, auditor_role=None):
    findings = assess_prompts(prompts if isinstance(prompts, list) else None)
    count = len(prompts) if isinstance(prompts, list) else 0
    failed = bool(findings)
    data = {
        "evidenceId": "student-prompt-clarity",
        "gateId": "STUDENT_PROMPT_CLARITY",
        "auditorRole": auditor_role or "CURRICULUM_AUDITOR",
        "performed": bool(prompts),
        "expectedInputs": ["student-prompts"] if prompts else [],
        "observedInputs": ["student-prompts"] if prompts and not failed else [],
        "thingBeingCertified": "candidate-prompts:%s" % identity.candidateHash,
        "independentEvidenceSource": "student-facing-text:%s" % identity.candidateHash,
        "findings": findings,
        "evidencePaths": [evidence_path],
        "failureReason": None,
        "notVerifiedReason": None,
        "invalidationReasons": [],
        "execution": {
            "succeeded": bool(prompts),
            "detectorException": False,
            "requiredInputsPresent": bool(prompts),
            "missingRender": False,
            "missingEvidence": not bool(prompts),
            "stale": False,
            "gateSpecificFailure": failed,
            "unavailableEvidence": False,
        },
        "inventory": [{
            "name": "prompts",
            "expected": count if count else 0,
            "observed": count if count else 0,
        }],
    }
    return seal(data, identity, producer=True)
