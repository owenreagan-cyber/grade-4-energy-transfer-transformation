#!/usr/bin/env python3
"""Phase 5B · Gate 2 structural QA — reuse the frozen canonical gates against the premium candidate.

Overrides qa_ch1_slides.py module paths to point at the premium hybrid candidate, then runs the
full 28-gate canonical suite (sequence, anchors, notes mirror, reveal, review letters, banned vocab,
pacing notes, font tiers, overflow, tokens, render geometry). No canonical file is modified.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa_ch1_slides as Q

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CAND = os.path.join(ROOT, "production", "candidates", "chapter-01", "ch1-premium-hybrid-v1")

Q.PPTX = os.path.join(CAND, "01-ch1-energy-causes-change-premium-hybrid-v1.pptx")
Q.PDF = os.path.join(CAND, "01-ch1-energy-causes-change-premium-hybrid-v1.pdf")
Q.REPORT = os.path.join(ROOT, "qa", "reports", "ch1-phase5b", "CH1_STRUCTURAL_QA.md")

if __name__ == "__main__":
    Q.main()
