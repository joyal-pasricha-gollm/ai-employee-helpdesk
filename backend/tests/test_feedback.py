"""Tests for AI feedback: who can give it, duplicates, and the support feedback view.

Every test runs in a database transaction that is rolled back afterwards.
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import engine, get_db
from app.main import app
from app.models.ai_suggestion import AISuggestion
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.ai import SUGGESTION_PENDING
from app.schemas.user import ROLE_EMPLOYEE, ROLE_SUPPORT_STAFF
from app.utils.security import create_access_token, hash_password

TEST_SECRET = "test-secret-key-that-is-long-enough-for-hs256"


@pytest.fixture(autouse=True)
def test_settings(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
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
    app.dependency_overrides[get_db] = lambda: db_session
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def make_user(db: Session, email: str, role: str) -> User:
    user = User(full_name=email.split("@")[0], email=email, password_hash=hash_password("StrongPass123"), role=role)
    db.add(user)
    db.flush()
    return user


def auth(user: User) -> dict[str, str]:
    return {"Authorization": f"Bearer {create_access_token(user.id, user.role)}"}


@pytest.fixture
def people(db_session: Session) -> dict[str, User]:
    return {
        "owner": make_user(db_session, "pytest.fb.owner@example.com", ROLE_EMPLOYEE),
        "other": make_user(db_session, "pytest.fb.other@example.com", ROLE_EMPLOYEE),
        "staff": make_user(db_session, "pytest.fb.staff@example.com", ROLE_SUPPORT_STAFF),
    }


@pytest.fixture
def suggestion(db_session: Session, people: dict[str, User]) -> AISuggestion:
    ticket = Ticket(
        subject="File share down",
        description="The whole finance department cannot open the shared drive.",
        requester_id=people["owner"].id,
        category="Network",
        priority="High",
        status="New",
    )
    db_session.add(ticket)
    db_session.flush()
    item = AISuggestion(
        ticket_id=ticket.id,
        suggested_category="Network",
        suggested_priority="Critical",
        summary="Department-wide file share outage.",
        explanation="Many users are blocked.",
        suggested_response="We are investigating the outage.",
        troubleshooting_steps=["Check the file server", "Check network shares"],
        confidence=0.9,
        model_name="qwen2.5:3b",
        status=SUGGESTION_PENDING,
    )
    db_session.add(item)
    db_session.flush()
    return item


def give(client: TestClient, suggestion_id: int, user: User, body: dict):
    return client.post(f"/api/ai-suggestions/{suggestion_id}/feedback", json=body, headers=auth(user))


def test_ticket_owner_gives_feedback_with_comment(client: TestClient, suggestion: AISuggestion, people: dict[str, User]) -> None:
    response = give(client, suggestion.id, people["owner"], {"is_helpful": True, "feedback_comment": "  Fixed it!  "})
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["employee_id"] == people["owner"].id
    assert body["is_helpful"] is True
    assert body["feedback_comment"] == "Fixed it!"
    assert body["created_at"] is not None


def test_support_staff_can_give_feedback(client: TestClient, suggestion: AISuggestion, people: dict[str, User]) -> None:
    response = give(client, suggestion.id, people["staff"], {"is_helpful": False, "feedback_comment": "   "})
    assert response.status_code == 201, response.text
    assert response.json()["feedback_comment"] is None


def test_reject_unauthorized_feedback(client: TestClient, suggestion: AISuggestion, people: dict[str, User]) -> None:
    assert give(client, suggestion.id, people["other"], {"is_helpful": True}).status_code == 404
    assert client.post(f"/api/ai-suggestions/{suggestion.id}/feedback", json={"is_helpful": True}).status_code == 401
    assert give(client, 999999999, people["owner"], {"is_helpful": True}).status_code == 404
    assert give(client, suggestion.id, people["owner"], {}).status_code == 422


def test_one_feedback_per_user_per_suggestion(client: TestClient, suggestion: AISuggestion, people: dict[str, User]) -> None:
    assert give(client, suggestion.id, people["owner"], {"is_helpful": True}).status_code == 201
    assert give(client, suggestion.id, people["owner"], {"is_helpful": False}).status_code == 409


def test_support_staff_views_feedback_with_helpful_percentage(
    client: TestClient, suggestion: AISuggestion, people: dict[str, User]
) -> None:
    give(client, suggestion.id, people["owner"], {"is_helpful": True})
    give(client, suggestion.id, people["staff"], {"is_helpful": False})
    response = client.get("/api/ai-feedback", headers=auth(people["staff"]))
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["total"] >= 2
    assert body["helpful_count"] + body["not_helpful_count"] == body["total"]
    assert 0 <= body["helpful_percentage"] <= 100
    mine = [item for item in body["items"] if item["suggestion_id"] == suggestion.id]
    assert {item["given_by_role"] for item in mine} == {ROLE_EMPLOYEE, ROLE_SUPPORT_STAFF}
    assert mine[0]["ticket_subject"] == "File share down"
    assert mine[0]["suggested_priority"] == "Critical"


def test_employee_cannot_view_feedback_list(client: TestClient, people: dict[str, User]) -> None:
    assert client.get("/api/ai-feedback", headers=auth(people["owner"])).status_code == 403
