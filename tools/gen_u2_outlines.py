"""Generate Unit 2 slideshow outlines (Ch2–9) in the same format as Ch1.

Each outline: title-only slide, Big Question-only slide, phenomenon hook, teaching
sequence mapped to guided notes, then 4–6 MCQ review questions.
"""
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = os.path.join(ROOT, "production", "slides", "outlines", "unit-02")
os.makedirs(OUT, exist_ok=True)

def outline(ch, title, notes_file, big_q, hook, teaching, review):
    """teaching: list of dicts; review: list of (q, options, answer)."""
    L = []
    L.append(f"# Slideshow Outline — Unit 2 Ch{ch}: {title}\n")
    L.append(f"> 16:9 · order matches `production/premium-notes/unit-02/{notes_file}`.")
    L.append("> **Typography:** slide title 42 pt · body 32 pt · labels 28 pt · titles 38–46 pt floor.")
    L.append("> **Palette:** navy / coral / gold / light. Grayscale-safe. **Cue legend:** NOTE · DRAW · LABEL · THINK · SCIENCE JOURNAL.\n")
    L.append("## Opening (required)\n")
    L.append(f"### Slide 1 — {title}")
    L.append("- **Purpose:** title only.")
    L.append("- **Visual:** representative photo (see description), muted.\n")
    L.append("### Slide 2 — Big Question")
    L.append(f'- **Key text:** "{big_q}"\n')
    L.append("### Slide 3 — Hook")
    L.append(f"- **Purpose:** phenomenon — {hook}.")
    L.append("- **Key text:** (pose the phenomenon as a question).")
    L.append("- **Student action:** THINK — predict.")
    L.append("- **Visual:** (see description).")
    L.append("- **Reveal:** outcome after discussion.\n")
    L.append("## Core instruction\n")
    for i, t in enumerate(teaching, start=4):
        L.append(f"### Slide {i} — {t['title']}")
        if t.get('supports'):
            L.append(f"- **Supports:** {t['supports']}.")
        if t.get('key'):
            L.append(f"- **Key text:** \"{t['key']}\"")
        if t.get('talk'):
            L.append(f"- **Talking point:** {t['talk']}.")
        if t.get('action'):
            L.append(f"- **Student action:** {t['action']}.")
        L.append(f"- **Visual:** {t['visual']}.")
        if t.get('cue'):
            L.append(f"- **Cue:** {t['cue']}.")
        if t.get('reveal'):
            L.append(f"- **Reveal:** {t['reveal']}.")
        L.append("")
    L.append("## Review\n")
    n = 4 + len(teaching)
    for j, (q, opts, ans) in enumerate(review):
        s = n + 2 * j
        L.append(f"### Slide {s} — Review Q{j+1}")
        L.append(f"- **Key text:** \"{q}\"")
        for o in opts:
            L.append(f"  - {o}")
        L.append("- **Reveal:** answer next.\n")
        L.append(f"### Slide {s+1} — Q{j+1} Answer")
        L.append(f"- **Answer:** {ans}.\n")
    path = os.path.join(OUT, f"{ch:02d}-ch{ch}-slideshow-outline.md".replace("ch1","ch1"))
    fn = f"{ch:02d}-u2-ch{ch}-slideshow-outline.md"
    with open(os.path.join(OUT, fn), "w") as f:
        f.write("\n".join(L))
    print("wrote", fn)

# ---- Ch2
outline(2, "Types of Fossil Fuels", "unit-02-ch2-types-of-fossil-fuels-guided-notes.docx",
    "What are fossil fuels?",
    "a train engine runs on diesel, lubricated with oil, and the engineer eats with a plastic fork",
    [
        dict(title="Key Words: coal, petroleum, natural gas",
             supports="Page 1 · Key Words",
             key="Coal (solid) · petroleum/crude oil (liquid) · natural gas (gas).",
             action="NOTE — complete the three fill-ins (state of matter).",
             visual="three labeled cards with state icons.", cue="NOTE"),
        dict(title="Three Fossil Fuels",
             supports="Page 1 · Three Fossil Fuels",
             key="All three form from the remains of organisms that lived long ago.",
             action="NOTE — fill the state-of-matter column.",
             visual="three columns: coal/petroleum/natural gas with a blank state cell.", cue="NOTE"),
        dict(title="How They Form",
             supports="Page 1 · How They Form",
             key="Buried remains + heat + pressure over millions of years.",
             talk="petroleum from marine organisms; coal from swamp plants; gas rises and gets trapped.",
             action="NOTE — complete the two formation fills.",
             visual="buried-layers cross-section with heat/pressure arrows.", cue="NOTE", reveal="staged arrows"),
        dict(title="Check Your Thinking",
             supports="Page 1 · Check Your Thinking",
             key="How are coal and petroleum alike? How are they different?",
             action="THINK — discuss, then write.",
             visual="question only.", cue="THINK"),
    ],
    [
        ("Which fossil fuel is a liquid?", ["A. coal","B. natural gas","C. petroleum","D. peat"], "C. Petroleum (crude oil) is a liquid."),
        ("Coal forms mainly from the remains of —", ["A. marine organisms","B. swamp plants","C. dinosaurs","D. minerals"], "B. Coal forms from plants that became peat, then coal."),
        ("Natural gas rises through Earth's crust because it is —", ["A. less dense than rock","B. heavier than oil","C. solid","D. cold"], "A. Natural gas is less dense and gets trapped under rock."),
        ("Which is a fossil fuel?", ["A. wind","B. sunlight","C. natural gas","D. flowing water"], "C. Natural gas is a fossil fuel."),
        ("Why are they called FOSSIL fuels?", ["A. they are old rocks","B. they form from the remains of organisms","C. they are found in fossils","D. they are very hard"], "B. They form from fossilized remains of organisms."),
    ])

