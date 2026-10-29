"""Stable fingerprints used for idempotent document/chunk processing."""

from hashlib import sha256
import re


def sha256_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def normalized_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text, flags=re.UNICODE)
    return text.strip()


def text_fingerprint(text: str) -> str:
    return sha256(normalized_text(text).encode("utf-8")).hexdigest()
