# PhotoForge v0.3 Specification

Status: LOCKED  
Version: 0.3.0  
Date: 2026-04-13  

This document defines the exact behavior of PhotoForge v0.3.  
All implementations must strictly follow this specification.  

If behavior is not explicitly defined here, it is considered out of scope.

---

## 1. Overview

PhotoForge v0.3 is a deterministic command-line tool that scans a directory of JPEG images, detects exact duplicates, identifies corrupt files, and generates a canonical rename and organization plan based on EXIF timestamps and fixed rules.

It can optionally apply the plan through safe file renaming and moving operations.

v0.3 extends v0.2 with deterministic corrupt file detection and reporting.

---

## 2. CLI Interface

### Command

photoforge `<input_path> [--output <output_path>] [--json] [--apply]`

### Arguments

`<input_path>` (required)  
Path to the root directory to scan recursively.

### Flags

`--output <output_path>`  
Target root directory for organized files.  
If not provided, files are renamed in place.  
If the path does not exist, it is allowed and will be created during apply.

`--json`  
Outputs the execution report in JSON format.  
If present, console output is replaced by JSON output.

`--apply`  
Executes file rename/move operations.  
If absent, runs in dry-run mode (default).

---

## 3. Supported File Formats

Only the following file extensions are processed:

- .jpg  
- .jpeg  

Rules:

- Extension matching is case-insensitive  
- All output files must use the .jpg extension (lowercase)  
- All other file types are ignored  

---

## 4. Directory Scanning

- The input directory is scanned recursively  
- Symbolic links are ignored  
- Only regular files with supported extensions are processed  
- Files that cannot be accessed are treated as errors  

### Corrupt File Detection

A file is classified as **corrupt** if it cannot be fully and successfully processed through the pipeline.

A file is considered corrupt if any of the following occurs:

- File cannot be read completely (I/O failure)
- File cannot be fully hashed
- File content is invalid for processing (e.g. malformed JPEG)

Rules:

- Corrupt classification must be deterministic  
- Same file must always produce the same classification  
- No heuristic or probabilistic detection is allowed  

Behavior:

- Corrupt files must not produce FileRecord objects  
- Corrupt files must be tracked separately  
- Processing must continue for all other files  

---

## 5. Timestamp Extraction Policy

Each valid file must be assigned a single canonical timestamp using the following fallback chain:

1. EXIF DateTimeOriginal  
2. EXIF DateTimeDigitized  
3. EXIF DateTime  
4. File modification time (mtime)  

### Normalization Rules

- EXIF timestamps must be parsed in the format: YYYY:MM:DD HH:MM:SS  
- Canonical timestamp format: YYYY-MM-DD HH:MM:SS  
- No timezone conversion is performed  
- All timestamps are treated as naive local time  
- Invalid EXIF values are treated as missing and trigger fallback  

---

## 6. Hashing Strategy

- Algorithm: SHA-256  
- Hash is computed on full file content  
- Full 64-character hex digest is used internally  
- Short hash = first 8 characters of SHA-256  

Files that cannot be fully hashed must be classified as corrupt.

---

## 7. Duplicate Grouping

- Files are grouped by identical SHA-256 hash  
- Each unique hash defines one group  
- Groups with more than one file are duplicate groups  
- Groups with a single file are still processed but not considered duplicates  

Corrupt files are excluded from grouping.

---

## 8. Canonical File Selection

Exactly one file per group is selected using:

1. Largest file size  
2. If equal, prefer EXIF timestamp over mtime  
3. If still equal, lexicographically smallest normalized absolute path  

Corrupt files are never considered for canonical selection.

---

## 9. Canonical Filename Format

Format:

YYYY-MM-DD_HHMMSS_`<short-hash>`.jpg

Rules:

- Timestamp comes from canonical timestamp  
- `<short-hash>` = first 8 characters of SHA-256  
- Extension is always .jpg (lowercase)  

Example:

2024-05-17_143211_ab12cd34.jpg

---

## 10. Target Path Resolution

If --output is not specified:

- Files are renamed in place  

If --output is specified:

- Files are moved to:

`<output_path>/<YYYY>/<MM>/<DD>/<filename>`

Rules:

- YYYY = four-digit year  
- MM = two-digit month (01–12)  
- DD = two-digit day (01–31)  
- Values are derived from canonical timestamp  
- No fallback or alternative structure is allowed  

---

## 11. Apply Behavior

### Default (Dry-Run)

- No file system changes  
- Full plan is computed and reported  

### With --apply

- Rename/move canonical files only  
- Create target directories if needed  
- Duplicate files are not modified  
- Corrupt files are not modified  
- No metadata changes  

---

## 12. Collision Handling Policy

If target path already exists:

- Do not overwrite  
- Skip operation  
- Record collision  

---

## 13. Dry-Run Behavior

- Dry-run is default  
- No files are modified  
- Output reflects exact actions that would occur  

---

## 14. Output and Reporting

### Console Output

Must include:

- Total files processed  
- Duplicate groups  
- Duplicate files  
- Planned actions (canonical files only)  
- Target paths  
- Timestamp source for each planned canonical action  
- Total corrupt files  

A dedicated section must list corrupt files including:

- file path  
- error type  

---

### JSON Output

Must include:

- summary  
- records list  
- actions  
- duplicate_group_id  
- duplicate_group_size  
- canonical flag  
- target path  
- action status  
- timestamp  
- timestamp_source  
- corrupt_files (list)  

Each corrupt file entry must include:

- path  
- error_type  

### Summary must include

- corrupt_file_count  

---

### Output Mode Rules

- Default output is console format  
- If --json is provided, only JSON output is produced  
- No mixed output modes are allowed  

---

## 15. Error Handling

### Non-Fatal Errors

- File unreadable  
- EXIF parsing failure  
- Hashing failure  

Behavior:

- File classified as corrupt if processing cannot complete  
- Issue recorded  
- Processing continues  

### Fatal Errors

- Invalid input path  
- Input path inaccessible  

---

## 16. IN SCOPE

- CLI operation  
- Recursive scanning  
- JPEG processing  
- EXIF timestamp extraction  
- SHA-256 hashing  
- Duplicate grouping  
- Deterministic canonical selection  
- Canonical naming  
- Year/month/day organization  
- Dry-run mode  
- Safe apply mode  
- Collision handling  
- Console reporting  
- JSON reporting  
- Timestamp source transparency  
- Corrupt file detection  
- Corrupt file reporting  

---

## 17. OUT OF SCOPE

- Perceptual duplicate detection  
- Non-JPEG formats  
- File deletion  
- Overwriting files  
- Metadata rewriting  
- Timezone normalization  
- Sidecar files  
- GUI  
- AI features  
- Cloud integration  
- Custom naming templates  
- Alternative folder structures  
- User-defined rules  
- File repair or recovery  

---

## 18. Determinism Requirement

For identical input:

- Same hashes  
- Same grouping  
- Same canonical selection  
- Same filenames  
- Same target paths  
- Same corrupt file classification  
- Same output  

No randomness allowed.
