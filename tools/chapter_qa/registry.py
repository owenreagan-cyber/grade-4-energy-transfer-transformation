"""Registered evidence producers. A mandatory gate cannot be sealed by an unknown caller."""

from __future__ import annotations

# id is the provenance stamp written into toolVersions["producer"].
PRODUCERS = {
    "SOURCE_AUTHORITY": {
        "id": "chapter_qa.file_producers:emit_source_authority_from_files",
        "version": "1.0",
        "role": "SOURCE_SCHOLAR",
    },
    "CURRICULUM_CORRECTNESS": {
        "id": "chapter_qa.file_producers:emit_curriculum_correctness_from_files",
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
        "id": "chapter_qa.file_producers:emit_notes_slides_sync_from_files",
        "version": "1.0",
        "role": "CROSS_ARTIFACT_AUDITOR",
    },
    "ANSWER_LEAKAGE": {
        "id": "chapter_qa.file_producers:emit_answer_leakage_from_files",
        "version": "1.0",
        "role": "CURRICULUM_AUDITOR",
    },
    "ASSESSMENT_ALIGNMENT": {
        "id": "chapter_qa.file_producers:emit_assessment_alignment_from_files",
        "version": "1.0",
        "role": "CURRICULUM_AUDITOR",
    },
    "SCHEDULE_POLICY": {
        "id": "chapter_qa.schedule_policy:emit_schedule_evidence_from_file",
        "version": "1.0",
        "role": "CURRICULUM_AUDITOR",
    },
    "PLAYBOOK_ALIGNMENT": {
        "id": "chapter_qa.file_producers:emit_playbook_alignment_from_files",
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
        "id": "chapter_qa.file_producers:emit_fresh_export_from_files",
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
        "id": "qa_status_authority:emit_status_evidence_from_files",
        "version": "1.0",
        "role": "CROSS_ARTIFACT_AUDITOR",
    },
    "ADVERSARIAL_QA": {
        "id": "chapter_qa.mandatory_producers:emit_adversarial_qa_from_file",
        "version": "1.0",
        "role": "QA_ADVERSARY",
    },
    "PRIOR_FROZEN_NONREGRESSION": {
        "id": "chapter_qa.mandatory_producers:emit_prior_frozen_from_tools",
        "version": "1.0",
        "role": "PROVENANCE_AUDITOR",
    },
    "STUDENT_PROMPT_CLARITY": {
        "id": "chapter_qa.student_prompt:emit_student_prompt_evidence",
        "version": "1.0",
        "role": "CURRICULUM_AUDITOR",
    },
    "LAB_STRUCTURE": {
        "id": "chapter_qa.file_producers:emit_lab_structure_from_files",
        "version": "1.0",
        "role": "CURRICULUM_AUDITOR",
    },
}


def expected_producer(gate_id: str) -> dict | None:
    return PRODUCERS.get(gate_id)


# F-3 producer-independence metadata. `observesFilesDirectly` is True only when
# the registered producer opens the actual artifact bytes and derives its own
# observation. Caller may still supply policy/config/expected, never the result.
PRODUCER_INDEPENDENCE = {
    "SOURCE_AUTHORITY": {"observesFilesDirectly": True, "method": "open Reader/TG/spec bytes"},
    "CURRICULUM_CORRECTNESS": {"observesFilesDirectly": True, "method": "open classroom files + boundary families"},
    "CHAPTER_SPEC": {"observesFilesDirectly": True, "method": "open chapter-spec JSON"},
    "STUDENT_PROMPT_CLARITY": {"observesFilesDirectly": True, "method": "open student files + extract prompts"},
    "NOTES_STRUCTURE": {"observesFilesDirectly": True, "method": "open notes docx/pdf + derive anchors/blanks"},
    "SLIDES_STRUCTURE": {"observesFilesDirectly": True, "method": "open pptx + derive slides/anchors/notes"},
    "NOTES_SLIDES_SYNC": {"observesFilesDirectly": True, "method": "three-way notes/slides/spec text comparison"},
    "ANSWER_LEAKAGE": {"observesFilesDirectly": True, "method": "open notes/slides/keys + reveal model"},
    "ASSESSMENT_ALIGNMENT": {"observesFilesDirectly": True, "method": "open quiz/practice + keys + score lines"},
    "SCHEDULE_POLICY": {"observesFilesDirectly": True, "method": "parse pacing calendar file"},
    "PLAYBOOK_ALIGNMENT": {"observesFilesDirectly": True, "method": "open playbook region vs spec"},
    "RENDER_COMPLETENESS": {"observesFilesDirectly": True, "method": "open render files + hash"},
    "RENDERED_VISUAL_QA": {"observesFilesDirectly": True, "method": "open render images + ink"},
    "PDF_QUALITY": {"observesFilesDirectly": True, "method": "qpdf/pdfinfo/pdffonts/pdftotext"},
    "FRESH_EXPORT": {"observesFilesDirectly": True, "method": "hash source + production, compare bytes"},
    "RETIRED_CONTENT": {"observesFilesDirectly": True, "method": "open files + scan vs baselines"},
    "INVENTORY": {"observesFilesDirectly": True, "method": "filesystem scan"},
    "RELEASE_EXACT_SET": {"observesFilesDirectly": True, "method": "open release dir + hash"},
    "RELEASE_PARITY": {"observesFilesDirectly": True, "method": "hash release dir vs originals"},
    "STATUS_AUTHORITY": {"observesFilesDirectly": True, "method": "open status surfaces from registry"},
    "ADVERSARIAL_QA": {"observesFilesDirectly": True, "method": "read runner result JSON"},
    "PRIOR_FROZEN_NONREGRESSION": {"observesFilesDirectly": True, "method": "run Ch1/Ch2 frozen tools"},
    "LAB_STRUCTURE": {"observesFilesDirectly": True, "method": "open Ramp It Up DOCX + verify table/graph/fair-test/reasoning structure"},
}


def producer_observes_files(gate_id: str) -> bool:
    return bool((PRODUCER_INDEPENDENCE.get(gate_id) or {}).get("observesFilesDirectly"))


def stamp(data: dict, gate_id: str) -> dict:
    spec = PRODUCERS[gate_id]
    versions = dict(data.get("toolVersions") or {})
    versions["producer"] = spec["id"]
    versions["producerVersion"] = spec["version"]
    data["toolVersions"] = versions
    return data


def stamp_provenance(data: dict, gate_id: str) -> dict:
    """Add producer provenance (tracked/clean/source-hash) to toolVersions."""
    from chapter_qa.producer_provenance import producer_provenance, provenance_toolversions

    spec = PRODUCERS.get(gate_id)
    if spec is None:
        return data
    versions = dict(data.get("toolVersions") or {})
    versions.update(provenance_toolversions(producer_provenance(gate_id, spec["id"])))
    data["toolVersions"] = versions
    return data
