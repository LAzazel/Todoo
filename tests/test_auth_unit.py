from datetime import timedelta
from unittest.mock import MagicMock

import pytest
from jose import jwt
from fastapi import HTTPException

from app.dependencies import bcrypt_context
from app.auth import authenticate_user, create_access_token, get_current_user
from app.config import SECRET_KEY, ALGORITHM


def test_authenticate_user_returns_user_when_credentials_are_valid():
    db = MagicMock()
    user = MagicMock()
    user.hashed_password = bcrypt_context.hash("secret123")
    db.query.return_value.filter.return_value.first.return_value = user

    result = authenticate_user(db, "john", "secret123")

    assert result == user


def test_authenticate_user_returns_false_when_password_is_invalid():
    db = MagicMock()
    user = MagicMock()
    user.hashed_password = bcrypt_context.hash("secret123")
    db.query.return_value.filter.return_value.first.return_value = user

    result = authenticate_user(db, "john", "wrong-password")

    assert result is False


def test_create_access_token_contains_expected_claims():
    token = create_access_token("john", 7, "admin", timedelta(minutes=5))
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert payload["sub"] == "john"
    assert payload["id"] == 7
    assert payload["role"] == "admin"
    assert "exp" in payload


def test_get_current_user_raises_for_invalid_token():
    with pytest.raises(HTTPException) as exc:
        get_current_user("not-a-real-token")

    assert exc.value.status_code == 401

