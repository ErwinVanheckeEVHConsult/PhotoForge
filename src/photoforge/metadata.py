from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .exif import extract_timestamp


@dataclass(frozen=True)
class ExtractedMetadata:
    naive_timestamp: datetime
    timestamp_source: str
    timezone_offset: timedelta | None = None


@dataclass(frozen=True)
class NormalizedMetadata:
    naive_timestamp: datetime
    timestamp_source: str
    timezone_offset: timedelta | None
    timezone_aware_timestamp: datetime | None
    utc_timestamp: datetime | None

    @property
    def timestamp(self) -> datetime:
        return self.naive_timestamp


def normalize_metadata(extracted_metadata: ExtractedMetadata) -> NormalizedMetadata:
    naive = extracted_metadata.naive_timestamp
    source = extracted_metadata.timestamp_source
    offset = extracted_metadata.timezone_offset

    # Required validations (non-redundant only)

    if naive.tzinfo is not None:
        raise TypeError("naive_timestamp must be naive")

    if not source:
        raise ValueError("timestamp_source must not be empty")

    # Representation construction

    if offset is None:
        return NormalizedMetadata(
            naive_timestamp=naive,
            timestamp_source=source,
            timezone_offset=None,
            timezone_aware_timestamp=None,
            utc_timestamp=None,
        )

    try:
        tz = timezone(offset)
    except Exception as exc:
        raise ValueError("timezone_offset is invalid") from exc

    aware = naive.replace(tzinfo=tz)

    if aware.replace(tzinfo=None) != naive:
        raise ValueError("timezone-aware timestamp must correspond to naive timestamp")

    utc = aware.astimezone(timezone.utc)

    return NormalizedMetadata(
        naive_timestamp=naive,
        timestamp_source=source,
        timezone_offset=offset,
        timezone_aware_timestamp=aware,
        utc_timestamp=utc,
    )


def extract_jpeg_normalized_metadata(path: Path, mtime_timestamp: float) -> NormalizedMetadata:
    timestamp, source = extract_timestamp(path, mtime_timestamp)
    return normalize_metadata(
        ExtractedMetadata(
            naive_timestamp=timestamp,
            timestamp_source=source,
        )
    )