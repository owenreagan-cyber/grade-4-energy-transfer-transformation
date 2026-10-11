import sys
sys.path.insert(0, "tools")
from ch3_seal_remaining import docx_text
print("PRACTICE")
print(docx_text("production/worksheets/03-ch3-energy-speed-practice.docx"))
print("---KEY---")
print(open("production/answer-keys/03-ch3-energy-speed-practice-key.md", encoding="utf-8").read())
