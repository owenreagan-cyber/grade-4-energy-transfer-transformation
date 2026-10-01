#!/usr/bin/env python3
"""Phase 13X — rebuild Unit 1 + Unit 2 final assessments to the locked 25/50 standard.

Generates: 2 student DOCX + 2 teacher key DOCX, plus diagram PNGs.
PDF export is done separately via soffice (see build steps in this script's __main__).
"""
import os
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT = "Calibri"
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
ARIAL_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
DIAG_DIR = "assets/assessment-diagrams"
DPI = 200

BLACK = (0, 0, 0)
GRAY_FILL = (240, 240, 240)
GRAY_LINE = (60, 60, 60)

os.makedirs(DIAG_DIR, exist_ok=True)


# ---------------------------------------------------------------- diagrams
def _f(size, bold=False):
    return ImageFont.truetype(ARIAL_B if bold else ARIAL, size)


def _box(d, x, y, w, h, text, font, fill=GRAY_FILL, outline=GRAY_LINE):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=fill, outline=outline, width=2)
    _ctext(d, x + w // 2, y + h // 2, text, font)


def _ctext(d, cx, cy, text, font, fill=BLACK):
    lines = text.split("\n")
    # approximate line height
    asc, desc = font.getmetrics()
    lh = asc + desc
    total = lh * len(lines)
    y = cy - total // 2
    for ln in lines:
        w = d.textlength(ln, font=font)
        d.text((cx - w // 2, y), ln, font=font, fill=fill)
        y += lh


def _arrow(d, x1, y, x2, color=GRAY_LINE, w=4):
    d.line([(x1, y), (x2, y)], fill=color, width=w)
    ah = 12
    d.polygon([(x2, y), (x2 - ah, y - ah // 2), (x2 - ah, y + ah // 2)], fill=color)


def _label(d, cx, y, text, font, fill=BLACK):
    w = d.textlength(text, font=font)
    d.text((cx - w // 2, y), text, font=font, fill=fill)


def _text_w(d, text, font):
    return max(d.textlength(ln, font=font) for ln in text.split("\n"))


def flow_diagram(items, outname, w_in=6.0, h_in=1.4, font_px=34, title=None):
    """items: list of box labels; draw horizontal flow with arrows, auto-sized boxes."""
    W = int(w_in * DPI)
    H = int(h_in * DPI)
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    font = _f(font_px)
    n = len(items)
    gap = 46
    box_w = [int(_text_w(d, it, font)) + 26 for it in items]
    total = sum(box_w) + gap * (n - 1)
    x = max(8, (W - total) // 2)
    box_h = int(H * 0.72)
    by = int(H * 0.14)
    if title:
        _ctext(d, W // 2, int(H * 0.06), title, _f(font_px, bold=True))
    for i, it in enumerate(items):
        _box(d, x, by, box_w[i], box_h, it, font)
        if i < n - 1:
            _arrow(d, x + box_w[i], by + box_h // 2, x + box_w[i] + gap)
        x += box_w[i] + gap
    img.save(os.path.join(DIAG_DIR, outname))


def cycle_diagram(items, outname, w_in=3.6, h_in=1.3, font_px=34):
    """4-step cycle drawn as 4 boxes with right-arrow and loop-back arrow."""
    W = int(w_in * DPI)
    H = int(h_in * DPI)
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    font = _f(font_px)
    n = len(items)
    gap = 44
    box_w = [int(_text_w(d, it, font)) + 22 for it in items]
    total = sum(box_w) + gap * (n - 1)
    x = max(8, (W - total) // 2)
    box_h = int(H * 0.52)
    by = int(H * 0.22)
    xs = []
    for i, it in enumerate(items):
        _box(d, x, by, box_w[i], box_h, it, font)
        if i < n - 1:
            _arrow(d, x + box_w[i], by + box_h // 2, x + box_w[i] + gap)
        xs.append(x)
        x += box_w[i] + gap
    # loop-back arrow below
    last_x = xs[-1]
    first_x = xs[0]
    ly = by + box_h + 20
    d.line([(last_x + box_w[-1] // 2, by + box_h), (last_x + box_w[-1] // 2, ly),
            (first_x + box_w[0] // 2, ly)], fill=GRAY_LINE, width=4)
    d.polygon([(first_x + box_w[0] // 2, by + box_h),
               (first_x + box_w[0] // 2 - 9, ly - 7),
               (first_x + box_w[0] // 2 + 9, ly - 7)], fill=GRAY_LINE)
    img.save(os.path.join(DIAG_DIR, outname))


def ramp_diagram(outname, w_in=6.0, h_in=1.5):
    """Same ball on a low ramp vs a high ramp."""
    W = int(w_in * DPI)
    H = int(h_in * DPI)
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    lab = _f(34)
    cx1 = int(W * 0.30)
    cx2 = int(W * 0.70)
    _label(d, cx1, int(H * 0.04), "LOW RAMP (slower)", lab)
    base_y = int(H * 0.74)
    # low ramp (left) — shallow slope
    d.line([(cx1 - 180, base_y), (cx1 + 180, base_y)], fill=GRAY_LINE, width=3)
    d.line([(cx1 - 160, base_y), (cx1 - 20, base_y - 80), (cx1 + 160, base_y - 80)], fill=GRAY_LINE, width=5)
    d.ellipse([cx1 + 110, base_y - 100, cx1 + 165, base_y - 45], fill=GRAY_FILL, outline=BLACK, width=3)
    # high ramp (right) — steeper slope
    _label(d, cx2, int(H * 0.04), "HIGH RAMP (faster)", lab)
    d.line([(cx2 - 180, base_y), (cx2 + 180, base_y)], fill=GRAY_LINE, width=3)
    d.line([(cx2 - 160, base_y), (cx2 - 20, base_y - 150), (cx2 + 160, base_y - 150)], fill=GRAY_LINE, width=5)
    d.ellipse([cx2 + 110, base_y - 170, cx2 + 165, base_y - 115], fill=GRAY_FILL, outline=BLACK, width=3)
    img.save(os.path.join(DIAG_DIR, outname))


def collision_diagram(outname, w_in=6.0, h_in=1.6):
    """BEFORE: car -> target ; AFTER: car stopped, target moved (centered)."""
    W = int(w_in * DPI)
    H = int(h_in * DPI)
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    f = _f(34)
    fb = _f(34, bold=True)
    car_w, car_h = 220, 84
    tgt_w = 140
    # BEFORE row (centered)
    _label(d, W // 2, 6, "BEFORE", fb)
    y1 = 42
    g1 = (W - (car_w + 60 + tgt_w)) // 2
    _box(d, g1, y1, car_w, car_h, "car", f)
    _arrow(d, g1 + car_w, y1 + car_h // 2, g1 + car_w + 60)
    _box(d, g1 + car_w + 60, y1, tgt_w, car_h, "target", f)
    # AFTER row (centered)
    _label(d, W // 2, 170, "AFTER", fb)
    y2 = 206
    g2w = car_w + 120 + tgt_w + 70 + 100
    g2 = (W - g2w) // 2
    _box(d, g2, y2, car_w, 100, "car\n(stopped)", f)
    tgt_x = g2 + car_w + 120
    _box(d, tgt_x, y2, tgt_w, 100, "target", f)
    _arrow(d, tgt_x + tgt_w, y2 + 50, tgt_x + tgt_w + 70)
    _label(d, tgt_x + tgt_w + 160, y2 + 50, "moved", f)
    img.save(os.path.join(DIAG_DIR, outname))


def source_path_receiver(outname, w_in=6.0, h_in=1.2):
    flow_diagram(["tapped cup\n(SOURCE)", "sound travels\n(PATH)", "paper moves\n(RECEIVER)"],
                 outname, w_in=w_in, h_in=h_in, font_px=34)


def flashlight_diagram(outname, w_in=4.0, h_in=1.2):
    flow_diagram(["battery", "wires", "bulb", "light"], outname, w_in=w_in, h_in=h_in, font_px=34)


def solar_diagram(outname, w_in=4.0, h_in=1.2):
    flow_diagram(["sunlight", "solar cell", "electricity"], outname, w_in=w_in, h_in=h_in, font_px=34)


def fuel_pathway(outname, w_in=6.8, h_in=1.3):
    flow_diagram(["burn fuel", "heat water\ninto steam", "spin\nturbine", "turn\ngenerator", "electricity"],
                 outname, w_in=w_in, h_in=h_in, font_px=34)


def nuclear_pathway(outname, w_in=6.0, h_in=1.2):
    flow_diagram(["nuclear heat", "steam", "turbine", "generator"], outname, w_in=w_in, h_in=h_in, font_px=34)


def hydro_diagram(outname, w_in=6.0, h_in=1.2):
    flow_diagram(["reservoir", "dam", "turbine", "generator"], outname, w_in=w_in, h_in=h_in, font_px=34)


# ---------------------------------------------------------------- docx helpers
def _set_font(run, size, bold=False, name=FONT):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    rfonts.set(qn('w:ascii'), name)
    rfonts.set(qn('w:hAnsi'), name)


def _para(doc, text=None, size=13.5, bold=False, align=None, space_after=4, space_before=0):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    if text is not None:
        r = p.add_run(text)
        _set_font(r, size, bold)
    return p


def _rich(doc, parts, size=13.5, space_after=4, space_before=0, align=None):
    """parts: list of (text, bold) tuples."""
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    for text, bold in parts:
        r = p.add_run(text)
        _set_font(r, size, bold)
    return p


def add_image_centered(doc, path, width_in):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run()
    run.add_picture(path, width=Inches(width_in))
    return p


def set_cell_margins(cell, top=20, bottom=20, left=80, right=80):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    mar = OxmlElement('w:tcMar')
    for tag, val in (('top', top), ('bottom', bottom), ('start', left), ('end', right)):
        e = OxmlElement(f'w:{tag}')
        e.set(qn('w:w'), str(val))
        e.set(qn('w:type'), 'dxa')
        mar.append(e)
    tcPr.append(mar)


# ---------------------------------------------------------------- data
U1_TERMS = [
    ("Energy Transfer", "F"),
    ("Stored Energy", "I"),
    ("Speed", "E"),
    ("Collision", "G"),
    ("Energy of Motion", "J"),
    ("Criteria", "H"),
    ("Energy Transformation", "C"),
    ("Energy", "B"),
]
U1_DEFS = [
    ("A", "The things that limit what can be used in a design.", True),
    ("B", "The ability to cause change.", False),
    ("C", "Energy changing from one form to another form.", False),
    ("D", "A form of energy that comes from a vibrating object.", True),
    ("E", "A measurement of the distance an object travels over an amount of time.", False),
    ("F", "Energy moving from one place or object to another.", False),
    ("G", "When two objects come together with impact.", False),
    ("H", "The things a good design must do or have.", False),
    ("I", "Energy that can cause a change at a later time.", False),
    ("J", "The energy an object has while it is moving.", False),
    ("K", "The process of an object changing position.", True),
]
# MC: (stem, [A,B,C,D], correct_letter, diagram_path_or_None, diagram_width)
U1_MC = [
    ("What does energy allow an object or a system to do?",
     ["Stay exactly the same forever", "Disappear without leaving a trace",
      "Cause a change", "Become invisible"], "C", None, None),
    ("The same ball rolls down two ramps. One ramp is low and one ramp is high. On which ramp will the ball most likely have more energy of motion at the bottom?",
     ["The high ramp, because the ball moves faster at the bottom",
      "The low ramp, because it is closer to the ground",
      "Both ramps, because it is the same ball",
      "Neither ramp, because ramp height does not matter"], "A", "ramp.png", 6.0),
    ("A battery in a flashlight that is turned off is an example of stored energy. What can stored energy do?",
     ["It disappears as soon as the flashlight is turned off",
      "It can only be stored inside a rubber band",
      "It always turns into light right away",
      "It can cause a change later, when the flashlight is turned on"], "D", None, None),
    ("After the crash, the rolling car stops and the target moves. What does this change tell us?",
     ["The energy disappeared when the car stopped",
      "Energy of motion transferred from the car to the target",
      "The target made its own energy",
      "No energy was involved in the crash"], "B", "collision.png", 6.0),
    ("In the diagram, energy leaves the tapped cup, travels through the air, and makes the paper move. What is this called?",
     ["Stored energy", "A transformation of light", "Energy transfer", "Energy of motion only"],
     "C", "source-path.png", 6.0),
    ("Which of these is an example of an energy TRANSFORMATION?",
     ["Energy moving from a warm cup to a cooler one",
      "A light bulb changing electrical energy into light",
      "A moving ball rolling across the floor",
      "Sound traveling through the air"], "B", None, None),
    ("Students are building a tabletop signal device that must make a sound. They may use only the materials in their box. The rule that they may use only the materials in their box is a ____.",
     ["Constraint", "Criterion", "Transformation", "Transfer"], "A", None, None),
    ("A student sees a light turn on and a fan begin to spin. How do we know energy was involved?",
     ["We can see energy itself moving",
      "Energy is involved only when something makes a sound",
      "The objects changed on their own without energy",
      "We observe the changes and use them as evidence"], "D", None, None),
    ("Which of these shows energy transferring from one place to another?",
     ["A battery sitting unused in a drawer", "A flashlight lighting a card across the room",
      "A pencil lying still on a desk", "A ball resting on the floor"], "B", None, None),
    ("Which object has stored energy that can cause a change later?",
     ["A ball that is already rolling across the floor", "A cup that just stopped moving",
      "A stretched rubber band ready to snap", "A paper that already fell to the ground"], "C", None, None),
    ("A car drives slowly through a parking lot and then fast on a highway. When does the car have more energy of motion?",
     ["When it is moving fast", "When it is moving slowly",
      "The car has the same energy of motion the whole time",
      "The car has no energy of motion on the highway"], "A", None, None),
    ("A flashlight changes stored energy in the battery into light. At the same time, energy moves through the wires to the bulb. Which is happening?",
     ["Transfer only", "Transformation only", "Neither transfer nor transformation",
      "Both transfer and transformation"], "D", "flashlight.png", 4.0),
    ("A student rolls the SAME ball down a low ramp and then down a higher ramp. The cup moves farther when the ball comes down the higher ramp. Which conclusion is best supported?",
     ["The ball became heavier on the higher ramp",
      "The ball had more energy of motion when it moved faster from the higher ramp",
      "The cup changed on its own",
      "Ramp height does not change the ball's energy of motion"], "B", None, None),
    ("An engineer builds a design, tests it, and sees that it does not work well. What should the engineer do next?",
     ["Use the test result as information to improve the design and test again",
      "Give up, because a failed test means the design is useless",
      "Ignore the test result and keep the design the same",
      "Remove the test result from the notebook"], "A", "cycle.png", 3.6),
    ("A moving marble hits a still marble. The still marble rolls away. Which conclusion is best supported?",
     ["The still marble created its own energy", "The moving marble's energy disappeared",
      "Energy of motion transferred from the moving marble to the still marble",
      "No energy was involved"], "C", None, None),
    ("Which sentence about Thomas Edison is true?",
     ["Edison invented the very first light bulb",
      "Edison worked completely alone and never tested his ideas",
      "Edison's bulb never needed to be improved by anyone else",
      "Edison improved earlier light bulb designs and tested many materials"], "D", None, None),
    ("Warm water is placed next to a cooler cup. Soon the cooler cup feels warmer. What happened?",
     ["Energy transferred from the warm water to the cooler cup",
      "Energy transferred from the cooler cup to the warm water",
      "The cooler cup made its own heat",
      "No energy moved at all"], "A", None, None),
]
U1_SOURCES = [
    ("Ch4 p.17", "04-ch4 p.1"),
    ("Ch3 p.14", "03-ch3 p.1"),
    ("Ch1 p.4", "01-ch1 p.2"),
    ("Ch5 p.25", "05-ch5 p.1"),
    ("Ch4 p.17", "04-ch4 p.2"),
    ("Ch6 p.32", "06-ch6 p.1"),
    ("Ch6 p.36", "06-ch6 p.3"),
    ("Ch1 p.1", "01-ch1 p.1"),
    ("Ch4 p.20", "04-ch4 p.2"),
    ("Ch1 p.4", "01-ch1 p.2"),
    ("Ch3 p.14", "03-ch3 p.1"),
    ("Ch4 p.17", "04-ch4 p.4"),
    ("Ch3 p.14", "03-ch3 p.3"),
    ("Ch6 p.36", "06-ch6 p.3"),
    ("Ch2 p.9", "02-ch2 p.1"),
    ("Ch7 p.39", "07-ch7 p.1"),
    ("Ch4 p.23", "04-ch4 p.3"),
]
U1_MATCH_SOURCES = [
    ("Ch4 p.17", "04-ch4 p.1"),
    ("Ch1 p.4", "01-ch1 p.2"),
    ("Ch3 p.13", "03-ch3 p.1"),
    ("Ch5 p.25", "05-ch5 p.1"),
    ("Ch2 p.9", "02-ch2 p.1"),
    ("Ch6 p.36", "06-ch6 p.3"),
    ("Ch6 p.32", "06-ch6 p.1"),
    ("Ch1 p.1", "01-ch1 p.1"),
]

U2_TERMS = [
    ("Generator", "B"),
    ("Nonrenewable Resource", "I"),
    ("Solar Cell", "J"),
    ("Fossil Fuel", "D"),
    ("Turbine", "G"),
    ("Geothermal Energy", "E"),
    ("Renewable Resource", "C"),
    ("Hydroelectric Power", "K"),
]
U2_DEFS = [
    ("A", "A gas fossil fuel, mostly methane, found underground.", True),
    ("B", "A machine that changes motion into electricity.", False),
    ("C", "A resource that can be restored more quickly than it is used up.", False),
    ("D", "A fuel formed from the remains of organisms that lived long ago.", False),
    ("E", "Energy produced by heat that is transferred from inside Earth.", False),
    ("F", "A nonrenewable material mined from rock, used for nuclear energy.", True),
    ("G", "A machine with blades that spin when wind, water, or steam pushes them.", False),
    ("H", "A solid fossil fuel formed from plants in wet, swampy places.", True),
    ("I", "A resource that cannot be restored as quickly as it is used.", False),
    ("J", "A device that converts sunlight to electricity.", False),
    ("K", "Electricity generated by the energy in moving water, usually through a dam.", False),
]
U2_MC = [
    ("Coal is plentiful right now, but it forms over millions of years. Is coal renewable or nonrenewable?",
     ["Renewable, because there is a lot of it right now", "Renewable, because it comes from plants",
      "Nonrenewable, because it is found underground",
      "Nonrenewable, because it forms much more slowly than it is used"], "D", None, None),
    ("Coal, petroleum, and natural gas all form from ____.",
     ["Rocks that melt deep underground", "The remains of organisms that lived long ago",
      "Wind blowing for millions of years", "Sunlight stored in the ground"], "B", None, None),
    ("Petroleum forms from tiny organisms buried on the ocean floor. Coal forms from ____.",
     ["Plants buried in swamps", "Organisms buried in desert sand",
      "Rocks buried under mountains", "Salt deposits under the sea"], "A", None, None),
    ("In a power plant, burning fuel heats water into steam. The steam then ____.",
     ["Turns into coal", "Turns into petroleum", "Spins a turbine that turns a generator",
      "Cools down and disappears"], "C", "fuel-pathway.png", 6.8),
    ("Which fossil fuel is a liquid found under Earth's surface?",
     ["Coal", "Petroleum (crude oil)", "Natural gas", "Uranium"], "B", None, None),
    ("Uranium is used to make nuclear energy. Which is true about uranium?",
     ["It is a renewable resource that grows back quickly", "It is a fossil fuel made from plants",
      "It is a form of moving water", "It is a nonrenewable material mined from rock"], "D", None, None),
    ("A nuclear power plant and a coal power plant are alike because both ____.",
     ["Burn coal to make heat", "Use moving water to spin a turbine",
      "Use heat to make steam that spins a turbine and turns a generator",
      "Use sunlight to make electricity"], "C", "nuclear-pathway.png", 6.0),
    ("In a wind turbine, what makes the blades spin?",
     ["Moving air (wind)", "Sunlight", "Heat from inside Earth", "Moving water"], "A", None, None),
    ("Why is wind called renewable but not always available?",
     ["Wind runs out and can never come back", "Wind is available every day in every place",
      "Wind keeps coming, but it does not blow all the time in every place",
      "Wind is made by burning fuel"], "C", None, None),
    ("In a hydroelectric dam, what makes the turbine spin?",
     ["Sunlight hitting the water", "Moving water flowing through the dam",
      "Heat from inside Earth", "Burning coal under the water"], "B", "hydro.png", 6.0),
    ("Why is hydroelectric power often more predictable than wind power?",
     ["Water never stops flowing anywhere", "Dams make their own water",
      "Wind is always stronger than water",
      "Water can be stored behind a dam and released when needed"], "D", None, None),
    ("What does a solar cell do?",
     ["It converts sunlight to electricity", "It burns sunlight like fuel",
      "It stores wind for later", "It spins a turbine with steam"], "A", "solar.png", 4.0),
    ("At night, a solar panel makes little or no electricity. Why?",
     ["Solar panels only work when they are hot", "There is no sunlight at night for the solar cell to use",
      "Solar panels store too much energy at night", "Wind blows harder at night"], "B", None, None),
    ("Where does geothermal energy come from?",
     ["Moving air above the ground", "Sunlight reflecting off the ground",
      "Heat transferred from inside Earth", "Water stored in clouds"], "C", None, None),
    ("Why can't every place use geothermal energy?",
     ["Geothermal works best in places with heat from Earth near the surface, and not every place has that",
      "Geothermal energy runs out after one use", "Geothermal energy is found only in the ocean",
      "Geothermal energy needs strong wind all year"], "A", None, None),
    ("Regenerative braking turns a car's energy of motion into ____.",
     ["Gasoline", "Coal", "Sunlight", "Stored energy that can be used again"], "D", None, None),
    ("A location has strong sunlight most days but very little moving water. Which resource would work better there, based on availability?",
     ["Hydroelectric power, because it needs moving water", "Geothermal energy, because it needs strong sunlight",
      "Solar power, because the location has strong sunlight most days",
      "Wind power, because it needs strong sunlight"], "C", None, None),
]
U2_SOURCES = [
    ("Ch1 p.1", "unit-02-ch1 p.1"),
    ("Ch2 p.2", "unit-02-ch2 p.1"),
    ("Ch2 p.4", "unit-02-ch2 p.1"),
    ("Ch3 p.13", "unit-02-ch3 p.2"),
    ("Ch2 p.4", "unit-02-ch2 p.1"),
    ("Ch4 p.21", "unit-02-ch4 p.1"),
    ("Ch4 p.22", "unit-02-ch4 p.1"),
    ("Ch5 p.28", "unit-02-ch5 p.1"),
    ("Ch5 p.29", "unit-02-ch5 p.2"),
    ("Ch6 p.31", "unit-02-ch6 p.1"),
    ("Ch6 p.33", "unit-02-ch6 p.2"),
    ("Ch7 p.37", "unit-02-ch7 p.1"),
    ("Ch7 p.38", "unit-02-ch7 p.2"),
    ("Ch8 p.43", "unit-02-ch8 p.1"),
    ("Ch8 p.44", "unit-02-ch8 p.2"),
    ("Ch9 p.49", "unit-02-ch9 p.2"),
    ("Ch7 p.38", "unit-02-ch7 p.2"),
]
U2_MATCH_SOURCES = [
    ("Ch5 p.28", "unit-02-ch5 p.1"),
    ("Ch1 p.1", "unit-02-ch1 p.1"),
    ("Ch7 p.37", "unit-02-ch7 p.1"),
    ("Ch2 p.2", "unit-02-ch1 p.1"),
    ("Ch5 p.28", "unit-02-ch5 p.1"),
    ("Ch8 p.43", "unit-02-ch8 p.1"),
    ("Ch1 p.1", "unit-02-ch1 p.1"),
    ("Ch6 p.31", "unit-02-ch6 p.1"),
]


# ---------------------------------------------------------------- builders
def build_student(title, subtitle, terms, defs, mc, outpath):
    doc = Document()
    # page margins ~0.8in
    for sec in doc.sections:
        sec.top_margin = Inches(0.7)
        sec.bottom_margin = Inches(0.7)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)

    # title
    _para(doc, title, size=20, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    _para(doc, subtitle, size=15, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=5)
    # header
    _para(doc, "Name: ________________________________    HR:   4A    4B    4C    4D",
          size=13, space_after=6)

    # directions
    _para(doc, "Directions: Read each question and choose the ONE BEST ANSWER.",
          size=13, space_after=6)

    # ---- matching section ----
    _para(doc, "Part 1: Matching (Questions 1–8)", size=16, bold=True, space_after=4)
    _para(doc, "Write the letter of the definition that matches each word.", size=13, space_after=5)

    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    hdr = table.rows[0].cells
    # term column header
    _cell_para(hdr[0], "Vocabulary", bold=True, size=13)
    _cell_para(hdr[1], "Definitions", bold=True, size=13)
    set_cell_margins(hdr[0]); set_cell_margins(hdr[1])

    n_terms = len(terms)
    n_defs = len(defs)
    rows = max(n_terms, n_defs)
    for i in range(rows):
        row = table.add_row().cells
        if i < n_terms:
            t, _ans = terms[i]
            _cell_para(row[0], f"{i+1}. ____ {t}", bold=False, size=13.5, bold_term=True)
        else:
            _cell_para(row[0], "", size=13.5)
        if i < n_defs:
            letter, dtext, _extra = defs[i]
            _cell_para(row[1], f"{letter}. {dtext}", bold=False, size=13, bold_letter=True)
        else:
            _cell_para(row[1], "", size=13)
        set_cell_margins(row[0]); set_cell_margins(row[1])

    # column widths
    from docx.oxml.ns import qn as _qn
    widths = [Inches(2.6), Inches(4.2)]
    for row in table.rows:
        for idx, w in enumerate(widths):
            row.cells[idx].width = w

    _para(doc, "", size=12, space_after=2)

    # ---- MC section ----
    _para(doc, "Part 2: Multiple Choice (Questions 9–25)", size=16, bold=True, space_after=4)
    _para(doc, "Choose the ONE BEST ANSWER for each question.", size=13, space_after=6)

    letters = ["A", "B", "C", "D"]
    for qi, (stem, opts, correct, diag, diag_w) in enumerate(mc):
        qnum = qi + 9
        if diag:
            pimg = add_image_centered(doc, os.path.join(DIAG_DIR, diag), diag_w)
            pimg.paragraph_format.keep_with_next = True
        stem_p = _rich(doc, [(f"{qnum}. ", True), (stem, False)], size=13.5, space_after=3, space_before=4)
        stem_p.paragraph_format.keep_with_next = True
        for li, opt in enumerate(opts):
            op = _rich(doc, [(f"{letters[li]}. ", True), (opt, False)], size=13, space_after=2)
            if li < len(opts) - 1:
                op.paragraph_format.keep_with_next = True

    doc.save(outpath)
    return doc


def _cell_para(cell, text, bold=False, size=13, bold_term=False, bold_letter=False):
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    if bold_term:
        # bold the term, not the number/blank
        num, rest = text.split("____", 1)
        r1 = p.add_run(num)
        _set_font(r1, size, False)
        r2 = p.add_run("____")
        _set_font(r2, size, False)
        r3 = p.add_run(rest)
        _set_font(r3, size, True)
        return
    if bold_letter:
        letter, rest = text.split(".", 1)
        r1 = p.add_run(letter + ".")
        _set_font(r1, size, True)
        r2 = p.add_run(rest)
        _set_font(r2, size, False)
        return
    r = p.add_run(text)
    _set_font(r, size, bold)


def build_key(title, subtitle, terms, defs, mc, match_sources, mc_sources, outpath):
    doc = Document()
    for sec in doc.sections:
        sec.top_margin = Inches(0.7); sec.bottom_margin = Inches(0.7)
        sec.left_margin = Inches(0.8); sec.right_margin = Inches(0.8)

    _para(doc, title + " — ANSWER KEY", size=20, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    _para(doc, subtitle, size=15, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    _para(doc, "Teacher only. 25 questions × 2 points = 50 points.", size=13, space_after=10)

    # matching key
    _para(doc, "Part 1: Matching — Answer Key", size=15, bold=True, space_after=4)
    def_by_letter = {l: (d, e) for l, d, e in defs}
    for i, (term, ans) in enumerate(terms):
        dtext, extra = def_by_letter[ans]
        _rich(doc, [(f"{i+1}. ", True), (term, True), (f"  →  {ans}. {dtext}", False)], size=12.5, space_after=2)

    _para(doc, "", size=12, space_after=2)
    _para(doc, "Part 2: Multiple Choice — Answer Key", size=15, bold=True, space_after=4)
    letters = ["A", "B", "C", "D"]
    for qi, (stem, opts, correct, diag, diag_w) in enumerate(mc):
        qnum = qi + 9
        correct_text = opts[letters.index(correct)]
        _rich(doc, [(f"{qnum}. ", True), (correct + ". ", True), (correct_text, False)], size=12.5, space_after=2)

    # source alignment table
    _para(doc, "", size=12, space_after=2)
    _para(doc, "Source Alignment", size=15, bold=True, space_after=4)
    tbl = doc.add_table(rows=1, cols=3)
    tbl.style = 'Light Grid Accent 1'
    hdr = tbl.rows[0].cells
    _cell_para(hdr[0], "Q", bold=True, size=11)
    _cell_para(hdr[1], "Reader", bold=True, size=11)
    _cell_para(hdr[2], "Guided Notes", bold=True, size=11)
    # matching
    for i in range(len(terms)):
        r = tbl.add_row().cells
        _cell_para(r[0], str(i+1), size=11)
        _cell_para(r[1], match_sources[i][0], size=11)
        _cell_para(r[2], match_sources[i][1], size=11)
    for qi in range(len(mc)):
        r = tbl.add_row().cells
        _cell_para(r[0], str(qi+9), size=11)
        _cell_para(r[1], mc_sources[qi][0], size=11)
        _cell_para(r[2], mc_sources[qi][1], size=11)

    doc.save(outpath)


def main():
    # generate diagrams
    ramp_diagram("ramp.png")
    collision_diagram("collision.png")
    source_path_receiver("source-path.png")
    flashlight_diagram("flashlight.png")
    cycle_diagram(["DESIGN", "TEST", "EVIDENCE", "IMPROVE"], "cycle.png")
    fuel_pathway("fuel-pathway.png")
    nuclear_pathway("nuclear-pathway.png")
    hydro_diagram("hydro.png")
    solar_diagram("solar.png")
    print("diagrams generated")

    # Unit 1
    build_student("Grade 4 Science", "Unit 1 Assessment — Energy Transfer & Transformation",
                  U1_TERMS, U1_DEFS, U1_MC, "production/quizzes/07-unit-final-assessment.docx")
    build_key("Grade 4 Science", "Unit 1 Assessment — Energy Transfer & Transformation",
              U1_TERMS, U1_DEFS, U1_MC, U1_MATCH_SOURCES, U1_SOURCES,
              "production/quizzes/07-unit-final-assessment-key.docx")
    # Unit 2
    build_student("Grade 4 Science", "Unit 2 Assessment — Using Natural Resources for Energy",
                  U2_TERMS, U2_DEFS, U2_MC, "production/quizzes/unit-02/unit-2-written-assessment-student.docx")
    build_key("Grade 4 Science", "Unit 2 Assessment — Using Natural Resources for Energy",
              U2_TERMS, U2_DEFS, U2_MC, U2_MATCH_SOURCES, U2_SOURCES,
              "production/quizzes/unit-02/unit-2-written-assessment-key.docx")
    print("DOCX built")


if __name__ == "__main__":
    main()
