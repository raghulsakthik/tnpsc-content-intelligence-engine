# Phase 01 — Corpus Inventory

## Goal

Build a read-only inventory boundary between Engine 1 and Engine 2 before any corpus-wide extraction or AI processing.

## Inputs

Engine 1 must provide the source-resource contract defined in `CONTENT_CONTRACT.md`.

Required identity/provenance fields include `resource_id`, source URL/reference, SHA-256, byte size, validation state, resource state and content labels.

## Inventory policy

1. Do not download resources from Engine 2.
2. Do not mutate or delete Engine 1 files.
3. Retain excluded resources in inventory reports for auditability.
4. Mark PYQ/PYQ compilations as `excluded_pyq` and prevent downstream generation.
5. Treat missing hashes or failed validation as incomplete candidates requiring review.
6. Preserve one-to-many mapping: one source document may eventually contribute to multiple curriculum topics.

## Inventory classifications

- `candidate` — eligible for later processing pending document validation.
- `excluded_pyq` — hard excluded from content generation.
- `invalid_source` — failed source validation.
- `unsupported` — source type requires a future adapter.
- `review_required` — metadata is insufficient or contradictory.

## Coverage report

The Phase 01 report must eventually include:

- total resources
- eligible resources
- PYQ resources
- invalid/quarantined resources
- byte totals
- language distribution
- exam distribution
- content-type distribution
- current-affairs coverage by date/year
- government-material coverage
- mock/MCQ coverage
- resources needing OCR
- resources missing usable hashes
- duplicate candidates
- curriculum areas with no known source coverage

## Current execution status

The connected Desktop Commander device is currently offline, so the live Engine 1 SQLite corpus cannot be inventoried from this session. The repository therefore contains the inventory contract and deterministic normalization code, but no fabricated corpus counts.

When the device is online, the next operation is a read-only export of Engine 1 resource metadata followed by `inventory_records(...)` and a persisted coverage report.

## Definition of Done

- Engine 1 metadata can be consumed without copying source bytes.
- Inventory output is deterministic.
- PYQ rows are retained but hard-excluded.
- Provenance fields are preserved.
- Unit tests cover exclusion and contract aliases.
- No corpus files are modified or deleted.
