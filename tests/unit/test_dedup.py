from engine.dedup.detector import DeduplicationDetector
from engine.dedup.models import DuplicateKind


def test_sha256_duplicate_is_exact_resource_candidate():
    detector = DeduplicationDetector()
    result = detector.compare_resources("a", "same", "alpha", "b", "same", "different")
    assert result[0].kind == DuplicateKind.EXACT_RESOURCE
    assert result[0].review_required


def test_normalized_text_duplicate_is_detected():
    detector = DeduplicationDetector()
    result = detector.compare_resources("a", "1", "Hello   World", "b", "2", " hello world ")
    assert result[0].kind == DuplicateKind.NORMALIZED_TEXT


def test_different_content_is_not_duplicate():
    detector = DeduplicationDetector(semantic_candidate_threshold=1.01)
    assert detector.compare_resources("a", "1", "Indian polity parliament", "b", "2", "organic chemistry atoms") == ()


def test_possible_semantic_match_never_auto_merges():
    detector = DeduplicationDetector(semantic_candidate_threshold=0.5)
    result = detector.compare_resources("a", "1", "Indian parliament and constitution", "b", "2", "Indian constitution parliament")
    assert result
    assert result[0].kind == DuplicateKind.POSSIBLE_SEMANTIC
    assert result[0].review_required


def test_many_comparison_is_pairwise():
    detector = DeduplicationDetector()
    result = detector.compare_many([
        {"id": "a", "sha256": "x", "text": "same"},
        {"id": "b", "sha256": "x", "text": "other"},
        {"id": "c", "sha256": "y", "text": "same"},
    ])
    assert len(result) == 2
