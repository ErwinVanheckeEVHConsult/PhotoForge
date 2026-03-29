# PhotoForge – Planner Core (v0.1)

## Purpose

The planner is the core deterministic engine of PhotoForge.

It transforms a list of scanned file records into a complete, immutable execution plan.

The planner is responsible for:

- grouping files by identical content (SHA-256)
- selecting a canonical file per group
- generating canonical filenames
- resolving target paths
- assigning actions (rename, move, skip, collision)
- producing a final plan used for reporting and execution

The planner does **not**:

- scan the filesystem
- extract EXIF data
- compute hashes
- modify files


---

## Input

The planner consumes a list of `FileRecord`.

### FileRecord

    @dataclass(frozen=True)
    class FileRecord:
        path: Path
        size: int
        timestamp: datetime
        timestamp_source: str
        sha256: str
        short_hash: str

### Requirements

- `path` must be a normalized absolute `Path`
- `sha256` must be a full 64-character hex digest
- `short_hash` must be the first 8 characters of `sha256`
- `timestamp` must already be resolved using the extraction fallback chain
- `timestamp_source` must be one of:

    exif_datetimeoriginal
    exif_datetimedigitized
    exif_datetime
    mtime


---

## Output

The planner returns a `PlanResult`.

    @dataclass(frozen=True)
    class PlanResult:
        records: list[PlannedRecord]
        actions: list[PlannedAction]


---

## PlannedRecord

Represents one file in the plan.

    @dataclass(frozen=True)
    class PlannedRecord:
        path: Path
        duplicate_group_id: str
        duplicate_group_size: int
        canonical: bool
        canonical_filename: str
        target_path: Path | None
        action_status: str
        sha256: str
        short_hash: str
        timestamp: datetime
        timestamp_source: str

### Rules

- Every input file produces exactly one `PlannedRecord`
- `duplicate_group_id` = SHA-256
- `duplicate_group_size` = number of files sharing the same hash
- `canonical` is `True` for exactly one file per group
- `target_path` is:
  - set only for canonical files
  - `None` for duplicates
- `action_status` is one of:

    rename
    move
    skip
    collision
    duplicate


---

## PlannedAction

Represents an action for canonical files only.

    @dataclass(frozen=True)
    class PlannedAction:
        source_path: Path
        target_path: Path
        action: str

### Rules

- Only canonical files produce actions
- Duplicates never produce actions
- `action` is one of:

    rename
    move
    skip
    collision


---

## Planner Pipeline

The planner must execute the following steps in order.


### 1. Sort Input

Sort all `FileRecord` by:

    path (lexicographically)

This guarantees deterministic behavior.


### 2. Group by SHA-256

Group records by `sha256`.

Rules:

- one group per unique hash
- groups sorted by hash (lexicographically)
- records inside each group sorted by path


### 3. Select Canonical File

For each group, select exactly one canonical file using strict tie-breakers:

1. largest file size
2. prefer EXIF timestamp over `mtime`
3. lexicographically smallest path

### EXIF Preference Rule

A timestamp is considered EXIF if:

    timestamp_source != "mtime"

### Ranking Key

Canonical selection must use:

    (-size, exif_priority, path)

Where:

    exif_priority = 0 if timestamp_source != "mtime" else 1

Canonical = minimum of this key.


### 4. Generate Canonical Filename

For the canonical file:

    YYYY-MM-DD_HHMMSS_<short-hash>.jpg

Rules:

- derived from canonical timestamp
- always lowercase `.jpg`
- no variation allowed


### 5. Resolve Target Path

#### In-place mode (no output path)

    target = source.parent / canonical_filename

#### Organized mode (`--output`)

    target = output_path / YYYY / canonical_filename

Where:

    YYYY = timestamp.strftime("%Y")


### 6. Classify Action

Only canonical files are evaluated.

Decision order:

1. if source_path == target_path → skip
2. if target_path.exists() → collision
3. if no output_path → rename
4. otherwise → move


### 7. Assign Duplicate Behavior

For all non-canonical files:

- `canonical = False`
- `target_path = None`
- `action_status = "duplicate"`

Duplicates are never modified.


### 8. Build Plan Records

For each file:

- populate `PlannedRecord`
- include:
  - group id
  - group size
  - canonical flag
  - timestamp and source
  - canonical filename
  - action status


### 9. Build Actions

For each canonical file:

- create one `PlannedAction`
- include:
  - source path
  - target path
  - action type

Duplicates produce no actions.


### 10. Final Ordering

- `records` sorted by `path`
- `actions` sorted by `source_path`


---

## Determinism Guarantees

The planner must produce identical output given identical input.

This is enforced by:

- sorting input records
- sorting groups by hash
- sorting records within groups
- deterministic canonical selection
- deterministic filename generation
- strict action decision order


---

## Constraints (v0.1)

- JPEG only
- SHA-256 exact matching only
- no perceptual hashing
- no file deletion
- no overwriting existing files
- no concurrency
- no database
- no plugins
- no optional behavior


---

## Implementation Notes

- Use `pathlib.Path` for all path handling
- Convert to string only in reporting layer
- Planner should remain mostly pure
- Filesystem access is limited to collision detection (`target_path.exists()`)


---

## Summary

The planner is a pure, deterministic transformation:

    FileRecord[] → PlanResult

It defines **what should happen**, not **how it is executed**.

This separation ensures:

- safety (dry-run by default)
- testability
- reproducibility
- simplicity
