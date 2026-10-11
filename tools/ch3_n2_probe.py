import sys
sys.path.insert(0, "tools")
from ch3_seal_remaining import contains_line, docx_text, slide_text, spec
chapter = spec()
notes = docx_text("production/premium-notes/03-ch3-energy-speed-guided-notes.docx")
slides = "\n".join(body for body, _note in slide_text())
row = next(item for item in chapter["anchors"] if item["code"] == "N2")
for line in row["lines"]:
    print("NOTES", contains_line(notes, line), "SLIDES", contains_line(slides, line), "|", line)
print("JOIN notes", contains_line(notes, " ".join(row["lines"])))
print("JOIN slides", contains_line(slides, " ".join(row["lines"])))
