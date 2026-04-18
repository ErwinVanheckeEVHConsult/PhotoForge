# PhotoForge — Operations

## Classification

BOUNDARY

---

## Purpose

The operations module executes filesystem changes based on planner output.

It consumes `PlannedAction` and applies deterministic file operations.

It does not define planning logic.

---

## Primary Entry Point

    apply_actions(actions: Iterable[PlannedAction]) -> None

---

## Responsibilities

The operations module is responsible for:

- iterating over planned actions
- executing filesystem operations for supported actions
- ensuring directories exist when required
- enforcing no-overwrite behavior

---

## Action Handling

Supported actions:

- skip
- collision
- rename
- move

Behavior:

### skip

- no operation

### collision

- no operation

### rename / move

- ensure parent directory exists
- move file using rename

Implementation behavior: :contentReference[oaicite:3]{index=3}  

- directory created if missing
- operation skipped if target already exists
- no overwrite allowed

---

## Inputs

- Iterable[PlannedAction]

Each action includes:

- source_path
- target_path
- action type

---

## Outputs

- filesystem side effects only
- no return value

---

## Determinism Constraints

Operations must be deterministic with respect to:

- input actions
- filesystem state

Behavior must not include:

- retries
- fallback strategies
- implicit conflict resolution

---

## Error Handling

- unsupported actions raise ValueError :contentReference[oaicite:4]{index=4}  
- existing target paths are silently skipped

---

## Non-Responsibilities

The operations module does not:

- determine which actions to execute
- validate planner decisions
- resolve collisions beyond skipping
- inspect corrupt files
- modify model objects
- generate output

---

## Integration Boundary

Consumed by CLI:

- only executed when `--apply` is enabled

Consumes:

- PlanResult.actions

---

## Final Contract

The operations module must:

1. execute planner-defined actions
2. never overwrite existing files
3. never reinterpret planner intent

It is an execution layer only.
