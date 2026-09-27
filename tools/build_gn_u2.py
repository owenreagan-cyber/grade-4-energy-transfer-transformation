"""Premium guided notes — Unit 2: Using Natural Resources for Energy (Chapters 1–9).

Reuses the Phase 12A gn_design system (BIG QUESTION · KEY IDEA · NOTES · MODEL IT ·
DRAW/LABEL · CHECK YOUR THINKING · CONNECT). Grade-4 vocabulary only; neutral,
evidence-based (no climate/advocacy framing). Page targets honored: Ch1/Ch3 = 3 pages,
Ch9 = 2 pages, all others = 2 pages.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gn_design import *

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
    "production", "premium-notes", "unit-02"))
os.makedirs(OUT_DIR, exist_ok=True)

UNIT_SUB = "Unit 2 Guided Notes · Grade 4 Using Natural Resources for Energy"

def benefit_limit(doc, rows, row_h=620):
    """BENEFIT / LIMITATION two-column writing table."""
    return two_col_table(doc, ["Benefit", "Limitation"], rows, row_h=row_h)

def pathway(doc, steps, size=12):
    """Compact vertical energy pathway (source → … → output)."""
    box_w = FULL_W - 2200
    first = True
    for w in steps:
        if not first:
            ap = doc.add_paragraph()
            ap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            apPr = ap._p.get_or_add_pPr()
            sp = OxmlElement('w:spacing'); sp.set(qn('w:before'), '0'); sp.set(qn('w:after'), '0'); apPr.append(sp)
            set_run(ap.add_run("↓"), size=size + 2, bold=True, color=CORAL)
        t = doc.add_table(rows=1, cols=1)
        no_table_borders(t)
        t.alignment = 1
        c = t.cell(0, 0)
        set_cell_width(c, box_w)
        set_cell_margins(c, top=20, left=60, bottom=20, right=60)
        shade_cell(c, NAVY_HEX)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run(p.add_run(w), size=size, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
        set_row_height(t.rows[0], 300, rule='atLeast')
        first = False

def save(doc, fn):
    path = os.path.join(OUT_DIR, fn)
    doc.save(path)
    print("saved", path)

# ================================================================== CH 1  (3 pages)
def ch1():
    doc = new_doc()
    title_block(doc, "Renewable and Nonrenewable Resources", "Chapter 1 " + UNIT_SUB)
    big_question(doc, "What is the difference between renewable and nonrenewable resources?")

    heading(doc, "Key Words")
    fill(doc, "renewable resource — a resource that can be restored", "________________", "than it is used up.")
    fill(doc, "nonrenewable resource — a resource that cannot be restored", "________________", "than it is used up.")
    fill(doc, "fossil fuel — a fuel formed from the remains of", "________________", "that lived long ago.")

    heading(doc, "Key Idea")
    key_idea(doc, "Abundant does NOT mean renewable.")
    body(doc, "Renewable means it comes back as quickly as it is used. Nonrenewable means it does not.", size=12, color=GRAY, after=20)

    heading(doc, "Sort It")
    body(doc, "Write each resource in the correct column.", size=12, color=GRAY, after=20)
    two_col_table(doc, ["Renewable", "Nonrenewable"],
                  [("", ""), ("", ""), ("", "")], row_h=500)
    body(doc, "Bank: coal · wood · wind · petroleum · flowing water · natural gas · sunlight · Earth's heat", size=12, italic=True, color=GRAY, after=30)

    # PAGE 2
    title_block(doc, "Availability and Location", "Chapter 1 · Page 2", new_page=True)
    heading(doc, "Renewable Is Not Always Available Everywhere")
    body(doc, "A renewable resource still depends on location and conditions.", size=12, color=GRAY, after=20)
    fill(doc, "Example: In a sunny place, sunlight is renewable and", "________________", ".")
    fill(doc, "Example: In Antarctica in winter, the sun is too", "________________", "to be a dependable energy source.")

    heading(doc, "Benefits and Limits")
    body(doc, "Renewable resources still have costs. Fill in one cost for each.", size=12, color=GRAY, after=20)
    two_col_table(doc, ["Renewable resource", "One cost or limit"],
                  [("wind turbines", ""), ("solar panels", ""), ("dams for water power", "")], row_h=620)

    heading(doc, "Model It")
    body(doc, "A resource is renewable if it can be restored as quickly as it is used.", size=12, italic=True, color=GRAY, after=30)
    model_boxes(doc, ["USED SLOWLY", "RESTORED QUICKLY", "RENEWABLE"], size=12)

    check_thinking(doc, "Coal is plentiful right now, but it forms over millions of years. Is coal renewable or nonrenewable? Explain.", lines=2)

    # PAGE 3
    title_block(doc, "Draw / Label", "Chapter 1 · Page 3", new_page=True)
    heading(doc, "Draw / Label")
    body(doc, "Draw one renewable and one nonrenewable resource you use or see.", size=12, color=GRAY, after=20)
    labeled_pair(doc, "RENEWABLE", "NONRENEWABLE", height_dxa=1500)

    check_thinking(doc, "Why does it matter how quickly a resource is restored?", lines=2)
    connect(doc, "Chapter 1 connection: renewable or nonrenewable depends on time — how fast we use it vs. how fast it comes back.")
    save(doc, "unit-02-ch1-renewable-nonrenewable-guided-notes.docx")

# ================================================================== CH 2  (2 pages)
def ch2():
    doc = new_doc()
    title_block(doc, "Types of Fossil Fuels", "Chapter 2 " + UNIT_SUB)
    big_question(doc, "What are fossil fuels?")

    heading(doc, "Key Words")
    fill(doc, "coal — a", "________________", "fossil fuel formed from plants in wet, swampy places.")
    fill(doc, "petroleum (crude oil) — a", "________________", "fossil fuel found under Earth's surface.")
    fill(doc, "natural gas — a", "________________", "fossil fuel, mostly methane, found underground.")

    heading(doc, "Three Fossil Fuels")
    body(doc, "Coal, petroleum, and natural gas all form from the remains of organisms that lived long ago.", size=12, color=GRAY, after=20)
    two_col_table(doc, ["Fossil fuel", "State of matter"],
                  [("coal", ""), ("petroleum (crude oil)", ""), ("natural gas", "")], row_h=560)

    heading(doc, "How They Form")
    body(doc, "Buried remains + heat + pressure over millions of years.", size=13, bold=True, after=20)
    fill(doc, "Petroleum forms from", "________________", "organisms buried on the ocean floor.")
    fill(doc, "Coal forms from", "________________", "buried in swamps that become peat, then coal.")

    check_thinking(doc, "How are coal and petroleum alike? How are they different?", lines=2)

    # PAGE 2
    title_block(doc, "Formation and Uses", "Chapter 2 · Page 2", new_page=True)
    heading(doc, "Model It")
    pathway(doc, ["PLANTS IN A SWAMP", "BURIED + SQUEEZED", "PEAT", "COAL"])
    heading(doc, "What We Use Them For")
    body(doc, "Match each fossil fuel to a use. Write a word or short phrase.", size=12, color=GRAY, after=20)
    two_col_table(doc, ["Fossil fuel", "A use"],
                  [("coal", ""), ("petroleum", ""), ("natural gas", "")], row_h=620)
    check_thinking(doc, "Why are these three fuels called FOSSIL fuels?", lines=2)
    connect(doc, "Chapter 2 connection: all fossil fuels come from the remains of living things from long ago.")
    save(doc, "unit-02-ch2-types-of-fossil-fuels-guided-notes.docx")

# ================================================================== CH 3  (3 pages)
def ch3():
    doc = new_doc()
    title_block(doc, "Using Fossil Fuels", "Chapter 3 " + UNIT_SUB)
    big_question(doc, "What are some costs and benefits of using fossil fuels?")

    heading(doc, "Key Words")
    fill(doc, "extract — to take a resource", "________________", "the ground.")
    fill(doc, "refine — to change crude oil into", "________________", "useful products.")
    fill(doc, "combustion —", "________________", "a fuel (burning).")

    heading(doc, "From Ground to Use")
    body(doc, "Number the steps in order from 1 to 4.", size=12, color=GRAY, after=20)
    two_col_table(doc, ["Step", "Order"],
                  [("extract (take it from the ground)", ""),
                   ("transport (move it)", ""),
                   ("refine (change it into useful products)", ""),
                   ("burn it to release energy", "")], row_h=560)

    check_thinking(doc, "Why is the order of these steps important?", lines=2)

    # PAGE 2
    title_block(doc, "Electricity Pathway", "Chapter 3 · Page 2", new_page=True)
    heading(doc, "Electricity Pathway")
    body(doc, "Burning fuel heats water into steam. The steam spins a turbine and turns a generator.", size=12, color=GRAY, after=20)
    pathway(doc, ["BURN THE FUEL", "HEAT WATER INTO STEAM", "SPIN A TURBINE", "TURN A GENERATOR", "ELECTRICITY"])
    heading(doc, "Draw / Label")
    body(doc, "Draw the pathway from burning fuel to electricity.", size=12, color=GRAY, after=20)
    draw_box(doc, FULL_W, 1100, "draw the electricity pathway here")

    # PAGE 3
    title_block(doc, "Benefits, Limitations, Stewardship", "Chapter 3 · Page 3", new_page=True)
    heading(doc, "Benefits and Limitations")
    benefit_limit(doc, [("heating homes and cooking", ""),
                        ("powering engines (cars, trucks)", ""),
                        ("making electricity", ""),
                        ("mining can be dangerous", "")], row_h=560)
    heading(doc, "Careful Use")
    body(doc, "Extraction and use can affect land, water, and air.", size=13, bold=True, after=20)
    fill(doc, "An oil spill can harm", "________________", "and wildlife.")
    fill(doc, "Burning fossil fuels releases", "________________", "and other substances into the air.")
    body(doc, "Stewardship means taking care of resources and the places we live.", size=12, italic=True, color=GRAY, after=20)
    wline(doc, 1, gap=28, after=18)
    check_thinking(doc, "Why might someone choose a renewable resource instead of a fossil fuel?", lines=2)
    connect(doc, "Chapter 3 connection: fossil fuels give us energy and products, but they have real costs to consider.")
    save(doc, "unit-02-ch3-using-fossil-fuels-guided-notes.docx")

# ================================================================== CH 4  (2 pages)
def ch4():
    doc = new_doc()
    title_block(doc, "Nuclear Energy", "Chapter 4 " + UNIT_SUB)
    big_question(doc, "What is nuclear power?")

    heading(doc, "Key Words")
    fill(doc, "nuclear energy — energy released from a material called", "________________", ".")
    fill(doc, "uranium — a", "________________", "material mined from rock.")

    heading(doc, "Key Idea")
    key_idea(doc, "Nuclear power uses heat to make electricity — the same pathway as coal.")
    body(doc, "Nuclear energy releases a lot of heat. That heat boils water into steam.", size=12, color=GRAY, after=20)

    heading(doc, "Electricity Pathway")
    pathway(doc, ["NUCLEAR HEAT", "BOIL WATER INTO STEAM", "SPIN A TURBINE", "TURN A GENERATOR", "ELECTRICITY"])

    check_thinking(doc, "How is a nuclear power plant like a coal power plant?", lines=2)

    # PAGE 2
    title_block(doc, "Benefits and Limitations", "Chapter 4 · Page 2", new_page=True)
    heading(doc, "Benefits and Limitations")
    benefit_limit(doc, [("reliable electricity", ""),
                        ("little air pollution from the plant", ""),
                        ("nonrenewable (uranium is rare)", ""),
                        ("dangerous used fuel must be stored safely", "")], row_h=600)
    heading(doc, "Safety First")
    body(doc, "Nuclear power must be controlled carefully. Used fuel can stay dangerous for a very long time and must be stored safely.", size=12, color=GRAY, after=20)
    fill(doc, "The heat must be", "________________", "so the reactor stays safe.")
    fill(doc, "Used fuel is placed in", "________________", "storage.")
    check_thinking(doc, "What is one benefit AND one limitation of nuclear power?", lines=2)
    connect(doc, "Chapter 4 connection: nuclear and coal power plants share the same heat → steam → turbine → generator pathway.")
    save(doc, "unit-02-ch4-nuclear-energy-guided-notes.docx")

# ================================================================== CH 5  (2 pages)
def ch5():
    doc = new_doc()
    title_block(doc, "Wind Energy", "Chapter 5 " + UNIT_SUB)
    big_question(doc, "How do people use wind as a source of energy?")

    heading(doc, "Key Words")
    fill(doc, "wind farm — many wind", "________________", "placed together to make electricity.")
    fill(doc, "turbine — a machine with blades that", "________________", "when wind pushes them.")

    heading(doc, "Electricity Pathway")
    pathway(doc, ["MOVING AIR (WIND)", "TURNS THE BLADES", "SPINS THE GENERATOR", "ELECTRICITY"])

    heading(doc, "Draw / Label")
    body(doc, "Draw a wind turbine. Label the blades and the generator.", size=12, color=GRAY, after=20)
    draw_box(doc, FULL_W, 1400, "draw a wind turbine here")

    check_thinking(doc, "Where does the energy to turn the blades come from?", lines=2)

    # PAGE 2
    title_block(doc, "Benefits and Limitations", "Chapter 5 · Page 2", new_page=True)
    heading(doc, "Benefits and Limitations")
    benefit_limit(doc, [("renewable (wind keeps coming)", ""),
                        ("no fuel is burned", ""),
                        ("needs a windy location", ""),
                        ("wind is not always blowing", "")], row_h=600)
    heading(doc, "Location Matters")
    body(doc, "Some places are windy one day and calm the next. Wind works best where the wind blows steadily and strongly enough.", size=12, color=GRAY, after=20)
    fill(doc, "Batteries can store electricity for times when the wind", "________________", "blowing.")
    check_thinking(doc, "Why is wind called renewable but not always available?", lines=2)
    connect(doc, "Chapter 5 connection: wind is free and renewable, but it depends on location and weather.")
    save(doc, "unit-02-ch5-wind-energy-guided-notes.docx")

# ================================================================== CH 6  (2 pages)
def ch6():
    doc = new_doc()
    title_block(doc, "Hydroelectric Energy", "Chapter 6 " + UNIT_SUB)
    big_question(doc, "How do people use moving water as a source of energy?")

    heading(doc, "Key Words")
    fill(doc, "hydroelectric power — electricity made from the energy of", "________________", "water, usually through a dam.")
    fill(doc, "reservoir — a large area of", "________________", "held behind a dam.")

    heading(doc, "Electricity Pathway")
    pathway(doc, ["WATER IN A RESERVOIR", "FLOWS THROUGH THE DAM", "SPINS A TURBINE", "TURNS A GENERATOR", "ELECTRICITY"])

    check_thinking(doc, "What makes the water move through the turbine?", lines=2)

    # PAGE 2
    title_block(doc, "Benefits and Limitations", "Chapter 6 · Page 2", new_page=True)
    heading(doc, "Benefits and Limitations")
    benefit_limit(doc, [("renewable (water keeps flowing)", ""),
                        ("more predictable (water can be stored)", ""),
                        ("floods land behind the dam", ""),
                        ("can block fish such as salmon", "")], row_h=600)
    heading(doc, "Caring for Rivers")
    body(doc, "Dams can change a river and the habitats around it. Fish ladders help fish move past a dam.", size=12, color=GRAY, after=20)
    fill(doc, "A fish", "________________", "helps salmon move up and down the river.")
    heading(doc, "Draw / Label")
    body(doc, "Draw a dam. Label the reservoir, turbine, and generator.", size=12, color=GRAY, after=20)
    draw_box(doc, FULL_W, 1200, "draw a dam and label the parts here")
    check_thinking(doc, "What is one way engineers reduce the harm a dam can cause?", lines=2)
    connect(doc, "Chapter 6 connection: moving water spins a turbine, just like wind — but water can be stored, making it more predictable.")
    save(doc, "unit-02-ch6-hydroelectric-energy-guided-notes.docx")

# ================================================================== CH 7  (2 pages)
def ch7():
    doc = new_doc()
    title_block(doc, "Solar Energy", "Chapter 7 " + UNIT_SUB)
    big_question(doc, "How do people use sunlight as a source of energy?")

    heading(doc, "Key Words")
    fill(doc, "solar power — the use of", "________________", "to meet energy needs.")
    fill(doc, "solar cell — a device that converts", "________________", "to electricity.")

    heading(doc, "Electricity Pathway")
    pathway(doc, ["SUNLIGHT", "STRIKES A SOLAR CELL", "MAKES ELECTRICITY"])

    heading(doc, "Other Ways to Use Sunlight")
    body(doc, "Sunlight can also heat water and cook food.", size=12, color=GRAY, after=20)
    two_col_table(doc, ["Way to use sunlight", "How it works"],
                  [("solar panel", ""), ("solar oven", ""), ("solar water heater", "")], row_h=540)

    check_thinking(doc, "What does a solar cell do?", lines=2)

    # PAGE 2
    title_block(doc, "Benefits and Limitations", "Chapter 7 · Page 2", new_page=True)
    heading(doc, "Benefits and Limitations")
    benefit_limit(doc, [("renewable (sun keeps shining)", ""),
                        ("no fuel is burned", ""),
                        ("depends on sunlight (not at night)", ""),
                        ("costs money to install", "")], row_h=600)
    heading(doc, "Available Light")
    body(doc, "Different places get different amounts of sunlight at different times. Solar power depends on the light that is available.", size=12, color=GRAY, after=20)
    fill(doc, "On a cloudy day, a solar panel makes", "________________", "electricity.")
    fill(doc, "At night, there is", "________________", "sunlight.")
    check_thinking(doc, "Why is solar called renewable but not always available?", lines=2)
    connect(doc, "Chapter 7 connection: sunlight is free and renewable, but it depends on location, weather, and time of day.")
    save(doc, "unit-02-ch7-solar-energy-guided-notes.docx")

# ================================================================== CH 8  (2 pages)
def ch8():
    doc = new_doc()
    title_block(doc, "Geothermal Energy", "Chapter 8 " + UNIT_SUB)
    big_question(doc, "What is geothermal energy, and how do people use it?")

    heading(doc, "Key Words")
    fill(doc, "geothermal energy — energy from", "________________", "that is transferred from inside Earth.")

    heading(doc, "Two Ways to Use It")
    two_col_table(doc, ["Way", "What it does"],
                  [("heat homes and buildings", ""),
                   ("make electricity (steam spins a turbine)", "")], row_h=620)

    heading(doc, "Electricity Pathway")
    pathway(doc, ["HEAT FROM EARTH", "BOILS WATER INTO STEAM", "SPINS A TURBINE", "TURNS A GENERATOR", "ELECTRICITY"])

    check_thinking(doc, "Where does geothermal energy come from?", lines=2)

    # PAGE 2
    title_block(doc, "Benefits and Limitations", "Chapter 8 · Page 2", new_page=True)
    heading(doc, "Benefits and Limitations")
    benefit_limit(doc, [("little pollution (clean)", ""),
                        ("heat is always available underground", ""),
                        ("needs a special location (near hot rock)", ""),
                        ("costs a lot to build", "")], row_h=600)
    heading(doc, "Location Matters")
    body(doc, "Most steam and hot-water sources are near areas where Earth's crust is active, such as volcanic areas.", size=12, color=GRAY, after=20)
    fill(doc, "Geothermal works best in places with", "________________", "activity.")
    check_thinking(doc, "Why can't every place use geothermal energy?", lines=2)
    connect(doc, "Chapter 8 connection: Earth's own heat can warm buildings and make electricity — but only in the right places.")
    save(doc, "unit-02-ch8-geothermal-energy-guided-notes.docx")

# ================================================================== CH 9  (2 pages)
def ch9():
    doc = new_doc()
    title_block(doc, "Energy Resource Innovations", "Chapter 9 " + UNIT_SUB)
    big_question(doc, "What other energy resources are being developed?")

    heading(doc, "Key Words")
    fill(doc, "biofuel — a fuel made from the remains of", "________________", "living organisms.")
    fill(doc, "hybrid — a vehicle that uses", "________________", "different sources of fuel.")

    heading(doc, "New Ideas")
    two_col_table(doc, ["Innovation", "What it does"],
                  [("biofuels (ethanol)", ""),
                   ("electric and hybrid cars", ""),
                   ("fuel cells (hydrogen)", ""),
                   ("wave energy", ""),
                   ("sidewalk tiles and clothing that make electricity", "")], row_h=540)

    check_thinking(doc, "Pick one innovation. What problem does it help solve?", lines=2)

    # PAGE 2
    title_block(doc, "Engineering Better Systems", "Chapter 9 · Page 2", new_page=True)
    heading(doc, "How Engineers Improve Systems")
    body(doc, "Engineers work to make energy systems better: more efficient, less wasteful, and safer.", size=12, color=GRAY, after=20)
    fill(doc, "Regenerative braking turns a car's energy of motion into", "________________", ".")
    fill(doc, "Better solar cells convert", "________________", "of the sunlight that strikes them.")
    heading(doc, "Draw / Label")
    body(doc, "Design your own energy idea. Draw it and label the parts.", size=12, color=GRAY, after=20)
    draw_box(doc, FULL_W, 1500, "draw your energy innovation here")
    check_thinking(doc, "Why do engineers keep testing and improving energy ideas?", lines=2)
    connect(doc, "Chapter 9 connection: engineering is how we find new, better ways to meet energy needs.")
    save(doc, "unit-02-ch9-energy-resource-innovations-guided-notes.docx")

if __name__ == "__main__":
    ch1(); ch2(); ch3(); ch4(); ch5(); ch6(); ch7(); ch8(); ch9()
    print("ALL DONE")
