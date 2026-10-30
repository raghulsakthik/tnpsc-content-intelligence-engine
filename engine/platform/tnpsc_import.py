"""Build a safe import payload for the existing Yash TNPSC platform."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Iterable

from engine.lessons.models import Lesson, LessonStatus
from engine.mcq.models import MCQ, MCQStatus


@dataclass(frozen=True, slots=True)
class PlatformImportItem:
    kind: str
    content_id: str
    topic_id: str
    payload: dict[str, object]


@dataclass(frozen=True, slots=True)
class PlatformImportPlan:
    publication_id: str
    manifest_hash: str
    items: tuple[PlatformImportItem, ...]
    review_required: tuple[str, ...] = ()

    @property
    def is_safe_to_send(self) -> bool:
        return bool(self.publication_id and self.manifest_hash and not self.review_required)


def _manifest_hash(publication_id: str, items: Iterable[PlatformImportItem]) -> str:
    canonical = [
        {"kind": i.kind, "content_id": i.content_id, "topic_id": i.topic_id, "payload": i.payload}
        for i in items
    ]
    raw = json.dumps({"publication_id": publication_id, "items": canonical}, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(raw.encode("utf-8")).hexdigest()


def build_import_plan(*, publication_id: str, lessons: Iterable[Lesson], mcqs: Iterable[MCQ]) -> PlatformImportPlan:
    """Create a deterministic import plan from approved engine content."""
    approved_lessons = [x for x in lessons if x.status == LessonStatus.APPROVED]
    approved_mcqs = [x for x in mcqs if x.status == MCQStatus.APPROVED]
    review: list[str] = []
    items: list[PlatformImportItem] = []

    lesson_by_topic: dict[str, list[Lesson]] = {}
    for lesson in approved_lessons:
        lesson_by_topic.setdefault(lesson.curriculum_node_id, []).append(lesson)
    for topic_id, topic_lessons in sorted(lesson_by_topic.items()):
        if len(topic_lessons) > 1:
            review.append(f"multiple-approved-lessons:{topic_id}")
            continue
        lesson = topic_lessons[0]
        items.append(PlatformImportItem("lesson", lesson.lesson_id, topic_id, {
            "title": lesson.title, "concept": lesson.concept, "definition": lesson.definition,
            "explanation": lesson.explanation, "examples": list(lesson.examples),
            "revisionNotes": list(lesson.revision_notes), "sourceIds": list(lesson.source_ids),
            "version": lesson.version,
        }))

    for mcq in sorted(approved_mcqs, key=lambda value: value.mcq_id):
        if mcq.is_pyq or mcq.status == MCQStatus.EXCLUDED_PYQ:
            review.append(f"pyq-block:{mcq.mcq_id}")
            continue
        if not mcq.source_evidence_ids:
            review.append(f"missing-provenance:{mcq.mcq_id}")
            continue
        correct = tuple(i for i, option in enumerate(mcq.options) if option.is_correct)
        if len(correct) != 1:
            review.append(f"invalid-answer-cardinality:{mcq.mcq_id}")
            continue
        items.append(PlatformImportItem("mcq", mcq.mcq_id, mcq.curriculum_node_id, {
            "question": mcq.question, "options": [x.text for x in mcq.options],
            "answerIndex": correct[0], "explanation": mcq.explanation,
            "difficulty": mcq.difficulty.value, "sourceIds": list(mcq.source_evidence_ids),
            "version": mcq.version,
        }))

    result = tuple(items)
    return PlatformImportPlan(publication_id, _manifest_hash(publication_id, result), result, tuple(sorted(set(review))))
