import pytest


@pytest.fixture
def context() -> dict:
    # Shared mutable context for BDD steps
    return {}
