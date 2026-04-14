from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .exif import extract_timestamp


@dataclass(frozen=True)
class NormalizedMetadata:
    """Format-agnostic metadata structure for pipeline-relevant fields only.

    This abstraction is intentionally minimal and passive for MS024.
    It mirrors the current pipeline contract without introducing any new
    behavior, fields, or format-specific logic.
    """

    timestamp: datetime
    timestamp_source: str


def build_normalized_metadata(timestamp: datetime, timestamp_source: str) -> NormalizedMetadata:
    """Adapt existing timestamp values into the normalized metadata structure."""

    return NormalizedMetadata(
        timestamp=timestamp,
        timestamp_source=timestamp_source,
    )


def extract_jpeg_normalized_metadata(path: Path, mtime_timestamp: float) -> NormalizedMetadata:
    """Wrap existing JPEG EXIF extraction without modifying its behavior.

    This function is intentionally not wired into the active pipeline in MS024.
    It exists only to establish the future abstraction boundary.
    """

    timestamp, timestamp_source = extract_timestamp(path, mtime_timestamp)
    return build_normalized_metadata(timestamp, timestamp_source)
