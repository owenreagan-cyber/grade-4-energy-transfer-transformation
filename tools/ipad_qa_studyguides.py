#!/usr/bin/env python3
"""One-shot bounded iPad A16 spot check for the Unit 1 + Unit 2 study-guide PDFs."""
import functools, http.server, os, socketserver, subprocess, threading, time

DEVICE = "00008120-001E54313E380032"
HOST = "192.168.4.47"
PORT = 8998
SERVE = "/tmp/ipad_serve"
OUT = "/tmp/ipad_sg"
PYM = ".venv/bin/pymobiledevice3"
TARGETS = [("u1_study_guide", "u1-study-guide.pdf"), ("u2_study_review", "u2-study-review.pdf")]

def nav(url):
    return subprocess.run([PYM, "webinspector", "js-shell", "--url", url, "--open-safari", "--timeout", "15"],
                          input="", capture_output=True, text=True, timeout=40)

def shot(path):
    return subprocess.run(["xcrun", "devicectl", "device", "capture", "screenshot",
                           "--device", DEVICE, "--destination", path],
                          capture_output=True, text=True, timeout=60)

def main():
    os.makedirs(OUT, exist_ok=True)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SERVE)
    httpd = socketserver.TCPServer((HOST, PORT), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True); t.start()
    time.sleep(1.0)
    try:
        for name, fn in TARGETS:
            r = nav(f"http://{HOST}:{PORT}/{fn}")
            nav_ok = "Created:" in r.stdout or r.returncode == 0
            time.sleep(2.5)
            s = shot(os.path.join(OUT, name + ".png"))
            ok = "Screenshot saved" in (s.stdout or "") + (s.stderr or "")
            print(f"[{'OK' if ok else 'FAIL'}] {name} nav={'ok' if nav_ok else 'rc'+str(r.returncode)}")
    finally:
        httpd.shutdown(); httpd.server_close()
        print("server stopped")

if __name__ == "__main__":
    main()
