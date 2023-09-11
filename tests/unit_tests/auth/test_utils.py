import pytest

from app.auth.models import User
from app.auth.schemas import RefreshToken
from app.auth.utils import (authenticate_user, create_access_token,
                            create_refresh_token, get_password_hash, get_user,
                            verify_password)


@pytest.mark.parametrize(
    ("password", "hashed_password", "result"),
    [
        (
            "string",
            "$2b$12$AH9QUNC3ThhI7REDWedAq.eraz1tG7jq0H8nSQrTzt/mxyAKb.QvC",
            True,
        ),
        (
            "wrong_password",
            "$2b$12$AH9QUNC3ThhI7REDWedAq.eraz1tG7jq0H8nSQrTzt/mxyAKb.QvC",
            False,
        ),
    ],
)
def test_verify_password(password, hashed_password, result):
    assert verify_password(password, hashed_password) is result


def test_get_password_hash():
    assert isinstance(get_password_hash("secret"), str)


def test_create_access_token():
    token = create_access_token(data={"user": "user"})
    assert isinstance(token, str)


@pytest.mark.parametrize(
    ("email", "result"),
    [
        ("user@example.com", User),
    ],
)
async def test_get_user(email, result):
    user = await get_user(email)
    if user:
        assert isinstance(user, result)
        assert user.email == email


@pytest.mark.parametrize(
    ("email", "password", "result"),
    [
        ("user@example.com", "string", User),
        ("user1@example.com", "string", False),
        ("user@example.com", "wrong_password", False),
    ],
)
async def test_authenticate_user(email, password, result):
    user = await authenticate_user(email, password)

    if user:
        assert isinstance(user, User)
    if not user:
        assert user is result


async def test_create_refresh_token():
    token = create_refresh_token()
    assert isinstance(token, RefreshToken)
