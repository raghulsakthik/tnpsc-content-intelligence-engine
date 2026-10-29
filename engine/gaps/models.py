"""Domain models for curriculum coverage gaps and acquisition requests."""

from dataclasses import dataclass, field
from enum import StrEnum


class GapSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AcquisitionStatus(StrEnum):
    PROPOSED = "proposed"
    QUEUED = "queued"
    SENT = "sent"
    SATISFIED = "satisfied"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class CoverageRecord:
    curriculum_node_id: str
    approved_lesson_count: int = 0
    approved_mcq_count: int = 0
    approved_test_count: int = 0
    source_count: int = 0
    quality_score: float = 0.0

    @property
    def content_score(self) -> float:
        return min(1.0, (self.approved_lesson_count / 2) * 0.5 + (self.approved_mcq_count / 10) * 0.3 + (self.approved_test_count > 0) * 0.2)


@dataclass(frozen=True, slots=True)
class CoverageGap:
    gap_id: str
    curriculum_node_id: str
    severity: GapSeverity
    coverage_score: float
    reasons: tuple[str, ...] = ()
    suggested_queries: tuple[str, ...] = ()
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AcquisitionRequest:
    request_id: str
    gap_id: str
    curriculum_node_id: str
    queries: tuple[str, ...]
    status: AcquisitionStatus = AcquisitionStatus.PROPOSED
    priority: int = 0
    metadata: dict[str, object] = field(default_factory=dict)
