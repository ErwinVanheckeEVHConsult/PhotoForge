from __future__ import annotations

from tests.e2e.helpers import assert_exact_match, fixture_ids, golden_dir, scenario_outputs


def test_default_outputs_match_golden() -> None:
    for fixture_id in fixture_ids():
        outputs = scenario_outputs(fixture_id=fixture_id)
        expected_dir = golden_dir(fixture_id)

        assert_exact_match(
            actual=outputs["default.console.txt"],
            expected_path=expected_dir / "default.console.txt",
        )
        assert_exact_match(
            actual=outputs["default.json"],
            expected_path=expected_dir / "default.json",
        )
