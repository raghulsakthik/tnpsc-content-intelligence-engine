"""Phase-0 contracts shared by pipeline stages.

These are deliberately small and dependency-free. Physical persistence models are
introduced after the contract tests are established.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class SourceResource:
    resource_id: str
    source_url: str
    sha256: str
    byte_size: int
    mime_type: str
    validation_status: str
    is_pyq: bool = False
    is_mock: bool = False
    is_current_affair: bool = False
    is_government_material: bool = False
    publication_date: Optional[datetime] = None
    content_year: Optional[int] = None


@dataclass(frozen=True)
class EvidenceRef:
    document_id: str
    page_number: Optional[int]
    block_id: Optional[str]
    source_resource_id: str


@dataclass(frozen=True)
class ContentIdentity:
    exam: str
    subject: str
    unit: str
    topic: str
    subtopic: Optional[str]
    language: str
    content_type: str


def is_publishable_source(resource: SourceResource) -> bool:
    """Return whether a source may enter generated-content stages."""
    return (
        resource.validation_status == "valid"
        and not resource.is_pyq
    )
