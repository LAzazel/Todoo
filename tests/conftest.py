import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.dependencies import get_db
from app.auth import get_current_user
from app.database import Base

SQLITE_TEST_URL = "sqlite:///./test_integration.db"

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


@pytest.fixture(scope="session")
def engine():
    _engine = create_engine(SQLITE_TEST_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=_engine)
    yield _engine
    Base.metadata.drop_all(bind=_engine)


@pytest.fixture(scope="function")
def db_session(engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    yield session
    
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.close()


@pytest.fixture(scope="function")
def integration_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


USER_PAYLOAD = {
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "secret123",
    "phone_number": "0501234567",
}


ADMIN_PAYLOAD = {
    "username": "adminuser",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User",
    "password": "adminpass",
    "phone_number": "0507654321",
    "role": "admin",
}


TODO_PAYLOAD = {
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": 3,
    "complete": False,
}


def register(integration_client, payload=None):
    payload = payload or USER_PAYLOAD
    return integration_client.post("/auth/", json=payload)

def login(integration_client, username, password):
    return integration_client.post("/auth/token", data={"username": username, "password": password})

def auth_headers(integration_client, username, password):
    r = login(integration_client, username, password)
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
