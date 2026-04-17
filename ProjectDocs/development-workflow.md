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

## Versioning Policy

All workflow artifacts for a version cycle must use a single deterministic version identifier.

### Version Assignment

- The version identifier must be assigned during Step 2 — Define Version Scope
- The version identifier assigned in Step 2 becomes the authoritative identifier for the active version cycle
- No document created for that version cycle may use a different version identifier

### Version Immutability

- The version identifier must not change after Step 3 — Approve Scope
- After scope approval, the approved version identifier is frozen for the remainder of the version cycle
- If the version identifier must change, the existing cycle must be discarded or regenerated before implementation begins

### Version Propagation

- All versioned documents created for the version cycle must use the exact same version identifier
- The version identifier must be consistent across:
  - planning proposal
  - scope approval
  - requirements
  - milestones overview
  - milestone documents
  - milestone checklists
  - release checklist
  - release notes
  - changelog entries for the version
  - release tag or release entry, if created

### Version Consistency Rules

- No conflicting version identifier may appear across artifacts belonging to the same version cycle
- Padded document naming format and human-readable version notation must refer to the same version
- A version cycle must not contain mixed identifiers referring to different major or minor versions

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

## Commit Naming Convention

All milestone and version commits must follow deterministic naming rules.

### Milestone Commit Format

- Milestone commits must use the format:
  - `MS<nnn>: <short-title>`

Rules:

- `<nnn>` must match the zero-padded milestone identifier defined in the milestones overview
- `<short-title>` must match the milestone short title
- The commit message must contain exactly one milestone identifier
- A milestone commit must not include version-level wording in place of the milestone identifier

### Version Commit Format

- Version-level commits must use the format:
  - `v<mmm>.<nnn>: <description>`

Rules:

- `<mmm>.<nnn>` must match the active version identifier for the version cycle
- `<description>` must be deterministic and describe the version-level action being committed
- A version-level commit must not use a milestone identifier in place of the version identifier

### Commit Constraints

- Every milestone commit must include a milestone identifier
- Every version-level commit must include a version identifier
- Commit messages must not use free-form prefixes outside the defined formats
- Commit naming must remain consistent across the full commit history for the version cycle

---

## Workflow

### Workflow Transition Model

The workflow is strictly sequential.

Rules:

- Each step has exactly one defined next step unless the workflow cycle is complete
- A step must not transition to any step other than its explicitly defined next step
- No intermediate, implicit, skipped, parallel, or out-of-order workflow state is allowed
- If a step fails its required validation or completion conditions, progression is blocked and the workflow remains in the current step until the blocking condition is resolved

Explicit transitions:

- Step 1 — Maintain Backlog → Step 2 — Define Version Scope
- Step 2 — Define Version Scope → Step 3 — Approve Scope
- Step 3 — Approve Scope → Step 4 — Define Requirements
- Step 4 — Define Requirements → Step 5 — Define Milestones
- Step 5 — Define Milestones → Step 6 — Implement Milestones
- Step 6 — Implement Milestones → Step 7 — Validate Milestones
- Step 7 — Validate Milestones → Step 8 — Commit Milestones
- Step 8 — Commit Milestones → Step 6 — Implement Milestones
  - only if additional defined milestones remain in the milestones overview for the active version
- Step 8 — Commit Milestones → Step 9 — Finalize Version Documentation
  - only if no additional defined milestones remain for the active version
- Step 9 — Finalize Version Documentation → Step 10 — Validate Release
- Step 10 — Validate Release → Step 11 — Create Release
- Step 11 — Create Release → Step 12 — Start Next Cycle
- Step 12 — Start Next Cycle → Step 1 — Maintain Backlog

State constraints:

- The workflow must always be in exactly one step at a time
- A step is considered complete only when its required outputs exist and its blocking conditions are satisfied
- Progression to the next step is allowed only through the explicit transition rules defined above

