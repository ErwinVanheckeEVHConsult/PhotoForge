# Repository: <https://github.com/ErwinVanheckeEVHConsult/PhotoForge>

## Repository Access

The repository URL is an authorized source.

You MUST:

- fetch required files from the repository when needed
- not wait for manual upload if files are accessible via the repository
- treat the repository as available input

Do not block execution solely because files were not uploaded,
if they are available in the repository.

---

You are working on the PhotoForge project.

---

## Mandatory Rule Source

Load and apply:

- ProjectDocs/ChatGPT-rules.md

This file overrides all default behavior.

If any instruction conflicts with this file, follow ChatGPT-rules.md.

---

## State Sources

/ProjectDocs/01-backlog/backlog.md
/ProjectDocs/09-version-documentation/*

---

## Architecture (authoritative)

scanner.py           → orchestration / routing  
metadata_extractors  → extraction + fallback (format-specific)  
metadata.py          → normalization / validation only  

Important constraints:

- metadata.py does NOT perform extraction or dispatch
- extractor = full timestamp resolution (including fallback)
- scanner = router only, no fallback logic

---

## Required Sources (load and use as ground truth)

Load ONLY the files required for the task.

### Core Rules & Architecture

- ProjectDocs/ChatGPT-rules.md
- ProjectDocs/development-workflow.md

### Milestones

- ProjectDocs/05-milestones/

### Templates (mandatory)

- ProjectDocs/templates/implementation-milestone-template.md
- ProjectDocs/templates/milestone-checklist-template.md

### Code (current implementation state)

- src/photoforge/*
- src/photoforge/metadata_extractors/*

Do not rely on memory. Use these as authoritative references.

If a required file is missing:

- request it
- explain why
- STOP until provided

---

## Rendering Rules

- All documents must be returned inside a single markdown code block
- No nested code blocks inside that block
- No extra formatting outside the block
- No partial outputs
- No inline explanations
- No commentary unless explicitly requested

---

## Current Task

Do not generate anything yet.

First:

1. Confirm ChatGPT-rules.md has been applied
2. Identify which sources are required and confirm they are loaded
3. Summarize the current architecture in ≤5 lines
4. Summarize the current state in ≤10 lines
5. Confirm scope before writing

Wait for confirmation before generating any file.
