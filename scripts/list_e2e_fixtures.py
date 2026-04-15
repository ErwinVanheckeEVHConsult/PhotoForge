from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from tests.e2e.helpers import fixture_ids


def main() -> int:
    for fixture_id in fixture_ids():
        print(fixture_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