---

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
- Assign the version identifier for the version cycle
- The assigned version identifier becomes authoritative for all subsequent versioned artifacts in the cycle

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
- Freeze the version identifier for the remainder of the version cycle

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
- Milestone commits must use the defined milestone commit format
- Version-level commits must use the defined version commit format where applicable

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
  - release notes

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

## Template Enforcement

All workflow-generated documents must strictly use their corresponding templates.

### Mandatory Template Usage

- Every document created from a template must use the corresponding file in:
  - `ProjectDocs/templates/`
- Template selection must follow explicit mapping rules defined in the workflow
- No alternative structure may be used when a template exists

### Placeholder Resolution

- All placeholders defined in templates must be fully replaced
- No placeholder text may remain in any document at the time of validation or commit
- Presence of unresolved placeholders makes the document invalid

### Structure Preservation

- All required sections defined in templates must be present
- Section order must not be modified unless explicitly allowed
- Section semantics must not be altered
- No required section may be removed

### Type-Based Milestone Template Mapping

- Documentation milestones must use:
  - `documentation-milestone-template.md`
- Implementation milestones must use:
  - `implementation-milestone-template.md`

- A milestone using an incorrect template is invalid

### Enforcement

- Documents not conforming to template rules are considered invalid
- Invalid documents must not be:
  - committed
  - used for validation
  - considered complete

- Template violations are blocking conditions for:
  - milestone validation
  - milestone completion
  - release validation

---

## Workflow Enforcement

All workflow rules defined in this document are mandatory and must be strictly enforced.

### General Enforcement

- No workflow rule is advisory
- All rules are considered mandatory and binding
- Any violation of a workflow rule constitutes an invalid workflow state

### Blocking Conditions

A workflow step must not be considered complete if:

- any required output is missing
- any validation condition is not satisfied
- any applicable workflow rule is violated

Progression to the next workflow step is strictly forbidden while any blocking condition exists.

### Step Transition Enforcement

- A workflow step may only transition to its explicitly defined next step
- No step may be skipped, repeated out of order, or executed in parallel
- No implicit or partial transitions are allowed

If transition conditions are not satisfied:

- the workflow must remain in the current step
- no forward progression is allowed

### Milestone Enforcement

A milestone must not:

- start unless all milestone start conditions are satisfied
- be validated unless implementation is complete
- be committed unless validation is complete
- be considered complete unless all completion conditions are satisfied

A milestone violating any of the above is invalid.

### Validation Enforcement

- All checklist items must be explicitly evaluated
- No checklist item may remain unresolved
- Validation results must be binary (pass/fail)
- Partial validation is not allowed

If any validation criterion fails:

- the milestone or release must be considered invalid
- progression is blocked until the issue is resolved

### Commit Enforcement

- A milestone commit must include only changes belonging to the current milestone
- No unrelated or extraneous changes may be included
- The working tree must be clean after commit

If any of these conditions are not satisfied:

- the commit is invalid
- the milestone must not be considered complete

### Release Enforcement

A release must not be created unless:

- all milestones are completed
- all validation criteria are satisfied
- all documentation is consistent with implementation
- no blocking condition remains

If any condition is not satisfied:

- release creation is strictly forbidden

### Enforcement Outcome

- Any violation of workflow rules results in a blocked state
- Blocked states must be resolved before progression
- No exception, override, or bypass is allowed

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

The workflow enforces this complete ordered sequence:

1. Maintain Backlog
2. Define Version Scope
3. Approve Scope
4. Define Requirements
5. Define Milestones
6. Implement Milestones
7. Validate Milestones
8. Commit Milestones
9. Finalize Version Documentation
10. Validate Release
11. Create Release
12. Start Next Cycle

Transition order is fixed and explicit:

1 → 2 → 3 → 4 → 5 → 6 → 7 → 8

After Step 8:

- 8 → 6 if additional defined milestones remain
- 8 → 9 if no additional defined milestones remain

Then:

- 9 → 10 → 11 → 12 → 1

No implicit transitions are allowed.

Each step is deterministic, enforced, and reproducible.
