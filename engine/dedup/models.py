"""Models for non-destructive duplicate and conflict detection."""

from dataclasses import dataclass, field
from enum import StrEnum


class DuplicateKind(StrEnum):
    EXACT_RESOURCE = "exact_resource"
    EXACT_TEXT = "exact_text"
    NORMALIZED_TEXT = "normalized_text"
    POSSIBLE_SEMANTIC = "possible_semantic"


class ConflictKind(StrEnum):
    CONTENT_VALUE = "content_value"
    CURRICULUM_MAPPING = "curriculum_mapping"
    PUBLICATION_DATE = "publication_date"
    SOURCE_METADATA = "source_metadata"


@dataclass(frozen=True, slots=True)
class DuplicateCandidate:
    left_id: str
    right_id: str
    kind: DuplicateKind
    similarity: float
    evidence: tuple[str, ...] = ()
    review_required: bool = True


@dataclass(frozen=True, slots=True)
class ConflictCandidate:
    left_id: str
    right_id: str
    kind: ConflictKind
    left_value: str
    right_value: str
    evidence: tuple[str, ...] = ()
    review_required: bool = True


@dataclass(frozen=True, slots=True)
class DeduplicationResult:
    duplicates: tuple[DuplicateCandidate, ...] = ()
    conflicts: tuple[ConflictCandidate, ...] = ()
    metadata: dict[str, object] = field(default_factory=dict)
