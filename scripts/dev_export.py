from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parent.parent

#TREE_OUTPUT = PROJECT_ROOT / "tree-src.txt"
GIT_OUTPUT = PROJECT_ROOT / "git-status.txt"


def generate_tree(subdir:str) -> None:
    treeoutput = PROJECT_ROOT / f"tree-{subdir}.txt"    
    root = PROJECT_ROOT / subdir

    lines: list[str] = []

    def walk(directory: Path, depth: int) -> None:
        entries = sorted(directory.iterdir(), key=lambda p: str(p).lower())

        for entry in entries:
            if "__pycache__" in entry.parts:
                continue
            
            if "photoforge.egg-info" in entry.parts:
                continue

            if subdir=="ProjectDocs" and entry.name in {"milestones", "planning-proposals", "templates"}:
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


def main():
    generate_tree("src")
    generate_tree("ProjectDocs")
    generate_git_status()


if __name__ == "__main__":
    main()