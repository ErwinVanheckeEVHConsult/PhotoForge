from __future__ import annotations

from pathlib import Path

from ..exif import extract_timestamp
from ..metadata import ExtractedMetadata


def extract_jpeg_timestamp(path: Path, mtime_timestamp: float) -> ExtractedMetadata:
    timestamp, source = extract_timestamp(path, mtime_timestamp)
    return ExtractedMetadata(
        naive_timestamp=timestamp,
        timestamp_source=source,
    )