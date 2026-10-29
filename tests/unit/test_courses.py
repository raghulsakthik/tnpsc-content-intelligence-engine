from engine.courses import (
    CourseNodeType,
    build_course,
    build_manifest,
    build_node,
    validate_course,
)


def test_course_id_is_deterministic():
    a = build_course(exam_code="TNPSC_GROUP_2", curriculum_version_id="cv1", title="General Studies")
    b = build_course(exam_code="TNPSC_GROUP_2", curriculum_version_id="cv1", title="General Studies")
    assert a.course_id == b.course_id


def test_manifest_is_stable_and_collects_content_refs():
    course = build_course(exam_code="TNPSC_GROUP_2", curriculum_version_id="cv1", title="General Studies")
    unit = build_node(course_id_value=course.course_id, node_type=CourseNodeType.UNIT, title="Science", ordinal=1)
    lesson = build_node(
        course_id_value=course.course_id,
        node_type=CourseNodeType.LESSON,
        title="Matter",
        ordinal=2,
        parent_id=unit.node_id,
        content_ref="lesson-1",
    )
    test = build_node(
        course_id_value=course.course_id,
        node_type=CourseNodeType.TEST,
        title="Science Test",
        ordinal=3,
        parent_id=unit.node_id,
        content_ref="test-1",
    )
    manifest = build_manifest(course, [test, lesson, unit])
    assert manifest.node_ids == (unit.node_id, lesson.node_id, test.node_id)
    assert manifest.required_content_refs == ("lesson-1", "test-1")
    assert len(manifest.content_hash) == 64


def test_validation_requires_lessons():
    course = build_course(exam_code="TNPSC_GROUP_2", curriculum_version_id="cv1", title="General Studies")
    unit = build_node(course_id_value=course.course_id, node_type=CourseNodeType.UNIT, title="Science", ordinal=1)
    result = validate_course(course, [unit])
    assert not result.valid
    assert "course-has-no-lessons" in result.errors


def test_validation_rejects_missing_content_reference():
    course = build_course(exam_code="TNPSC_GROUP_2", curriculum_version_id="cv1", title="General Studies")
    lesson = build_node(course_id_value=course.course_id, node_type=CourseNodeType.LESSON, title="Matter", ordinal=1)
    result = validate_course(course, [lesson])
    assert not result.valid
    assert "missing-content-ref:" + lesson.node_id in result.errors
