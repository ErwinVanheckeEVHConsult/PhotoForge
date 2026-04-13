from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class FileRecord:
    path: Path
    size: int
    timestamp: datetime
    timestamp_source: str
    sha256: str
    short_hash: str


@dataclass(frozen=True)
class CorruptFile:
    path: Path
    error_type: str


@dataclass(frozen=True)
class PlannedRecord:
    path: Path
    duplicate_group_id: str
    duplicate_group_size: int
    canonical: bool
    canonical_filename: str
    target_path: Path | None
    action_status: str
    sha256: str
    short_hash: str
    timestamp: datetime
    timestamp_source: str


@dataclass(frozen=True)
class PlannedAction:
    source_path: Path
    target_path: Path
    action: str


@dataclass(frozen=True)
class PlanResult:
    records: tuple[PlannedRecord, ...]
    actions: tuple[PlannedAction, ...]
    corrupt_files: tuple[CorruptFile, ...]