#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import sys

sheet_path = Path("assets/Cinematic Energy Concepts Storyboard (1).png")
if not sheet_path.exists():
    print(f"Error: Could not find {sheet_path}")
    sys.exit(1)

out_dir = Path("assets/ch1")
out_dir.mkdir(parents=True, exist_ok=True)

img = Image.open(sheet_path)
W, H = img.size

panels = {
    "panel-01-bedroom-light.png": (0.000, 0.000, 0.395, 0.338),
    "panel-02-single-bulb.png":   (0.395, 0.000, 0.680, 0.338),
    "panel-03-candle-change.png": (0.680, 0.000, 1.000, 0.338),
    "panel-04-flashlight-cut.png":(0.000, 0.338, 0.313, 0.584),
    "panel-05-rubber-band.png":   (0.313, 0.338, 0.648, 0.584),
    "panel-06-apple-drop.png":    (0.648, 0.338, 1.000, 0.584),
    "panel-07-change-cards.png":  (0.000, 0.584, 0.285, 0.803),
    "panel-08-forms-of-energy.png":(0.285, 0.584, 0.676, 0.803),
    "panel-09-blank-model-chain.png": (0.676, 0.584, 1.000, 0.803),
    "panel-10-living-room.png":   (0.000, 0.803, 0.328, 1.000),
    "panel-11-three-stored.png":  (0.328, 0.803, 0.680, 1.000),
    "panel-12-diurnal-energy.png":(0.680, 0.803, 1.000, 1.000),
}

print(f"Slicing panels from {sheet_path.name} ({W}x{H})...")

for name, (x1, y1, x2, y2) in panels.items():
    box = (int(x1 * W), int(y1 * H), int(x2 * W), int(y2 * H))
    crop = img.crop(box)
    out_file = out_dir / name
    crop.save(out_file)
    print(f"✓ Saved {out_file.name} ({crop.width}x{crop.height}px)")

print("\nDone. All assets ready in assets/ch1/")
