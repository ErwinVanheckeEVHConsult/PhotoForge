# PhotoForge — Video Metadata Extractor

## Classification

INTERNAL

---

## Purpose

Provides metadata extraction for video files.

---

## Responsibilities

- extract timestamp-related metadata from video files

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

Extracts metadata from video files without defining system-level behavior.
