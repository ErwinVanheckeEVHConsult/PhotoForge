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

Business logic is intentionally not implemented yet.

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

## Notes

- Dry-run is the default mode
- `--apply` enables filesystem changes
- `--output` selects a target root for organized files
- `--json` enables JSON report output in addition to standard console output
