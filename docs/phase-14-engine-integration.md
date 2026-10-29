# Phase 14 — Engine Integration

## Goal

Define a safe, deterministic boundary between the TNPSC Material Retrieval Engine (Engine 1) and the Content Intelligence Engine (Engine 2).

## Flow

```text
Engine 1
  Search → Download → Hash → Validate → Classify
                         ↓
                 Ingestion Envelope
                         ↓
Engine 2
  Document → Extract → Clean → Classify → Evidence
      → Lessons / MCQs → Quality → Admin Review → Course
                         ↓
                  Curriculum Gaps
                         ↓
                   Engine 1 search
```

## Boundary rules

- Engine 2 does not download arbitrary URLs.
- Engine 1 remains responsible for retrieval, HTTP safety, redirects, disk limits and file integrity.
- SHA-256 is carried across the boundary so derived content remains traceable to the immutable source.
- Resource IDs remain stable provenance identifiers.
- PYQ resources are hard-excluded and cannot enter content processing.
- The integration layer does not silently mutate Engine 1 state.
- Invalid envelopes fail closed.
- Gap feedback is a signal, not an automatic authorization to download.

## Idempotency

A resource is identified by its Engine 1 resource ID plus SHA-256. Reprocessing must produce the same document identity and derived version inputs. Persistence/orchestration can later add a durable processing ledger without changing this contract.

## Gap-driven acquisition

Content coverage can emit `CurriculumGap` signals containing a canonical curriculum node, reason, priority and optional language preference. Engine 1 may use these signals to prioritize discovery. It must still apply its normal source, SSRF, PYQ, integrity and storage policies.

## Security boundary

Untrusted source URLs, extracted text and document content are never treated as executable instructions. LLM-generated values must be structured and validated before persistence. No model output may bypass PYQ exclusion, provenance requirements, quality gates or admin approval.
