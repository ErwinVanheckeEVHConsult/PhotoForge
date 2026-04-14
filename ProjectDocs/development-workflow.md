# Development Workflow

This document defines the deterministic workflow for developing, validating, and releasing PhotoForge versions.

---

## Principles

- Development is deterministic and reproducible
- Scope is strictly controlled and derived from the backlog
- Each step produces a complete and verifiable output
- No implicit decisions or partial state transitions are allowed
- Workflow steps must be executed strictly in defined order
- No step may be skipped or reordered

---

## Document Storage

All generated documents must be stored in fixed locations:

- Planning proposals → ProjectDocs/planning-proposals/
- Milestones → ProjectDocs/milestones/
- Milestone checklists → ProjectDocs/milestones/ (alongside milestone documents)
- Release checklists → ProjectDocs/planning-proposals/ (per version)
- Changelog → ProjectDocs/changelog.md
- Workflow → ProjectDocs/development-workflow.md
- Templates → ProjectDocs/templates/

All documents must be stored in their defined location. No alternative locations are allowed.

---

## Naming Conventions

All documents must follow deterministic naming rules:

- Planning proposals → `v<mmm>.<nnn>-planning-proposal.md`
- Release checklists → `v<mmm>.<nnn>-release-checklist.md`
- Milestones → `v<mmm>.<nnn>-ms<nnn>-<short-title>.md`
- Milestone checklists → `v<mmm>.<nnn>-ms<nnn>-checklist.md`

Where:

- `<mmm>`  is the zero-padded major version (e.g. 000, 001)
- `<nnn>` is the zero-padded minor version or milestone number (e.g. 004, 018)
- `<short-title>` is lowercase and hyphen-separated

Naming conventions must be applied exactly. No deviation is allowed.

Human-readable version notation inside documents may remain unpadded (e.g. v0.4).

---

## Workflow

### 1. Maintain Backlog

- Add or refine backlog entries in ProjectDocs/backlog.md
- Entries must remain minimal and one-line
- Entries must not include implementation details
- Entries must not duplicate existing items

---

### 2. Define Version Scope

- Select backlog items from ProjectDocs/backlog.md
- Selected items must be explicitly listed in the planning proposal
- No implicit scope inclusion is allowed

- Create planning proposal using:
  - ProjectDocs/templates/planning-proposal-template.md
  - Template structure must not be modified
  - All placeholders must be replaced

- Store planning proposal as:
  - `ProjectDocs/planning-proposals/v<mmm>.<nnn>-planning-proposal.md`

- Create release checklist using:
  - ProjectDocs/templates/release-checklist-template.md
  - Template structure must not be modified
  - All placeholders must be replaced

- Store release checklist as:
  - `ProjectDocs/planning-proposals/v<mmm>.<nnn>-release-checklist.md`

- Scope must be limited strictly to selected backlog items

---

### 3. Approve Scope

- Confirm selected backlog items
- Define explicit non-goals
- Freeze scope before implementation begins
- No scope changes are allowed after approval

---

### 4. Define Milestones

- Break scope into isolated milestones
- Each milestone must represent a single unit of work

For each milestone:

- Create milestone document using:
  - ProjectDocs/templates/milestone-template.md
  - Template structure must not be modified
  - All placeholders must be replaced

- Store milestone as:
  - `ProjectDocs/milestones/v<mmm>.<nnn>-ms<nnn>-<short-title>.md`

- Create milestone checklist using:
  - ProjectDocs/templates/milestone-checklist-template.md
  - Template structure must not be modified
  - All placeholders must be replaced

- Store checklist as:
  - `ProjectDocs/milestones/v<mmm>.<nnn>-ms<nnn>-checklist.md`

---

### 5. Implement Milestones

- Implement only the defined milestone scope
- No changes outside milestone scope are allowed
- Existing validated behavior must not change

- A milestone must not be started unless the previous milestone is:
  - fully implemented
  - fully validated
  - fully committed

---

### 6. Validate Milestones

- Validate implementation using the milestone checklist

- All checklist items must be explicitly evaluated
- No checklist item may remain unresolved

- Confirm:
  - all responsibilities are implemented
  - behavior matches defined behavior
  - no unintended side effects exist
  - no scope creep or redesign is introduced

---

### 7. Commit Milestones

- Each milestone must be committed as a single logical unit
- A commit must not include changes outside the milestone scope
- A milestone must not be split across multiple unrelated commits

- No uncommitted changes may remain after a milestone commit

---

### 8. Finalize Version Documentation

- Update README if changes affect documented behavior or usage
- Update specification if required

- Update changelog using:
  - ProjectDocs/templates/changelog-template.md
  - Template structure must not be modified
  - All placeholders must be replaced

- Remove fulfilled backlog entries from ProjectDocs/backlog.md

---

### 9. Validate Release

- Validate release using the release checklist

- All checklist items must be explicitly evaluated
- No checklist item may remain unresolved

- Ensure full consistency between:
  - planning proposal
  - milestone documents
  - milestone checklists
  - changelog
  - backlog

- Confirm:
  - scope matches planning proposal
  - all milestones are complete
  - documentation is fully aligned
  - behavior is validated

---

### 10. Create Release

- Tag version in version control
- Create release entry
- Mark as pre-release if applicable

- Version must match:
  - planning proposal
  - changelog
  - release checklist

---

### 11. Start Next Cycle

- Return to ProjectDocs/backlog.md
- Select next version scope
- Repeat workflow from step 1

---

## Template Usage

- All template-based documents must use the corresponding template in ProjectDocs/templates/
- Template structure must not be modified
- All placeholders must be replaced
- Documents must be generated as complete units
- Partial or incremental document creation is not allowed

---

## Summary

The workflow enforces a strict sequence:

backlog → planning → milestones → validation → commit → release

Each step is deterministic, enforced, and reproducible.
