# PhotoForge Backlog

This file tracks ideas, improvements, and future work.

Nothing in this file should influence v0.1 implementation.

---

## Timestamp & EXIF

- Handle incorrect camera timezone (manual offset)
- Per-folder or per-batch timezone correction
- Support GPS-based timezone inference
- Detect inconsistent timestamp clusters
- Optional interactive timestamp correction
- Support EXIF timezone fields if present
- Use filename and folder name patterns as fallback timestamp source when EXIF is missing

---

## File Format Support

- PNG support
- HEIC / HEIF support
- RAW formats (CR2, NEF, ARW, etc.)
- TIFF support
- Video file support (MP4, MOV)
- Apple Live Photos handling

---

## Duplicate Handling

- Optional duplicate deletion
- Duplicate reporting enhancements
- Keep-best-file heuristics beyond size
- Perceptual hashing (near-duplicate detection)
- Same-photo-different-encoding detection
- Allow configurable priority rules (beyond timestamp) to select the best/canonical photo (e.g. resolution, file size, filename patterns, source preference)

---

## Naming & Organization

- Custom filename templates
- Month/day folder structure
- Folder-by-camera model
- Folder-by-event or grouping
- User-defined naming rules

---

## Performance

- Parallel hashing
- Incremental scanning (cache results)
- Large library optimization
- I/O performance improvements

---

## CLI & UX

- Verbosity levels
- Progress indicator
- Dry-run diff-style output
- Interactive confirmation mode
- Better error reporting formatting

---

## Metadata

- Sidecar (XMP) support
- Metadata rewriting
- Keyword/tag extraction
- GPS-based naming or grouping
- Extract contextual metadata from filenames and folder names (e.g. location, event labels)

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

---

## Project / Dev

- PyPI packaging and publishing
- GitHub Actions (CI)
- Test coverage expansion
- Documentation for contributors
- Versioned releases and changelog

---

## Notes

- v0.1 scope is intentionally minimal and deterministic
- All items here are out of scope for v0.1 unless explicitly promoted
