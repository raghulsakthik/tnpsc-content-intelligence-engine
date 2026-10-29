# ADR-007: Storage-Aware Ingestion

## Status
Accepted

## Decision

Engine 2 must process through bounded, resumable stages and must respect the retrieval engine's storage reservation. It must not trigger uncontrolled duplicate copies of source files.

## Rationale

The local deployment has finite disk capacity. Content processing can create temporary extraction/OCR artifacts much larger than the original PDF.

## Consequences

- Prefer streaming/bounded extraction.
- Clean temporary artifacts after successful stage completion.
- Track disk requirements before expensive stages.
- Use idempotent processing to avoid repeated intermediate copies.
- Never delete source material automatically as a storage workaround.
