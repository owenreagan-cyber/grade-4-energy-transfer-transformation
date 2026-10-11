#!/usr/bin/env python3
"""Physical iPad (A16) capture harness via `xcrun devicectl`.

Automates the supported, documented screenshot path for a physical iPad:
`xcrun devicectl device capture screenshot`. Each capture is paired with an
optional independent vision inspection (ollama qwen3-vl) so a screenshot is
never claimed to be a presentation open, and a screenshot is never claimed to
be proof of playback.

No desktop automation, no Simulator substitution, no app installs.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from vision import analyze, IPAD_RUBRIC


def capture(device: str, destination: str) -> dict:
    dest = Path(destination)
    dest.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["xcrun", "devicectl", "device", "capture", "screenshot",
         "--device", device, "--destination", str(dest)],
        capture_output=True, text=True,
    )
    ok = proc.returncode == 0 and dest.is_file()
    return {
        "device": device,
        "destination": str(dest),
        "captured": ok,
        "stderr": proc.stderr.strip()[:500],
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def device_details(device: str) -> dict:
    proc = subprocess.run(
        ["xcrun", "devicectl", "device", "info", "details", "--device", device],
        capture_output=True, text=True,
    )
    return {"exit": proc.returncode, "text": proc.stdout + proc.stderr}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--vision", action="store_true",
                    help="run independent vision inspection on the capture")
    args = ap.parse_args()

    rec = capture(args.device, args.out)
    if args.vision and rec["captured"]:
        rec["vision"] = analyze(args.out, IPAD_RUBRIC)
    print(json.dumps(rec, indent=2))
    sys.exit(0 if rec["captured"] else 1)


if __name__ == "__main__":
    main()
