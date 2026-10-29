"""Models for deterministic and review-oriented content quality checks."""

from dataclasses import dataclass, field
from enum import StrEnum


class QualityStatus(StrEnum):
    PASS = "pass"
    REVIEW = "review"
    FAIL = "fail"


class CheckSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class QualityCheck:
    name: str
    status: QualityStatus
    severity: CheckSeverity
    message: str
    evidence_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class QualityReport:
    content_id: str
    checks: tuple[QualityCheck, ...] = ()
    metadata: dict[str, object] = field(default_factory=dict)

    @property
    def status(self) -> QualityStatus:
        if any(c.status == QualityStatus.FAIL for c in self.checks):
            return QualityStatus.FAIL
        if any(c.status == QualityStatus.REVIEW for c in self.checks):
            return QualityStatus.REVIEW
        return QualityStatus.PASS

    def publishable(self) -> bool:
        return self.status == QualityStatus.PASS
