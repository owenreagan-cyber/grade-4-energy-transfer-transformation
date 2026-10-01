"""Phase 13AC — Final classroom delivery package organizer.

Creates `production/final-delivery/` as a navigable teacher-facing structure using
RELATIVE SYMLINKS (no file duplication; single source of truth = canonical
production paths). Also generates:
  - RELEASE_HASH_MANIFEST.csv   (SHA-256 + size for backup integrity)
  - docs/reviews/GOOGLE_DRIVE_MIRROR_MANIFEST.md (Drive mirror metadata)

Method: relative symlinks (documented in final-delivery/README.md). No classroom
artifact is copied, modified, or regenerated. Run again any time to re-sync.

Usage: python tools/build_final_delivery.py
"""
import csv, hashlib, os, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DELIV = os.path.join(REPO, "production", "final-delivery")

# ---------------------------------------------------------------------------
# Delivery symlink map: (destination path relative to DELIV, source path relative to REPO)
# ---------------------------------------------------------------------------
# Shared cross-unit teacher docs (flat, descriptive names)
SHARED = [
    ("Shared/Printing Guide.md",                    "production/final-8.5-week/PRINTING_GUIDE.md"),
    ("Shared/Teacher Prep Guide.md",                "production/final-8.5-week/TEACHER_PREP_GUIDE.md"),
    ("Shared/Supply List.md",                       "production/final-8.5-week/MASTER_SUPPLY_LIST_20_STUDENTS.md"),
    ("Shared/Master Curriculum Map.md",             "production/final-8.5-week/MASTER_CURRICULUM_MAP.md"),
    ("Shared/Final Release Manifest.md",            "production/final-8.5-week/FINAL_RELEASE_MANIFEST.md"),
    ("Shared/Master Pacing.md",                     "production/final-8.5-week/ENERGY_AND_NATURAL_RESOURCES_MASTER_PACING.md"),
    ("Shared/Master Resource Index.md",             "production/final-8.5-week/MASTER_RESOURCE_INDEX.md"),
    ("Shared/Master Resource Inventory.md",         "production/final-8.5-week/MASTER_RESOURCE_INVENTORY.md"),
    ("Shared/Release Freeze.md",                    "production/final-8.5-week/RELEASE_FREEZE.md"),
    ("Shared/Video Integration Matrix.md",          "production/final-8.5-week/VIDEO_PRESENTATION_INTEGRATION_MATRIX.md"),
    ("Shared/Final Video Inventory.md",             "production/final-8.5-week/FINAL_VIDEO_INVENTORY.md"),
    ("Shared/Friday Flex Bank.md",                  "production/friday-flex/FRIDAY_FLEX_BANK.md"),
    ("Shared/Bundle Preview Index.md",              "production/final-8.5-week/BUNDLE_PREVIEW_INDEX.md"),
]

# Unit 1 (Energy)
U1_TEACHER = []
for c in range(1, 8):
    d = f"curriculum/chapter-{c:02d}/teacher"
    if not os.path.isdir(os.path.join(REPO, d)):
        continue
    for fn in sorted(os.listdir(os.path.join(REPO, d))):
        if fn.endswith(".md"):
            U1_TEACHER.append((f"Energy/Unit 1 Teacher Guide/{fn}", f"{d}/{fn}"))
U1_TEACHER += [
    ("Energy/Unit 1 Teacher Guide/WEEK1_2_QUICKSTART.md", "production/final-8.5-week/WEEK1_2_TEACHER_QUICKSTART.md"),
    ("Energy/Unit 1 Teacher Guide/WEEK3_4_QUICKSTART.md", "production/final-8.5-week/WEEK3_4_TEACHER_QUICKSTART.md"),
    ("Energy/Unit 1 Teacher Guide/UNIT1_ASSESSMENT_ADMINISTRATION_NOTE.md", "production/final-8.5-week/UNIT1_ASSESSMENT_ADMINISTRATION_NOTE.md"),
]

