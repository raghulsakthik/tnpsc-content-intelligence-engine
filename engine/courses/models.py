"""Versioned course domain models."""

from dataclasses import dataclass, field
from enum import StrEnum


class CourseStatus(StrEnum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    RETIRED = "retired"


class CourseNodeType(StrEnum):
    UNIT = "unit"
    TOPIC = "topic"
    LESSON = "lesson"
    MCQ_SET = "mcq_set"
    TEST = "test"


@dataclass(frozen=True, slots=True)
class Course:
    course_id: str
    exam_code: str
    curriculum_version_id: str
    title: str
    status: CourseStatus = CourseStatus.DRAFT
    version: int = 1
    description: str = ""
    metadata: dict[str, object] = field(default_factory=dict)

    def is_publishable(self) -> bool:
        return self.status in {CourseStatus.APPROVED, CourseStatus.PUBLISHED}


@dataclass(frozen=True, slots=True)
class CourseNode:
    node_id: str
    course_id: str
    node_type: CourseNodeType
    title: str
    ordinal: int
    parent_id: str | None = None
    content_ref: str | None = None
    required: bool = True
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CourseDependency:
    course_id: str
    prerequisite_node_id: str
    dependent_node_id: str


@dataclass(frozen=True, slots=True)
class CourseManifest:
    course_id: str
    version: int
    node_ids: tuple[str, ...]
    required_content_refs: tuple[str, ...]
    curriculum_version_id: str
    content_hash: str
