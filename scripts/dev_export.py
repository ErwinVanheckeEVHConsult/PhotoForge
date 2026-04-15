from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TREE_OUTPUT = PROJECT_ROOT / "tree-src.txt"
GIT_OUTPUT = PROJECT_ROOT / "git-status.txt"


def generate_tree():
    root = PROJECT_ROOT / "src" / "photoforge"

    lines: list[str] = []

    for path in sorted(root.rglob("*"), key=lambda p: str(p).lower()):
        if "__pycache__" in path.parts:
            continue

        relative = path.relative_to(root)
        indent = "    " * (len(relative.parts) - 1)
        lines.append(f"{indent}{relative.name}")

    TREE_OUTPUT.write_text("\n".join(lines), encoding="utf-8")


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
        output_lines.append("No staged changes")
    else:
        output_lines.extend(staged)

    # Optional: keep the rest of the status below (recommended)
    if filtered:
        output_lines.append("")
        output_lines.append("Other changes:")
        output_lines.extend(filtered)

    GIT_OUTPUT.write_text("\n".join(output_lines), encoding="utf-8")


def main():
    generate_tree()
    generate_git_status()


if __name__ == "__main__":
    main()