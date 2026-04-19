# src/photoforge/metadata_extractors/heic.py

from __future__ import annotations

from pathlib import Path

from ..model import TimestampCandidate
from .filesystem import extract_filesystem_timestamp_candidates


def extract_heic_timestamp(
    path: Path,
    mtime_timestamp: float,
) -> tuple[TimestampCandidate, ...]:
    return extract_filesystem_timestamp_candidates(path, mtime_timestamp)