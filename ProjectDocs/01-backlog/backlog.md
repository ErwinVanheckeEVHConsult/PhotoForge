# PhotoForge Backlog

This file tracks ideas, improvements, and future work.

Nothing in this file should influence v0.1 implementation.

Backlog hygiene rules:

- Keep entries minimal and one-line
- Prefer extending existing entries over creating new ones
- Avoid duplication across sections
- Do not include implementation details or solutions

---

## Timestamp & EXIF

- Handle incorrect camera timezone (manual offset)
- Per-folder or per-batch timezone correction
- Support GPS-based timezone inference
- Detect inconsistent timestamp clusters
- Optional interactive timestamp correction
- Support EXIF timezone fields if present
- Use filename patterns as fallback timestamp source when EXIF is missing
- Use folder name patterns as fallback timestamp source when EXIF is missing
- Classify timestamp inconsistencies as comparable vs non-comparable
- Infer timezone correction from trusted device clusters
- Detect event-bounded folders vs mixed-content folders

---

## File Format Support

- Full processing support for non-JPEG formats
- TIFF support
- Define TIFF metadata extraction completeness
- Apple Live Photos handling

---

## Duplicate Handling

- Optional duplicate deletion
- Duplicate reporting enhancements
- Perceptual hashing (near-duplicate detection)
- Configurable canonical selection rules (beyond timestamp, size, filename patterns, source preference)
- Prefer original filenames over copy variants (e.g. “- Copy”, “(1)”)
- Detect same-photo-different-encoding cases

---

## Naming & Organization

- Custom filename templates
- Folder-by-camera model
- Folder-by-event or grouping
- User-defined filename rules
- User-defined folder structure rules
- Support additional filename timestamp patterns

---

## Performance

- Parallel hashing
- Incremental scanning (cache results)
- Large library optimization
- I/O performance improvements
- Size-based pre-grouping before hashing

---

## CLI & UX

- Verbosity levels
- Progress indicator
- Dry-run diff-style output
- Interactive confirmation mode
- Better error reporting formatting
- Improve console output usability for large scans

---

## Metadata

- Sidecar (XMP) support
- Metadata rewriting
- Keyword/tag extraction
- GPS-based naming or grouping
- Extract metadata from filenames
- Extract metadata from folder names
- Infer batch context from metadata sources
- Expose EXIF diagnostics (missing, unreadable, invalid fields)
- Define metadata source trust model
- Expose structured timestamp representations in output

---

## Advanced Features

- Face detection
- Event clustering
- AI-based photo classification
- Quality scoring / best photo selection

---

## Integration

- iCloud Photos integration
- Google Photos integration
- Dropbox / OneDrive support
- Watch mode (auto-process new files)
- Apple Live Photos handling

---

## Project / Dev

- PyPI packaging and publishing
- GitHub Actions (CI)
- Test coverage expansion
- Documentation for contributors
- Add a scripted procedure to export and flatten project files for ChatGPT source uploads
- Deterministically rename exported files to preserve scope in flat source contexts
- Include docs, templates, specs, and source modules in the export bundle
- Refresh ChatGPT source bundle after each validated milestone commit or release
- Replace version.py by pyproject.toml
- Define and enforce runtime pyproject.toml
- Move CHANGELOG.md to /
- Align EXIF module placement with metadata_extractors structure
- Formalize scope-refinement-addendum as part of scope approval workflow
- Define rules for creation, content, and validation of scope-refinement-addendum
- Define storage and lifecycle rules for scope-refinement-addendum

---

## Notes

- v0.1 scope is intentionally minimal and deterministic
- All items here are out of scope for v0.1 unless explicitly promoted
