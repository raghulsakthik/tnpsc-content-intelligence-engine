import pytest

from engine.security.policy import validate_archive_member, validate_external_url


def test_public_https_url_is_allowed():
    validate_external_url("https://example.com/material.pdf")


@pytest.mark.parametrize("url", [
    "file:///etc/passwd",
    "http://localhost:8787/health",
    "http://127.0.0.1/file",
    "http://10.0.0.5/file",
    "http://169.254.169.254/latest/meta-data",
])
def test_unsafe_urls_are_blocked(url):
    with pytest.raises(ValueError):
        validate_external_url(url)


def test_archive_traversal_is_blocked():
    with pytest.raises(ValueError):
        validate_archive_member("../../etc/passwd", 100)


def test_archive_member_size_is_limited():
    with pytest.raises(ValueError):
        validate_archive_member("material.pdf", 101 * 1024 * 1024)


def test_normal_archive_member_is_allowed():
    validate_archive_member("nested/material.pdf", 1024)
