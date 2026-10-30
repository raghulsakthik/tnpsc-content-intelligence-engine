# Phase 23 — Automated CI Integration

## Objective

Make the content-engine/platform boundary continuously testable in GitHub Actions without requiring a production database or learner data.

## Workflows

### Engine repository

`.github/workflows/content-platform-contract.yml`

Runs the platform-boundary contract suite:

```text
pytest -q tests/unit/test_platform_import.py
```

This protects deterministic publication manifests, provenance checks, PYQ exclusion, and platform-topic constraints.

### Platform repository

`.github/workflows/content-engine-contract.yml`

Runs on Node 22 and executes:

1. `npm ci`
2. `node --test tests/content-engine-runtime.smoke.mjs`
3. `npm test`

The first test is intentionally database-free and validates the content-engine manifest contract. The complete suite then protects existing platform behavior.

## Runtime boundary

CI does not fabricate an authenticated PostgreSQL environment. Live import/review/approval testing remains a separate deployment-level test and must use a controlled test database and test account.

## Safety gates

CI must fail if:

- the manifest hash becomes nondeterministic;
- changing content does not change the manifest;
- publication identity is not included in the manifest;
- the engine platform-boundary tests reject previously approved-safe fixtures;
- the existing platform test suite regresses.

## Phase 23 completion criteria

- [x] Engine contract workflow added.
- [x] Platform integration workflow added.
- [x] Runtime smoke test included.
- [x] Full existing platform test suite included.
- [x] No production credentials or learner data embedded in CI.
- [ ] Authenticated PostgreSQL E2E deployment test — deferred to runtime environment phase.
