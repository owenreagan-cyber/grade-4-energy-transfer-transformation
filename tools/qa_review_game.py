#!/usr/bin/env python3
"""Shared review-game QA (Phases 13Z + 13AA).

Verifies the clickable board hyperlinks, slide ordering, absence of external
link dependencies, and off-scope vocabulary. Supports both Unit 1 (53 slides)
and Unit 2 (55 slides incl. final challenge) via --unit.

Usage:
  python qa_review_game.py <deck.pptx> --unit 1|2
"""
import argparse, re, sys, zipfile

N_CAT = 5
N_VAL = 5
SL_BOARD = 3

OFFSCOPE = {
    1: [r'\bkinetic\b', r'\bpotential\b', r'mechanical energy', r'chemical energy',
        r'\bthermal energy\b', r'\bradiant\b', r'\bmomentum\b', r'\bforce\b', r'\bimpulse\b',
        r'\bdeformation\b', r'\bproves\b', r'\bprove\b'],
    2: [r'\bfission\b', r'\bU-235\b', r'\bkinetic\b', r'mechanical energy', r'chemical energy',
        r'\bthermal energy\b', r'\bradiant\b', r'\belectron\b', r'\bphoton\b', r'\bsemiconductor\b',
        r'\bbaseload\b', r'\bdispatch\b', r'grid stabilization', r'peak demand',
        r'climate change', r'global warming', r'carbon footprint', r'\bgreen energy\b',
        r'\bclean energy\b', r'zero emissions', r'\bpolicy\b', r'\bactivism\b',
        r'\bpotential\b', r'\bmomentum\b', r'\bforce\b', r'\bimpulse\b', r'\bdeformation\b',
        r'\bproves\b', r'\bprove\b'],
}

def qSlide(c, v):
    return 4 + 2 * (c * N_VAL + v)

def aSlide(c, v):
    return qSlide(c, v) + 1

def finalQSlide():
    return 4 + 2 * N_CAT * N_VAL      # 54

def finalASlide():
    return finalQSlide() + 1          # 55

def slide_rels(z):
    out = {}
    for name in z.namelist():
        m = re.match(r'ppt/slides/_rels/slide(\d+)\.xml\.rels$', name)
        if not m:
            continue
        n = int(m.group(1))
        data = z.read(name).decode('utf-8', 'ignore')
        out[n] = [int(t) for t in re.findall(r'Target="slide(\d+)\.xml"', data)]
    return out

def slide_text(z, n):
    data = z.read(f'ppt/slides/slide{n}.xml').decode('utf-8', 'ignore')
    return ' '.join(re.findall(r'<a:t>(.*?)</a:t>', data))

def run(pptx_path, unit, has_final):
    z = zipfile.ZipFile(pptx_path)
    rels = slide_rels(z)
    errors = []

    slides = sorted(int(m.group(1)) for m in
                    [re.match(r'ppt/slides/slide(\d+)\.xml$', n) for n in z.namelist()] if m)
    expected_total = 3 + 2 * N_CAT * N_VAL + (2 if has_final else 0)
    print(f"Slides present: {len(slides)} (expected {expected_total})")
    if len(slides) != expected_total:
        errors.append(f"slide count {len(slides)} != {expected_total}")

    # board tiles -> questions
    board_targets = sorted(set(rels.get(SL_BOARD, [])))
    expected_tiles = sorted(set(qSlide(c, v) for c in range(N_CAT) for v in range(N_VAL)))
    if has_final:
        expected_tiles = sorted(expected_tiles + [finalQSlide()])
    print(f"Board tile targets ({len(board_targets)}): {board_targets}")
    if board_targets != expected_tiles:
        errors.append(f"board targets mismatch: got {board_targets}, want {expected_tiles}")

    for c in range(N_CAT):
        for v in range(N_VAL):
            q, a = qSlide(c, v), aSlide(c, v)
            qt, at = set(rels.get(q, [])), set(rels.get(a, []))
            if a not in qt:
                errors.append(f"Q slide {q} (FILE{c+1} ${(v+1)*100}) missing link to answer {a}")
            if SL_BOARD not in qt:
                errors.append(f"Q slide {q} missing link to board {SL_BOARD}")
            if SL_BOARD not in at:
                errors.append(f"A slide {a} missing link to board {SL_BOARD}")
            if q not in at:
                errors.append(f"A slide {a} missing link back to question {q}")

    if has_final:
        fq, fa = finalQSlide(), finalASlide()
        fqt, fat = set(rels.get(fq, [])), set(rels.get(fa, []))
        if fa not in fqt:
            errors.append(f"Final challenge Q {fq} missing link to answer {fa}")
        if SL_BOARD not in fqt:
            errors.append(f"Final challenge Q {fq} missing link to board")
        if SL_BOARD not in fat:
            errors.append(f"Final challenge A {fa} missing link to board")

    ext = []
    for name in z.namelist():
        if name.endswith('.xml.rels') or name.endswith('.xml'):
            data = z.read(name).decode('utf-8', 'ignore')
            if re.search(r'Target="(https?://|file://|mailto:)', data):
                ext.append(name)
    if ext:
        errors.append(f"external link targets found: {ext}")

    joined = ' '.join(slide_text(z, n) for n in slides).lower()
    hits = {t: len(re.findall(t, joined)) for t in OFFSCOPE[unit] if re.findall(t, joined)}
    if hits:
        errors.append(f"off-scope terms found: {hits}")
    else:
        print("Off-scope vocabulary: clean")

    print("\n" + "=" * 60)
    if errors:
        print("FAILURES:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL CHECKS PASSED")
        print(f"  {N_CAT*N_VAL} board tiles -> questions  : OK")
        print(f"  {N_CAT*N_VAL} questions -> answer reveals   : OK")
        print(f"  {N_CAT*N_VAL} answers -> back to board      : OK")
        if has_final:
            print("  final challenge -> reveal -> board  : OK")
        print("  no external link dependencies       : OK")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pptx')
    ap.add_argument('--unit', type=int, choices=[1, 2], default=1)
    ap.add_argument('--final', dest='has_final', action='store_true', help='deck includes a final challenge slide pair')
    args = ap.parse_args()
    run(args.pptx, args.unit, args.has_final)

if __name__ == '__main__':
    main()
