from PIL import Image

image = Image.open("qa/work/ch3-factory-2026-10-06/renders/03-ch3-energy-speed-slides-p001-300dpi.png").convert("RGB")
w, h = image.size
margin = 150
cobalt = (27, 79, 194)
px = image.load()
other = []
for y in list(range(margin)) + list(range(h - margin, h)):
    for x in range(w):
        rgb = px[x, y]
        if rgb != cobalt and rgb != (255, 255, 255):
            other.append((x, y, rgb))
            if len(other) > 12:
                break
    if len(other) > 12:
        break
print("non-cobalt margin samples", other[:12], "count_capped", len(other))
# content slides: is dirty only the last column?
for name in ("p002", "p010", "p020", "p041"):
    im = Image.open("qa/work/ch3-factory-2026-10-06/renders/03-ch3-energy-speed-slides-%s-300dpi.png" % name).convert("RGB")
    p = im.load()
    xs = set()
    for y in range(150):
        for x in range(im.width - 20, im.width):
            if p[x, y] != (255, 255, 255):
                xs.add(x)
    print(name, "dirty x in right 20px of top margin", sorted(xs))
