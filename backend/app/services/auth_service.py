"""Authentication business logic: employee registration and login."""

import logging

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.user import ROLE_EMPLOYEE
from app.utils.security import hash_password, verify_dummy_password, verify_password

logger = logging.getLogger(__name__)


class EmailAlreadyRegisteredError(Exception):
    """Raised when registering an email that already exists in users."""


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalars(select(User).where(User.email == email.strip().lower())).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def register_employee(db: Session, data: RegisterRequest) -> User:
    """Create a new employee account. Support staff are never created here."""
    if get_user_by_email(db, data.email) is not None:
        raise EmailAlreadyRegisteredError

    user = User(
        full_name=data.full_name,
        email=data.email,
        password_hash=hash_password(data.password),
        role=ROLE_EMPLOYEE,
        # Set by the database clock; the model has no default, so without
        # these SQLAlchemy would save NULL.
        created_at=func.now(),
        updated_at=func.now(),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as error:  # two sign-ups with the same email at once
        db.rollback()
        raise EmailAlreadyRegisteredError from error
    db.refresh(user)
    logger.info("Employee registered: user_id=%s", user.id)
    return user


def authenticate_user(db: Session, data: LoginRequest) -> User | None:
    """Return the user if the email and password match, otherwise None."""
    user = get_user_by_email(db, data.email)
    if user is None:
        verify_dummy_password(data.password)
        logger.warning("Login failed: unknown account")
        return None
    if not verify_password(data.password, user.password_hash):
        logger.warning("Login failed: wrong password for user_id=%s", user.id)
        return None
    logger.info("Login succeeded: user_id=%s role=%s", user.id, user.role)
    return user
