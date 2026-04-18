# PhotoForge — Pipeline Orchestration

## Purpose

The pipeline orchestration layer composes scanning, planning, and contextual grouping into a single deterministic execution flow.

Its role is to coordinate existing components without changing their individual responsibilities.

The pipeline layer does **not** define:

- scanner behavior
- planner behavior
- grouping rules
- reporting behavior
- filesystem execution behavior

It only defines orchestration.

---

## Primary Entry Point

The pipeline orchestration entry point is:

    run_pipeline(
        input_path: Path,
        *planner_args: object,
        plan_files: PlannerFunction | None = None,
        build_contextual_grouping: GroupingBuilder | None = None,
        **planner_kwargs: object,
    ) -> tuple[PlanResult, ContextualGrouping]

This function returns:

- `PlanResult`
- `ContextualGrouping`

These are returned separately.

---

## Responsibility Boundary

### pipeline.py is responsible for

- invoking scanner execution
- obtaining the valid `FileRecord` set from `ScanResult`
- invoking contextual grouping exactly once from the full valid record set
- invoking the planner entry point
- forwarding planner arguments and keyword arguments unchanged
- returning `PlanResult` and `ContextualGrouping` as separate outputs

### pipeline.py is not responsible for

- validating CLI arguments
- deriving `CorruptFile` from scanner diagnostics
- rendering output
- executing filesystem actions
- defining planner rules
- defining grouping rules
- mutating scan results
- embedding contextual grouping into `PlanResult`

---

## Execution Flow

Current implementation executes the following sequence:

1. call `scan_directory(input_path)`
2. obtain `scan_result.records`
3. call contextual grouping builder with `scan_result.records`
4. call planner with `scan_result.records` and forwarded planner arguments
5. return both outputs separately

Expressed structurally:

    scan_result = scan_directory(input_path)
    records = scan_result.records

    grouping = build_contextual_grouping(records)
    plan_result = plan_files(records, *planner_args, **planner_kwargs)

    return plan_result, grouping

---

## Scanner Interaction

The pipeline invokes the scanner directly:

    scan_directory(input_path) -> ScanResult

Only the following scanner output is used by the pipeline itself:

- `scan_result.records`

The pipeline does not directly use:

- `scan_result.skipped`
- `scan_result.issues`
- `scan_result.total_entries_seen`
- `scan_result.supported_files_processed`

This means the pipeline consumes only the valid-file planning input produced by scanning.

---

## Corrupt File Boundary

The pipeline does not derive corrupt files from scanner output.

Current system behavior is split across components:

1. CLI performs an initial scan
2. CLI derives `CorruptFile` from skipped entries whose reason starts with `corrupt_`
3. CLI passes `corrupt_files=...` into `run_pipeline(...)`
4. `run_pipeline(...)` forwards that keyword argument unchanged to the planner

Therefore:

- corrupt-file transformation is outside the pipeline boundary
- corrupt-file propagation into planning is supported through forwarded planner keyword arguments
- pipeline orchestration does not interpret corrupt-file semantics

---

## Planner Interaction

The planner entry point is loaded either:

- from the explicit `plan_files=...` argument
- or lazily from `.planner.plan_files`

The pipeline calls the planner exactly once per `run_pipeline(...)` invocation.

Behavior:

- planner receives the complete valid `FileRecord` set from the pipeline scan
- planner also receives forwarded positional and keyword arguments unchanged
- planner output is returned unchanged as `PlanResult`

The pipeline does not:

- inspect `PlanResult`
- modify `PlanResult`
- merge `ContextualGrouping` into `PlanResult`

---

## Grouping Interaction

The contextual grouping builder is loaded either:

- from the explicit `build_contextual_grouping=...` argument
- or lazily from an importable builder function

Module resolution order is:

1. `.grouping.build_contextual_grouping`
2. `.contextual_grouping.build_contextual_grouping`

The builder is called exactly once with:

    tuple[FileRecord, ...]

