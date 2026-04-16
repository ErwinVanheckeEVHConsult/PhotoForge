from pathlib import Path
import subprocess
import tarfile
import pathspec

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXCLUDED_BY_ROOT = {
    "src": {"photoforge.egg-info"},
    "ProjectDocs": {"milestones", "planning-proposals", "templates"},
}

#TREE_OUTPUT = PROJECT_ROOT / "tree-src.txt"
GIT_OUTPUT = PROJECT_ROOT / "git-status.txt"

def load_gitignore() -> pathspec.PathSpec:
    gitignore = PROJECT_ROOT / ".gitignore"

    if not gitignore.exists():
        return pathspec.PathSpec.from_lines("gitwildmatch", [])

    patterns = gitignore.read_text(encoding="utf-8").splitlines()
    return pathspec.PathSpec.from_lines("gitwildmatch", patterns)


def generate_tree(subdir:str) -> None:
    excluded = EXCLUDED_BY_ROOT.get(subdir, set())
    treeoutput = PROJECT_ROOT / f"tree-{subdir}.txt"    
    root = PROJECT_ROOT / subdir

    lines: list[str] = []

    def walk(directory: Path, depth: int) -> None:
        entries = sorted(directory.iterdir(), key=lambda p: str(p).lower())

        for entry in entries:
            if "__pycache__" in entry.parts:
                continue
            
            if entry.name in excluded:
                continue

            indent = "    " * depth
            lines.append(f"{indent}{entry.name}")

            if entry.is_dir():
                walk(entry, depth + 1)

    walk(root, 0)

    treeoutput.write_text("\n".join(lines), encoding="utf-8")


def generate_git_status() -> None:
    result: subprocess.CompletedProcess[str] = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
    )

    all_lines: list[str] = result.stdout.splitlines()

    # Exclude untracked
    filtered: list[str] = [
        line for line in all_lines
        if not line.startswith("??")
    ]

    # Detect staged changes (index column != space)
    staged: list[str] = [
        line for line in filtered
        if len(line) > 0 and line[0] != " "
    ]

    output_lines: list[str] = []

    output_lines.append("Staged changes:")

    if not staged:
        output_lines.append("")
        output_lines.append("No staged changes")
    else:
        output_lines.extend(staged)

    # Optional: keep the rest of the status below (recommended)
    if filtered:
        output_lines.append("")
        unstaged: list[str] = [
            line for line in filtered
            if not (len(line) > 0 and line[0] != " ")
        ]

        if unstaged:
            output_lines.append("")
            output_lines.append("Unstaged changes:")
            output_lines.extend(unstaged)

    GIT_OUTPUT.write_text("\n".join(output_lines), encoding="utf-8")

def archive_markdown() -> None:
    source_root = PROJECT_ROOT
    tar_path = PROJECT_ROOT / "archive" / "markdown.tar.gz"

    excluded_roots = {
        PROJECT_ROOT / "ProjectDocs" / "milestones",
        PROJECT_ROOT / "ProjectDocs" / "planning-proposals",
        PROJECT_ROOT / "ProjectDocs" / "templates",
    }

    gitignore_spec = load_gitignore()

    files: list[Path] = sorted(
        source_root.rglob("*.md"),
        key=lambda p: str(p).lower(),
    )

    for source_path in files:
        relative_str = str(source_path.relative_to(source_root))

        # Apply .gitignore
        if gitignore_spec.match_file(relative_str):
            continue

    if tar_path.exists():
        tar_path.unlink()

    tar_path.parent.mkdir(parents=True, exist_ok=True)

    with tarfile.open(tar_path, "w:gz") as tar:
        for source_path in files:
            if any(source_path.is_relative_to(excluded) for excluded in excluded_roots):
                continue

            if "archive" in source_path.parts:
                continue

            arcname = source_path.relative_to(source_root)
            tar.add(source_path, arcname=arcname)

def main():
    generate_tree("src")
    generate_tree("ProjectDocs")
    generate_git_status()
    archive_markdown()

if __name__ == "__main__":
    main()