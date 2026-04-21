# src/photoforge/timestamp_diagnostics.py

from __future__ import annotations

from datetime import datetime, timezone

from .metadata import NormalizedMetadata
from .model import MetadataDiagnostics, TimestampComparison

_REPRESENTATION_ORDER: dict[str, int] = {
    "utc": 0,
    "naive": 1,
}


def build_metadata_diagnostics(
    candidates: tuple[NormalizedMetadata, ...],
) -> MetadataDiagnostics:
    sorted_candidates = tuple(
        sorted(candidates, key=_candidate_sort_key)
    )

    comparisons: list[TimestampComparison] = []
    inconsistent_pairs: list[TimestampComparison] = []

    for index, left in enumerate(sorted_candidates):
        for right in sorted_candidates[index + 1 :]:
            if left.timestamp_source == right.timestamp_source:
                continue

            comparison = compare_metadata_pair(left, right)
            if comparison is None:
                continue

            comparisons.append(comparison)

            if not comparison.equal:
                inconsistent_pairs.append(comparison)

    return MetadataDiagnostics(
        comparisons=tuple(comparisons),
        inconsistent_pairs=tuple(inconsistent_pairs),
    )


def compare_metadata_pair(
    left: NormalizedMetadata,
    right: NormalizedMetadata,
) -> TimestampComparison | None:
    left_representation, left_value = _comparison_value(left)
    right_representation, right_value = _comparison_value(right)

    if left_representation != right_representation:
        return None

    return TimestampComparison(
        left_source=left.timestamp_source,
        right_source=right.timestamp_source,
        representation=left_representation,
        left_value=left_value,
        right_value=right_value,
        equal=left_value == right_value,
    )


def _candidate_sort_key(candidate: NormalizedMetadata) -> tuple[str, int, str, str, str]:
    comparison_representation, _, _, _ = _comparison_fields(candidate)

    return (
        candidate.timestamp_source,
        _REPRESENTATION_ORDER[comparison_representation],
        candidate.naive_timestamp.isoformat(),
        candidate.timezone_aware_timestamp.isoformat()
        if candidate.timezone_aware_timestamp is not None
        else "",
        candidate.utc_timestamp.isoformat()
        if candidate.utc_timestamp is not None
        else "",
    )


def _comparison_value(candidate: NormalizedMetadata) -> tuple[str, datetime]:
    comparison_representation, naive_value, aware_value, utc_value = _comparison_fields(
        candidate
    )

    if comparison_representation == "utc":
        if utc_value is not None:
            return "utc", utc_value

        if aware_value is None:
            raise ValueError(
                "utc comparison representation requires timezone_aware_timestamp or utc_timestamp"
            )

        return "utc", aware_value.astimezone(timezone.utc)

    return "naive", naive_value


def _comparison_fields(
    candidate: NormalizedMetadata,
) -> tuple[str, datetime, datetime | None, datetime | None]:
    if candidate.utc_timestamp is not None and candidate.timezone_aware_timestamp is not None:
        if candidate.timezone_aware_timestamp.astimezone(timezone.utc) != candidate.utc_timestamp:
            raise ValueError("timezone_aware_timestamp and utc_timestamp mismatch")
        
    if candidate.utc_timestamp is not None:
        return (
            "utc",
            candidate.naive_timestamp,
            candidate.timezone_aware_timestamp,
            candidate.utc_timestamp,
        )

    if candidate.timezone_aware_timestamp is not None:
        return (
            "utc",
            candidate.naive_timestamp,
            candidate.timezone_aware_timestamp,
            candidate.utc_timestamp,
        )

    return (
        "naive",
        candidate.naive_timestamp,
        candidate.timezone_aware_timestamp,
        candidate.utc_timestamp,
    )