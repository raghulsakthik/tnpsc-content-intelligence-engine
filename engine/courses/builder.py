"""Deterministic construction and validation of course manifests."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable

from .models import Course, CourseManifest, CourseNode, CourseNodeType


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def course_id(exam_code: str, title: str, version: int = 1) -> str:
    key = f"{exam_code}|{_clean(title).lower()}|{version}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]


def build_course(
    *,
    exam_code: str,
    curriculum_version_id: str,
    title: str,
    description: str = "",
    version: int = 1,
) -> Course:
    """Create a draft course. It never publishes content."""
    return Course(
        course_id=course_id(exam_code, title, version),
        exam_code=exam_code,
        curriculum_version_id=curriculum_version_id,
        title=_clean(title),
        description=_clean(description),
        version=version,
    )


def build_node(
    *,
    course_id_value: str,
    node_type: CourseNodeType,
    title: str,
    ordinal: int,
    parent_id: str | None = None,
    content_ref: str | None = None,
    required: bool = True,
) -> CourseNode:
    """Build a deterministic node identity from its stable structural inputs."""
    key = f"{course_id_value}|{node_type}|{ordinal}|{_clean(title).lower()}|{parent_id or ''}"
    node_id = hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]
    return CourseNode(
        node_id=node_id,
        course_id=course_id_value,
        node_type=node_type,
        title=_clean(title),
        ordinal=ordinal,
        parent_id=parent_id,
        content_ref=content_ref,
        required=required,
    )


def build_manifest(course: Course, nodes: Iterable[CourseNode]) -> CourseManifest:
    """Create a stable manifest and reject malformed course trees."""
    ordered = tuple(sorted(nodes, key=lambda n: (n.ordinal, n.node_id)))
    if any(node.course_id != course.course_id for node in ordered):
        raise ValueError("course node belongs to another course")
    ids = {node.node_id for node in ordered}
    for node in ordered:
        if node.parent_id and node.parent_id not in ids:
            raise ValueError(f"missing parent for node {node.node_id}")
    refs = tuple(dict.fromkeys(node.content_ref for node in ordered if node.content_ref))
    digest_input = "\n".join(
        f"{n.node_id}|{n.node_type}|{n.title}|{n.ordinal}|{n.parent_id or ''}|{n.content_ref or ''}"
        for n in ordered
    )
    content_hash = hashlib.sha256(digest_input.encode("utf-8")).hexdigest()
    return CourseManifest(
        course_id=course.course_id,
        version=course.version,
        node_ids=tuple(n.node_id for n in ordered),
        required_content_refs=refs,
        curriculum_version_id=course.curriculum_version_id,
        content_hash=content_hash,
    )
