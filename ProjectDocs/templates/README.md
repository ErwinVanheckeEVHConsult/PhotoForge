# Templates

This directory contains reusable templates for planning, milestones, and release workflow.

---

## Usage Rules (ChatGPT)

When using any template:

- All .md document output must be presented by ChatGPT inside one single fenced markdown code block.
- The fenced block must contain the complete document and nothing else.
- Any remarks, questions, or validation must be outside that fenced block.
- Follow-up responses must return the full updated document again inside one fenced markdown code block.
- ChatGPT must ensure the fence is not accidentally broken during rendering or copying.
- When the document itself contains triple backticks, ChatGPT must use a longer outer fence so the markdown block remains intact.

---

## Principles

- Templates are deterministic and minimal
- Templates must not include placeholders requiring interpretation
- Templates may use explicit placeholders (e.g. ``<Deliverable>``, ``<Added item>``)
- Placeholders must:
  - be concrete and unambiguous
  - require direct substitution (no interpretation)
  - prevent copy-paste reuse without modification
  - not encode logic (e.g. "for each x")
- Repetition must be expressed as "(repeat as needed)"
- No structural modification when used
- Templates define structure, not content
