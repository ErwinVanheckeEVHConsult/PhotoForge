# PhotoForge — HEIC Metadata Extractor

## Classification

INTERNAL

---

## Purpose

Provides metadata extraction for HEIC files.

This module is part of the metadata extraction layer.

---

## Responsibilities

- extract timestamp-related metadata from HEIC files

---

## Inputs

- file path

---

## Outputs

- timestamp and timestamp source (format defined by caller)

---

## Determinism Constraints

- identical file content must yield identical extracted metadata
- no environment-dependent behavior

---

## Non-Responsibilities

- no normalization
- no fallback logic
- no corrupt-file classification
- no FileRecord construction
- no planner or grouping interaction

---

## Integration Boundary

Used by:

- metadata extraction layer (via metadata module or scanner integration)

---

## Final Contract

Extracts metadata from HEIC files without defining system-level behavior.
