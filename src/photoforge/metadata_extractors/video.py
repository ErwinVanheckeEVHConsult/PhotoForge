# metadata_extractors/video.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def extract_video_timestamp(path: Path, mtime_timestamp: float) -> tuple[datetime, str]:
    """
    Deterministic video timestamp extraction for MS025.

    Supported later by caller-side extension routing, e.g.:
    - .mp4
    - .mov

    Current behavior:
    - no embedded video metadata is read yet
    - fallback is explicitly and deterministically file mtime

    Inputs that affect output:
    - file format path (video extractor selected by caller)
    - provided mtime_timestamp

    The path parameter is accepted for interface consistency and future use.
    """
    _ = path
    return datetime.fromtimestamp(mtime_timestamp), "mtime"