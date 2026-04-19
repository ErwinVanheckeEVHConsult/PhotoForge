from __future__ import annotations

from datetime import datetime
from pathlib import Path

from ..metadata import ExtractedMetadata


def extract_raw_timestamp(path: Path, mtime_timestamp: float) -> ExtractedMetadata:
    _ = path
    return ExtractedMetadata(
        naive_timestamp=datetime.fromtimestamp(mtime_timestamp),
        timestamp_source="mtime",
    )