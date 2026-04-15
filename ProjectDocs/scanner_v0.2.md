# PhotoForge v0.1 — Scanner Pipeline Specification

## Purpose

The scanner pipeline is responsible for discovering files, enriching supported JPEG files into complete `FileRecord` objects, and reporting skipped files and errors.

The scanner does **not**:

- modify files
- plan actions
- infer duplicates
- generate filenames

It produces fully enriched, deterministic input for the planner.

---

## High-Level Pipeline

For a given input directory:

1. Validate input path
2. Recursively discover all files
3. Filter supported JPEG files
4. Normalize paths
5. Read file metadata (size, mtime)
6. Extract canonical timestamp (via EXIF fallback chain)
7. Compute SHA-256 hash
8. Construct `FileRecord`
9. Record skipped files and errors
10. Return scan result

---

## Detailed Pipeline

### 1. Input Validation

Before scanning:

- Resolve input path to absolute `Path`
- Verify:
  - path exists
  - path is accessible
  - path is a directory

If any check fails:

→ **Fatal error (abort execution)**

---

### 2. File Discovery

Function:

~~~python
discover_files(input_path: Path) -> list[Path]
~~~

Behavior:

- Recursively walk directory tree
- Include only:
  - regular files
- Exclude:
  - symbolic links
  - non-regular files
- Normalize all paths to absolute `Path`
- Sort lexicographically

Output:

→ deterministic list of all files

---

### 3. Supported File Filtering

Function:

~~~python
is_supported_file(path: Path) -> bool
~~~

Supported formats (strict):

- `.jpg`
- `.jpeg`
- case-insensitive

Behavior:

- If supported → continue pipeline
- If not supported:
  - add `SkippedFile(reason="unsupported_extension")`
  - do not process further

---

### 4. Path Normalization

Function:

~~~python
normalize_path(path: Path) -> Path
~~~

Rules:

- must be absolute
- must be normalized
- no string paths inside the model

---

### 5. File Metadata Extraction

Function:

~~~python
get_file_size_and_mtime(path: Path) -> tuple[int, float]
~~~

Returns:

- `size: int` (bytes)
- `mtime_timestamp: float` (POSIX timestamp)

Failure:

- unreadable metadata → **error + skipped**

---

### 6. Timestamp Extraction (EXIF)

Handled by `exif.py`

Function:

~~~python
extract_timestamp(path: Path, mtime_timestamp: float) -> tuple[datetime, str]
~~~

Fallback chain (strict order):

1. EXIF `DateTimeOriginal`
2. EXIF `DateTimeDigitized`
3. EXIF `DateTime`
4. filesystem `mtime`

Normalization:

- EXIF format must be: `YYYY:MM:DD HH:MM:SS`
- Convert to naive `datetime`
- No timezone handling
- Invalid EXIF values are ignored (fallback continues)

Returned:

- `timestamp: datetime`
- `timestamp_source: str`

Allowed `timestamp_source` values:

- `exif_datetimeoriginal`
- `exif_datetimedigitized`
- `exif_datetime`
- `mtime`

Important:

- EXIF failure is **not an error** if fallback succeeds
- `mtime` is always valid fallback

---

### 7. Hashing

Handled by `hashing.py`

Function:

~~~python
compute_sha256(path: Path) -> str
~~~

Rules:

- SHA-256 only
- Full file content
- Lowercase hex digest
- 64 characters

Short hash:

~~~python
short_hash = sha256[:8]
~~~

Failure:

- hashing failure → **error + skipped**

---

### 8. FileRecord Construction

A `FileRecord` is created only if all steps succeed.

Fields:

- `path: Path`
- `size: int`
- `timestamp: datetime`
- `timestamp_source: str`
- `sha256: str`
- `short_hash: str`

No partial records are allowed.

---

### 9. Error Handling

#### Fatal Errors (abort)

- invalid input path
- inaccessible input path
- input is not a directory

---

#### Non-Fatal Per-File Errors

Continue scanning:

- metadata unreadable
- timestamp cannot be resolved
- hashing failure
- file cannot be opened

Behavior:

- do not create `FileRecord`
- add `SkippedFile`
- add `ScanIssue(severity="error")`
- continue

---

#### EXIF Behavior

- missing EXIF → not an error
- invalid EXIF → not an error
- fallback to mtime → valid

No warnings required in v0.1.

---

#### Unsupported Files

- not an error
- recorded as skipped

---

#### Symbolic Links

- ignored
- recorded as skipped

---

## Reporting Model

### Skipped Files

~~~python
@dataclass(frozen=True)
class SkippedFile:
    path: Path
    reason: str
~~~

Reason values:

- `unsupported_extension`
- `symlink`
- `not_regular_file`
- `metadata_unreadable`
- `timestamp_unresolved`
- `hash_failed`

---

### Issues (Errors Only in v0.1)

~~~python
@dataclass(frozen=True)
class ScanIssue:
    path: Path
    severity: str  # "error"
    code: str
    message: str
~~~

Examples:

- `metadata_unreadable`
- `hash_failed`
- `file_unreadable`

---

### Scan Result

~~~python
@dataclass(frozen=True)
class ScanResult:
    records: list[FileRecord]
    skipped: list[SkippedFile]
    issues: list[ScanIssue]
    total_entries_seen: int
    supported_files_processed: int
~~~

---

## Determinism Rules

- discovered files sorted lexicographically
- skipped files sorted by path
- issues sorted by path then code
- no randomness allowed

---

## Scanner Responsibility Boundary

### scanner.py

- orchestration
- discovery
- filtering
- metadata reading
- calling EXIF + hashing
- constructing `FileRecord`
- collecting diagnostics

---

### exif.py

- EXIF reading
- timestamp parsing
- fallback logic
- timestamp normalization

---

### hashing.py

- SHA-256 computation only

---

## Final Contract

`scan_directory(input_path)` must:

1. validate input
2. discover all files
3. filter supported JPEG files
4. enrich valid files into complete `FileRecord`
5. collect skipped + errors
6. return deterministic `ScanResult`

Only fully valid `FileRecord` objects are passed to the planner.

No exceptions.
No ambiguity.
No partial data.
