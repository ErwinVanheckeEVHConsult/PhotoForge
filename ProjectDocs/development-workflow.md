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

All generated documents must be stored according to workflow step.

Each folder represents the step in which the document is created or finalized.

- Backlog → ProjectDocs/01-backlog/
  - backlog.md

- Version scope → ProjectDocs/02-version-scope/
  - ``v<mmm>.<nnn>-planning-proposal.md``

- Scope approval → ProjectDocs/03-scope-approval/
  - ``v<mmm>.<nnn>-scope-approval.md``

- Requirements → ProjectDocs/04-requirements/
  - ``v<mmm>.<nnn>-requirements.md``

- Milestones → ProjectDocs/05-milestones/
  - ``v<mmm>.<nnn>-milestones.md``
  - ``v<mmm>.<nnn>-ms<nnn>-<short-title>.md``
  - ``v<mmm>.<nnn>-ms<nnn>-checklist.md``

- Version documentation → ProjectDocs/09-version-documentation/
  - ``v<mmm>.<nnn>-release-checklist.md``
  - ``v<mmm>.<nnn>-release-notes.md``
  - changelog.md

- Release validation → ProjectDocs/10-release-validation/
  - validation outputs (if stored)

- Release → ProjectDocs/11-release/
  - release artifacts (if documented)

- Workflow → ProjectDocs/development-workflow.md

- Templates → ProjectDocs/templates/

All documents must be stored in their defined location. No alternative locations are allowed.

- Workflow steps are authoritative for document storage structure

- Documents must be stored in the folder corresponding to the workflow step in which they are created or finalized
- No alternative locations are allowed
- No duplication of documents across steps is allowed

- Folder numbering must follow integer workflow steps only
- Sub-steps (e.g. 3.5, 6.5) do not create new folders

- New workflow steps may be introduced:
  - between existing steps
  - before the first step
  - after the last step

- When a new top-level step is introduced:
  - folder numbering must be updated to preserve correct ordering
  - affected folders must be renamed accordingly
  - all documents must be moved to the correct step folder

- When a step is renamed:
  - the corresponding folder must be renamed
  - all contained documents must remain consistent with the new step definition

- Folder structure must always reflect the current workflow exactly
  - no legacy structure may remain
  - no transitional or deprecated folders are allowed

- Renaming and moving folders is considered a required maintenance operation
  - it is not optional
  - it must be performed immediately when the workflow changes

---

## Naming Conventions

All documents must follow deterministic naming rules:

- Planning proposals → `v<mmm>.<nnn>-planning-proposal.md`
- Scope approval → `v<mmm>.<nnn>-scope-approval.md`
- Requirements → `v<mmm>.<nnn>-requirements.md`
- Release checklists → `v<mmm>.<nnn>-release-checklist.md`
- Release notes → `v<mmm>.<nnn>-release-notes.md`
- Milestones overview → `v<mmm>.<nnn>-milestones.md`
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

- Add or refine backlog entries in ProjectDocs/01-backlog/backlog.md
- Entries must remain minimal and one-line
- Entries must not include implementation details
- Entries must not duplicate existing items

---

### 2. Define Version Scope

- Select backlog items from ProjectDocs/01-backlog/backlog.md
- Selected items must be explicitly listed in the planning proposal
- No implicit scope inclusion is allowed

- Create planning proposal using:
  - ProjectDocs/templates/planning-proposal-template.md
  - Template structure must not be modified
  - All placeholders must be replaced

- Store planning proposal as:
  - ``ProjectDocs/02-version-scope/v<mmm>.<nnn>-planning-proposal.md``

- Create release checklist using:
  - ProjectDocs/templates/release-checklist-template.md
  - Template structure must not be modified
  - All placeholders must be replaced

- Store release checklist as:
  - ``ProjectDocs/09-version-documentation/v<mmm>.<nnn>-release-checklist.md``

---

### 3. Approve Scope

- Confirm selected backlog items
- Define explicit non-goals
- Freeze scope before implementation begins
- No scope changes are allowed after approval
- Scope must be limited strictly to selected backlog items

- Store approved scope as:
  - ``ProjectDocs/03-scope-approval/v<mmm>.<nnn>-scope-approval.md``

---

### 4. Define Requirements

- Derive requirements from approved scope
- Approved scope must be decomposed into atomic requirements when defining requirements

- Requirements must:
  - be explicit
  - be atomic
  - be testable
  - contain no ambiguity
  - not introduce new scope

- Requirements must not:
  - infer behavior
  - assume implementation details
  - contain implicit logic
  - be split after definition

- Store requirements as:
  - ``ProjectDocs/04-requirements/v<mmm>.<nnn>-requirements.md``

---

### 5. Define Milestones

- Derive milestones from requirements
- Each milestone must represent a coherent, testable unit of work

- Each milestone must declare a type

#### Milestone Types

Allowed types:

- documentation
- implementation

Rules:

- A milestone must not be created without a type
- A milestone must not mix multiple types
- A milestone must strictly follow the template associated with its type

#### Template Mapping

- documentation → ProjectDocs/templates/documentation-milestone-template.md
- implementation → ProjectDocs/templates/implementation-milestone-template.md

Rules:

- Template structure must not be modified
- All placeholders must be replaced
- All required sections must be present

#### Requirement Mapping

- Requirements must be atomic and must not be split
- A requirement must not be split across milestone types
- A requirement must be fully covered within a single milestone

- All requirements must be fully covered across all milestones

- No requirement behavior may:
  - be omitted
  - be duplicated across milestones

- All milestones for the version must be defined before implementation begins

- Create milestones overview using:
  - ProjectDocs/templates/milestones-overview-template.md
  - Template structure must not be modified
  - All placeholders must be replaced
