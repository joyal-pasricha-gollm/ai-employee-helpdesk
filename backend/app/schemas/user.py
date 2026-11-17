"""User request and response schemas.

Field names match the users table exactly: id, full_name, email,
password_hash, role, created_at, updated_at.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

# Allowed values for users.role. Import these instead of typing the strings.
ROLE_EMPLOYEE = "employee"
ROLE_SUPPORT_STAFF = "support_staff"
UserRole = Literal["employee", "support_staff"]


class UserResponse(BaseModel):
    """Public view of a user. Never includes password_hash."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    role: UserRole
    created_at: datetime | None = None
    updated_at: datetime | None = None
