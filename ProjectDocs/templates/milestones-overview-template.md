# Milestones - <version>

File name: <version>-milestones.md

---

## Context

- Requirements are defined in ``v<mmm>.<nnn>-requirements.md``
- Scope is limited to approved backlog items
- No changes outside defined scope are allowed
- All milestones must preserve existing runtime behavior exactly

---

## Milestones

For each milestone:

- Must be listed exactly once
- Must include:
  - identifier
  - short title
  - type
  - responsibilities summary
  - covered requirements

---

### MS<nnn> - <short-title>

**Type:**

- documentation | implementation

**Summary:**

- ``<explicit description of the milestone outcome>``
- Must describe concrete result (not intent)
- Must be consistent with milestone deliverables

**Covered Requirements:**

- R<xxx> — <requirement-name>
- No partial coverage allowed
- No duplication across milestones

---

(repeat for all milestones)

---

## Ordering

- Milestones must be listed in execution order
- Execution order must be deterministic
- Execution order fully defines milestone dependencies
- A milestone may require outputs from earlier milestones only
- No milestone may require outputs from a later milestone
- If a milestone requires an earlier milestone to complete, that requirement must be reflected by ordering in this overview before the overview is frozen

---

## Consistency Rules

- Every milestone listed here must have:
  - a milestone definition document
  - a milestone checklist

- No milestone may exist outside this overview
- No milestone may be missing from this overview

- All requirements must be covered exactly once across all milestones
- No requirement may be:
  - omitted
  - duplicated
  - split across milestones or types

---

## Type Constraints

- Milestone type must match the nature of covered requirements:
  - documentation requirements → documentation milestones
  - implementation requirements → implementation milestones
- Each milestone must declare exactly one type
- Allowed types:
  - documentation
  - implementation

- A milestone must not mix types
- Template selection must be based solely on type

---

## Validation Criteria

- Milestone list is complete
- Ordering fully encodes all milestone dependencies
- All requirements are covered exactly once
- All milestones have valid type declarations
- Milestone types match requirement nature
- All milestones in overview match existing milestone definition documents
- No contradictions exist between:
  - milestones
  - requirements
  - workflow
