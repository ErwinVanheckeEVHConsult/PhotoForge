# src/photoforge/metadata.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from .model import TimestampCandidate


@dataclass(frozen=True)
class NormalizedMetadata:
    timestamp: datetime
    timestamp_source: str


def normalize_metadata(primary_candidate: TimestampCandidate) -> NormalizedMetadata:
    naive = primary_candidate.naive_timestamp
    source = primary_candidate.source_detail
    offset = primary_candidate.timezone_offset

    if offset is None:
        return NormalizedMetadata(
            timestamp=naive,
            timestamp_source=source,
        )

    aware = naive.replace(tzinfo=timezone(offset))

    return NormalizedMetadata(
        timestamp=aware.astimezone(timezone.utc),
        timestamp_source=source,
    )