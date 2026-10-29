from engine.document_ir.fingerprint import normalized_text, text_fingerprint
from engine.document_ir.models import Document, DocumentBlock, DocumentChunk, DocumentPage, DocumentVersion


def test_document_source_identity_is_preserved():
    document = Document(
        document_id="doc-1",
        resource_id="resource-10",
        sha256="abc123",
        source_url="https://example.test/a.pdf",
        mime_type="application/pdf",
        byte_size=100,
    )
    assert document.resource_id == "resource-10"
    assert document.sha256 == "abc123"


def test_ir_chain_preserves_provenance_ids():
    version = DocumentVersion("doc-1", "v1", "pdf-text-1", "hash", "2026-10-29T00:00:00Z")
    page = DocumentPage("page-1", version.version_id, 1, text="Tamil Nadu")
    block = DocumentBlock("block-1", page.page_id, "paragraph", 0, "Tamil Nadu")
    chunk = DocumentChunk("chunk-1", version.version_id, (block.block_id,), "Tamil Nadu", 0, text_fingerprint("Tamil Nadu"))
    assert page.version_id == version.version_id
    assert block.page_id == page.page_id
    assert chunk.block_ids == (block.block_id,)


def test_text_fingerprint_normalizes_whitespace():
    assert normalized_text("A   B\nC") == "A B C"
    assert text_fingerprint("A B") == text_fingerprint("A   B")
