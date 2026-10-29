from pathlib import Path

from engine.extraction.models import ExtractionMethod
from engine.extraction.pdf import NativePdfExtractor
from engine.extraction.pipeline import ExtractionPipeline


class FakePdfBackend:
    def __init__(self, pages: list[str]):
        self.pages = pages

    def page_count(self, path: Path) -> int:
        return len(self.pages)

    def page_text(self, path: Path, page_number: int) -> str:
        return self.pages[page_number - 1]


def test_native_extraction_preserves_page_boundaries(tmp_path):
    source = tmp_path / "sample.pdf"
    source.write_bytes(b"fake-pdf-content")
    extractor = NativePdfExtractor(FakePdfBackend(["General Studies science", "Indian polity and constitution"]))

    result = ExtractionPipeline(extractor).run(str(source))

    assert result.method is ExtractionMethod.NATIVE_TEXT
    assert result.page_count == 2
    assert result.pages[0].page_number == 1
    assert result.pages[1].page_number == 2
    assert result.pages[0].text == "General Studies science"
    assert result.warnings == ()


def test_image_only_pages_are_marked_for_ocr(tmp_path):
    source = tmp_path / "scan.pdf"
    source.write_bytes(b"fake-scan")
    extractor = NativePdfExtractor(FakePdfBackend(["", "tiny"]))

    result = ExtractionPipeline(extractor).run(str(source))

    assert result.method is ExtractionMethod.OCR
    assert all(page.image_only for page in result.pages)
    assert "page_1:ocr_required" in result.warnings


def test_mixed_pdf_uses_hybrid_signal(tmp_path):
    source = tmp_path / "mixed.pdf"
    source.write_bytes(b"mixed")
    extractor = NativePdfExtractor(FakePdfBackend(["A sufficiently long native text page for extraction", ""]))

    result = ExtractionPipeline(extractor).run(str(source))

    assert result.method is ExtractionMethod.HYBRID
    assert result.pages[1].image_only is True
