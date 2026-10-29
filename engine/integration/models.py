"""Stable boundary models for Engine 1 -> Engine 2 ingestion."""

from dataclasses import dataclass, field
from enum import StrEnum


class IngestionStatus(StrEnum):
    RECEIVED = "received"
    ELIGIBLE = "eligible"
    EXCLUDED_PYQ = "excluded_pyq"
    PROCESSING = "processing"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class IngestionEnvelope:
    resource_id: str
    sha256: str
    source_url: str | None
    mime_type: str
    byte_size: int
    local_path: str | None = None
    exam_code: str | None = None
    is_pyq: bool = False
    metadata: dict[str, object] = field(default_factory=dict)

    def status(self) -> IngestionStatus:
        return IngestionStatus.EXCLUDED_PYQ if self.is_pyq else IngestionStatus.ELIGIBLE

    def is_valid(self) -> bool:
        return bool(self.resource_id and self.sha256 and self.mime_type and self.byte_size >= 0)
