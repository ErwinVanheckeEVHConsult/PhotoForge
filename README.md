# PhotoForge

PhotoForge is a deterministic command-line tool for scanning JPEG files, extracting timestamps from EXIF metadata, detecting exact duplicates using SHA-256, and generating a canonical rename plan.

The tool is designed to be predictable, safe, and reproducible, with a strict dry-run-first workflow.

---

## Version

Current version: v0.4.0-alpha1

This release establishes the core deterministic pipeline:

- scanning
- timestamp extraction
- hashing
- duplicate grouping
- canonical selection
- planned filesystem operations

---

## Specification

- See ./SPEC_v0.1.md for the v0.1 behavior contract.
- See ./SPEC_v0.2.md for the v0.2 behavior contract.
- See ./SPEC.md for the current behavior.

All runtime behavior remains identical to v0.3 and is fully defined there.

---

## Scope (v0.4)

PhotoForge v0.4 supports the following command:

```bash
photoforge <input_path> [--output <output_path>] [--json] [--apply]
```

### Behavior

- Scans a directory recursively
- Processes JPEG files only (.jpg, .jpeg)
- Extracts timestamps using a strict EXIF fallback chain
- Computes SHA-256 hashes for exact duplicate detection
- Selects a single canonical file per duplicate group
- Generates a deterministic rename plan
- Detects and reports corrupt files (excluded from processing)

---

## Installation

```bash
pip install .
```

For development:

```bash
pip install -e .
```

---

## Usage

### Show help

```bash
photoforge --help
```

### Dry-run (default)

```bash
photoforge /path/to/input
```

- No filesystem changes are made
- A full plan is printed to stdout

### Apply changes

```bash
photoforge /path/to/input --apply
```

- Executes the planned rename/move operations
- Only canonical files are affected
- Duplicate files remain untouched

### Output to structured directory

```bash
photoforge /path/to/input --output /path/to/output
```

### JSON Output

```bash
photoforge /path/to/input --json
```

---

## Output

The tool prints a deterministic console report including:

- total files processed
- number of duplicate groups
- total duplicates
- planned actions:
  - rename
  - skip
  - collision

Output modes:

- Default: deterministic human-readable console report
- Optional: deterministic JSON output via --json

---

## Supported File Formats

- .jpg
- .jpeg

---

## Safety Model

- Dry-run is the default mode
- No changes occur unless --apply is provided
- Files are never overwritten
- Collisions are detected and skipped
- Only canonical files are modified
- All operations are precomputed and visible before execution

---

## ⚠️ Safety Warning

When using --apply, PhotoForge performs real filesystem changes.

Before applying:

- Always run a dry-run first
- Review the planned actions carefully
- Test on a small subset of files
- Use backups for important data

This is an alpha release. Behavior is deterministic but not yet hardened against all edge cases.

---

## Design Principles

- Deterministic behavior (same input → same output)
- No hidden heuristics
- No implicit decisions
- Strict separation between planning and execution
- Fail-safe defaults

---

## Roadmap (Future)

Planned future capabilities include:

- Extended file format support (PNG, HEIC, RAW, video)
- Advanced duplicate detection (perceptual hashing)
- Metadata-based organization (camera, location, events)

---

## v0.4 Notes

v0.4 introduces no changes to runtime behavior.

This release standardizes the development workflow through:

- reusable templates
- deterministic documentation structure
- formalized release and validation process

All runtime behavior remains identical to v0.3.

---

## v0.3 Notes

- This release focuses on a minimal, reliable core
- All additional features are deferred to future versions
- Backward compatibility will be preserved as the CLI evolves
