from engine.document_ir.models import DocumentChunk, DocumentPage
from engine.evidence.extractor import extract_evidence


def test_page_evidence_preserves_coordinates_and_is_deterministic() -> None:
    pages = [DocumentPage(page_id="p1", version_id="v1", page_number=1, text="Indian Polity")]

    first = extract_evidence(
        document_id="doc-1",
        version_id="v1",
        source_sha256="abc123",
        pages=pages,
    )
    second = extract_evidence(
        document_id="doc-1",
        version_id="v1",
        source_sha256="abc123",
        pages=pages,
    )

    assert first == second
    assert first[0].coordinate() == "doc-1:v1:p1:c-"
    assert first[0].span is not None
    assert first[0].span.quote == "Indian Polity"


def test_chunk_evidence_retains_chunk_identity() -> None:
    pages = [DocumentPage(page_id="p1", version_id="v1", page_number=3, text="Topic")]
    chunk = DocumentChunk(
        chunk_id="chunk-1",
        version_id="v1",
        block_ids=("block-1",),
        text="Fundamental Rights",
        ordinal=0,
        content_hash="hash",
        metadata={"page_id": "p1", "page_number": 3},
    )

    evidence = extract_evidence(
        document_id="doc-1",
        version_id="v1",
        source_sha256="abc123",
        pages=pages,
        chunks=[chunk],
    )

    chunk_evidence = evidence[1]
    assert chunk_evidence.chunk_id == "chunk-1"
    assert chunk_evidence.page_id == "p1"
    assert chunk_evidence.page_number == 3
    assert chunk_evidence.text == "Fundamental Rights"


def test_empty_pages_and_chunks_produce_no_evidence() -> None:
    pages = [DocumentPage(page_id="p1", version_id="v1", page_number=1, text="")]
    assert extract_evidence(document_id="d", version_id="v", source_sha256=None, pages=pages) == ()
