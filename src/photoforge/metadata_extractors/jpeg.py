from __future__ import annotations

from datetime import datetime
from pathlib import Path

from ..exif import extract_timestamp


def extract_jpeg_timestamp(path: Path, mtime_timestamp: float) -> tuple[datetime, str]:
    return extract_timestamp(path, mtime_timestamp)