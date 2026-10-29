# Phase 12 — Admin Review & Content Management

## Goal

Create an explicit human-review boundary between generated content and published TNPSC learning content.

## Review lifecycle

```text
Generated draft
  -> quality checks
  -> review queue
  -> assigned reviewer
  -> evidence inspection
  -> approve / request changes / reject
  -> immutable audit event
  -> publication layer
```

## Review states

- `queued`: waiting for a reviewer
- `in_review`: actively being reviewed
- `changes_requested`: reviewer requires correction
- `approved`: approved for the publication layer
- `rejected`: permanently rejected by this review cycle

## Review requirements

A review item must have:

- content type and ID
- positive content version
- at least one evidence ID
- quality-check references where available
- reviewer identity for decisions
- decision reason
- timestamp

## Publication boundary

Approval does not mutate the original document or erase evidence. It authorizes the reviewed content version to enter the publication layer. Edits must create a new content version rather than silently changing an approved version.

PYQ/excluded content must remain blocked upstream and cannot be made publishable by an admin review decision.

## Auditability

Every decision generates an `AuditEvent` containing actor, action, entity, timestamp, version information, review ID, and reason. Audit events are deterministic in identity for the same review decision.

## Security model

The domain layer intentionally does not implement authentication or RBAC itself. API/admin integration must enforce permissions before invoking review operations. Recommended roles are reviewer, senior reviewer, content administrator, and publisher, with least privilege and explicit separation of approval and publication where required.

## Next phase

Phase 13 builds versioned courses and curriculum-facing course structures on top of approved lessons, topics, MCQs, and tests.
