# PhotoForge — Version

## Classification

INTERNAL

---

## Purpose

The version module defines the current version identifier of the PhotoForge application.

It provides a single constant used for display and reporting purposes.

---

## Contents

- VERSION

---

## Responsibilities

The version module is responsible for:

- exposing the current application version string

---

## Inputs

None

---

## Outputs

- VERSION: str

---

## Determinism Constraints

The version value must be constant within a given release.

---

## Non-Responsibilities

The version module does not:

- influence behavior
- control feature flags
- affect pipeline logic
- interact with any component

---

## Integration Boundary

Used by:

- reporter (for display)

---

## Final Contract

The version module must provide a single constant VERSION used for reporting purposes.
