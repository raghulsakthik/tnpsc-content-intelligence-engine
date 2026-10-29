"""Models for deterministic content classification."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Optional


class ClassificationStatus(StrEnum):
    CLASSIFIED = "classified"
    REVIEW_REQUIRED = "review_required"
    EXCLUDED_PYQ = "excluded_pyq"
    UNCLASSIFIED = "unclassified"


@dataclass(frozen=True, slots=True)
class ClassificationScores:
    subject: float = 0.0
    unit: float = 0.0
    content_type: float = 0.0
    pyq: float = 0.0
    government_material: float = 0.0

    def as_dict(self) -> dict[str, float]:
        return {
            "subject": self.subject,
            "unit": self.unit,
            "content_type": self.content_type,
            "pyq": self.pyq,
            "government_material": self.government_material,
        }


@dataclass(frozen=True, slots=True)
class ClassificationDecision:
    document_id: Optional[str]
    exam: str
    subject: Optional[str]
    unit: Optional[str]
    topic: Optional[str]
    subtopic: Optional[str]
    language: Optional[str]
    content_type: Optional[str]
    is_pyq: bool
    is_mock: bool
    is_current_affair: bool
    is_government_material: bool
    evidence_terms: tuple[str, ...] = ()
    scores: ClassificationScores = field(default_factory=ClassificationScores)
    status: ClassificationStatus = ClassificationStatus.UNCLASSIFIED
    review_reasons: tuple[str, ...] = ()

    @property
    def publishable(self) -> bool:
        """Classification is never a publication approval; PYQs are always blocked."""
        return self.status not in {
            ClassificationStatus.EXCLUDED_PYQ,
            ClassificationStatus.REVIEW_REQUIRED,
            ClassificationStatus.UNCLASSIFIED,
        } and not self.is_pyq
