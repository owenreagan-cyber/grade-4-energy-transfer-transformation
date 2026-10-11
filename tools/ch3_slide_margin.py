from PIL import Image

def bands(path):
    image = Image.open(path).convert("RGB")
    w, h = image.size
    margin = 150

    def dirty(box):
        crop = image.crop(box)
        colors = crop.getcolors(maxcolors=crop.width * crop.height) or []
        return sum(count for count, rgb in colors if rgb != (255, 255, 255))

    print(path, image.size, "top", dirty((0, 0, w, margin)), "bottom", dirty((0, h - margin, w, h)), "left", dirty((0, 0, margin, h)))

bands("qa/work/ch3-factory-2026-10-06/renders/03-ch3-energy-speed-slides-p001-300dpi.png")
bands("qa/work/ch3-factory-2026-10-06/renders/03-ch3-energy-speed-slides-p002-300dpi.png")
raw = open("production/premium-notes/03-ch3-energy-speed-guided-notes.pdf", "rb").read()
print("Tj", b"Tj" in raw, "TJ", b"TJ" in raw, "size", len(raw))
