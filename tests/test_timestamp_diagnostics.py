# tests/test_timestamp_diagnostics.py

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from photoforge.model import ExtractionDiagnostic, TimestampCandidate
from photoforge.timestamp_diagnostics import (
    build_metadata_diagnostics,
    compare_timestamp_candidates,
)


def test_compare_naive_candidates() -> None:
    left = TimestampCandidate(
        source_kind="filename",
        source_detail="filename_yyyymmdd_hhmmss",
        naive_timestamp=datetime(2024, 1, 2, 3, 4, 5),
        precision="datetime",
        timezone_offset=None,
    )
    right = TimestampCandidate(
        source_kind="filesystem",
        source_detail="filesystem_mtime",
        naive_timestamp=datetime(2024, 1, 2, 3, 4, 5),
        precision="datetime",
        timezone_offset=None,
    )

    comparison = compare_timestamp_candidates(left, right)

    assert comparison is not None
    assert comparison.representation == "naive"
    assert comparison.equal is True


def test_compare_utc_candidates() -> None:
    left = TimestampCandidate(
        source_kind="exif",
        source_detail="exif_datetimeoriginal",
        naive_timestamp=datetime(2024, 1, 2, 12, 0, 0),
        precision="datetime",
        timezone_offset=timedelta(hours=2),
    )
    right = TimestampCandidate(
        source_kind="exif",
        source_detail="exif_datetime",
        naive_timestamp=datetime(2024, 1, 2, 11, 0, 0),
        precision="datetime",
        timezone_offset=timedelta(hours=1),
    )

    comparison = compare_timestamp_candidates(left, right)

    assert comparison is not None
    assert comparison.representation == "utc"
    assert comparison.equal is True
    assert comparison.left_value == datetime(2024, 1, 2, 10, 0, 0, tzinfo=timezone.utc)
    assert comparison.right_value == datetime(2024, 1, 2, 10, 0, 0, tzinfo=timezone.utc)


def test_mixed_representation_pair_is_not_comparable() -> None:
    left = TimestampCandidate(
        source_kind="filename",
        source_detail="filename_yyyymmdd_hhmmss",
        naive_timestamp=datetime(2024, 1, 2, 3, 4, 5),
        precision="datetime",
        timezone_offset=None,
    )
    right = TimestampCandidate(
        source_kind="exif",
        source_detail="exif_datetimeoriginal",
        naive_timestamp=datetime(2024, 1, 2, 3, 4, 5),
        precision="datetime",
        timezone_offset=timedelta(hours=2),
    )

    comparison = compare_timestamp_candidates(left, right)

    assert comparison is None


def test_build_metadata_diagnostics_includes_extraction_diagnostics() -> None:
    candidates = (
        TimestampCandidate(
            source_kind="filesystem",
            source_detail="filesystem_mtime",
            naive_timestamp=datetime(2024, 1, 2, 3, 4, 5),
            precision="datetime",
            timezone_offset=None,
        ),
        TimestampCandidate(
            source_kind="filename",
            source_detail="filename_yyyymmdd_hhmmss",
            naive_timestamp=datetime(2024, 1, 2, 3, 4, 6),
            precision="datetime",
            timezone_offset=None,
        ),
    )

    extraction_diagnostics = (
        ExtractionDiagnostic(
            source_kind="exif",
            diagnostic_type="missing",
        ),
    )

    diagnostics = build_metadata_diagnostics(
        candidates,
        extraction_diagnostics=extraction_diagnostics,
    )

    assert diagnostics.extraction_diagnostics == extraction_diagnostics
    assert len(diagnostics.comparisons) == 1
    assert len(diagnostics.inconsistent_pairs) == 1
    assert diagnostics.has_inconsistency is True
    assert diagnostics.has_extraction_diagnostics is True