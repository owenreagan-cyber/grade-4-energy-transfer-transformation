import sys
from PIL import Image
sys.path.insert(0, "tools")
from chapter_qa.visual_qa import _ink_extent, _intersection
from ch3_seal_remaining import bbox_lines, boxes_for_page
pdf = "production/slides/03-ch3-energy-speed-slides.pdf"
parsed = bbox_lines(pdf)
for page in (38, 39, 41):
    image = Image.open("qa/work/ch3-factory-2026-10-06/renders/03-ch3-energy-speed-slides-p%03d-300dpi.png" % page)
    boxes = [box for box in boxes_for_page(parsed[page - 1]) if box["kind"] == "text"]
    print("==", page)
    shown = 0
    extents = [_ink_extent(image, box, 300) for box in boxes]
    for i, ink in enumerate(extents):
        if ink is None:
            continue
        for j in range(i + 1, len(boxes)):
            shared = _intersection(ink, extents[j]) if extents[j] else None
            if shared and shared["h"] > 0.04 and shared["w"] > 0.04:
                shown += 1
                if shown <= 6:
                    print(repr(boxes[i]["text"]), "vs", repr(boxes[j]["text"]), round(shared["w"], 3), round(shared["h"], 3))
    print("pairs", shown)
