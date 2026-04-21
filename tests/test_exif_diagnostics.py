from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest

import photoforge.metadata_extractors.exif as exif_module


def test_extract_exif_diagnostics_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_load_exif(path: Path) -> tuple[str, dict[int, object]]:
        _ = path
        return ("missing", {})

    monkeypatch.setattr(exif_module, "_load_exif", fake_load_exif)

    result = exif_module.extract_exif_diagnostics(Path("dummy.jpg"))

    assert len(result) == 1
    assert result[0].source_kind == "exif"
    assert result[0].diagnostic_type == "missing"
    assert result[0].field_name is None


def test_extract_exif_diagnostics_unreadable(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_load_exif(path: Path) -> tuple[str, dict[int, object]]:
        _ = path
        return ("unreadable", {})

    monkeypatch.setattr(exif_module, "_load_exif", fake_load_exif)

    result = exif_module.extract_exif_diagnostics(Path("dummy.jpg"))

    assert len(result) == 1
    assert result[0].diagnostic_type == "unreadable"


def test_extract_exif_metadata_reports_invalid_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_exif: dict[int, object] = {
        36867: "not-a-timestamp",
        36881: "+99:99",
        36868: "2024:01:02 03:04:05",
        36882: "+02:30",
    }

    def fake_load_exif(path: Path) -> tuple[str, dict[int, object]]:
        _ = path
        return ("ok", fake_exif)

    monkeypatch.setattr(exif_module, "_load_exif", fake_load_exif)

    candidates, diagnostics = exif_module.extract_exif_metadata(Path("dummy.jpg"))

    assert len(candidates) == 1
    assert candidates[0].source_detail == "exif_datetimedigitized"
    assert candidates[0].naive_timestamp == datetime(2024, 1, 2, 3, 4, 5)
    assert candidates[0].timezone_offset == timedelta(hours=2, minutes=30)

    assert tuple((d.diagnostic_type, d.field_name) for d in diagnostics) == (
        ("invalid", "exif_datetimeoriginal"),
    )