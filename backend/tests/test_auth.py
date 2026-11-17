"""Tests for authentication and authorization behavior.

API tests run inside a database transaction that is rolled back afterwards,
so nothing is saved to the real database.
"""

from collections.abc import Generator

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import engine, get_db
from app.dependencies.permissions import require_employee, require_support_staff
from app.main import app
from app.models.user import User
from app.schemas.user import ROLE_SUPPORT_STAFF
from app.utils.security import (
    InvalidTokenError,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

TEST_SECRET = "test-secret-key-that-is-long-enough-for-hs256"
PASSWORD = "StrongPass123"


@pytest.fixture(autouse=True)
def test_secret_key(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    monkeypatch.setenv("SECRET_KEY", TEST_SECRET)
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    # A small extra router to prove role checks work on any protected route.
    @app.get("/test-only/support")
    def support_only(user: User = Depends(require_support_staff)) -> dict[str, str]:
        return {"role": user.role}

    @app.get("/test-only/employee")
    def employee_only(user: User = Depends(require_employee)) -> dict[str, str]:
        return {"role": user.role}

    app.dependency_overrides[get_db] = lambda: db_session
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        app.router.routes[:] = [r for r in app.router.routes if not getattr(r, "path", "").startswith("/test-only")]


def register(client: TestClient, email: str = "pytest.employee@example.com") -> dict:
    response = client.post(
        "/api/auth/register",
        json={"full_name": "Pytest Employee", "email": email, "password": PASSWORD},
    )
    assert response.status_code == 201, response.text
    return response.json()


def login(client: TestClient, email: str, password: str = PASSWORD):
    return client.post("/api/auth/login", json={"email": email, "password": password})


# ---------- unit tests (no database) ----------

def test_password_is_hashed_with_argon2() -> None:
    password_hash = hash_password(PASSWORD)
    assert password_hash != PASSWORD
    assert password_hash.startswith("$argon2")
    assert verify_password(PASSWORD, password_hash)
    assert not verify_password("WrongPass123", password_hash)


def test_placeholder_hash_never_matches() -> None:
    assert not verify_password(PASSWORD, "TEMP_HASH_1")


def test_token_round_trip_and_tampering() -> None:
    token = create_access_token(user_id=42, role="employee")
    assert decode_access_token(token) == 42
    with pytest.raises(InvalidTokenError):
        decode_access_token(token + "x")


# ---------- API tests (rolled-back database transaction) ----------

def test_register_creates_employee_without_password_hash(client: TestClient) -> None:
    body = register(client, "Pytest.Upper@Example.com")
    assert body["role"] == "employee"
    assert body["email"] == "pytest.upper@example.com"
    assert "password_hash" not in body
    assert body["created_at"] is not None
    assert body["updated_at"] is not None


def test_register_duplicate_email_returns_409(client: TestClient) -> None:
    register(client)
    response = client.post(
        "/api/auth/register",
        json={"full_name": "Again", "email": "pytest.employee@example.com", "password": PASSWORD},
    )
    assert response.status_code == 409


def test_register_cannot_choose_role(client: TestClient) -> None:
    response = client.post(
        "/api/auth/register",
        json={"full_name": "Sneaky", "email": "pytest.sneaky@example.com",
              "password": PASSWORD, "role": "support_staff"},
    )
    assert response.status_code == 201
    assert response.json()["role"] == "employee"


def test_register_invalid_input_returns_422(client: TestClient) -> None:
    response = client.post(
        "/api/auth/register", json={"full_name": "", "email": "not-an-email", "password": "short"}
    )
    assert response.status_code == 422


def test_valid_login_returns_token_and_user(client: TestClient) -> None:
    register(client)
    response = login(client, "pytest.employee@example.com")
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["user"]["role"] == "employee"
    assert body["access_token"]


def test_wrong_password_returns_401(client: TestClient) -> None:
    register(client)
    assert login(client, "pytest.employee@example.com", "WrongPass123").status_code == 401


def test_unknown_email_returns_401(client: TestClient) -> None:
    assert login(client, "pytest.nobody@example.com").status_code == 401


def test_missing_credentials_returns_422(client: TestClient) -> None:
    assert client.post("/api/auth/login", json={}).status_code == 422


def test_me_requires_token(client: TestClient) -> None:
    assert client.get("/api/auth/me").status_code == 401


def test_me_rejects_invalid_token(client: TestClient) -> None:
    response = client.get("/api/auth/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert response.status_code == 401


def test_me_returns_logged_in_user(client: TestClient) -> None:
    register(client)
    token = login(client, "pytest.employee@example.com").json()["access_token"]
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "pytest.employee@example.com"


def test_employee_cannot_access_support_route(client: TestClient) -> None:
    register(client)
    token = login(client, "pytest.employee@example.com").json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    assert client.get("/test-only/support", headers=headers).status_code == 403
    assert client.get("/test-only/employee", headers=headers).status_code == 200


def test_support_staff_can_access_support_route(client: TestClient, db_session: Session) -> None:
    staff = User(full_name="Pytest Staff", email="pytest.staff@example.com",
                 password_hash=hash_password(PASSWORD), role=ROLE_SUPPORT_STAFF)
    db_session.add(staff)
    db_session.commit()
    token = login(client, "pytest.staff@example.com").json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    assert client.get("/test-only/support", headers=headers).status_code == 200
    assert client.get("/test-only/employee", headers=headers).status_code == 403
