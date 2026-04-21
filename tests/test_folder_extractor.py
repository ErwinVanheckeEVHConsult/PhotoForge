# tests/test_folder_extractor.py

from datetime import datetime

from photoforge.metadata_extractors.folder import extract_folder_timestamp


def test_single_date_compact() -> None:
    result = extract_folder_timestamp("20240102")
    assert len(result) == 1
    candidate = result[0]
    assert candidate.source_kind == "folder"
    assert candidate.source_detail == "folder_yyyymmdd"
    assert candidate.naive_timestamp == datetime(2024, 1, 2, 0, 0, 0)
    assert candidate.precision == "date"
    assert candidate.timezone_offset is None


def test_single_date_dashed() -> None:
    result = extract_folder_timestamp("2024-01-02")
    assert len(result) == 1
    candidate = result[0]
    assert candidate.source_detail == "folder_yyyy-mm-dd"
    assert candidate.naive_timestamp == datetime(2024, 1, 2, 0, 0, 0)


def test_range_compact_uses_start_date_only() -> None:
    result = extract_folder_timestamp("20240102-20240105")
    assert len(result) == 1
    candidate = result[0]
    assert candidate.source_detail == "folder_yyyymmdd_range"
    assert candidate.naive_timestamp == datetime(2024, 1, 2, 0, 0, 0)


def test_range_dashed_uses_start_date_only() -> None:
    result = extract_folder_timestamp("2024-01-02 - 2024-01-05")
    assert len(result) == 1
    candidate = result[0]
    assert candidate.source_detail == "folder_yyyy-mm-dd_range"
    assert candidate.naive_timestamp == datetime(2024, 1, 2, 0, 0, 0)


def test_range_beats_single_date_when_same_start_position() -> None:
    result = extract_folder_timestamp("20240102-20240105")
    assert len(result) == 1
    assert result[0].source_detail == "folder_yyyymmdd_range"


def test_left_to_right_first_match_wins() -> None:
    result = extract_folder_timestamp("20240102 misc 20240103-20240104")
    assert len(result) == 1
    assert result[0].source_detail == "folder_yyyymmdd"
    assert result[0].naive_timestamp == datetime(2024, 1, 2, 0, 0, 0)


def test_invalid_numeric_values_are_rejected() -> None:
    result = extract_folder_timestamp("20241302")
    assert result == ()


def test_boundary_rules_are_enforced() -> None:
    result = extract_folder_timestamp("x120240102")
    assert result == ()


def test_no_valid_pattern_returns_no_candidate() -> None:
    result = extract_folder_timestamp("holiday_photos")
    assert result == ()