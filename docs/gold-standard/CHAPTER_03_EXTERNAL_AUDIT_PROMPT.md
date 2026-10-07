# Chapter 3 External Audit Prompt

The external reviewer is the final independent red team. The reviewer is not the primary QA system. Internal certification and the Release Judge come first.

```
cd /Users/owen/Projects/grade-4-energy-transfer-transformation

CHAPTER 3 EXTERNAL AUDIT — FINAL INDEPENDENT RED TEAM

You are read-only on canonical classroom files unless the owner opens a
remediation pass. Do not rebuild the Chapter Factory. Do not start a new
chapter. Do not assign PASS to a gate. The Release Judge already ran;
you test whether that result holds.

Read the Reader and Teacher Guide yourself:
assets/authoritative/student-reader/chapters/Chapter_3_Energy_and_Speed_Are_Related.pdf
assets/authoritative/teacher-guide/Science 4 - Energy Transfer - TG .pdf
Lesson 4 begins on printed p. 33. Lesson 5 begins on printed p. 39.
Big Question: How are energy and speed related?

Test:
- source correctness against those files
- curriculum completeness and the same-object speed comparison
- no mass confound and no required kinetic, potential, or mechanical energy
- notes and slides alignment, including exact anchors
- rendered pixels, print usability, and writing space
- answer leakage
- assessment alignment and the TG boundary: students are not required to
  measure speed or energy quantitatively
- schedule and Friday policy: Friday is not first exposure to required content
- Ramp It Up 2.0: same ball, measured centimeter height, measured centimeter
  displacement, no fake m/s, no claim that height is speed
- release parity
- status and version authority
- QA of the QA evidence
- fresh held-out mutations you invent, not the project suite
- provenance and whether the release set matches the certified bytes
- whether the Release Judge evidence belongs to this build and is not stale

A factory defect is a defect in the shared gates, producers, hooks, or
Judge. Report it as a factory defect. Do not treat a one-line Chapter 3
wording fix as a repair of the factory.

End with exactly one outcome:

APPROVE PROPAGATION
APPROVE WITH FIXES
DO NOT PROPAGATE YET

APPROVE PROPAGATION means no blocking defect remains.
APPROVE WITH FIXES means the science and structure hold and the listed
fixes are narrow.
DO NOT PROPAGATE YET means a blocking science, leakage, identity, or
factory defect is still open.
```
