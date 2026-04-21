# src/photoforge/metadata.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from .model import TimestampCandidate


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


def normalize_metadata(candidate: TimestampCandidate) -> NormalizedMetadata:
    naive = candidate.naive_timestamp
    source = candidate.source_detail
    offset = candidate.timezone_offset

    if candidate.precision != "datetime":
        raise ValueError('candidate.precision must be "datetime"')

    if naive.tzinfo is not None:
        raise TypeError("naive_timestamp must be naive")

    if not source:
        raise ValueError("timestamp_source must not be empty")

    if offset is None:
        return NormalizedMetadata(
            naive_timestamp=naive,
            timestamp_source=source,
            timezone_offset=None,
            timezone_aware_timestamp=None,
            utc_timestamp=None,
        )

    try:
        if not (-timedelta(hours=23, minutes=59) <= offset <= timedelta(hours=23, minutes=59)):
            raise ValueError("timezone_offset is invalid")
        
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