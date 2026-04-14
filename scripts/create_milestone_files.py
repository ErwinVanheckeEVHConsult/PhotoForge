from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


MILESTONE_HEADING_RE = re.compile(
    r"^###\s+MS(?P<number>\d{3})\s+—\s+(?P<title>[a-z0-9-]+)\s*$"
)


@dataclass(frozen=True)
class MilestoneDefinition:
    number: str
    short_title: str
    description_lines: tuple[str, ...]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/create_milestone_files.py <milestones-md>")
        return 1

    source_path = Path(sys.argv[1])
    if not source_path.exists():
        print(f"Error: file not found: {source_path}")
        return 1

    version = extract_version(source_path.name)
    if version is None:
        print("Error: filename must be vXXX.XXX-milestones.md")
        return 1

    content = source_path.read_text(encoding="utf-8")
    milestones = parse_milestones(content)

    target_dir = Path("ProjectDocs") / "milestones"
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"Version: {version}")
    print(f"Milestones found: {len(milestones)}\n")

    for ms in milestones:
        milestone_file = target_dir / f"{version}-ms{ms.number}-{ms.short_title}.md"
        checklist_file = target_dir / f"{version}-ms{ms.number}-checklist.md"

        create_empty_file(milestone_file)
        create_empty_file(checklist_file)

        print(f"MS{ms.number} — {ms.short_title}")
        for line in ms.description_lines:
            print(f"  {line}")
        print()

    return 0


def extract_version(filename: str) -> str | None:
    match = re.fullmatch(r"(v\d{3}\.\d{3})-milestones\.md", filename)
    return match.group(1) if match else None


def parse_milestones(content: str) -> list[MilestoneDefinition]:
    lines = content.splitlines()

    milestones: list[MilestoneDefinition] = []
    current_number = None
    current_title = None
    current_desc: list[str] = []

    for raw_line in lines:
        line = raw_line.rstrip()

        # Detect new milestone
        m = MILESTONE_HEADING_RE.match(line)
        if m:
            if current_number is not None and current_title is not None:
                milestones.append(
                    MilestoneDefinition(
                        current_number,
                        current_title,
                        tuple(current_desc),
                    )
                )
            current_number = m.group("number")
            current_title = m.group("title")
            current_desc = []
            continue

        if current_number is None:
            continue

        stripped = line.strip()

        # Skip separators
        if stripped == "---":
            continue

        # Capture all bullet levels
        if stripped.startswith("- "):
            current_desc.append(stripped)

    # Final milestone
    if current_number is not None and current_title is not None:
        milestones.append(
            MilestoneDefinition(
                current_number,
                current_title,
                tuple(current_desc),
            )
        )

    return milestones


def create_empty_file(path: Path) -> None:
    if path.exists():
        print(f"⚠ Skipped: {path}")
        return
    path.touch()
    print(f"✅ Created: {path}")


if __name__ == "__main__":
    raise SystemExit(main())