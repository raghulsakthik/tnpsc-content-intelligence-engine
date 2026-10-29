"""Deterministic admin review state transitions."""

from __future__ import annotations

import hashlib

from .models import AuditEvent, ReviewDecision, ReviewDecisionRecord, ReviewItem, ReviewStatus


_ALLOWED: dict[ReviewStatus, set[ReviewStatus]] = {
    ReviewStatus.QUEUED: {ReviewStatus.IN_REVIEW},
    ReviewStatus.IN_REVIEW: {
        ReviewStatus.CHANGES_REQUESTED,
        ReviewStatus.APPROVED,
        ReviewStatus.REJECTED,
    },
    ReviewStatus.CHANGES_REQUESTED: {ReviewStatus.IN_REVIEW, ReviewStatus.REJECTED},
    ReviewStatus.APPROVED: set(),
    ReviewStatus.REJECTED: set(),
}


def review_id(content_type: str, content_id: str, version: int) -> str:
    raw = f"{content_type}|{content_id}|{version}".encode()
    return hashlib.sha256(raw).hexdigest()[:24]


def start_review(item: ReviewItem, reviewer_id: str) -> ReviewItem:
    if not reviewer_id.strip():
        raise ValueError("reviewer_id is required")
    if not item.can_be_reviewed():
        raise ValueError("review item is missing content version or evidence")
    if ReviewStatus.IN_REVIEW not in _ALLOWED[item.status]:
        raise ValueError(f"cannot start review from {item.status}")
    return ReviewItem(
        review_id=item.review_id,
        content_type=item.content_type,
        content_id=item.content_id,
        content_version=item.content_version,
        evidence_ids=item.evidence_ids,
        quality_check_ids=item.quality_check_ids,
        status=ReviewStatus.IN_REVIEW,
        assigned_reviewer=reviewer_id,
        metadata=item.metadata,
    )


def apply_decision(item: ReviewItem, decision: ReviewDecisionRecord) -> tuple[ReviewItem, AuditEvent]:
    if item.status not in {ReviewStatus.IN_REVIEW, ReviewStatus.CHANGES_REQUESTED}:
        raise ValueError(f"cannot decide review from {item.status}")
    if not decision.is_valid() or decision.review_id != item.review_id:
        raise ValueError("invalid review decision")
    if decision.decision == ReviewDecision.APPROVE:
        status = ReviewStatus.APPROVED
    elif decision.decision == ReviewDecision.REQUEST_CHANGES:
        status = ReviewStatus.CHANGES_REQUESTED
    else:
        status = ReviewStatus.REJECTED

    updated = ReviewItem(
        review_id=item.review_id,
        content_type=item.content_type,
        content_id=item.content_id,
        content_version=item.content_version,
        evidence_ids=item.evidence_ids,
        quality_check_ids=item.quality_check_ids,
        status=status,
        assigned_reviewer=item.assigned_reviewer,
        metadata=item.metadata,
    )
    event_key = f"{item.review_id}|{decision.reviewer_id}|{decision.created_at}|{decision.decision}"
    event = AuditEvent(
        event_id=hashlib.sha256(event_key.encode()).hexdigest()[:24],
        actor_id=decision.reviewer_id,
        action=decision.decision.value,
        entity_type=item.content_type,
        entity_id=item.content_id,
        timestamp=decision.created_at,
        before_version=item.content_version,
        after_version=decision.edited_content_version,
        metadata={"review_id": item.review_id, "reason": decision.reason},
    )
    return updated, event
