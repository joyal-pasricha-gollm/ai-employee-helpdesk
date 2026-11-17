"""Authentication request and response schemas."""

import re

from pydantic import BaseModel, Field, field_validator

from app.schemas.user import UserResponse

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _normalize_email(value: str) -> str:
    email = value.strip().lower()
    if not _EMAIL_PATTERN.match(email):
        raise ValueError("Enter a valid email address")
    return email


class RegisterRequest(BaseModel):
    """Public employee sign-up. The role is always employee; it cannot be chosen."""

    full_name: str = Field(min_length=1, max_length=100, examples=["Priya Sharma"])
    email: str = Field(max_length=150, examples=["priya@example.com"])
    password: str = Field(min_length=8, max_length=128, examples=["StrongPass123"])

    @field_validator("full_name")
    @classmethod
    def full_name_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Full name is required")
        return value

    @field_validator("email")
    @classmethod
    def email_valid(cls, value: str) -> str:
        return _normalize_email(value)


class LoginRequest(BaseModel):
    email: str = Field(max_length=150, examples=["priya@example.com"])
    password: str = Field(min_length=1, max_length=128, examples=["StrongPass123"])

    @field_validator("email")
    @classmethod
    def email_valid(cls, value: str) -> str:
        return _normalize_email(value)


class TokenResponse(BaseModel):
    """Returned after login. The frontend uses user.role to pick the portal."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse
