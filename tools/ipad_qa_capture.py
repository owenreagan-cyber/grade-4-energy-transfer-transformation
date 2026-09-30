#!/usr/bin/env python3
"""Phase 13T physical-iPad QA capture harness.

Navigates Safari on the attached iPad (A16) to a local QA harness URL using
pymobiledevice3 WebInspector (inspector mode, no Remote Automation needed),
then captures a screenshot via `xcrun devicectl`.

Usage:
  python tools/ipad_qa_capture.py --name <label> --url <url> [--sleep N]
"""
import argparse
import subprocess
import sys
import time

DEVICE = "00008120-001E54313E380032"
BASE = "qa/temp/phase13t/ipad"
PYM = ".venv/bin/pymobiledevice3"


def navigate(url, timeout=15):
    """Navigate the existing Safari page to `url` via WebInspector inspector mode."""
    # pipe EOF so the REPL exits immediately after navigation
    r = subprocess.run(
        [PYM, "webinspector", "js-shell", "--url", url, "--open-safari",
         "--timeout", str(timeout)],
        input="", capture_output=True, text=True, timeout=timeout + 20,
    )
    return r


def screenshot(path):
    r = subprocess.run(
        ["xcrun", "devicectl", "device", "capture", "screenshot",
         "--device", DEVICE, "--destination", path],
        capture_output=True, text=True, timeout=60,
    )
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--sleep", type=float, default=2.5)
    args = ap.parse_args()

    safe_name = args.name.replace("/", "_").replace(" ", "_")
    out = f"{BASE}/shots/{safe_name}.png"

    nav = navigate(args.url)
    if "Created:" not in nav.stdout and nav.returncode != 0:
        print(f"[nav-fail] {args.name}: rc={nav.returncode} err={nav.stderr[-200:]}")
    time.sleep(args.sleep)
    shot = screenshot(out)
    ok = "Screenshot saved" in shot.stdout or "Screenshot saved" in shot.stderr
    print(f"[{'OK' if ok else 'FAIL'}] {args.name} -> {out}")


if __name__ == "__main__":
    main()
