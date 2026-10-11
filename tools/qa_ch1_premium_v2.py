#!/usr/bin/env python3
"""Phase 5C structural QA — re-run the frozen 28-gate canonical suite (tools/qa_ch1_slides.py) against the
ch1-premium-hybrid-v2 candidate. Paths are overridden in-process; no canonical or Phase 5B file is modified."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa_ch1_slides as Q

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CAND = os.environ.get("CH1_V2_OUT") or os.path.join(ROOT, "production", "candidates", "chapter-01", "ch1-premium-hybrid-v2")

Q.PPTX = os.path.join(CAND, "01-ch1-energy-causes-change-premium-hybrid-v2.pptx")
Q.PDF = os.path.join(CAND, "01-ch1-energy-causes-change-premium-hybrid-v2.pdf")
Q.REPORT = os.path.join(ROOT, "qa", "reports", "ch1-phase5c", "CH1_STRUCTURAL_QA_V2.md")

if __name__ == "__main__":
    Q.main()
