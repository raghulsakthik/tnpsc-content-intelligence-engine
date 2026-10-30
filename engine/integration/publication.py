"""Deterministic publication package contract for the TNPSC platform admin module."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Iterable, Mapping

from ..lessons.models import Lesson
from ..mcq.models import MCQ


class PublicationContractError(ValueError):
    """Raised when engine output cannot safely cross the platform boundary."""


def _canonical(value: object) -> object:
    if isinstance(value, dict):
        return {key: _canonical(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    return value


def manifest_hash(publication_id: str, items: list[dict[str, object]]) -> str:
    """Match the platform's recursive canonical JSON + SHA-256 contract."""
    canonical = _canonical(
        {
            "publication_id": publication_id,
            "items": [
                {
                    "kind": item["kind"],
                    "content_id": item["content_id"],
                    "topic_id": item["topic_id"],
                    "payload": item["payload"],
                }
                for item in items
            ],
        }
    )
    encoded = json.dumps(canonical, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _lesson_item(lesson: Lesson, topic_id: str) -> dict[str, object]:
    if not lesson.is_publishable():
        raise PublicationContractError(f"lesson-not-publishable:{lesson.lesson_id}")
    return {
        "kind": "lesson",
        "content_id": lesson.lesson_id,
        "topic_id": topic_id,
        "payload": {
            "title": lesson.title,
            "concept": lesson.concept,
            "definition": lesson.definition,
            "explanation": lesson.explanation,
            "examples": list(lesson.examples),
            "revisionNotes": list(lesson.revision_notes),
            "sourceIds": list(lesson.source_ids),
            "version": lesson.version,
            "isPyq": False,
        },
    }


def _mcq_item(mcq: MCQ, topic_id: str) -> dict[str, object]:
    if not mcq.is_publishable():
        raise PublicationContractError(f"mcq-not-publishable:{mcq.mcq_id}")
    if len(mcq.correct_options()) != 1:
        raise PublicationContractError(f"mcq-answer-cardinality:{mcq.mcq_id}")
    options = [option.text for option in mcq.options]
    answer_index = next(i for i, option in enumerate(mcq.options) if option.is_correct)
    if len(set(options)) != len(options):
        raise PublicationContractError(f"mcq-duplicate-options:{mcq.mcq_id}")
    return {
        "kind": "mcq",
        "content_id": mcq.mcq_id,
        "topic_id": topic_id,
        "payload": {
            "question": mcq.question,
            "options": options,
            "answerIndex": answer_index,
            "explanation": mcq.explanation,
            "difficulty": mcq.difficulty.value,
            "sourceIds": list(mcq.source_evidence_ids),
            "version": mcq.version,
            "isPyq": False,
        },
    }


@dataclass(frozen=True, slots=True)
class PublicationPackage:
    publication_id: str
    manifest_hash: str
    items: tuple[dict[str, object], ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "publicationId": self.publication_id,
            "manifestHash": self.manifest_hash,
            "items": [dict(item) for item in self.items],
        }


def build_publication_package(
    *,
    publication_id: str,
    lessons: Iterable[Lesson] = (),
    mcqs: Iterable[MCQ] = (),
    topic_map: Mapping[str, str],
) -> PublicationPackage:
    """Convert approved engine content into the exact Admin Content Engine contract.

    ``topic_map`` is mandatory so the engine never guesses a platform topic. Missing
    mappings fail closed instead of creating or silently collapsing curriculum nodes.
    """
    if not publication_id.strip():
        raise PublicationContractError("publication-id-required")

    items: list[dict[str, object]] = []
    for lesson in lessons:
        topic_id = topic_map.get(lesson.curriculum_node_id)
        if not topic_id:
            raise PublicationContractError(
                f"missing-platform-topic:{lesson.curriculum_node_id}"
            )
        items.append(_lesson_item(lesson, topic_id))

    for mcq in mcqs:
        topic_id = topic_map.get(mcq.curriculum_node_id)
        if not topic_id:
            raise PublicationContractError(
                f"missing-platform-topic:{mcq.curriculum_node_id}"
            )
        items.append(_mcq_item(mcq, topic_id))

    if not items:
        raise PublicationContractError("publication-has-no-items")

    # Stable ordering makes the same approved engine output produce the same hash.
    items.sort(key=lambda item: (str(item["topic_id"]), str(item["kind"]), str(item["content_id"])))
    digest = manifest_hash(publication_id, items)
    return PublicationPackage(publication_id, digest, tuple(items))
