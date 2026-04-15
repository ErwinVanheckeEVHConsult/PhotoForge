# metadata_extractors/png.py
 
from __future__ import annotations

from datetime import datetime
from pathlib import Path


def extract_png_timestamp(path: Path, mtime_timestamp: float) -> tuple[datetime, str]:
    """
    Deterministic PNG timestamp extraction for MS025.

    Current behavior:
    - no embedded PNG metadata is read yet
    - fallback is explicitly and deterministically file mtime

    Inputs that affect output:
    - file format path (PNG extractor selected by caller)
    - provided mtime_timestamp

    The path parameter is accepted for interface consistency and future use.
    """
    _ = path
    return datetime.fromtimestamp(mtime_timestamp), "mtime"