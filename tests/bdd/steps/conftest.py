from typing import Dict

import pytest


@pytest.fixture
def context() -> Dict:
    # Shared mutable context for BDD steps
    return {}