U1_SLIDES = [(f"Energy/Unit 1 Slide Decks/{fn}", f"production/slides/{fn}") for fn in [
    "01-ch1-energy-causes-change-slides.pptx",
    "02-ch2-moving-objects-have-energy-slides.pptx",
    "03-ch3-energy-speed-slides.pptx",
    "04-ch4-energy-transfer-slides.pptx",
    "05-ch5-collisions-slides.pptx",
    "06-ch6-energy-transformations-slides.pptx",
    "07-ch7-edison-unit-synthesis-slides.pptx",
]]

U1_NOTES = []
for ch in ["01-ch1-energy-causes-change", "02-ch2-moving-objects-have-energy",
           "03-ch3-energy-speed", "04-ch4-energy-transfer", "05-ch5-collisions-transfer-energy",
           "06-ch6-energy-transformations", "07-ch7-edison-unit-synthesis"]:
    for ext in ("docx", "pdf"):
        U1_NOTES.append((f"Energy/Unit 1 Guided Notes/{ch}-guided-notes.{ext}",
                         f"production/premium-notes/{ch}-guided-notes.{ext}"))

U1_STUDENT = [(f"Energy/Unit 1 Student Resources/{fn}", f"production/worksheets/{fn}") for fn in [
    "01-ch1-energy-causes-change-practice.docx",
    "02-ch2-moving-objects-have-energy-practice.docx",
    "03-ch3-energy-speed-practice.docx",
    "04-ch4-energy-transfer-practice.docx",
    "05-ch5-collisions-practice.docx",
    "06-ch6-energy-transformations-practice.docx",
    "07-energy-big-questions.docx",
    "07-unit-synthesis-review.docx",
]]

U1_LABS = []
for fn in ["01-ch1-energy-detectives-student.docx", "02-ch2-moving-marbles-student.docx",
           "03-ch3-ramp-it-up-student.docx", "03-ch3-drop-it-student.docx",
           "05-ch5-crash-lab-student.docx", "04-ch4-heat-transfer-student.docx",
           "04-ch4-light-transfer-student.docx", "04-ch4-sound-transfer-student.docx",
           "04-ch4-electricity-transfer-student.docx", "06-ch6-engineering-performance-task.docx"]:
    U1_LABS.append((f"Energy/Unit 1 Labs/{fn}", f"production/worksheets/{fn}"))
for fn in ["01-ch1-energy-detectives-teacher-spec.md", "02-ch2-moving-marbles-teacher-spec.md",
           "03-ch3-ramp-it-up-teacher-spec.md", "03-ch3-drop-it-teacher-spec.md",
           "05-ch5-crash-lab-teacher-spec.md", "04-ch4-heat-transfer-teacher-spec.md",
           "04-ch4-light-transfer-teacher-spec.md", "04-ch4-sound-transfer-teacher-spec.md",
           "04-ch4-electricity-transfer-teacher-spec.md", "06-ch6-engineering-capstone-teacher-spec.md"]:
    U1_LABS.append((f"Energy/Unit 1 Labs/{fn}", f"production/labs/{fn}"))
for fn in ["01-ch1-energy-detectives-key.md", "02-ch2-moving-marbles-key.md",
           "03-ch3-ramp-it-up-key.md", "03-ch3-drop-it-key.md", "05-ch5-crash-lab-key.md",
           "04-ch4-heat-transfer-key.md", "04-ch4-light-transfer-key.md",
           "04-ch4-sound-transfer-key.md", "04-ch4-electricity-transfer-key.md",
           "06-ch6-engineering-key.md", "06-ch6-engineering-teacher-key.md"]:
    U1_LABS.append((f"Energy/Unit 1 Labs/{fn}", f"production/answer-keys/{fn}"))
for fn in ["ramp-it-up-setup-guide.docx", "ramp-it-up-setup-guide.pdf",
           "crash-lab-setup-guide.docx", "crash-lab-setup-guide.pdf"]:
    U1_LABS.append((f"Energy/Unit 1 Labs/{fn}", f"production/lab-setup-guides/{fn}"))

