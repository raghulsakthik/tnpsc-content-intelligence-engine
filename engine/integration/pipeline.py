"""Idempotent orchestration boundary between retrieval and content processing."""

from dataclasses import dataclass
from .models import IngestionEnvelope, IngestionStatus


@dataclass(frozen=True, slots=True)
class IntegrationResult:
    resource_id: str
    status: IngestionStatus
    reason: str = ""


class IntegrationPipeline:
    """Accept validated Engine 1 resources without owning downloading."""

    def ingest(self, envelope: IngestionEnvelope) -> IntegrationResult:
        if not envelope.is_valid():
            return IntegrationResult(envelope.resource_id, IngestionStatus.FAILED, "invalid-ingestion-envelope")
        if envelope.is_pyq:
            return IntegrationResult(envelope.resource_id, IngestionStatus.EXCLUDED_PYQ, "pyq-content-is-never-processable")
        return IntegrationResult(envelope.resource_id, IngestionStatus.RECEIVED, "accepted-for-processing")
