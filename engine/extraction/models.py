"""Contracts for deterministic document extraction."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ExtractionMethod(StrEnum):
    NATIVE_TEXT = "native_text"
    OCR = "ocr"
    HYBRID = "hybrid"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True, slots=True)
class PageExtraction:
    page_number: int
    text: str
    method: ExtractionMethod
    text_char_count: int
    image_only: bool = False
    quality: float | None = None
    warnings: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ExtractionResult:
    method: ExtractionMethod
    pages: tuple[PageExtraction, ...]
    extractor_name: str
    extractor_version: str
    source_sha256: str
    warnings: tuple[str, ...] = ()

    @property
    def page_count(self) -> int:
        return len(self.pages)

    @property
    def text(self) -> str:
        return "\n\n".join(page.text for page in self.pages if page.text)
