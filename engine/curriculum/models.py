"""Versioned canonical curriculum entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum
from typing import Optional


class CurriculumStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    RETIRED = "retired"


class NodeType(StrEnum):
    EXAM = "exam"
    SUBJECT = "subject"
    UNIT = "unit"
    TOPIC = "topic"
    SUBTOPIC = "subtopic"


@dataclass(frozen=True, slots=True)
class CurriculumVersion:
    id: str
    exam_code: str
    source_reference: str
    effective_from: date
    status: CurriculumStatus = CurriculumStatus.DRAFT


@dataclass(frozen=True, slots=True)
class CurriculumNode:
    id: str
    curriculum_version_id: str
    node_type: NodeType
    canonical_key: str
    title_en: str
    title_ta: Optional[str] = None
    parent_id: Optional[str] = None
    aliases: tuple[str, ...] = field(default_factory=tuple)
    sort_order: int = 0

    def is_root(self) -> bool:
        return self.parent_id is None
