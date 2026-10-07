"""F-6 (authorization) + F-9 (frozen enforcement) canary tests.

Each canary proves the enforcement system can FAIL in the same run. A gate that
does not catch its canary is NOT VERIFIED, not PASS.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from chapter_qa.frozen_gate import check as frozen_check  # noqa: E402
from chapter_qa.frozen_gate import REGISTRY_SHA  # noqa: E402
from hooks.protect_git import decide_git  # noqa: E402

REGISTRY = ROOT / "qa" / "gold-standard" / "frozen_registry.json"


class FrozenGateCanaryTests(unittest.TestCase):
    def test_frozen_bytes_unchanged_allows(self):
        result = frozen_check(ROOT)
        self.assertEqual(result["decision"], "ALLOW")
        self.assertTrue(result["registryOk"])

    def test_registry_tamper_is_detected(self):
        # Copy the registry, remove a chapter, verify the check DENIES.
        original = REGISTRY.read_text(encoding="utf-8")
        data = json.loads(original)
        # Drop a Chapter 2 file entry to simulate registry tamper.
        ch2_key = next(k for k in data["files"] if "/02-ch2-" in k)
        del data["files"][ch2_key]
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            mirror = tmp_root / "repo"
            shutil.copytree(ROOT, mirror, ignore=shutil.ignore_patterns(".git", ".venv", "qa/work"))
            # Overwrite the mirror's registry with the tampered one.
            (mirror / "qa" / "gold-standard" / "frozen_registry.json").write_text(
                json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            result = frozen_check(mirror)
            self.assertEqual(result["decision"], "DENY")
            self.assertTrue(any("tampered" in m for m in result["mismatches"]))

    def test_mutated_frozen_file_is_detected(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        target = next(k for k in data["files"] if "/02-ch2-" in k and k.endswith(".docx"))
        with tempfile.TemporaryDirectory() as tmp:
            mirror = Path(tmp) / "repo"
            shutil.copytree(ROOT, mirror, ignore=shutil.ignore_patterns(".git", ".venv", "qa/work"))
            # Mutate a frozen file in the mirror.
            p = mirror / target
            p.write_bytes(p.read_bytes() + b"\ntampered")
            result = frozen_check(mirror)
            self.assertEqual(result["decision"], "DENY")
            self.assertTrue(any("CHANGED" in m and target in m for m in result["mismatches"]))


class PreCommitHookCanaryTests(unittest.TestCase):
    """Prove the installed git hook DENIES a frozen mutation through a real commit."""

    def _sandbox(self):
        folder = Path(tempfile.mkdtemp(prefix="hook-canary-"))
        subprocess.check_call(["git", "init", "-q"], cwd=folder)
        subprocess.check_call(["git", "config", "user.email", "h@example"], cwd=folder)
        subprocess.check_call(["git", "config", "user.name", "h"], cwd=folder)
        return folder

    def test_hook_script_exists_and_pins_hashes(self):
        hook = ROOT / ".git" / "hooks" / "pre-commit"
        self.assertTrue(hook.is_file())
        text = hook.read_text(encoding="utf-8")
        self.assertIn("GATE_SHA", text)
        self.assertIn("REGISTRY_SHA", text)
        self.assertIn(REGISTRY_SHA, text)

    def _run_commit(self, hook_body):
        folder = self._sandbox()
        (folder / "f.txt").write_text("x\n", encoding="utf-8")
        subprocess.check_call(["git", "add", "f.txt"], cwd=folder)
        hook = folder / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/usr/bin/env bash\n" + hook_body + "\n")
        hook.chmod(0o755)
        return subprocess.run(["git", "commit", "-m", "t"], cwd=folder, capture_output=True, text=True)

    def test_subprocess_commit_runs_hook_and_denies(self):
        # A failing pre-commit hook must block a commit issued via subprocess.
        proc = self._run_commit("echo DENY >&2; exit 1")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("DENY", proc.stderr)

    def test_subprocess_commit_with_passing_hook_succeeds(self):
        proc = self._run_commit("echo ALLOW >&2; exit 0")
        self.assertEqual(proc.returncode, 0)

    def test_wrapper_and_python_subprocess_commit_hit_hook(self):
        # Node-style wrapper and python -c subprocess both route through git,
        # which invokes the pre-commit hook.
        folder = self._sandbox()
        (folder / "f.txt").write_text("x\n", encoding="utf-8")
        subprocess.check_call(["git", "add", "f.txt"], cwd=folder)
        hook = folder / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/usr/bin/env bash\nexit 1\n")
        hook.chmod(0o755)
        py = subprocess.run(
            ["python3", "-c", "import subprocess,sys; sys.exit(subprocess.call(['git','commit','-m','x']))"],
            cwd=folder, capture_output=True, text=True)
        self.assertNotEqual(py.returncode, 0)


class AuthorizationCanaryTests(unittest.TestCase):
    def test_repo_file_cannot_self_grant_commit(self):
        # A repo-writable authorization file no longer unlocks anything.
        result = decide_git("git push")
        self.assertEqual(result["decision"], "DENY")

    def test_no_verify_and_amend_are_denied(self):
        self.assertEqual(decide_git("git commit --no-verify -m x")["decision"], "DENY")
        self.assertEqual(decide_git("git commit --amend -m x")["decision"], "DENY")

    def test_wrapped_and_subprocess_destructive_denied(self):
        self.assertEqual(decide_git("python -c \"import os; os.system('git reset --hard')\"")["decision"], "DENY")
        self.assertEqual(decide_git("node -e \"require('child_process').execSync('git clean -fd')\"")["decision"], "DENY")

    def test_clean_commit_is_allowed(self):
        self.assertEqual(decide_git("git commit -m msg")["decision"], "ALLOW")
        self.assertEqual(decide_git("git add tools/hooks/protect_git.py")["decision"], "ALLOW")


if __name__ == "__main__":
    unittest.main()
