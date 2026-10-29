"""Course structure validation and publication gates."""

from dataclasses import dataclass

from .models import Course, CourseNode, CourseNodeType


@dataclass(frozen=True, slots=True)
class CourseValidation:
    valid: bool
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


def validate_course(course: Course, nodes: list[CourseNode]) -> CourseValidation:
    errors: list[str] = []
    warnings: list[str] = []

    if not course.exam_code.strip():
        errors.append("missing-exam-code")
    if not course.curriculum_version_id.strip():
        errors.append("missing-curriculum-version")
    if not course.title.strip():
        errors.append("missing-course-title")
    if not nodes:
        errors.append("course-has-no-nodes")
        return CourseValidation(False, tuple(errors), tuple(warnings))

    ids = {node.node_id for node in nodes}
    if len(ids) != len(nodes):
        errors.append("duplicate-node-id")

    ordinals = [node.ordinal for node in nodes]
    if len(ordinals) != len(set(ordinals)):
        warnings.append("duplicate-ordinal")

    for node in nodes:
        if node.course_id != course.course_id:
            errors.append(f"foreign-course-node:{node.node_id}")
        if not node.title.strip():
            errors.append(f"missing-node-title:{node.node_id}")
        if node.parent_id and node.parent_id not in ids:
            errors.append(f"missing-parent:{node.node_id}")
        if node.node_type in {CourseNodeType.LESSON, CourseNodeType.MCQ_SET, CourseNodeType.TEST} and not node.content_ref:
            errors.append(f"missing-content-ref:{node.node_id}")

    # A course should expose learning structure rather than only assessment nodes.
    if not any(n.node_type == CourseNodeType.LESSON for n in nodes):
        errors.append("course-has-no-lessons")
    if not any(n.node_type == CourseNodeType.TEST for n in nodes):
        warnings.append("course-has-no-test")

    return CourseValidation(not errors, tuple(dict.fromkeys(errors)), tuple(dict.fromkeys(warnings)))
