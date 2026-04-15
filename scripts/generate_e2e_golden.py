from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from tests.e2e.helpers import (
    E2EError,
    ensure_golden_dir,
    fixture_ids,
    scenario_outputs,
    write_text_atomic,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", help="Single fixture id to generate")
    parser.add_argument("--all", action="store_true", help="Generate all fixtures")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Required explicit flag to write golden files",
    )
    return parser.parse_args()


def selected_fixture_ids(args: argparse.Namespace) -> tuple[str, ...]:
    if args.fixture and args.all:
        raise E2EError("Use either --fixture or --all, not both")

    if not args.write:
        raise E2EError("Refusing to write without explicit --write")

    if args.fixture:
        return (args.fixture,)

    if args.all:
        return fixture_ids()

    raise E2EError("Specify either --fixture <id> or --all")


def main() -> int:
    args = parse_args()

    for fixture_id in selected_fixture_ids(args):
        outputs = scenario_outputs(fixture_id=fixture_id)
        target_dir = ensure_golden_dir(fixture_id)

        for filename, content in outputs.items():
            write_text_atomic(target_dir / filename, content)

        print(f"Wrote golden outputs for fixture: {fixture_id}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
