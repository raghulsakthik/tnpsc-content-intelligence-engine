# Content Contract

This is the logical contract between Engine 1 and Engine 2. The physical API/schema can evolve while preserving these semantics.

## Source resource

Required fields:

```text
resource_id
source_url
source_type
source_domain
local_path or content_reference
sha256
byte_size
mime_type
validation_status
resource_state
exam_hint
is_pyq
is_mock
is_current_affair
is_government_material
publication_date
content_year
created_at
updated_at
```

## Rules

1. `sha256` identifies immutable source bytes.
2. Engine 2 must be able to replay processing from the source resource.
3. A source resource may map to multiple subjects/topics.
4. A source resource may be rejected without being deleted.
5. `is_pyq=true` or a high-confidence PYQ classification blocks content generation for publication.
6. Source metadata is never treated as learner-facing content without transformation/review.

## Processing identity

Every processing attempt should have:

```text
processing_run_id
resource_id
pipeline_version
stage
input_hash
output_hash
status
started_at
completed_at
error_code
```

The combination of resource fingerprint + pipeline version + stage should support idempotent replay.

## Derived content contract

Lessons and MCQs must contain source references. A generated object without evidence is invalid for publication.

```text
content_id
content_version
exam
subject
unit
 topic
subtopic
language
content_type
source_refs
evidence_refs
confidence_vector
processing_status
admin_status
created_at
updated_at
```

## Publication states

`draft → review → approved → published`

Terminal rejection/archive states may be introduced without deleting historical versions.
