from engine.lessons.models import Lesson, LessonStatus
from engine.mcq.models import Difficulty, MCQ, MCQOption, MCQStatus
from engine.platform.tnpsc_import import build_import_plan


def lesson(topic: str, lesson_id: str = "lesson-1") -> Lesson:
    return Lesson(
        lesson_id=lesson_id,
        curriculum_node_id=topic,
        title="Fractions",
        concept="A fraction represents a part of a whole.",
        definition="A ratio of numerator to denominator.",
        source_ids=("evidence-1",),
        status=LessonStatus.APPROVED,
    )


def mcq(topic: str, *, pyq: bool = False, evidence: tuple[str, ...] = ("evidence-1",)) -> MCQ:
    return MCQ(
        mcq_id="mcq-1",
        lesson_id="lesson-1",
        curriculum_node_id=topic,
        question="Which is a fraction?",
        options=(
            MCQOption("a", "1/2"),
            MCQOption("b", "2", True),
            MCQOption("c", "0"),
            MCQOption("d", "-1"),
        ),
        explanation="2 is the correct option.",
        difficulty=Difficulty.EASY,
        source_evidence_ids=evidence,
        is_pyq=pyq,
        status=MCQStatus.APPROVED,
    )


def test_approved_content_builds_deterministic_plan():
    first = build_import_plan(publication_id="pub-1", lessons=[lesson("aptitude.fractions")], mcqs=[mcq("aptitude.fractions")])
    second = build_import_plan(publication_id="pub-1", lessons=[lesson("aptitude.fractions")], mcqs=[mcq("aptitude.fractions")])

    assert first.manifest_hash == second.manifest_hash
    assert first.is_safe_to_send
    assert [item.kind for item in first.items] == ["lesson", "mcq"]


def test_pyq_is_blocked_at_platform_boundary():
    plan = build_import_plan(publication_id="pub-1", lessons=[lesson("aptitude.fractions")], mcqs=[mcq("aptitude.fractions", pyq=True)])

    assert not plan.is_safe_to_send
    assert "pyq-block:mcq-1" in plan.review_required


def test_missing_evidence_is_blocked():
    plan = build_import_plan(publication_id="pub-1", lessons=[], mcqs=[mcq("aptitude.fractions", evidence=())])

    assert not plan.is_safe_to_send
    assert "missing-provenance:mcq-1" in plan.review_required


def test_multiple_lessons_for_single_platform_topic_require_review():
    plan = build_import_plan(
        publication_id="pub-1",
        lessons=[lesson("aptitude.fractions", "lesson-1"), lesson("aptitude.fractions", "lesson-2")],
        mcqs=[],
    )

    assert not plan.is_safe_to_send
    assert "multiple-approved-lessons:aptitude.fractions" in plan.review_required
