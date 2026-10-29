"""Conservative, provenance-preserving text cleaning.

Cleaning must improve retrieval/generation quality without silently changing
meaning. Every transformation is deterministic and reported in the result.
"""

from dataclasses import dataclass, field
import re
from typing import Iterable


@dataclass(frozen=True, slots=True)
class CleaningConfig:
    collapse_whitespace: bool = True
    remove_repeated_page_numbers: bool = True
    remove_repeated_headers_footers: bool = True
    min_repeated_page_frequency: float = 0.60


@dataclass(frozen=True, slots=True)
class CleaningResult:
    cleaned_pages: tuple[str, ...]
    removed_patterns: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    changed_page_count: int = 0
    metadata: dict[str, object] = field(default_factory=dict)


def _normalize_line(line: str) -> str:
    return re.sub(r"[ \t]+", " ", line.strip())


def _is_page_number(line: str) -> bool:
    value = line.strip().lower()
    return bool(re.fullmatch(r"(?:page\s*)?\d{1,4}(?:\s*(?:of|/|-)\s*\d{1,4})?", value))


def _common_edge_lines(pages: list[list[str]], threshold: float) -> set[str]:
    if len(pages) < 2:
        return set()
    counts: dict[str, int] = {}
    for lines in pages:
        seen = set(lines[:3] + lines[-3:])
        for line in seen:
            if line:
                counts[line] = counts.get(line, 0) + 1
    minimum = max(2, int(len(pages) * threshold + 0.999))
    return {line for line, count in counts.items() if count >= minimum}


def clean_document(pages: Iterable[str], config: CleaningConfig | None = None) -> CleaningResult:
    """Clean extracted pages while retaining page boundaries and warnings."""
    cfg = config or CleaningConfig()
    raw_pages = list(pages)
    normalized = [[_normalize_line(line) for line in page.splitlines()] for page in raw_pages]
    normalized = [[line for line in lines if line] for lines in normalized]

    repeated_edges = (
        _common_edge_lines(normalized, cfg.min_repeated_page_frequency)
        if cfg.remove_repeated_headers_footers
        else set()
    )

    cleaned: list[str] = []
    removed: set[str] = set()
    changed = 0

    for lines in normalized:
        output: list[str] = []
        for line in lines:
            if cfg.remove_repeated_page_numbers and _is_page_number(line):
                removed.add("page-number")
                continue
            if line in repeated_edges:
                removed.add(f"repeated-edge:{line}")
                continue
            output.append(line)

        text = "\n".join(output)
        if cfg.collapse_whitespace:
            text = re.sub(r"\n{3,}", "\n\n", text).strip()
        cleaned.append(text)
        if text != "\n".join(lines).strip():
            changed += 1

    warnings: list[str] = []
    if any(not page.strip() for page in cleaned):
        warnings.append("one-or-more-pages-empty-after-cleaning")

    return CleaningResult(
        cleaned_pages=tuple(cleaned),
        removed_patterns=tuple(sorted(removed)),
        warnings=tuple(warnings),
        changed_page_count=changed,
        metadata={"input_page_count": len(raw_pages)},
    )
