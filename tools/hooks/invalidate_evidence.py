"""Dry-run edit invalidation.

Maps a changed path to the Phase A invalidation graph. It calls
`propagate` and `dependents`. It does not reimplement those rules
and it does not edit the file that changed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parents[1]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from chapter_qa.gates import load_gates
from chapter_qa.invalidation import dependents, propagate

from hooks.decisions import allow, deny, warn

_PRIORITY = {
    "GATE_VERSION_CHANGED": 0,
    "SOURCE_CHANGED": 1,
    "CANDIDATE_CHANGED": 1,
    "FREEZE_CHANGED": 1,
    "EXPECTED_INVENTORY_CHANGED": 1,
    "AUDITOR_VERSION_CHANGED": 1,
    "TOOL_VERSION_CHANGED": 1,
    "DEPENDENCY_CHANGED": 5,
}

_ARTIFACT_REASON = {
    "authoritative-source": "SOURCE_CHANGED",
    "notes": "CANDIDATE_CHANGED",
    "slides": "CANDIDATE_CHANGED",
    "assessment": "CANDIDATE_CHANGED",
    "schedule": "CANDIDATE_CHANGED",
    "playbook": "CANDIDATE_CHANGED",
    "release": "CANDIDATE_CHANGED",
    "inventory": "EXPECTED_INVENTORY_CHANGED",
    "freeze": "FREEZE_CHANGED",
}

# Detector file -> gates whose evidence that file can produce.
_DETECTOR_GATES = {
    "tools/qa_pdf_quality.py": ("PDF_QUALITY",),
    "tools/qa_ooxml.py": ("OOXML_FORENSICS",),
    "tools/qa_status_authority.py": ("STATUS_AUTHORITY",),
    "tools/qa_source_closure.py": ("SOURCE_CLOSURE",),
    "tools/qa_release_parity.py": ("RELEASE_PARITY",),
    "tools/chapter_qa/source_audit.py": ("SOURCE_AUTHORITY", "CURRICULUM_CORRECTNESS"),
    "tools/chapter_qa/cross_artifact.py": (
        "NOTES_STRUCTURE",
        "SLIDES_STRUCTURE",
        "NOTES_SLIDES_SYNC",
        "ASSESSMENT_ALIGNMENT",
        "PLAYBOOK_ALIGNMENT",
    ),
    "tools/chapter_qa/visual_qa.py": ("RENDERED_VISUAL_QA",),
    "tools/chapter_qa/render_completeness.py": ("RENDER_COMPLETENESS",),
    "tools/chapter_qa/schedule_policy.py": ("SCHEDULE_POLICY",),
    "tools/chapter_qa/release_set.py": ("RELEASE_EXACT_SET", "RELEASE_PARITY"),
    "tools/chapter_qa/provenance.py": ("SOURCE_CLOSURE", "PROVENANCE_INTEGRITY"),
    "tools/chapter_qa/clean_room.py": ("CLEAN_ROOM_REPRODUCTION",),
    "tools/chapter_qa/adversary.py": ("ADVERSARIAL_QA",),
}

_CONTRACT_FILES = frozenset({
    "tools/chapter_qa/evidence.py",
    "tools/chapter_qa/release_judge.py",
    "tools/chapter_qa/identity.py",
    "tools/chapter_qa/completeness.py",
    "tools/chapter_qa/gates.py",
    "tools/chapter_qa/invalidation.py",
    "tools/chapter_qa/emit.py",
    "tools/chapter_qa/lifecycle.py",
    "tools/chapter_qa/roles.py",
})


def normalize_path(path: str) -> str:
    text = str(path or "").replace("\\", "/")
    parts = []
    for part in text.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return "/".join(parts)


def classify_path(path: str) -> str | None:
    """Return an artifact class, 'gate-definition', 'detector', or None.

    Directory roles win over a substring such as ``note`` or ``quiz``.
    """
    name = normalize_path(path).lower()
    if not name:
        return None
    if name.startswith("docs/") and not name.endswith("gates.json"):
        return None
    if name.startswith("qa/reports/") or name.startswith("tools/hooks/"):
        return None
    if name.endswith("gates.json") or name.endswith("gate.schema.json"):
        return "gate-definition"
    if name.startswith("tools/chapter_qa/") or name.startswith("tools/qa_") or name.startswith("tools/certify_") or name.startswith("tools/run_adversarial"):
        return "detector"
    if name.startswith("assets/authoritative/"):
        return "authoritative-source"
    if name.startswith("production/releases/"):
        return "release"
    if name.startswith("production/premium-notes/") or "guided-notes" in name or name.endswith("-notes.docx"):
        return "notes"
    if name.startswith("production/slides/"):
        return "slides"
    if name.startswith("production/quizzes/") or name.startswith("production/worksheets/") or "answer-key" in name or "answer_key" in name:
        return "assessment"
    if "playbook" in name:
        return "playbook"
    if name.endswith("inventory.json") or "expected-inventory" in name:
        return "inventory"
    if any(token in name for token in ("schedule", "friday", "pacing")) and not name.startswith("docs/"):
        return "schedule"
    if "/freeze" in name or name.endswith("golden.json"):
        return "freeze"
    return None


def _merge(target: dict, source: dict) -> None:
    for gate_id, reason in source.items():
        current = target.get(gate_id)
        if current is None or _PRIORITY.get(reason, 9) < _PRIORITY.get(current, 9):
            target[gate_id] = reason


def _stamp_gate(affected: dict, gate_id: str, reason: str, gates) -> None:
    affected[gate_id] = reason
    for child in dependents(gate_id, gates):
        affected.setdefault(child, "DEPENDENCY_CHANGED")


def versions_from_gates(gates) -> dict:
    return {gate.gateId: gate.gateVersion for gate in gates}


def changed_versions(previous: dict, current: dict) -> dict:
    """gateId -> (old, new) for ids whose version text differs."""
    changed = {}
    for gate_id in set(previous) | set(current):
        old = previous.get(gate_id)
        new = current.get(gate_id)
        if old != new:
            changed[gate_id] = (old, new)
    return changed


def invalidate_versions(previous: dict, current: dict, gates) -> dict:
    affected = {}
    for gate_id in changed_versions(previous, current):
        _stamp_gate(affected, gate_id, "GATE_VERSION_CHANGED", gates)
    return affected


def _detector_ids(path: str, gates) -> tuple[str, ...]:
    name = normalize_path(path)
    if name in _CONTRACT_FILES:
        return tuple(gate.gateId for gate in gates)
    if name in _DETECTOR_GATES:
        return _DETECTOR_GATES[name]
    if name.startswith("tools/qa_") or name.startswith("tools/chapter_qa/") or name.startswith("tools/certify_") or name.startswith("tools/run_adversarial"):
        return tuple(gate.gateId for gate in gates)
    return ()


def invalidate_path(path: str, gates, previous_versions=None, current_versions=None) -> dict:
    kind = classify_path(path)
    if kind is None:
        return {}
    if kind == "gate-definition":
        if previous_versions is None or current_versions is None:
            raise ValueError("gate definition edit requires both version maps")
        return invalidate_versions(previous_versions, current_versions, gates)
    if kind == "detector":
        affected = {}
        for gate_id in _detector_ids(path, gates):
            _stamp_gate(affected, gate_id, "AUDITOR_VERSION_CHANGED", gates)
        return affected
    return propagate(kind, _ARTIFACT_REASON[kind], gates)


def _all_stale(gates) -> dict:
    affected = {}
    for gate in gates:
        _stamp_gate(affected, gate.gateId, "AUDITOR_VERSION_CHANGED", gates)
    return affected


def invalidate_edit(payload, gates=None) -> dict:
    """ALLOW the edit, and return the gates whose evidence is now stale.

    A failure marks every gate stale and WARNs. It does not block the edit
    and it does not rewrite the file.
    """
    try:
        chosen = tuple(gates) if gates is not None else load_gates()
    except Exception:
        return warn(
            "gate definitions unavailable; certification must fail closed",
            affected={},
            failClosed=True,
        )
    if not isinstance(payload, dict):
        return warn("malformed edit input; every gate treated as stale", affected=_all_stale(chosen))
    paths = payload.get("paths")
    if paths is None and payload.get("path"):
        paths = [payload.get("path")]
    if not isinstance(paths, list):
        return warn("malformed edit path; every gate treated as stale", affected=_all_stale(chosen))
    if not paths:
        return allow("no edited paths", affected={})
    previous = payload.get("previousGateVersions")
    current = payload.get("currentGateVersions")
    affected = {}
    try:
        for path in paths:
            if not isinstance(path, str):
                return warn("malformed edit path; every gate treated as stale", affected=_all_stale(chosen))
            _merge(affected, invalidate_path(path, chosen, previous, current))
    except Exception:
        return warn("invalidation failed closed; every gate treated as stale", affected=_all_stale(chosen))
    if not affected:
        return allow("path does not feed a certification gate", affected={})
    return allow("evidence invalidated", affected=affected)


def main(argv=None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Dry-run evidence invalidation. Does not edit files.")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    if args.apply:
        sys.stdout.write(json.dumps(deny("hook activation is refused; dry-run only")))
        return 2
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        result = invalidate_edit(payload)
    except Exception:
        result = warn("invalidation failed closed", affected={}, failClosed=True)
    sys.stdout.write(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
