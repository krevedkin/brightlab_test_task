import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dao import RefreshSessionsDAO, UsersDAO
from app.auth.models import RefreshSessions, User


@pytest.mark.parametrize(
    ("email", "result"),
    [
        ("user@example.com", User),
        ("nouser@example.com", None),
    ],
)
async def test_get_user_by_email(email, result):
    user = await UsersDAO().get_by_email(email)

    if user:
        assert isinstance(user, result)
    else:
        assert user is None


async def test_add_refresh_token(session: AsyncSession):
    user_id = 2
    token = uuid.uuid4()
    expire = datetime.now(timezone.utc)

    await RefreshSessionsDAO().add_refresh_token(user_id, token, expire)

    query = select(RefreshSessions).where(
        RefreshSessions.user_id == user_id,
    )

    result = await session.execute(query)
    result = result.scalar_one_or_none()

    assert result is not None
    assert result.user_id == user_id
    assert result.refresh_token == token
    assert result.expire == expire

    refresh_session = await RefreshSessionsDAO().get_refresh_session(token)
    assert refresh_session is not None
    assert refresh_session.refresh_token == result.refresh_token
