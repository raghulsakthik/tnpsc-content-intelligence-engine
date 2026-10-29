from engine.classification.classifier import classify_text
from engine.classification.models import ClassificationStatus


def test_general_studies_classifies_to_polity():
    result = classify_text(
        "General Studies. Indian Polity and Constitution. Fundamental Rights. "
        "This study material explains the Constitution of India."
    )
    assert result.subject == "general-studies"
    assert result.unit == "indian-polity"
    assert result.is_pyq is False
    assert result.status == ClassificationStatus.CLASSIFIED


def test_tamil_mock_is_mock_and_reviewable():
    result = classify_text("பொது தமிழ் - இலக்கணம் - மாதிரி தேர்வு")
    assert result.subject == "general-tamil"
    assert result.is_mock is True
    assert result.content_type == "mock_test"
    assert result.status == ClassificationStatus.CLASSIFIED


def test_current_affairs_is_flagged():
    result = classify_text("October 2026 Daily Current Affairs and practice MCQs")
    assert result.is_current_affair is True
    assert result.content_type == "current_affairs"


def test_pyq_is_hard_excluded():
    result = classify_text("TNPSC Group 2 Previous Year Question Paper 2024")
    assert result.is_pyq is True
    assert result.status == ClassificationStatus.EXCLUDED_PYQ
    assert result.publishable is False


def test_unknown_material_requires_review():
    result = classify_text("A generic document without curriculum identifiers")
    assert result.status == ClassificationStatus.REVIEW_REQUIRED
    assert result.publishable is False


def test_government_material_is_labeled():
    result = classify_text("Tamil Nadu Government official study material on geography")
    assert result.is_government_material is True
    assert result.subject == "general-studies"
    assert result.unit == "geography"
