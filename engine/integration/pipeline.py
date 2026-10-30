"""Idempotent retrieval -> content-engine -> publication orchestration boundary.

Retrieval owns acquisition; the content engine owns transformation and approval;
the platform owns review and publication. This module never writes to the
platform database.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .models import IngestionEnvelope, IngestionStatus
from .publication import PublicationPackage, build_publication_package
from ..lessons.models import Lesson
from ..mcq.models import MCQ


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


class PipelineBoundaryError(ValueError):
    """Raised when a retrieval resource cannot safely enter publication."""


@dataclass(frozen=True, slots=True)
class RetrievalResource:
    """Minimum Engine 1 contract required by publication preparation."""

    resource_id: str
    sha256: str
    mime_type: str
    byte_size: int
    source_url: str | None = None
    local_path: str | None = None
    exam_code: str | None = None
    is_pyq: bool = False
    metadata: Mapping[str, object] | None = None

    def envelope(self) -> IngestionEnvelope:
        envelope = IngestionEnvelope(
            resource_id=self.resource_id,
            sha256=self.sha256,
            source_url=self.source_url,
            mime_type=self.mime_type,
            byte_size=self.byte_size,
            local_path=self.local_path,
            exam_code=self.exam_code,
            is_pyq=self.is_pyq,
            metadata=dict(self.metadata or {}),
        )
        if not envelope.is_valid():
            raise PipelineBoundaryError(f"invalid-resource:{self.resource_id}")
        if envelope.is_pyq:
            raise PipelineBoundaryError(f"pyq-resource-excluded:{self.resource_id}")
        return envelope


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """Auditable result of one deterministic publication preparation run."""

    publication: PublicationPackage
    resource_ids: tuple[str, ...]
    resource_sha256: tuple[str, ...]


def prepare_publication(
    *,
    publication_id: str,
    resources: Iterable[RetrievalResource],
    lessons: Iterable[Lesson] = (),
    mcqs: Iterable[MCQ] = (),
    topic_map: Mapping[str, str],
) -> PipelineResult:
    """Validate retrieved resources and create the platform publication package.

    Content is not generated here. Lessons/MCQs must already be produced by the
    engine's extraction/evidence/generation/validation stages.
    """
    resource_list = list(resources)
    if not resource_list:
        raise PipelineBoundaryError("retrieval-resources-required")

    envelopes = [resource.envelope() for resource in resource_list]
    ids = tuple(envelope.resource_id for envelope in envelopes)
    hashes = tuple(envelope.sha256 for envelope in envelopes)

    if len(set(ids)) != len(ids):
        raise PipelineBoundaryError("duplicate-resource-id")
    if len(set(hashes)) != len(hashes):
        raise PipelineBoundaryError("duplicate-resource-sha256")

    publication = build_publication_package(
        publication_id=publication_id,
        lessons=lessons,
        mcqs=mcqs,
        topic_map=topic_map,
    )
    return PipelineResult(publication, ids, hashes)
