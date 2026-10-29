"""Deterministic, resumable corpus orchestration.

The processor owns orchestration only. Domain stages remain responsible for
content transformation and validation. A completed item is never reprocessed
unless its immutable input fingerprint changes.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Iterable

from .models import BatchItem, BatchManifest, ItemStatus


Stage = Callable[[BatchItem], BatchItem]


class CorpusProcessor:
    """Run a sequence of stages with checkpoint-friendly item state."""

    def __init__(self, stages: Iterable[tuple[str, Stage]]) -> None:
        self._stages = tuple(stages)
        if not self._stages:
            raise ValueError("at least one corpus stage is required")
        names = [name for name, _ in self._stages]
        if len(names) != len(set(names)):
            raise ValueError("stage names must be unique")

    @staticmethod
    def manifest(batch_id: str, items: Iterable[BatchItem], created_at: str) -> BatchManifest:
        ordered = tuple(sorted(items, key=lambda item: item.item_id))
        payload = "\n".join(f"{i.item_id}|{i.resource_id}|{i.sha256}" for i in ordered)
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return BatchManifest(
            batch_id=batch_id,
            item_ids=tuple(i.item_id for i in ordered),
            manifest_hash=digest,
            created_at=created_at,
        )

    def process_item(self, item: BatchItem) -> BatchItem:
        """Process one item from its saved stage; failed stages are resumable."""
        current = item
        if current.status == ItemStatus.COMPLETE:
            return current

        start_index = 0
        if current.stage:
            for index, (name, _) in enumerate(self._stages):
                if name == current.stage:
                    start_index = index
                    break
            else:
                raise ValueError(f"unknown checkpoint stage: {current.stage}")

        for index in range(start_index, len(self._stages)):
            name, stage = self._stages[index]
            try:
                current = stage(
                    BatchItem(
                        item_id=current.item_id,
                        resource_id=current.resource_id,
                        sha256=current.sha256,
                        status=ItemStatus.PROCESSING,
                        attempt=current.attempt + 1,
                        stage=name,
                        error=None,
                        metadata=current.metadata,
                    )
                )
            except Exception as exc:
                return BatchItem(
                    item_id=current.item_id,
                    resource_id=current.resource_id,
                    sha256=current.sha256,
                    status=ItemStatus.FAILED,
                    attempt=current.attempt + 1,
                    stage=name,
                    error=f"{type(exc).__name__}: {exc}",
                    metadata=current.metadata,
                )

        return BatchItem(
            item_id=current.item_id,
            resource_id=current.resource_id,
            sha256=current.sha256,
            status=ItemStatus.COMPLETE,
            attempt=current.attempt,
            stage="complete",
            metadata=current.metadata,
        )
