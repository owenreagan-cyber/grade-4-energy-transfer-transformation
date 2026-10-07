"""Registered evidence producers. A mandatory gate cannot be sealed by an unknown caller."""

from __future__ import annotations

# id is the provenance stamp written into toolVersions["producer"].
PRODUCERS = {
    "SOURCE_AUTHORITY": {
        "id": "chapter_qa.source_audit:emit_source_evidence",
        "version": "1.0",
        "role": "SOURCE_SCHOLAR",
    },
    "CURRICULUM_CORRECTNESS": {
        "id": "chapter_qa.source_audit:emit_source_evidence",
        "version": "1.0",
        "role": "CURRICULUM_AUDITOR",
    },
    "CHAPTER_SPEC": {
        "id": "chapter_qa.mandatory_producers:emit_chapter_spec",
        "version": "1.0",
        "role": "CURRICULUM_AUDITOR",
    },
    "NOTES_STRUCTURE": {
        "id": "chapter_qa.mandatory_producers:emit_notes_structure",
        "version": "1.0",
        "role": "CROSS_ARTIFACT_AUDITOR",
    },
    "SLIDES_STRUCTURE": {
        "id": "chapter_qa.mandatory_producers:emit_slides_structure",
        "version": "1.0",
        "role": "CROSS_ARTIFACT_AUDITOR",
    },
    "NOTES_SLIDES_SYNC": {
        "id": "chapter_qa.cross_artifact:emit_cross_evidence",
        "version": "1.0",
        "role": "CROSS_ARTIFACT_AUDITOR",
    },
    "ANSWER_LEAKAGE": {
        "id": "chapter_qa.mandatory_producers:emit_answer_leakage",
        "version": "1.0",
        "role": "CURRICULUM_AUDITOR",
    },
    "ASSESSMENT_ALIGNMENT": {
        "id": "chapter_qa.cross_artifact:emit_cross_evidence",
        "version": "1.0",
        "role": "CURRICULUM_AUDITOR",
    },
    "SCHEDULE_POLICY": {
        "id": "chapter_qa.schedule_policy:emit_schedule_evidence",
        "version": "1.0",
        "role": "CURRICULUM_AUDITOR",
    },
    "PLAYBOOK_ALIGNMENT": {
        "id": "chapter_qa.cross_artifact:emit_cross_evidence",
        "version": "1.0",
        "role": "CROSS_ARTIFACT_AUDITOR",
    },
    "RENDER_COMPLETENESS": {
        "id": "chapter_qa.render_completeness:emit_render_evidence",
        "version": "1.0",
        "role": "VISUAL_QA_AUDITOR",
    },
    "RENDERED_VISUAL_QA": {
        "id": "chapter_qa.visual_qa:emit_visual_evidence",
        "version": "1.0",
        "role": "VISUAL_QA_AUDITOR",
    },
    "PDF_QUALITY": {
        "id": "qa_pdf_quality:emit_pdf_evidence",
        "version": "1.0",
        "role": "PDF_OOXML_FORENSICS",
    },
    "FRESH_EXPORT": {
        "id": "chapter_qa.mandatory_producers:emit_fresh_export",
        "version": "1.0",
        "role": "PDF_OOXML_FORENSICS",
    },
    "RETIRED_CONTENT": {
        "id": "chapter_qa.mandatory_producers:emit_retired_content",
        "version": "1.0",
        "role": "PROVENANCE_AUDITOR",
    },
    "INVENTORY": {
        "id": "chapter_qa.mandatory_producers:emit_inventory",
        "version": "1.0",
        "role": "CROSS_ARTIFACT_AUDITOR",
    },
    "RELEASE_EXACT_SET": {
        "id": "chapter_qa.release_set:emit_release_evidence",
        "version": "1.0",
        "role": "PROVENANCE_AUDITOR",
    },
    "RELEASE_PARITY": {
        "id": "chapter_qa.release_set:emit_release_evidence",
        "version": "1.0",
        "role": "PROVENANCE_AUDITOR",
    },
    "STATUS_AUTHORITY": {
        "id": "qa_status_authority:emit_status_evidence",
        "version": "1.0",
        "role": "CROSS_ARTIFACT_AUDITOR",
    },
    "ADVERSARIAL_QA": {
        "id": "chapter_qa.mandatory_producers:emit_adversarial_qa",
        "version": "1.0",
        "role": "QA_ADVERSARY",
    },
    "PRIOR_FROZEN_NONREGRESSION": {
        "id": "chapter_qa.mandatory_producers:emit_prior_frozen",
        "version": "1.0",
        "role": "PROVENANCE_AUDITOR",
    },
}


def expected_producer(gate_id: str) -> dict | None:
    return PRODUCERS.get(gate_id)


def stamp(data: dict, gate_id: str) -> dict:
    spec = PRODUCERS[gate_id]
    versions = dict(data.get("toolVersions") or {})
    versions["producer"] = spec["id"]
    versions["producerVersion"] = spec["version"]
    data["toolVersions"] = versions
    return data
