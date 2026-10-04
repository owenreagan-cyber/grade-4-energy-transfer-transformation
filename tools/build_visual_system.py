#!/usr/bin/env python3
"""
Unit 1 Visual System — local asset + sample generator.

Reads assets/visual-system/design-tokens.json (single source of truth) and
deterministically emits:
  - reusable SVG assets  -> assets/visual-system/{icons,hud,badges,vocabulary,diagrams,chapter-themes}/
  - 4 sample pages (SVG) -> qa/temp/phase1_visual/samples/*.svg  (+ PNG renders)
  - contact sheet        -> qa/temp/phase1_visual/contact_sheet.png

Usage: .venv/bin/python tools/build_visual_system.py
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS_PATH = os.path.join(ROOT, "assets", "visual-system", "design-tokens.json")
ASSET_ROOT = os.path.join(ROOT, "assets", "visual-system")
QA_ROOT = os.path.join(ROOT, "qa", "temp", "phase1_visual")

FONT = "Avenir Next, Helvetica Neue, Helvetica, Arial, sans-serif"

with open(TOKENS_PATH) as f:
    T = json.load(f)

C = T["colors"]
UNIT = C["unit"]
CH = C["chapters"]


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def svg_doc(w, h, parts, color=None):
    body = "\n".join(parts)
    color_attr = f' color="{color}"' if color else ""
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="{FONT}"{color_attr}>\n{body}\n</svg>\n')


def txt(x, y, s, size, fill="#1A1D26", weight="Regular", anchor="start", ls=None, role=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    ls_attr = f' letter-spacing="{ls}"' if ls else ""
    w_attr = f' font-weight="{weight}"' if weight != "Regular" else ""
    r_attr = f' data-role="{role}"' if role else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}"'
            f'{w_attr}{a}{ls_attr}{r_attr} font-family="{FONT}">{esc(s)}</text>')


def rect(x, y, w, h, fill="none", stroke="none", sw=1, rx=0):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def line(x1, y1, x2, y2, stroke, sw, cap="round"):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"/>')


def circle(cx, cy, r, fill="none", stroke="none", sw=1):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def path(d, fill="none", stroke="none", sw=1, cap="round", join="round"):
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="{cap}" stroke-linejoin="{join}"/>')


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def tint(hexcolor, alpha):
    r, g, b = hex_to_rgb(hexcolor)
    return f"rgba({r},{g},{b},{alpha})"


def ensure(p):
    os.makedirs(p, exist_ok=True)


def write_svg(relpath, parts, w, h, color=None):
    p = os.path.join(ASSET_ROOT, relpath)
    ensure(os.path.dirname(p))
    with open(p, "w") as f:
        f.write(svg_doc(w, h, parts, color=color))
    return p


# --------------------------------------------------------------------------
# 1. ICONS  (generic HUD/action icons, 48x48, 2pt stroke)
# --------------------------------------------------------------------------

def icon_shapes(kind, s):
    p = []
    if kind == "recite":
        p += [path("M8 16h32v18a6 6 0 0 1-6 6H20l-6 4v-4h-6z", stroke=s, sw=2),
              line(16, 25, 32, 25, s, 2), line(16, 31, 28, 31, s, 2)]
    elif kind == "write":
        p += [path("M14 40 L8 46 L12 36 L34 14 A4 4 0 0 1 40 20 L18 42 Z", stroke=s, sw=2),
              line(30, 18, 38, 26, s, 2)]
    elif kind == "predict":
        p += [circle(24, 26, 14, stroke=s, sw=2), line(24, 8, 24, 12, s, 2),
              line(24, 40, 24, 44, s, 2), line(10, 26, 14, 26, s, 2),
              line(34, 26, 38, 26, s, 2), circle(24, 26, 3, fill=s)]
    elif kind == "vote":
        p += [path("M10 22 C14 12 24 12 24 22 L24 38 L14 38 C10 38 10 32 10 32 C6 32 6 26 10 26 C8 26 8 22 10 22 Z", stroke=s, sw=2),
              path("M30 22 L30 38 L38 38 L38 26 C38 22 34 20 30 22 Z", stroke=s, sw=2)]
    elif kind == "turntalk":
        p += [path("M8 14h22v14a5 5 0 0 1-5 5H16l-5 3v-3H8z", stroke=s, sw=2),
              path("M18 28h14v10a4 4 0 0 1-4 4h-5l-4 2v-2h-3z", stroke=s, sw=2, fill="#FFFFFF")]
    elif kind == "check":
        p += [path("M10 25 l9 9 L40 14", stroke=s, sw=2)]
    elif kind == "trace":
        p += [path("M10 38 C14 22 22 20 24 26 C26 32 30 32 32 22", stroke=s, sw=2),
              circle(32, 22, 2, fill=s)]
    elif kind == "draw":
        p += [path("M12 40 L12 30 Q24 12 38 20 Q40 28 30 32 L12 40", stroke=s, sw=2),
              line(26, 36, 34, 30, s, 2)]
    elif kind == "watch":
        p += [path("M8 24 C8 14 15 8 24 8 C33 8 40 14 40 24 C40 34 33 40 24 40 C15 40 8 34 8 24 Z", stroke=s, sw=2),
              circle(24, 24, 5, stroke=s, sw=2), circle(24, 24, 2, fill=s)]
    elif kind == "observe":
        p += [circle(20, 20, 9, stroke=s, sw=2), line(27, 27, 40, 40, s, 2)]
    elif kind == "evidence":
        p += [rect(12, 8, 24, 32, stroke=s, sw=2, rx=3), line(18, 16, 30, 16, s, 2),
              line(18, 23, 30, 23, s, 2), line(18, 30, 26, 30, s, 2)]
    elif kind == "data":
        p += [line(8, 40, 40, 40, s, 2), line(8, 40, 8, 8, s, 2),
              rect(14, 26, 6, 14, fill=s), rect(24, 18, 6, 22, fill=s),
              rect(34, 10, 6, 30, fill=s)]
    elif kind == "engineer":
        p += [path("M18 24 a8 8 0 0 1 14 -2 L40 30 L30 34 L26 28 A8 8 0 0 1 18 24 Z", stroke=s, sw=2)]
    elif kind == "explain":
        p += [path("M18 20 h12 a6 6 0 0 1 0 12 h-2 l-6 5 v-5 h-4 a6 6 0 0 1 0 -12 Z", stroke=s, sw=2),
              line(14, 24, 22, 24, s, 2), line(14, 29, 26, 29, s, 2)]
    else:
        p += [circle(24, 24, 14, stroke=s, sw=2)]
    return p


ICONS = ["recite", "write", "predict", "vote", "turntalk", "check", "trace",
         "draw", "watch", "observe", "evidence", "data", "engineer", "explain"]


def build_icons():
    out = []
    for k in ICONS:
        parts = ['<g fill="none" stroke-linecap="round" stroke-linejoin="round">']
        parts += icon_shapes(k, "#1A1D26")
        parts.append("</g>")
        out.append(write_svg(f"icons/{k}.svg", parts, 48, 48))
    return out


# --------------------------------------------------------------------------
# 2. HUD action bubbles
# --------------------------------------------------------------------------

def hud_icon_key(act):
    m = {"turn & talk": "turntalk"}
    a = act.lower()
    return m.get(a, a.replace("&", "").replace(" ", "_"))


def build_hud():
    out = []
    actions = T["hud_actions"]["normal"] + T["hud_actions"]["optional"]
    expected = {hud_icon_key(a) + ".svg" for a in actions}
    hud_dir = os.path.join(ASSET_ROOT, "hud")
    ensure(hud_dir)
    for stale in os.listdir(hud_dir):
        if stale.endswith(".svg") and stale not in expected:
            os.remove(os.path.join(hud_dir, stale))
    w = T["components"]["hud_bubble"]["width_pt"]
    h = T["components"]["hud_bubble"]["height_pt"]
    for act in actions:
        key = hud_icon_key(act)
        label = act.replace("&", "&amp;")
        parts = [
            rect(0, 0, w, h, fill="currentColor", rx=32),
            circle(32, 32, 18, fill="#FFFFFF"),
            f'<g transform="translate(20,20)" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">',
        ]
        parts += icon_shapes(key if key in ICONS else "check", "currentColor")
        parts.append("</g>")
        parts.append(txt(62, 39, label, 24, fill="#FFFFFF", weight="Bold"))
        out.append(write_svg(f"hud/{key}.svg", parts, w, h, color=CH["ch1"]["primary"]))
    return out


# --------------------------------------------------------------------------
# 3. Resource badges
# --------------------------------------------------------------------------

def build_badges():
    out = []
    w = T["components"]["resource_badge"]["width_pt"]
    h = T["components"]["resource_badge"]["height_pt"]
    for b in T["resource_badges"]:
        key = b.lower().replace(" ", "_")
        parts = [rect(0, 0, w, h, fill=UNIT["ink"], rx=22),
                 txt(22, 29, b, 15, fill="#FFFFFF", weight="Bold", ls="0.5")]
        out.append(write_svg(f"badges/{key}.svg", parts, w, h))
    return out


# --------------------------------------------------------------------------
# 4. Vocabulary card (one premium architecture)
# --------------------------------------------------------------------------

def build_vocabulary_card():
    w = T["components"]["vocabulary_card"]["width_pt"]
    h = T["components"]["vocabulary_card"]["height_pt"]
    prim = CH["ch1"]["primary"]
    acc = CH["ch1"]["accent"]
    parts = [
        rect(0, 0, w, h, fill="#FFFFFF", stroke=UNIT["rule"], sw=1.25, rx=12),
        rect(0, 0, w, 12, fill=prim, rx=12),
        rect(0, 6, w, 6, fill=prim),
        rect(24, 40, w - 48, 150, fill=tint(acc, 0.10), stroke=tint(acc, 0.45), sw=1, rx=8),
        txt(w / 2, 126, "Sample Vocabulary Term", 26, fill=UNIT["ink"], weight="Bold", anchor="middle"),
        txt(24, 254, "ENERGY", 64, fill=prim, weight="Bold"),
        txt(24, 288, "Sample definition line — exact Reader wording goes here.", 18, fill=UNIT["ink"]),
        txt(24, 316, "Second line of the definition, if needed.", 18, fill=UNIT["ink"]),
        txt(24, 344, "Reader p. 1", 13, fill=UNIT["ink_soft"], weight="DemiBold"),
        rect(w - 100, 328, 76, 26, fill=tint(prim, 0.10), rx=13),
        txt(w - 62, 346, "TEACH", 12, fill=prim, weight="Bold", anchor="middle"),
    ]
    return write_svg("vocabulary/vocabulary-card.svg", parts, w, h)


# --------------------------------------------------------------------------
# 5. Diagram primitives
# --------------------------------------------------------------------------

def build_diagrams():
    out = []

    def node(label, fill, textfill):
        return [rect(0, 0, 160, 60, fill=fill, stroke=UNIT["rule"], sw=1.25, rx=10),
                txt(80, 36, label, 16, fill=textfill, weight="Bold", anchor="middle")]

    out.append(write_svg("diagrams/arrow-transfer.svg",
                         [path("M10 40 H140 L150 40 L138 32 M140 40 L138 48", stroke="#1A1D26", sw=2.5)], 160, 80))
    out.append(write_svg("diagrams/arrow-motion.svg",
                         [path("M10 40 C 40 10 80 70 140 40", stroke="#1A1D26", sw=2.5)], 160, 80))
    out.append(write_svg("diagrams/arrow-transformation.svg",
                         [path("M10 40 H140 L150 40 L138 32 M140 40 L138 48", stroke="#1A1D26", sw=2.5),
                          path("M70 28 L80 40 L70 52 L60 40 Z", stroke="#1A1D26", sw=2)], 160, 80))
    out.append(write_svg("diagrams/arrow-cause-effect.svg",
                         [path("M10 40 H120 L130 40 L120 32 M120 40 L120 48 M130 40 L138 40", stroke="#1A1D26", sw=2.5)], 160, 80))

    out.append(write_svg("diagrams/node-source.svg", node("SOURCE", tint("#1F2A5A", 0.12), "#1F2A5A"), 160, 60))
    out.append(write_svg("diagrams/node-receiver.svg", node("RECEIVER", tint("#1F5C3D", 0.12), "#1F5C3D"), 160, 60))
    out.append(write_svg("diagrams/node-evidence.svg", node("EVIDENCE", tint("#C98A2D", 0.15), "#3E2C1F"), 160, 60))

    out.append(write_svg("diagrams/label-tag.svg",
                         [rect(0, 0, 140, 40, fill="#FFFFFF", stroke=UNIT["rule"], sw=1, rx=8),
                          txt(70, 26, "LABEL", 13, fill=UNIT["ink"], weight="DemiBold", anchor="middle")], 140, 40))

    w, h = 620, 200
    parts = [
        rect(0, 0, w, h, fill="#FFFFFF", stroke=UNIT["rule"], sw=1, rx=12),
        rect(24, 70, 160, 60, fill=tint("#1F2A5A", 0.12), stroke=UNIT["rule"], sw=1.25, rx=10),
        txt(104, 106, "SOURCE", 16, fill="#1F2A5A", weight="Bold", anchor="middle"),
        rect(436, 70, 160, 60, fill=tint("#1F5C3D", 0.12), stroke=UNIT["rule"], sw=1.25, rx=10),
        txt(516, 106, "RECEIVER", 16, fill="#1F5C3D", weight="Bold", anchor="middle"),
        path("M184 100 H436 L446 100 L434 92 M436 100 L434 108", stroke="#1A1D26", sw=2.5),
        txt(310, 60, "PATH", 14, fill=UNIT["ink_soft"], weight="DemiBold", anchor="middle"),
        txt(310, 24, "Sample Energy Path Diagram", 16, fill=UNIT["ink"], weight="Bold", anchor="middle"),
    ]
    out.append(write_svg("diagrams/source-path-receiver.svg", parts, w, h))
    return out


# --------------------------------------------------------------------------
# 6. Chapter theme swatches + chapter tab
# --------------------------------------------------------------------------

def build_chapter_themes():
    out = []
    for key, theme in CH.items():
        w, h = 300, 180
        parts = [
            rect(0, 0, w, h, fill="#FFFFFF", stroke=UNIT["rule"], sw=1, rx=10),
            txt(16, 28, theme["name"], 15, fill=UNIT["ink"], weight="Bold"),
            txt(16, 46, key.upper() + " · " + " · ".join(theme["keywords"]), 11, fill=UNIT["ink_soft"]),
        ]
        swatches = [("primary", theme["primary"]), ("accent", theme["accent"]),
                    ("neutral", theme["neutral"]), ("surface", theme["surface"])]
        x = 16
        for name, val in swatches:
            parts += [rect(x, 66, 60, 60, fill=val, stroke=UNIT["rule"], sw=1, rx=6),
                      txt(x + 30, 142, name, 10, fill=UNIT["ink_soft"], anchor="middle"),
                      txt(x + 30, 154, val, 10, fill=UNIT["ink"], anchor="middle")]
            x += 68
        out.append(write_svg(f"chapter-themes/{key}-palette.svg", parts, w, h))

    parts = [rect(0, 0, T["components"]["chapter_tab"]["width_pt"],
                  T["components"]["chapter_tab"]["height_pt"], fill="currentColor",
                  rx=T["components"]["chapter_tab"]["radius_pt"]),
             txt(20, 33, "CHAPTER 1 · SAMPLE CHAPTER", 16, fill="#FFFFFF", weight="Bold")]
    out.append(write_svg("chapter-themes/chapter-tab.svg", parts,
                         T["components"]["chapter_tab"]["width_pt"],
                         T["components"]["chapter_tab"]["height_pt"],
                         color=CH["ch1"]["primary"]))
    return out


# --------------------------------------------------------------------------
# 7. Sample pages
# --------------------------------------------------------------------------

def sample_slide():
    w, h = 1280, 720
    prim = CH["ch1"]["primary"]
    acc = CH["ch1"]["accent"]
    parts = [
        rect(0, 0, w, h, fill="#FFFFFF"),
        rect(40, 32, 320, 52, fill=prim, rx=10),
        txt(60, 65, "CHAPTER 1 · SAMPLE CHAPTER", 16, fill="#FFFFFF", weight="Bold"),
        rect(980, 32, 260, 44, fill=UNIT["ink"], rx=22),
        txt(1110, 61, "GUIDED NOTES", 15, fill="#FFFFFF", weight="Bold", anchor="middle"),
        txt(60, 150, "Sample Slide Title", 42, fill=prim, weight="Bold", role="content"),
        rect(40, 200, 1200, 96, fill=prim, rx=12),
        txt(80, 260, "Sample Big Question — one line, large type.", 34, fill="#FFFFFF", weight="Bold", role="content"),
        txt(60, 360, "Sample body text at 32pt for projector readability.", 32, fill=UNIT["ink"], role="content"),
        rect(40, 420, 240, 64, fill=prim, rx=32),
        txt(76, 459, "PREDICT", 24, fill="#FFFFFF", weight="Bold"),
        circle(48, 452, 16, fill="#FFFFFF"),
        rect(40, 520, 1200, 160, fill=tint(acc, 0.08), stroke=tint(acc, 0.5), sw=1.25, rx=12),
        txt(80, 610, "Sample diagram / visual region (dummy)", 28, fill=UNIT["ink_soft"], weight="DemiBold", role="content"),
    ]
    return svg_doc(w, h, parts)


def sample_notes():
    w, h = 612, 792
    prim = CH["ch1"]["primary"]
    acc = CH["ch1"]["accent"]
    M = 54
    parts = [
        rect(0, 0, w, h, fill="#FFFFFF"),
        rect(0, 0, w, 8, fill=prim),
        rect(M, 28, 168, 36, fill=UNIT["ink"], rx=18),
        txt(M + 16, 51, "GUIDED NOTES", 13, fill="#FFFFFF", weight="Bold"),
        txt(M, 96, "Sample Note Section", 26, fill=prim, weight="Bold"),
        rect(M, 116, w - 2 * M, 64, fill=prim, rx=10),
        txt(M + 20, 156, "Sample Big Question", 19, fill="#FFFFFF", weight="Bold"),
        txt(M, 220, "KEY WORDS", 16, fill=prim, weight="Bold"),
        line(M, 228, M + 90, 228, prim, 2),
    ]
    for i in range(2):
        cx = M + i * (w - 2 * M) // 2
        cw = (w - 2 * M) // 2 - 14
        parts += [
            rect(cx, 240, cw, 118, fill="#FFFFFF", stroke=UNIT["rule"], sw=1.25, rx=10),
            rect(cx, 240, cw, 8, fill=acc, rx=10),
            rect(cx, 244, cw, 4, fill=acc),
            txt(cx + 14, 282, "Sample Vocabulary Term", 15, fill=prim, weight="Bold"),
            txt(cx + 14, 306, "Sample definition line.", 12, fill=UNIT["ink"]),
            txt(cx + 14, 324, "Reader p. 1", 11, fill=UNIT["ink_soft"], weight="DemiBold"),
        ]
    parts += [
        txt(M, 396, "MODEL IT", 16, fill=prim, weight="Bold"),
        line(M, 404, M + 74, 404, prim, 2),
        txt(M, 426, "Sample note prompt with a fill-in blank: ______.", 14, fill=UNIT["ink"]),
    ]
    y = 448
    for i in range(4):
        parts.append(line(M, y, w - M, y, UNIT["rule"], 1))
        y += 32
    parts.append(txt(M, 700, "Reader pp. 1–2", 11, fill=UNIT["ink_soft"], weight="DemiBold"))
    return svg_doc(w, h, parts)


def sample_assessment():
    w, h = 612, 792
    prim = CH["ch1"]["primary"]
    M = 54
    parts = [
        rect(0, 0, w, h, fill="#FFFFFF"),
        rect(0, 0, w, 8, fill=prim),
        txt(M, 96, "SAMPLE ASSESSMENT · Section 1", 20, fill=prim, weight="Bold"),
        line(M, 108, w - M, 108, prim, 2),
        rect(w - M - 150, 36, 150, 44, fill=tint(prim, 0.10), stroke=prim, sw=1.25, rx=8),
        txt(w - M - 140, 64, "SCORE  ___ / 8", 14, fill=prim, weight="Bold"),
        txt(M, 160, "1.", 16, fill=UNIT["ink"], weight="Bold"),
        txt(M + 28, 160, "Sample question text at a readable Grade 4 size.", 15, fill=UNIT["ink"]),
    ]
    y = 190
    for i in range(3):
        parts.append(line(M + 28, y, w - M, y, UNIT["rule"], 1.25))
        y += 44
    parts += [
        txt(M, 350, "2.", 16, fill=UNIT["ink"], weight="Bold"),
        txt(M + 28, 350, "Sample explain prompt (at least two lines).", 15, fill=UNIT["ink"]),
    ]
    y = 380
    for i in range(2):
        parts.append(line(M + 28, y, w - M, y, UNIT["rule"], 1.25))
        y += 44
    parts.append(txt(M, 700, "raw score + percentage", 11, fill=UNIT["ink_soft"], weight="DemiBold"))
    return svg_doc(w, h, parts)


def sample_playbook():
    w, h = 612, 792
    prim = CH["ch1"]["primary"]
    M = 54
    parts = [
        rect(0, 0, w, h, fill="#FFFFFF"),
        rect(0, 0, w, 8, fill=prim),
        rect(M, 28, 320, 52, fill=prim, rx=10),
        txt(M + 18, 60, "CHAPTER 1 · SAMPLE CHAPTER", 16, fill="#FFFFFF", weight="Bold"),
        rect(w - M - 190, 32, 190, 44, fill=UNIT["ink"], rx=22),
        txt(w - M - 95, 61, "TEACHER PLAYBOOK", 15, fill="#FFFFFF", weight="Bold", anchor="middle"),
        txt(M, 124, "Demonstration Guide (sample)", 26, fill=prim, weight="Bold"),
        rect(M, 150, w - 2 * M, 150, fill=tint(prim, 0.06), stroke=prim, sw=1.25, rx=12),
        rect(M, 150, 6, 150, fill=prim, rx=3),
        rect(M + 24, 172, 110, 26, fill=prim, rx=13),
        txt(M + 79, 189, "MATERIALS", 12, fill="#FFFFFF", weight="Bold", anchor="middle"),
        txt(M + 24, 222, "Sample materials list — teacher-facing text.", 14, fill=UNIT["ink"]),
        rect(M, 320, w - 2 * M, 130, fill=tint(prim, 0.06), stroke=prim, sw=1.25, rx=12),
        rect(M, 320, 6, 130, fill=prim, rx=3),
        rect(M + 24, 342, 110, 26, fill=tint(prim, 0.15), rx=13),
        txt(M + 79, 359, "LISTEN-FOR", 11, fill=prim, weight="Bold", anchor="middle"),
        txt(M + 24, 392, "Sample \"listen for\" note.", 14, fill=UNIT["ink"]),
        txt(M, 490, "Teacher-note convention:", 14, fill=UNIT["ink"], weight="DemiBold"),
        txt(M, 514, "LIVE · BACKUP · TIME · ASK · LISTEN-FOR · NEXT · IF-SHORT-ON-TIME", 13, fill=UNIT["ink_soft"]),
    ]
    return svg_doc(w, h, parts)


# --------------------------------------------------------------------------
# render + contact sheet
# --------------------------------------------------------------------------

def render_png(svg_path, png_path):
    r = subprocess.run(["rsvg-convert", svg_path, "-o", png_path],
                       capture_output=True, text=True)
    return r.returncode == 0


def contact_sheet(pngs, out_path, cols=2, thumb_w=520):
    from PIL import Image, ImageDraw
    if not pngs:
        return
    imgs = []
    for p in pngs:
        try:
            im = Image.open(p)
            w0, h0 = im.size
            nh = max(1, int(h0 * thumb_w / w0))
            imgs.append((os.path.basename(p), im.resize((thumb_w, nh))))
        except Exception as e:
            print(f"  !! cannot open {p}: {e}")
    if not imgs:
        return
    pad = 12
    label_h = 18
    rows = (len(imgs) + cols - 1) // cols
    cell_w = thumb_w + pad
    cell_h = max(im.height for _, im in imgs) + label_h + pad
    sheet = Image.new("RGB", (cols * cell_w + pad, rows * cell_h + pad), "white")
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(imgs):
        r, c = divmod(i, cols)
        x = pad + c * cell_w
        y = pad + r * cell_h
        sheet.paste(im, (x, y + label_h))
        d.text((x, y), name, fill="black")
    sheet.save(out_path)
    print(f"  contact sheet -> {out_path}")


def grayscale_proof(sources, out_path, cols=3, thumb_w=360):
    from PIL import Image, ImageDraw
    imgs = []
    for p in sources:
        try:
            im = Image.open(p).convert("L")
            w0, h0 = im.size
            nh = max(1, int(h0 * thumb_w / w0))
            imgs.append((os.path.basename(p), im.resize((thumb_w, nh))))
        except Exception as e:
            print(f"  !! grayscale proof cannot open {p}: {e}")
    if not imgs:
        return False
    pad = 12
    label_h = 18
    rows = (len(imgs) + cols - 1) // cols
    cell_w = thumb_w + pad
    cell_h = max(im.height for _, im in imgs) + label_h + pad
    sheet = Image.new("RGB", (cols * cell_w + pad, rows * cell_h + pad), "white")
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(imgs):
        r, c = divmod(i, cols)
        x = pad + c * cell_w
        y = pad + r * cell_h
        sheet.paste(im, (x, y + label_h))
        d.text((x, y), name, fill="black")
    sheet.save(out_path)
    print(f"  grayscale proof -> {out_path}")
    return True


def main():
    ensure(ASSET_ROOT)
    ensure(QA_ROOT)
    assets = []
    assets += build_icons()
    assets += build_hud()
    assets += build_badges()
    assets += [build_vocabulary_card()]
    assets += build_diagrams()
    assets += build_chapter_themes()
    print(f"Generated {len(assets)} SVG assets under assets/visual-system/")

    samples = {
        "sample-slide": sample_slide(),
        "sample-notes": sample_notes(),
        "sample-assessment": sample_assessment(),
        "sample-playbook": sample_playbook(),
    }
    sample_dir = os.path.join(QA_ROOT, "samples")
    ensure(sample_dir)
    rendered = []
    for name, content in samples.items():
        sp = os.path.join(sample_dir, f"{name}.svg")
        with open(sp, "w") as f:
            f.write(content)
        pp = os.path.join(sample_dir, f"{name}.png")
        if render_png(sp, pp):
            rendered.append(pp)
            print(f"  sample -> {pp}")
        else:
            print(f"  !! render failed: {sp}")

    asset_pngs = []
    for a in assets:
        rel = os.path.relpath(a, ASSET_ROOT)
        pp = os.path.join(QA_ROOT, "assets", os.path.splitext(rel)[0] + ".png")
        ensure(os.path.dirname(pp))
        if render_png(a, pp):
            asset_pngs.append(pp)

    contact_sheet(rendered, os.path.join(QA_ROOT, "contact_sheet.png"), cols=2, thumb_w=520)
    print(f"Rendered {len(asset_pngs)} asset PNGs + {len(rendered)} sample PNGs.")

    # Grayscale proof (non-production; demonstrates B/W print usability)
    gray_sources = [
        os.path.join(sample_dir, "sample-notes.png"),
        os.path.join(sample_dir, "sample-assessment.png"),
        os.path.join(sample_dir, "sample-slide.png"),
        os.path.join(QA_ROOT, "assets", "vocabulary", "vocabulary-card.png"),
    ] + [os.path.join(QA_ROOT, "assets", "chapter-themes", f"ch{i}-palette.png") for i in range(1, 8)]
    grayscale_proof(gray_sources, os.path.join(QA_ROOT, "grayscale_proof.png"), cols=3, thumb_w=360)


if __name__ == "__main__":
    main()
