"""Deterministic curriculum coverage analysis and acquisition planning."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable, Mapping

from .models import AcquisitionRequest, CoverageGap, CoverageRecord, GapSeverity


def _query_label(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def gap_id(curriculum_node_id: str, reasons: Iterable[str]) -> str:
    key = f"{curriculum_node_id}|{'|'.join(sorted(set(reasons)))}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]


def _severity(score: float, reasons: tuple[str, ...]) -> GapSeverity:
    if score < 0.20 or "no-approved-content" in reasons:
        return GapSeverity.CRITICAL
    if score < 0.45 or len(reasons) >= 3:
        return GapSeverity.HIGH
    if score < 0.70:
        return GapSeverity.MEDIUM
    return GapSeverity.LOW


def analyze_coverage(
    records: Iterable[CoverageRecord],
    *,
    minimum_quality: float = 0.70,
) -> tuple[CoverageGap, ...]:
    """Find weak curriculum nodes without generating or publishing content."""
    gaps: list[CoverageGap] = []
    for record in records:
        reasons: list[str] = []
        score = min(record.content_score, max(0.0, min(1.0, record.quality_score)))
        if record.approved_lesson_count == 0:
            reasons.append("no-approved-content")
        elif record.approved_lesson_count < 2:
            reasons.append("insufficient-lessons")
        if record.approved_mcq_count < 10:
            reasons.append("insufficient-mcqs")
        if record.approved_test_count == 0:
            reasons.append("missing-topic-test")
        if record.source_count == 0:
            reasons.append("missing-source-provenance")
        if record.quality_score < minimum_quality:
            reasons.append("quality-below-threshold")

        if reasons:
            reason_tuple = tuple(dict.fromkeys(reasons))
            gaps.append(
                CoverageGap(
                    gap_id=gap_id(record.curriculum_node_id, reason_tuple),
                    curriculum_node_id=record.curriculum_node_id,
                    severity=_severity(score, reason_tuple),
                    coverage_score=round(score, 4),
                    reasons=reason_tuple,
                    suggested_queries=(record.curriculum_node_id.replace("-", " "),),
                )
            )
    return tuple(sorted(gaps, key=lambda gap: (-_priority(gap.severity), gap.curriculum_node_id)))


def _priority(severity: GapSeverity) -> int:
    return {
        GapSeverity.CRITICAL: 4,
        GapSeverity.HIGH: 3,
        GapSeverity.MEDIUM: 2,
        GapSeverity.LOW: 1,
    }[severity]


def build_acquisition_requests(gaps: Iterable[CoverageGap]) -> tuple[AcquisitionRequest, ...]:
    """Turn gaps into Engine 1 discovery requests; no fetching occurs here."""
    requests: list[AcquisitionRequest] = []
    for gap in gaps:
        priority = _priority(gap.severity)
        request_key = f"{gap.gap_id}|{'|'.join(gap.suggested_queries)}"
        request_id = hashlib.sha256(request_key.encode("utf-8")).hexdigest()[:24]
        requests.append(
            AcquisitionRequest(
                request_id=request_id,
                gap_id=gap.gap_id,
                curriculum_node_id=gap.curriculum_node_id,
                queries=tuple(_query_label(query) for query in gap.suggested_queries if _query_label(query)),
                priority=priority,
            )
        )
    return tuple(sorted(requests, key=lambda item: (-item.priority, item.request_id)))