U1_ASSESS = []
for fn in ["01-ch1-energy-causes-change-quiz.docx", "02-ch2-moving-objects-have-energy-quiz.docx",
           "03-ch3-energy-speed-quiz.docx", "04-ch4-energy-transfer-quiz.docx",
           "05-ch5-collisions-quiz.docx", "06-ch6-concept-checkpoint.docx",
           "07-unit-final-assessment.docx", "07-unit-final-assessment-key.docx"]:
    U1_ASSESS.append((f"Energy/Unit 1 Assessments/{fn}", f"production/quizzes/{fn}"))
U1_ASSESS.append(("Energy/Unit 1 Assessments/07-unit-final-assessment-scoring-guide.md",
                  "production/quizzes/07-unit-final-assessment-scoring-guide.md"))
for fn in ["01-ch1-energy-causes-change-quiz-key.md", "02-ch2-moving-objects-have-energy-quiz-key.md",
           "03-ch3-energy-speed-quiz-key.md", "04-ch4-energy-transfer-quiz-key.md",
           "05-ch5-collisions-quiz-key.md", "06-ch6-checkpoint-key.md",
           "07-unit-final-assessment-key.md"]:
    U1_ASSESS.append((f"Energy/Unit 1 Assessments/{fn}", f"production/answer-keys/{fn}"))

U1_REVIEW = [
    ("Energy/Unit 1 Review Game/unit1-review-game.pptx", "production/review/unit-01/unit1-review-game.pptx"),
    ("Energy/Unit 1 Review Game/unit1-review-game-guide.md", "production/review/unit-01/unit1-review-game-guide.md"),
    ("Energy/Unit 1 Review Game/unit1-review-game-scorecards.pdf", "production/review/unit-01/unit1-review-game-scorecards.pdf"),
    ("Energy/Unit 1 Review Game/unit1-review-game-scorecards.docx", "production/review/unit-01/unit1-review-game-scorecards.docx"),
    ("Energy/Unit 1 Review Game/unit1-review-game-cards.docx", "production/review/unit-01/unit1-review-game-cards.docx"),
]

U1_STUDYGUIDE = [
    ("Energy/Unit 1 Study Guide/unit1-study-guide.docx", "production/review/unit-01/unit1-study-guide.docx"),
    ("Energy/Unit 1 Study Guide/unit1-study-guide.pdf", "production/review/unit-01/unit1-study-guide.pdf"),
    ("Energy/Unit 1 Study Guide/unit1-study-guide-key.docx", "production/review/unit-01/unit1-study-guide-key.docx"),
    ("Energy/Unit 1 Study Guide/unit1-study-guide-key.pdf", "production/review/unit-01/unit1-study-guide-key.pdf"),
]

U1_INFOGRAPHICS = [(f"Energy/Infographics/{fn}", f"production/infographics/{fn}") for fn in [
    "unit1-energy-detective-anchor.png",
    "unit1-transfer-vs-transformation.png",
    "unit1-engineering-design-cycle.png",
    "unit1-collision-energy-transfer.png",
]]

# Unit 2 (Natural Resources)
U2_TEACHER = [
    ("Natural Resources/Unit 2 Teacher Guide/WEEK5_6_QUICKSTART.md", "production/final-8.5-week/WEEK5_6_TEACHER_QUICKSTART.md"),
    ("Natural Resources/Unit 2 Teacher Guide/WEEK7_8_5_QUICKSTART.md", "production/final-8.5-week/WEEK7_8_5_TEACHER_QUICKSTART.md"),
    ("Natural Resources/Unit 2 Teacher Guide/UNIT2_ABSENT_RECOVERY_INDEX.md", "production/final-8.5-week/UNIT2_ABSENT_RECOVERY_INDEX.md"),
]

