"""Admin tool: create a user, or reset an existing user's password.

Support staff cannot sign up through the API, so use this script to create
them. It also replaces placeholder password_hash values with a real Argon2 hash.
The password is typed at a hidden prompt and never stored in plain text.

Run from the backend folder:
    .\\.venv\\Scripts\\python.exe -m scripts.create_user --email arjun@example.com --full-name "Arjun Mehta" --role support_staff
"""

import argparse
import getpass
import sys

from sqlalchemy import func

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import ROLE_EMPLOYEE, ROLE_SUPPORT_STAFF
from app.services.auth_service import get_user_by_email
from app.utils.security import hash_password


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--email", required=True)
    parser.add_argument("--full-name", help="Required when creating a new user")
    parser.add_argument("--role", choices=[ROLE_EMPLOYEE, ROLE_SUPPORT_STAFF], default=ROLE_EMPLOYEE)
    args = parser.parse_args()

    email = args.email.strip().lower()
    password = getpass.getpass("New password (min 8 characters, hidden): ")
    if len(password) < 8 or password != getpass.getpass("Repeat password: "):
        print("Passwords must match and be at least 8 characters.")
        return 1

    db = SessionLocal()
    try:
        user = get_user_by_email(db, email)
        if user is None:
            if not args.full_name:
                print("--full-name is required to create a new user.")
                return 1
            user = User(full_name=args.full_name.strip(), email=email, role=args.role,
                        password_hash=hash_password(password),
                        created_at=func.now(), updated_at=func.now())
            db.add(user)
            action = "Created"
        else:
            user.password_hash = hash_password(password)
            user.updated_at = func.now()
            action = "Updated password for"
        db.commit()
        db.refresh(user)
        print(f"{action} user id={user.id} email={user.email} role={user.role}")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
