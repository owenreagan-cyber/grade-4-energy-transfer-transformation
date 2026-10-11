#!/usr/bin/env python3
import base64, json, sys, urllib.request

img = sys.argv[1] if len(sys.argv) > 1 else "qa/slides-qa/ch1/ipad/00-device-home-test.png"
data = base64.b64encode(open(img, "rb").read()).decode()
payload = {
    "model": "qwen3-vl:30b",
    "prompt": "Describe this image in one paragraph.",
    "images": [data],
    "stream": False,
    "options": {"temperature": 0.0},
}
req = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=900) as r:
    resp = json.loads(r.read().decode())
print("KEYS:", list(resp.keys()))
print("done_reason:", resp.get("done_reason"))
print("error:", resp.get("error"))
print("response len:", len(resp.get("response", "")))
print("RESPONSE:", resp.get("response", "")[:2000])
