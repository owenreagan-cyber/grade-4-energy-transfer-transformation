# Data Quality QA — Chapter 3

> Dedicated data-quality check (Phase 5 addition). Verifies trials, units, graph-vs-table consistency, averaging, axes, precision, and that no speed/energy number is invented.

## Repeated trials feasible?
- Ramp It Up! 2.0: 3 heights × 3 trials = 9 releases. At ~30 s/release + reset, ≈ 8–10 min of hands-on — feasible in a 15-min test window. ✅
- Drop It: 2–3 heights × 3 trials; sand re-smoothing is the reset bottleneck (~30 s each) — feasible in a 12-min window. ✅

## Measurement units consistent?
- Ramp: cup displacement in **cm** (all trials + average). ✅
- Ramp height in **books** (1/2/3). ✅
- Drop: drop height in **cm** (30/60/90); crater width in **cm**. ✅
- No mixed units (no "inches" or "mm" anywhere). ✅

## Graph matches data table?
- Table columns: Ramp Height | Trial 1 | Trial 2 | Trial 3 | Average Cup Displacement (cm). ✅
- Graph: X = Ramp Height (books), Y = Average Cup Displacement (cm). ✅
- Three categories (1/2/3 books) map to three bars/points; Y ticks 0–30 cm cover the sample range (6–22 cm). ✅

## Average calculation correct?
- Sample class data: 1 book → 6 cm, 2 books → 14 cm, 3 books → 22 cm. The ramp page guides students to compute the average from their own 3 trials; no pre-computed average is imposed on the student page. ✅
- Recovery page provides full class averages so absent students can graph without inventing numbers. ✅

## Axes match variables actually measured?
- X = ramp height (measured). Y = cup displacement (measured). ✅
- Graph title "Ramp Height vs. Average Cup Displacement" — never "Speed vs. Energy." ✅
- Drop It has no graph (crater width is the measured outcome; the explanation is qualitative+inferred). ✅

## No fake precision?
- Crater depth is qualitative only (shallow/medium/deep) — no millimeter depth. ✅
- No decimals forced; whole-cm measurement is expected. ✅

## No speed number invented?
- Students never record a speed value; "faster" is inferred from ramp/drop height. ✅
- No artifact labels speed with a number or unit. ✅

## No energy number invented?
- Students never record an energy value; energy of motion is inferred from the observed change. ✅

## Conclusions match evidence?
- Expected conclusion "higher ramp → farther cup → (inferred) faster → (inferred) greater energy of motion" is fully supported by the measured displacement pattern. ✅
- Recovery/sample data direction (6 → 14 → 22 cm) matches the science and the expected pattern. ✅

## Result: **PASS**
