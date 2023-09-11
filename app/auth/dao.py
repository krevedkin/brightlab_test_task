from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.auth.models import RefreshSessions, User
from app.dao.base import BaseDAO
from app.database import async_session_maker


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def add_user(cls, **data):
        await super(UsersDAO, cls).insert_record(**data)

    @classmethod
    async def get_by_email(cls, email: str):
        async with async_session_maker() as session:
            query = select(User).where(User.email == email)
            result = await session.execute(query)
            return result.scalar_one_or_none()


class RefreshSessionsDAO(BaseDAO):
    model = RefreshSessions

    @classmethod
    async def add_refresh_token(cls, user_id: int, token: UUID, expire: datetime):
        """Создает запись в БД о refresh сессии для id пользователя
        либо обновляет запись если такая уже есть

        Args:
            user_id (int): Идентификатор пользователя
            token (UUID): refresh токен
            expire (int): время жизни токена
        """
        async with async_session_maker() as session:
            stmt = (
                insert(RefreshSessions)
                .values(
                    user_id=user_id,
                    refresh_token=token,
                    expire=expire,
                )
                .on_conflict_do_update(
                    constraint="refresh_sessions_user_id_key",
                    set_=dict(refresh_token=token, expire=expire, user_id=user_id),
                )
            )

            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get_refresh_session(
        cls,
        refresh_token: UUID,
    ) -> RefreshSessions | None:
        async with async_session_maker() as session:
            query = select(RefreshSessions).where(
                RefreshSessions.refresh_token == refresh_token
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()