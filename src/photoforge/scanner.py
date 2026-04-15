from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .exif import extract_timestamp
from .hashing import compute_sha256
from .model import FileRecord
from .metadata import normalize_metadata

PROCESSABLE_EXTENSIONS = {
    ".jpg", ".jpeg",
}

RECOGNIZED_EXTENSIONS = {
    ".png",
    ".heic", ".heif",
    ".cr2", ".nef", ".arw",
    ".mp4", ".mov",
}

SUPPORTED_EXTENSIONS = PROCESSABLE_EXTENSIONS | RECOGNIZED_EXTENSIONS


@dataclass(frozen=True)
class SkippedFile:
    path: Path
    reason: str


@dataclass(frozen=True)
class ScanIssue:
    path: Path
    severity: str
    code: str
    message: str


@dataclass(frozen=True)
class ScanResult:
    records: tuple[FileRecord, ...]
    skipped: tuple[SkippedFile, ...]
    issues: tuple[ScanIssue, ...]
    total_entries_seen: int
    supported_files_processed: int


def normalize_path(path: Path) -> Path:
    return path.resolve(strict=True)


def is_supported_file(path: Path) -> bool:
    return path.suffix.lower() in SUPPORTED_EXTENSIONS


def is_processable_file(path: Path) -> bool:
    return path.suffix.lower() in PROCESSABLE_EXTENSIONS


def is_recognized_file(path: Path) -> bool:
    return path.suffix.lower() in RECOGNIZED_EXTENSIONS


def discover_files(input_path: Path) -> tuple[Path, ...]:
    discovered: list[Path] = []

    for root, dirnames, filenames in os.walk(input_path, topdown=True, followlinks=False):
        dirnames.sort()
        filenames.sort()

        root_path = Path(root)
        for filename in filenames:
            discovered.append((root_path / filename).resolve(strict=False))

    return tuple(discovered)


def get_file_size_and_mtime(path: Path) -> tuple[int, float]:
    stat_result = path.stat()
    return stat_result.st_size, stat_result.st_mtime


def scan_directory(input_path: Path) -> ScanResult:
    root_path = _validate_input_directory(input_path)
    discovered_paths = discover_files(root_path)

    records: list[FileRecord] = []
    skipped: list[SkippedFile] = []
    issues: list[ScanIssue] = []

    for path in discovered_paths:
        if path.is_symlink():
            skipped.append(SkippedFile(path=path, reason="symlink"))
            continue

        if not path.is_file():
            skipped.append(SkippedFile(path=path, reason="not_regular_file"))
            continue

        if not is_supported_file(path):
            skipped.append(SkippedFile(path=path, reason="unsupported_extension"))
            continue

        if is_recognized_file(path):
            skipped.append(SkippedFile(path=path, reason="recognized_format_not_processable"))
            continue

        try:
            size, mtime_timestamp = get_file_size_and_mtime(path)
        except OSError as exc:
            _record_corrupt_file(
                skipped=skipped,
                issues=issues,
                path=path,
                reason="corrupt_metadata_unreadable",
                code="corrupt_metadata_unreadable",
                message=str(exc),
            )
            continue

        try:
            extracted_timestamp, extracted_timestamp_source = extract_timestamp(path, mtime_timestamp)

            normalized_metadata = normalize_metadata(
                extracted_timestamp,
                extracted_timestamp_source,
            )

        except Exception as exc:
            _record_corrupt_file(
                skipped=skipped,
                issues=issues,
                path=path,
                reason="corrupt_timestamp_unresolved",
                code="corrupt_timestamp_unresolved",
                message=str(exc),
            )
            continue

        try:
            sha256 = compute_sha256(path)
        except OSError as exc:
            _record_corrupt_file(
                skipped=skipped,
                issues=issues,
                path=path,
                reason="corrupt_file_unreadable",
                code="corrupt_file_unreadable",
                message=str(exc),
            )
            continue
        except Exception as exc:
            _record_corrupt_file(
                skipped=skipped,
                issues=issues,
                path=path,
                reason="corrupt_hash_failed",
                code="corrupt_hash_failed",
                message=str(exc),
            )
            continue

        records.append(
            FileRecord(
                path=path,
                size=size,
                timestamp=normalized_metadata.timestamp,
                timestamp_source=normalized_metadata.timestamp_source,
                sha256=sha256,
                short_hash=sha256[:8],
            )
        )

    return ScanResult(
        records=tuple(records),
        skipped=tuple(_sorted_skipped(skipped)),
        issues=tuple(_sorted_issues(issues)),
        total_entries_seen=len(discovered_paths),
        supported_files_processed=len(records),
    )


def _record_corrupt_file(
    skipped: list[SkippedFile],
    issues: list[ScanIssue],
    path: Path,
    reason: str,
    code: str,
    message: str,
) -> None:
    skipped.append(SkippedFile(path=path, reason=reason))
    issues.append(
        ScanIssue(
            path=path,
            severity="error",
            code=code,
            message=message,
        )
    )


def _validate_input_directory(input_path: Path) -> Path:
    try:
        normalized = normalize_path(input_path)
    except FileNotFoundError as exc:
        raise ValueError(f"Input path does not exist: {input_path}") from exc
    except OSError as exc:
        raise ValueError(f"Input path is not accessible: {input_path}") from exc

    if not normalized.is_dir():
        raise ValueError(f"Input path is not a directory: {normalized}")

    return normalized


def _sorted_skipped(items: Iterable[SkippedFile]) -> list[SkippedFile]:
    return sorted(items, key=lambda item: str(item.path))


def _sorted_issues(items: Iterable[ScanIssue]) -> list[ScanIssue]:
    return sorted(items, key=lambda item: (str(item.path), item.code))