"""Contracts for exposing approved content to the TNPSC platform.

The platform layer is intentionally read/publication oriented. It must not
approve, mutate, or silently rewrite content owned by the intelligence engine.
"""

from dataclasses import dataclass, field
from enum import StrEnum


class PlatformPublicationStatus(StrEnum):
    READY = "ready"
    PUBLISHED = "published"
    SUPERSEDED = "superseded"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class PlatformContentRef:
    content_id: str
    content_type: str
    version: int
    curriculum_node_id: str
    source_ids: tuple[str, ...] = ()
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PlatformCourseRef:
    course_id: str
    version: int
    exam_code: str
    curriculum_version_id: str
    manifest_hash: str
    content_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class PublicationEnvelope:
    publication_id: str
    course: PlatformCourseRef
    contents: tuple[PlatformContentRef, ...]
    status: PlatformPublicationStatus = PlatformPublicationStatus.READY

    def is_publishable(self) -> bool:
        if self.status != PlatformPublicationStatus.READY:
            return False
        if not self.course.manifest_hash:
            return False
        return all(item.source_ids for item in self.contents)
