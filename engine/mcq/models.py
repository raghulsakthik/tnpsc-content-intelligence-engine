"""Versioned, source-backed MCQ domain models."""

from dataclasses import dataclass, field
from enum import StrEnum


class Difficulty(StrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class MCQStatus(StrEnum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXCLUDED_PYQ = "excluded_pyq"


@dataclass(frozen=True, slots=True)
class MCQOption:
    option_id: str
    text: str
    is_correct: bool = False


@dataclass(frozen=True, slots=True)
class MCQ:
    mcq_id: str
    lesson_id: str
    curriculum_node_id: str
    question: str
    options: tuple[MCQOption, ...]
    explanation: str
    difficulty: Difficulty
    source_evidence_ids: tuple[str, ...] = ()
    is_pyq: bool = False
    status: MCQStatus = MCQStatus.DRAFT
    version: int = 1
    metadata: dict[str, object] = field(default_factory=dict)

    def correct_options(self) -> tuple[MCQOption, ...]:
        return tuple(option for option in self.options if option.is_correct)

    def is_publishable(self) -> bool:
        return (
            self.status == MCQStatus.APPROVED
            and not self.is_pyq
            and len(self.source_evidence_ids) > 0
        )


@dataclass(frozen=True, slots=True)
class MCQValidationResult:
    valid: bool
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    fingerprint: str | None = None
