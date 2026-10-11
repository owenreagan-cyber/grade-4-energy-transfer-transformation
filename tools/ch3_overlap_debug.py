import sys
from PIL import Image
sys.path.insert(0, "tools")
from chapter_qa.visual_qa import margin_content_ink
from ch3_seal_remaining import bbox_lines, boxes_for_page

image = Image.open("qa/work/ch3-factory-2026-10-06/renders/03-ch3-energy-speed-guided-notes-p001-300dpi.png")
print("margin", margin_content_ink(image, 300))
parsed = bbox_lines("production/premium-notes/03-ch3-energy-speed-guided-notes.pdf")
boxes = boxes_for_page(parsed[0])
print("boxes", len(boxes))
outside = [box for box in boxes if box["x"] < 0 or box["y"] < 0 or box["x"] + box["w"] > box["pageWidthIn"] or box["y"] + box["h"] > box["pageHeightIn"]]
print("outside", len(outside))
if outside:
    print(outside[0])
texts = [box for box in boxes if box["kind"] == "text"]
pairs = 0
for i, box in enumerate(texts):
    for other in texts[i + 1:]:
        x0 = max(box["x"], other["x"])
        y0 = max(box["y"], other["y"])
        x1 = min(box["x"] + box["w"], other["x"] + other["w"])
        y1 = min(box["y"] + box["h"], other["y"] + other["h"])
        if x1 > x0 and y1 > y0:
            pairs += 1
            if pairs <= 3:
                print("overlap h", round(y1 - y0, 3), "texts", box["text"][:40], "|", other["text"][:40])
print("overlap pairs", pairs)
from chapter_qa.visual_qa import page_record
from chapter_qa.identity import hash_file
png = "qa/work/ch3-factory-2026-10-06/renders/03-ch3-energy-speed-guided-notes-p001-300dpi.png"
record = page_record({
    "artifactId": "notes-p001", "artifactPath": "production/premium-notes/03-ch3-energy-speed-guided-notes.docx",
    "artifactHash": hash_file("production/premium-notes/03-ch3-energy-speed-guided-notes.docx"),
    "renderPath": png, "renderHash": hash_file(png), "pageOrSlide": 1, "dpi": 300,
    "width": image.width, "height": image.height, "inspectionMethod": "rendered-page",
    "reviewerRole": "VISUAL_QA_AUDITOR",
}, boxes=boxes, image=image)
print("findings", [(item["code"], item["message"]) for item in record["findings"]])
