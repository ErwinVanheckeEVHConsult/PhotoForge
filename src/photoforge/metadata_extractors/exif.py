# src/photoforge/metadata_extractors/exif.py

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from ..model import ExtractionDiagnostic, TimestampCandidate

_EXIF_DATETIME_TAGS: tuple[tuple[int, str, int], ...] = (
    (36867, "exif_datetimeoriginal", 36881),
    (36868, "exif_datetimedigitized", 36882),
    (306, "exif_datetime", 36880),
)

_EXIF_DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"


def extract_exif_timestamp_candidates(path: Path) -> tuple[TimestampCandidate, ...]:
    candidates, _ = extract_exif_metadata(path)
    return candidates


def extract_exif_diagnostics(path: Path) -> tuple[ExtractionDiagnostic, ...]:
    _, diagnostics = extract_exif_metadata(path)
    return diagnostics


def extract_exif_metadata(
    path: Path,
) -> tuple[tuple[TimestampCandidate, ...], tuple[ExtractionDiagnostic, ...]]:
    status, exif = _load_exif(path)

    if status == "missing":
        return (), (ExtractionDiagnostic(source_kind="exif", diagnostic_type="missing"),)

    if status == "unreadable":
        return (), (ExtractionDiagnostic(source_kind="exif", diagnostic_type="unreadable"),)

    candidates: list[TimestampCandidate] = []
    diagnostics: list[ExtractionDiagnostic] = []

    for timestamp_tag_id, source_detail, timezone_tag_id in _EXIF_DATETIME_TAGS:
        timestamp_value = exif.get(timestamp_tag_id)

        if timestamp_value is None:
            continue

        parsed_timestamp = _parse_exif_datetime(timestamp_value)
        if parsed_timestamp is None:
            diagnostics.append(
                ExtractionDiagnostic(
                    source_kind="exif",
                    diagnostic_type="invalid",
                    field_name=source_detail,
                )
            )
            continue

        timezone_value = exif.get(timezone_tag_id)
        parsed_timezone_offset = _parse_exif_offset(timezone_value)

        if timezone_value is not None and parsed_timezone_offset is None:
            diagnostics.append(
                ExtractionDiagnostic(
                    source_kind="exif",
                    diagnostic_type="invalid",
                    field_name=f"{source_detail}_offset",
                )
            )

        candidates.append(
            TimestampCandidate(
                source_kind="exif",
                source_detail=source_detail,
                naive_timestamp=parsed_timestamp,
                precision="datetime",
                timezone_offset=parsed_timezone_offset,
            )
        )

    if not candidates and not diagnostics:
        diagnostics.append(
            ExtractionDiagnostic(
                source_kind="exif",
                diagnostic_type="missing",
            )
        )


    return tuple(candidates), tuple(diagnostics)


def _load_exif(path: Path) -> tuple[str, dict[int, object]]:
    try:
        with Image.open(path) as image:
            exif = image.getexif()
            if not exif:
                return "missing", {}
            return "ok", dict(exif)
    except (OSError, UnidentifiedImageError):
        return "unreadable", {}


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