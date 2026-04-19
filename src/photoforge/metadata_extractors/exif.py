# src/photoforge/metadata_extractors/exif.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from ..model import TimestampCandidate

_EXIF_DATETIME_TAGS: tuple[tuple[int, str], ...] = (
    (36867, "exif_datetimeoriginal"),
    (36868, "exif_datetimedigitized"),
    (306, "exif_datetime"),
)

_EXIF_DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"


def extract_exif_timestamp_candidates(path: Path) -> tuple[TimestampCandidate, ...]:
    exif = _read_exif(path)
    candidates: list[TimestampCandidate] = []

    for tag_id, source_detail in _EXIF_DATETIME_TAGS:
        value = exif.get(tag_id)
        parsed = _parse_exif_datetime(value)
        if parsed is None:
            continue

        candidates.append(
            TimestampCandidate(
                source_kind="exif",
                source_detail=source_detail,
                naive_timestamp=parsed,
                precision="datetime",
                timezone_offset=None,
            )
        )

    return tuple(candidates)


def _read_exif(path: Path) -> dict[int, object]:
    try:
        with Image.open(path) as image:
            exif = image.getexif()
            if not exif:
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