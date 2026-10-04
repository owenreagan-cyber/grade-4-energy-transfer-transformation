#!/usr/bin/env python3
"""
Unit 1 Visual System — automated QA.

Checks against assets/visual-system/design-tokens.json and the generated
SVG assets + sample pages:

  1. contrast (WCAG AA) — primary/neutral as text (4.5:1); accent as
     non-text/arrow (3:1)
  2. grayscale survival — desaturated primary/accent still >= 3:1 vs white;
     primary darker than accent
  3. font floors — sample content text respects floors (slide 28pt / handout
     body 12pt / caption 11pt)
  4. margins / overflow — every sample element stays within canvas + margins
  5. render integrity — every SVG rasterizes with rsvg-convert without error
  6. component consistency — HUD/badge dimensions uniform, palette keys complete
  7. token validation — freeze version 1.0 + canonical component dims present
  8. figma parity — parity manifest matches tokens + local generated assets
  9. grayscale proof — B/W proof sheet present, non-blank, all-gray pixels

Emits qa/temp/phase1_visual/qa_report.json and prints PASS/WARN/FAIL per gate.

Usage: .venv/bin/python tools/qa_visual_system.py
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS_PATH = os.path.join(ROOT, "assets", "visual-system", "design-tokens.json")
ASSET_ROOT = os.path.join(ROOT, "assets", "visual-system")
QA_ROOT = os.path.join(ROOT, "qa", "temp", "phase1_visual")
SAMPLES = os.path.join(QA_ROOT, "samples")

with open(TOKENS_PATH) as f:
    T = json.load(f)
UNIT = T["colors"]["unit"]
CH = T["colors"]["chapters"]

TEXT_AA = 4.5
NONTEXT_AA = 3.0


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(h):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = hex_to_rgb(h)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


def grayscale(h):
    r, g, b = hex_to_rgb(h)
    gv = round(0.299 * r + 0.587 * g + 0.114 * b)
    return f"#{gv:02x}{gv:02x}{gv:02x}"


results = []


def record(gate, ok, detail, warn=False):
    status = "PASS" if ok and not warn else ("WARN" if ok else "FAIL")
    results.append((gate, status, detail))


# --------------------------------------------------------------------------
# Gate 1: contrast
#   primary  vs white   >= 4.5  (primary as text on white; white text on band)
#   primary  vs surface >= 4.5  (primary text on light surface)
#   accent   vs white   >= 3.0  (non-text arrow/graphic)
#   accent   vs surface >= 3.0
#   neutral  vs surface >= 4.5  (secondary text on surface)
# --------------------------------------------------------------------------
contrast_issues = []
for key, th in CH.items():
    p = th["primary"]; a = th["accent"]; n = th["neutral"]; s = th["surface"]
    if contrast(p, "#FFFFFF") < TEXT_AA:
        contrast_issues.append(f"{key}.primary vs white = {contrast(p, '#FFFFFF')}")
    if contrast(p, s) < TEXT_AA:
        contrast_issues.append(f"{key}.primary vs surface = {contrast(p, s)}")
    if contrast(a, "#FFFFFF") < NONTEXT_AA:
        contrast_issues.append(f"{key}.accent vs white = {contrast(a, '#FFFFFF')}")
    if contrast(a, s) < NONTEXT_AA:
        contrast_issues.append(f"{key}.accent vs surface = {contrast(a, s)}")
    if contrast(n, s) < TEXT_AA:
        contrast_issues.append(f"{key}.neutral vs surface = {contrast(n, s)}")
ink_white = contrast(UNIT["ink"], "#FFFFFF")
ink_soft_white = contrast(UNIT["ink_soft"], "#FFFFFF")
if ink_white < TEXT_AA:
    contrast_issues.append(f"ink vs white = {ink_white}")
if ink_soft_white < TEXT_AA:
    contrast_issues.append(f"ink_soft vs white = {ink_soft_white}")

record("contrast", not contrast_issues,
       "all chapter colors meet role contrast floors"
       if not contrast_issues else "; ".join(contrast_issues[:8]))

# --------------------------------------------------------------------------
# Gate 2: grayscale survival
# --------------------------------------------------------------------------
gs_issues = []
for key, th in CH.items():
    for slot in ("primary", "accent"):
        g = grayscale(th[slot])
        c = contrast(g, "#FFFFFF")
        if c < NONTEXT_AA:
            gs_issues.append(f"{key}.{slot} grayscale {g} vs white = {c}")
    p_l = luminance(grayscale(th["primary"]))
    a_l = luminance(grayscale(th["accent"]))
    if p_l >= a_l:
        gs_issues.append(f"{key} primary grayscale not darker than accent")

record("grayscale", not gs_issues,
       "all primaries/accents survive B/W (>= 3:1, primary darker than accent)"
       if not gs_issues else "; ".join(gs_issues[:8]))

# --------------------------------------------------------------------------
# Gate 3: font floors
# --------------------------------------------------------------------------
font_issues = []
for name in ("sample-slide", "sample-notes", "sample-assessment", "sample-playbook"):
    sp = os.path.join(SAMPLES, f"{name}.svg")
    if not os.path.exists(sp):
        font_issues.append(f"{name} missing"); continue
    content = open(sp).read()
    pairs = re.findall(r'<text[^>]*font-size="([\d.]+)"[^>]*?(?:data-role="(\w+)")?[^>]*>', content)
    # pairs: (size, role-or-'')
    sizes = [float(m[0]) for m in pairs]
    if not sizes:
        font_issues.append(f"{name}: no text found"); continue
    if name == "sample-slide":
        content_sizes = [float(s) for s, r in pairs if r == "content"]
        below = [s for s in content_sizes if s < 28]
        if below:
            font_issues.append(f"slide content below 28pt: {sorted(set(below))}")
    else:
        body_sizes = [float(s) for s, r in pairs if r == "content"]
        below = [s for s in body_sizes if s < 12]
        if below:
            font_issues.append(f"{name} content below 12pt: {sorted(set(below))}")
        # absolute floor (captions/page refs allowed at 11)
        if min(sizes) < 11:
            font_issues.append(f"{name} below absolute 11pt floor: {min(sizes)}")

record("font_floors", not font_issues,
       "sample content respects font floors (slide 28 / handout body 12 / caption 11)"
       if not font_issues else "; ".join(font_issues))

# --------------------------------------------------------------------------
# Gate 4: margins / overflow
# --------------------------------------------------------------------------
overflow_issues = []
canvas = {"sample-slide": (1280, 720), "sample-notes": (612, 792),
          "sample-assessment": (612, 792), "sample-playbook": (612, 792)}
for name, (cw, chh) in canvas.items():
    sp = os.path.join(SAMPLES, f"{name}.svg")
    if not os.path.exists(sp):
        continue
    content = open(sp).read()
    for m in re.finditer(r'<rect x="([\d.-]+)" y="([\d.-]+)" width="([\d.-]+)" height="([\d.-]+)"', content):
        x, y, w, h = map(float, m.groups())
        if x < -0.5 or y < -0.5 or x + w > cw + 0.5 or y + h > chh + 0.5:
            overflow_issues.append(f"{name}: rect({x:.0f},{y:.0f},{w:.0f},{h:.0f})")
            break
    # margin check (handouts: content within 54pt side margins)
    if name != "sample-slide":
        for m in re.finditer(r'<rect x="([\d.-]+)"[^>]*width="([\d.-]+)"', content):
            x, w = float(m.group(1)), float(m.group(2))
            if x < 1:  # full-bleed decorative bar (intentional)
                continue
            if x < 48 or x + w > cw - 48:
                overflow_issues.append(f"{name}: rect breaches side margin x={x:.0f} w={w:.0f}")
                break

record("overflow", not overflow_issues,
       "no sample element exceeds canvas or side margins"
       if not overflow_issues else "; ".join(overflow_issues[:5]))

# --------------------------------------------------------------------------
# Gate 5: render integrity
# --------------------------------------------------------------------------
render_fail = []
svg_files = []
for dirpath, _, files in os.walk(ASSET_ROOT):
    for fn in files:
        if fn.endswith(".svg"):
            svg_files.append(os.path.join(dirpath, fn))
svg_files += [os.path.join(SAMPLES, f) for f in os.listdir(SAMPLES) if f.endswith(".svg")]

for sp in sorted(set(svg_files)):
    r = subprocess.run(["rsvg-convert", sp, "-o", "/tmp/qa_rsvg.png"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        render_fail.append(os.path.relpath(sp, ROOT))

record("render_integrity", not render_fail,
       f"{len(set(svg_files))} SVGs rasterize cleanly"
       if not render_fail else "; ".join(render_fail[:5]))

# --------------------------------------------------------------------------
# Gate 6: component consistency
# --------------------------------------------------------------------------
consistency = []
hud_dir = os.path.join(ASSET_ROOT, "hud")
hud_sizes = set()
for fn in os.listdir(hud_dir):
    if fn.endswith(".svg"):
        m = re.search(r'width="(\d+)" height="(\d+)"', open(os.path.join(hud_dir, fn)).read())
        if m:
            hud_sizes.add(m.groups())
if len(hud_sizes) != 1:
    consistency.append(f"HUD bubble sizes vary: {hud_sizes}")
n_hud = len([f for f in os.listdir(hud_dir) if f.endswith(".svg")])
expected_hud = len(T["hud_actions"]["normal"]) + len(T["hud_actions"]["optional"])
if n_hud != expected_hud:
    consistency.append(f"HUD count {n_hud} != {expected_hud}")
n_badges = len([f for f in os.listdir(os.path.join(ASSET_ROOT, "badges")) if f.endswith(".svg")])
if n_badges != len(T["resource_badges"]):
    consistency.append(f"badge count {n_badges} != {len(T['resource_badges'])}")
n_ch = len([f for f in os.listdir(os.path.join(ASSET_ROOT, "chapter-themes")) if "palette" in f])
if n_ch != 7:
    consistency.append(f"chapter palettes {n_ch} != 7")
for k in ("ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7"):
    for slot in ("primary", "accent", "neutral", "surface"):
        if not re.match(r"^#[0-9A-Fa-f]{6}$", CH[k][slot]):
            consistency.append(f"{k}.{slot} invalid hex: {CH[k][slot]}")

record("component_consistency", not consistency,
       "HUD/badge/palette counts + hex values consistent"
       if not consistency else "; ".join(consistency[:5]))

# --------------------------------------------------------------------------
# Gate 7: token validation (freeze version + component dims)
# --------------------------------------------------------------------------
token_issues = []
if T.get("design_system_version") != "1.0":
    token_issues.append(f"design_system_version={T.get('design_system_version')} != 1.0")
if T.get("status") != "FROZEN":
    token_issues.append(f"status={T.get('status')} != FROZEN")
comps = T.get("components", {})
for c in ("chapter_tab", "vocabulary_card", "hud_bubble", "resource_badge"):
    if c not in comps:
        token_issues.append(f"components.{c} missing"); continue
    for f in ("width_pt", "height_pt"):
        if not isinstance(comps[c].get(f), (int, float)):
            token_issues.append(f"components.{c}.{f} missing/invalid")
if "bq_panel" not in comps or not isinstance(comps["bq_panel"].get("height_pt"), (int, float)):
    token_issues.append("components.bq_panel.height_pt missing/invalid")

record("token_validation", not token_issues,
       "freeze version 1.0 + component dims present"
       if not token_issues else "; ".join(token_issues[:5]))

# --------------------------------------------------------------------------
# Gate 8: Figma parity (manifest snapshot == canonical tokens + local assets)
# --------------------------------------------------------------------------
parity_issues = []
MANIFEST_PATH = os.path.join(ASSET_ROOT, "figma-parity-manifest.json")
if not os.path.exists(MANIFEST_PATH):
    parity_issues.append("figma-parity-manifest.json missing")
else:
    M = json.load(open(MANIFEST_PATH))
    if M.get("design_system_version") != T.get("design_system_version"):
        parity_issues.append("manifest design_system_version drift")
    if M.get("colors", {}).get("unit") != UNIT:
        parity_issues.append("manifest unit colors != tokens")
    mch = M.get("colors", {}).get("chapters", {})
    for k in ("ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7"):
        for slot in ("primary", "accent", "neutral", "surface"):
            if mch.get(k, {}).get(slot) != CH[k][slot]:
                parity_issues.append(f"manifest {k}.{slot} drift")
    mcomps = M.get("components", {})
    for c in ("chapter_tab", "vocabulary_card", "hud_bubble", "resource_badge"):
        want = {k: T["components"][c][k] for k in ("width_pt", "height_pt")}
        if mcomps.get(c) != want:
            parity_issues.append(f"manifest {c} {mcomps.get(c)} != {want}")
    if mcomps.get("bq_panel", {}).get("height_pt") != T["components"]["bq_panel"]["height_pt"]:
        parity_issues.append(f"manifest bq_panel height drift")

    def svg_size(relpath):
        p = os.path.join(ASSET_ROOT, relpath)
        if not os.path.exists(p):
            return None
        m = re.search(r'width="([\d.]+)" height="([\d.]+)"', open(p).read())
        return (float(m.group(1)), float(m.group(2))) if m else None

    loc_checks = {
        "chapter-themes/chapter-tab.svg": ("chapter_tab", ("width_pt", "height_pt")),
        "vocabulary/vocabulary-card.svg": ("vocabulary_card", ("width_pt", "height_pt")),
    }
    for rel, (comp, fields) in loc_checks.items():
        want = tuple(T["components"][comp][f] for f in fields)
        if svg_size(rel) != want:
            parity_issues.append(f"{rel} {svg_size(rel)} != tokens {want}")

record("figma_parity", not parity_issues,
       "Figma manifest matches tokens + local assets"
       if not parity_issues else "; ".join(parity_issues[:5]))

# --------------------------------------------------------------------------
# Gate 9: grayscale proof artifact
# --------------------------------------------------------------------------
gs_proof = os.path.join(QA_ROOT, "grayscale_proof.png")
gs_proof_issues = []
if not os.path.exists(gs_proof):
    gs_proof_issues.append("grayscale_proof.png missing")
else:
    try:
        from PIL import Image
        import statistics
        im = Image.open(gs_proof).convert("RGB")
        w, h = im.size
        if w < 100 or h < 100:
            gs_proof_issues.append("grayscale proof too small")
        else:
            px = im.load()
            non_gray = 0
            checked = 0
            for y in range(0, h, max(1, h // 24)):
                for x in range(0, w, max(1, w // 24)):
                    r, g, b = px[x, y]
                    checked += 1
                    if not (abs(r - g) <= 2 and abs(g - b) <= 2):
                        non_gray += 1
            if non_gray > checked * 0.01:
                gs_proof_issues.append(f"{non_gray}/{checked} sampled pixels not grayscale")
            vals = [px[x, y][0] for y in range(0, h, 8) for x in range(0, w, 8)]
            if statistics.mean(vals) > 252:
                gs_proof_issues.append("grayscale proof appears blank")
    except Exception as e:
        gs_proof_issues.append(f"grayscale proof read error: {e}")

record("grayscale_proof", not gs_proof_issues,
       "grayscale proof present, non-blank, all-gray"
       if not gs_proof_issues else "; ".join(gs_proof_issues[:5]))

# --------------------------------------------------------------------------
# Aggregate + report
# --------------------------------------------------------------------------
fail = any(s == "FAIL" for _, s, _ in results)
warn = any(s == "WARN" for _, s, _ in results)
overall = "FAIL" if fail else ("WARN" if warn else "PASS")

report = {"overall": overall,
          "gates": [{"gate": g, "status": s, "detail": d} for g, s, d in results],
          "ink_vs_white": ink_white,
          "ink_soft_vs_white": ink_soft_white}
with open(os.path.join(QA_ROOT, "qa_report.json"), "w") as f:
    json.dump(report, f, indent=2)

print("=" * 64)
print("UNIT 1 VISUAL SYSTEM — AUTOMATED QA")
print("=" * 64)
for g, s, d in results:
    print(f"  [{s:4}] {g:<22} {d}")
print("-" * 64)
print(f"  OVERALL: {overall}")
print(f"  ink vs white = {ink_white} · ink_soft vs white = {ink_soft_white}")
print("=" * 64)
