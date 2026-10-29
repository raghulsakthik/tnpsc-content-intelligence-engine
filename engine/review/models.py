"""Admin review domain models and explicit publication boundaries."""

from dataclasses import dataclass, field
from enum import StrEnum


class ReviewDecision(StrEnum):
    APPROVE = "approve"
    REQUEST_CHANGES = "request_changes"
    REJECT = "reject"


class ReviewStatus(StrEnum):
    QUEUED = "queued"
    IN_REVIEW = "in_review"
    CHANGES_REQUESTED = "changes_requested"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class ReviewItem:
    review_id: str
    content_type: str
    content_id: str
    content_version: int
    evidence_ids: tuple[str, ...] = ()
    quality_check_ids: tuple[str, ...] = ()
    status: ReviewStatus = ReviewStatus.QUEUED
    assigned_reviewer: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)

    def can_be_reviewed(self) -> bool:
        return bool(self.content_id and self.content_version > 0 and self.evidence_ids)


@dataclass(frozen=True, slots=True)
class ReviewDecisionRecord:
    review_id: str
    reviewer_id: str
    decision: ReviewDecision
    reason: str
    created_at: str
    edited_content_version: int | None = None

    def is_valid(self) -> bool:
        return bool(self.reviewer_id and self.reason.strip() and self.created_at)


@dataclass(frozen=True, slots=True)
class AuditEvent:
    event_id: str
    actor_id: str
    action: str
    entity_type: str
    entity_id: str
    timestamp: str
    before_version: int | None = None
    after_version: int | None = None
    metadata: dict[str, object] = field(default_factory=dict)
