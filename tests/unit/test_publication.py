import hashlib
import json

import pytest

from engine.integration.publication import (
    PublicationContractError,
    build_publication_package,
    manifest_hash,
)
from engine.lessons.builder import build_lesson
from engine.lessons.models import LessonStatus
from engine.mcq.models import Difficulty, MCQ, MCQOption, MCQStatus


def approved_lesson():
    lesson = build_lesson(
        curriculum_node_id="aptitude.fractions",
        title="Fractions",
        concept="Parts of a whole",
        definition="A fraction represents a part of a whole.",
        explanation="The numerator counts selected parts and the denominator counts equal parts.",
        source_ids=["evidence-1"],
    )
    return LessonStatus, lesson.__class__(**{**lesson.__dict__}) if False else lesson


def test_publication_package_matches_platform_hash_contract():
    lesson = build_lesson(
        curriculum_node_id="aptitude.fractions",
        title="Fractions",
        concept="Parts of a whole",
        source_ids=["evidence-1"],
    )
    lesson = lesson.__class__(
        **{field: getattr(lesson, field) for field in lesson.__dataclass_fields__},
        status=LessonStatus.APPROVED,
    )
    package = build_publication_package(
        publication_id="pub-1",
        lessons=[lesson],
        topic_map={"aptitude.fractions": "topic-123"},
    )
    items = list(package.items)
    canonical = json.dumps(
        {
            "publication_id": "pub-1",
            "items": [
                {
                    "kind": item["kind"],
                    "content_id": item["content_id"],
                    "topic_id": item["topic_id"],
                    "payload": item["payload"],
                }
                for item in items
            ],
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    expected = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    assert package.manifest_hash == expected
    assert manifest_hash("pub-1", items) == expected


def test_missing_topic_mapping_fails_closed():
    lesson = build_lesson(
        curriculum_node_id="history.chola",
        title="Chola Administration",
        concept="Administration",
        source_ids=["evidence-2"],
    )
    with pytest.raises(PublicationContractError, match="missing-platform-topic"):
        build_publication_package(
            publication_id="pub-2",
            lessons=[lesson],
            topic_map={},
        )


def test_unapproved_content_cannot_be_published():
    lesson = build_lesson(
        curriculum_node_id="history.chola",
        title="Chola Administration",
        concept="Administration",
        source_ids=["evidence-3"],
    )
    with pytest.raises(PublicationContractError, match="lesson-not-publishable"):
        build_publication_package(
            publication_id="pub-3",
            lessons=[lesson],
            topic_map={"history.chola": "topic-456"},
        )


def test_pyq_mcq_cannot_cross_boundary():
    mcq = MCQ(
        mcq_id="pyq-1",
        lesson_id="lesson-1",
        curriculum_node_id="history.chola",
        question="Which?",
        options=(MCQOption("a", "A", True), MCQOption("b", "B")),
        explanation="Because.",
        difficulty=Difficulty.EASY,
        source_evidence_ids=("evidence-4",),
        is_pyq=True,
        status=MCQStatus.APPROVED,
    )
    with pytest.raises(PublicationContractError, match="mcq-not-publishable"):
        build_publication_package(
            publication_id="pub-4",
            mcqs=[mcq],
            topic_map={"history.chola": "topic-456"},
        )
