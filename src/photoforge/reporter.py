from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence, cast

from .model import ContextualGrouping, PlanResult
from .version import VERSION


def build_summary(plan_result: PlanResult) -> dict[str, int]:
    records = tuple(plan_result.records)
    actions = tuple(plan_result.actions)
    corrupt_files = tuple(plan_result.corrupt_files)

    total_files_processed = len(records)
    duplicate_groups = sum(
        1 for record in records if record.canonical and record.duplicate_group_size > 1
    )
    total_duplicates = sum(1 for record in records if not record.canonical)

    planned_renames = sum(1 for action in actions if action.action == "rename")
    planned_moves = sum(1 for action in actions if action.action == "move")
    planned_skips = sum(1 for action in actions if action.action == "skip")
    collisions = sum(1 for action in actions if action.action == "collision")

    corrupt_file_count = len(corrupt_files)

    return {
        "total_files_processed": total_files_processed,
        "duplicate_groups": duplicate_groups,
        "total_duplicates": total_duplicates,
        "planned_renames": planned_renames,
        "planned_moves": planned_moves,
        "planned_skips": planned_skips,
        "collisions": collisions,
        "corrupt_file_count": corrupt_file_count,
    }


def render_console_report(
    plan_result: PlanResult,
    contextual_grouping: ContextualGrouping | None = None,
    include_context: bool = False,
) -> str:
    if include_context and contextual_grouping is None:
        raise ValueError(
            "contextual_grouping must be provided when include_context=True"
        )

    summary = build_summary(plan_result)
    lines: list[str] = []

    lines.append(f"PhotoForge {VERSION}")
    lines.append("Mode: dry-run")
    lines.append("")
    lines.append("Summary")
    lines.append(f"  Total files processed: {summary['total_files_processed']}")
    lines.append(f"  Duplicate groups: {summary['duplicate_groups']}")
    lines.append(f"  Total duplicates: {summary['total_duplicates']}")
    lines.append(f"  Planned renames: {summary['planned_renames']}")
    lines.append(f"  Planned moves: {summary['planned_moves']}")
    lines.append(f"  Planned skips: {summary['planned_skips']}")
    lines.append(f"  Collisions: {summary['collisions']}")
    lines.append(f"  Corrupt files: {summary['corrupt_file_count']}")
    lines.append("")
    lines.append("Planned actions")

    canonical_records = [record for record in plan_result.records if record.canonical]
    if not canonical_records:
        lines.append("  None")
    else:
        for record in canonical_records:
            lines.append(f"  [{record.action_status}]")
            lines.append(f"    source: {record.path}")
            lines.append(f"    target: {record.target_path}")
            lines.append(f"    timestamp source: {record.timestamp_source}")

    lines.append("")
    lines.append("Corrupt files")

    if not plan_result.corrupt_files:
        lines.append("  None")
    else:
        for corrupt_file in plan_result.corrupt_files:
            lines.append(f"  {corrupt_file.error_type}")
            lines.append(f"    path: {corrupt_file.path}")

    if include_context:
        assert contextual_grouping is not None

        lines.append("")
        lines.append("Contextual groups")

        if not contextual_grouping.groups:
            lines.append("  None")
        else:
            for group in contextual_grouping.groups:
                lines.append(f"  {group.group_id}")
                for record_ref in group.member_refs:
                    lines.append(f"    {record_ref}")

    return "\n".join(lines)


def render_json_report(
    plan_result: PlanResult,
    contextual_grouping: ContextualGrouping | None = None,
    include_context: bool = False,
) -> str:
    if include_context and contextual_grouping is None:
        raise ValueError(
            "contextual_grouping must be provided when include_context=True"
        )

    payload: dict[str, Any] = {
        "summary": build_summary(plan_result),
        "records": [_to_jsonable(record) for record in plan_result.records],
        "actions": [_to_jsonable(action) for action in plan_result.actions],
        "corrupt_files": [_to_jsonable(cf) for cf in plan_result.corrupt_files],
    }

    if include_context:
        assert contextual_grouping is not None
        payload["contextual_groups"] = [
            {
                "group_id": group.group_id,
                "member_refs": list(group.member_refs),
            }
            for group in contextual_grouping.groups
        ]

    return json.dumps(payload, indent=2, sort_keys=True)


def _to_jsonable(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        dataclass_dict = asdict(value)
        return {key: _to_jsonable(item) for key, item in dataclass_dict.items()}

    if isinstance(value, dict):
        mapping_value = cast(Mapping[Any, Any], value)
        return {str(key): _to_jsonable(item) for key, item in mapping_value.items()}

    if isinstance(value, (list, tuple)):
        sequence_value = cast(Sequence[Any], value)
        return [_to_jsonable(item) for item in sequence_value]

    if isinstance(value, Path):
        return str(value)

    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    return value