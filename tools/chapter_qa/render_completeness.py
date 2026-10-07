"""Expected render inventory versus observed renders.

Contact sheets are navigation aids. They are not page evidence.
"""

from __future__ import annotations

from pathlib import Path

from chapter_qa.emit import seal
from chapter_qa.evidence import REPO_ROOT
from chapter_qa.severity import resolve_severity


def _key(item: dict) -> tuple:
    return (item.get("artifactId"), item.get("pageOrSlide"))


def _render_path_ok(path: str) -> bool:
    if not path:
        return False
    relative = Path(str(path))
    if relative.is_absolute() or ".." in relative.parts:
        return False
    return (REPO_ROOT / relative).is_file()


def assess_renders(expected: list[dict], observed: list[dict], *, command_failed=False, output_empty=False, candidate_hash=None) -> dict:
    findings = []
    fails = False
    instructional = [item for item in observed if not item.get("navigation")]
    codes = []

    def add(code, message, context=None):
        nonlocal fails
        decision = resolve_severity(code, context)
        findings.append({"severity": decision["severity"], "code": code, "message": message})
        if decision["failsGate"]:
            fails = True
        codes.append(code)

    if command_failed:
        add("missing_required_render", "render command failed")
    if not expected:
        add("missing_required_render", "no expected render inventory was declared")
    if output_empty or (expected and not instructional):
        add("missing_required_render", "render output directory has no instructional pages")

    seen = {}
    for item in instructional:
        key = _key(item)
        if key in seen:
            add("missing_required_render", "duplicate render index %s page %s" % key)
        seen[key] = item

    expected_keys = {_key(item) for item in expected}
    observed_keys = set(seen)
    for key in sorted(expected_keys - observed_keys):
        add("missing_required_render", "missing render %s page %s" % key)
    for key in sorted(observed_keys - expected_keys):
        add("missing_required_render", "unexpected render %s page %s" % key)
    for item in expected:
        found = seen.get(_key(item))
        if not found:
            continue
        if candidate_hash is not None and item.get("artifactHash") != candidate_hash:
            add("missing_required_render", "expected render %s page %s is not this candidate" % _key(item))
        if found.get("artifactHash") != item.get("artifactHash"):
            add("missing_required_render", "render %s page %s came from a different artifact hash" % _key(item))
        if not found.get("renderPath") or not found.get("renderHash"):
            add("missing_required_render", "render %s page %s has no render identity" % _key(item))
        elif not _render_path_ok(found.get("renderPath")):
            add("missing_required_render", "render file %s is missing" % found.get("renderPath"))
    paths = [item.get("renderPath") for item in instructional]
    if len(paths) != len(set(paths)):
        add("missing_required_render", "render pages do not have distinct files")
    return {
        "findings": findings,
        "failsGate": fails or bool(codes),
        "expectedCount": len(expected),
        "observedCount": len(instructional),
        "commandFailed": command_failed,
        "outputEmpty": output_empty or (bool(expected) and not instructional),
    }


def emit_render_evidence(expected, observed, identity, evidence_path: str, *, command_failed=False, output_empty=False, auditor_role=None):
    assessed = assess_renders(
        expected, observed, command_failed=command_failed, output_empty=output_empty,
        candidate_hash=identity.candidateHash,
    )
    instructional = [item for item in observed if not item.get("navigation")]
    render_hash = instructional[0].get("renderHash") if instructional else "none"
    names = ["%s:%s" % _key(item) for item in expected]
    data = {
        "evidenceId": "render-completeness",
        "gateId": "RENDER_COMPLETENESS",
        "auditorRole": auditor_role,
        "performed": True,
        "expectedInputs": names,
        "observedInputs": names if assessed["expectedCount"] and assessed["expectedCount"] == assessed["observedCount"] and not assessed["failsGate"] else [],
        "thingBeingCertified": "candidate-artifacts:%s" % identity.candidateHash,
        "independentEvidenceSource": "rendered-pages:%s" % render_hash,
        "findings": assessed["findings"],
        "evidencePaths": [evidence_path],
        "failureReason": None,
        "notVerifiedReason": None,
        "invalidationReasons": [],
        "execution": {
            "succeeded": not command_failed and not assessed["outputEmpty"],
            "detectorException": command_failed,
            "requiredInputsPresent": bool(expected) and not assessed["outputEmpty"],
            "missingRender": assessed["outputEmpty"] or command_failed or assessed["expectedCount"] != assessed["observedCount"],
            "missingEvidence": assessed["outputEmpty"],
            "stale": False,
            "gateSpecificFailure": assessed["failsGate"],
            "unavailableEvidence": False,
        },
        "inventory": [{
            "name": "renders",
            "expected": assessed["expectedCount"],
            "observed": 0 if assessed["outputEmpty"] else assessed["observedCount"],
        }],
    }
    if not expected:
        data["expectedInputs"] = []
        data["observedInputs"] = []
    return seal(data, identity, producer=True)
