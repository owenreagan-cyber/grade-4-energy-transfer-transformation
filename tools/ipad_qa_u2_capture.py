#!/usr/bin/env python3
"""One-shot bounded iPad A16 physical capture for Phase 13AA Unit 2 review game.

Serves the key rendered PNGs over a short-lived local HTTP server, navigates the
attached iPad (A16) Safari to each via pymobiledevice3 WebInspector, captures a
devicectl screenshot, then shuts the server down and exits. No lingering process.
"""
import functools
import http.server
import os
import socketserver
import subprocess
import sys
import threading
import time

DEVICE = "00008120-001E54313E380032"   # physical iPad (A16), paired
HOST = "192.168.4.47"
PORT = 8999
SERVE = "/tmp/ipad_serve"
OUT = "/tmp/ipad_u2"
PYM = ".venv/bin/pymobiledevice3"

TARGETS = [
    ("title", "title-01.png"),
    ("board", "board-03.png"),
    ("diagram_wind", "diagram_wind-28.png"),
    ("diagram_solar", "diagram_solar-38.png"),
    ("final", "final-54.png"),
    ("scorecard", "scorecard-1.png"),
]

def run_nav(url):
    return subprocess.run(
        [PYM, "webinspector", "js-shell", "--url", url, "--open-safari", "--timeout", "15"],
        input="", capture_output=True, text=True, timeout=40,
    )

def run_shot(path):
    return subprocess.run(
        ["xcrun", "devicectl", "device", "capture", "screenshot",
         "--device", DEVICE, "--destination", path],
        capture_output=True, text=True, timeout=60,
    )

def main():
    os.makedirs(OUT, exist_ok=True)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SERVE)
    httpd = socketserver.TCPServer((HOST, PORT), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    time.sleep(1.0)
    try:
        for name, fn in TARGETS:
            url = f"http://{HOST}:{PORT}/{fn}"
            nav = run_nav(url)
            nav_ok = "Created:" in nav.stdout or nav.returncode == 0
            time.sleep(2.2)
            shot = run_shot(os.path.join(OUT, name + ".png"))
            ok = "Screenshot saved" in (shot.stdout or "") + (shot.stderr or "")
            print(f"[{'OK' if ok else 'FAIL'}] {name} nav={'ok' if nav_ok else 'rc'+str(nav.returncode)}")
    finally:
        httpd.shutdown()
        httpd.server_close()
        print("server stopped")

if __name__ == "__main__":
    main()
