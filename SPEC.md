# PhotoForge Specification

Status: Accepted  
Version: v0.5.0
Date: 2026-04-15  

This document defines the exact behavior of PhotoForge as implemented.

Implementation is the source of truth.
This specification must reflect actual behavior.

---

## 1. Overview

PhotoForge is a deterministic command-line tool that:

- scans a directory
- extracts and normalizes metadata
- detects exact duplicates (SHA-256)
- identifies corrupt files
- generates a canonical rename and organization plan
- optionally produces contextual grouping output

All behavior is deterministic.

---

## 2. CLI Interface

### Command

```bash
photoforge <input_path> [--output <output_path>] [--json] [--apply] [--context]
```

### Flags

- `--output <output_path>`
- `--json`
- `--apply`
- `--context` (include contextual grouping in output only)

---

## 3. Pipeline Execution

The system executes the following pipeline:

``
scan_directory(input_path) -> ScanResult

CLI:
    derive CorruptFile from ScanResult.skipped

run_pipeline(...):
    plan_files(records, corrupt_files) -> PlanResult
    compute_contextual_grouping(records) -> ContextualGrouping

reporter(...):
    render output
``

---

## 4. File Classification

The scanner classifies files into:

### 4.1 Processable

- `.jpg`
- `.jpeg`

These files are fully processed into `FileRecord`.

---

### 4.2 Recognized but Not Processable

- `.png`, `.heic`, `.heif`
- `.cr2`, `.nef`, `.arw`
- `.mp4`, `.mov`

Behavior:

- recorded as skipped
- not processed further
- not considered corrupt

---

### 4.3 Unsupported

- all other file types

Behavior:

- recorded as skipped
- not processed further

---

## 5. Corrupt File Definition

A file is corrupt if it is processable but cannot be fully processed.

Corrupt conditions:

- metadata unreadable
- timestamp cannot be resolved
- file unreadable
- hashing failure

Behavior:

- no `FileRecord` is created
- file is recorded as skipped with reason `corrupt_*`
- `ScanIssue` is recorded

---

## 6. Corrupt File Propagation

Corrupt files are transformed into `CorruptFile` objects.

Transformation rule:

``
CorruptFile.path = SkippedFile.path
CorruptFile.error_type = SkippedFile.reason
``

Selection rule:

- include only `SkippedFile.reason` values starting with `"corrupt_"`

Notes:

- transformation occurs at CLI layer
- `ScanIssue` is diagnostic only and not used for transformation

---

## 7. Metadata Extraction

Timestamp fallback chain:

1. EXIF `DateTimeOriginal`
2. EXIF `DateTimeDigitized`
3. EXIF `DateTime`
4. filesystem `mtime`

Rules:

- timestamps are naive
- invalid EXIF values are ignored
- `mtime` is valid fallback

---

## 8. Hashing

- SHA-256 over full file content
- lowercase hex digest
- short hash = first 8 characters

---

## 9. Duplicate Grouping

- files grouped by identical SHA-256
- one group per unique hash
- groups sorted deterministically

---

## 10. Canonical Selection

Exactly one file per group is selected using:

1. largest size
2. prefer EXIF timestamp over `mtime`
3. lexicographically smallest path

---

## 11. Canonical Filename

``
YYYY-MM-DD_HHMMSS_<short-hash>.jpg
``

---

## 12. Target Path Resolution

### In-place

``
source.parent / filename
``

### Output mode

``
output/YYYY/MM/DD/filename
``

---

## 13. Action Classification

For canonical files:

- `skip`
- `collision`
- `rename`
- `move`

For duplicates:

- `duplicate`

---

## 14. Planner Output

Planner returns:

``
PlanResult:
    records
    actions
    corrupt_files
``

Rules:

- corrupt files do not produce records
- corrupt files do not produce actions
- corrupt files do not affect planning

---

## 15. Contextual Grouping

Contextual grouping:

- operates on `FileRecord` set
- produces `ContextualGrouping`
- independent from duplicate grouping
- does not affect planning

Included in output only when:

``
--context
``

---

## 16. Reporting

Output modes:

- console (default)
- JSON (`--json`)

Includes:

- summary
- records
- actions
- corrupt_files
- contextual_groups (optional)

---

## 17. Apply Behavior

Default: dry-run

With `--apply`:

- execute actions for canonical files only
- duplicates are not modified
- corrupt files are not modified
- no overwrite allowed

---

## 18. Determinism

For identical input:

- identical scan results
- identical grouping
- identical planning
- identical output

No randomness allowed.

---

## 19. Constraints

- JPEG processing only
- exact duplicate detection only
- no perceptual hashing
- no file deletion
- no overwrite
- no concurrency
- no external state
