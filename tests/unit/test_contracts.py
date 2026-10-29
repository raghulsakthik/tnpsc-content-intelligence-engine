from engine.contracts import SourceResource, is_publishable_source


def make_resource(**overrides):
    values = {
        "resource_id": "r1",
        "source_url": "https://example.org/a.pdf",
        "sha256": "a" * 64,
        "byte_size": 100,
        "mime_type": "application/pdf",
        "validation_status": "valid",
    }
    values.update(overrides)
    return SourceResource(**values)


def test_valid_non_pyq_source_is_publishable():
    assert is_publishable_source(make_resource()) is True


def test_pyq_source_is_never_publishable():
    assert is_publishable_source(make_resource(is_pyq=True)) is False


def test_invalid_source_is_not_publishable():
    assert is_publishable_source(make_resource(validation_status="invalid")) is False
