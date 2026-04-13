# Changelog

All notable changes to this project will be documented in this file.

The format is simple and human-readable.
Versions follow semantic versioning where applicable.

---

## [Unreleased]

### Added

- Optional output directory support via --output
- Deterministic JSON output mode via --json
- Timestamp source included in console report output

### Changed

- Output directory structure when using --output now follows:
  `<output>/<year>/<month>/<day>/<filename>`

### Fixed

-

---

## [0.1.0-alpha1] - 2026-04-01

### Added

- Initial implementation of PhotoForge
- JPEG scanning with EXIF timestamp extraction
- SHA-256 duplicate detection
- Deterministic canonical selection
- Canonical filename generation
- Dry-run mode
- Apply mode (safe rename/move)
- CLI interface

### Notes

- First alpha release
- Intended for testing and feedback
