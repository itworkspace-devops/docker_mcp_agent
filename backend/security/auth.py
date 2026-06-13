import base64
import hashlib
import hmac
from contextvars import ContextVar
from datetime import datetime, timedelta

from fastapi import Header, HTTPException

from backend.config.settings import (
    settings
)
from backend.database.repository import (
    get_user_by_username
)

_current_user = ContextVar("current_user", default=None)


def hash_password(password: str) -> str:

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:

    return hash_password(password) == password_hash


def create_access_token(
    username: str,
    role: str,
    expires_minutes: int = 1440,
) -> str:

    expires_at = int(
        (datetime.utcnow() + timedelta(minutes=expires_minutes))
        .timestamp()
    )

    payload = f"{username}|{role}|{expires_at}"
    signature = hmac.new(
        settings.secret_key.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    token = f"{payload}|{signature}"

    return base64.urlsafe_b64encode(
        token.encode("utf-8")
    ).decode("utf-8")


def verify_access_token(token: str):

    try:
        decoded = base64.urlsafe_b64decode(
            token.encode("utf-8")
        ).decode("utf-8")
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization token",
        )

    parts = decoded.split("|")

    if len(parts) != 4:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization token format",
        )

    username, role, expires_at_str, signature = parts

    expected_payload = f"{username}|{role}|{expires_at_str}"
    expected_signature = hmac.new(
        settings.secret_key.encode("utf-8"),
        expected_payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization token signature",
        )

    if int(expires_at_str) < int(datetime.utcnow().timestamp()):
        raise HTTPException(
            status_code=401,
            detail="Authorization token expired",
        )

    user = get_user_by_username(username)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found for token",
        )

    return {
        "username": user.username,
        "role": user.role,
        "password_changed": bool(getattr(user, "password_changed", False)),
    }


def set_current_user(user):

    _current_user.set(user)


def clear_current_user():

    _current_user.set(None)


def get_current_role():

    current = _current_user.get()

    if not current:
        return "viewer"

    return current.get("role", "viewer")


def parse_authorization_header(
    authorization: str | None,
) -> str:

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authorization header must use Bearer token",
        )

    return authorization.split(" ", 1)[1]


async def get_current_user(
    authorization: str | None = Header(None, alias="Authorization")
):

    token = parse_authorization_header(authorization)

    return verify_access_token(token)


def authenticate_user(
    username: str,
    password: str,
):

    user = get_user_by_username(username)

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def is_password_change_required(user) -> bool:

    if user.username == "admin":
        return verify_password("admin", user.password_hash)

    return False
