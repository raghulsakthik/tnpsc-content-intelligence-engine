"""Curriculum coverage and acquisition planning."""

from .analyzer import analyze_coverage, build_acquisition_requests, gap_id
from .models import AcquisitionRequest, AcquisitionStatus, CoverageGap, CoverageRecord, GapSeverity

__all__ = [
    "AcquisitionRequest",
    "AcquisitionStatus",
    "CoverageGap",
    "CoverageRecord",
    "GapSeverity",
    "analyze_coverage",
    "build_acquisition_requests",
    "gap_id",
]
