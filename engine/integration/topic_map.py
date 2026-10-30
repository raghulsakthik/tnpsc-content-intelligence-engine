"""Validate the platform-owned topic map before publication.

The platform is authoritative for platform topic IDs. The engine may map its
curriculum node IDs to those IDs, but it must never invent or infer a missing
platform topic.
"""

from __future__ import annotations

from typing import Mapping

from .publication import PublicationContractError


def validate_platform_topic_map(
    *,
    mapping: Mapping[str, str],
    platform_export: Mapping[str, object],
) -> dict[str, str]:
    """Return a normalized engine-node -> platform-topic mapping.

    ``platform_export`` is the JSON returned by the platform's
    ``/api/admin/content-engine/topic-map`` endpoint. Every mapped platform
    topic must exist in that export. Empty or duplicate targets fail closed.
    """
    topics = platform_export.get("topics")
    if not isinstance(topics, list):
        raise PublicationContractError("platform-topic-export-invalid")

    platform_topic_ids = {
        str(row.get("topic_id"))
        for row in topics
        if isinstance(row, dict) and row.get("topic_id")
    }
    if not platform_topic_ids:
        raise PublicationContractError("platform-topic-export-empty")

    normalized: dict[str, str] = {}
    reverse: dict[str, str] = {}
    for engine_node, platform_topic in mapping.items():
        source = str(engine_node).strip()
        target = str(platform_topic).strip()
        if not source or not target:
            raise PublicationContractError("platform-topic-map-empty-entry")
        if target not in platform_topic_ids:
            raise PublicationContractError(f"unknown-platform-topic:{target}")
        previous = reverse.get(target)
        if previous is not None and previous != source:
            raise PublicationContractError(
                f"platform-topic-target-collision:{target}:{previous}:{source}"
            )
        normalized[source] = target
        reverse[target] = source

    return normalized
