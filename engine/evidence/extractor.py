"""Deterministic evidence extraction from document chunks.

This layer never invents evidence. It only records text that already exists in
an extracted document and its exact source coordinates.
"""

from collections.abc import Iterable
from uuid import uuid5, NAMESPACE_URL

from engine.document_ir.models import DocumentChunk, DocumentPage

from .models import Evidence, EvidenceSpan, EvidenceType


def _evidence_id(document_id: str, version_id: str, page_id: str, text: str) -> str:
    return str(uuid5(NAMESPACE_URL, f"{document_id}:{version_id}:{page_id}:{text}"))


def extract_evidence(
    *,
    document_id: str,
    version_id: str,
    source_sha256: str | None,
    pages: Iterable[DocumentPage],
    chunks: Iterable[DocumentChunk] = (),
) -> tuple[Evidence, ...]:
    """Create provenance records for non-empty page/chunk text.

    Page evidence remains available even when no chunking was performed.
    Chunk evidence additionally carries a chunk coordinate. The function is
    intentionally deterministic so reruns produce the same evidence IDs.
    """
    results: list[Evidence] = []
    page_by_id = {page.page_id: page for page in pages}

    for page in page_by_id.values():
        text = page.text.strip()
        if not text:
            continue
        results.append(
            Evidence(
                evidence_id=_evidence_id(document_id, version_id, page.page_id, text),
                document_id=document_id,
                version_id=version_id,
                page_id=page.page_id,
                chunk_id=None,
                page_number=page.page_number,
                evidence_type=EvidenceType.TEXT,
                text=text,
                span=EvidenceSpan(0, len(text), text),
                source_sha256=source_sha256,
            )
        )

    for chunk in chunks:
        if not chunk.text.strip():
            continue
        for block_id in chunk.block_ids:
            page = next((p for p in page_by_id.values() if p.page_id == block_id), None)
            if page is not None:
                page_id = page.page_id
                page_number = page.page_number
                break
        else:
            # Blocks are not pages; the first chunk-linked page must be supplied
            # by metadata when the chunk does not expose a page object directly.
            page_id = str(chunk.metadata.get("page_id", "unknown"))
            page_number = int(chunk.metadata.get("page_number", 0))

        results.append(
            Evidence(
                evidence_id=_evidence_id(document_id, version_id, page_id, chunk.text),
                document_id=document_id,
                version_id=version_id,
                page_id=page_id,
                chunk_id=chunk.chunk_id,
                page_number=page_number,
                evidence_type=EvidenceType.TEXT,
                text=chunk.text.strip(),
                span=EvidenceSpan(0, len(chunk.text.strip()), chunk.text.strip()),
                source_sha256=source_sha256,
                metadata={"ordinal": chunk.ordinal},
            )
        )

    return tuple(results)
