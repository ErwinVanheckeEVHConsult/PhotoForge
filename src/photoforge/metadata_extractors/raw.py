# metadata_extractors/raw.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def extract_raw_timestamp(path: Path, mtime_timestamp: float) -> tuple[datetime, str]:
    """
    Deterministic RAW timestamp extraction for MS025.

    Supported later by caller-side extension routing, e.g.:
    - .cr2
    - .nef
    - .arw

    Current behavior:
    - no embedded RAW metadata is read yet
    - fallback is explicitly and deterministically file mtime

    Inputs that affect output:
    - file format path (RAW extractor selected by caller)
    - provided mtime_timestamp

    The path parameter is accepted for interface consistency and future use.
    """
    _ = path
    return datetime.fromtimestamp(mtime_timestamp), "mtime"