U2_SLIDES = [(f"Natural Resources/Unit 2 Slide Decks/{fn}", f"production/slides/{fn}") for fn in [
    "01-u2-ch1-renewable-nonrenewable-slides.pptx",
    "02-u2-ch2-slides.pptx", "03-u2-ch3-slides.pptx", "04-u2-ch4-slides.pptx",
    "05-u2-ch5-slides.pptx", "06-u2-ch6-slides.pptx", "07-u2-ch7-slides.pptx",
    "08-u2-ch8-slides.pptx", "09-u2-ch9-slides.pptx",
]]

U2_NOTES = []
for ch in ["unit-02-ch1-renewable-nonrenewable", "unit-02-ch2-types-of-fossil-fuels",
           "unit-02-ch3-using-fossil-fuels", "unit-02-ch4-nuclear-energy",
           "unit-02-ch5-wind-energy", "unit-02-ch6-hydroelectric-energy",
           "unit-02-ch7-solar-energy", "unit-02-ch8-geothermal-energy",
           "unit-02-ch9-energy-resource-innovations"]:
    for ext in ("docx", "pdf"):
        U2_NOTES.append((f"Natural Resources/Unit 2 Guided Notes/{ch}-guided-notes.{ext}",
                         f"production/premium-notes/unit-02/{ch}-guided-notes.{ext}"))

U2_STUDENT = []
for fn in ["energy-resource-detective-chart.docx", "energy-resource-scenario-challenge.docx",
           "fast-and-curious.docx", "transfer-transformation-both-sort.docx",
           "solar-device-mini-investigation.docx", "chocolate-chip-mining-flex-model.docx",
           "energy-detective-certificate.docx"]:
    U2_STUDENT.append((f"Natural Resources/Unit 2 Student Resources/{fn}", f"production/activities/unit-02/{fn}"))
for fn in ["energy-resource-detective-chart.pdf", "energy-resource-scenario-challenge.pdf",
           "fast-and-curious.pdf", "transfer-transformation-both-sort.pdf",
           "solar-device-mini-investigation.pdf", "chocolate-chip-mining-flex-model.pdf",
           "energy-detective-certificate.pdf"]:
    U2_STUDENT.append((f"Natural Resources/Unit 2 Student Resources/{fn}", f"production/activities/unit-02/{fn}"))

U2_LABS = [
    ("Natural Resources/Unit 2 Labs/water-wheel-flagship-lab-student.docx", "production/labs/unit-02/water-wheel-flagship-lab-student.docx"),
    ("Natural Resources/Unit 2 Labs/water-wheel-flagship-lab-student.pdf", "production/labs/unit-02/water-wheel-flagship-lab-student.pdf"),
    ("Natural Resources/Unit 2 Labs/water-wheel-flagship-lab-teacher.docx", "production/labs/unit-02/water-wheel-flagship-lab-teacher.docx"),
    ("Natural Resources/Unit 2 Labs/water-wheel-flagship-lab-teacher.pdf", "production/labs/unit-02/water-wheel-flagship-lab-teacher.pdf"),
    ("Natural Resources/Unit 2 Labs/water-wheel-setup-guide.docx", "production/lab-setup-guides/water-wheel-setup-guide.docx"),
    ("Natural Resources/Unit 2 Labs/water-wheel-setup-guide.pdf", "production/lab-setup-guides/water-wheel-setup-guide.pdf"),
    ("Natural Resources/Unit 2 Labs/solar-device-setup-guide.docx", "production/lab-setup-guides/solar-device-setup-guide.docx"),
    ("Natural Resources/Unit 2 Labs/solar-device-setup-guide.pdf", "production/lab-setup-guides/solar-device-setup-guide.pdf"),
]

U2_ASSESS = [
    ("Natural Resources/Unit 2 Assessments/unit-2-written-assessment-student.docx", "production/quizzes/unit-02/unit-2-written-assessment-student.docx"),
    ("Natural Resources/Unit 2 Assessments/unit-2-written-assessment-student.pdf", "production/quizzes/unit-02/unit-2-written-assessment-student.pdf"),
    ("Natural Resources/Unit 2 Assessments/unit-2-written-assessment-key.docx", "production/quizzes/unit-02/unit-2-written-assessment-key.docx"),
    ("Natural Resources/Unit 2 Assessments/unit-2-written-assessment-key.pdf", "production/quizzes/unit-02/unit-2-written-assessment-key.pdf"),
]

