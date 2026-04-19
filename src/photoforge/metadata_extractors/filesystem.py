# src/photoforge/metadata_extractors/filesystem.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from ..model import TimestampCandidate


def extract_filesystem_timestamp_candidates(
    path: Path,
    mtime_timestamp: float,
) -> tuple[TimestampCandidate, ...]:
    _ = path

    return (
        TimestampCandidate(
            source_kind="filesystem",
            source_detail="mtime",
            naive_timestamp=datetime.fromtimestamp(mtime_timestamp),
            precision="datetime",
        ),
    )