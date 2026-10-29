"""Persistent-safe models for resumable corpus processing."""

from dataclasses import dataclass, field
from enum import StrEnum


class BatchStatus(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETE = "complete"
    FAILED = "failed"


class ItemStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETE = "complete"
    SKIPPED = "skipped"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class BatchItem:
    item_id: str
    resource_id: str
    sha256: str
    status: ItemStatus = ItemStatus.PENDING
    attempt: int = 0
    stage: str = "registration"
    error: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class BatchManifest:
    batch_id: str
    item_ids: tuple[str, ...]
    manifest_hash: str
    created_at: str
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CorpusRun:
    run_id: str
    batch_id: str
    status: BatchStatus
    completed_items: int = 0
    failed_items: int = 0
    skipped_items: int = 0
    checkpoint: str | None = None
