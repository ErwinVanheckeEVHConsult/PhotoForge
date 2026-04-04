# PhotoForge

PhotoForge is a deterministic command-line tool for scanning JPEG files, extracting timestamps from EXIF metadata, detecting exact duplicates using SHA-256, and generating a canonical rename plan.

The tool is designed to be predictable, safe, and reproducible, with a strict dry-run-first workflow.

---

## Version

Current version: v0.1.0-alpha1

This release establishes the core deterministic pipeline:
- scanning
- timestamp extraction
- hashing
- duplicate grouping
- canonical selection
- planned filesystem operations

---

## Specification

See SPEC.md for the locked v0.1 behavior contract.

All behavior in this version is fully deterministic and defined there.

---

## Scope (v0.1)

PhotoForge v0.1 supports the following command:

```
photoforge <input_path> [--apply]
```

### Behavior

- Scans a directory recursively
- Processes JPEG files only (.jpg, .jpeg)
- Extracts timestamps using a strict EXIF fallback chain
- Computes SHA-256 hashes for exact duplicate detection
- Selects a single canonical file per duplicate group
- Generates a deterministic rename plan

---

## Installation

```
pip install .
```

For development:

```
pip install -e .
```

---

## Usage

### Show help

```
photoforge --help
```

### Dry-run (default)

```
photoforge /path/to/input
```

- No filesystem changes are made
- A full plan is printed to stdout

### Apply changes

```
photoforge /path/to/input --apply
```

- Executes the planned rename/move operations
- Only canonical files are affected
- Duplicate files remain untouched

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

No other output formats are supported in v0.1.

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

## Roadmap (Post v0.1)

Planned future capabilities include:

- JSON output mode (--json)
- Custom output directory (--output)
- Extended file format support (PNG, HEIC, RAW, video)
- Advanced duplicate detection (perceptual hashing)
- Metadata-based organization (camera, location, events)

---

## Notes

- This release focuses on a minimal, reliable core
- All additional features are deferred to future versions
- Backward compatibility will be preserved as the CLI evolves