Rules:

- grouping is computed from the complete valid record set of the pipeline scan
- grouping is returned separately
- grouping does not affect planner invocation or planner output

---

## Ordering and Independence

Execution order in the current implementation is:

1. scan
2. grouping
3. planning

This execution order is explicit and mandatory.

Rules:

- contextual grouping is computed before planner invocation
- planner must not depend on contextual grouping output
- contextual grouping builder must not depend on planner output
- contextual grouping is not embedded into `PlanResult`
- contextual grouping is returned as a separate structural result

This independence is a required contract of the current implementation.

---

## Double-Scan Behavior

Current runtime behavior includes two scans during normal CLI execution:

### First scan

Performed in `cli.py` to derive `CorruptFile` from scanner diagnostics.

### Second scan

Performed inside `run_pipeline(...)` to obtain the valid `FileRecord` set used for grouping and planning.

This means the pipeline is not the sole owner of scanning in end-to-end execution.

The pipeline owns the scan used for planning and grouping.
The CLI owns the scan used for corrupt-file derivation.

This is current implementation behavior and must be documented explicitly.

The two scans must produce identical valid `FileRecord` sets for the same input directory and filesystem state.

Rules:

- no divergence between CLI scan results and pipeline scan results is allowed
- corrupt-file derivation in CLI must remain consistent with the valid-file set used by the pipeline
- the existence of two scans must not introduce nondeterministic planning behavior

---

## Dependency Loading Behavior

The pipeline uses lazy imports for planner and grouping integration.

### Planner loading

If `plan_files` is not provided explicitly, the pipeline imports:

    .planner.plan_files

If import fails, `RuntimeError` is raised.

### Grouping builder loading

If `build_contextual_grouping` is not provided explicitly, the pipeline attempts to import:

- `.grouping.build_contextual_grouping`
- `.contextual_grouping.build_contextual_grouping`

If neither is available, `RuntimeError` is raised.

This makes the pipeline the integration point for planner and grouping composition while allowing explicit injection for testing or staged integration.

---

## Determinism Guarantees

The pipeline layer must preserve deterministic behavior.

For identical inputs and identical injected planner/grouping functions, it must produce identical:

- planner invocation inputs
- grouping invocation inputs
- `PlanResult`
- `ContextualGrouping`

The pipeline layer must not introduce:

- randomness
- hidden state
- implicit transformations
- environment-dependent branching

Determinism of outputs depends on the determinism of:

- scanner
- planner
- grouping builder

The pipeline must preserve that determinism by forwarding inputs unchanged and invoking components in fixed order.

---

## Error Boundary

The pipeline does not absorb or reinterpret integration failures.

Failures may occur if:

- planner entry point cannot be imported
- contextual grouping builder cannot be imported

In these cases, the pipeline raises `RuntimeError`.

The pipeline does not define recovery or fallback behavior beyond explicit candidate lookup for the grouping builder.

---

## Model Boundary

The pipeline exchanges model-layer objects only at orchestration boundaries.

### Consumed

- `FileRecord` via `ScanResult.records`

### Produced

- `PlanResult`
- `ContextualGrouping`

The pipeline does not define new model objects and does not mutate model objects.

---

## Integration Summary

The pipeline orchestration layer is the composition point between:

- scanner
- planner
- contextual grouping

But not between:

- scanner diagnostics and corrupt-file derivation
- reporting
- filesystem execution

That makes it a partial orchestration layer rather than a complete end-to-end application controller.

---

## Final Contract

`run_pipeline(...)` must:

1. scan the input path
2. obtain the valid `FileRecord` set from scanner output
3. compute contextual grouping exactly once from that valid record set
4. invoke the planner exactly once with that valid record set and forwarded arguments
5. return:
   - `PlanResult`
   - `ContextualGrouping`

It must not:

- derive corrupt files
- alter planner semantics
- alter grouping semantics
- merge outputs
- render results
- execute actions
