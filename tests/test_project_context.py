from aegis40.project_context import DEFAULT_CONTEXT


def test_context_basics() -> None:
    assert DEFAULT_CONTEXT.project_name == "Aegis-40 iPWR"
    assert DEFAULT_CONTEXT.nominal_power_mwe == 40.0
    assert "3S-by-design" in DEFAULT_CONTEXT.design_principles
