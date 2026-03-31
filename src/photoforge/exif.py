from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PIL import Image, UnidentifiedImageError


_EXIF_DATETIME_TAGS: tuple[tuple[int, str], ...] = (
    (36867, "exif_datetimeoriginal"),
    (36868, "exif_datetimedigitized"),
    (306, "exif_datetime"),
)

_EXIF_DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"


def extract_timestamp(path: Path, mtime_timestamp: float) -> tuple[datetime, str]:
    exif = _read_exif(path)

    for tag_id, source in _EXIF_DATETIME_TAGS:
        value = exif.get(tag_id)
        parsed = _parse_exif_datetime(value)
        if parsed is not None:
            return parsed, source

    return datetime.fromtimestamp(mtime_timestamp), "mtime"


def _read_exif(path: Path) -> dict[int, object]:
    try:
        with Image.open(path) as image:
            exif = image.getexif()
            if exif is None:
                return {}
            return dict(exif)
    except (OSError, UnidentifiedImageError):
        return {}


def _parse_exif_datetime(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None

    try:
        return datetime.strptime(value, _EXIF_DATETIME_FORMAT)
    except ValueError:
        return None