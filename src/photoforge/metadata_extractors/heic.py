# metadata_extractors/heic.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def extract_heic_timestamp(path: Path, mtime_timestamp: float) -> tuple[datetime, str]:
    """
    Deterministic HEIC / HEIF timestamp extraction for MS025.

    Current behavior:
    - no embedded HEIC/HEIF metadata is read yet
    - fallback is explicitly and deterministically file mtime

    Inputs that affect output:
    - file format path (HEIC/HEIF extractor selected by caller)
    - provided mtime_timestamp

    The path parameter is accepted for interface consistency and future use.
    """
    _ = path
    return datetime.fromtimestamp(mtime_timestamp), "mtime"