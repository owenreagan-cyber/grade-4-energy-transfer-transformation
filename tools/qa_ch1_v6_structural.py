#!/usr/bin/env python3
"""Phase 5H — run the frozen 28-gate canonical structural QA against the v6 embedded-media candidate."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa_ch1_slides as Q

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CAND = os.path.join(ROOT, "production", "candidates", "chapter-01", "ch1-premium-hybrid-v6-embedded-media")
Q.PPTX = os.path.join(CAND, "01-ch1-energy-causes-change-premium-hybrid-v6-embedded-media.pptx")
Q.PDF = os.path.join(CAND, "01-ch1-energy-causes-change-premium-hybrid-v6-embedded-media.pdf")
Q.REPORT = os.path.join(ROOT, "qa", "reports", "ch1-phase5g", "CH1_STRUCTURAL_QA_5H.md")

if __name__ == "__main__":
    Q.main()
