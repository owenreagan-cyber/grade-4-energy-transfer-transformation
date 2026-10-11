#!/usr/bin/env python3
"""Chapter slides QA orchestrator (reusable).

Pipeline (deterministic, no builder metadata):
  structural (PPTX/txt) -> render PDF to PNG -> independent vision audit
  (blind) -> curriculum parity -> defect register -> markdown report.

Retrieval of the live Google Slides deck is performed by the Drive MCP layer
(see README.md); this tool consumes the exported artifacts.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parent / "lib"
sys.path.insert(0, str(LIB))

from structural import load_pptx, load_txt, summary as structural_summary
from render import render_pdf, pdf_page_count
from curriculum import run as curriculum_run
from vision import analyze, SLIDE_RUBRIC
from defects import DefectRegister, new_defect


def vision_audit(records: list[dict], out_dir: Path, limit: int = 0,
                 skip: bool = False) -> list[dict]:
    """Run the independent vision model on each rendered slide (blind)."""
    results = []
    items = records if not limit else records[:limit]
    for r in items:
        png = r["path"]
        out = out_dir / f"vision-{r['page']:02d}.json"
        if skip:
            results.append({"page": r["page"], "path": png, "vision": {"skipped": True}})
            continue
        try:
            v = analyze(png, SLIDE_RUBRIC)
        except Exception as e:  # noqa: BLE001
            v = {"error": str(e)}
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(v, indent=2), encoding="utf-8")
        results.append({"page": r["page"], "path": png, "vision": v})
    return results


def build_defects(vis: list[dict], slides: list[dict], reg: DefectRegister) -> None:
    """Map vision findings into the defect register."""
    slide_by_idx = {s["index"]: s for s in slides}
    for r in vis:
        v = r.get("vision", {})
        if not isinstance(v, dict) or v.get("skipped"):
            continue
        page = r["page"]
        sid = slide_by_idx.get(page, {}).get("stable_id", f"s{page:02d}")
        overall = v.get("overall", "")
        if overall not in ("FAIL", "WARN"):
            continue
        maps = {
            "text_issues": ("TEXT_CLIP_OVERFLOW", v.get("text_issues", [])),
            "readability_issues": ("FONT_READABILITY", v.get("readability_issues", [])),
            "image_issues": ("IMAGE_QUALITY", v.get("image_issues", [])),
            "overlap_issues": ("OVERLAP", v.get("overlap_issues", [])),
            "label_issues": ("LABEL_BADGE", v.get("label_issues", [])),
            "hierarchy_issues": ("HIERARCHY_ALIGNMENT", v.get("hierarchy_issues", [])),
            "science_issues": ("SCIENCE_ERROR", v.get("science_issues", [])),
            "answer_leak": ("ANSWER_LEAK", v.get("answer_leak", [])),
            "composition_issues": ("COMPOSITION", v.get("composition_issues", [])),
        }
        for _, (cat, items) in maps.items():
            for item in items:
                reg.add(new_defect(
                    slide=page, slide_id=sid, category=cat,
                    severity="MEDIUM" if overall == "WARN" else "HIGH",
                    evidence=[r["path"]], expected="", actual=str(item),
                    proposed_repair="review slide and correct the issue",
                ))


def render_markdown(bundle: dict, out: Path) -> None:
    lines = ["# Chapter Slides QA — Report", ""]
    lines.append(f"- Deck slide count: {bundle['structural']['slideCount']}")
    lines.append(f"- Video slides detected: {bundle['structural']['videoSlides']}")
    lines.append("")
    lines.append("## Curriculum parity")
    lines.append("| Check | Expected | Actual | Status |")
    lines.append("|---|---|---|---|")
    for c in bundle["curriculum"]["checks"]:
        exp = str(c.get("expected", "")).replace("|", "\\|")
        act = str(c.get("actual", "")).replace("|", "\\|")
        lines.append(f"| {c['check']} | {exp} | {act} | **{c['status']}** |")
    lines.append("")
    s = bundle["curriculum"]["summary"]
    lines.append(f"Parity summary: {s['pass']} pass / {s['fail']} fail / {s['warn']} warn of {s['total']}")
    lines.append("")
    lines.append("## Visual audit (independent vision model)")
    for r in bundle["visual"]:
        v = r.get("vision", {})
        if isinstance(v, dict) and "summary" in v:
            lines.append(f"- Slide {r['page']}: **{v.get('overall','?')}** — {v.get('summary','')}")
    out.write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pptx")
    ap.add_argument("--txt")
    ap.add_argument("--pdf")
    ap.add_argument("--expected", default="ch1/expected_ch1.json")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--limit", type=int, default=0, help="limit vision slides")
    ap.add_argument("--skip-vision", action="store_true")
    args = ap.parse_args()

    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    if args.pptx:
        slides = load_pptx(args.pptx)
    elif args.txt:
        slides = load_txt(args.txt)
    else:
        raise SystemExit("provide --pptx or --txt")

    bundle = {"structural": structural_summary(slides)}

    if args.pdf:
        renders_dir = out / "renders"
        records = render_pdf(args.pdf, str(renders_dir), args.dpi)
        bundle["renderedPages"] = len(records)
        vis = vision_audit(records, out / "vision", limit=args.limit, skip=args.skip_vision)
        bundle["visual"] = vis
    else:
        bundle["visual"] = []

    bundle["curriculum"] = curriculum_run(args.expected, slides)

    # defect register
    reg = DefectRegister(str(out / "defect-register.json"))
    build_defects(bundle["visual"], slides, reg)

    # curriculum-derived structural defects (slide count)
    struct = bundle["curriculum"]["checks"]
    for c in struct:
        if c["check"] == "slide_count" and c["status"] == "FAIL":
            reg.add(new_defect(
                slide=0, slide_id="deck", category="SLIDE_COUNT",
                severity="BLOCKING" if abs(c["expected"] - c["actual"]) != 0 else "MEDIUM",
                evidence=[], expected=str(c["expected"]), actual=str(c["actual"]),
                proposed_repair="reconcile slide count with canonical deck",
            ))
    reg.save()

    bundle["defects"] = reg.data["defects"]
    (out / "results.json").write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    render_markdown(bundle, out / "REPORT.md")
    print(json.dumps({
        "slideCount": bundle["structural"]["slideCount"],
        "videoSlides": bundle["structural"]["videoSlides"],
        "renderedPages": bundle.get("renderedPages", 0),
        "visualAudited": len(bundle["visual"]),
        "curriculum": bundle["curriculum"]["summary"],
        "defects": len(bundle["defects"]),
    }, indent=2))


if __name__ == "__main__":
    main()
