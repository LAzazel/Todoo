import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from ..app.main import app
from ..app.dependencies import get_db
from ..app.auth import get_current_user


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def client(mock_db):
    def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def set_current_user():
    def _set(user_data):
        def override_get_current_user():
            return user_data

        app.dependency_overrides[get_current_user] = override_get_current_user

    return _set

