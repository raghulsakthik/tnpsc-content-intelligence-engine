import hashlib
import json

import pytest

from engine.integration.pipeline import PipelineBoundaryError, RetrievalResource
from engine.integration.retrieval_manifest import (
    build_retrieval_manifest,
    retrieval_manifest_hash,
)


def resource(resource_id="g2-book-001", exam_code="TNPSC_GROUP_2"):
    return RetrievalResource(
        resource_id=resource_id,
        sha256=("a" * 64 if resource_id.endswith("001") else "b" * 64),
        mime_type="application/pdf",
        byte_size=1024,
        source_url="https://example.invalid/source.pdf",
        exam_code=exam_code,
        metadata={"title": "Official study material"},
    )


def test_manifest_is_deterministic_and_sorted():
    first = build_retrieval_manifest(
        manifest_id="batch-1",
        exam_code="TNPSC_GROUP_2",
        resources=[resource("g2-book-002"), resource("g2-book-001")],
    )
    second = build_retrieval_manifest(
        manifest_id="batch-1",
        exam_code="TNPSC_GROUP_2",
        resources=[resource("g2-book-001"), resource("g2-book-002")],
    )
    assert first.manifest_hash == second.manifest_hash
    assert [x["resource_id"] for x in first.resources] == ["g2-book-001", "g2-book-002"]


def test_manifest_hash_matches_canonical_contract():
    manifest = build_retrieval_manifest(
        manifest_id="batch-2",
        exam_code="TNPSC_GROUP_2A",
        resources=[resource("g2a-book-001", "TNPSC_GROUP_2A")],
    )
    expected_payload = {
        "manifest_id": "batch-2",
        "exam_code": "TNPSC_GROUP_2A",
        "resources": list(manifest.resources),
    }
    canonical = json.dumps(expected_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    assert manifest.manifest_hash == hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    assert retrieval_manifest_hash("batch-2", "TNPSC_GROUP_2A", manifest.resources) == manifest.manifest_hash


def test_pyq_resource_is_blocked():
    pyq = RetrievalResource(
        resource_id="pyq-2025",
        sha256="c" * 64,
        mime_type="application/pdf",
        byte_size=100,
        exam_code="TNPSC_GROUP_2",
        is_pyq=True,
    )
    with pytest.raises(PipelineBoundaryError, match="pyq-resource-excluded"):
        build_retrieval_manifest(
            manifest_id="batch-pyq",
            exam_code="TNPSC_GROUP_2",
            resources=[pyq],
        )


def test_mixed_exam_batch_fails_closed():
    with pytest.raises(PipelineBoundaryError, match="resource-exam-mismatch"):
        build_retrieval_manifest(
            manifest_id="batch-mixed",
            exam_code="TNPSC_GROUP_2",
            resources=[resource("g2a-book-001", "TNPSC_GROUP_2A")],
        )


def test_duplicate_sha_fails_closed():
    first = resource("g2-book-001")
    duplicate_sha = RetrievalResource(
        resource_id="g2-book-999",
        sha256=first.sha256,
        mime_type="application/pdf",
        byte_size=100,
        exam_code="TNPSC_GROUP_2",
    )
    with pytest.raises(PipelineBoundaryError, match="duplicate-resource-sha256"):
        build_retrieval_manifest(
            manifest_id="batch-dup",
            exam_code="TNPSC_GROUP_2",
            resources=[first, duplicate_sha],
        )
