# tests/test_filename_extractor.py

from datetime import datetime

from photoforge.metadata_extractors.filename import extract_filename_timestamp


def test_full_pattern_compact() -> None:
    result = extract_filename_timestamp("IMG_20240102_030405.jpg")
    assert len(result) == 1
    c = result[0]
    assert c.naive_timestamp == datetime(2024, 1, 2, 3, 4, 5)
    assert c.precision == "datetime"


def test_full_pattern_dashed() -> None:
    result = extract_filename_timestamp("photo_2024-01-02_03-04-05.png")
    assert result[0].naive_timestamp == datetime(2024, 1, 2, 3, 4, 5)


def test_full_pattern_space() -> None:
    result = extract_filename_timestamp("2024-01-02 03-04-05 file.txt")
    assert result[0].naive_timestamp == datetime(2024, 1, 2, 3, 4, 5)


def test_date_only_compact() -> None:
    result = extract_filename_timestamp("backup_20240102.zip")
    assert result[0].naive_timestamp == datetime(2024, 1, 2, 0, 0, 0)
    assert result[0].precision == "date"


def test_date_only_dashed() -> None:
    result = extract_filename_timestamp("2024-01-02-report.pdf")
    assert result[0].naive_timestamp == datetime(2024, 1, 2, 0, 0, 0)


def test_full_over_date_priority() -> None:
    result = extract_filename_timestamp("20240102_030405_20240102.txt")
    assert result[0].precision == "datetime"


def test_invalid_date_rejected() -> None:
    result = extract_filename_timestamp("IMG_20241302_030405.jpg")
    assert result == ()


def test_boundary_enforced() -> None:
    result = extract_filename_timestamp("file_120240102_030405.txt")
    assert result == ()


def test_no_match() -> None:
    result = extract_filename_timestamp("file_without_date.txt")
    assert result == ()