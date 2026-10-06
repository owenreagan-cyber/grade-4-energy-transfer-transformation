"""Auditor roles and the existing-agent map.

One agent is not given two final-certification authorities.
"""

from __future__ import annotations

ROLES = (
    "SOURCE_SCHOLAR",
    "BUILDER",
    "CURRICULUM_AUDITOR",
    "CROSS_ARTIFACT_AUDITOR",
    "VISUAL_QA_AUDITOR",
    "PDF_OOXML_FORENSICS",
    "PROVENANCE_AUDITOR",
    "QA_ADVERSARY",
    "RELEASE_JUDGE",
)

# editCanonical: may change the canonical artifact under review
# writeEvidence: may write evidence/reports
# mutateThrowaway: may change an isolated copy only
# certifyRelease: may issue INTERNAL RELEASE CERTIFICATION
CAPABILITIES = {
    "SOURCE_SCHOLAR": {
        "editCanonical": False,
        "writeEvidence": True,
        "mutateThrowaway": False,
        "certifyRelease": False,
    },
    "BUILDER": {
        "editCanonical": True,
        "writeEvidence": True,
        "mutateThrowaway": False,
        "certifyRelease": False,
    },
    "CURRICULUM_AUDITOR": {
        "editCanonical": False,
        "writeEvidence": True,
        "mutateThrowaway": False,
        "certifyRelease": False,
    },
    "CROSS_ARTIFACT_AUDITOR": {
        "editCanonical": False,
        "writeEvidence": True,
        "mutateThrowaway": False,
        "certifyRelease": False,
    },
    "VISUAL_QA_AUDITOR": {
        "editCanonical": False,
        "writeEvidence": True,
        "mutateThrowaway": False,
        "certifyRelease": False,
    },
    "PDF_OOXML_FORENSICS": {
        "editCanonical": False,
        "writeEvidence": True,
        "mutateThrowaway": False,
        "certifyRelease": False,
    },
    "PROVENANCE_AUDITOR": {
        "editCanonical": False,
        "writeEvidence": True,
        "mutateThrowaway": True,
        "certifyRelease": False,
    },
    "QA_ADVERSARY": {
        "editCanonical": False,
        "writeEvidence": True,
        "mutateThrowaway": True,
        "certifyRelease": False,
    },
    "RELEASE_JUDGE": {
        "editCanonical": False,
        "writeEvidence": True,
        "mutateThrowaway": False,
        "certifyRelease": True,
        "evidenceOnly": True,
    },
}

# Existing agents are reused. New agents cover roles that had no owner.
# visual-art-director stays a design producer and is not VISUAL_QA_AUDITOR.
AGENT_ROLE_MAP = {
    "curriculum-source-reviewer": {
        "classification": "REUSE_AS_IS",
        "functions": ["SOURCE_SCHOLAR", "CURRICULUM_AUDITOR"],
        "finalCertificationRole": None,
        "note": (
            "Source-authority evidence cites Reader/TG bytes. "
            "Curriculum-correctness evidence cites those sources against the candidate. "
            "This agent does not issue release certification."
        ),
    },
    "guided-notes-specialist": {
        "classification": "REUSE_AS_IS",
        "functions": ["BUILDER"],
        "finalCertificationRole": None,
    },
    "slideshow-specialist": {
        "classification": "REUSE_AS_IS",
        "functions": ["BUILDER"],
        "finalCertificationRole": None,
    },
    "assessment-student-resource-specialist": {
        "classification": "REUSE_AS_IS",
        "functions": ["BUILDER"],
        "finalCertificationRole": None,
    },
    "visual-art-director": {
        "classification": "REUSE_AS_IS",
        "functions": ["BUILDER"],
        "notRoles": ["VISUAL_QA_AUDITOR"],
        "finalCertificationRole": None,
        "note": "Design producer. Not the visual QA certifier.",
    },
    "qa-certification-reviewer": {
        "classification": "REUSE_AS_IS",
        "functions": ["CROSS_ARTIFACT_AUDITOR"],
        "notRoles": ["RELEASE_JUDGE"],
        "finalCertificationRole": None,
        "note": "Cross-artifact gate evidence only. Release certification belongs to release-judge.",
    },
    "provenance-auditor": {
        "classification": "NEW",
        "functions": ["PROVENANCE_AUDITOR"],
        "finalCertificationRole": None,
    },
    "qa-adversary": {
        "classification": "NEW",
        "functions": ["QA_ADVERSARY"],
        "finalCertificationRole": None,
    },
    "release-judge": {
        "classification": "NEW",
        "functions": ["RELEASE_JUDGE"],
        "finalCertificationRole": "RELEASE_JUDGE",
    },
}

# Roles with no dedicated agent yet. Do not borrow visual-art-director to fill them.
UNASSIGNED_ROLES = ("VISUAL_QA_AUDITOR", "PDF_OOXML_FORENSICS")


def may_issue_release_certification(role: str) -> bool:
    return CAPABILITIES[role]["certifyRelease"] is True


def is_builder(role: str) -> bool:
    return role == "BUILDER"
