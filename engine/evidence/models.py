"""Immutable provenance models for content evidence."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class EvidenceType(StrEnum):
    TEXT = "text"
    HEADING = "heading"
    TABLE = "table"
    LIST = "list"
    CLASSIFICATION = "classification"
    SOURCE_METADATA = "source_metadata"


@dataclass(frozen=True, slots=True)
class EvidenceSpan:
    """A precise span within a source chunk."""

    start: int
    end: int
    quote: str

    def __post_init__(self) -> None:
        if self.start < 0 or self.end < self.start:
            raise ValueError("invalid evidence span")
        if not self.quote and self.end > self.start:
            raise ValueError("non-empty span requires quote")


@dataclass(frozen=True, slots=True)
class Evidence:
    """Evidence tied back to immutable document coordinates."""

    evidence_id: str
    document_id: str
    version_id: str
    page_id: str
    chunk_id: str | None
    page_number: int
    evidence_type: EvidenceType
    text: str
    span: EvidenceSpan | None = None
    source_sha256: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def coordinate(self) -> str:
        chunk = self.chunk_id or "-"
        return f"{self.document_id}:{self.version_id}:p{self.page_number}:c{chunk}"
