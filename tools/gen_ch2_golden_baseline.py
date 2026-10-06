"""Write the Chapter 2 golden text snapshot from the current canonical sources.

Run once when the reviewed text is accepted. Do not call this from release builds.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch2_golden_collect import collect, exact_chrome, playbook_chapter_region

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "qa/baselines/ch2_golden_text.json")


def main():
    data = collect(ROOT)
    data["exact_chrome"] = exact_chrome(data)
    data["role"] = "PRE-FREEZE approved Chapter 2 instructional text. Post-freeze edits require a reviewed baseline update."
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(data, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(OUT)
    print("slides", len(data["artifacts"]["slides"]["slides"]))
    print("chrome lines", len(data["exact_chrome"]))
    region = playbook_chapter_region(os.path.join(ROOT, data["artifacts"]["playbook"]["path"]))
    print("playbook entries", len(region["lines"]))
    print("playbook paragraphs", len(region["paragraphs"]))
    print("playbook table rows", len(region["rows"]))
    print("playbook first", region["lines"][0])
    print("playbook last", region["lines"][-1])


if __name__ == "__main__":
    main()
