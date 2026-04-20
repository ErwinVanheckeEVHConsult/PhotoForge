# tests/test_timestamp_diagnostics.py

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from photoforge.metadata import NormalizedMetadata
from photoforge.timestamp_diagnostics import (
    build_metadata_diagnostics,
    compare_metadata_pair,
)


def test_compare_naive_candidates() -> None:
    left = NormalizedMetadata(
        naive_timestamp=datetime(2024, 1, 2, 3, 4, 5),
        timestamp_source="filename",
        timezone_offset=None,
        timezone_aware_timestamp=None,
        utc_timestamp=None,
    )
    right = NormalizedMetadata(
        naive_timestamp=datetime(2024, 1, 2, 3, 4, 5),
        timestamp_source="folder",
        timezone_offset=None,
        timezone_aware_timestamp=None,
        utc_timestamp=None,
    )

    comparison = compare_metadata_pair(left, right)

    assert comparison is not None
    assert comparison.representation == "naive"
    assert comparison.equal is True


def test_compare_timezone_aware_candidates_in_utc_space() -> None:
    left = NormalizedMetadata(
        naive_timestamp=datetime(2024, 1, 2, 12, 0, 0),
        timestamp_source="exif_datetimeoriginal",
        timezone_offset=timedelta(hours=2),
        timezone_aware_timestamp=datetime(
            2024, 1, 2, 12, 0, 0, tzinfo=timezone(timedelta(hours=2))
        ),
        utc_timestamp=datetime(2024, 1, 2, 10, 0, 0, tzinfo=timezone.utc),
    )
    right = NormalizedMetadata(
        naive_timestamp=datetime(2024, 1, 2, 11, 0, 0),
        timestamp_source="exif_datetime",
        timezone_offset=timedelta(hours=1),
        timezone_aware_timestamp=datetime(
            2024, 1, 2, 11, 0, 0, tzinfo=timezone(timedelta(hours=1))
        ),
        utc_timestamp=datetime(2024, 1, 2, 10, 0, 0, tzinfo=timezone.utc),
    )

    comparison = compare_metadata_pair(left, right)

    assert comparison is not None
    assert comparison.representation == "utc"
    assert comparison.equal is True
    assert comparison.left_value == datetime(2024, 1, 2, 10, 0, 0, tzinfo=timezone.utc)
    assert comparison.right_value == datetime(2024, 1, 2, 10, 0, 0, tzinfo=timezone.utc)


def test_mixed_representation_pair_is_not_comparable() -> None:
    left = NormalizedMetadata(
        naive_timestamp=datetime(2024, 1, 2, 3, 4, 5),
        timestamp_source="filename",
        timezone_offset=None,
        timezone_aware_timestamp=None,
        utc_timestamp=None,
    )
    right = NormalizedMetadata(
        naive_timestamp=datetime(2024, 1, 2, 3, 4, 5),
        timestamp_source="exif_datetimeoriginal",
        timezone_offset=timedelta(hours=2),
        timezone_aware_timestamp=datetime(
            2024, 1, 2, 3, 4, 5, tzinfo=timezone(timedelta(hours=2))
        ),
        utc_timestamp=datetime(2024, 1, 2, 1, 4, 5, tzinfo=timezone.utc),
    )

    comparison = compare_metadata_pair(left, right)

    assert comparison is None


def test_build_metadata_diagnostics_skips_same_timestamp_source() -> None:
    left = NormalizedMetadata(
        naive_timestamp=datetime(2024, 1, 2, 3, 4, 5),
        timestamp_source="exif_datetimeoriginal",
        timezone_offset=None,
        timezone_aware_timestamp=None,
        utc_timestamp=None,
    )
    right = NormalizedMetadata(
        naive_timestamp=datetime(2024, 1, 2, 4, 4, 5),
        timestamp_source="exif_datetimeoriginal",
        timezone_offset=None,
        timezone_aware_timestamp=None,
        utc_timestamp=None,
    )

    diagnostics = build_metadata_diagnostics((left, right))

    assert diagnostics.comparisons == ()
    assert diagnostics.inconsistent_pairs == ()
    assert diagnostics.has_inconsistency is False


def test_build_metadata_diagnostics_flags_unequal_comparable_pairs() -> None:
    left = NormalizedMetadata(
        naive_timestamp=datetime(2024, 1, 2, 3, 4, 5),
        timestamp_source="filename",
        timezone_offset=None,
        timezone_aware_timestamp=None,
        utc_timestamp=None,
    )
    right = NormalizedMetadata(
        naive_timestamp=datetime(2024, 1, 2, 3, 4, 6),
        timestamp_source="folder",
        timezone_offset=None,
        timezone_aware_timestamp=None,
        utc_timestamp=None,
    )

    diagnostics = build_metadata_diagnostics((left, right))

    assert len(diagnostics.comparisons) == 1
    assert len(diagnostics.inconsistent_pairs) == 1
    assert diagnostics.has_inconsistency is True
    assert diagnostics.inconsistent_pairs[0].equal is False