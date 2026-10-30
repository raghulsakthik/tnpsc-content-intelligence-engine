"""Build a safe import payload for the existing Yash TNPSC platform.

The platform currently stores one primary lesson per topic and questions as
rows in ``question``.  The intelligence engine may contain multiple lessons
per topic, so this adapter never silently drops them: it selects an explicit
primary lesson and reports additional lessons as review-required items.

This module only transforms already-approved engine objects. It performs no
HTTP requests, database writes, approval, or publication.
"""

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
        {
            "kind": item.kind,
            "content_id": item.content_id,
            "topic_id": item.topic_id,
            "payload": item.payload,
        }
        for item in items
    ]
    raw = json.dumps(
        {"publication_id": publication_id, "items": canonical},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return sha256(raw.encode("utf-8")).hexdigest()


def build_import_plan(
    *,
    publication_id: str,
    lessons: Iterable[Lesson],
    mcqs: Iterable[MCQ],
) -> PlatformImportPlan:
    """Create a deterministic import plan from approved engine content.

    PYQ content is rejected. Unapproved content is rejected. Multiple
    approved lessons for one topic are reported rather than silently lost.
    """
    approved_lessons = [lesson for lesson in lessons if lesson.status == LessonStatus.APPROVED]
    approved_mcqs = [mcq for mcq in mcqs if mcq.status == MCQStatus.APPROVED]

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
        items.append(
            PlatformImportItem(
                kind="lesson",
                content_id=lesson.lesson_id,
                topic_id=topic_id,
                payload={
                    "title": lesson.title,
                    "concept": lesson.concept,
                    "definition": lesson.definition,
                    "explanation": lesson.explanation,
                    "examples": list(lesson.examples),
                    "revisionNotes": list(lesson.revision_notes),
                    "sourceIds": list(lesson.source_ids),
                    "version": lesson.version,
                },
            )
        )

    for mcq in sorted(approved_mcqs, key=lambda value: value.mcq_id):
        # The MCQ model carries the hard PYQ gate. Keep the adapter defensive
        # because this is the last boundary before platform persistence.
        if getattr(mcq, "is_pyq", False) or str(getattr(mcq, "generation_source", "")).lower() == "pyq":
            review.append(f"pyq-block:{mcq.mcq_id}")
            continue
        if not mcq.source_ids:
            review.append(f"missing-provenance:{mcq.mcq_id}")
            continue
        items.append(
            PlatformImportItem(
                kind="mcq",
                content_id=mcq.mcq_id,
                topic_id=mcq.curriculum_node_id,
                payload={
                    "question": mcq.question,
                    "options": list(mcq.options),
                    "answerIndex": mcq.answer_index,
                    "explanation": mcq.explanation,
                    "difficulty": mcq.difficulty.value,
                    "sourceIds": list(mcq.source_ids),
                    "version": mcq.version,
                },
            )
        )

    items_tuple = tuple(items)
    return PlatformImportPlan(
        publication_id=publication_id,
        manifest_hash=_manifest_hash(publication_id, items_tuple),
        items=items_tuple,
        review_required=tuple(sorted(set(review))),
    )
