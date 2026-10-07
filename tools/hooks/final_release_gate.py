"""Dry-run stop hook for certification claims.

Ordinary work is allowed without a Release Judge result. A claim that
the chapter is ready, certified, approved for freeze, or frozen is
allowed only when `judge()` returns PASS and the lifecycle rules for
that claim hold.

The hook never trusts a status or judgment object supplied by the caller.
It does not write evidence, freeze a chapter, or issue certification text.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parents[1]
_REPO = _TOOLS.parent
_WORK = (_REPO / "qa" / "work").resolve()
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from chapter_qa.evidence import evidence_from_dict
from chapter_qa.gates import default_release_gates, gate_by_id, load_gates
from chapter_qa.lifecycle import legal_transition
from chapter_qa.release_judge import judge as release_judge

from hooks.decisions import allow, deny
from hooks.invalidate_evidence import invalidate_edit
from hooks.validate_evidence import identity_from_payload

ORDINARY = frozenset({"show_failures", "build_draft", "ordinary"})
CERT_ACTIONS = frozenset({
    "chapter_ready",
    "internally_certified",
    "release_ready",
    "ready_for_external_audit",
    "approved_for_freeze",
    "freeze_chapter",
})

# Longer phrases first so "ready for freeze" is not halved.
_PHRASES = (
    ("ready for external audit", "ready_for_external_audit"),
    ("approved for freeze", "approved_for_freeze"),
    ("approved_for_freeze", "approved_for_freeze"),
    ("internally certified", "internally_certified"),
    ("internally_certified", "internally_certified"),
    ("ready for freeze", "freeze_chapter"),
    ("freeze chapter", "freeze_chapter"),
    ("chapter ready", "chapter_ready"),
    ("release ready", "release_ready"),
    ("chapter is frozen", "freeze_chapter"),
    ("status is frozen", "freeze_chapter"),
    ("internal release certification", "chapter_ready"),
    ("this build is certified", "chapter_ready"),
    ("build is certified", "chapter_ready"),
    ("build certified", "chapter_ready"),
    ("froze the chapter", "freeze_chapter"),
    ("i've frozen", "freeze_chapter"),
    ("i have frozen", "freeze_chapter"),
    ("now frozen", "freeze_chapter"),
    ("ready to freeze", "freeze_chapter"),
)


def _normalize_message(text: str) -> str:
    text = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", text)
    return re.sub(r"\s+", " ", text.lower()).strip()


def _negated(window: str) -> bool:
    window = re.sub(r"\bnot only\b", "", window)
    clause = re.split(r"[,.!;]", window)[-1]
    return re.search(r"\b(not|never|don't|do not|isn't|is not|cannot|can't)\b", clause) is not None


def _asserts_phrase(lowered: str, phrase: str) -> bool:
    """True when the phrase is present and not negated in the preceding words."""
    start = 0
    while True:
        at = lowered.find(phrase, start)
        if at < 0:
            return False
        window = lowered[max(0, at - 80):at]
        after = lowered[at + len(phrase):at + len(phrase) + 24]
        if re.search(r"\b(fail|failed|failure)\b", after):
            start = at + len(phrase)
            continue
        if not _negated(window):
            return True
        start = at + len(phrase)


def message_asserts_certification(payload: dict) -> bool:
    message = payload.get("message", "")
    if not isinstance(message, str) or not message:
        return False
    return classify_action({"message": message}) != "ordinary"


def classify_action(payload: dict) -> str:
    action = payload.get("requestedAction")
    if isinstance(action, str) and action:
        if action in ORDINARY:
            return "ordinary"
        if action in CERT_ACTIONS:
            return action
        return "malformed"
    message = payload.get("message", "")
    if message is None:
        message = ""
    if not isinstance(message, str):
        return "malformed"
    lowered = _normalize_message(message)
    for phrase, name in _PHRASES:
        if _asserts_phrase(lowered, phrase):
            return name
    return "ordinary"


def _load_records(payload, gates):
    """Load evidence JSON from the directory. A caller-supplied list is ignored."""
    directory = Path(payload.get("evidenceDirectory") or "")
    files = sorted(path for path in directory.glob("*.json") if path.is_file())
    files = [path for path in files if path.name != "lifecycle.json"]
    if not files:
        raise ValueError("no evidence files")
    records = []
    for path in files:
        row = json.loads(path.read_text(encoding="utf-8"))
        record = evidence_from_dict(row)
        gate_by_id(gates, record.gateId)
        if _design_source(record.independentEvidenceSource):
            raise ValueError("design server state is not independent evidence")
        records.append(record)
    return records


def _design_source(source: str) -> bool:
    raw = (source or "").lower()
    text = re.sub(r"[\s_-]+", " ", raw)
    compact = re.sub(r"[\s_-]+", "", raw)
    if any(marker in text for marker in ("figma", "canva", "design server")):
        return True
    return any(marker in compact for marker in ("figma", "canva", "designserver"))


def _inside_work(path: Path) -> bool:
    resolved = path.resolve()
    return resolved == _WORK or _WORK in resolved.parents


def _read_lifecycle(payload, identity) -> dict:
    path = payload.get("lifecyclePath")
    if not isinstance(path, str) or not path.strip():
        raise ValueError("lifecycle record missing")
    life = Path(path)
    evidence_dir = Path(payload.get("evidenceDirectory") or "")
    if not _inside_work(life) or evidence_dir.resolve() not in life.resolve().parents:
        raise ValueError("lifecycle record is outside the evidence directory")
    data = json.loads(life.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("lifecycle record malformed")
    if data.get("buildId") != identity.buildId:
        raise ValueError("lifecycle build mismatch")
    claimed = payload.get("lifecycleState")
    if claimed is not None and claimed != data.get("state"):
        raise ValueError("lifecycle mismatch")
    return data


def decide_stop(payload, judge_fn=None, gates=None) -> dict:
    """ALLOW or DENY a final response. Certification failures deny."""
    if not isinstance(payload, dict):
        return deny("malformed hook input")
    action = classify_action(payload)
    if action == "malformed":
        return deny("malformed hook input")
    if payload.get("timedOut") is True and action != "ordinary":
        return deny("hook timed out before certification could be checked")
    if action == "ordinary":
        if message_asserts_certification(payload):
            return deny("certification claim contradicts the ordinary action")
        return allow("ordinary work does not require certification")
    if payload.get("invalidationFailClosed") is True or payload.get("failClosed") is True:
        return deny("invalidation failed closed")
    if payload.get("dependencyMissing") is True or judge_fn is False:
        return deny("enforcement dependency unavailable")
    edited = payload.get("editedPaths")
    if not isinstance(edited, list) or any(not isinstance(item, str) for item in edited):
        return deny("edited paths missing")
    invalidation = invalidate_edit({"paths": edited})
    if invalidation.get("failClosed") is True:
        return deny("invalidation failed closed")
    computed = invalidation.get("affected") or {}
    supplied = payload.get("affected")
    if supplied is not None and supplied != computed:
        return deny("invalidation map does not match the edited paths")
    directory = payload.get("evidenceDirectory")
    if not isinstance(directory, str) or not directory.strip():
        return deny("evidence directory unavailable")
    directory_path = Path(directory)
    if not directory_path.is_dir() or not _inside_work(directory_path):
        return deny("evidence directory unavailable")
    try:
        chosen = tuple(gates) if gates is not None else load_gates()
        release_gates = default_release_gates(chosen)
        if not release_gates:
            return deny("no required gate definition")
        identity = identity_from_payload(payload.get("build"))
        records = _load_records(payload, chosen)
        runner = release_judge if judge_fn is None else judge_fn
        result = runner(release_gates, records, identity, computed)
    except Exception:
        return deny("release judge failed closed")
    if getattr(result, "status", None) != "PASS":
        return deny("release judge did not pass")
    needs_lifecycle = action in {"ready_for_external_audit", "approved_for_freeze", "freeze_chapter"}
    if needs_lifecycle:
        try:
            recorded = _read_lifecycle(payload, identity)
        except Exception:
            return deny("lifecycle record rejected")
        state = recorded.get("state")
        if action == "ready_for_external_audit" and state != "INTERNALLY_CERTIFIED":
            return deny("external audit requires an internally certified lifecycle state")
        if action == "approved_for_freeze":
            if state != "EXTERNAL_AUDIT_PENDING" or recorded.get("externalAuditAccepted") is not True:
                return deny("approved for freeze requires external authorization")
        if action == "freeze_chapter":
            if payload.get("ownerAuthorizedFreeze") is not True:
                return deny("freeze requires owner authorization")
            if recorded.get("externalAuditAccepted") is not True:
                return deny("freeze requires external authorization")
            if not legal_transition(state or "", "FROZEN"):
                return deny("freeze is not a legal transition")
    return allow("release judge passed for %s" % action)


def main(argv=None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Dry-run certification stop gate.")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    if args.apply:
        sys.stdout.write(json.dumps(deny("hook activation is refused; dry-run only")))
        return 2
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        result = decide_stop(payload)
    except Exception:
        result = deny("certification hook failed closed")
    sys.stdout.write(json.dumps(result))
    return 2 if result["decision"] == "DENY" else 0


if __name__ == "__main__":
    raise SystemExit(main())
