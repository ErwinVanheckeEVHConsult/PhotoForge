from pathlib import Path
import sys

if len(sys.argv) != 2:
    print("Usage: python scripts/create_version_files.py v000.005")
    sys.exit(1)

version = sys.argv[1]

base_dir = Path("ProjectDocs")
planning_dir = base_dir / "planning-proposals"
planning_dir.mkdir(parents=True, exist_ok=True)

files = [
    planning_dir / f"{version}-planning-proposal.md",
    planning_dir / f"{version}-release-checklist.md",
]

def create_file(path: Path) -> None:
    if path.exists():
        print(f"⚠️  Skipped (exists): {path}")
        return
    path.touch()
    print(f"✅ Created: {path}")

for file_path in files:
    create_file(file_path)