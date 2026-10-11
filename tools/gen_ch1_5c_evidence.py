#!/usr/bin/env python3
"""Phase 5C evidence package: v1 | v2 side-by-side comparisons, pilot comparison sheet, build SHA-256 manifest.
Read-only on both candidates; writes only under qa/reports/ch1-phase5c/ and the v2 candidate's BUILD_SHA256.json."""
import glob, hashlib, json, os
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
V1 = os.path.join(ROOT, "production/candidates/chapter-01/ch1-premium-hybrid-v1")
V2 = os.path.join(ROOT, "production/candidates/chapter-01/ch1-premium-hybrid-v2")
OUT = os.path.join(ROOT, "qa/reports/ch1-phase5c")
CHANGED = [1, 4, 6, 8, 10, 14, 15, 17, 19, 20, 23, 24, 25, 28, 29, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]
PILOT = [1, 4, 8, 10, 17, 20, 25, 28, 30, 31, 34, 35]


def pair(n, w=900):
    a = Image.open(os.path.join(V1, "previews/slide-%02d.png" % n)).convert("RGB")
    b = Image.open(os.path.join(V2, "previews/slide-%02d.png" % n)).convert("RGB")
    h = int(w * a.height / a.width)
    a, b = a.resize((w, h)), b.resize((w, h))
    im = Image.new("RGB", (2 * w + 30, h + 40), (40, 40, 40))
    im.paste(a, (10, 30)); im.paste(b, (w + 20, 30))
    d = ImageDraw.Draw(im)
    d.text((10, 8), "slide %d - Phase 5B (ch1-premium-hybrid-v1)" % n, fill=(230, 230, 230))
    d.text((w + 20, 8), "slide %d - Phase 5C (ch1-premium-hybrid-v2)" % n, fill=(230, 230, 230))
    return im


def main():
    cdir = os.path.join(OUT, "comparisons"); os.makedirs(cdir, exist_ok=True)
    for n in CHANGED:
        pair(n).save(os.path.join(cdir, "slide-%02d-v1-vs-v2.png" % n))
    ims = [pair(n, 640) for n in PILOT]
    sheet = Image.new("RGB", (ims[0].width, sum(i.height for i in ims)), (40, 40, 40))
    y = 0
    for i in ims:
        sheet.paste(i, (0, y)); y += i.height
    sheet.save(os.path.join(OUT, "pilot", "PILOT_COMPARISON_SHEET.png"))
    sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
    files = sorted(f for f in glob.glob(os.path.join(V2, "**", "*"), recursive=True)
                   if os.path.isfile(f) and not f.endswith("BUILD_SHA256.json"))
    man = {os.path.relpath(f, ROOT): sha(f) for f in files}
    for t in ["tools/build_ch1_premium_v2.py", "tools/slide_layout_kit.py", "tools/render_slides_isolated.py",
              "tools/qa_slide_visual_v2.py", "tools/qa_slide_visual_v2_negative_tests.py",
              "tools/qa_ch1_premium_v2.py", "tools/qa_ch1_premium_v2_parity.py", "tools/gen_ch1_5c_evidence.py"]:
        man[t] = sha(os.path.join(ROOT, t))
    json.dump(man, open(os.path.join(V2, "BUILD_SHA256.json"), "w"), indent=1)
    print("comparisons:", len(CHANGED), "| manifest entries:", len(man))


if __name__ == "__main__":
    main()
