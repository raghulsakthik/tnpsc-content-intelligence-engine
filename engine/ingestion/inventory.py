"""Normalize Engine 1 resource metadata into an inventory-safe representation.

This stage does not read or mutate source files. It only inventories metadata and
applies the hard PYQ exclusion policy used by downstream processing.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Iterable


@dataclass(frozen=True, slots=True)
class InventoryItem:
    resource_id: str
    source_url: str | None
    source_type: str | None
    source_domain: str | None
    local_path: str | None
    sha256: str | None
    byte_size: int | None
    mime_type: str | None
    validation_status: str | None
    resource_state: str | None
    exam_hint: str | None
    is_pyq: bool
    is_mock: bool
    is_current_affair: bool
    is_government_material: bool
    publication_date: str | None
    content_year: int | None
    eligibility: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _truthy(value: Any) -> bool:
    return value is True or str(value).strip().lower() in {"1", "true", "yes", "y"}


def inventory_records(records: Iterable[dict[str, Any]]) -> list[InventoryItem]:
    """Return deterministic inventory rows without downloading or deleting anything.

    PYQ records are retained in the inventory for audit/coverage reporting but are
    marked ``excluded_pyq`` so later stages cannot accidentally generate content.
    """
    result: list[InventoryItem] = []
    for row in records:
        resource_id = str(row.get("resource_id", "")).strip()
        if not resource_id:
            raise ValueError("resource_id is required")

        is_pyq = _truthy(row.get("is_pyq"))
        result.append(
            InventoryItem(
                resource_id=resource_id,
                source_url=row.get("source_url"),
                source_type=row.get("source_type"),
                source_domain=row.get("source_domain"),
                local_path=row.get("local_path") or row.get("content_reference"),
                sha256=row.get("sha256"),
                byte_size=row.get("byte_size"),
                mime_type=row.get("mime_type"),
                validation_status=row.get("validation_status"),
                resource_state=row.get("resource_state"),
                exam_hint=row.get("exam_hint"),
                is_pyq=is_pyq,
                is_mock=_truthy(row.get("is_mock")),
                is_current_affair=_truthy(row.get("is_current_affair")),
                is_government_material=_truthy(row.get("is_government_material")),
                publication_date=row.get("publication_date"),
                content_year=row.get("content_year"),
                eligibility="excluded_pyq" if is_pyq else "candidate",
            )
        )
    return result
