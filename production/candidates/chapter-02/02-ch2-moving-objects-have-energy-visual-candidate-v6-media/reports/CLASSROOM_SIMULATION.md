# Classroom Simulation (v6-media)

Pacing authority: `tools/ch2_pacing.py` (single authoritative Chapter 2 timing system).

## Schedule (Week 1)
- **Wednesday 10/14 — Session 1 (Motion and Cause):** slides 1–16, 24.0 required min, 6.0 min buffer.
- **Thursday 10/15 — Session 2 (Energy of Motion, Use, Quiz):** slide 2 re-entry + 17–27, 12.0 required min, plus 12.0 min protected quiz = 24.0 min, 6.0 min buffer.
- Friday 10/16 is Chapter 1 Session 3 (quiz) — Chapter 2 puts no new content or quiz there.

## Video impact on pacing
- VIDEO A (slide 6) and VIDEO B (slide 15) are both **OPTIONAL** slides (required=false
  in the alignment contract). They sit inside the 6-minute buffer; neither consumes a
  required teaching minute. Speaker notes state the live marble demonstration is the
  default and the video is a replay.
- The 40 s clips fit comfortably in the buffer; they do not displace any writing,
  explanation, or the Thursday quiz.
- Every session remains fully teachable without video (the "live demo is default /
  continue if video unavailable" fallback is on slide 6).

## Internal consistency
`tools/ch2_pacing.py check_plan()` reports no problems (verified structure: both
sessions ≤ 25 required min, Thursday quiz handout at minute 12, no Friday content).
