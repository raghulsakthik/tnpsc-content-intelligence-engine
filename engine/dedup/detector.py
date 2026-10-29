"""Deterministic, non-destructive duplicate detection.

Semantic similarity is deliberately represented as a candidate only. Nothing in
this module merges, deletes, or overwrites source material.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from hashlib import sha256

from .models import DuplicateCandidate, DuplicateKind


@dataclass(frozen=True, slots=True)
class DeduplicationDetector:
    semantic_candidate_threshold: float = 0.90

    @staticmethod
    def normalize_text(text: str) -> str:
        text = text.casefold()
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @classmethod
    def text_fingerprint(cls, text: str) -> str:
        return sha256(cls.normalize_text(text).encode("utf-8")).hexdigest()

    @staticmethod
    def _token_counter(text: str) -> Counter[str]:
        return Counter(re.findall(r"[\w\u0B80-\u0BFF]+", text.casefold()))

    @classmethod
    def cosine_similarity(cls, left: str, right: str) -> float:
        a, b = cls._token_counter(left), cls._token_counter(right)
        if not a or not b:
            return 0.0
        common = set(a) & set(b)
        dot = sum(a[t] * b[t] for t in common)
        left_norm = sum(v * v for v in a.values()) ** 0.5
        right_norm = sum(v * v for v in b.values()) ** 0.5
        return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0

    def compare_resources(
        self,
        left_id: str,
        left_sha256: str,
        left_text: str,
        right_id: str,
        right_sha256: str,
        right_text: str,
    ) -> tuple[DuplicateCandidate, ...]:
        if left_sha256 and left_sha256 == right_sha256:
            return (DuplicateCandidate(left_id, right_id, DuplicateKind.EXACT_RESOURCE, 1.0, ("sha256-match",)),)

        left_normalized = self.normalize_text(left_text)
        right_normalized = self.normalize_text(right_text)
        if left_normalized and left_normalized == right_normalized:
            return (DuplicateCandidate(left_id, right_id, DuplicateKind.NORMALIZED_TEXT, 1.0, ("normalized-text-match",)),)

        if left_text and left_text == right_text:
            return (DuplicateCandidate(left_id, right_id, DuplicateKind.EXACT_TEXT, 1.0, ("exact-text-match",)),)

        similarity = self.cosine_similarity(left_text, right_text)
        if similarity >= self.semantic_candidate_threshold:
            return (DuplicateCandidate(left_id, right_id, DuplicateKind.POSSIBLE_SEMANTIC, similarity, ("token-cosine-candidate",)),)
        return ()

    def compare_many(self, resources: list[dict[str, str]]) -> tuple[DuplicateCandidate, ...]:
        candidates: list[DuplicateCandidate] = []
        for index, left in enumerate(resources):
            for right in resources[index + 1 :]:
                candidates.extend(
                    self.compare_resources(
                        left["id"], left.get("sha256", ""), left.get("text", ""),
                        right["id"], right.get("sha256", ""), right.get("text", ""),
                    )
                )
        return tuple(candidates)
