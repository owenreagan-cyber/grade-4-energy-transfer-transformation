"""Source closure from a builder entrypoint.

A hand-written file list is not treated as complete. Static AST evidence
is compared with the declared closure.
"""

from __future__ import annotations

import ast
import os
from pathlib import Path

from chapter_qa.emit import seal

CLOSURE_CODES = (
    "UNTRACKED_RUNTIME_DEPENDENCY",
    "UNRESOLVED_IMPORT",
    "OUTSIDE_FREEZE_DEPENDENCY",
    "UNDECLARED_ENVIRONMENT_INPUT",
    "MISSING_SOURCE",
    "SOURCE_HASH_DRIFT",
    "TOOL_VERSION_DRIFT",
)


def _calls_name(node: ast.AST) -> str:
    func = getattr(node, "func", None)
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        base = func.value
        if isinstance(base, ast.Name):
            return base.id + "." + func.attr
        return func.attr
    return ""


def discover_static(entrypoint: Path) -> dict:
    """Imports, open() literals, environment reads, and subprocess commands."""
    tree = ast.parse(entrypoint.read_text(encoding="utf-8"), filename=str(entrypoint))
    imports = []
    opens = []
    env = []
    tools = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module.split(".")[0])
        elif isinstance(node, ast.Call):
            name = _calls_name(node)
            if name == "open" and node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                mode = ""
                if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
                    mode = str(node.args[1].value)
                if "w" not in mode and "a" not in mode:
                    opens.append(node.args[0].value)
            if name in ("os.getenv", "os.environ.get") and node.args and isinstance(node.args[0], ast.Constant):
                env.append(str(node.args[0].value))
            if name in ("subprocess.run", "subprocess.check_call", "subprocess.check_output") and node.args:
                arg = node.args[0]
                if isinstance(arg, ast.List) and arg.elts and isinstance(arg.elts[0], ast.Constant):
                    tools.append(str(arg.elts[0].value))
        elif isinstance(node, ast.Subscript):
            value = node.value
            if isinstance(value, ast.Attribute) and value.attr == "environ":
                sl = node.slice
                if isinstance(sl, ast.Constant):
                    env.append(str(sl.value))
    return {
        "imports": sorted(set(imports)),
        "files": sorted(set(opens)),
        "environment": sorted(set(env)),
        "tools": sorted(set(tools)),
        "method": "ast",
    }


def resolve_local_imports(entrypoint: Path, imports: list[str]) -> list[str]:
    folder = entrypoint.parent
    found = []
    for name in imports:
        candidate = folder / (name + ".py")
        if candidate.is_file():
            found.append(candidate.name)
    return found


def assess_closure(entrypoint: Path, declared: dict, *, present_files: set[str] | None = None,
                   env: dict | None = None, tool_versions: dict | None = None) -> dict:
    """Compare a declared closure with what the entrypoint can read."""
    discovered = discover_static(entrypoint)
    local = resolve_local_imports(entrypoint, discovered["imports"])
    declared_files = set(declared.get("files") or [])
    declared_env = set(declared.get("environment") or [])
    declared_tools = dict(declared.get("tools") or {})
    present = set(present_files) if present_files is not None else set(declared_files)
    findings = []

    def add(code, message):
        findings.append({"code": code, "message": message})

    for name in local:
        if name not in declared_files:
            add("UNTRACKED_RUNTIME_DEPENDENCY", "local import %s is not in the closure" % name)
        if name not in present:
            add("MISSING_SOURCE", "local import %s is missing" % name)
    for name in discovered["files"]:
        if name not in declared_files:
            add("UNTRACKED_RUNTIME_DEPENDENCY", "opened file %s is not in the closure" % name)
        if name not in present:
            add("MISSING_SOURCE", "opened file %s is missing" % name)
    for name in discovered["imports"]:
        if name in ("os", "sys", "json", "pathlib", "ast", "hashlib", "shutil"):
            continue
        if name not in declared.get("imports", []) and (entrypoint.parent / (name + ".py")).is_file() is False:
            if name not in (declared.get("imports") or []):
                add("UNRESOLVED_IMPORT", "import %s is not declared" % name)
    for name in discovered["environment"]:
        if name not in declared_env:
            add("UNDECLARED_ENVIRONMENT_INPUT", "environment variable %s is not declared" % name)
        elif env is not None and not env.get(name):
            add("UNDECLARED_ENVIRONMENT_INPUT", "environment variable %s is absent" % name)
    for tool in discovered["tools"]:
        if tool not in declared_tools:
            add("TOOL_VERSION_DRIFT", "tool %s is not in the closure" % tool)
        elif tool_versions and declared_tools.get(tool) and tool_versions.get(tool) != declared_tools.get(tool):
            add("TOOL_VERSION_DRIFT", "tool %s version drifted" % tool)
    for path in declared.get("outsideRepo") or []:
        add("OUTSIDE_FREEZE_DEPENDENCY", "closure lists outside-repo path %s" % path)
    for recorded, current in (declared.get("hashDrift") or {}).items():
        add("SOURCE_HASH_DRIFT", "hash drifted for %s" % recorded)
    return {"discovered": discovered, "findings": findings, "fails": bool(findings)}


def emit_closure_evidence(entrypoint, identity, evidence_path, declared, *, auditor_role="PROVENANCE_AUDITOR",
                          present_files=None, env=None, tool_versions=None, gate_id="SOURCE_CLOSURE"):
    assessed = assess_closure(
        Path(entrypoint), declared, present_files=present_files, env=env, tool_versions=tool_versions,
    )
    names = list(declared.get("files") or ["entrypoint"])
    data = {
        "evidenceId": "closure-%s" % gate_id.lower(),
        "gateId": gate_id,
        "auditorRole": auditor_role,
        "performed": True,
        "expectedInputs": names,
        "observedInputs": [] if assessed["fails"] else names,
        "thingBeingCertified": "candidate-builder:%s" % identity.candidateHash,
        "independentEvidenceSource": "static-ast:%s" % identity.sourceHash,
        "findings": [{"severity": "BLOCKING", "code": item["code"], "message": item["message"]} for item in assessed["findings"]],
        "evidencePaths": [evidence_path],
        "failureReason": None,
        "notVerifiedReason": None,
        "invalidationReasons": [],
        "execution": {
            "succeeded": True,
            "detectorException": False,
            "requiredInputsPresent": bool(names),
            "missingRender": False,
            "missingEvidence": False,
            "stale": False,
            "gateSpecificFailure": assessed["fails"],
            "unavailableEvidence": False,
        },
        "inventory": [{"name": "closureFiles", "expected": len(names), "observed": 0 if assessed["fails"] else len(names)}],
    }
    return seal(data, identity), assessed
