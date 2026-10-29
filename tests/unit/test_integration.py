from engine.integration.gaps import CurriculumGap, rank_gaps
from engine.integration.models import IngestionEnvelope, IngestionStatus
from engine.integration.pipeline import IntegrationPipeline


def envelope(**kwargs):
    values = dict(resource_id="r1", sha256="abc", source_url="https://example.test/a.pdf", mime_type="application/pdf", byte_size=100)
    values.update(kwargs)
    return IngestionEnvelope(**values)


def test_valid_resource_is_accepted():
    result = IntegrationPipeline().ingest(envelope())
    assert result.status == IngestionStatus.RECEIVED


def test_pyq_is_hard_excluded():
    result = IntegrationPipeline().ingest(envelope(is_pyq=True))
    assert result.status == IngestionStatus.EXCLUDED_PYQ


def test_invalid_resource_is_rejected():
    result = IntegrationPipeline().ingest(envelope(sha256=""))
    assert result.status == IngestionStatus.FAILED


def test_gap_ranking_is_deterministic():
    gaps = [CurriculumGap("b", "missing", 1), CurriculumGap("a", "missing", 2)]
    assert [g.curriculum_node_id for g in rank_gaps(gaps)] == ["a", "b"]