# ---- Ch3
outline(3, "Using Fossil Fuels", "unit-02-ch3-using-fossil-fuels-guided-notes.docx",
    "What are some costs and benefits of using fossil fuels?",
    "a car engine runs on gasoline — you see moving parts and feel heat; then a refinery photo",
    [
        dict(title="Key Words: extract, refine, combustion",
             supports="Page 1 · Key Words",
             key="Extract = take from the ground · refine = change into useful products · combustion = burning.",
             action="NOTE — complete the three fill-ins.",
             visual="three labeled cards.", cue="NOTE"),
        dict(title="From Ground to Use",
             supports="Page 1 · From Ground to Use",
             key="extract → transport → refine → burn (1–4).",
             action="NOTE — number the four steps in order.",
             visual="four-step flow with blank order numbers.", cue="NOTE", reveal="staged"),
        dict(title="Electricity Pathway",
             supports="Page 2 · Electricity Pathway",
             key="burn fuel → heat water into steam → spin a turbine → turn a generator → electricity.",
             action="NOTE — copy the pathway; then DRAW the pathway box.",
             visual="system diagram: boiler, turbine, generator with arrows.", cue="NOTE / DRAW / LABEL", reveal="staged"),
        dict(title="Benefits and Limitations",
             supports="Page 3 · Benefits and Limitations",
             key="Benefits: heat, engines, electricity, products. Limitations: mining danger, spills, air pollution.",
             action="NOTE — fill one benefit and one limitation for each row.",
             visual="two-column benefit/limitation table.", cue="NOTE"),
        dict(title="Careful Use & Stewardship",
             supports="Page 3 · Careful Use",
             key="Extraction and use can affect land, water, and air.",
             talk="oil spills harm wildlife; burning releases substances into the air.",
             action="NOTE — complete the two fills; write one stewardship idea.",
             visual="oil-spill and smoke photos (neutral, factual).", cue="NOTE"),
    ],
    [
        ("What is the FIRST step in using petroleum?", ["A. refine it","B. extract it","C. burn it","D. transport it"], "B. Extract (take it from the ground) first."),
        ("Burning fuel heats water into —", ["A. ice","B. steam","C. oil","D. coal"], "B. Steam spins the turbine."),
        ("In a power plant, the generator makes —", ["A. steam","B. heat","C. electricity","D. fuel"], "C. The generator makes electricity."),
        ("Which is a BENEFIT of fossil fuels?", ["A. oil spills","B. mining danger","C. heating homes and cooking","D. air pollution"], "C. Heating and cooking are benefits."),
        ("Which is a LIMITATION of fossil fuels?", ["A. they power engines","B. they can cause pollution and spills","C. they make electricity","D. they heat homes"], "B. Pollution and spills are limitations."),
    ])

