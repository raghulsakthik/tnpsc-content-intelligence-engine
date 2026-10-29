# Canonical Curriculum

The curriculum is a versioned taxonomy, not a collection of labels inferred independently for every PDF.

## Hierarchy

```text
Exam
└── Subject
    └── Unit
        └── Topic
            └── Subtopic
```

Content can reference one or more evidence blocks but should map to one canonical curriculum node at each relevant level.

## Initial TNPSC Group II/IIA domains

The first curriculum version should cover the official Group II/IIA scheme/syllabus and be expanded only through explicit versioned changes. Initial domains include:

- General Studies
- Aptitude & Mental Ability
- General Tamil
- General English
- Thirukkural
- Current Affairs

General Studies should be decomposed into the applicable science, geography, history/culture, Indian national movement, polity, economy, development administration in Tamil Nadu, Tamil Nadu history/culture/heritage and socio-political movements, science & technology, socio-economic issues and environment areas defined by the selected syllabus version.

## Versioning

A curriculum version has:

```text
curriculum_version_id
exam
source_reference
effective_from
status
created_at
```

Nodes use stable identifiers. Renaming or restructuring creates a new version/mapping rather than silently changing historical content.

## Mapping policy

- Exact syllabus terminology has priority.
- Aliases are stored separately.
- English/Tamil labels can point to the same canonical node.
- Ambiguous classification becomes a review item.
- A document can contribute to multiple nodes.
- A lesson should remain topic-bounded even when its source document is broad.