U2_REVIEW = [
    ("Natural Resources/Unit 2 Review Game/unit2-review-game.pptx", "production/review/unit-02/unit2-review-game.pptx"),
    ("Natural Resources/Unit 2 Review Game/unit2-review-game-guide.md", "production/review/unit-02/unit2-review-game-guide.md"),
    ("Natural Resources/Unit 2 Review Game/unit2-review-game-scorecards.pdf", "production/review/unit-02/unit2-review-game-scorecards.pdf"),
    ("Natural Resources/Unit 2 Review Game/unit2-review-game-scorecards.docx", "production/review/unit-02/unit2-review-game-scorecards.docx"),
    ("Natural Resources/Unit 2 Review Game/unit2-review-game-cards.docx", "production/review/unit-02/unit2-review-game-cards.docx"),
]

U2_STUDYGUIDE = [
    ("Natural Resources/Unit 2 Study Guide/unit2-written-study-review.docx", "production/review/unit-02/unit2-written-study-review.docx"),
    ("Natural Resources/Unit 2 Study Guide/unit2-written-study-review.pdf", "production/review/unit-02/unit2-written-study-review.pdf"),
    ("Natural Resources/Unit 2 Study Guide/unit2-written-study-review-key.docx", "production/review/unit-02/unit2-written-study-review-key.docx"),
    ("Natural Resources/Unit 2 Study Guide/unit2-written-study-review-key.pdf", "production/review/unit-02/unit2-written-study-review-key.pdf"),
]

U2_INFOGRAPHICS = [(f"Natural Resources/Infographics/{fn}", f"production/infographics/{fn}") for fn in [
    "unit2-renewable-nonrenewable-resources.png",
    "unit2-turbine-generator-pathways.png",
]]

DELIVERY_MAP = (SHARED + U1_TEACHER + U1_SLIDES + U1_NOTES + U1_STUDENT + U1_LABS +
                U1_ASSESS + U1_REVIEW + U1_STUDYGUIDE + U1_INFOGRAPHICS +
                U2_TEACHER + U2_SLIDES + U2_NOTES + U2_STUDENT + U2_LABS +
                U2_ASSESS + U2_REVIEW + U2_STUDYGUIDE + U2_INFOGRAPHICS)

# ---------------------------------------------------------------------------
# Hash manifest entries: (source rel path, unit, category, status)
# Includes the 5 embedded classroom-cut MP4s (git-excluded but release media).
# ---------------------------------------------------------------------------
def _u1(fn, cat, status="ACTIVE"):
    return (fn, "UNIT 1", cat, status)

def _u2(fn, cat, status="ACTIVE"):
    return (fn, "UNIT 2", cat, status)

HASH_ENTRIES = []

# Unit 1
for fn in ["01-ch1-energy-causes-change-slides.pptx","02-ch2-moving-objects-have-energy-slides.pptx",
           "03-ch3-energy-speed-slides.pptx","04-ch4-energy-transfer-slides.pptx",
           "05-ch5-collisions-slides.pptx","06-ch6-energy-transformations-slides.pptx",
           "07-ch7-edison-unit-synthesis-slides.pptx"]:
    HASH_ENTRIES.append(_u1(f"production/slides/{fn}", "SLIDES"))
for ch in ["01-ch1-energy-causes-change","02-ch2-moving-objects-have-energy","03-ch3-energy-speed",
           "04-ch4-energy-transfer","05-ch5-collisions-transfer-energy","06-ch6-energy-transformations",
           "07-ch7-edison-unit-synthesis"]:
    for ext in ("docx","pdf"):
        HASH_ENTRIES.append(_u1(f"production/premium-notes/{ch}-guided-notes.{ext}", "GUIDED NOTES"))
