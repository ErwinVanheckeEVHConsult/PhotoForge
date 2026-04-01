# PhotoForge

PhotoForge is a deterministic command-line tool for scanning JPEG files, extracting timestamps from EXIF metadata, detecting exact duplicates using SHA-256, and generating a canonical rename and organization plan.

Version `0.0.1` is a packaging scaffold aligned with the locked v0.1 CLI shape.

## Specification

See [SPEC.md](./SPEC.md) for the locked v0.1 behavior contract.

## Scope

PhotoForge v0.1 is defined around the following command shape:

```bash
photoforge <input_path> [--apply] [--output <output_path>] [--json]
```

Current scaffold includes:

- installable Python package
- `src/` layout
- CLI entry point
- argument parsing only

Core v0.1 functionality is implemented, including scanning, planning, reporting, and apply mode.

## Supported file formats

Planned v0.1 support is limited to JPEG files only:

- `.jpg`
- `.jpeg`

## Installation

```bash
pip install .
```

For editable development install:

```bash
pip install -e .
```

## Usage

Show help:

```bash
photoforge --help
```

Dry-run against an input directory:

```bash
photoforge /path/to/input
```

Apply changes:

```bash
photoforge /path/to/input --apply
```

Write organized output to a target root:

```bash
photoforge /path/to/input --output /path/to/output
```

Emit JSON report in addition to standard console output:

```bash
photoforge /path/to/input --json
```

Combine flags:

```bash
photoforge /path/to/input --apply --output /path/to/output --json
```

## ⚠️ Safety Warning (Beta)

PhotoForge can perform real filesystem modifications when used with `--apply`.

Before using `--apply`, you **must understand the following**:

- Files may be **renamed and/or moved** based on the generated plan  
- Operations are executed **exactly as planned**, without additional prompts  
- **No files are overwritten**, but existing files may cause collisions and skipped actions  
- Duplicate files are **not deleted**, but only canonical files are acted upon  
- The tool assumes **full control over the target paths** it generates  

### Recommendations

- Always run a **dry-run first** and review the report carefully  
- Test on a **copy of your data**, not your primary photo library  
- Verify results on a **small subset** before scaling up  
- Use backups or versioning if operating on important data  

> This is a beta release. Behavior is deterministic but not yet hardened against all real-world edge cases.

## Notes

- Dry-run is the default mode
- `--apply` enables filesystem changes
- `--output` selects a target root for organized files
- `--json` enables JSON report output in addition to standard console output
