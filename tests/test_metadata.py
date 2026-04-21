# tests/test_metadata.py

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from photoforge.metadata import normalize_metadata
from photoforge.model import TimestampCandidate


def test_normalize_metadata_without_timezone() -> None:
    candidate = TimestampCandidate(
        source_kind="filesystem",
        source_detail="mtime",
        naive_timestamp=datetime(2024, 1, 2, 3, 4, 5),
        precision="datetime",
        timezone_offset=None,
    )

    result = normalize_metadata(candidate)

    assert result.naive_timestamp == datetime(2024, 1, 2, 3, 4, 5)
    assert result.timestamp_source == "mtime"
    assert result.timezone_offset is None
    assert result.timezone_aware_timestamp is None
    assert result.utc_timestamp is None


def test_normalize_metadata_with_timezone() -> None:
    candidate = TimestampCandidate(
        source_kind="exif",
        source_detail="exif_datetimeoriginal",
        naive_timestamp=datetime(2024, 1, 2, 3, 4, 5),
        precision="datetime",
        timezone_offset=timedelta(hours=2, minutes=30),
    )

    result = normalize_metadata(candidate)

    assert result.naive_timestamp == datetime(2024, 1, 2, 3, 4, 5)
    assert result.timestamp_source == "exif_datetimeoriginal"
    assert result.timezone_offset == timedelta(hours=2, minutes=30)
    assert result.timezone_aware_timestamp == datetime(
        2024,
        1,
        2,
        3,
        4,
        5,
        tzinfo=timezone(timedelta(hours=2, minutes=30)),
    )
    assert result.utc_timestamp == datetime(
        2024,
        1,
        2,
        0,
        34,
        5,
        tzinfo=timezone.utc,
    )


def test_normalize_metadata_rejects_date_precision() -> None:
    candidate = TimestampCandidate(
        source_kind="filename",
        source_detail="filename_date_only",
        naive_timestamp=datetime(2024, 1, 2, 0, 0, 0),
        precision="date",
        timezone_offset=None,
    )

    with pytest.raises(ValueError, match='candidate.precision must be "datetime"'):
        normalize_metadata(candidate)


def test_normalize_metadata_rejects_aware_naive_timestamp() -> None:
    candidate = TimestampCandidate(
        source_kind="exif",
        source_detail="exif_datetimeoriginal",
        naive_timestamp=datetime(2024, 1, 2, 3, 4, 5, tzinfo=timezone.utc),
        precision="datetime",
        timezone_offset=None,
    )

    with pytest.raises(TypeError, match="naive_timestamp must be naive"):
        normalize_metadata(candidate)


def test_normalize_metadata_rejects_invalid_timezone_offset() -> None:
    candidate = TimestampCandidate(
        source_kind="exif",
        source_detail="exif_datetimeoriginal",
        naive_timestamp=datetime(2024, 1, 2, 3, 4, 5),
        precision="datetime",
        timezone_offset=timedelta(hours=30),
    )

    with pytest.raises(ValueError, match="timezone_offset is invalid"):
        normalize_metadata(candidate)