- Store milestones overview as:
  - ``ProjectDocs/05-milestones/v<mmm>.<nnn>-milestones.md``

- The milestones overview must:
  - list all milestones exactly once
  - be ordered by ascending `MS<nnn>`
  - not be structurally modified after definition
    only status annotations (e.g. completion markers) may be added without altering:
    - ordering
    - milestone definitions
    - requirement coverage

For each milestone:

- Create milestone document using the template corresponding to its type
- Store milestone as:
  - ``ProjectDocs/05-milestones/v<mmm>.<nnn>-ms<nnn>-<short-title>.md``

- Create milestone checklist using:
  - ProjectDocs/templates/milestone-checklist-template.md
  - Template structure must not be modified
  - All placeholders must be replaced
- Store checklist as:
  - ``ProjectDocs/05-milestones/v<mmm>.<nnn>-ms<nnn>-checklist.md``

- Consistency rules:

  - Every milestone in the overview must have:
    - a milestone document
    - a milestone checklist

  - No milestone may exist outside the overview

  - No milestone may exist in the overview without corresponding files

---

### 6. Implement Milestones

- Only implementation-type milestones may modify runtime behavior
- Documentation-type milestones must not modify runtime behavior

- Implement only the defined milestone scope
- No changes outside milestone scope are allowed
- Existing validated behavior must not change unless explicitly defined

- A milestone must not be started unless the previous milestone is:
  - fully implemented
  - fully validated
  - fully committed

- A milestone must not be started unless:
  - all milestones are defined
  - requirements are complete

---

### 7. Validate Milestones

- Validate implementation using the milestone checklist

- All checklist items must be explicitly evaluated
- No checklist item may remain unresolved

- Confirm:
  - all responsibilities are implemented
  - behavior matches defined behavior
  - no unintended side effects exist
  - no scope creep or redesign is introduced

- Confirm:
  - implementation matches requirements
  - no undocumented behavior exists
  - no contradictions between code and documentation exist

- Documentation must be updated to match implementation

- Requirement coverage must be validated using:
  - milestone "Covered Requirements" sections

- If validation fails:
  - milestone must not be committed

---

### 8. Commit Milestones

- Each milestone must be committed as a single logical unit
- A commit must not include changes outside the milestone scope
- A milestone must not be split across multiple unrelated commits

- No uncommitted changes may remain after a milestone commit

---

### 9. Finalize Version Documentation

- Update README if changes affect documented behavior or usage
- Update specification if required
- Update module documentation if impacted

- Update changelog using:
  - ProjectDocs/templates/changelog-template.md
  - Template structure must not be modified
  - All placeholders must be replaced

- Generate release notes
- Store release notes as:
  - ``ProjectDocs/09-version-documentation/v<mmm>.<nnn>-release-notes.md``

- Ensure:
  - changelog reflects completed milestones only
  - documentation matches implementation
  - no outdated behavior remains

- Remove fulfilled backlog entries from ProjectDocs/01-backlog/backlog.md

---

### 10. Validate Release

- Validate release using the release checklist

- All checklist items must be explicitly evaluated
- No checklist item may remain unresolved

- Ensure full consistency between:
  - planning proposal
  - requirements
  - milestones overview
  - milestone documents
  - milestone checklists
  - changelog
  - release notes
  - backlog

- Confirm:
  - scope matches planning proposal
  - all requirements are implemented
  - all milestones are complete
  - documentation is fully aligned
  - behavior is validated

- If validation produces artifacts:
  - they must be stored in ProjectDocs/10-release-validation/

- If any condition is not satisfied:
  - release must be blocked until resolved

---

### 11. Create Release

- Tag version in version control
- Create release entry
- Mark as pre-release if applicable

- Version must match:
  - planning proposal
  - changelog
  - release checklist

---

### 12. Start Next Cycle

- Return to ProjectDocs/01-backlog/backlog.md
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

## Local Scaffolding Rules

Pre-generated milestone and planning files may exist locally as scaffolding to support workflow efficiency.

Rules:

- Such files must not be considered authoritative until the corresponding milestone or step is explicitly started
- A milestone is considered started only when:
  - its milestone document is actively used
  - its checklist is used for validation
  - implementation work has begun
- Pre-generated files must not influence scope, ordering, or implementation decisions
- Pre-generated files must not be committed unless they belong to the currently active milestone or workflow step
- Pre-generated files may be regenerated, modified, or discarded without constraint prior to milestone start

The repository state must always reflect only active and completed work, not future intent.

---

## Milestone Start Definition

A milestone is considered officially started when all of the following conditions are met:

- The milestone document (`v<mmm>.<nnn>-ms<nnn>-<short-title>.md`) is fully defined, contains no placeholders, and is ready for implementation without further interpretation
- The milestone checklist (`v<mmm>.<nnn>-ms<nnn>-checklist.md`) is created and ready for validation
- The previous milestone has been:
  - fully implemented
  - fully validated
  - committed with no remaining changes in the working tree
- Implementation work for the milestone has begun (code or document changes directly related to the milestone)

Rules:

- The existence of pre-generated or placeholder milestone files does not constitute milestone start
- A milestone must not be started implicitly or partially
- Only one milestone may be active at any time
- Work performed must correspond exclusively to the currently active milestone

---

## Milestone Completion Definition

A milestone is complete when:

- all checklist items are resolved
- behavior matches specification
- no unresolved validation issues or checklist items remain
- all changes are committed
- working tree is clean (no uncommitted or unrelated changes)

---

## Summary

The workflow enforces a strict sequence:

backlog → scope → approval → requirements → milestones → implementation → validation → commit → release

Each step is deterministic, enforced, and reproducible.
