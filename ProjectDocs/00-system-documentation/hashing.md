# PhotoForge — Hashing

## Classification

INTERNAL

---

## Purpose

The hashing module provides deterministic SHA-256 hashing utilities for file content.

It is used by the scanner to derive:

- full SHA-256 digest
- short hash derived from that digest

The hashing module does not define duplicate grouping policy or planner behavior.

---

## Primary Functions

The module provides:

- `compute_sha256(path: Path) -> str`
- `derive_short_hash(sha256_hex: str) -> str`
- `hash_file(path: Path) -> tuple[str, str]`

---

## Responsibilities

The hashing module is responsible for:

- reading file content in fixed-size chunks
- computing SHA-256 over full file content
- returning lowercase hexadecimal digest
- deriving short hash as the first 8 characters
- exposing a convenience function that returns both values

---

## Hash Algorithm

Algorithm:

- SHA-256

Digest representation:

- lowercase hexadecimal string

Chunk size:

    1024 * 1024

The full file is hashed sequentially until EOF.

---

## Function Behavior

### `compute_sha256(path)`

Behavior:

- open file in binary mode
- read content in fixed-size chunks
- update SHA-256 state for each chunk
- return final hexadecimal digest

### `derive_short_hash(sha256_hex)`

Behavior:

- return `sha256_hex[:8]`

### `hash_file(path)`

Behavior:

- compute full SHA-256
- derive short hash from full digest
- return `(sha256_hex, short_hash)`

---

## Inputs

The hashing module consumes:

- `path: Path`
- full SHA-256 string for short-hash derivation

---

## Outputs

The hashing module produces:

- 64-character lowercase SHA-256 hex digest
- 8-character short hash derived from the full digest

---

## Determinism Constraints

The hashing module must remain deterministic.

For identical file content, it must return identical:

- full SHA-256 digest
- short hash

The hashing module must not introduce:

- randomness
- content-dependent algorithm switching
- truncation rules other than the fixed first 8 characters
- alternative digest encodings

---

## Error Boundary

The hashing module does not reinterpret I/O failures.

Errors from file open or file read propagate to the caller.

The scanner is responsible for converting those failures into scanner-level corrupt classification.

---

## Non-Responsibilities

The hashing module does not:

- classify duplicates
- define duplicate group identity at system level
- classify corrupt files
- construct `FileRecord`
- inspect metadata
- interact with planner, reporter, or operations

---

## Integration Boundary

The hashing module is used by the scanner during processable-file enrichment.

The scanner is responsible for:

- deciding when hashing occurs
- storing the digest in `FileRecord`
- deriving corrupt-file classification from hashing failures

The hashing module only computes hash values.

---

## Final Contract

The hashing module must:

1. compute full-file SHA-256 using fixed chunked reads
2. return lowercase hexadecimal digest
3. derive short hash as the first 8 characters of the full digest

It is an internal deterministic helper for content hashing only.
