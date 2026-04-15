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

def normalize_metadata(
    timestamp: datetime,
    timestamp_source: str,
) -> NormalizedMetadata:
    """Enforce deterministic metadata structure.

    This function is the single normalization entry point.
    It performs validation only and must not introduce any transformation,
    inference, or fallback behavior.
    """
    
    if not isinstance(timestamp, datetime): # type: ignore[unnecessary-isinstance]
        raise TypeError("timestamp must be a datetime")

    if timestamp.tzinfo is not None and timestamp.utcoffset() is not None:
        raise TypeError("timestamp must be naive")
    
    if not isinstance(timestamp_source, str): # type: ignore[unnecessary-isinstance]
        raise TypeError("timestamp_source must be a string")
    
    if not timestamp_source:
        raise ValueError("timestamp_source must not be empty")
    
    # No transformation allowed
    # No timezone conversion
    # No fallback
    # No mutation

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
    return normalize_metadata(timestamp, timestamp_source)