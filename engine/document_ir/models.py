"""Canonical intermediate representation for source documents.

The IR preserves provenance while allowing extraction/cleaning stages to create
new derived representations without mutating the immutable source record.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Document:
    document_id: str
    resource_id: str
    sha256: str
    source_url: str | None
    mime_type: str
    byte_size: int
    language_hint: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DocumentVersion:
    document_id: str
    version_id: str
    extraction_version: str
    content_hash: str
    created_at: str
    status: str = "created"


@dataclass(frozen=True)
class DocumentPage:
    page_id: str
    version_id: str
    page_number: int
    width: float | None = None
    height: float | None = None
    text: str = ""
    extraction_quality: float | None = None


@dataclass(frozen=True)
class DocumentBlock:
    block_id: str
    page_id: str
    block_type: str
    ordinal: int
    text: str
    bbox: tuple[float, float, float, float] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    version_id: str
    block_ids: tuple[str, ...]
    text: str
    ordinal: int
    content_hash: str
    metadata: dict[str, Any] = field(default_factory=dict)
