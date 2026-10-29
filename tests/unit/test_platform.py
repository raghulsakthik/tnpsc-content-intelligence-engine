from engine.courses.models import Course, CourseNode, CourseNodeType
from engine.platform import build_publication


def course() -> Course:
    return Course(
        course_id="course-1",
        exam_code="TNPSC_GROUP_2_2A",
        curriculum_version_id="curriculum-v1",
        title="TNPSC Group II Foundation",
        version=2,
    )


def test_publication_only_emits_approved_content_with_provenance():
    nodes = [
        CourseNode("n1", "course-1", CourseNodeType.LESSON, "Lesson", 1, content_ref="lesson-1"),
        CourseNode("n2", "course-1", CourseNodeType.MCQ_SET, "MCQs", 2, content_ref="mcq-1"),
    ]
    envelope = build_publication(
        course=course(),
        manifest_hash="manifest-1",
        nodes=nodes,
        approved_content_ids={"lesson-1"},
        source_ids_by_content={"lesson-1": ("evidence-1",)},
    )
    assert envelope.is_publishable()
    assert envelope.course.content_refs == ("lesson-1",)
    assert envelope.contents[0].source_ids == ("evidence-1",)


def test_unapproved_content_is_not_emitted():
    node = CourseNode("n1", "course-1", CourseNodeType.LESSON, "Lesson", 1, content_ref="lesson-1")
    envelope = build_publication(
        course=course(),
        manifest_hash="manifest-1",
        nodes=[node],
        approved_content_ids=set(),
        source_ids_by_content={"lesson-1": ("evidence-1",)},
    )
    assert envelope.contents == ()


def test_missing_provenance_blocks_publication():
    node = CourseNode("n1", "course-1", CourseNodeType.LESSON, "Lesson", 1, content_ref="lesson-1")
    envelope = build_publication(
        course=course(),
        manifest_hash="manifest-1",
        nodes=[node],
        approved_content_ids={"lesson-1"},
        source_ids_by_content={},
    )
    assert not envelope.is_publishable()
