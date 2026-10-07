"""Frozen-chapter byte enforcement (F-9).

Recomputes SHA-256 for every frozen classroom artifact and the combined
playbook from the working tree, and compares against the frozen registry.
The registry's own integrity is pinned by ``REGISTRY_SHA`` below; the hook that
invokes this gate pins THIS file's hash separately, so neither the registry nor
this gate can be edited in-repo without tripping enforcement.

The check compares actual current bytes to the frozen baseline, never working-tree
dirtiness. It is invoked by the real git ``pre-commit`` hook, so it runs on every
commit regardless of invocation path (direct, subprocess, wrapper).

Machine-readable result on stdout; exit 0 = ALLOW, exit 1 = DENY.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "qa" / "gold-standard" / "frozen_registry.json"

# Pinned SHA-256 of qa/gold-standard/frozen_registry.json. Editing the registry
# (e.g. removing a chapter) breaks this and DENIES.
REGISTRY_SHA = "4676567ff776ffd502e4c6bf922a5bb4556290fa096c5e3592c9e24f7f342564"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(root: Path | None = None) -> dict:
    """Return a machine-readable enforcement result."""
    base = root or ROOT
    registry_path = base / "qa" / "gold-standard" / "frozen_registry.json"
    result = {
        "gateId": "FROZEN_BYTES",
        "registryOk": False,
        "decision": "DENY",
        "mismatches": [],
        "frozenCount": 0,
    }

    if not registry_path.is_file():
        result["mismatches"].append("frozen registry missing")
        return result

    registry_sha = _sha256(registry_path)
    if registry_sha != REGISTRY_SHA:
        result["mismatches"].append("frozen registry tampered (hash %s)" % registry_sha[:16])
        return result
    result["registryOk"] = True

    try:
        files = json.loads(registry_path.read_text(encoding="utf-8"))["files"]
    except (OSError, ValueError, KeyError):
        result["mismatches"].append("frozen registry unreadable")
        return result

    result["frozenCount"] = len(files)
    for rel in sorted(files):
        recorded = files[rel]
        target = base / rel
        if not target.is_file():
            result["mismatches"].append("%s: MISSING" % rel)
            continue
        current = _sha256(target)
        if current != recorded:
            result["mismatches"].append("%s: CHANGED" % rel)

    result["decision"] = "ALLOW" if not result["mismatches"] else "DENY"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = check()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("FROZEN_BYTES %s (%d files, %d mismatches)" % (
            result["decision"], result["frozenCount"], len(result["mismatches"])))
        for m in result["mismatches"]:
            print("  %s" % m)
    return 0 if result["decision"] == "ALLOW" else 1


if __name__ == "__main__":
    raise SystemExit(main())
