# Documentation Validation Procedure

## Purpose

This document defines the deterministic procedure for validating documentation coverage and consistency.

The goal is to ensure that:

* all runtime modules are documented
* all documentation reflects actual implementation
* no behavior is undocumented
* no documentation contradicts implementation

Documentation must be treated as a **verified representation of the system**, not a best-effort description.

---

## Scope

This procedure applies:

* after each milestone (partial validation)
* before every release (full validation, mandatory)

---

## Definitions

### Module

A Python file under:

``
src/photoforge/
``

### Module Documentation

A markdown file under:

``
ProjectDocs/<module>.md
``

Mapping rule:

``
<module>.py → ProjectDocs/<module>.md
``

This mapping is mandatory.

---

## Validation Rules

### Rule 1 — Complete Module Coverage

Every module must have a corresponding documentation file.

No exceptions.

---

### Rule 2 — Single Source of Truth

Each module must be documented in exactly one corresponding file.

No duplication across multiple module-level documents.

---

### Rule 3 — Tiered Documentation Depth

Each module must be classified as:

* CORE
* BOUNDARY
* INTERNAL

This classification determines documentation depth.

---

### Rule 4 — Implementation is Authoritative

If documentation and code differ:

→ the code is correct
→ the documentation must be updated

---

### Rule 5 — No Hidden Behavior

Any behavior present in code must be explicitly documented.

---

### Rule 6 — No Undocumented Assumptions

Documentation must not introduce behavior that is not implemented.

---

### Rule 7 — Deterministic Wording

Documentation must avoid:

* vague language
* implied behavior
* assumptions not enforced by code

---

## Validation Procedure

If any step detects a failure condition, validation must stop immediately and return REJECTED.

No further steps may be executed after a blocking failure is detected.

### Step 0 — Freeze Validation Scope

The validation scope is defined strictly as:

* all modules under src/photoforge/
* all corresponding module documentation
* generic documentation:
  * README.md
  * SPEC.md
  * ProjectDocs/architecture.md

No additional files may be included or excluded during validation.

Scope must not change once validation begins.

### Step 1 — Enumerate Modules

List all modules:

```bash
find src/photoforge -name "*.py"
```

This list defines the complete validation scope.

---

### Step 2 — Enforce Module → Doc Mapping

For each module:

``
<module>.py → ProjectDocs/<module>.md
``

Check:

* documentation file exists
* file name matches module name exactly

Failure condition:

* missing documentation file

---

### Step 3 — Classify Module Tier

Each module must be classified as:

#### CORE

Defines core system behavior.

Examples:

* scanner
* planner
* grouping
* pipeline
* model

#### BOUNDARY

Defines orchestration or external interaction.

Examples:

* cli
* reporter
* operations

#### INTERNAL

Defines supporting functionality.

Examples:

* metadata
* exif
* hashing

This classification must be reflected in the documentation.

---

### Step 4 — Validate Module Documentation

#### All modules

Check:

* reflects current implementation
* no contradictions with code
* no outdated behavior
* no undocumented behavior

---

#### CORE modules

Must include:

* responsibilities
* full behavior description
* execution flow
* invariants
* integration boundaries

---

#### BOUNDARY modules

Must include:

* responsibilities
* integration points
* explicit transformations (if any)
* clear boundaries

---

#### INTERNAL modules

Must include:

* purpose
* responsibilities
* inputs / outputs
* determinism constraints
* explicit non-responsibilities

Must not:

* define system-level behavior
* duplicate higher-level documentation

---

### Step 5 — Validate Generic Documentation

The following documents must always be validated:

* `README.md`
* `SPEC.md`
* `ProjectDocs/architecture.md`

Check:

* consistent with implementation
* consistent with module documentation
* no contradictions
* no missing behavior

---

### Step 6 — Build Coverage Matrix

Construct mapping:

``
<module>.py → <module>.md → referenced in:
    - README.md
    - SPEC.md
    - architecture.md
``

Each module must be referenced in at least one of:

* README.md
* SPEC.md
* architecture.md

If a module defines system-level behavior, it must be referenced in:

* SPEC.md
* architecture.md

Failure conditions:

* module has no references in generic docs
* module defines behavior but is not referenced in SPEC.md or architecture.md

---

### Step 7 — Detect Missing Documentation

If a module:

* has no documentation
* or has behavior not documented

Then:

* create new documentation
* or extend existing documentation

---

### Step 8 — Detect Documentation Drift

Identify:

* documentation describing non-existent behavior
* implementation behavior not documented
* inconsistent terminology across documents

All drift must be resolved before validation passes.

---

### Step 9 — Produce Validation Result

Output must be:

``
Status: ACCEPTED / REJECTED
``

If REJECTED:

* list missing documentation
* list mismatches
* list inconsistencies

Release must not proceed if status is REJECTED.

---

## Partial Validation (Post-Milestone)

After each milestone:

* identify affected modules
* run Steps 2–4 for affected modules only
* update generic documentation if impacted

---

## Full Validation (Pre-Release)

Before release:

* run full procedure (Steps 1–9)
* no skipped modules
* no partial checks allowed

---

## Final Rule

Documentation is considered valid if and only if:

* every module is documented
* documentation matches implementation
* no behavior is undocumented
* no contradictions exist across documents

If any of these conditions fail:

→ documentation is invalid
→ release is blocked

---
