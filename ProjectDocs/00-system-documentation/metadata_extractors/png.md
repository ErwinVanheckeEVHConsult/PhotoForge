# PhotoForge — PNG Metadata Extractor

## Classification

INTERNAL

---

## Purpose

Provides metadata extraction for PNG files.

---

## Responsibilities

- extract timestamp-related metadata from PNG files

---

## Inputs

- file path

---

## Outputs

- timestamp and timestamp source (format defined by caller)

---

## Determinism Constraints

- identical file content must yield identical extracted metadata

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

- metadata extraction layer

---

## Final Contract

Extracts metadata from PNG files without defining system-level behavior.