# ---- Ch4
outline(4, "Nuclear Energy", "unit-02-ch4-nuclear-energy-guided-notes.docx",
    "What is nuclear power?",
    "a cooling tower photo — steam rises; is that smoke or steam?",
    [
        dict(title="Key Words: nuclear energy, uranium",
             supports="Page 1 · Key Words",
             key="Nuclear energy comes from a material called uranium (mined from rock).",
             action="NOTE — complete the two fill-ins.",
             visual="uranium ore + fuel pellet photo.", cue="NOTE"),
        dict(title="Key Idea: same pathway as coal",
             supports="Page 1 · Key Idea",
             key="Nuclear power uses heat to make electricity — the same pathway as coal.",
             action="NOTE — highlight the key idea.",
             visual="coal plant vs. nuclear plant side-by-side, same turbine/generator boxes.", cue="NOTE"),
        dict(title="Electricity Pathway",
             supports="Page 1 · Electricity Pathway",
             key="nuclear heat → boil water into steam → spin a turbine → turn a generator → electricity.",
             action="NOTE — copy the pathway.",
             visual="nuclear plant cutaway with heat/steam/turbine/generator arrows.", cue="NOTE", reveal="staged"),
        dict(title="Benefits and Limitations",
             supports="Page 2 · Benefits and Limitations",
             key="Benefits: reliable, little air pollution. Limitations: nonrenewable, used fuel must be stored safely.",
             action="NOTE — fill benefit/limitation rows.",
             visual="two-column table.", cue="NOTE"),
        dict(title="Safety First",
             supports="Page 2 · Safety First",
             key="Heat must be controlled; used fuel is stored safely.",
             action="NOTE — complete the two fills.",
             visual="containment/storage diagram (neutral, factual).", cue="NOTE"),
    ],
    [
        ("Nuclear power plants make electricity using —", ["A. wind","B. heat from boiling water into steam","C. sunlight","D. coal"], "B. Heat boils water into steam that spins a turbine."),
        ("Uranium is —", ["A. renewable","B. a fossil fuel","C. a mined material used for nuclear energy","D. a gas"], "C. Uranium is mined from rock."),
        ("A nuclear plant and a coal plant both use —", ["A. uranium","B. a steam-spun turbine and generator","C. solar cells","D. wind"], "B. Both use the heat → steam → turbine → generator pathway."),
        ("Which is a LIMITATION of nuclear power?", ["A. reliable electricity","B. little air pollution","C. used fuel stays dangerous a long time","D. it heats homes"], "C. Used fuel must be stored safely for a very long time."),
        ("The mechanism of nuclear fission (splitting atoms) is —", ["A. the main learning goal","B. NOT a required learning objective","C. the only thing to memorize","D. how solar cells work"], "B. We learn heat → steam → turbine → generator, not fission detail."),
    ])

# ---- Ch5
outline(5, "Wind Energy", "unit-02-ch5-wind-energy-guided-notes.docx",
    "How do people use wind as a source of energy?",
    "an island shuts off its diesel generator as wind turbines take over for the afternoon",
    [
        dict(title="Key Words: wind farm, turbine",
             supports="Page 1 · Key Words",
             key="A turbine has blades that spin when wind pushes them; many together make a wind farm.",
             action="NOTE — complete the two fill-ins.",
             visual="wind farm photo + turbine diagram.", cue="NOTE"),
        dict(title="Electricity Pathway",
             supports="Page 1 · Electricity Pathway",
             key="moving air → turns the blades → spins the generator → electricity.",
             action="NOTE — copy the pathway; then DRAW a labeled turbine.",
             visual="turbine cutaway: blades, shaft, generator with arrows.", cue="NOTE / DRAW / LABEL", reveal="staged"),
        dict(title="Benefits and Limitations",
             supports="Page 2 · Benefits and Limitations",
             key="Benefits: renewable, no fuel burned. Limitations: needs wind, not always blowing.",
             action="NOTE — fill benefit/limitation rows.",
             visual="two-column table.", cue="NOTE"),
        dict(title="Location Matters",
             supports="Page 2 · Location Matters",
             key="Wind works best where it blows steadily and strongly enough.",
             action="NOTE — complete the fill about batteries.",
             visual="windy coast vs. calm inland map/photo.", cue="NOTE"),
    ],
    [
        ("Wind turns the blades, which —", ["A. cool the air","B. spin a generator to make electricity","C. store water","D. burn fuel"], "B. Blades spin a generator that makes electricity."),
        ("Wind is called renewable because —", ["A. it is always windy","B. wind keeps coming back","C. turbines last forever","D. wind is cheap"], "B. Wind is restored naturally and continuously."),
        ("Wind power depends on —", ["A. coal","B. location and weather","C. uranium","D. dams"], "B. Wind power needs a steady, strong enough wind."),
        ("Which is a LIMITATION of wind?", ["A. no fuel burned","B. renewable","C. not always blowing","D. makes electricity"], "C. Wind is not always blowing."),
    ])

