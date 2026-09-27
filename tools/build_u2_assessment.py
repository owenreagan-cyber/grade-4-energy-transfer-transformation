"""Unit 2 written assessment — student + teacher key (22 points).

Assesses: renewable vs nonrenewable, abundant vs renewable, fossil fuels, nuclear, wind,
hydro, solar, geothermal, innovations, benefits/limitations, energy pathways.
No: base-load, scrubber detail, fission mechanics, battery-only-night assumptions.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gn_design import *

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
    "production", "quizzes", "unit-02"))
os.makedirs(OUT_DIR, exist_ok=True)
SUB = "Unit 2 Written Assessment · Using Natural Resources for Energy"

def save(doc, fn):
    doc.save(os.path.join(OUT_DIR, fn))
    print("saved", fn)

def build_student():
    doc = new_doc()
    title_block(doc, "Using Natural Resources for Energy", SUB + " · Student")
    body(doc, "Name: ____________________________    Date: ____________    Score: ______ / 22", size=12, bold=True, after=30)

    heading(doc, "Part A · Matching (8 points)")
    body(doc, "Write the letter of the meaning next to each term.", size=12, color=GRAY, after=16)
    two_col_table(doc, ["Term", "Meaning (write the letter)"],
        [("1. renewable resource", ""),
         ("2. nonrenewable resource", ""),
         ("3. fossil fuel", ""),
         ("4. turbine", ""),
         ("5. generator", ""),
         ("6. solar cell", ""),
         ("7. geothermal energy", ""),
         ("8. hydroelectric power", "")],
        col_widths=(3600, FULL_W - 3600), row_h=420)
    body(doc, "Meanings:", size=12, bold=True, after=6)
    body(doc, "A. heat that is transferred from inside Earth", size=12, after=4)
    body(doc, "B. electricity made from moving water, usually through a dam", size=12, after=4)
    body(doc, "C. a machine with blades that spins when steam, wind, or water pushes it", size=12, after=4)
    body(doc, "D. a resource that cannot be restored as quickly as it is used", size=12, after=4)
    body(doc, "E. a device that converts sunlight to electricity", size=12, after=4)
    body(doc, "F. a machine that makes electricity when a turbine spins it", size=12, after=4)
    body(doc, "G. a fuel formed from the remains of organisms that lived long ago", size=12, after=4)
    body(doc, "H. a resource that can be restored as quickly as it is used", size=12, after=16)

    # PAGE 2
    title_block(doc, "Parts B–C", SUB + " · Page 2", new_page=True)
    heading(doc, "Part B · Multiple Choice (5 points)")
    body(doc, "Circle the best answer.", size=12, color=GRAY, after=12)
    body(doc, "1. Coal is plentiful now but forms over millions of years. Coal is —", size=13, bold=True, after=2)
    body(doc, "   A. renewable    B. nonrenewable    C. a solar resource    D. not a resource", size=12, after=8)
    body(doc, "2. Abundant means a resource is —", size=13, bold=True, after=2)
    body(doc, "   A. always renewable    B. plentiful right now    C. free    D. restored quickly", size=12, after=8)
    body(doc, "3. In a power plant, the generator makes —", size=13, bold=True, after=2)
    body(doc, "   A. steam    B. heat    C. electricity    D. fuel", size=12, after=8)
    body(doc, "4. Which resource needs a windy location to work well?", size=13, bold=True, after=2)
    body(doc, "   A. geothermal    B. wind    C. coal    D. petroleum", size=12, after=8)
    body(doc, "5. Which is a renewable resource?", size=13, bold=True, after=2)
    body(doc, "   A. uranium    B. natural gas    C. sunlight    D. coal", size=12, after=10)

    heading(doc, "Part C · Energy Pathway (3 points)")
    body(doc, "Number the electricity pathway in order from 1 to 5.", size=12, color=GRAY, after=12)
    two_col_table(doc, ["Step", "Order"],
        [("spin a turbine", ""), ("burn the fuel", ""), ("turn a generator", ""),
         ("heat water into steam", ""), ("electricity", "")], row_h=320)

    # PAGE 3
    title_block(doc, "Parts D–E", SUB + " · Page 3", new_page=True)
    heading(doc, "Part D · Renewable or Nonrenewable (3 points)")
    body(doc, "Write R for renewable or N for nonrenewable.", size=12, color=GRAY, after=12)
    two_col_table(doc, ["Resource", "R or N"],
        [("coal", ""), ("wind", ""), ("petroleum", ""), ("sunlight", ""), ("uranium", ""), ("flowing water", "")],
        row_h=240)

    heading(doc, "Part E · Scenario (3 points)")
    body(doc, "A town gets strong, steady wind most of the year. It has no large river nearby and many cloudy days.", size=13, bold=True, after=12)
    body(doc, "1. Which resource would be reasonable to investigate for this town? ____________________", size=13, after=12)
    body(doc, "2. Write one fact that supports your choice.", size=13, after=6)
    wline(doc, 1, gap=24, after=10)
    body(doc, "3. Write one limitation they would still need to consider.", size=13, after=6)
    wline(doc, 1, gap=24, after=10)

    heading(doc, "Check Your Thinking")
    body(doc, "Why does a higher water wheel lift more paperclips? Use the words energy of motion and transfer in your answer.", size=13, bold=True, after=8)
    wline(doc, 2, gap=24, after=16)
    save(doc, "unit-2-written-assessment-student.docx")

def build_key():
    doc = new_doc()
    title_block(doc, "Using Natural Resources for Energy", SUB + " · Teacher Key")
    heading(doc, "Part A · Matching (8 points)")
    body(doc, "1-H · 2-D · 3-G · 4-C · 5-F · 6-E · 7-A · 8-B", size=13, after=16)
    heading(doc, "Part B · Multiple Choice (5 points)")
    body(doc, "1-B · 2-B · 3-C · 4-B · 5-C", size=13, after=16)
    heading(doc, "Part C · Energy Pathway (3 points)")
    body(doc, "burn the fuel (1) → heat water into steam (2) → spin a turbine (3) → turn a generator (4) → electricity (5)", size=13, after=16)
    heading(doc, "Part D · Renewable or Nonrenewable (3 points)")
    body(doc, "coal N · wind R · petroleum N · sunlight R · uranium N · flowing water R", size=13, after=16)
    heading(doc, "Part E · Scenario (3 points)")
    body(doc, "1. Wind. 2. Strong, steady wind most of the year (supports wind). 3. Wind can be calm some days / needs a windy location. (Accept any reasoned choice with one fact + one limitation.)", size=13, after=16)
    heading(doc, "Check Your Thinking (2 points)")
    body(doc, "Falling water from higher up has more energy of motion. That energy transfers to the wheel, which lifts more paperclips.", size=13, after=16)
    body(doc, "Total: 22 points.", size=13, bold=True, after=16)
    save(doc, "unit-2-written-assessment-key.docx")

if __name__ == "__main__":
    build_student()
    build_key()
    print("DONE")
