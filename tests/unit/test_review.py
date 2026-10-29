from engine.review import (
    ReviewDecision,
    ReviewDecisionRecord,
    ReviewItem,
    ReviewStatus,
    apply_decision,
    review_id,
    start_review,
)


def item():
    return ReviewItem(
        review_id=review_id("lesson", "lesson-1", 1),
        content_type="lesson",
        content_id="lesson-1",
        content_version=1,
        evidence_ids=("ev-1",),
    )


def test_review_starts_only_with_evidence():
    updated = start_review(item(), "admin-1")
    assert updated.status == ReviewStatus.IN_REVIEW
    assert updated.assigned_reviewer == "admin-1"


def test_approve_creates_audit_event():
    current = start_review(item(), "admin-1")
    decision = ReviewDecisionRecord(
        review_id=current.review_id,
        reviewer_id="admin-1",
        decision=ReviewDecision.APPROVE,
        reason="Evidence and quality checks reviewed.",
        created_at="2026-10-29T12:00:00Z",
    )
    updated, event = apply_decision(current, decision)
    assert updated.status == ReviewStatus.APPROVED
    assert event.action == "approve"
    assert event.entity_id == "lesson-1"


def test_request_changes_can_return_to_review():
    current = start_review(item(), "admin-1")
    decision = ReviewDecisionRecord(
        review_id=current.review_id,
        reviewer_id="admin-1",
        decision=ReviewDecision.REQUEST_CHANGES,
        reason="Clarify the explanation.",
        created_at="2026-10-29T12:00:00Z",
    )
    updated, _ = apply_decision(current, decision)
    assert updated.status == ReviewStatus.CHANGES_REQUESTED
    resumed = start_review(updated, "admin-2")
    assert resumed.status == ReviewStatus.IN_REVIEW


def test_approved_item_cannot_be_reviewed_again():
    current = start_review(item(), "admin-1")
    decision = ReviewDecisionRecord(
        review_id=current.review_id,
        reviewer_id="admin-1",
        decision=ReviewDecision.APPROVE,
        reason="Approved.",
        created_at="2026-10-29T12:00:00Z",
    )
    approved, _ = apply_decision(current, decision)
    try:
        start_review(approved, "admin-2")
    except ValueError:
        pass
    else:
        raise AssertionError("approved content must be immutable in this workflow")
