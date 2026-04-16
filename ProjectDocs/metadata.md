# PhotoForge — Metadata Normalization

## Classification

INTERNAL

---

## Purpose

The metadata module defines a minimal, deterministic abstraction for metadata used in the pipeline.

It provides:

- a normalized metadata structure
- a single validation entry point
- a strict boundary between extraction and usage

This module does not perform extraction, fallback, or transformation logic.

---

## Primary Components

### Data Structure

    NormalizedMetadata

Fields:

- timestamp: datetime
- timestamp_source: str

---

### Functions

- normalize_metadata(...)
- extract_jpeg_normalized_metadata(...) [boundary helper]

---

## Responsibilities

The metadata module is responsible for:

- enforcing structural validity of metadata
- validating timestamp type and constraints
- validating timestamp_source presence
- returning a normalized immutable metadata object

It does not modify or derive metadata.

---

## Normalization Function

    normalize_metadata(timestamp, timestamp_source) -> NormalizedMetadata

Validation rules:

- timestamp must be a datetime :contentReference[oaicite:0]{index=0}  
- timestamp must be naive (no timezone) :contentReference[oaicite:1]{index=1}  
- timestamp_source must be a non-empty string :contentReference[oaicite:2]{index=2}  

No transformation is allowed:

- no fallback logic
- no timezone conversion
- no mutation

---

## Extraction Boundary Helper

    extract_jpeg_normalized_metadata(path, mtime_timestamp)

Behavior:

- calls EXIF extraction
- passes result to normalize_metadata

Important:

- not part of the active pipeline
- exists only to define abstraction boundary

---

## Inputs

- timestamp: datetime
- timestamp_source: str

---

## Outputs

- NormalizedMetadata object

---

## Determinism Constraints

The module must be strictly deterministic:

- identical inputs → identical outputs
- no fallback logic
- no environment-dependent behavior

---

## Non-Responsibilities

The metadata module does not:

- read files
- extract EXIF directly (delegates)
- define fallback rules
- classify corrupt files
- construct FileRecord
- interact with planner, reporter, or operations

---

## Integration Boundary

Used by scanner:

- after timestamp extraction
- before FileRecord construction

The scanner owns:

- when normalization is called
- how failures are classified

---

## Final Contract

The metadata module must:

1. validate timestamp structure
2. enforce deterministic metadata shape
3. return NormalizedMetadata without modification

It is a strict validation layer, not a transformation layer.
