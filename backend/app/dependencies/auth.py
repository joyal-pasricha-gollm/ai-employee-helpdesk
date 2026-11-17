"""Authentication dependency: turns the Bearer token into the logged-in User.

Usage in any route:
    current_user: User = Depends(get_current_user)
"""

import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.auth_service import get_user_by_id
from app.utils.security import InvalidTokenError, decode_access_token

logger = logging.getLogger(__name__)

# auto_error=False so we can always answer 401 (not 403) when the token is missing.
bearer_scheme = HTTPBearer(auto_error=False, description="Paste the access_token from /api/auth/login")


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Return the user who owns the token, or respond 401."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise _unauthorized("Not authenticated")

    try:
        user_id = decode_access_token(credentials.credentials)
    except InvalidTokenError:
        logger.warning("Rejected request with invalid or expired token")
        raise _unauthorized("Invalid or expired token")

    user = get_user_by_id(db, user_id)
    if user is None:
        logger.warning("Rejected token for missing user_id=%s", user_id)
        raise _unauthorized("User no longer exists")
    return user
