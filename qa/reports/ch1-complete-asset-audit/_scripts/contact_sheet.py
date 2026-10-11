#!/usr/bin/env python3
"""Compose labeled contact sheets from a directory of images.
Usage: python3 contact_sheet.py IMG_DIR OUT.png [--cols N] [--label-files]
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def main():
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    cols = 5
    if '--cols' in sys.argv:
        cols = int(sys.argv[sys.argv.index('--cols') + 1])
    label_files = '--label-files' in sys.argv

    files = sorted(
        [p for p in src.iterdir() if p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp')],
        key=lambda p: p.name,
    )
    if not files:
        print(f"no images in {src}")
        return

    cell_w, cell_h = 420, 236
    thumb_w, thumb_h = cell_w - 8, cell_h - 34
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * cell_w + 4, rows * cell_h + 4), (30, 30, 30))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 18)
        small = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 14)
    except Exception:
        font = ImageFont.load_default()
        small = font

    for i, f in enumerate(files):
        r, c = divmod(i, cols)
        x, y = 4 + c * cell_w, 4 + r * cell_h
        try:
            im = Image.open(f).convert('RGB')
            im.thumbnail((thumb_w, thumb_h))
            px = x + (thumb_w - im.width) // 2
            py = y + (thumb_h - im.height) // 2
            sheet.paste(im, (px, py))
        except Exception as e:
            draw.rectangle([x, y, x + thumb_w, y + thumb_h], fill=(60, 0, 0))
            draw.text((x + 4, y + 4), f'ERR {e}', fill='white', font=small)
        label = f.name if label_files else str(i)
        draw.text((x + 4, y + thumb_h + 2), label, fill='white', font=font)

    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"wrote {out} ({sheet.width}x{sheet.height}) from {len(files)} images")


if __name__ == '__main__':
    main()
