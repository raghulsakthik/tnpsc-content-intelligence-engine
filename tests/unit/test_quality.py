from engine.quality import QualityStatus, check_lesson, check_mcq


def test_lesson_without_sources_fails():
    report = check_lesson(
        lesson_id="l1",
        title="Photosynthesis",
        concept="How plants make food",
        explanation="Plants use light energy.",
        source_ids=[],
    )
    assert report.status == QualityStatus.FAIL
    assert not report.publishable()


def test_lesson_with_sources_requires_semantic_review():
    report = check_lesson(
        lesson_id="l1",
        title="Photosynthesis",
        concept="How plants make food",
        explanation="Plants use light energy.",
        source_ids=["ev1"],
    )
    assert report.status == QualityStatus.REVIEW
    assert not report.publishable()


def test_mcq_pyq_is_hard_failure():
    report = check_mcq(
        mcq_id="m1",
        question="Which is correct?",
        options=["A", "B", "C", "D"],
        correct_option_ids=["A"],
        explanation="Evidence-backed explanation.",
        source_ids=["ev1"],
        is_pyq=True,
    )
    assert report.status == QualityStatus.FAIL


def test_mcq_duplicate_options_fail():
    report = check_mcq(
        mcq_id="m1",
        question="Which is correct?",
        options=["A", "A", "C", "D"],
        correct_option_ids=["A"],
        explanation="Explanation.",
        source_ids=["ev1"],
    )
    assert report.status == QualityStatus.FAIL


def test_mcq_multiple_correct_answers_fail():
    report = check_mcq(
        mcq_id="m1",
        question="Which are correct?",
        options=["A", "B", "C", "D"],
        correct_option_ids=["A", "B"],
        explanation="Explanation.",
        source_ids=["ev1"],
    )
    assert report.status == QualityStatus.FAIL
