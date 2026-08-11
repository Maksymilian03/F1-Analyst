from unittest.mock import AsyncMock

import pytest

from main import app, get_anthropic_client


@pytest.fixture(autouse=True)
def override_anthropic_client():
    app.dependency_overrides[get_anthropic_client] = lambda: AsyncMock()
    yield
    app.dependency_overrides.clear()
