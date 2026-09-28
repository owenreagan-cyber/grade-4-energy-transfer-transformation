"""Build all 9 Unit 2 slide decks (16:9 PPTX) from the approved outlines.

Design system matches the guided notes: navy / coral / gold / ink / mid-tint.
Typography (back-of-room floor): title 46-52 · slide title 42 · body 30-32 ·
labels 28 · Big Question 34-40. Grayscale-safe.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
    "production", "slides"))
os.makedirs(OUT, exist_ok=True)

NAVY  = RGBColor(0x2F, 0x3C, 0x7E)
CORAL = RGBColor(0xC0, 0x3D, 0x3D)
GOLD  = RGBColor(0xE8, 0xC5, 0x4A)
INK   = RGBColor(0x1F, 0x1F, 0x1F)
MID   = RGBColor(0xE8, 0xEA, 0xF2)
LIGHT = RGBColor(0xFA, 0xFA, 0xF8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY  = RGBColor(0x59, 0x5B, 0x66)
GREEN = RGBColor(0x3E, 0x7A, 0x4E)
PALE  = RGBColor(0xC9, 0xD2, 0xE8)

CUE_COLORS = {
    "NOTE": RGBColor(0x2F, 0x3C, 0x7E),
    "DRAW": RGBColor(0x3E, 0x7A, 0x4E),
    "LABEL": RGBColor(0xE8, 0xC5, 0x4A),
    "THINK": RGBColor(0xC0, 0x3D, 0x3D),
    "WRITE": RGBColor(0x2E, 0x6E, 0x8E),
    "SCIENCE JOURNAL": RGBColor(0x6B, 0x4F, 0xA0),
    "TEST": RGBColor(0xC0, 0x3D, 0x3D),
    "REVEAL": RGBColor(0xC0, 0x3D, 0x3D),
}


def new_prs():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def add_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def rect(slide, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE):
    sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.fill.solid()
    sp.fill.fore_color.rgb = fill
    sp.line.fill.background()
    sp.shadow.inherit = False
    return sp


def textbox(slide, x, y, w, h, text, size=24, color=INK, bold=False, align=PP_ALIGN.LEFT,
            anchor=MSO_ANCHOR.TOP, italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(4)
        r = p.add_run(); r.text = line
        r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
        r.font.color.rgb = color; r.font.name = "Arial"
    return tb


def cue_badge(slide, cue):
    if not cue:
        return
    c = CUE_COLORS.get(cue, GRAY)
    sp = rect(slide, 12.0, 0.28, 1.15, 0.46, c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    tf = sp.text_frame; tf.word_wrap = False
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = cue
    r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = "Arial"


def model_strip(slide, items, y=5.6, x=0.9, w=11.5, box_h=0.95):
    """Pathway banner: single navy rounded bar with 26 pt white/gold arrow chain."""
    sp = rect(slide, x, y, w, box_h, NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    tf = sp.text_frame; tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Pt(10); tf.margin_right = Pt(10)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    for i, it in enumerate(items):
        r = p.add_run(); r.text = it
        r.font.size = Pt(26); r.font.bold = True
        r.font.color.rgb = GOLD if i == 0 else WHITE
        r.font.name = "Arial"
        if i < len(items) - 1:
            ar = p.add_run(); ar.text = " → "
            ar.font.size = Pt(26); ar.font.bold = True
            ar.font.color.rgb = CORAL; ar.font.name = "Arial"


def title_slide(prs, title, subtitle):
    s = add_slide(prs)
    rect(s, 0, 0, 13.333, 7.5, NAVY)
    rect(s, 0, 5.35, 13.333, 0.08, GOLD)
    textbox(s, 0.9, 2.3, 11.5, 1.6, title, size=48, color=WHITE, bold=True)
    textbox(s, 0.9, 4.0, 11.5, 0.6, subtitle, size=22, color=PALE)
    textbox(s, 0.9, 5.7, 11.5, 0.5, "Unit 2 · Using Natural Resources for Energy · Grade 4",
            size=15, color=PALE, italic=True)
    return s


def big_question_slide(prs, question, num):
    s = add_slide(prs)
    rect(s, 0, 0, 13.333, 7.5, LIGHT)
    rect(s, 0, 2.5, 13.333, 2.5, NAVY)
    textbox(s, 0.9, 2.1, 11.5, 0.5, "Big Question", size=16, color=GRAY, align=PP_ALIGN.CENTER)
    textbox(s, 0.9, 2.7, 11.5, 2.1, question, size=36, color=WHITE, bold=True,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, 11.6, 0.32, 0.8, 0.4, str(num), size=14, color=GRAY, align=PP_ALIGN.RIGHT)
    return s


def concept(prs, title, subtitle, lines, cue=None, num=None, strip=None, size=32, reveal=False):
    s = add_slide(prs)
    rect(s, 0, 0, 13.333, 7.5, LIGHT)
    rect(s, 0, 0, 13.333, 1.55, NAVY)
    textbox(s, 0.5, 0.12, 11.4, 0.95, title, size=38, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    if subtitle:
        textbox(s, 0.5, 1.12, 11.4, 0.36, subtitle, size=15, color=PALE)
    if num:
        textbox(s, 11.6, 0.34, 0.8, 0.4, str(num), size=15, color=PALE, align=PP_ALIGN.RIGHT)
    cue_badge(s, cue)
    body_y = 1.8
    if reveal:
        textbox(s, 0.5, 1.66, 11.8, 0.4, "Reveal after students try.", size=14, color=CORAL, italic=True)
        body_y = 2.2
    body = s.shapes.add_textbox(Inches(0.9), Inches(body_y), Inches(11.5), Inches(3.3))
    tf = body.text_frame; tf.word_wrap = True
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(10)
        r = p.add_run(); r.text = ln
        r.font.size = Pt(size); r.font.color.rgb = INK; r.font.name = "Arial"
    if strip:
        model_strip(s, strip)
    return s


def review_q(prs, question, options, num):
    s = add_slide(prs)
    rect(s, 0, 0, 13.333, 7.5, LIGHT)
    rect(s, 0, 0, 13.333, 0.9, NAVY)
    textbox(s, 0.5, 0.16, 11.5, 0.6, "Review", size=24, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, 11.4, 0.28, 0.8, 0.4, str(num), size=14, color=PALE, align=PP_ALIGN.RIGHT)
    textbox(s, 0.9, 1.6, 11.5, 1.3, question, size=30, color=INK, bold=True)
    opt = "\n".join(f"{'ABCD'[i]}.  {o}" for i, o in enumerate(options))
    textbox(s, 0.9, 3.1, 11.5, 3.4, opt, size=28, color=INK)
    return s


def review_a(prs, answer, num):
    s = add_slide(prs)
    rect(s, 0, 0, 13.333, 7.5, LIGHT)
    rect(s, 0, 0, 13.333, 0.9, GREEN)
    textbox(s, 0.5, 0.16, 11.5, 0.6, "Answer", size=24, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, 11.4, 0.28, 0.8, 0.4, str(num), size=14, color=WHITE, align=PP_ALIGN.RIGHT)
    textbox(s, 0.9, 1.8, 11.5, 2.0, answer, size=30, color=INK, bold=True)
    return s


def C(title, subtitle, lines, cue, strip=None, reveal=False):
    return dict(title=title, subtitle=subtitle, lines=lines, cue=cue, strip=strip, reveal=reveal)


CHAPTERS = [
dict(
 file="01-u2-ch1-renewable-nonrenewable-slides.pptx",
 title="Renewable and Nonrenewable Resources",
 sub="Chapter 1 · Grade 4 · Week 5",
 big="What is the difference between renewable and nonrenewable resources?",
 hook=("Three hikers cook dinner",
       ["One cooks on a propane stove, one on a wood fire, one in a solar oven.",
        "Which energy sources can come back, and which cannot?"]),
 concepts=[
   C("Key Words: renewable / nonrenewable", "Page 1 · Key Words",
     ["Renewable = restored as quickly as it is used.",
      "Nonrenewable = NOT restored that quickly."], "NOTE"),
   C("Key Idea: abundant ≠ renewable", "Page 1 · Key Idea",
     ["Abundant does NOT mean renewable.",
      "Coal is plentiful now but forms over millions of years."], "NOTE"),
   C("Sort It", "Page 1 · Sort It",
     ["Sort each resource: renewable or nonrenewable?"], "NOTE"),
   C("Renewable ≠ always available", "Page 2 · Availability",
     ["Renewable depends on location and conditions.",
      "Some places get little sun or steady wind."], "NOTE", reveal=True),
   C("Benefits and limits of renewables", "Page 2 · Benefits and Limits",
     ["Renewables still have costs — turbines, panel cost, dams flood land."], "NOTE"),
   C("Model It: restored quickly", "Page 2 · Model It",
     ["Copy the chain."], "NOTE",
     strip=["USED SLOWLY", "RESTORED QUICKLY", "RENEWABLE"], reveal=True),
   C("Draw / Label", "Page 3 · Draw/Label",
     ["Draw one renewable and one nonrenewable resource."], "DRAW"),
 ],
 review=[
   ("Coal is plentiful now but forms over millions of years. Coal is —",
    ["renewable", "nonrenewable", "both", "not a resource"],
    "B. Nonrenewable — it is used much faster than it forms."),
   ("Which is a renewable resource?",
    ["petroleum", "natural gas", "wind", "coal"],
    "C. Wind is restored naturally and quickly."),
   ("Sunlight is renewable but not always available. Why?",
    ["the sun disappears forever", "some places/times get little sunlight", "solar cells break", "sunlight is nonrenewable"],
    "B. Location and time of day/year affect available sunlight."),
   ("What makes a resource renewable?",
    ["it is abundant", "it is cheap", "it is restored as quickly as it is used", "it comes from the ground"],
    "C. Renewability is about how fast it is restored vs. used."),
   ("A resource can be abundant and still be —",
    ["renewable", "free", "nonrenewable", "water"],
    "C. Abundant does NOT mean renewable."),
 ]),
dict(
 file="02-u2-ch2-slides.pptx",
 title="Types of Fossil Fuels",
 sub="Chapter 2 · Grade 4 · Week 5",
 big="What are fossil fuels?",
 hook=("A long train trip",
       ["A train engine runs on diesel, is lubricated with oil, and the engineer eats with a plastic fork.",
        "What do these three things have in common?"]),
 concepts=[
   C("Key Words: coal, petroleum, natural gas", "Page 1 · Key Words",
     ["Coal (solid) · petroleum/crude oil (liquid) · natural gas (gas)."], "NOTE"),
   C("Three Fossil Fuels", "Page 1 · Three Fossil Fuels",
     ["All three form from the remains of organisms that lived long ago."], "NOTE"),
   C("How They Form", "Page 1 · How They Form",
     ["Buried remains + heat + pressure over millions of years.",
      "Coal from swamp plants · petroleum from marine organisms · gas rises and gets trapped."],
     "NOTE", reveal=True),
   C("Check Your Thinking", "Page 1 · Check Your Thinking",
     ["How are coal and petroleum alike? How are they different?"], "THINK"),
 ],
 review=[
   ("Which fossil fuel is a liquid?",
    ["coal", "natural gas", "petroleum", "peat"],
    "C. Petroleum (crude oil) is a liquid."),
   ("Coal forms mainly from the remains of —",
    ["marine organisms", "swamp plants", "dinosaurs", "minerals"],
    "B. Coal forms from plants that became peat, then coal."),
   ("Natural gas rises through Earth's crust because it is —",
    ["less dense than rock", "heavier than oil", "solid", "cold"],
    "A. Natural gas is less dense and gets trapped under rock."),
   ("Which is a fossil fuel?",
    ["wind", "sunlight", "natural gas", "flowing water"],
    "C. Natural gas is a fossil fuel."),
   ("Why are they called FOSSIL fuels?",
    ["they are old rocks", "they form from the remains of organisms", "they are found in fossils", "they are very hard"],
    "B. They form from fossilized remains of organisms."),
 ]),
dict(
 file="03-u2-ch3-slides.pptx",
 title="Using Fossil Fuels",
 sub="Chapter 3 · Grade 4 · Week 6",
 big="What are some costs and benefits of using fossil fuels?",
 hook=("Under the hood",
       ["A car engine runs on gasoline — you see moving parts and feel heat.",
        "Then a refinery photo: what happens to the fuel before it reaches the car?"]),
 concepts=[
   C("Key Words: extract, refine, combustion", "Page 1 · Key Words",
     ["Extract = take from the ground · refine = change into useful products · combustion = burning."], "NOTE"),
   C("From Ground to Use", "Page 1 · From Ground to Use",
     ["Number the four steps in order (1–4)."], "NOTE",
     strip=["EXTRACT", "TRANSPORT", "REFINE", "BURN"], reveal=True),
   C("Electricity Pathway", "Page 2 · Electricity Pathway",
     ["Copy the pathway; then DRAW the pathway box."], "NOTE",
     strip=["BURN FUEL", "STEAM", "TURBINE", "GENERATOR", "ELECTRICITY"], reveal=True),
   C("Benefits and Limitations", "Page 3 · Benefits and Limitations",
     ["Benefits: heat, engines, electricity, products.",
      "Limitations: mining danger, spills, air pollution."], "NOTE"),
   C("Careful Use & Stewardship", "Page 3 · Careful Use",
     ["Extraction and use can affect land, water, and air.",
      "Oil spills harm wildlife; burning releases substances into the air."], "NOTE"),
 ],
 review=[
   ("What is the FIRST step in using petroleum?",
    ["refine it", "extract it", "burn it", "transport it"],
    "B. Extract (take it from the ground) first."),
   ("Burning fuel heats water into —",
    ["ice", "steam", "oil", "coal"],
    "B. Steam spins the turbine."),
   ("In a power plant, the generator makes —",
    ["steam", "heat", "electricity", "fuel"],
    "C. The generator makes electricity."),
   ("Which is a BENEFIT of fossil fuels?",
    ["oil spills", "mining danger", "heating homes and cooking", "air pollution"],
    "C. Heating and cooking are benefits."),
   ("Which is a LIMITATION of fossil fuels?",
    ["they power engines", "they can cause pollution and spills", "they make electricity", "they heat homes"],
    "B. Pollution and spills are limitations."),
 ]),
dict(
 file="04-u2-ch4-slides.pptx",
 title="Nuclear Energy",
 sub="Chapter 4 · Grade 4 · Week 6",
 big="What is nuclear power?",
 hook=("Steam or smoke?",
       ["A cooling tower photo — steam rises.",
        "Is that smoke, or is it just steam?"]),
 concepts=[
   C("Key Words: nuclear energy, uranium", "Page 1 · Key Words",
     ["Nuclear energy comes from a material called uranium (mined from rock)."], "NOTE"),
   C("Key Idea: same pathway as coal", "Page 1 · Key Idea",
     ["Nuclear power uses heat to make electricity — the same pathway as coal."], "NOTE"),
   C("Electricity Pathway", "Page 1 · Electricity Pathway",
     ["Copy the pathway."], "NOTE",
     strip=["NUCLEAR HEAT", "STEAM", "TURBINE", "GENERATOR", "ELECTRICITY"], reveal=True),
   C("Benefits and Limitations", "Page 2 · Benefits and Limitations",
     ["Benefits: reliable, little air pollution.",
      "Limitations: nonrenewable, used fuel must be stored safely."], "NOTE"),
   C("Safety First", "Page 2 · Safety First",
     ["Heat must be controlled; used fuel is stored safely."], "NOTE"),
 ],
 review=[
   ("Nuclear power plants make electricity using —",
    ["wind", "heat from boiling water into steam", "sunlight", "coal"],
    "B. Heat boils water into steam that spins a turbine."),
   ("Uranium is —",
    ["renewable", "a fossil fuel", "a mined material used for nuclear energy", "a gas"],
    "C. Uranium is mined from rock."),
   ("A nuclear plant and a coal plant both use —",
    ["uranium", "a steam-spun turbine and generator", "solar cells", "wind"],
    "B. Both use the heat → steam → turbine → generator pathway."),
   ("Which is a LIMITATION of nuclear power?",
    ["reliable electricity", "little air pollution", "used fuel stays dangerous a long time", "it heats homes"],
    "C. Used fuel must be stored safely for a very long time."),
   ("The mechanism of nuclear fission (splitting atoms) is —",
    ["the main learning goal", "NOT a required learning objective", "the only thing to memorize", "how solar cells work"],
    "B. We learn heat → steam → turbine → generator, not fission detail."),
 ]),
dict(
 file="05-u2-ch5-slides.pptx",
 title="Wind Energy",
 sub="Chapter 5 · Grade 4 · Week 7",
 big="How do people use wind as a source of energy?",
 hook=("The island switch",
       ["An island shuts off its diesel generator as wind turbines take over for the afternoon.",
        "Where does the energy come from when the wind blows?"]),
 concepts=[
   C("Key Words: wind farm, turbine", "Page 1 · Key Words",
     ["A turbine has blades that spin when wind pushes them; many together make a wind farm."], "NOTE"),
   C("Electricity Pathway", "Page 1 · Electricity Pathway",
     ["Copy the pathway; then DRAW a labeled turbine."], "NOTE",
     strip=["MOVING AIR", "BLADES", "GENERATOR", "ELECTRICITY"], reveal=True),
   C("Benefits and Limitations", "Page 2 · Benefits and Limitations",
     ["Benefits: renewable, no fuel burned.",
      "Limitations: needs wind, not always blowing."], "NOTE"),
   C("Location Matters", "Page 2 · Location Matters",
     ["Wind works best where it blows steadily and strongly enough."], "NOTE"),
 ],
 review=[
   ("Wind turns the blades, which —",
    ["cool the air", "spin a generator to make electricity", "store water", "burn fuel"],
    "B. Blades spin a generator that makes electricity."),
   ("Wind is called renewable because —",
    ["it is always windy", "wind keeps coming back", "turbines last forever", "wind is cheap"],
    "B. Wind is restored naturally and continuously."),
   ("Wind power depends on —",
    ["coal", "location and weather", "uranium", "dams"],
    "B. Wind power needs a steady, strong enough wind."),
   ("Which is a LIMITATION of wind?",
    ["no fuel burned", "renewable", "not always blowing", "makes electricity"],
    "C. Wind is not always blowing."),
 ]),
dict(
 file="06-u2-ch6-slides.pptx",
 title="Hydroelectric Energy",
 sub="Chapter 6 · Grade 4 · Week 7",
 big="How do people use moving water as a source of energy?",
 hook=("The dam's secret",
       ["A dam releases water that spins turbines.",
        "The reservoir is a stored source of energy. What does 'stored' mean here?"]),
 concepts=[
   C("Key Words: hydroelectric, reservoir", "Page 1 · Key Words",
     ["Hydroelectric power = electricity from moving water (usually through a dam).",
      "A reservoir holds water behind the dam."], "NOTE"),
   C("Electricity Pathway", "Page 1 · Electricity Pathway",
     ["Copy the pathway."], "NOTE",
     strip=["WATER", "DAM", "TURBINE", "GENERATOR", "ELECTRICITY"], reveal=True),
   C("Benefits and Limitations", "Page 2 · Benefits and Limitations",
     ["Benefits: renewable, predictable (water stored).",
      "Limitations: floods land, can block fish."], "NOTE"),
   C("Caring for Rivers", "Page 2 · Caring for Rivers",
     ["Fish ladders help salmon move past a dam.", "Then DRAW a labeled dam."], "NOTE"),
 ],
 review=[
   ("What holds water for a hydroelectric dam?",
    ["a wind farm", "a reservoir", "a solar panel", "a mine"],
    "B. The reservoir holds water behind the dam."),
   ("Moving water spins a —",
    ["generator directly", "turbine connected to a generator", "solar cell", "boiler"],
    "B. Water spins a turbine that turns a generator."),
   ("Hydroelectric is more predictable than wind because —",
    ["water can be stored", "water never stops", "dams are cheap", "rivers are everywhere"],
    "A. Water can be stored behind a dam."),
   ("Which is a LIMITATION of dams?",
    ["renewable", "they flood land and can block fish", "no fuel burned", "make electricity"],
    "B. Dams flood land and can block fish like salmon."),
 ]),
dict(
 file="07-u2-ch7-slides.pptx",
 title="Solar Energy",
 sub="Chapter 7 · Grade 4 · Week 8",
 big="How do people use sunlight as a source of energy?",
 hook=("Lights out at sunset?",
       ["A solar farm powers a town.",
        "What happens when clouds come or the sun sets?"]),
 concepts=[
   C("Key Words: solar power, solar cell", "Page 1 · Key Words",
     ["Solar power = using sunlight. A solar cell converts sunlight to electricity."], "NOTE"),
   C("Electricity Pathway", "Page 1 · Electricity Pathway",
     ["Copy the pathway."], "NOTE",
     strip=["SUNLIGHT", "SOLAR CELL", "ELECTRICITY"], reveal=True),
   C("Other Ways to Use Sunlight", "Page 1 · Other Ways",
     ["Sunlight can heat water and cook food (solar oven)."], "NOTE"),
   C("Benefits and Limitations", "Page 2 · Benefits and Limitations",
     ["Benefits: renewable, no fuel burned.",
      "Limitations: needs sunlight, costs to install."], "NOTE"),
   C("Available Light", "Page 2 · Available Light",
     ["Solar depends on light that is available — location, weather, time of day."], "NOTE"),
 ],
 review=[
   ("A solar cell converts —",
    ["wind to electricity", "sunlight to electricity", "heat to light", "water to steam"],
    "B. A solar cell converts sunlight to electricity."),
   ("Why is solar called renewable but not always available?",
    ["the sun burns out", "sunlight depends on location and time", "panels break daily", "solar is nonrenewable"],
    "B. Sunlight depends on location, weather, and time."),
   ("On a cloudy day, a solar panel makes —",
    ["more electricity", "less electricity", "no difference", "steam"],
    "B. Less sunlight means less electricity."),
   ("Which is a LIMITATION of solar?",
    ["free sunlight", "no fuel burned", "costs money to install", "renewable"],
    "C. Installation cost is a limitation."),
 ]),
dict(
 file="08-u2-ch8-slides.pptx",
 title="Geothermal Energy",
 sub="Chapter 8 · Grade 4 · Week 8",
 big="What is geothermal energy, and how do people use it?",
 hook=("The warm cabin",
       ["A cabin far from power lines is warmed by heat piped from deep underground.",
        "Where does that heat come from?"]),
 concepts=[
   C("Key Words: geothermal energy", "Page 1 · Key Words",
     ["Geothermal energy = heat transferred from inside Earth."], "NOTE"),
   C("Two Ways to Use It", "Page 1 · Two Ways",
     ["Heat homes/buildings; or make electricity (steam spins a turbine)."], "NOTE"),
   C("Electricity Pathway", "Page 1 · Electricity Pathway",
     ["Copy the pathway."], "NOTE",
     strip=["EARTH'S HEAT", "STEAM", "TURBINE", "GENERATOR", "ELECTRICITY"], reveal=True),
   C("Benefits and Limitations", "Page 2 · Benefits and Limitations",
     ["Benefits: little pollution, heat always available underground.",
      "Limitations: needs hot rock, costly."], "NOTE"),
   C("Location Matters", "Page 2 · Location Matters",
     ["Most steam/hot-water sources are near volcanic areas."], "NOTE"),
 ],
 review=[
   ("Geothermal energy comes from —",
    ["the sun", "wind", "heat inside Earth", "moving water"],
    "C. Heat transferred from Earth's interior."),
   ("Where does geothermal work best?",
    ["everywhere", "near hot rock / volcanic areas", "only at the poles", "only in deserts"],
    "B. Areas where Earth's crust is active."),
   ("Which is a BENEFIT of geothermal?",
    ["little pollution", "needs hot rock", "costly to build", "only in some places"],
    "A. Geothermal produces little pollution."),
   ("Which is a LIMITATION of geothermal?",
    ["clean", "heat is always underground", "needs a special location", "renewable"],
    "C. It needs a special (volcanic) location."),
 ]),
dict(
 file="09-u2-ch9-slides.pptx",
 title="Energy Resource Innovations",
 sub="Chapter 9 · Grade 4 · Week 8",
 big="What other energy resources are being developed?",
 hook=("Step and light",
       ["A sidewalk tile lights up when someone steps on it.",
        "Energy from everyday motion? How?"]),
 concepts=[
   C("Key Words: biofuel, hybrid", "Page 1 · Key Words",
     ["Biofuel = fuel from recently living organisms. Hybrid = a vehicle with two fuel sources."], "NOTE"),
   C("New Ideas", "Page 1 · New Ideas",
     ["biofuels, electric/hybrid cars, fuel cells (hydrogen), wave energy, motion-harvesting tiles/clothing."], "NOTE"),
   C("Engineering Better Systems", "Page 2 · Engineering",
     ["Engineers make systems more efficient, less wasteful, and safer.",
      "Regenerative braking turns motion energy back into electricity."], "NOTE"),
   C("Draw / Label: your own idea", "Page 2 · Draw/Label",
     ["Design your own energy idea and label the parts."], "DRAW"),
 ],
 review=[
   ("Ethanol is a —",
    ["fossil fuel", "biofuel", "mineral", "nuclear fuel"],
    "B. Ethanol is a biofuel from plants."),
   ("A hybrid car uses —",
    ["one fuel", "two different sources of fuel", "no energy", "only sunlight"],
    "B. A hybrid uses two fuel sources."),
   ("Regenerative braking turns motion energy into —",
    ["heat only", "electricity stored in a battery", "gasoline", "steam"],
    "B. It converts motion into electricity stored in a battery."),
   ("Why do engineers keep improving energy systems?",
    ["to use more fuel", "to make them more efficient and less wasteful", "to stop testing", "to make them cost more"],
    "B. To make systems more efficient, safer, and less wasteful."),
   ("Wave energy is really another way to harness —",
    ["wind energy", "coal", "uranium", "geothermal heat"],
    "A. Waves are made by wind; water delivers the motion."),
 ]),
]


def build(ch):
    prs = new_prs()
    title_slide(prs, ch["title"], ch["sub"])
    n = 2
    big_question_slide(prs, ch["big"], n); n += 1
    h = ch["hook"]
    concept(prs, h[0], "Opening phenomenon", h[1], cue="THINK", num=n); n += 1
    for c in ch["concepts"]:
        concept(prs, c["title"], c["subtitle"], c["lines"], cue=c["cue"],
                num=n, strip=c["strip"], reveal=c["reveal"]); n += 1
    for (q, opts, ans) in ch["review"]:
        review_q(prs, q, opts, n); n += 1
        review_a(prs, ans, n); n += 1
    out = os.path.join(OUT, ch["file"])
    prs.save(out)
    return out, len(prs.slides._sldIdLst)


if __name__ == "__main__":
    for ch in CHAPTERS:
        out, cnt = build(ch)
        print(f"built {os.path.basename(out)}: {cnt} slides")
    print("TOTAL decks:", len(CHAPTERS))
