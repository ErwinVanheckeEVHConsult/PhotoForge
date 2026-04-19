# Milestone - {{version}}-ms{{nnn}} - {{short-title}}

File name: {{version}}-ms{{nnn}}-{{short-title}}.md
Commit message: ms{{nnn}}: Milestone definition

---

## Type

documentation

---

## Context

- Reference current documentation state
- Identify missing, inconsistent, or ambiguous elements
- List affected documents and sections

---

## Goal

Define a precise, verifiable documentation outcome.

Rules:

- Must define observable result (not intent)
- Must be verifiable through document inspection
- Must not be ambiguous

---

## Affected Documents

- ``<file path>`` (repeat as needed)

Must explicitly identify:

- modified documents
- created documents
- untouched documents (if relevant)

## Definitions

Define all required structures, rules, or constraints.

- ``<rule or structure>`` (repeat as needed)

Rules:

- Must be explicit and complete
- Must be independently understandable
- Must not rely on other sections for interpretation
- Must not contain implicit logic

---

## Invariants

- Existing validated rules must remain unchanged unless explicitly redefined
- Existing document structure must not change unless explicitly specified
- No implicit behavior may be introduced
- All changes must preserve consistency with:
  - development-workflow.md
  - requirements
  - milestones overview

---

## Responsibilities

- Define required documentation changes
- Ensure alignment with workflow and requirements
- Eliminate ambiguity and inconsistency

---

## Deliverables

Explicit, verifiable outputs:

- ``<file created or updated>``
- ``<section added or modified>``
- ``<rule explicitly defined>``

Rules:

- Every deliverable must be:
  - file-based OR
  - rule-based AND verifiable
- No abstract deliverables allowed

---

## Constraints

- No changes to runtime behavior
- No modifications outside defined scope
- No introduction of implicit behavior

---

## Validation Criteria

- All deliverables exist and match specification
- All rules are explicitly defined
- No ambiguity remains in affected documents
- No contradictions exist between:
  - documents
  - workflow
  - requirements
- No placeholder or incomplete definitions remain

All criteria must be binary (pass/fail)

---

## Non-Goals

Explicitly define what is not changed.

---

## Covered Requirements

- R{{xxx}} - {{requirement-name}}
