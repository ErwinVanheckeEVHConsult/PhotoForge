# Changelog

All notable changes to this project will be documented in this file.

The format is simple and human-readable.
Versions follow semantic versioning where applicable.

---

## [0.4.0-alpha1] - 2026-04-14

### Added v0.4

- Development workflow definition
- Reusable templates for:
  - planning proposals
  - milestones
  - milestone checklists
  - release checklists
  - changelog entries

### Changed v0.4

- Standardized project lifecycle (planning → milestones → validation → release)

### Notes v0.4

- No runtime behavior changes
- This release introduces workflow and documentation only

---

## [0.3.0-alpha1] - 2026-04-13

### Added v0.3

- Deterministic corrupt file detection during scanning
- Explicit corrupt file classification
- Corrupt file propagation through planning pipeline
- Corrupt file reporting in console output
- Corrupt file reporting in JSON output

### Changed v0.3

- Summary now includes corrupt file count
- Console output includes dedicated corrupt file section
- JSON output includes corrupt_files collection

### Notes v0.3

- Corrupt files are excluded from duplicate grouping and planning
- No filesystem operations are performed on corrupt files

---

## [0.2.0-alpha1] - 2026-04-13

### Added v0.2

- Optional output directory support via --output
- Deterministic JSON output mode via --json
- Timestamp source included in console report output

### Changed v0.2

- Output directory structure when using --output now follows:
  `<output>/<year>/<month>/<day>/<filename>`

### Fixed v0.2

-

---

## [0.1.0-alpha1] - 2026-04-01

### Added v0.1

- Initial implementation of PhotoForge
- JPEG scanning with EXIF timestamp extraction
- SHA-256 duplicate detection
- Deterministic canonical selection
- Canonical filename generation
- Dry-run mode
- Apply mode (safe rename/move)
- CLI interface

### Notes v0.1

- First alpha release
- Intended for testing and feedback
