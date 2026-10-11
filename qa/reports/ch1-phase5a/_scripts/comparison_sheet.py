#!/usr/bin/env python3
"""Labeled side-by-side comparison sheets for visual candidate review.
Usage: python3 comparison_sheet.py SPEC.json OUT_DIR
SPEC.json = {"group_id": {"title": "...", "items": [{"label": "...", "path": "..."}]}}
Each group becomes OUT_DIR/<group_id>.png — a labeled horizontal strip of thumbnails.
"""
import sys, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

THUMB_W, THUMB_H = 460, 300
LABEL_H = 40
PAD = 12


def main():
    spec = json.load(open(sys.argv[1]))
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 22)
        font_big = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 30)
    except Exception:
        font = ImageFont.load_default()
        font_big = font

    for gid, group in spec.items():
        title = group.get('title', gid)
        items = group.get('items', [])
        n = len(items)
        title_h = 46 if title else 0
        W = max(n, 1) * (THUMB_W + PAD) + PAD
        H = title_h + THUMB_H + LABEL_H + PAD * 2
        sheet = Image.new('RGB', (W, H), (24, 26, 32))
        d = ImageDraw.Draw(sheet)
        if title:
            d.text((PAD, 10), title, fill=(255, 220, 140), font=font_big)
        for i, it in enumerate(items):
            x = PAD + i * (THUMB_W + PAD)
            y = title_h + PAD
            # thumbnail
            try:
                im = Image.open(it['path']).convert('RGB')
                im.thumbnail((THUMB_W, THUMB_H))
                px = x + (THUMB_W - im.width) // 2
                py = y + (THUMB_H - im.height) // 2
                sheet.paste(im, (px, py))
            except Exception as e:
                d.rectangle([x, y, x + THUMB_W, y + THUMB_H], fill=(70, 0, 0))
                d.text((x + 6, y + 6), f'ERR {e}', fill='white', font=font)
            d.rectangle([x, y, x + THUMB_W, y + THUMB_H], outline=(120, 120, 120), width=1)
            d.text((x + 4, y + THUMB_H + 6), it.get('label', str(i)), fill='white', font=font)
        out = out_dir / f"{gid}.png"
        sheet.save(out)
        print(f"wrote {out}")


if __name__ == '__main__':
    main()
