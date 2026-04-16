# PhotoForge — EXIF Timestamp Extraction

## Classification

INTERNAL

---

## Purpose

The EXIF module provides deterministic timestamp extraction for processable image files.

It is used by the scanner to derive a timestamp and timestamp source from image metadata, with a deterministic fallback to filesystem modification time.

The EXIF module does not define scanner policy, corrupt-file classification, or metadata normalization.

---

## Primary Entry Point

The primary function is:

    extract_timestamp(path: Path, mtime_timestamp: float) -> tuple[datetime, str]

This function returns:

- extracted `datetime`
- timestamp source string

---

## Responsibilities

The EXIF module is responsible for:

- attempting to read EXIF metadata from an image file
- checking supported EXIF datetime tags in fixed order
- parsing EXIF datetime strings in a fixed format
- returning the first valid EXIF timestamp found
- falling back deterministically to filesystem `mtime`

---

## EXIF Tag Order

The module checks EXIF tags in this exact order:

1. `DateTimeOriginal` → `exif_datetimeoriginal`
2. `DateTimeDigitized` → `exif_datetimedigitized`
3. `DateTime` → `exif_datetime`

If no valid EXIF datetime is found, fallback is:
4. filesystem `mtime` → `mtime`

This order is fixed.

---

## Datetime Parsing

Supported EXIF datetime format:

    %Y:%m:%d %H:%M:%S

Behavior:

- non-string EXIF values are ignored
- invalid datetime strings are ignored
- parsing failure does not raise an error at this layer
- parsing continues to the next candidate

---

## EXIF Read Behavior

EXIF is read through image loading.

Behavior:

- open image with Pillow
- retrieve EXIF mapping
- return empty dict if no EXIF exists
- return empty dict if image open or EXIF read fails with:
  - `OSError`
  - `UnidentifiedImageError`

This means unreadable or non-identifiable EXIF is treated as missing EXIF at this module boundary.

---

## Fallback Behavior

If no valid EXIF datetime is found, the module returns:

- `datetime.fromtimestamp(mtime_timestamp)`
- source `"mtime"`

This fallback is deterministic and explicit.

---

## Inputs

The EXIF module consumes:

- `path: Path`
- `mtime_timestamp: float`

---

## Outputs

The EXIF module produces:

- `datetime`
- source string in:
  - `exif_datetimeoriginal`
  - `exif_datetimedigitized`
  - `exif_datetime`
  - `mtime`

---

## Determinism Constraints

The EXIF module must remain deterministic.

For identical image content and identical `mtime_timestamp`, it must return identical:

- timestamp value
- timestamp source

The EXIF module must not introduce:

- randomness
- locale-dependent parsing
- heuristic tag ordering
- environment-dependent fallback rules

---

## Non-Responsibilities

The EXIF module does not:

- normalize metadata
- classify corrupt files
- decide whether fallback is acceptable at system level
- create `FileRecord`
- inspect skipped files
- interact with planner, reporter, or operations

---

## Integration Boundary

The EXIF module is called by the scanner during timestamp extraction.

The scanner is responsible for:

- calling this function
- passing filesystem `mtime`
- normalizing the returned timestamp/source
- converting exceptions outside this module into scanner-level corrupt classification where applicable

The EXIF module only extracts and returns a timestamp candidate.

---

## Final Contract

`extract_timestamp(path, mtime_timestamp)` must:

1. attempt EXIF read
2. evaluate EXIF datetime tags in fixed order
3. return the first valid parsed EXIF datetime found
4. otherwise return `mtime` fallback

This module is an internal deterministic helper for timestamp extraction only.
