from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .model import PlanResult


def build_summary(plan_result: PlanResult) -> dict[str, int]:
    records = tuple(plan_result.records)
    actions = tuple(plan_result.actions)

    total_files_processed = len(records)
    duplicate_groups = sum(1 for record in records if record.canonical and record.duplicate_group_size > 1)
    total_duplicates = sum(1 for record in records if not record.canonical)

    planned_renames = sum(1 for action in actions if action.action == "rename")
    planned_moves = sum(1 for action in actions if action.action == "move")
    planned_skips = sum(1 for action in actions if action.action == "skip")
    collisions = sum(1 for action in actions if action.action == "collision")

    return {
        "total_files_processed": total_files_processed,
        "duplicate_groups": duplicate_groups,
        "total_duplicates": total_duplicates,
        "planned_renames": planned_renames,
        "planned_moves": planned_moves,
        "planned_skips": planned_skips,
        "collisions": collisions,
    }


def render_console_report(plan_result: PlanResult) -> str:
    summary = build_summary(plan_result)
    lines: list[str] = []

    lines.append("PhotoForge v0.1")
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
    lines.append("")
    lines.append("Planned actions")

    actions = tuple(plan_result.actions)
    if not actions:
        lines.append("  None")
        return "\n".join(lines)

    for action in actions:
        lines.append(f"  [{action.action}]")
        lines.append(f"    source: {action.source_path}")
        lines.append(f"    target: {action.target_path}")

    return "\n".join(lines)


def render_json_report(plan_result: PlanResult) -> str:
    payload = {
        "summary": build_summary(plan_result),
        "records": [_to_jsonable(record) for record in plan_result.records],
        "actions": [_to_jsonable(action) for action in plan_result.actions],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def _to_jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _to_jsonable(item) for key, item in asdict(value).items()}

    if isinstance(value, dict):
        return {str(key): _to_jsonable(item) for key, item in value.items()}

    if isinstance(value, (list, tuple)):
        return [_to_jsonable(item) for item in value]

    if isinstance(value, Path):
        return str(value)

    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    return value