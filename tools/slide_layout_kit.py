"""Reusable content-first layout kit for python-pptx science decks (Phase 5C).

Root-cause fixes (see qa/reports/ch1-phase5c/CH1_VISUAL_QA_ROOT_CAUSE_ANALYSIS.md):
  RC-1  regions were fixed numbers, never derived from the text they hold -> measure() / need_h()
  RC-2  photos were letterboxed into leftover space ("aspect-FIT") -> cover() crops to the exact region aspect
  RC-3  pictures were appended after text and could paint over it -> constructors draw photo, then text, and
        never place text inside a photo rectangle unless it sits on an opaque chip
  RC-4  nothing failed at build time -> FitError is raised when measured text exceeds its reserved box

Measurement uses the real font files with Pillow. Calibration against LibreOffice 26.8 renders (Phase 5C):
line pitch = 1.2 x size; paragraph space_after is added between paragraphs; widths are padded 4%.
"""
import os
from PIL import Image, ImageFont

FONT_FILES = {
    ("Avenir Next", False, False): ("/System/Library/Fonts/Avenir Next.ttc", 7),
    ("Avenir Next", True, False): ("/System/Library/Fonts/Avenir Next.ttc", 0),
    ("Avenir Next", False, True): ("/System/Library/Fonts/Avenir Next.ttc", 4),
    ("Avenir Next", True, True): ("/System/Library/Fonts/Avenir Next.ttc", 1),
    ("Georgia", False, False): ("/System/Library/Fonts/Supplemental/Georgia.ttf", 0),
    ("Georgia", True, False): ("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 0),
    ("Georgia", False, True): ("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", 0),
    ("Georgia", True, True): ("/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf", 0),
}
LINE = 1.2          # line pitch / font size (LibreOffice, measured)
W_PAD = 1.04        # width safety factor (kerning / renderer differences)
_cache = {}


class FitError(Exception):
    pass


def _font(family, bold, italic, size):
    key = (family, bool(bold), bool(italic), size)
    if key not in _cache:
        path, idx = FONT_FILES[(family, bool(bold), bool(italic))]
        _cache[key] = ImageFont.truetype(path, size * 10, index=idx)   # 10 units per pt for precision
    return _cache[key]


def text_width_in(s, size, family="Avenir Next", bold=False, italic=False):
    return _font(family, bold, italic, size).getlength(s) / 10.0 / 72.0 * W_PAD


def wrap(s, width_in, size, family="Avenir Next", bold=False, italic=False):
    """Greedy word wrap, honouring explicit newlines. Returns list of lines."""
    out = []
    for hard in s.split("\n"):
        words, cur = hard.split(" "), ""
        for w in words:
            trial = (cur + " " + w) if cur else w
            if cur and text_width_in(trial, size, family, bold, italic) > width_in:
                out.append(cur); cur = w
            else:
                cur = trial
        out.append(cur)
    return out


def need_h(paras, width_in, size, family="Avenir Next", bold=False, italic=False, gap_pt=10):
    """Height (in) needed for a list of paragraphs (str or list)."""
    if isinstance(paras, str):
        paras = [paras]
    lines = sum(len(wrap(p, width_in, size, family, bold, italic)) for p in paras)
    if lines == 1:                 # a lone line only needs its glyph height; extra leading is harmless
        return 1.1 * size / 72.0
    return (lines * LINE * size + max(len(paras) - 1, 0) * gap_pt) / 72.0


def n_lines(s, width_in, size, family="Avenir Next", bold=False, italic=False):
    return len(wrap(s, width_in, size, family, bold, italic))


def check_fit(label, paras, w, h, size, family="Avenir Next", bold=False, italic=False, gap_pt=10, tol=0.02):
    need = need_h(paras, w, size, family, bold, italic, gap_pt)
    if need > h + tol:
        raise FitError("%s: text needs %.2fin but box is %.2fin (w=%.2fin, %spt) -> %r"
                       % (label, need, h, w, size, (paras if isinstance(paras, str) else " / ".join(paras))[:70]))
    return need


def cover(src, w_in, h_in, stage_dir, name, focus=(0.5, 0.5), box=None):
    """Crop `src` (optionally pre-cropped to `box`) to exactly the w:h aspect around `focus` (fractions of the
    usable image) and save to stage_dir/name. Returns the staged path. No letterboxing, no distortion."""
    im = Image.open(src).convert("RGB")
    if box:
        im = im.crop(box)
    iw, ih = im.size
    target = w_in / h_in
    if iw / ih > target:            # too wide -> crop width
        nw, nh = int(round(ih * target)), ih
    else:                           # too tall -> crop height
        nw, nh = iw, int(round(iw / target))
    cx, cy = focus[0] * iw, focus[1] * ih
    x0 = int(min(max(cx - nw / 2, 0), iw - nw)); y0 = int(min(max(cy - nh / 2, 0), ih - nh))
    out = im.crop((x0, y0, x0 + nw, y0 + nh))
    os.makedirs(stage_dir, exist_ok=True)
    p = os.path.join(stage_dir, name)
    out.save(p, quality=92) if p.lower().endswith(".jpg") else out.save(p)
    return p
