from dataclasses import replace

import pytest

from engine.integration import PipelineBoundaryError, RetrievalResource, prepare_publication
from engine.lessons.builder import build_lesson
from engine.lessons.models import LessonStatus


def _resource(resource_id="g2-source-001", sha256="a" * 64, is_pyq=False):
    return RetrievalResource(
        resource_id=resource_id,
        sha256=sha256,
        mime_type="application/pdf",
        byte_size=1024,
        source_url="https://example.test/source.pdf",
        exam_code="TNPSC_GROUP_2",
        is_pyq=is_pyq,
    )


def _approved_lesson():
    draft = build_lesson(
        curriculum_node_id="aptitude.number-system",
        title="Number System",
        concept="Numbers and their properties",
        definition="A number represents a quantity.",
        explanation="Basic number-system concepts.",
        source_ids=["g2-source-001"],
    )
    return replace(draft, status=LessonStatus.APPROVED)


def test_retrieval_resource_flows_into_publication():
    result = prepare_publication(
        publication_id="pub-g2-001",
        resources=[_resource()],
        lessons=[_approved_lesson()],
        topic_map={"aptitude.number-system": "aptitude.number-system"},
    )
    assert result.resource_ids == ("g2-source-001",)
    assert result.publication.items[0]["topic_id"] == "aptitude.number-system"
    assert result.publication.manifest_hash


def test_pyq_resource_is_blocked_before_publication():
    with pytest.raises(PipelineBoundaryError, match="pyq-resource-excluded"):
        prepare_publication(
            publication_id="pub-pyq-001",
            resources=[_resource(is_pyq=True)],
            lessons=[_approved_lesson()],
            topic_map={"aptitude.number-system": "aptitude.number-system"},
        )


def test_duplicate_resource_id_fails_closed():
    with pytest.raises(PipelineBoundaryError, match="duplicate-resource-id"):
        prepare_publication(
            publication_id="pub-duplicate-001",
            resources=[_resource(), _resource(sha256="b" * 64)],
            lessons=[_approved_lesson()],
            topic_map={"aptitude.number-system": "aptitude.number-system"},
        )


def test_duplicate_resource_hash_fails_closed():
    with pytest.raises(PipelineBoundaryError, match="duplicate-resource-sha256"):
        prepare_publication(
            publication_id="pub-duplicate-002",
            resources=[_resource("g2-source-001"), _resource("g2-source-002")],
            lessons=[_approved_lesson()],
            topic_map={"aptitude.number-system": "aptitude.number-system"},
        )
