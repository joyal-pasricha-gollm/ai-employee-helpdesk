"""Role-based access control dependencies.

Usage in any route:
    current_user: User = Depends(require_support_staff)   # support staff only
    current_user: User = Depends(require_employee)        # employees only
    current_user: User = Depends(get_current_user)        # any logged-in user
"""

import logging
from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import ROLE_EMPLOYEE, ROLE_SUPPORT_STAFF

logger = logging.getLogger(__name__)


def require_roles(*allowed_roles: str) -> Callable[..., User]:
    """Build a dependency that allows only the given roles (others get 403)."""

    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            logger.warning(
                "Forbidden: user_id=%s role=%s needs one of %s",
                current_user.id,
                current_user.role,
                allowed_roles,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user

    return checker


require_employee = require_roles(ROLE_EMPLOYEE)
require_support_staff = require_roles(ROLE_SUPPORT_STAFF)
