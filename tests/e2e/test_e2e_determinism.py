from __future__ import annotations

from tests.e2e.helpers import fixture_ids, load_manifest, scenario_outputs


def test_outputs_are_identical_across_repeated_runs() -> None:
    for fixture_id in fixture_ids():
        manifest = load_manifest(fixture_id)
        runs = int(manifest["scenarios"]["determinism_runs"])

        baseline = scenario_outputs(fixture_id=fixture_id)

        for _ in range(runs - 1):
            repeated = scenario_outputs(fixture_id=fixture_id)
            assert repeated == baseline
