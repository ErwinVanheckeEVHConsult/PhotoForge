# src/photoforge/model.py

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


@dataclass(frozen=True)
class TimestampCandidate:
    source_kind: str
    source_detail: str
    naive_timestamp: datetime
    precision: str
    timezone_offset: timedelta | None = None

    def __post_init__(self) -> None:
        if self.source_kind == "":
            raise ValueError("source_kind must not be empty")

        if self.source_detail == "":
            raise ValueError("source_detail must not be empty")

        if self.naive_timestamp.tzinfo is not None:
            raise ValueError("naive_timestamp must be naive")

        if self.precision not in {"date", "datetime"}:
            raise ValueError("precision must be 'date' or 'datetime'")


@dataclass(frozen=True)
class TimestampResolutionResult:
    primary_candidate: TimestampCandidate
    valid_candidates: tuple[TimestampCandidate, ...]

    def __post_init__(self) -> None:
        if not self.valid_candidates:
            raise ValueError("valid_candidates must not be empty")

        if self.primary_candidate != self.valid_candidates[0]:
            raise ValueError(
                "primary_candidate must be the first item in valid_candidates"
            )


@dataclass(frozen=True)
class TimestampComparison:
    left_source: str
    right_source: str
    representation: str
    left_value: datetime
    right_value: datetime
    equal: bool

    def __post_init__(self) -> None:
        if self.left_source == "":
            raise ValueError("left_source must not be empty")

        if self.right_source == "":
            raise ValueError("right_source must not be empty")

        if self.representation not in {"utc", "naive"}:
            raise ValueError("representation must be 'utc' or 'naive'")


@dataclass(frozen=True)
class MetadataDiagnostics:
    comparisons: tuple[TimestampComparison, ...]
    inconsistent_pairs: tuple[TimestampComparison, ...]

    def __post_init__(self) -> None:
        comparison_set = set(self.comparisons)
        for comparison in self.inconsistent_pairs:
            if comparison not in comparison_set:
                raise ValueError(
                    "inconsistent_pairs must be a subset of comparisons"
                )

    @property
    def has_inconsistency(self) -> bool:
        return bool(self.inconsistent_pairs)


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


@dataclass(frozen=True)
class ContextualGroup:
    group_id: str
    member_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        validate_member_refs(self.member_refs)

        expected_group_id = compute_group_id(self.member_refs)
        if self.group_id != expected_group_id:
            raise ValueError(
                "ContextualGroup.group_id does not match the computed group_id"
            )


@dataclass(frozen=True)
class ContextualGrouping:
    groups: tuple[ContextualGroup, ...]

    def __post_init__(self) -> None:
        group_ids = tuple(group.group_id for group in self.groups)

        if len(set(group_ids)) != len(group_ids):
            raise ValueError(
                "ContextualGrouping.groups must contain unique group_id values"
            )

        sorted_group_ids = tuple(sorted(group_ids))
        if group_ids != sorted_group_ids:
            raise ValueError(
                "ContextualGrouping.groups must be sorted lexicographically by group_id"
            )


def to_record_ref(file_record: FileRecord) -> str:
    return str(file_record.path)


def validate_record_ref(record_ref: str) -> None:
    if record_ref == "":
        raise ValueError("record_ref must not be empty")


def _encode_member_refs(member_refs: tuple[str, ...]) -> bytes:
    return json.dumps(
        member_refs,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")


def compute_group_id(member_refs: tuple[str, ...]) -> str:
    """Compute deterministic group_id from canonical JSON encoding of member_refs."""
    validate_member_refs(member_refs)
    canonical_json = _encode_member_refs(member_refs)
    return hashlib.sha256(canonical_json).hexdigest()


def validate_member_refs(member_refs: tuple[str, ...]) -> None:
    if not member_refs:
        raise ValueError("member_refs must not be empty")

    for record_ref in member_refs:
        validate_record_ref(record_ref)

    sorted_member_refs = tuple(sorted(member_refs))
    if member_refs != sorted_member_refs:
        raise ValueError("member_refs must be sorted lexicographically")

    if len(set(member_refs)) != len(member_refs):
        raise ValueError("member_refs must contain unique record_ref values")


def validate_contextual_group(group: ContextualGroup) -> None:
    validate_member_refs(group.member_refs)

    expected_group_id = compute_group_id(group.member_refs)
    if group.group_id != expected_group_id:
        raise ValueError(
            "ContextualGroup.group_id must match the deterministic group_id computed from member_refs"
        )


def validate_contextual_grouping(grouping: ContextualGrouping) -> None:
    group_ids = tuple(group.group_id for group in grouping.groups)

    if len(set(group_ids)) != len(group_ids):
        raise ValueError(
            "ContextualGrouping.groups must contain unique group_id values"
        )

    sorted_group_ids = tuple(sorted(group_ids))
    if group_ids != sorted_group_ids:
        raise ValueError(
            "ContextualGrouping.groups must be sorted lexicographically by group_id"
        )

    seen_record_refs: set[str] = set()
    for group in grouping.groups:
        validate_contextual_group(group)

        overlapping_record_refs = seen_record_refs.intersection(group.member_refs)
        if overlapping_record_refs:
            raise ValueError(
                "ContextualGrouping.groups must not contain duplicate record_ref values across groups"
            )

        seen_record_refs.update(group.member_refs)