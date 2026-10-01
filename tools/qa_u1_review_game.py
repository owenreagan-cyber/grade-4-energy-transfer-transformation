#!/usr/bin/env python3
"""Phase 13Z QA — verify the Unit 1 review game hyperlinks, slide order, and
off-scope vocabulary. Parses the packed .pptx relationships directly."""
import os, re, sys, zipfile

PPTX = sys.argv[1] if len(sys.argv) > 1 else \
    "/Users/owen/Projects/grade-4-energy-transfer-transformation/tools/.pptxbuild/unit1-review-game.pptx"

N_CAT = 5
N_VAL = 5
SL_BOARD = 3

def qSlide(c, v):
    return 4 + 2 * (c * N_VAL + v)

def aSlide(c, v):
    return qSlide(c, v) + 1

def slide_rels(z):
    """Return dict slide_num -> list of target slide numbers."""
    out = {}
    for name in z.namelist():
        m = re.match(r'ppt/slides/_rels/slide(\d+)\.xml\.rels$', name)
        if not m:
            continue
        n = int(m.group(1))
        data = z.read(name).decode('utf-8', 'ignore')
        targets = [int(t) for t in re.findall(r'Target="slide(\d+)\.xml"', data)]
        out[n] = targets
    return out

def slide_text(z, n):
    """Extract plain text from slide n's XML."""
    name = f'ppt/slides/slide{n}.xml'
    data = z.read(name).decode('utf-8', 'ignore')
    # a:t elements hold text runs
    texts = re.findall(r'<a:t>(.*?)</a:t>', data)
    return ' '.join(texts)

def main():
    z = zipfile.ZipFile(PPTX)
    rels = slide_rels(z)
    errors = []

    # 1. slide count / presence
    slides = sorted(int(m.group(1)) for m in
                    [re.match(r'ppt/slides/slide(\d+)\.xml$', n) for n in z.namelist()]
                    if m)
    expected_total = 3 + 2 * N_CAT * N_VAL  # 53
    print(f"Slides present: {len(slides)} (expected {expected_total})")
    if len(slides) != expected_total:
        errors.append(f"slide count {len(slides)} != {expected_total}")

    # 2. board tiles -> question slides
    board = rels.get(SL_BOARD, [])
    # dedupe
    board_targets = sorted(set(board))
    expected_tiles = sorted(set(qSlide(c, v) for c in range(N_CAT) for v in range(N_VAL)))
    print(f"Board tile targets ({len(board_targets)}): {board_targets}")
    if board_targets != expected_tiles:
        errors.append(f"board targets mismatch: got {board_targets}, want {expected_tiles}")

    # 3. question slides -> reveal answer (answer slide) + board
    # 4. answer slides -> back to board + back to question
    for c in range(N_CAT):
        for v in range(N_VAL):
            q = qSlide(c, v)
            a = aSlide(c, v)
            qt = set(rels.get(q, []))
            at = set(rels.get(a, []))
            if a not in qt:
                errors.append(f"Q slide {q} (cat{c+1} ${(v+1)*100}) missing link to answer {a}")
            if SL_BOARD not in qt:
                errors.append(f"Q slide {q} missing link to board {SL_BOARD}")
            if SL_BOARD not in at:
                errors.append(f"A slide {a} missing link to board {SL_BOARD}")
            if q not in at:
                errors.append(f"A slide {a} missing link back to question {q}")

    # 5. no external URLs (http/https/file) anywhere
    ext = []
    for name in z.namelist():
        if name.endswith('.xml.rels') or name.endswith('.xml'):
            data = z.read(name).decode('utf-8', 'ignore')
            if re.search(r'Target="(https?://|file://|mailto:)', data):
                ext.append(name)
    if ext:
        errors.append(f"external link targets found: {ext}")

    # 6. off-scope vocabulary scan across all slide text
    offscope = [r'\bkinetic\b', r'\bpotential\b', r'mechanical energy', r'chemical energy',
                r'thermal energy', r'\bradiant\b', r'\bmomentum\b', r'\bforce\b', r'\bimpulse\b',
                r'\bdeformation\b', r'\bproves\b', r'\bprove\b']
    full_text = []
    for n in slides:
        full_text.append(slide_text(z, n))
    joined = ' '.join(full_text).lower()
    hits = {}
    for term in offscope:
        m = re.findall(term, joined)
        if m:
            hits[term] = len(m)
    if hits:
        errors.append(f"off-scope terms found: {hits}")
    else:
        print("Off-scope vocabulary: clean")

    # 7. report
    print("\n" + "=" * 60)
    if errors:
        print("FAILURES:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL CHECKS PASSED")
        print(f"  {len(board_targets)} board tiles -> questions  : OK")
        print(f"  {N_CAT*N_VAL} questions -> answer reveals   : OK")
        print(f"  {N_CAT*N_VAL} answers -> back to board      : OK")
        print("  no external link dependencies            : OK")

if __name__ == '__main__':
    main()
