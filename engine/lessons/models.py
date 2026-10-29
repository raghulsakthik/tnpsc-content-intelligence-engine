"""Versioned lesson domain models."""

from dataclasses import dataclass, field
from enum import StrEnum


class LessonStatus(StrEnum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class LessonSource:
    evidence_id: str
    source_label: str | None = None


@dataclass(frozen=True, slots=True)
class Lesson:
    lesson_id: str
    curriculum_node_id: str
    title: str
    concept: str
    definition: str = ""
    explanation: str = ""
    examples: tuple[str, ...] = ()
    revision_notes: tuple[str, ...] = ()
    source_ids: tuple[str, ...] = ()
    status: LessonStatus = LessonStatus.DRAFT
    version: int = 1
    metadata: dict[str, object] = field(default_factory=dict)

    def is_publishable(self) -> bool:
        return self.status == LessonStatus.APPROVED and bool(self.source_ids)
