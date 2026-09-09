from unittest.mock import AsyncMock

import pytest

from main import app, get_anthropic_client, get_redis_client


@pytest.fixture(autouse=True)
def override_anthropic_client():
    app.dependency_overrides[get_anthropic_client] = lambda: AsyncMock()
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def override_redis_client():
    asyncmock = AsyncMock()
    asyncmock.get.return_value = None
    app.dependency_overrides[get_redis_client] = lambda: asyncmock
    yield
    app.dependency_overrides.clear()

