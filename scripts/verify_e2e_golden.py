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
    assert_exact_match,
    fixture_ids,
    golden_dir,
    scenario_outputs,
)

EXPECTED_FILES = (
    "default.console.txt",
    "default.json",
    "context.console.txt",
    "context.json",
    "models.json",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", help="Single fixture id to verify")
    parser.add_argument("--all", action="store_true", help="Verify all fixtures")
    return parser.parse_args()


def selected_fixture_ids(args: argparse.Namespace) -> tuple[str, ...]:
    if args.fixture and args.all:
        raise E2EError("Use either --fixture or --all, not both")

    if args.fixture:
        return (args.fixture,)

    if args.all:
        return fixture_ids()

    raise E2EError("Specify either --fixture <id> or --all")


def main() -> int:
    args = parse_args()

    for fixture_id in selected_fixture_ids(args):
        actual_outputs = scenario_outputs(fixture_id=fixture_id)
        expected_dir = golden_dir(fixture_id)

        for filename in EXPECTED_FILES:
            assert_exact_match(
                actual=actual_outputs[filename],
                expected_path=expected_dir / filename,
            )

        print(f"Verified fixture: {fixture_id}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
