"""Deterministic manifest for retrieved TNPSC Group 2/2A resources.

The retrieval engine owns acquisition and immutable source identity. This module
turns the retrieved inventory into a stable batch contract for the content engine
without reading, mutating, uploading, or deleting source files.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Iterable, Mapping

from .pipeline import PipelineBoundaryError, RetrievalResource

SUPPORTED_EXAMS = frozenset({"TNPSC_GROUP_2", "TNPSC_GROUP_2A", "TNPSC_GROUP_2_2A"})


def _canonical(value: object) -> object:
    if isinstance(value, dict):
        return {key: _canonical(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class RetrievalManifest:
    manifest_id: str
    exam_code: str
    resources: tuple[dict[str, object], ...]
    manifest_hash: str

    def as_dict(self) -> dict[str, object]:
        return {
            "manifestId": self.manifest_id,
            "examCode": self.exam_code,
            "resources": [dict(resource) for resource in self.resources],
            "manifestHash": self.manifest_hash,
        }


def retrieval_manifest_hash(
    manifest_id: str,
    exam_code: str,
    resources: Iterable[Mapping[str, object]],
) -> str:
    payload = _canonical(
        {
            "manifest_id": manifest_id,
            "exam_code": exam_code,
            "resources": list(resources),
        }
    )
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def build_retrieval_manifest(
    *,
    manifest_id: str,
    exam_code: str,
    resources: Iterable[RetrievalResource],
) -> RetrievalManifest:
    """Build a stable retrieval batch after validating every resource boundary."""
    manifest_id = manifest_id.strip()
    exam_code = exam_code.strip().upper()
    if not manifest_id:
        raise PipelineBoundaryError("retrieval-manifest-id-required")
    if exam_code not in SUPPORTED_EXAMS:
        raise PipelineBoundaryError(f"unsupported-exam-code:{exam_code}")

    rows: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    seen_hashes: set[str] = set()
    for resource in resources:
        if resource.exam_code and resource.exam_code.strip().upper() != exam_code:
            raise PipelineBoundaryError(f"resource-exam-mismatch:{resource.resource_id}")
        resource.envelope()
        if resource.resource_id in seen_ids:
            raise PipelineBoundaryError(f"duplicate-resource-id:{resource.resource_id}")
        if resource.sha256 in seen_hashes:
            raise PipelineBoundaryError(f"duplicate-resource-sha256:{resource.resource_id}")
        seen_ids.add(resource.resource_id)
        seen_hashes.add(resource.sha256)
        rows.append(
            {
                "resource_id": resource.resource_id,
                "sha256": resource.sha256,
                "mime_type": resource.mime_type,
                "byte_size": resource.byte_size,
                "source_url": resource.source_url,
                "local_path": resource.local_path,
                "exam_code": exam_code,
                "metadata": dict(resource.metadata or {}),
            }
        )

    if not rows:
        raise PipelineBoundaryError("retrieval-manifest-empty")

    rows.sort(key=lambda row: (str(row["resource_id"]), str(row["sha256"])))
    digest = retrieval_manifest_hash(manifest_id, exam_code, rows)
    return RetrievalManifest(manifest_id, exam_code, tuple(rows), digest)
