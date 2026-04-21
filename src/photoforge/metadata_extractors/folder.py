# src/photoforge/metadata_extractors/folder.py

from __future__ import annotations

import re
from datetime import datetime
from typing import Final

from photoforge.model import TimestampCandidate


# Order within the same start position:
# range patterns before single-date patterns
_PATTERNS: Final[list[tuple[str, str]]] = [
    ("folder_yyyymmdd_range", r"(?<!\d)(\d{8})-(\d{8})(?!\d)"),
    ("folder_yyyy-mm-dd_range", r"(?<!\d)(\d{4}-\d{2}-\d{2})\s*-\s*(\d{4}-\d{2}-\d{2})(?!\d)"),
    ("folder_yyyymmdd", r"(?<!\d)(\d{8})(?!\d)"),
    ("folder_yyyy-mm-dd", r"(?<!\d)(\d{4}-\d{2}-\d{2})(?!\d)"),
]


def extract_folder_timestamp(folder_name: str) -> tuple[TimestampCandidate, ...]:
    matches: list[tuple[int, int, str, re.Match[str]]] = []

    for priority, (source_detail, pattern) in enumerate(_PATTERNS):
        for match in re.finditer(pattern, folder_name):
            matches.append((match.start(), priority, source_detail, match))

    if not matches:
        return ()

    matches.sort(key=lambda item: (item[0], item[1]))

    for _, _, source_detail, match in matches:
        try:
            dt = _parse_folder_date(match, source_detail)
            return (
                TimestampCandidate(
                    source_kind="folder",
                    source_detail=source_detail,
                    naive_timestamp=dt,
                    precision="date",
                    timezone_offset=None,
                ),
            )
        except ValueError:
            continue

    return ()


def _parse_folder_date(match: re.Match[str], source_detail: str) -> datetime:
    if source_detail == "folder_yyyymmdd":
        return _parse_compact_date(match.group(1))

    if source_detail == "folder_yyyy-mm-dd":
        return _parse_dashed_date(match.group(1))

    if source_detail == "folder_yyyymmdd_range":
        return _parse_compact_date(match.group(1))

    if source_detail == "folder_yyyy-mm-dd_range":
        return _parse_dashed_date(match.group(1))

    raise ValueError(f"unsupported source_detail: {source_detail}")


def _parse_compact_date(date_part: str) -> datetime:
    year = int(date_part[0:4])
    month = int(date_part[4:6])
    day = int(date_part[6:8])
    return datetime(year, month, day, 0, 0, 0)


def _parse_dashed_date(date_part: str) -> datetime:
    year_text, month_text, day_text = date_part.split("-")
    year = int(year_text)
    month = int(month_text)
    day = int(day_text)
    return datetime(year, month, day, 0, 0, 0)