"""Read-only classification evidence for remediation loop 2."""
import re
import subprocess
from collections import Counter
from PIL import Image

def margin_pixels(path, margin=150, limit=8):
    image = Image.open(path).convert("RGB")
    w, h = image.size
    hits = []
    bands = {
        "top": (0, 0, w, margin),
        "bottom": (0, h - margin, w, h),
        "left": (0, 0, margin, h),
        "right": (w - margin, 0, w, h),
    }
    for name, box in bands.items():
        crop = image.crop(box)
        px = crop.load()
        count = 0
        samples = []
        for y in range(crop.height):
            for x in range(crop.width):
                rgb = px[x, y]
                if rgb != (255, 255, 255):
                    count += 1
                    if len(samples) < 3:
                        ox = box[0] + x
                        oy = box[1] + y
                        samples.append((ox, oy, rgb))
        hits.append((name, count, samples))
    return image.size, hits

for label, path in (
    ("title", "qa/work/ch3-factory-2026-10-06/renders/03-ch3-energy-speed-slides-p001-300dpi.png"),
    ("content", "qa/work/ch3-factory-2026-10-06/renders/03-ch3-energy-speed-slides-p002-300dpi.png"),
    ("notes", "qa/work/ch3-factory-2026-10-06/renders/03-ch3-energy-speed-guided-notes-p001-300dpi.png"),
):
    size, hits = margin_pixels(path)
    print("==", label, size)
    for name, count, samples in hits:
        print(" ", name, count, samples)

raw = subprocess.check_output(["pdftotext", "-bbox", "production/premium-notes/03-ch3-energy-speed-guided-notes.pdf", "-"], text=True)
words = re.findall(r'yMin="([0-9.]+)".*?>([^<]+)</word>', raw)
print("first notes words", words[:6], "count", len(words))
print("page tag", re.search(r"<page[^>]*>", raw).group(0))

print("--- slide images ---")
print(subprocess.check_output(["pdfimages", "-list", "production/slides/03-ch3-energy-speed-slides.pdf"], text=True)[:1500])
