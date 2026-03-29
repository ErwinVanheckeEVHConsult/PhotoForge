# PhotoForge v0.1 — Implementation Plan

## Principles

- Follow `SPEC.md` exactly, no redesign, no feature creep
- Build strictly bottom-up
- Each step must be testable in isolation
- No filesystem mutation before dry-run is correct
- Determinism is mandatory at every stage

## Implementation Order

1. `model.py`
2. `exif.py`
3. `hashing.py`
4. `scanner.py`
5. `planner.py`
6. `reporter.py`
7. Wire dry-run `cli.py`
8. `operations.py`
9. Wire `--apply`

## Milestones

### 1. Model Layer (`model.py`)

Define all dataclasses:

- `FileRecord`
- `PlannedRecord`
- `PlannedAction`
- `PlanResult`

Rules:

- Use `Path`, not `str`
- No business logic
- No optional fields unless specified

Test:

- Instantiation works
- No mutable defaults

### 2. EXIF Extraction (`exif.py`)

Implement:

- EXIF parsing
- Fallback chain:
  1. `DateTimeOriginal`
  2. `DateTimeDigitized`
  3. `DateTime`
  4. `mtime`

Returns:

- `(datetime, timestamp_source)`

Test:

- All fallback paths
- Invalid EXIF handled
- Correct source labels

### 3. Hashing (`hashing.py`)

Implement:

- SHA-256 full file hashing

Test:

- Known hash values
- Empty file
- Output format, 64-character lowercase hex

### 4. Scanner — Discovery + Enrichment (`scanner.py`)

Implement:

- Recursive file discovery
- Supported file filtering, JPEG only
- Deterministic ordering
- Metadata extraction, size and mtime timestamp
- Timestamp extraction via EXIF module
- Hash computation
- Build complete `FileRecord`

Test:

- Unsupported files skipped
- Errors are per-file, non-fatal
- Deterministic output
- Identical files produce identical hash

### 5. Planner — Grouping + Canonical Selection (`planner.py`)

Implement:

- Group by `sha256`
- Deterministic ordering
- Canonical selection

Ranking key:

```python
(-record.size, 0 if record.timestamp_source != "mtime" else 1, str(record.path))
