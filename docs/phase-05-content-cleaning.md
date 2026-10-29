# Phase 05 — Content Cleaning

## Goal

Convert extracted document text into a conservative, deterministic cleaned representation without destroying meaning or source provenance.

## Implemented

- Page boundaries are preserved.
- Whitespace is normalized deterministically.
- Repeated page numbers can be removed.
- Repeated header/footer candidates are detected from page edges.
- Cleaning is configurable and can be disabled for forensic review.
- Empty-page warnings are surfaced instead of silently discarded.
- Every cleaning result reports removed patterns and changed-page count.

## Safety rules

Cleaning never mutates the immutable source document. The result is a derived representation. A repeated string is only treated as a header/footer candidate when it occurs frequently enough across page edges; one-off content is preserved.

The cleaner intentionally does not yet perform semantic rewriting, summarization, translation, table destruction, or aggressive punctuation normalization.

## Next integration

Phase 06 will classify the cleaned representation against the versioned TNPSC curriculum: exam → subject → unit → topic → subtopic, with confidence and review candidates rather than silent auto-publication.
