# Milestone Checklist — {{version}}-ms{{nnn}}

File name: {{version}}-ms{{nnn}}-checklist.md
Commit message: ms{{nnn}}: Milestone checklist

---

## Type

``<documentation|implementation>``

---

## Type Validation

- Milestone type is explicitly declared
- Milestone type matches the milestone definition document
- Milestone uses the correct template for its declared type
- Type-specific validation rules are applied correctly

---

## Scope Validation

- All work performed belongs strictly to the defined milestone scope
- No changes outside the milestone scope are present
- No redesign or scope expansion has been introduced
- All non-goals defined in the milestone document remain unchanged

---

## Responsibility Coverage

- Every responsibility defined in the milestone document has been completed
- No responsibility is partially implemented
- No undocumented work has been introduced

---

## Deliverable Validation

For each deliverable defined in the milestone document:

- Deliverable exists
- Deliverable is in the correct file or location
- Deliverable matches the milestone definition exactly and is verifiable without interpretation
- No required deliverable is missing
- No extra undeclared deliverable is present

---

## Definition Validation

For documentation milestones:

- All defined rules, structures, or constraints are explicitly present
- All affected documents reflect the defined rules exactly
- No ambiguity remains in defined documentation sections
- No placeholder remains in milestone document or checklist

For implementation milestones:

- All defined behavior is implemented exactly
- Inputs, processing rules, outputs, and edge cases match the behavior specification
- No implicit or undefined behavior exists

---

## Invariant Validation

- All invariants defined in the milestone document are preserved
- Existing validated behavior or rules remain unchanged unless explicitly redefined
- No implicit behavior has been introduced
- Consistency is preserved with:
  - development-workflow.md
  - requirements
  - milestones overview
  - relevant documentation or implementation artifacts

---

## Constraint Validation

- No constraint defined in the milestone document has been violated
- No runtime behavior has changed for documentation milestones
- No undocumented behavior exists for implementation milestones
- No hidden side effects are present

---

## Determinism Validation

- Identical input produces identical output
- All ordering is explicit and deterministic
- No environment-dependent behavior exists
- No incidental ordering, locale-dependent behavior, or filesystem-dependent behavior is relied upon

---

## Requirement Coverage Validation

- Every covered requirement listed in the milestone document is fully addressed
- No listed requirement is only partially satisfied
- No unlisted requirement has been implicitly addressed

---

## Consistency Validation

- Milestone implementation matches the milestone document exactly
- Milestone implementation matches covered requirements exactly
- Milestone remains consistent with:
  - development-workflow.md
  - milestones overview
  - related templates
  - related documentation
- No contradictions exist between milestone artifacts and authoritative documents

---

## Completion Validation

- All checklist items are resolved
- No unresolved validation issue remains
- Milestone is ready for commit
- All changes included in the commit belong to the current milestone
- No unrelated changes are staged for commit
- Presence of scaffolding or non-authoritative files is allowed, provided they are not modified as part of the milestone
- Scaffolding or non-authoritative files must not be modified unless explicitly part of the milestone scope

---

## Status

<DRAFT|READY|PASS|FAIL>
