"""Report non-white pixels inside a 0.5 inch margin of one render."""
from PIL import Image

path = "qa/work/ch3-factory-2026-10-06/renders/03-ch3-energy-speed-guided-notes-p001-300dpi.png"
image = Image.open(path).convert("RGB")
dpi = 300
margin = int(0.5 * dpi)
print("size", image.size)

def dirty(box):
    crop = image.crop(box)
    colors = crop.getcolors(maxcolors=crop.width * crop.height) or []
    bad = [(count, rgb) for count, rgb in colors if rgb != (255, 255, 255)]
    return sum(count for count, _ in bad), bad[:3]

w, h = image.size
bands = {
    "top": (0, 0, w, margin),
    "bottom": (0, h - margin, w, h),
    "left": (0, 0, margin, h),
    "right": (w - margin, 0, w, h),
}
for name, box in bands.items():
    count, sample = dirty(box)
    print(name, count, sample)
