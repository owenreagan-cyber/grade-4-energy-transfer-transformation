"""STUDENT_PROMPT_CLARITY producer.

Student difficulty must come from the science, not from guessing what the prompt
means. This producer opens the actual student-facing files, extracts prompt-like
sentences, and flags vague or unscoped prompts. It never trusts caller-supplied
prompt text, classification, or evidence-reference booleans.
"""

from __future__ import annotations

import re

from chapter_qa.emit import seal
from chapter_qa.observation import read_any_text

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
    # "what happened" is vague only when it lacks a local explicit referent;
    # "What happened to the average cup movement?" names its referent.
    re.compile(r"\bwhat happened\b(?!\s+to\b)", re.I),
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

# Imperative openers that signal a student task prompt.
_PROMPT_OPENERS = (
    re.compile(r"^\s*(write|name|compare|explain|describe|circle|draw|measure|record|"
                r"infer|predict|label|complete|show|list|choose|read|find|tell|state)\b", re.I),
)

_QUESTION = re.compile(r"\?\s*$")


def _finding(code: str, message: str) -> dict:
    return {"severity": "HIGH", "code": code, "message": message}


def _classify(text: str) -> str | None:
    lowered = text.lower()
    if re.search(r"\b(claim|evidence|support)\b", lowered) and re.search(r"\b(your|two|value|average|data|table|graph)\b", lowered):
        return "CLAIM_EVIDENCE"
    if _DATA_TOKENS.search(lowered) and re.search(r"\b(which|what|read|how many|average)\b", lowered):
        return "READ_DATA"
    if re.search(r"\bcompare\b|\bvs\.?\b|\bversus\b", lowered) and re.search(r"\band\b|\bor\b", lowered):
        return "COMPARE"
    if re.search(r"\bexplain\b", lowered):
        return "EXPLAIN"
    if re.search(r"\baverage\b|\badd\b|\bsum\b|\bpercent\b", lowered):
        return "CALCULATE"
    if re.search(r"\bwhich|what|who\b", lowered):
        return "IDENTIFY"
    if re.search(r"\b(measure|record|observe|describe)\b", lowered):
        return "OBSERVE"
    return "RECALL"


def extract_prompts(files: list[dict]) -> list[dict]:
    """Open each student-facing file and derive prompt records from its text."""
    prompts = []
    for entry in files or []:
        if not isinstance(entry, dict):
            continue
        path = entry.get("path")
        artifact = str(entry.get("artifact") or "artifact")
        text = read_any_text(path) if path else ""
        if not text:
            continue
        for line in text.splitlines():
            candidate = line.strip()
            if len(candidate) < 6:
                continue
            is_question = bool(_QUESTION.search(candidate))
            is_imperative = any(o.search(candidate) for o in _PROMPT_OPENERS)
            if not (is_question or is_imperative):
                continue
            prompts.append({
                "artifact": artifact,
                "anchor": "",
                "text": candidate,
                "classification": _classify(candidate),
            })
    return prompts


def assess_prompts(prompts: list[dict] | None) -> list[dict]:
    if not isinstance(prompts, list) or not prompts:
        return [_finding("no_prompts", "no student-facing prompts were extracted")]
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


def emit_student_prompt_evidence(files, identity, evidence_path: str, *, auditor_role=None):
    """Open the actual student-facing files and derive prompts."""
    prompts = extract_prompts(files if isinstance(files, list) else None)
    findings = assess_prompts(prompts)
    count = len(prompts)
    failed = bool(findings)
    data = {
        "evidenceId": "student-prompt-clarity",
        "gateId": "STUDENT_PROMPT_CLARITY",
        "auditorRole": auditor_role or "CURRICULUM_AUDITOR",
        "performed": bool(files),
        "expectedInputs": ["student-files"] if files else [],
        "observedInputs": ["student-files"] if files and not failed else [],
        "thingBeingCertified": "candidate-prompts:%s" % identity.candidateHash,
        "independentEvidenceSource": "student-facing-text:%s" % identity.candidateHash,
        "findings": findings,
        "evidencePaths": [evidence_path],
        "failureReason": None,
        "notVerifiedReason": None,
        "invalidationReasons": [],
        "execution": {
            "succeeded": bool(files),
            "detectorException": False,
            "requiredInputsPresent": bool(files),
            "missingRender": False,
            "missingEvidence": not bool(files),
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
