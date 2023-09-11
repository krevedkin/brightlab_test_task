from sqlalchemy import delete, insert, select

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def get_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(  # type: ignore
                **filter_by
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def insert_record(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)  # type: ignore
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def delete_record(cls, **filter_by):
        async with async_session_maker() as session:
            stmt = delete(cls.model).filter_by(**filter_by)  # type: ignore
            await session.execute(stmt)
            await session.commit()
