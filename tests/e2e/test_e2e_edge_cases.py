from __future__ import annotations

from tests.e2e.helpers import scenario_outputs


def test_empty_fixture_executes_without_crashing() -> None:
    outputs = scenario_outputs(fixture_id="empty")

    assert "default.console.txt" in outputs
    assert "default.json" in outputs
    assert "context.console.txt" in outputs
    assert "context.json" in outputs
    assert "models.json" in outputs
