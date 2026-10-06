"""Machine-readable adversarial cases. Attack prose is not stored here."""

from __future__ import annotations

import json
from pathlib import Path

# caseId, family, method, gate, expected, held-out eligible
_ROWS = [
    ("T01", "text", "append_unsupported", "CURRICULUM_CORRECTNESS", "FAIL"),
    ("T02", "text", "remove_sentence", "POST_FREEZE_GOLDEN", "FAIL"),
    ("T03", "text", "change_definition", "CURRICULUM_CORRECTNESS", "FAIL"),
    ("T04", "text", "out_of_scope", "SOURCE_AUTHORITY", "FAIL"),
    ("T05", "text", "teacher_guidance", "CURRICULUM_CORRECTNESS", "FAIL"),
    ("T06", "text", "harmless_region", "SOURCE_AUTHORITY", "FAIL"),
    ("C-TEXT", "text", "curriculum_exact", "SOURCE_AUTHORITY", "PASS"),
    ("S01", "anchors", "anchor_extra", "NOTES_SLIDES_SYNC", "FAIL"),
    ("S02", "anchors", "slide_extra", "NOTES_SLIDES_SYNC", "FAIL"),
    ("S03", "anchors", "remove_blank", "NOTES_SLIDES_SYNC", "FAIL"),
    ("S04", "anchors", "reorder", "NOTES_SLIDES_SYNC", "FAIL"),
    ("S05", "anchors", "anchor_code", "NOTES_SLIDES_SYNC", "FAIL"),
    ("S06", "anchors", "speaker_line", "NOTES_SLIDES_SYNC", "FAIL"),
    ("C-ANCHOR", "anchors", "anchor_clean", "NOTES_SLIDES_SYNC", "PASS"),
    ("L01", "leakage", "early_answer", "NOTES_SLIDES_SYNC", "FAIL"),
    ("L02", "leakage", "prefill", "ASSESSMENT_ALIGNMENT", "FAIL"),
    ("L03", "leakage", "speaker_early", "NOTES_SLIDES_SYNC", "FAIL"),
    ("L04", "leakage", "key_split", "ASSESSMENT_ALIGNMENT", "FAIL"),
    ("C-LEAK", "leakage", "assessment_clean", "ASSESSMENT_ALIGNMENT", "PASS"),
    ("ST01", "status", "unknown_token", "SCHEDULE_POLICY", "FAIL"),
    ("ST02", "status", "stale_words", "STATUS_AUTHORITY", "FAIL"),
    ("ST03", "status", "frozen_vs_human", "STATUS_AUTHORITY", "FAIL"),
    ("C-STATUS", "status", "status_clean", "STATUS_AUTHORITY", "PASS"),
    ("SC01", "schedule", "friday_required", "SCHEDULE_POLICY", "FAIL"),
    ("SC02", "schedule", "friday_date", "SCHEDULE_POLICY", "FAIL"),
    ("SC03", "schedule", "friday_table", "SCHEDULE_POLICY", "FAIL"),
    ("SC04", "schedule", "friday_clean", "SCHEDULE_POLICY", "PASS"),
    ("A01", "assessment", "quiz_answer", "ASSESSMENT_ALIGNMENT", "FAIL"),
    ("A02", "assessment", "bad_question", "ASSESSMENT_ALIGNMENT", "FAIL"),
    ("A03", "assessment", "drop_score", "ASSESSMENT_ALIGNMENT", "FAIL"),
    ("A04", "assessment", "key_disagree", "ASSESSMENT_ALIGNMENT", "FAIL"),
    ("A05", "assessment", "untaught", "CURRICULUM_CORRECTNESS", "FAIL"),
    ("C-ASSESS", "assessment", "assessment_clean", "ASSESSMENT_ALIGNMENT", "PASS"),
    ("R01", "render", "render_delete", "RENDER_COMPLETENESS", "FAIL"),
    ("R02", "render", "render_dup", "RENDER_COMPLETENESS", "FAIL"),
    ("R03", "render", "render_sub", "RENDER_COMPLETENESS", "FAIL"),
    ("R04", "render", "crop_off", "RENDERED_VISUAL_QA", "FAIL"),
    ("R05", "render", "overlap", "RENDERED_VISUAL_QA", "FAIL"),
    ("R06", "render", "tiny_font", "RENDERED_VISUAL_QA", "FAIL"),
    ("R07", "render", "small_write", "RENDERED_VISUAL_QA", "FAIL"),
    ("R08", "render", "missing_crop", "RENDERED_VISUAL_QA", "FAIL"),
    ("C-RENDER", "render", "render_clean", "RENDER_COMPLETENESS", "PASS"),
    ("C-VISUAL", "render", "visual_clean", "RENDERED_VISUAL_QA", "PASS"),
    ("P01", "pdf", "pdf_corrupt", "PDF_QUALITY", "FAIL"),
    ("P02", "pdf", "pdf_size", "PDF_QUALITY", "FAIL"),
    ("P03", "pdf", "pdf_low", "PDF_QUALITY", "FAIL"),
    ("P04", "pdf", "pdf_keyswap", "PDF_QUALITY", "FAIL"),
    ("P05", "pdf", "pdf_stale", "PDF_QUALITY", "FAIL"),
    ("P06", "pdf", "pdf_image_only", "PDF_QUALITY", "FAIL"),
    ("C-PDF", "pdf", "pdf_clean", "PDF_QUALITY", "PASS"),
    ("O01", "ooxml", "ooxml_rel", "OOXML_FORENSICS", "FAIL"),
    ("O02", "ooxml", "ooxml_target", "OOXML_FORENSICS", "FAIL"),
    ("O03", "ooxml", "ooxml_hidden", "OOXML_FORENSICS", "FAIL"),
    ("O04", "ooxml", "ooxml_xml", "OOXML_FORENSICS", "FAIL"),
    ("O05", "ooxml", "ooxml_notes", "OOXML_FORENSICS", "FAIL"),
    ("O06", "ooxml", "ooxml_external", "OOXML_FORENSICS", "FAIL"),
    ("C-OOXML", "ooxml", "ooxml_clean", "OOXML_FORENSICS", "PASS"),
    ("REL01", "release", "rel_delete", "RELEASE_EXACT_SET", "FAIL"),
    ("REL02", "release", "rel_extra", "RELEASE_EXACT_SET", "FAIL"),
    ("REL03", "release", "rel_retired", "RETIRED_CONTENT", "FAIL"),
    ("REL04", "release", "rel_manifest", "RELEASE_PARITY", "FAIL"),
    ("REL05", "release", "rel_artifact", "RELEASE_PARITY", "FAIL"),
    ("REL06", "release", "rel_launder", "RELEASE_PARITY", "FAIL"),
    ("REL07", "release", "rel_status", "STATUS_AUTHORITY", "FAIL"),
    ("C-RELEASE", "release", "rel_clean", "RELEASE_EXACT_SET", "PASS"),
    ("RET01", "retired", "ret_reinsert", "RETIRED_CONTENT", "FAIL"),
    ("RET02", "retired", "ret_rename", "RETIRED_CONTENT", "FAIL"),
    ("RET03", "retired", "ret_raster", "RETIRED_CONTENT", "FAIL"),
    ("RET04", "retired", "ret_embed", "RETIRED_CONTENT", "FAIL"),
    ("B01", "baseline", "launder_golden", "POST_FREEZE_GOLDEN", "FAIL"),
    ("B02", "baseline", "launder_hash", "POST_FREEZE_GOLDEN", "FAIL"),
    ("B03", "baseline", "repin_baseline", "POST_FREEZE_GOLDEN", "FAIL"),
    ("B04", "baseline", "build_swap", "RELEASE_JUDGE", "FAIL"),
    ("B05", "baseline", "stale_record", "RELEASE_JUDGE", "FAIL"),
    ("B06", "baseline", "inventory_rewrite", "RENDER_COMPLETENESS", "FAIL"),
    ("H01", "test-harness", "harness_import", "ADVERSARIAL_QA", "FAIL"),
    ("H02", "test-harness", "harness_skip", "ADVERSARIAL_QA", "FAIL"),
    ("H03", "test-harness", "harness_empty", "RENDER_COMPLETENESS", "FAIL"),
    ("H04", "test-harness", "harness_silent", "ADVERSARIAL_QA", "FAIL"),
    ("H05", "test-harness", "harness_name", "CURRICULUM_CORRECTNESS", "FAIL"),
    ("H06", "test-harness", "harness_truncate", "ADVERSARIAL_QA", "FAIL"),
    ("H07", "test-harness", "harness_severity", "ADVERSARIAL_QA", "FAIL"),
    ("H08", "test-harness", "harness_status", "ADVERSARIAL_QA", "FAIL"),
    ("C-HARNESS", "test-harness", "harness_clean", "ADVERSARIAL_QA", "PASS"),
    ("D01", "provenance", "dep_import", "CLEAN_ROOM_REPRODUCTION", "FAIL"),
    ("D02", "provenance", "dep_template", "CLEAN_ROOM_REPRODUCTION", "FAIL"),
    ("D03", "provenance", "dep_asset", "CLEAN_ROOM_REPRODUCTION", "FAIL"),
    ("D04", "provenance", "dep_config", "CLEAN_ROOM_REPRODUCTION", "FAIL"),
    ("D05", "provenance", "dep_source", "CLEAN_ROOM_REPRODUCTION", "FAIL"),
    ("D06", "provenance", "dep_runtime", "PROVENANCE_INTEGRITY", "FAIL"),
    ("C-CLOSURE", "provenance", "closure_clean", "SOURCE_CLOSURE", "PASS"),
    ("C-CLEANROOM", "provenance", "clean_room_ok", "CLEAN_ROOM_REPRODUCTION", "PASS"),
    ("E01", "environment", "env_missing_tool", "CLEAN_ROOM_REPRODUCTION", "FAIL"),
    ("E02", "environment", "env_version", "PROVENANCE_INTEGRITY", "FAIL"),
    ("E03", "environment", "env_absent", "PROVENANCE_INTEGRITY", "FAIL"),
    ("E04", "environment", "env_undeclared", "PROVENANCE_INTEGRITY", "FAIL"),
    ("E05", "environment", "env_locale", "PROVENANCE_INTEGRITY", "NOT_APPLICABLE"),
    ("RJ01", "release-judge", "judge_missing", "RELEASE_JUDGE", "FAIL"),
    ("RJ02", "release-judge", "build_swap", "RELEASE_JUDGE", "FAIL"),
    ("RJ03", "release-judge", "stale_record", "RELEASE_JUDGE", "FAIL"),
    ("RJ04", "release-judge", "judge_builder", "RELEASE_JUDGE", "FAIL"),
    ("RJ05", "release-judge", "judge_not_verified", "RELEASE_JUDGE", "FAIL"),
    ("RJ06", "release-judge", "judge_version", "RELEASE_JUDGE", "FAIL"),
    ("RJ07", "release-judge", "judge_blocking", "RELEASE_JUDGE", "FAIL"),
    ("RJ08", "release-judge", "judge_hash", "RELEASE_JUDGE", "FAIL"),
    ("C-JUDGE", "release-judge", "judge_clean", "RELEASE_JUDGE", "PASS"),
]


