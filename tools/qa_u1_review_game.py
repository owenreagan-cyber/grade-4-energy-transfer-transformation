#!/usr/bin/env python3
"""Unit 1 review-game QA — thin wrapper over the shared qa_review_game.py."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_review_game import run

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: qa_u1_review_game.py <deck.pptx>")
        sys.exit(2)
    run(sys.argv[1], unit=1, has_final=False)