# ---- Ch6
outline(6, "Hydroelectric Energy", "unit-02-ch6-hydroelectric-energy-guided-notes.docx",
    "How do people use moving water as a source of energy?",
    "a dam releases water that spins turbines — the reservoir is a stored source of energy",
    [
        dict(title="Key Words: hydroelectric, reservoir",
             supports="Page 1 · Key Words",
             key="Hydroelectric power = electricity from moving water (usually through a dam). A reservoir holds water behind the dam.",
             action="NOTE — complete the two fill-ins.",
             visual="dam + reservoir diagram.", cue="NOTE"),
        dict(title="Electricity Pathway",
             supports="Page 1 · Electricity Pathway",
             key="water in a reservoir → flows through the dam → spins a turbine → turns a generator → electricity.",
             action="NOTE — copy the pathway.",
             visual="dam cross-section with reservoir/intake/turbine/generator arrows.", cue="NOTE", reveal="staged"),
        dict(title="Benefits and Limitations",
             supports="Page 2 · Benefits and Limitations",
             key="Benefits: renewable, predictable (water stored). Limitations: floods land, can block fish.",
             action="NOTE — fill benefit/limitation rows.",
             visual="two-column table.", cue="NOTE"),
        dict(title="Caring for Rivers",
             supports="Page 2 · Caring for Rivers",
             key="Fish ladders help salmon move past a dam.",
             action="NOTE — complete the fill; then DRAW a labeled dam.",
             visual="fish ladder photo + dam diagram template.", cue="NOTE / DRAW / LABEL"),
    ],
    [
        ("What holds water for a hydroelectric dam?", ["A. a wind farm","B. a reservoir","C. a solar panel","D. a mine"], "B. The reservoir holds water behind the dam."),
        ("Moving water spins a —", ["A. generator directly","B. turbine connected to a generator","C. solar cell","D. boiler"], "B. Water spins a turbine that turns a generator."),
        ("Hydroelectric is more predictable than wind because —", ["A. water can be stored","B. water never stops","C. dams are cheap","D. rivers are everywhere"], "A. Water can be stored behind a dam."),
        ("Which is a LIMITATION of dams?", ["A. renewable","B. they flood land and can block fish","C. no fuel burned","D. make electricity"], "B. Dams flood land and can block fish like salmon."),
    ])

# ---- Ch7
outline(7, "Solar Energy", "unit-02-ch7-solar-energy-guided-notes.docx",
    "How do people use sunlight as a source of energy?",
    "a solar farm powers a town — but what happens when clouds come or the sun sets?",
    [
        dict(title="Key Words: solar power, solar cell",
             supports="Page 1 · Key Words",
             key="Solar power = using sunlight. A solar cell converts sunlight to electricity.",
             action="NOTE — complete the two fill-ins.",
             visual="solar cell close-up + panel.", cue="NOTE"),
        dict(title="Electricity Pathway",
             supports="Page 1 · Electricity Pathway",
             key="sunlight → strikes a solar cell → makes electricity.",
             action="NOTE — copy the pathway.",
             visual="sun → panel → wire → light bulb chain.", cue="NOTE", reveal="staged"),
        dict(title="Other Ways to Use Sunlight",
             supports="Page 1 · Other Ways",
             key="Sunlight can heat water and cook food (solar oven).",
             action="NOTE — fill the three rows.",
             visual="solar oven + rooftop water heater photos.", cue="NOTE"),
        dict(title="Benefits and Limitations",
             supports="Page 2 · Benefits and Limitations",
             key="Benefits: renewable, no fuel burned. Limitations: needs sunlight, costs to install.",
             action="NOTE — fill benefit/limitation rows.",
             visual="two-column table.", cue="NOTE"),
        dict(title="Available Light",
             supports="Page 2 · Available Light",
             key="Solar depends on light that is available — location, weather, time of day.",
             action="NOTE — complete the two fills.",
             visual="sunny vs. cloudy vs. night comparison.", cue="NOTE"),
    ],
    [
        ("A solar cell converts —", ["A. wind to electricity","B. sunlight to electricity","C. heat to light","D. water to steam"], "B. A solar cell converts sunlight to electricity."),
        ("Why is solar called renewable but not always available?", ["A. the sun burns out","B. sunlight depends on location and time","C. panels break daily","D. solar is nonrenewable"], "B. Sunlight depends on location, weather, and time."),
        ("On a cloudy day, a solar panel makes —", ["A. more electricity","B. less electricity","C. no difference","D. steam"], "B. Less sunlight means less electricity."),
        ("Which is a LIMITATION of solar?", ["A. free sunlight","B. no fuel burned","C. costs money to install","D. renewable"], "C. Installation cost is a limitation."),
    ])

