from __future__ import annotations

import argparse
from pathlib import Path

from .scanner import scan_directory
from .planner import plan_files
from .reporter import render_console_report
from .operations import apply_actions


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="photoforge",
        description="PhotoForge v0.1 - deterministic photo deduplication",
    )
    parser.add_argument(
        "input_path",
        metavar="input_path",
        help="Path to the directory to scan",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Execute planned filesystem changes",
    )
    return parser


def validate_input_path(raw_input_path: str) -> Path:
    path = Path(raw_input_path).expanduser()

    if not path.exists():
        raise ValueError(f"Input path does not exist: {path}")

    if not path.is_dir():
        raise ValueError(f"Input path is not a directory: {path}")

    return path.resolve()


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    input_path = validate_input_path(args.input_path)

    scan_result = scan_directory(input_path)
    plan_result = plan_files(scan_result.records)
    report = render_console_report(plan_result)

    # Must always print report before any filesystem changes
    print(report)

    if args.apply:
        apply_actions(plan_result.actions)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())