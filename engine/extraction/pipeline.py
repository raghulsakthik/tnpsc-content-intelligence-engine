"""Extraction orchestration and IR conversion."""

from __future__ import annotations

from .models import ExtractionResult


class ExtractionPipeline:
    """Convert an extraction result into the Phase-3 document IR shape."""

    def __init__(self, extractor) -> None:
        self.extractor = extractor

    def run(self, path: str) -> ExtractionResult:
        result = self.extractor.extract(path)
        self._validate(result)
        return result

    @staticmethod
    def _validate(result: ExtractionResult) -> None:
        if not result.source_sha256:
            raise ValueError("extraction result is missing source SHA-256")
        expected = list(range(1, result.page_count + 1))
        actual = [page.page_number for page in result.pages]
        if actual != expected:
            raise ValueError("extracted pages must be contiguous and 1-based")
        for page in result.pages:
            if page.text_char_count != len(page.text):
                raise ValueError(f"page {page.page_number} has inconsistent text length")