for fn in ["unit1-energy-detective-anchor.png","unit1-transfer-vs-transformation.png",
           "unit1-engineering-design-cycle.png","unit1-collision-energy-transfer.png"]:
    HASH_ENTRIES.append(_u1(f"production/infographics/{fn}", "INFOGRAPHICS"))
for fn in ["01-ch1-energy-causes-change-practice.docx","02-ch2-moving-objects-have-energy-practice.docx",
           "03-ch3-energy-speed-practice.docx","04-ch4-energy-transfer-practice.docx",
           "05-ch5-collisions-practice.docx","06-ch6-energy-transformations-practice.docx",
           "07-energy-big-questions.docx","07-unit-synthesis-review.docx"]:
    HASH_ENTRIES.append(_u1(f"production/worksheets/{fn}", "STUDENT RESOURCES"))
for fn in ["01-ch1-energy-detectives-student.docx","02-ch2-moving-marbles-student.docx",
           "03-ch3-ramp-it-up-student.docx","03-ch3-drop-it-student.docx","05-ch5-crash-lab-student.docx",
           "04-ch4-heat-transfer-student.docx","04-ch4-light-transfer-student.docx",
           "04-ch4-sound-transfer-student.docx","04-ch4-electricity-transfer-student.docx",
           "06-ch6-engineering-performance-task.docx"]:
    HASH_ENTRIES.append(_u1(f"production/worksheets/{fn}", "LABS"))
for fn in ["ramp-it-up-setup-guide.docx","ramp-it-up-setup-guide.pdf",
           "crash-lab-setup-guide.docx","crash-lab-setup-guide.pdf"]:
    HASH_ENTRIES.append(_u1(f"production/lab-setup-guides/{fn}", "LABS", "TEACHER ONLY"))
for fn in ["01-ch1-energy-causes-change-quiz.docx","02-ch2-moving-objects-have-energy-quiz.docx",
           "03-ch3-energy-speed-quiz.docx","04-ch4-energy-transfer-quiz.docx","05-ch5-collisions-quiz.docx",
           "06-ch6-concept-checkpoint.docx","07-unit-final-assessment.docx"]:
    HASH_ENTRIES.append(_u1(f"production/quizzes/{fn}", "ASSESSMENTS"))
HASH_ENTRIES.append(_u1("production/quizzes/07-unit-final-assessment-key.docx", "ASSESSMENTS", "TEACHER ONLY"))
for fn in ["unit1-study-guide.docx","unit1-study-guide.pdf"]:
    HASH_ENTRIES.append(_u1(f"production/review/unit-01/{fn}", "STUDY GUIDE"))
for fn in ["unit1-study-guide-key.docx","unit1-study-guide-key.pdf"]:
    HASH_ENTRIES.append(_u1(f"production/review/unit-01/{fn}", "STUDY GUIDE", "TEACHER ONLY"))
HASH_ENTRIES.append(_u1("production/review/unit-01/unit1-review-game.pptx", "REVIEW GAME"))
HASH_ENTRIES.append(_u1("production/review/unit-01/unit1-review-game-scorecards.pdf", "REVIEW GAME"))
for fn in ["unit1-review-game-scorecards.docx","unit1-review-game-cards.docx"]:
    HASH_ENTRIES.append(_u1(f"production/review/unit-01/{fn}", "REVIEW GAME", "TEACHER ONLY"))
HASH_ENTRIES.append(_u1("assets/supplemental/media/chapter-03/speed-and-energy-ramp-it-up-classroom-cut.mp4", "MEDIA"))
HASH_ENTRIES.append(_u1("assets/supplemental/media/chapter-07/journey-of-energy-unit1-recap-classroom-cut.mp4", "MEDIA"))

# Unit 2
for fn in ["01-u2-ch1-renewable-nonrenewable-slides.pptx","02-u2-ch2-slides.pptx","03-u2-ch3-slides.pptx",
           "04-u2-ch4-slides.pptx","05-u2-ch5-slides.pptx","06-u2-ch6-slides.pptx","07-u2-ch7-slides.pptx",
           "08-u2-ch8-slides.pptx","09-u2-ch9-slides.pptx"]:
    HASH_ENTRIES.append(_u2(f"production/slides/{fn}", "SLIDES"))
