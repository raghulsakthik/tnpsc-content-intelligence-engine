"""Initial TNPSC Group II/IIA canonical taxonomy.

This is intentionally a seed taxonomy, not a claim that every syllabus
revision is identical. The source reference and curriculum version must be
updated when the official syllabus changes.
"""

from __future__ import annotations

from .models import CurriculumNode, CurriculumVersion, CurriculumStatus, NodeType


CURRICULUM = CurriculumVersion(
    id="tnpsc-group-2-2a-2022-v1",
    exam_code="TNPSC_GROUP_2_2A",
    source_reference="TNPSC Revised Group II/IIA Scheme & Syllabus 27-01-2022",
    effective_from=__import__("datetime").date(2022, 1, 27),
    status=CurriculumStatus.ACTIVE,
)


def _subject(key: str, en: str, ta: str, order: int) -> CurriculumNode:
    return CurriculumNode(
        id=f"{CURRICULUM.id}:{key}",
        curriculum_version_id=CURRICULUM.id,
        node_type=NodeType.SUBJECT,
        canonical_key=key,
        title_en=en,
        title_ta=ta,
        sort_order=order,
    )


SUBJECTS = (
    _subject("general-studies", "General Studies", "பொது அறிவு", 10),
    _subject("aptitude-mental-ability", "Aptitude & Mental Ability", "திறனறிவு மற்றும் மனத்திறன்", 20),
    _subject("general-tamil", "General Tamil", "பொதுத்தமிழ்", 30),
    _subject("general-english", "General English", "பொது ஆங்கிலம்", 40),
    _subject("thirukkural", "Thirukkural", "திருக்குறள்", 50),
    _subject("current-affairs", "Current Affairs", "நடப்பு நிகழ்வுகள்", 60),
)


def general_studies_units() -> tuple[CurriculumNode, ...]:
    parent = next(x for x in SUBJECTS if x.canonical_key == "general-studies")
    specs = (
        ("science", "Science", "அறிவியல்"),
        ("geography", "Geography", "புவியியல்"),
        ("history-culture", "History & Culture", "வரலாறு மற்றும் பண்பாடு"),
        ("indian-national-movement", "Indian National Movement", "இந்திய தேசிய இயக்கம்"),
        ("indian-polity", "Indian Polity", "இந்திய அரசியல் அமைப்பு"),
        ("indian-economy", "Indian Economy", "இந்திய பொருளாதாரம்"),
        ("tn-development-administration", "Development Administration in Tamil Nadu", "தமிழ்நாட்டின் வளர்ச்சி நிர்வாகம்"),
        ("tn-history-culture-heritage", "Tamil Nadu History, Culture & Heritage", "தமிழ்நாடு வரலாறு, பண்பாடு மற்றும் பாரம்பரியம்"),
        ("science-technology", "Science & Technology", "அறிவியல் மற்றும் தொழில்நுட்பம்"),
        ("socio-economic-issues", "Socio-Economic Issues", "சமூக-பொருளாதாரப் பிரச்சினைகள்"),
        ("environment", "Environment", "சுற்றுச்சூழல்"),
    )
    return tuple(
        CurriculumNode(
            id=f"{CURRICULUM.id}:gs:{key}",
            curriculum_version_id=CURRICULUM.id,
            node_type=NodeType.UNIT,
            canonical_key=f"general-studies.{key}",
            title_en=en,
            title_ta=ta,
            parent_id=parent.id,
            sort_order=(i + 1) * 10,
        )
        for i, (key, en, ta) in enumerate(specs)
    )
