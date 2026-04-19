# src/photoforge/metadata.py

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
class TimestampComparison:
    left_source: str
    right_source: str
    representation: str
    left_value: datetime
    right_value: datetime
    equal: bool


@dataclass(frozen=True)
class MetadataDiagnostics:
    comparisons: tuple[TimestampComparison, ...]
    inconsistent_pairs: tuple[TimestampComparison, ...]

    @property
    def has_inconsistency(self) -> bool:
        return bool(self.inconsistent_pairs)


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


def _primary_representation(metadata: NormalizedMetadata) -> str:
    if metadata.utc_timestamp is not None:
        return "utc"
    if metadata.timezone_aware_timestamp is not None:
        return "timezone_aware"
    return "naive"


def _comparison_value(metadata: NormalizedMetadata) -> tuple[str, datetime]:
    representation = _primary_representation(metadata)

    if representation == "utc":
        utc_value = metadata.utc_timestamp
        if utc_value is None:
            raise ValueError("utc representation requires utc_timestamp")
        return "utc", utc_value

    if representation == "timezone_aware":
        aware_value = metadata.timezone_aware_timestamp
        if aware_value is None:
            raise ValueError(
                "timezone_aware representation requires timezone_aware_timestamp"
            )
        return "utc", aware_value.astimezone(timezone.utc)

    return "naive", metadata.naive_timestamp


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


def build_metadata_diagnostics(
    candidates: tuple[NormalizedMetadata, ...],
) -> MetadataDiagnostics:
    sorted_candidates = tuple(
        sorted(
            candidates,
            key=lambda item: (
                item.timestamp_source,
                _primary_representation(item),
                item.naive_timestamp.isoformat(),
                item.timezone_aware_timestamp.isoformat()
                if item.timezone_aware_timestamp is not None
                else "",
                item.utc_timestamp.isoformat() if item.utc_timestamp is not None else "",
            ),
        )
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


def extract_jpeg_normalized_metadata(path: Path, mtime_timestamp: float) -> NormalizedMetadata:
    timestamp, source = extract_timestamp(path, mtime_timestamp)
    return normalize_metadata(
        ExtractedMetadata(
            naive_timestamp=timestamp,
            timestamp_source=source,
        )
    )