for ch in ["unit-02-ch1-renewable-nonrenewable","unit-02-ch2-types-of-fossil-fuels",
           "unit-02-ch3-using-fossil-fuels","unit-02-ch4-nuclear-energy","unit-02-ch5-wind-energy",
           "unit-02-ch6-hydroelectric-energy","unit-02-ch7-solar-energy","unit-02-ch8-geothermal-energy",
           "unit-02-ch9-energy-resource-innovations"]:
    for ext in ("docx","pdf"):
        HASH_ENTRIES.append(_u2(f"production/premium-notes/unit-02/{ch}-guided-notes.{ext}", "GUIDED NOTES"))
for fn in ["unit2-renewable-nonrenewable-resources.png","unit2-turbine-generator-pathways.png"]:
    HASH_ENTRIES.append(_u2(f"production/infographics/{fn}", "INFOGRAPHICS"))
for fn in ["energy-resource-detective-chart.docx","energy-resource-scenario-challenge.docx",
           "fast-and-curious.docx","transfer-transformation-both-sort.docx",
           "solar-device-mini-investigation.docx","energy-detective-certificate.docx"]:
    HASH_ENTRIES.append(_u2(f"production/activities/unit-02/{fn}", "STUDENT RESOURCES"))
HASH_ENTRIES.append(_u2("production/activities/unit-02/chocolate-chip-mining-flex-model.docx", "STUDENT RESOURCES", "OPTIONAL"))
for fn in ["water-wheel-flagship-lab-student.docx","water-wheel-flagship-lab-student.pdf"]:
    HASH_ENTRIES.append(_u2(f"production/labs/unit-02/{fn}", "LABS"))
for fn in ["water-wheel-flagship-lab-teacher.docx","water-wheel-flagship-lab-teacher.pdf"]:
    HASH_ENTRIES.append(_u2(f"production/labs/unit-02/{fn}", "LABS", "TEACHER ONLY"))
for fn in ["water-wheel-setup-guide.docx","water-wheel-setup-guide.pdf",
           "solar-device-setup-guide.docx","solar-device-setup-guide.pdf"]:
    HASH_ENTRIES.append(_u2(f"production/lab-setup-guides/{fn}", "LABS", "TEACHER ONLY"))
for fn in ["unit-2-written-assessment-student.docx","unit-2-written-assessment-student.pdf"]:
    HASH_ENTRIES.append(_u2(f"production/quizzes/unit-02/{fn}", "ASSESSMENTS"))
for fn in ["unit-2-written-assessment-key.docx","unit-2-written-assessment-key.pdf"]:
    HASH_ENTRIES.append(_u2(f"production/quizzes/unit-02/{fn}", "ASSESSMENTS", "TEACHER ONLY"))
for fn in ["unit2-written-study-review.docx","unit2-written-study-review.pdf"]:
    HASH_ENTRIES.append(_u2(f"production/review/unit-02/{fn}", "STUDY GUIDE"))
for fn in ["unit2-written-study-review-key.docx","unit2-written-study-review-key.pdf"]:
    HASH_ENTRIES.append(_u2(f"production/review/unit-02/{fn}", "STUDY GUIDE", "TEACHER ONLY"))
HASH_ENTRIES.append(_u2("production/review/unit-02/unit2-review-game.pptx", "REVIEW GAME"))
HASH_ENTRIES.append(_u2("production/review/unit-02/unit2-review-game-scorecards.pdf", "REVIEW GAME"))
for fn in ["unit2-review-game-scorecards.docx","unit2-review-game-cards.docx"]:
    HASH_ENTRIES.append(_u2(f"production/review/unit-02/{fn}", "REVIEW GAME", "TEACHER ONLY"))
