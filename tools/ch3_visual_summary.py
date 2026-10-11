import json
from collections import Counter
from PIL import Image

rows = json.load(open("qa/work/ch3-factory-2026-10-06/visual-map.json", encoding="utf-8"))
counts = Counter()
for row in rows:
    codes = sorted({item["code"] for item in row["findings"]})
    if codes:
        counts[row["artifact"]] += 1
        if row["page"] == 1:
            print(row["artifact"], codes)
print("dirty pages", sum(counts.values()), "of", len(rows))
for name, count in counts.most_common():
    print(count, name)

path = "qa/work/ch3-factory-2026-10-06/renders/03-ch3-energy-speed-slides-p001-300dpi.png"
image = Image.open(path).convert("RGB")
print("slide", image.size)
margin = 150
w, h = image.size

def dirty(box):
    crop = image.crop(box)
    colors = crop.getcolors(maxcolors=crop.width * crop.height) or []
    return sum(count for count, rgb in colors if rgb != (255, 255, 255))

print("top", dirty((0, 0, w, margin)), "bottom", dirty((0, h - margin, w, h)), "left", dirty((0, 0, margin, h)), "right", dirty((w - margin, 0, w, h)))
summary = json.load(open("qa/work/ch3-factory-2026-10-06/seal-summary.json", encoding="utf-8"))
print("PDF")
for row in summary["pdf"]:
    print(row["gate"], row["status"], row.get("pages"), row.get("size"), row["findings"][:2])
print("playbook findings", summary["playbook"]["findings"])
