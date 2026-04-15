# ChatGPT Rules — PhotoForge

This document defines mandatory interaction rules for ChatGPT when working on the PhotoForge project.

These rules ensure deterministic, high-quality, and implementation-safe outputs.

---

## 1. Formatting Rules (CRITICAL)

- Responses must be copy-paste safe by default
- Nested fenced code blocks are strictly forbidden
- Markdown must not break rendering in common clients (VSCode, GitHub, ChatGPT UI)
- When generating `.md` documents:
  - Output must be contained in a single fenced code block
  - No additional fences may exist inside that block
- Inline code blocks must not interfere with outer formatting

---

## 2. No Guessing Rule (HARD CONSTRAINT)

ChatGPT must not:

- guess behavior
- infer undocumented logic
- assume missing implementation details
- “fill in” unspecified behavior

If information is missing:

- explicitly request the required file or artifact
- explain why it is required
- pause progress until provided

---

## 3. Source of Truth Hierarchy

1. Implementation (code) is authoritative
2. Model definitions (`model.py`) define data contracts
3. Documentation must reflect implementation
4. Historical specs are not authoritative

Rules:

- Code must never be modified to match documentation in validation milestones
- Documentation must be updated to match implementation

---

## 4. Determinism Enforcement

All outputs must respect:

- identical input → identical output
- no randomness
- no environment-dependent behavior
- explicit ordering everywhere

ChatGPT must:

- call out any implicit ordering
- reject ambiguous definitions
- enforce deterministic wording in documentation

---

## 5. Scope Discipline

ChatGPT must:

- operate strictly within the current milestone scope
- not introduce redesign
- not introduce new features
- not expand scope implicitly

If a gap is identified:

- flag it explicitly
- do not silently resolve it outside scope

---

## 6. Documentation Rules

When generating or validating documentation:

- documentation must describe the system **as implemented**
- not as originally designed
- not as “intended”

All documents must be:

- consistent with each other
- consistent with code
- free of contradictions
- free of outdated assumptions

---

## 7. Validation Behavior

When validating:

- focus only on real mismatches (code vs docs vs spec)
- ignore stylistic preferences unless they introduce ambiguity
- clearly classify issues:
  - blocking
  - major
  - minor

ChatGPT must:

- provide actionable corrections
- not rewrite everything unnecessarily
- not introduce speculative fixes

---

## 8. Interaction Rules

ChatGPT must:

- be direct and precise
- avoid filler or generic explanations
- avoid unnecessary verbosity

ChatGPT must not:

- patronize
- over-explain obvious concepts
- derail into unrelated topics

---

## 9. Output Discipline

- Outputs must be immediately usable
- No partial documents
- No placeholder leakage unless explicitly required by templates
- No broken formatting

---

## 10. Priority of Rules

If rules conflict:

1. No Guessing Rule
2. Formatting Rules
3. Source of Truth
4. Determinism
5. Scope Discipline

---

## 11. Enforcement

If any rule is violated:

- the user may interrupt and correct
- ChatGPT must immediately:
  - acknowledge
  - correct
  - continue without justification loops
  