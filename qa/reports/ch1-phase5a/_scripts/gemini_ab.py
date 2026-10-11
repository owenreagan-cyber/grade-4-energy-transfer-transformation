#!/usr/bin/env python3
"""Side-by-side A/B sheet for Gemini Session 2 (Forms_of_Energy vs Forms_of_Energy-2)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

A = Path('/tmp/ch1_audit/gemini-Forms_of_Energy/media')
B = Path('/tmp/ch1_audit/gemini-Forms_of_Energy-2/media')
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

THUMB_W, THUMB_H = 500, 300
try:
    font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 24)
except Exception:
    font = ImageFont.load_default()

afiles = sorted(A.glob('*.png'), key=lambda p: int(p.stem.replace('image', '')))
bfiles = sorted(B.glob('*.png'), key=lambda p: int(p.stem.replace('image', '')))
n = max(len(afiles), len(bfiles))
cols = 4
rows = (n + cols - 1) // cols
cell_w = THUMB_W * 2 + 30
W = cols * cell_w + 20
H = rows * (THUMB_H + 60) + 20
sheet = Image.new('RGB', (W, H), (24, 26, 32))
d = ImageDraw.Draw(sheet)

for i in range(n):
    r, c = divmod(i, cols)
    x = 20 + c * cell_w
    y = 20 + r * (THUMB_H + 60)
    for col, (flist, tag) in enumerate([(afiles, 'Forms_of_Energy (v1)'), (bfiles, 'Forms_of_Energy-2 (v2)')]):
        px = x + col * (THUMB_W + 30)
        if i < len(flist):
            try:
                im = Image.open(flist[i]).convert('RGB')
                im.thumbnail((THUMB_W, THUMB_H))
                sheet.paste(im, (px + (THUMB_W - im.width)//2, y + (THUMB_H - im.height)//2))
            except Exception as e:
                d.text((px, y), f'ERR {e}', fill='white', font=font)
        d.text((px, y + THUMB_H + 6), f'S{i+1:02d} {tag}', fill='white', font=font)
out = OUT / 'gemini-session2-ab.png'
sheet.save(out)
print(f'wrote {out}')
