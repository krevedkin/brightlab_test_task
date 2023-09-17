import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy import text

from app.auth.models import User  # noqa: F401
from app.task.models import Task, TaskUser, CeleryTask  # noqa: F401
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app


@pytest.fixture(autouse=True, scope="function")
async def prepare_database():
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        def read_sql_file(file_name: str):
            with open(f"tests/mock_data/{file_name}.sql") as f:
                return f.read()

        sql_files = ("users_mock", "tasks_mock", "task_users_mock")

        for file in sql_files:
            query = text(read_sql_file(file))
            await conn.execute(query)


@pytest.fixture(scope="session")
def event_loop(request):
    """
    Взято из документации pytest
    Create an instance of the default event loop
    for each test case
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
async def auth_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        response = await client.post(
            "/auth/token",
            data={
                "username": "user@example.com",
                "password": "string",
            },
        )

        token = response.json().get("access_token")
        client.headers["Authorization"] = f"Bearer {token}"
        yield client
