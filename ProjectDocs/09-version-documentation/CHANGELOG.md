# Changelog

All notable changes to this project will be documented in this file.

The format is simple and human-readable.
Versions follow semantic versioning where applicable.

---

## [0.5.0] - 2026-04-17

### Added v0.5

- Contextual grouping as a deterministic, independent structural output
- Metadata normalization layer with strict validation rules
- Support for additional recognized (non-processable) formats (PNG, HEIC/HEIF, RAW, video)
- Explicit corrupt-file propagation through CLI to planner
- JSON reporting with deterministic formatting and ordering
- `--context` CLI flag for optional contextual grouping output

### Changed v0.5

- Pipeline architecture now includes explicit orchestration layer (`run_pipeline`)
- Double-scan behavior formalized and documented
- Metadata handling unified through extraction → normalization flow
- Reporter extended to optionally include contextual grouping without affecting default output
- CLI flow updated to derive corrupt files before pipeline execution

### Fixed v0.5

- Enforced strict naive timestamp validation in metadata normalization
- Removed ambiguity in contextual grouping rules (ordering + time window)
- Ensured deterministic JSON output (sorted keys, fixed indentation)
- Aligned all documentation with implemented behavior (SPEC, README, module docs)

### Removed v0.5

- Deprecated documentation (`scanner_v0.2.md`)

### Notes v0.5

- Implementation is the source of truth; all documentation now reflects actual behavior
- No breaking changes to core deterministic pipeline behavior from v0.4
- System remains strictly deterministic, with no hidden heuristics or implicit logic

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
