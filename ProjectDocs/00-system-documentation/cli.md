# PhotoForge — CLI

## Classification

BOUNDARY

---

## Purpose

The CLI module is the application entrypoint of PhotoForge.

It is responsible for:

- parsing command-line arguments
- validating user-provided paths
- performing the initial scan used for corrupt-file derivation
- deriving `CorruptFile` objects from scanner output
- invoking pipeline orchestration
- selecting report format
- printing the report
- optionally invoking filesystem actions

The CLI does not define scanner, planner, grouping, reporting, or operations behavior.

---

## Primary Entry Point

The CLI entry point is:

    main(argv: list[str] | None = None) -> int

Supporting functions:

- `build_parser() -> argparse.ArgumentParser`
- `validate_input_path(raw_input_path: str) -> Path`
- `validate_output_path(raw_output_path: str) -> Path`

---

## Responsibilities

### Argument Parsing

The CLI defines the following interface:

    photoforge <input_path> [--output <output_path>] [--json] [--apply] [--context]

Supported flags:

- `--output`
- `--json`
- `--apply`
- `--context`

The CLI is responsible for converting raw arguments into validated runtime inputs.

---

### Input Path Validation

`validate_input_path(...)`:

- expands `~`
- checks existence
- checks directory status
- resolves to absolute path

Failure behavior:

- raises `ValueError` if the path does not exist
- raises `ValueError` if the path is not a directory

---

### Output Path Validation

`validate_output_path(...)`:

- expands `~`
- resolves path with `strict=False`
- allows non-existent output directory roots
- rejects existing non-directory paths

Failure behavior:

- raises `ValueError` if resolved output path exists and is not a directory

---

### Initial Scan for Corrupt Derivation

Before invoking the pipeline, the CLI performs an initial scan:

    scan_result = scan_directory(input_path)

This first scan is used only for corrupt-file derivation.

---

### Corrupt-File Transformation

The CLI derives `CorruptFile` from scanner skip results.

Transformation rule:

- iterate over `scan_result.skipped`
- include only entries where `reason.startswith("corrupt_")`
- map:
  - `CorruptFile.path = SkippedFile.path`
  - `CorruptFile.error_type = SkippedFile.reason`

Important:

- `ScanIssue` is not used in this transformation
- this transformation is the only runtime conversion from scanner diagnostics into planner-layer corrupt-file objects

---

### Pipeline Invocation

The CLI invokes:

    run_pipeline(
        input_path,
        output_path=output_path,
        corrupt_files=corrupt_files,
    )

This means:

- `input_path` is passed into the pipeline
- `output_path` is forwarded to the planner through the pipeline
- `corrupt_files` is forwarded to the planner through the pipeline

The CLI does not perform planning directly.

---

### Report Selection and Rendering

The CLI selects report mode based on `--json`.

If `--json` is enabled:

- use `render_json_report(...)`

Otherwise:

- use `render_console_report(...)`

In both modes:

- `PlanResult` is passed in
- `ContextualGrouping` is passed in
- `include_context=args.context`

The CLI controls whether contextual grouping is included in rendered output through the `--context` flag.

---

### Output Ordering

The CLI must always print the report before any filesystem changes occur.

This ordering is explicit and mandatory.

---

### Apply Behavior

If `--apply` is enabled:

- call `apply_actions(plan_result.actions)`

If `--apply` is not enabled:

- no filesystem actions are executed

The CLI does not inspect or reinterpret action semantics.

---

## End-to-End Flow

Current CLI runtime flow is:

1. parse arguments
2. validate input path
3. validate output path if provided
4. scan input directory
5. derive corrupt files from skipped corrupt entries
6. invoke `run_pipeline(...)`
7. render report
8. print report
9. optionally execute actions

This means normal CLI execution performs two scans:

- first scan in CLI for corrupt-file derivation
- second scan inside `run_pipeline(...)` for planning and grouping

Determinism requirement:

- for the same input directory and filesystem state, the CLI scan and the pipeline scan must produce identical valid `FileRecord` sets
- no divergence between the two scans is allowed

---

## Inputs

The CLI consumes:

- raw command-line arguments
- filesystem paths
- scanner output
- pipeline output

---

## Outputs

The CLI produces:

- printed report text
- optional filesystem changes through operations
- integer process exit code

Current success return value:

    0

---

## Determinism Constraints

The CLI must preserve deterministic behavior by:

- validating paths explicitly
- deriving corrupt files using explicit prefix rules
- selecting report mode only from explicit flags
- printing before applying actions
- not introducing hidden transformations

The CLI must not introduce:

- randomness
- implicit fallback behavior
- environment-dependent branching unrelated to explicit filesystem state

---

## Non-Responsibilities

The CLI must not:

- define scanner classification rules
- define timestamp extraction rules
- define hashing behavior
- define planning rules
- define grouping rules
- define report formatting internals
- define filesystem action semantics

---

## Final Contract

The CLI is the application boundary of PhotoForge.

It must:

1. parse and validate user input
2. derive `CorruptFile` from scanner diagnostics
3. invoke the pipeline with explicit planner arguments
4. render output
5. print output before any filesystem changes
6. optionally invoke operations when `--apply` is enabled

It is a boundary/orchestration module only.
