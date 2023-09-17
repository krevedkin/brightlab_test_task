import typing

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.auth.models import User
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.task import exceptions as exc
from app.task.models import CeleryTask, Task, TaskUser


class TaskDAO(BaseDAO):
    model = Task

    @classmethod
    async def get_all_tasks_with_users(cls) -> typing.Sequence[Task]:
        async with async_session_maker() as session:
            stmt = select(cls.model).options(
                selectinload(cls.model.users).load_only(User.id, User.email)
            )

            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def get_task_with_users(cls, task_id: int) -> Task | None:
        async with async_session_maker() as session:
            stmt = (
                select(cls.model)
                .options(selectinload(cls.model.users).load_only(User.id, User.email))
                .where(cls.model.id == task_id)
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()


class TaskUserDAO(BaseDAO):
    model = TaskUser

    @classmethod
    async def insert_record(cls, task_id: int, user_id: int):
        try:
            return await super().insert_record(task_id=task_id, user_id=user_id)
        except IntegrityError as e:
            match e.orig.pgcode:  # type: ignore
                case "23505":
                    raise exc.UserAlreadyAddedToTaskDatabaseError
                case "23503":
                    raise exc.CantAddUserToTaskDatabaseError


class CeleryTaskDAO(BaseDAO):
    model = CeleryTask
