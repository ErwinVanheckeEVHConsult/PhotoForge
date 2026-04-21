# src/photoforge/timestamp_diagnostics.py

from __future__ import annotations

from datetime import datetime, timezone

from .model import (
    ExtractionDiagnostic,
    MetadataDiagnostics,
    TimestampCandidate,
    TimestampComparison,
)

_REPRESENTATION_ORDER: dict[str, int] = {
    "utc": 0,
    "naive": 1,
}


def build_metadata_diagnostics(
    valid_candidates: tuple[TimestampCandidate, ...],
    extraction_diagnostics: tuple[ExtractionDiagnostic, ...] = (),
) -> MetadataDiagnostics:
    sorted_candidates = tuple(sorted(valid_candidates, key=_candidate_sort_key))

    comparisons: list[TimestampComparison] = []
    inconsistent_pairs: list[TimestampComparison] = []

    for index, left in enumerate(sorted_candidates):
        for right in sorted_candidates[index + 1 :]:
            if left.source_detail == right.source_detail:
                continue

            comparison = compare_timestamp_candidates(left, right)
            if comparison is None:
                continue

            comparisons.append(comparison)

            if not comparison.equal:
                inconsistent_pairs.append(comparison)

    return MetadataDiagnostics(
        extraction_diagnostics=tuple(sorted(extraction_diagnostics, key=_diagnostic_sort_key)),
        comparisons=tuple(comparisons),
        inconsistent_pairs=tuple(inconsistent_pairs),
    )


def compare_timestamp_candidates(
    left: TimestampCandidate,
    right: TimestampCandidate,
) -> TimestampComparison | None:
    left_representation, left_value = _comparison_value(left)
    right_representation, right_value = _comparison_value(right)

    if left_representation != right_representation:
        return None

    return TimestampComparison(
        left_source=left.source_detail,
        right_source=right.source_detail,
        representation=left_representation,
        left_value=left_value,
        right_value=right_value,
        equal=left_value == right_value,
    )


def _candidate_sort_key(candidate: TimestampCandidate) -> tuple[str, int, str, str]:
    representation = _comparison_representation(candidate)
    offset_key = (
        ""
        if candidate.timezone_offset is None
        else str(int(candidate.timezone_offset.total_seconds()))
    )

    return (
        candidate.source_detail,
        _REPRESENTATION_ORDER[representation],
        candidate.naive_timestamp.isoformat(),
        offset_key,
    )


def _diagnostic_sort_key(diagnostic: ExtractionDiagnostic) -> tuple[str, str, str]:
    return (
        diagnostic.source_kind,
        diagnostic.diagnostic_type,
        diagnostic.field_name or "",
    )


def _comparison_representation(candidate: TimestampCandidate) -> str:
    if candidate.timezone_offset is not None:
        return "utc"
    return "naive"


def _comparison_value(candidate: TimestampCandidate) -> tuple[str, datetime]:
    if candidate.timezone_offset is None:
        return "naive", candidate.naive_timestamp

    aware = candidate.naive_timestamp.replace(tzinfo=timezone(candidate.timezone_offset))
    return "utc", aware.astimezone(timezone.utc)