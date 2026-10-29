"""Build a platform-safe publication envelope from approved course content."""

from __future__ import annotations

import hashlib

from engine.courses.models import Course, CourseNode
from engine.platform.models import (
    PlatformContentRef,
    PlatformCourseRef,
    PublicationEnvelope,
)


def publication_id(course_id: str, version: int, manifest_hash: str) -> str:
    value = f"{course_id}|{version}|{manifest_hash}"
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]


def build_publication(
    *,
    course: Course,
    manifest_hash: str,
    nodes: list[CourseNode],
    approved_content_ids: set[str],
    source_ids_by_content: dict[str, tuple[str, ...]],
) -> PublicationEnvelope:
    """Create a publication boundary without changing the source content.

    Only nodes with approved content references are emitted. Missing approval,
    provenance, or manifest identity results in a non-publishable envelope.
    """
    refs: list[PlatformContentRef] = []
    for node in sorted(nodes, key=lambda item: (item.ordinal, item.node_id)):
        if not node.content_ref:
            continue
        if node.content_ref not in approved_content_ids:
            continue
        sources = source_ids_by_content.get(node.content_ref, ())
        refs.append(
            PlatformContentRef(
                content_id=node.content_ref,
                content_type=node.node_type.value,
                version=course.version,
                curriculum_node_id=node.metadata.get("curriculum_node_id", ""),
                source_ids=tuple(dict.fromkeys(sources)),
            )
        )

    course_ref = PlatformCourseRef(
        course_id=course.course_id,
        version=course.version,
        exam_code=course.exam_code,
        curriculum_version_id=course.curriculum_version_id,
        manifest_hash=manifest_hash,
        content_refs=tuple(item.content_id for item in refs),
    )
    return PublicationEnvelope(
        publication_id=publication_id(course.course_id, course.version, manifest_hash),
        course=course_ref,
        contents=tuple(refs),
    )
