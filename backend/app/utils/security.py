"""Password hashing (Argon2) and JWT access-token utilities."""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from app.config import SECRET_KEY_PLACEHOLDER, get_settings

password_hasher = PasswordHash((Argon2Hasher(),))

# Used when a login email does not exist, so a failed login takes about the
# same time whether or not the account exists.
_DUMMY_PASSWORD_HASH = password_hasher.hash("dummy-password-for-timing")


class InvalidTokenError(Exception):
    """Raised when a JWT is missing, expired, tampered with, or malformed."""


def hash_password(plain_password: str) -> str:
    """Return an Argon2 hash suitable for the users.password_hash column."""
    return password_hasher.hash(plain_password)


def verify_password(plain_password: str, password_hash: str | None) -> bool:
    """Check a plain password against a stored hash.

    Returns False (never raises) for unknown or malformed hashes, for example
    placeholder values inserted manually into the database.
    """
    if not password_hash:
        password_hasher.verify(plain_password, _DUMMY_PASSWORD_HASH)
        return False
    try:
        return password_hasher.verify(plain_password, password_hash)
    except Exception:
        return False


def verify_dummy_password(plain_password: str) -> None:
    """Spend the same time as a real check when the user does not exist."""
    password_hasher.verify(plain_password, _DUMMY_PASSWORD_HASH)


def _get_signing_key() -> str:
    secret_key = get_settings().secret_key
    if not secret_key or secret_key == SECRET_KEY_PLACEHOLDER or len(secret_key) < 32:
        raise RuntimeError(
            "SECRET_KEY is missing or unsafe. Add a random value of at least "
            "32 characters to backend\\.env (see README)."
        )
    return secret_key


def create_access_token(user_id: int, role: str) -> str:
    """Create a signed JWT that identifies the user and their role."""
    settings = get_settings()
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(payload, _get_signing_key(), algorithm=settings.algorithm)


def decode_access_token(token: str) -> int:
    """Validate a JWT and return the user id stored in it.

    Raises InvalidTokenError if the signature, expiry, or contents are invalid.
    """
    settings = get_settings()
    try:
        payload = jwt.decode(token, _get_signing_key(), algorithms=[settings.algorithm])
    except JWTError as error:
        raise InvalidTokenError("Invalid or expired token") from error

    subject = payload.get("sub")
    if subject is None or not str(subject).isdigit():
        raise InvalidTokenError("Token has no valid subject")
    return int(subject)