for fn in ["assets/supplemental/media/unit-02/chapter-02/fossil-fuel-formation-classroom-cut.mp4",
           "assets/supplemental/media/unit-02/chapter-03/turbine-generator-classroom-cut.mp4",
           "assets/supplemental/media/unit-02/chapter-05/wind-hydro-power-classroom-cut.mp4"]:
    HASH_ENTRIES.append(_u2(fn, "MEDIA"))

# ---------------------------------------------------------------------------
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def build_symlinks():
    made = broken = 0
    for dest_rel, src_rel in DELIVERY_MAP:
        dest = os.path.join(DELIV, dest_rel)
        src = os.path.join(REPO, src_rel)
        if not os.path.exists(src):
            print(f"[MISSING SRC] {src_rel}")
            broken += 1
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if os.path.islink(dest) or os.path.exists(dest):
            os.remove(dest)
        target = os.path.relpath(src, os.path.dirname(dest))
        os.symlink(target, dest)
        made += 1
    print(f"symlinks: {made} made, {broken} missing sources")

def build_hash_manifest():
    rows = []
    for src_rel, unit, cat, status in HASH_ENTRIES:
        p = os.path.join(REPO, src_rel)
        if not os.path.exists(p):
            print(f"[MISSING HASH SRC] {src_rel}")
            continue
        size = os.path.getsize(p)
        rows.append([os.path.basename(src_rel), unit, cat, src_rel, sha256(p), str(size), status])
    out = os.path.join(DELIV, "RELEASE_HASH_MANIFEST.csv")
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["FILE", "UNIT", "CATEGORY", "LOCAL PATH", "SHA-256", "SIZE", "STATUS"])
        for r in rows:
            w.writerow(r)
    print(f"hash manifest: {len(rows)} rows -> {out}")
    return rows

def build_mirror_manifest(rows):
    by_unit = {"UNIT 1": [], "UNIT 2": []}
    for r in rows:
        by_unit[r[1]].append(r)
    lines = []
    lines.append("# GOOGLE DRIVE MIRROR MANIFEST")
    lines.append("")
    lines.append("> **SOURCE OF TRUTH:** Local frozen release repository (`production/`, git-tracked).")
    lines.append("> **Backup destination:** Google Drive → `My Drive → 2026-2027 → Science`.")
    lines.append("> Metadata only — do not upload unless approved Drive tooling is available.")
    lines.append("")
    for unit, folder in (("UNIT 1", "Energy"), ("UNIT 2", "Natural Resources")):
        lines.append(f"## Folder: {folder}")
        lines.append("")
        lines.append("| File | Category | Local Path | SHA-256 | Size | Status |")
        lines.append("|---|---|---|---|---|---|")
        for r in sorted(by_unit[unit], key=lambda x: (x[2], x[0])):
            lines.append(f"| `{r[0]}` | {r[2]} | `{r[3]}` | `{r[4][:16]}…` | {r[5]} | {r[6]} |")
        lines.append("")
    lines.append("## Sync Notes")
    lines.append("")
    lines.append("- Drive tree: `My Drive → 2026-2027 → Science → Energy` (Unit 1) and `… → Natural Resources` (Unit 2).")
    lines.append("- `TEACHER ONLY` items live in a parallel teacher-only folder; do not share them with students.")
    lines.append("- Embedded classroom-cut MP4s are git-excluded (`assets/supplemental/media/`) but are listed here for backup integrity.")
    lines.append("- Verify integrity with `shasum -a 256 -c` against `RELEASE_HASH_MANIFEST.csv`.")
    out = os.path.join(REPO, "docs", "reviews", "GOOGLE_DRIVE_MIRROR_MANIFEST.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"mirror manifest -> {out}")

def verify_links():
    bad = 0
    for dirpath, dirs, files in os.walk(DELIV):
        for fn in files:
            p = os.path.join(dirpath, fn)
            if os.path.islink(p) and not os.path.exists(p):
                print(f"[BROKEN LINK] {p}")
                bad += 1
    print(f"verify: {bad} broken links")
    return bad

if __name__ == "__main__":
    build_symlinks()
    rows = build_hash_manifest()
    build_mirror_manifest(rows)
    verify_links()
    print("DONE")
