from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="photoforge",
        description=(
            "Scan a directory of JPEG files, detect exact duplicates, and "
            "generate a deterministic rename and organization plan."
        ),
    )

    parser.add_argument(
        "input_path",
        type=Path,
        help="Path to the root directory to scan recursively.",
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Execute file rename/move operations. Default is dry-run.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        metavar="output_path",
        help=(
            "Target root directory for organized files. "
            "If omitted, files are renamed in place."
        ),
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help=(
            "Output the execution report in JSON format in addition to "
            "standard console output."
        ),
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Placeholder behavior for scaffold phase
    print(
        f"[PHOTOFORGE] input_path={args.input_path} "
        f"apply={args.apply} output={args.output} json={args.json}"
    )

    return 0
