"""Teacher lab setup diagrams (x4) — one-page setup guides with a clean, grayscale-printable
top-down/side-view diagram each. Output: DOCX master + PDF export (via soffice).

Labs:
  A. Ramp It Up (Wk2 Thu)
  B. Crash Lab (Wk3 Thu)
  C. Water Wheel (Wk7 Thu)
  D. Available-Light Solar Device (Wk8 Thu)

Diagram convention (grayscale-safe):
  - objects = black outlines, white/light-gray fills
  - CHANGE variable = dark-gray fill + thick outline
  - KEEP SAME = light-gray fill + label
  - MEASURE = white fill + thick outline + measurement arrows
  - legend at the bottom of each diagram
"""
import os, sys, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gn_design import *
from docx.shared import Inches

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
    "production", "lab-setup-guides"))
os.makedirs(OUT_DIR, exist_ok=True)
SVG_DIR = os.path.join(OUT_DIR, "source")   # committed editable diagram source
os.makedirs(SVG_DIR, exist_ok=True)

SINK = "#1F1F1F"
GRAY_L = "#E4E4E4"
GRAY_M = "#B9B9B9"
GRAY_D = "#5A5A5A"
WHITE = "#FFFFFF"

# ------------------------------------------------------------------ SVG primitives
ARROW_MARKER = '<marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="3" ' \
    'orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,3 L0,6 z" fill="{c}"/></marker>'

