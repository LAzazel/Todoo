import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.infrastructure.database import Base
from app.presentation.dependencies import get_db

from app.infrastructure.orm.models import UserORM, TodoORM

SQLITE_TEST_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    _engine = create_engine(SQLITE_TEST_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
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
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


USER_PAYLOAD = {
    "username": "johndoe", "email": "john@example.com",
    "first_name": "John", "last_name": "Doe",
    "password": "secret123", "phone_number": "0501234567"
}


ADMIN_PAYLOAD = {
    "username": "adminuser", "email": "admin@example.com",
    "first_name": "Admin", "last_name": "User",
    "password": "adminpass", "phone_number": "0507654321",
    "role": "admin"
}


TODO_PAYLOAD = {
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": 3
}


def register(client, payload=USER_PAYLOAD):
    return client.post("/auth/register", json=payload)

def auth_headers(client, email, password):
    r = client.post("/auth/login", json={"email": email, "password": password})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}