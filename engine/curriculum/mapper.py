"""Deterministic curriculum label matching primitives."""

from __future__ import annotations

from dataclasses import dataclass

from .models import CurriculumNode


@dataclass(frozen=True, slots=True)
class MappingCandidate:
    node_id: str
    score: float
    matched_alias: str | None = None


def normalize_label(value: str) -> str:
    return " ".join(value.casefold().strip().split())


def candidate_nodes(label: str, nodes: tuple[CurriculumNode, ...]) -> tuple[MappingCandidate, ...]:
    """Return deterministic exact/alias candidates.

    This function never auto-publishes a mapping. Ambiguous candidates must
    remain reviewable by the classification layer.
    """
    needle = normalize_label(label)
    results: list[MappingCandidate] = []
    for node in nodes:
        labels = (node.title_en, node.title_ta, node.canonical_key, *node.aliases)
        for raw in labels:
            if not raw:
                continue
            normalized = normalize_label(raw)
            if needle == normalized:
                results.append(
                    MappingCandidate(node_id=node.id, score=1.0, matched_alias=raw)
                )
                break
    return tuple(results)
