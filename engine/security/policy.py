"""Fail-closed security policy for acquisition and content processing.

The policy is intentionally dependency-light so it can be reused by Engine 1
and Engine 2 without coupling security decisions to a web client or LLM.
"""

from dataclasses import dataclass
import ipaddress
import posixpath
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class SecurityPolicy:
    allowed_schemes: tuple[str, ...] = ("https", "http")
    max_archive_member_bytes: int = 100 * 1024 * 1024
    max_archive_members: int = 10_000
    max_path_length: int = 240


def validate_external_url(url: str, policy: SecurityPolicy | None = None) -> None:
    """Reject malformed, local, private, loopback, or unsupported URLs.

    DNS resolution is deliberately left to the HTTP layer, which must resolve
    and validate the destination IP immediately before connecting as well.
    """
    cfg = policy or SecurityPolicy()
    parsed = urlparse(url)
    if parsed.scheme.lower() not in cfg.allowed_schemes:
        raise ValueError("unsupported URL scheme")
    if not parsed.hostname:
        raise ValueError("URL hostname is required")
    host = parsed.hostname.strip().lower()
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".localhost"):
        raise ValueError("local hostname is blocked")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    if address is not None and (
        address.is_private or address.is_loopback or address.is_link_local
        or address.is_multicast or address.is_reserved or address.is_unspecified
    ):
        raise ValueError("private or non-public IP address is blocked")


def validate_archive_member(name: str, size: int, policy: SecurityPolicy | None = None) -> None:
    """Reject ZIP path traversal and oversized archive members."""
    cfg = policy or SecurityPolicy()
    if not name or len(name) > cfg.max_path_length:
        raise ValueError("invalid archive member path")
    normalized = posixpath.normpath(name.replace("\\", "/"))
    if normalized.startswith("/") or normalized == ".." or normalized.startswith("../"):
        raise ValueError("archive path traversal detected")
    if size < 0 or size > cfg.max_archive_member_bytes:
        raise ValueError("archive member exceeds size limit")
