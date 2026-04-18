# PhotoForge — Metadata Extraction Layer

## Classification

INTERNAL

---

## Purpose

This document defines the metadata extraction layer as a formal system structure.

It establishes:

- the structure of metadata extractors
- the interface contract for extractors
- the boundary between extraction and downstream processing
- the alignment rules for EXIF and non-JPEG formats

This document defines structure only.
It does not introduce or modify runtime behavior.

---

## Current System State

Metadata extraction currently exists in multiple locations:

- ``src/photoforge/exif.py`` performs JPEG EXIF extraction
- ``src/photoforge/metadata_extractors/`` contains format-specific extractors:
  - HEIC.py
  - PNG.py
  - RAW.py
  - video.py
- ``scanner.py`` directly invokes extraction functions
- ``metadata.py`` performs normalization but does not control extraction

The extraction layer is not yet unified.

---

## Target Structure

The metadata extraction layer defines the future single entry point for all metadata extraction.

Once implemented:

- all metadata extraction must be routed through this layer
- no module outside the layer may access format-specific extraction logic directly

---

## Extractor Location

All format-specific extractors must reside under:

```bash
src/photoforge/metadata_extractors/
```

Each format must have a dedicated extractor.

Existing extractors:

- ``extract_heic_timestamp``
- ``extract_png_timestamp``
- ``extract_raw_timestamp``
- ``extract_video_timestamp``

JPEG extraction currently resides outside this structure and must be aligned in future milestones.

---

## Extractor Interface

All extractors must implement:

```python
(path: Path, mtime_timestamp: float) -> tuple[datetime, str]
```

Inputs:

- ``path``: file path
- ``mtime_timestamp``: filesystem timestamp (float)

Outputs:

- ``datetime``: extracted timestamp (naive)
- ``str``: timestamp source identifier

---

## Extractor Behavior Constraints

Extractors must:

- be deterministic
- produce identical output for identical input
- depend only on:
  - provided path
  - provided timestamp
  - file content (if used)

Extractors must not:

- perform normalization
- perform cross-source fallback beyond defined extractor scope
- modify filesystem state
- depend on global or environment-specific state
- introduce implicit logic

---

## Current Extractor Behavior

Existing non-JPEG extractors:

- do not read embedded metadata
- deterministically fallback to filesystem timestamp
- return ``("mtime")`` as source

Example:

```python
return datetime.fromtimestamp(mtime_timestamp), "mtime"
```

This behavior is explicitly defined and must remain unchanged.

---

## Layer Boundary

The metadata extraction layer must:

- select extractor based on file format
- invoke the extractor
- return raw extracted metadata

The layer must not:

- perform normalization
- perform comparison
- perform diagnostics

---

## Integration with Metadata Module

The metadata module

- validates structure
- enforces deterministic metadata shape
- does not perform extraction

Pipeline order:

``
extractor → normalize_metadata → FileRecord
``

The extraction layer operates strictly before normalization.

---

## EXIF Alignment Rule

JPEG EXIF extraction must be aligned with the extraction layer:

- EXIF logic must be integrated into ``metadata_extractors``
- EXIF extraction must conform to the extractor interface
- direct use of standalone EXIF modules by the pipeline must be removed once alignment is implemented

Current behavior:

- ``scanner.py`` calls EXIF extraction directly
- this remains valid until alignment is completed

---

## Invariants

- Existing runtime behavior must remain unchanged
- Timestamp output must remain:
  - naive datetime
  - deterministic
- Extractors must not introduce:
  - implicit fallback
  - timezone inference
- Format-specific logic must remain isolated within extractors

---

## Non-Responsibilities

The metadata extraction layer does not:

- normalize metadata
- define fallback precedence across sources
- compare timestamps
- classify inconsistencies
- construct pipeline objects

---

## Final Contract

The metadata extraction layer defines:

1. extractor structure
2. extractor interface
3. extraction boundary

It ensures that metadata extraction is:

- explicit
- deterministic
- isolated from downstream processing
