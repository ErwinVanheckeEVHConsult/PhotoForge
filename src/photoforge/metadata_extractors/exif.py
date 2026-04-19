from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from ..model import TimestampCandidate

_EXIF_DATETIME_TAGS: tuple[tuple[int, str, int], ...] = (
    (36867, "exif_datetimeoriginal", 36881),
    (36868, "exif_datetimedigitized", 36882),
    (306, "exif_datetime", 36880),
)

_EXIF_DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"


def extract_exif_timestamp_candidates(path: Path) -> tuple[TimestampCandidate, ...]:
    exif = _read_exif(path)
    candidates: list[TimestampCandidate] = []

    for timestamp_tag_id, source_detail, timezone_tag_id in _EXIF_DATETIME_TAGS:
        timestamp_value = exif.get(timestamp_tag_id)
        parsed_timestamp = _parse_exif_datetime(timestamp_value)
        if parsed_timestamp is None:
            continue

        timezone_value = exif.get(timezone_tag_id)
        parsed_timezone_offset = _parse_exif_offset(timezone_value)

        candidates.append(
            TimestampCandidate(
                source_kind="exif",
                source_detail=source_detail,
                naive_timestamp=parsed_timestamp,
                precision="datetime",
                timezone_offset=parsed_timezone_offset,
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


def _parse_exif_offset(value: object) -> timedelta | None:
    if not isinstance(value, str):
        return None

    if len(value) != 6:
        return None

    sign = value[0]
    if sign not in {"+", "-"}:
        return None

    if value[3] != ":":
        return None

    hour_text = value[1:3]
    minute_text = value[4:6]

    if not hour_text.isdigit() or not minute_text.isdigit():
        return None

    hours = int(hour_text)
    minutes = int(minute_text)

    if hours > 23 or minutes > 59:
        return None

    offset = timedelta(hours=hours, minutes=minutes)
    if sign == "-":
        offset = -offset

    return offset