def svg_open(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'font-family="Arial, Helvetica, sans-serif">\n<defs>{ARROW_MARKER.format(c=SINK)}'
            f'{ARROW_MARKER.format(c=GRAY_D)}</defs>\n'
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="#FFFFFF"/>\n')

def r(x, y, w, h, fill=WHITE, stroke=SINK, sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>\n'

def line(x1, y1, x2, y2, stroke=SINK, sw=2, dash=None, marker=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    m = f' marker-end="url(#arr)"' if marker else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}{m}/>\n'

def txt(x, y, s, size=20, weight="normal", anchor="start", fill=SINK, italic=False):
    st = ' font-style="italic"' if italic else ''
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{fill}"{st}>{s}</text>\n')

def circle(cx, cy, rad, fill=WHITE, stroke=SINK, sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>\n'

def label_box(x, y, w, text, fill=GRAY_L, sw=2, size=20, weight="bold", anchor="middle", color=SINK):
    return (r(x, y, w, 46, fill=fill, stroke=SINK, sw=sw) +
            txt(x + w/2, y + 31, text, size=size, weight=weight, anchor=anchor, fill=color))

def legend(x, y, items):
    """items = [(fill, stroke, sw, label), ...] rendered as a row of swatch+label."""
    out = ""
    cx = x
    for fill, stroke, sw, label in items:
        out += r(cx, y, 34, 34, fill=fill, stroke=stroke, sw=sw)
        out += txt(cx + 42, y + 26, label, size=19)
        cx += 42 + len(label) * 11 + 30
    return out

# ------------------------------------------------------------------ A. Ramp It Up
def diagram_ramp():
    out = svg_open(1000, 560)
    # ground line
    out += line(60, 470, 940, 470, sw=3)
    # book stack (3 books) at left
    for i, (by, bh) in enumerate([(430, 40), (390, 40), (350, 40)]):
        out += r(120, by, 220, bh, fill=GRAY_L)
        out += txt(360, by + 28, f"book {i+1}", size=16, anchor="end", fill=GRAY_D)
    # CHANGE bracket (up/down arrow over the stack)
    out += line(350, 330, 350, 300, sw=3, marker="arr")
    out += line(350, 380, 350, 410, sw=3, marker="arr")
    out += label_box(150, 250, 200, "CHANGE", fill=GRAY_D, color=WHITE)
    out += txt(245, 316, "ramp height", size=19, weight="bold", anchor="start")
    out += txt(245, 344, "1 / 2 / 3 books", size=17, anchor="start", fill=GRAY_D)
    # ramp board from top book down to ground
    out += line(120, 350, 470, 470, sw=5)
    out += r(90, 336, 40, 16, fill=GRAY_D, stroke=SINK, sw=1)  # ramp top cap
    # ball on ramp at release point (dashed vertical)
    out += circle(155, 398, 16, fill=GRAY_D, stroke=SINK, sw=2)
    out += line(180, 350, 180, 470, sw=2, dash="6,4")
    out += txt(188, 360, "release point (SAME)", size=17, anchor="start", fill=GRAY_D)
    # target cup at ramp end
    out += r(470, 430, 46, 40, fill=GRAY_L)
    out += line(470, 430, 452, 470, sw=2)
    out += line(516, 430, 534, 470, sw=2)
    out += txt(460, 520, "target cup", size=17, weight="bold")
    # displacement arrow to the right
    out += line(520, 452, 660, 452, sw=3, marker="arr")
    out += txt(585, 442, "cup displacement", size=18, weight="bold", anchor="middle")
    out += txt(585, 540, "MEASURE", size=18, weight="bold", anchor="middle", fill=GRAY_D)
    # measuring ruler along ground
    out += r(520, 500, 200, 10, fill=WHITE, stroke=SINK, sw=2)
    for k in range(0, 201, 40):
        out += line(520 + k, 500, 520 + k, 510, sw=1)
    out += txt(560, 555, "ruler (cm)", size=15, anchor="middle", fill=GRAY_D)
    # KEEP SAME note
    out += txt(760, 300, "KEEP SAME:", size=18, weight="bold")
    for dy, s in [(30, "ball"), (58, "release point"), (86, "target cup"), (114, "surface")]:
        out += txt(770, 300 + dy, s, size=17, fill=GRAY_D)
    # legend
    out += legend(60, 150, [(GRAY_D, SINK, 2, "CHANGE"), (GRAY_L, SINK, 2, "KEEP SAME"), (WHITE, SINK, 3, "MEASURE")])
    out += "</svg>\n"
    return out

# ------------------------------------------------------------------ B. Crash Lab
def diagram_crash():
    out = svg_open(1000, 560)
    # lane (top view) surface
    out += r(60, 120, 880, 240, fill="#FBFBFB", stroke=SINK, sw=2)
    out += txt(80, 150, "lane surface (SAME)", size=16, fill=GRAY_D)
    # ramp at left
    out += r(110, 180, 120, 120, fill=GRAY_L, stroke=SINK, sw=2)
    out += txt(170, 240, "ramp", size=18, weight="bold", anchor="middle")
    # book height stack indicator
    out += line(170, 160, 170, 130, sw=3, marker="arr")
    out += txt(150, 118, "1 / 2 / 3 books", size=16, anchor="end")
    out += label_box(300, 96, 200, "CHANGE", fill=GRAY_D, color=WHITE)
    out += txt(305, 180, "ramp height", size=18, weight="bold", anchor="start")
    out += txt(305, 206, "(= speed condition)", size=16, anchor="start", fill=GRAY_D)
    # car
    out += r(250, 225, 70, 34, fill=GRAY_D, stroke=SINK, sw=2)
    out += circle(268, 262, 7, fill=WHITE)
    out += circle(302, 262, 7, fill=WHITE)
    out += txt(285, 288, "car (SAME)", size=16, anchor="middle", fill=GRAY_D)
    # motion arrow
    out += line(330, 242, 470, 242, sw=3, marker="arr")
    # target
    out += r(470, 210, 46, 60, fill=GRAY_L)
    out += txt(470, 292, "target", size=16, anchor="middle")
    # displacement measurement area
    out += line(520, 240, 760, 240, sw=3, marker="arr")
    out += txt(640, 228, "target displacement", size=18, weight="bold", anchor="middle")
    out += txt(640, 336, "MEASURE", size=18, weight="bold", anchor="middle", fill=GRAY_D)
    out += r(520, 300, 240, 10, fill=WHITE, stroke=SINK, sw=2)
    for k in range(0, 241, 48):
        out += line(520 + k, 300, 520 + k, 310, sw=1)
    out += txt(640, 352, "ruler (cm)", size=15, anchor="middle", fill=GRAY_D)
    # sound note
    out += txt(800, 250, "sound =", size=17, anchor="start")
    out += txt(800, 276, "QUALITATIVE only", size=16, weight="bold", anchor="start")
    out += txt(800, 300, "(louder / quieter)", size=15, anchor="start", fill=GRAY_D)
    # Part B optional
    out += r(60, 390, 880, 120, fill=GRAY_L, stroke=GRAY_D, sw=2, dash="8,5")
    out += txt(80, 422, "PART B (OPTIONAL — separate fair test)", size=18, weight="bold")
    out += txt(80, 452, "CHANGE: car mass (1 / 2 / 3 cars taped)  ·  KEEP SAME: ramp height, target, surface", size=16)
    out += txt(80, 478, "Never change speed AND mass at once.", size=15, italic=True, fill=GRAY_D)
    out += legend(60, 60, [(GRAY_D, SINK, 2, "CHANGE"), (GRAY_L, SINK, 2, "KEEP SAME"), (WHITE, SINK, 3, "MEASURE")])
    out += "</svg>\n"
    return out

# ------------------------------------------------------------------ C. Water Wheel
def diagram_waterwheel():
    out = svg_open(1000, 580)
    # water source cup with spout, three locked pour heights
    out += r(70, 90, 130, 90, fill=GRAY_L)
    out += txt(135, 150, "pour cup", size=17, weight="bold", anchor="middle")
    out += txt(135, 200, "(SAME opening)", size=15, anchor="middle", fill=GRAY_D)
    out += line(200, 120, 250, 170, sw=3)  # spout
    for hy, lab in [(100, "15 cm"), (150, "30 cm"), (200, "45 cm")]:
        out += line(200, 135, 260, hy + 20, sw=2, dash="5,4")
        out += txt(268, hy + 24, lab, size=15, anchor="start", fill=GRAY_D)
    out += line(200, 90, 200, 230, sw=3, marker="arr")
    out += label_box(300, 60, 200, "CHANGE", fill=GRAY_D, color=WHITE)
    out += txt(305, 200, "pour height", size=18, weight="bold", anchor="start")
    # water stream
    out += line(255, 185, 360, 300, sw=4, stroke=GRAY_D)
    # wheel
    out += circle(420, 300, 90, fill=WHITE, stroke=SINK, sw=3)
    out += circle(420, 300, 12, fill=GRAY_D)
    for ang in range(0, 360, 45):
        import math
        x1 = 420 + 90 * math.cos(math.radians(ang))
        y1 = 300 + 90 * math.sin(math.radians(ang))
        x2 = 420 + 24 * math.cos(math.radians(ang))
        y2 = 300 + 24 * math.sin(math.radians(ang))
        out += line(x1, y1, x2, y2, sw=3)
    out += txt(420, 430, "wheel + blades (SAME)", size=16, anchor="middle", fill=GRAY_D)
    # axle + thread + load
    out += line(420, 312, 420, 470, sw=3)  # thread from axle
    out += r(392, 470, 56, 30, fill=GRAY_D, stroke=SINK, sw=2)  # paperclip load
    out += txt(420, 492, "paperclip load", size=16, anchor="middle")
    out += txt(420, 520, "MEASURE: paperclips lifted", size=17, weight="bold", anchor="middle", fill=GRAY_D)
    # catch tray
    out += r(300, 545, 280, 24, fill=GRAY_L, stroke=SINK, sw=2)
    out += txt(440, 562, "catch basin / tray", size=15, anchor="middle", fill=GRAY_D)
    # KEEP SAME note
    out += txt(580, 120, "KEEP SAME:", size=18, weight="bold")
    for dy, s in [(30, "wheel"), (56, "blade setup"), (82, "water volume (500 mL)"), (108, "pour opening"), (134, "thread / load system")]:
        out += txt(590, 120 + dy, s, size=16, fill=GRAY_D)
    # containment note
    out += txt(580, 300, "CONTAINMENT:", size=17, weight="bold")
    out += txt(590, 326, "pour over the basin only", size=16)
    out += txt(590, 350, "wipe spills immediately", size=16)
    out += legend(60, 40, [(GRAY_D, SINK, 2, "CHANGE"), (GRAY_L, SINK, 2, "KEEP SAME"), (WHITE, SINK, 3, "MEASURE")])
    out += "</svg>\n"
    return out

# ------------------------------------------------------------------ D. Solar Device
def diagram_solar():
    out = svg_open(1000, 560)
    # three condition columns
    out += txt(500, 50, "SAME device · SAME measurement method · CHANGE ONLY the light", size=19, weight="bold", anchor="middle")
    # device (top view) on a stand
    out += r(430, 90, 140, 90, fill=GRAY_L, stroke=SINK, sw=2)
    out += r(450, 100, 40, 26, fill=GRAY_D)  # solar cell
    out += circle(550, 150, 12, fill=GRAY_D)  # LED
    out += txt(500, 120, "solar device", size=16, anchor="middle", fill=GRAY_D)
    # light sources
    out += circle(700, 130, 40, fill=GRAY_D)  # sun (bright/close)
    for k in range(0, 8):
        import math
        x1 = 700 + 52 * math.cos(math.radians(k * 45 + 22))
        y1 = 130 + 52 * math.sin(math.radians(k * 45 + 22))
        x2 = 700 + 46 * math.cos(math.radians(k * 45 + 22))
        y2 = 130 + 46 * math.sin(math.radians(k * 45 + 22))
        out += line(x1, y1, x2, y2, sw=2)
    out += txt(700, 200, "bright / close", size=17, weight="bold", anchor="middle")
    out += circle(700, 300, 40, fill=GRAY_M)  # dim/far
    out += txt(700, 370, "dim / far", size=17, weight="bold", anchor="middle")
    out += r(640, 420, 120, 70, fill=GRAY_L, stroke=SINK, sw=2)  # shade
    out += txt(700, 440, "shaded", size=17, weight="bold", anchor="middle")
    out += txt(700, 466, "(card/box shade)", size=14, anchor="middle", fill=GRAY_D)
    # arrows from light to device
    out += line(660, 130, 570, 130, sw=3, marker="arr")
    out += line(660, 300, 570, 180, sw=3, marker="arr", stroke=GRAY_D)
    out += line(640, 455, 570, 180, sw=3, marker="arr", stroke=GRAY_D)
    # output observation
    out += txt(360, 180, "MEASURE:", size=18, weight="bold", fill=GRAY_D)
    out += txt(370, 210, "observable device output", size=16)
    out += txt(370, 234, "(LED on/off, brightness)", size=15, fill=GRAY_D)
    # CHANGE / KEEP SAME
    out += label_box(80, 300, 200, "CHANGE", fill=GRAY_D, color=WHITE)
    out += txt(85, 356, "available light", size=17, weight="bold", anchor="start")
    out += txt(85, 380, "condition", size=17, weight="bold", anchor="start")
    out += txt(80, 420, "KEEP SAME:", size=17, weight="bold")
    out += txt(90, 446, "device · method", size=16, fill=GRAY_D)
    # indoor lamp backup note
    out += r(80, 470, 820, 64, fill=GRAY_L, stroke=GRAY_D, sw=2, dash="8,5")
    out += txt(100, 496, "INDOOR BACKUP:", size=16, weight="bold")
    out += txt(220, 496, "one consistent lamp/flashlight per group — same lamp, same distance for every trial.", size=15)
    out += txt(100, 522, "Test each kit with the lamp the day before so the LED responds. Low-voltage cells only.", size=15, italic=True)
    out += legend(80, 250, [(GRAY_D, SINK, 2, "CHANGE"), (GRAY_L, SINK, 2, "KEEP SAME"), (WHITE, SINK, 3, "MEASURE")])
    out += "</svg>\n"
    return out

# ------------------------------------------------------------------ DOCX assembly
def render_svg(svg, name):
    svg_path = os.path.join(SVG_DIR, name + ".svg")
    with open(svg_path, "w") as f:
        f.write(svg)
    tmp = tempfile.mkdtemp(prefix="labdiagram_")
    png_path = os.path.join(tmp, name + ".png")
    subprocess.run(["rsvg-convert", "-z", "1.6", "-o", png_path, svg_path], check=True)
    return png_path

def add_var_table(doc, change, keep, measure):
    data_table(doc, ["Change", "Keep the same", "Measure"],
        [(change, keep, measure)],
        col_widths=(2600, 4400, 3080), row_h=900)

def labeled_para(doc, lead, text, size=12):
    """Compact bold-lead paragraph to keep each guide to one page."""
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    sp = OxmlElement('w:spacing'); sp.set(qn('w:after'), '60'); pPr.append(sp)
    set_run(p.add_run(lead + "  "), size=size, bold=True, color=NAVY, caps=True)
    set_run(p.add_run(text), size=size, color=INK)
    return p

def guide(doc, title, week, diagram_name, svg, change, keep, measure,
          materials, per_group, safety, reset, prep):
    heading(doc, title, 18, before=0)
    body(doc, week + "  ·  Teacher setup guide  ·  TEACHER ONLY (laminate for prep binder)", size=11, italic=True, color=GRAY, after=10)
    png = render_svg(svg, diagram_name)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(png, width=Inches(6.55))
    sp = doc.add_paragraph()
    spPr = sp._p.get_or_add_pPr()
    spelm = OxmlElement('w:spacing'); spelm.set(qn('w:after'), '30'); spPr.append(spelm)
    add_var_table(doc, change, keep, measure)
    labeled_para(doc, "Materials", " · ".join(materials))
    labeled_para(doc, "Per group", per_group)
    labeled_para(doc, "Safety", safety)
    labeled_para(doc, "Reset / cleanup", reset)
    labeled_para(doc, "Prep note", prep)

def build():
    specs = [
        dict(fn="ramp-it-up-setup-guide", title="Ramp It Up — Setup Diagram",
             week="Week 2 · Thursday", dname="ramp", svg=diagram_ramp(),
             change="ramp height (1 / 2 / 3 books)",
             keep="ball · release point · target cup · surface",
             measure="cup displacement (cm)",
             materials=["ramp board (or stacked books)", "ONE identical ball type", "books/blocks (3 heights)",
                        "target cup", "meter stick / ruler (cm)", "tape (release-point marker)"],
             per_group="1 ramp · 1 ball · 3 books · 1 cup · 1 ruler · tape",
             safety="Clear the roll path; balls ROLL (never thrown); fixed release point.",
             reset="Return balls/books/cups; remove tape marks; straighten rulers.",
             prep="Pre-build 5 identical stations; mark the release point and start line the same on every ramp."),
        dict(fn="crash-lab-setup-guide", title="Crash Lab — Setup Diagram",
             week="Week 3 · Thursday", dname="crash", svg=diagram_crash(),
             change="speed condition / ramp height (1 / 2 / 3 books)",
             keep="car · target · surface",
             measure="target displacement (cm)",
             materials=["identical toy car (SAME type)", "ramp (cardboard/wood)", "books/blocks (3 heights)",
                        "target: plastic cup or small block", "meter stick / ruler (cm)", "tape (start line)",
                        "Part B only: 2 extra cars + tape (mass comparison)"],
             per_group="1 car (Part A) · 3 books · 1 target · 1 ruler · tape · (Part B: +2 cars)",
             safety="Clear the crash lane; cars ROLL (never thrown); Newton's cradle = teacher demo only; no heat measurement.",
             reset="Return cars/ramps/targets; reset lanes; remove tape.",
             prep="Use IDENTICAL cars for Part A. Part B (mass) is OPTIONAL and a SEPARATE fair test — never change speed and mass together."),
        dict(fn="water-wheel-setup-guide", title="Water Wheel — Setup Diagram",
             week="Week 7 · Thursday", dname="wheel", svg=diagram_waterwheel(),
             change="pour height (15 / 30 / 45 cm)",
             keep="wheel · blade setup · water volume (500 mL) · pour opening · thread/load system",
             measure="paperclips lifted (final locked primary response)",
             materials=["paper plate / plastic lid wheel", "8–10 blade cups or popsicle-stick blades",
                        "straw / dowel axle", "~50 cm thread", "paperclips (load)", "pour cup (fixed opening)",
                        "500 mL water source", "basin / tray (catch)", "ruler (height)", "towel"],
             per_group="1 wheel + axle · ~50 cm thread · paperclips · 1 pour cup · 500 mL water · 1 basin · 1 ruler · 1 towel",
             safety="Pour over the basin only; wipe spills immediately; no horseplay near water.",
             reset="Dry wheels/blades/basins; dispose water in a sink; respool thread; return paperclips.",
             prep="Build wheels Wed; fill pitchers Thu. Lock the pour height with a marked ruler; same 500 mL and same opening every trial."),
        dict(fn="solar-device-setup-guide", title="Available-Light Solar Device — Setup Diagram",
             week="Week 8 · Thursday", dname="solar", svg=diagram_solar(),
             change="available light condition (bright/close · dim/far · shaded)",
             keep="device · measurement method",
             measure="observable device output (LED on/off, brightness)",
             materials=["small solar cell + LED", "flashlight / desk lamp (indoor backup)",
                        "card or box (for the shaded condition)", "observation sheet", "low-voltage cell only"],
             per_group="1 solar device · 1 lamp/flashlight · 1 shade card · 1 observation sheet",
             safety="Keep the panel at a shallow angle; do NOT look directly at the sun; low-voltage cells only.",
             reset="Store solar kits; return lamps; file observation sheets.",
             prep="PRIMARY = window/outdoor light; BACKUP = one consistent lamp per group (same lamp, same distance). Test each kit with the lamp the day before."),
    ]
    for spec in specs:
        doc = new_doc()
        guide(doc, spec["title"], spec["week"], spec["dname"], spec["svg"],
              spec["change"], spec["keep"], spec["measure"], spec["materials"],
              spec["per_group"], spec["safety"], spec["reset"], spec["prep"])
        doc.save(os.path.join(OUT_DIR, spec["fn"] + ".docx"))
        print("saved", spec["fn"] + ".docx")

if __name__ == "__main__":
    build()
    print("DONE")
