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
        print("Usage: python scripts/create_milestone_files.py <path-to-milestones-md>")
        return 1

    source_path = Path(sys.argv[1])
    if not source_path.exists():
        print(f"Error: file does not exist: {source_path}")
        return 1

    version = extract_version_from_filename(source_path.name)
    if version is None:
        print(
            "Error: source filename must match 'v<mmm>.<nnn>-milestones.md', "
            f"got: {source_path.name}"
        )
        return 1

    content = source_path.read_text(encoding="utf-8")
    milestones = parse_milestones(content)

    if not milestones:
        print("Error: no milestones found.")
        return 1

    target_dir = Path("ProjectDocs") / "milestones"
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"Version: {version}")
    print(f"Found {len(milestones)} milestone(s).")
    print()

    for milestone in milestones:
        milestone_filename = (
            f"{version}-ms{milestone.number}-{milestone.short_title}.md"
        )
        checklist_filename = f"{version}-ms{milestone.number}-checklist.md"

        milestone_path = target_dir / milestone_filename
        checklist_path = target_dir / checklist_filename

        create_empty_file(milestone_path)
        create_empty_file(checklist_path)

        print(f"MS{milestone.number} — {milestone.short_title}")
        for line in milestone.description_lines:
            print(f"  {line}")
        print()

    return 0


def extract_version_from_filename(filename: str) -> str | None:
    match = re.fullmatch(r"(v\d{3}\.\d{3})-milestones\.md", filename)
    if match is None:
        return None
    return match.group(1)


def parse_milestones(content: str) -> list[MilestoneDefinition]:
    lines = content.splitlines()
    milestones: list[MilestoneDefinition] = []

    current_number: str | None = None
    current_title: str | None = None
    current_description: list[str] = []

    for raw_line in lines:
        line = raw_line.rstrip()
        heading_match = MILESTONE_HEADING_RE.match(line)

        if heading_match is not None:
            if current_number is not None and current_title is not None:
                milestones.append(
                    MilestoneDefinition(
                        number=current_number,
                        short_title=current_title,
                        description_lines=tuple(current_description),
                    )
                )

            current_number = heading_match.group("number")
            current_title = heading_match.group("title")
            current_description = []
            continue

        if current_number is None:
            continue

        if line.startswith("### "):
            continue

        if line.strip() == "":
            continue

        if line.startswith("- "):
            current_description.append(line)

    if current_number is not None and current_title is not None:
        milestones.append(
            MilestoneDefinition(
                number=current_number,
                short_title=current_title,
                description_lines=tuple(current_description),
            )
        )

    return milestones


def create_empty_file(path: Path) -> None:
    if path.exists():
        print(f"⚠ Skipped (exists): {path}")
        return

    path.touch()
    print(f"✅ Created: {path}")


if __name__ == "__main__":
    raise SystemExit(main())
