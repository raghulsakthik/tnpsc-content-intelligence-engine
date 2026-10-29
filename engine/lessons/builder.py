"""Conservative lesson construction from evidence."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable

from .models import Lesson


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def lesson_id(curriculum_node_id: str, title: str, version: int = 1) -> str:
    key = f"{curriculum_node_id}|{_clean(title).lower()}|{version}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]


def build_lesson(
    *,
    curriculum_node_id: str,
    title: str,
    concept: str,
    definition: str = "",
    explanation: str = "",
    examples: Iterable[str] = (),
    revision_notes: Iterable[str] = (),
    source_ids: Iterable[str] = (),
    version: int = 1,
) -> Lesson:
    """Build a source-backed draft; it never approves or publishes content."""
    sources = tuple(dict.fromkeys(s for s in source_ids if s))
    return Lesson(
        lesson_id=lesson_id(curriculum_node_id, title, version),
        curriculum_node_id=curriculum_node_id,
        title=_clean(title),
        concept=_clean(concept),
        definition=_clean(definition),
        explanation=_clean(explanation),
        examples=tuple(_clean(x) for x in examples if _clean(x)),
        revision_notes=tuple(_clean(x) for x in revision_notes if _clean(x)),
        source_ids=sources,
        version=version,
    )
