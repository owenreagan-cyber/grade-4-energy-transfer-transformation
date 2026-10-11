import subprocess
from PIL import Image

image = Image.open("qa/work/ch3-factory-2026-10-06/renders/03-ch3-energy-speed-slides-p002-300dpi.png").convert("RGB")
print("corner", image.getpixel((10, 10)), "mid", image.getpixel((2000, 200)))
notes = "production/premium-notes/03-ch3-energy-speed-guided-notes.pdf"
print(subprocess.run(["pdftotext", notes, "-"], capture_output=True, text=True).stdout[:180])
print("images")
print(subprocess.run(["pdfimages", "-list", "production/slides/03-ch3-energy-speed-slides.pdf"], capture_output=True, text=True).stdout[:800])
text = open("docs/chapter-03/CH3_PLAYBOOK_REGION.md", encoding="utf-8").read()
print("--- LAB region ---")
start = text.find("## LAB")
print(text[start:start + 400] if start >= 0 else "NO LAB HEADING")
print("headings", [line for line in text.splitlines() if line.startswith("## ")])
