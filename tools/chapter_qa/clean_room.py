"""Rebuild a candidate from a declared closure in an empty directory.

Generator output compared with a second copy of that same output is not
independent evidence. The expected bytes are fixed before the rebuild.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
from pathlib import Path


def _hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def reproduce(closure_dir: Path, entry_script: str, expected_hash: str, output_name: str, *, env: dict | None = None) -> dict:
    """Run entry_script inside closure_dir. Compare output to a predeclared hash."""
    script = closure_dir / entry_script
    if not script.is_file():
        return {"status": "FAIL", "reason": "MISSING_SOURCE", "outputHash": ""}
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    completed = subprocess.run(
        [os.environ.get("PHASE_C_PYTHON", "python3"), str(script)],
        cwd=str(closure_dir),
        capture_output=True,
        text=True,
        env=run_env,
        check=False,
    )
    output = closure_dir / output_name
    if completed.returncode != 0 or not output.is_file():
        return {"status": "FAIL", "reason": "rebuild failed", "outputHash": "", "stderr": completed.stderr[-400:]}
    digest = _hash_bytes(output.read_bytes())
    if digest != expected_hash:
        return {"status": "FAIL", "reason": "output identity mismatch", "outputHash": digest}
    return {"status": "PASS", "reason": "", "outputHash": digest}


def stage_closure(files: dict[str, bytes], dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for name, data in files.items():
        path = dest / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def same_output_is_not_independent(left: bytes, right: bytes) -> bool:
    """True when the two blobs are the same generator output, which cannot certify itself."""
    return left == right
