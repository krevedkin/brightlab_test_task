from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("")

async_sesson_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    ...