# ---- Ch8
outline(8, "Geothermal Energy", "unit-02-ch8-geothermal-energy-guided-notes.docx",
    "What is geothermal energy, and how do people use it?",
    "a cabin far from power lines is warmed by heat piped from deep underground",
    [
        dict(title="Key Words: geothermal energy",
             supports="Page 1 · Key Words",
             key="Geothermal energy = heat transferred from inside Earth.",
             action="NOTE — complete the fill-in.",
             visual="geothermal heat pump diagram (pipes into ground).", cue="NOTE"),
        dict(title="Two Ways to Use It",
             supports="Page 1 · Two Ways",
             key="Heat homes/buildings; or make electricity (steam spins a turbine).",
             action="NOTE — fill the two rows.",
             visual="heat pump + steam power plant side-by-side.", cue="NOTE"),
        dict(title="Electricity Pathway",
             supports="Page 1 · Electricity Pathway",
             key="heat from Earth → boils water into steam → spins a turbine → turns a generator → electricity.",
             action="NOTE — copy the pathway.",
             visual="geothermal plant cutaway with arrows.", cue="NOTE", reveal="staged"),
        dict(title="Benefits and Limitations",
             supports="Page 2 · Benefits and Limitations",
             key="Benefits: little pollution, heat always available underground. Limitations: needs hot rock, costly.",
             action="NOTE — fill benefit/limitation rows.",
             visual="two-column table.", cue="NOTE"),
        dict(title="Location Matters",
             supports="Page 2 · Location Matters",
             key="Most steam/hot-water sources are near volcanic areas.",
             action="NOTE — complete the fill.",
             visual="volcanic region map/photo.", cue="NOTE"),
    ],
    [
        ("Geothermal energy comes from —", ["A. the sun","B. wind","C. heat inside Earth","D. moving water"], "C. Heat transferred from Earth's interior."),
        ("Where does geothermal work best?", ["A. everywhere","B. near hot rock / volcanic areas","C. only at the poles","D. only in deserts"], "B. Areas where Earth's crust is active."),
        ("Which is a BENEFIT of geothermal?", ["A. little pollution","B. needs hot rock","C. costly to build","D. only in some places"], "A. Geothermal produces little pollution."),
        ("Which is a LIMITATION of geothermal?", ["A. clean","B. heat is always underground","C. needs a special location","D. renewable"], "C. It needs a special (volcanic) location."),
    ])

# ---- Ch9
outline(9, "Energy Resource Innovations", "unit-02-ch9-energy-resource-innovations-guided-notes.docx",
    "What other energy resources are being developed?",
    "a sidewalk tile lights up when someone steps on it — energy from everyday motion",
    [
        dict(title="Key Words: biofuel, hybrid",
             supports="Page 1 · Key Words",
             key="Biofuel = fuel from recently living organisms. Hybrid = a vehicle with two fuel sources.",
             action="NOTE — complete the two fill-ins.",
             visual="ethanol pump + hybrid car photo.", cue="NOTE"),
        dict(title="New Ideas",
             supports="Page 1 · New Ideas",
             key="biofuels, electric/hybrid cars, fuel cells (hydrogen), wave energy, motion-harvesting tiles/clothing.",
             action="NOTE — fill the five rows.",
             visual="icon grid of the five innovations.", cue="NOTE"),
        dict(title="Engineering Better Systems",
             supports="Page 2 · Engineering",
             key="Engineers make systems more efficient, less wasteful, and safer.",
             talk="regenerative braking turns motion energy back into electricity; better cells convert more sunlight.",
             action="NOTE — complete the two fills.",
             visual="regenerative braking + solar cell efficiency graphic.", cue="NOTE"),
        dict(title="Draw / Label: your own idea",
             supports="Page 2 · Draw/Label",
             key="Design your own energy idea and label the parts.",
             action="DRAW — complete the design box.",
             visual="empty design template box.", cue="DRAW / LABEL"),
    ],
    [
        ("Ethanol is a —", ["A. fossil fuel","B. biofuel","C. mineral","D. nuclear fuel"], "B. Ethanol is a biofuel from plants."),
        ("A hybrid car uses —", ["A. one fuel","B. two different sources of fuel","C. no energy","D. only sunlight"], "B. A hybrid uses two fuel sources."),
        ("Regenerative braking turns motion energy into —", ["A. heat only","B. electricity stored in a battery","C. gasoline","D. steam"], "B. It converts motion into electricity stored in a battery."),
        ("Why do engineers keep improving energy systems?", ["A. to use more fuel","B. to make them more efficient and less wasteful","C. to stop testing","D. to make them cost more"], "B. To make systems more efficient, safer, and less wasteful."),
        ("Wave energy is really another way to harness —", ["A. wind energy","B. coal","C. uranium","D. geothermal heat"], "A. Waves are made by wind; water delivers the motion."),
    ])
