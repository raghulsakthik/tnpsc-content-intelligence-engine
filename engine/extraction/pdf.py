"""PDF extraction adapter with a native-text first strategy.

The adapter intentionally keeps OCR behind a separate interface. It detects
pages that are effectively image-only instead of silently treating them as
successfully extracted text.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Protocol

from .models import ExtractionMethod, ExtractionResult, PageExtraction


class PdfBackend(Protocol):
    def page_count(self, path: Path) -> int: ...

    def page_text(self, path: Path, page_number: int) -> str: ...


class NativePdfExtractor:
    """Backend-neutral native PDF extractor.

    A concrete PDF library can implement PdfBackend without changing the
    content-engine contracts. This avoids coupling curriculum logic to a PDF
    implementation.
    """

    def __init__(self, backend: PdfBackend, *, version: str = "native-pdf-v1") -> None:
        self.backend = backend
        self.version = version

    def extract(self, path: str | Path) -> ExtractionResult:
        source = Path(path)
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        pages: list[PageExtraction] = []
        warnings: list[str] = []

        for number in range(1, self.backend.page_count(source) + 1):
            text = self.backend.page_text(source, number) or ""
            stripped = text.strip()
            image_only = len(stripped) < 20
            page_warnings = ("ocr_required",) if image_only else ()
            pages.append(
                PageExtraction(
                    page_number=number,
                    text=text,
                    method=ExtractionMethod.NATIVE_TEXT,
                    text_char_count=len(text),
                    image_only=image_only,
                    quality=None if image_only else 1.0,
                    warnings=page_warnings,
                )
            )
            if image_only:
                warnings.append(f"page_{number}:ocr_required")

        method = ExtractionMethod.OCR if pages and all(p.image_only for p in pages) else ExtractionMethod.HYBRID if any(p.image_only for p in pages) else ExtractionMethod.NATIVE_TEXT
        return ExtractionResult(
            method=method,
            pages=tuple(pages),
            extractor_name="native-pdf",
            extractor_version=self.version,
            source_sha256=digest,
            warnings=tuple(warnings),
        )
