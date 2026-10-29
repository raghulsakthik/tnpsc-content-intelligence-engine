# Phase 04 — Document Extraction

## Goal

Turn an immutable source PDF into a page-aware extraction result without losing provenance or pretending that scanned pages contain usable text.

## Pipeline

```text
Source PDF
   ↓
Native PDF extraction
   ↓
Page boundaries preserved
   ↓
Image-only detection
   ├── native text → continue
   ├── mixed pages → hybrid/OCR queue
   └── image-only document → OCR queue
   ↓
ExtractionResult
   ↓
Phase 3 Document IR
```

## Contracts

`ExtractionResult` records:

- extraction method
- extractor name/version
- source SHA-256
- page-level results
- warnings

`PageExtraction` records:

- page number
- extracted text
- method
- character count
- image-only signal
- quality when known
- warnings

## Important rules

1. Source files remain immutable.
2. Page numbering is 1-based and contiguous.
3. Native text extraction is attempted before OCR.
4. A page with effectively no text is marked `ocr_required`; it is not treated as a successful empty page.
5. Mixed documents receive a `hybrid` signal.
6. OCR implementation is intentionally an adapter boundary so the core engine is not coupled to a particular OCR vendor/library.
7. SHA-256 is recomputed from the source bytes and carried through the result.
8. Extraction does not classify, summarize, generate lessons, or generate MCQs.

## Current implementation

The repository contains a backend-neutral `PdfBackend` protocol, native extraction orchestration, validation, and unit tests using a fake PDF backend. This lets the contracts be tested without storing real TNPSC PDFs in Git.

## Next work

- add a production PDF backend
- add OCR backend with Tamil/English language packs
- preserve tables and layout blocks
- emit Phase 3 `DocumentPage` / `DocumentBlock` records directly
- add extraction metrics and failure/quarantine handling
- add corpus fixtures for normal, scanned, mixed-language, table-heavy, corrupt, and password-protected PDFs
