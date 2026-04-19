# src/photoforge/metadata_extractors/jpeg.py

from __future__ import annotations

from pathlib import Path

from ..model import TimestampCandidate
from .exif import extract_exif_timestamp_candidates
from .filesystem import extract_filesystem_timestamp_candidates


def extract_jpeg_timestamp(
    path: Path,
    mtime_timestamp: float,
) -> tuple[TimestampCandidate, ...]:
    return (
        *extract_exif_timestamp_candidates(path),
        *extract_filesystem_timestamp_candidates(path, mtime_timestamp),
    )