def cases():
    rows = []
    for case_id, family, method, gate, expected in _ROWS:
        rows.append({
            "caseId": case_id,
            "family": family,
            "description": "%s via %s" % (case_id, method),
            "historicalOrigin": "phase-c-catalog",
            "targetGate": gate,
            "expectedStatus": expected,
            "mutationMethod": method,
            "requiredInputs": ["seed"],
            "cleanControl": expected == "PASS",
            "safety": "workspace-only",
            "heldOutEligible": expected == "FAIL" and not case_id.startswith("RJ"),
            "notes": "Attack text is generated from the seed at runtime.",
            "implemented": "NOT_APPLICABLE" if expected == "NOT_APPLICABLE" else "IMPLEMENTED",
        })
    return rows


def write_case_files(root: Path) -> None:
    by_family = {}
    for row in cases():
        by_family.setdefault(row["family"], []).append(row)
    for family, rows in by_family.items():
        folder = root / family
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "cases.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


def matrix_markdown(results: list[dict]) -> str:
    lines = [
        "# Adversarial matrix",
        "",
        "| caseId | family | historicalOrigin | targetGate | implemented | projectRegression | heldOutEligible | expectedOutcome | actualOutcome | cleanControl | status |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    by_id = {row["caseId"]: row for row in cases()}
    for result in results:
        case = by_id.get(result["caseId"], {})
        expected = result["expectedStatus"]
        actual = result.get("actualStatus")
        if expected == "NOT_APPLICABLE":
            status = "NOT_APPLICABLE"
        elif expected == "FAIL" and result.get("caught"):
            status = "CAUGHT"
        elif expected == "PASS" and result.get("caught"):
            status = "CLEAN_PASS"
        else:
            status = "ESCAPE" if expected == "FAIL" else "CLEAN_RED"
        lines.append("| %s | %s | %s | %s | %s | yes | %s | %s | %s | %s | %s |" % (
            result["caseId"], result["family"], case.get("historicalOrigin", ""),
            result["expectedGate"], case.get("implemented", "IMPLEMENTED"),
            "yes" if case.get("heldOutEligible") else "no",
            expected, actual, "yes" if case.get("cleanControl") else "no", status,
        ))
    return "\n".join(lines) + "\n"
