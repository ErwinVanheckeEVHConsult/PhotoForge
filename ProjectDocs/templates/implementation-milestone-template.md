# Milestone - <version>-ms<nnn> - <short-title>

File name: <version>-ms<nnn>-<short-title>.md

---

## Type

implementation

---

## Context

- Reference current implementation state
- Identify missing, incorrect, or incomplete behavior
- List affected modules, functions, or components

---

## Goal

Define a precise, testable behavioral outcome.

Rules:

- Must define observable behavior (inputs → outputs)
- Must be verifiable through execution
- Must not be ambiguous

---

## Affected Components

List all impacted code elements:

- ``<file path>``
- ``<module>``
- ``<class/function>``

Must explicitly identify:

- modified components
- created components
- untouched components (if relevant)

---

## Behavior Specification

### Inputs

- ``<input definition>`` (repeat as needed)

### Processing Rules

- ``<deterministic transformation rule>`` (repeat as needed)

### Outputs

- ``<output definition>`` (repeat as needed)

### Edge Cases

- ``<edge case>`` (repeat as needed)

Rules:

- Must be explicit and complete
- Must be independently understandable
- Must not rely on implicit behavior
- Must not depend on environment-specific conditions

---

## Invariants

- Existing validated behavior must remain unchanged unless explicitly redefined
- Output structure must not change unless explicitly specified
- No implicit behavior may be introduced
- All changes must preserve consistency with:
  - implementation
  - requirements
  - documentation

---

## Responsibilities

- Implement defined behavior exactly
- Modify only specified components
- Prevent side effects outside scope

---

## Deliverables

Explicit, verifiable outputs:

- ``<file created or modified>``
- ``<function/class implemented or updated>``
- ``<behavior explicitly implemented>``

Rules:

- Every deliverable must be:
  - code-based OR
  - behavior-based AND verifiable
- No abstract deliverables allowed

---

## Constraints

- No changes outside defined scope
- No redesign unless explicitly required
- No hidden side effects
- No undocumented behavior

---

## Validation Criteria

- Given defined inputs → expected outputs are produced
- All edge cases behave as specified
- No regression in existing behavior
- Output is deterministic across runs
- All ordering in outputs is explicitly defined and deterministic
- No environment-dependent behavior exists
- Implementation matches:
  - requirements
  - documentation

All criteria must be binary (pass/fail)

---

## Non-Goals

Explicitly define what is not changed.

---

## Covered Requirements

- R<xxx> — <requirement-name>
