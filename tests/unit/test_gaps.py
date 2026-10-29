from engine.gaps import (
    AcquisitionStatus,
    CoverageRecord,
    GapSeverity,
    analyze_coverage,
    build_acquisition_requests,
)


def test_missing_content_is_critical():
    gaps = analyze_coverage([CoverageRecord("indian-polity", quality_score=0.0)])
    assert len(gaps) == 1
    assert gaps[0].severity == GapSeverity.CRITICAL
    assert "no-approved-content" in gaps[0].reasons


def test_weak_content_produces_gap():
    gaps = analyze_coverage([CoverageRecord("science", approved_lesson_count=1, approved_mcq_count=3, source_count=1, quality_score=0.8)])
    assert gaps[0].severity in {GapSeverity.HIGH, GapSeverity.MEDIUM}
    assert "insufficient-lessons" in gaps[0].reasons
    assert "insufficient-mcqs" in gaps[0].reasons
    assert "missing-topic-test" in gaps[0].reasons


def test_complete_high_quality_topic_has_no_gap():
    records = [CoverageRecord("geography", approved_lesson_count=3, approved_mcq_count=20, approved_test_count=1, source_count=2, quality_score=0.95)]
    assert analyze_coverage(records) == ()


def test_requests_are_prioritized_and_do_not_fetch():
    gaps = analyze_coverage([
        CoverageRecord("economy", quality_score=0.0),
        CoverageRecord("history", approved_lesson_count=1, approved_mcq_count=3, source_count=1, quality_score=0.6),
    ])
    requests = build_acquisition_requests(gaps)
    assert requests[0].priority >= requests[1].priority
    assert requests[0].status == AcquisitionStatus.PROPOSED
    assert all(request.queries for request in requests)


def test_gap_ids_are_deterministic():
    record = CoverageRecord("environment", quality_score=0.5)
    assert analyze_coverage([record])[0].gap_id == analyze_coverage([record])[0].gap_id
