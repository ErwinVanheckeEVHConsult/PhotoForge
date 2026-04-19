# tests/test_timestamp_comparison.py

from __future__ import annotations

from datetime import datetime, timedelta

from photoforge.metadata import (
    ExtractedMetadata,
    build_metadata_diagnostics,
    compare_metadata_pair,
    normalize_metadata,
)


def test_compare_utc_candidates_equal() -> None:
    left = normalize_metadata(
        ExtractedMetadata(
            naive_timestamp=datetime(2024, 1, 1, 10, 0, 0),
            timestamp_source="source_a",
            timezone_offset=timedelta(hours=1),
        )
    )
    right = normalize_metadata(
        ExtractedMetadata(
            naive_timestamp=datetime(2024, 1, 1, 9, 0, 0),
            timestamp_source="source_b",
            timezone_offset=timedelta(0),
        )
    )

    comparison = compare_metadata_pair(left, right)

    assert comparison is not None
    assert comparison.representation == "utc"
    assert comparison.equal is True


def test_compare_naive_candidates_equal() -> None:
    left = normalize_metadata(
        ExtractedMetadata(
            naive_timestamp=datetime(2024, 1, 1, 10, 0, 0),
            timestamp_source="source_a",
        )
    )
    right = normalize_metadata(
        ExtractedMetadata(
            naive_timestamp=datetime(2024, 1, 1, 10, 0, 0),
            timestamp_source="source_b",
        )
    )

    comparison = compare_metadata_pair(left, right)

    assert comparison is not None
    assert comparison.representation == "naive"
    assert comparison.equal is True


def test_aware_and_naive_are_not_compared() -> None:
    aware = normalize_metadata(
        ExtractedMetadata(
            naive_timestamp=datetime(2024, 1, 1, 10, 0, 0),
            timestamp_source="source_a",
            timezone_offset=timedelta(hours=1),
        )
    )
    naive = normalize_metadata(
        ExtractedMetadata(
            naive_timestamp=datetime(2024, 1, 1, 10, 0, 0),
            timestamp_source="source_b",
        )
    )

    comparison = compare_metadata_pair(aware, naive)

    assert comparison is None


def test_build_metadata_diagnostics_detects_inconsistency() -> None:
    left = normalize_metadata(
        ExtractedMetadata(
            naive_timestamp=datetime(2024, 1, 1, 10, 0, 0),
            timestamp_source="source_a",
        )
    )
    right = normalize_metadata(
        ExtractedMetadata(
            naive_timestamp=datetime(2024, 1, 1, 11, 0, 0),
            timestamp_source="source_b",
        )
    )

    diagnostics = build_metadata_diagnostics((right, left))

    assert len(diagnostics.comparisons) == 1
    assert len(diagnostics.inconsistent_pairs) == 1
    assert diagnostics.has_inconsistency is True


def test_build_metadata_diagnostics_ignores_same_source_pairs() -> None:
    first = normalize_metadata(
        ExtractedMetadata(
            naive_timestamp=datetime(2024, 1, 1, 10, 0, 0),
            timestamp_source="source_a",
        )
    )
    second = normalize_metadata(
        ExtractedMetadata(
            naive_timestamp=datetime(2024, 1, 1, 11, 0, 0),
            timestamp_source="source_a",
        )
    )

    diagnostics = build_metadata_diagnostics((second, first))

    assert diagnostics.comparisons == ()
    assert diagnostics.inconsistent_pairs == ()
    assert diagnostics.has_inconsistency is False