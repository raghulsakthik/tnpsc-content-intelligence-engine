# Phase 18 — Security & Production Readiness

## Objective

Make the retrieval/content pipeline fail closed at trust boundaries and provide a production checklist before connecting it to the learner-facing TNPSC platform.

## Security boundaries

1. **External URLs** — only HTTP(S); reject localhost, loopback, private, link-local, multicast, reserved and unspecified IP literals. The HTTP client must also resolve DNS and validate the resulting IP immediately before each connection to prevent DNS-rebinding SSRF.
2. **Archives** — reject absolute paths and `..` traversal, enforce member-size and member-count limits, and extract into a dedicated temporary directory.
3. **Documents** — verify MIME/signature, byte size and SHA-256 before processing. Treat HTML returned from a PDF URL as an invalid document.
4. **PYQs** — exclusion is fail-closed and occurs at both classification and Engine 1 → Engine 2 boundaries. Excluded material is never publishable.
5. **Prompt injection** — source documents are untrusted data. Never follow instructions embedded in PDFs/web pages. LLM output must be structured, validated, source-backed and unable to directly execute SQL, shell commands or publication operations.
6. **AI authority** — AI can propose classifications, lessons, MCQs, duplicate candidates and conflicts; it cannot approve, publish, delete evidence, bypass curriculum controls, change learner marks/mastery, or overwrite approved content.
7. **Secrets** — credentials, browser session state, API keys and tokens stay outside Git. Logs must redact secrets and authorization headers.
8. **RBAC/audit** — ingestion, review, approval, publication and administration are separate capabilities. Every approval/publication decision records actor, timestamp, content/course version and reason.
9. **Idempotency** — source SHA-256, deterministic content IDs and versioned manifests prevent accidental duplicate publication.
10. **Rate/disk safety** — acquisition remains bounded by concurrency, rate, timeout and free-space controls. Emergency disk thresholds stop downloads rather than risking corruption.

## Production gates

- [ ] Environment configuration validated; production secrets supplied by secret manager.
- [ ] SSRF validation enforced before request and after DNS resolution.
- [ ] Redirect destinations are revalidated on every hop.
- [ ] PDF/ZIP size, extraction and decompression limits enforced.
- [ ] Temporary files use restricted permissions and are removed after successful promotion.
- [ ] Database backups and restore procedure tested.
- [ ] SQLite WAL/transaction behavior validated for local deployment; use a server database if concurrent production writers require it.
- [ ] Structured logs contain correlation IDs but no credentials or raw session cookies.
- [ ] Health/readiness checks distinguish dependency failure from application failure.
- [ ] CI runs unit tests, security tests, type/static checks and packaging checks.
- [ ] Approved content and published course manifests are immutable.
- [ ] Rollback uses a previous approved/published version, never destructive mutation.
- [ ] Admin actions require authentication and least-privilege authorization.
- [ ] Current-affairs content has explicit publication/expiry dates and is versioned separately from evergreen content.
- [ ] Conflict records block automatic publication until reviewed.
- [ ] Disaster recovery and corpus reprocessing are documented and tested.

## End-to-end trust model

```text
UNTRUSTED WEB / PORTAL
        |
        v
URL + SSRF + redirect checks
        |
        v
DOWNLOAD + SIGNATURE + HASH + DISK SAFETY
        |
        v
IMMUTABLE DOCUMENT
        |
        v
EXTRACTION + CLEANING
        |
        v
CLASSIFICATION + PYQ HARD BLOCK
        |
        v
EVIDENCE + PROVENANCE
        |
        v
AI / DETERMINISTIC PROPOSALS
        |
        v
QUALITY VALIDATION
        |
        v
ADMIN REVIEW + AUDIT
        |
        v
VERSIONED COURSE MANIFEST
        |
        v
PLATFORM PUBLICATION
```

## Important limitation

This phase hardens the content-intelligence repository. It does **not** claim that a separate TNPSC learner platform is production-secure. The platform backend/frontend must undergo its own authenticated API, RBAC, dependency, deployment, secret, database and browser-flow security assessment before production integration.
